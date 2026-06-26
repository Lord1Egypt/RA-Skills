#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.25.0",
# ]
# ///
"""
comfyui_generate.py — Part of the comfyui-bridge OpenClaw skill.

Sends image generation, editing, faceswap, LivePortrait, and style-transfer
requests to a running ComfyUI Bridge server and downloads the result.

When the bridge is unreachable the request is serialised to a local queue
(~/.openclaw/faceswap-queue/) and processed automatically by queue_processor.py
once the bridge comes back online.

Repository: https://github.com/Bortlesboat/comfyui-bridge (see repo for full source)

Usage examples
--------------
txt2img:
    uv run comfyui_generate.py --prompt "a yacht at sunset" --filename "output.png"

img2img:
    uv run comfyui_generate.py --prompt "make it sunset" --filename "output.png" -i /tmp/input.png --strength 0.5

faceswap:
    uv run comfyui_generate.py --faceswap --source-face /tmp/face.png -i /tmp/target.png --filename "output.png"

Environment variables
---------------------
COMFYUI_BRIDGE_URL  URL of the ComfyUI Bridge server (default: http://localhost:8100)
"""

import argparse
import os
import sys
import time
from pathlib import Path


BRIDGE_URL = os.environ.get("COMFYUI_BRIDGE_URL", "http://localhost:8100")

QUEUE_DIR = Path.home() / ".openclaw" / "faceswap-queue"

def ensure_jpeg(image_path: Path) -> Path:
    """Convert HEIC/HEIF to JPEG using sips (macOS built-in). Returns original path if not HEIC."""
    import subprocess as _sp
    if image_path.suffix.lower() in (".heic", ".heif"):
        jpg_path = image_path.with_suffix(".jpg")
        try:
            result = _sp.run(
                ["sips", "-s", "format", "jpeg", str(image_path), "--out", str(jpg_path)],
                capture_output=True, timeout=15
            )
            if result.returncode == 0 and jpg_path.exists():
                print(f"Converted HEIC to JPEG: {jpg_path.name}")
                return jpg_path
        except Exception as exc:
            print(f"HEIC conversion failed ({exc}), using original", file=sys.stderr)
    return image_path


def check_faceswap_quality(image_path: Path, timeout: int = 20) -> tuple:
    """Use gemma3:12b via local Ollama to verify faceswap quality.
    Returns (passed: bool, reason: str). Fails open on error."""
    import base64, json as _json, urllib.request as _req
    try:
        img_b64 = base64.b64encode(image_path.read_bytes()).decode()
        payload = {
            "model": "gemma3:12b",
            "prompt": (
                "Examine this image. Does it show a human face naturally integrated "
                "(not blank, glitched, distorted, or missing)? "
                "Reply with exactly: PASS or FAIL, then a comma, then a brief reason."
            ),
            "images": [img_b64],
            "stream": False,
        }
        data = _json.dumps(payload).encode()
        request = _req.Request(
            "http://localhost:11434/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        resp = _req.urlopen(request, timeout=timeout)
        result = _json.loads(resp.read())
        response_text = result.get("response", "").strip()
        passed = response_text.upper().startswith("PASS")
        return passed, response_text
    except Exception as exc:
        return True, f"QA skipped ({exc})"




def queue_request(args_list, description="a request", source_face=None,
                  input_image=None, style_ref=None, output_file=None):
    """Queue a failed request for later processing when bridge comes back."""
    import json
    import datetime
    import shutil
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    req_id = f"request_{ts}"

    # Copy image files to queue dir so they persist
    saved_images = {}
    for label, path_str in [("source_face", source_face), ("input_image", input_image), ("style_ref", style_ref)]:
        if path_str:
            src = Path(path_str).expanduser()
            if src.exists():
                dst = QUEUE_DIR / f"{req_id}_{label}{src.suffix}"
                shutil.copy2(str(src), str(dst))
                saved_images[label] = str(dst)
                args_list = [str(dst) if a == str(src) else a for a in args_list]

    # Strip --no-media from queued args so the processor does not accumulate it on retries
    args_list = [a for a in args_list if a != "--no-media"]

    req_data = {
        "args": args_list,
        "description": description,
        "queued_at": datetime.datetime.now().isoformat(),
        "output_file": output_file or "",
        **saved_images,
    }

    req_file = QUEUE_DIR / f"{req_id}.json"
    tmp_file = req_file.with_suffix(".tmp")
    tmp_file.write_text(json.dumps(req_data, indent=2))
    tmp_file.rename(req_file)
    return str(req_file)


def _describe_request(args):
    """Generate a human-readable description of the request."""
    if getattr(args, "faceswap_pipeline", False):
        return "faceswap pipeline"
    elif getattr(args, "targeted_faceswap", False):
        return "targeted faceswap"
    elif getattr(args, "faceswap", False):
        return "faceswap"
    elif getattr(args, "liveportrait", False):
        preset = getattr(args, "expression_preset", "")
        return f"liveportrait ({preset})" if preset else "liveportrait"
    elif getattr(args, "style_transfer", False):
        return "style transfer"
    elif getattr(args, "restyle", False):
        return "restyle"
    elif getattr(args, "input_image", None):
        return "img2img"
    return "txt2img"




def handle_bridge_error(e, operation: str):
    """Print actionable error message for bridge communication failures."""
    import httpx as _httpx
    if isinstance(e, _httpx.TimeoutException):
        print(f"Error: {operation} timed out. ComfyUI may be overloaded or processing a large job.", file=sys.stderr)
        print(f"Check queue: curl {BRIDGE_URL}/diagnostics | python -m json.tool", file=sys.stderr)
    elif isinstance(e, _httpx.HTTPStatusError):
        status = e.response.status_code
        try:
            detail = e.response.json().get("detail", e.response.text[:200])
        except Exception:
            detail = e.response.text[:200]
        print(f"Error: {operation} failed (HTTP {status}): {detail}", file=sys.stderr)
        if status == 502:
            print("ComfyUI may have crashed. Check ComfyUI terminal for errors.", file=sys.stderr)
        elif status == 422:
            print("Invalid request parameters. Check your flags.", file=sys.stderr)
        elif status == 413:
            print("Image too large. Max upload size is 50MB.", file=sys.stderr)
    else:
        print(f"Error: {operation} failed: {e}", file=sys.stderr)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate/edit images via ComfyUI Bridge"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="Image description or edit instruction"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., sunset.png)"
    )
    parser.add_argument(
        "--input-image", "-i",
        dest="input_image",
        help="Input image path for img2img or faceswap target"
    )
    parser.add_argument(
        "--source-face",
        dest="source_face",
        help="Source face image path (for faceswap mode)"
    )
    parser.add_argument(
        "--faceswap",
        action="store_true",
        help="Enable faceswap mode (requires --source-face and -i)"
    )
    parser.add_argument(
        "--targeted-faceswap",
        action="store_true",
        help="Targeted faceswap: swap onto a specific face in a multi-face image (requires --source-face, -i, and --target-face-index)"
    )
    parser.add_argument(
        "--faceswap-pipeline",
        action="store_true",
        help="Faceswap + img2img cleanup in one call. Swap face then refine with Juggernaut. (requires --source-face and -i)"
    )
    parser.add_argument(
        "--cleanup-prompt",
        default="",
        help="Prompt for img2img cleanup step in pipeline mode (optional)"
    )
    parser.add_argument(
        "--cleanup-strength",
        type=float,
        default=0.40,
        help="Denoise strength for cleanup step: 0.3=subtle, 0.5=major (default: 0.40)"
    )
    parser.add_argument(
        "--target-face-index",
        default="0",
        help="Which face(s) in the target image to replace. Comma-separated. 0=first detected (left-to-right), 1=second, '0,2'=first+third (default: 0)"
    )
    parser.add_argument(
        "--source-face-index",
        default="0",
        help="Which face in the source image to use (default: 0)"
    )
    # Style transfer modes
    parser.add_argument(
        "--style-transfer",
        action="store_true",
        help="Generate new image in the style of a reference (requires --style-ref and --prompt)"
    )
    parser.add_argument(
        "--restyle",
        action="store_true",
        help="Apply reference style to existing photo (requires --style-ref and -i)"
    )
    parser.add_argument(
        "--style-ref",
        dest="style_ref",
        help="Style reference image path (for --style-transfer or --restyle)"
    )
    parser.add_argument(
        "--style-weight",
        type=float,
        default=0.85,
        help="How strongly to follow reference style: 0.5=loose, 0.85=strong, 1.0=near-copy (default: 0.85)"
    )
    # LivePortrait mode
    parser.add_argument(
        "--liveportrait",
        action="store_true",
        help="LivePortrait expression editor: animate faces in any photo (requires -i)"
    )
    parser.add_argument("--smile", type=float, default=0.0, help="Smile intensity: -0.3 to 1.3 (default: 0)")
    parser.add_argument("--blink-val", type=float, default=0.0, dest="blink_val", help="Blink: -20 (closed) to 5 (default: 0)")
    parser.add_argument("--eyebrow-val", type=float, default=0.0, dest="eyebrow_val", help="Eyebrow: -10 to 15 (default: 0)")
    parser.add_argument("--wink-val", type=float, default=0.0, dest="wink_val", help="Wink: 0 to 25 (default: 0)")
    parser.add_argument("--pupil-x", type=float, default=0.0, help="Pupil X: -15 to 15 (default: 0)")
    parser.add_argument("--pupil-y", type=float, default=0.0, help="Pupil Y: -15 to 15 (default: 0)")
    parser.add_argument("--aaa", type=float, default=0.0, help="Open mouth: -30 to 120 (default: 0)")
    parser.add_argument("--eee", type=float, default=0.0, help="Eee mouth: -20 to 15 (default: 0)")
    parser.add_argument("--woo", type=float, default=0.0, help="Woo mouth: -20 to 15 (default: 0)")
    parser.add_argument("--pitch", type=float, default=0.0, help="Head pitch: -20 to 20 (default: 0)")
    parser.add_argument("--yaw", type=float, default=0.0, help="Head yaw: -20 to 20 (default: 0)")
    parser.add_argument("--roll", type=float, default=0.0, help="Head roll: -20 to 20 (default: 0)")
    parser.add_argument(
        "--expression-preset",
        choices=["smile", "surprised", "wink", "suspicious", "derp", "angry", "sleepy"],
        help="Quick expression preset (overrides individual expression params)"
    )
    parser.add_argument(
        "--model", "-m",
        default="juggernaut",
        choices=["juggernaut", "flux", "realvis"],
        help="Model: juggernaut (luxury/architecture), flux (max photorealism), realvis (people/portraits)"
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        default="1:1",
        choices=["1:1", "4:5", "9:16", "16:9", "5:4"],
        help="Output aspect ratio"
    )
    parser.add_argument(
        "--strength", "-s",
        type=float,
        default=0.6,
        help="img2img denoise strength: 0.1=subtle, 0.9=major changes (default: 0.6)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=-1,
        help="Seed (-1 = random)"
    )
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Disable prompt enhancement"
    )
    parser.add_argument(
        "--no-media",
        action="store_true",
        help="Suppress MEDIA: line on stdout (bot handles delivery separately)"
    )
    parser.add_argument(
        "--enhanced", "-e",
        action="store_true",
        help="Use enhanced workflow: FaceDetailer + 4x-UltraSharp upscale (net 2x res). Adds ~30s for txt2img, ~10s for faceswap."
    )
    # Faceswap quality options
    parser.add_argument(
        "--no-boost",
        action="store_true",
        help="Disable FaceBoost pre-swap enhancement (faceswap only)"
    )
    parser.add_argument(
        "--codeformer-weight",
        type=float,
        default=0.7,
        help="CodeFormer weight: 0.0=max quality, 1.0=max fidelity (default: 0.7)"
    )
    parser.add_argument(
        "--restore-visibility",
        type=float,
        default=0.85,
        help="Face restore visibility: 0.0=original, 1.0=full restore (default: 0.85)"
    )

    args = parser.parse_args()

    import httpx

    # Health check first
    try:
        r = httpx.get(f"{BRIDGE_URL}/health", timeout=5)
        r.raise_for_status()
        health = r.json()
        print(f"Bridge online: {BRIDGE_URL}")
        if health.get("status") != "ok":
            print(f"Warning: Bridge up but ComfyUI may be degraded: {health}", file=sys.stderr)
    except httpx.ConnectTimeout:
        print(f"BRIDGE_OFFLINE", file=sys.stderr)
        q = queue_request(sys.argv[1:], description=_describe_request(args),
                          source_face=getattr(args, "source_face", None),
                          input_image=getattr(args, "input_image", None),
                          style_ref=getattr(args, "style_ref", None),
                          output_file=args.filename)
        print(f"QUEUED:{q}")
        print("Request queued — will auto-process when bridge comes back online.")
        sys.exit(0)
    except httpx.ConnectError as e:
        print(f"BRIDGE_OFFLINE", file=sys.stderr)
        q = queue_request(sys.argv[1:], description=_describe_request(args),
                          source_face=getattr(args, "source_face", None),
                          input_image=getattr(args, "input_image", None),
                          style_ref=getattr(args, "style_ref", None),
                          output_file=args.filename)
        print(f"QUEUED:{q}")
        print("Request queued — will auto-process when bridge comes back online.")
        sys.exit(0)
    except Exception as e:
        print(f"BRIDGE_OFFLINE", file=sys.stderr)
        q = queue_request(sys.argv[1:], description=_describe_request(args),
                          source_face=getattr(args, "source_face", None),
                          input_image=getattr(args, "input_image", None),
                          style_ref=getattr(args, "style_ref", None),
                          output_file=args.filename)
        print(f"QUEUED:{q}")
        print("Request queued — will auto-process when bridge comes back online.")
        sys.exit(0)

    output_path = Path(args.filename).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine mode
    if args.liveportrait:
        if not args.input_image:
            print("Error: LivePortrait requires -i (portrait image)", file=sys.stderr)
            sys.exit(1)
        result = do_liveportrait(args, httpx)
    elif args.style_transfer:
        if not args.style_ref or not args.prompt:
            print("Error: Style transfer requires --style-ref and --prompt", file=sys.stderr)
            sys.exit(1)
        result = do_style_transfer(args, httpx)
    elif args.restyle:
        if not args.style_ref or not args.input_image:
            print("Error: Restyle requires --style-ref and -i (input image)", file=sys.stderr)
            sys.exit(1)
        result = do_restyle(args, httpx)
    elif args.faceswap_pipeline:
        if not args.source_face or not args.input_image:
            print("Error: Faceswap pipeline requires --source-face and -i (target image)", file=sys.stderr)
            sys.exit(1)
        result = do_faceswap_pipeline(args, httpx)
    elif args.targeted_faceswap:
        if not args.source_face or not args.input_image:
            print("Error: Targeted faceswap requires --source-face and -i (target image)", file=sys.stderr)
            sys.exit(1)
        result = do_targeted_faceswap(args, httpx)
    elif args.faceswap:
        if not args.source_face or not args.input_image:
            print("Error: Faceswap requires --source-face and -i (target image)", file=sys.stderr)
            sys.exit(1)
        result = do_faceswap(args, httpx)
    elif args.input_image:
        if not args.prompt:
            print("Error: img2img requires --prompt", file=sys.stderr)
            sys.exit(1)
        result = do_img2img(args, httpx)
    else:
        if not args.prompt:
            print("Error: txt2img requires --prompt", file=sys.stderr)
            sys.exit(1)
        result = do_txt2img(args, httpx)

    if not result:
        sys.exit(1)

    # Handle partial results (e.g., pipeline cleanup failed but swap succeeded)
    if result.get("status") == "partial":
        print(f"Warning: {result.get('detail', 'Partial result')}", file=sys.stderr)
        print(f"Returning intermediate result: {result.get('swap_filename', 'unknown')}", file=sys.stderr)

    # Download the result image — prefer direct LAN download, fall back to Discord CDN
    prompt_id = result.get("prompt_id", "")
    discord_url = result.get("discord_url", "")

    downloaded = False
    if prompt_id:
        download_url = f"{BRIDGE_URL}/download/{prompt_id}"
        print(f"Downloading result directly from bridge...")
        try:
            img_resp = httpx.get(download_url, timeout=30)
            img_resp.raise_for_status()
            output_path.write_bytes(img_resp.content)
            downloaded = True
        except Exception as e:
            print(f"Direct download failed, trying Discord CDN: {e}", file=sys.stderr)

    if not downloaded:
        if not discord_url:
            print("Error: No download URL available", file=sys.stderr)
            print(f"Response: {result}", file=sys.stderr)
            sys.exit(1)
        print(f"Downloading result from Discord CDN...")
        try:
            img_resp = httpx.get(discord_url, timeout=30, follow_redirects=True)
            img_resp.raise_for_status()
            output_path.write_bytes(img_resp.content)
        except Exception as e:
            print(f"Error downloading image: {e}", file=sys.stderr)
            sys.exit(1)

    # Validate downloaded file — size gate catches blank ReActor outputs (~1955 bytes)
    is_faceswap_mode = getattr(args, "faceswap", False) or getattr(args, "faceswap_pipeline", False) or getattr(args, "targeted_faceswap", False)
    file_size = output_path.stat().st_size
    BLANK_THRESHOLD = 50_000  # 50KB threshold: ReActor blanks ~1955 bytes, bad swaps can be 10-40KB, real swaps 100KB+

    if is_faceswap_mode and file_size < BLANK_THRESHOLD:
        # Auto-retry up to 2 more times (3 total attempts) for small/blank outputs
        MAX_SWAP_RETRIES = 2
        for swap_retry in range(1, MAX_SWAP_RETRIES + 1):
            print(f"Warning: Output looks small/blank ({file_size} bytes) — retry {swap_retry}/{MAX_SWAP_RETRIES}...", file=sys.stderr)
            retry_result = None
            if args.faceswap_pipeline:
                retry_result = do_faceswap_pipeline(args, httpx)
            elif args.targeted_faceswap:
                retry_result = do_targeted_faceswap(args, httpx)
            else:
                retry_result = do_faceswap(args, httpx)
            if not retry_result:
                print(f"Retry {swap_retry} request failed", file=sys.stderr)
                continue
            retry_prompt_id = retry_result.get("prompt_id", "")
            retry_discord = retry_result.get("discord_url", "")
            retry_downloaded = False
            if retry_prompt_id:
                try:
                    r2 = httpx.get(f"{BRIDGE_URL}/download/{retry_prompt_id}", timeout=30)
                    r2.raise_for_status()
                    output_path.write_bytes(r2.content)
                    retry_downloaded = True
                except Exception as e2:
                    print(f"Retry {swap_retry} direct download failed: {e2}", file=sys.stderr)
            if not retry_downloaded and retry_discord:
                try:
                    r2 = httpx.get(retry_discord, timeout=30, follow_redirects=True)
                    r2.raise_for_status()
                    output_path.write_bytes(r2.content)
                    retry_downloaded = True
                except Exception as e2:
                    print(f"Retry {swap_retry} CDN download failed: {e2}", file=sys.stderr)
            file_size = output_path.stat().st_size
            if file_size >= BLANK_THRESHOLD:
                print(f"Retry {swap_retry} succeeded ({file_size} bytes)")
                break  # Good result, continue with delivery
        else:
            # All retries exhausted
            print(f"FACESWAP_BLANK: Output still blank after {MAX_SWAP_RETRIES} retries ({file_size} bytes) — no face detected or face too small", file=sys.stderr)
            sys.exit(1)

    if file_size < 100:
        print(f"Error: Downloaded file is too small ({file_size} bytes) — likely corrupt", file=sys.stderr)
        sys.exit(1)

    # gemma3:12b vision QA for faceswap outputs
    if is_faceswap_mode:
        print("Running vision QA check (gemma3:12b)...")
        qa_passed, qa_reason = check_faceswap_quality(output_path)
        if not qa_passed:
            flagged_path = output_path.with_stem(output_path.stem + "_qa_flagged")
            output_path.rename(flagged_path)
            output_path = flagged_path
            print(f"Warning: QA flagged output — {qa_reason}", file=sys.stderr)
            print(f"Delivering anyway: {output_path.name}")
        else:
            print(f"QA passed: {qa_reason}")

    full_path = output_path.resolve()
    print(f"\nImage saved: {full_path} ({file_size:,} bytes)")
    if not args.no_media:
        print(f"MEDIA: {full_path}")


def do_txt2img(args, httpx):
    """Generate image from text prompt."""
    payload = {
        "prompt": args.prompt,
        "model": args.model,
        "aspect_ratio": args.aspect_ratio,
        "seed": args.seed,
        "enhance": not args.no_enhance,
        "enhanced": args.enhanced,
    }
    mode_str = "txt2img+enhanced" if args.enhanced else "txt2img"
    print(f"Generating image ({mode_str}, model={args.model})...")
    print(f"Prompt: {args.prompt}")
    try:
        r = httpx.post(
            f"{BRIDGE_URL}/generate",
            json=payload,
            timeout=120,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return handle_bridge_error(e, "txt2img")


def do_img2img(args, httpx):
    """Modify an existing image with a prompt."""
    img_path = Path(args.input_image).expanduser()
    if not img_path.exists():
        print(f"Error: Input image not found: {img_path}", file=sys.stderr)
        return None

    print(f"Modifying image (img2img, model={args.model}, strength={args.strength})...")
    print(f"Input: {img_path}")
    print(f"Prompt: {args.prompt}")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            with open(img_path, "rb") as f:
                files = {"image": (img_path.name, f, "image/png")}
                data = {
                    "prompt": args.prompt,
                    "strength": str(args.strength),
                    "model": args.model,
                    "aspect_ratio": args.aspect_ratio,
                    "seed": str(args.seed),
                    "enhance": str(not args.no_enhance).lower(),
                }
                r = httpx.post(
                    f"{BRIDGE_URL}/img2img",
                    files=files,
                    data=data,
                    timeout=120,
                )
            if r.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            return handle_bridge_error(e, "img2img")
        except Exception as e:
            return handle_bridge_error(e, "img2img")
    print(f"Error: Bridge busy after all retries. Check: curl {BRIDGE_URL}/diagnostics", file=sys.stderr)
    return None


def do_faceswap_pipeline(args, httpx):
    """Faceswap + img2img cleanup in one call."""
    source_path = Path(args.source_face).expanduser()
    target_path = Path(args.input_image).expanduser()
    target_path = ensure_jpeg(target_path)

    if not source_path.exists():
        print(f"Error: Source face not found: {source_path}", file=sys.stderr)
        return None
    if not target_path.exists():
        print(f"Error: Target image not found: {target_path}", file=sys.stderr)
        return None

    print(f"Faceswap pipeline (swap + cleanup)...")
    print(f"Source face: {source_path}")
    print(f"Target image: {target_path}")
    print(f"Cleanup strength: {args.cleanup_strength}")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            with open(source_path, "rb") as sf, open(target_path, "rb") as ti:
                files = {
                    "source_face": (source_path.name, sf, "image/png"),
                    "target_image": (target_path.name, ti, "image/png"),
                }
                data = {
                    "cleanup_prompt": args.cleanup_prompt or "",
                    "cleanup_strength": str(args.cleanup_strength),
                    "face_boost": str(not args.no_boost).lower(),
                    "codeformer_weight": str(args.codeformer_weight),
                    "restore_visibility": str(args.restore_visibility),
                    "enhanced": str(args.enhanced).lower(),
                }
                r = httpx.post(
                    f"{BRIDGE_URL}/faceswap/pipeline",
                    files=files,
                    data=data,
                    timeout=600,
                )
            if r.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            r.raise_for_status()
            result = r.json()
            total = result.get("total_time_s", "?")
            swap_t = result.get("swap_time_s", "?")
            print(f"Pipeline complete: swap {swap_t}s + cleanup = {total}s total")
            return result
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            return handle_bridge_error(e, "faceswap pipeline")
        except Exception as e:
            return handle_bridge_error(e, "faceswap pipeline")
    print(f"Error: Bridge busy after all retries. Check: curl {BRIDGE_URL}/diagnostics", file=sys.stderr)
    return None


def do_faceswap(args, httpx):
    """Swap a face from source onto target image."""
    source_path = Path(args.source_face).expanduser()
    target_path = Path(args.input_image).expanduser()
    target_path = ensure_jpeg(target_path)

    if not source_path.exists():
        print(f"Error: Source face not found: {source_path}", file=sys.stderr)
        return None
    if not target_path.exists():
        print(f"Error: Target image not found: {target_path}", file=sys.stderr)
        return None

    print(f"Swapping face...")
    print(f"Source face: {source_path}")
    print(f"Target image: {target_path}")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            with open(source_path, "rb") as sf, open(target_path, "rb") as ti:
                files = {
                    "source_face": (source_path.name, sf, "image/png"),
                    "target_image": (target_path.name, ti, "image/png"),
                }
                data = {
                    "face_boost": str(not args.no_boost).lower(),
                    "codeformer_weight": str(args.codeformer_weight),
                    "restore_visibility": str(args.restore_visibility),
                    "enhanced": str(args.enhanced).lower(),
                }
                r = httpx.post(
                    f"{BRIDGE_URL}/faceswap",
                    files=files,
                    data=data,
                    timeout=360,
                )
            if r.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            return handle_bridge_error(e, "generation")
        except Exception as e:
            return handle_bridge_error(e, "generation")
    print(f"Error: Bridge busy after all retries. Check: curl {BRIDGE_URL}/diagnostics", file=sys.stderr)
    return None


EXPRESSION_PRESETS = {
    "smile":      {"smile": 1.0, "eyebrow_val": 3},
    "surprised":  {"aaa": 60, "eyebrow_val": 10, "blink_val": -5},
    "wink":       {"wink_val": 15, "smile": 0.5},
    "suspicious": {"eyebrow_val": -5, "pupil_x": 10, "smile": -0.2},
    "derp":       {"pupil_x": 15, "pupil_y": -10, "aaa": 40, "roll": 10},
    "angry":      {"eyebrow_val": -8, "eee": 5, "pitch": -3},
    "sleepy":     {"blink_val": -15, "eyebrow_val": -3, "pitch": 5},
}


def do_liveportrait(args, httpx):
    """Animate facial expressions on a portrait photo."""
    portrait_path = Path(args.input_image).expanduser()
    if not portrait_path.exists():
        print(f"Error: Portrait image not found: {portrait_path}", file=sys.stderr)
        return None

    # Apply preset if specified
    if args.expression_preset:
        preset = EXPRESSION_PRESETS[args.expression_preset]
        for k, v in preset.items():
            setattr(args, k, v)
        print(f"Using preset: {args.expression_preset}")

    print(f"LivePortrait expression edit...")
    print(f"Portrait: {portrait_path}")
    if args.expression_preset:
        print(f"Preset: {args.expression_preset}")
    else:
        active = {k: getattr(args, k) for k in ["smile", "blink_val", "eyebrow_val", "wink_val",
                  "pupil_x", "pupil_y", "aaa", "eee", "woo", "pitch", "yaw", "roll"]
                  if getattr(args, k) != 0.0}
        print(f"Expressions: {active or 'neutral (no changes)'}")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            with open(portrait_path, "rb") as f:
                files = {"portrait": (portrait_path.name, f, "image/png")}
                data = {
                    "smile": str(args.smile),
                    "blink": str(args.blink_val),
                    "eyebrow": str(args.eyebrow_val),
                    "wink": str(args.wink_val),
                    "pupil_x": str(args.pupil_x),
                    "pupil_y": str(args.pupil_y),
                    "aaa": str(args.aaa),
                    "eee": str(args.eee),
                    "woo": str(args.woo),
                    "rotate_pitch": str(args.pitch),
                    "rotate_yaw": str(args.yaw),
                    "rotate_roll": str(args.roll),
                }
                r = httpx.post(
                    f"{BRIDGE_URL}/liveportrait",
                    files=files,
                    data=data,
                    timeout=180,
                )
            if r.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            return handle_bridge_error(e, "generation")
        except Exception as e:
            return handle_bridge_error(e, "generation")
    print(f"Error: Bridge busy after all retries. Check: curl {BRIDGE_URL}/diagnostics", file=sys.stderr)
    return None


def do_style_transfer(args, httpx):
    """Generate a new image in the style of a reference image."""
    style_path = Path(args.style_ref).expanduser()
    if not style_path.exists():
        print(f"Error: Style reference not found: {style_path}", file=sys.stderr)
        return None

    print(f"Style transfer...")
    print(f"Style reference: {style_path}")
    print(f"Prompt: {args.prompt}")
    print(f"Style weight: {args.style_weight}")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            with open(style_path, "rb") as sf:
                files = {"style_image": (style_path.name, sf, "image/png")}
                data = {
                    "prompt": args.prompt,
                    "aspect_ratio": args.aspect_ratio,
                    "seed": str(args.seed),
                    "style_weight": str(args.style_weight),
                    "enhance": str(not args.no_enhance).lower(),
                }
                r = httpx.post(
                    f"{BRIDGE_URL}/style-transfer",
                    files=files,
                    data=data,
                    timeout=360,
                )
            if r.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            return handle_bridge_error(e, "generation")
        except Exception as e:
            return handle_bridge_error(e, "generation")
    print(f"Error: Bridge busy after all retries. Check: curl {BRIDGE_URL}/diagnostics", file=sys.stderr)
    return None


def do_restyle(args, httpx):
    """Apply a reference image's style to an existing photo."""
    style_path = Path(args.style_ref).expanduser()
    input_path = Path(args.input_image).expanduser()

    if not style_path.exists():
        print(f"Error: Style reference not found: {style_path}", file=sys.stderr)
        return None
    if not input_path.exists():
        print(f"Error: Input image not found: {input_path}", file=sys.stderr)
        return None

    print(f"Restyling image...")
    print(f"Style reference: {style_path}")
    print(f"Input image: {input_path}")
    print(f"Style weight: {args.style_weight}, Strength: {args.strength}")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            with open(style_path, "rb") as sf, open(input_path, "rb") as ii:
                files = {
                    "style_image": (style_path.name, sf, "image/png"),
                    "input_image": (input_path.name, ii, "image/png"),
                }
                data = {
                    "prompt": args.prompt or "a photograph",
                    "seed": str(args.seed),
                    "style_weight": str(args.style_weight),
                    "strength": str(args.strength),
                }
                r = httpx.post(
                    f"{BRIDGE_URL}/restyle",
                    files=files,
                    data=data,
                    timeout=360,
                )
            if r.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            return handle_bridge_error(e, "generation")
        except Exception as e:
            return handle_bridge_error(e, "generation")
    print(f"Error: Bridge busy after all retries. Check: curl {BRIDGE_URL}/diagnostics", file=sys.stderr)
    return None


def do_targeted_faceswap(args, httpx):
    """Swap a face from source onto a specific face in a multi-face target image."""
    source_path = Path(args.source_face).expanduser()
    target_path = Path(args.input_image).expanduser()

    if not source_path.exists():
        print(f"Error: Source face not found: {source_path}", file=sys.stderr)
        return None
    if not target_path.exists():
        print(f"Error: Target image not found: {target_path}", file=sys.stderr)
        return None

    print(f"Targeted faceswap...")
    print(f"Source face: {source_path}")
    print(f"Target image: {target_path}")
    print(f"Target face index: {args.target_face_index} (0=leftmost detected face)")
    print(f"Source face index: {args.source_face_index}")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            with open(source_path, "rb") as sf, open(target_path, "rb") as ti:
                files = {
                    "source_face": (source_path.name, sf, "image/png"),
                    "target_image": (target_path.name, ti, "image/png"),
                }
                data = {
                    "target_face_index": args.target_face_index,
                    "source_face_index": args.source_face_index,
                    "face_boost": str(not args.no_boost).lower(),
                    "codeformer_weight": str(args.codeformer_weight),
                    "restore_visibility": str(args.restore_visibility),
                }
                r = httpx.post(
                    f"{BRIDGE_URL}/faceswap/targeted",
                    files=files,
                    data=data,
                    timeout=360,
                )
            if r.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                print(f"Bridge busy (429), retrying in 10s... (attempt {attempt}/{max_retries})")
                time.sleep(10)
                continue
            return handle_bridge_error(e, "generation")
        except Exception as e:
            return handle_bridge_error(e, "generation")
    print(f"Error: Bridge busy after all retries. Check: curl {BRIDGE_URL}/diagnostics", file=sys.stderr)
    return None


if __name__ == "__main__":
    main()
