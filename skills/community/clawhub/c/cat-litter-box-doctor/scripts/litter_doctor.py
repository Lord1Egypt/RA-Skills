#!/usr/bin/env python3
"""Litter box doctor: diagnosis ladder, box audit, transitions, decontamination.

Commands:
  diagnose     (interactive: red flags -> medical -> box audit -> marking fork)
  boxes        --cats N --boxes N [--hooded yes|no] [--location TXT]
               [--scooped hourly|daily|2day|weekly] [--senior yes|no]
  transition   --from LITTER --to LITTER [--days 7]
  decon        --surface TXT --severity fresh|set-in|recurring
All doctrine from references/elimination-rules-and-protocols.md.
"""
import argparse

RED_FLAGS = [
    ("straining_no_urine",
     "Straining/crying in the box with NO urine produced (esp. MALE cat)"),
    ("blood_urine", "Pink/red/bloody urine or blood-tinged litter"),
    ("frequent_small", "Frequent small attempts + genital licking + hiding"),
    ("anuria_vomiting", "No urine 12h+ with vomiting/lethargy"),
]

MEDICAL_QUESTIONS = [
    ("sudden_change", "Change was SUDDEN (cat previously always used the box)?"),
    ("senior_cat", "Cat is 10+ years old?"),
    ("large_clumps", "Clumps/urine volume noticeably LARGER, or drinking more?"),
    ("straining_history", "Any straining, crying, or repeated quick box visits?"),
    ("defecation_issue", "Problem is (also) defecation: dry stool/straining/diarrhea?"),
    ("weight_loss", "Weight loss or appetite change in recent months?"),
    ("arthritis_signs", "Hesitates jumping, stiff gait, stops covering waste?"),
]

BEHAVIOR_QUESTIONS = [
    ("posture_standing", "Cat backs to VERTICAL surfaces standing, tail quivering?"),
    ("small_amounts", "Deposits are SMALL and strongly scented (not full volumes)?"),
    ("new_trigger", "Recent change: new pet/baby/renovation/outdoor cat at window?"),
    ("multi_cat_tension", "Multi-cat home with staring/blocking/boxing-out?"),
    ("box_adjacent", "Accidents happen right BESIDE the box?"),
    ("soft_surfaces", "Preference for beds/rugs/bath mats (soft absorbent surfaces)?"),
    ("laundry_piles", "Targets laundry piles or specific person's belongings?"),
]


def ask(key: str, text: str) -> bool:
    while True:
        a = input(f"  {text} [y/n] ").strip().lower()
        if a in ("y", "yes", "n", "no"):
            return a.startswith("y")


def cmd_diagnose(args) -> None:
    print("= LITTER BOX DIAGNOSIS LADDER =")
    print("\nSTEP 0 — RED FLAGS (emergency screen):")
    for key, text in RED_FLAGS:
        if ask(key, text):
            print("\n!! EMERGENCY: urethral obstruction / hematuria cluster.")
            print("   STOP. Go to an emergency vet NOW (male blocked cat: death")
            print("   in 24-72h). Do not continue behavioral triage.")
            return

    print("\nSTEP 1 — MEDICAL SCREEN (a 'no' here changes everything):")
    medical_hits = [k for k, t in MEDICAL_QUESTIONS if ask(k, t)]
    if medical_hits:
        print(f"\n-> {len(medical_hits)} medical signal(s): {', '.join(medical_hits)}")
        print("   VERDICT: VET FIRST (urinalysis + age-appropriate bloods,")
        print("   arthritis/pain assessment). Sudden-change cats have a body")
        print("   problem until proven otherwise. Re-run this after the visit;")
        print("   box fixes below are still worth doing in parallel.")
    else:
        print("   No medical signals reported — proceed, but any sudden change")
        print("   still warrants a urinalysis before calling it behavioral.")

    print("\nSTEP 2 — MARKING vs TOILETING FORK:")
    beh = {k: ask(k, t) for k, t in BEHAVIOR_QUESTIONS}
    spray_score = sum((beh["posture_standing"], beh["small_amounts"],
                       beh["new_trigger"], beh["multi_cat_tension"]))
    toilet_score = sum((beh["box_adjacent"], beh["soft_surfaces"],
                        beh["laundry_piles"]))
    if spray_score >= 2 and spray_score > toilet_score:
        print("   FORK: SPRAYING/MARKING (anxiety-territory communication).")
        print("   Plan: identify+reduce trigger (outdoor-cat sightlines, inter-cat")
        print("   tension), enzymatic-clean all marks, pheromone diffuser,")
        print("   play therapy; never punish (raises the anxiety driving it).")
        print("   Refractory after 4-6 wks: vet discussion of anxiolytics.")
    else:
        print("   FORK: TOILETING (box rejection or urgency).")
        print("   Plan: full box audit next — count/scoop/location/litter.")
        if beh["box_adjacent"]:
            print("   - Beside-box deposits = box itself rejected (cleanliness,")
            print("     litter, hood, or a medical urgency). Scoop 2x/day now.")
        if beh["soft_surfaces"]:
            print("   - Soft-surface preference: add a fine unscented clumping")
            print("     box; trial litters side-by-side; consider attraction additive.")

    print("\nSTEP 3 — BOX MANAGEMENT AUDIT (fix ALL failures at once):")
    cats = int(input("  Number of cats? ") or "1")
    boxes = int(input("  Number of litter boxes? ") or "1")
    need = cats + 1
    if boxes < need:
        print(f"   [FAIL] {boxes} box(es) for {cats} cat(s): rule is cats+1 = {need}.")
    else:
        print(f"   [ok] {boxes} boxes for {cats} cats (>= cats+1).")
    print("   Daily scoop minimum (2x/day during resolution); unscented soap wash;")
    print("   1.5x body-length boxes; hood off for anxious/ambushed/senior cats;")
    print("   quiet location with sightlines, away from appliances.")

    print("\nSTEP 4 — DECONTAMINATE every accident site (enzymatic only,")
    print("   never ammonia/bleach; blacklight pass for old sites).")
    print("\nRe-assess at 2 weeks: no improvement -> recheck medicals, then")
    print("escalate per references/ follow-up ladder.")


def cmd_boxes(args) -> None:
    fails, warns = [], []
    need = args.cats + 1
    if args.boxes < need:
        fails.append(f"count: {args.boxes} box(es) for {args.cats} cat(s) "
                     f"(rule: cats+1 = {need})")
    if args.scooped in ("weekly", "2day"):
        fails.append(f"scooped {args.scooped}: daily minimum, 2x/day during "
                     f"resolution")
    elif args.scooped == "daily":
        warns.append("scooped daily: acceptable; 2x/day during active resolution")
    loc = (args.location or "").lower()
    if any(w in loc for w in ("laundry", "washer", "boiler", "furnace",
                              "utility", "garage", "basement")):
        fails.append(f"location '{args.location}': appliance/noise/remote zone; "
                     f"move to quiet area with sightlines")
    if args.hooded == "yes":
        if args.senior == "yes":
            fails.append("hood + senior cat: arthritis makes hoods/height a pain "
                         "wall; open low-entry box")
        else:
            warns.append("hood: offer one open box alongside; hoods trap odor and "
                         "block escape sightlines")
    if args.senior == "yes":
        warns.append("senior: low-entry box, 1 more box than rule, night lighting "
                     "on route; vet arthritis assessment")
    print(f"BOX AUDIT — {args.cats} cat(s), {args.boxes} box(es)")
    for f in fails:
        print(f"  [FAIL] {f}")
    for w in warns:
        print(f"  [warn] {w}")
    if not fails and not warns:
        print("  [ok] management basics pass — problem is medical or "
              "substrate/location specifics")
    if fails:
        print(f"Verdict: {len(fails)} management failure(s) — fix ALL before any "
              f"behavior conclusion.")


def cmd_transition(args) -> None:
    days = args.days
    steps = [(1, 75, 25), (2, 50, 50), (3, 25, 75)]
    if days < 7:
        print("Note: 7 days is the floor; slower is safer. Using 7.")
    print(f"LITTER TRANSITION: {args.src} -> {args.dst} over 7 days")
    for d, old, new in steps:
        if d == 1:
            print(f"  Day 1-2: {old}% {args.src} / {new}% {args.dst}")
        elif d == 2:
            print(f"  Day 3-4: {old}% {args.src} / {new}% {args.dst}")
        else:
            print(f"  Day 5-6: {old}% {args.src} / {new}% {args.dst}")
    print(f"  Day 7:   100% {args.dst}")
    print("  PLUS: one fallback box of pure old litter in another location;")
    print("  keep it 7+ days after full switch.")
    print("  Roll back one stage on any refusal sign: circling, fast exit,")
    print("  half-in posture, deposit at box edge.")


def cmd_decon(args) -> None:
    print(f"DECONTAMINATION — {args.surface} ({args.severity})")
    print("  1. Blot (never rub) fresh urine; remove solids.")
    print("  2. Rinse with cool water; blot again.")
    print("  3. ENZYMATIC cleaner (urease/uricase class): saturate to the depth")
    print("     the urine reached — carpet means pad/underlay too.")
    print("  4. Keep wet per label (10-15 min, covered), air-dry. Repeat once.")
    if args.severity == "set-in":
        print("  5. SET-IN: blacklight (365 nm) scan in darkness for ALL sites;")
        print("     inject enzymatic into padding depth; treat both faces.")
    if args.severity == "recurring":
        print("  5. RECURRING: cat re-marking treated spot = unresolved trigger")
        print("     (see marking fork) or a missed crystal site — rescan.")
    if any(w in (args.surface or "").lower() for w in ("carpet", "couch",
                                                       "mattress", "fabric",
                                                       "rug")):
        print("  Fabric note: never steam BEFORE enzymatic (heat bonds proteins);")
        print("  mattress: syringe-inject cleaner, both sides, 2 wks to full cure.")
    print("  NEVER: ammonia cleaners (advertises 'cat toilet'), bleach (ignores")
    print("  uric acid; toxic mix), vinegar-only (masks briefly).")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("diagnose"); p.set_defaults(func=cmd_diagnose)
    p = sub.add_parser("boxes")
    p.add_argument("--cats", type=int, required=True)
    p.add_argument("--boxes", type=int, required=True)
    p.add_argument("--hooded", default="no", choices=["yes", "no"])
    p.add_argument("--location", default="")
    p.add_argument("--scooped", default="daily",
                   choices=["hourly", "daily", "2day", "weekly"])
    p.add_argument("--senior", default="no", choices=["yes", "no"])
    p.set_defaults(func=cmd_boxes)
    p = sub.add_parser("transition")
    p.add_argument("--from", dest="src", required=True)
    p.add_argument("--to", dest="dst", required=True)
    p.add_argument("--days", type=int, default=7)
    p.set_defaults(func=cmd_transition)
    p = sub.add_parser("decon")
    p.add_argument("--surface", required=True)
    p.add_argument("--severity", default="fresh",
                   choices=["fresh", "set-in", "recurring"])
    p.set_defaults(func=cmd_decon)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
