# Macro Regime Detector

Detect structural market regime transitions using cross-asset ratio analysis for long-term strategic positioning.

## Description

Macro Regime Detector identifies 1-2 year structural shifts in market character by analyzing six components: market concentration (RSP/SPY), yield curve (10Y-2Y), credit conditions (HYG/LQD), size factor (IWM/SPY), equity-bond relationship (SPY/TLT correlation), and sector rotation (XLY/XLP). It classifies the current regime as Concentration, Broadening, Contraction, Inflationary, or Transitional and provides strategic positioning guidance.

## Key Features

- **Six-component analysis** - Cross-asset ratios and correlation patterns
- **Monthly frequency** - Focuses on structural shifts, not short-term noise
- **Five regime classifications** - Concentration, Broadening, Contraction, Inflationary, Transitional
- **Strategic guidance** - Asset allocation and factor tilts for each regime
- **Historical context** - Reference periods for regime identification
- **No subjective calls** - Mechanical scoring based on quantitative thresholds

## Regime Types

- **Concentration**: Mega-cap leadership, narrow market breadth, large-cap growth dominance
- **Broadening**: Expanding participation, small-cap/value rotation, cyclical strength
- **Contraction**: Credit tightening, defensive rotation, risk-off environment
- **Inflationary**: Positive stock-bond correlation, commodities outperform, rate sensitivity high
- **Transitional**: Mixed signals, unclear pattern, regime shift in progress

## Quick Start

```bash
# Install dependencies
pip install yfinance pandas

# Run regime analysis
python3 scripts/macro_regime_detector.py --api-key $FMP_API_KEY
# OR use Yahoo Finance (free)
python3 scripts/macro_regime_detector.py --source yahoo
```

**Output:**
```
MACRO REGIME ANALYSIS

Current Regime: Broadening (Score: 68/100)

Component Breakdown:
1. Market Concentration (RSP/SPY): Rising → Broadening signal
2. Yield Curve (10Y-2Y): +0.45% → Expansion bias
3. Credit Conditions (HYG/LQD): Stable → Neutral
4. Size Factor (IWM/SPY): Outperforming → Small-cap strength
5. Equity-Bond (SPY/TLT): Negative correlation → Normal regime
6. Sector Rotation (XLY/XLP): Cyclical leadership

Strategic Positioning:
- Tilt toward small-cap value
- Reduce mega-cap concentration
- Increase cyclical exposure
- Maintain equity duration bias
```

## What It Does NOT Do

- Does NOT predict short-term market movements (1-2 year horizon only)
- Does NOT provide specific stock picks
- Does NOT replace tactical risk management (use with other tools)
- Does NOT work well during extreme volatility (designed for structural shifts)
- Does NOT account for fundamental macro shocks (chart-based only)

## Requirements

- Python 3.8+
- yfinance or FMP API
- pandas
- FMP API key (optional, can use Yahoo Finance)

## License

MIT
