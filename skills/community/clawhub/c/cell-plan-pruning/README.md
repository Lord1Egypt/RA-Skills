# cell-plan-pruning

**Audit your phone bill against real usage and compute honest pruning savings.**
Classifies every line and add-on KEEP / DOWNGRADE / DROP / SWITCH, matches each
line's data reality to the right plan shape, runs device-insurance breakeven math
per phone, and totals the independently-executable annual savings.

## The real-world problem

The average US household pays **$100–$250/month for mobile service** that its actual
usage doesn't justify. Fat accumulates silently:

- "Unlimited" buckets sized for imaginary usage while the median line uses under 10 GB
- $15–$25/month device insurance on 2.5-year-old phones worth $250 — where 18 months
  of premium + deductible exceeds the phone's value
- Per-line access fees and add-ons (cloud, premium voicemail) that MVNOs include free
- The upgrade treadmill: "free" phones financed into the plan, locking the exit

Switching feels risky, so inertia wins for years. This skill turns the decision into
line-item math: what each action saves, and what switching actually costs.

## What it does

| Capability | Detail |
|---|---|
| Bill audit | every recurring line + add-on classified with $/yr impact |
| Usage → plan shape | per-line 3–6-mo average data mapped to LIGHT/MEDIUM/HEAVY with the right plan tier |
| Insurance breakeven | premium×18 + deductible vs 40% of phone value, age-triggered DROP rule |
| MVNO switch math | all-in (tax-adjusted) comparison, per line, with exit-cost gates |
| Taxes/fees honesty | postpaid sticker vs all-in comparison both directions |

## Quick start

```bash
python3 scripts/plan_pruner.py --demo
python3 scripts/plan_pruner.py --bill scripts/bill.example.json
python3 scripts/plan_pruner.py --insurance 30 320 17 200
```

Stdlib only.

## Example

A 4-line family at $327/mo all-in (2 adults ~10 GB, 1 teen 26 GB, grandma 1.5 GB,
insurance ×2, cloud + voicemail add-ons). The audit:

- 2 adult MEDIUM lines → mid-tier MVNO: **−$988/yr**
- teen's HEAVY line → MVNO unlimited tier: **−$302/yr**
- grandma's LIGHT line → capped plan: **−$355/yr**
- insurance ×2 (both fail the 40%-of-value test): **−$481/yr**
- cloud + premium voicemail add-ons: DROP: **−$212/yr**

**Total $2,338/yr saved → bill drops to ~$132/mo** — each action independently
executable.

## Why it matters

Phone service is a top-10 household recurring expense, paid monthly and reviewed
approximately never. The pruning actions here require no behavior change — same
towers (MVNOs ride host networks), same numbers (porting), same phones — just less
money leaving. Typical finds: $500–$2,000/yr per household.
