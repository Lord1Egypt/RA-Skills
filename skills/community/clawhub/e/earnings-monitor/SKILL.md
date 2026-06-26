# Daily Earnings Monitor Skill

## Trigger
Use when user wants to monitor earnings calls and create analyst reports.

## How It Works

1. **Fetch Earnings Data** - Get upcoming/recent earnings from financial API
2. **Generate Report** - Write 400-500 word analyst deep-dive
3. **Save to Obsidian** - Save in `Stock Archive/{TICKER}/` folder
4. **Update Notion** - Add entry to earnings database
5. **Alert via Telegram** - Notify user of new report

## Configuration Required

Edit `/root/.openclaw/skills/earnings-monitor/scripts/config.py`:
- `OBSIDIAN_VAULT_PATH` - Path to Obsidian vault on your Mac
- `NOTION_API_KEY` - Your Notion API key
- `NOTION_DATABASE_ID` - Database ID for earnings tracker
- `STOCKS_TO_MONITOR` - List of tickers to track

## Output

- Obsidian: `Stock Archive/{TICKER}/{DATE} - {TICKER} Earnings.md`
- Notion: New row in database with all columns filled
- Telegram: Alert with report summary
