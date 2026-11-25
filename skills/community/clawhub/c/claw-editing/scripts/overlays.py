"""Reusable overlays on top of render.py (the house style).

- PanelTag: name tag clipped to one half of a split-screen call (panel 0 = left, 1 = right).
- SectionOverlay: centered chapter marker across the bottom ("01 · SHOW NAME" + title [+ sub]).
- Explainer: full-screen animated cutaway (kicker + title at top, emblem drawing below) whose
  elements appear on word onsets: pass beats_src={key: source_seconds}, read card.beats[key] (clip-local).
- Explainer drawing helpers: appear, text_in, kick_in, item/bullet, box, rrect_path, Wander,
  agent_in_box, tool_icon, k8s_icon, term_icon, pi_icon.
- em_* functions are the worked explainers from the OpenClaw Enterprise interview; copy and adapt.

Call R.set_fps(<source fps>) before rendering. Encode with R.encode(clip, outdir).
"""
import math, os, sys, subprocess, json
import numpy as np
import skia
import render as R
from render import (W, H, RED, RED_LIT, GLOW, EMBER, BONE, BONE_DIM, KICK, TF_TITLE, TF_ITAL, TF_KICK,
                    Card, em_bookend, paint, glow_stroke, spark, trimmed, draw_tracked, text_w,
                    ramp, ease_out, ease_io, new_surface, surface_rgba, grain)



# ---------------- overlays ----------------
def unpremul(surf):
    rgba = surface_rgba(surf).astype(np.float32)
    a = rgba[..., 3:4]
    rgba[..., :3] = np.where(a > 0, rgba[..., :3] * 255.0 / np.maximum(a, 1), 0)
    return np.clip(rgba, 0, 255).astype(np.uint8)


class PanelTag:
    """Name tag for one half of the split-screen call (clipped to that panel)."""

    def __init__(self, name, dur, panel, kicker, title, sub):
        self.name, self.dur, self.panel = name, dur, panel
        self.kicker, self.title, self.sub = kicker, title, sub
        self.f_k, self.f_t, self.f_s = skia.Font(TF_KICK, 24), skia.Font(TF_TITLE, 58), skia.Font(TF_ITAL, 29)
        self.width = max(text_w(title, self.f_t, 1), text_w(sub, self.f_s, 0.5), text_w(kicker, self.f_k, 7))

    def frame(self, i):
        t = i / R.FPS
        tout = ease_io(ramp(t, self.dur - 0.55, self.dur))
        surf = new_surface()
        cv = surf.getCanvas()
        px = 0 if self.panel == 0 else 960
        cv.save()
        cv.clipRect(skia.Rect(px, 0, px + 960, H))
        x0, yk, yt, ys = px + 64, 900, 968, 1010
        ba = ease_io(ramp(t, 0.0, 0.6)) * (1 - tout)
        if ba > 0:
            ext = self.width + 200
            cv.drawOval(skia.Rect(px - 240, 820, x0 + ext, 1200), paint((8, 4, 3), 0.72 * ba, blur=60))
        rg = ease_out(ramp(t, 0.1, 0.65)) * (1 - tout)
        if rg > 0:
            top, bot = yk - 30, (ys if self.sub else yt) + 12
            ytop = bot - (bot - top) * rg
            cv.drawLine(x0, bot, x0, ytop, paint(GLOW, 0.5 * rg, stroke=6, blur=5))
            cv.drawLine(x0, bot, x0, ytop, paint(KICK, rg, stroke=2.2))
            spark(cv, x0, ytop, 0.5, rg, t)
        tx = x0 + 30
        ka = ease_out(ramp(t, 0.3, 0.75)) * (1 - tout)
        if ka > 0:
            draw_tracked(cv, self.kicker, tx + 12 * (1 - ka), yk, self.f_k, paint(KICK, ka), 7)
        for (txt, font, y, col, st, tr) in ((self.title, self.f_t, yt, BONE, 0.4, 1), (self.sub, self.f_s, ys, BONE_DIM, 0.6, 0.5)):
            if not txt:
                continue
            g = ease_out(ramp(t, st, st + 0.6))
            a = g * (1 - tout)
            if a <= 0:
                continue
            cv.save()
            cv.clipRect(skia.Rect(tx - 6, y - 90, tx + (text_w(txt, font, tr) + 40) * g, y + 26))
            off = -20 * (1 - g) - 14 * tout
            draw_tracked(cv, txt, tx + off, y, font, paint((0, 0, 0), 0.6 * a, blur=9), tr)
            draw_tracked(cv, txt, tx + off, y, font, paint(col, a), tr)
            cv.restore()
        cv.restore()
        return unpremul(surf)


class SectionOverlay:
    """Centered chapter marker across the bottom of the split screen."""

    def __init__(self, name, dur, kicker, title, sub=""):
        self.name, self.dur, self.kicker, self.title, self.sub = name, dur, kicker, title, sub
        self.f_k, self.f_t, self.f_s = skia.Font(TF_KICK, 26), skia.Font(TF_TITLE, 66), skia.Font(TF_ITAL, 32)

    def frame(self, i):
        t = i / R.FPS
        tout = ease_io(ramp(t, self.dur - 0.6, self.dur))
        surf = new_surface()
        cv = surf.getCanvas()
        cx = W / 2
        yk, yt, ys = 902 if self.sub else 930, 975 if self.sub else 1003, 1022
        tw = max(text_w(self.title, self.f_t, 1), text_w(self.sub, self.f_s, 0.5))
        ba = ease_io(ramp(t, 0.0, 0.6)) * (1 - tout)
        if ba > 0:
            cv.drawOval(skia.Rect(cx - tw / 2 - 330, 830, cx + tw / 2 + 330, 1230), paint((8, 4, 3), 0.74 * ba, blur=70))
        ka = ease_out(ramp(t, 0.15, 0.7)) * (1 - tout)
        if ka > 0:
            tr = 8 + 4 * (1 - ka)
            wk = text_w(self.kicker, self.f_k, tr)
            draw_tracked(cv, self.kicker, cx, yk, self.f_k, paint(KICK, ka), tr, "center")
            lw = 90 * ease_out(ramp(t, 0.2, 0.9)) * (1 - tout)
            y = yk - 9
            cv.drawLine(cx - wk / 2 - 22 - lw, y, cx - wk / 2 - 22, y, paint(KICK, ka * 0.85, stroke=1.6))
            cv.drawLine(cx + wk / 2 + 22, y, cx + wk / 2 + 22 + lw, y, paint(KICK, ka * 0.85, stroke=1.6))
            spark(cv, cx - wk / 2 - 22 - lw, y, 0.4, ka, t)
            spark(cv, cx + wk / 2 + 22 + lw, y, 0.4, ka, t + 0.3)
        for (txt, font, y, col, st, tr) in ((self.title, self.f_t, yt, BONE, 0.35, 1), (self.sub, self.f_s, ys, BONE_DIM, 0.6, 0.5)):
            if not txt:
                continue
            g = ease_out(ramp(t, st, st + 0.6))
            a = g * (1 - tout)
            if a > 0:
                yy = y + 14 * (1 - g)
                draw_tracked(cv, txt, cx, yy, font, paint((0, 0, 0), 0.6 * a, blur=10), tr, "center")
                draw_tracked(cv, txt, cx, yy, font, paint(col, a), tr, "center")
        return unpremul(surf)


# ---------------- explainer helpers ----------------
F_HEAD = skia.Font(TF_TITLE, 50)
F_ITEM = skia.Font(TF_TITLE, 36)
F_ITAL = skia.Font(TF_ITAL, 32)
F_SMALL = skia.Font(TF_ITAL, 27)
F_K = skia.Font(TF_KICK, 22)


def appear(t, t0, d=0.45):
    return ease_out(ramp(t, t0, t0 + d))


def text_in(cv, txt, x, y, font, col, t, t0, align="left", track=0.5, rise=12):
    g = appear(t, t0)
    if g > 0:
        draw_tracked(cv, txt, x, y + rise * (1 - g), font, paint(col, g), track, align)
    return g


def kick_in(cv, txt, x, y, t, t0, align="left", col=KICK):
    g = appear(t, t0)
    if g > 0:
        draw_tracked(cv, txt, x, y + 8 * (1 - g), F_K, paint(col, g), 6, align)
    return g


def rrect_path(x0, y0, x1, y1, r=18):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r))
    return p


def box(cv, x0, y0, x1, y1, t, t0, col=BONE, width=2.2, dash=False, a=0.9, glow=0.35, d=0.9):
    p = rrect_path(x0, y0, x1, y1)
    if dash:
        q = paint(col, a * appear(t, t0, d), stroke=width)
        q.setPathEffect(skia.DashPathEffect.Make([14, 10], 0))
        cv.drawPath(p, q)
    else:
        glow_stroke(cv, p, col, width, a, ease_io(ramp(t, t0, t0 + d)), glow=glow)


def bullet(cv, x, y, t, t0, col=EMBER):
    g = appear(t, t0, 0.3)
    if g > 0:
        p = skia.Path()
        s = 7 * g
        p.moveTo(x, y - s); p.lineTo(x + s, y); p.lineTo(x, y + s); p.lineTo(x - s, y); p.close()
        cv.drawPath(p, paint(GLOW, 0.5 * g, blur=5))
        cv.drawPath(p, paint(col, g))


def item(cv, txt, x, y, t, t0, font=F_ITEM, col=BONE):
    bullet(cv, x, y - 12, t, t0)
    text_in(cv, txt, x + 24, y, font, col, t, t0 + 0.05)


class Wander:
    """An agent spark roaming a rectangle (deterministic)."""

    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        self.f = rng.random(4) * 0.6 + 0.35
        self.p = rng.random(4) * math.tau

    def pos(self, t, x0, y0, x1, y1):
        u = 0.5 + 0.5 * math.sin(t * self.f[0] * 1.7 + self.p[0]) * math.cos(t * self.f[1] * 0.9 + self.p[1])
        v = 0.5 + 0.5 * math.sin(t * self.f[2] * 1.3 + self.p[2]) * math.cos(t * self.f[3] * 1.1 + self.p[3])
        return x0 + (x1 - x0) * u, y0 + (y1 - y0) * v


def agent_in_box(cv, t, t0, x0, y0, x1, y1, wander, trail=True):
    g = appear(t, t0, 0.5)
    if g <= 0:
        return
    if trail:
        for k in range(10, 0, -1):
            px, py = wander.pos(t - k * 0.05, x0, y0, x1, y1)
            cv.drawCircle(px, py, 3, paint(GLOW, 0.06 * g * (10 - k), blur=3))
    x, y = wander.pos(t, x0, y0, x1, y1)
    spark(cv, x, y, 0.55, g, t)


def tool_icon(cv, x, y, kind, t, t0):
    g = appear(t, t0, 0.4)
    if g <= 0:
        return
    c = paint(BONE, 0.85 * g, stroke=2)
    if kind == 0:      # wrench-ish
        cv.drawCircle(x - 8, y - 8, 8, c); cv.drawLine(x - 2, y - 2, x + 12, y + 12, c)
    elif kind == 1:    # terminal
        cv.drawRect(skia.Rect(x - 16, y - 12, x + 16, y + 12), c)
        cv.drawLine(x - 9, y - 4, x - 3, y + 1, c); cv.drawLine(x - 3, y + 1, x - 9, y + 6, c)
    elif kind == 2:    # globe
        cv.drawCircle(x, y, 14, c); cv.drawLine(x - 14, y, x + 14, y, c)
        cv.drawOval(skia.Rect(x - 6, y - 14, x + 6, y + 14), c)
    else:              # envelope
        cv.drawRect(skia.Rect(x - 16, y - 11, x + 16, y + 11), c)
        cv.drawLine(x - 16, y - 11, x, y + 2, c); cv.drawLine(x, y + 2, x + 16, y - 11, c)


# ---------------- explainers ----------------
def em_trusted(cv, t, card):
    b = card.beats
    div = skia.Path(); div.moveTo(0, -250); div.lineTo(0, 330)
    glow_stroke(cv, div, RED_LIT, 2.2, 0.85, ease_io(ramp(t, 0.2, 1.3)), glow=0.8)
    for y in range(-240, 330, 26):          # hatching on the boundary
        g = ease_io(ramp(t, 0.2 + (y + 250) / 580, 0.5 + (y + 250) / 580))
        cv.drawLine(-7, y, 7, y + 10, paint(RED_LIT, 0.45 * g, stroke=1.2))
    xl, xr = -470, 470
    kick_in(cv, "CONTROL", xl, -232, t, b["trusted"] - 0.1, "center")
    text_in(cv, "Trusted workloads", xl, -180, F_HEAD, BONE, t, b["trusted"], "center")
    text_in(cv, "Traditional enterprise software", xl, -128, F_ITAL, BONE_DIM, t, b["traditional"], "center", 0.3)
    item(cv, "RBAC on every entity", xl - 230, -30, t, b["rbac"])
    item(cv, "Audit logs", xl - 230, 50, t, b["audit"])
    item(cv, "Security policy, enforced", xl - 230, 130, t, b["policy"])
    kick_in(cv, "AGENTS", xr, -232, t, b["untrusted"] - 0.1, "center")
    text_in(cv, "Untrusted workloads", xr, -180, F_HEAD, BONE, t, b["untrusted"], "center")
    text_in(cv, "An agent with access to tools", xr, -128, F_ITAL, BONE_DIM, t, b["agent"], "center", 0.3)
    bx0, by0, bx1, by1 = xr - 260, -70, xr + 260, 210
    box(cv, bx0, by0, bx1, by1, t, b["agent"] - 0.3, dash=True, a=0.7)
    icons = [(bx0 + 60, by0 + 55), (bx1 - 60, by0 + 55), (bx0 + 60, by1 - 50), (bx1 - 60, by1 - 50)]
    for k, (x, y) in enumerate(icons):
        tool_icon(cv, x, y, k, t, b["tools"] + 0.15 * k)
    agent_in_box(cv, t, b["agent"], bx0 + 40, by0 + 40, bx1 - 40, by1 - 40, card.wander)
    text_in(cv, "Can do anything it wants inside its environment", xr, 270, F_SMALL, BONE_DIM, t, b["anything"], "center", 0.3)


def em_isolation(cv, t, card):
    b = card.beats
    lx0, lx1, rx0, rx1, y0, y1 = -760, -120, 120, 760, -190, 230
    clusters = appear(t, b["clusters"], 0.7)
    contain = appear(t, b["container"], 0.6)
    for (a0, a1) in ((lx0, lx1), (rx0, rx1)):    # container / cluster outlines
        if contain > 0:
            q = paint(RED_LIT, 0.55 * contain, stroke=1.6)
            q.setPathEffect(skia.DashPathEffect.Make([10, 8], 0))
            cv.drawPath(rrect_path(a0 - 22, y0 - 22, a1 + 22, y1 + 22, 24), q)
        if clusters > 0:
            cv.drawPath(rrect_path(a0 - 44, y0 - 44, a1 + 44, y1 + 44, 30), paint(RED_LIT, 0.5 * clusters, stroke=1.4))
            for k in range(6):
                cv.drawCircle(a0 - 44 + (a1 - a0 + 88) * (k + 0.5) / 6, y1 + 44, 5, paint(EMBER, clusters))
    box(cv, lx0, y0, lx1, y1, t, b["control"])
    kick_in(cv, "OPENCLAW ENTERPRISE", (lx0 + lx1) / 2, y0 + 50, t, b["control"] + 0.2, "center")
    text_in(cv, "Control plane", (lx0 + lx1) / 2, y0 + 108, F_HEAD, BONE, t, b["control"] + 0.3, "center")
    for k, (lab, key) in enumerate((("Provisioning", "prov"), ("Configuration", "config"), ("Runtime config", "runtime"), ("Sandbox", "sandbox"))):
        item(cv, lab, lx0 + 70, y0 + 190 + k * 58, t, b[key], F_ITEM)
    wall = skia.Path(); wall.moveTo(0, y0 - 70); wall.lineTo(0, y1 + 70)
    glow_stroke(cv, wall, GLOW, 3.0, 0.95, ease_io(ramp(t, b["boundary"], b["boundary"] + 0.8)), glow=1.2)
    text_in(cv, "isolation boundary", 0, y0 - 92, F_SMALL, EMBER, t, b["boundary"] + 0.3, "center", 0.3)
    box(cv, rx0, y0, rx1, y1, t, b["agentbox"], dash=True, a=0.75)
    text_in(cv, "Agent", (rx0 + rx1) / 2, y0 + 108, F_HEAD, BONE, t, b["agentbox"] + 0.2, "center")
    kick_in(cv, "SANDBOX", (rx0 + rx1) / 2, y0 + 50, t, b["agentbox"] + 0.1, "center")
    agent_in_box(cv, t, b["agentbox"] + 0.3, rx0 + 60, y0 + 150, rx1 - 60, y1 - 40, card.wander)
    ya = y1 + 120
    g1 = appear(t, b["container"]) * (1 - appear(t, b["clusters"] - 0.2, 0.3))
    if g1 > 0:
        draw_tracked(cv, "By default: separate containers", 0, ya, F_ITAL, paint(BONE_DIM, g1), 0.3, "center")
    text_in(cv, "At OpenAI: completely separate clusters", 0, ya, F_ITAL, BONE, t, b["clusters"] + 0.1, "center", 0.3)


def em_contract(cv, t, card):
    b = card.beats
    R0 = 175
    ring = skia.Path(); ring.addCircle(0, 0, R0)
    std = appear(t, b["standard"], 0.8)
    glow_stroke(cv, ring, BONE, 2.4, 0.95, ease_io(ramp(t, 0.2, 1.2)), glow=0.4 + 1.2 * std)
    if std > 0:
        ring2 = skia.Path(); ring2.addCircle(0, 0, R0 + 22)
        q = paint(EMBER, 0.8 * std, stroke=1.6)
        q.setPathEffect(skia.DashPathEffect.Make([6, 9], t * 30))
        cv.drawPath(ring2, q)
    text_in(cv, "OpenClaw", 0, -52, skia.Font(TF_TITLE, 40), BONE, t, 0.5, "center")
    text_in(cv, "Enterprise", 0, -8, skia.Font(TF_TITLE, 40), BONE, t, 0.6, "center")
    for k, (lab, key) in enumerate((("SUBSTRATE", "substrate"), ("CONTROL PLANE", "control"), ("MANAGED PLANE", "managed"))):
        kick_in(cv, lab, 0, 40 + k * 34, t, b[key], "center")
    nodes = [("Sandboxes", "sandboxes", -150), ("MCP gateways", "gateways", -90), ("Secret brokers", "brokers", -30)]
    rx, ry = 640, 300
    pts = []
    for k, (lab, key, deg) in enumerate(nodes):
        a = math.radians(deg)
        pts.append((rx * math.cos(a), ry * math.sin(a), lab, b[key]))
    extra = [(180, 0.0), (140, 0.25), (105, 0.5), (75, 0.75), (40, 1.0), (0, 1.25)]
    for k, (deg, dt) in enumerate(extra):
        a = math.radians(deg)
        pts.append((rx * math.cos(a), ry * math.sin(a), "", b["else"] + dt * 0.6))
    for k, (x, y, lab, t0) in enumerate(pts):
        g = appear(t, t0)
        d = math.hypot(x, y)
        ex, ey = x / d * (R0 + 22), y / d * (R0 + 22)
        plug = skia.Path(); plug.moveTo(x, y); plug.lineTo(ex, ey)
        glow_stroke(cv, plug, GLOW, 1.6, 0.85 * g, ease_io(ramp(t, b["plug"] + 0.12 * k, b["plug"] + 0.12 * k + 0.6)), glow=0.8)
        if appear(t, b["plug"] + 0.12 * k + 0.5) > 0:
            s = 7
            cv.drawRect(skia.Rect(ex - s, ey - s, ex + s, ey + s), paint(EMBER, appear(t, b["plug"] + 0.12 * k + 0.5)))
        if g <= 0:
            continue
        if lab:
            cv.drawPath(rrect_path(x - 155, y - 40, x + 155, y + 40, 20), paint((20, 10, 8), 0.85 * g))
            box(cv, x - 155, y - 40, x + 155, y + 40, t, t0, d=0.5)
            text_in(cv, lab, x, y + 12, F_ITEM, BONE, t, t0 + 0.1, "center")
        else:
            cv.drawCircle(x, y, 16, paint(BONE_DIM, 0.6 * g, stroke=1.6))
            cv.drawCircle(x, y, 4, paint(EMBER, g))
    text_in(cv, "Plug in once, in a standard way", 0, 390, F_ITAL, BONE_DIM, t, b["standard"] + 0.2, "center", 0.3)


def k8s_icon(cv, x, y, s, g):
    p = skia.Path()
    for k in range(8):
        a = -math.pi / 2 + k * math.tau / 7
        (p.moveTo if k == 0 else p.lineTo)(x + s * math.cos(a), y + s * math.sin(a))
    cv.drawPath(p, paint(BONE, g, stroke=2.4))
    cv.drawCircle(x, y, s * 0.28, paint(BONE, g, stroke=2.2))
    for k in range(7):
        a = -math.pi / 2 + k * math.tau / 7
        cv.drawLine(x + s * 0.28 * math.cos(a), y + s * 0.28 * math.sin(a), x + s * 0.72 * math.cos(a), y + s * 0.72 * math.sin(a), paint(BONE, g, stroke=2))


def term_icon(cv, x, y, s, g):
    cv.drawRoundRect(skia.Rect(x - s, y - s * 0.72, x + s, y + s * 0.72), 8, 8, paint(BONE, g, stroke=2.4))
    cv.drawLine(x - s * 0.6, y - s * 0.2, x - s * 0.25, y + s * 0.05, paint(BONE, g, stroke=2.4))
    cv.drawLine(x - s * 0.25, y + s * 0.05, x - s * 0.6, y + s * 0.3, paint(BONE, g, stroke=2.4))
    cv.drawLine(x - s * 0.1, y + s * 0.32, x + s * 0.35, y + s * 0.32, paint(BONE, g, stroke=2.4))


def pi_icon(cv, x, y, s, g):
    cv.drawRoundRect(skia.Rect(x - s, y - s * 0.68, x + s, y + s * 0.68), 6, 6, paint(BONE, g, stroke=2.4))
    for k in range(9):
        cv.drawCircle(x - s * 0.8 + k * s * 0.2, y - s * 0.5, 2.2, paint(BONE, g))
    cv.drawRect(skia.Rect(x - s * 0.3, y - s * 0.15, x + s * 0.15, y + s * 0.35), paint(BONE, g, stroke=2))
    cv.drawRect(skia.Rect(x + s * 0.45, y - s * 0.1, x + s * 0.85, y + s * 0.4), paint(BONE, g, stroke=2))


def em_drivers(cv, t, card):
    b = card.beats
    box(cv, -330, -300, 330, -150, t, b["driver"] - 0.4)
    kick_in(cv, "OPENCLAW ENTERPRISE", 0, -248, t, b["driver"] - 0.2, "center")
    text_in(cv, "Compute driver", 0, -190, F_HEAD, BONE, t, b["driver"], "center")
    slots = [(-560, "Kubernetes", "Reference implementation", b["k8s"], k8s_icon),
             (0, "SSH", "Peter’s driver for existing dev boxes", b["ssh"], term_icon),
             (560, "Raspberry Pi", "If it’s powerful enough", b["pi"], pi_icon)]
    for x, lab, sub, t0, icon in slots:
        wire = skia.Path(); wire.moveTo(0, -150); wire.cubicTo(0, -40, x, -60, x, 40)
        glow_stroke(cv, wire, GLOW, 1.8, 0.85, ease_io(ramp(t, t0 - 0.2, t0 + 0.5)), glow=0.9)
        ph = appear(t, b["anybody"]) * (1 - appear(t, t0))
        if ph > 0 and x != -560:
            q = paint(BONE_DIM, 0.6 * ph, stroke=1.6)
            q.setPathEffect(skia.DashPathEffect.Make([10, 8], 0))
            cv.drawCircle(x, 120, 80, q)
            draw_tracked(cv, "your driver", x, 130, F_SMALL, paint(BONE_DIM, ph), 0.3, "center")
        g = appear(t, t0, 0.6)
        if g > 0:
            c = skia.Path(); c.addCircle(x, 120, 80)
            glow_stroke(cv, c, BONE, 2.2, 0.9, g, glow=0.5)
            icon(cv, x, 120, 40, g)
            spark(cv, x, 40, 0.5, g * (1 - 0.6 * appear(t, t0 + 0.6, 1.0)), t)
            text_in(cv, lab, x, 262, F_HEAD, BONE, t, t0 + 0.15, "center")
            text_in(cv, sub, x, 306, F_SMALL, BONE_DIM, t, t0 + 0.35, "center", 0.3)


def em_pilots(cv, t, card):
    b = card.beats
    part2 = card.part == 2
    T1 = -10 if part2 else 0       # step 1 already complete in part 2
    s1 = (-760, -40, -60, 300)
    s2 = (60, -250, 760, 300)
    # rising connector
    if part2:
        arr = skia.Path(); arr.moveTo(-60, 90); arr.cubicTo(-10, 90, 10, -20, 60, -20)
        glow_stroke(cv, arr, GLOW, 2.0, 0.9, ease_io(ramp(t, b["go"] - 0.3, b["go"] + 0.5)), glow=0.9)
    box(cv, *s1, t, T1 + 0.1)
    kick_in(cv, "01  ·  START HERE", s1[0] + 50, s1[1] + 56, t, T1 + 0.3)
    text_in(cv, "Q&A Agent", s1[0] + 50, s1[1] + 122, F_HEAD, BONE, t, T1 + 0.4)
    item(cv, "Read-only access", s1[0] + 60, s1[1] + 200, t, T1 + b.get("readonly", 0.6))
    item(cv, "A GTM or questions channel", s1[0] + 60, s1[1] + 256, t, T1 + b.get("channel", 0.6))
    item(cv, "Answers questions", s1[0] + 60, s1[1] + 312, t, T1 + b.get("answers", 0.6))
    if not part2:
        q = paint(BONE_DIM, 0.45 * appear(t, 0.8), stroke=1.6)
        q.setPathEffect(skia.DashPathEffect.Make([12, 10], 0))
        cv.drawPath(rrect_path(*s2), q)
        text_in(cv, "then go further…", (s2[0] + s2[2]) / 2, (s2[1] + s2[3]) / 2, F_ITAL, BONE_DIM, t, 1.0, "center", 0.3)
        return
    box(cv, *s2, t, b["go"])
    kick_in(cv, "02  ·  GO FURTHER", s2[0] + 50, s2[1] + 56, t, b["go"] + 0.2)
    text_in(cv, "Software Engineer Agent", s2[0] + 50, s2[1] + 122, F_HEAD, BONE, t, b["go"] + 0.3)
    item(cv, "Observability stack", s2[0] + 60, s2[1] + 200, t, b["obs"])
    item(cv, "Message boards", s2[0] + 60, s2[1] + 256, t, b["msg"])
    item(cv, "Code base — and can push changes", s2[0] + 60, s2[1] + 312, t, b["code"])
    g = appear(t, b["prs"], 0.6)
    if g > 0:
        y = s2[1] + 440
        spark(cv, s2[0] + 64, y - 16, 0.7, g, t)
        draw_tracked(cv, "A dozen+ PRs a day, per claw", s2[0] + 100, y + 10 * (1 - g), skia.Font(TF_TITLE, 44), paint(EMBER, g), 0.5)


def em_overhang(cv, t, card):
    b = card.beats
    x0, L = -700, 1400
    base = skia.Path(); base.moveTo(x0, -170); base.lineTo(x0, 260)
    glow_stroke(cv, base, BONE_DIM, 1.6, 0.7, ease_io(ramp(t, 0.2, 1.0)), glow=0.2)
    # what models can do
    ga = ease_io(ramp(t, b["can"], b["can"] + 1.6))
    kick_in(cv, "WHAT MODELS CAN DO TODAY", x0 + 10, -150, t, b["can"])
    cv.drawRect(skia.Rect(x0, -120, x0 + L * ga, -60), paint(RED, 0.8))
    cv.drawRect(skia.Rect(x0, -120, x0 + L * ga, -60), paint(GLOW, 0.5, stroke=1.6, blur=3))
    text_in(cv, "Solving millennium problems like Navier–Stokes", x0 + 10, -14, F_ITAL, BONE, t, b["navier"], "left", 0.3)
    # how they're used
    gu = ease_io(ramp(t, b["used"], b["used"] + 1.0))
    kick_in(cv, "HOW THEY’RE ACTUALLY USED", x0 + 10, 90, t, b["used"])
    cv.drawRect(skia.Rect(x0, 120, x0 + L * 0.16 * gu, 180), paint(BONE_DIM, 0.8))
    text_in(cv, "Maybe a Q&A chatbot", x0 + 10, 226, F_ITAL, BONE, t, b["chatbot"], "left", 0.3)
    # the gap
    gg = appear(t, b["gap"], 0.7)
    if gg > 0:
        xa, xb = x0 + L * 0.16 + 20, x0 + L
        y = 150
        q = paint(EMBER, gg, stroke=2)
        q.setPathEffect(skia.DashPathEffect.Make([10, 8], -t * 40))
        cv.drawLine(xa, y, xa + (xb - xa) * gg, y, q)
        cv.drawLine(xb, -60, xb, y, paint(EMBER, 0.7 * gg, stroke=1.6))
        draw_tracked(cv, "the overhang", (xa + xb) / 2, y - 22, skia.Font(TF_TITLE, 44), paint(EMBER, gg), 0.5, "center")


class Explainer(Card):
    def __init__(self, name, start, end, kicker, title, emblem, beats_src, seed, **kw):
        super().__init__(name, end - start, kicker, title, "", emblem, seed=seed, emblem_cy=kw.pop("cy", 620),
                         text_y=kw.pop("text_y", 175), title_size=kw.pop("title_size", 78), fades=(0.35, 0.45))
        self.start = start
        self.beats = {k: v - start for k, v in beats_src.items()}
        self.wander = Wander(seed)
        self.part = kw.get("part", 1)
        self.embers.p[:, 1] = self.embers.p[:, 1]  # keep


