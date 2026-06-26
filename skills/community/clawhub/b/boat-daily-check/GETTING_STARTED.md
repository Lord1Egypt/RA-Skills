# Getting Started with Boat Daily Check

Quick start guide to get monitoring your Victron power systems in 5 minutes.

## Prerequisites

- Python 3.7+
- Victron VRM account (free): https://vrm.victronenergy.com
- OpenClaw (optional, for automated emails)

## Step 1: Get Your VRM API Token

1. Visit https://vrm.victronenergy.com/access-tokens
2. Click "Create new token"
3. Name it something like `boat-daily-check`
4. Copy the token (save somewhere safe)

## Step 2: Find Your Installation ID

1. Log into https://vrm.victronenergy.com
2. Click on your system
3. Look at the URL: `https://vrm.victronenergy.com/installation/YOUR_ID/dashboard`
4. Copy the ID (the number after `/installation/`)

## Step 3: Install Boat Daily Check

### Option A: Via ClawHub (Recommended)
```bash
npm install -g clawhub
clawhub install boat-daily-check
```

### Option B: From GitHub
```bash
git clone https://github.com/lkilpatrick/boat-daily-check.git
cd boat-daily-check
pip install -r requirements.txt
```

## Step 4: Configure Your Boats

Edit `scripts/boat-email-report.py` and update:

```python
VRM_TOKEN = os.environ.get("VRM_TOKEN", "YOUR_TOKEN_HERE")

INSTALLATIONS = {
    "boat1": {
        "id": YOUR_INSTALLATION_ID,  # Replace with your ID
        "name": "My Boat",
        "batteryInstance": 279,
    }
}
```

Or set environment variable:
```bash
export VRM_TOKEN="your-token-here"
python3 scripts/boat-email-report.py
```

## Step 5: Run It!

```bash
python3 scripts/boat-email-report.py
```

You'll get:
- `out/boat-daily-email.html` — Beautiful email report
- `out/boat-status.json` — Structured data
- `out/boat-status.csv` — Spreadsheet-friendly export

## Step 6: Automate (Optional)

### With OpenClaw
```bash
openclaw cron add -j '{
  "name": "boat-daily-check",
  "schedule": {"kind": "cron", "expr": "0 7 * * *"},
  "payload": {
    "kind": "agentTurn",
    "message": "python3 /path/to/boat-email-report.py"
  },
  "sessionTarget": "isolated"
}'
```

### With crontab
```bash
0 7 * * * cd /path/to/boat-daily-check && python3 scripts/boat-email-report.py >> cron.log 2>&1
```

### With systemd Timer
Create `/etc/systemd/system/boat-daily-check.service`:
```ini
[Unit]
Description=Boat Daily Check - Victron Monitoring
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/boat-daily-check/scripts/boat-email-report.py
StandardOutput=journal
StandardError=journal
User=youruser

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### "ModuleNotFoundError: requests"
```bash
pip install requests
```

### "Child 'BatterySummary' not found"
- Check your installation ID is correct
- Verify SmartShunt is online in VRM dashboard

### No data in email
- Verify VRM_TOKEN is correct
- Check INSTALLATIONS dict has your boat's ID
- Run manually to see errors: `python3 scripts/boat-email-report.py`

### "Connection refused"
- Check internet connection
- VRM API might be down (rare)
- Check your firewall isn't blocking vrmapi.victronenergy.com

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [SKILL.md](SKILL.md) for detailed API info
- See [references/](references/) for attribute codes and API patterns
- Customize the HTML template for your style

## Support

- VRM API Docs: https://vrm-api-docs.victronenergy.com/
- Victron Community: https://community.victronenergy.com/
- GitHub Issues: https://github.com/lkilpatrick/boat-daily-check/issues

---

Ready to monitor your boat's power system? You've got this! ⛵
