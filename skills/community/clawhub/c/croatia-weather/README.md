# croatia-weather

An [OpenClaw](https://github.com/openclaw/openclaw) skill that gives your AI agents comprehensive access to Croatian weather data from **DHMZ** (Državni hidrometeorološki zavod — Croatian Meteorological and Hydrological Service).

**27 commands** covering current conditions, multi-day forecasts, severe weather warnings, agriculture, maritime, hydrology, environment, and 125+ years of climate history — all from official DHMZ XML feeds.

## Features

| Category | Commands | What you get |
|---|---|---|
| **Weather** | `current`, `forecast`, `forecast3`, `outlook`, `regions`, `temp-extremes`, `europe` | Live conditions, 7-day / 3-day / 3-hourly forecasts, regional text forecasts, European capitals |
| **Warnings** | `warnings`, `heatwave`, `coldwave`, `bio` | CAP alerts (3 days), heat/cold wave indicators, biometeorological forecast |
| **Agriculture** | `frost`, `soil`, `agro`, `agro7` | Ground frost (5cm), soil temps (5/10/20cm), weekly agro bulletin, per-station agro data |
| **Water** | `precip`, `snow`, `rivers`, `hydro`, `sea` | Precipitation, snow depth, river temps, flood alerts, Adriatic sea temps |
| **Maritime** | `adriatic`, `maritime` | Nautical forecast, detailed maritime forecast with station tables |
| **Environment** | `uvi`, `fire` | UV index (hourly), forest fire danger (FWI) |
| **Climate** | `climate`, `climate-rain` | 125-year monthly averages, annual precipitation by station |
| **Utility** | `stations`, `full` | Station name lookup, combined weather overview |

## Requirements

- **Python 3.6+** (stdlib only — zero external dependencies)
- **OpenClaw** (any version with skill support)

## Installation

Copy this directory into your OpenClaw agent's skills folder:

```bash
cp -r croatia-weather /path/to/.openclaw/workspaces/<agent>/skills/
```

Or clone directly:

```bash
cd /path/to/.openclaw/workspaces/<agent>/skills/
git clone https://github.com/<your-username>/croatia-weather.git
```

OpenClaw will automatically discover the skill from `SKILL.md`.

## Configuration

### Home Station

By default, commands without a station argument use **Zagreb** as the home station. To set your own home station, configure these environment variables (e.g. in your shell profile or OpenClaw agent env):

| Variable | Purpose | Default |
|---|---|---|
| `DHMZ_HOME_CURRENT` | Station name for current conditions feed | `Zagreb-Grič` |
| `DHMZ_HOME_FORECAST` | Station name for forecast feeds | `Zagreb_Maksimir` |
| `DHMZ_HOME_ALIASES` | Extra words that resolve to home (comma-separated) | _(empty)_ |

**Example** — set Osijek as home:

```bash
export DHMZ_HOME_CURRENT="RC Osijek-Čepin"
export DHMZ_HOME_FORECAST="Osijek"
export DHMZ_HOME_ALIASES="čepin,cepin,osijek"
```

Station names differ between feeds. Run `python3 scripts/dhmz.py stations` to see all available names, or consult `references/stations.md` for a cross-reference table.

### OpenClaw Integration

The `{baseDir}` template variable in `SKILL.md` is automatically resolved by OpenClaw to the skill's directory path. No manual path configuration is needed.

## Usage

### Standalone (without OpenClaw)

```bash
# Current conditions for Zagreb (default home)
python3 scripts/dhmz.py current

# Current conditions for Split
python3 scripts/dhmz.py current Split

# All stations
python3 scripts/dhmz.py current --all

# 7-day forecast
python3 scripts/dhmz.py forecast Dubrovnik

# Active weather warnings
python3 scripts/dhmz.py warnings

# Full overview (current + frost + warnings + forecast + regions + biometeo + hydro)
python3 scripts/dhmz.py full

# Historical climate data
python3 scripts/dhmz.py climate zagreb_maksimir

# List all available commands
python3 scripts/dhmz.py --help
```

### With OpenClaw

Once installed as a skill, your OpenClaw agent will automatically use this skill when the user asks about Croatian weather. The agent reads `SKILL.md` for command documentation and `references/quick-guide.md` for a decision table mapping user questions to the right commands.

## Station Matching

The script uses fuzzy matching — you don't need exact station names:

| You type | Matches |
|---|---|
| `Zagreb` | Zagreb-Grič (current) / Zagreb_Maksimir (forecast) |
| `Split` | Split-Marjan (current) / Split (forecast) |
| `home`, `doma`, `my` | Your configured home station |
| Any partial name | Exact → contains → word match |

## Data Sources

All data comes from DHMZ public XML feeds — **no API key required**. Data is licensed under the [Open Licence of the Republic of Croatia](https://data.gov.hr/open-licence-republic-croatia).

**Attribution required:** Izvor: DHMZ

The full list of feed URLs and their update frequencies is documented in `SKILL.md` and `references/quick-guide.md`.

> **Feed URL reference:** https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici

## Project Structure

```
croatia-weather/
├── SKILL.md                    # OpenClaw skill definition (agent reads this)
├── README.md                   # This file
├── scripts/
│   └── dhmz.py                 # CLI tool (27 commands, Python 3 stdlib only)
└── references/
    ├── stations.md             # Station name cross-reference across feeds
    └── quick-guide.md          # Decision table: user question → command(s)
```

## License

MIT

Data source: **DHMZ** — https://meteo.hr
Data licence: [Open Licence (data.gov.hr)](https://data.gov.hr/open-licence-republic-croatia)
