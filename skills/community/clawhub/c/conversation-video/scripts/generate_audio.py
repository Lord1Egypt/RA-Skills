#!/usr/bin/env python3
"""
generate_audio.py — Multi-voice TTS audio generator for conversation videos.

Reads a JSON manifest and produces a single concatenated audio file with
per-speaker voice assignment. Designed for Supertonic TTS.

Usage:
    python generate_audio.py manifest.json output.wav

Manifest format:
    [
      {"speaker": "Alice", "text": "Hello there", "voice": "M1", "speed": 1.0},
      {"speaker": "Bob",   "text": "Hi Alice",    "voice": "M2", "speed": 0.95}
    ]

Fields:
    - speaker:  display name (used for labels, not TTS)
    - text:     text to synthesize
    - voice:    Supertonic voice name (e.g. M1, M2, M3, M4, M5, F1, F2)
    - speed:    optional playback speed factor (default 1.0)
"""

import json
import os
import sys
import subprocess
import tempfile


def load_tts():
    """Import Supertonic TTS, probing common install paths."""
    try:
        from supertonic import TTS
        return TTS
    except ImportError:
        # Probe common venv paths
        candidates = [
            os.path.expanduser("~/.openclaw/workspace/.browser-use-venv/lib/python3.14/site-packages"),
            os.path.expanduser("~/.openclaw/workspace/.browser-use-venv/lib/python3.13/site-packages"),
            os.path.expanduser("~/.openclaw/workspace/.browser-use-venv/lib/python3.12/site-packages"),
        ]
        for c in candidates:
            if c not in sys.path and os.path.isdir(c):
                sys.path.insert(0, c)
        try:
            from supertonic import TTS
            return TTS
        except ImportError:
            print("ERROR: supertonic TTS not found. Install with: pip install supertonic-tts", file=sys.stderr)
            sys.exit(1)


def find_ffmpeg():
    """Find a usable ffmpeg binary."""
    for candidate in ["/usr/lib/jellyfin-ffmpeg/ffmpeg", "ffmpeg"]:
        try:
            subprocess.run([candidate, "-version"], capture_output=True, check=True)
            return candidate
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    print("ERROR: ffmpeg not found. Install ffmpeg first.", file=sys.stderr)
    sys.exit(1)


def synthesize_segment(tts, voice_style, text, speed, out_path):
    """Synthesize one segment to a WAV file."""
    wav, _ = tts.synthesize(
        text=text,
        lang="en",
        voice_style=voice_style,
        total_steps=10,
        speed=speed,
        silence_duration=0.3,
    )
    tts.save_audio(wav, out_path)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <manifest.json> <output.wav>", file=sys.stderr)
        sys.exit(1)

    manifest_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(manifest_path) as f:
        segments = json.load(f)

    if not segments:
        print("ERROR: manifest is empty", file=sys.stderr)
        sys.exit(1)

    TTS = load_tts()
    tts = TTS(auto_download=True)
    ffmpeg = find_ffmpeg()

    # Cache voice styles
    voice_cache = {}
    def get_voice(name):
        if name not in voice_cache:
            voice_cache[name] = tts.get_voice_style(voice_name=name)
        return voice_cache[name]

    work_dir = tempfile.mkdtemp(prefix="conv_audio_")
    wav_files = []

    for i, seg in enumerate(segments):
        text = seg["text"]
        voice_name = seg.get("voice", "M1")
        speed = seg.get("speed", 1.0)
        speaker = seg.get("speaker", "SPEAKER")

        wav_path = os.path.join(work_dir, f"seg_{i:03d}.wav")
        print(f"[{i+1}/{len(segments)}] ({speaker}) {text[:55]}...")

        try:
            voice = get_voice(voice_name)
            synthesize_segment(tts, voice, text, speed, wav_path)
            wav_files.append(wav_path)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    # Concatenate via ffmpeg
    concat_file = os.path.join(work_dir, "concat.txt")
    with open(concat_file, "w") as f:
        for wf in wav_files:
            f.write(f"file '{wf}'\n")

    cmd = [
        ffmpeg, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file, "-c", "copy", output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    # Report duration
    result = subprocess.run(
        [ffmpeg, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", output_path],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    print(f"\nDone! {output_path}")
    print(f"Duration: {duration:.1f}s ({duration/60:.1f} min)")

    # Also emit a timing manifest for video sync
    timing_manifest = os.path.splitext(output_path)[0] + "_timings.json"
    # Build cumulative timings from segment durations
    timings = []
    offset = 0.0
    for i, seg in enumerate(segments):
        result = subprocess.run(
            [ffmpeg, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", wav_files[i]],
            capture_output=True, text=True
        )
        seg_dur = float(result.stdout.strip())
        timings.append({
            "speaker": seg.get("speaker", "SPEAKER"),
            "text": seg["text"],
            "start": round(offset, 3),
            "end": round(offset + seg_dur, 3),
            "duration": round(seg_dur, 3),
            "voice": seg.get("voice", "M1"),
            "speed": seg.get("speed", 1.0),
            "align": seg.get("align", "center"),
        })
        offset += seg_dur

    with open(timing_manifest, "w") as f:
        json.dump(timings, f, indent=2)
    print(f"Timing manifest: {timing_manifest}")


if __name__ == "__main__":
    main()
