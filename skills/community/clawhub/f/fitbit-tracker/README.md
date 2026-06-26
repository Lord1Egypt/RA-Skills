# fitbit-tracker

**The smartest way to track your Fitbit data in any chat.**

Effortless health monitoring powered by the official Fitbit API. No apps, no dashboards — just ask and get your health stats instantly.

## Features

- **Smart sleep tracking** — Automatically separates naps from main sleep
- **Complete activity picture** — Steps, calories, distance, active minutes, HR zones
- **Adaptive reporting** — Only shows what you ask for
- **Clean formatting** — Numbers formatted for readability
- **Nap detection** — Automatically identifies and reports daytime sleep

## Quick Start

### 1. Create Fitbit Developer App

1. Go to [dev.fitbit.com](https://dev.fitbit.com)
2. Register a new app
3. Set OAuth redirect URI to `http://localhost:8080`
4. Copy your Client ID and Client Secret

### 2. Configure

```bash
export FITBIT_CLIENT_ID="your_client_id"
export FITBIT_CLIENT_SECRET="your_client_secret"
export FITBIT_REDIRECT_URI="http://localhost:8080"
export FITBIT_TZ="Europe/London"
```

### 3. Authenticate

```bash
python3 scripts/fitbit_oauth_login.py
```

### 4. Use

Ask naturally:
- "how did I sleep?" → Sleep report with stages
- "just my steps" → Step count
- "full report" → Everything

## Example Output

**Sleep:**
```
Fitbit — 2026-03-21
- Sleep: 7h 32m (score 85) | 93% efficiency
  - Stages: Deep: 1h 42m, Light: 3h 20m, REM: 1h 45m, Wake: 45m
- Nap: 1h 6m
```

**Full summary:**
```
Fitbit — 2026-03-21
- Sleep: 7h 32m | 93% efficiency
  - Stages: Deep: 1h 42m, Light: 3h 20m, REM: 1h 45m, Wake: 45m
- Nap: 1h 6m
- Steps: 8,234
- Calories: 1,892 (1,048 BMR)
- Distance: 6.2 km
- Resting HR: 58 bpm
  - Active mins: V. Active: 45m, Fair: 23m, Light: 1h 24m
  - HR Zones: Fat Burn: 1h 30m, Cardio: 32m
```

## Requirements

- Fitbit account
- Fitbit OAuth app (dev.fitbit.com)
- Python 3.9+ (standard library only, no deps)

## Data

Uses official Fitbit API:
- Activity summary (steps, calories, distance, HR zones)
- Sleep records with staging (Deep, Light, REM, Wake)

No third-party services. No data stored externally.

## License

MIT
