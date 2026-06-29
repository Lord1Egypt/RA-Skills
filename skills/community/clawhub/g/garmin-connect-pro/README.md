# Garmin Connect Pro

> Want to be fit like @steipete? Well, now you can track every step of your journey—literally.

**The most comprehensive Garmin Connect skill for OpenClaw.** Retrieve activities, health data, sleep analysis, heart rate, stress, body battery, training readiness, VO2 max, and more from your Fenix, Forerunner, Index scales, or other Garmin devices.

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

## What makes this different

| Feature | Garmin Connect Pro | Others |
|---------|-------------------|--------|
| **Natural Language Queries** | ✅ "how did I sleep?" | ❌ |
| **ASCII Charts** | ✅ Built-in | ❌ |
| **Week-over-Week Comparison** | ✅ | ❌ |
| **Race Predictions** | ✅ 5K to Marathon | Limited |
| **Body Composition** | ✅ Weight, muscle, fat | Limited |
| **VO2 Max Tracking** | ✅ | Limited |
| **FIT/GPX Download** | ✅ | ✅ |
| **Training Effect** | ✅ Aerobic + Anaerobic | Limited |
| **HR Zones per Activity** | ✅ | Limited |
| **Emoji-Powered Output** | ✅ Quick scanning | ❌ |
| **Full JSON Export** | ✅ | ✅ |

## Quick Start

```bash
# Install
pip3 install garminconnect

# Option A: Environment variables (recommended)
export GARMIN_EMAIL="you@example.com"
export GARMIN_PASSWORD="your-password"

# Option B: Credentials file
mkdir -p ~/.config/garmin-connect
echo '{"email": "you@example.com", "password": "your-password"}' > ~/.config/garmin-connect/credentials.json
chmod 600 ~/.config/garmin-connect/credentials.json

# Login (generates OAuth tokens)
python3 scripts/garmin.py login

# Ask questions naturally
python3 scripts/garmin.py ask "how did I sleep?"
python3 scripts/garmin.py ask "what's my body battery?"
```

## Natural Language Queries

Just ask questions in plain English:

```
python3 scripts/garmin.py ask "how did I sleep last night?"
python3 scripts/garmin.py ask "what's my body battery?"
python3 scripts/garmin.py ask "how many steps today?"
python3 scripts/garmin.py ask "am I ready to train?"
```

Responses include context and recommendations:
```
🔋 Body Battery:
   Current: 35%
   ⚠️ Low - light activity recommended
```

## Commands

### Natural Language
```bash
python3 scripts/garmin.py ask "how did I sleep?"
python3 scripts/garmin.py ask "what's my training readiness?"
```

### Daily Summary
```bash
python3 scripts/garmin.py summary
python3 scripts/garmin.py summary --date 2026-03-03
```

### Activities
```bash
python3 scripts/garmin.py activities --limit 5
python3 scripts/garmin.py activity --id 123456  # Full details with HR zones
```

### Health Metrics
```bash
python3 scripts/garmin.py stats --today
python3 scripts/garmin.py sleep --today
python3 scripts/garmin.py hr --today
python3 scripts/garmin.py hrv --today
python3 scripts/garmin.py stress --today
python3 scripts/garmin.py body-battery --today
```

### Body Composition & VO2 Max
```bash
python3 scripts/garmin.py body              # Weight, muscle mass, fat %
python3 scripts/garmin.py vo2max            # VO2 max + race predictions
```

### Training
```bash
python3 scripts/garmin.py training --today
python3 scripts/garmin.py race              # Race predictions
```

### Trends & Charts
```bash
python3 scripts/garmin.py week --days 7
python3 scripts/garmin.py trends --days 14
python3 scripts/garmin.py compare           # Week over week
python3 scripts/garmin.py chart steps --days 30
python3 scripts/garmin.py chart hr --days 7
python3 scripts/garmin.py chart stress --days 14
```

### Download Activities
```bash
python3 scripts/garmin.py download          # List recent activities
python3 scripts/garmin.py download --id 123456 --format fit
python3 scripts/garmin.py download --id 123456 --format gpx
```

## Cron Job Setup

⚠️ **Security Note:** Using environment variables is more secure than storing credentials on disk.

### Option A: Environment Variables (Recommended)

```bash
# In your crontab or OpenClaw cron config:
GARMIN_EMAIL="you@example.com" GARMIN_PASSWORD="your-password" python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py summary
```

### Option B: Credentials File

```bash
# Morning motivation at 6:30
openclaw cron add --name "Morning Fitness" --cron "30 6 * * *" \
  --message "python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py summary"

# Midday check at 12:00
openclaw cron add --name "Midday Check" --cron "0 12 * * *" \
  --message "python3 ~/.agents/skills/garmin-connect-pro/scripts/garmin.py ask 'body battery'"
```

**Note:** Cron jobs that run scripts with access to stored credentials increase the attack surface. Consider:
- Using a dedicated Garmin account with limited permissions
- Using environment variables instead of credential files
- Running on a secure, isolated system

## Output Examples

### Natural Language Response
```
🔋 Body Battery:
   Current: 35%
   ⚠️ Low - light activity recommended
```

### ASCII Charts
```
📈 TRENDS - Last 7 Days

👣 Steps
──────────────────────────────────────────────────────
12000 │         █
10000 │     █   █       █
 8000 │     █   █   █   █
 6000 │ █   █   █   █   █   █
 4000 │ █   █   █   █   █   █   █
    0 └──────────────────────────────────
      Mon  Tue  Wed  Thu  Fri  Sat  Sun
```

### Week Comparison
```
📊 WEEK VS WEEK
─────────────────────────────────────────────────
Metric          This Week   Last Week   Change
─────────────────────────────────────────────────
Steps              45,000      40,000    ↑ 12.5%
Distance (km)         38.0        32.5   ↑ 16.9%
Calories            19,000      18,000     ↑ 5.6%
Resting HR            55.0        56.5     ↓ 2.7%
```

## Data Available

| Category | Metrics |
|----------|---------|
| **Activities** | Name, type, duration, distance, calories, HR zones, training effect, elevation, splits |
| **Daily Stats** | Steps, distance, floors, calories, HR (resting/min/max), stress, body battery |
| **Sleep** | Total, deep, light, REM, awake, score |
| **Heart** | Resting HR, min/max HR, HR zones, HRV |
| **Training** | Readiness score, intensity minutes, race predictions, FTP |
| **Body** | Weight, muscle mass, fat percentage, BMI |
| **Health** | SpO2, respiration, hydration, stress |
| **Devices** | Fenix 7, Forerunner, Index scales, firmware, battery |

## JSON Output

Add `--json` to any command for scripting:

```bash
python3 scripts/garmin.py summary --json | jq '.totalSteps'
python3 scripts/garmin.py activities --json | jq '.[0].averageHR'
python3 scripts/garmin.py export --days 30 --json > monthly_data.json
```

## Requirements

- Python 3.7+
- `garminconnect` (`pip install garminconnect`)
- Garmin Connect account

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
- Garmin may rate-limit excessive requests
- Add delays between bulk operations

## The Honest Truth

This won't make you fitter. But it will make it harder to ignore the data. Your Garmin already knows you skipped leg day—now OpenClaw can remind you too.

---

*Want to be fit like @steipete? Well, now you can track every step of your journey—literally.*