# Follow-Through Day Detector

Detect market bottom signals using William O'Neil's Follow-Through Day methodology with dual-index state tracking.

## Description

Follow-Through Day (FTD) Detector identifies market bottom confirmation signals that indicate when it's safe to re-enter the market after corrections. It tracks both S&P 500 and NASDAQ through a state machine (correction → rally attempt → FTD qualification) and generates a quality score (0-100) with specific exposure guidance. Complementary to market top detection—this is the offensive counterpart for timing re-entry.

## Key Features

- **Dual-index tracking** - S&P 500 and NASDAQ Composite for confirmation
- **State machine** - Correction detection → Rally attempt → FTD qualification
- **Quality scoring** - 0-100 FTD strength with volume and price action validation
- **Post-FTD monitoring** - Health checks after confirmation signal
- **Exposure guidance** - Specific recommendations for position sizing (25%, 50%, 75%, 100%)
- **Rally attempt tracking** - Detects early bounce attempts before full FTD

## Quick Start

```bash
# Install dependencies
pip install yfinance pandas

# Run FTD detector
python3 scripts/ftd_detector.py --api-key $FMP_API_KEY
# OR use Yahoo Finance (free, no key)
python3 scripts/ftd_detector.py --source yahoo
```

**Output:**
```
FOLLOW-THROUGH DAY ANALYSIS

S&P 500:
  State: FTD Confirmed (Day 4 of rally)
  FTD Quality: 85/100
  Price: +1.8% on strong volume (+15% vs avg)
  
NASDAQ:
  State: FTD Confirmed (Day 5 of rally)
  FTD Quality: 78/100
  Price: +2.1% on heavy volume (+22% vs avg)

Dual Confirmation: YES
Exposure Guidance: 75% - Strong FTD with both indices confirming
Action: Safe to increase exposure gradually
```

## What It Does NOT Do

- Does NOT predict exact bottom timing (confirms after the fact)
- Does NOT work during sideways markets (needs clear correction first)
- Does NOT replace risk management (still use stops and position sizing)
- Does NOT identify individual stock entries (market-wide signal only)
- Does NOT guarantee successful rally (provides probabilistic edge)

## Requirements

- Python 3.8+
- yfinance or FMP API access
- pandas
- FMP API key (optional, can use free Yahoo Finance)

## License

MIT
