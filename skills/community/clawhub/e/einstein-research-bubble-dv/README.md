# Market Bubble Detector

Data-driven market bubble risk assessment using a revised quantitative framework with strict objectivity criteria.

## Description

Market Bubble Detector evaluates current bubble risk using a two-phase process: first, mandatory quantitative data collection across put/call ratios, VIX, margin debt, breadth, and IPO activity; second, limited qualitative adjustments based on measurable evidence. The framework produces a risk score (0-10+) with specific investment guidance for each phase.

## Key Features

- **Quantitative-first approach** - Mandatory data collection before evaluation
- **Seven risk phases** - From "No Concern" to "Extreme Bubble Risk"
- **Strict qualitative limits** - Max +3 points for qualitative factors (down from +5)
- **Confirmation bias prevention** - Explicit checklist to avoid over-scoring
- **Clear thresholds** - Specific numerical criteria for each indicator
- **Actionable guidance** - Investment recommendations for each risk phase
- **Multiple data sources** - CBOE, Yahoo Finance, FINRA, IPO calendars

## Quick Start

```bash
# Install dependencies
pip install yfinance requests pandas

# Run bubble risk assessment
python3 scripts/bubble_detector.py --verbose
```

**Output:**
```
BUBBLE RISK ASSESSMENT

Phase 1: Quantitative Scoring
- Put/Call Ratio: 0.75 (1 point - complacent)
- VIX: 12.3 (1 point - extreme complacency)
- Margin Debt: +8% YoY (0 points - normal)
- Breadth: 45% above 200-day MA (0 points - healthy)
- IPO Activity: 15 IPOs last month (1 point - elevated)

Quantitative Score: 3/10

Phase 2: Qualitative Adjustment
- FOMO narratives present but not mainstream (0 points)
- No measurable evidence of "revolutionary" mania (+0 points)

Final Score: 3/10 (Caution - Early Warning)
Guidance: Trim 10-15% of riskiest positions. Maintain core holdings.
```

## What It Does NOT Do

- Does NOT predict exact market tops or crash timing
- Does NOT replace comprehensive risk management
- Does NOT evaluate individual stocks (market-level only)
- Does NOT work without recent data (requires fresh metrics)
- Does NOT account for geopolitical or macro shocks

## Requirements

- Python 3.8+
- yfinance, requests, pandas
- No API keys required (uses public data sources)
- Internet connection for data fetching

## License

MIT
