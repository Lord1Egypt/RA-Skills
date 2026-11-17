# Packing Physics — the reference behind cargo-space-packer

Practical load-planning numbers for trucks, vans, and trailers. Rules are
approximations distilled from moving-industry practice and 49 CFR 393-style
tie-down minimums — when a regulation applies to you, the regulation wins.

## 1. The Box-Volume vs Truck-Volume Trap (the ~80% Cube Ceiling)

Truck ads quote total box cube. Real loads never reach it:

- **Wheel wells** steal ~15 cm of floor width over the rear third.
- **The "mom's attic"** over the cab is sloped and low — soft goods only.
- **The door slope** kills the last ~30 cm of height.
- **Irregular furniture** (sofas, dressers, bikes) interlocks far worse
  than the identical boxes used in brochure photos.

Load factors by loader:

| Loader | Achievable cube |
|---|---|
| DIY, first move, no plan | 50-60% |
| Careful DIY with a load plan | 60-70% |
| Professional movers, stacked tiers | 70-80% |
| Uniform same-size boxes only | 85%+ |

**The rule: if your loose cargo volume exceeds ~80-85% of the bay's cube,
it will not fit — no amount of Tetris saves it.** Take the next size up.
Between 70% and 85% it fits only with discipline (tiers, fillers, on-end
placement); plan for that before you're standing in the ramp line.

Worked example: 60 book boxes at 60×40×40 cm = 5.76 m³. A cargo van at
~9 m³ bay → 64% cube: fits with room. The same load in a 4×8 trailer
(~3.1 m³) → 186%: doesn't fit, and no rearrangement changes arithmetic.

## 2. Density Stacking Classes

| Class | Density | Typical contents | Rule |
|---|---|---|---|
| Heavy | ≥300 kg/m³ | books (400-600), tools, canned food, weights | floor level only; ≤3-4 boxes high; small boxes (≤60×40×40, ≤30 kg each) |
| Medium | 100-300 kg/m³ | dish packs, appliances, file boxes, electronics | mid tiers, on top of heavy |
| Light | <100 kg/m³ | linens, pillows, lampshades, plastic toys | top tier only; nothing but light above light |

- **Crush rule: never place an item on a lower-density item.** Equal class
  on equal class is fine. The packing algorithm enforces this; humans
  under time pressure don't.
- Book boxes are the classic failure: a 60×40×40 filled with books is
  35-45 kg and ~450 kg/m³. Cap books at ~30 kg per box and use the
  smallest boxes you have.
- Weight caps matter for the humans too: nothing you can't carry goes in
  anything you can't slide.

## 3. The Load Pyramid (Heavy Low-Forward)

Order of loading, front (bulkhead/cab) to back (door):

1. **Heaviest appliances and furniture flat against the bulkhead**,
   spread across the width — washer, fridge (upright!), safe, tool chest.
2. **Heavy box tier** beside/behind them, built to a level height.
3. **Medium furniture and boxes** in the next tiers, keeping tops level.
4. **Long flat items on edge** along the walls: mattresses, box springs,
   table tops, mirrors (pad between).
5. **Light/bulky/soft** last — pillows, lampshades, garage oddities —
   wedged against the door wall, which gets a load bar + 2 straps.

Why forward-heavy: braking throws mass toward the door; a tail-heavy load
lightens the steering axle and induces sway. Keep the pyramid's center of
mass in the front 40% of the floor.

**On-end doctrine:** mattresses and box springs travel best **on edge**
(their strong axis) along a sidewall — they occupy 5× less floor than flat.
Sofas go **on end** (wrapped, feet toward the wall, arm padded) to use bay
height. **Upright-only appliances:** refrigerators, freezers, washers,
dryers, ranges never ride on their side or back (compressor oil migrates).
If one must tip briefly, let it stand unplugged for several hours — 24 h
is the safe answer — before powering it.

## 4. L-Track / E-Track and Ratchet Tie-Down Math

**Hardware:** E-track = horizontal slotted rows inside the box walls (one
row ~30 cm off the floor, one high); L-track (airline track) = surface
rails on floor/walls in vans. Fittings clip in anywhere along the track —
that's the point: your anchor count is slots, not fixed D-rings.

**Working Load Limit (WLL) math.** A typical 2" ratchet strap: WLL
~907 kg (breaking strength ~3× that; never use breaking strength for
planning). Aggregate rule (49 CFR 393.106): the sum of strap WLLs must be
at least **half the cargo weight**:

    straps ≥ cargo_kg / (2 × 907)

500 kg of cargo → 1 strap by law. That's the floor, not the plan.

**Article count minimums (49 CFR 393.110):** an article ≤1.5 m long needs
1 tie-down; 1.5-3 m needs 2; over 3 m needs 2 plus 1 per additional 3 m.

**Practical moving plan:**

- 2 straps per large article, crossed at ~45° to opposing track slots
- 2 straps cinching the door headload (plus a jack/load bar)
- 1 strap per ~450 kg of loose boxed goods run through the track at
  mid-height around each tier
- Straps pull at an angle: a 45° diagonal retains ~70% of its rating —
  cross pairs cancel lateral slip; anchor low (rub-rail/floor track level)
- Re-tension after 15 km — ratchet straps settle, rope stretches

## 5. Blanketing Protocol

- **Wrap in the room the item lives in**, never in the truck: the blanket
  goes on before the item crosses a door frame, and the wrap goes on
  before it crosses the ramp.
- Moving blanket next to the surface, **shrink wrap over the blanket**
  (wrap holds the blanket on; the blanket does the protecting). Tape on
  the wrap, never on wood or fabric finish.
- **Corners get double layers** — every impact lands on a corner. Sofa
  arms, table legs, dresser corners especially.
- Leather: paper or cloth first, plastic only for hours (it traps
  moisture and marks finished surfaces long-term).
- Glass/mirrors: flat, on edge, padded between, or in a mirror carton.
- Hardware: bagged, labeled, taped inside a drawer of the item it
  belongs to.
- Blanket math: one blanket covers ~1.8 m² with proper overlap. Count
  surface area, not items — a sofa is 4 blankets, a chair is 1-2, a
  mattress is 2.

## 6. Weight Distribution — the 60/40 Axle Goal

- Target **~60% of cargo mass ahead of the rear axle** — in practice,
  ≥55% of the mass in the front half of the load floor.
- **Tail-heavy:** light steering, trailer-like sway, rear axle overload,
  door wall failure under braking. The classic DIY mistake (easy boxes
  first at the door end).
- **Nose-heavy:** front axle overload, wallowed braking, lifted rear —
  rare but happens when a safe goes in last-minute behind the cab.
- Spread mass across the width too: a truck leaned onto one sidewall
  unloads the far tires and bends strap geometry.
- Respect the data plate: payload ≈ GVWR − curb weight. A "half-ton"
  pickup is ~450-600 kg of real payload; a 15-ft box truck is typically
  ~1,700-2,000 kg; density (books!) breaks payload long before it breaks
  cube.

## 7. DIY vs Moving-Truck-Size Table

Approximate interior bays; rental fleets vary ±15%.

| Rig | Bay (m³ / ft³) | Typical load | Notes |
|---|---|---|---|
| SUV, seats folded | 1.9 / 68 | dorm run, 5-8 boxes + duffels | soft goods win |
| 8-ft pickup + cap | 3.5 / 125 | studio sub-load, yard stuff | 450 kg payload |
| 4×8 trailer | 3.1 / 110 | mattress set + boxes | tongue weight 10-15% |
| 5×8 cargo trailer | 5.9 / 208 | studio apt | ~700 kg max load |
| Cargo van | 9 / 320 | studio/1-bed, no appliances | dock height friendly |
| 6×12 cargo trailer | 11.2 / 395 | 1-bed apt | ~900-1,100 kg max |
| 10-ft truck | 11.5 / 405 | 1-bed apt | low deck, tight |
| 12-ft truck | 14.4 / 510 | 1-bed + appliance | |
| 15-ft truck | 20.8 / 735 | 1-2 bed apt | first "easy" size |
| 17-ft truck | 25.2 / 890 | 2-bed apt | |
| 20-ft truck | 29.0 / 1,025 | 2-3 bed house | |
| 26-ft truck | 46.0 / 1,625 | 3-4 bed house | needs a load plan, not vibes |

Planning shortcut: ~5-7 m³ per bedroom + 4-6 m³ for living/kitchen, then
check the ceiling rule. When in doubt, one size up costs less than a
second trip or an abandoned sofa.

## Formula Summary (what the script computes)

    cube %         = cargo volume / bay volume        (ceiling 85%, tight 70%)
    density class  = kg per m³ → heavy ≥300 / medium 100-300 / light <100
    straps         = max(article minimums + 2 door, cargo_kg/(2×WLL), 4)
    blankets       = Σ ceil(surface m² / 1.8), min 1 per furniture piece
    axle split     = front-half mass / total mass, target ≥ 0.55
