# Birthday Party Architect

**The average kid's party now runs $200–$500, and most of that pain is four planning failures nobody warns parents about: a 2-hour structured party for 4-year-olds (meltdown engine), a cake that serves 12 at a 20-kid party, 30 kids in a living room built for 12, and the venue contract's 90-minute cap + cake-cutting fees.**

This planner turns `age + guests + venue + budget` into the whole plan: an age-band doctrine (duration, supervision ratio, drop-off policy, competition rules), a minute-by-minute timeline that puts food *before* the fatigue wall, cake/pizza/drink quantities from real charts, favor doctrine ($3–5, one quality item), and a home-vs-venue cost comparison that prices the venue's hidden fees and the home party's invisible line item — your Saturday.

## Example
```
$ python3 scripts/party_plan.py --age 5 --kids 12 --adults 8 --venue home --budget 250 --start 10:00
AGE BAND 3-5 (preschool): 90 min | 1 adult : 2-3 kids (caregivers stay) | drop-off NO
HEADCOUNT: invited 12 kids -> expect 8-10 (70-85% show rate); plan supplies for 12
TIMELINE (90 min, start 10:00)
  10:00-10:15  arrival: sticker + coloring station (soft start)
  10:15-10:45  station rotation: playdough / beanbag toss / craft
  10:45-10:55  group moment: freeze dance or parachute
  10:55-11:15  food, then cake + candles
  11:15-11:30  favor handout + bubble exit
CAKE: 20 servings -> 8" round double layer (20) or 9x13
FOOD: toddler snack table + ADULT platter ...  DRINKS: 24 child + 16 adult servings
FAVORS: 12 x $3-5 -> $48 — one quality item beats a bag of plastic
BUDGET $250 (home): food $100 / cake $45 / decor $30 / activity $25 / favors $48 / buffer $13
TRAPS: NO elimination games; never schedule against nap; caregivers must stay — count adult chairs.
```

Stdlib-only Python, no network, works offline.

## License
MIT
