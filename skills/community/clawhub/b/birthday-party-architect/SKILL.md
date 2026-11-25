---
name: birthday-party-architect
description: "Use when planning a child's birthday party — guest count, duration, activities, cake size, food quantities, favors, budget, venue-vs-home. Age-band engine prevents the classic failures: 2-hour structured games for 4-year-olds, undersized cake, 30 kids in a living room, and the $400 party a six-year-old won't remember."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [parenting, party-planning, birthday, kids, budget, events]
---

# Birthday Party Architect

## The problem it solves
The average kid's party in the US now runs $200–$500, and most of the stress comes from four planning failures the industry never warns you about:
1. **Wrong duration for the age** — a structured 2-hour party for 4-year-olds is a meltdown engine; teens want drop-off, toddlers want 60 minutes and a caregiver per child.
2. **Wrong headcount physics** — the "invite the whole class" rule of thumb collides with venue caps, living-room floor area, and the 70–85% show rate.
3. **Cake and food math** — 8″ round ≠ 24 guests; pizza is 3 slices/child not 1; adults at a toddler party are 100% of the supervision plan and 0% of most orders.
4. **Budget shape** — venue packages price per child and quietly multiply; favors are $3–5/child of plastic that dies in a day.

This skill generates the whole plan from age + guest count + venue + budget: minute-by-minute timeline, activity list matched to attention spans, cake sizing, food quantities, favor budget, and a venue-vs-home cost comparison.

## When to trigger
- "We're planning [child]'s birthday party" — any mention of planning a kids' party.
- Questions like "how long should a party be for a 5-year-old", "how much cake for 20 kids", "should we do a venue or home party".
- Post-mortems: "last year's party was chaos" → rebuild the plan.

## Steps
1. Collect: child's age, expected guest kids, expected adults, venue (home / park / venue-package), budget ceiling, party date/time of day.
2. **Age-band engine** (see references/age-bands.md): duration, activity structure, supervision ratio, drop-off policy, competition rules (under-7: everyone-wins or team games; individual eliminations cause tears).
3. **Headcount reality:** RSVP show-rate 70–85% for class invites; siblings +tagalongs +15%; cap = venue limit or living-room floor (rule: ~2 m² of open floor per child for activity parties).
4. **Timeline generator:** arrival quiet activity → energy peak games → food (sits them down, resets mood) → cake → present-or-favor close. Party ends BEFORE the age band's fatigue wall.
5. **Quantities:** cake servings chart (round/sheet), pizza (3 slices/child 5+, 2 for under-5, 1 per 3 adults), drinks (2/child), snack tables, favor rule ($3–5/child, one quality item beats a bag of plastic).
6. **Budget breakdown:** percent bands per category for home vs venue; venue per-child price × realistic headcount + cake + tips vs the home-party stack (food + decor + activity rent + your Saturday).
7. Output: the printable plan + a "what to buy" list + the 3 failure traps specific to this age.

## Pitfalls
- **Never schedule against nap** for under-5: 10:00–11:30 or 15:30–17:00, never 12:30.
- **Opening presents live** is a social-media hazard and a gratitude trap for under-8s — defer to home; do a group "thank you cheer" instead.
- **Water/decor hazards:** balloons pop into choke hazards for toddler siblings; confetti in a rental; piñata candy scramble injures toddlers annually.
- **Venue packages are per-child AND 90 minutes** — overtime fees and per-head cake-cutting fees are the hidden stack; the script prices both paths.
- **Invite-whole-class etiquette:** if you hand invites at school, you invite all — otherwise use direct contact only.
- Food allergies: collect at RSVP; serve labeled.

## Example
```
$ python3 scripts/party_plan.py --age 5 --kids 12 --adults 8 --venue home --budget 250
AGE BAND 3-5: 90 min, caregiver-per-child (adults must stay), parallel-play stations, no elimination games
TIMELINE (Sat 10:00-11:30)
  10:00-10:15  arrival: sticker + coloring station (soft start, no dead time)
  10:15-10:45  station rotation: playdough / beanbag toss / bubble corner
  ...
CAKE: 12 kids + 8 adults = 20 servings -> quarter-sheet (24 servings) or 10" round + 4" tier
FOOD: 3 pizza (12 slices child + 4 adult) ...  DRINKS: 24 child + 16 adult servings
BUDGET: $250 -> food $100 / cake $45 / decor $30 / favors $48 (12x$4) / buffer $27
TRAPS for age 5: no elimination games; end by 11:30 before hunger-meltdown wall.
```

## Files
- `scripts/party_plan.py` — the full planner (age bands, timeline, quantities, budget split, venue compare). Stdlib only.
- `references/age-bands.md` — developmental logic per band: duration, activity types, supervision, competition, drop-off age.
- `references/quantities-and-budget.md` — cake chart, food/drink math, favor doctrine, home-vs-venue cost anatomy.
- `README.md` — real-world framing.
