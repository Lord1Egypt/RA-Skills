---
name: declutter-pilot
description: "Use when your home/office/garage has accumulated more stuff than it can hold and every past cleanup attempt stalled after 20 minutes. Physics-based decluttering: item registry with volume estimates, container/trash bag math (how many bags/bins this will actually fill), a fill-first greedy packing order that front-loads visible wins (the first bag out is 80% of the psychological battle), a 20-minute sortie planner with a room+category target list so sessions never stall at 'where do I start', keep/toss decision rules with sunk-cost counters (what the indecision itself costs in money and space), and a donation/receipt/sell batch manifest. Fighting the two real enemies: decision fatigue and the invisible cost of storing junk you'll never use."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [decluttering, minimalism, moving, garage, basement, storage, organization, cleaning]
---

# Declutter Pilot — Physics-Based Decluttering Planner

## Overview

Decluttering fails the same way every time: not from lack of will, but from
**decision fatigue**. Each object demands a micro-decision ("might need it
someday", "was expensive", "a gift"), and after 20–30 decisions the brain
refuses to make more. The pile stays half-sorted, now worse than before
because it's been touched and abandoned.

Meanwhile every store decision has a real carrying cost: a typical cluttered
home stores $2,000–6,000 of never-used items at $10–40/mo per m² of storage
value, and moving companies charge by volume — decluttering before a move
literally saves hundreds in truck space.

This skill inverts the problem: **do the physics first, decide second.**

1. **Volume accounting** — items logged with volume estimates; the tool
   computes how many trash bags / boxes / car-loads the declutter will
   actually produce. Seeing "23 bags, 4 donation boxes, 1 trailer run" turns
   a vague dread into a bounded project.
2. **Fill-first greedy order** — ranks items by volume ÷ decision-difficulty.
   The first sortie should remove the most cubic meters with the fewest
   agonizing decisions. Visible win in 20 minutes = the project survives.
3. **Sortie planner** — each session is a 20-minute run with a named room,
   category, container count, and exit condition. Never "clean the garage";
   always "garage / sports gear / fill 2 bags".
4. **Decision rules** — the standard tests (12-month rule, replacement-cost
   rule, sunk-cost counter) applied consistently, plus the "sunk cost of
   indecision": what keeping-it costs per year in space and attention.
5. **Disposition manifest** — sell / donate / recycle / trash batches with
   donation value estimates, sell-price suggestions (rule of thirds), and a
   printable drop-off manifest.

One local `declutter.json`; no cloud, no account.

## When to Use

- Chronic clutter: garage/basement/attic/closets at or past capacity
- Pre-move purge (volume = money: fewer boxes, smaller truck)
- Post-breakup / post-bereavement clearing where emotional load makes decisions hard
- Seasonal resets (spring cleaning that actually finishes)
- Helping someone else declutter (estate light, hoarding-adjacent — gentle mode)
- Don't use for: actual hoarding disorder (a clinical situation needing
  professional support — this tool can help structure work *alongside* that,
  never instead of it), or digital decluttering (different physics entirely).

## How It Works

1. `item add "Old monitor" --room office --volume 30 --difficulty 2 --value 0 --decision toss`
   — volume in liters, difficulty 1 (easy toss) to 5 (emotional heirloom).
2. `plan` — greedy order: biggest volume-per-difficulty first; prints sortie
   list: which items, how many bags, est. minutes.
3. `sortie start / done` — runs the 20-minute session; `done` marks items
   out, logs bags filled, shows cumulative stats and remaining volume.
4. `bags` — container math: liters → 60L trash bags / 60L boxes / car-loads.
5. `decide "Old monitor"` — runs the decision rules and prints the verdict +
   sunk-cost-of-keeping math.
6. `manifest` — disposition batches with donation value, sell prices
   (rule-of-thirds), drop-off manifest.

## Commands

```bash
# Log items (volume liters, difficulty 1-5)
python3 scripts/declutter.py item add "Broken desk chair" --room office --volume 80 --difficulty 1 --decision toss
python3 scripts/declutter.py item add "Jeans size 32" --room bedroom --volume 4 --difficulty 2 --decision donate
python3 scripts/declutter.py item add "University textbooks" --room office --volume 45 --difficulty 3 --decision sell --value 60

# The plan: biggest-bang-first sortie order
python3 scripts/declutter.py plan
# → SORTIE 1: office / furniture — 2 items, 160L ≈ 3 bags, ~15 min, easy decisions

# Run a session
python3 scripts/declutter.py sortie start
python3 scripts/declutter.py sortie done --bags 3

# Reality math
python3 scripts/declutter.py bags          # 400L ≈ 7 trash bags or 1 car-load

# One hard decision, decomposed
python3 scripts/declutter.py decide "University textbooks"

# Where it all goes
python3 scripts/declutter.py manifest
```

## The Decision Rules (applied in `decide`)

| Test | Question | Fail → |
|---|---|---|
| 12-month | Used in the last 12 months? (seasonal items: last 2 cycles) | toss/donate |
| Replacement | Can it be replaced in <30 min for <$30? | toss |
| Sunk cost | "I paid a lot" — that money is gone either way | keeping ≠ refund |
| Cost of keeping | space rent + attention + guilt, per year | often exceeds item value |
| Active vs passive | Does it serve a current project/life, or a hypothetical one? | hypothetical = donate |

## Common Pitfalls

1. **Starting with the hardest box.** Sentiment boxes (photos, kid stuff,
   heirlooms) are difficulty 5 — starting there kills the project in 15
   minutes. The planner front-loads difficulty 1–2 volume; save the 5s for
   when momentum exists.
2. **The "maybe" pile.** A maybe pile is a decision deferred with extra
   steps. Rule: maybe = keep for one cycle (30 days), then auto-toss — the
   tool flags aging maybes.
3. **Buying storage to solve clutter.** New bins organize the problem; they
   don't remove it. Container math shows the bin cost vs the space freed.
4. **Selling everything.** Listing 40 items at $8 each is a part-time job.
   Rule of thirds: sell only items worth ≥3× the effort; donate the rest.
   The manifest applies it automatically.
5. **No exit condition.** "Clean the garage" cannot be finished; "2 bags out
   of the garage sports corner" can. Sorties always have a target.
6. **One heroic weekend.** Eight-hour sessions create burnout and
   re-cluttering (the middle-of-room pile). 20-minute sorties, 3–4×/week,
   clear more volume in a month with zero drama.
7. **Ignoring the volume reality.** 20 bags doesn't fit in a hatchback. The
   bags/car-load math prevents the Saturday night driveway-full-of-staff
   surprise.

## Verification Checklist

- [ ] `item add` records volume, difficulty, decision; volume required (physics first)
- [ ] `plan` sorts by volume÷difficulty descending and groups into ≤20-min sorties
- [ ] `sortie done` updates state, prints cumulative freed liters and % complete
- [ ] `bags` converts liters to 60L bags / boxes / car-loads correctly
- [ ] `decide` applies all five tests and prints annual cost-of-keeping
- [ ] `manifest` batches by disposition with donation values and sell-price suggestions
- [ ] All state local, one JSON file

## References

- `references/decision-science.md` — decision fatigue research notes, the
  space-cost model, donation value tables, runbook for a full house purge
