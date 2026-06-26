---
name: claude-usage-tracker
version: 1.0.0
description: Track Claude.ai token usage and session costs by scraping the Claude.ai
  usage dashboard. Use when you need to monitor spend or compare usage across sessions.
metadata:
  openclaw:
    emoji: 📊
    requires:
      bins:
      - python3
    network:
      outbound: true
      reason: Fetches usage data from the Claude.ai web dashboard.
---

# Skill: Claude.ai Usage Tracker
**Last used:** 2026-03-24
**Memory references:** 1
**Status:** Active

**Owner:** Becky  
**Tool:** `scripts/claude-usage-tracker.py`  
**State file:** `~/.openclaw/workspace/memory/claude-usage-tracker.json`  
**Python:** `/Users/loki/.pyenv/versions/3.14.3/bin/python3`

---

## When to Use This Skill

Activate whenever Nissan asks about:
- "How much Claude am I using?"
- "How close am I to the limit?"
- "Will I run out this week?"
- "What's my extra usage spend?"
- "How much credit do I have left?"
- "Is Sonnet nearly full?"
- Any question about claude.ai usage, limits, or billing

---

## Quick Commands

### Check current status
```bash
python3 scripts/claude-usage-tracker.py status
```
This shows: current % for session / all-models / Sonnet, extra spend, balance, Langfuse API usage.

### See next-week projection
```bash
python3 scripts/claude-usage-tracker.py project
```
Shows daily burn rate, days to exhaustion, 7-day forecast table.

### List recent snapshots
```bash
python3 scripts/claude-usage-tracker.py snapshots --last 5
```

---

## Logging a New Snapshot (when Nissan shares data)

When Nissan tells you percentages from his claude.ai dashboard:

```bash
python3 scripts/claude-usage-tracker.py log \
  --session <SESSION_PCT> \
  --all-models <ALL_MODELS_PCT> \
  --sonnet <SONNET_PCT> \
  --extra-spend <DOLLARS_SPENT> \
  --extra-limit 200 \
  --balance <BALANCE_DOLLARS> \
  --notes "<optional notes>"
```

**Optional reset timers** (minutes from now until reset):
```bash
  --reset-session <minutes>   # e.g. 213 for 3h33m
  --reset-all <minutes>       # e.g. 333 for 5h33m
  --reset-sonnet <minutes>    # e.g. 453 for 7h33m
```

**Example** (from the Mar 20 snapshot):
```bash
python3 scripts/claude-usage-tracker.py log \
  --session 2 --all-models 58 --sonnet 95 \
  --extra-spend 73.83 --extra-limit 200 \
  --balance 23.69 \
  --reset-session 213 --reset-all 333 --reset-sonnet 453 \
  --notes "promo_window"
```

After logging, always run `status` to confirm and share the output with Nissan.

---

## Answering "Best Guess for Next Week"

1. Run `python3 scripts/claude-usage-tracker.py project`
2. Read the **7-day projection table** — this shows projected % per day
3. Check **confidence level** — tell Nissan if it's LOW/VERY LOW (needs more snapshots)
4. Note: Projections during the **promo window (Mar 13–27)** are promo-corrected — they reflect % of the *normal* baseline limit, not the doubled promo limit

**Script for answering:**
> "Based on [N] snapshot(s), your daily burn is ~X%/day all-models and ~Y%/day Sonnet. At that rate, next week you'd end at ~Z% Sonnet. [Confidence: LOW — I need more data points over different days to refine this.]"

---

## ⚠️ Risk Flags — What to Tell Nissan

### Balance low + auto-reload OFF
**This is the critical risk.** Extra usage charges against the prepaid balance. If balance hits $0, extra usage stops — even if the $200 monthly cap isn't reached.

Tell Nissan:
> "⚠️ Your balance is $X with auto-reload OFF. Once this hits $0, any extra usage beyond your included limits stops immediately. You should either top up your balance or enable auto-reload to avoid unexpected blocks."

Current thresholds:
- Balance < $20: 🔴 URGENT — flag immediately
- Balance $20–$50: 🟡 WARN — mention proactively

### Sonnet near limit (≥ 95%)
Tell Nissan:
> "⚠️ Sonnet weekly usage is at X%. It resets [day/time]. If you hit 100%, you can still use extra usage budget for Sonnet, but it will draw from your balance."

### All-models near limit (≥ 95%)
Same as above — when all-models hits 100%, everything stops unless extra usage kicks in.

### Extra spend cap approaching
At >80% of $200: warn that heavy use could hit the hard stop before end of month.

---

## Promo Window Handling (March 2026)

Anthropic doubled usage limits Mar 13–27, 2026 **outside peak hours**.

During the promo:
- The dashboard shows % of the *promoted* (2x) limit
- 95% during promo = ~47.5% of the *normal* limit
- The tool automatically corrects for this in projections
- Snapshots are tagged `is_promo_period: true` and promo-corrected values are stored

**After Mar 27:** Limits return to normal. The first post-promo snapshot will likely show lower absolute usage for the same work.

---

## Config Updates

If auto-reload status changes:
```bash
python3 scripts/claude-usage-tracker.py config --auto-reload true
# or
python3 scripts/claude-usage-tracker.py config --auto-reload false
```

After promo ends:
```bash
python3 scripts/claude-usage-tracker.py config --set-promo false
```

---

## Calibration Notes

**More snapshots = better projections.** Priority asks for Nissan:
1. Capture a snapshot right after a weekly reset (~0% starting point)
2. Capture after a heavy usage day (25%+)
3. These two give us the true daily burn rate with high confidence

Until we have 3+ multi-day snapshots, always caveat projections as LOW confidence.

---

## Data Sources

| Signal | What it tracks | Reset |
|---|---|---|
| Session % | 5-hour rolling window | Rolling (5h) |
| All-models % | Across all Claude models, weekly | Weekly (Thu ~14:00 AEST) |
| Sonnet % | Sonnet 4.x models only, weekly | Weekly (Thu ~16:00 AEST) |
| Extra spend | Pay-as-you-go overage (API rates) | Monthly (Apr 1) |
| Balance | Prepaid credit remaining | Depletes with extra usage |
| Langfuse tokens | OpenClaw API usage (separate!) | Weekly (Fri 4pm AEST) |

**⚠️ Important:** Langfuse tracks *OpenClaw API key* usage, NOT claude.ai web usage. They are separate but may correlate (active project weeks = both go up).
