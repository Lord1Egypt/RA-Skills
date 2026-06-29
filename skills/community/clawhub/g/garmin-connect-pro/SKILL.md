---
name: garmin-connect-pro
version: 1.4.0
description: |
  Want to be fit like @steipete? Well, now you can track every step of your journey—literally. This skill pulls your complete Garmin Connect data into OpenClaw: activities, sleep, heart rate, stress, body battery, training readiness, VO2 max, and those race predictions you keep ignoring. Works with Fenix, Forerunner, Index scales, and anything else Garmin throws at you. Includes natural language queries ("how did I sleep?"), ASCII charts, week-over-week comparisons, and FIT/GPX downloads.
metadata:
  openclaw:
    emoji: "⌚"
    requires:
      bins: [python3]
      pips: [garminconnect>=0.2.38]
    config:
      environment:
        GARMIN_EMAIL:
          description: Garmin Connect email (RECOMMENDED - more secure than file)
          required: false
          secret: true
        GARMIN_PASSWORD:
          description: Garmin Connect password (RECOMMENDED - more secure than file)
          required: false
          secret: true
      files:
        - path: ~/.config/garmin-connect/credentials.json
          description: "Fallback: Credentials file if env vars not set. WARNING: Plaintext - use env vars instead."
          required: false
          permissions: "600"
          containsSecrets: true
        - path: ~/.config/garmin-connect/tokens/
          description: OAuth tokens (auto-generated after login, 600 permissions)
          required: false
          containsSecrets: true
    security:
      - "CREDENTIAL PRIORITY: Environment variables > Credentials file > macOS Keychain (if configured)"
      - "RECOMMENDED: Use GARMIN_EMAIL/GARMIN_PASSWORD env vars - not stored on disk, survives reboots with launchd/keychain"
      - "FALLBACK: Credentials file at ~/.config/garmin-connect/credentials.json (plaintext, 600 permissions)"
      - "OAuth tokens are cached locally after first login - subsequent logins use tokens, not password"
      - "Third-party library: garminconnect (https://github.com/cyberjunkie/garminconnect) - open source, auditable"
      - "NO data transmission except to Garmin API servers via official garminconnect library"
      - "For cron jobs: Pass env vars in crontab or use launchd with EnvironmentVariables key"
---

# Garmin Connect Pro

The most comprehensive Garmin Connect skill for OpenClaw. Retrieve activities, health data, sleep analysis, heart rate, stress, body battery, training readiness, VO2 max, and more from your Fenix, Forerunner, Index scales, or other Garmin devices.

## Security & Privacy

⚠️ **Important Security Information:**

### Credential Options

**Option 1: Environment Variables (Recommended for cron jobs)**
```bash
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"
```
- More secure for automated/scheduled usage
- Not stored on disk
- Works with cron jobs without leaving plaintext files

**Option 2: Credentials File**
```bash
mkdir -p ~/.config/garmin-connect
echo '{"email": "your-email@example.com", "password": "your-password"}' > ~/.config/garmin-connect/credentials.json
chmod 600 ~/.config/garmin-connect/credentials.json
```
- Stored in plaintext (any process with file access can read it)
- File permissions set to 600 (owner read/write only)
- Consider excluding from backups

### Third-Party Library

This skill uses the `garminconnect` Python library for all Garmin API communication. 
- **Source code:** https://github.com/cyberjunkie/garminconnect
- **Trust boundary:** All API calls go through this library
- **Recommendation:** Audit the library if you have strict security requirements

### Data Flow

```
Your Credentials → garminconnect library → Garmin API servers
                     ↓
              OAuth tokens cached locally
```

No data is transmitted to any third parties other than Garmin via the official garminconnect library.

## Setup

### First-time Login

```bash
# Install dependency
pip3 install garminconnect

# Option A: Use environment variables (recommended)
export GARMIN_EMAIL="your-email@example.com"
export GARMIN_PASSWORD="your-password"

# Option B: Use credentials file
mkdir -p ~/.config/garmin-connect
echo '{"email": "your-email@example.com", "password": "your-password"}' > ~/.config/garmin-connect/credentials.json
chmod 600 ~/.config/garmin-connect/credentials.json

# Login (generates OAuth tokens)
python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py login
```

## Features

| Feature | Description |
|---------|-------------|
| **Natural Language Queries** | "how did I sleep?", "what's my body battery?", "should I train today?" |
| **ASCII Charts** | Visual trends for steps, HR, stress, battery |
| **Week-over-Week Comparison** | Track progress vs last week |
| **Race Predictions** | 5K, 10K, half marathon, marathon |
| **Body Composition** | Weight, muscle mass, fat percentage |
| **VO2 Max Tracking** | Cardio fitness from activities |
| **FIT/GPX Downloads** | Export activity files |
| **Training Effect** | Aerobic + anaerobic impact |
| **HR Zones per Activity** | Time in each zone |
| **Emoji-Powered Output** | Quick visual scanning |

## Quick Start

```bash
# Ask questions naturally
python3 scripts/garmin.py ask "how did I sleep?"
python3 scripts/garmin.py ask "what's my training readiness?"

# Daily summary
python3 scripts/garmin.py summary

# Trends with charts
python3 scripts/garmin.py trends --days 7
python3 scripts/garmin.py chart steps --days 14

# Compare weeks
python3 scripts/garmin.py compare

# Download activities
python3 scripts/garmin.py download --id 123456 --format fit
```

## Commands

### Natural Language
```bash
python3 scripts/garmin.py ask "how did I sleep?"
python3 scripts/garmin.py ask "am I stressed?"
python3 scripts/garmin.py ask "how many steps today?"
```

### Daily Metrics
```bash
python3 scripts/garmin.py summary              # Full daily summary
python3 scripts/garmin.py stats --today        # Steps, HR, calories
python3 scripts/garmin.py sleep --today        # Sleep stages
python3 scripts/garmin.py hr --today           # Heart rate data
python3 scripts/garmin.py hrv --today          # HRV
python3 scripts/garmin.py stress --today       # Stress levels
python3 scripts/garmin.py body-battery --today # Energy level
```

### Activities
```bash
python3 scripts/garmin.py activities --limit 5
python3 scripts/garmin.py activity --id 123456 --full
python3 scripts/garmin.py download --id 123456 --format fit
```

### Training & Performance
```bash
python3 scripts/garmin.py training --today     # Readiness + intensity
python3 scripts/garmin.py vo2max              # VO2 max + predictions
python3 scripts/garmin.py body                 # Body composition
python3 scripts/garmin.py race                 # Race predictions
```

### Trends
```bash
python3 scripts/garmin.py week --days 7
python3 scripts/garmin.py trends --days 14
python3 scripts/garmin.py compare              # Week vs week
python3 scripts/garmin.py chart steps --days 30
```

## Example Output

### Natural Language Response
```
🔋 Body Battery:
   Current: 45%
   ⚠️ Moderate - lighter activity recommended
```

### Weekly Comparison
```
📊 WEEK VS WEEK
─────────────────────────────────────────────────
Metric          This Week   Last Week   Change
─────────────────────────────────────────────────
Steps              42,500      38,200    ↑ 11.3%
Distance (km)         35.2        28.9   ↑ 21.8%
Calories            18,500      17,200     ↑ 7.6%
Resting HR            56.0        57.5     ↓ 2.6%
```

### ASCII Chart
```
📈 STEPS - Last 7 Days
──────────────────────────────────────────────
10000 │       █           █
 8000 │   █   █   █       █
 6000 │   █   █   █   █   █
 4000 │   █   █   █   █   █   █
 2000 │   █   █   █   █   █   █   █
    0 └────────────────────────────────
      Mon  Tue  Wed  Thu  Fri  Sat  Sun
```

## Cron Job Setup

⚠️ **Security Note:** Using environment variables is more secure than storing credentials on disk.

### Option A: Environment Variables (Recommended)

```bash
# In your crontab or OpenClaw cron config:
GARMIN_EMAIL="your-email@example.com" GARMIN_PASSWORD="your-password" python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py summary
```

### Option B: Credentials File

```bash
# Morning briefing at 6:30
openclaw cron add --name "Morning Fitness" --cron "30 6 * * *" \
  --message "python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py summary"

# Midday check at 12:00
openclaw cron add --name "Midday Check" --cron "0 12 * * *" \
  --message "python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py ask 'body battery'"

# Evening summary at 20:00
openclaw cron add --name "Evening Summary" --cron "0 20 * * *" \
  --message "python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py week --days 1"
```

**Note:** Cron jobs that run scripts with access to stored credentials increase the attack surface. Consider:
- Using a dedicated Garmin account with limited permissions
- Using environment variables instead of credential files
- Running on a secure, isolated system

## Data Available

| Category | Metrics |
|----------|---------|
| **Activities** | Name, type, duration, distance, calories, HR zones, training effect, elevation, splits, steps |
| **Daily Stats** | Steps, distance, floors, calories (total/active/BMR), HR (resting/min/max), stress, body battery |
| **Sleep** | Total, deep, light, REM, awake, sleep score |
| **Heart** | Resting HR, min/max HR, HR zones, HRV (heart rate variability) |
| **Training** | Readiness score, intensity minutes (moderate/vigorous), aerobic/anaerobic effect |
| **Body** | Weight, muscle mass, fat percentage, BMI (with Index scale) |
| **Performance** | VO2 max, race predictions (5K-marathon), FTP (cycling) |
| **Health** | SpO2, respiration rate, hydration, stress timeline |
| **Devices** | Fenix, Forerunner, Index scales, firmware, battery level |

## JSON Output

Add `--json` to any command for scripting:

```bash
python3 scripts/garmin.py summary --json | jq '.totalSteps'
python3 scripts/garmin.py activities --json | jq '.[0].averageHR'
python3 scripts/garmin.py export --days 30 --json > monthly_export.json
```

## Requirements

- Python 3.7+
- `garminconnect` library (`pip install garminconnect`)
- Garmin Connect account with devices synced

## Troubleshooting

### "Authentication failed"
- Verify email and password in credentials file or environment variables
- Delete tokens: `rm -rf ~/.config/garmin-connect/tokens/`
- Re-run login

### "No data for date"
- Device may not have synced yet
- Sleep data appears after morning sync
- Some metrics (HRV, training readiness) require overnight processing

### Rate Limits
- Garmin may rate-limit excessive API calls
- Add delays between bulk requests

## The Honest Truth

This won't make you fitter. But it will make it harder to ignore the data. Your Garmin already knows you skipped leg day—now OpenClaw can remind you too.

---

*Want to be fit like @steipete? Well, now you can track every step of your journey—literally.*