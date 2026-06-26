#!/usr/bin/env python3
"""genart — Generative art engine. SVG + PNG output, stdlib only."""

import argparse
import math
import os
import random
import subprocess
import sys
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------
# Palettes
# ---------------------------------------------------------------------------

PALETTES = {
    "midnight": ["#0d1b2a", "#1b2838", "#1b3a5c", "#3a6ea5", "#6b9ac4", "#c0d6df", "#ffffff"],
    "fire": ["#1a0a00", "#4a1500", "#8b2500", "#cd3700", "#ee5500", "#ff8c00", "#ffd700", "#fff8dc"],
    "forest": ["#1a2e1a", "#2d4a2d", "#3e6b3e", "#5a8a3c", "#7fb069", "#a4c17a", "#d4e09b", "#f0f4e1"],
    "vapor": ["#0d0221", "#261447", "#6b2fa0", "#ff6ec7", "#ff71ce", "#01cdfe", "#05ffa1", "#b967ff"],
    "mono": ["#000000", "#1a1a1a", "#333333", "#555555", "#888888", "#bbbbbb", "#dddddd", "#ffffff"],
    "berlin": ["#2c2c2c", "#444444", "#666666", "#888888", "#aaaaaa", "#ff0066", "#00ffcc", "#ffcc00"],
    "ocean": ["#03071e", "#023e8a", "#0077b6", "#0096c7", "#00b4d8", "#48cae4", "#90e0ef", "#caf0f8"],
    "sunset": ["#210124", "#52042c", "#8c1843", "#c33c54", "#e36b5b", "#f2a65a", "#eec170", "#f4e8c1"],
}


def get_palette(name, rng):
    if name == "random" or name is None:
        name = rng.choice(list(PALETTES.keys()))
    return PALETTES.get(name, PALETTES["midnight"]), name


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex(r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t)


def sample_palette(palette, t):
    """Sample a color from palette at position t in [0,1]."""
    t = max(0.0, min(1.0, t))
    n = len(palette) - 1
    idx = t * n
    lo = int(idx)
    hi = min(lo + 1, n)
    frac = idx - lo
    return lerp_color(palette[lo], palette[hi], frac)


# ---------------------------------------------------------------------------
# Noise — smooth value noise for flow fields and organic shapes
# ---------------------------------------------------------------------------

class ValueNoise:
    """2D value noise with smooth interpolation."""

    def __init__(self, rng, grid_size=32):
        self.grid_size = grid_size
        self.values = [[rng.random() for _ in range(grid_size + 1)] for _ in range(grid_size + 1)]

    def _smooth(self, t):
        return t * t * (3 - 2 * t)

    def sample(self, x, y):
        gx = (x % 1.0) * self.grid_size
        gy = (y % 1.0) * self.grid_size
        ix, iy = int(gx), int(gy)
        fx, fy = self._smooth(gx - ix), self._smooth(gy - iy)
        ix2 = min(ix + 1, self.grid_size)
        iy2 = min(iy + 1, self.grid_size)
        a = self.values[iy][ix] + (self.values[iy][ix2] - self.values[iy][ix]) * fx
        b = self.values[iy2][ix] + (self.values[iy2][ix2] - self.values[iy2][ix]) * fx
        return a + (b - a) * fy


def fbm(noise, x, y, octaves=4, lacunarity=2.0, gain=0.5):
    """Fractal Brownian Motion — layer noise at multiple scales."""
    val = 0.0
    amp = 1.0
    freq = 1.0
    for _ in range(octaves):
        val += amp * noise.sample(x * freq, y * freq)
        amp *= gain
        freq *= lacunarity
    return val


# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

def svg_header(w, h, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">\n<defs>\n{defs}</defs>\n'
    )


def svg_footer():
    return "</svg>\n"


def svg_rect(x, y, w, h, fill, opacity=1.0, extra=""):
    op = f' opacity="{opacity}"' if opacity < 1.0 else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{op}{extra}/>\n'


def svg_circle(cx, cy, r, fill, opacity=1.0, stroke="none", stroke_width=0):
    op = f' opacity="{opacity}"' if opacity < 1.0 else ""
    st = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke != "none" else ""
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}"{op}{st}/>\n'


def svg_path(d, stroke="none", stroke_width=1, fill="none", opacity=1.0, extra=""):
    op = f' opacity="{opacity}"' if opacity < 1.0 else ""
    return (
        f'<path d="{d}" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'fill="{fill}"{op} stroke-linecap="round" stroke-linejoin="round"{extra}/>\n'
    )


def svg_linear_gradient(gid, x1, y1, x2, y2, stops):
    """stops: list of (offset%, color, opacity)"""
    s = (
        f'<linearGradient id="{gid}" x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%">\n'
    )
    for off, col, op in stops:
        s += f'  <stop offset="{off}%" stop-color="{col}" stop-opacity="{op}"/>\n'
    s += "</linearGradient>\n"
    return s


def svg_radial_gradient(gid, cx, cy, r, stops):
    s = f'<radialGradient id="{gid}" cx="{cx}%" cy="{cy}%" r="{r}%">\n'
    for off, col, op in stops:
        s += f'  <stop offset="{off}%" stop-color="{col}" stop-opacity="{op}"/>\n'
    s += "</radialGradient>\n"
    return s


# ---------------------------------------------------------------------------
# Generator: flow
# ---------------------------------------------------------------------------

def gen_flow(seed, width, height, palette_name):
    rng = random.Random(seed)
    palette, pname = get_palette(palette_name, rng)
    # Low-frequency noise for smooth, coherent flow
    noise1 = ValueNoise(rng, grid_size=8)

    # Use only the two darkest colors for background
    defs = svg_linear_gradient("bggrad", 0, 0, 100, 100, [
        (0, palette[0], 1), (100, palette[min(1, len(palette)-1)], 1)
    ])
    # Build a bright sub-palette from the lighter half of the palette
    mid = max(len(palette) // 2, 2)
    bright_colors = palette[mid:]
    if len(bright_colors) < 2:
        bright_colors = palette[-3:]

    parts = [svg_header(width, height, defs)]
    parts.append(svg_rect(0, 0, width, height, "url(#bggrad)"))

    num_particles = 1200
    steps = 200
    step_len = 2.0

    for i in range(num_particles):
        x = rng.uniform(0, width)
        y = rng.uniform(0, height)
        points = [(x, y)]
        for _ in range(steps):
            nx = x / width
            ny = y / height
            # Low-frequency noise → smooth, sweeping curves
            angle = fbm(noise1, nx * 1.5, ny * 1.5, octaves=2, gain=0.4) * math.pi * 3
            x += math.cos(angle) * step_len
            y += math.sin(angle) * step_len
            if x < -20 or x > width + 20 or y < -20 or y > height + 20:
                break
            points.append((x, y))
        if len(points) < 6:
            continue

        # Use bright colors only
        color = rng.choice(bright_colors)
        opacity = rng.uniform(0.25, 0.7)
        sw = rng.uniform(0.6, 2.0)

        d = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
        for j in range(1, len(points) - 2, 2):
            cx_ = points[j][0]
            cy_ = points[j][1]
            ex = (points[j][0] + points[j+1][0]) / 2
            ey = (points[j][1] + points[j+1][1]) / 2
            d += f" Q {cx_:.1f} {cy_:.1f} {ex:.1f} {ey:.1f}"
        parts.append(svg_path(d, stroke=color, stroke_width=sw, opacity=opacity))

    parts.append(svg_footer())
    return "".join(parts)


# ---------------------------------------------------------------------------
# Generator: fractal
# ---------------------------------------------------------------------------

def gen_fractal(seed, width, height, ftype):
    rng = random.Random(seed)

    if ftype == "tree":
        return _fractal_tree(rng, width, height)
    elif ftype == "sierpinski":
        return _fractal_sierpinski(rng, width, height)
    else:
        return _fractal_escape(rng, width, height, ftype)


def _fractal_escape(rng, width, height, ftype):
    """Mandelbrot or Julia set rendered as SVG rectangles with smooth coloring."""
    palette = PALETTES["ocean"]
    cell = 4  # pixel block size for SVG performance
    cols = width // cell
    rows = height // cell
    max_iter = 80

    if ftype == "julia":
        # Pick a nice Julia constant
        presets = [(-0.7, 0.27015), (-0.4, 0.6), (0.285, 0.01), (-0.8, 0.156)]
        cr, ci = rng.choice(presets)
        x_min, x_max = -1.8, 1.8
        y_min, y_max = -1.8, 1.8
    else:
        cr, ci = 0, 0  # unused for mandelbrot
        x_min, x_max = -2.5, 1.0
        y_min, y_max = -1.2, 1.2

    bg = palette[0]
    parts = [svg_header(width, height)]
    parts.append(svg_rect(0, 0, width, height, bg))

    for row in range(rows):
        for col in range(cols):
            px = x_min + (col / cols) * (x_max - x_min)
            py = y_min + (row / rows) * (y_max - y_min)

            if ftype == "julia":
                zr, zi = px, py
            else:
                zr, zi = 0.0, 0.0
                cr, ci = px, py

            it = 0
            for it in range(max_iter):
                zr2, zi2 = zr * zr, zi * zi
                if zr2 + zi2 > 4.0:
                    break
                zi = 2 * zr * zi + ci
                zr = zr2 - zi2 + cr

            if it < max_iter - 1 and it > 0:
                # Smooth iteration count
                log_zn = math.log(zr * zr + zi * zi) / 2
                nu = math.log(log_zn / math.log(2)) / math.log(2)
                smooth_it = it + 1 - nu
                t = smooth_it / max_iter
                color = sample_palette(palette, t)
                parts.append(
                    f'<rect x="{col*cell}" y="{row*cell}" '
                    f'width="{cell}" height="{cell}" fill="{color}"/>\n'
                )

    parts.append(svg_footer())
    return "".join(parts)


def _fractal_tree(rng, width, height):
    palette = PALETTES["forest"]
    defs = svg_linear_gradient("sky", 0, 0, 0, 100, [
        (0, "#1a1a2e", 1), (70, "#16213e", 1), (100, "#0f3460", 1)
    ])
    parts = [svg_header(width, height, defs)]
    parts.append(svg_rect(0, 0, width, height, "url(#sky)"))

    branches = []

    def tree(x, y, angle, length, depth, thickness):
        if depth == 0 or length < 2:
            return
        ex = x + math.cos(math.radians(angle)) * length
        ey = y + math.sin(math.radians(angle)) * length
        t = 1.0 - depth / 12.0
        color = sample_palette(palette, t * 0.7 + 0.15)
        opacity = 0.6 + 0.4 * (depth / 12.0)
        branches.append((x, y, ex, ey, color, thickness, opacity))
        spread = rng.uniform(18, 35)
        shrink = rng.uniform(0.65, 0.78)
        tree(ex, ey, angle - spread, length * shrink, depth - 1, max(0.5, thickness * 0.7))
        tree(ex, ey, angle + spread, length * shrink, depth - 1, max(0.5, thickness * 0.7))
        if depth > 5 and rng.random() < 0.3:
            tree(ex, ey, angle + rng.uniform(-10, 10), length * shrink * 0.9, depth - 1, max(0.5, thickness * 0.6))

    tree(width / 2, height * 0.88, -90, height * 0.22, 11, 8)

    for x1, y1, x2, y2, col, sw, op in branches:
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{col}" stroke-width="{sw:.1f}" opacity="{op:.2f}" '
            f'stroke-linecap="round"/>\n'
        )

    parts.append(svg_footer())
    return "".join(parts)


def _fractal_sierpinski(rng, width, height):
    palette = PALETTES["vapor"]
    defs = svg_linear_gradient("bg", 0, 0, 0, 100, [
        (0, palette[0], 1), (100, palette[1], 1)
    ])
    parts = [svg_header(width, height, defs)]
    parts.append(svg_rect(0, 0, width, height, "url(#bg)"))

    margin = 40
    # Equilateral triangle
    top = (width / 2, margin)
    bl = (margin, height - margin)
    br = (width - margin, height - margin)

    def sierpinski(ax, ay, bx, by, cx, cy, depth):
        if depth == 0:
            t = rng.uniform(0.3, 0.95)
            color = sample_palette(palette, t)
            op = 0.6 + 0.35 * rng.random()
            parts.append(
                f'<polygon points="{ax:.1f},{ay:.1f} {bx:.1f},{by:.1f} {cx:.1f},{cy:.1f}" '
                f'fill="{color}" opacity="{op:.2f}" stroke="{palette[-2]}" stroke-width="0.5"/>\n'
            )
            return
        mx_ab = (ax + bx) / 2
        my_ab = (ay + by) / 2
        mx_bc = (bx + cx) / 2
        my_bc = (by + cy) / 2
        mx_ca = (cx + ax) / 2
        my_ca = (cy + ay) / 2
        sierpinski(ax, ay, mx_ab, my_ab, mx_ca, my_ca, depth - 1)
        sierpinski(mx_ab, my_ab, bx, by, mx_bc, my_bc, depth - 1)
        sierpinski(mx_ca, my_ca, mx_bc, my_bc, cx, cy, depth - 1)

    sierpinski(top[0], top[1], bl[0], bl[1], br[0], br[1], 6)

    parts.append(svg_footer())
    return "".join(parts)


# ---------------------------------------------------------------------------
# Generator: cellular
# ---------------------------------------------------------------------------

def gen_cellular(seed, width, height, rule, steps):
    rng = random.Random(seed)
    palette = PALETTES["mono"]

    cols = width // 3
    if steps is None:
        steps = height // 3

    defs = ""
    parts = [svg_header(width, height, defs)]
    parts.append(svg_rect(0, 0, width, height, palette[-1]))

    # 1D elementary cellular automaton
    rule_bin = format(rule, "08b")
    rule_map = {}
    for i in range(8):
        triple = format(7 - i, "03b")
        rule_map[triple] = rule_bin[i]

    row = ["0"] * cols
    row[cols // 2] = "1"
    # Also seed a few random cells for visual interest
    for _ in range(cols // 20):
        row[rng.randint(0, cols - 1)] = "1"

    cell_w = width / cols
    cell_h = height / steps

    accent_colors = ["#ff0066", "#00ffcc", "#3366ff"]

    for step in range(steps):
        for c in range(cols):
            if row[c] == "1":
                # Color varies subtly by position
                t = step / max(steps - 1, 1)
                shade = sample_palette(palette, 0.0 + t * 0.4)
                parts.append(
                    f'<rect x="{c * cell_w:.2f}" y="{step * cell_h:.2f}" '
                    f'width="{cell_w + 0.5:.2f}" height="{cell_h + 0.5:.2f}" fill="{shade}"/>\n'
                )
        # Evolve
        new_row = ["0"] * cols
        for c in range(cols):
            left = row[(c - 1) % cols]
            center = row[c]
            right = row[(c + 1) % cols]
            new_row[c] = rule_map.get(left + center + right, "0")
        row = new_row

    parts.append(svg_footer())
    return "".join(parts)


# ---------------------------------------------------------------------------
# Generator: circles (circle packing)
# ---------------------------------------------------------------------------

def gen_circles(seed, width, height, count, palette_name):
    rng = random.Random(seed)
    palette, pname = get_palette(palette_name, rng)

    defs = svg_radial_gradient("bgr", 50, 50, 60, [
        (0, palette[1], 1), (100, palette[0], 1)
    ])
    parts = [svg_header(width, height, defs)]
    parts.append(svg_rect(0, 0, width, height, "url(#bgr)"))

    circles = []
    max_attempts = count * 150
    min_r = 4
    max_r = min(width, height) * 0.18

    for _ in range(max_attempts):
        if len(circles) >= count:
            break
        cx = rng.uniform(0, width)
        cy = rng.uniform(0, height)

        # Find max radius that doesn't overlap
        max_allowed = max_r
        for ox, oy, or_ in circles:
            dist = math.hypot(cx - ox, cy - oy)
            space = dist - or_ - 2  # 2px gap
            if space < min_r:
                max_allowed = -1
                break
            max_allowed = min(max_allowed, space)

        # Don't go outside canvas
        max_allowed = min(max_allowed, cx, cy, width - cx, height - cy)

        if max_allowed < min_r:
            continue

        r = rng.uniform(min_r, max_allowed)
        circles.append((cx, cy, r))

    # Sort large to small for drawing order (large first, small on top)
    circles.sort(key=lambda c: -c[2])

    # Generate per-circle gradient defs
    grad_defs = ""
    for i, (cx, cy, r) in enumerate(circles):
        t = r / max_r
        base_color = sample_palette(palette, rng.uniform(0.15, 0.95))
        highlight = lerp_color(base_color, "#ffffff", 0.4)
        grad_defs += svg_radial_gradient(f"cg{i}", 35, 35, 65, [
            (0, highlight, 0.9), (100, base_color, 1.0)
        ])

    # Re-create header with gradients
    all_defs = defs + grad_defs
    parts = [svg_header(width, height, all_defs)]
    parts.append(svg_rect(0, 0, width, height, "url(#bgr)"))

    for i, (cx, cy, r) in enumerate(circles):
        op = 0.75 + 0.25 * (r / max_r)
        parts.append(svg_circle(cx, cy, r, f"url(#cg{i})", opacity=op))

    parts.append(svg_footer())
    return "".join(parts)


# ---------------------------------------------------------------------------
# Generator: waves
# ---------------------------------------------------------------------------

def gen_waves(seed, width, height, layers, palette_name):
    rng = random.Random(seed)
    palette, pname = get_palette(palette_name, rng)

    # Background sky gradient
    defs = svg_linear_gradient("sky", 0, 0, 0, 100, [
        (0, palette[0], 1), (50, palette[1], 1), (100, palette[2] if len(palette) > 2 else palette[1], 1)
    ])

    # Layer gradients
    for i in range(layers):
        t = (i + 1) / (layers + 1)
        c1 = sample_palette(palette, t)
        c2 = sample_palette(palette, t + 0.12)
        defs += svg_linear_gradient(f"wg{i}", 0, 0, 0, 100, [
            (0, c1, 0.95), (100, c2, 0.85)
        ])

    parts = [svg_header(width, height, defs)]
    parts.append(svg_rect(0, 0, width, height, "url(#sky)"))

    # Optional: subtle sun/moon circle
    sun_y = height * 0.25
    sun_x = width * rng.uniform(0.3, 0.7)
    sun_r = min(width, height) * 0.08
    sun_color = sample_palette(palette, 0.85)
    defs_sun = svg_radial_gradient("sun", 50, 50, 50, [
        (0, "#ffffff", 0.9), (60, sun_color, 0.5), (100, sun_color, 0.0)
    ])
    # Inject sun into parts (after bg)
    parts.append(f'<defs>{defs_sun}</defs>\n')
    parts.append(svg_circle(sun_x, sun_y, sun_r * 2.5, "url(#sun)"))

    for i in range(layers):
        base_y = height * (0.35 + 0.6 * i / layers)
        freq1 = rng.uniform(0.004, 0.012)
        freq2 = rng.uniform(0.008, 0.02)
        amp1 = rng.uniform(15, 50)
        amp2 = rng.uniform(8, 25)
        phase1 = rng.uniform(0, math.pi * 2)
        phase2 = rng.uniform(0, math.pi * 2)

        points = []
        for x in range(0, width + 4, 3):
            y = base_y
            y += math.sin(x * freq1 + phase1) * amp1
            y += math.sin(x * freq2 + phase2) * amp2
            y += math.sin(x * 0.025 + phase1 * 2) * amp1 * 0.3
            points.append((x, y))

        d = f"M 0 {height}"
        for px, py in points:
            d += f" L {px:.1f} {py:.1f}"
        d += f" L {width} {height} Z"

        parts.append(svg_path(d, fill=f"url(#wg{i})", opacity=0.85))

    parts.append(svg_footer())
    return "".join(parts)


# ---------------------------------------------------------------------------
# Generator: grid
# ---------------------------------------------------------------------------

def gen_grid(seed, width, height, cols, rows, palette_name):
    rng = random.Random(seed)
    palette, pname = get_palette(palette_name, rng)

    defs = ""
    parts = [svg_header(width, height, defs)]
    parts.append(svg_rect(0, 0, width, height, palette[0]))

    cw = width / cols
    ch = height / rows
    margin = min(cw, ch) * 0.12

    def draw_circle_element(cx, cy, sz, color, op):
        return svg_circle(cx, cy, sz * 0.4, color, opacity=op)

    def draw_square_element(cx, cy, sz, color, op):
        s = sz * 0.7
        angle = rng.uniform(0, 45)
        return (
            f'<rect x="{cx - s/2:.1f}" y="{cy - s/2:.1f}" width="{s:.1f}" height="{s:.1f}" '
            f'fill="{color}" opacity="{op:.2f}" '
            f'transform="rotate({angle:.1f} {cx:.1f} {cy:.1f})"/>\n'
        )

    def draw_triangle_element(cx, cy, sz, color, op):
        s = sz * 0.4
        angle = rng.uniform(0, 360)
        pts = []
        for k in range(3):
            a = math.radians(angle + k * 120)
            pts.append(f"{cx + math.cos(a)*s:.1f},{cy + math.sin(a)*s:.1f}")
        return (
            f'<polygon points="{" ".join(pts)}" fill="{color}" opacity="{op:.2f}"/>\n'
        )

    def draw_line_element(cx, cy, sz, color, op):
        angle = rng.uniform(0, 180)
        s = sz * 0.4
        x1 = cx + math.cos(math.radians(angle)) * s
        y1 = cy + math.sin(math.radians(angle)) * s
        x2 = cx - math.cos(math.radians(angle)) * s
        y2 = cy - math.sin(math.radians(angle)) * s
        return (
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{max(1, sz*0.06):.1f}" opacity="{op:.2f}" '
            f'stroke-linecap="round"/>\n'
        )

    def draw_arc_element(cx, cy, sz, color, op):
        r = sz * 0.35
        a1 = rng.uniform(0, 360)
        sweep = rng.uniform(90, 270)
        a2 = a1 + sweep
        x1 = cx + math.cos(math.radians(a1)) * r
        y1 = cy + math.sin(math.radians(a1)) * r
        x2 = cx + math.cos(math.radians(a2)) * r
        y2 = cy + math.sin(math.radians(a2)) * r
        large = 1 if sweep > 180 else 0
        return (
            f'<path d="M {x1:.1f} {y1:.1f} A {r:.1f} {r:.1f} 0 {large} 1 {x2:.1f} {y2:.1f}" '
            f'stroke="{color}" stroke-width="{max(1, sz*0.06):.1f}" fill="none" '
            f'opacity="{op:.2f}" stroke-linecap="round"/>\n'
        )

    def draw_concentric(cx, cy, sz, color, op):
        result = ""
        for k in range(3, 0, -1):
            r = sz * 0.12 * k
            c = lerp_color(color, palette[0], (3 - k) * 0.25)
            result += svg_circle(cx, cy, r, "none", opacity=op,
                                 stroke=c, stroke_width=max(0.8, sz * 0.03))
        return result

    drawers = [draw_circle_element, draw_square_element, draw_triangle_element,
               draw_line_element, draw_arc_element, draw_concentric]

    for row in range(rows):
        for col in range(cols):
            cx = col * cw + cw / 2
            cy = row * ch + ch / 2
            sz = min(cw, ch) - margin * 2
            t = rng.uniform(0.2, 0.95)
            color = sample_palette(palette, t)
            op = rng.uniform(0.5, 0.95)
            draw = rng.choice(drawers)
            parts.append(draw(cx, cy, sz, color, op))

    parts.append(svg_footer())
    return "".join(parts)


# ---------------------------------------------------------------------------
# Generator: glitch
# ---------------------------------------------------------------------------

def gen_glitch(seed, input_file, output_base):
    rng = random.Random(seed)

    if input_file and os.path.exists(input_file):
        with open(input_file, "r") as f:
            svg_text = f.read()
    else:
        svg_text = gen_grid(seed + 1000, 800, 800, 8, 8, "vapor")

    # Parse as XML for safe manipulation
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ns = {"svg": "http://www.w3.org/2000/svg"}
    root = ET.fromstring(svg_text)

    vb = root.get("viewBox", "0 0 800 800")
    vb_parts = vb.split()
    canvas_w = float(vb_parts[2]) if len(vb_parts) >= 3 else 800
    canvas_h = float(vb_parts[3]) if len(vb_parts) >= 4 else 800

    def glitch_element(elem):
        # Color shift
        for attr in ("fill", "stroke"):
            color = elem.get(attr, "")
            if color.startswith("#") and len(color) == 7 and rng.random() < 0.35:
                r, g, b = hex_to_rgb(color)
                shift = rng.randint(-80, 80)
                ch = rng.randint(0, 2)
                if ch == 0: r = max(0, min(255, r + shift))
                elif ch == 1: g = max(0, min(255, g + shift))
                else: b = max(0, min(255, b + shift))
                elem.set(attr, rgb_to_hex(r, g, b))

        # Position displacement
        if rng.random() < 0.18:
            for attr in ("x", "y", "cx", "cy"):
                val = elem.get(attr)
                if val:
                    try:
                        elem.set(attr, f"{float(val) + rng.uniform(-20, 20):.1f}")
                    except ValueError:
                        pass

    # Walk all elements
    for elem in root.iter():
        glitch_element(elem)

    # Add scanline overlay
    for yy in range(0, int(canvas_h), 4):
        if rng.random() < 0.4:
            sl = ET.SubElement(root, "rect")
            sl.set("x", "0")
            sl.set("y", str(yy))
            sl.set("width", str(int(canvas_w)))
            sl.set("height", "1")
            sl.set("fill", "#000000")
            sl.set("opacity", f"{rng.uniform(0.03, 0.12):.2f}")

    return ET.tostring(root, encoding="unicode")


# ---------------------------------------------------------------------------
# Output / PNG conversion
# ---------------------------------------------------------------------------

def write_output(svg_content, output_path):
    """Write SVG and attempt PNG conversion. Returns list of created files."""
    svg_path_out = output_path if output_path.endswith(".svg") else output_path + ".svg"
    png_path = svg_path_out.rsplit(".", 1)[0] + ".png"

    with open(svg_path_out, "w") as f:
        f.write(svg_content)

    files = [svg_path_out]

    # Try rsvg-convert
    rsvg = "/usr/bin/rsvg-convert"
    if os.path.exists(rsvg):
        try:
            subprocess.run([rsvg, svg_path_out, "-o", png_path],
                           check=True, capture_output=True, timeout=30)
            files.append(png_path)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            pass

    return files


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_size(s):
    parts = s.lower().split("x")
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    return 800, 800


def main():
    parser = argparse.ArgumentParser(prog="genart", description="Generative art engine")
    sub = parser.add_subparsers(dest="command")

    # flow
    p = sub.add_parser("flow", help="Flow field art")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--size", default="800x800")
    p.add_argument("--palette", default=None)
    p.add_argument("-o", "--output", default=None)

    # fractal
    p = sub.add_parser("fractal", help="Fractal art")
    p.add_argument("--type", dest="ftype", choices=["mandelbrot", "julia", "sierpinski", "tree"],
                   default="mandelbrot")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--size", default="800x800")
    p.add_argument("-o", "--output", default=None)

    # cellular
    p = sub.add_parser("cellular", help="Cellular automata")
    p.add_argument("--rule", type=int, default=30)
    p.add_argument("--steps", type=int, default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--size", default="800x800")
    p.add_argument("-o", "--output", default=None)

    # circles
    p = sub.add_parser("circles", help="Circle packing")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--count", type=int, default=50)
    p.add_argument("--size", default="800x800")
    p.add_argument("--palette", default=None)
    p.add_argument("-o", "--output", default=None)

    # waves
    p = sub.add_parser("waves", help="Layered wave art")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--layers", type=int, default=5)
    p.add_argument("--size", default="800x800")
    p.add_argument("--palette", default=None)
    p.add_argument("-o", "--output", default=None)

    # grid
    p = sub.add_parser("grid", help="Grid pattern art")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--cols", type=int, default=10)
    p.add_argument("--rows", type=int, default=10)
    p.add_argument("--size", default="800x800")
    p.add_argument("--palette", default=None)
    p.add_argument("-o", "--output", default=None)

    # glitch
    p = sub.add_parser("glitch", help="Glitch art")
    p.add_argument("--input", dest="input_file", default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("-o", "--output", default=None)

    # random
    p = sub.add_parser("random", help="Random style")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--size", default="800x800")
    p.add_argument("-o", "--output", default=None)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    seed = args.seed if args.seed is not None else random.randint(1, 999999)
    size = parse_size(getattr(args, "size", "800x800"))
    width, height = size

    output = getattr(args, "output", None)
    if output is None:
        output = f"/tmp/genart-{args.command}-{seed}.svg"

    if args.command == "flow":
        svg = gen_flow(seed, width, height, args.palette)
    elif args.command == "fractal":
        svg = gen_fractal(seed, width, height, args.ftype)
    elif args.command == "cellular":
        svg = gen_cellular(seed, width, height, args.rule, args.steps)
    elif args.command == "circles":
        svg = gen_circles(seed, width, height, args.count, args.palette)
    elif args.command == "waves":
        svg = gen_waves(seed, width, height, args.layers, args.palette)
    elif args.command == "grid":
        svg = gen_grid(seed, width, height, args.cols, args.rows, args.palette)
    elif args.command == "glitch":
        svg = gen_glitch(seed, getattr(args, "input_file", None), output)
    elif args.command == "random":
        rng = random.Random(seed)
        style = rng.choice(["flow", "fractal", "circles", "waves", "grid"])
        palette_name = rng.choice(list(PALETTES.keys()))
        if style == "flow":
            svg = gen_flow(seed, width, height, palette_name)
        elif style == "fractal":
            ftype = rng.choice(["mandelbrot", "julia", "sierpinski", "tree"])
            svg = gen_fractal(seed, width, height, ftype)
        elif style == "circles":
            svg = gen_circles(seed, width, height, 50, palette_name)
        elif style == "waves":
            svg = gen_waves(seed, width, height, 5, palette_name)
        elif style == "grid":
            svg = gen_grid(seed, width, height, 10, 10, palette_name)
        output = f"/tmp/genart-random-{seed}.svg"
    else:
        parser.print_help()
        sys.exit(1)

    files = write_output(svg, output)
    for f in files:
        print(f)


if __name__ == "__main__":
    main()
