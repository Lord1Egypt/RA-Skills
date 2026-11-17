#!/usr/bin/env python3
"""
# © 2026 Vortex Group. Alle rettigheder forbeholdt.
🎬 CC Animator — Tegnefilm generator
======================================
CC kan selv lave animationer! Ingen eksterne sider.
Bruger Cairo til at tegne scener + ffmpeg til video.

Kør: python3 cc_animator.py --scene 9
     python3 cc_animator.py --scene 9 --preview
"""

import sys, os, json, math, time, subprocess, tempfile
from pathlib import Path
import cairocffi as cairo
import numpy as np
from PIL import Image

WORKSPACE = Path.home() / ".openclaw" / "workspace"
OUTPUT_DIR = WORKSPACE / "projects" / "factsage" / "output"
FRAMES_DIR = Path("/tmp") / "cc_frames"
TEMPLATE_DIR = WORKSPACE / "projects" / "factsage" / "animation" / "manim_templates"

FRAMES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

W, H = 1080, 1920  # Vertical video (TikTok/Shorts)
FPS = 30

# ─── FARVER ────────────────────────────────────────────────
GOLD = (0.85, 0.65, 0.15)
DARK_GOLD = (0.6, 0.45, 0.1)
PARCHMENT = (0.95, 0.88, 0.75)
DEEP_BLUE = (0.05, 0.1, 0.25)
DARK_BG = (0.08, 0.05, 0.12)
WARM_WHITE = (0.95, 0.93, 0.88)
CRIMSON = (0.75, 0.1, 0.1)
GREEN = (0.1, 0.4, 0.15)

def create_surface():
    """Opret en ny frame at tegne på — RGB24 (ingen alpha)."""
    return cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)

def save_frame(surface, frame_num):
    """Gem frame som PNG."""
    path = FRAMES_DIR / f"frame_{frame_num:05d}.png"
    surface.write_to_png(str(path))
    return path

def draw_islamic_background(ctx):
    """Tegn islamisk geometrisk baggrund."""
    # Gradient baggrund
    for y in range(0, H, 2):
        t = y / H
        r = 0.05 * (1 - t) + 0.12 * t
        g = 0.08 * (1 - t) + 0.08 * t
        b = 0.15 * (1 - t) + 0.2 * t
        ctx.set_source_rgb(r, g, b)
        ctx.rectangle(0, y, W, 2)
        ctx.fill()
    
    # Islamisk stjerne mønster (gentaget)
    ctx.set_source_rgba(0.85, 0.65, 0.15, 0.08)
    for cx in range(0, W + 100, 200):
        for cy in range(0, H + 100, 200):
            draw_eight_pointed_star(ctx, cx, cy, 40)

def draw_eight_pointed_star(ctx, cx, cy, size):
    """Tegn 8-takkede islamisk stjerne."""
    ctx.save()
    ctx.translate(cx, cy)
    for i in range(8):
        ctx.rotate(math.pi / 4)
        ctx.move_to(0, -size)
        ctx.line_to(size * 0.2, -size * 0.3)
        ctx.line_to(0, 0)
        ctx.line_to(-size * 0.2, -size * 0.3)
        ctx.close_path()
    ctx.fill()
    ctx.restore()

def draw_arched_window(ctx, x, y, width, height):
    """Tegn en islamisk bue-vindue."""
    ctx.save()
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(3)
    
    # Bue
    arc_x = x + width / 2
    arc_radius = width / 2
    ctx.arc(arc_x, y + height - arc_radius, arc_radius, math.pi, 0)
    ctx.stroke()
    
    # Søjler
    ctx.move_to(x, y + height)
    ctx.line_to(x, y + height - arc_radius)
    ctx.stroke()
    ctx.move_to(x + width, y + height)
    ctx.line_to(x + width, y + height - arc_radius)
    ctx.stroke()
    ctx.restore()

def draw_mosque_scene(ctx, progress=0):
    """Tegn moské/scene med animation."""
    ctx.save()
    
    # Måne
    moon_y = 100 + progress * 20
    ctx.set_source_rgb(*GOLD)
    ctx.arc(W - 150, moon_y, 40, 0, 2 * math.pi)
    ctx.fill()
    ctx.set_source_rgb(*DARK_BG)
    ctx.arc(W - 140, moon_y - 10, 35, 0, 2 * math.pi)
    ctx.fill()
    
    # Kuppel
    dome_center_x = W / 2
    dome_center_y = H * 0.55
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(2)
    
    # Hovedkuppel
    ctx.arc(dome_center_x, dome_center_y, 200, math.pi, 2 * math.pi)
    ctx.set_source_rgba(0.85, 0.65, 0.15, 0.3)
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.stroke()
    
    # Minareter (animerede)
    sway = math.sin(progress * 2) * 5
    for i, x_pos in enumerate([dome_center_x - 300 + sway, dome_center_x + 300 - sway]):
        minaret_height = 350
        ctx.save()
        ctx.set_source_rgb(*GOLD)
        ctx.set_line_width(4)
        ctx.move_to(x_pos, dome_center_y)
        ctx.line_to(x_pos, dome_center_y - minaret_height)
        ctx.stroke()
        # Spids
        ctx.move_to(x_pos - 15, dome_center_y - minaret_height)
        ctx.line_to(x_pos, dome_center_y - minaret_height - 30)
        ctx.line_to(x_pos + 15, dome_center_y - minaret_height)
        ctx.stroke()
        ctx.restore()
    
    # Arkader (række af buer)
    for i in range(8):
        wx = 100 + i * 120
        wy = dome_center_y + 50
        draw_arched_window(ctx, wx, wy, 80, 150)
    
    ctx.restore()

def draw_text_cairo(ctx, text, x, y, size=40, color=WARM_WHITE, center=True):
    """Tegn tekst med Cairo (ingen font loading nødvendig)."""
    ctx.save()
    ctx.set_source_rgb(*color)
    ctx.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    
    if center:
        x_bearing, y_bearing, width, height = ctx.text_extents(text)[:4]
        x -= width / 2
    
    ctx.move_to(x, y)
    ctx.show_text(text)
    ctx.restore()

def draw_golden_frame(ctx):
    """Tegn guld-ramme omkring videoen."""
    ctx.save()
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(6)
    ctx.rectangle(10, 10, W - 20, H - 20)
    ctx.stroke()
    
    # Hjørne ornamenter
    for cx, cy in [(15, 15), (W - 15, 15), (15, H - 15), (W - 15, H - 15)]:
        ctx.set_source_rgb(*GOLD)
        ctx.arc(cx, cy, 10, 0, 2 * math.pi)
        ctx.fill()
    ctx.restore()

global_frame_counter = [0]  # mutable counter til at holde styr på tværs af scenes

def animate_scene_draw(scene_name, num_frames, draw_func, voiceover_duration=0):
    """Generer en animeret scene."""
    print(f"  🎨 Tegner {scene_name}...")
    
    for f in range(num_frames):
        progress = f / num_frames
        surface = create_surface()
        ctx = cairo.Context(surface)
        
        # Baggrund
        draw_islamic_background(ctx)
        
        # Scene-specifik tegning
        draw_func(ctx, progress)
        
        # Guld-ramme
        draw_golden_frame(ctx)
        
        # Titel
        draw_text_cairo(ctx, scene_name, W // 2, H - 100, 30, GOLD)
        
        save_frame(surface, global_frame_counter[0])
        global_frame_counter[0] += 1
    
    print(f"    ✅ {num_frames} frames genereret")

def render_video(output_name, fps=FPS):
    """Saml frames til video med ffmpeg."""
    print(f"  🎞 Renderer video...")
    
    video_path = OUTPUT_DIR / f"{output_name}.mp4"
    frames_pattern = str(FRAMES_DIR / "frame_%05d.png")
    
    # Video med ffmpeg (RGB24 = ingen alpha)
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", frames_pattern,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "23",
        "-vf", "format=yuv420p",
        str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"    ❌ ffmpeg fejl: {result.stderr[-200:]}")
    else:
        print(f"    ✅ Video: {video_path}")
        print(f"    📁 Størrelse: {video_path.stat().st_size / 1024 / 1024:.1f}MB")
    return video_path

def clean_frames():
    """Ryd midlertidige frames."""
    for f in FRAMES_DIR.glob("*.png"):
        f.unlink()

# ─── SCENES ────────────────────────────────────────────────

def scene_house_of_wisdom(ctx, progress):
    """House of Wisdom scene — bibliotek i Baghdad."""
    # Bogreoler
    for i in range(12):
        sx = 50 + i * 85
        sy = 400 + math.sin(i + progress * 3) * 20
        ctx.set_source_rgb(*GOLD if i % 2 == 0 else DARK_GOLD)
        ctx.rectangle(sx, sy, 60, 300)
        ctx.set_source_rgba(0.85, 0.65, 0.15, 0.15)
        ctx.fill()
        ctx.set_source_rgb(*GOLD)
        ctx.set_line_width(1)
        ctx.stroke()
    
    # Bøger på hylderne
    for i in range(8):
        bx = 65 + i * 85
        by = 420 + math.sin(i * 2 + progress * 2) * 15
        ctx.set_source_rgb(*CRIMSON if i % 3 == 0 else DEEP_BLUE if i % 3 == 1 else GREEN)
        ctx.rectangle(bx + 5, by - 40, 20, 35)
        ctx.fill()

def scene_baghdad_morning(ctx, progress):
    """Baghdad morgen — solopgang over byen."""
    # Sol (stiger op)
    sun_y = 800 - progress * 400
    ctx.set_source_rgb(1, 0.7, 0.1)
    ctx.arc(W // 2, sun_y, 60 + math.sin(progress * 10) * 5, 0, 2 * math.pi)
    ctx.fill()
    
    # Solstråler
    ctx.set_source_rgba(1, 0.7, 0.1, 0.15)
    for i in range(12):
        angle = i * math.pi / 6 + progress
        ctx.move_to(W // 2, sun_y)
        ctx.line_to(W // 2 + math.cos(angle) * 300, sun_y + math.sin(angle) * 300)
        ctx.set_line_width(3)
        ctx.stroke()
    
    # Skyline (bygninger)
    for i in range(10):
        bx = i * 120 - 60
        bh = 200 + 100 * math.sin(i * 1.5)
        ctx.set_source_rgb(*DARK_GOLD)
        ctx.rectangle(bx, 900 - bh, 90, bh)
        ctx.fill()

def scene_scholar_reading(ctx, progress):
    """En lærd der læser ved lys."""
    # Bord
    ctx.set_source_rgb(*GOLD)
    ctx.rectangle(300, 800, 500, 20)
    ctx.fill()
    
    # Åben bog på bordet
    book_width = 200 + math.sin(progress * 3) * 10
    ctx.set_source_rgb(*PARCHMENT)
    ctx.rectangle(W // 2 - book_width / 2, 720, book_width, 80)
    ctx.fill()
    
    # Lys fra stearinlys (flimrer)
    flicker = 0.9 + math.sin(progress * 15) * 0.1
    ctx.set_source_rgba(1, 0.8, 0.3, 0.15 * flicker)
    ctx.arc(W // 2, 650, 150 * flicker, 0, 2 * math.pi)
    ctx.fill()

def scene_timeline(ctx, progress):
    """Tidslinje med årstal."""
    # Linje
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(4)
    ctx.move_to(100, 1100)
    ctx.line_to(100 + progress * 900, 1100)
    ctx.stroke()
    
    # Årstal
    years = [(0, "700 CE"), (0.2, "750 CE"), (0.4, "800 CE"), (0.6, "830 CE"), (0.8, "1000 CE"), (1.0, "1258 CE")]
    for pos, label in years:
        if pos <= progress:
            x = 100 + pos * 900
            draw_text_cairo(ctx, label, x, 1140, 25, GOLD)

# ─── MAIN ─────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🎬 CC Animator")
    parser.add_argument("--scene", type=int, default=9, help="Script nummer (1-9)")
    parser.add_argument("--preview", action="store_true", help="Kun 10 frames til test")
    parser.add_argument("--fps", type=int, default=FPS, help="Frames per sekund")
    args = parser.parse_args()
    
    scene_num = args.scene
    fps = args.fps
    
    clean_frames()
    
    total_frames = 60 if args.preview else fps * 12  # 12 sekunder
    
    print(f"\n🎬 CC ANIMATOR — Scene #{scene_num}")
    print(f"   {total_frames} frames at {fps}fps = {total_frames/fps:.1f}s")
    print()
    
    # Vælg scener baseret på script nummer
    scenes = [
        ("House of Wisdom", scene_house_of_wisdom),
        ("Baghdad Morning", scene_baghdad_morning),
        ("Scholar Reading", scene_scholar_reading),
        ("Timeline", scene_timeline),
    ]
    
    # Generer scener
    frames_per_scene = total_frames // len(scenes)
    for name, draw_func in scenes:
        animate_scene_draw(name, frames_per_scene, draw_func)
    
    # Render video
    print(f"\n  🎞 Samler video...")
    video_path = render_video(f"cc-animated-{scene_num:02d}")
    
    total_size = sum(f.stat().st_size for f in FRAMES_DIR.glob("*.png"))
    print(f"\n  📊 Total: {total_size/1024/1024:.1f}MB frames → {video_path.stat().st_size/1024/1024:.1f}MB video")
    print(f"\n  ✅ FÆRDIG! {video_path}")
    print()
    print(f"  📱 Send til Boss: {video_path}")
    
    # Ryd frames
    if not args.preview:
        clean_frames()

if __name__ == "__main__":
    main()
