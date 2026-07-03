#!/usr/bin/env python3
"""
Karaoke-Style Subtitle Renderer — Whisper transcription + Pillow frame rendering.

Transcribes audio with Whisper, then generates transparent PNG frames with
word-by-word orange highlight (karaoke effect). Frames are overlayed onto the
video with FFmpeg.

Usage:
    # Step 1: Transcribe audio
    python3 render_subtitles.py transcribe --audio content_audio.wav --output subs.json

    # Step 2: Render subtitle frames
    python3 render_subtitles.py render \
        --timestamps subs.json \
        --fps 24 \
        --resolution 1280x720 \
        --output-dir subs_frames/

    # Step 3: Overlay onto video (manual FFmpeg)
    ffmpeg -i video.mp4 -framerate 24 -i subs_frames/frame_%05d.png \
        -filter_complex "overlay=0:0" -c:v libx264 -crf 20 output.mp4

The script auto-detects Whisper (openai-whisper or faster-whisper).
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


# ─── Subtitle Style Configuration ──────────────────────────────────────────

FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_SIZE = 44
SPOKEN_COLOR = (255, 107, 43, 255)     # Orange #FF6B2B
UNSPOKEN_COLOR = (255, 255, 255, 255)  # White
OUTLINE_COLOR = (0, 0, 0, 255)         # Black
OUTLINE_WIDTH = 2
BG_BAR_COLOR = (0, 0, 0, 160)          # Semi-transparent black
BG_BAR_HEIGHT = 80
BG_BAR_MARGIN_BOTTOM = 40

# Text correction mapping (add project-specific entries here)
CORRECTIONS = {}


def load_font():
    """Load the subtitle font, falling back to default if not found."""
    if Path(FONT_PATH).exists():
        return ImageFont.truetype(FONT_PATH, FONT_SIZE)
    print(f"Warning: {FONT_PATH} not found, using default font")
    return ImageFont.load_default()


def transcribe(audio_path, output_path, model_name="small", language="zh"):
    """
    Transcribe audio with Whisper and save word-level timestamps.

    Returns the parsed transcription data.
    """
    print(f"Transcribing {audio_path} with Whisper {model_name}...")

    try:
        import whisper
    except ImportError:
        print("Installing openai-whisper...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper"],
                       check=True)
        import whisper

    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language=language, word_timestamps=True)

    # Build structured output
    segments = []
    for seg in result.get("segments", []):
        words = []
        for w in seg.get("words", []):
            text = w.get("word", "").strip()
            # Apply corrections
            text = CORRECTIONS.get(text, text)
            words.append({
                "word": text,
                "start": w.get("start", 0),
                "end": w.get("end", 0),
            })
        segments.append({
            "text": seg.get("text", "").strip(),
            "start": seg.get("start", 0),
            "end": seg.get("end", 0),
            "words": words,
        })

    output = {
        "language": result.get("language", language),
        "duration": result.get("duration", 0),
        "segments": segments,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Transcription saved → {output_path} ({len(segments)} segments)")
    return output


def render_frames(timestamps_path, fps, resolution, output_dir):
    """
    Render transparent PNG frames from word-level timestamps.

    Each frame shows the current sentence with spoken words in orange
    and upcoming words in white.
    """
    with open(timestamps_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    duration = data.get("duration", 0)
    if not segments:
        print("Error: No segments in timestamps file")
        sys.exit(1)

    total_frames = int(duration * fps)
    width, height = resolution

    os.makedirs(output_dir, exist_ok=True)
    font = load_font()

    # Bar position
    bar_y = height - BG_BAR_HEIGHT - BG_BAR_MARGIN_BOTTOM
    text_y = bar_y + (BG_BAR_HEIGHT - FONT_SIZE) // 2

    for frame_idx in range(total_frames):
        frame_time = frame_idx / fps

        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Find current segment
        current_seg = None
        for seg in segments:
            if seg["start"] <= frame_time <= seg["end"]:
                current_seg = seg
                break

        if current_seg is None:
            # No subtitle for this frame — save transparent
            img.save(f"{output_dir}/frame_{frame_idx:05d}.png")
            continue

        # Draw background bar
        draw.rectangle(
            [(0, bar_y), (width, bar_y + BG_BAR_HEIGHT)],
            fill=BG_BAR_COLOR,
        )

        # Build text with word-level colors
        words = current_seg.get("words", [])
        full_text = current_seg.get("text", "")

        if not words:
            # No word-level data: render entire text in white
            bbox = draw.textbbox((0, 0), full_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            _draw_text_with_outline(draw, (x, text_y), full_text, UNSPOKEN_COLOR, font)
        else:
            # Render word by word with color
            x = 40  # left margin
            for w in words:
                word_text = w["word"]
                is_spoken = frame_time >= w["start"]
                color = SPOKEN_COLOR if is_spoken else UNSPOKEN_COLOR

                # Draw word with outline
                _draw_text_with_outline(draw, (x, text_y), word_text, color, font)

                # Advance x position (approximate)
                bbox = draw.textbbox((0, 0), word_text + " ", font=font)
                x += bbox[2] - bbox[0]

        img.save(f"{output_dir}/frame_{frame_idx:05d}.png")

        if (frame_idx + 1) % 100 == 0:
            print(f"  Rendered {frame_idx + 1}/{total_frames} subtitle frames")

    print(f"Rendered {total_frames} subtitle frames → {output_dir}/")


def _draw_text_with_outline(draw, position, text, fill_color, font):
    """Draw text with black outline for readability."""
    x, y = position
    # Draw outline (offset in 8 directions)
    outline = OUTLINE_COLOR
    for dx in range(-OUTLINE_WIDTH, OUTLINE_WIDTH + 1):
        for dy in range(-OUTLINE_WIDTH, OUTLINE_WIDTH + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=outline)
    # Draw main text
    draw.text((x, y), text, font=font, fill=fill_color)


def main():
    parser = argparse.ArgumentParser(description="Karaoke subtitle renderer")
    sub = parser.add_subparsers(dest="command", required=True)

    # transcribe subcommand
    t = sub.add_parser("transcribe", help="Transcribe audio with Whisper")
    t.add_argument("--audio", type=str, required=True, help="Audio file path")
    t.add_argument("--output", type=str, required=True, help="Output timestamps JSON")
    t.add_argument("--model", type=str, default="small", help="Whisper model size")
    t.add_argument("--language", type=str, default="zh", help="Audio language")

    # render subcommand
    r = sub.add_parser("render", help="Render subtitle PNG frames")
    r.add_argument("--timestamps", type=str, required=True, help="Timestamps JSON file")
    r.add_argument("--fps", type=int, default=24, help="Frame rate")
    r.add_argument("--resolution", type=str, default="1280x720", help="Resolution WxH")
    r.add_argument("--output-dir", type=str, required=True, help="Output directory for PNG frames")

    args = parser.parse_args()

    if args.command == "transcribe":
        transcribe(args.audio, args.output, args.model, args.language)
    elif args.command == "render":
        w, h = map(int, args.resolution.split("x"))
        render_frames(args.timestamps, args.fps, (w, h), args.output_dir)


if __name__ == "__main__":
    main()
