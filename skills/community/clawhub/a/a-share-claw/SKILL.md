---
name: a-share-claw
description: A-share paper-trading automation workflow for MX APIs. Use when user asks to run scheduled A-share mock trading, enforce risk limits (single position cap, total exposure cap, stale-order cancellation), generate daily review, or maintain Day/Balance/Daily Return tracking.
---

# A-Share Claw

Execute this workflow for A-share paper trading with MX APIs.

## Steps

1. Ensure environment:
   - `MX_APIKEY` is set.
   - `MX_API_URL` defaults to `https://mkapi2.dfcfs.com/finskillshub`.

2. Ensure runtime files under workspace:
   - `mx_autotrade/config.json`
   - `mx_autotrade/run_autotrade.py`
   - `mx_autotrade/daily_review.py`

3. Ensure schedules (trading days):
   - `09:24` run strategy
   - `10:30` run strategy
   - `14:30` run strategy (risk-first)
   - `15:10` run daily review

4. Enforce risk rules:
   - Single symbol position cap (`maxPositionPerStock`, default 15%)
   - Total exposure cap (`maxTotalPosition`, default 60%)
   - Auto-cancel stale pending orders (>20 min)

5. Daily output:
   - Produce review JSON (`mx_autotrade/reviews/review-YYYY-MM-DD.json`)
   - Update README day table with: `Day | Balance | Daily Return` (no Day0)

## Quick run commands

```bash
python3 mx_autotrade/run_autotrade.py
python3 mx_autotrade/daily_review.py
```

## Notes

- Fail safely: if account is not bound, stop and report clearly.
- Prefer discipline over trade frequency.
