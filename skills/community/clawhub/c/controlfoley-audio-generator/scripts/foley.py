#!/usr/bin/env python3
"""Controlfoley Audio Generator — text-to-audio & video-to-audio sound effects generation."""

import argparse
import json
import os
import sys
import time
import ssl
import urllib.request
import urllib.parse
import urllib.error

API_BASE = "https://controlfoley.ai.xiaomi.com"
POLL_INTERVAL = 3
MAX_POLLS = 100  # ~5 min timeout



def submit_t2a(prompt: str, model: str = "ControlFoley", duration: float = 8.0,
               negative_prompt: str = "", cfg_strength: float = 4.5,
               count: int = 1, seed: int = None) -> str:
    """Submit text-to-audio task. Returns task_id."""
    import subprocess
    cmd = [
        "curl", "-s", "-X", "POST", f"{API_BASE}/api/v1/v2a/submit",
        "-F", f"model={model}",
        "-F", f"prompt={prompt}",
        "-F", f"duration={duration}",
        "-F", f"cfg_strength={cfg_strength}",
        "-F", f"count={count}",
    ]
    if negative_prompt:
        cmd += ["-F", f"negative_prompt={negative_prompt}"]
    if seed is not None:
        cmd += ["-F", f"seed={seed}"]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"Submit failed: {result.stderr}")
    resp = json.loads(result.stdout)
    tid = resp.get("task_id") or resp.get("taskId")
    if tid:
        print(f"[OK] Task submitted: {tid}", file=sys.stderr)
        return tid
    raise RuntimeError(f"Submit error: {resp}")


def submit_v2a(video_path: str, model: str = "ControlFoley", prompt: str = "",
               negative_prompt: str = "", reference_audio: str = None,
               cfg_strength: float = 4.5, count: int = 1, seed: int = None) -> str:
    """Submit video-to-audio task. Returns task_id."""
    import subprocess
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    cmd = [
        "curl", "-s", "-X", "POST", f"{API_BASE}/api/v1/v2a/submit",
        "-F", f"model={model}",
        "-F", f"file=@{video_path}",
        "-F", f"cfg_strength={cfg_strength}",
        "-F", f"count={count}",
    ]
    if prompt:
        cmd += ["-F", f"prompt={prompt}"]
    if negative_prompt:
        cmd += ["-F", f"negative_prompt={negative_prompt}"]
    if reference_audio and os.path.isfile(reference_audio):
        cmd += ["-F", f"reference_audio=@{reference_audio}"]
    if seed is not None:
        cmd += ["-F", f"seed={seed}"]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    resp = json.loads(result.stdout)
    tid = resp.get("task_id") or resp.get("taskId")
    if tid:
        print(f"[OK] Task submitted: {tid}", file=sys.stderr)
        return tid
    raise RuntimeError(f"Submit error: {resp}")


def poll_result(task_id: str) -> list:
    """Poll until done. Returns list of result URLs."""
    for i in range(MAX_POLLS):
        url = f"{API_BASE}/api/v1/v2a/status/{task_id}"
        try:
            req = urllib.request.Request(url)
            resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
        except urllib.error.HTTPError as e:
            print(f"[!!] Poll HTTP {e.code}, retrying...", file=sys.stderr)
            time.sleep(POLL_INTERVAL)
            continue

        status = resp.get("status", "")
        if status == "success" and resp.get("done"):
            urls = resp.get("processed_urls") or resp.get("urls") or []
            print(f"[OK] Done! {len(urls)} file(s) ready", file=sys.stderr)
            return urls
        if status == "failed":
            raise RuntimeError(f"Task failed: {resp.get('error', 'unknown')}")
        if status in ("pending", "processing"):
            pos = resp.get("queue_pos", "?")
            print(f"[..] {status} (queue={pos}, poll {i+1}/{MAX_POLLS})", file=sys.stderr)
            time.sleep(POLL_INTERVAL)
            continue
        # Unknown status
        time.sleep(POLL_INTERVAL)

    raise TimeoutError("Task timed out after polling")


def download(url: str, output_dir: str, task_id: str = None) -> str:
    """Download file from URL. Falls back to API download endpoint for internal URLs."""
    filename = url.split("/")[-1]
    output = os.path.join(output_dir, filename)
    try:
        url = urllib.parse.quote(url, safe=':/')
        print(f"[..] Downloading {url} to {output}", file=sys.stderr)
        data = urllib.request.urlopen(url, timeout=60).read()
    except (urllib.error.URLError, urllib.error.HTTPError):
        # Internal URLs (.xiaomi.srv) may not be accessible; use API download endpoint
        if task_id and filename:
            fallback = f"{API_BASE}/api/v1/v2a/ControlFoley_output/{task_id}/{filename}"
            print(f"[!!] Direct URL failed, trying API endpoint: {fallback}", file=sys.stderr)
            data = urllib.request.urlopen(fallback, timeout=60).read()
        else:
            raise

    with open(output, "wb") as f:
        f.write(data)
    print(f"[OK] Saved: {output} ({len(data)} bytes)", file=sys.stderr)
    return output


def list_models():
    """List available models."""
    url = f"{API_BASE}/api/v1/v2a/models"
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
    for m in resp.get("models", []):
        status = "✅" if m.get("enabled") else "❌"
        print(f"  {status} {m['name']}")


def main():
    p = argparse.ArgumentParser(description="XM Plus Foley Gen — Sound Effects Generation")
    sub = p.add_subparsers(dest="cmd", required=True)

    # Text-to-Audio
    t2a = sub.add_parser("t2a", help="Text to audio")
    t2a.add_argument("prompt", help="Audio description (e.g. 'dog barking in park')")
    t2a.add_argument("--model", default="ControlFoley", help="Model ID")
    t2a.add_argument("--duration", type=float, default=8.0, help="Duration in seconds (max 30)")
    t2a.add_argument("--negative", default="", help="Negative prompt")
    t2a.add_argument("--cfg", type=float, default=4.5, help="CFG strength")
    t2a.add_argument("--count", type=int, default=1, help="Number of results (1-5)")
    t2a.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    t2a.add_argument("-o", "--outdir", default="./output", help="Output directory")

    # Video-to-Audio
    v2a = sub.add_parser("v2a", help="Video to audio")
    v2a.add_argument("video", help="Input video file path") 
    v2a.add_argument("--prompt", default="", help="Text prompt to guide audio generation")
    v2a.add_argument("--model", default="ControlFoley", help="Model ID")
    v2a.add_argument("--negative", default="", help="Negative prompt")
    v2a.add_argument("--ref-audio", default=None, help="Reference audio file")
    v2a.add_argument("--cfg", type=float, default=4.5, help="CFG strength")
    v2a.add_argument("--count", type=int, default=1, help="Number of results")
    v2a.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    v2a.add_argument("-o", "--outdir", default="./output", help="Output directory")

    # List models
    sub.add_parser("models", help="List available models")

    args = p.parse_args()

    if args.cmd == "models":
        list_models()
        return

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    if args.cmd == "t2a":
        task_id = submit_t2a(
            prompt=args.prompt, model=args.model, duration=args.duration,
            negative_prompt=args.negative, cfg_strength=args.cfg,
            count=args.count, seed=args.seed
        )
    elif args.cmd == "v2a":
        task_id = submit_v2a(
            video_path=args.video, model=args.model, prompt=args.prompt,
            negative_prompt=args.negative, reference_audio=args.ref_audio,
            cfg_strength=args.cfg, count=args.count, seed=args.seed
        )

    urls = poll_result(task_id)
    for url in urls:
        path = download(url, args.outdir, task_id=task_id)
        print(path)  # stdout for piping


if __name__ == "__main__":
    main()
