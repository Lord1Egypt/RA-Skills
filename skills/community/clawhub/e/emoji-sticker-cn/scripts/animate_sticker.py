#!/usr/bin/env python3
"""单张静态贴纸 → 内容匹配动效 GIF(emoji-sticker-cn v2,零 API 成本)。

源图需透明底(PNG RGBA)。按情绪配方(蓄力→动作→过冲→落定 + 程序化粒子符号)
输出循环透明 GIF,默认微信规范 240×240、≤500KB。配方与情绪匹配规则见
references/动效匹配规则.md。

用法:
  python3 animate_sticker.py cat.png --recipe happy --out cat_happy.gif
  python3 animate_sticker.py cat.png --recipe sleepy --out sleep.gif
  python3 animate_sticker.py cat.png --anim bounce --out old.gif   # v1 兼容映射
  python3 animate_sticker.py --list                                # 查看全部配方
"""
import argparse
import math
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
    from PIL.Image import Resampling
except ImportError:
    sys.stderr.write("缺少依赖 Pillow,请先运行: pip install Pillow\n")
    sys.exit(2)

LANCZOS = Resampling.LANCZOS
BICUBIC = Resampling.BICUBIC

# ---------- 缓动(禁止线性运动) ----------
def ease_in(t):
    return t * t * t

def ease_out(t):
    return 1 - (1 - t) ** 3

def ease_out_back(t, s=1.70158):
    t -= 1
    return 1 + (s + 1) * t ** 3 + s * t * t

def clamp01(t):
    return max(0.0, min(1.0, t))

# ---------- 主体 ----------
def load_subject(path):
    im = Image.open(path).convert("RGBA")
    bbox = im.getbbox()
    if bbox is None:
        sys.stderr.write(f"错误: {path} 是全透明图,没有任何可见像素\n")
        sys.exit(2)
    return im.crop(bbox)

def dominant_color(subject):
    """主体主色(提亮保可见),粒子配色用。"""
    small = subject.resize((24, 24))
    alpha = small.getchannel("A").tobytes()
    pix = small.load()
    n = r = g = b = 0
    for y in range(24):
        for x in range(24):
            if alpha[y * 24 + x] > 128:
                p = pix[x, y]
                n += 1
                r += p[0]
                g += p[1]
                b += p[2]
    if n == 0:
        return (255, 200, 60)
    r, g, b = r // n, g // n, b // n
    m = max(r, g, b)
    if m < 160:
        k = 160 / max(m, 1)
        r, g, b = int(r * k), int(g * k), int(b * k)
    return (min(r, 255), min(g, 255), min(b, 255))

# ---------- 配方:每类返回 (sx, sy, dx, dy, rot),f(0)=f(1) 保证无缝循环 ----------
def r_happy(t, S):
    sx = sy = 1.0; dx = dy = 0.0; rot = 0.0
    if t < 0.18:            # 蓄力下蹲(ease-in)
        u = ease_in(t / 0.18); q = 0.12 * u
        sy = 1 - q; sx = 1 + q * 0.9; dy = 3 * u
    elif t < 0.62:          # 弹跳(抛物线 + 空中拉伸)
        u = (t - 0.18) / 0.44
        h = math.sin(math.pi * u)
        dy = -S[1] * 0.16 * h
        st = 0.07 * h
        sy = 1 + st; sx = 1 - st * 0.8
    elif t < 0.80:          # 落地压扁
        u = (t - 0.62) / 0.18
        q = 0.14 * math.sin(math.pi * u)
        sy = 1 - q; sx = 1 + q * 0.9; dy = 2 * math.sin(math.pi * u)
    else:                   # 回弹呼吸(衰减)
        u = (t - 0.80) / 0.20
        w = math.sin(2 * math.pi * u) * (1 - u)
        sy = 1 + 0.02 * w; sx = 1 - 0.02 * w
    return sx, sy, dx, dy, rot

def r_angry(t, S):
    f = math.sin(2 * math.pi * 6 * t)
    dx = S[0] * 0.022 * f
    rot = 2.0 * math.sin(2 * math.pi * 6 * t + 0.6)
    s = 1 + 0.02 * f
    return s, s, dx, 0.0, rot

def r_sad(t, S):
    rot = 2.5 * math.sin(2 * math.pi * t)
    dy = S[1] * 0.03 * (0.5 + 0.5 * math.sin(2 * math.pi * t - math.pi / 2))
    s = 1 - 0.015 * (0.5 + 0.5 * math.sin(2 * math.pi * t - math.pi / 2))
    return s, s, 0.0, dy, rot

def r_surprised(t, S):
    s = 1 + 0.16 * (math.sin(math.pi * t) ** 0.7)   # 快起慢落
    rot = 1.0 * math.sin(math.pi * t)
    return s, s, 0.0, -S[1] * 0.02 * math.sin(math.pi * t), rot

def r_shy(t, S):
    rot = 4.0 * math.sin(2 * math.pi * t)
    dy = S[1] * 0.015 * math.sin(2 * math.pi * t + math.pi / 3)
    s = 1 + 0.01 * math.sin(2 * math.pi * t)
    return s, s, 0.0, dy, rot

def r_speechless(t, S):
    w = math.sin(2 * math.pi * t)
    return 1 - 0.008 * w, 1 + 0.012 * w, 0.0, 1.5 * w, 0.5 * w

def r_sleepy(t, S):
    w = math.sin(2 * math.pi * t)
    return 1 - 0.018 * w, 1 + 0.02 * w, 0.0, 2.0 * w, 0.0

def r_neutral(t, S):
    w = math.sin(2 * math.pi * t)
    return 1 - 0.02 * w, 1 + 0.025 * w, 0.0, 0.0, 0.0

def r_text(t, S):
    s = 1 + 0.10 * max(0.0, math.sin(2 * math.pi * t)) ** 0.8
    dx = S[0] * 0.012 * math.sin(2 * math.pi * 2 * t)
    return s, s, dx, 0.0, 1.2 * math.sin(2 * math.pi * 2 * t)

RECIPES = {
    "happy":      r_happy,
    "angry":      r_angry,
    "sad":        r_sad,
    "surprised":  r_surprised,
    "shy":        r_shy,
    "speechless": r_speechless,
    "sleepy":     r_sleepy,
    "neutral":    r_neutral,
    "text":       r_text,
}

# 配方元数据:帧数 / 基础帧时长 ms / 关键姿势停留帧(×1.8)/ 底部锚定
META = {
    "happy":      (14, 85,  (0, 7, 13), True),
    "angry":      (12, 55,  (0, 11),    True),
    "sad":        (12, 170, (0, 6, 11), False),
    "surprised":  (8,  90,  (0, 7),     False),
    "shy":        (12, 150, (0, 6, 11), False),
    "speechless": (10, 160, (0, 9),     False),
    "sleepy":     (12, 150, (0, 6, 11), False),
    "neutral":    (10, 140, (0, 5, 9),  False),
    "text":       (12, 110, (0, 6, 11), True),
}

LEGACY = {"bounce": "happy", "shake": "angry", "pulse": "neutral", "wobble": "shy"}

# ---------- 粒子(程序化绘制,极简几何风;坐标为静止主体框的相对比例) ----------
PARTICLES = {
    "happy": [
        dict(kind="star",  rx=0.12, ry=-0.10, r=10, phase=0.20, dur=0.50, motion="twinkle"),
        dict(kind="star",  rx=0.88, ry=-0.06, r=12, phase=0.30, dur=0.45, motion="twinkle"),
        dict(kind="star",  rx=0.50, ry=-0.16, r=9,  phase=0.40, dur=0.40, motion="twinkle"),
    ],
    "angry": [
        dict(kind="anger", rx=0.10, ry=-0.04, r=14, phase=0.0, dur=1.0, motion="pulse"),
        dict(kind="anger", rx=0.90, ry=-0.04, r=14, phase=0.0, dur=1.0, motion="pulse"),
    ],
    "sad": [
        dict(kind="drop",  rx=0.82, ry=0.02, r=9, phase=0.10, dur=0.55, motion="fall"),
    ],
    "surprised": [
        dict(kind="excl",  rx=0.74, ry=-0.12, r=12, phase=0.0, dur=0.50, motion="pop"),
    ],
    "shy": [
        dict(kind="heart", rx=0.08, ry=-0.02, r=8, phase=0.10, dur=0.50, motion="rise"),
        dict(kind="heart", rx=0.92, ry=-0.06, r=9, phase=0.40, dur=0.50, motion="rise"),
    ],
    "speechless": [
        dict(kind="dots",  rx=0.76, ry=-0.10, r=10, phase=0.15, dur=0.60, motion="twinkle"),
        dict(kind="drop",  rx=0.24, ry=0.00, r=7, phase=0.45, dur=0.50, motion="fall"),
    ],
    "sleepy": [
        dict(kind="zzz",   rx=0.80, ry=-0.04, r=9,  phase=0.05, dur=0.55, motion="rise"),
        dict(kind="zzz",   rx=0.88, ry=-0.14, r=11, phase=0.35, dur=0.55, motion="rise"),
        dict(kind="zzz",   rx=0.96, ry=-0.24, r=13, phase=0.65, dur=0.55, motion="rise"),
    ],
    "neutral": [],
    "text": [],
}

PCOLOR = {"anger": (230, 60, 60), "drop": (120, 180, 240), "heart": (240, 90, 120),
          "zzz": (150, 150, 255), "dots": (130, 130, 130)}

def _font(size):
    try:
        return ImageFont.load_default(size)
    except Exception:
        return ImageFont.load_default()

def draw_particle(d, spec, t, box, dom_color):
    p = (t - spec["phase"]) / spec["dur"]
    if p <= 0 or p >= 1:
        return
    x0, y0, w, h = box
    cx = x0 + spec["rx"] * w
    cy = y0 + spec["ry"] * h
    alpha = int(235 * math.sin(math.pi * p))
    r = spec["r"]
    m = spec["motion"]
    if m == "twinkle":
        s = 0.65 + 0.35 * math.sin(math.pi * p * 3)
    elif m == "rise":
        s = 0.8 + 0.5 * p
        cy -= p * h * 0.22
        cx += p * w * 0.08
    elif m == "fall":
        s = 1.0
        cy += p * h * 0.30
    elif m == "pop":
        s = max(0.05, ease_out_back(p))
    else:  # pulse
        s = 0.9 + 0.15 * math.sin(math.pi * p * 4)
    r2 = max(1.0, r * s)
    kind = spec["kind"]
    col = PCOLOR.get(kind, dom_color)

    if kind == "star":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r2 if i % 2 == 0 else r2 * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col + (alpha,))
    elif kind == "heart":
        d.ellipse([cx - r2, cy - r2 * 0.9, cx, cy + r2 * 0.1], fill=col + (alpha,))
        d.ellipse([cx, cy - r2 * 0.9, cx + r2, cy + r2 * 0.1], fill=col + (alpha,))
        d.polygon([(cx - r2 * 0.98, cy - r2 * 0.05), (cx + r2 * 0.98, cy - r2 * 0.05), (cx, cy + r2)],
                  fill=col + (alpha,))
    elif kind == "drop":
        d.polygon([(cx, cy - r2 * 1.4), (cx - r2 * 0.75, cy + r2 * 0.5), (cx + r2 * 0.75, cy + r2 * 0.5)],
                  fill=col + (alpha,))
        d.ellipse([cx - r2 * 0.75, cy - r2 * 0.1, cx + r2 * 0.75, cy + r2 * 1.1], fill=col + (alpha,))
    elif kind == "anger":
        for ang in (45, 135, 225, 315):
            a = math.radians(ang)
            d.line([cx + r2 * 0.45 * math.cos(a), cy + r2 * 0.45 * math.sin(a),
                    cx + r2 * 1.05 * math.cos(a), cy + r2 * 1.05 * math.sin(a)],
                   fill=col + (alpha,), width=max(2, int(r2 * 0.28)))
    elif kind in ("zzz", "excl", "dots"):
        txt = {"zzz": "Z", "excl": "!", "dots": "…"}[kind]
        d.text((cx, cy), txt, fill=col + (alpha,), font=_font(int(r2 * 1.6)), anchor="mm")

# ---------- 渲染 ----------
def make_frame(subject, size, k, sx, sy, dx, dy, rot, bottom):
    w = max(1, int(subject.width * k * sx))
    h = max(1, int(subject.height * k * sy))
    s = subject.resize((w, h), LANCZOS)
    if rot:
        s = s.rotate(rot, resample=BICUBIC, expand=True)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (size[0] - s.width) // 2 + int(dx)
    y = (size[1] - s.height - 8) + int(dy) if bottom else (size[1] - s.height) // 2 + int(dy)
    canvas.paste(s, (x, y), s)
    return canvas

def build_frames(subject, size, recipe, n, scale):
    base = int(size[1] * scale)
    k = base / max(subject.height, 1)
    bottom = META[recipe][3]
    fn = RECIPES[recipe]
    specs = PARTICLES[recipe]
    dom = dominant_color(subject)
    # 静止主体框(粒子锚定用)
    rw = subject.width * k
    rh = subject.height * k
    if bottom:
        box = ((size[0] - rw) / 2, size[1] - rh - 8, rw, rh)
    else:
        box = ((size[0] - rw) / 2, (size[1] - rh) / 2, rw, rh)

    frames = []
    for i in range(n):
        t = i / n
        sx, sy, dx, dy, rot = fn(t, size)
        frame = make_frame(subject, size, k, sx, sy, dx, dy, rot, bottom)
        if specs:
            overlay = Image.new("RGBA", size, (0, 0, 0, 0))
            d = ImageDraw.Draw(overlay)
            for spec in specs:
                draw_particle(d, spec, t, box, dom)
            frame = Image.alpha_composite(frame, overlay)
        frames.append(frame)
    return frames

def to_p(frame, colors=255):
    alpha = frame.getchannel("A")
    p = frame.convert("RGB").quantize(colors=colors, method=2)
    mask = alpha.point(lambda a: 255 if a < 128 else 0)
    p.paste(255, mask)
    p.info["transparency"] = 255
    return p

def save_gif(frames_rgba, out, durations, colors):
    ps = [to_p(f, colors) for f in frames_rgba]
    ps[0].save(out, save_all=True, append_images=ps[1:],
               duration=durations, loop=0, transparency=255, disposal=2)

def durations_for(recipe, n, base):
    holds = set(META[recipe][2])
    return [int(base * (1.8 if i in holds else 1.0)) for i in range(n)]

def main():
    ap = argparse.ArgumentParser(description="静态贴纸 → 内容匹配动效 GIF (v2)")
    ap.add_argument("input", nargs="?", help="透明底 PNG 源图(--list 时可省略)")
    ap.add_argument("--recipe", choices=sorted(RECIPES), help="情绪配方(见 references/动效匹配规则.md)")
    ap.add_argument("--anim", choices=sorted(LEGACY), help="v1 兼容动效名(自动映射配方)")
    ap.add_argument("--size", default="240x240", help="输出尺寸,默认 240x240(微信规范)")
    ap.add_argument("--frames", type=int, help="帧数(默认按配方)")
    ap.add_argument("--duration", type=int, help="基础帧时长 ms(默认按配方)")
    ap.add_argument("--scale", type=float, default=0.68, help="主体占画布高度比例,默认 0.68")
    ap.add_argument("--out", help="输出 GIF 路径")
    ap.add_argument("--max-kb", type=int, default=500, help="体积上限 KB,默认 500(微信)")
    ap.add_argument("--list", action="store_true", help="列出全部配方")
    args = ap.parse_args()

    if args.list:
        print("配方 | 帧数 | 基础帧时长 | 粒子")
        for r in RECIPES:
            n, base, _, _ = META[r]
            kinds = ",".join(sorted({s["kind"] for s in PARTICLES[r]})) or "无"
            print(f"{r:11s} | {n:2d} | {base:3d}ms | {kinds}")
        return

    if not args.input or not args.out:
        ap.error("需要 input 与 --out")
    recipe = args.recipe or LEGACY.get(args.anim) or "happy"
    n, base, _, _ = META[recipe]
    n = args.frames or n
    base = args.duration or base
    if n < 4:
        sys.stderr.write("帧数至少 4\n")
        sys.exit(2)
    if not (0 < args.scale <= 1):
        sys.stderr.write("--scale 需在 (0, 1] 区间\n")
        sys.exit(2)

    w, h = (int(x) for x in args.size.lower().split("x"))
    if w <= 0 or h <= 0:
        sys.stderr.write(f"非法尺寸: {args.size}\n")
        sys.exit(2)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)

    subject = load_subject(args.input)
    frames = build_frames(subject, (w, h), recipe, n, args.scale)
    durations = durations_for(recipe, n, base)

    last_kb = None
    for colors in (255, 127, 63):
        save_gif(frames, args.out, durations, colors)
        kb = os.path.getsize(args.out) / 1024
        last_kb = kb
        if kb <= args.max_kb:
            loop_ms = sum(durations)
            print(f"完成: {args.out} | {w}x{h} | {recipe} | {n}帧 | 循环{loop_ms}ms | "
                  f"{colors}色 | {kb:.1f}KB ≤ {args.max_kb}KB PASS")
            return
        if colors == 63 and kb > args.max_kb and n > 8:
            thin = frames[::2]
            save_gif(thin, args.out, [d * 2 for d in durations[::2]], 63)
            kb = os.path.getsize(args.out) / 1024
            last_kb = kb
            if kb <= args.max_kb:
                print(f"完成(已抽帧至 {len(thin)} 帧): {args.out} | {kb:.1f}KB PASS")
                return
    print(f"警告: 仍超限 {last_kb:.1f}KB > {args.max_kb}KB,请减帧(--frames)或缩小主体占比(--scale)")


if __name__ == "__main__":
    main()
