# 🏖️ Beach Safety MCP

Get comprehensive beach and surf conditions for any beach in the world — just say the name. No API keys needed for most data.

> "How's the surf at Waikiki?" → instant full report

⭐ If you find this useful, please star the repo — it helps others discover it.

## What You Get

- 🌊 **Waves** — height, period, direction
- 🌫️ **Swell** — swell height, period, direction
- 💨 **Wind** — speed and direction
- 🌡️ **Temperature** — air and water
- ☀️ **UV Index** — current UV + daily max, day/night aware *(free, no API key)*
- ⚠️ **Rip Current Risk** — Low / Moderate / High
- 🛡️ **Safety Score** — 1-10 with recommendations

## Data Sources (all free — no API keys)

| Source | Data |
|--------|------|
| OpenStreetMap / Photons | Beach name → coordinates |
| Open-Meteo Marine | Wave height, swell, ocean currents |
| Open-Meteo Weather | Air temp, wind, precipitation, UV index |
| NOAA NWS | Rip current risk, surf zone forecast |

UV index data comes from Open-Meteo at no cost — no API key needed.

## Installation

### 1. Clone / copy the project

```bash
git clone <repo-url>
cd beach-safety-mcp
```

Or just copy the `src/server.py` file to wherever you want it.

### 2. Add to mcporter

```bash
mcporter config add beach-safety \
  --command python3 \
  --args "path/to/beach-safety-mcp/src/server.py" \
  --cwd "path/to/beach-safety-mcp/config"
```

### Add to mcporter manually

Or manually add to `~/.openclaw/workspace/config/mcporter.json`:

```json
{
  "beach-safety": {
    "command": "python3",
    "args": ["/full/path/to/beach-safety-mcp/src/server.py"]
  }
}
```

### 3. Test it

```bash
mcporter call beach-safety.get_beach_json beach_name="Waikiki"
```

## Usage

### From any AI assistant (via mcporter)

```
get_beach_report(beach_name="Waikiki")
get_beach_report(beach_name="Bondi Beach, Sydney")
get_beach_report(beach_name="Cocoa Beach, FL")
```

Just say the beach name — coordinates are auto-resolved.

### From the CLI

```bash
python3 beach_lookup.py "Waikiki"
python3 beach_lookup.py "Praia da Rocha, Portugal"
python3 beach_lookup.py "Bondi Beach, Sydney"
```

### Surf forecast only

```bash
mcporter call beach-safety.get_surf_forecast lat=21.27 lon=-157.82
```

## Example Output

```
🌊 Bondi Beach, Sydney Beach Conditions
   Lat/Lon: -33.8907, 151.2724
   Updated: 2026-03-23T10:30:00Z UTC

🛡️ SAFETY (Score: 8/10)
   Rip Current Risk: Moderate
   Safety: Moderate rip current risk

🌊 WAVES
   Wave Height: 2.8 ft (0.84m)
   Wave Period: 6.7 sec
   Swell: 2.4 ft @ 4.8 sec from E

💨 WIND
   Speed: 4.0 mph from NE

🌡️ TEMPERATURE
   Air: 68°F | Water: 75°F

☀️ UV INDEX: current=6 (daily max=9) (Very High) — sunscreen recommended
   *(at night shows current=0 with daily max, UV risk based on max)*

📋 RECOMMENDATIONS:
   ⚠️ Swim near a lifeguard. Be aware of rip currents.
```

## Safety Score Guide

| Score | Meaning | Action |
|-------|---------|--------|
| 9-10 | Generally safe | Enjoy with normal precautions |
| 7-8 | Minor concerns | Caution advised |
| 4-6 | Caution | Swim near lifeguard |
| 1-3 | Dangerous | **Stay out of the water** |

## Notes

- Works for any beach worldwide — just name it
- NOAA surf zone data is most detailed for US coasts
- Open-Meteo marine data covers global oceans
- Some less-famous beaches may not resolve — try adding country/state (e.g., "Kuta Beach, Bali, Indonesia")
- Beach name → coordinates powered by OpenStreetMap + Photons (free)

## Project Structure

```
beach-safety-mcp/
├── src/
│   └── server.py          # MCP server (Python, stdio)
├── beach_lookup.py        # CLI tool
├── LICENSE                # MIT License
└── README.md
```
