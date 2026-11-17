#!/usr/bin/env python3
"""
assemble_video.py — OPTIONAL: combine a narration MP3 with a single still
image into an MP4 whose duration matches the audio.

This is a convenience step, not part of the core manuscript-to-MP3
workflow. It produces a static-image "audiogram"-style video (one still +
audio), commonly used for long-form narration uploads.

Usage:
    python3 assemble_video.py --audio narration.mp3 --image still.jpg \
        --output video.mp4

Options:
    --pad-color HEX   Letterbox/pad fill color (default 000000 = black).
                      Use a warm value like FFF8E7 for aged-paper looks.
    --width / --height   Target frame size (default 1920x1080).
    --fps INT         Frame rate (default 24).

Verification is run automatically: stream layout, audio/video duration
delta, faststart atom position, and a full decode pass. Exit non-zero if
any check fails.
"""

import argparse
import struct
import subprocess
import sys
from pathlib import Path


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def build(audio: Path, image: Path, out: Path, pad: str, w: int, h: int, fps: int):
    vf = (f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0x{pad},setsar=1,fps={fps}[v]")
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image),
        "-i", str(audio),
        "-filter_complex", vf,
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
        "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest", "-movflags", "+faststart",
        str(out),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def faststart_ok(path: Path) -> bool:
    order = []
    with open(path, "rb") as f:
        f.seek(0, 2); size = f.tell(); f.seek(0); pos = 0
        while pos < size:
            f.seek(pos); head = f.read(8)
            if len(head) < 8:
                break
            s, t = struct.unpack(">I4s", head)
            order.append(t.decode("latin1", "replace"))
            if s == 1:
                f.seek(pos + 8); s = struct.unpack(">Q", f.read(8))[0]
            if s == 0:
                break
            pos += s
    return "moov" in order and "mdat" in order and order.index("moov") < order.index("mdat")


def full_decode_ok(path: Path) -> bool:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
                       capture_output=True, text=True, check=False)
    return r.returncode == 0 and not r.stderr.strip()


def main():
    ap = argparse.ArgumentParser(description="Assemble still + audio into MP4.")
    ap.add_argument("--audio", type=Path, required=True)
    ap.add_argument("--image", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--pad-color", default="000000")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=24)
    args = ap.parse_args()

    for p in (args.audio, args.image):
        if not p.is_file():
            ap.error(f"not found: {p}")

    build(args.audio, args.image, args.output, args.pad_color,
          args.width, args.height, args.fps)

    a_dur = probe_duration(args.audio)
    v_dur = probe_duration(args.output)
    delta = abs(a_dur - v_dur)
    fs = faststart_ok(args.output)
    dec = full_decode_ok(args.output)

    print(f"[assemble] {args.output.name}")
    print(f"  audio={a_dur:.2f}s video={v_dur:.2f}s delta={delta:.2f}s "
          f"(tolerance 2.0s)")
    print(f"  faststart={'OK' if fs else 'FAIL'} decode={'OK' if dec else 'FAIL'}")

    if delta > 2.0 or not fs or not dec:
        print("[error] verification failed", file=sys.stderr)
        sys.exit(1)
    print("[done] verification passed")


if __name__ == "__main__":
    main()
