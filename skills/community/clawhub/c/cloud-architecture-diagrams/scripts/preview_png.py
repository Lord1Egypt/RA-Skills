#!/usr/bin/env python3
"""
Render a .excalidraw file (with embedded SVG icons) to a PNG for a quick visual
check. The inline Excalidraw tool can't display the base64-embedded icons, so
this gives you — and the user — a faithful preview of what the diagram looks
like.

Not a pixel-perfect Excalidraw clone: it draws rectangles, dashed/rounded
borders, text, straight/elbow arrows with arrowheads, numbered badges, and
pastes the icons. That's enough to judge layout, overlaps, and icon choice.

Usage:
    python preview_png.py diagram.excalidraw            # -> diagram.png
    python preview_png.py diagram.excalidraw -o out.png --scale 1.5

Requires: cairosvg, pillow  (pip install cairosvg pillow --break-system-packages)
"""
import argparse
import base64
import io
import json
import math
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont


def load_font(size: int, bold: bool):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def rounded_rect(d, box, r, outline, width, fill, dashed):
    x0, y0, x1, y1 = box
    if fill and fill != "transparent":
        d.rounded_rectangle(box, radius=r, fill=fill)
    if not dashed:
        d.rounded_rectangle(box, radius=r, outline=outline, width=width)
    else:
        # approximate dashed border with segments along the perimeter
        dash, gap = 8, 6
        def seg(x0, y0, x1, y1):
            length = math.hypot(x1 - x0, y1 - y0)
            if length == 0:
                return
            ux, uy = (x1 - x0) / length, (y1 - y0) / length
            pos = 0
            while pos < length:
                a = pos
                b = min(pos + dash, length)
                d.line([x0 + ux * a, y0 + uy * a, x0 + ux * b, y0 + uy * b],
                       fill=outline, width=width)
                pos += dash + gap
        seg(x0 + r, y0, x1 - r, y0)
        seg(x1, y0 + r, x1, y1 - r)
        seg(x1 - r, y1, x0 + r, y1)
        seg(x0, y1 - r, x0, y0 + r)


def arrowhead(d, x, y, ang, color, size=10):
    a1 = ang + math.radians(150)
    a2 = ang - math.radians(150)
    p1 = (x + size * math.cos(a1), y + size * math.sin(a1))
    p2 = (x + size * math.cos(a2), y + size * math.sin(a2))
    d.polygon([(x, y), p1, p2], fill=color)


def render(doc: dict, scale: float) -> Image.Image:
    els = doc["elements"]
    files = doc.get("files", {})
    maxx = max((e["x"] + e.get("width", 0) for e in els), default=1000)
    maxy = max((e["y"] + e.get("height", 0) for e in els), default=700)
    W, H = int((maxx + 40) * scale), int((maxy + 40) * scale)
    img = Image.new("RGBA", (W, H), "white")
    d = ImageDraw.Draw(img)

    def S(v):
        return v * scale

    for e in els:
        t = e["type"]
        if t == "rectangle":
            rounded_rect(
                d, [S(e["x"]), S(e["y"]), S(e["x"] + e["width"]), S(e["y"] + e["height"])],
                r=10 * scale, outline=e.get("strokeColor", "#1e1e1e"),
                width=max(1, int(e.get("strokeWidth", 1) * scale)),
                fill=None if e.get("backgroundColor") == "transparent" else e.get("backgroundColor"),
                dashed=e.get("strokeStyle") == "dashed")
        elif t == "ellipse":
            box = [S(e["x"]), S(e["y"]), S(e["x"] + e["width"]), S(e["y"] + e["height"])]
            d.ellipse(box, fill=e.get("backgroundColor"), outline=e.get("strokeColor"))
        elif t == "image":
            fid = e.get("fileId")
            f = files.get(fid)
            if not f:
                continue
            b64 = f["dataURL"].split(",", 1)[1]
            png = cairosvg.svg2png(bytestring=base64.b64decode(b64),
                                   output_width=int(S(e["width"])),
                                   output_height=int(S(e["height"])))
            icon = Image.open(io.BytesIO(png)).convert("RGBA")
            img.paste(icon, (int(S(e["x"])), int(S(e["y"])), ), icon)
        elif t == "text":
            font = load_font(max(8, int(e.get("fontSize", 16) * scale)),
                             bold=False)
            color = e.get("strokeColor", "#1e1e1e")
            d.text((S(e["x"]), S(e["y"])), e.get("text", ""), fill=color, font=font)
        elif t == "arrow":
            x0, y0 = S(e["x"]), S(e["y"])
            pts = [(x0 + dx * scale, y0 + dy * scale) for dx, dy in e["points"]]
            color = e.get("strokeColor", "#1e1e1e")
            w = max(1, int(e.get("strokeWidth", 2) * scale))
            for i in range(len(pts) - 1):
                d.line([pts[i], pts[i + 1]], fill=color, width=w)
            if e.get("endArrowhead"):
                (px, py), (qx, qy) = pts[-2], pts[-1]
                arrowhead(d, qx, qy, math.atan2(qy - py, qx - px), color, 9 * scale)
            if e.get("startArrowhead"):
                (px, py), (qx, qy) = pts[1], pts[0]
                arrowhead(d, qx, qy, math.atan2(qy - py, qx - px), color, 9 * scale)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("-o", "--out")
    ap.add_argument("--scale", type=float, default=1.5)
    args = ap.parse_args()
    doc = json.loads(Path(args.file).read_text())
    img = render(doc, args.scale)
    out = args.out or str(Path(args.file).with_suffix(".png"))
    img.convert("RGB").save(out)
    print(f"Wrote {out} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
