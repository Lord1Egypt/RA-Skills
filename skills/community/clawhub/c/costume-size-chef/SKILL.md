---
name: costume-size-chef
description: "Use when you need a costume in days not weeks (Halloween crunch, school book-character day, theme party) — builds costumes from clothes and household items you already own with a difficulty x time-budget filter, sizes kid/adult adaptations, handles group and couple costumes as coordinated sets, flags safety issues (visibility, flammable fabrics near flames, mask sightlines for trick-or-treat), and produces a printable shopping list for the few things actually worth buying."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [costume, halloween, diy, kids, crafts, parties]
---

# Costume Size Chef

**Book-character day is TOMORROW and the notice is crumpled in a
backpack.** Store costumes sell out and cost $30-60 for one night;
the good ones go first. This tool assembles costumes from a closet
inventory + household items, filtered by the time you actually
have, sized to the wearer, and safety-checked for
trick-or-treat conditions.

## Overview

1. **inventory** — declare what you have (clothes by type/color,
   craft basics, makeup) once; recipes check against it.
2. **find** — occasion + wearer + time budget → ranked costume
   recipes with build steps, each item marked HAVE / SUBSTITUTE /
   BUY (cheap).
3. **groups** — couple/family/group coordination: themed sets where
   each person's costume stands alone too.
4. **safety** — trick-or-treat checklist: visibility (reflective
   tape placement), mask sightlines vs face paint, flammable
   fabrics near jack-o-lanterns, cape length vs stairs, prop rules
   at school events.
5. **list** — consolidated BUY list with priorities, so a single
   store run covers multiple costumes.

Stdlib Python, offline, 40+ recipe knowledge base.

## When to Use

- Halloween with days-to-go and nothing planned
- School events on short notice: book-character day, decade day,
  spirit week themes, school plays
- Theme parties (adult): 80s, pirates, movie characters — without
  buying a one-wear costume
- Group/family costume coordination on a budget

**Don't use for:** theater-grade costume construction (sewing
pattern territory), mascot/professional costumes.

## How It Works — Numbered Steps

1. Register inventory (once, takes 5 min):
   ```
   python3 scripts/costume_chef.py inventory --item "black hoodie" --item "red striped shirt" --item "face paint set" --item "cardboard"
   ```
2. Find costumes for the occasion and time you have:
   ```
   python3 scripts/costume_chef.py find --occasion halloween --wearer kid --minutes 30
   python3 scripts/costume_chef.py find --occasion book-character --wearer kid --minutes 20
   python3 scripts/costume_chef.py find --occasion "80s party" --wearer adult --minutes 15
   ```
3. Build steps for a chosen recipe:
   ```
   python3 scripts/costume_chef.py build --recipe "where's waldo"
   ```
4. Group sets:
   ```
   python3 scripts/costume_chef.py groups --theme "wizarding world" --people 3
   ```
5. Safety check before trick-or-treat:
   ```
   python3 scripts/costume_chef.py safety --context trick-or-treat
   ```
6. Shopping list across chosen recipes:
   ```
   python3 scripts/costume_chef.py list --recipes "where's waldo,black cat"
   ```

## Recipe Excerpt

| Recipe | Core items (HAVE-class) | Time | Wear with |
|---|---|---|---|
| Where's Waldo | red/white striped shirt, beanie, glasses | 10 min | jeans |
| Black cat | black clothes, eyeliner whiskers, headband ears | 15 min | — |
| 80s aerobicizer | tights, leotard/oversized tee, leg warmers, side ponytail | 15 min | — |
| Gnome | beard hat or cotton-ball beard, belt over oversized shirt | 20 min | — |
| Box robot | 2 boxes, foil, duct tape | 45 min | — |
| Tourist | hawaiian shirt, camera, sunhat, socks+sandals | 10 min | — |
| Wednesday Addams | black dress, white collar, braids | 15 min | — |
| Crayon | solid-color outfit + construction-paper hat | 20 min | — |
| Scarecrow | flannel, jeans, straw/hay, face-paint nose | 25 min | — |
| Static cling | laundry basket, clothes pinned all over | 30 min | — |

## Common Pitfalls

1. **Mask on a 6-year-old at dusk.** Sightlines + street crossing
   = face paint instead. The safety check enforces this swap.
2. **Capes and stairs / escalators.** Hem above ankle or pin up.
3. **Costume over a winter coat.** Plan the costume one size big or
   make it coat-compatible (it's cold in most of the north on Oct
   31); a frozen pirate is a sad pirate.
4. **Open flames + synthetic fabric.** Fake fur/polyester melts;
   keep distance from jack-o-lanterns or use LED candles.
5. **Props that look like weapons at school.** Cardboard swords get
   confiscated at many schools; check the event's prop policy
   (safety output reminds).
6. **Buying the wig.** Wigs are the #1 wasted costume purchase —
   they itch, kids rip them off, and 80% of recipes look right with
   a styled hat/hairband instead. The BUY list marks wigs as
   last-resort.
7. **Perfectionism on crunch night.** The find command's time
   filter exists because a 3-hour costume at 9 PM is a failure
   mode; pick the 20-minute one.

## Example

```
$ costume_chef.py find --occasion book-character --wearer kid --minutes 20
BOOK-CHARACTER, KID, <=20 MIN — ranked by inventory match:

1. WHERE'S WALDO (100% match) — 10 min
   HAVE: red striped shirt, jeans, beanie
   SUBSTITUTE: round glasses -> paper + cellophane circles on your
   sunglasses (10 min)
2. CRAYON (85%) — 20 min — solid yellow outfit + cone hat
3. GNERM... (see build output)

$ costume_chef.py safety --context trick-or-treat
- face paint over mask for under-8s (sightlines)
- reflective tape: ankles + treat bag (motion = visibility)
- cape hem above ankle bone; no dragging fabric near stairs
- LED tea lights only within arm's reach of costume
- prop policy check if school event: no weapon-looking props
```

## Verification Checklist

- [ ] Inventory entered; recipes ranked by what you HAVE
- [ ] Time budget realistic for the actual evening you have
- [ ] Weather/cold plan: costume fits over a coat or is warm
- [ ] Safety check run for the context (trick-or-treat/school)
- [ ] BUY list consolidated to ONE store run, wigs resisted
