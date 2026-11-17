#!/usr/bin/env python3
"""Ergo Desk Calibrator — personal workstation numbers from body height.

Stdlib only. Reflects widely published ergonomic guidance (OSHA-style
computer workstation concepts); not medical advice.
"""
import argparse

# anthropometric fractions of stature H (cm)
F_SEAT = 0.26        # popliteal + shoe allowance
F_ELBOW_ABOVE_SEAT = 0.155
F_DESK = F_SEAT + F_ELBOW_ABOVE_SEAT   # 0.415
F_EYE_SIT = 0.674    # seated erect eye height from floor
F_ELBOW_STAND = 0.63
F_VIEW = 0.38        # viewing distance target before clamping

SYMPTOMS = {
    "neck": [
        ("Monitor top edge below eye line (neck flexion)", "raise screen: top edge at/below eye line", 0.9),
        ("Laptop flat on desk", "riser to eye line + external keyboard/mouse", 0.85),
        ("Monitor too far / text too small (leaning in)", "distance 50-85 cm, increase font 10-15%", 0.6),
        ("Document flat on desk (head bobbing)", "document holder beside screen", 0.4),
        ("Craning at a second monitor placed to the side", "primary monitor straight ahead; secondary at ~30°", 0.4),
    ],
    "shoulder": [
        ("Desk too high → shrugged shoulders", "raise chair to elbow height + footrest, or lower desk", 0.9),
        ("Mouse too far away (reaching)", "mouse next to keyboard, elbows at sides", 0.7),
        ("Armrests too high/low", "armrests support forearms at elbow height, not pushing shoulders", 0.5),
        ("Phone pinched ear-to-shoulder", "headset/speakerphone", 0.5),
    ],
    "wrist": [
        ("Keyboard positive tilt (feet out)", "fold feet flat, slight negative tilt", 0.8),
        ("Wrists extended (angled up) while typing", "keyboard at elbow height; wrists neutral/floating", 0.8),
        ("Wrist rests used WHILE typing", "rest only during pauses", 0.5),
        ("Mouse gripping too high/low", "mouse at keyboard level, close in", 0.6),
    ],
    "eye": [
        ("Screen closer than 50 cm", "push back to 50-85 cm, enlarge text", 0.85),
        ("Screen glare / facing window", "screen perpendicular to windows; matte filter", 0.7),
        ("No breaks (accommodation lock)", "20-20-20 rule: every 20 min look 6 m away for 20 s", 0.8),
        ("Screen much dimmer/darker than room", "match screen to room brightness", 0.5),
        ("Uncorrected vision at monitor distance", "eye exam; mention computer distance ~66 cm", 0.5),
    ],
    "back": [
        ("Chair lacks lumbar support / pelvis rotated back", "support at belt line; sit bones bearing weight", 0.85),
        ("Seat too deep (no knee room, slouch forward)", "seat depth: 3-finger gap behind knees", 0.6),
        ("Feet dangling (pelvis tips)", "lower chair or footrest", 0.6),
        ("Wallet/objects in back pocket", "empty pockets", 0.4),
        ("Too many consecutive hours seated", "stand/walk 5 min every 30-60 min", 0.6),
    ],
}

def cm(x):
    return f"{x:.1f} cm"

def cmd_calibrate(a):
    H = a.height
    print(f"PERSONAL ERGONOMIC NUMBERS for height {H:.0f} cm"
          f"{' (STANDING desk)' if a.standing else ' (sitting)'}")
    print()
    if a.standing:
        desk = F_ELBOW_STAND * H
        eye = 0.936 * H
        print(f"  Standing desk height:   {cm(desk)}  (elbow height; elbows 90-110°)")
        print(f"  Monitor top edge:       {cm(eye - 5)} to {cm(eye)} (at/slightly below standing eye line {cm(eye)})")
        print(f"  Viewing distance:       {cm(max(50, F_VIEW*H))} or more")
        print(f"  Anti-fatigue:           stand 15-30 min per hour, not all day;")
        print(f"                          one foot on a rail/box alternately; soft mat.")
        print(f"  Tilt:                   desk 5-10° downward away from you if available.")
    else:
        seat = F_SEAT * H
        desk = F_DESK * H
        eye = F_EYE_SIT * H
        view = min(85, max(50, F_VIEW * H))
        print(f"  Chair seat height:      {cm(seat)}  (feet flat, knees 90-100°)")
        print(f"  Desk / keyboard height: {cm(desk)}  (elbows 90-110°, shoulders relaxed)")
        print(f"  Monitor TOP edge:       {cm(eye)} from floor = {cm(eye - desk)} above desk")
        print(f"  Screen center:          ~10-15 cm below eye line")
        print(f"  Viewing distance:       50-85 cm (your target ~{cm(view)})")
        print(f"  Lumbar support:         at belt line (L4-L5); recline 100-110°")
        print(f"  Feet:                   flat on floor or footrest — never crossed")
        print()
        if a.desk:
            print(f"  YOUR DESK {a.desk} cm vs ideal {cm(desk)}:")
            d = a.desk - desk
            if d > 2:
                print(f"    {cm(d)} too high → raise chair by {cm(d)}, add footrest "
                      f"{cm(max(0, d))}.")
            elif d < -2:
                print(f"    {cm(-d)} too low → risers under legs (stable!), or "
                      f"higher chair + footrest.")
            else:
                print("    within tolerance ±2 cm. Good.")

def cmd_monitor(a):
    H = a.height
    panel_h = a.size * 2.54 * 0.49  # 16:9 panel height from diagonal
    eye_above_desk = F_EYE_SIT * H - F_DESK * H
    stand_low = a.stand  # bottom edge above desk on lowest setting
    top = stand_low + panel_h
    dist = min(95, max(55, F_VIEW * H + (a.size - 24) * 1.1))
    print(f"{a.size}\" monitor (panel height ≈ {cm(panel_h)}), your eye line is "
          f"{cm(eye_above_desk)} above the desk surface.")
    print(f"Bottom edge on lowest stand ≈ {cm(stand_low)} above desk → "
          f"top edge ≈ {cm(top)} above desk.")
    d = top - eye_above_desk
    if d > 1.5:
        print(f"  VERDICT: top edge {cm(d)} ABOVE eye line → lower stand; if at "
              f"minimum: increase distance to ~{cm(dist)} and tilt screen up slightly.")
    elif d < -12:
        print(f"  VERDICT: top edge {cm(-d)} below eye line → raise monitor by "
              f"riser {cm(-d - 5)} (aim: top edge at/slightly below eye line).")
    else:
        print(f"  VERDICT: GOOD — top edge near/below eye line. "
              f"Keep distance ≈ {cm(dist)}.")
    print(f"Recommended viewing distance for {a.size}\": ~{cm(dist)} "
          f"(arm's-length check: fully extended fingers just touch the screen).")

def cmd_laptop(a):
    H = a.height
    print("LAPTOP PROTOCOL — the screen/keyboard conflict is unsolvable in")
    print("one device; split the functions:\n")
    print(f"  1. Screen: raise laptop so its TOP edge reaches your eye line")
    print(f"     ({cm(F_EYE_SIT*H - F_DESK*H)} above the desk) — riser stand or")
    print(f"     books; use external keyboard + mouse. This is the only fix.")
    print("  2. Short sessions (<30 min) without riser: accept the compromise,")
    print("     but never all-day on a flat laptop.")
    print("  3. On the sofa/bed: pillow behind back, laptop on cushion at")
    print("     lap height, screen tilted far back — neck angle is the enemy.")
    print("  4. Docking at a desk: lid closed + external screen beats")
    print("     laptop-open-plus-monitor (dual different heights = constant neck")
    print("     repositioning) unless screens are height-matched.")
    print("\nBudget path: books + any USB keyboard fixes 80% of the problem for $15.")

def cmd_symptom(a):
    rows = SYMPTOMS[a.pain]
    print(f"PAIN: {a.pain} → ranked likely causes (probability heuristic):")
    for i, (cause, fix, p) in enumerate(sorted(rows, key=lambda r: -r[2]), 1):
        print(f"  {i}. [{p*100:.0f}%] {cause}")
        print(f"       FIX: {fix}")
    print("\nIf fixes don't relieve within 1-2 weeks, see a clinician — this is")
    print("geometry triage, not medicine.")

def cmd_checklist(a):
    items = [
        "Feet flat on floor/footrest; knees 90-100°; legs not crossed",
        "Sit bones bearing weight; small lumbar cushion at belt line",
        "Elbows 90-110°, shoulders LOW (shrug test: raise shoulders, drop)",
        "Wrists neutral while typing; keyboard feet folded flat",
        "Mouse NEXT to keyboard, same height, no reaching",
        "Monitor TOP edge at or just below eye line",
        "Screen 50+ cm away; text readable without leaning",
        "Screen perpendicular to windows; no light source behind screen",
        "Documents on a holder beside the screen, not flat on desk",
        "20-20-20: every 20 min → look ~6 m away for 20 s",
        "Stand/walk 5 min every 30-60 min (best posture = next posture)",
        "Water within reach (dehydration amplifies fatigue and headache)",
    ]
    print("POSTURE SELF-AUDIT (weekly):")
    for i, s in enumerate(items, 1):
        print(f"  [ ] {i:2d}. {s}")
    print("\nScore: 10+/12 = solid; <8 = pick the 3 worst and fix this week.")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("calibrate", help="your numbers from height")
    c.add_argument("--height", type=float, required=True)
    c.add_argument("--standing", action="store_true")
    c.add_argument("--desk", type=float, default=None, help="your actual desk height for comparison")
    c.set_defaults(fn=cmd_calibrate)

    m = sub.add_parser("monitor", help="check a monitor size for your setup")
    m.add_argument("--height", type=float, required=True)
    m.add_argument("--size", type=float, required=True, help="diagonal inches")
    m.add_argument("--stand", type=float, default=5.0, help="bottom edge height above desk on lowest stand, cm")
    m.set_defaults(fn=cmd_monitor)

    l = sub.add_parser("laptop", help="laptop compromise protocol")
    l.add_argument("--height", type=float, required=True)
    l.set_defaults(fn=cmd_laptop)

    s = sub.add_parser("symptom", help="pain → ranked causes → fixes")
    s.add_argument("--pain", required=True, choices=sorted(SYMPTOMS))
    s.set_defaults(fn=cmd_symptom)

    k = sub.add_parser("checklist", help="12-point posture self-audit")
    k.set_defaults(fn=cmd_checklist)

    a = p.parse_args()
    a.fn(a)

if __name__ == "__main__":
    main()
