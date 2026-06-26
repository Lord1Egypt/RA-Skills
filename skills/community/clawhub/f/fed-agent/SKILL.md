# Fed Agent Skill - FED-AGENT-SKILL-001

## Purpose
Acts as an economic analyst to track Federal Reserve policy movements, interest rate decisions, inflation data (CPI/PCE), and key speeches from Fed officials. Provides clean, factual summaries of:
1. **FOMC meetings** (date, voting outcome, rate decision)
2. **Interest rates & monetary policy** (current target range, recent adjustments)
3. **Inflation metrics** (CPI, Core CPI, PCE with year-over-year changes)
4. **Fed Chair speeches** (Jerome Powell remarks on inflation, employment, economic outlook)
5. **Dot Plot projections** (fed rate path as of most recent FOMC meeting)

## What This Skill Does
1. **Polls** Federal Reserve data sources for latest policy information
2. **Extracts** factual economic indicators and policy decisions
3. **Formats** output as clean markdown table with timestamps
4. **Outputs** directly to this chat (not posted externally)

---

## Quick Start (One Command - Print Output Here)

```powershell
python "C:\Users\Legion 5i Pro\.openclaw\workspace\skills\fed-agent\scripts\track_fed_policy.py" --output-file ""
```

### Example Full Command
```powershell
python "C:\Users\Legion 5i Pro\.openclaw\workspace\skills\fed-agent\scripts\track_fed_policy.py" --output-file ""
```

**Note:** `--output-file ""` means **print output directly to this chat**. Use `--output-file "fed_data.md"` to save to file instead.

---

## Output Format (Markdown Table)

When `--output-file ""`:

```markdown
## Federal Reserve Policy Tracker

| Metric | Value/Status | Date/Time | Source |
|--------|--------------|-----------|--------|
| Current Fed Funds Rate | 4.25% - 4.50% (No Change) | Mar 16, 2026 09:00 AM EST | FOMC Statement |
| Target Range | 4.25-4.50% (Unchanged) | Mar 15, 2026 | FOMC Press Release |
| Inflation (CPI YoY) | 2.8% (Down 0.3 pp from prior) | Feb 13, 2026 | BLS Data |
| Core CPI YoY | 3.1% (Down 0.5 pp) | Feb 13, 2026 | BLS Data |
| Fed Chair Speech | "Tightening pace depends on inflation trajectory" | Mar 14, 2026 15:00 EST | H.19/2.07 |
| Dot Plot (Median Rate Path) | 3.8% - 4.4% over next cycle | Mar 14, 2026 | FOMC Statement |
```

---

## Advanced Options

### Option 1: Add Inflation Data
```powershell
python "...\track_fed_policy.py" --output-file "" --with-inflation
```

### Option 2: Add Employment Data
```powershell
python "...\track_fed_policy.py" --output-file "" --with-employment
```

### Option 3: Save to Markdown File
```powershell
python "...\track_fed_policy.py" --output-file "fed_daily.md"
```

### Option 4: JSON Output (For Automation)
```powershell
python "...\track_fed_policy.py" --output-mode json
```

---

## Example Session

```powershell
$ python "C:\Users\Legion 5i Pro\.openclaw\workspace\skills\fed-agent\scripts\track_fed_policy.py" --output-file ""
[+] Federal Reserve Tracker v1.0 executed successfully.
[+] Output sent to console (print here).

## Federal Reserve Policy Tracker

| Metric | Value/Status | Date/Time | Source |
|--------|--------------|-----------|--------|
| Current Fed Funds Rate | 4.25% - 4.50% (No Change) | Mar 16, 2026 09:00 AM EST | FOMC Statement |
| ... | ... | ... | ... |
```

**✅ Success!** Output printed directly to chat interface.

---

## How It Works

### What Data Is Being Used?
This skill uses **publicly available Federal Reserve data**:
1. [FOMC Statements](https://www.federalreserve.gov/monetarypolicy/fomc.htm)
2. [Interest Rate Decisions](https://www.federalreserve.gov/financialservices/moneymarket/index.htm)
3. [Inflation Reports (CPI/PCE)](https://www.bls.gov/cpi/inflatedata.htm)
4. [Employment Data](https://www.bls.gov/emp/)
5. [Federal Reserve Speeches](https://www.federalreserve.gov/speeches/)

### What Skills Are Used?
- **poll_polymarket_markets.py** (for market context if needed)
- **summarize_news.py** (for economic news aggregation)
- **fetch_econ_data.py** (for direct data scraping)

---

## Troubleshooting

### No Output?
1. Check that `--output-file ""` is used (empty string)
2. Verify PowerShell compatibility with Python 3.8+
3. Ensure no other process is blocking console output

### Missing Data Points?
- Run with specific flags: `--with-inflation --with-employment`
- Some data may be unavailable due to delayed releases

---

## Configuration (Optional)
Edit `scripts/track_fed_policy.py` in the root folder if you need to customize:
- Default time periods for data retrieval
- API endpoints for polling
- Output formatting preferences

---

## Example Commands

### Basic Execution
```powershell
python "C:\Users\Legion 5i Pro\.openclaw\workspace\skills\fed-agent\scripts\track_fed_policy.py" --output-file ""
```

### With Inflation Data
```powershell
python "...\track_fed_policy.py" --output-file "" --with-inflation
```

### Save to File
```powershell
python "...\track_fed_policy.py" --output-file "fed_report.md"
```

---

## Related Skills
- **cnbc-geopolitics-fetcher** - Economic news from CNBC
- **polymarket-analyst** - Geopolitical market polling
- **bloomberg-economic-tracker** - Market data aggregation

---

**Status:** ✅ Ready for execution  
**Last Updated:** 2026-03-15  
**Skill Version:** FED-AGENT-SKILL-001
