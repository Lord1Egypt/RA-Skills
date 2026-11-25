#!/usr/bin/env python3
"""aging_audit.py — aging-in-place fall-risk audit engine.

Modes:
  --demo              run the built-in sample case (82F, walker, 1 fall)
  --answers FILE      JSON answers: {"item_id": 0-3 severity, ...} (missing = 0)
  --interactive       prompt for every item
Each catalog item: id, room, hazard, why, fix, cost band, tier (1 weekend/2 month/3 plan).
Scores 0-3 per item; outputs total score, tier lists sorted by points, escalation flags.
Stdlib only.
"""
import argparse
import json
import sys

# (id, room, hazard, why, fix, cost_band, tier, points_per_severity)
CATALOG = [
    ("bath_toilet_bar", "Bathroom", "No grab bar at toilet",
     "Sit-to-stand transfer is the #1 bathroom fall point",
     "Stud-mounted, 250-lb-rated bar beside toilet", "$25-50 + drill", 1, 4),
    ("bath_shower_bar", "Bathroom", "No grab bar in shower/tub",
     "Wet surfaces cut traction; reaching for a sliding glass door or towel bar fails",
     "Two bars (entry + wall), vertical + angled; NEVER a towel bar", "$40-80", 1, 4),
    ("bath_nonslip", "Bathroom", "No non-slip surface in tub/shower",
     "Soap + smooth tub = the classic bathtub fracture",
     "Adhesive strips or rubber mat with suction", "$10-25", 1, 3),
    ("bath_toilet_height", "Bathroom", "Toilet seat too low (standard 15in)",
     "Low seat makes rising hard with weak quadriceps",
     "Raised seat 17-19in or safety frame", "$25-60", 1, 2),
    ("bath_handheld", "Bathroom", "No handheld shower head / no seat",
     "Standing balance in shower for 10 min is avoidable",
     "Handheld shower + shower chair", "$30-80", 2, 2),
    ("bath_nightlight", "Bathroom", "No night light",
     "2AM trips in the dark are the most common nighttime fall",
     "Dusk-sensor LED plug light on the path", "$8-15", 1, 3),
    ("bed_path_light", "Bedroom", "No lit path bed->bathroom",
     "Furniture memory fails half-asleep; walking in dark compensates badly",
     "Motion-sensor plug lights along path", "$20-35", 1, 4),
    ("bed_reach", "Bedroom", "Lamp/phone not reachable from bed",
     "Getting up unaided in the dark to reach a switch",
     "Bedside lamp + phone within arm's reach; clap/tap lamp", "$15-30", 1, 3),
    ("bed_height", "Bedroom", "Bed too low/high to rise safely",
     "Knees should hit ~90 degrees seated; too-low beds trap a fallen person",
     "Risers or mattress swap to get 20-23in seat height", "$0-80", 2, 2),
    ("floor_rugs", "Floors", "Loose throw rugs",
     "The single most common trip object in elder homes",
     "Remove, or fix with dual-sided rug tape; keep only rubber-backed", "$10-20", 1, 5),
    ("floor_cords", "Floors", "Cords crossing walkways",
     "Low-visibility snags for shuffling gaits",
     "Reroute along walls, cord covers for crossings", "$10-25", 1, 3),
    ("floor_threshold", "Floors", "Doorway threshold >13 mm (1/2in)",
     "Toe catch point, worst with walkers",
     "Beveled threshold ramp", "$15-40", 2, 3),
    ("stairs_rails", "Stairs", "Rail on only one side / no rail",
     "One-sided railing gives no help when the weak side slips",
     "Rail BOTH sides, 34-36in, extend past first/last step", "$80-250", 2, 5),
    ("stairs_light", "Stairs", "Single switch (not top AND bottom)",
     "Descending stairs unlit or reaching over the void for a switch",
     "Three-way switches both ends, or motion lights", "$30-100", 1, 4),
    ("stairs_contrast", "Stairs", "No contrast strip on top/bottom steps",
     "Depth perception loss hides the last step",
     "Contrast tape on first/last treads (and nosings if worn)", "$15-30", 1, 3),
    ("stairs_clutter", "Stairs", "Objects on steps",
     "Steps are storage in many homes; a book on step 4 is a trap",
     "Clear every tread permanently; add a stair basket at top", "$0", 1, 3),
    ("stairs_first_floor", "Stairs", "No bedroom/bath on main floor",
     "Multiple daily stair trips multiply exposure; post-fall stairs end independence",
     "First-floor bedroom conversion plan, or stair lift ($3-5k) / plan Tier-3", "plan", 3, 4),
    ("kitchen_reach", "Kitchen", "Daily items above shoulder or below knee",
     "Step stools + overhead reach = fall + shoulder injury combo",
     "Reorganize: daily items between waist and shoulder", "$0", 1, 3),
    ("kitchen_stool", "Kitchen", "No safe step stool (or a folding chair in use)",
     "Chairs and wobbly stools substitute badly",
     "Step stool WITH handle rail, rated 300 lb", "$30-60", 2, 3),
    ("entry_steps", "Entries", "Entry step with no rail / no lighting",
     "Entries carry groceries + thresholds + weather at once",
     "Rail + motion floodlight; check with walker clearance", "$40-120", 2, 3),
    ("light_general", "Whole home", "General lighting dim (aging eyes need 2-3x)",
     "A 60-year-old retina gets ~1/3 the light of a 20-year-old's to the brain",
     "LED bulb swap 800+ lumens in task areas, 1600+ in rooms", "$30-80", 1, 4),
    ("comm_device", "Whole home", "No way to call for help when alone on the floor",
     "'Long lie' after a fall (>1h) drives the worst outcomes",
     "Medical alert wearable (fall-detect) + phone in every room reachable from floor", "$25-45/mo", 1, 0),
    ("meds_vision", "Whole home", "Sedating meds / new glasses / bifocals on stairs",
     "Bifocal/progressive lenses distort step depth on stairs; sedatives double fall risk",
     "Bring the med list to the doctor for a fall-risk review (beers criteria)", "$0", 2, 3),
]

ESCALATION_RULES = [
    ("repeat falls + lives alone",
     "2+ falls in 12 months while living alone: discuss medical alert NOW and a PT balance program (e.g., Stepping On / Otago)."),
    ("walker or wheelchair in a multi-level home",
     "Mobility aid + stairs: a first-floor living plan or stair lift is not optional — schedule the OT assessment."),
    ("score >= 40",
     "High density of fixable hazards: get a professional OT home assessment (orderable via the primary doctor; Medicare covers with a referral)."),
]


def run_audit(answers: dict, profile: dict):
    findings = []
    total = 0
    max_total = 0
    for item_id, room, hazard, why, fix, cost, tier, pts in CATALOG:
        sev = int(answers.get(item_id, 0))
        # comm_device scores as yes/no special: severity 3 if absent and lives alone
        if item_id == "comm_device":
            sev = 3 if sev else 0
            if not profile.get("lives_alone"):
                sev = min(sev, 2)
        max_total += 3 * pts
        if sev > 0:
            score = sev * pts
            total += score
            findings.append({"id": item_id, "room": room, "hazard": hazard, "why": why,
                             "fix": fix, "cost": cost, "tier": tier, "pts": score})
    return findings, total, max_total


def main():
    ap = argparse.ArgumentParser(description="Aging-in-place fall-risk audit")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--answers", help="JSON file {item_id: 0-3}")
    ap.add_argument("--interactive", action="store_true")
    ap.add_argument("--profile", default="{}",
                    help='JSON profile: {"age":82,"aid":"walker","falls":1,"lives_alone":true,"multilevel":true}')
    args = ap.parse_args()

    profile = json.loads(args.profile)
    if args.demo:
        profile = {"age": 82, "aid": "walker", "falls": 1, "lives_alone": True, "multilevel": True}
        answers = {"bath_toilet_bar": 3, "bath_shower_bar": 2, "bath_nonslip": 2, "bath_nightlight": 3,
                   "bed_path_light": 3, "bed_reach": 2, "floor_rugs": 3, "floor_cords": 2,
                   "stairs_rails": 3, "stairs_light": 2, "stairs_contrast": 3, "stairs_clutter": 1,
                   "kitchen_reach": 1, "light_general": 2, "comm_device": 3, "meds_vision": 2}
    elif args.answers:
        answers = json.loads(open(args.answers).read())
    elif args.interactive:
        answers = {}
        for item_id, room, hazard, why, fix, cost, tier, pts in CATALOG:
            while True:
                raw = input(f"{room}: {hazard} [0 absent/1 mild/2 notable/3 severe] ").strip()
                if raw in "0123":
                    answers[item_id] = int(raw)
                    break
    else:
        sys.exit("use --demo, --answers FILE, or --interactive")

    findings, total, max_total = run_audit(answers, profile)
    pct = round(100 * total / max_total) if max_total else 0
    level = "HIGH" if pct >= 50 else ("MODERATE" if pct >= 25 else "LOW")
    aid = profile.get("aid", "none")
    print(f"PROFILE: {profile.get('age','?')}y, aid={aid}, falls/yr={profile.get('falls',0)}, "
          f"lives_alone={profile.get('lives_alone', False)}, multilevel={profile.get('multilevel', False)}")
    print(f"TOTAL RISK SCORE: {total}/{max_total} ({pct}%) — {level}\n")

    for tier, title in [(1, "TIER 1 — this weekend (<$100)"), (2, "TIER 2 — this month (contractor)"),
                        (3, "TIER 3 — plan & budget")]:
        items = sorted([f for f in findings if f["tier"] == tier], key=lambda x: -x["pts"])
        if not items:
            continue
        print(title)
        for i, f in enumerate(items, 1):
            print(f"  {i}. {f['room']}: {f['hazard']:<44} [{f['pts']} pts] "
                  f"fix: {f['fix']}\n     cost: {f['cost']}  WHY: {f['why']}")
        print()

    print("ESCALATION")
    if profile.get("falls", 0) >= 2 and profile.get("lives_alone"):
        print("  ! " + ESCALATION_RULES[0][1])
    if aid in ("walker", "wheelchair") and profile.get("multilevel"):
        print("  ! " + ESCALATION_RULES[1][1])
    if pct >= 50:
        print("  ! " + ESCALATION_RULES[2][1])
    if not any("!" in line for line in []):
        pass
    print("\nTake this list to the primary-care doctor: med review (sedatives, blood-pressure drops) + "
          "balance program referral are as important as the hardware.")


if __name__ == "__main__":
    main()
