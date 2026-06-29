---
name: ad-budget-governor
description: Cross-platform rolling ad-spend cap that blocks overspend across multiple ad platforms combined, not just per-platform daily limits. Fails closed on unreadable spend data.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Ad Budget Governor

Most per-platform ad tools (Meta, TikTok, Google, etc.) only enforce their
own daily spend cap. If your agent runs ad spend across more than one
platform, none of them know about each other — total combined spend can
exceed what you actually intended even when every individual platform
"cap" is technically respected.

This skill adds one rolling-window cap that sums spend across **all**
platforms you configure, and blocks any spend action that would push the
combined total over your limit — regardless of which platform is asking.

## Why fail-closed matters

If the spend ledger for a platform is corrupted, missing in an unexpected
way, or fails to parse, this skill treats that platform's spend as
**unknown**, not zero, and blocks new spend until it's resolved. A governor
that silently assumes "unreadable = $0 spent" will let real overspend
through at exactly the moment something is already wrong. This is the
single most important property of this skill — don't change it.

## Setup

1. Copy `ad_budget_governor.py` into your project.
2. Edit `LEDGER_PATHS` to point at your own platform spend-tracking files.
   Each ledger is a JSON file containing a list of records shaped like:
   ```json
   {"timestamp": "2026-06-22T14:00:00Z", "amount_usd": 12.50}
   ```
   Extra fields are ignored. If your platform wrapper doesn't already log
   spend in this shape, add that logging before wiring this in.
3. Call `check_rolling_budget(amount_usd)` before every spend action, on
   every platform:
   ```python
   from ad_budget_governor import check_rolling_budget

   ok, reason = check_rolling_budget(amount_usd=25.00)
   if not ok:
       # do not spend — surface `reason` to the operator
       ...
   ```
4. Set your cap (defaults to $0 — intentionally, so nothing spends before
   a real number is chosen):
   ```python
   from ad_budget_governor import set_cap
   set_cap(300.0, note="initial cap")
   ```

## API

| Function | Returns |
|---|---|
| `check_rolling_budget(amount_usd)` | `(ok: bool, reason: str \| None)` |
| `rolling_spend_usd(window_days=30)` | `(total: float, had_read_error: bool)` |
| `get_status()` | dict with cap, spent, remaining, at_cap, ledger_read_error |
| `set_cap(new_cap_usd, note="")` | updated status dict |

## Tested against

Built and verified in production governing real Meta + TikTok ad spend for
a live marketing campaign before being generalized for publication here.
