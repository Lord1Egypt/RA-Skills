import json
import os
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Format Euskalmet forecast")
parser.add_argument("--username", help="Username for greeting")
args = parser.parse_args()

# Get username from env or args (args takes priority)
username = args.username or os.environ.get("EUSKALMET_GREETING_NAME")

json_path = "forecasts/laudio-euskalmet.json"
if not os.path.exists(json_path):
    print("Errorea: Ez da daturik aurkitu.")
    exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ordenatu egunak dataren arabera
trends = sorted(data.get("trendsByDate", []), key=lambda x: x["date"])

# Iragazi gaurko eta etorkizuneko egunak soilik
today_str = datetime.now().strftime("%Y-%m-%d")
future_trends = [t for t in trends if t["date"] >= today_str]

if not future_trends:
    print("Ez dago iragarpenik eskuragarri.")
    exit(0)

def get_emoji(weather_desc):
    desc = weather_desc.lower()
    if "oskarbi" in desc or "eguzki" in desc: return "☀️"
    if "hodei gutxi" in desc or "hodeitsu" in desc or "tarteka" in desc: return "🌤️"
    if "hodei" in desc or "estalia" in desc or "laino" in desc: return "☁️"
    if "euri" in desc or "zaparrada" in desc or "zirimiria" in desc: return "🌧️"
    if "elur" in desc: return "❄️"
    if "ekaitz" in desc: return "⛈️"
    return "🌡️"

# Gaurkoa (zerrendako lehenengoa)
today = future_trends[0]
t_min = today["temperatureRange"]["min"]
t_max = today["temperatureRange"]["max"]
t_desc = today["weather"]["nameByLang"]["BASQUE"]
t_emoji = get_emoji(t_desc)

# Gaurko data formateatu
today_date = datetime.strptime(today["date"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

greeting = f"Egun on, {username}!" if username else "Egun on!"
msg = f"{greeting} ✨\n\n"
msg += f"Gaur ({today_date}) Laudion **{t_desc}** {t_emoji} izango dugu, {t_max} °C maximoarekin eta {t_min} °C minimoarekin.\n\n"
msg += "Hona hemen datozen egunetarako joera:\n"

labels = ["Bihar", "Etzi", "Etzidamu"]
for i in range(1, min(4, len(future_trends))):
    day = future_trends[i]
    d_min = day["temperatureRange"]["min"]
    d_max = day["temperatureRange"]["max"]
    d_desc = day["weather"]["nameByLang"]["BASQUE"]
    d_emoji = get_emoji(d_desc)
    label = labels[i-1] if i-1 < len(labels) else "Hurrengoa"
    msg += f"📅 **{label}:** {d_desc} {d_emoji} | ⬇️ {d_min} °C  ⬆️ {d_max} °C\n"

msg += "\nEgun bikaina izan! 🚀"
print(msg)
