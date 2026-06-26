# Price Monitor Template

Purpose: track price changes for specified assets or products and notify users periodically.

## Supported Monitoring Targets

- cryptocurrency
- stocks
- product prices

## Parameters

Required:
- target asset

Optional:
- price threshold
- percentage change alert

## Suggested Schedule

- hourly
- daily

## Task Behavior

1. Fetch latest price information.
2. Compare with previous values or thresholds.
3. Generate alert summary if conditions are met.

## Output

Asset
Current price
Change
Relevant link

## Delivery

Delivery handled by delivery router.
