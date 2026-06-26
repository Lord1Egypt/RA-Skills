#!/usr/bin/env python3
"""ComfyUI generation script — supports image, text-to-video, image-to-video."""

import argparse
import base64
import json
import os
import random
import shutil
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")
COMFYUI_OUTPUT = os.path.expanduser("~/ComfyUI/output")
COMFYUI_INPUT = os.path.expanduser("~/ComfyUI/input")

# ── Image defaults (Flux schnell) ──
IMG_DEFAULT_MODEL = "flux1-schnell.safetensors"
IMG_DEFAULT_VAE = "ae.safetensors"
IMG_DEFAULT_CLIP_L = "clip_l.safetensors"
IMG_DEFAULT_CLIP_T5 = "t5xxl_fp16.safetensors"
IMG_DEFAULT_STEPS = 4
IMG_DEFAULT_CFG = 1.0
IMG_DEFAULT_SAMPLER = "euler"
IMG_DEFAULT_SCHEDULER = "simple"
IMG_DEFAULT_WEIGHT_DTYPE = "fp8_e4m3fn"

# ── Video defaults (Wan2.1 T2V-1.3B) ──
VID_DEFAULT_UNET = "wan2.1_t2v_1.3B_bf16.safetensors"
VID_DEFAULT_VAE = "wan2.1_vae.pth"
VID_DEFAULT_CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
VID_DEFAULT_CLIP_I2V = "open_clip_xlm_roberta_large_vit_huge_14.pth"
VID_DEFAULT_STEPS = 20
VID_DEFAULT_CFG = 5.0
VID_DEFAULT_SAMPLER = "uni_pc_bh2"
VID_DEFAULT_SCHEDULER = "simple"
VID_DEFAULT_WIDTH = 832
VID_DEFAULT_HEIGHT = 480
VID_DEFAULT_LENGTH = 49          # frames, (length-1)//4 + 1 latent frames
VID_DEFAULT_FPS = 16


def check_server(url=COMFYUI_URL):
    try:
        urllib.request.urlopen(f"{url}/system_stats", timeout=5)
        return True
    except Exception:
        return False


def submit_prompt(workflow, url=COMFYUI_URL):
    data = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(f"{url}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read()).get("prompt_id")


def wait_for_completion(prompt_id, timeout=300, url=COMFYUI_URL):
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(2)
        try:
            resp = urllib.request.urlopen(f"{url}/history/{prompt_id}", timeout=10)
            hist = json.loads(resp.read())
            if prompt_id in hist:
                status = hist[prompt_id].get("status", {})
                if status.get("completed"):
                    outputs = hist[prompt_id].get("outputs", {})
                    images = []
                    for node_out in outputs.values():
                        if "images" in node_out:
                            for img in node_out["images"]:
                                images.append({
                                    "filename": img["filename"],
                                    "subfolder": img.get("subfolder", ""),
                                })
                    return {"status": "completed", "images": images}
                elif status.get("status_str") == "error":
                    msgs = status.get("messages", [])
                    exc = "unknown"
                    for m in reversed(msgs):
                        if m and isinstance(m, list) and len(m) > 1:
                            last = m[-1]
                            if isinstance(last, dict) and "exception_message" in last:
                                exc = last["exception_message"]
                                break
                    return {"status": "error", "message": exc}
        except Exception:
            pass
    return {"status": "timeout"}


def collect_images(result, output_path=None):
    """Collect generated images, optionally copy to output_path."""
    paths = []
    for img in result["images"]:
        sub = img["subfolder"]
        sub = sub.rstrip("/") + "/" if sub else ""
        src = os.path.join(COMFYUI_OUTPUT, sub + img["filename"])
        if output_path and os.path.exists(src):
            if output_path.endswith(".png"):
                shutil.copy2(src, output_path)
            else:
                os.makedirs(output_path, exist_ok=True)
                shutil.copy2(src, os.path.join(output_path, img["filename"]))
            paths.append(output_path if output_path.endswith(".png") else os.path.join(output_path, img["filename"]))
        else:
            paths.append(src)
    return paths


# ──────────── Image workflow ────────────

def build_image_workflow(prompt, negative_prompt="", width=1024, height=1024,
                         steps=IMG_DEFAULT_STEPS, seed=None, model=IMG_DEFAULT_MODEL,
                         weight_dtype=IMG_DEFAULT_WEIGHT_DTYPE):
    if seed is None:
        seed = random.randint(0, 2**32)
    return {
        "3": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": steps, "cfg": IMG_DEFAULT_CFG,
            "sampler_name": IMG_DEFAULT_SAMPLER, "scheduler": IMG_DEFAULT_SCHEDULER,
            "denoise": 1.0, "model": ["10", 0],
            "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {
            "width": width, "height": height, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {
            "text": prompt, "clip": ["11", 0]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {
            "text": negative_prompt, "clip": ["11", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {
            "samples": ["3", 0], "vae": ["9", 0]}},
        "9": {"class_type": "VAELoader", "inputs": {"vae_name": IMG_DEFAULT_VAE}},
        "10": {"class_type": "UNETLoader", "inputs": {
            "unet_name": model, "weight_dtype": weight_dtype}},
        "11": {"class_type": "DualCLIPLoader", "inputs": {
            "clip_name1": IMG_DEFAULT_CLIP_L, "clip_name2": IMG_DEFAULT_CLIP_T5, "type": "flux"}},
        "12": {"class_type": "SaveImage", "inputs": {
            "filename_prefix": "NovaGen", "images": ["8", 0]}},
    }


# ──────────── Video: Text-to-Video ────────────

def build_t2v_workflow(prompt, negative_prompt="", width=VID_DEFAULT_WIDTH,
                        height=VID_DEFAULT_HEIGHT, length=VID_DEFAULT_LENGTH,
                        steps=VID_DEFAULT_STEPS, seed=None,
                        unet=VID_DEFAULT_UNET):
    if seed is None:
        seed = random.randint(0, 2**32)
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": unet, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": VID_DEFAULT_CLIP, "type": "wan"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VID_DEFAULT_VAE}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {
            "text": prompt, "clip": ["2", 0]}},
        "5": {"class_type": "WanImageToVideo", "inputs": {
            "positive": ["4", 0], "negative": ["4", 0],
            "vae": ["3", 0], "width": width, "height": height,
            "length": length, "batch_size": 1}},
        "6": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": steps, "cfg": VID_DEFAULT_CFG,
            "sampler_name": VID_DEFAULT_SAMPLER, "scheduler": VID_DEFAULT_SCHEDULER,
            "denoise": 1.0, "model": ["1", 0],
            "positive": ["5", 0], "negative": ["5", 1], "latent_image": ["5", 2]}},
        "7": {"class_type": "VAEDecode", "inputs": {
            "samples": ["6", 0], "vae": ["3", 0]}},
        "8": {"class_type": "SaveImage", "inputs": {
            "filename_prefix": "WanT2V", "images": ["7", 0]}},
    }


# ──────────── Video: Image-to-Video ────────────

def upload_image(image_path, url=COMFYUI_URL):
    """Upload an image to ComfyUI input directory via API."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    filename = os.path.basename(image_path)
    # Copy to input dir as fallback
    os.makedirs(COMFYUI_INPUT, exist_ok=True)
    dst = os.path.join(COMFYUI_INPUT, filename)
    shutil.copy2(image_path, dst)

    # Also upload via API
    with open(image_path, "rb") as f:
        boundary = "----ComfyUIFormBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
            f"Content-Type: image/png\r\n\r\n"
        ).encode() + f.read() + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        f"{url}/upload/image", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass  # file already copied to input dir
    return filename


def build_i2v_workflow(prompt, image_filename, negative_prompt="",
                        width=VID_DEFAULT_WIDTH, height=VID_DEFAULT_HEIGHT,
                        length=VID_DEFAULT_LENGTH, steps=VID_DEFAULT_STEPS, seed=None):
    if seed is None:
        seed = random.randint(0, 2**32)
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": VID_DEFAULT_UNET, "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": VID_DEFAULT_CLIP, "type": "wan"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": VID_DEFAULT_VAE}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {
            "text": prompt, "clip": ["2", 0]}},
        "5": {"class_type": "LoadImage", "inputs": {"image": image_filename}},
        "6": {"class_type": "WanImageToVideo", "inputs": {
            "positive": ["4", 0], "negative": ["4", 0],
            "vae": ["3", 0], "width": width, "height": height,
            "length": length, "batch_size": 1,
            "start_image": ["5", 0]}},
        "7": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": steps, "cfg": VID_DEFAULT_CFG,
            "sampler_name": VID_DEFAULT_SAMPLER, "scheduler": VID_DEFAULT_SCHEDULER,
            "denoise": 1.0, "model": ["1", 0],
            "positive": ["6", 0], "negative": ["6", 1], "latent_image": ["6", 2]}},
        "8": {"class_type": "VAEDecode", "inputs": {
            "samples": ["7", 0], "vae": ["3", 0]}},
        "9": {"class_type": "SaveImage", "inputs": {
            "filename_prefix": "WanI2V", "images": ["8", 0]}},
    }


def ensure_server(url=COMFYUI_URL):
    if not check_server(url):
        print("ERROR: ComfyUI server is not running.", file=sys.stderr)
        print("Start it with:", file=sys.stderr)
        print("  cd ~/ComfyUI && LD_LIBRARY_PATH=~/comfyui-venv/lib/python3.12/site-packages/nvidia/cuda_runtime/lib:$LD_LIBRARY_PATH ~/comfyui-venv/bin/python main.py --listen 127.0.0.1 --port 8188", file=sys.stderr)
        sys.exit(1)


# ──────────── Main ────────────

def main():
    parser = argparse.ArgumentParser(description="Generate images/videos with ComfyUI")
    sub = parser.add_subparsers(dest="mode")

    # image subcommand
    p_img = sub.add_parser("image", help="Generate image (Flux schnell)")
    p_img.add_argument("--prompt", required=True)
    p_img.add_argument("--negative", default="")
    p_img.add_argument("--width", type=int, default=1024)
    p_img.add_argument("--height", type=int, default=1024)
    p_img.add_argument("--steps", type=int, default=IMG_DEFAULT_STEPS)
    p_img.add_argument("--seed", type=int, default=None)
    p_img.add_argument("--output", default=None)
    p_img.add_argument("--model", default=IMG_DEFAULT_MODEL)
    p_img.add_argument("--weight-dtype", default=IMG_DEFAULT_WEIGHT_DTYPE)
    p_img.add_argument("--wait", type=int, default=120)
    p_img.add_argument("--url", default=COMFYUI_URL)

    # t2v subcommand
    p_t2v = sub.add_parser("t2v", help="Text-to-Video (Wan2.1 T2V-1.3B)")
    p_t2v.add_argument("--prompt", required=True)
    p_t2v.add_argument("--negative", default="")
    p_t2v.add_argument("--width", type=int, default=VID_DEFAULT_WIDTH)
    p_t2v.add_argument("--height", type=int, default=VID_DEFAULT_HEIGHT)
    p_t2v.add_argument("--length", type=int, default=VID_DEFAULT_LENGTH,
                       help="Number of frames (default 49 ≈ 3s at 16fps)")
    p_t2v.add_argument("--steps", type=int, default=VID_DEFAULT_STEPS)
    p_t2v.add_argument("--seed", type=int, default=None)
    p_t2v.add_argument("--output", default=None)
    p_t2v.add_argument("--unet", default=VID_DEFAULT_UNET)
    p_t2v.add_argument("--wait", type=int, default=300)
    p_t2v.add_argument("--url", default=COMFYUI_URL)

    # i2v subcommand
    p_i2v = sub.add_parser("i2v", help="Image-to-Video (Wan2.1 T2V-1.3B + image)")
    p_i2v.add_argument("--prompt", required=True)
    p_i2v.add_argument("--image", required=True, help="Path to input image")
    p_i2v.add_argument("--negative", default="")
    p_i2v.add_argument("--width", type=int, default=VID_DEFAULT_WIDTH)
    p_i2v.add_argument("--height", type=int, default=VID_DEFAULT_HEIGHT)
    p_i2v.add_argument("--length", type=int, default=VID_DEFAULT_LENGTH)
    p_i2v.add_argument("--steps", type=int, default=VID_DEFAULT_STEPS)
    p_i2v.add_argument("--seed", type=int, default=None)
    p_i2v.add_argument("--output", default=None)
    p_i2v.add_argument("--wait", type=int, default=300)
    p_i2v.add_argument("--url", default=COMFYUI_URL)

    args = parser.parse_args()
    url = getattr(args, "url", COMFYUI_URL)
    ensure_server(url)

    if args.mode == "image":
        wf = build_image_workflow(
            prompt=args.prompt, negative_prompt=args.negative,
            width=args.width, height=args.height, steps=args.steps,
            seed=args.seed, model=args.model, weight_dtype=args.weight_dtype)
        print(f"📷 Image: \"{args.prompt}\" ({args.width}×{args.height}, {args.steps} steps)")

    elif args.mode == "t2v":
        wf = build_t2v_workflow(
            prompt=args.prompt, negative_prompt=args.negative,
            width=args.width, height=args.height, length=args.length,
            steps=args.steps, seed=args.seed, unet=args.unet)
        duration = round(args.length / VID_DEFAULT_FPS, 1)
        print(f"🎬 T2V: \"{args.prompt}\" ({args.width}×{args.height}, {args.length} frames ≈ {duration}s, {args.steps} steps)")

    elif args.mode == "i2v":
        img_filename = upload_image(args.image, url)
        wf = build_i2v_workflow(
            prompt=args.prompt, image_filename=img_filename,
            negative_prompt=args.negative,
            width=args.width, height=args.height, length=args.length,
            steps=args.steps, seed=args.seed)
        duration = round(args.length / VID_DEFAULT_FPS, 1)
        print(f"🎬 I2V: image={img_filename}, prompt=\"{args.prompt}\" ({args.length} frames ≈ {duration}s, {args.steps} steps)")

    else:
        parser.print_help()
        sys.exit(1)

    prompt_id = submit_prompt(wf, url)
    print(f"   Prompt ID: {prompt_id}")

    result = wait_for_completion(prompt_id, timeout=args.wait, url=url)

    if result["status"] == "completed":
        paths = collect_images(result, args.output)
        seed_val = None
        for node in wf.values():
            inputs = node.get("inputs", {})
            if "seed" in inputs:
                seed_val = inputs["seed"]
                break
        print(f"✅ Generated {len(paths)} frame(s)")
        if seed_val is not None:
            print(f"   Seed: {seed_val}")
        for p in paths[:5]:
            print(f"   → {p}")
        if len(paths) > 5:
            print(f"   ... and {len(paths)-5} more frames")
    elif result["status"] == "timeout":
        print(f"⏰ Timed out after {args.wait}s", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"❌ Error: {result.get('message', 'unknown')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
