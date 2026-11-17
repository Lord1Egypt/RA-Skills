#!/usr/bin/env python3
"""Bike fit estimator — frame size, contact points, pain routing.

Subcommands:
  size       Frame size + saddle height/setback/crank from body measurements
  position   Bar drop/reach class by flexibility x ride type
  pain       Symptom -> ranked fit causes -> first adjustment to try
  standover  Clearance check for a specific frame

All formulas are established bike-fit starting points (LeMond 0.885,
Holmes 25-35deg knee angle, KOPS starting setback). They get you in the
right zone; individual anatomy moves you a few mm from there.

Stdlib only. Offline.
"""
import argparse
import json
import math

# saddle-to-bar drop by (flexibility, ride type)
DROP = {
    #                endurance/commute   sportive    race
    "low":       {"endurance": (0, 1),  "sportive": (0, 2),  "race": (1, 3)},
    "medium":    {"endurance": (0, 2),  "sportive": (2, 4),  "race": (3, 6)},
    "high":      {"endurance": (1, 3),  "sportive": (3, 6),  "race": (5, 9)},
}

TYPE_STANDOVER = {"road": 2, "commuter": 3, "gravel": 4, "mtb": 6}  # cm min clearance

# ride type -> typical seat tube angle (degrees)
STA = {"road": 73.5, "commuter": 72.0, "gravel": 72.5, "mtb": 74.0}

PAIN_TABLE = {
    "front-knee": [
        ("Saddle too low — knee closes too much at top, quadriceps overworks",
         "Raise saddle +3 mm; re-check after 2 rides. Repeat to 25-35 deg knee angle."),
        ("Saddle too far forward — knee tracks ahead of the pedal axle",
         "Move saddle back 5 mm (watch total setback)."),
        ("Cleat too far back is rare for front knee; mashing big gears amplifies both",
         "Cadence 85+ while sorting geometry."),
    ],
    "back-knee": [
        ("Saddle too high — leg overextends at bottom, hamstring/posterior chain loaded",
         "Lower saddle 3 mm; repeat until heel no longer rocks."),
        ("Saddle too far back — increases effective extension",
         "Move saddle forward 5 mm."),
        ("Cleat too far forward",
         "Move cleat back 2-4 mm."),
    ],
    "outer-knee": [
        ("Cleat rotation wrong — foot angle forces IT band friction",
         "Set cleats so feet track naturally (sit on table edge, let feet hang: that angle)."),
        ("Cleat float too little",
         "Use cleats with float (e.g. yellow SPD-SL 6 deg) if forced angle persists."),
        ("Saddle too high (secondary)",
         "Lower 2 mm."),
    ],
    "numb-hands": [
        ("Too much weight forward: drop too deep or reach too long for your flexibility",
         "Raise stem with spacers or flip stem; shorten reach 10-20 mm."),
        ("Saddle nose-down shifts weight onto hands",
         "Level the saddle (small spirit level or phone app)."),
        ("Hand position monotony",
         "Flared bars / bar tape thicker; move hands every 10 min; padded gloves."),
        ("Brake hoods too low/rotated down",
         "Rotate hoods up slightly so wrists stay neutral."),
    ],
    "saddle-numbness": [
        ("Too much drop pitches you onto the nose",
         "Reduce drop 1-2 cm."),
        ("Saddle width/shape wrong for your sit-bone width",
         "Measure sit bones (foam pad or cardboard impress) -> width +20-30 mm = saddle width."),
        ("Saddle tilt",
         "Nose level to 1 deg down; never more."),
        ("Chronic: cutout/center-channel saddle; persistent perineal numbness is MEDICAL.",
         "See a doctor if numbness persists off the bike."),
    ],
    "hot-foot": [
        ("Cleat too far forward concentrates pressure under the metatarsals",
         "Move cleat back 3-5 mm."),
        ("Shoes too tight / strap placement",
         "Loosen forefoot strap; wide-fit shoes."),
        ("Socks/thickness + heat swelling on long rides",
         "Size shoes for afternoon feet; thin socks on hot days."),
    ],
    "neck-traps": [
        ("Drop too deep for current neck/hamstring flexibility",
         "Raise bars 1-2 cm; re-earn drop gradually."),
        ("Reach too long — neck hyperextends to see",
         "Shorter stem 10-20 mm."),
        ("Helmet/h Glasses fit (surprisingly common)",
         "Check helmet isn't forcing head tilt; adjust pad height."),
    ],
    "lower-back": [
        ("Reach too long + drop too deep: pelvis locked posteriorly",
         "Shorten reach 10-20 mm, raise bars."),
        ("Saddle nose-down rotates pelvis forward",
         "Level saddle."),
        ("Hamstring flexibility limit",
         "Raise bars NOW; stretch daily; drop returns as flexibility improves."),
    ],
    "hip-rocking": [
        ("Saddle too high — hips compensate for overextension",
         "Lower 2-3 mm until rock disappears (watch knees from behind, or feel)."),
    ],
}

# pain aliases -> canonical key
ALIASES = {
    "knee-front": "front-knee", "anterior-knee": "front-knee",
    "knee-back": "back-knee", "posterior-knee": "back-knee",
    "knee-outside": "outer-knee", "it-band": "outer-knee",
    "hands-numb": "numb-hands", "hand-numbness": "numb-hands",
    "perineum": "saddle-numbness", "saddle-pain": "saddle-numbness",
    "feet-hot": "hot-foot", "hotfoot": "hot-foot", "foot-numbness": "hot-foot",
    "neck": "neck-traps", "neck-pain": "neck-traps",
    "back": "lower-back", "lower-back-pain": "lower-back",
    "hips-rock": "hip-rocking", "hip-rock": "hip-rocking",
}


def deg(x):
    return math.radians(x)


def canon_symptom(s):
    s = s.strip().lower()
    return ALIASES.get(s, s)


# ------------------------------------------------------------------ size

def cmd_size(a):
    inseam = a.inseam
    height = a.height
    btype = a.type
    saddle_h = inseam * 0.885  # BB axis -> saddle top (LeMond)
    # frame size (seat tube c-t) rough bands by type
    if btype == "road":
        frame = inseam * 0.665
        frame_label = f"{frame-1:.0f}-{frame+1:.0f} cm seat tube (c-t), or equiv compact geometry"
    elif btype == "commuter":
        frame = inseam * 0.64
        frame_label = f"{frame-1:.0f}-{frame+1:.0f} cm"
    elif btype == "gravel":
        frame = inseam * 0.65
        frame_label = f"{frame-1:.0f}-{frame+1:.0f} cm"
    else:  # mtb
        mtb_bands = [(155, "S", "15\" / 38 cm"), (165, "S/M", "16\" / 41 cm"),
                     (175, "M", "17\" / 43 cm"), (185, "L", "18-19\" / 46-48 cm"),
                     (10**9, "XL", "20-21\" / 51-53 cm")]
        size_name, frame_label = next((s, f"{s} ({d}") for h, s, d in mtb_bands if height <= h)
        frame_label = frame_label + ")"
        frame = None

    crank = round(inseam * 10 * 0.20 / 2.5) * 2.5  # inseam cm->mm x0.20, snap to 2.5
    crank = min(175.0, max(160.0, crank))

    # setback: horizontal distance BB -> saddle nose, KOPS starting point
    sta = STA[btype]
    clamp_offset = saddle_h * math.cos(deg(sta))  # BB -> rail clamp, horizontal
    setback = clamp_offset - 9.0  # typical nose ~9 cm ahead of clamp
    setback = round(max(2.0, min(9.0, setback)), 1)

    standover_min = TYPE_STANDOVER[btype]
    expected_standover = round(inseam - standover_min, 1)

    return {
        "inputs": {"inseam_cm": inseam, "height_cm": height, "bike_type": btype},
        "frame_size": frame_label,
        "saddle_height_cm_bb_to_top": round(saddle_h, 1),
        "saddle_height_why": "inseam x 0.885 (LeMond); verify knee angle 25-35 deg at bottom (Holmes)",
        "crank_length_mm": crank,
        "setback_cm_bb_to_saddle_nose": setback,
        "setback_why": f"KOPS starting point at {sta} deg seat tube angle; adjust for hamstrings",
        "standover": {
            "min_clearance_cm": standover_min,
            "max_frame_standover_cm": expected_standover,
            "note": f"Frame's stated standover must be <= {expected_standover} cm for {standover_min} cm clearance",
        },
        "next": "run `position` for bar drop/reach, then `pain` if anything hurts",
    }


# ------------------------------------------------------------------ position

def cmd_position(a):
    flex = a.flexibility
    btype = a.type
    # classify ride-type bucket
    bucket = ("endurance" if btype in ("commuter", "mtb")
              else "sportive" if btype != "race" else "race")
    if btype in ("road", "gravel"):
        bucket = "sportive"
    lo, hi = DROP[flex][bucket]
    out = {
        "flexibility": flex,
        "ride_type": btype,
        "bucket": bucket,
        "saddle_to_bar_drop_cm": [lo, hi],
        "drop_meaning": "Saddle top minus bar top; negative = bars ABOVE saddle (fine for commuters)",
    }
    out["reach"] = ("Bars at your natural elbow-to-hand span. If you must lock elbows "
                    "or shrug to reach, shorten stem 10-20 mm.")
    out["saddle_tilt"] = "Level to nose-down 1 deg. Nose-up loads hands/perineum."
    out["flexibility_tests"] = [
        "standing toe touch past knees without rounding = high",
        "fingertips to mid-shin = medium",
        "knees or below = low (raise bars, don't fight it)",
    ]
    out["transition_protocol"] = [
        "Change ONE variable at a time.",
        "Ride 2-3 times (50+ km total) before judging.",
        "Increments: saddle height 2-3 mm, reach 10 mm, cleats 2 mm.",
        "Keep a ride log: what changed, when, what hurt.",
    ]
    if flex == "low":
        out["warning"] = "Low flexibility + deep drop = neck/back/perineum pain. Bars up first, stretch daily."
    return out


# ------------------------------------------------------------------ pain

def cmd_pain(a):
    key = canon_symptom(a.symptom)
    if key not in PAIN_TABLE:
        return {"error": f"unknown symptom '{a.symptom}'",
                "known": sorted(set(list(PAIN_TABLE) + list(ALIASES)))}
    rows = PAIN_TABLE[key]
    out = {"symptom": key, "likely_causes_ranked": []}
    for i, (cause, fix) in enumerate(rows, 1):
        out["likely_causes_ranked"].append({"rank": i, "cause": cause, "first_fix": fix})
    out["protocol"] = [
        "Apply the rank-1 fix ONLY. Ride 2-3 times.",
        "Better but not gone -> repeat same direction once more.",
        "No change -> move to rank 2.",
        "Worse -> revert, skip to rank 2.",
        "3-4 failed iterations or any off-the-bike symptoms -> professional fit / medical.",
    ]
    return out


# ------------------------------------------------------------------ standover

def cmd_standover(a):
    clearance = a.inseam - a.standover_height
    need = TYPE_STANDOVER.get(a.type, 3)
    ok = clearance >= need
    return {
        "inseam_cm": a.inseam,
        "frame_standover_cm": a.standover_height,
        "clearance_cm": round(clearance, 1),
        "required_cm": need,
        "verdict": "FITS" if ok else "TOO TALL",
        "note": "" if ok else f"Short by {round(need - clearance, 1)} cm — sizing down or a sloping top tube helps.",
    }


# ------------------------------------------------------------------ cli

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("size", help="frame size + contact points")
    sp.add_argument("--inseam", type=float, required=True, help="cm, book method")
    sp.add_argument("--height", type=float, required=True, help="cm, no shoes")
    sp.add_argument("--type", default="road", choices=["road", "commuter", "gravel", "mtb"])
    sp.set_defaults(fn=cmd_size)

    sp = sub.add_parser("position", help="bar drop/reach by flexibility")
    sp.add_argument("--height", type=float, required=True, help="cm")
    sp.add_argument("--flexibility", default="medium", choices=["low", "medium", "high"])
    sp.add_argument("--type", default="road", choices=["road", "commuter", "gravel", "mtb"])
    sp.set_defaults(fn=cmd_position)

    sp = sub.add_parser("pain", help="symptom -> causes -> first fix")
    sp.add_argument("--symptom", required=True,
                    help="front-knee|back-knee|outer-knee|numb-hands|saddle-numbness|hot-foot|neck-traps|lower-back|hip-rocking (aliases ok)")
    sp.set_defaults(fn=cmd_pain)

    sp = sub.add_parser("standover", help="clearance check")
    sp.add_argument("--inseam", type=float, required=True, help="cm")
    sp.add_argument("--standover-height", type=float, required=True, help="cm, frame spec")
    sp.add_argument("--type", default="road", choices=["road", "commuter", "gravel", "mtb"])
    sp.set_defaults(fn=cmd_standover)

    args = ap.parse_args()
    print(json.dumps(args.fn(args), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
