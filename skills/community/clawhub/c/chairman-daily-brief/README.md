# Chairman Daily Brief

A daily market briefing system designed for listed company chairmen, providing executive-level market intelligence from a strategic decision-making perspective.

## Quick Start

### 1. Installation

Copy this skill to your OpenClaw skills directory:

```bash
cp -r chairman-daily-brief ~/.openclaw/skills/
```

### 2. Configuration

Copy the watchlist example:

```bash
cp config/watchlist.example.json config/watchlist.json
```

Edit `config/watchlist.json` to add companies and competitors you want to track.

### 3. Set API Key

```bash
export QVERIS_API_KEY="your-api-key-here"
```

Get your API Key from https://qveris.ai.

### 4. Run

```bash
# Generate morning report
cd ~/.openclaw/skills/chairman-daily-brief
node scripts/chairman_daily.mjs morning --symbol 600519.SS --company "Kweichow Moutai"

# Generate evening report
node scripts/chairman_daily.mjs evening --symbol 0700.HK --company "Tencent Holdings"

# Generate multi-company briefing using watchlist
node scripts/chairman_daily.mjs morning --watchlist holdings
```

## Features

### 🌅 Morning Brief
- Overnight global markets overview
- Macro policy express delivery
- Company pre-market outlook
- Industry radar
- Competitor intelligence
- Risk alerts
- Today's focus points

### 🌙 Evening Brief
- Market close overview and trading analysis
- Today's announcements summary
- Media monitoring
- Institutional activity
- Policy interpretation
- Tomorrow's strategy recommendations

## Command Reference

```bash
# Generate morning report
node scripts/chairman_daily.mjs morning --symbol <code> --company <name>

# Generate evening report
node scripts/chairman_daily.mjs evening --symbol <code> --company <name>

# Add company to watchlist
node scripts/chairman_daily.mjs watch --action add \
  --symbol 600519.SS --company "Kweichow Moutai" --role self

# Add competitor
node scripts/chairman_daily.mjs watch --action add \
  --symbol 002594.SZ --company "BYD" --role competitor --peer-group "New Energy Vehicles"

# View watchlist
node scripts/chairman_daily.mjs watch --action list
```

## Cron Jobs

Set up automated daily briefings:

```bash
# Morning 8:00 AM
openclaw cron add --name "Chairman Morning Brief" \
  --cron "0 8 * * 1-5" --tz Asia/Shanghai \
  --message "Run chairman-daily-brief to generate morning report"

# Evening 3:35 PM
openclaw cron add --name "Chairman Evening Brief" \
  --cron "35 15 * * 1-5" --tz Asia/Shanghai \
  --message "Run chairman-daily-brief to generate evening report"
```

## Data Sources

- THS iFinD
- Caidazi
- Alpha Vantage
- Finnhub
- X/Twitter Sentiment

## License

MIT
