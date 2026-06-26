# Earnings Scorecard

description: 8-dimension tone + 6 content-integrity checks for earnings releases. Triggers on "earnings", "results", "scorecard", "earnings call", "profit warning".

## Workflow

### Step 1: Frame
Confirm ticker and earnings period. Note: HK companies report half-year and full-year (not quarterly like US).

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_ticker_info(ticker=ticker)` — latest earnings data, EPS, revenue
- `get_hkex_disclosures(ticker=ticker, type="earnings", limit=5)` — earnings announcement

Then:
- `get_news_signals(ticker=ticker, limit=10)` — post-earnings analyst commentary

### Step 3: Analyze — 8 Dimensions + 6 Integrity Checks

**Tone Dimensions** (score -2 to +2):
1. Revenue guidance / beat-miss
2. Margin trajectory
3. Dividend policy signal
4. Balance sheet health
5. Management tone (cautious vs confident)
6. Macro headwind acknowledgment
7. Structural narrative consistency
8. Guidance specificity

**Content Integrity Checks** (pass/fail):
1. Numbers tie between announcement and presentation
2. Segment breakdown provided
3. Year-ago comparables restated consistently
4. Cash flow reconciliation shown
5. Related-party transactions disclosed
6. Auditor sign-off without qualification

### Step 4: Present
```
| Tone Dimension | Score (-2 to +2) | Evidence |
|----------------|------------------|----------|
| Revenue | ... | ... |
| Margins | ... | ... |
| ... | ... | ... |
| Total Tone Score | ... | ... |

| Integrity Check | Pass/Fail | Note |
|-----------------|-----------|------|
| Numbers tie | ... | ... |
| Segment breakdown | ... | ... |
| ... | ... | ... |
```

Add "HK Earnings Nuance" section:
- Half-year vs full-year reporting cadence
- Profit warning requirements under HKEX rules
- Earnings call vs analyst briefing differences

## Important Notes
- Token: respect depth setting from style.md; scorecard first, detail on request
- HK-specific: profit warnings are HKEX-mandated; check if one was issued pre-results
- Do not score dimensions without evidence from the disclosure
- Max 2 parallel calls per step
