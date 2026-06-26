---
name: clawcost
description: Track OpenClaw agent costs. Check daily/weekly spending and model breakdown.
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins:
        - python3
---

# ClawCost

Run this command:
```bash
python3 {baseDir}/scripts/clawcost.py --budget 10
```

## Output
JSON with:
- `balance`: {initial, spent, remaining} or null
- `today`: cost, budget, pct
- `week`: total week cost
- `total`: all-time cost, tokens
- `models`: breakdown all-time
- `models_today`: breakdown for today only
- `daily`: cost per day (last 7 days)

## Set Balance
User sets INITIAL balance (when they top up):
```bash
python3 {baseDir}/scripts/clawcost.py --set-balance 50.00
```
Remaining auto-calculates: initial - total_spent

## How to Present

**Tone:** Friendly, like a helpful assistant checking expenses. Use emojis sparingly.

**Format:** Use tree-style (├ └) for clean output:
```
💰 clawleaks
├ Balance $42.98 / $50 remaining
├ Today   $1.36 / $10 (14%) ✅
├ Week    $7.02
└ Total   $7.02 (15.5M tok)

📈 Sonnet $3.99 (57%) • Haiku $2.06 (29%) • Opus $0.97 (14%)
```

**Rules:**
- Skip $0 models
- Add brief insight ("Opus only 14%, nice savings 👍")

**Alerts (IMPORTANT):**
- If `today.pct` > 80%: Start with ⚠️ **"Warning: Daily budget {pct}% used!"**
- If `today.pct` > 100%: Start with 🚨 **"OVER BUDGET! ${cost} spent"**
- If `balance.remaining` < 5: Warn "💸 Low balance: ${remaining} left"
- If `balance` is null: Suggest "Set initial balance with --set-balance"
- If budget is fine: End with ✅

**Contextual:**
- Quick question → short answer
- Wants detail → full breakdown + daily
- Over budget → always show warning first, suggest switching to Haiku
