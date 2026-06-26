---
name: arrivelah
description: One-word trigger for next bus arrival to your destination
homepage: https://github.com/abhay/arrivelah
metadata: {"clawdbot":{"emoji":"🚌","requires":{"bins":["curl","jq"]},"tags":["singapore","transport","bus"]}}
---

# ArriveLah - Singapore Bus Arrivals

Get your next bus arrival with a single word.

## Usage

```
bus
```

Returns: Next bus to your saved destination with arrival time.

## Configuration

Edit `config.json` to set:
- `defaultStop`: Your usual bus stop code (e.g., "10051")
- `defaultService`: Your usual bus number (e.g., "120")
- `destination`: Where you're usually going (for display)

## API

Uses the free Arrivelah2 API (https://arrivelah2.busrouter.sg/)
No API key required.

## Example Output

```
🚌 Bus 120 → Home
⏰ Next: 2 min (Seats available)
📍 From: Blk 149 Jalan Bukit Merah
```
