import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_weather(api_key, city, result_text, back_button):
    base_url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # You can change to 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data['main']['temp']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            result_text.insert(tk.END, f'Temperature in {city}: {temperature}°C\n')
            result_text.insert(tk.END, f'Pressure in {city}: {pressure} hPa\n')
            result_text.insert(tk.END, f'Humidity in {city}: {humidity}%\n')
            result_text.insert(tk.END, f'Wind Speed in {city}: {wind_speed} m/s\n')

            # Check soil pH based on temperature, humidity, and pressure
            soil_ph = get_soil_ph(temperature, humidity, pressure)
            result_text.insert(tk.END, f'Estimated Soil pH in {city}: {soil_ph}\n')

            # Check drought risk based on temperature (you can adjust the threshold as needed)
            if temperature > 30:
                result_text.insert(tk.END, f'High risk of drought and famine in {city} due to high temperature.\n')
            else:
                result_text.insert(tk.END, f'No significant risk of drought and famine in {city} based on current conditions.\n')

            # Enable the Back to Results button
            back_button.config(state=tk.NORMAL)

            # Plot the temperature-pressure scatter plot
            plot_scatter(temperature, pressure)

        else:
            messagebox.showerror("Error", f'Error: {data["message"]}')

    except Exception as e:
        messagebox.showerror("Error", f'Error: {str(e)}')

def get_soil_ph(temperature, humidity, pressure):
    # This is a simplified estimation. You may need a more sophisticated model for accurate predictions.
    # Adjust the formula based on your specific requirements.
    soil_ph = 7.0 - 0.1 * temperature + 0.05 * humidity - 0.01 * pressure
    return round(soil_ph, 2)

def check_drought(api_key, city, result_text, back_button):
    result_text.delete(1.0, tk.END)  # Clear previous results
    back_button.config(state=tk.DISABLED)  # Disable the Back to Results button
    get_weather(api_key, city, result_text, back_button)

def reset_results(result_text):
    result_text.delete(1.0, tk.END)  # Clear all results

def plot_scatter(temperature, pressure):
    # Create a scatter plot
    fig, ax = plt.subplots()
    ax.scatter(temperature, pressure, color='blue')
    ax.set_title('Temperature vs Pressure')
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Pressure (hPa)')

    # Display the plot in a Tkinter window
    root = tk.Tk()
    root.title("Temperature vs Pressure")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    back_button = tk.Button(root, text="Back to Results", command=root.destroy)
    back_button.pack()

    root.mainloop()

# GUI setup
def create_gui(api_key):
    root = tk.Tk()
    root.title("Drought Prediction")

    city_label = tk.Label(root, text="Enter city name:")
    city_label.pack()

    city_entry = tk.Entry(root)
    city_entry.pack()

    result_text = tk.Text(root, height=15, width=50)
    result_text.pack()

    check_button = tk.Button(root, text="Check Drought Risk", command=lambda: check_drought(api_key, city_entry.get(), result_text, back_button))
    check_button.pack(side=tk.LEFT)

    reset_button = tk.Button(root, text="Reset", command=lambda: reset_results(result_text), bg='red', fg='white')
    reset_button.pack(side=tk.RIGHT)

    graph_button = tk.Button(root, text="Show Graph", command=lambda: get_weather(api_key, city_entry.get(), result_text, back_button))
    graph_button.pack()

    back_button = tk.Button(root, text="Back to Results", state=tk.DISABLED, command=lambda: result_text.delete(tk.END))
    back_button.pack()

    root.mainloop()

if __name__ == "__main__":
    api_key = 'ab89170292068125915e2d02c73d002b'  # Replace with your actual API key
    create_gui(api_key)

