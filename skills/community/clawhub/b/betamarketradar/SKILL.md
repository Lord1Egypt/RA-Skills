---
name: market-radar
description: Real-time market scanning and alert system. Monitors SPX, major indices, VIX, and key crypto prices. Generates alerts when significant levels are crossed.
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: [python3]
    always: false
---

# Market Radar

Real-time market scanning and alert system. Monitors key levels, detects breakouts, and generates structured alerts.

## Usage

```bash
python3 radar.py --watch SPX,QQQ,VIX --threshold 1.5
```

## Alerts Generated

- Breakout alerts (price crosses key levels)
- VIX spike alerts (>20 = elevated risk)
- Unusual volume detection
- Sector rotation signals
