#!/usr/bin/env python3
"""Render a digital-human talking-head video from a still avatar + audio.

Engines (priority order):
  sadtalker  - LOCAL true lip-sync. Requires PyTorch + SadTalker repo.
               Set --sadtalker-home or env SADTALKER_HOME to the cloned repo.
  did        - CLOUD true lip-sync via D-ID. Requires DID_TOKEN (Bearer) OR
               DID_KEY + DID_SECRET (Basic auth) env vars. Works with local files
               (sent as base64 data URIs).
  heygen     - CLOUD true lip-sync via HeyGen. Requires HEYGEN_API_KEY plus
               public HEYGEN_IMAGE_URL + HEYGEN_AUDIO_URL env vars (HeyGen needs
               reachable URLs, not local files).
  fallback   - ffmpeg still-image + audio with subtle zoom. ALWAYS works, but has
               NO lip-sync. Use only when no true lip-sync engine is available.

Usage:
  python talking_head.py --image avatar.png --audio en.mp3 --out en_talk.mp4 --engine sadtalker
  python talking_head.py --image avatar.png --audio ar.mp3 --out ar_talk.mp4 --engine did
  python talking_head.py --image avatar.png --audio en.mp3 --out en_talk.mp4 --engine fallback
"""
import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request


def find_ffmpeg(explicit=None):
    if explicit:
        return explicit
    found = shutil.which("ffmpeg")
    if not found:
        # Common PASM Studio / local bundles
        candidate = os.path.join(
            os.environ.get("LOCALAPPDATA", ""), "PASMStudio", "bin", "ffmpeg.exe"
        )
        if os.path.exists(candidate):
            return candidate
        sys.exit("ffmpeg not found. Install ffmpeg and put it on PATH, or pass --ffmpeg.")
    return found


def run_cmd(cmd):
    print("[cmd]", " ".join(cmd))
    subprocess.run(cmd, check=True)


def b64_file(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def convert_to_wav(audio: str, ffmpeg: str) -> str:
    wav = os.path.splitext(audio)[0] + ".wav"
    if audio.lower().endswith(".wav"):
        return audio
    run_cmd(
        [
            ffmpeg,
            "-y",
            "-i",
            audio,
            "-ar",
            "16000",
            "-ac",
            "1",
            wav,
        ]
    )
    return wav


def run_sadtalker(image: str, audio: str, out: str, home: str, ffmpeg: str):
    if not home or not os.path.isdir(home):
        sys.exit(
            "SadTalker home not found. Clone + install it, then set --sadtalker-home or "
            "SADTALKER_HOME.\n"
            "  git clone https://github.com/vinthony/SadTalker.git\n"
            "  cd SadTalker && pip install -r requirements.txt\n"
            "  (also install: pip install gfpgan facexlib)\n"
            "See references/pipeline.md for full setup."
        )
    python = shutil.which("python") or sys.executable
    wav = convert_to_wav(audio, ffmpeg)
    result_dir = os.path.join(os.path.dirname(out) or ".", "sadtalker_out")
    os.makedirs(result_dir, exist_ok=True)
    cmd = [
        python,
        os.path.join(home, "inference.py"),
        "--driven_audio",
        wav,
        "--source_image",
        image,
        "--result_dir",
        result_dir,
        "--preprocess",
        "full",
        "--still",
        "--enhancer",
        "gfpgan",
    ]
    try:
        run_cmd(cmd)
    except subprocess.CalledProcessError as exc:
        sys.exit(f"SadTalker failed (exit {exc.returncode}). See references/pipeline.md.")

    # SadTalker writes <result_dir>/<timestamp>/<audio_stem>.mp4
    mp4s = []
    for root, _dirs, files in os.walk(result_dir):
        for fn in files:
            if fn.endswith(".mp4"):
                mp4s.append(os.path.join(root, fn))
    if not mp4s:
        sys.exit("SadTalker produced no mp4. Check its output above.")
    newest = max(mp4s, key=os.path.getmtime)
    shutil.copy(newest, out)
    print(f"[talking_head] sadtalker -> {out} (true lip-sync)")


def _d-id_headers():
    token = os.environ.get("DID_TOKEN")
    key = os.environ.get("DID_KEY")
    secret = os.environ.get("DID_SECRET")
    if token:
        return {"Authorization": f"Bearer {token}"}
    if key and secret:
        basic = base64.b64encode(f"{key}:{secret}".encode()).decode()
        return {"Authorization": f"Basic {basic}"}
    sys.exit("D-ID requires DID_TOKEN (Bearer) OR DID_KEY+DID_SECRET (Basic) env vars.")


def run_did(image: str, audio: str, out: str):
    headers = {**_d-id_headers(), "Content-Type": "application/json"}
    payload = {
        "source_url": f"data:image/png;base64,{b64_file(image)}",
        "script": {
            "type": "audio",
            "audio": f"data:audio/mpeg;base64,{b64_file(audio)}",
        },
        "config": {"fluent": True, "result_format": "mp4"},
    }
    req = urllib.request.Request(
        "https://api.d-id.com/talks",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        talk = json.load(resp)
    talk_id = talk["id"]
    print(f"[talking_head] D-ID talk {talk_id} created, waiting...")
    while True:
        req2 = urllib.request.Request(
            f"https://api.d-id.com/talks/{talk_id}", headers=headers
        )
        with urllib.request.urlopen(req2, timeout=60) as resp:
            st = json.load(resp)
        if st.get("status") == "done":
            break
        if st.get("status") == "error":
            sys.exit(f"D-ID error: {st}")
        time.sleep(5)
    result_url = st["result_url"]
    urllib.request.urlretrieve(result_url, out)
    print(f"[talking_head] did -> {out} (true lip-sync)")


def run_heygen(image: str, audio: str, out: str):
    api_key = os.environ.get("HEYGEN_API_KEY")
    img_url = os.environ.get("HEYGEN_IMAGE_URL")
    aud_url = os.environ.get("HEYGEN_AUDIO_URL")
    if not (api_key and img_url and aud_url):
        sys.exit(
            "HeyGen requires HEYGEN_API_KEY + HEYGEN_IMAGE_URL + HEYGEN_AUDIO_URL "
            "(HeyGen needs public URLs, not local files). Host the image and audio "
            "first, then re-run. See references/pipeline.md."
        )
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    payload = {
        "video_inputs": [
            {
                "character": {"type": "talking_photo", "image_url": img_url},
                "voice": {"type": "audio", "audio_url": aud_url},
            }
        ],
        "dimension": {"width": 1280, "height": 720},
    }
    req = urllib.request.Request(
        "https://api.heygen.com/v2/video/talking_photo",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    video_id = data["data"]["video_id"]
    print(f"[talking_head] HeyGen video {video_id} created, waiting...")
    while True:
        req2 = urllib.request.Request(
            f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
            headers=headers,
        )
        with urllib.request.urlopen(req2, timeout=60) as resp:
            st = json.load(resp)
        if st["data"]["status"] == "completed":
            break
        if st["data"]["status"] == "failed":
            sys.exit(f"HeyGen failed: {st}")
        time.sleep(8)
    urllib.request.urlretrieve(st["data"]["video_url"], out)
    print(f"[talking_head] heygen -> {out} (true lip-sync)")


def run_fallback(image: str, audio: str, out: str, ffmpeg: str):
    dur = get_duration(audio, ffmpeg) or 10
    vf = (
        "zoompan=z='min(zoom+0.0008,1.06)':d=1:s=1280x720:fps=25,scale=1280:720,"
        "setsar=1"
    )
    run_cmd(
        [
            ffmpeg,
            "-y",
            "-loop",
            "1",
            "-i",
            image,
            "-i",
            audio,
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-pix_fmt",
            "yuv420p",
            "-t",
            str(dur),
            out,
        ]
    )
    print(
        "[talking_head] fallback -> still image + audio (NO lip-sync). "
        "Upgrade to sadtalker/did for true mouth sync."
    )


def get_duration(path: str, ffmpeg: str):
    ffprobe = shutil.which("ffprobe") or os.path.join(
        os.path.dirname(ffmpeg), "ffprobe"
    )
    if not ffprobe or not os.path.exists(ffprobe):
        return None
    try:
        out = subprocess.check_output(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            stderr=subprocess.DEVNULL,
        )
        return float(out.strip())
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description="Avatar + audio -> talking-head video")
    ap.add_argument("--image", required=True, help="Avatar still image (png/jpg)")
    ap.add_argument("--audio", required=True, help="Driving audio (mp3/wav)")
    ap.add_argument("--out", required=True, help="Output video (.mp4)")
    ap.add_argument(
        "--engine",
        default="sadtalker",
        choices=["sadtalker", "did", "heygen", "fallback"],
    )
    ap.add_argument("--sadtalker-home", default=None, help="Path to cloned SadTalker repo")
    ap.add_argument("--ffmpeg", default=None, help="Path to ffmpeg binary")
    args = ap.parse_args()

    ffmpeg = find_ffmpeg(args.ffmpeg)
    home = args.sadtalker_home or os.environ.get("SADTALKER_HOME")

    if args.engine == "sadtalker":
        run_sadtalker(args.image, args.audio, args.out, home, ffmpeg)
    elif args.engine == "did":
        run_did(args.image, args.audio, args.out)
    elif args.engine == "heygen":
        run_heygen(args.image, args.audio, args.out)
    else:
        run_fallback(args.image, args.audio, args.out, ffmpeg)


if __name__ == "__main__":
    main()
