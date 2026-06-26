# CNBC Geopolitics Fetcher Skill

## Purpose
Fetches latest CNBC geopolitical news articles, extracts complete factual data (NO truncation), and posts each article individually to Discord with enhanced analyst/Polymarket-relevant context.

## What This Skill Does
1. **Scrapes** 5 latest CNBC articles on geopolitics (Iran, Middle East, oil markets, energy policy)
2. **Extracts** complete sentences - NO truncation or summarization
3. **Identifies** analyst forecasts and Polymarket-relevant data (odds, probabilities, market pricing)
4. **Posts** each article as a separate Discord message (1-by-1, not batched)
5. **Auto-splits** long messages to fit Discord's 2000-character limit

---

## Quick Start (One Command)
Run this from workspace root:

```powershell
python "C:\Users\Legion 5i Pro\.openclaw\workspace\skills\cnbc-geopolitics-fetcher\scripts\fetch_cnbc_geopolitics.py" --webhook "YOUR_DISCORD_WEBHOOK_URL" --verbose
```

### Required Arguments
- `--webhook`: Discord webhook URL (required)
- `--config`: Path to config file containing webhook (alternative to --webhook)
- `--count`: Number of articles to fetch (default: 5)
- `--verbose`: Show detailed extraction output

### Example (Full Command)
```powershell
python "C:\Users\Legion 5i Pro\.openclaw\workspace\skills\cnbc-geopolitics-fetcher\scripts\fetch_cnbc_geopolitics.py" --webhook "https://discord.com/api/webhooks/1482043765471445333/-cHOLCqBtvU_Wua8STfoINes7J0pFNFsXB27EJ3f8F7BklC5P_OkIGAx2HQLDPZe1bNJ" --count 5 --verbose
```

---

## Configuration

### Option 1: Command-Line Webhook
Pass webhook URL directly:
```powershell
python fetch_cnbc_geopolitics.py --webhook "https://discord.com/api/webhooks/..."
```

### Option 2: Config File
Create `references/config.md` with:
```markdown
## Discord Webhook
https://discord.com/api/webhooks/1482043765471445333/-cHOLCqBtvU_Wua8STfoINes7J0pFNFsXB27EJ3f8F7BklC5P_OkIGAx2HQLDPZe1bNJ
```

Then run:
```powershell
python fetch_cnbc_geopolitics.py --config "C:\Users\Legion 5i Pro\.openclaw\workspace\skills\cnbc-geopolitics-fetcher\references\config.md"
```

---

## Output Format (Discord Message)

Each article posts as:

```markdown
### Article

**[Full Article Title]**

**URL:** https://www.cnbc.com/2026/03/13/...

**Market Impact:** Energy: [complete sentence about oil/energy]; Stocks: [complete sentence about markets]; Analyst: [forecast/prediction]

**Hard Facts:**
  - Official: [complete quoted statement from official]
  - Action: [complete sentence describing military/diplomatic action]
  - Data: [complete sentence with numbers/statistics]
  - Timeline: [complete sentence with dates/deadlines]
  - Analyst: [complete sentence with forecast/market prediction]

*(Raw data - no editorial analysis)*
```

### Key Features
- **Complete sentences** - NO truncation (removed all length limits)
- **Analyst/Polymarket data** - extracts forecasts, odds, probabilities, market pricing
- **One-by-one posting** - each article is a separate Discord message
- **Auto-split** - messages >2000 chars split into parts automatically

---

## How It Works (Architecture)

### 1. Article Discovery
- Searches CNBC HTML for article links matching pattern: `https://www.cnbc.com/YYYY/MM/...`
- Filters out video, premium, pro, tag, section, live URLs
- Returns up to 25 unique geopolitical article URLs

### 2. Article Scraping
- Uses Scrapling (stealth headless browser) to bypass anti-bot protections
- Extracts: title, full article text, description metadata
- Falls back to regex extraction if Scrapling fails

### 3. Fact Extraction (NO Truncation)
- Splits article text into complete sentences
- Scans for 6 fact categories:
  1. **Official**: Quoted statements with attribution (said/stated/announced)
  2. **Action**: Military/diplomatic/economic actions (strike/launch/sanctions)
  3. **Data**: Numbers with units (million/billion/percent/barrel/$)
  4. **Timeline**: Dates/deadlines (by/before/after/until/expected)
  5. **Analyst**: Forecasts/predictions (forecast/expect/project/likely/recession)
  6. **Market**: Polymarket/prediction market language (odds/probability/betting)
- Returns up to 5 complete facts per article

### 4. Market Impact Extraction
- Scans for energy, stocks, currency, analyst, Polymarket sentences
- Returns complete sentences (NO length limits)
- Categories: Energy, Stocks, Currency, Analyst, Polymarket

### 5. Discord Posting
- Formats each article as markdown
- Checks message length against 2000-char Discord limit
- If too long: splits into Title+URL+Market, Facts, Disclaimer parts
- Posts each article individually (not batched)
- Small delay (0.3s) between split parts

---

## File Structure
```
skills/cnbc-geopolitics-fetcher/
├── SKILL.md                 # This documentation
├── scripts/
│   └── fetch_cnbc_geopolitics.py   # Main scraper script
└── references/
    └── config.md            # Discord webhook configuration
```

---

## Dependencies
- Python 3.x
- `scrapling` (stealth web scraping)
- `beautifulsoup4` (HTML parsing)
- `requests` (HTTP client)

Install dependencies:
```powershell
pip install scrapling beautifulsoup4 requests
```

---

## Customization Tips

### Change Article Count
```powershell
python fetch_cnbc_geopolitics.py --webhook "..." --count 10
```

### Output to File Instead of Discord
```powershell
python fetch_cnbc_geopolitics.py --output "output.md" --count 5
```

### Disable Verbose Output
Remove `--verbose` flag for cleaner console output.

---

## Troubleshooting

### Error: "can't open file"
- Quote the full path: `python "C:\path\with\spaces\script.py"`
- Use forward slashes or escape backslashes

### Error: "Discord error 400"
- Message exceeds 2000 characters
- Script should auto-split, but check format_single_article() function

### Error: "No facts extracted"
- Article may have anti-bot protection
- Check Scrapling installation: `pip install scrapling`
- Try with `--verbose` to see extraction details

### Error: "ModuleNotFoundError"
- Install dependencies: `pip install scrapling beautifulsoup4 requests`

---

## LLM Integration Notes

### For Any LLM to Use This Skill
1. **Read this SKILL.md** - understand purpose and usage
2. **Check config.md** - get webhook URL from references/config.md
3. **Run the command** - execute the Python script with proper path quoting
4. **Verify output** - check Discord for posted articles

### Key Constraints to Remember
- **NO truncation** - script extracts complete sentences only
- **One-by-one posting** - each article = separate Discord message
- **Raw facts only** - no editorial analysis or opinions
- **Polymarket-ready** - extracts analyst forecasts and prediction market data

### Example LLM Prompt
> "Fetch latest CNBC geopolitical news and post to Discord using the cnbc-geopolitics-fetcher skill."

### Expected LLM Action
1. Locate skill at: `skills/cnbc-geopolitics-fetcher/`
2. Read config: `references/config.md` for webhook URL
3. Execute:
   ```powershell
   python "skills/cnbc-geopolitics-fetcher/scripts/fetch_cnbc_geopolitics.py" --config "skills/cnbc-geopolitics-fetcher/references/config.md" --verbose
   ```
4. Confirm: "5 articles posted individually to Discord"

---

## Version History
- **v2.0** (2026-03-15): One-by-one posting, NO truncation, analyst/Polymarket extraction, auto-split long messages
- **v1.0**: Initial batched posting with truncation limits

---

## Support
- Skill location: `C:\Users\Legion 5i Pro\.openclaw\workspace\skills\cnbc-geopolitics-fetcher\`
- Script: `scripts/fetch_cnbc_geopolitics.py`
- Config: `references/config.md`
