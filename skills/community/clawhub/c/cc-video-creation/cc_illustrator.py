#!/usr/bin/env python3
"""
# © 2026 Vortex Group. Alle rettigheder forbeholdt.
🎨 CC Illustrator — Tegner historiske scener til FactSage
=========================================================
CC kan selv lave flotte 2D illustrationer!
Ingen eksterne sider, ingen API, 0 kr.

Kør: python3 cc_illustrator.py --scene baghdad
     python3 cc_illustrator.py --scene library
     python3 cc_illustrator.py --video
"""

import cairocffi as cairo
import math, os, subprocess, json
from pathlib import Path

W, H = 1080, 1920
OUTPUT = Path.home() / ".openclaw" / "workspace" / "projects" / "factsage" / "output"
FRAMES = Path("/tmp") / "cc_frames"
FRAMES.mkdir(exist_ok=True)
OUTPUT.mkdir(exist_ok=True)

GOLD = (0.85, 0.65, 0.15)
DARK_GOLD = (0.6, 0.45, 0.1)
WARM = (0.95, 0.88, 0.75)
DARK = (0.06, 0.04, 0.1)
WARM_GOLD = (0.95, 0.85, 0.6)
SKY_TOP = (0.05, 0.08, 0.2)
SKY_BOT = (0.1, 0.12, 0.25)
SAND = (0.76, 0.7, 0.5)
BROWN = (0.4, 0.25, 0.1)
SKIN = (0.7, 0.55, 0.35)
WHITE = (0.95, 0.93, 0.9)
RED = (0.75, 0.15, 0.15)
GREEN = (0.1, 0.4, 0.15)

def surface():
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    return s, cairo.Context(s)

def save(s, name):
    s.write_to_png(str(FRAMES / name))

# ─── BYGNINGER ──────────────────────────────────────────

def draw_mosque(ctx, cx=540, ground=1600, scale=1.0):
    """Tegn en smuk moské med kuppel og minareter."""
    ctx.save()
    ctx.translate(cx, ground)
    ctx.scale(scale, scale)
    
    # Hovedkuppel
    dome_r = 200
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(2)
    ctx.save()
    # Kuppel bue
    ctx.arc(0, -220, dome_r, math.pi, 0)
    ctx.set_source_rgba(0.85, 0.65, 0.15, 0.2)
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.stroke()
    # Månespids på kuppel
    ctx.move_to(-15, -420)
    ctx.line_to(0, -440)
    ctx.line_to(15, -420)
    ctx.stroke()
    ctx.restore()
    
    # Hovedbygning
    ctx.set_source_rgb(*WARM)
    ctx.set_line_width(1)
    ctx.rectangle(-250, -220, 500, 220)  # vægge
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.stroke()
    
    # Buer på facaden
    for i in range(5):
        bx = -200 + i * 100
        ctx.save()
        ctx.translate(bx, 0)
        ctx.set_source_rgb(*GOLD)
        ctx.set_line_width(1.5)
        ctx.arc(0, -50 - 80, 40, math.pi, 0)
        ctx.set_source_rgba(0.2, 0.15, 0.1, 0.5)
        ctx.fill()
        ctx.set_source_rgb(*GOLD)
        ctx.stroke()
        # Søjle
        ctx.move_to(-35, 0)
        ctx.line_to(-35, -130)
        ctx.stroke()
        ctx.move_to(35, 0)
        ctx.line_to(35, -130)
        ctx.stroke()
        ctx.restore()
    
    # Minareter
    for dx in [-300, 300]:
        ctx.save()
        ctx.translate(dx, 0)
        # Tårn
        ctx.set_source_rgb(*WARM)
        ctx.rectangle(-15, -400, 30, 400)
        ctx.fill()
        ctx.set_source_rgb(*GOLD)
        ctx.set_line_width(1.5)
        ctx.stroke()
        # Spids
        ctx.move_to(-15, -400)
        ctx.line_to(0, -430)
        ctx.line_to(15, -400)
        ctx.fill()
        ctx.stroke()
        # Balcon
        ctx.set_source_rgb(*GOLD)
        ctx.rectangle(-20, -200, 40, 10)
        ctx.fill()
        ctx.restore()
    
    # Dør (indgang)
    ctx.set_source_rgb(*BROWN)
    ctx.rectangle(-40, -60, 80, 60)
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(2)
    ctx.stroke()
    
    ctx.restore()

def draw_palace(ctx, cx=540, ground=1600, scale=0.8):
    """Tegn et islamisk palads."""
    ctx.save()
    ctx.translate(cx, ground)
    ctx.scale(scale, scale)
    
    # Hovedbygning
    ctx.set_source_rgb(*WARM)
    ctx.rectangle(-300, -250, 600, 250)
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Store bueindgang
    ctx.save()
    ctx.translate(0, 0)
    ctx.arc(0, -120, 100, math.pi, 0)
    ctx.set_source_rgba(0.2, 0.15, 0.1, 0.6)
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.stroke()
    ctx.restore()
    
    # Tag med brystværn
    for i in range(9):
        bx = -280 + i * 70
        ctx.rectangle(bx, -250, 40, 20)
        ctx.set_source_rgb(*GOLD)
        ctx.fill()
    
    ctx.restore()

def draw_library(ctx, cx=540, ground=1600, scale=0.9):
    """Tegn et bibliotek (House of Wisdom)."""
    ctx.save()
    ctx.translate(cx, ground)
    ctx.scale(scale, scale)
    
    # Vægge
    ctx.set_source_rgb(*WARM)
    ctx.rectangle(-280, -300, 560, 300)
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Bogreoler (fyldt med "bøger")
    colors = [(0.75,0.1,0.1), (0.1,0.3,0.1), (0.1,0.15,0.4), (0.5,0.3,0.1), (0.4,0.2,0.5)]
    for shelf_x in range(-250, 300, 90):
        for shelf_y in range(-280, 0, 60):
            ctx.set_source_rgb(*colors[(shelf_x + shelf_y) % 5])
            ctx.rectangle(shelf_x + 5, shelf_y, 70, 40)
            ctx.fill()
    
    # Bue over indgang
    ctx.arc(0, -60, 100, math.pi, 0)
    ctx.set_source_rgba(0.85, 0.65, 0.15, 0.15)
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(2)
    ctx.stroke()
    
    ctx.restore()

# ─── MENNESKER ──────────────────────────────────────────

def draw_scholar(ctx, x, y, scale=1.0, facing_right=True):
    """Tegn en lærd (stiliseret figur)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale * (1 if facing_right else -1), scale)
    
    # Krop (kappe)
    ctx.set_source_rgb(0.6, 0.4, 0.15)
    ctx.move_to(-30, 0)
    ctx.line_to(-40, -120)
    ctx.line_to(40, -120)
    ctx.line_to(30, 0)
    ctx.close_path()
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(1)
    ctx.stroke()
    
    # Hoved
    ctx.set_source_rgb(*SKIN)
    ctx.arc(0, -145, 30, 0, 2*math.pi)
    ctx.fill()
    ctx.set_source_rgb(*GOLD)
    ctx.set_line_width(1)
    ctx.stroke()
    
    # Turban
    ctx.set_source_rgb(*WARM)
    ctx.arc(0, -165, 28, 0, math.pi)
    ctx.fill()
    ctx.stroke()
    
    # Turban spids
    ctx.move_to(-5, -193)
    ctx.line_to(0, -210)
    ctx.line_to(5, -193)
    ctx.fill()
    
    # Bog i hænderne
    ctx.set_source_rgb(0.8, 0.7, 0.5)
    ctx.rectangle(-25, -90, 50, 35)
    ctx.fill()
    ctx.set_source_rgb(*BROWN)
    ctx.set_line_width(1)
    ctx.stroke()
    
    ctx.restore()

# ─── SCENER ──────────────────────────────────────────────

def make_scene_baghdad(offset=0):
    """Scene 1: Baghdad skyline - Den gyldne by."""
    frames = 90
    for f in range(frames):
        progress = f / frames
        s, ctx = surface()
        
        # Himmel (gradient)
        for y in range(0, H, 4):
            t = y / H
            r = 0.05 - t * 0.02
            g = 0.08 - t * 0.04
            b = 0.2 + t * 0.05
            ctx.set_source_rgb(r, g, b)
            ctx.rectangle(0, y, W, 4)
            ctx.fill()
        
        # Stjerner på himlen (blinkende)
        import random
        random.seed(42)
        for star in range(50):
            sx = random.randint(0, W)
            sy = random.randint(0, 500)
            brightness = 0.3 + 0.3 * math.sin(f * 0.1 + star)
            ctx.set_source_rgba(0.95, 0.85, 0.6, brightness)
            ctx.arc(sx, sy, random.randint(1, 3), 0, 2*math.pi)
            ctx.fill()
        
        # Måne
        ctx.set_source_rgb(*GOLD)
        ctx.arc(W - 150, 150, 50, 0, 2*math.pi)
        ctx.fill()
        ctx.set_source_rgb(*DARK)
        ctx.arc(W - 140, 140, 45, 0, 2*math.pi)
        ctx.fill()
        
        # Ørken/sand i bunden
        for y in range(1400, H, 4):
            t = (y - 1400) / 520
            ctx.set_source_rgb(0.5 + t*0.3, 0.35 + t*0.3, 0.1 + t*0.2)
            ctx.rectangle(0, y, W, 4)
            ctx.fill()
        
        # Palmer (stiliseret)
        for px in [100, 350, 750, 980]:
            ctx.save()
            ctx.translate(px, 1580)
            # Stamme
            ctx.set_source_rgb(*BROWN)
            ctx.set_line_width(6)
            ctx.move_to(0, 0)
            ctx.line_to(0, -150 - 50 * math.sin(px * 0.1))
            ctx.stroke()
            # Blade
            for b in range(5):
                angle = b * 1.2 - 0.5
                ctx.set_source_rgb(0.1, 0.35, 0.1)
                ctx.move_to(0, -150)
                ctx.curve_to(0, -200, 
                           math.cos(angle) * 80, -180 + math.sin(f*0.02+b)*10, 
                           math.cos(angle) * 100, -160)
                ctx.set_line_width(4)
                ctx.stroke()
            ctx.restore()
        
        # Bygninger i horisonten
        draw_mosque(ctx, 540, 1500, 0.7)
        # Mindre bygninger omkring
        for bx in [200, 350, 720, 850]:
            bh = 100 + 80 * math.sin(bx * 0.1)
            ctx.set_source_rgb(*WARM)
            ctx.rectangle(bx - 30, 1500 - bh, 60, bh)
            ctx.fill()
            ctx.set_source_rgb(*GOLD)
            ctx.set_line_width(1)
            ctx.stroke()
        
        # Titel
        ctx.set_source_rgb(*WARM_GOLD)
        ctx.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(60)
        ctx.move_to(200, 800)
        ctx.show_text("The Golden Age")
        ctx.set_font_size(30)
        ctx.move_to(300, 870)
        ctx.show_text("Baghdad — Center of the World")
        
        # Text der fader ind
        if progress > 0.5:
            alpha = min(1, (progress - 0.5) * 4)
            ctx.set_source_rgba(*WARM_GOLD, alpha)
            ctx.set_font_size(22)
            text = "A beacon of knowledge, science, and culture"
            ctx.move_to(220, 950)
            ctx.show_text(text)
        
        save(s, f"frame_{offset+f:05d}.png")
        if f % 20 == 0:
            print(f"  Baghdad: {f/frames*100:.0f}%", flush=True)

def make_scene_library(offset=0):
    """Scene 2: House of Wisdom bibliotek."""
    frames = 90
    for f in range(frames):
        progress = f / frames
        s, ctx = surface()
        
        # Indendørs baggrund (varm belysning)
        for y in range(0, H, 4):
            t = y / H
            ctx.set_source_rgb(0.15 + t*0.1, 0.1 + t*0.08, 0.05)
            ctx.rectangle(0, y, W, 4)
            ctx.fill()
        
        # Gulv (marmor mønster)
        ctx.set_source_rgb(0.3, 0.25, 0.2)
        ctx.rectangle(0, 1500, W, 420)
        ctx.fill()
        for gx in range(0, W, 60):
            ctx.set_source_rgba(0.85, 0.65, 0.15, 0.05)
            ctx.rectangle(gx, 1500, 2, 420)
            ctx.fill()
        
        # Bogreoler på væggen
        draw_library(ctx, 540, 1480, 0.7)
        
        # Lærde der studerer
        draw_scholar(ctx, 250, 1470, 1.2, True)
        draw_scholar(ctx, 800, 1480, 1.0, False)
        
        # Samtale bobler (bare lysprikker der viser aktivitet)
        for sparkle in range(10):
            sx = 400 + 200 * math.sin(sparkle * 1.5)
            sy = 1200 + 50 * math.sin(f * 0.05 + sparkle)
            ctx.set_source_rgba(0.95, 0.85, 0.6, 0.1 + 0.1 * math.sin(f * 0.1 + sparkle))
            ctx.arc(sx, sy, 5, 0, 2*math.pi)
            ctx.fill()
        
        # Lyskilde (olielampe/lys) der flimrer
        flicker = 0.8 + 0.2 * math.sin(f * 0.15)
        ctx.set_source_rgba(1, 0.8, 0.3, 0.06 * flicker)
        ctx.arc(540, 800, 400 * flicker, 0, 2*math.pi)
        ctx.fill()
        ctx.set_source_rgba(1, 0.8, 0.3, 0.04 * flicker)
        ctx.arc(540, 800, 600 * flicker, 0, 2*math.pi)
        ctx.fill()
        
        # Titel
        ctx.set_source_rgb(*WARM_GOLD)
        ctx.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(55)
        ctx.move_to(220, 400)
        ctx.show_text("House of Wisdom")
        ctx.set_font_size(25)
        ctx.set_source_rgb(*GOLD)
        ctx.move_to(300, 470)
        ctx.show_text("830 CE · Baghdad, Iraq")
        
        if progress > 0.5:
            alpha = min(1, (progress - 0.5) * 4)
            ctx.set_source_rgba(*WARM_GOLD, alpha)
            ctx.set_font_size(22)
            ctx.move_to(230, 550)
            ctx.show_text("Scholars translating and preserving knowledge")
        
        save(s, f"frame_{offset+f:05d}.png")
        if f % 20 == 0:
            print(f"  Library: {f/frames*100:.0f}%", flush=True)

def make_scene_scholars(offset=0):
    """Scene 3: Scholars at work."""
    frames = 90
    for f in range(frames):
        progress = f / frames
        s, ctx = surface()
        
        # Varm indendørs baggrund
        for y in range(0, H, 4):
            t = y / H
            ctx.set_source_rgb(0.18 - t*0.05, 0.12 - t*0.03, 0.06)
            ctx.rectangle(0, y, W, 4)
            ctx.fill()
        
        # Islamisk bue vindue i baggrunden
        ctx.save()
        ctx.translate(540, 600)
        ctx.arc(0, 0, 250, math.pi, 0)
        ctx.set_source_rgba(0.05, 0.08, 0.15, 0.3)
        ctx.fill()
        ctx.set_source_rgb(*GOLD)
        ctx.set_line_width(3)
        ctx.stroke()
        # Måneskin gennem vinduet
        ctx.set_source_rgba(0.85, 0.65, 0.15, 0.05)
        ctx.arc(50, -80, 30, 0, 2*math.pi)
        ctx.fill()
        ctx.restore()
        
        # Bord
        ctx.set_source_rgb(*BROWN)
        ctx.rectangle(250, 1350, 580, 25)  # bordplade
        ctx.fill()
        ctx.set_source_rgb(*GOLD)
        ctx.set_line_width(1)
        ctx.stroke()
        # Bordben
        ctx.rectangle(270, 1375, 25, 200)
        ctx.fill()
        ctx.rectangle(785, 1375, 25, 200)
        ctx.fill()
        
        # Bøger på bordet
        ctx.set_source_rgb(0.8, 0.7, 0.5)
        ctx.rectangle(350, 1300, 180, 50)
        ctx.fill()
        ctx.set_source_rgb(0.7, 0.5, 0.3)
        ctx.rectangle(530, 1310, 120, 40)
        ctx.fill()
        ctx.set_source_rgb(*RED)
        ctx.rectangle(650, 1300, 80, 50)
        ctx.fill()
        
        # Lærde
        draw_scholar(ctx, 300, 1450, 1.3, True)
        draw_scholar(ctx, 760, 1460, 1.1, False)
        
        # Skrivehånd der bevæger sig
        hand_x = 380 + 30 * math.sin(f * 0.08)
        hand_y = 1300 + 10 * math.sin(f * 0.12)
        ctx.set_source_rgb(*SKIN)
        ctx.arc(hand_x, hand_y, 12, 0, 2*math.pi)
        ctx.fill()
        
        # Lyskilde
        flicker = 0.85 + 0.15 * math.sin(f * 0.2)
        ctx.set_source_rgba(1, 0.8, 0.3, 0.05 * flicker)
        ctx.arc(540, 1000, 500 * flicker, 0, 2*math.pi)
        ctx.fill()
        
        # Titel
        ctx.set_source_rgb(*WARM_GOLD)
        ctx.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(50)
        ctx.move_to(280, 350)
        ctx.show_text("The Scholars")
        ctx.set_font_size(25)
        ctx.set_source_rgb(*GOLD)
        ctx.move_to(250, 420)
        ctx.show_text("Preserving civilization's greatest works")
        
        if progress > 0.5:
            alpha = min(1, (progress - 0.5) * 4)
            ctx.set_source_rgba(*WARM_GOLD, alpha)
            ctx.set_font_size(22)
            ctx.move_to(180, 1800)
            ctx.show_text("Subjects: Mathematics · Astronomy · Medicine · Philosophy")
        
        save(s, f"frame_{offset+f:05d}.png")
        if f % 20 == 0:
            print(f"  Scholars: {f/frames*100:.0f}%", flush=True)

def make_scene_legacy(offset=0):
    """Scene 4: Legacy - tidslinje."""
    frames = 90
    for f in range(frames):
        progress = f / frames
        s, ctx = surface()
        
        # Baggrund
        for y in range(0, H, 4):
            t = y / H
            ctx.set_source_rgb(0.06, 0.05 - t*0.02, 0.1 + t*0.05)
            ctx.rectangle(0, y, W, 4)
            ctx.fill()
        
        # Islamisk stjerne mønster (meget svagt i baggrunden)
        ctx.set_source_rgba(0.85, 0.65, 0.15, 0.03)
        for gx in range(-50, W+50, 150):
            for gy in range(-50, H+50, 150):
                ctx.save()
                ctx.translate(gx, gy)
                ctx.rotate(f * 0.005)
                for i in range(8):
                    ctx.rotate(math.pi/4)
                    ctx.move_to(0, -15)
                    ctx.line_to(4, -5)
                    ctx.line_to(0, 0)
                    ctx.line_to(-4, -5)
                    ctx.close_path()
                ctx.fill()
                ctx.restore()
        
        # Tidslinje
        timeline_y = 700
        ctx.set_source_rgb(*GOLD)
        ctx.set_line_width(3)
        ctx.move_to(100, timeline_y)
        ctx.line_to(980, timeline_y)
        ctx.stroke()
        
        # Årstal på tidslinje
        events = [
            (0.0, "700 CE", "Paper reaches\nIslamic world", 30),
            (0.25, "750 CE", "Translation\nmovement begins", 35),
            (0.5, "830 CE", "House of\nWisdom founded", 45),
            (0.75, "1000 CE", "Golden Age\nat its peak", 40),
            (1.0, "1258 CE", "Legacy\nlives on", 35),
        ]
        
        for pos, year, desc, size in events:
            reveal_pos = progress * 1.2 - pos
            if reveal_pos > 0:
                x = 100 + pos * 880
                alpha = min(1, reveal_pos * 3)
                
                # Prik på tidslinje
                ctx.set_source_rgba(*GOLD, alpha)
                ctx.arc(x, timeline_y, 10, 0, 2*math.pi)
                ctx.fill()
                
                # Årstal
                ctx.set_source_rgba(*WARM_GOLD, alpha)
                ctx.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                ctx.set_font_size(size)
                ctx.move_to(x - 30, timeline_y - 50)
                ctx.show_text(year)
                
                # Beskrivelse
                ctx.set_font_size(18)
                lines = desc.split("\n")
                for li, line in enumerate(lines):
                    ctx.move_to(x - 40, timeline_y + 40 + li * 25)
                    ctx.show_text(line)
        
        # Titel
        ctx.set_source_rgb(*WARM_GOLD)
        ctx.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(55)
        ctx.move_to(300, 250)
        ctx.show_text("A Lasting Legacy")
        
        # CTA (call to action)
        if progress > 0.7:
            alpha = min(1, (progress - 0.7) * 4)
            ctx.set_source_rgba(*WARM_GOLD, alpha)
            ctx.set_font_size(40)
            ctx.move_to(300, 1800)
            ctx.show_text("FactSage — Islamic History")
            ctx.set_font_size(20)
            ctx.move_to(340, 1860)
            ctx.show_text("Discover the stories that shaped our world")
        
        save(s, f"frame_{offset+f:05d}.png")
        if f % 20 == 0:
            print(f"  Legacy: {f/frames*100:.0f}%", flush=True)

# ─── MAIN ────────────────────────────────────────────────

def render_video(name="cc-illustrated-09", fps=30):
    print("\n🎞 Renderer video...")
    output = OUTPUT / f"{name}.mp4"
    result = subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", str(FRAMES / "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "fast", "-crf", "23",
        str(output)
    ], capture_output=True, text=True)
    if result.returncode == 0:
        size = output.stat().st_size
        print(f"  ✅ FÆRDIG! {size/1024:.0f}KB - {output}")
    else:
        print(f"  ❌ {result.stderr[-200:]}")
    return output

def clean():
    for f in FRAMES.glob("*.png"):
        f.unlink()

if __name__ == "__main__":
    import sys
    
    clean()
    print("\n🎨 CC ILLUSTRATOR — Historiske scener")
    print("="*50)
    
    make_scene_baghdad(offset=0)
    make_scene_library(offset=90)
    make_scene_scholars(offset=180)
    make_scene_legacy(offset=270)
    
    video = render_video()
    
    total_frames = len(list(FRAMES.glob("*.png")))
    print(f"\n  📊 {total_frames} frames → {video.stat().st_size/1024:.0f}KB video")
    print(f"\n  ✅ KLAR! {video}")
    
    clean()
