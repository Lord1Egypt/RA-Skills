"""OpenClaw motion-graphics core (the house style).

Style reference: openclaw.ai foundation social image (assets/style-reference.png):
near-black fresco texture, deep lobster red, bone/parchment linework, a single
ember spark. Everything is drawn procedurally with Skia. Output: ProRes 4444 w/ alpha.

Library use:   import render as R; R.set_fps(30)   # match the source video BEFORE rendering
Then build Card / LowerThird / em_* clips and call R.encode(clip, outdir).
The build() at the bottom is the original 9.9 update timeline, kept as a worked example.
"""
import math, os, sys, subprocess, json
import numpy as np
import skia
from PIL import Image, ImageFilter

W, H = 1920, 1080
FPS = 60000 / 1001


def _find_ffmpeg():
    import shutil
    for c in (os.environ.get("OPENCLAW_FFMPEG"), shutil.which("ffmpeg"),
              "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if c and os.path.exists(c):
            return c
    raise SystemExit("ffmpeg not found: install it (brew install ffmpeg) or set OPENCLAW_FFMPEG")


FFMPEG = _find_ffmpeg()
FFPROBE = os.path.join(os.path.dirname(FFMPEG), "ffprobe")


def set_fps(fps):
    """Render at the source video's frame rate (e.g. 30, 60000/1001)."""
    global FPS
    FPS = float(fps)


def rate_str():
    for num, den in ((60000, 1001), (30000, 1001), (24000, 1001)):
        if abs(FPS - num / den) < 1e-6:
            return f"{num}/{den}"
    return f"{FPS:g}"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- palette ----------
BG = (14, 9, 8)
RED = (150, 42, 32)
RED_LIT = (196, 70, 52)
GLOW = (255, 86, 52)
EMBER = (255, 138, 88)
BONE = (228, 216, 194)
BONE_DIM = (168, 154, 136)
KICK = (232, 92, 64)


def C(rgb, a=1.0):
    return skia.Color(int(rgb[0]), int(rgb[1]), int(rgb[2]), int(max(0, min(1, a)) * 255))


# ---------- fonts ----------
def tf(fam, w, italic=False):
    sl = skia.FontStyle.kItalic_Slant if italic else skia.FontStyle.kUpright_Slant
    return skia.Typeface(fam, skia.FontStyle(w, 5, sl))


TF_TITLE = tf("Baskerville", 600)
TF_ITAL = tf("Baskerville", 400, True)
TF_KICK = tf("Avenir Next Condensed", 600)
TF_KICK_H = tf("Avenir Next Condensed", 800)


# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ramp(t, t0, t1):
    return clamp((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t0)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ---------- texture ----------
def value_noise(w, h, cells, seed):
    rng = np.random.default_rng(seed)
    small = rng.random((max(2, int(h / w * cells)), cells)).astype(np.float32)
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im, np.float32) / 255.0


def make_fresco(w=W, h=H, seed=7, vignette=True):
    n = (value_noise(w, h, 6, seed) * 0.38 + value_noise(w, h, 18, seed + 1) * 0.26
         + value_noise(w, h, 60, seed + 2) * 0.16 + value_noise(w, h, 220, seed + 3) * 0.12
         + value_noise(w, h, 640, seed + 6) * 0.08)
    redb = value_noise(w, h, 9, seed + 4)
    redb = np.clip((redb - 0.55) * 2.2, 0, 1) ** 1.5
    base = np.array(BG, np.float32)[None, None, :]
    img = base * (0.7 + 0.6 * n[..., None])
    img += np.array([38, 8, 5], np.float32)[None, None, :] * redb[..., None] * (0.5 + n[..., None])
    rng = np.random.default_rng(seed + 5)
    # speckles (plaster pits / pigment flecks)
    for count, val, size in ((9000, -6, 1), (5000, 9, 1), (500, 22, 2)):
        ys = rng.integers(0, h - size, count)
        xs = rng.integers(0, w - size, count)
        for dy in range(size):
            for dx in range(size):
                img[ys + dy, xs + dx] += np.array([val, val * 0.55, val * 0.45])
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    # hairline cracks
    arr = np.asarray(im, np.float32).copy()
    crack = Image.new("L", (w, h), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(crack)
    for _ in range(26):
        x, y = rng.random() * w, rng.random() * h
        ang = rng.random() * math.tau
        pts = [(x, y)]
        for _ in range(rng.integers(20, 70)):
            ang += rng.normal(0, 0.45)
            step = rng.random() * 9 + 3
            x += math.cos(ang) * step
            y += math.sin(ang) * step
            pts.append((x, y))
        d.line(pts, fill=int(60 + rng.random() * 80), width=1)
    crack = np.asarray(crack.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
    arr *= (1 - 0.45 * crack[..., None])
    if vignette:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        r = np.sqrt(((xx - w / 2) / (w * 0.62)) ** 2 + ((yy - h / 2) / (h * 0.68)) ** 2)
        arr *= np.clip(1.15 - 0.75 * r ** 2, 0.25, 1.0)[..., None]
    return np.clip(arr, 0, 255).astype(np.uint8)


_grain = None


def grain(i):
    global _grain
    if _grain is None:
        rng = np.random.default_rng(11)
        _grain = [rng.normal(0, 3.2, (H, W, 1)).astype(np.float32) for _ in range(6)]
    return _grain[(i // 2) % 6]


def to_skimage(rgb):
    rgba = np.dstack([rgb, np.full(rgb.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)


# ---------- drawing primitives ----------
def paint(rgb, a=1.0, stroke=None, blur=None, cap=skia.Paint.kRound_Cap):
    p = skia.Paint(AntiAlias=True, Color=C(rgb, a))
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def trimmed(path, frac):
    if frac >= 0.999:
        return path
    if frac <= 0.001:
        return skia.Path()
    m = skia.PathMeasure(path, False)
    out = skia.Path()
    # walk all contours
    total = []
    while True:
        total.append(m.getLength())
        if not m.nextContour():
            break
    L = sum(total) * frac
    m = skia.PathMeasure(path, False)
    for seg in total:
        if L <= 0:
            break
        m.getSegment(0, min(seg, L), out, True)
        L -= seg
        m.nextContour()
    return out


def glow_stroke(cv, path, rgb, width, a=1.0, frac=1.0, glow=1.0, core=None):
    p = trimmed(path, frac)
    if glow > 0:
        cv.drawPath(p, paint(rgb, 0.35 * a * glow, stroke=width * 5, blur=width * 4))
        cv.drawPath(p, paint(rgb, 0.6 * a * glow, stroke=width * 2, blur=width * 1.2))
    cv.drawPath(p, paint(core or rgb, a, stroke=width))


def spark(cv, x, y, s=1.0, a=1.0, t=0.0):
    if a <= 0:
        return
    fl = 1 + 0.08 * math.sin(t * 23.0) + 0.05 * math.sin(t * 37.0 + 1)
    r = 150 * s * fl
    sh = skia.GradientShader.MakeRadial(
        (x, y), r,
        [C(GLOW, 0.55 * a), C(GLOW, 0.18 * a), C(RED, 0.05 * a), C(RED, 0)],
        [0, 0.18, 0.5, 1.0])
    cv.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Shader=sh))
    # thin horizontal flare like the reference
    fl_p = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear(
        [(x - 90 * s, y), (x + 90 * s, y)], [C(GLOW, 0), C(EMBER, 0.55 * a), C(GLOW, 0)]))
    fl_p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.2))
    cv.drawRect(skia.Rect(x - 90 * s, y - 1.0 * s, x + 90 * s, y + 1.0 * s), fl_p)
    cv.drawCircle(x, y, 7 * s, paint(EMBER, 0.9 * a, blur=4 * s))
    cv.drawCircle(x, y, 2.4 * s, paint((255, 236, 214), a))


class Embers:
    def __init__(self, n, seed, box=(0, 0, W, H), rise=28.0):
        rng = np.random.default_rng(seed)
        self.p = rng.random((n, 2)) * [box[2] - box[0], box[3] - box[1]] + [box[0], box[1]]
        self.v = np.c_[rng.normal(0, 6, n), -rng.random(n) * rise - 4]
        self.ph = rng.random(n) * math.tau
        self.sz = rng.random(n) ** 2 * 2.2 + 0.6
        self.br = rng.random(n) * 0.7 + 0.3
        self.box = box

    def draw(self, cv, t, a=1.0):
        bw, bh = self.box[2] - self.box[0], self.box[3] - self.box[1]
        for i in range(len(self.p)):
            x = (self.p[i, 0] + self.v[i, 0] * t + 10 * math.sin(t * 0.7 + self.ph[i]) - self.box[0]) % bw + self.box[0]
            y = (self.p[i, 1] + self.v[i, 1] * t - self.box[1]) % bh + self.box[1]
            tw = 0.55 + 0.45 * math.sin(t * 3.1 + self.ph[i] * 3)
            al = a * self.br[i] * tw
            cv.drawCircle(x, y, self.sz[i] * 3, paint(GLOW, 0.35 * al, blur=self.sz[i] * 2.5))
            cv.drawCircle(x, y, self.sz[i] * 0.8, paint(EMBER, al))


def draw_tracked(cv, text, x, y, font, p, track=0.0, align="left"):
    widths = [font.measureText(ch) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    if align == "center":
        x -= total / 2
    for ch, w_ in zip(text, widths):
        cv.drawString(ch, x, y, font, p)
        x += w_ + track
    return total


def text_w(text, font, track=0.0):
    return sum(font.measureText(ch) for ch in text) + track * (len(text) - 1)


def bezier(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


def poly_path(pts, close=False):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    return p


def person(cv, x, y, s, rgb, a, frac=1.0, glow=0.5):
    head = skia.Path()
    head.addCircle(x, y - 26 * s, 15 * s)
    body = skia.Path()
    body.moveTo(x - 30 * s, y + 30 * s)
    body.cubicTo(x - 30 * s, y - 2 * s, x + 30 * s, y - 2 * s, x + 30 * s, y + 30 * s)
    glow_stroke(cv, head, rgb, 2.6 * s, a, frac, glow)
    glow_stroke(cv, body, rgb, 2.6 * s, a, frac, glow)


# ---------- the claw (stylised, after the reference) ----------
_claw_tex = None


def claw_texture():
    global _claw_tex
    if _claw_tex is None:
        n = value_noise(1400, 800, 90, 21) * 0.3 + value_noise(1400, 800, 300, 22) * 0.4 + value_noise(1400, 800, 700, 23) * 0.3
        rgb = np.stack([n * 255] * 3, -1).astype(np.uint8)
        _claw_tex = to_skimage(rgb)
    return _claw_tex


def claw_paths():
    """Claw pointing right; tips near (0,0). Returns (fill path, detail paths)."""
    up_outer = bezier((-330, -150), (-210, -215), (-70, -130), (0, -6))
    up_inner = bezier((0, -6), (-70, -58), (-170, -62), (-275, -32), 50)
    lo_outer = bezier((-338, 150), (-230, 182), (-95, 120), (-14, 30))
    lo_inner = bezier((-14, 30), (-90, 62), (-175, 66), (-268, 38), 50)

    def teeth(pts, sign):
        out = []
        for i, q in enumerate(pts):
            if 4 < i < len(pts) - 3 and i % 3 == 0:
                d = pts[min(i + 1, len(pts) - 1)] - pts[i - 1]
                nrm = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-6)
                out.append(q + nrm * sign * 7)
            else:
                out.append(q)
        return out

    upper = list(up_outer) + teeth(up_inner, -1) + [(-330, -10)]
    lower = list(lo_outer) + teeth(lo_inner, 1)[::-1][::-1] + [(-330, 20)]
    palm = skia.Path()
    palm.moveTo(-660, -98)
    palm.cubicTo(-560, -150, -430, -182, -320, -152)
    palm.lineTo(-290, -40)
    palm.lineTo(-300, 60)
    palm.lineTo(-330, 152)
    palm.cubicTo(-440, 186, -570, 158, -660, 100)
    palm.close()
    fill = poly_path(upper, True)
    fill = skia.Op(fill, poly_path(lower, True), skia.kUnion_PathOp)
    fill = skia.Op(fill, palm, skia.kUnion_PathOp)
    arm = skia.Path()
    for (ax0, ax1, hh) in ((-1250, -935, 86), (-940, -770, 92), (-775, -600, 100)):
        seg_ = skia.Path()
        seg_.addRRect(skia.RRect.MakeRectXY(skia.Rect(ax0, -hh, ax1, hh), 34, 34))
        arm = skia.Op(arm, seg_, skia.kUnion_PathOp)
    fill = skia.Op(fill, arm, skia.kUnion_PathOp)
    details = []
    for x, hh in ((-620, 104), (-785, 96), (-950, 90)):
        seg = skia.Path()
        seg.moveTo(x + 10, -hh)
        seg.cubicTo(x - 16, -hh * 0.35, x - 16, hh * 0.35, x + 10, hh)
        details.append(seg)
    joint = skia.Path()
    joint.moveTo(-318, -130)
    joint.cubicTo(-300, -60, -340, -20, -305, 0)
    details.append(joint)
    seam = skia.Path()
    seam.moveTo(-330, 22)
    seam.cubicTo(-300, 60, -320, 110, -300, 150)
    details.append(seam)
    return fill, details


def draw_claw(cv, x, y, s, a=1.0, rot=0.0):
    fill, details = claw_paths()
    cv.save()
    cv.translate(x, y)
    cv.rotate(rot)
    cv.scale(s, s)
    cv.saveLayerAlpha(None, int(a * 255))
    sh = skia.GradientShader.MakeLinear([(0, -200), (0, 200)], [C((175, 58, 42)), C((120, 32, 24)), C((58, 14, 11))], [0, 0.5, 1])
    cv.drawPath(fill, skia.Paint(AntiAlias=True, Shader=sh))
    cv.save()
    cv.clipPath(fill, doAntiAlias=True)
    tp = skia.Paint(BlendMode=skia.BlendMode.kOverlay, Alphaf=0.5)
    cv.drawImageRect(claw_texture(), skia.Rect(-1260, -400, 140, 400), skia.SamplingOptions(skia.FilterMode.kLinear), tp)
    # rim darkening + top highlight
    cv.drawPath(fill, paint((20, 4, 3), 0.9, stroke=40 / s * 0 + 36, blur=16))
    hl = skia.Path(fill)
    hl.offset(0, 10)
    cv.drawPath(hl, paint((255, 140, 110), 0.18, stroke=4, blur=6))
    for d in details:
        cv.drawPath(d, paint((35, 8, 6), 0.85, stroke=7, blur=2))
        d2 = skia.Path(d)
        d2.offset(6, 0)
        cv.drawPath(d2, paint((220, 100, 80), 0.18, stroke=2, blur=1.5))
    cv.restore()
    cv.restore()
    cv.restore()


# ---------- frame helpers ----------
def new_surface():
    return skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))


def surface_rgba(surf):
    return surf.toarray(colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)


# ================== SECTION CARDS ==================
class Card:
    """Full-screen cutaway. Background push-in, emblem, kicker/title/sub."""
    fade_in = 0.30
    fade_out = 0.35

    def __init__(self, name, dur, kicker, title, sub, emblem, seed=1, emblem_cy=430, text_y=800, title_size=104, fades=None):
        if fades:
            self.fade_in, self.fade_out = fades
        self.title_size = title_size
        self.name, self.dur = name, dur
        self.kicker, self.title, self.sub = kicker, title, sub
        self.emblem, self.seed = emblem, seed
        self.cy, self.ty = emblem_cy, text_y
        self.bg = None
        self.embers = Embers(70, seed)

    def frame(self, i):
        t = i / FPS
        if self.bg is None:
            self.bg = to_skimage(make_fresco(W + 120, H + 68, seed=self.seed))
        surf = new_surface()
        cv = surf.getCanvas()
        z = 1.0 + 0.035 * (t / self.dur)
        cv.save()
        cv.translate(W / 2, H / 2)
        cv.scale(z, z)
        cv.translate(-(W + 120) / 2, -(H + 68) / 2)
        cv.drawImage(self.bg, 0, 0)
        cv.restore()
        self.embers.draw(cv, t, 0.7 * ease_io(ramp(t, 0.1, 1.0)))
        cv.save()
        cv.translate(W / 2, self.cy)
        cv.scale(z ** 0.6, z ** 0.6)
        self.emblem(cv, t, self)
        cv.restore()
        self.draw_text(cv, t)
        rgba = surface_rgba(surf).astype(np.float32)
        rgba[..., :3] += grain(i)
        fade = ease_io(ramp(t, 0, self.fade_in)) * (1 - ease_io(ramp(t, self.dur - self.fade_out, self.dur)))
        rgba[..., 3] = 255 * fade
        return np.clip(rgba, 0, 255).astype(np.uint8)

    def draw_text(self, cv, t):
        cx = W / 2
        ka = ease_out(ramp(t, 0.35, 0.85))
        if self.kicker and ka > 0:
            f = skia.Font(TF_KICK, 28)
            tr = 9 + 4 * (1 - ka)
            wk = text_w(self.kicker, f, tr)
            draw_tracked(cv, self.kicker, cx, self.ty - self.title_size * 0.95, f, paint(KICK, ka), tr, "center")
            lw = 70 * ka
            y = self.ty - self.title_size * 0.95 - 9
            cv.drawLine(cx - wk / 2 - 24 - lw, y, cx - wk / 2 - 24, y, paint(KICK, ka * 0.8, stroke=1.6))
            cv.drawLine(cx + wk / 2 + 24, y, cx + wk / 2 + 24 + lw, y, paint(KICK, ka * 0.8, stroke=1.6))
        ta = ease_out(ramp(t, 0.55, 1.15))
        if ta > 0:
            f = skia.Font(TF_TITLE, self.title_size)
            y = self.ty + 18 * (1 - ta)
            draw_tracked(cv, self.title, cx, y, f, paint((0, 0, 0), 0.55 * ta, blur=14), 1.5, "center")
            draw_tracked(cv, self.title, cx, y, f, paint(BONE, ta), 1.5, "center")
        sa = ease_out(ramp(t, 0.85, 1.45))
        if self.sub and sa > 0:
            f = skia.Font(TF_ITAL, 42)
            y = self.ty + 74 + 12 * (1 - sa)
            draw_tracked(cv, self.sub, cx, y, f, paint(BONE_DIM, sa), 0.5, "center")


# ---- emblems (drawn around origin = emblem centre) ----
def em_multiplayer(cv, t, card):
    n = 5
    ang0 = -0.25 + 0.06 * t
    rx, ry = 330, 150
    ring = skia.Path()
    ring.addOval(skia.Rect(-rx, -ry, rx, ry))
    glow_stroke(cv, ring, BONE_DIM, 1.2, 0.35, ease_io(ramp(t, 0.1, 1.2)), glow=0.2)
    ring2 = skia.Path()
    ring2.addOval(skia.Rect(-rx - 26, -ry - 14, rx + 26, ry + 14))
    cv.drawPath(trimmed(ring2, ease_io(ramp(t, 0.3, 1.5))), paint(RED_LIT, 0.35, stroke=1.0))
    pts = []
    for k in range(n):
        a = ang0 + k * math.tau / n
        pts.append((rx * math.cos(a), ry * math.sin(a)))
    order = sorted(range(n), key=lambda k: pts[k][1])
    for j, k in enumerate(order):
        x, y = pts[k]
        st = 0.35 + 0.12 * j
        line = skia.Path()
        line.moveTo(x, y - 10)
        line.quadTo(x * 0.4, y * 0.1 - 60, 0, 0)
        glow_stroke(cv, line, GLOW, 1.8, 0.85, ease_io(ramp(t, st + 0.25, st + 0.9)), glow=0.8)
        sc = 0.75 + 0.25 * (y + ry) / (2 * ry)
        person(cv, x, y - 10, sc * 1.1, BONE, ease_out(ramp(t, st, st + 0.4)), ease_io(ramp(t, st, st + 0.6)))
    spark(cv, 0, 0, 1.15, ease_out(ramp(t, 0.9, 1.3)), t)


def em_interactive(cv, t, card):
    pw, ph = 560, 320
    a_in = ease_io(ramp(t, 0.05, 0.9))
    panel = skia.Path()
    panel.addRRect(skia.RRect.MakeRectXY(skia.Rect(-pw / 2, -ph / 2, pw / 2, ph / 2), 18, 18))
    glow_stroke(cv, panel, BONE, 2.2, 0.9, a_in, glow=0.35)
    # header dots + rule
    hd = ease_out(ramp(t, 0.5, 0.9))
    for k in range(3):
        cv.drawCircle(-pw / 2 + 30 + k * 22, -ph / 2 + 28, 5, paint(BONE_DIM, 0.7 * hd))
    cv.drawLine(-pw / 2 + 18, -ph / 2 + 52, -pw / 2 + 18 + (pw - 36) * hd, -ph / 2 + 52, paint(BONE_DIM, 0.4, stroke=1.2))
    # bars with hatch
    vals = [0.35, 0.55, 0.42, 0.7, 0.62, 0.88]
    bw, gap = 54, 26
    x0 = -pw / 2 + 50
    base = ph / 2 - 36
    for k, v in enumerate(vals):
        g = ease_out(ramp(t, 0.55 + k * 0.08, 1.15 + k * 0.08))
        hgt = v * 190 * g
        r = skia.Rect(x0 + k * (bw + gap), base - hgt, x0 + k * (bw + gap) + bw, base)
        cv.drawRect(r, paint(RED, 0.75 * g))
        cv.save()
        cv.clipRect(r)
        for yy in range(int(base - 200), int(base) + 60, 9):
            cv.drawLine(r.left() - 10, yy, r.right() + 10, yy - 22, paint((0, 0, 0), 0.25, stroke=1.4))
        cv.restore()
        cv.drawRect(r, paint(RED_LIT, 0.9 * g, stroke=1.4))
    # trend line
    line = skia.Path()
    for k, v in enumerate(vals):
        px = x0 + k * (bw + gap) + bw / 2
        py = base - v * 190 - 26
        line.moveTo(px, py) if k == 0 else line.lineTo(px, py)
    glow_stroke(cv, line, EMBER, 2.4, 0.95, ease_io(ramp(t, 1.0, 1.9)), glow=1.0)
    # pin drops onto the panel corner
    pt = ease_out(ramp(t, 1.4, 1.85))
    if pt > 0:
        px, py = pw / 2 - 10, -ph / 2 + 4 - 60 * (1 - pt)
        pin = skia.Path()
        pin.moveTo(px, py)
        pin.lineTo(px + 22, py - 40)
        cv.drawPath(pin, paint(BONE, pt, stroke=3))
        cv.drawCircle(px + 26, py - 48, 13, paint(RED_LIT, pt))
        cv.drawCircle(px + 26, py - 48, 13, paint(BONE, pt, stroke=2))
        spark(cv, px, py, 0.6, ease_out(ramp(t, 1.8, 2.1)), t)


def em_memory(cv, t, card):
    rng = np.random.default_rng(5)
    n = 46
    conv = ease_io(ramp(t, 0.1, 1.7))
    for k in range(n):
        a0 = rng.random() * math.tau
        r0 = 180 + rng.random() * 260
        a = a0 + conv * 2.2
        r = r0 * (1 - conv) + 6
        x, y = r * math.cos(a), r * math.sin(a) * 0.62
        al = 0.9 * (1 - conv * 0.85)
        cv.drawCircle(x, y, 7, paint(GLOW, 0.4 * al, blur=5))
        cv.drawCircle(x, y, 2.2, paint(EMBER, al))
    for k, rr in enumerate((120, 190, 270)):
        ring = skia.Path()
        ring.addOval(skia.Rect(-rr, -rr * 0.62, rr, rr * 0.62))
        cv.drawPath(trimmed(ring, ease_io(ramp(t, 0.2 + k * 0.15, 1.2 + k * 0.15))), paint(BONE_DIM, 0.22, stroke=1.1))
    # the "skill": a cut gem / hexagon drawn on
    s = 105
    hexp = skia.Path()
    for k in range(7):
        a = math.pi / 6 + k * math.pi / 3
        (hexp.moveTo if k == 0 else hexp.lineTo)(s * math.cos(a), s * math.sin(a))
    facets = skia.Path()
    for k in range(6):
        a = math.pi / 6 + k * math.pi / 3
        facets.moveTo(0, 0)
        facets.lineTo(s * math.cos(a), s * math.sin(a))
    inner = skia.Path()
    for k in range(7):
        a = math.pi / 6 + k * math.pi / 3
        (inner.moveTo if k == 0 else inner.lineTo)(s * 0.5 * math.cos(a), s * 0.5 * math.sin(a))
    g = ease_io(ramp(t, 1.2, 2.1))
    if g > 0:
        cv.drawPath(hexp, paint(RED, 0.45 * g))
    glow_stroke(cv, hexp, BONE, 2.6, 0.95, ease_io(ramp(t, 1.1, 1.9)), glow=0.6)
    glow_stroke(cv, inner, EMBER, 1.6, 0.8, ease_io(ramp(t, 1.4, 2.1)), glow=0.8)
    cv.drawPath(trimmed(facets, ease_io(ramp(t, 1.5, 2.3))), paint(BONE_DIM, 0.55, stroke=1.2))
    spark(cv, 0, 0, 0.9, ease_out(ramp(t, 1.5, 1.9)), t)


def em_voice(cv, t, card):
    for k in range(5):
        ph = (t * 0.55 + k / 5) % 1.0
        rr = 60 + ph * 330
        al = (1 - ph) * ease_io(ramp(t, 0.2, 0.8)) * 0.7
        for side in (-1, 1):
            arc = skia.Path()
            arc.addArc(skia.Rect(-rr, -rr, rr, rr), 180 - 38 if side < 0 else -38, 76)
            cv.drawPath(arc, paint(BONE_DIM if k % 2 else RED_LIT, al, stroke=1.6))
    # waveform bars
    nb = 41
    for k in range(nb):
        u = (k - nb // 2) / (nb // 2)
        env = math.exp(-u * u * 2.8)
        reveal = ease_out(ramp(t, 0.25 + abs(u) * 0.6, 0.65 + abs(u) * 0.6))
        amp = env * (0.35 + 0.65 * abs(math.sin(t * 7.3 + k * 0.9) * math.sin(t * 3.1 + k * 0.37)))
        hh = 12 + 150 * amp * reveal
        x = u * 340
        col = EMBER if abs(u) < 0.2 else (RED_LIT if abs(u) < 0.55 else BONE_DIM)
        cv.drawLine(x, -hh, x, hh, paint(col, 0.5 * reveal, stroke=10, blur=6))
        cv.drawLine(x, -hh, x, hh, paint(col, 0.95 * reveal, stroke=5))
    spark(cv, 0, 0, 0.9, ease_out(ramp(t, 0.8, 1.2)) * 0.8, t)


def em_setup(cv, t, card):
    a_in = ease_io(ramp(t, 0.05, 1.0))
    sw, sh_ = 470, 290
    screen = skia.Path()
    screen.addRRect(skia.RRect.MakeRectXY(skia.Rect(-sw / 2, -sh_ / 2 - 30, sw / 2, sh_ / 2 - 30), 16, 16))
    basep = skia.Path()
    basep.moveTo(-sw / 2 - 60, sh_ / 2 - 6)
    basep.lineTo(sw / 2 + 60, sh_ / 2 - 6)
    basep.lineTo(sw / 2 + 40, sh_ / 2 + 14)
    basep.lineTo(-sw / 2 - 40, sh_ / 2 + 14)
    basep.close()
    glow_stroke(cv, screen, BONE, 2.4, 0.95, a_in, glow=0.35)
    glow_stroke(cv, basep, BONE, 2.0, 0.85, ease_io(ramp(t, 0.4, 1.1)), glow=0.25)
    # resources streaming in from the dark
    rng = np.random.default_rng(9)
    for k in range(18):
        side = -1 if k % 2 == 0 else 1
        sx = side * (640 + rng.random() * 200)
        sy = (rng.random() - 0.5) * 520
        st = 0.5 + rng.random() * 1.6
        u = ease_io(ramp(t, st, st + 0.9))
        if 0 < u < 1:
            x = sx + (0 - sx) * u
            y = sy + (-30 - sy) * u - math.sin(u * math.pi) * 60
            tail = skia.Path()
            tx = sx + (0 - sx) * max(0, u - 0.12)
            ty = sy + (-30 - sy) * max(0, u - 0.12) - math.sin(max(0, u - 0.12) * math.pi) * 60
            tail.moveTo(tx, ty)
            tail.lineTo(x, y)
            cv.drawPath(tail, paint(GLOW, 0.5 * (1 - u), stroke=2, blur=2))
            cv.drawCircle(x, y, 4, paint(EMBER, 1 - u * 0.6))
    # checklist rows
    for k in range(3):
        st = 1.1 + k * 0.5
        g = ease_out(ramp(t, st, st + 0.35))
        y = -sh_ / 2 + 40 + k * 64
        box = skia.Path()
        box.addRRect(skia.RRect.MakeRectXY(skia.Rect(-sw / 2 + 50, y, -sw / 2 + 82, y + 32), 6, 6))
        cv.drawPath(box, paint(BONE_DIM, 0.8 * a_in, stroke=1.8))
        chk = skia.Path()
        chk.moveTo(-sw / 2 + 56, y + 17)
        chk.lineTo(-sw / 2 + 64, y + 26)
        chk.lineTo(-sw / 2 + 80, y + 4)
        glow_stroke(cv, chk, EMBER, 3.2, 1.0, g, glow=0.9)
        cv.drawLine(-sw / 2 + 104, y + 16, -sw / 2 + 104 + (230 - k * 40) * g, y + 16, paint(BONE_DIM, 0.6, stroke=6))
    spark(cv, 0, -30 + sh_ / 2 - 40, 0.5, ease_out(ramp(t, 2.7, 3.1)) * 0.6, t)


def em_next(cv, t, card):
    # claw from the left reaching toward the spark at the start of the road
    cl = ease_out(ramp(t, 0.0, 1.4))
    draw_claw(cv, -520 - 260 * (1 - cl), 30, 0.62, 0.95 * ease_io(ramp(t, 0.0, 0.6)), rot=-4)
    spark(cv, -480, 28, 0.9, ease_out(ramp(t, 0.9, 1.3)), t)
    road = skia.Path()
    road.moveTo(-460, 28)
    road.cubicTo(-200, 28, 100, -10, 620, -10)
    glow_stroke(cv, road, RED_LIT, 2.2, 0.8, ease_io(ramp(t, 1.0, 2.0)), glow=0.6)
    labels = [("Stability", 0.0, 2.40), ("User Experience", 0.5, 3.15), ("Multiplayer", 1.0, 4.55)]
    m = skia.PathMeasure(road, False)
    L = m.getLength()
    f = skia.Font(TF_TITLE, 46)
    fk = skia.Font(TF_KICK, 22)
    for idx, (lab, u, tt) in enumerate(labels):
        pos, _ = m.getPosTan(L * (0.27 + 0.66 * u))
        x, y = pos.x(), pos.y()
        g = ease_out(ramp(t, tt, tt + 0.45))
        cv.drawCircle(x, y, 9, paint(BONE, 0.3 + 0.7 * g, stroke=2))
        if g > 0:
            cv.drawCircle(x, y, 5, paint(EMBER, g))
            spark(cv, x, y, 0.45, g * (1 - 0.6 * ease_io(ramp(t, tt + 0.4, tt + 1.2))), t)
            cv.drawLine(x, y - 18, x, y - 18 - 70 * g, paint(BONE_DIM, 0.6 * g, stroke=1.2))
            draw_tracked(cv, f"0{idx + 1}", x, y - 158 + 10 * (1 - g), fk, paint(KICK, g), 6, "center")
            draw_tracked(cv, lab, x, y - 98 + 10 * (1 - g), f, paint(BONE, g), 0.5, "center")


def em_bookend(cv, t, card):
    cl = ease_out(ramp(t, 0.0, 1.3))
    draw_claw(cv, -46 - 340 * (1 - cl), 6, 0.78, ease_io(ramp(t, 0.0, 0.5)), rot=-2)
    spark(cv, 0, 0, 1.25, ease_out(ramp(t, 0.85, 1.25)), t)


class StoryCard(Card):
    """Peter -> Vyctor -> Josh in one shared session (timed to the VO)."""

    def __init__(self, name, dur, beats):
        super().__init__(name, dur, "MULTIPLAYER IN PRACTICE", "", "", None, seed=4)
        self.beats = beats  # local seconds for Peter, Vyctor, Josh

    def frame(self, i):
        t = i / FPS
        if self.bg is None:
            self.bg = to_skimage(make_fresco(W + 120, H + 68, seed=self.seed))
        surf = new_surface()
        cv = surf.getCanvas()
        z = 1.0 + 0.03 * (t / self.dur)
        cv.save()
        cv.translate(W / 2, H / 2)
        cv.scale(z, z)
        cv.translate(-(W + 120) / 2, -(H + 68) / 2)
        cv.drawImage(self.bg, 0, 0)
        cv.restore()
        self.embers.draw(cv, t, 0.6 * ease_io(ramp(t, 0.1, 1.0)))
        ka = ease_out(ramp(t, 0.3, 0.8))
        f = skia.Font(TF_KICK, 28)
        draw_tracked(cv, self.kicker, W / 2, 190, f, paint(KICK, ka), 9, "center")
        fi = skia.Font(TF_ITAL, 40)
        draw_tracked(cv, "one agent · one shared session", W / 2, 245, fi, paint(BONE_DIM, ka * 0.9), 0.5, "center")
        # the shared session -- a long ellipse holding everyone
        sess = skia.Path()
        sess.addOval(skia.Rect(170, 320, 1750, 850))
        glow_stroke(cv, sess, RED_LIT, 1.6, 0.6, ease_io(ramp(t, 0.2, 1.6)), glow=0.5)
        xs = [560, 960, 1360]
        names = ["Peter", "Vyctor", "Josh"]
        roles = ["the feature", "the design", "the performance"]
        fn = skia.Font(TF_TITLE, 60)
        fr = skia.Font(TF_ITAL, 34)
        y = 560
        # threads between people
        for k in (1, 2):
            th = skia.Path()
            th.moveTo(xs[k - 1] + 60, y - 20)
            th.cubicTo(xs[k - 1] + 160, y - 110, xs[k] - 160, y - 110, xs[k] - 60, y - 20)
            glow_stroke(cv, th, GLOW, 2.2, 0.9, ease_io(ramp(t, self.beats[k] - 0.6, self.beats[k] + 0.2)), glow=1.0)
        for k in range(3):
            g = ease_out(ramp(t, self.beats[k], self.beats[k] + 0.5))
            if g <= 0:
                continue
            person(cv, xs[k], y, 2.0, BONE, g, ease_io(ramp(t, self.beats[k], self.beats[k] + 0.7)), glow=0.4)
            draw_tracked(cv, names[k], xs[k], y + 140 + 10 * (1 - g), fn, paint(BONE, g), 1, "center")
            draw_tracked(cv, roles[k], xs[k], y + 190 + 10 * (1 - g), fr, paint(BONE_DIM, g * 0.9), 0.5, "center")
            # active pulse on the newest collaborator
            nxt = self.beats[k + 1] if k < 2 else self.dur
            act = ramp(t, self.beats[k], self.beats[k] + 0.3) * (1 - ramp(t, nxt, nxt + 0.4))
            spark(cv, xs[k], y - 95, 0.55, act, t)
        rgba = surface_rgba(surf).astype(np.float32)
        rgba[..., :3] += grain(i)
        fade = ease_io(ramp(t, 0, self.fade_in)) * (1 - ease_io(ramp(t, self.dur - self.fade_out, self.dur)))
        rgba[..., 3] = 255 * fade
        return np.clip(rgba, 0, 255).astype(np.uint8)


# ================== LOWER THIRDS ==================
class LowerThird:
    def __init__(self, name, dur, kicker, title, sub):
        self.name, self.dur = name, dur
        self.kicker, self.title, self.sub = kicker, title, sub
        self.f_k = skia.Font(TF_KICK, 30)
        self.f_t = skia.Font(TF_TITLE, 74)
        self.f_s = skia.Font(TF_ITAL, 36)
        self.width = max(text_w(title, self.f_t, 1), text_w(sub, self.f_s, 0.5), text_w(kicker, self.f_k, 8))

    def frame(self, i):
        t = i / FPS
        out_t = self.dur - 0.55
        tin = t
        tout = ease_io(ramp(t, out_t, self.dur))
        surf = new_surface()
        cv = surf.getCanvas()
        x0, yk, yt, ys = 120, 858, 948, 1000
        # smoke backing for legibility
        ba = ease_io(ramp(tin, 0.0, 0.6)) * (1 - tout)
        if ba > 0:
            ext = self.width + 260
            cv.drawOval(skia.Rect(-260, 790, x0 + ext, 1200), paint((8, 4, 3), 0.72 * ba, blur=70))
            cv.drawOval(skia.Rect(-120, 860, x0 + ext * 0.85, 1120), paint((8, 4, 3), 0.35 * ba, blur=40))
        # vertical rule + spark
        rg = ease_out(ramp(tin, 0.1, 0.65)) * (1 - tout)
        if rg > 0:
            top = yk - 34
            bot = ys + 14
            ytop = bot - (bot - top) * rg
            cv.drawLine(x0, bot, x0, ytop, paint(GLOW, 0.5 * rg, stroke=6, blur=5))
            cv.drawLine(x0, bot, x0, ytop, paint(KICK, rg, stroke=2.4))
            spark(cv, x0, ytop, 0.55, rg, t)
        tx = x0 + 34
        # kicker
        ka = ease_out(ramp(tin, 0.3, 0.75)) * (1 - tout)
        if ka > 0:
            draw_tracked(cv, self.kicker, tx + 14 * (1 - ka), yk, self.f_k, paint(KICK, ka), 8)
        # title: wipe reveal from the rule
        for (txt, font, y, col, st, tr) in ((self.title, self.f_t, yt, BONE, 0.4, 1), (self.sub, self.f_s, ys, BONE_DIM, 0.6, 0.5)):
            g = ease_out(ramp(tin, st, st + 0.6))
            a = g * (1 - tout)
            if a <= 0:
                continue
            cv.save()
            wpx = (text_w(txt, font, tr) + 40) * g
            cv.clipRect(skia.Rect(tx - 6, y - 110, tx + wpx, y + 30))
            off = -22 * (1 - g) - 16 * tout
            draw_tracked(cv, txt, tx + off, y, font, paint((0, 0, 0), 0.6 * a, blur=10), tr)
            draw_tracked(cv, txt, tx + off, y, font, paint(col, a), tr)
            cv.restore()
        rgba = surface_rgba(surf).astype(np.float32)
        a = rgba[..., 3:4]
        rgba[..., :3] = np.where(a > 0, rgba[..., :3] * 255.0 / np.maximum(a, 1), 0)  # un-premultiply
        return np.clip(rgba, 0, 255).astype(np.uint8)


# ================== timeline ==================
def build():
    cards = [
        (24.55, Card("card-01-multiplayer", 3.20, "01  ·  OPENCLAW 9.9", "Multiplayer Mode", "One agent. Your whole team. Full context.", em_multiplayer, seed=3)),
        (57.10, StoryCard("card-01b-multiplayer-story", 12.70, beats=[0.20, 3.20, 10.35])),
        (87.70, Card("card-02-interactive-responses", 3.30, "02  ·  OPENCLAW 9.9", "Interactive Responses", "Tools, dashboards and charts you can pin.", em_interactive, seed=5)),
        (125.50, Card("card-03-memory-learning", 3.30, "03  ·  OPENCLAW 9.9", "Memory & Learning", "Lessons become reusable skills.", em_memory, seed=6)),
        (136.60, Card("card-04-meetings-voice", 3.30, "04  ·  OPENCLAW 9.9", "Meetings & Voice", "First-class voice, everywhere you work.", em_voice, seed=8)),
        (155.35, Card("card-05-easier-setup", 4.25, "05  ·  OPENCLAW 9.9", "Easier Setup", "A guided Mac installer that finds what you already have.", em_setup, seed=9)),
        (168.35, Card("card-06-whats-next", 5.95, "THE NEXT FEW MONTHS", "What’s Next", "", em_next, seed=10, emblem_cy=560, text_y=250)),
    ]
    lts = [
        (18.55, LowerThird("lt-00b-models", 5.7, "ALSO IN 9.9", "New Model Support", "Two of the latest models, ready to use")),
        (27.90, LowerThird("lt-01-multiplayer", 5.4, "01  ·  MULTIPLAYER MODE", "Now Publicly Live", "After two months in beta")),
        (40.10, LowerThird("lt-01a-meat-proxy", 5.8, "WHAT IT SOLVES", "The Meat-Proxy Problem", "No more passing agent work back and forth")),
        (76.90, LowerThird("lt-01c-cloud-session", 6.2, "ONE CLOUD SESSION", "No Git. No Local Code.", "Everyone builds in the same session")),
        (91.10, LowerThird("lt-02-interactive", 5.6, "02  ·  INTERACTIVE RESPONSES", "Build It, Then Pin It", "Tools, dashboards and charts for everyday work")),
        (104.80, LowerThird("lt-02b-content-calendar", 6.0, "EXAMPLE", "A Shared Content Calendar", "Personal view + team view in multiplayer")),
        (128.80, LowerThird("lt-03-memory", 5.6, "03  ·  MEMORY & LEARNING", "Consolidated Memories", "Past lessons turn into reusable skills")),
        (140.10, LowerThird("lt-04-voice", 5.9, "04  ·  MEETINGS & VOICE", "First-Class Voice", "Across every surface, with the latest voice models")),
        (148.40, LowerThird("lt-04b-meetings", 6.6, "IN YOUR MEETINGS", "Teams & Zoom", "Searchable notes and transcripts when you’re done")),
        (160.30, LowerThird("lt-05-setup", 6.1, "05  ·  EASIER SETUP", "Guided Mac Installer", "Finds the AI resources already on your computer")),
        (176.40, LowerThird("lt-06-cta", 3.25, "COME BACK AND TRY IT", "Download OpenClaw", "openclaw.ai")),
    ]
    bookends = [
        Card("intro-title", 3.5035, "OPENCLAW 9.9", "OpenClaw Update", "and other features you should know", em_bookend,
             seed=12, emblem_cy=400, text_y=790, title_size=132, fades=(0.35, 0.5)),
        Card("outro-foundation", 3.3033, "", "OpenClaw Foundation", "", em_bookend,
             seed=13, emblem_cy=400, text_y=790, title_size=118, fades=(0.3, 0.6)),
    ]
    return cards, lts, bookends


def nframes(dur):
    return int(round(dur * FPS))


def encode(clip, outdir):
    out = os.path.join(outdir, clip.name + ".mov")
    cmd = [FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", rate_str(), "-i", "-",
           "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuva444p10le",
           "-c:v", "prores_ks", "-profile:v", "4444", "-alpha_bits", "16", "-vendor", "apl0", "-qscale:v", "6",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(nframes(clip.dur)):
        p.stdin.write(clip.frame(i).tobytes())
    p.stdin.close()
    p.wait()
    return out, p.returncode


def still(clip, t, path):
    a = clip.frame(int(round(t * FPS)))
    Image.fromarray(a).save(path)


if __name__ == "__main__":
    cards, lts, bookends = build()
    allc = {c.name: (s, c) for s, c in cards + lts}
    allc.update({c.name: (None, c) for c in bookends})
    mode = sys.argv[1]
    if mode == "list":
        print(json.dumps({n: [round(s, 3), c.dur] for n, (s, c) in allc.items() if s is not None}, indent=1))
    elif mode == "still":
        name, t, path = sys.argv[2], float(sys.argv[3]), sys.argv[4]
        still(allc[name][1], t, path)
    elif mode == "encode":
        outdir = sys.argv[2]
        os.makedirs(outdir, exist_ok=True)
        for name in sys.argv[3:]:
            print(encode(allc[name][1], outdir), flush=True)
