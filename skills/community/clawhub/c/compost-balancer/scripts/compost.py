#!/usr/bin/env python3
"""compost.py — compost mix balancer, diagnostician, and system sizer.

Subcommands:
  mix       compute blended C:N + moisture from 'ingredient:kg' pairs,
            prescribe exact additions when off-target
  diagnose  symptom -> cause -> fix routing (smell/heat/pests/moisture)
  size      bin system sizing from household waste stream
  log       temperature log with phase tracking (hot-pile discipline)

Ingredient values are typical midpoints; real materials vary ±30%. The
prescription math is what matters — weigh inputs once, get kg answers.
"""
import argparse
import json
import sys

# name: (C:N, moisture %, class)
ING = {
    "scraps":       (17, 85, "green"),
    "coffee":       (20, 60, "green"),
    "tea":          (20, 60, "green"),
    "grass":        (17, 80, "green"),
    "manure-chicken": (8, 55, "green"),
    "manure-horse": (22, 60, "green"),
    "manure-cow":   (23, 65, "green"),
    "weeds":        (25, 70, "green"),
    "leaves":       (55, 25, "brown"),
    "straw":        (75, 10, "brown"),
    "cardboard":    (300, 6, "brown"),
    "paper":        (175, 6, "brown"),
    "sawdust":      (400, 10, "brown"),
    "woodchips":    (400, 15, "brown"),
    "pine-needles": (70, 20, "brown"),
    "ash":          (25, 5, "brown"),
    "old-compost":  (20, 45, "green"),
}
GREEN = "high-nitrogen (green)"
BROWN = "high-carbon (brown)"
TARGET_CN = (25.0, 30.0)
TARGET_H2O = (50.0, 60.0)
HOT_MIN_M3 = 1.0

def lookup(name):
    key = name.lower().strip()
    if key in ING:
        return key, ING[key]
    for k, v in ING.items():
        if k.startswith(key) or key.startswith(k):
            return k, v
    raise SystemExit(f"unknown ingredient '{name}' — known: {', '.join(sorted(ING))}")

def parse_mix(items):
    total_n = total_w = total_h = 0.0
    parsed = []
    for it in items:
        name, _, w = it.rpartition(":")
        w = float(w)
        key, (cn, h2o, cls) = lookup(name)
        parsed.append((key, w, cn, h2o))
        total_w += w
        total_n += w * cn
        total_h += w * h2o
    if total_w == 0:
        raise SystemExit("empty mix")
    return parsed, total_n / total_w, total_h / total_w, total_w

def cmd_mix(a):
    parsed, cn, h2o, w = parse_mix(a.items)
    print(f"Mix: " + ", ".join(f"{k} {g:.1f} kg" for k, g, _, _ in parsed))
    print(f"Total {w:.1f} kg | blended C:N ≈ {cn:.0f}:1 | moisture ≈ {h2o:.0f}%")
    verdict_cn = "IN BAND" if TARGET_CN[0] <= cn <= TARGET_CN[1] else (
        "TOO NITROGENOUS (will smell ammonia)" if cn < TARGET_CN[0]
        else "TOO CARBONY (will sit cold)")
    verdict_h2o = "IN BAND" if TARGET_H2O[0] <= h2o <= TARGET_H2O[1] else (
        "TOO WET (anaerobic risk)" if h2o > TARGET_H2O[1] else "TOO DRY (stalls)")
    print(f"C:N {cn:.0f}:1 {verdict_cn}   [target 25–30:1]")
    print(f"H2O {h2o:.0f}% {verdict_h2o}   [target 50–60%]")
    if cn < TARGET_CN[0]:
        for key in ("leaves", "cardboard", "sawdust"):
            addcn = ING[key][0]
            x = w * (cn - TARGET_CN[1]) / (TARGET_CN[1] - addcn)
            if x > 0:
                print(f"  fix: add {x:.1f} kg {key} (brings C:N to ~30:1)")
    elif cn > TARGET_CN[1]:
        for key in ("coffee", "grass", "manure-chicken"):
            addcn = ING[key][0]
            x = w * (cn - TARGET_CN[0]) / (TARGET_CN[0] - addcn)
            if x > 0:
                print(f"  fix: add {x:.1f} kg {key} (brings C:N to ~25:1)")
    if h2o > TARGET_H2O[1]:
        print(f"  fix wet: turn in dry cardboard/leaves; squeeze-test a handful after")
    elif h2o < TARGET_H2O[0]:
        print(f"  fix dry: water while turning until a squeezed handful yields a few drops")
    vol = w / 350.0  # rough kg->m3 for mixed organic waste
    if vol < HOT_MIN_M3:
        print(f"Volume ≈ {vol:.2f} m³ — below the 1 m³ hot-composting threshold; "
              "expect cold-slow (still fine) or stockpile to build bigger")
    return 0

DIAG = [
    # (matcher keys, cause, fix lines)
    (dict(smell="ammonia"), "nitrogen excess (C:N < 20)",
     ["turn the pile", "add browns per 'mix' calculation (leaves/cardboard)",
      "re-check in 3 days — ammonia should fade"]),
    (dict(smell="rotten-egg"), "anaerobic: >65% moisture or compacted",
     ["turn immediately — you're venting H₂S", "fold in dry wicking browns (cardboard best)",
      "check bin base drainage; fork air channels"]),
    (dict(smell="sweet-musty"), "early-stage normal or slightly wet",
     ["usually fine; monitor temperature", "turn if it shifts to sour"]),
    (dict(heat="none"), "multiple candidates — check in order",
     ["1. size ≥ 1 m³? else merge bins / accept cold mode",
      "2. moisture 50–60%? squeeze test",
      "3. C:N ≤ 35? run 'mix' on what went in",
      "4. ambient < 10 °C? physics — insulate or wait"]),
    (dict(heat="peaked-and-dropped"), "normal thermophilic progression",
     ["TURN now (outer material to center)", "repeat each time temp drops ~10 °C from peak",
      "after 4–5 turns with no re-heat → curing phase"]),
    (dict(pest="flies"), "exposed food",
     ["bury greens ≥ 15 cm under browns", "keep a brown blanket on top",
      "no meat/dairy/oils in backyard bins"]),
    (dict(pest="rodents"), "access + nesting",
     ["6 mm hardware cloth floor + walls", "no cooked food",
      "remove cozy dry nesting material from edges"]),
    (dict(texture="slimy"), "anaerobic mats (grass clippings class)",
     ["thin layers < 10 cm", "mix in structural straw/cardboard", "turn"]),
    (dict(texture="white-powder"), "actinomycetes / fire fang — dry & past peak",
     ["normal; moisten if dusty", "turn to finish"]),
]

def cmd_diagnose(a):
    sig = {k: v for k, v in a.__dict__.items() if k not in ("fn", "cmd") and v}
    hit = False
    for match, cause, fixes in DIAG:
        if all(match.get(k) == v for k, v in match.items()) and match:
            if any(sig.get(k) == v for k, v in match.items()):
                print(f"Symptom: {match} → CAUSE: {cause}")
                for f in fixes:
                    print(f"  - {f}")
                hit = True
    if not hit:
        print("No specific match — run with --smell ammonia|rotten-egg|sweet-musty,")
        print("--heat none|peaked-and-dropped, --pest flies|rodents, --texture slimy|white-powder")
    return 0

def cmd_size(a):
    kg_day = a.people * (0.22 if not a.garden else 0.35)
    yr = kg_day * 365
    if a.mode == "hot":
        print(f"Household {a.people} → ~{kg_day:.1f} kg/day waste ({yr:.0f} kg/yr)")
        print("HOT mode: stockpile until you can fill 1 m³ at once (~250–350 kg mixed)")
        print(f"  → build {'%.0f' % (yr / 300)} hot piles/yr; 3-bin rotation (fill/cook/cure),")
        print("  each 0.8–1.0 m³, 50 cm reachable from each side. Dial thermometer essential.")
        print("  timeline: 4–8 weeks per pile with turning discipline")
    else:
        print(f"Household {a.people} → ~{kg_day:.1f} kg/day waste ({yr:.0f} kg/yr)")
        print("COLD mode: single 300–400 L bin minimum (2 better), add-as-you-go,")
        print("  bury greens, 5 cm brown blanket each addition; turn monthly if ever.")
        print("  timeline: 6–18 months to usable compost — legitimate low-effort choice")
    if a.garden:
        print("Garden waste stream: expect 2–4× kitchen mass in season; plan a leaf")
        print("surplus bin (leaf-mold: leaves only, 12–24 months, zero effort)")
    return 0

def cmd_log(a):
    import datetime
    fn = "compost_temp_log.json"
    try:
        log = json.load(open(fn))
    except Exception:
        log = []
    if a.temp is not None:
        entry = dict(date=str(datetime.date.today()), temp=a.temp, bin=a.bin)
        log.append(entry)
        json.dump(log, open(fn, "w"), indent=1)
        print(f"logged {entry['date']} {a.bin}: {a.temp} °C ({len(log)} entries)")
    temps = [e["temp"] for e in log if e["bin"] == a.bin]
    if temps:
        peak = max(temps)
        last = temps[-1]
        hot_days = sum(1 for t in temps if t >= 55)
        print(f"bin '{a.bin}': peak {peak} °C, last {last} °C, {hot_days} readings ≥55 °C")
        if peak >= 55 and last < peak - 10:
            print("  → temp fell >10 °C from peak: TURN the pile now (outside → center)")
        if hot_days >= 15:
            print("  → ≥15 hot-day readings across turns: sanitizing threshold met")
        if peak < 40 and len(temps) >= 4:
            print("  → never reached thermophilic: check size/moisture/C:N (diagnose --heat none)")
    return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mix")
    m.add_argument("items", nargs="+", help="ingredient:kg pairs, e.g. scraps:3 coffee:1")
    m.set_defaults(fn=cmd_mix)
    d = sub.add_parser("diagnose")
    d.add_argument("--smell", choices=["ammonia", "rotten-egg", "sweet-musty"])
    d.add_argument("--heat", choices=["none", "peaked-and-dropped"])
    d.add_argument("--pest", choices=["flies", "rodents"])
    d.add_argument("--texture", choices=["slimy", "white-powder"])
    d.set_defaults(fn=cmd_diagnose)
    s = sub.add_parser("size")
    s.add_argument("--people", type=int, default=4)
    s.add_argument("--mode", choices=["hot", "cold"], default="hot")
    s.add_argument("--garden", action="store_true")
    s.set_defaults(fn=cmd_size)
    g = sub.add_parser("log")
    g.add_argument("--temp", type=float)
    g.add_argument("--bin", default="main")
    g.set_defaults(fn=cmd_log)
    a = ap.parse_args()
    sys.exit(a.fn(a))

if __name__ == "__main__":
    main()
