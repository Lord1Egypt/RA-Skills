#!/usr/bin/env python3

# © 2026 Vortex Group. Alle rettigheder forbeholdt.
# produce_with_manim.py — Manim — matematisk animation
# Tilhører: projects/factsage/produce_with_manim.py
"""
FactSage Producer — CC's Animation Configs Integration
========================================================
Bruger CC's animation_configs.py (source of truth) til at
rendere hvert segment med den korrekte template.

Pipeline:
  Segment config → instantiate_segment() → render() → segment.mp4
  + Edge TTS → ffmpeg stitch → færdig video

Kørsel:
  python3 produce_with_manim.py              # Batch alle
  python3 produce_with_manim.py 9            # Kun video 9
  python3 produce_with_manim.py 9 --quick    # Hurtig rendering
"""

import os, sys, json, asyncio, subprocess, re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "animation"))

from video_configs import VIDEOS

# Manim templates + CC configs
try:
    from manim_templates.base_renderer import COLORS, W, H, FPS
    from animation_configs import get_script_config, instantiate_segment
    HAS_CC = True
except ImportError as e:
    print(f"⚠️ CC configs not available: {e}")
    HAS_CC = False
    W, H, FPS = 1080, 1920, 30

AUDIO_DIR = BASE_DIR / "audio"
SEGMENTS_DIR = BASE_DIR / "segments"
OUTPUT_DIR = BASE_DIR / "output"
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(SEGMENTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

QUICK_MODE = "--quick" in sys.argv


# ==== FALLBACK: Ken Burns (når ingen CC config) ====

def make_fallback_frame(lines):
    # make_fallback_frame() — Udfører opgaven
    """Generer en statisk frame med Parchment & Gold stil"""
    from PIL import Image, ImageDraw, ImageFont
    
    FONT_B = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    FONT_T = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
    FONT_S = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    W, H = 1080, 1920
    GOLD = (255, 215, 0)
    WHITE = (255, 255, 255)
    EMOJI = set('⭐✈️0️⃣🗡️🏝️🏛️🎓🏥🐐☕🌍✝️🌎💃♾️🔢📜📚🔭🕌🗺️⚔️🏹💡🧠🔥✨🏆💎🎯🦅🌙💔🪙🔬')
    
    img = Image.new('RGBA', (W, H), (28, 16, 10))
    draw = ImageDraw.Draw(img)
    
    # Islamic pattern
    cx, cy = W // 2, H // 2
    for i in range(0, H // 2, 25):
        draw.ellipse([cx - H + i*2, cy - H + i*2, cx + H - i*2, cy + H - i*2],
                     outline=(30 + i//10, 18 + i//12, 10), width=1)
    
    # Text
    total = len([l for l in lines if l.strip()])
    base_y = H // 2 - (total * 70) // 2 + 35
    ai = 0
    for line in lines:
        s = line.strip()
        if not s:
            ai += 1; continue
        he = any(c in s for c in EMOJI)
        ct = (ai == total-1) and ('FactSage' in s or 'Follow' in s)
        f, c = (FONT_T, GOLD) if he or ai == 0 else (FONT_S, GOLD) if ct else (FONT_B, WHITE)
        bb = draw.textbbox((0, 0), s, font=f)
        x = (W - (bb[2]-bb[0])) // 2
        y = base_y + ai * 70
        draw.text((x+2, y+2), s, font=f, fill=(0, 0, 0, 200))
        draw.text((x, y), s, font=f, fill=(*c, 255))
        ai += 1
    
    wf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    draw.text((30, 25), "FACTSAGE", font=wf, fill=(120, 80, 20, 150))
    return img


def render_fallback(lines, duration, seg_idx, vid_id):
    # render_fallback() — Renderer output
    """Ken Burns fallback segment"""
    from PIL import Image
    
    img = make_fallback_frame(lines)
    img_path = SEGMENTS_DIR / f"fb_{vid_id:02d}_s{seg_idx:02d}.png"
    img.save(img_path)
    
    out = SEGMENTS_DIR / f"fb_{vid_id:02d}_s{seg_idx:02d}.mp4"
    nf = int(duration * FPS)
    ze = f"if(eq(on,1),1,1+0.06*(on-1)/{max(1,nf-1)})"
    
    subprocess.run(['ffmpeg', '-y', '-loop', '1', '-i', str(img_path),
        '-vf', f"zoompan=z='{ze}':d={nf}:s={W}x{H}:fps={FPS}",
        '-c:v', 'libx264', '-t', str(duration),
        '-preset', 'ultrafast', '-crf', '28', '-pix_fmt', 'yuv420p', str(out)],
        capture_output=True, check=True)
    img_path.unlink()
    return str(out)


# ==== AUDIO ====

async def gen_audio(text, path):
    # gen_audio() — Udfører opgaven
    import edge_tts
    await edge_tts.Communicate(text, "en-US-JennyNeural", rate="-5%").save(path)


# ==== FIND BACKGROUND ====

def find_bg(video_name):
    # find_bg() — Udfører opgaven
    media = BASE_DIR / "media"
    nl = video_name.lower()
    fm = {"fatima":"fatima","hospitals":"hospitals","stars":"stars","flying":"flying",
          "zero":"zero","salahuddin":"salahuddin","sicily":"sicily","wisdom":"wisdom"}
    for k, v in fm.items():
        if k in nl:
            fp = media / v
            if fp.exists():
                for f in sorted(fp.iterdir()):
                    if f.suffix.lower() in ('.jpg','.jpeg','.png'):
                        return str(f)
    return None


# ==== MAIN BUILDER ====

def build_video(vid_id, name, vo_text, segments_config, accent='GOLD'):
    # build_video() — Udfører opgaven
    print(f"\n{'='*50}")
    print(f"🎬 #{vid_id}: {name}")
    print(f"{'='*50}")
    
    safe = name.lower().replace(' ', '_').replace("'","").replace(":","_")[:35]
    
    # 1. Load CC configs
    cc_config = get_script_config(vid_id) if HAS_CC else None
    cc_segs = cc_config.get("segments", []) if cc_config else None
    use_cc = cc_segs is not None and len(cc_segs) > 0
    # Når CC config findes, bruger vi den som source of truth
    # (segments + durations fra CC, voiceover fra video_configs)
    
    if use_cc:
        print(f"  🧠 CC configs: {len(cc_segs)} segments")
        for i, s in enumerate(cc_segs):
            print(f"       {i}. {s['template']} — {s['params'].get('duration',5):.0f}s")
    else:
        print(f"  🖼 Ken Burns fallback ({len(segments_config)} segments)")
    
    # 2. Audio
    ap = AUDIO_DIR / f"cc_{vid_id:02d}.mp3"
    print(f"  🎤 Voiceover...")
    asyncio.run(gen_audio(vo_text, str(ap)))
    
    r = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
        '-of','default=noprint_wrappers=1:nokey=1', str(ap)],
        capture_output=True, text=True)
    ad = float(r.stdout.strip())
    print(f"  ⏱ {ad:.1f}s")
    
    # Scale segment durations — brug CC's durations hvis tilgængelige
    if use_cc:
        ts = sum(s["params"].get("duration", 5) for s in cc_segs)
    else:
        ts = sum(s[1] for s in segments_config)
    scale = ad / ts if ts else 1
    
    # 3. Render segments
    print(f"  🎞 Rendering...")
    seg_files = []
    bg = find_bg(name)
    
    total_segs = len(cc_segs) if use_cc else len(segments_config)
    
    for i in range(total_segs):
        if use_cc:
            # CC template — brug CC's duration
            sc = cc_segs[i].copy()
            sc["params"] = sc.get("params", {}).copy()
            sd = sc["params"].get("duration", 5.0) * scale
            sc["params"]["duration"] = sd
            lines = [sc.get("segment_text", "").split(". ")[0]]
        else:
            lines, ed, _ = segments_config[i]
            sd = ed * scale
        
        # Try template render (CC eller fallback)
        if use_cc:
            try:
                anim = instantiate_segment(sc)
                out = str(SEGMENTS_DIR / f"cc_{vid_id:02d}_s{i:02d}.mp4")
                anim.render(out, cleanup=True)
                seg_files.append(out)
                print(f"    {i}: 🧠 {sc['template']:20s} {sd:.1f}s")
                continue
            except Exception as e:
                print(f"    {i}: ⚠️ template error: {e}")
        
        # Fallback: Ken Burns
        out = render_fallback(lines, sd, i, vid_id)
        seg_files.append(out)
        print(f"    {i}: 🖼 {sd:.1f}s")
    
    # 4. Concat
    cf = SEGMENTS_DIR / f"cc_{vid_id:02d}_list.txt"
    cv = SEGMENTS_DIR / f"cc_{vid_id:02d}_concat.mp4"
    with open(cf, 'w') as f:
        for s in seg_files:
            f.write(f"file '{s}'\n")
    subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(cf),'-c','copy',str(cv)],
                   capture_output=True, check=True)
    
    # 5. Audio
    out = OUTPUT_DIR / f"cc-{vid_id:02d}-{safe}.mp4"
    print(f"  🔊 Final assembly...")
    subprocess.run(['ffmpeg','-y','-i',str(cv),'-i',str(ap),
        '-c:v','copy','-c:a','aac','-b:a','128k','-shortest',
        '-map','0:v:0','-map','1:a:0',str(out)], capture_output=True, check=True)
    
    mb = os.path.getsize(out) / 1024 / 1024
    print(f"  ✅ {mb:.1f}MB, {ad:.1f}s")
    return str(out), ad, mb


# ==== MAIN ====

if __name__ == "__main__":
    print("🎬 FACTSAGE — CC Animation Configs Producer")
    print("=" * 40)
    
    sid = None
    if len(sys.argv) > 1:
        try: sid = int(sys.argv[1])
        except: pass
    
    results = []
    for v in VIDEOS:
        if sid and v[0] != sid: continue
        try:
            r = build_video(*v)
            results.append((v[0], v[1], *r, "✅"))
        except Exception as e:
            import traceback; traceback.print_exc()
            results.append((v[0], v[1], "", 0, 0, f"❌ {e}"))
    
    print(f"\n{'='*40}")
    print("📊 RESULTS")
    for i, n, _, dur, mb, s in results:
        print(f"  #{i} {s} | {n[:40]:40s} | {dur:5.1f}s | {mb:5.1f}MB")
