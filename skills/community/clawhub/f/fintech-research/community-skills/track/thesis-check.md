# Thesis Check

description: Quarterly thesis review with Intact/Improved/Weakening/Broken verdict. Triggers on "thesis check", "thesis review", "conviction", "still hold".

## Workflow

### Step 1: Frame
Load stored thesis for ticker (if exists) or ask user to state it (max 1 question).
Required thesis components:
- Bull/bear case in 1-2 sentences
- Key metrics to monitor
- Stop-loss / re-evaluation triggers

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_ticker_info(ticker=ticker)` — latest financials, price, valuation
- `get_price_history(ticker=ticker, period="6mo")` — price action

Then:
- `get_ah_spread(ticker=ticker)` — if dual-listed, monitor spread change as sentiment

### Step 3: Evaluate
Score thesis on 4 pillars (Intact/Improved/Weakening/Broken):

| Pillar | Check | Verdict |
|--------|-------|---------|
| 1. Revenue/EPS trend | Trailing 2 quarters vs thesis | ... |
| 2. Valuation support | Current vs thesis entry; AH spread movement | ... |
| 3. Margin health | Gross/EBIT margin trajectory | ... |
| 4. Macro/sector tailwind | Thematic support still valid? | ... |

Overall verdict logic:
- All Intact/Improved → **Intact**
- 1 Weakening, rest Intact → **Monitoring**
- 2+ Weakening or 1 Broken → **Weakening**
- 2+ Broken → **Broken**

### Step 4: Present
```
Ticker: [TICKER] | Thesis: [BRIEF]

| Pillar | Verdict | Evidence |
|--------|---------|----------|
| Revenue/EPS | ... | ... |
| Valuation | ... | ... |
| Margins | ... | ... |
| Macro | ... | ... |

Overall: INTACT / IMPROVED / WEAKENING / BROKEN

Action: [HOLD / ADD / REDUCE / EXIT / REVIEW]
```

Add "Connect Flow Signal": if Connect holdings changed >5% in reporting period, flag as confirming/contradicting.

## Important Notes
- Token: respect depth setting from style.md; verdict first, evidence on request
- HK-specific: Connect holdings change is a strong signal; always check
- Be honest: if data is insufficient, verdict is "REVIEW — data incomplete"
- Max 2 parallel calls per step
