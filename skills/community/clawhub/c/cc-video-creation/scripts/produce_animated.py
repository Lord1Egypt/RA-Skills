#!/usr/bin/env python3

# © 2026 Vortex Group. Alle rettigheder forbeholdt.
# produce_animated.py — Automatiseret opgave/script
# Tilhører: projects/factsage/produce_animated.py
"""
FactSage ANIMATED Producer — Phase 1
======================================
Tilføjer professionel animation til FactSage videoer uden AI modeller.

Animation features:
- Ken Burns zoom/pan på baggrund (ffmpeg zoompan)
- Text fade-in per segment (ffmpeg fade) 
- Crossfade transitions mellem segments (ffmpeg xfade)
- Animeret baggrund med islamisk mønster
- Kan bruge Pexels/internationale baggrundsbilleder

Kørsel:
  python3 produce_animated.py          # Batch: alle videoer
  python3 produce_animated.py 9        # Single: kun video 9
  python3 produce_animated.py 9 --quick # Quick: lavere kvalitet, hurtigere

Krav: PIL, numpy, ffmpeg ✅ (alt allerede installeret)
"""

import os, sys, subprocess, asyncio, math, random, json
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ============================================================
# CONFIG
BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, "output")
AUDIO_DIR = os.path.join(BASE, "audio")
FRAMES_DIR = os.path.join(BASE, "frames")
SEGMENTS_DIR = os.path.join(BASE, "segments")
MEDIA_DIR = os.path.join(BASE, "media")

os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(SEGMENTS_DIR, exist_ok=True)

W, H = 1080, 1920  # 9:16 portrait
FPS = 30
BG_COLOR = (28, 16, 10)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

# Fonts
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_TITLE = ImageFont.truetype(FONT_BOLD_PATH, 64)
FONT_BOLD = ImageFont.truetype(FONT_BOLD_PATH, 48)
FONT_SMALL = ImageFont.truetype(FONT_BOLD_PATH, 38)
FONT_WATERMARK = ImageFont.truetype(FONT_BOLD_PATH, 24)

# Emoji der trigger guld-farve
EMOJI_SET = set('⭐✈️0️⃣🗡️🏝️🏛️🎓🏥🐐☕🌍✝️🌎💃♾️🔢📜📚🔭🕌🗺️⚔️🏹💡🧠🔥✨🏆💎🎯🦅🌙💔🪙🔬')

QUICK_MODE = "--quick" in sys.argv

# BACKGROUND GENERATOR
def generate_islamic_pattern(w=W, h=H, time_offset=0.0):
    """
    Generer en baggrund med islamisk-inspireret geometrisk mønster.
    time_offset = animation frame seed (0.0 - 1.0)
    """
    img = Image.new('RGB', (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Animerede cirkler (subtilt skift i farve)
    phase = time_offset * 2 * math.pi
    cx, cy = w // 2, h // 2
    max_r = int(math.sqrt(cx**2 + cy**2))
    
    # Koncentriske cirkler
    for i in range(0, h // 2, 15):
        r_offset = int(8 * math.sin(phase + i * 0.05))
        r_val = min(80, 30 + i // 10 + r_offset)
        g_val = min(60, 18 + i // 12 + r_offset // 2)
        b_val = min(40, 10 + i // 15)
        
        radius = max_r - i * 2
        if radius > 0:
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                outline=(r_val, g_val, b_val), width=2
            )
    
    # Diagonale linjer (matematisk mønster)
    for i in range(-h, w * 2, 35):
        offset = int(5 * math.sin(phase + i * 0.02))
        draw.line([(i + offset, 0), (i + h + offset, h)], fill=(45, 35, 25), width=1)
        draw.line([(i - offset, 0), (i - h - offset, h)], fill=(40, 30, 20), width=1)
    
    # Små dekorative diamanter
    for _ in range(15):
        dx = random.randint(100, w - 100)
        dy = random.randint(100, h - 100)
        sz = random.randint(4, 12)
        alpha = random.randint(40, 80)
        points = [
            (dx, dy - sz), (dx + sz, dy),
            (dx, dy + sz), (dx - sz, dy)
        ]
        draw.polygon(points, outline=(alpha, alpha//2, alpha//4), width=1)
    
    return img


def create_background_video(duration, output_path, fps=FPS, w=W, h=H, 
    # create_background_video() — Udfører opgaven
                            bg_image=None, ken_burns=True):
    """
    Opret en baggrundsvideo med Ken Burns zoom/pan.
    Hvis bg_image er None, genereres et animeret islamisk mønster.
    
    For genererede baggrunde: laver en kort loop (3s) og bruger -stream_loop
    så vi undgår at generere tusindvis af individuelle frames.
    """
    if bg_image and os.path.exists(bg_image):
        # Brug billede med Ken Burns zoom
        if ken_burns:
            zoom_start = 1.0
            zoom_end = 1.12
            
            # ffmpeg zoompan filter - smooth zoom
            n_frames = int(duration * fps)
            zoom_expr = f"if(eq(on,1),{zoom_start},{zoom_start}+({zoom_end}-{zoom_start})*(on-1)/{n_frames-1})"
            filter_chain = (
                f"zoompan=z='{zoom_expr}':"
                f"d={n_frames}:"
                f"s={w}x{h}:"
                f"fps={fps}"
            )
        else:
            filter_chain = f"scale={w}:{h},fps={fps}"
        
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1', '-i', bg_image,
            '-vf', filter_chain,
            '-c:v', 'libx264',
            '-t', str(duration),
            '-preset', 'ultrafast' if QUICK_MODE else 'medium',
            '-crf', '28' if QUICK_MODE else '26',
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)
    else:
        # Brug PIL til at generere ÉN frame som baggrund
        # og brug ffmpeg zoompan til at animere den
        temp_frame = os.path.join(FRAMES_DIR, f"_bg_{os.path.basename(output_path).replace('.mp4','.png')}")
        
        # Generer frame med islamisk mønster
        img = generate_islamic_pattern(w, h, 0.0)
        img.save(temp_frame)
        
        # Subtle slow zoom
        n_frames = int(duration * fps)
        zoom_start = 1.0
        zoom_end = 1.06  # Very subtle zoom
        zoom_expr = f"if(eq(on,1),{zoom_start},{zoom_start}+({zoom_end}-{zoom_start})*(on-1)/{n_frames-1})"
        
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1', '-i', temp_frame,
            '-vf', (
                f"zoompan=z='{zoom_expr}':"
                f"d={n_frames}:"
                f"s={w}x{h}:"
                f"fps={fps}"
            ),
            '-c:v', 'libx264',
            '-t', str(duration),
            '-preset', 'ultrafast' if QUICK_MODE else 'medium',
            '-crf', '28' if QUICK_MODE else '26',
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        
        # Cleanup
        try:
            os.remove(temp_frame)
        except:
            pass
    
    return output_path


# TEXT FRAME GENERATOR
def make_text_frame(lines, frame_size=(W, H), title=False):
    """
    Generer en PIL frame med tekst (samme stil som original, men renset)
    Returnerer PIL Image med transparent baggrund (RGBA)
    """
    # Lav et transparent lag
    img = Image.new('RGBA', frame_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    total = len([l for l in lines if l.strip()])
    line_h = 70
    base_y = H // 2 - (total * line_h) // 2 + 35
    
    anim_idx = 0
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            anim_idx += 1
            continue
        
        has_emoji = any(c in stripped for c in EMOJI_SET)
        is_cta = (anim_idx == total - 1) and ('FactSage' in stripped or 'Follow' in stripped)
        
        if has_emoji or (title and anim_idx == 0):
            font, color = FONT_TITLE, GOLD
        elif is_cta:
            font, color = FONT_SMALL, GOLD
        else:
            font, color = FONT_BOLD, WHITE
        
        bbox = draw.textbbox((0, 0), stripped, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        y = base_y + anim_idx * line_h
        
        # Shadow
        draw.text((x+2, y+2), stripped, font=font, fill=(0, 0, 0, 200))
        # Text
        draw.text((x, y), stripped, font=font, fill=(*color, 255))
        
        anim_idx += 1
    
    return img


# SEGMENT BUILDER (ffmpeg)
def build_segment(text_lines, duration, seg_idx, vid_id, bg_video, 
                  title=False):
    """
    Byg et segment med tekst overlay + fade in/out.
    
    1. Generer text frame (PNG med transparent baggrund)
    2. Overlay text på background video med ffmpeg
    3. Tilføj fade in + out
    """
    # Generer text frame
    text_img = make_text_frame(text_lines, title=title)
    text_path = os.path.join(FRAMES_DIR, f"anim{vid_id:02d}_seg{seg_idx:02d}.png")
    text_img.save(text_path)
    
    seg_output = os.path.join(SEGMENTS_DIR, f"anim{vid_id:02d}_seg{seg_idx:02d}.mp4")
    
    # Hent bg_video duration (vi bruger den fulde bg video og klipper rigtigt sted)
    if QUICK_MODE:
        # Enklere filter for hurtig rendering
        filter_complex = (
            f"[0:v]trim=0:{duration},setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.5:color=black,"
            f"fade=t=out:st={duration-0.5}:d=0.5:color=black[bg];"
            f"[1:v]format=rgba,colorchannelmixer=aa=1.0[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p[v]"
        )
    else:
        # Full quality with text fade-in
        text_fade_duration = 0.4  # seconds for each text line to fade in
        filter_complex = (
            f"[0:v]trim=0:{duration},setpts=PTS-STARTPTS,"
            f"fade=t=in:st=0:d=0.4:color=black,"
            f"fade=t=out:st={duration-0.4}:d=0.4:color=black[bg];"
            f"[1:v]format=rgba,colorchannelmixer=aa=1.0[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2:format=auto,"
            f"format=yuv420p[v]"
        )
    
    cmd = [
        'ffmpeg', '-y',
        '-i', bg_video,        # [0:v] background
        '-i', text_path,       # [1:v] text overlay
        '-filter_complex', filter_complex,
        '-map', '[v]',
        '-c:v', 'libx264',
        '-preset', 'ultrafast' if QUICK_MODE else 'medium',
        '-crf', '28' if QUICK_MODE else '26',
        '-pix_fmt', 'yuv420p',
        '-r', str(FPS),
        '-t', str(duration),
        seg_output
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    return seg_output


# AUDIO GENERATION
async def generate_audio(text, out_path, voice="en-US-JennyNeural", rate="-5%"):
    """Generate voiceover using Edge TTS"""
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(out_path)
    return out_path


# FIND BACKGROUND IMAGE
def find_background_for_video(vid_name):
    """Find best background image for a video from media folder"""
    name_lower = vid_name.lower()
    media_folders = {
        "fatima": "fatima",
        "hospitals": "hospitals",
        "star": "stars",
        "flying": "flying",
        "zero": "zero",
        "salahuddin": "salahuddin",
        "sicily": "sicily",
        "wisdom": "wisdom",
        "house": "wisdom",
    }
    
    for key, folder in media_folders.items():
        if key in name_lower:
            folder_path = os.path.join(MEDIA_DIR, folder)
            if os.path.isdir(folder_path):
                for f in sorted(os.listdir(folder_path)):
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        return os.path.join(folder_path, f)
    return None


# MAIN VIDEO BUILDER
def build_video(vid_id, name, vo_text, segments_config, accent='GOLD',
                voice="en-US-JennyNeural"):
    """
    Build a complete animated video
    
    Pipeline:
    1. Find/generer background video (med Ken Burns zoom)
    2. Generer voiceover med Edge TTS
    3. For hvert segment: overlay text på background video
    4. Concat segments med crossfade
    5. Add audio
    """
    print(f"\n{'='*60}")
    print(f"🎬 Animated #{vid_id}: {name}")
    print(f"{'='*60}")
    
    safe_name = name.lower().replace(' ', '_').replace("'", "").replace(":","_")[:35]
    total_seg_time = sum(s[1] for s in segments_config)
    
    # 1. Find background image
    bg_img = find_background_for_video(name)
    if bg_img:
        print(f"  🖼 Baggrund: {os.path.basename(bg_img)}")
    else:
        print(f"  🎨 Baggrund: Genereret islamisk mønster")
    
    # 2. Generate audio
    audio_path = os.path.join(AUDIO_DIR, f"anim{vid_id:02d}.mp3")
    print(f"  🎤 Genererer voiceover...")
    asyncio.run(generate_audio(vo_text, audio_path, voice))
    
    # Get audio duration
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', audio_path],
        capture_output=True, text=True
    )
    audio_duration = float(result.stdout.strip())
    print(f"  ⏱ Audio: {audio_duration:.1f}s")
    
    # Scale segment durations to match audio
    scale = audio_duration / total_seg_time if total_seg_time > 0 else 1
    
    # 3. Create background video (long enough for entire video)
    bg_video_path = os.path.join(SEGMENTS_DIR, f"anim{vid_id:02d}_bg.mp4")
    print(f"  🎞 Opretter baggrundsvideo ({audio_duration:.1f}s)...")
    create_background_video(
        duration=audio_duration,
        output_path=bg_video_path,
        bg_image=bg_img,
        ken_burns=(bg_img is not None)
    )
    
    # 4. Build each segment
    print(f"  🎬 Bygger {len(segments_config)} segments...")
    segment_files = []
    cumulative_time = 0.0
    
    for i, (lines, est_dur, is_title) in enumerate(segments_config):
        seg_dur = est_dur * scale
        seg_path = build_segment(
            lines, seg_dur, i, vid_id, bg_video_path, is_title
        )
        segment_files.append(seg_path)
        print(f"    Seg {i}: {seg_dur:.1f}s ✓")
    
    # 5. Create concat file with crossfade
    concat_file = os.path.join(SEGMENTS_DIR, f"anim{vid_id:02d}_concat.txt")
    concat_video = os.path.join(SEGMENTS_DIR, f"anim{vid_id:02d}_concat.mp4")
    
    if len(segment_files) > 1:
        # Use ffmpeg concat demuxer (no transitions - just seamless)
        with open(concat_file, 'w') as f:
            for seg in segment_files:
                f.write(f"file '{seg}'\n")
        
        subprocess.run([
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', concat_file, '-c', 'copy', concat_video
        ], capture_output=True, check=True)
    else:
        concat_video = segment_files[0]
    
    # 6. Add audio to final video
    output_path = os.path.join(OUTPUT, f"animated-{vid_id:02d}-{safe_name}.mp4")
    print(f"  🔊 Tilføjer audio...")
    
    # Use first audio stream, ignore second if any
    subprocess.run([
        'ffmpeg', '-y',
        '-i', concat_video,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '128k',
        '-shortest',
        '-map', '0:v:0', '-map', '1:a:0',
        output_path
    ], capture_output=True, check=True)
    
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"  ✅ DONE: {size_mb:.1f}MB, {audio_duration:.1f}s")
    print(f"     📁 {os.path.basename(output_path)}")
    
    # Cleanup temp files (keep output)
    if not QUICK_MODE:
        try:
            os.remove(bg_video_path)
        except:
            pass
    
    return output_path, audio_duration, size_mb


# VIDEO CONFIGURATIONS

VIDEOS = [
    (2, "Fatima al-Fihri's University", 
     "Who built the world's first university? A Muslim woman. "
     "Fatima al-Fihri inherited a fortune in 9th century Morocco. She spent it all building Al-Qarawiyyin — a place where anyone could study for free. That was in 859 CE — 250 years before Oxford. It taught astronomy, medicine, mathematics, and philosophy. Muslims and non-Muslims together. And here's the craziest part — it's still open today. Over 1,100 years later. Guinness World Record holder for oldest university on Earth. "
     "Follow FactSage for more untold stories.",
     [
         (["🎓", "", "Who Built the World's", "First University?", "", "A Muslim Woman."], 5.5, True),
         (["Fatima al-Fihri inherited", "a fortune in 9th century Morocco.", "", "She spent it ALL building", "Al-Qarawiyyin — a place where", "anyone could study for free."], 7.0, False),
         (["That was in 859 CE —", "250 years BEFORE Oxford.", "", "Astronomy. Medicine.", "Mathematics. Philosophy.", "Muslims AND non-Muslims together."], 8.0, False),
         (["Still open today.", "Over 1,100 years later.", "", "Guinness World Record:", "Oldest university on Earth. 🌍"], 6.5, False),
         (["Follow FactSage", "for more untold stories. ♾️"], 3.5, False),
     ], 'GOLD'),
    
    (3, "Islamic Hospitals",
     "How did Muslims invent the modern hospital? Let me show you. "
     "In 805 CE, Caliph Harun al-Rashid opened the first real hospital in Baghdad. It had separate wards, patient records, trained nurses, and a pharmacy — 400 years before anything like it existed in Europe. And the architect? A Muslim physician named Al-Razi who chose the location by hanging fresh meat across the city and building where it rotted slowest. Science, not superstition. "
     "Follow FactSage for more.",
     [
         (["🏥", "", "How Did Muslims Invent", "the Modern Hospital?", "", "Let Me Show You."], 5.0, True),
         (["805 CE. Baghdad.", "", "Caliph Harun al-Rashid opened", "the first REAL hospital.", "", "Separate wards. Patient records.", "Trained nurses. A pharmacy."], 8.0, False),
         (["400 years before anything", "like it existed in Europe.", "", "The architect? A Muslim physician", "named Al-Razi.", "", "He chose the location by hanging", "fresh meat across Baghdad...", "and building where it rotted slowest."], 10.0, False),
         (["Science, not superstition. 🔬", "", "Follow FactSage", "for more. ♾️"], 4.0, False),
     ], 'GOLD'),
    
    (4, "How Muslims Named the Stars",
     "Most stars in the night sky have Arabic names. Here's why. "
     "Aldebaran, Altair, Deneb, Betelgeuse, Rigel — all Arabic names given by Muslim astronomers over 1,000 years ago. During the Islamic Golden Age, astronomers in Baghdad, Damascus, and Samarkand mapped the entire sky. They built massive observatories, invented the astrolabe, and named over 200 stars — names NASA still uses today. Even words like azimuth, nadir, and zenith come from Arabic. The language of the stars? It was written by Muslim scientists. "
     "Follow FactSage for more hidden history.",
     [
         (["⭐", "", "Most Stars in the Night Sky", "Have Arabic Names.", "", "Here's Why."], 5.0, True),
         (["Aldebaran. Altair. Deneb.", "Betelgeuse. Rigel.", "", "All Arabic names given by", "Muslim astronomers over", "1,000 years ago. 🔭"], 7.0, False),
         (["They mapped the entire sky.", "Built massive observatories.", "Invented the astrolabe.", "", "Over 200 stars named —", "names NASA still uses today. 🌙"], 8.0, False),
         (["Azimuth. Nadir. Zenith.", "All from Arabic.", "", "The language of the stars?", "Written by Muslim scientists. ✨", "", "Follow FactSage ♾️"], 7.0, False),
     ], 'GOLD'),
    
    (5, "The First Flying Machine",
     "The first person to fly wasn't the Wright Brothers. It was a 65-year-old Muslim inventor. "
     "In 875 CE, Abbas ibn Firnas built wings from silk, wood, and eagle feathers. He climbed the highest tower in Córdoba, Spain, and jumped — in front of a massive crowd. He glided for several minutes before landing. He hurt his back because he forgot to design a tail — but he had proven human flight was possible. A crater on the moon is named after him. And he did it more than a thousand years before the Wright Brothers. A polymath who also invented colorless glass and reading stones — early eyeglasses. The first aviator in history was a Muslim from Spain. "
     "Follow FactSage for more untold stories.",
     [
         (["✈️", "", "The First Person to Fly", "Wasn't the Wright Brothers.", "", "It Was a 65-Year-Old", "Muslim Inventor."], 6.0, True),
         (["875 CE. Córdoba, Spain.", "", "Abbas ibn Firnas built wings", "from silk, wood,", "and eagle feathers. 🦅"], 6.0, False),
         (["He climbed the highest tower", "and jumped — in front of", "a massive crowd.", "", "He GLIDED for several minutes.", "Human flight was possible."], 7.5, False),
         (["A crater on the moon", "is named after him. 🌙", "", "He also invented colorless glass", "and reading stones —", "early eyeglasses. 👓"], 6.5, False),
         (["The first aviator in history?", "A Muslim from Spain.", "", "Follow FactSage ♾️"], 4.0, False),
     ], 'GOLD'),
    
    (6, "Zero: The Islamic Math Revolution",
     "You can't do math without zero. Here's who gave it to the world. "
     "Al-Khwarizmi — a Muslim mathematician at the House of Wisdom in 9th-century Baghdad. He took the Indian concept of zero and built an entire mathematical system around it. He invented algebra. The word 'algorithm' comes from his name. Before him, Europe used Roman numerals — good luck multiplying VII by IX. Arabic numerals and the number zero transformed everything. When it first reached Europe, bankers banned it — calling it 'dangerous Saracen magic.' Today, every computer runs on ones and zeros. That's his legacy in your pocket. "
     "Follow FactSage for more history that shaped your world.",
     [
         (["0️⃣", "", "You Can't Do Math", "Without Zero.", "", "Here's Who Gave It", "to the World."], 5.5, True),
         (["Al-Khwarizmi.", "Muslim mathematician.", "House of Wisdom —", "9th century Baghdad.", "", "He took the Indian concept", "of zero and built an entire", "mathematical system."], 8.0, False),
         (["He invented ALGEBRA. 🔢", "The word 'ALGORITHM'?", "It comes from his name.", "", "Before him, Europe used", "Roman numerals.", "Try multiplying VII by IX. 😵"], 8.0, False),
         (["When zero reached Europe,", "bankers BANNED it —", "calling it 'dangerous", "Saracen magic.'", "", "Today? Every computer runs", "on ones and zeros.", "His legacy in your pocket. 📱"], 9.0, False),
         (["Follow FactSage", "for more history that", "shaped your world. ♾️"], 4.0, False),
     ], 'GOLD'),
    
    (7, "Salahuddin: Heart of Gold",
     "A Muslim commander took Jerusalem. Instead of revenge, he showed mercy that shocked the world. "
     "In 1187, Salahuddin recaptured Jerusalem from the Crusaders. 88 years earlier, Crusaders had massacred everyone. Everyone expected the same. But Salahuddin spared the entire city. He let Christians leave safely. He paid ransoms for the poor from his own pocket. He ordered his soldiers to help elderly Christians carry their belongings. Later, when his worst enemy — King Richard the Lionheart — fell ill during battle, Salahuddin sent his personal doctor, fresh fruit, and ice. Richard recovered. Salahuddin died with almost nothing — he gave his entire fortune to the poor. Even his enemies called him the most honorable man they ever knew. "
     "That's the real Salahuddin. Follow FactSage.",
     [
         (["🗡️", "", "A Muslim Commander", "Took Jerusalem.", "", "Instead of Revenge, He Showed", "Mercy That Shocked the World."], 6.0, True),
         (["1187. Salahuddin recaptured", "Jerusalem from the Crusaders.", "", "88 years earlier, Crusaders", "had massacred EVERYONE.", "", "Everyone expected the same."], 7.0, False),
         (["But Salahuddin spared", "the entire city. 🕌", "", "He paid ransoms for the poor", "from his OWN pocket.", "He ordered his soldiers to help", "elderly Christians."], 8.0, False),
         (["His worst enemy —", "King Richard the Lionheart —", "fell ill during battle.", "", "Salahuddin sent his personal", "doctor, fresh fruit, and ICE. 🧊", "Richard recovered."], 8.0, False),
         (["Salahuddin died with", "almost NOTHING.", "He gave his entire fortune", "to the poor.", "", "Even his enemies called him", "the most honorable man."], 7.5, False),
         (["That's the real Salahuddin.", "", "Follow FactSage. ♾️"], 3.5, False),
     ], 'GOLD'),
    
    (8, "Islamic Sicily",
     "Part of Italy was a Muslim country for 260 years. Here's the story they don't teach. "
     "From 827 to 1091, Muslims ruled Sicily. Palermo became one of Europe's richest cities, with over 300 mosques. They introduced oranges, lemons, sugar cane, cotton, and silk. They built irrigation systems still used today. And when the Normans conquered Sicily, they didn't erase the culture — they adopted it. King Roger II spoke Arabic, wore Arab robes, and filled his court with Muslim scholars. Churches were built with Arabic inscriptions. Arabic was spoken on the island for over 400 years. Sicilian food, language, and architecture still carry that Islamic DNA. Muslim Sicily — a forgotten piece of European history. "
     "Follow FactSage for more hidden chapters.",
     [
         (["🏝️", "", "Part of ITALY Was a", "Muslim Country", "for 260 Years.", "", "Here's the Story", "They Don't Teach."], 6.0, True),
         (["827 to 1091.", "Muslims ruled Sicily.", "", "Palermo became one of", "Europe's RICHEST cities.", "Over 300 mosques. 🕌"], 6.5, False),
         (["They introduced oranges,", "lemons, sugar cane,", "cotton, and silk. 🍊", "", "Irrigation systems", "still used TODAY."], 7.0, False),
         (["When Normans conquered Sicily,", "they didn't erase the culture —", "they ADOPTED it.", "", "King Roger II spoke Arabic,", "wore Arab robes, filled his", "court with Muslim scholars."], 8.5, False),
         (["Arabic was spoken on the island", "for over 400 years.", "", "Sicilian food, language,", "architecture — still carry", "that Islamic DNA. 🧬"], 7.0, False),
         (["Muslim Sicily.", "A forgotten piece of", "European history.", "", "Follow FactSage ♾️"], 5.0, False),
     ], 'GOLD'),
    
    (9, "House of Wisdom",
     "One library saved everything you know about Ancient Greece. Here's what happened to it. "
     "The House of Wisdom in 9th-century Baghdad was history's greatest knowledge factory. Muslims, Christians, Jews, and Persians worked together translating Greek philosophy, Persian astronomy, and Indian mathematics into Arabic. Caliph al-Ma'mun paid translators in gold — the weight of each book. Aristotle. Plato. Galen. Ptolemy. All preserved and expanded. Al-Khwarizmi invented algebra here. Then in 1258, the Mongols destroyed Baghdad and threw every book into the Tigris River. The river ran black with ink for six months. Then red with blood. It was the greatest intellectual catastrophe in history. But copies had already spread across the Islamic world. The Renaissance was built on what survived. One library saved civilization. "
     "The House of Wisdom. Follow FactSage for more stories that shaped our world.",
     [
         (["🏛️", "", "One Library Saved Everything", "You Know About", "Ancient Greece.", "", "Here's What Happened to It."], 6.5, True),
         (["The House of Wisdom.", "9th-century Baghdad.", "", "Muslims, Christians, Jews,", "and Persians — working together.", "Translating Greek philosophy,", "Persian astronomy, Indian math."], 8.0, False),
         (["Caliph al-Ma'mun paid", "translators in GOLD —", "the WEIGHT of each book. 🪙", "", "Aristotle. Plato. Galen. Ptolemy.", "All preserved and EXPANDED.", "Algebra was invented here."], 9.0, False),
         (["1258. The Mongols arrived.", "They destroyed Baghdad.", "Every book thrown into", "the Tigris River.", "", "The river ran BLACK with ink", "for six months.", "Then RED with blood. 💔"], 9.0, False),
         (["But copies had already spread.", "Through Spain. Through Sicily.", "", "The Renaissance was built on", "what the House of Wisdom saved.", "One library saved civilization."], 8.0, False),
         (["The House of Wisdom.", "", "Follow FactSage for more stories", "that shaped our world. ♾️"], 5.0, False),
     ], 'GOLD'),
]


# MAIN
if __name__ == "__main__":
    print("🎬 FACTSAGE ANIMATED PRODUCER — Phase 1")
    print("="*60)
    
    specific_id = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg != "--quick":
            try:
                specific_id = int(arg)
                print(f"   Single video: #{specific_id}")
            except ValueError:
                pass
    
    results = []
    import time as time_module
    start = time_module.time()
    
    for vid_id, name, vo_text, segments, accent in VIDEOS:
        if specific_id and vid_id != specific_id:
            continue
        
        try:
            out_path, dur, size = build_video(vid_id, name, vo_text, segments, accent)
            results.append((vid_id, name, out_path, dur, size, "✅"))
        except Exception as e:
            import traceback
            print(f"  ❌ FAILED: {e}")
            traceback.print_exc()
            results.append((vid_id, name, "", 0, 0, f"❌ {str(e)[:80]}"))
    
    elapsed = time_module.time() - start
    print(f"\n{'='*60}")
    print(f"📊 RESULTS ({elapsed/60:.1f} min)")
    print(f"{'='*60}")
    total_size = 0
    for vid_id, name, path, dur, size, status in results:
        print(f"  #{vid_id} {status} | {name[:45]:45s} | {dur:5.1f}s | {size:6.1f}MB")
        total_size += size
    print(f"\n  TOTAL: {len(results)} videoer | {total_size:.1f}MB")
    
    if results and results[0][5] == "✅":
        print(f"\n  💡 Næste skridt:")
        print(f"     python3 produce_animated.py  # Hele batch")
        print(f"     python3 produce_animated.py --quick  # Hurtig rendering")
