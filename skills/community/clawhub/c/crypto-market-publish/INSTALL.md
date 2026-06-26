# Crypto Market Monitor - Installation

## Quick Installation

```bash
# 1. Install skill
clawhub install crypto-market

# Or manually extract to workspace
unzip crypto-market.skill -d ~/.openclaw/workspace/skills/

# 2. Create required directories
mkdir -p ~/.openclaw/workspace/crypto/{economic,scripts,data,logs}

# 3. Copy skill files to crypto workspace
cp -r ~/.openclaw/workspace/skills/crypto-market/* ~/.openclaw/workspace/crypto/

# 4. Set executable permissions
chmod +x ~/.openclaw/workspace/crypto/scripts/*.py

# 5. Create data file
touch ~/.openclaw/workspace/crypto/data/actual_data.json

echo "✅ Installation complete!"
```

## Manual Installation

```bash
# 1. Extract skill to skills directory
unzip crypto-market.skill -d ~/.openclaw/workspace/skills/

# 2. Copy files to crypto workspace
cp -r ~/.openclaw/workspace/skills/crypto-market/* ~/.openclaw/workspace/crypto/

# 3. Create directories if not exist
mkdir -p ~/.openclaw/workspace/crypto/{economic,scripts,data,logs}

# 4. Initialize data file
echo '{}' > ~/.openclaw/workspace/crypto/data/actual_data.json
```

## Path Configuration

### Default Paths
- Workspace: `~/.openclaw/workspace/crypto/`
- Scripts: `~/.openclaw/workspace/crypto/scripts/`
- Data: `~/.openclaw/workspace/crypto/data/`
- Logs: `~/.openclaw/workspace/crypto/logs/`

### Custom Paths

If you want to use a different workspace, create a config file:

```bash
# Create ~/.openclaw/crypto-config.json
cat > ~/.openclaw/crypto-config.json << 'EOF'
{
  "workspace": "/path/to/your/workspace/crypto",
  "economic_dir": "economic",
  "scripts_dir": "scripts",
  "data_dir": "data",
  "logs_dir": "logs"
}
EOF
```

## Verify Installation

```bash
# Test economic calendar
cd ~/.openclaw/workspace/crypto/economic
python3 economic_calendar.py

# Test data analysis
python3 update_economic_data.py analyze "CPI" "2.1%" "2.3%" "2.4%"

# Test monitoring
cd ~/.openclaw/workspace/crypto/scripts
python3 crypto_monitor_telegram.py
```

## Cron Jobs

```bash
# Edit crontab
crontab -e

# Add these lines (adjust paths if needed):
0 8 * * * cd ~/.openclaw/workspace/crypto/economic && /usr/bin/python3 daily_economic_report_v2.py >> ~/.openclaw/workspace/crypto/logs/economic_report.log 2>&1

*/30 * * * * cd ~/.openclaw/workspace/crypto/scripts && /usr/bin/python3 crypto_monitor_telegram.py >> ~/.openclaw/workspace/crypto/logs/crypto_monitor.log 2>&1
```

## Requirements

- Python 3.6+
- requests
- pytz
- feedparser

Install dependencies:
```bash
pip3 install requests pytz feedparser
```

## Troubleshooting

### Permission denied
```bash
chmod +x ~/.openclaw/workspace/crypto/scripts/*.py
```

### Module not found
```bash
cd ~/.openclaw/workspace/crypto/economic  # For economic modules
cd ~/.openclaw/workspace/crypto/scripts   # For monitoring scripts
```

### Path errors
- Ensure all directories exist: `mkdir -p ~/.openclaw/workspace/crypto/{economic,scripts,data,logs}`
- Check file permissions: `ls -l ~/.openclaw/workspace/crypto/`
- Verify Python path: `which python3`
