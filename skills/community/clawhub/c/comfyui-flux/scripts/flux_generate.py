#!/usr/bin/env python3
"""Generate images locally via ComfyUI + Flux.1 Dev.

Submits a Flux workflow to ComfyUI's API, polls for completion, and downloads the result.

Usage:
  python3 flux_generate.py --prompt "..." [OPTIONS]

Requires ComfyUI running at http://127.0.0.1:8188
"""

import argparse
import json
import os
import random
import sys
import time
import urllib.request
import urllib.error
import uuid

COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8200")

# Flux.1 Dev API workflow template
FLUX_WORKFLOW = {
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["11", 0],
            "text": ""
        }
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": ["13", 0],
            "vae": ["10", 0]
        }
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "flux_api",
            "images": ["8", 0]
        }
    },
    "10": {
        "class_type": "VAELoader",
        "inputs": {
            "vae_name": "ae.safetensors"
        }
    },
    "11": {
        "class_type": "DualCLIPLoader",
        "inputs": {
            "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
            "clip_name2": "clip_l.safetensors",
            "type": "flux"
        }
    },
    "12": {
        "class_type": "UNETLoader",
        "inputs": {
            "unet_name": "flux1-dev.safetensors",
            "weight_dtype": "default"
        }
    },
    "13": {
        "class_type": "KSampler",
        "inputs": {
            "cfg": 1.0,
            "denoise": 1.0,
            "latent_image": ["14", 0],
            "model": ["12", 0],
            "negative": ["15", 0],
            "positive": ["6", 0],
            "sampler_name": "euler",
            "scheduler": "simple",
            "seed": 0,
            "steps": 20
        }
    },
    "14": {
        "class_type": "EmptySD3LatentImage",
        "inputs": {
            "batch_size": 1,
            "height": 1024,
            "width": 1024
        }
    },
    "15": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["11", 0],
            "text": ""
        }
    }
}


def check_comfyui():
    """Check if ComfyUI is running."""
    try:
        req = urllib.request.Request(f"{COMFYUI_URL}/system_stats")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return True
    except Exception:
        return False


def queue_prompt(prompt_workflow, client_id):
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


def poll_history(prompt_id, timeout_s=600):
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


def download_image(prompt_id, history_entry, output_path):
    """Download the generated image from ComfyUI."""
    outputs = history_entry.get("outputs", {})
    for node_id, node_output in outputs.items():
        images = node_output.get("images", [])
        for img_info in images:
            filename = img_info["filename"]
            subfolder = img_info.get("subfolder", "")
            img_type = img_info.get("type", "output")

            params = urllib.parse.urlencode({
                "filename": filename,
                "subfolder": subfolder,
                "type": img_type,
            })
            url = f"{COMFYUI_URL}/view?{params}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=60) as resp:
                with open(output_path, "wb") as f:
                    f.write(resp.read())
            return True
    return False


def main():
    import urllib.parse  # needed for download

    parser = argparse.ArgumentParser(description="ComfyUI Flux.1 Dev Image Generation")
    parser.add_argument("--prompt", required=True, help="Image description")
    parser.add_argument("--negative", default="", help="Negative prompt")
    parser.add_argument("--width", type=int, default=1024, help="Image width (default: 1024)")
    parser.add_argument("--height", type=int, default=1024, help="Image height (default: 1024)")
    parser.add_argument("--steps", type=int, default=20, help="Sampling steps (default: 20)")
    parser.add_argument("--cfg", type=float, default=1.0, help="CFG scale (default: 1.0, Flux works best at 1.0)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (default: random)")
    parser.add_argument("--output", default=None, help="Output file path")
    parser.add_argument("--timeout", type=int, default=600, help="Max wait seconds")
    args = parser.parse_args()

    # Check ComfyUI
    if not check_comfyui():
        print("Error: ComfyUI is not running at http://127.0.0.1:8188", file=sys.stderr)
        print("Start it with: cd /Users/chrisliu/ComfyUI && python main.py", file=sys.stderr)
        sys.exit(1)

    # Build workflow
    workflow = json.loads(json.dumps(FLUX_WORKFLOW))
    workflow["6"]["inputs"]["text"] = args.prompt
    workflow["15"]["inputs"]["text"] = args.negative
    workflow["14"]["inputs"]["width"] = args.width
    workflow["14"]["inputs"]["height"] = args.height
    workflow["13"]["inputs"]["steps"] = args.steps
    workflow["13"]["inputs"]["cfg"] = args.cfg
    workflow["13"]["inputs"]["seed"] = args.seed if args.seed is not None else random.randint(0, 2**32 - 1)

    # Set unique filename prefix to identify our output
    run_id = f"flux_api_{int(time.time())}"
    workflow["9"]["inputs"]["filename_prefix"] = run_id

    client_id = str(uuid.uuid4())

    print(f"Submitting to ComfyUI (Flux.1 Dev, {args.width}x{args.height}, {args.steps} steps)...", file=sys.stderr)
    result = queue_prompt(workflow, client_id)
    prompt_id = result.get("prompt_id")
    if not prompt_id:
        print(f"Error: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    print(f"Prompt ID: {prompt_id}", file=sys.stderr)

    # Poll
    history_entry = poll_history(prompt_id, args.timeout)

    # Determine output path
    if args.output:
        out_file = args.output
    else:
        out_file = f"generated-images/flux-{int(time.time())}.png"

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
    # Ensure urllib.parse is available
    import urllib.parse
    main()
