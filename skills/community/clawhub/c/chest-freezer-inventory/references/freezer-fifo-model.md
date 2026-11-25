# Chest Freezer Inventory — Reference

## 1. Why chest freezers become black holes
An upright freezer presents its contents; a chest freezer presents its
*top layer*. Access is vertical, gravity migrates mass downward, and
there is no visible date on anything. Result: studies of household food
waste consistently find frozen items aged years past usefulness,
duplicates purchased because existing stock is invisible, and a
"mystery bag" stratum at the bottom. The USDA is blunt that freezing
keeps food *safe* indefinitely — which lulls owners into ignoring that
*quality* has a class-dependent clock, and that the dollar value in
the box silently depreciates.

The fix is an inventory that matches the physics: layer-aware
(top/middle/bottom), date-stamped at freeze time, and consulted before
meals and before store runs.

## 2. USDA quality clocks (days, ≈)
| Class | Window | Notes |
|---|---|---|
| ground meat | 120 | high surface area, fast oxidation |
| bacon | 30 | cured fat goes rancid first |
| sausage | 60 | seasoning accelerates staling |
| chops / steaks | 180–240 | chops first, steaks after |
| roasts | 300 | dense mass ages slowest |
| whole poultry | 365 | skin-on carcass holds a year |
| poultry parts | 270 | bone-in pieces |
| fatty fish (salmon, mackerel) | 90 | omega-3 fats oxidize — the fastest major class |
| lean fish (cod, tilapia) | 180 | |
| shellfish | 120 | |
| cooked dishes / casseroles / soups | 90 | flavors flatten, sauces separate |
| bread | 90 | then dry/stale character even frozen |
| baked goods | 60 | |
| fruit / vegetables (blanched) | 300 | texture degradation is the limit |
| butter | 270 | |
| cheese / milk / ice cream | 180 / 90 / 60 | |
| herbs / coffee / nuts-flour | 180 / 90 / 180 | aromatic oils fade |

Verdict bands used by the tool: PRIME <50% of window elapsed, FADING
50–75%, USE-FIRST 75–100%, BURN RISK past the window.

## 3. Usage model
- **add**: 10 seconds at freeze time; layer defaults to `top` because
  new stock enters at the top. `--value` (replacement $/unit) is what
  makes the waste visible later.
- **Layers are a user-maintained approximation**: after a dig, moved
  items shift layers; the map is a heuristic, not a survey.
- **dig**: strict FIFO (oldest date first) within an optional class
  filter, plus the "dig past" list — the items physically above the
  target. Retrieval cost is the hidden deterrent to FIFO; naming it
  helps plan one excavation for multiple targets.
- **plan**: greedy oldest-first with a 2-per-class variety cap, dated
  from today, night-before thaw moves flagged, dollars consumed
  tallied.
- **use**: partial consumption supported; entries auto-retire at zero.
- **stats**: totals, class histogram, value-at-risk (USE-FIRST+BURN
  share), burn report, and the DEFROST DAY trigger (>30% of entries
  past window): eat down, empty, defrost, dry, gasket-check, restart.

## 4. Practice notes
- Freeze flat in single layers where possible, then stand upright —
  faster freezing (quality) and better packing.
- Label with contents + date at the door, not the freezer: discipline
  fails at -18 °C with bare hands.
- The 24-hour fridge thaw is the quality-preserving route; cold-water
  thaw for forgotten mornings; never counter thaw.
- Power-outage rule of thumb: a full chest freezer holds a safe frozen
  state ~48 h unopened (half-full ~24 h) — see the
  outage-food-safety-triage skill for the after-event decisions.
- Chest freezers are efficient *because* cold air pools at the bottom —
  which is exactly why they stratify. The design isn't changing; the
  record-keeping has to.

## 5. Store format
`freezer_inventory.json` in the working directory (override with
`--store`): `{"items": [{id, item, class, qty, date, layer, value}],
"next_id": N}`. Plain JSON, editable by hand, no dependencies.
`--today YYYY-MM-DD` overrides the clock for reproducible runs.
