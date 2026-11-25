# Worked example from the original project. Paths are placeholders: point them at your files.
"""OpenClaw 10.1 short: same look as the 9.9 update (render.py), new section graphics.

Clip timings are local; placement on the edit timeline lives in edit101.py.
"""
import math, os, sys, json
import numpy as np
import skia
from render import (W, H, FPS, RED, RED_LIT, GLOW, EMBER, BONE, BONE_DIM, KICK, TF_TITLE, TF_KICK,
                    Card, LowerThird, em_bookend, paint, glow_stroke, spark, trimmed, draw_tracked,
                    ramp, ease_out, ease_io, encode, still)


def hexagon(cx, cy, s):
    p = skia.Path()
    for k in range(7):
        a = math.pi / 6 + k * math.pi / 3
        (p.moveTo if k == 0 else p.lineTo)(cx + s * math.cos(a), cy + s * math.sin(a))
    return p


def em_skills(cv, t, card):
    """An agent (the spark) sweeps the dark and lights up skills as it finds them."""
    rx, ry = 360, 175
    for k, sc in enumerate((0.45, 0.75, 1.0)):
        ring = skia.Path()
        ring.addOval(skia.Rect(-rx * sc, -ry * sc, rx * sc, ry * sc))
        cv.drawPath(trimmed(ring, ease_io(ramp(t, 0.05 + 0.1 * k, 0.7 + 0.1 * k))), paint(BONE_DIM, 0.25, stroke=1.1))
    t0, rate = 0.25, math.tau / 1.7
    sweep = -math.pi / 2 + max(0.0, t - t0) * rate
    swept = max(0.0, t - t0) * rate
    sa = ease_io(ramp(t, t0, t0 + 0.2)) * (1 - ease_io(ramp(t, t0 + 1.8, t0 + 2.2)))
    if sa > 0:
        for j in range(14):
            a = sweep - j * 0.045
            cv.drawLine(0, 0, rx * math.cos(a), ry * math.sin(a), paint(GLOW, sa * 0.5 * (1 - j / 14) ** 2, stroke=2.2, blur=2))
        cv.drawLine(0, 0, rx * math.cos(sweep), ry * math.sin(sweep), paint(EMBER, sa * 0.9, stroke=1.6))
    rng = np.random.default_rng(3)
    for k in range(7):
        ang = -math.pi / 2 + 0.35 + k * math.tau / 7 + rng.normal(0, 0.12)
        rr = 0.62 + 0.38 * rng.random()
        x, y = rx * rr * math.cos(ang), ry * rr * math.sin(ang)
        rel = (ang + math.pi / 2) % math.tau          # angle the sweep needs to reach this node
        hit = t0 + rel / rate
        g = ease_out(ramp(t, hit, hit + 0.3))
        link = skia.Path()
        link.moveTo(0, 0)
        link.lineTo(x, y)
        glow_stroke(cv, link, GLOW, 1.4, 0.75 * g, ease_io(ramp(t, hit, hit + 0.25)), glow=0.7)
        hx = hexagon(x, y, 26)
        if g > 0:
            cv.drawPath(hx, paint(RED, 0.55 * g))
        glow_stroke(cv, hx, BONE, 2.0, 0.25 + 0.75 * g, ease_io(ramp(t, 0.1 + k * 0.05, 0.6 + k * 0.05)), glow=0.5 * g)
        cv.drawCircle(x, y, 4, paint(EMBER, g))
    spark(cv, 0, 0, 1.0, ease_out(ramp(t, 0.1, 0.45)), t)


def make_em_trio(labels, beats):
    def em(cv, t, card):
        road = skia.Path()
        road.moveTo(-820, 0)
        road.lineTo(820, 0)
        glow_stroke(cv, road, RED_LIT, 2.0, 0.75, ease_io(ramp(t, 0.0, 0.6)), glow=0.6)
        f = skia.Font(TF_TITLE, 41)
        fk = skia.Font(TF_KICK, 22)
        for idx, (lab, tt) in enumerate(zip(labels, beats)):
            x = -585 + 585 * idx
            g = ease_out(ramp(t, tt, tt + 0.4))
            cv.drawCircle(x, 0, 10, paint(BONE, 0.3 + 0.7 * g, stroke=2))
            if g <= 0:
                continue
            cv.drawCircle(x, 0, 5.5, paint(EMBER, g))
            spark(cv, x, 0, 0.5, g * (1 - 0.6 * ease_io(ramp(t, tt + 0.4, tt + 1.2))), t)
            cv.drawLine(x, 20, x, 20 + 64 * g, paint(BONE_DIM, 0.6 * g, stroke=1.2))
            draw_tracked(cv, f"0{idx + 3}", x, 126 + 10 * (1 - g), fk, paint(KICK, g), 6, "center")
            draw_tracked(cv, lab, x, 178 + 10 * (1 - g), f, paint(BONE, g), 0.5, "center")
    return em


def make_em_five(labels, beats):
    """Five features on one line; labels alternate below / above so they never collide."""
    def em(cv, t, card):
        road = skia.Path()
        road.moveTo(-840, 0)
        road.lineTo(840, 0)
        glow_stroke(cv, road, RED_LIT, 2.0, 0.75, ease_io(ramp(t, 0.0, 0.6)), glow=0.6)
        f = skia.Font(TF_TITLE, 40)
        fk = skia.Font(TF_KICK, 22)
        for idx, (lab, tt) in enumerate(zip(labels, beats)):
            x = -650 + 318 * idx
            up = idx % 2 == 1
            g = ease_out(ramp(t, tt, tt + 0.4))
            cv.drawCircle(x, 0, 10, paint(BONE, 0.3 + 0.7 * g, stroke=2))
            if g <= 0:
                continue
            cv.drawCircle(x, 0, 5.5, paint(EMBER, g))
            spark(cv, x, 0, 0.5, g * (1 - 0.6 * ease_io(ramp(t, tt + 0.4, tt + 1.2))), t)
            d = -1 if up else 1
            cv.drawLine(x, 20 * d, x, (20 + 60 * g) * d, paint(BONE_DIM, 0.6 * g, stroke=1.2))
            ky, ly = (-150, -112) if up else (122, 172)
            draw_tracked(cv, f"0{idx + 1}", x, ky + 10 * (1 - g), fk, paint(KICK, g), 6, "center")
            draw_tracked(cv, lab, x, ly + 10 * (1 - g), f, paint(BONE, g), 0.5, "center")
    return em


FIVE_IN = 249.60     # source time the five-feature card starts (inside segment D)
D_END, E_IN = 253.96, 272.50


def five_beats():
    """local card times of the word onsets (measured from the source audio)"""
    d = [250.68, 252.32]                 # "better skill discovery", "richer MCP applications"
    e = [272.68, 273.92, 275.20]         # "external backups", "conversation snooze", "better offline continuity"
    return [x - FIVE_IN for x in d] + [(D_END - FIVE_IN) + (x - E_IN) for x in e]


def build():
    # local beat times inside the trio card = word onsets measured from the source audio
    clips = {
        "intro-title": Card("intro-title", 3.5035, "OPENCLAW 10.1", "OpenClaw Update", "a few features you should look out for", em_bookend,
                            seed=12, emblem_cy=400, text_y=790, title_size=132, fades=(0.35, 0.5)),
        "card-01-05-features": Card("card-01-05-features", (D_END - FIVE_IN) + (276.46 - E_IN) + 0.35,
                                    "01 \u2013 05  \u00b7  OPENCLAW 10.1", "New in 10.1", "",
                                    make_em_five(["Skill Discovery", "Richer MCP Apps", "External Backups",
                                                  "Conversation Snooze", "Better Offline Continuity"], five_beats()),
                                    seed=10, emblem_cy=600, text_y=280, fades=(0.25, 0.35)),
        "lt-06-mac-setup": LowerThird("lt-06-mac-setup", 4.3, "06  ·  OPENCLAW 10.1", "Simpler Mac Setup", "Even easier to get started on a Mac"),
        "lt-07-cta": LowerThird("lt-07-cta", 3.8, "AVAILABLE NOW", "Update to 10.1", "openclaw.ai"),
        "outro-foundation": Card("outro-foundation", 3.3033, "", "OpenClaw Foundation", "", em_bookend,
                                 seed=13, emblem_cy=400, text_y=790, title_size=118, fades=(0.3, 0.6)),
    }
    return clips


if __name__ == "__main__":
    clips = build()
    mode = sys.argv[1]
    if mode == "still":
        still(clips[sys.argv[2]], float(sys.argv[3]), sys.argv[4])
    elif mode == "encode":
        os.makedirs(sys.argv[2], exist_ok=True)
        for name in sys.argv[3:]:
            print(encode(clips[name], sys.argv[2]), flush=True)
