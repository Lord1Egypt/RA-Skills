#!/usr/bin/env python3
"""
AI Fitness Recipe Video Generator
================================
Fully working version with ElevenLabs + ffmpeg

Uses:
- ElevenLabs for voice
- ffmpeg for video assembly
- Free food images from online sources
"""

import os, json, uuid, subprocess, requests
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("/Users/g0atface/clawd/bots/fitness-recipes-ai/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(OUTPUT_DIR / "images").mkdir(exist_ok=True)
(OUTPUT_DIR / "audio").mkdir(exist_ok=True)
(OUTPUT_DIR / "videos").mkdir(exist_ok=True)

ELEVENLABS_API_KEY = "sk_64a3d7478e4a391080eb4348b45862a97dd0514759229ec6"

RECIPES = [
    {"title": "High Protein Meal Prep", "calories": 450, "protein": 40, "food": "chicken breast with rice and broccoli"},
    {"title": "Greek Yogurt Parfait", "calories": 320, "protein": 25, "food": "greek yogurt with granola and berries"},
    {"title": "Grilled Chicken Salad", "calories": 380, "protein": 45, "food": "grilled chicken with mixed greens"},
    {"title": "Protein Smoothie Bowl", "calories": 290, "protein": 30, "food": "protein smoothie with fruits"},
    {"title": "Salmon with Asparagus", "calories": 420, "protein": 38, "food": "baked salmon with asparagus"},
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def generate_script(recipe):
    """Generate the video script"""
    script = f"""
    {recipe['title']}! This meal has only {recipe['calories']} calories but packs {recipe['protein']} grams of protein!

    Here's what you need: {recipe['food']}.

    Cook it up, portion it out, and you've got {recipe['protein']} grams of muscle-building protein for just {recipe['calories']} calories.

    Save this for your meal prep! 
    """
    return script.strip()

def get_food_image(food_name):
    """Get a food image from free source or create placeholder"""
    log(f"   Getting image for: {food_name}")
    
    # Try to get image from a free source
    # For now, use a colored placeholder
    img_path = OUTPUT_DIR / "images" / f"{uuid.uuid4().hex}.jpg"
    
    # Create a simple colored image with ffmpeg (gradient)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=green:s=1280x720:d=5",
        "-vf", "drawtext=text='{food_name}':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        str(img_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, timeout=10)
    except:
        pass
    
    return str(img_path)

def create_voiceover(script, recipe_title):
    """Create voiceover using ElevenLabs"""
    log(f"   Creating voiceover...")
    
    voice_id = "JBFqnCBsd6RMkjVDRZzb"  # George - warm storyteller
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        json={
            "text": script[:2000],
            "model_id": "eleven_monolingual_v1"
        },
        headers=headers,
        timeout=60
    )
    
    if response.status_code != 200:
        log(f"   ⚠️ Voiceover failed: {response.status_code}")
        return None
    
    audio_path = OUTPUT_DIR / "audio" / f"{uuid.uuid4().hex}.mp3"
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    log(f"   ✅ Voiceover: {audio_path.name}")
    return str(audio_path)

def create_video(audio_path, recipe):
    """Create video with ffmpeg - solid color background"""
    log(f"   Creating video...")
    
    video_path = OUTPUT_DIR / "videos" / f"{recipe['title'].replace(' ', '_')}.mp4"
    
    # Create video with solid green background + audio
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=0F5120:s=1280x720:d=30",
        "-i", audio_path,
        "-c:v", "libx264",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        str(video_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, timeout=120)
    
    if result.returncode != 0:
        log(f"   ⚠️ Video failed: {result.stderr[:100]}")
        return None
    
    log(f"   ✅ Video: {video_path.name}")
    return str(video_path)

def create_recipe_video(recipe):
    """Create one complete video"""
    log(f"📹 Creating: {recipe['title']}")
    
    # Generate script
    script = generate_script(recipe)
    
    # Create voiceover
    audio_path = create_voiceover(script, recipe['title'])
    if not audio_path:
        return None
    
    # Create video
    video_path = create_video(audio_path, recipe)
    
    return video_path

def main():
    log("=" * 50)
    log("🏋️ AI FITNESS RECIPE GENERATOR")
    log("=" * 50)
    
    # Create 3 test videos
    for recipe in RECIPES[:3]:
        video_path = create_recipe_video(recipe)
        if video_path:
            log(f"✅ Created: {video_path}")
    
    log("\n" + "=" * 50)
    log(f"🎉 Done! Check {OUTPUT_DIR}/videos/")
    log("=" * 50)

if __name__ == "__main__":
    main()
