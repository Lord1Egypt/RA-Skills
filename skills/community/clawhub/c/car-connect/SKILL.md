---
name: car-connect
description: Control multiple car brands (Tesla, Mercedes, Volkswagen, Toyota, Ford, Kia, Honda) from macOS via their official connected APIs. Supports vehicle status, lock/unlock, climate control, charge/fuel, location, tyres, trunk, windows, horn, and more. Use when you want to check or control your car remotely.
metadata:
{
  "openclaw": {
    "emoji": "🚗",
    "os": ["darwin", "linux"],
    "requires": {
      "bins": ["python3"],
      "packages": ["teslapy", "hyundai_kia_connect_api", "pymyhondaplus"],
      "env": {
        "tesla": ["TESLA_EMAIL"],
        "mercedes": ["MERCEDES_EMAIL", "MERCEDES_PASSWORD"],
        "volkswagen": ["VW_EMAIL", "VW_PASSWORD"],
        "toyota": ["TOYOTA_EMAIL", "TOYOTA_PASSWORD"],
        "ford": ["FORD_USERNAME", "FORD_PASSWORD"],
        "kia": ["KIA_EMAIL", "KIA_PASSWORD"],
        "honda": ["HONDA_EMAIL", "HONDA_PASSWORD"]
      }
    },
    "install": [
      {
        "id": "pip-tesla",
        "kind": "pip",
        "formula": "teslapy",
        "label": "Install teslapy for Tesla"
      },
      {
        "id": "pip-kia",
        "kind": "pip",
        "formula": "hyundai_kia_connect_api",
        "label": "Install hyundai_kia_connect_api for Kia/Hyundai"
      },
      {
        "id": "pip-honda",
        "kind": "pip",
        "formula": "pymyhondaplus",
        "label": "Install pymyhondaplus for Honda"
      },
      {
        "id": "pip-toyota",
        "kind": "pip",
        "formula": "pytoyoda",
        "label": "Install pytoyoda for Toyota (EU)"
      },
      {
        "id": "pip-fordpass",
        "kind": "pip",
        "formula": "fordpass",
        "label": "Install fordpass for Ford"
      }
    ]
  }
}
---

# Car Connect

**Author:** Suvo — [@deadlybutsoft](https://github.com/deadlybutsoft)
**Version:** 3.0.0 | **Brands:** Tesla, Mercedes, Volkswagen, Toyota, Ford, Kia, Honda

Control multiple car brands from your terminal. Each brand uses its official connected services API.

## Supported Brands

| Brand | API | Features | Env Vars |
|-------|-----|----------|----------|
| Tesla | Tesla Owner API | Full control | TESLA_EMAIL |
| Mercedes | Mercedes Me API | Full control | MERCEDES_EMAIL, MERCEDES_PASSWORD |
| Volkswagen | We Connect ID | Full control | VW_EMAIL, VW_PASSWORD |
| Toyota | Toyota Connected (EU) | Status, climate | TOYOTA_EMAIL, TOYOTA_PASSWORD |
| Ford | FordPass | Status, lock/unlock, engine | FORD_USERNAME, FORD_PASSWORD |
| Kia | UVO Connect | Full control | KIA_EMAIL, KIA_PASSWORD |
| Honda | My Honda+ (EU) | Lock/unlock/horn/climate | HONDA_EMAIL, HONDA_PASSWORD |

## Setup

### 1. Install dependencies

```bash
pip install teslapy hyundai_kia_connect_api pymyhondaplus pytoyoda fordpass
```

### 2. Set environment variables

```bash
# Tesla
export TESLA_EMAIL="you@email.com"

# Mercedes
export MERCEDES_EMAIL="you@email.com"
export MERCEDES_PASSWORD="your_password"

# Volkswagen
export VW_EMAIL="you@email.com"
export VW_PASSWORD="your_password"

# Toyota (EU only)
export TOYOTA_EMAIL="you@email.com"
export TOYOTA_PASSWORD="your_password"

# Ford
export FORD_USERNAME="you@email.com"
export FORD_PASSWORD="your_password"

# Kia / Hyundai
export KIA_EMAIL="you@email.com"
export KIA_PASSWORD="your_password"

# Honda (EU)
export HONDA_EMAIL="you@email.com"
export HONDA_PASSWORD="your_password"
```

### 3. First-time authentication

```bash
# Tesla
python3 {baseDir}/scripts/car_connect.py auth tesla

# Mercedes
python3 {baseDir}/scripts/car_connect.py auth mercedes

# Volkswagen
python3 {baseDir}/scripts/car_connect.py auth volkswagen

# Kia / Hyundai
python3 {baseDir}/scripts/car_connect.py auth kia

# Honda
python3 {baseDir}/scripts/car_connect.py auth honda

# Toyota (EU)
python3 {baseDir}/scripts/car_connect.py auth toyota

# Ford
python3 {baseDir}/scripts/car_connect.py auth ford
```

## Commands

### List all cars (all brands)

```bash
python3 {baseDir}/scripts/car_connect.py list
python3 {baseDir}/scripts/car_connect.py list --brand tesla
python3 {baseDir}/scripts/car_connect.py list --brand kia
python3 {baseDir}/scripts/car_connect.py list --all
```

### Status summary (all brands)

```bash
python3 {baseDir}/scripts/car_connect.py summary --brand tesla
python3 {baseDir}/scripts/car_connect.py summary --brand mercedes --car "EQS"
python3 {baseDir}/scripts/car_connect.py summary --brand volkswagen --car "ID4"
python3 {baseDir}/scripts/car_connect.py summary --brand kia --car "EV6"
python3 {baseDir}/scripts/car_connect.py summary --brand toyota --car "RAV4"
python3 {baseDir}/scripts/car_connect.py summary --brand honda --car "Honda e"
python3 {baseDir}/scripts/car_connect.py summary --brand ford
python3 {baseDir}/scripts/car_connect.py summary --all
```

### Detailed status

```bash
python3 {baseDir}/scripts/car_connect.py status --brand tesla
python3 {baseDir}/scripts/car_connect.py status --brand kia --car "EV6"
python3 {baseDir}/scripts/car_connect.py status --json --brand tesla
```

### Lock / Unlock

```bash
# Lock
python3 {baseDir}/scripts/car_connect.py lock --brand tesla --car "Model 3" --yes
python3 {baseDir}/scripts/car_connect.py lock --brand mercedes --yes
python3 {baseDir}/scripts/car_connect.py lock --brand kia --car "EV6" --yes
python3 {baseDir}/scripts/car_connect.py lock --brand honda --yes

# Unlock
python3 {baseDir}/scripts/car_connect.py unlock --brand tesla --car "Model 3" --yes
python3 {baseDir}/scripts/car_connect.py unlock --brand mercedes --yes
python3 {baseDir}/scripts/car_connect.py unlock --brand kia --car "EV6" --yes
```

### Climate control

```bash
# Temperature (default: Fahrenheit)
python3 {baseDir}/scripts/car_connect.py climate temp 72 --brand tesla
python3 {baseDir}/scripts/car_connect.py climate temp 22 --celsius --brand kia

# Climate on/off
python3 {baseDir}/scripts/car_connect.py climate on --brand tesla --yes
python3 {baseDir}/scripts/car_connect.py climate off --brand tesla --yes

# Defrost
python3 {baseDir}/scripts/car_connect.py climate defrost on --brand tesla --yes
python3 {baseDir}/scripts/car_connect.py climate defrost on --brand mercedes --yes

# Climate start (Honda)
python3 {baseDir}/scripts/car_connect.py climate-start --brand honda --yes
```

### Charge / Fuel

```bash
# Charge status (Tesla, Kia, Mercedes EV)
python3 {baseDir}/scripts/car_connect.py charge status --brand tesla
python3 {baseDir}/scripts/car_connect.py charge status --brand kia
python3 {baseDir}/scripts/car_connect.py charge status --brand mercedes

# Charge start/stop (safety gated)
python3 {baseDir}/scripts/car_connect.py charge start --brand tesla --yes
python3 {baseDir}/scripts/car_connect.py charge stop --brand tesla --yes
python3 {baseDir}/scripts/car_connect.py charge start --brand kia --car "EV6" --yes

# Charge limit (Tesla: 50-100%)
python3 {baseDir}/scripts/car_connect.py charge limit 80 --brand tesla --yes

# Fuel status (Volkswagen ICE, Ford)
python3 {baseDir}/scripts/car_connect.py fuel status --brand volkswagen
python3 {baseDir}/scripts/car_connect.py fuel status --brand ford
```

### Location

```bash
# Approximate location
python3 {baseDir}/scripts/car_connect.py location --brand tesla
python3 {baseDir}/scripts/car_connect.py location --brand kia --car "EV6"

# Precise location
python3 {baseDir}/scripts/car_connect.py location --yes --brand tesla
```

### Tyre pressure

```bash
python3 {baseDir}/scripts/car_connect.py tyres --brand tesla
python3 {baseDir}/scripts/car_connect.py tyres --brand kia
python3 {baseDir}/scripts/car_connect.py tyres --brand mercedes
```

### Trunk / Frunk

```bash
# Open trunk
python3 {baseDir}/scripts/car_connect.py trunk open --brand tesla --yes
python3 {baseDir}/scripts/car_connect.py trunk open --brand kia --car "EV6" --yes

# Open frunk
python3 {baseDir}/scripts/car_connect.py frunk open --brand tesla --yes
```

### Windows

```bash
# Status
python3 {baseDir}/scripts/car_connect.py windows --brand tesla

# Vent (open windows slightly)
python3 {baseDir}/scripts/car_connect.py windows vent --brand tesla --yes

# Close windows
python3 {baseDir}/scripts/car_connect.py windows close --brand tesla --yes
```

### Honk / Flash (find car)

```bash
python3 {baseDir}/scripts/car_connect.py honk --brand tesla --yes
python3 {baseDir}/scripts/car_connect.py flash --brand tesla --yes
python3 {baseDir}/scripts/car_connect.py horn --brand honda --yes
```

### Engine start/stop (Ford)

```bash
python3 {baseDir}/scripts/car_connect.py engine on --brand ford --yes
python3 {baseDir}/scripts/car_connect.py engine off --brand ford --yes
```

### All brands summary

```bash
# One command for all configured brands
python3 {baseDir}/scripts/car_connect.py summary --all

# JSON output
python3 {baseDir}/scripts/car_connect.py summary --all --json
```

## Safety Defaults

Actions requiring `--yes` confirmation:
- `lock`, `unlock`
- `trunk open`, `frunk open`
- `windows vent`, `windows close`
- `charge start`, `charge stop`, `charge limit`
- `engine on`, `engine off`
- `climate on`, `climate defrost on`, `climate-start`
- `honk`, `flash`, `horn`

## Privacy

- Tokens cached locally only (brand-specific paths)
- Location is approximate by default
- Do not commit tokens, VINs, or precise location data
- Use `--json` for machine-readable, privacy-safe output

## Examples

**Morning check — all cars:**
```
User: Check all my cars
Assistant: Runs summary --all for all 7 brands
```

**Lock from bed:**
```
User: Lock the Kia
Assistant: car-connect lock --brand kia --yes
```

**Pre-heat before trip:**
```
User: Start heating the Tesla
Assistant: car-connect climate defrost on --brand tesla --yes
```

**Check charge before road trip:**
```
User: How much charge does the VW have?
Assistant: car-connect charge status --brand volkswagen
```