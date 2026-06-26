---
name: boat-daily-check
description: Monitor Victron Energy power systems and generate beautiful daily email reports with battery status, solar generation, and active alarms. Integrates with Victron VRM API to fetch real-time metrics for multiple installations and sends formatted HTML emails. Perfect for boat owners, RV enthusiasts, and off-grid solar systems.
---

# Boat Daily Check — Victron VRM API Monitor

Monitor your Victron power systems with automated daily reports. Fetch real-time battery state of charge, voltage, current, solar generation, and active alarms from the Victron VRM API, then deliver beautifully formatted HTML emails showing status of all your installations.

## Overview

This skill:
- 📊 Fetches live power system metrics from Victron VRM API
- 📧 Generates professional HTML email reports
- ⚓ Supports multiple installations (boats, RVs, homes)
- 🎨 Beautiful, responsive email design
- 🔄 Integrates seamlessly with OpenClaw cron jobs
- 📱 Mobile-friendly HTML output

## What You'll Get

Each morning, a clean HTML email with:
- **Battery Status**: SOC %, voltage, current, temperature
- **Solar Data**: Power, today's yield, max charge, PV voltage
- **Inverter/AC Info**: Input voltage, status (for grid/shore power)
- **Active Alarms**: Real-time alerts from your system
- **Hardware Status**: Gateway version, last contact time
- **Dashboard Links**: Direct links to VRM dashboards for quick access

## Setup

### 1. Get Your Victron VRM API Token

1. Visit https://vrm.victronenergy.com/access-tokens
2. Create a new access token
3. Copy the token (you'll need this for configuration)

### 2. Find Your Installation IDs

Each Victron system has an installation ID visible in the VRM URL:
```
https://vrm.victronenergy.com/installation/000000/dashboard
                                         ^^^^^^
                                    Installation ID
```

### 3. Identify Your SmartShunt Instance

The skill uses the SmartShunt (battery monitor) to fetch battery data. Find its instance number:
- Check your VRM diagnostics or alarms endpoint
- Default instance is usually `279` (adjust if yours differs)

### 4. Configure Your Installation

Edit the Python script with your details:

```bash
vim /home/jeanclaude/.openclaw/workspace/skills/boat-daily-check/scripts/boat-email-report.py
```

Update these variables:
```python
VRM_TOKEN = "your-token-here"

INSTALLATIONS = {
    "boat1": {
        "id": 000000,           # Your installation ID
        "name": "Titanic",  # Display name
        "batteryInstance": 279,  # SmartShunt instance number
    },
    "boat2": {
        "id": 000001,
        "name": "Endeavour",
        "batteryInstance": 279,
    }
}
```

## Usage

### Generate a Report Now

```bash
python3 /home/jeanclaude/.openclaw/workspace/skills/boat-daily-check/scripts/boat-email-report.py
```

This generates:
- **HTML Email**: `out/boat-daily-email.html`
- **JSON Data**: `out/boat-status.json`
- **CSV Export**: `out/boat-status.csv`

### Integrate with OpenClaw Cron

Add to your morning email report (or standalone):

```bash
openclaw cron add -j '{
  "name": "boat-daily-check",
  "schedule": {"kind": "cron", "expr": "0 7 * * *", "tz": "America/Los_Angeles"},
  "payload": {
    "kind": "agentTurn",
    "message": "Run boat power system check: python3 /path/to/boat-email-report.py"
  },
  "delivery": {"mode": "announce"},
  "sessionTarget": "isolated"
}'
```

Or embed in an existing job to include boat status with fishing/weather reports.

## API Reference

The skill queries the Victron VRM API v2:

### Endpoint: Battery Summary
```
GET /v2/installations/{id}/widgets/BatterySummary/latest?instance={instance}
```

Returns: SOC%, voltage, current, temperature, time to go, and alarm states.

### Endpoint: Diagnostics
```
GET /v2/installations/{id}/diagnostics
```

Returns: All device metadata including solar charger power, inverter status, etc.

### Endpoint: Alarms
```
GET /v2/installations/{id}/alarms?limit=10
```

Returns: Active alarms with details and device information.

**Authentication**: All requests use `X-Authorization: Token {your-token}`

**Rate Limits**: VRM API has reasonable rate limits (~10 req/sec). The daily script respects these.

## Files

```
boat-daily-check/
├── SKILL.md (this file)
├── scripts/
│   └── boat-email-report.py       # Main data collection + HTML generation
├── references/
│   ├── victron_attributes.md      # Victron attribute code reference
│   └── vrm_api_guide.md           # VRM API quick reference
├── out/
│   ├── boat-daily-email.html      # Generated email (latest run)
│   ├── boat-status.json           # JSON data export
│   └── boat-status.csv            # CSV export
└── templates/ (optional)
    └── boat-email-template.html   # Email template (customizable)
```

## Customization

### Change Email Recipients

Edit `boat-email-report.py` and modify the email sending logic:

```python
# Change recipient email
recipients = ["your-email@example.com"]
```

### Customize HTML Template

The email template uses Handlebars-style placeholders. Edit the HTML section in the Python script:

```python
html = html.replace("{{pitterPatter.battery.soc}}", f"{value}%")
```

Or create a custom template file and modify the script to load it.

### Add More Installations

Add entries to the `INSTALLATIONS` dict:

```python
"boat3": {
    "id": 999999,
    "name": "My Third Boat",
    "batteryInstance": 279,
}
```

Then update the report generation logic to include your new installation.

### Modify Metric Selection

Pick different metrics from the Victron widget response. Edit the battery data extraction:

```python
def fetch_battery_data(installation_id, instance):
    # Returns: soc, voltage, current, temp
    # Add fields like: time_to_go, mid_voltage, etc.
```

## Troubleshooting

### "Child 'BatterySummary' not found"
- Check that your installation ID is correct
- Verify the SmartShunt instance number

### Missing solar/inverter data
- Run `python3 boat-email-report.py` manually to debug
- Check the JSON output for missing fields
- Verify your devices are online in VRM

### Email not sending
- Ensure OpenClaw cron job is enabled
- Check delivery mode: `"delivery": {"mode": "announce"}`
- Verify recipient email is correct

### Empty data in email
- Check VRM API token is valid
- Confirm installation IDs are correct
- Verify SmartShunt instance number

## Performance

- **Data fetch time**: ~5-10 seconds (3 API calls per installation)
- **HTML generation**: ~1 second
- **Email delivery**: Handled by OpenClaw (async)
- **Total execution**: <30 seconds for 2 installations

## Requirements

- Python 3.7+
- `requests` library (pip install requests)
- Victron VRM API token with read access
- OpenClaw cron job support (for scheduling)

## Limitations

- VRM API has ~10 req/sec rate limit
- Historical data not available (only latest values)
- Some widget types not yet supported (add via custom implementation)
- Email delivery depends on OpenClaw email infrastructure

## Next Steps

1. ✅ Get your VRM API token
2. ✅ Find your installation IDs and battery instance numbers
3. ✅ Update the Python script with your details
4. ✅ Test with: `python3 boat-email-report.py`
5. ✅ Set up a cron job for daily automated reports

## Support & Contributions

- VRM API Docs: https://vrm-api-docs.victronenergy.com/
- Victron Community: https://community.victronenergy.com/
- GitHub Repo: https://github.com/dirkjanfaber/victron-vrm-api (reference implementation)

## License

This skill is open source. Feel free to fork, modify, and share!
