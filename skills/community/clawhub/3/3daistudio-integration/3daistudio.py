#!/usr/bin/env python3
"""
3D AI Studio - Image/Text to 3D Model
API: https://www.3daistudio.com/Platform/API/Documentation

Usage:
    export THREE_D_AI_STUDIO_API_KEY="your-api-key"
    python 3daistudio.py trellis --image photo.png -o model.glb
"""

import sys
import os
import json
import time
import base64
import argparse
import urllib.request
import urllib.error

API_KEY = os.environ.get("THREE_D_AI_STUDIO_API_KEY", "")
if not API_KEY:
    print("Error: THREE_D_AI_STUDIO_API_KEY environment variable not set.")
    print("Get your API key from: https://www.3daistudio.com/Platform/API")
    sys.exit(1)

BASE_URL = "https://api.3daistudio.com"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def api_get(path):
    url = BASE_URL + path
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def api_post(path, payload):
    url = BASE_URL + path
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def image_to_base64(path):
    import os
    ext = os.path.splitext(path)[1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext.strip("."), "image/png")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


def poll_status(task_id, interval=12, max_wait=600):
    """Poll until FINISHED or FAILED. Returns result dict."""
    path = f"/v1/generation-request/{task_id}/status/"
    start = time.time()
    while True:
        elapsed = int(time.time() - start)
        try:
            r = api_get(path)
        except Exception as e:
            print(f"  [poll] Error: {e}")
            time.sleep(interval)
            continue

        status = r.get("status", "UNKNOWN")
        progress = r.get("progress", 0)
        print(f"  [{elapsed}s] Status: {status} ({progress}%)")

        if status == "FINISHED":
            return r
        if status == "FAILED":
            print("  Generation FAILED - credits refunded.")
            return r
        if elapsed > max_wait:
            print("  Timeout waiting for result.")
            return r

        time.sleep(interval)


def download_result(result, output_path):
    """Download the first 3D model from results."""
    results = result.get("results", [])
    if not results:
        print("No results found.")
        return

    # Prefer 3D_MODEL type over ARCHIVE
    preferred = next((r for r in results if r.get("asset_type") == "3D_MODEL"), None)
    entry = preferred or results[0]
    asset_url = entry.get("asset") or entry.get("asset_url")
    if not asset_url:
        print("No asset URL in results.")
        print(json.dumps(entry, indent=2))
        return

    print(f"  Downloading from: {asset_url}")
    req = urllib.request.Request(asset_url)
    with urllib.request.urlopen(req, timeout=60) as r:
        with open(output_path, "wb") as f:
            f.write(r.read())
    print(f"  Saved to: {output_path}")

    thumbnail = results[0].get("thumbnail")
    if thumbnail:
        print(f"  Thumbnail: {thumbnail}")


# --- Commands ---

def cmd_balance(args):
    """Check credit balance."""
    try:
        r = api_get("/account/user/wallet/")
        balance = r.get("balance", "?")
        print(f"Credit Balance: {balance} credits")
        print(json.dumps(r, indent=2))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("[!] Wallet API returned 404. Check your API key is valid.")
            print("    Balance visible at https://www.3daistudio.com/Platform/API")
        else:
            print(f"Error {e.code}: {e.read().decode()[:200]}")
    except Exception as e:
        print(f"Error: {e}")


def cmd_trellis(args):
    """TRELLIS.2 image-to-3D generation."""
    payload = {}

    if args.image:
        print(f"  Encoding image: {args.image}")
        payload["image"] = image_to_base64(args.image)
    elif args.image_url:
        payload["image_url"] = args.image_url
    else:
        print("Error: provide --image or --image-url")
        sys.exit(1)

    payload["resolution"] = args.resolution
    payload["steps"] = args.steps
    payload["textures"] = args.textures
    if args.textures:
        payload["texture_size"] = args.texture_size
    payload["decimation_target"] = args.decimation_target
    payload["generate_thumbnail"] = args.thumbnail

    # Credit estimate
    credit_map = {
        "512":  {False: 15, True: {1024: 25, 2048: 25, 4096: 30}},
        "1024": {False: 20, True: {1024: 30, 2048: 30, 4096: 40}},
        "1536": {False: 25, True: {1024: 40, 2048: 40, 4096: 55}},
    }
    base = credit_map.get(args.resolution, {})
    if args.textures:
        cost = base.get(True, {}).get(args.texture_size, "?")
    else:
        cost = base.get(False, "?")
    if args.thumbnail:
        cost = f"{cost}+2" if isinstance(cost, int) else cost
    print(f"  Model: TRELLIS.2 | Resolution: {args.resolution} | Textures: {args.textures} | Est. credits: {cost}")

    print("  Submitting generation request...")
    try:
        r = api_post("/v1/3d-models/trellis2/generate/", payload)
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")
        sys.exit(1)

    task_id = r.get("task_id")
    print(f"  Task ID: {task_id}")

    if args.output:
        print("  Polling for result...")
        result = poll_status(task_id)
        if result.get("status") == "FINISHED":
            download_result(result, args.output)
    else:
        print(f"  Use 'status {task_id}' to check progress.")
        print(f"  Use 'download {task_id} --output model.glb' to download.")


def cmd_rapid(args):
    """Hunyuan Rapid generation (text or image)."""
    payload = {}

    if args.image:
        print(f"  Encoding image: {args.image}")
        payload["image"] = image_to_base64(args.image)
    elif args.prompt:
        payload["prompt"] = args.prompt
    else:
        print("Error: provide --image or --prompt")
        sys.exit(1)

    payload["enable_pbr"] = args.pbr
    payload["enable_geometry"] = args.geometry

    cost = 35 + (20 if args.pbr else 0)
    print(f"  Model: Hunyuan Rapid | PBR: {args.pbr} | Est. credits: {cost}")

    print("  Submitting generation request...")
    try:
        r = api_post("/v1/3d-models/tencent/generate/rapid/", payload)
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")
        sys.exit(1)

    task_id = r.get("task_id")
    print(f"  Task ID: {task_id}")

    if args.output:
        print("  Polling for result (typically 2-3 min)...")
        result = poll_status(task_id, interval=15)
        if result.get("status") == "FINISHED":
            download_result(result, args.output)
    else:
        print(f"  Use 'status {task_id}' to check progress.")


def cmd_pro(args):
    """Hunyuan Pro generation (text, image, or multi-view)."""
    payload = {"model": args.model}

    if args.image:
        print(f"  Encoding image: {args.image}")
        payload["image"] = image_to_base64(args.image)
    elif args.prompt:
        payload["prompt"] = args.prompt
    else:
        print("Error: provide --image or --prompt")
        sys.exit(1)

    payload["enable_pbr"] = args.pbr
    payload["face_count"] = args.face_count
    payload["generate_type"] = args.generate_type

    cost = 60 + (20 if args.pbr else 0)
    print(f"  Model: Hunyuan Pro {args.model} | PBR: {args.pbr} | Type: {args.generate_type} | Est. credits: {cost}")

    print("  Submitting generation request...")
    try:
        r = api_post("/v1/3d-models/tencent/generate/pro/", payload)
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")
        sys.exit(1)

    task_id = r.get("task_id")
    print(f"  Task ID: {task_id}")

    if args.output:
        print("  Polling for result (typically 3-6 min)...")
        result = poll_status(task_id, interval=20, max_wait=800)
        if result.get("status") == "FINISHED":
            download_result(result, args.output)
    else:
        print(f"  Use 'status {task_id}' to check progress.")


def cmd_status(args):
    """Check status of a generation task."""
    path = f"/v1/generation-request/{args.task_id}/status/"
    try:
        r = api_get(path)
        print(json.dumps(r, indent=2))
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")


def cmd_download(args):
    """Download result of a finished task."""
    path = f"/v1/generation-request/{args.task_id}/status/"
    try:
        r = api_get(path)
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")
        sys.exit(1)

    status = r.get("status")
    if status != "FINISHED":
        print(f"Task not finished yet. Status: {status}")
        sys.exit(1)

    download_result(r, args.output)


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="3D AI Studio CLI")
    sub = parser.add_subparsers(dest="cmd")

    # balance
    sub.add_parser("balance", help="Check credit balance")

    # trellis
    p = sub.add_parser("trellis", help="TRELLIS.2 image-to-3D")
    p.add_argument("--image", help="Path to local image file")
    p.add_argument("--image-url", dest="image_url", help="Public image URL")
    p.add_argument("--resolution", default="1024", choices=["512","1024","1536"])
    p.add_argument("--steps", type=int, default=12)
    p.add_argument("--textures", action="store_true", help="Enable PBR textures")
    p.add_argument("--texture-size", dest="texture_size", type=int, default=2048, choices=[1024,2048,4096])
    p.add_argument("--decimation-target", dest="decimation_target", type=int, default=1000000)
    p.add_argument("--thumbnail", action="store_true", help="Generate thumbnail (+2 credits)")
    p.add_argument("--output", "-o", help="Output .glb file path (triggers auto-poll)")

    # rapid
    p = sub.add_parser("rapid", help="Hunyuan Rapid (text or image)")
    p.add_argument("--image", help="Path to local image file")
    p.add_argument("--prompt", help="Text description")
    p.add_argument("--pbr", action="store_true", help="Enable PBR textures (+20 credits)")
    p.add_argument("--geometry", action="store_true", help="Enable geometry optimization")
    p.add_argument("--output", "-o", help="Output .glb file path (triggers auto-poll)")

    # pro
    p = sub.add_parser("pro", help="Hunyuan Pro (text or image)")
    p.add_argument("--image", help="Path to local image file")
    p.add_argument("--prompt", help="Text description")
    p.add_argument("--model", default="3.1", choices=["3.0","3.1"])
    p.add_argument("--pbr", action="store_true", help="Enable PBR textures (+20 credits)")
    p.add_argument("--face-count", dest="face_count", type=int, default=500000)
    p.add_argument("--generate-type", dest="generate_type", default="Normal",
                   choices=["Normal","LowPoly","Geometry","Sketch"])
    p.add_argument("--output", "-o", help="Output .glb file path (triggers auto-poll)")

    # status
    p = sub.add_parser("status", help="Check generation status")
    p.add_argument("task_id")

    # download
    p = sub.add_parser("download", help="Download finished result")
    p.add_argument("task_id")
    p.add_argument("--output", "-o", default="model.glb")

    args = parser.parse_args()

    dispatch = {
        "balance": cmd_balance,
        "trellis": cmd_trellis,
        "rapid": cmd_rapid,
        "pro": cmd_pro,
        "status": cmd_status,
        "download": cmd_download,
    }

    if not args.cmd or args.cmd not in dispatch:
        parser.print_help()
        sys.exit(1)

    dispatch[args.cmd](args)


if __name__ == "__main__":
    main()
