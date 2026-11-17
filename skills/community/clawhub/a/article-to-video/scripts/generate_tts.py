# -*- coding: utf-8 -*-
"""
Stage 2: TTS Generation
Converts narration text to speech with retry, fallback, and caching.

Features:
- Primary engine: edge-tts (free, high quality)
- Fallback chain: edge-tts → gTTS → pyttsx3
- Retry with exponential backoff on 429 rate limit
- Precise duration measurement via ffprobe
- Caching: skip regeneration if text hash matches
- Progress tracking for breakpoint resume

Usage:
    python generate_tts.py --scenes scenes.json --outdir ./audio --voice zh-CN-XiaoxiaoNeural
"""

import argparse
import asyncio
import json
import os
import sys
import time
import hashlib
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import TTS_CONFIG, CACHE_CONFIG, PATHS_CONFIG, VOICE_PROFILES, EFFECTS_CONFIG


# ============================================================
# Duration Measurement
# ============================================================

def measure_audio_duration(audio_path: str) -> float:
    """Measure audio duration using ffprobe, with ffmpeg -i fallback.

    Uses a multi-tier approach:
    1. ffprobe (most precise, if available)
    2. ffmpeg -i stderr parsing (works with bundled imageio-ffmpeg)
    3. File size estimation with corrected bitrate (48kbps for edge-tts)
    """
    import re

    # Tier 1: Try ffprobe
    try:
        result = subprocess.run(
            [PATHS_CONFIG["ffprobe"], "-v", "error",
             "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1",
             audio_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except (ValueError, subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Tier 2: Parse ffmpeg -i stderr output (works with imageio-ffmpeg)
    try:
        result = subprocess.run(
            [PATHS_CONFIG["ffmpeg"], "-i", audio_path],
            capture_output=True, text=True, timeout=10
        )
        match = re.search(r'Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)', result.stderr)
        if match:
            h, m, s = match.groups()
            return int(h) * 3600 + int(m) * 60 + float(s)
    except Exception:
        pass

    # Tier 3: Estimate from file size (edge-tts generates at ~48kbps)
    try:
        size = os.path.getsize(audio_path)
        # edge-tts MP3 at ~48kbps: 1 sec ≈ 6KB
        return round(size / 6000, 2)
    except OSError:
        return 0.0


# ============================================================
# Cache Management
# ============================================================

def get_cache_path(text_hash: str, cache_dir: str) -> str:
    """Get cache file path for a given text hash."""
    return os.path.join(cache_dir, f"{text_hash}.mp3")


def check_cache(text_hash: str, cache_dir: str) -> Optional[str]:
    """Check if cached audio exists for given text hash."""
    if not CACHE_CONFIG["enabled"]:
        return None
    cache_path = get_cache_path(text_hash, cache_dir)
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        return cache_path
    return None


def save_to_cache(src_path: str, text_hash: str, cache_dir: str):
    """Copy generated audio to cache."""
    if not CACHE_CONFIG["enabled"]:
        return
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = get_cache_path(text_hash, cache_dir)
    shutil.copy2(src_path, cache_path)


# ============================================================
# TTS Engines
# ============================================================

async def generate_edge_tts(text: str, output_path: str, voice: str,
                             rate: str = "+0%", pitch: str = "+0Hz") -> bool:
    """Generate speech using edge-tts."""
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 0


def generate_gtts(text: str, output_path: str, lang: str = "zh-cn") -> bool:
    """Generate speech using gTTS (Google Translate TTS)."""
    from gtts import gTTS
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 0


def generate_pyttsx3(text: str, output_path: str) -> bool:
    """Generate speech using pyttsx3 (offline, lower quality)."""
    import pyttsx3
    engine = pyttsx3.init()
    # Try to set Chinese voice if available
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 180)  # Speed
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return os.path.exists(output_path) and os.path.getsize(output_path) > 0


# ============================================================
# Retry Logic with Exponential Backoff
# ============================================================

async def generate_with_retry(text: str, output_path: str, voice: str,
                               rate: str, pitch: str,
                               max_retries: int, delay: float) -> Tuple[bool, str]:
    """
    Generate TTS with retry and fallback chain.
    Returns: (success, engine_used)
    """
    fallback_chain = TTS_CONFIG["fallback_chain"]

    for engine_name in fallback_chain:
        if engine_name == "edge-tts":
            for attempt in range(max_retries):
                try:
                    success = await generate_edge_tts(text, output_path, voice, rate, pitch)
                    if success:
                        return True, "edge-tts"
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "Too Many Requests" in error_msg:
                        wait_time = (2 ** attempt) + delay
                        print(f"    [edge-tts] 429 rate limited, "
                              f"waiting {wait_time:.1f}s (attempt {attempt+1}/{max_retries})")
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"    [edge-tts] Error: {error_msg}")
                        await asyncio.sleep(delay)
            print(f"    [edge-tts] Failed after {max_retries} retries, trying fallback...")

        elif engine_name == "gtts":
            try:
                lang = "zh-cn" if "zh" in voice else "en"
                success = generate_gtts(text, output_path, lang)
                if success:
                    print(f"    [gTTS] Success (fallback)")
                    return True, "gtts"
            except Exception as e:
                print(f"    [gTTS] Error: {e}")

        elif engine_name == "pyttsx3":
            try:
                success = generate_pyttsx3(text, output_path)
                if success:
                    print(f"    [pyttsx3] Success (offline fallback)")
                    return True, "pyttsx3"
            except Exception as e:
                print(f"    [pyttsx3] Error: {e}")

    return False, "none"


# ============================================================
# Progress / Resume
# ============================================================

def load_progress(progress_path: str) -> dict:
    """Load progress file for breakpoint resume."""
    if not CACHE_CONFIG["resume"]:
        return {}
    if os.path.exists(progress_path):
        with open(progress_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_progress(progress_path: str, progress: dict):
    """Save progress for breakpoint resume."""
    if not CACHE_CONFIG["resume"]:
        return
    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


# ============================================================
# Main Pipeline
# ============================================================

async def process_scene(scene: dict, output_dir: str, voice: str,
                        rate: str, pitch: str, delay: float,
                        max_retries: int, cache_dir: str) -> dict:
    """Process a single scene: generate TTS and measure duration."""
    index = scene["index"]
    text = scene["narration"]
    text_hash = scene.get("text_hash", hashlib.sha256(text.encode('utf-8')).hexdigest()[:16])

    # Output file: scene_001.mp3 (ASCII-only name for FFmpeg compatibility)
    audio_file = os.path.join(output_dir, f"scene_{index:03d}.mp3")

    # Check cache first
    cached = check_cache(text_hash, cache_dir)
    if cached:
        print(f"  Scene {index}: cache hit, copying...")
        shutil.copy2(cached, audio_file)
        duration = measure_audio_duration(audio_file)
        return {"index": index, "audio_file": audio_file, "duration": duration,
                "engine": "cached", "hash": text_hash}

    # Check if already generated (resume)
    if os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
        print(f"  Scene {index}: already exists, measuring duration...")
        duration = measure_audio_duration(audio_file)
        if duration > 0:
            return {"index": index, "audio_file": audio_file, "duration": duration,
                    "engine": "existing", "hash": text_hash}

    # Generate new TTS
    print(f"  Scene {index}: generating TTS ({len(text)} chars)...")
    success, engine = await generate_with_retry(
        text, audio_file, voice, rate, pitch, max_retries, delay
    )

    if not success:
        print(f"  Scene {index}: ALL TTS ENGINES FAILED!")
        return {"index": index, "audio_file": None, "duration": 0.0,
                "engine": "failed", "hash": text_hash}

    # Measure actual duration
    duration = measure_audio_duration(audio_file)
    print(f"  Scene {index}: done ({engine}, {duration:.1f}s)")

    # Save to cache
    save_to_cache(audio_file, text_hash, cache_dir)

    return {"index": index, "audio_file": audio_file, "duration": duration,
            "engine": engine, "hash": text_hash}


async def run_tts_pipeline(scenes_path: str, output_dir: str, voice: str,
                           rate: str = "+0%", pitch: str = "+0Hz",
                           profile_name: str = None):
    """Run the complete TTS pipeline."""
    # Load scenes
    with open(scenes_path, 'r', encoding='utf-8') as f:
        scenes_data = json.load(f)

    scenes = scenes_data["scenes"]
    total = len(scenes)

    print(f"TTS Pipeline: {total} scenes, voice={voice}")
    print(f"Output: {output_dir}")
    print()

    os.makedirs(output_dir, exist_ok=True)

    # Setup cache
    cache_dir = CACHE_CONFIG["cache_dir"]
    os.makedirs(cache_dir, exist_ok=True)

    # Setup progress
    progress_path = os.path.join(output_dir, "progress.json")
    progress = load_progress(progress_path)

    delay = TTS_CONFIG["delay_between_calls"]
    max_retries = TTS_CONFIG["max_retries"]

    results = []
    for i, scene in enumerate(scenes):
        print(f"[{i+1}/{total}] Scene {scene['index']}")

        result = await process_scene(
            scene, output_dir, voice, rate, pitch, delay, max_retries, cache_dir
        )
        results.append(result)

        # Save progress
        progress[str(scene["index"])] = {
            "done": result["audio_file"] is not None,
            "duration": result["duration"],
            "engine": result["engine"]
        }
        save_progress(progress_path, progress)

        # Anti-throttle delay between scenes
        if i < total - 1 and result["engine"] not in ("cached", "existing"):
            print(f"    Waiting {delay}s (anti-throttle)...")
            await asyncio.sleep(delay)

    # Extract profile params for timing.json
    narration_volume = EFFECTS_CONFIG["narration_volume"]
    bgm_style = None
    if profile_name and profile_name in VOICE_PROFILES:
        profile = VOICE_PROFILES[profile_name]
        narration_volume = profile.get("narration_volume", narration_volume)
        bgm_style = profile.get("bgm_style")

    # Save timing info (includes profile params for downstream stages)
    timing = {
        "scenes": results,
        "total_duration": sum(r["duration"] for r in results),
        "voice": voice,
        "rate": rate,
        "pitch": pitch,
        "profile": profile_name,
        "narration_volume": narration_volume,
        "bgm_style": bgm_style,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    timing_path = os.path.join(output_dir, "timing.json")
    with open(timing_path, 'w', encoding='utf-8') as f:
        json.dump(timing, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Total duration: {timing['total_duration']:.1f}s "
          f"({timing['total_duration']/60:.1f} min)")
    print(f"Timing saved to: {timing_path}")

    return timing


# ============================================================
# Main Entry Point
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio from scenes")
    parser.add_argument("--scenes", "-s", required=True, help="scenes.json path")
    parser.add_argument("--outdir", "-o", required=True, help="Output audio directory")
    parser.add_argument("--profile", default=None,
                       choices=list(VOICE_PROFILES.keys()),
                       help="Voice profile preset (overrides voice/rate/pitch). "
                            "Options: professional, casual, energetic, documentary, warm")
    parser.add_argument("--voice", "-v", default=TTS_CONFIG["voice"],
                       help="TTS voice (default: %(default)s)")
    parser.add_argument("--rate", "-r", default=TTS_CONFIG["rate"],
                       help="Speech rate (e.g. +10%%, -5%%)")
    parser.add_argument("--pitch", "-p", default=TTS_CONFIG["pitch"],
                       help="Pitch adjustment")
    args = parser.parse_args()

    # Apply voice profile if specified (overrides individual settings)
    voice = args.voice
    rate = args.rate
    pitch = args.pitch
    if args.profile:
        profile = VOICE_PROFILES[args.profile]
        voice = profile["voice"]
        rate = profile["rate"]
        pitch = profile["pitch"]
        print(f"Using voice profile: {args.profile} ({profile['label']})")
        print(f"  Voice: {voice}, Rate: {rate}, Pitch: {pitch}")

    asyncio.run(run_tts_pipeline(
        args.scenes, args.outdir, voice, rate, pitch,
        profile_name=args.profile
    ))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
