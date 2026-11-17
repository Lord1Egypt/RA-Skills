# Feast Scheduling — The Full Problem

## Why meals collapse

A multi-dish meal is a **job-shop scheduling problem** in disguise:
- jobs = dishes, each a chain `prep → cook → rest`
- machines = oven (capacity by shelves, temperature-locked windows),
  burners (count), counter (infinite), your hands (capacity 1)
- deadline = one serve time for everything

Humans run this in their heads and fail at exactly two places:
1. **Backward planning under rest/hold asymmetry** — the turkey needs 3h and
   rests 45 min; the popovers need 20 min and hold 5. Mental math breaks.
2. **Resource contention at the deadline** — everything wants the oven in
   the last hour.

## Model

### Stages and slack

For dish *d*:
- `cook_end_latest = serve + hold − rest`
- `cook_start_latest = cook_end_latest − cook`
- `prep window = [cook_start − prep, cook_start]`

`hold_min` is the honest slack: how long the finished dish is still good.
Gravy holds 60 min in a warm pan; fried anything holds ~5. Rest time
(tenting a roast) is part of quality, not slack, and happens after cook.

### Oven co-baking rule

Two oven dishes may run simultaneously iff:
1. `|temp_A − temp_B| ≤ 25°F` at every overlapping minute, AND
2. `sum(shelves) ≤ oven_shelves`.

The 25°F tolerance reflects real kitchen practice: doneness windows of
casseroles, roasts and bakes are wide enough that 350 vs 375 is
interchangeable with minor time adjustment. 250 vs 450 is not — those
dishes must be **sequenced**.

Why sequencing usually works: total oven-hours demanded on a feast day
rarely exceeds availability once rest windows, hold slack, and make-ahead
splits are exploited. When it doesn't, the tool reports infeasibility
instead of guessing.

### Burners

Burner dishes claim one burner for their cook window. Capacity defaults to
4. Stir-sensitive dishes are noted in output (stirring demand isn't
scheduled minute-by-minute — a human stir is 20 seconds).

### Hands-on audit

Prep windows are the hands-on work. The scheduler staggers them naturally
(each dish's prep sits right before its cook start, and cook starts are
spread by the resource solver), then **audits** overlaps pairwise and
warns. A warning means: move that prep earlier yourself (most preps can
slide back freely — only the tool's placement is tight, not reality).

### Make-ahead

Any dish with `"make_ahead": true` is excluded from day-of contention and
listed under "Day before". Use it for: cranberry sauce, pies (reheat 20
min day-of — encode as a separate small dish), stock, peeled/chopped
aromatics, casseroles assembled and refrigerated.

## Feasibility search

If a dish's prep would start before `--now`, the serve time is infeasible.
The tool then searches serve times forward in 5-minute steps (up to +4 h)
for the first feasible plan and reports it. This converts "can I make it?"
from anxiety into arithmetic.

## Reading the output

The timeline lists events in time order:
- `PREP <dish>` (hands-on)
- `<dish> → OVEN @ 350°F` / `→ BURNER 2/4`
- `<dish> OUT — rest 45 min`
- `SERVE <dish>` (its ready window)

Warnings section lists prep collisions, oven utilisation peaks, and dishes
whose hold slack was fully consumed (zero remaining slack = tightest dish —
protect it).

## Practical numbers used by the example

- 14 lb (6.3 kg) turkey: ~13 min/lb at 350°F unstuffed ≈ 180 min, rest 45
- Casserole 375°F 35 min
- Popovers 450°F 20 min, hold 5 — sequenced *before* the 350 roast by the
  solver using pre-roast oven time
- Potatoes 30 min boil + mash prep
- Gravy 15 min after turkey rests (uses pan drippings — deliberately
  scheduled after turkey OUT; model this by `--after` ordering… or simply
  prep-window placement; the sample keeps it independent)

## Safety notes

- Poultry rest is not optional (carryover + juiciness); 45 min tented is
  standard for a large roast.
- Hot-holding above 60°C / 140°F is safe indefinitely; below that, 2-hour
  window applies — that's why hold windows matter for more than quality.
