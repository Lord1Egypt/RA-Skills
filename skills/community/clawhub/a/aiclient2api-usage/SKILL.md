---
name: aiclient2api-usage
description: Check AIClient2API usage statistics, quotas, and account status. Use when the user asks about AIClient2API usage, credits, quotas, subscription status, or when they want to monitor their API consumption.
---

# AIClient2API Usage Checker

Query and display AIClient2API usage statistics, including credits consumed, remaining quotas, subscription type, and expiration dates.

## Quick Start

Check current usage:

```bash
bash scripts/check_usage.sh
```

Refresh usage data:

```bash
bash scripts/refresh_usage.sh
```

Or read the usage cache file directly:

```bash
cat ~/web/AIClient-2-API/configs/usage-cache.json
```

## Usage Information

The script reads from `~/web/AIClient-2-API/configs/usage-cache.json` and displays:

- **Account information**: Email, user ID, subscription type
- **Free trial status**: Current usage, limit, expiration date
- **Monthly quota**: Credits used, limit, reset date
- **Overage policy**: Rate, cap, current charges

## Key Metrics

- **Credits**: Usage units for API calls
- **Free Trial**: Temporary promotional credits (if active)
- **Monthly Quota**: Recurring monthly allocation
- **Next Reset**: When the monthly quota refreshes

## Notes

- Usage data is cached and updated periodically by AIClient2API (every few minutes)
- The cache file is located at `~/web/AIClient-2-API/configs/usage-cache.json`
- For real-time data, access the web UI at `http://127.0.0.1:16825` (requires authentication)
- To manually trigger a refresh via Web UI:
  1. Visit `http://127.0.0.1:16825`
  2. Login with password from `configs/pwd`
  3. Navigate to Providers section and click refresh button
