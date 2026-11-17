# Circuit Guide — Depth & Reference

## Wire gauge ↔ breaker (why you never upsize a breaker)

| Wire | Copper ampacity (NEC 310.15 residential, 60°C col.) | Typical use |
|---|---|---|
| 14 AWG | 15 A | lights, bedrooms |
| 12 AWG | 20 A | kitchens, baths, garages, outdoor |
| 10 AWG | 30 A | dryers (some), AC, well pumps |
| 8 AWG | 40 A | ranges (some), EV chargers (32A) |
| 6 AWG | 55 A | ranges, 48A EV charger runs |

The breaker protects the WIRE, not the appliances. A 20 A breaker on 14 AWG copper lets the wire overheat inside walls before the breaker ever trips. This is the single most dangerous "fix" in DIY electrical work.

## Extension cords & power strips — derating reality

- A power strip is a 15 A device maximum, regardless of the circuit behind it. Daisy-chaining strips does not make more capacity.
- Cord resistance scales with length and thinness. For a 1500 W heater:
  - ≤ 25 ft: 14 AWG minimum
  - 25-50 ft: 12 AWG
  - 50-100 ft: 10 AWG
- A hot cord or plug = undersized. Warm is the early warning; soft/melting = discard now.
- "Surge protector" ≠ overcurrent protection. It clamps voltage spikes; it will happily pass 2000 W until its own 15 A breaker melts.

## GFCI vs AFCI vs dual-function

| Device | Protects against | Where required (modern code) |
|---|---|---|
| GFCI (Class A, 4-6 mA) | Ground fault → shock | Bathrooms, kitchens, garages, outdoors, basements, laundry, within 6 ft of sinks |
| AFCI | Arc faults → fire | Bedrooms + most living areas (NEC 2014+) |
| Dual-function | Both | New work |

A GFCI RECEPTACLE protects everything downstream of it on the same circuit — that is why an upstairs bathroom trip can kill the garage outlets. The LOAD-side terminals of a GFCI are what feed downstream; line-side is upstream. When replacing, LINE goes to the hot feed, or everything downstream stays dead.

Old two-prong outlets wired with no ground: GFCI-labeling them "No Equipment Ground" is code-legal protection for people (not for surge-sensitive electronics).

## Appliance draw reference (INPUT watts)

Kitchen: microwave 1000-1600 (input!), toaster 900-1200, kettle 1200-1500, air fryer 1500, instant pot 1000-1200 (heat phase), coffee maker 800-1400, blender 300-1000 (peak), dishwasher 1200-1800 (heater phase), disposal 400-800, slow cooker 200-300.

Personal/heating: hair dryer 1500-1875, space heater 1500 (almost universally), iron 1100-1800, electric blanket 200-400, heated mattress pad 60-150.

Laundry/mech: washer 500-1200 (motor + heater phases), gas dryer 400 (motor), electric dryer 3000-5000 @240V, gas furnace blower 400-800, electric water heater 4500 @240V, sump pump 800-1200 (surge 2-3×), well pump 750-1500 @240V, dehumidifier 300-700, garage opener 350-600 (surge 3× starting).

Electronics: TV 100-200, desktop + monitors 200-450, laptop 60-100, router/modem 20-40, game console 120-200, LED bulb 8-15, incandescent 60-100, ceiling fan 30-100, aquarium heater 50-300, chest freezer 100-250 running (surge 3×).

## Multiwire branch circuits (MWBC) — the shared-neutral trap

Houses from the 1970s-2000s often share one neutral between two 120V halves. If you open a box and see a red AND black on the same 2-pole or handle-tied breaker with one white: it's an MWBC. Rules:

- Never work it hot — the neutral can carry full current from the OTHER half even when "your" breaker is off.
- Splitting a receptacle (top/bottom on different circuits) at an MWBC outlet requires breaking the tab on the HOT side only, never the neutral tab.
- A lost neutral on an MWBC puts 240V across 120V loads — random appliance deaths. Symptom: two rooms' devices die weirdly together.

## The "big three 240V" — never DIY-load these casually

Electric dryer (30 A), electric range/oven (40-50 A), electric water heater (30 A), plus central AC (25-40 A) and well pumps. Load planning for adding any NEW 240V load (hot tub, EV charger, tankless water heater) needs a whole-dwelling load calculation (NEC 220.83), because the service itself (100/150/200 A) is the real constraint. This is electrician + permit work.

## When a breaker itself is the problem

Breakers do wear out: repeated hard trips, thermal fatigue, internal corrosion. Symptoms: breaker trips at progressively LOWER loads, feels hot to touch at the panel face, physically won't latch, or buzzes. Electricians swap breakers cheaply; the panel interior is not DIY surface.

Federal Pacific Electric (FPE Stab-Lok) panels (1960s-80s): documented failure-to-trip. If found: replacement panel consultation, not repairs. Zinsco similar vintage concerns.

## Diagnostic kit worth owning (~$40)

- Non-contact voltage tester (NCVT) — first tool out, every time
- Receptacle tester with GFCI trip button ($10) — instant read on open ground/neutral/hot reversal
- Multimeter — for outlet voltage (expect 114-126 V)
- Ammeter plug (kill-a-watt type) — measures real draw of suspicious appliances
- Circuit breaker finder (for mapping outlets to breakers from the outlet end)

## Tamper-resistant, weatherproof, in-use covers

Outdoor outlets need "in-use"/bubble covers if anything stays plugged in (block heaters, holiday lights, pumps). TR outlets (internal shutters) required indoors in new work; stiff-plug feel is normal, not a fault.
