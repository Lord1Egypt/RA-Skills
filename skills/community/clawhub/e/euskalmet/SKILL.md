---
name: euskalmet
description: Tool for obtaining weather forecasts for the Basque Country through the Euskalmet agency. Use when the user wants to know today's weather, temperatures, or the general forecast.
---
# Euskalmet Skill

Specialized tool for retrieving weather forecast data from the Euskalmet (Basque Meteorology Agency) API.

## Usage

Execute both scripts from the skill root directory to fetch and format the weather forecast:

```bash
cd ~/.openclaw/skills/euskalmet
./venv/bin/python3 scripts/main.py && ./venv/bin/python3 scripts/format_forecast.py
```

**Optional:** Pass a username for a personalized greeting:

```bash
./venv/bin/python3 scripts/format_forecast.py --username "Urtzi"
# Output: "Egun on, Urtzi! ✨"

# Without username:
# Output: "Egun on! ✨"
```

You can also set `EUSKALMET_GREETING_NAME` in your `.env` file (not related to API credentials — used only for the greeting):

```bash
EUSKALMET_GREETING_NAME=Urtzi
```

**Important:** Always run both scripts in sequence. The first (`main.py`) downloads the raw JSON forecast data, and the second (`format_forecast.py`) formats it into a human-readable message in Basque.

### Output

The formatted output includes:
- **Current date** in the header (e.g., "Gaur (2026-03-24)")
- **Location name** (e.g., "Laudion")
- **Weather description** with emoji
- **Min/Max temperatures** for today
- **3-day forecast** with weather, emoji, and temperature ranges

Example output:
```
Egun on, Urtzi! ✨

Gaur (2026-03-24) Laudion **Zaparrada txikiak** 🌧️ izango dugu, 11.5 °C maximoarekin eta 5.8 °C minimoarekin.

Hona hemen datozen egunetarako joera:
📅 **Bihar:** Euri txikia 🌧️ | ⬇️ 4.4 °C  ⬆️ 9.1 °C
📅 **Etzi:** Zaparrada txikiak 🌧️ | ⬇️ 3.1 °C  ⬆️ 10.9 °C
📅 **Etzidamu:** Euri txikia 🌧️ | ⬇️ 2.2 °C  ⬆️ 11.5 °C

Egun bikaina izan! 🚀
```

## Files

### Scripts (`scripts/`)
- `main.py` — Downloads the raw JSON forecast from the Euskalmet API and saves it to `forecasts/`
- `format_forecast.py` — Reads the JSON and outputs a formatted Basque-language weather message
- `test_env.py` — Tests that your API credentials are valid
- `download_images.py` — Downloads weather icons from Euskalmet API
- `test_structure.py` — Verifies the skill file structure is correct

### Data
- `forecasts/<location>-euskalmet.json` — Raw JSON data for each location
- `available-locations.json` — List of available locations supported by the API

## Directory Structure

```
euskalmet/
├── SKILL.md                    # This file
├── scripts/
│   ├── main.py                # Main script (downloads forecast data)
│   ├── format_forecast.py     # Formats forecast into human-readable message
│   ├── test_env.py           # Test API credentials
│   ├── download_images.py    # Download weather icons
│   └── test_structure.py      # Verify skill file structure
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API credentials) [not in repo]
├── available-locations.json    # List of available locations
├── venv/                      # Python virtual environment (Python 3.12)
├── forecasts/                 # Generated forecast JSON files
│   └── laudio-euskalmet.json # Example: Laudio/Llodio forecast
├── images/                   # Weather icons (legacy PNG)
└── images-modern/            # Weather icons (modern SVG)
```

## Setup

### 1. Virtual Environment

Create (or recreate) the virtual environment with Python 3.12:

```bash
cd ~/.openclaw/skills/euskalmet
rm -rf venv
python3.12 -m venv venv
./venv/bin/pip install -r requirements.txt
```

**Note:** The venv must use Python 3.12+ for compatibility with the latest dependencies.

### 2. Environment Variables

Configure your `.env` file with your Euskalmet API credentials:

```bash
EUSKALMET_API_EMAIL=your_email@example.com
EUSKALMET_API_PRIVATE_KEY=your_private_key
```

**Optional:** Add a name for a personalized greeting (not related to API credentials):

```bash
EUSKALMET_GREETING_NAME=YourName
```

If not set, the greeting will be "Egun on!" instead of "Egun on, YourName!"

To obtain API credentials, register at: https://www.euskalmet.euskadi.eus/

### 3. Test Setup

Test that your API credentials are correct:

```bash
cd ~/.openclaw/skills/euskalmet
./venv/bin/python3 scripts/test_env.py
```

Verify the skill file structure:

```bash
cd ~/.openclaw/skills/euskalmet
./venv/bin/python3 scripts/test_structure.py
```

## Additional Commands

### Download Forecast for a Location

```bash
./venv/bin/python3 scripts/main.py
```

### Download Available Locations List

```bash
./venv/bin/python3 scripts/main.py --download
```

### List All Available Locations

```bash
./venv/bin/python3 scripts/main.py --locations
```

### Download Weather Icons

```bash
./venv/bin/python3 scripts/download_images.py
```

## Data Retrieved

The skill extracts:
1. **Date** — The date of the forecast (YYYY-MM-DD format)
2. **Location** — The town/location name (e.g., "Laudio")
3. **Weather Description** — Basque-language description (e.g., "Zaparrada txikiak")
4. **Min/Max Temperatures** — Daily temperature range in Celsius
5. **Weather Icons** — Emoji representation of weather conditions

## Weather Conditions (Emoji Mapping)

| Basque Keyword | Emoji |
|---------------|-------|
| oskarbi, eguzki | ☀️ |
| hodei gutxi, hodeitsu, tarteka | 🌤️ |
| hodei, estalia, laino | ☁️ |
| euri, zaparrada, zirimiria | 🌧️ |
| elur | ❄️ |
| ekaitz | ⛈️ |
| (default) | 🌡️ |
