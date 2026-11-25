---
name: chest-freezer-inventory
description: FIFO discipline for the chest freezer black hole — layer-aware inventory (top/middle/bottom, because that's how chest freezers actually stratify), USDA quality-clock aging per food class (ground meat 4 mo vs whole poultry 12 mo vs fatty fish 3 mo), USE-FIRST/BURN RISK verdicts on every item, dig lists that tell you what you'll have to excavate past, a dated FIFO week menu, consumption logging, and a stats mode that prices the food at risk in dollars and schedules the annual defrost day.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [freezer, food-inventory, food-waste, meal-planning, kitchen, home]
---

# Chest Freezer Inventory

Chest freezers violate every rule of inventory: you load from the top,
gravity pulls old food down, and nothing has a visible date. Two years
later nobody remembers what's under the venison. This tool is the
inventory discipline the freezer's design makes impossible.

## When to trigger
- "What's in the chest freezer that we should eat before it dies?"
- "I'm meal planning / broke / avoiding the store — what's frozen?"
- "Is this salmon from last year still good?"
- before grocery runs (stop buying duplicates of what's buried)
- after big batch-cook sessions, hunts, or CSA/garden surpluses

## How it works

1. **Capture on freeze** — the 10-second habit: whenever food goes in,
   `add --item "turkey chili" --class cooked-dishes --qty 3
   --date 2026-08-02 --layer top --value 6`. Layer defaults to top
   (new food always enters at the top); as you dig, old stock migrates
   down, which you record with `--layer`.
2. **Quality clocks** — every class gets a USDA-based quality window
   (ground meat 120 d, chops 180, roasts 300, whole poultry 365, fatty
   fish 90, cooked dishes 90, bread 90, fruit/veg 300…). Frozen food
   stays *safe* indefinitely; the clock is flavor/texture, and the
   tool says so.
3. **Verdicts** — PRIME (<50% of window) / FADING (50–75%) /
   USE-FIRST (75–100%) / BURN RISK (past window).
4. **`list`** prints the depth map (TOP/MIDDLE/BOTTOM) so the mental
   model matches the physical strata, items oldest-first per layer.
5. **`dig`** answers "what's for dinner" the FIFO way: strict
   oldest-first, and for each pick, **what you'll dig past** — the
   excavation cost the top-down design hides.
6. **`plan --days 7`** builds a dated FIFO week (max 2 picks per class
   so you're not eating soup seven nights), names the night-before
   thaw moves, and totals the dollars consumed that you didn't spend.
7. **`use`** logs consumption (partial quantities supported);
   **`stats`** prices the whole stock, flags the USE-FIRST/BURN share
   in dollars, prints the burn report, and triggers the DEFROST DAY
   recommendation when >30% of entries have blown their windows.

## Pitfalls encoded
- **The black hole is structural**: chest freezers have no FIFO shelf
  — without a recorded layer map, "eat oldest first" is impossible
  because the oldest is invisible.
- **Quality vs safety**: "safe indefinitely if continuously frozen" is
  true and useless — the tool separates the safety floor from the
  quality ceiling so people neither panic-toss nor serve cardboard.
- **Fatty foods die first** (fish 90 d, cooked 90 d) while lean and
  poultry hold a year — the class table encodes the asymmetry people
  don't know.
- **Value at risk makes the waste visible**: $130 of a $138 stock in
  USE-FIRST/BURN is a number that changes behavior; "old stuff" is
  not.
- **Duplicates**: buying more peas with 4 buried is the silent tax;
  the depth map catches it before the store run.
- Freeze-date discipline: undated items become MYSTERY stock — the
  tool requires a date on `add`.

## Examples

```bash
# Capture a batch-cook session
python3 scripts/freezer_inventory.py add --item "turkey chili" \
    --class cooked-dishes --qty 3 --date 2026-08-02 --value 6

# What's for dinner + what will I excavate?
python3 scripts/freezer_inventory.py dig --count 2

# Sunday planning
python3 scripts/freezer_inventory.py plan --days 7
python3 scripts/freezer_inventory.py use --id 3 --qty 2

# The quarterly reality check
python3 scripts/freezer_inventory.py stats
# → DEFROST DAY trigger when >30% of entries are past their window
```

## Output contract
- depth map (TOP/MIDDLE/BOTTOM with item×qty per layer)
- per-item aging verdicts with days remaining
- dig list with excavation ("dig past") hints
- dated FIFO week plan + thaw reminders + dollars consumed
- stats: stock value, value-at-risk %, burn report, defrost trigger
