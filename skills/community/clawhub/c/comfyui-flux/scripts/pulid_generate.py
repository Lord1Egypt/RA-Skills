#!/usr/bin/env python3
"""Generate face-consistent images locally via ComfyUI + Flux.1 Dev + PuLID.

Submits a PuLID-Flux workflow to ComfyUI's API with a reference face image,
polls for completion, and downloads the result.

Usage:
  python3 pulid_generate.py --prompt "..." --ref-image path/to/face.jpg [OPTIONS]

Requires ComfyUI running with PuLID-Flux custom node installed.
"""

import argparse
import base64
import io
import json
import mimetypes
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8200")


def build_pulid_workflow(
    prompt: str,
    ref_image_name: str,
    negative: str = "",
    width: int = 768,
    height: int = 1024,
    steps: int = 10,
    cfg: float = 3.5,
    seed: int = 0,
    weight: float = 1.0,
    start_at: float = 0.0,
    end_at: float = 1.0,
    filename_prefix: str = "pulid_api",
) -> dict:
    """Build PuLID-Flux workflow JSON matching the example template."""
    return {
        # --- Model loaders ---
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "flux1-dev.safetensors",
                "weight_dtype": "default",
            },
        },
        "2": {
            "class_type": "DualCLIPLoader",
            "inputs": {
                "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
                "clip_name2": "clip_l.safetensors",
                "type": "flux",
            },
        },
        "3": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": "ae.safetensors",
            },
        },
        # --- PuLID loaders ---
        "10": {
            "class_type": "PulidFluxModelLoader",
            "inputs": {
                "pulid_file": "pulid_flux_v0.9.1.safetensors",
            },
        },
        "11": {
            "class_type": "PulidFluxInsightFaceLoader",
            "inputs": {
                "provider": "CPU",
            },
        },
        "12": {
            "class_type": "PulidFluxEvaClipLoader",
            "inputs": {},
        },
        # --- Reference image ---
        "13": {
            "class_type": "LoadImage",
            "inputs": {
                "image": ref_image_name,
                "upload": "image",
            },
        },
        # --- Apply PuLID to model ---
        "20": {
            "class_type": "ApplyPulidFlux",
            "inputs": {
                "model": ["1", 0],
                "pulid_flux": ["10", 0],
                "eva_clip": ["12", 0],
                "face_analysis": ["11", 0],
                "image": ["13", 0],
                "weight": weight,
                "start_at": start_at,
                "end_at": end_at,
            },
        },
        # --- Text encoding ---
        "30": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["2", 0],
                "text": prompt,
            },
        },
        "31": {
            "class_type": "FluxGuidance",
            "inputs": {
                "conditioning": ["30", 0],
                "guidance": cfg,
            },
        },
        # --- Latent + Sampling ---
        "40": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1,
            },
        },
        "41": {
            "class_type": "RandomNoise",
            "inputs": {
                "noise_seed": seed,
            },
        },
        "42": {
            "class_type": "KSamplerSelect",
            "inputs": {
                "sampler_name": "euler",
            },
        },
        "43": {
            "class_type": "BasicScheduler",
            "inputs": {
                "model": ["20", 0],
                "scheduler": "simple",
                "steps": steps,
                "denoise": 1.0,
            },
        },
        "44": {
            "class_type": "BasicGuider",
            "inputs": {
                "model": ["20", 0],
                "conditioning": ["31", 0],
            },
        },
        "45": {
            "class_type": "SamplerCustomAdvanced",
            "inputs": {
                "noise": ["41", 0],
                "guider": ["44", 0],
                "sampler": ["42", 0],
                "sigmas": ["43", 0],
                "latent_image": ["40", 0],
            },
        },
        # --- Decode + Save ---
        "50": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["45", 0],
                "vae": ["3", 0],
            },
        },
        "51": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": filename_prefix,
                "images": ["50", 0],
            },
        },
    }


def check_comfyui() -> bool:
    """Check if ComfyUI is running."""
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
        with urllib.request.urlopen(req, timeout=5):
            return True
    except Exception:
        return False


def upload_image(image_path: str) -> str:
    """Upload a reference image to ComfyUI's input folder. Returns the filename."""
    filename = os.path.basename(image_path)

    with open(image_path, "rb") as f:
        image_data = f.read()

    # Multipart form upload
    boundary = uuid.uuid4().hex
    content_type, _ = mimetypes.guess_type(image_path)
    if content_type is None:
        content_type = "image/jpeg"

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + image_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        f"{COMFYUI_URL}/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())

    uploaded_name = result.get("name", filename)
    print(f"Uploaded reference image: {uploaded_name}", file=sys.stderr)
    return uploaded_name


def queue_prompt(prompt_workflow: dict, client_id: str) -> dict:
    """Submit a workflow to ComfyUI."""
    payload = {
        "prompt": prompt_workflow,
        "client_id": client_id,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def poll_history(prompt_id: str, timeout_s: int = 600) -> dict:
    """Poll ComfyUI history until the prompt completes."""
    start = time.time()
    while time.time() - start < timeout_s:
        time.sleep(3)
        elapsed = int(time.time() - start)
        try:
            req = urllib.request.Request(f"{COMFYUI_URL}/history/{prompt_id}")
            with urllib.request.urlopen(req, timeout=10) as resp:
                history = json.loads(resp.read().decode())
        except Exception:
            continue

        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("completed", False):
                return entry
            if status.get("status_str") == "error":
                msgs = status.get("messages", [])
                print(f"Error: {msgs}", file=sys.stderr)
                sys.exit(1)

        if elapsed % 30 == 0 and elapsed > 0:
            print(f"Generating... ({elapsed}s)", file=sys.stderr)

    print(f"Timed out after {timeout_s}s.", file=sys.stderr)
    sys.exit(1)


def download_image(prompt_id: str, history_entry: dict, output_path: str) -> bool:
    """Download the generated image from ComfyUI."""
    outputs = history_entry.get("outputs", {})
    for node_id, node_output in outputs.items():
        images = node_output.get("images", [])
        for img_info in images:
            filename = img_info["filename"]
            subfolder = img_info.get("subfolder", "")
            img_type = img_info.get("type", "output")

            params = urllib.parse.urlencode(
                {
                    "filename": filename,
                    "subfolder": subfolder,
                    "type": img_type,
                }
            )
            url = f"{COMFYUI_URL}/view?{params}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=60) as resp:
                with open(output_path, "wb") as f:
                    f.write(resp.read())
            return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="ComfyUI PuLID-Flux Face-Consistent Image Generation"
    )
    parser.add_argument("--prompt", required=True, help="Image description")
    parser.add_argument(
        "--ref-image", required=True, help="Reference face image path"
    )
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument(
        "--width", type=int, default=896, help="Image width (default: 896)"
    )
    parser.add_argument(
        "--height", type=int, default=1152, help="Image height (default: 1152)"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=28,
        help="Sampling steps (default: 28, official PuLID-Flux recommendation)",
    )
    parser.add_argument(
        "--cfg",
        type=float,
        default=4.0,
        help="Guidance scale (default: 4.0, official PuLID-Flux recommendation)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed (default: random)"
    )
    parser.add_argument(
        "--weight",
        type=float,
        default=1.0,
        help="PuLID face weight 0.0-5.0 (default: 1.0, higher = more face similarity)",
    )
    parser.add_argument(
        "--start-at",
        type=float,
        default=0.0,
        help="PuLID start timestep 0.0-1.0 (default: 0.0)",
    )
    parser.add_argument(
        "--end-at",
        type=float,
        default=1.0,
        help="PuLID end timestep 0.0-1.0 (default: 1.0)",
    )
    parser.add_argument("--output", default=None, help="Output file path")
    parser.add_argument(
        "--timeout", type=int, default=600, help="Max wait seconds (default: 600)"
    )
    args = parser.parse_args()

    # Validate ref image
    if not os.path.isfile(args.ref_image):
        print(f"Error: Reference image not found: {args.ref_image}", file=sys.stderr)
        sys.exit(1)

    # Check ComfyUI
    if not check_comfyui():
        print(
            f"Error: ComfyUI is not running at {COMFYUI_URL}",
            file=sys.stderr,
        )
        print(
            "Start it with: bash /Users/chrisliu/ComfyUI/start.sh",
            file=sys.stderr,
        )
        sys.exit(1)

    # Upload reference image
    print("Uploading reference image...", file=sys.stderr)
    ref_name = upload_image(args.ref_image)

    # Build workflow
    seed = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)
    run_id = f"pulid_api_{int(time.time())}"

    workflow = build_pulid_workflow(
        prompt=args.prompt,
        ref_image_name=ref_name,
        negative=args.negative,
        width=args.width,
        height=args.height,
        steps=args.steps,
        cfg=args.cfg,
        seed=seed,
        weight=args.weight,
        start_at=args.start_at,
        end_at=args.end_at,
        filename_prefix=run_id,
    )

    client_id = str(uuid.uuid4())

    print(
        f"Submitting PuLID-Flux workflow ({args.width}x{args.height}, "
        f"{args.steps} steps, weight={args.weight}, seed={seed})...",
        file=sys.stderr,
    )
    result = queue_prompt(workflow, client_id)
    prompt_id = result.get("prompt_id")
    if not prompt_id:
        print(f"Error: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    print(f"Prompt ID: {prompt_id}", file=sys.stderr)

    # Poll for completion
    history_entry = poll_history(prompt_id, args.timeout)

    # Determine output path
    if args.output:
        out_file = args.output
    else:
        out_file = f"generated-images/pulid-{int(time.time())}.png"

    out_dir = os.path.dirname(out_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Download
    print("Downloading image...", file=sys.stderr)
    if download_image(prompt_id, history_entry, out_file):
        full_path = os.path.abspath(out_file)
        print(f"MEDIA:{full_path}")
    else:
        print("Error: No image found in output.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
