#!/usr/bin/env python3
"""
Feishu Voice Send - Send native Feishu voice messages.
Automatically selects TTS engine: MiniMax when quota available, fallback to Edge TTS when exhausted.

Usage: python3 send_feishu_voice.py "text to speak" [output.ogg]
"""
import subprocess
import av
import os
import re
import sys
import json
import tempfile

EDGE_TTS_SCRIPT = "/home/node/.openclaw/plugin-skills/edge-tts/scripts/tts-converter.js"
DEFAULT_VOICE = "Chinese (Mandarin)_Gentleman"
MINIMAX_TTS_MODEL = "speech-2.8-hd"


def check_minimax_quota() -> int:
    """Check MiniMax speech-hd weekly quota remaining. Returns remaining count, ≤0 means no quota."""
    try:
        result = subprocess.run(
            ['mmx', 'quota', 'show', '--output', 'json'],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode != 0:
            return 0

        data = json.loads(result.stdout)
        for cat in data.get('category_remains', []):
            if cat.get('category') == 'speech_generation':
                return cat.get('current_interval_total_count', 0) - cat.get('current_interval_usage_count', 0)
        return 0
    except Exception:
        return 0


def generate_minimax_tts(text: str) -> str:
    """Generate MP3 using MiniMax TTS. Returns file path."""
    tmp = tempfile.mktemp(suffix='.mp3')
    result = subprocess.run(
        ['mmx', 'speech', 'synthesize', '--text', text, '--out', tmp],
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"MiniMax TTS failed: {result.stderr}")
    if not os.path.exists(tmp):
        raise RuntimeError(f"MiniMax TTS output not found: {tmp}")
    return tmp


def generate_edge_tts(text: str) -> str:
    """Generate MP3 using Edge TTS. Returns file path."""
    # Filter TTS keywords to avoid loop
    text_clean = re.sub(r'\b(TTS|voice|text-to-speech)\b', '', text, flags=re.IGNORECASE).strip()
    if not text_clean:
        text_clean = "Voice message"

    result = subprocess.run(
        ['node', EDGE_TTS_SCRIPT, text_clean, '--voice', DEFAULT_VOICE],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(EDGE_TTS_SCRIPT),
        timeout=20
    )
    if result.returncode != 0:
        raise RuntimeError(f"Edge TTS failed: {result.stderr}")

    match = re.search(r'Audio saved to: (.+)', result.stdout)
    if not match:
        raise RuntimeError(f"Could not find output file in: {result.stdout}")
    return match.group(1).strip()


def convert_mp3_to_ogg(mp3_path: str, output_path: str = None) -> str:
    """Convert MP3 to Feishu-native Ogg/Opus format using PyAV."""
    if output_path is None:
        output_path = tempfile.mktemp(suffix='.ogg')

    out = av.open(output_path, 'w', format='ogg')
    stream = out.add_stream('libopus', rate=16000)
    inp = av.open(mp3_path)
    resampler = av.audio.resampler.AudioResampler(format='s16', layout='mono', rate=16000)

    try:
        for frame in inp.decode(audio=0):
            resampled = resampler.resample(frame)
            if resampled is not None:
                if not isinstance(resampled, list):
                    resampled = [resampled]
                for f in resampled:
                    for p in stream.encode(f):
                        out.mux(p)

        # Flush encoder
        resampled = resampler.resample(None)
        if resampled is not None:
            if not isinstance(resampled, list):
                resampled = [resampled]
            for f in resampled:
                for p in stream.encode(f):
                    out.mux(p)

        for p in stream.encode(None):
            out.mux(p)
    finally:
        out.close()
        inp.close()

    return output_path


def send_voice(text: str, voice: str = DEFAULT_VOICE) -> str:
    """Generate and send Feishu voice message. Unified TTS engine selection."""
    quota = check_minimax_quota()
    print(f"[TTS] MiniMax speech-hd quota remaining: {quota}", file=sys.stderr)

    if quota > 0:
        print(f"[TTS] Using MiniMax TTS (speech-2.8-hd)", file=sys.stderr)
        mp3_path = generate_minimax_tts(text)
    else:
        print(f"[TTS] MiniMax quota exhausted, falling back to Edge TTS", file=sys.stderr)
        mp3_path = generate_edge_tts(text)

    ogg_path = convert_mp3_to_ogg(mp3_path)
    return ogg_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    text = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        ogg_path = send_voice(text)
        if output:
            import shutil
            shutil.copy(ogg_path, output)
            print(f"OK: {output}")
        else:
            print(f"OK: {ogg_path}")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)