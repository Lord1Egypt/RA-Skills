---
name: "ashare-fast-watcher"
description: "A-Share millisecond-level market data watcher using Tencent direct API."
version: "1.0.0"
---

# Ashare Fast Watcher

A high-performance skill to monitor A-Share market movements.

## Actions

### get_market_snapshot
Fetches real-time price, change, volume, and Level-1 quotes.
#### Parameters
- `codes`: (Required) String. Stock codes with prefix, e.g., "sh600519,sz000001".

### check_volatility
Detects sudden volume spikes or price movements.
#### Parameters
- `code`: (Required) String. Single stock code.
