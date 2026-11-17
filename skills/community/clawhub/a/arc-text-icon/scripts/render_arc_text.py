#!/usr/bin/env python3
"""
arc-text-icon skill: render Chinese/CJK text along an upper arc.

Always writes both a transparent-background main file AND a white-background
preview file, and runs a strong-pixel self-check before exit.

Usage:
    python3 render_arc_text.py \
        --text "在此填入要生成的文字" \
        --font-size 78 \
        --half-angle-deg 55 \
        --chord 1500 \
        --font kai \
        --color "#000000" \
        --canvas 1600 700 \
        --out 2026-07-14+v1+文字说明.png \
        --transparent
"""
import argparse
import os
import sys
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as pe
import numpy as np
from PIL import Image


# ---------- Font registry ----------
FONT_PATHS = {
    "kai":  "/usr/share/fonts/truetype/arphic/ukai.ttc",       # 楷体
    "song": "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",  # 宋体
    "hei":  "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",   # 黑体
}


def get_font(name: str) -> FontProperties:
    path = FONT_PATHS.get(name)
    if path is None or not os.path.exists(path):
        raise SystemExit(
            f"[arc-text-icon] font '{name}' not found.\n"
            f"  Available: {list(FONT_PATHS)}\n"
            f"  Install: apt install fonts-arphic-ukai fonts-noto-cjk"
        )
    return FontProperties(fname=path)


# ---------- Geometry ----------
def compute_positions(text, cx, cy, r, half_angle_rad, progress_padding=0.0):
    """
    Place each character on an upper arc.
    progress_padding shrinks both ends (purely cosmetic, does NOT widen inter-char spacing).
    Returns list of (dx, dy, theta_deg, char).
    """
    n = len(text)
    if n < 1:
        raise SystemExit("[arc-text-icon] text is empty")

    positions = []
    for i, ch in enumerate(text):
        raw = (i + 0.5) / n
        progress = progress_padding + raw * (1 - 2 * progress_padding)
        theta = half_angle_rad * (2 * progress - 1)
        dx = cx + r * math.sin(theta)
        dy = cy - r * (1 - math.cos(theta))
        positions.append((dx, dy, -math.degrees(theta), ch))  # rotation = -theta (字头朝外)
    return positions


def check_spacing(positions, font_size):
    """
    Verify char center spacing > ink width + safety margin.
    Returns (min_spacing, ink_width, is_safe).
    """
    n = len(positions)
    if n < 2:
        return (0.0, font_size * 1.05, True)
    dists = []
    for i in range(1, n):
        dx0, dy0, _, _ = positions[i - 1]
        dx1, dy1, _, _ = positions[i]
        d = math.hypot(dx1 - dx0, dy1 - dy0)
        dists.append(d)
    ink_width = font_size * 1.05
    return (min(dists), ink_width, min(dists) > ink_width + 5)


def render(canvas, font_path, font_size, positions, text_color, stroke_color, stroke_width, transparent, bg_color, out_path):
    W, H = canvas
    # 关键：transparent=True 时 facecolor 必须为 'none'，否则会被 matplotlib 双重处理
    # 导致输出为白底纯白图（v1.0.0 假成功 bug）
    if transparent:
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor='none')
    else:
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=bg_color if bg_color else 'white')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect('equal')
    ax.axis('off')
    if not transparent:
        ax.set_facecolor(bg_color if bg_color else 'white')

    for dx, dy, rot, ch in positions:
        text_obj = ax.text(dx, dy, ch, fontproperties=font_path, fontsize=font_size,
                ha='center', va='center', rotation=rot, color=text_color)
        if stroke_color:
            text_obj.set_path_effects([pe.withStroke(linewidth=stroke_width, foreground=stroke_color)])

    # 保存时: transparent=False 时显式设置 facecolor, transparent=True 让 PNG alpha 通道生效
    if transparent:
        fig.savefig(out_path, transparent=True, dpi=100)
    else:
        fig.savefig(out_path, dpi=100, facecolor=bg_color if bg_color else 'white')
    plt.close(fig)


def self_check(path, expect_strong_pixels_min=5000):
    """Return (strong_pixel_count, ok_bool).

    关键修复：必须同时检查 alpha 和 RGB，alpha=255+RGB=255 是 "假成功"陷阱。
    真实有效像素 = alpha>128 且 RGB 至少一个通道 < 200（非白色）。
    """
    im = Image.open(path)
    arr = np.array(im)
    if arr.shape[-1] == 4:
        a = arr[..., -1]
        rgb_max = arr[..., :3].max(axis=-1)  # 取 RGB 三通道中的最大值
        # 真实有效像素：alpha>128 且不是纯白（R/G/B 至少一个 < 200）
        strong = int(((a > 128) & (rgb_max < 200)).sum())
    else:
        # RGB 图：任何不是纯白的像素
        rgb_max = arr[..., :3].max(axis=-1)
        strong = int((rgb_max < 600).sum()) if arr.shape[-1] == 3 else int(rgb_max < 200).sum()
    return strong, strong >= expect_strong_pixels_min


def main():
    p = argparse.ArgumentParser(description="Render upper-arc text icon")
    p.add_argument("--text", required=True)
    p.add_argument("--font-size", type=int, default=78)
    p.add_argument("--half-angle-deg", type=float, default=55)
    p.add_argument("--chord", type=int, default=1500)
    p.add_argument("--font", choices=list(FONT_PATHS), default="kai")
    p.add_argument("--color", default="#000000")
    p.add_argument("--stroke-color", default=None)
    p.add_argument("--stroke-width", type=int, default=2)
    p.add_argument("--canvas", type=int, nargs=2, default=[1600, 700])
    p.add_argument("--bg", default="#FFFFFF")
    p.add_argument("--transparent", action="store_true")
    p.add_argument("--out", required=True, help="Output filename. Convention: YYYY-MM-DD+vN+说明.png (script does not auto-prefix; you provide it)")
    args = p.parse_args()

    W, H = args.canvas
    half_angle = math.radians(args.half_angle_deg)
    r = args.chord / (2 * math.sin(half_angle))
    # y_top = 弧顶在画布的 y 坐标（matplotlib y 向上，画布底=0，顶=H）
    # 弧顶在画布中下部（H/2 到 H*0.85 之间），弦在弧顶上方 h_arc 处
    # dx = cx + r*sin(theta)         # 范围 cx ± r*sin(half_angle)
    # dy = y_top - 0 + r*cos(theta)  # theta=0 时 dy = y_top + r (弧顶? 不不...)
    # 
    # 几何反复调试: dy = y_top + r*cos(theta) - r  =  r*cos(theta) - (r - y_top)
    # 当 theta=0: dy = r - (r - y_top) = y_top  (弧顶位置)
    # 当 theta=±half: dy = r*cos(half) - (r - y_top) = r*cos(half) - r + y_top = y_top - r*(1-cos(half)) = y_top - h_arc (弦高)
    #
    # 所以 v32 公式其实是用 cy = y_top - h_arc 作为参考, + dy = r*(cos-1) 
    # 让我用更直观的公式: 弧顶在画布中的 y = top_y, 弦端点 (y - h_arc)
    # 让 top_y 位于 画布中部偏下
    # 
    # 简化：让弧顶 (top_y) = H * 0.85, 弧底 (弦端) = H * 0.85 - h_arc
    # 要求 弦端 ≥ 30 → top_y - h_arc ≥ 30 → top_y ≥ h_arc + 30
    h_arc = r * (1 - math.cos(half_angle))
    # v32 实际使用的是: cy = 620 (即接近 H), dy = cy - r*(1-cos)
    # 弧顶在 cy 处, 弦在 cy - h_arc
    # 要让弧底 ≥ 50, cy - h_arc ≥ 50 → cy ≥ h_arc + 50
    cy = min(H - 50, int(h_arc + 80))   # y_top = cy
    print(f'[arc-text-icon] 弧半径 r={r:.0f}, 弧高 h_arc={h_arc:.0f}, cy(弧顶)={cy}')
    print(f'[arc-text-icon] 弦端 y = cy - h_arc = {cy - h_arc:.0f} (画布高 H={H})')
    assert cy - h_arc >= 30, f'越界: 弦端 {cy - h_arc:.0f} 太小'
    assert cy <= H - 10, f'越界: cy={cy} ≥ H-10'
    cx = W // 2
    font = get_font(args.font)

    positions = compute_positions(args.text, cx, cy, r, half_angle)

    # Spacing pre-check
    min_dist, ink_w, safe = check_spacing(positions, args.font_size)
    print(f"[arc-text-icon] chars={len(args.text)} font_size={args.font_size} "
          f"half_angle={args.half_angle_deg}° chord={args.chord}")
    print(f"[arc-text-icon] min char-center spacing = {min_dist:.1f}px, "
          f"estimated ink width = {ink_w:.0f}px → {'SAFE' if safe else 'OVERLAP RISK'}")
    if not safe:
        print(f"[arc-text-icon] ⚠️  字中心间距 {min_dist:.1f}px < 字宽 {ink_w:.0f}px + 5px, 可能重叠")
        print(f"[arc-text-icon] 建议: --font-size {int(args.font_size * 0.85)} 或 --chord {int(args.chord * 1.2)}")

    out_path = args.out
    out_dir = os.path.dirname(out_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    # Main output (transparent or colored)
    render((W, H), font, args.font_size, positions,
           args.color, args.stroke_color, args.stroke_width,
           args.transparent, args.bg, out_path)

    strong, ok = self_check(out_path)
    print(f"[arc-text-icon] {out_path}: strong pixels = {strong}, "
          f"{'PASS' if ok else 'FAIL'}")
    if not ok:
        print("[arc-text-icon] ❌ 主稿强像素不足 (<5000), 图可能空白, 请检查几何公式")
        sys.exit(1)

    # White-bg preview
    base, ext = os.path.splitext(out_path)
    preview = f"{base}_预览{ext}"
    render((W, H), font, args.font_size, positions,
           args.color, args.stroke_color, args.stroke_width,
           False, "#FFFFFF", preview)
    p_strong, p_ok = self_check(preview)
    print(f"[arc-text-icon] {preview}: strong pixels = {p_strong}, "
          f"{'PASS' if p_ok else 'FAIL'}")

    print(f"[arc-text-icon] ✅ Done. Main={out_path}, Preview={preview}")


if __name__ == "__main__":
    main()