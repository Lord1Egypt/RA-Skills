#!/usr/bin/env python3
"""party_plan.py — kids' birthday party planner.

Generates a full plan from age + headcount + venue + budget:
  age-band doctrine, minute-by-minute timeline, cake/food/drink quantities,
  favor budget, home-vs-venue cost compare, age-specific failure traps.
Stdlib only. Run:  python3 party_plan.py --age 5 --kids 12 --adults 8 --venue home --budget 250
"""
import argparse

AGE_BANDS = {
    "1-2": dict(lo=1, hi=2, minutes=60, label="1-2 (toddler)",
                doctrine="Caregiver stays with each child. NO structured games: free play + bubbles + balloons-on-floor. "
                         "Morning party only (9:30-10:30). Guest cap: match child's age in years (2 kids for a 2yo) "
                         "— this party is for the adults; the baby needs a nap and a smash cake.",
                supervision="1 adult per child (caregivers stay)",
                dropoff=False, competition="none", fatigue="ends before 11:00 nap wall"),
    "3-5": dict(lo=3, hi=5, minutes=90, label="3-5 (preschool)",
                doctrine="Caregivers stay (1 adult : 2-3 kids minimum). Parallel-play STATIONS beat group games: "
                         "3 stations rotating every 10 min. Short group moments: parachute, bubbles, freeze dance. "
                         "NEVER elimination games — every 4yo who is 'out' cries.",
                supervision="1 adult : 2-3 kids (caregivers stay)",
                dropoff=False, competition="team/everyone-wins only", fatigue="90 min hard wall; feed them at minute 60"),
    "6-8": dict(lo=6, hi=8, minutes=120, label="6-8 (early elementary)",
                doctrine="Organized group games now work (relay, treasure hunt, musical statues). Keep 2-3 max; "
                         "mix one craft station as a calm-down. Competition OK as TEAMS. Caregivers may drop; "
                         "2 adult hosts per 10 kids.",
                supervision="1 adult : 4-5 kids",
                dropoff=True, competition="team-based fine", fatigue="food break at 60-70 min resets the room"),
    "9-12": dict(lo=9, hi=12, minutes=150, label="9-12 (tween)",
                doctrine="One marquee activity (trampoline/laser tag/NERF/movie/craft workshop) IS the party — "
                         "do not stack 5 games on top. Drop-off standard. Music they pick. Seating cliques matter: "
                         "set the table with named places.",
                supervision="1 adult : 6 kids (host visible, not leading)",
                dropoff=True, competition="self-managing", fatigue="they self-pace; guard the last 20 min for cake+chill"),
    "13+": dict(lo=13, hi=19, minutes=180, label="13+ (teen)",
                doctrine="Food + music + one anchor activity; parents absent by design. Budget shifts to food. "
                         "Co-ed guest balance matters more than games. Dark/dim lighting is requested — comply.",
                supervision="1 adult on-premise, low-visibility",
                dropoff=True, competition="n/a", fatigue="3h ceiling; later end time fine (evening)"),
}

CAKE_CHART = [  # (servings, description)
    (8, '6" round (8) — tiny party'),
    (12, '8" round single layer (12)'),
    (20, '8" round double layer (20) or 9x13 quarter-ish'),
    (24, 'quarter sheet 9x13 (24)'),
    (36, 'half sheet 11x15 (36)'),
    (48, '11x15 double-layer or 10" + 8" tier (48)'),
    (72, 'full sheet 18x24 (72)'),
]


def band_for(age: int) -> dict:
    for k, b in AGE_BANDS.items():
        if b["lo"] <= age <= b["hi"]:
            return k, b
    return "13+", AGE_BANDS["13+"]


def cake_pick(servings: int):
    best = CAKE_CHART[0]
    for s, desc in CAKE_CHART:
        if s >= servings:
            return s, desc
    return CAKE_CHART[-1][0], CAKE_CHART[-1][1] + f" — need {servings}; order 2 ({CAKE_CHART[-1][0]*2} servings)"


def timeline(band: dict, start: str) -> str:
    m = band["minutes"]
    blocks = []
    if m <= 60:  # toddler
        blocks = [(0, 15, "arrival: free play corner + music, no dead time"),
                  (15, 35, "bubbles + balloons on floor (host-led)"),
                  (35, 45, "smash-cake moment + photos"),
                  (45, 60, "quiet close: board books / goodie handout")]
    elif m == 90:  # preschool
        blocks = [(0, 15, "arrival: sticker + coloring station (soft start)"),
                  (15, 45, "station rotation (10 min each): playdough / beanbag toss / craft"),
                  (45, 55, "group moment: freeze dance or parachute"),
                  (55, 75, "food (sitting resets mood), then cake + candles"),
                  (75, 90, "favor handout + bubble exit; parents collect at door")]
    elif m == 120:  # 6-8
        blocks = [(0, 10, "arrival: name tags + warmup craft"),
                  (10, 45, "game 1 + game 2 (relay, treasure hunt) — team-based"),
                  (45, 55, "calm station + drink break"),
                  (55, 80, "food, then cake + candles"),
                  (80, 110, "game 3 (energy release: freeze dance / scavenger finale)"),
                  (110, 120, "favors + pickup flow")]
    else:  # 9-12 / teen
        blocks = [(0, 15, "arrival + music (they picked the playlist)"),
                  (15, 105, "marquee activity block (venue activity / movie / NERF / workshop)"),
                  (105, 135, "food + cake"),
                  (135, m, "hangout: music, games console, photo wall; favors on exit")]
    out = []
    hh, mm = map(int, start.split(":"))
    for a, b, what in blocks:
        t1 = f"{(hh + (mm + a) // 60) % 24:02d}:{(mm + a) % 60:02d}"
        t2 = f"{(hh + (mm + b) // 60) % 24:02d}:{(mm + b) % 60:02d}"
        out.append(f"  {t1}-{t2}  {what}")
    return "\n".join(out)


def plan(age, kids, adults, venue, budget, start):
    key, band = band_for(age)
    m = band["minutes"]
    print(f"AGE BAND {band['label']}: {m} min | {band['supervision']} | "
          f"drop-off {'OK' if band['dropoff'] else 'NO — caregivers stay'}")
    print(f"DOCTRINE: {band['doctrine']}")
    print(f"FATIGUE RULE: {band['fatigue']}")
    # headcount reality
    expect_lo, expect_hi = round(kids * 0.7), round(kids * 0.85)
    floor_needed = round(expect_hi * 2)
    print(f"\nHEADCOUNT: invited {kids} kids -> expect {expect_lo}-{expect_hi} (70-85% class show rate); "
          f"+siblings ~15% -> plan supplies for {min(kids, expect_hi + 2)}")
    if venue == "home":
        print(f"HOME CAP CHECK: activity party needs ~2 m2 open floor per child -> "
              f"{floor_needed} m2 clear floor for the expected count")
    print(f"\nTIMELINE ({m} min, start {start})\n{timeline(band, start)}")

    cake_servings = kids + adults
    s, desc = cake_pick(cake_servings)
    print(f"\nCAKE: {cake_servings} servings needed -> {desc}")

    if age >= 5:
        pizza = -(-kids * 3 // 8) + -(-adults // 3)
        print(f"FOOD: pizza -> {kids * 3} child slices + ~{adults // 3 * 8 if adults >= 3 else 0} adult slices "
              f"= {pizza} large pizzas (3 slices/child 5+, 2 under-5; 1 pizza per 3 adults)")
    else:
        print("FOOD: under-5 party = toddler snack table (fruit, crackers, cheese) + ADULT platter — "
              "adults are the real guests; order for them")
    print(f"DRINKS: {kids * 2} child servings + {adults * 2} adult servings "
          f"(juice boxes + water; coffee for caregivers at morning parties)")

    favors = min(kids, expect_hi + 2)
    favor_cost = favors * 4
    print(f"\nFAVORS: {favors} x $3-5 -> budget ${favor_cost} — one quality item (book, plant, craft kit) "
          f"beats a bag of plastic")

    if budget:
        if venue == "home":
            split = [("food", 0.40), ("cake", 0.18), ("decor", 0.12), ("activity supplies", 0.10),
                     ("favors", favor_cost / budget), ("buffer", 0.05)]
        else:
            split = [("venue package (per-child x expected count)", 0.60), ("cake", 0.15),
                     ("favors + extras (tips, pizza upgrade)", 0.15), ("buffer", 0.10)]
        print(f"\nBUDGET ${budget} ({venue} party):")
        for name, frac in split:
            print(f"  {name:<48} ${round(budget * frac)}")
        if venue == "venue":
            per_child = round(budget * 0.60 / max(expect_hi, 1))
            print(f"  -> venue budget implies ~${per_child}/child package; verify 90-min overtime fees + "
                  f"per-head cake-cutting fees in the contract")
    print(f"\nTRAPS for age {age}: ", end="")
    traps = {
        "1-2": "balloons pop into choke hazards for toddler siblings; no structured games; guests = age in years.",
        "3-5": "NO elimination games (every 'out' 4yo cries); schedule around nap (10:00 or 15:30, never 12:30); "
               "caregivers must stay — count chairs for adults.",
        "6-8": "opening presents live creates envy chaos — defer to home, do a group thank-you cheer; "
               "food break at minute 60 resets the room.",
        "9-12": "don't stack games onto a marquee activity; named seating (cliques); ask about food allergies at RSVP.",
        "13+": "co-ed balance, dim lighting, food quantity doubles; keep one adult on-premise but invisible.",
    }
    print(traps.get(key, traps["13+"]))
    print("\nRSVP etiquette: whole-class invites go through school only if ALL are invited; "
          "otherwise contact parents directly. Collect allergies at RSVP.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Kids' birthday party planner")
    ap.add_argument("--age", type=int, required=True)
    ap.add_argument("--kids", type=int, required=True, help="invited kids")
    ap.add_argument("--adults", type=int, default=0)
    ap.add_argument("--venue", choices=["home", "venue"], default="home")
    ap.add_argument("--budget", type=int, default=0)
    ap.add_argument("--start", default="10:00")
    a = ap.parse_args()
    plan(a.age, a.kids, a.adults, a.venue, a.budget, a.start)
