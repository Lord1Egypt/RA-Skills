#!/usr/bin/env python3
"""
MiniMax Multimodal API Toolkit — Python (cross-platform)

Supports: Image generation (t2i, i2i), TTS, Music, Video generation.
Requires: MINIMAX_API_KEY env var. Optional: MINIMAX_API_HOST (default: https://api.minimaxi.com).
No third-party dependencies — uses only Python standard library.
"""

from __future__ import print_function

import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import urllib.error
import uuid

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_API_HOST = "https://api.minimaxi.com"
DEFAULT_OUTPUT_DIR = "minimax-output"


def _get_config():
    """Return (api_key, api_host, api_base). Raises if key is missing."""
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        raise RuntimeError("MINIMAX_API_KEY environment variable is not set")
    api_host = os.environ.get("MINIMAX_API_HOST", DEFAULT_API_HOST).rstrip("/")
    return api_key, api_host, api_host + "/v1"


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _api_request(endpoint, method="GET", body=None, timeout=120, query=None):
    """Make an API request and return the parsed JSON response."""
    api_key, _, api_base = _get_config()
    url = api_base + "/" + endpoint
    if query:
        sep = "&" if "?" in url else "?"
        url += sep + urllib.parse.urlencode(query)

    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + api_key)
    if body is not None:
        req.add_header("Content-Type", "application/json; charset=utf-8")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        try:
            err_body = exc.read().decode("utf-8")
            err_json = json.loads(err_body)
            br = err_json.get("base_resp", {})
            raise RuntimeError(
                "API [{}] {} : {}".format(
                    br.get("status_code", exc.code),
                    br.get("status_msg", ""),
                    err_body[:200],
                )
            )
        except Exception:
            raise RuntimeError("HTTP {} — {}".format(exc.code, str(exc)))

    result = json.loads(raw)

    br = result.get("base_resp")
    if br and int(br.get("status_code", 0)) != 0:
        raise RuntimeError("API [{}]: {}".format(br["status_code"], br.get("status_msg", "")))
    return result


def _download_url(url, output_path):
    """Download a URL to a local file."""
    _ensure_dir(output_path)
    urllib.request.urlretrieve(url, output_path)
    return output_path


def _ensure_dir(filepath):
    """Create parent directory for filepath if needed."""
    d = os.path.dirname(filepath)
    if d:
        os.makedirs(d, exist_ok=True)


def _hex_to_file(hex_string, output_path):
    """Decode a hex string to binary and write to file."""
    _ensure_dir(output_path)
    with open(output_path, "wb") as f:
        f.write(bytes.fromhex(hex_string))
    return output_path


def _upload_file(filepath, purpose="image"):
    """Upload a file and return file_id."""
    api_key, _, api_base = _get_config()
    url = api_base + "/files/upload"

    import mimetypes
    mime = mimetypes.guess_type(filepath)[0] or "application/octet-stream"

    boundary = uuid.uuid4().hex
    with open(filepath, "rb") as f:
        file_data = f.read()
    filename = os.path.basename(filepath)

    body_parts = []
    body_parts.append(("--" + boundary).encode())
    body_parts.append(
        ('Content-Disposition: form-data; name="file"; filename="{}"'.format(filename)).encode()
    )
    body_parts.append(("Content-Type: {}".format(mime)).encode())
    body_parts.append(b"")
    body_parts.append(file_data)
    body_parts.append(("--" + boundary).encode())
    body_parts.append(b'Content-Disposition: form-data; name="purpose"')
    body_parts.append(b"")
    body_parts.append(purpose.encode())
    body_parts.append(("--" + boundary + "--").encode())
    body_parts.append(b"")

    body = b"\r\n".join(body_parts)
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", "Bearer " + api_key)
    req.add_header("Content-Type", "multipart/form-data; boundary=" + boundary)

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    br = result.get("base_resp")
    if br and int(br.get("status_code", 0)) != 0:
        raise RuntimeError("Upload [{}]: {}".format(br["status_code"], br.get("status_msg", "")))
    return result["data"]


# ---------------------------------------------------------------------------
# Media duration helper
# ---------------------------------------------------------------------------

def get_duration_ms(filepath):
    """Get duration of a media file in milliseconds using ffprobe if available, else raise."""
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", filepath],
            stderr=subprocess.STDOUT,
        )
        return int(float(out.strip()) * 1000)
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        raise RuntimeError("ffprobe not available or file is not a valid media file")


# ---------------------------------------------------------------------------
# TTS — POST /v1/t2a_v2
# ---------------------------------------------------------------------------

def generate_tts(
    text,
    output=None,
    voice_id="female-shaonv",
    emotion="",
    model="speech-2.8-hd",
    speed=1.0,
    volume=1.0,
    pitch=0,
    audio_format="mp3",
    sample_rate=32000,
):
    """Synthesize speech from text using MiniMax TTS.

    Args:
        text: Text to synthesize (up to 10,000 chars).
        output: Output file path (e.g. 'minimax-output/hello.mp3'). If None, returns hex string.
        voice_id: Voice ID (e.g. 'female-shaonv', 'male-qn-qingse', 'presenter_male').
        emotion: Emotion tag ('happy', 'sad', 'angry', 'fearful', 'surprised', 'calm', 'whisper', ''). Empty = auto.
        model: TTS model ('speech-2.8-hd', 'speech-2.8-turbo', 'speech-02-hd', 'speech-02-turbo').
        speed: Speech speed (0.5 - 2.0, default 1.0).
        volume: Volume (0.1 - 10.0, default 1.0).
        pitch: Pitch shift (-12 to 12, default 0).
        audio_format: Output format ('mp3', 'pcm', 'flac', 'wav').
        sample_rate: Sample rate (16000, 24000, 32000).

    Returns:
        If output is set: the output file path.
        If output is None: dict with 'hex' key.
    """
    voice_setting = {"voice_id": voice_id, "speed": speed, "vol": volume, "pitch": pitch}
    if emotion:
        voice_setting["emotion"] = emotion

    body = {
        "model": model,
        "text": text,
        "voice_setting": voice_setting,
        "audio_setting": {
            "sample_rate": sample_rate,
            "bitrate": 128000,
            "format": audio_format,
            "channel": 1,
        },
        "stream": False,
        "subtitle_enable": False,
        "output_format": "hex",
    }

    print("Synthesizing ({}): {}...".format(model, text[:60]))
    result = _api_request("t2a_v2", method="POST", body=body, timeout=120)

    audio_hex = result.get("data", {}).get("audio", "")
    if not audio_hex:
        raise RuntimeError("No audio data returned from TTS API")

    if output:
        path = _hex_to_file(audio_hex, output)
        print("  Saved: {} ({} bytes)".format(path, len(audio_hex) // 2))
        return path
    return {"hex": audio_hex}


# ---------------------------------------------------------------------------
# Music — POST /v1/music_generation (synchronous with long timeout)
# ---------------------------------------------------------------------------

def generate_music(
    prompt,
    output=None,
    lyrics="",
    instrumental=False,
    model="music-2.5",
    timeout=300,
):
    """Generate music using MiniMax Music API.

    Args:
        prompt: Music description (style, mood, instruments).
        output: Output file path. If None, returns dict with 'url'.
        lyrics: Song lyrics in structured format ('[verse]\\n...'). Required unless instrumental.
        instrumental: If True, generates background music without vocals.
        model: Music model ('music-2.5').
        timeout: HTTP timeout in seconds (music generation is slow, 30-300s).

    Returns:
        If output is set: dict with 'path' and 'url'.
        If output is None: dict with 'url'.
    """
    if instrumental:
        body = {
            "model": model,
            "prompt": prompt + ", pure music, no lyrics",
            "lyrics": "[intro]\n[outro]",
            "output_format": "url",
            "stream": False,
        }
    elif lyrics:
        body = {
            "model": model,
            "prompt": prompt,
            "lyrics": lyrics,
            "output_format": "url",
            "stream": False,
        }
    else:
        raise RuntimeError("Lyrics required for music generation (use instrumental=True for BGM)")

    print("Generating music ({}, timeout={}s)...".format(model, timeout))
    result = _api_request("music_generation", method="POST", body=body, timeout=timeout)

    audio_url = result.get("data", {}).get("audio", "")
    if not audio_url:
        raise RuntimeError("No audio URL returned from music API")

    extra = result.get("extra_info", {})
    dur_s = round(extra.get("music_duration", 0) / 1000, 1)
    size_mb = round(extra.get("music_size", 0) / 1048576, 2)
    print("  Duration: {}s, Size: {}MB".format(dur_s, size_mb))

    if output:
        path = _download_url(audio_url, output)
        print("  Saved: {}".format(path))
        return {"path": path, "url": audio_url}
    return {"url": audio_url}


# ---------------------------------------------------------------------------
# Image Generation — POST /v1/image_generation
# ---------------------------------------------------------------------------

def generate_image(
    prompt,
    output=None,
    aspect_ratio="1:1",
    count=1,
    model="image-01",
    prompt_optimizer=False,
    seed=-1,
):
    """Generate images from text prompts using MiniMax Image API.

    Args:
        prompt: Text description of the image.
        output: Output file path. If None, returns list of dicts with 'url'.
        aspect_ratio: Image aspect ratio ('1:1', '16:9', '4:3', '3:2', '2:3', '3:4', '9:16', '21:9').
        count: Number of images to generate (1-4).
        model: Image model ('image-01').
        prompt_optimizer: Enable automatic prompt optimization.
        seed: Random seed (-1 for random).

    Returns:
        If output is set: list of dicts with 'path' and 'url'.
        If output is None: list of dicts with 'url'.
    """
    body = {
        "model": model,
        "request_id": uuid.uuid4().hex,
        "prompt": prompt,
    }
    if prompt_optimizer:
        body["prompt_optimizer"] = True
    if seed >= 0:
        body["seed"] = seed
    if count > 1:
        body["n"] = count

    print("Generating image ({})...".format(model))
    result = _api_request("image_generation", method="POST", body=body, timeout=120)

    urls = result.get("data", {}).get("image_urls", [])
    if not urls:
        raise RuntimeError("No images returned from image API")

    outputs = []
    for i, img_url in enumerate(urls):
        if output:
            base, ext = os.path.splitext(output)
            if not ext:
                ext = ".png"
            suffix = "_{}".format(i + 1) if len(urls) > 1 else ""
            path = _download_url(img_url, base + suffix + ext)
            print("  Saved: {}".format(path))
            outputs.append({"path": path, "url": img_url})
        else:
            outputs.append({"url": img_url})
            print("  URL: {}".format(img_url))
    return outputs


def image_to_image(
    prompt,
    image_path,
    output=None,
    aspect_ratio="1:1",
    count=1,
    model="image-01",
    prompt_optimizer=False,
    seed=-1,
):
    """Generate images from a reference image using MiniMax Image-to-Image API.

    Args:
        prompt: Text description for the new image.
        image_path: Path or URL to the reference image.
        output: Output file path. If None, returns list of dicts with 'url'.
        aspect_ratio: Image aspect ratio.
        count: Number of images to generate (1-4).
        model: Image model ('image-01').
        prompt_optimizer: Enable automatic prompt optimization.
        seed: Random seed (-1 for random).

    Returns:
        If output is set: list of dicts with 'path' and 'url'.
        If output is None: list of dicts with 'url'.
    """
    # If image_path is a URL, use directly; otherwise base64 encode
    if image_path.startswith("http://") or image_path.startswith("https://"):
        image_file = image_path
    else:
        import base64
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        image_file = "data:image/jpeg;base64," + b64

    body = {
        "model": model,
        "request_id": uuid.uuid4().hex,
        "prompt": prompt,
        "image_file": image_file,
    }
    if prompt_optimizer:
        body["prompt_optimizer"] = True
    if seed >= 0:
        body["seed"] = seed
    if count > 1:
        body["n"] = count

    print("Generating image-to-image ({})...".format(model))
    result = _api_request("image_generation", method="POST", body=body, timeout=120)

    urls = result.get("data", {}).get("image_urls", [])
    if not urls:
        raise RuntimeError("No images returned from image-to-image API")

    outputs = []
    for i, img_url in enumerate(urls):
        if output:
            base, ext = os.path.splitext(output)
            if not ext:
                ext = ".png"
            suffix = "_{}".format(i + 1) if len(urls) > 1 else ""
            path = _download_url(img_url, base + suffix + ext)
            print("  Saved: {}".format(path))
            outputs.append({"path": path, "url": img_url})
        else:
            outputs.append({"url": img_url})
            print("  URL: {}".format(img_url))
    return outputs


# ---------------------------------------------------------------------------
# Video Generation — POST /v1/video_generation (async) + polling
# ---------------------------------------------------------------------------

def _wait_video_task(task_id, interval=10, max_wait=600):
    """Poll video generation task until completion."""
    api_key, _, api_base = _get_config()
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(interval)
        elapsed += interval
        url = api_base + "/query/video_generation?task_id=" + urllib.parse.quote(task_id)
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", "Bearer " + api_key)
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        status = result.get("status", "")
        print("  [{}s] Status: {}".format(elapsed, status))
        if status == "Success":
            return result
        if status == "Failed":
            raise RuntimeError("Video generation task failed")
    raise RuntimeError("Video generation timed out after {}s".format(max_wait))


def _get_video_url(file_id):
    """Retrieve download URL for a video file_id."""
    result = _api_request("files/retrieve", query={"file_id": file_id}, timeout=30)
    return result.get("file", {}).get("download_url", "")


def generate_video(
    prompt,
    output=None,
    mode="t2v",
    first_frame="",
    last_frame="",
    subject_image="",
    model="MiniMax-Hailuo-2.3",
    max_wait=600,
):
    """Generate video using MiniMax Video API.

    Args:
        prompt: Video description (subject + scene + movement + camera + aesthetic).
        output: Output file path (.mp4). If None, returns dict with 'url'.
        mode: Generation mode — 't2v' (text-to-video), 'i2v' (image-to-video),
              'sef' (start-end frame), 'ref' (subject reference).
        first_frame: Path to first frame image (for i2v and sef modes).
        last_frame: Path to last frame image (for sef mode).
        subject_image: Path to subject reference image (for ref mode).
        model: Video model ('MiniMax-Hailuo-2.3', 'MiniMax-Hailuo-2.3-Fast', 'MiniMax-Hailuo-02').
        max_wait: Max polling wait time in seconds.

    Returns:
        If output is set: dict with 'path' and 'url'.
        If output is None: dict with 'url'.
    """
    body = {"model": model, "prompt": prompt}

    if mode == "i2v" and first_frame:
        upload = _upload_file(first_frame, "image")
        body["first_frame_image"] = upload["file_id"]
    elif mode == "sef":
        if first_frame:
            upload = _upload_file(first_frame, "image")
            body["first_frame_image"] = upload["file_id"]
        if last_frame:
            upload = _upload_file(last_frame, "image")
            body["last_frame_image"] = upload["file_id"]
    elif mode == "ref" and subject_image:
        upload = _upload_file(subject_image, "image")
        body["subject_reference_image"] = upload["file_id"]

    print("Generating video ({}, {})...".format(mode, model))
    result = _api_request("video_generation", method="POST", body=body, timeout=120)

    task_id = result.get("task_id", "")
    if not task_id:
        raise RuntimeError("No task_id returned from video API")

    print("  Task: {} (polling up to {}s)...".format(task_id, max_wait))
    final = _wait_video_task(task_id, max_wait=max_wait)

    file_id = final.get("file_id", "")
    if not file_id:
        raise RuntimeError("No file_id in video result")

    video_url = _get_video_url(file_id)
    if not video_url:
        raise RuntimeError("Could not retrieve video download URL")

    w = final.get("video_width", "?")
    h = final.get("video_height", "?")
    print("  Video: {}x{}".format(w, h))

    if output:
        path = _download_url(video_url, output)
        print("  Saved: {}".format(path))
        return {"path": path, "url": video_url}
    print("  URL: {}".format(video_url))
    return {"url": video_url}


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """Simple CLI for direct invocation."""
    import argparse

    parser = argparse.ArgumentParser(description="MiniMax Multimodal API Toolkit")
    sub = parser.add_subparsers(dest="command")

    # TTS
    p = sub.add_parser("tts", help="Text-to-Speech")
    p.add_argument("text", help="Text to synthesize")
    p.add_argument("-o", "--output", default="", help="Output file path")
    p.add_argument("--voice", default="female-shaonv", help="Voice ID")
    p.add_argument("--emotion", default="", help="Emotion tag")
    p.add_argument("--model", default="speech-2.8-hd", help="TTS model")

    # Music
    p = sub.add_parser("music", help="Music generation")
    p.add_argument("prompt", help="Music description")
    p.add_argument("-o", "--output", default="", help="Output file path")
    p.add_argument("--lyrics", default="", help="Song lyrics")
    p.add_argument("--instrumental", action="store_true", help="Generate instrumental")
    p.add_argument("--model", default="music-2.5", help="Music model")

    # Image
    p = sub.add_parser("image", help="Text-to-Image")
    p.add_argument("prompt", help="Image description")
    p.add_argument("-o", "--output", default="", help="Output file path")
    p.add_argument("--ratio", default="1:1", help="Aspect ratio")
    p.add_argument("--count", type=int, default=1, help="Number of images")
    p.add_argument("--model", default="image-01", help="Image model")
    p.add_argument("--optimize", action="store_true", help="Enable prompt optimizer")

    # Image-to-Image
    p = sub.add_parser("i2i", help="Image-to-Image")
    p.add_argument("prompt", help="Image description")
    p.add_argument("image", help="Reference image path or URL")
    p.add_argument("-o", "--output", default="", help="Output file path")
    p.add_argument("--ratio", default="1:1", help="Aspect ratio")
    p.add_argument("--count", type=int, default=1, help="Number of images")

    # Video
    p = sub.add_parser("video", help="Video generation")
    p.add_argument("prompt", help="Video description")
    p.add_argument("-o", "--output", default="", help="Output file path")
    p.add_argument("--mode", default="t2v", help="Mode: t2v, i2v, sef, ref")
    p.add_argument("--first-frame", default="", help="First frame image (i2v/sef)")
    p.add_argument("--last-frame", default="", help="Last frame image (sef)")
    p.add_argument("--subject", default="", help="Subject reference image (ref)")
    p.add_argument("--model", default="MiniMax-Hailuo-2.3", help="Video model")
    p.add_argument("--max-wait", type=int, default=600, help="Max wait seconds")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "tts":
            out = args.output or None
            generate_tts(args.text, output=out, voice_id=args.voice,
                         emotion=args.emotion, model=args.model)
        elif args.command == "music":
            out = args.output or None
            generate_music(args.prompt, output=out, lyrics=args.lyrics,
                           instrumental=args.instrumental, model=args.model)
        elif args.command == "image":
            out = args.output or None
            generate_image(args.prompt, output=out, aspect_ratio=args.ratio,
                           count=args.count, model=args.model, prompt_optimizer=args.optimize)
        elif args.command == "i2i":
            out = args.output or None
            image_to_image(args.prompt, args.image, output=out, aspect_ratio=args.ratio,
                           count=args.count)
        elif args.command == "video":
            out = args.output or None
            generate_video(args.prompt, output=out, mode=args.mode,
                           first_frame=args.first_frame, last_frame=args.last_frame,
                           subject_image=args.subject, model=args.model,
                           max_wait=args.max_wait)
    except Exception as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
