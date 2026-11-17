---
name: breakup-buddy
description: "Use when a cohabiting relationship is ending and two lives must be untangled — shared-catalog splitting (who keeps what, who owes what), shared subscription/account/service audit with per-item transfer-or-cancel actions, moving-out logistics with handoff handoff and key return, split-expense reconciliation (who owes whom the final settle-up), and a clean named-account inventory (bank, utilities, streaming, insurance, domain names) so nothing stays joint by accident. Handles the object with the worst possible emotional loading: the shared life."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [breakup, moving, shared-assets, subscriptions, life-transitions, expenses]
---

# Breakup Buddy — Cohabitation Untangler

## Overview

When a cohabiting relationship ends, the emotional work gets all the attention, but the logistical work is what actually ruins the following three months: who keeps the sofa bought together, the Netflix account still joint, the car insurance policy that auto-renews in two weeks, the utility bill in one person's name at an address they no longer live at. Shared lives accrete joint objects and joint accounts silently; unwinding them requires decisions about hundreds of items and dozens of accounts while both parties are at their worst negotiation capacity.

This skill is a **structured untangling system**:

1. **Shared catalog** — every shared physical item with purchase price, date, purchaser, and current condition; splitting proceeds by agreed rules instead of vibes.
2. **Account audit** — inventory of shared digital accounts/subscriptions/services, each flagged KEEP-MINE / TRANSFER / CANCEL / DISPUTE with renewal dates so nothing auto-renews into next year.
3. **Split-expense settle-up** — final reconciliation of who paid for what since move-in or since an agreed cutoff; net one-payment settle instead of relitigating history.
4. **Moving logistics** — who moves when, what handoffs happen, deposit recovery, key/ access device return.
5. **Legal-adjacent checklist** — lease-breaking steps, name changes on utilities, forwarding mail, joint-tax-year notes. Informational, not legal advice.

## When to Use

- A cohabiting relationship (romantic or long-term roommate) is ending and property/accounts must be divided
- Moving out of a shared apartment with joint bills and a joint lease
- Divorce-adjacent untangling of digital accounts (banking apps, streaming, cloud storage, family plans)
- Roommate exit audit: shared furniture, shared kitchen gear, deposit split
- Don't use for: dividing a deceased person's estate (different legal regime — see digital-legacy), business partnership dissolution (different law), or actual legal advice — this organizes decisions, it doesn't make them legally binding.

## How It Works

1. **Catalog items** — `item add` records shared purchases: name, price, date, payer, who principally uses it, sentimental flag.
2. **Split decisions** — `split` runs the negotiated settlement: alternate-picks draft (like a sports draft — provably fair), buy-out pricing (one keeps the sofa, pays half equity), or sell-and-split.
3. **Audit accounts** — `accounts` manages shared accounts with action flags and renewal dates; `accounts --due 60` lists what renews in 60 days and still has no action decided.
4. **Settle expenses** — `settle` computes net balance from recorded shared expenses and prints the single settling payment + receipt line.
5. **Move-out plan** — `moveout` generates the dated checklist: notice dates, handoff events, utility name changes, deposit demand letter.
6. **Report** — `report` prints the full untangling status: items decided/undecided, accounts pending action, settle-up balance, move-out blockers.

## Commands

```bash
# Shared catalog
python3 scripts/untangle.py item add "Sofa" --price 1200 --date 2024-03-15 --payer both \
    --user her --sentimental no
python3 scripts/untangle.py item add "Record player" --price 400 --payer him --user him --sentimental yes
python3 scripts/untangle.py item list

# Fair split via alternating draft
python3 scripts/untangle.py split draft --seed 20260101
python3 scripts/untangle.py split buyout          # equity-based buyout prices
python3 scripts/untangle.py split list

# Shared accounts
python3 scripts/untangle.py account add "Netflix" --type subscription --renews 2026-11-01 \
    --owner both --action transfer
python3 scripts/untangle.py account add "Gas bill" --type utility --owner him --action rename
python3 scripts/untangle.py accounts --due 60

# Expense settle-up
python3 scripts/untangle.py expense add "October rent" 950 --payer her --shared-with him
python3 scripts/untangle.py expense add "Movers deposit" 300 --payer him --shared-with her
python3 scripts/untangle.py settle

# Move-out plan
python3 scripts/untangle.py moveout --move-date 2026-10-01 --notice-days 30
python3 scripts/untangle.py report
```

Storage: single `untangle.json` in cwd (or `--db path`). 100% local — this data is among the most sensitive there is.

## Splitting Rules

| Rule | How it works | Best for |
|---|---|---|
| `draft` | Alternating picks over equity-ranked items; coin-flip first pick (seeded) | Contentious splits, many similar-value items |
| `buyout` | Each item to principal user at half current equity; cash settles difference | One party keeping the home/furniture |
| `sellsplit` | Everything sellable is sold, proceeds 50/50 (or custom ratio) | Both moving out, no buyout interest |
| `custom` | Manual assignment in `items edit` | Amicable, few items |

Sentimental items are excluded from draft/buyout automation — they must be resolved by explicit agreement (`item edit --to him/her`).

## Common Pitfalls

1. **Forgetting auto-renewing joint subscriptions.** The #1 post-breakup leak. Always run `accounts --due 90` before the final conversation and kill/transfer everything inside 90 days.
2. **Splitting by purchase price, not equity.** A $1,200 sofa 18 months old is worth maybe $500. `split buyout` uses depreciated value (configurable rate) — splitting list price overpays the keeper.
3. **Leaving one name on a lease.** Even after move-out, lease liability persists until the lease ends or a formal release. Track it in `moveout` until signed release is confirmed.
4. **Settling with vibes.** "You owe me like $800" invites counter-memory. Record every shared expense in `expense add` and let `settle` print the single net number.
5. **Doing this without a paper trail.** `report` output is timestamped and itemized — attach it to any mediation or small-claims process.

## Verification Checklist

- [ ] All shared items cataloged with payer and user
- [ ] Split rule chosen and run; sentimental items resolved manually
- [ ] Every shared account has an action flag and (if renewing) a decision before renewal
- [ ] `accounts --due 90` returns empty
- [ ] Net settle-up balance computed and single payment recorded
- [ ] Move-out checklist generated; notice/forwarding/utility steps dated
- [ ] Final `report` printed and archived
