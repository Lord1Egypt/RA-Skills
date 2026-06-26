# Theme Detector

Identify and analyze trending market themes across sectors with lifecycle maturity and direction-aware scoring.

## Description

Theme Detector identifies market themes (AI, clean energy, defense, etc.) by analyzing cross-sector momentum, volume, breadth, and narrative signals. It provides a three-dimensional assessment: Theme Heat (0-100 strength), Lifecycle Maturity (Early/Mid/Late/Exhaustion), and Confidence (Low/Medium/High). The skill distinguishes bullish themes (upward momentum) from bearish themes (downward pressure) and integrates narrative confirmation via web search.

## Key Features

- **Bullish and bearish themes** - Direction-aware scoring for uptrends and downtrends
- **Lifecycle maturity** - Identify emerging vs. crowded/exhausted themes
- **Theme heat score (0-100)** - Quantitative strength based on momentum, volume, breadth
- **ETF proliferation tracking** - More thematic ETFs = more mature/crowded trade
- **Narrative confirmation** - Web search validation of quantitative signals
- **Dual data modes** - FINVIZ Elite (fast) or public scraping (free, slower)
- **Cross-sector analysis** - Aggregate industry data to detect macro themes

## Quick Start

```bash
# Install dependencies
pip install requests beautifulsoup4 pandas

# Run theme detection (FINVIZ Elite mode)
python3 scripts/theme_detector.py \
  --finviz-elite-key $FINVIZ_ELITE_KEY \
  --output reports/

# Run theme detection (public scraping mode)
python3 scripts/theme_detector.py \
  --mode scraping \
  --output reports/

# Analyze specific theme
python3 scripts/theme_detector.py \
  --theme "Artificial Intelligence" \
  --validate-narrative
```

**Output:**
```
MARKET THEME ANALYSIS

Top Bullish Themes:
1. Artificial Intelligence (Heat: 92/100, Lifecycle: Mid, Confidence: High)
   - Sectors: Software, Semiconductors, Cloud Infrastructure
   - ETF Proliferation: 12 dedicated ETFs (moderate crowding)
   - Narrative: Strong media coverage, earnings momentum confirmed

2. Defense & Aerospace (Heat: 78/100, Lifecycle: Early, Confidence: Medium)
   - Sectors: Aerospace, Defense Contractors
   - ETF Proliferation: 3 ETFs (emerging theme)
   - Narrative: Geopolitical tensions driving demand

Top Bearish Themes:
1. Commercial Real Estate (Heat: 68/100, Lifecycle: Late, Confidence: High)
   - Sectors: REITs, Office REITs
   - Downward momentum confirmed
```

## What It Does NOT Do

- Does NOT provide individual stock picks (theme-level only)
- Does NOT predict theme duration or reversal timing
- Does NOT replace sector-specific analysis (use sector-analyst for deep dives)
- Does NOT work well during sideways markets (needs clear directional momentum)
- Does NOT account for fundamental valuations (momentum-focused)

## Requirements

- Python 3.8+
- requests, beautifulsoup4, pandas
- FINVIZ Elite subscription (optional, for fast mode)
- Web search access for narrative confirmation

## License

MIT
