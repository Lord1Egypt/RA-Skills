---
id: 'einstein-research-themes'
name: 'einstein-research-themes'
description: 'Detect and analyze trending market themes across sectors. Use when user
  asks about current market themes, trending sectors, sector rotation, thematic investing,
  what themes are hot or cold, or wants to identify bullish and bearish market narratives
  with lifecycle analysis.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Theme Detector

## Overview

This skill detects and ranks trending market themes by analyzing cross-sector momentum, volume, and breadth signals. It identifies both bullish (upward momentum) and bearish (downward pressure) themes, assesses lifecycle maturity (early/mid/late/exhaustion), and provides a confidence score combining quantitative data with narrative analysis.

**3-Dimensional Scoring Model:**
1. **Theme Heat** (0-100): Direction-neutral strength of the theme (momentum, volume, uptrend ratio, breadth)
2. **Lifecycle Maturity**: Stage classification (Early / Mid / Late / Exhaustion) based on duration, extremity clustering, valuation, and ETF proliferation
3. **Confidence** (Low / Medium / High): Reliability of the detection, combining quantitative breadth with narrative confirmation

**Key Features:**
- Cross-sector theme detection using FINVIZ industry data
- Direction-aware scoring (bullish and bearish themes)
- Lifecycle maturity assessment to identify crowded vs. emerging trades
- ETF proliferation scoring (more ETFs = more mature/crowded theme)
- Integration with uptrend-dashboard for 3-point evaluation
- Dual-mode operation: FINVIZ Elite (fast) or public scraping (slower, limited)
- WebSearch-based narrative confirmation for top themes

---

## When to Use This Skill

**Explicit Triggers:**
- "What market themes are trending right now?"
- "Which sectors are hot/cold?"
- "Detect current market themes"
- "What are the strongest bullish/bearish narratives?"
- "Is AI/clean energy/defense still a strong theme?"
- "Where is sector rotation heading?"
- "Show me thematic investing opportunities"

**Implicit Triggers:**
- User wants to understand broad market narrative shifts
- User is looking for thematic ETF or sector allocation ideas
- User asks about crowded trades or late-cycle themes
- User wants to know which themes are emerging vs. exhausted

**When NOT to Use:**
- Individual stock analysis (use us-stock-analysis instead)
- Specific sector deep-dive with chart reading (use sector-analyst instead)
- Portfolio rebalancing (use portfolio-manager instead)
- Dividend/income investing (use value-dividend-screener instead)

---

## Workflow

### Step 1: Verify Requirements

Check for required API keys and dependencies:

```bash
# Check for FINVIZ Elite API key (optional but recommended)
echo $FINVIZ_API_KEY

# Check for FMP API key (optional, used for valuation metrics)
echo $FMP_API_KEY
```

**Requirements:**
- **Python 3.7+** with `requests`, `beautifulsoup4`, `lxml`
- **FINVIZ Elite API key** (recommended for full industry coverage and speed)
- **FMP API key** (optional, for P/E ratio valuation data)
- Without FINVIZ Elite, the skill uses public FINVIZ scraping (limited to ~20 stocks per industry, slower rate limits)

**Installation:**
```bash
pip install requests beautifulsoup4 lxml
```

### Step 2: Execute Theme Detection Script

Run the main detection script:

```bash
python3 skills/theme-detector/scripts/theme_detector.py \
  --output-dir reports/
```

**Script Options:**
```bash
# Full run (public FINVIZ mode, no API key required)
python3 skills/theme-detector/scripts/theme_detector.py \
  --output-dir reports/

# With FINVIZ Elite API key
python3 skills/theme-detector/scripts/theme_detector.py \
  --finviz-api-key $FINVIZ_API_KEY \
  --output-dir reports/

# With FMP API key for enhanced stock data
python3 skills/theme-detector/scripts/theme_detector.py \
  --fmp-api-key $FMP_API_KEY \
  --output-dir reports/

# Custom limits
python3 skills/theme-detector/scripts/theme_detector.py \
  --max-themes 5 \
  --max-stocks-per-theme 5 \
  --output-dir reports/

# Explicit FINVIZ mode
python3 skills/theme-detector/scripts/theme_detector.py \
  --finviz-mode public \
  --output-dir reports/
```

**Expected Execution Time:**
- FINVIZ Elite mode: ~2-3 minutes (14+ themes)
- Public FINVIZ mode: ~5-8 minutes (rate-limited scraping)

### Step 3: Read and Parse Detection Results

The script generates two output files:
- `theme_detector_YYYY-MM-DD_HHMMSS.json` - Structured data for programmatic use
- `theme_detector_YYYY-MM-DD_HHMMSS.md` - Human-readable report

Read the JSON output to understand quantitative results:

```bash
# Find the latest report
ls -lt reports/theme_detector_*.json | head -1

# Read the JSON output
cat reports/theme_detector_YYYY-MM-DD_HHMMSS.json
```

### Step 4: Perform Narrative Confirmation via WebSearch

For the top 5 themes (by Theme Heat score), execute WebSearch queries to confirm narrative strength:

**Search Pattern:**
```
"[theme name] stocks market [current month] [current year]"
"[theme name] sector momentum [current month] [current year]"
```

**Evaluate narrative signals:**
- **Strong narrative**: Multiple major outlets covering the theme, analyst upgrades, policy catalysts
- **Moderate narrative**: Some coverage, mixed sentiment, no clear catalyst
- **Weak narrative**: Little coverage, or predominantly contrarian/skeptical tone

Update Confidence levels based on findings:
- Quantitative High + Narrative Strong = **High** confidence
- Quantitative High + Narrative Weak = **Medium** confidence (possible momentum divergence)
- Quantitative Low + Narrative Strong = **Medium** confidence (narrative may lead price)
- Quantitative Low + Narrative Weak = **Low** confidence

### Step 5: Analyze Results and Provide Recommendations

Cross-reference detection results with knowledge bases:

**Reference Documents to Consult:**
1. `references/cross_sector_themes.md` - Theme definitions and constituent industries
2. `references/thematic_etf_catalog.md` - ETF exposure options by theme
3. `references/theme_detection_methodology.md` - Scoring model details
4. `references/finviz_industry_codes.md` - Industry classification reference

**Analysis Framework:**

For **Hot Bullish Themes** (Heat >= 70, Direction = Bullish):
- Identify lifecycle stage (Early = opportunity, Late/Exhaustion = caution)
- List top-performing industries within the theme
- Recommend proxy ETFs for exposure
- Flag if ETF proliferation is high (crowded trade warning)

For **Hot Bearish Themes** (Heat >= 70, Direction = Bearish):
- Identify industries under pressure
- Assess if bearish momentum is accelerating or decelerating
- Recommend hedging strategies or sectors to avoid
- Note potential mean-reversion opportunities if lifecycle is Late/Exhaustion

For **Emerging Themes** (Heat 40-69, Lifecycle = Early):
- These may represent early rotation signals
- Recommend monitoring with watchlist
- Identify catalyst events that could accelerate the theme

For **Exhausted Themes** (Heat >= 60, Lifecycle = Exhaustion):
- Warn about crowded trade risk
- High ETF count confirms excessive retail participation
- Consider contrarian positioning or reducing ex
