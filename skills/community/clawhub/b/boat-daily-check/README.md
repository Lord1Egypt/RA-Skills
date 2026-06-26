# ⚓ Boat Daily Check — Victron Power System Monitor

Beautiful, automated daily email reports for Victron Energy power systems.

![Status](https://img.shields.io/badge/status-stable-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)

## What is Boat Daily Check?

**Stop logging into VRM every morning.** Boat Daily Check automatically monitors your Victron power systems and sends beautiful daily email reports showing:

- 🔋 Battery state of charge, voltage, current, temperature
- ☀️ Solar generation & daily yield
- 🔌 Inverter/AC power status
- 🚨 Active alarms and alerts
- 📊 Real-time hardware status

Perfect for boat owners, RV adventurers, and anyone with Victron power systems who wants to monitor their setup without manual VRM dashboard checks.

### The Problem It Solves

- **Manual checking is tedious**: Log into VRM daily, navigate to your installation, check battery status
- **Easy to miss alerts**: Alarms buried in dashboards, no notifications
- **Multi-boat headache**: Multiple installations mean multiple logins
- **No historical context**: Quick snapshots, no tracking over time

### The Solution

One beautiful email every morning with everything you need to know about your power systems. Works standalone or integrated into your morning routine (fishing reports, weather, boat status—all in one email).

### Built for Real-World Use

- Used by boat owners monitoring live systems (Pitter Patter & Pegasus)
- Battle-tested Victron VRM API integration
- Production-grade Python code with error handling
- Comprehensive documentation for customization
- MIT licensed—free to use, modify, and share

## Features

✨ **Real-time Battery Monitoring**
- State of Charge (%), voltage, current, temperature
- Time-to-go estimates
- Battery alarm detection

☀️ **Solar Generation Tracking** (for MPPT chargers)
- Live PV power output (watts)
- Daily yield totals (kWh)
- Maximum charge power
- PV voltage monitoring

🔌 **AC Power Status** (for inverter/shore power)
- AC input voltage
- Active input detection
- Charger/inverter status

📧 **Beautiful HTML Emails**
- Professional responsive design
- Color-coded status badges
- Battery visual progress bars
- Multiple installations in one email
- Mobile-friendly layout

🔄 **Easy Integration**
- Works with OpenClaw cron jobs
- Standalone script for manual runs
- JSON + CSV exports for data processing
- Integrates with existing email workflows

## Quick Start

### 1. Get API Token
```bash
# Visit: https://vrm.victronenergy.com/access-tokens
# Create a new token, copy it
export VRM_TOKEN="your-token-here"
```

### 2. Find Your Installation ID
Check your VRM dashboard URL:
```
https://vrm.victronenergy.com/installation/123456/dashboard
                                         ^^^^^^
                                    Installation ID
```

### 3. Update the Script
```bash
# Edit the Python script with your details
vim scripts/boat-email-report.py

# Set your token and installation IDs:
VRM_TOKEN = "your-token-here"
INSTALLATIONS = {
    "boat1": {"id": 000000, "name": "My Boat", "batteryInstance": 279}
}
```

### 4. Run It
```bash
# Generate report now
python3 scripts/boat-email-report.py

# Check output
open out/boat-daily-email.html
```

### 5. Automate (Optional)
```bash
# Add to your morning report in OpenClaw
# Or create a standalone daily cron job at 7 AM
```

## What the Email Shows

```
⚓ BOAT POWER SYSTEMS STATUS
═════════════════════════════════════════

🚤 Pitter Patter                [✓ Healthy]
   Battery SOC ......... 100.0 %
   Voltage ............. 14.17 V
   Current ............. 3.50 A
   
   ⚡ Solar Status
   Today's Yield ....... 0.59 kWh
   Max Charge .......... 168 W
   PV Voltage .......... 18.6 V
   
   🔌 Hardware
   Gateway ............. Cerbo GX v3.70 (3 min ago)
   Battery Monitor ..... SmartShunt 500A v4.19
   Solar Charger ....... SmartSolar MPPT 75/15 v1.73

🚤 Pegasus                      [⚠️ Alert]
   Battery SOC ......... 100.0 %
   Voltage ............. 13.63 V
   AC Input ............ 121.4 V
   
   🚨 Active Alarms
   • VE.Bus System [276] - "Active input"
   
   🔌 Hardware
   Gateway ............. Cerbo GX v3.70 (2 min ago)
   Inverter/Charger .... MultiPlus Compact v508
```

## Files

```
boat-daily-check/
├── README.md                          # This file
├── SKILL.md                           # OpenClaw skill definition
├── scripts/
│   └── boat-email-report.py          # Main Python script
├── references/
│   ├── victron_attributes.md         # Attribute code reference
│   └── vrm_api_guide.md              # VRM API quick reference
├── out/                              # Generated outputs (auto-created)
│   ├── boat-daily-email.html
│   ├── boat-status.json
│   └── boat-status.csv
└── assets/                           # Optional customizations
    └── email-template.html
```

## Installation

### Option 1: OpenClaw Skill (Recommended)
```bash
# Install from clawhub (when published)
openclaw clawhub install victron/boat-daily-check
```

### Option 2: Manual Setup
```bash
# Clone/copy to your skills directory
git clone <repo> ~/.openclaw/workspace/skills/boat-daily-check
cd boat-daily-check
python3 scripts/boat-email-report.py
```

## Configuration

### Edit Python Script
Update `INSTALLATIONS` dict with your boats:

```python
VRM_TOKEN = "your-api-token"

INSTALLATIONS = {
    "boat1": {
        "id": 000000,              # Installation ID from VRM
        "name": "Titanic",   # Display name for email
        "batteryInstance": 279,    # SmartShunt instance (usually 279)
        "hasSolar": True,          # Fetch solar data?
        "hasInverter": False,      # Fetch inverter data?
    },
    "boat2": {
        "id": 000001,
        "name": "Endeavour",
        "batteryInstance": 279,
        "hasSolar": False,
        "hasInverter": True,
    }
}
```

### Custom Email Recipients
```python
# In boat-email-report.py, modify the email sending section
recipients = ["your-email@example.com", "team@example.com"]
```

### Integrate with OpenClaw Cron
```bash
openclaw cron add -j '{
  "name": "boat-daily-check",
  "schedule": {"kind": "cron", "expr": "0 7 * * *"},
  "payload": {"kind": "agentTurn", "message": "python3 /path/to/boat-email-report.py"},
  "sessionTarget": "isolated"
}'
```

Or embed in existing email job:
```bash
# Add to fishing-surf-report or other morning email
# Just call: python3 /path/to/boat-email-report.py
# Then append HTML to your email body
```

## Usage Examples

### Standalone Execution
```bash
python3 scripts/boat-email-report.py
# Generates: out/boat-daily-email.html
```

### In a Shell Script
```bash
#!/bin/bash
cd /path/to/boat-daily-check
python3 scripts/boat-email-report.py
HTML=$(cat out/boat-daily-email.html)
# Send $HTML via email...
```

### With OpenClaw
```bash
# Manual trigger
openclaw cron run -j boat-daily-check

# View last run
openclaw cron runs -j boat-daily-check
```

### Get JSON Export
```bash
python3 scripts/boat-email-report.py
# Check: out/boat-status.json for structured data
cat out/boat-status.json | jq '.pitterPatter.battery.soc'
```

## Troubleshooting

### Script returns empty data
1. Check API token is valid: https://vrm.victronenergy.com/access-tokens
2. Verify installation ID (from VRM URL)
3. Check SmartShunt is online in VRM dashboard
4. Try different `batteryInstance` (default 279)

### No solar data
- Confirm MPPT charger is online
- Check `"hasSolar": True` is set in config
- MPPT might be sleeping (no output during night)

### Email not sending
- If using OpenClaw: check delivery mode in cron job
- Check `recipients` email list in script
- Look for OpenClaw email service errors

### "Child not found" error
- Installation ID is invalid
- Device offline in VRM
- Widget not available for this device

### Rate limit errors (429)
- VRM API limits ~10 req/sec
- Script has built-in delays
- Try again in a few minutes

## API Details

### Victron VRM API v2
- **Base**: `https://vrmapi.victronenergy.com/v2`
- **Auth**: `X-Authorization: Token {token}`
- **Docs**: https://vrm-api-docs.victronenergy.com/

### Key Endpoints
- `GET /installations/{id}/widgets/BatterySummary/latest?instance={n}` — Battery data
- `GET /installations/{id}/diagnostics` — All device metrics
- `GET /installations/{id}/alarms` — Active alarms

### Metrics Collected
- Battery: SOC%, voltage, current, temperature
- Solar: Power, yield today, max charge, PV voltage
- Inverter: AC input voltage, active input status
- Alarms: Active alarm list with details
- Hardware: Device names, versions, last contact time

## Performance

- API calls: ~5 seconds
- HTML generation: ~1 second
- Email delivery: ~5 seconds
- **Total runtime**: <15 seconds for 2 boats

Suitable for daily cron jobs with no performance issues.

## Customization

### Change Email Design
Edit the HTML template in `boat-email-report.py`:

```python
html = html.replace("{{pitterPatter.battery.soc}}", f"{soc}%")
# Modify CSS, layout, colors, etc.
```

### Add New Metrics
Find attribute codes in `references/victron_attributes.md`, then:

```python
# In fetch_battery_data():
"mid_voltage": records.get("116", {}).get("valueFloat", 0),
# In HTML:
html.replace("{{boat.mid_voltage}}", f"{mid_voltage}V")
```

### Support More Installations
Add to `INSTALLATIONS` dict and update report generation loop.

## Real-World Impact

This skill was born from a real problem: **manual daily VRM checks are tedious.**

### Before Boat Daily Check
- Log into VRM dashboard daily
- Navigate to installation
- Check battery SOC, voltage, solar power
- Check for alarms
- Repeat for multiple boats
- ⏱️ 2-3 minutes of manual work every morning

### With Boat Daily Check
- One beautiful email arrives at 7 AM
- See all boats at a glance
- Battery status, solar generation, alarms
- Zero manual effort
- ⏱️ 0 minutes of work, 100% information

### Example Systems Monitored
- **Titanic** (ID: 000000) — Example boat with solar charging
- **Endeavour** (ID: 000001) — Example boat with AC power

### Broader Community Value
Boat Daily Check solves this problem for anyone with Victron power systems:
- Live-aboards who monitor their home daily
- RV adventurers tracking power on remote trips
- Fishing charter operators managing multiple boats
- Off-grid cabin owners with solar systems
- Tiny home builders automating their setup

The skill is open-source, well-documented, and MIT-licensed so the entire Victron community can benefit.

## Requirements

- **Python** 3.7+
- **Libraries**: `requests`
  ```bash
  pip install requests
  ```
- **Victron VRM API Token** (free, from https://vrm.victronenergy.com/access-tokens)
- **OpenClaw** (for cron scheduling, optional)

## License

MIT License — Feel free to use, modify, and distribute.

## Support

- **VRM API Docs**: https://vrm-api-docs.victronenergy.com/
- **Victron Community**: https://community.victronenergy.com/
- **GitHub Reference**: https://github.com/dirkjanfaber/victron-vrm-api
- **Report Issues**: Open an issue on GitHub

---

## Get Started in 5 Minutes

1. Get your VRM API token: https://vrm.victronenergy.com/access-tokens
2. Find your installation ID (from VRM URL)
3. Install: `clawhub install boat-daily-check` or `git clone` this repo
4. Configure with your boat IDs
5. Run: `python3 scripts/boat-email-report.py`
6. Enjoy beautiful daily emails!

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup.

---

## Why This Matters

A production-grade monitoring skill for one of the most popular marine power systems. 

Boat owners worldwide can now automate their daily power system checks instead of logging into VRM manually. This solves a real problem, has clean code, great documentation, and is licensed for sharing. 

**The Victron community deserves tools that work as hard as their power systems do.** ⚡

---

**Built for boat owners, RV adventurers, and anyone monitoring Victron power systems.**

Fair winds! ⛵
