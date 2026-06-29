#!/usr/bin/env python3
"""Generate images or edit existing images using ChatArt Common Task APIs.

## AGENT INSTRUCTIONS — READ FIRST
- Default workflow: ALWAYS use `run` (submit + auto-poll).
  Do NOT ask the user to run query manually.
- Only use `query` when `run` has already timed out and a taskId exists,
  or when the user explicitly provides a taskId to resume.
- When using `query`, keep polling (default timeout=600s) until
  status is 'completed' or 'failed'. Do NOT stop after a single check.
- Never hand a pending taskId back to the user and say "check it later".
  Always poll to completion within the timeout window.

Supported task types:
    text2image   Text-to-Image  — generate images from a text prompt
    image_edit   Image Edit     — edit images with prompt + reference images

Subcommands:
    run           Submit task AND poll until done — DEFAULT, use this first
    submit        Submit only, print taskId, exit — use for parallel batch jobs
    query         Poll an existing taskId until done (or timeout) — use for recovery
    list-models   Show supported models and parameter constraints
    estimate-cost Estimate credit cost before running

Usage:
    python ai_image.py run  --type text2image --model "Nano Banana" --prompt "..." [options]
    python ai_image.py run  --type image_edit --model "Nano Banana" --prompt "..." --input-images <image url|local paths> [options]
    python ai_image.py submit --type <text2image|image_edit> [task-specific options]
    python ai_image.py query  --type <text2image|image_edit> --task-id <taskId> [options]
"""

import argparse
import json as json_mod
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(__file__))

from shared.client import ChatArtClient, ChatArtError, TaskStatus
from shared.upload import resolve_local_file

TASK_TYPES = ("text2image", "image_edit")

ENDPOINTS = {
    "text2image": {
        "submit": "/web/art/create",
        "query": "/web/art/get-draw-task",
    },
    "image_edit": {
        "submit": "/web/art/create",
        "query": "/web/art/get-draw-task",
    },
}

DEFAULT_TIMEOUT = 1200
DEFAULT_INTERVAL = 30

# ---------------------------------------------------------------------------
# Model constraints
# Each entry: { "aspectRatio": list, "resolution": list|None, "maxImages": int }
#   resolution=None means the model does NOT support resolution (do not send).
#   resolution=[...] means the parameter is required.
# ---------------------------------------------------------------------------

TEXT2IMAGE_MODELS = {
    "Gpt Image 2":      {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16", "5:4", "4:5"],      "resolution": ["1K", "2K", "4K"], "model_id": 2, "quality": ["low", "medium", "high"]},
    "Nano Banana 2":    {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["2K", "4K"], "model_id": 9, "quality": None},
    "Nano Banana Pro":  {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["2K", "4K"], "model_id": 4, "quality": None},
    "Seedream 5.0":     {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["2K", "3K"], "model_id": 5, "quality": None},
}

IMAGE_EDIT_MODELS = {
    "Gpt Image 2":      {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16", "5:4", "4:5"],      "resolution": ["1K", "2K", "4K"], "model_id": 2, "quality": ["low", "medium", "high"]},
    "Nano Banana 2":    {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["2K", "4K"], "model_id": 9, "quality": None},
    "Nano Banana Pro":  {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["2K", "4K"], "model_id": 4, "quality": None},
    "Seedream 5.0":     {"aspectRatio": ["1:1", "4:3", "3:4", "3:2", "2:3", "16:9", "9:16"],                    "resolution": ["2K", "3K"], "model_id": 8, "quality": None},
}

MODEL_REGISTRY = {"text2image": TEXT2IMAGE_MODELS, "image_edit": IMAGE_EDIT_MODELS}

# ---------------------------------------------------------------------------
# Pricing — credits per task (exact lookup table based on model + resolution + quality).
# Key format: "model|resolution" -> {1: totalCost}
# For models without quality, use "model|resolution" (quality=None in registry).
# Gpt Image 2 uses quality-based pricing: "Gpt Image 2|default|low|medium|high"
# ---------------------------------------------------------------------------

_PRICING = {
    "text2image": {
        # Gpt Image 2 — resolution + quality pricing
        "Gpt Image 2|1K|low":     {1: 6},
        "Gpt Image 2|1K|medium":   {1: 20},
        "Gpt Image 2|1K|high":     {1: 70},
        "Gpt Image 2|2K|low":     {1: 8},
        "Gpt Image 2|2K|medium":   {1: 30},
        "Gpt Image 2|2K|high":     {1: 100},
        "Gpt Image 2|4K|low":     {1: 10},
        "Gpt Image 2|4K|medium":   {1: 50},
        "Gpt Image 2|4K|high":     {1: 180},
        # Other models
        "Nano Banana 2|2K":   {1: 6},
        "Nano Banana 2|4K":   {1: 10},
        "Nano Banana Pro|2K": {1: 10},
        "Nano Banana Pro|4K": {1: 16},
        "Seedream 5.0|2K":    {1: 6},
        "Seedream 5.0|3K":    {1: 10},
    },
    "image_edit": {
        # Gpt Image 2 — resolution + quality pricing
        "Gpt Image 2|1K|low":     {1: 6},
        "Gpt Image 2|1K|medium":   {1: 20},
        "Gpt Image 2|1K|high":     {1: 70},
        "Gpt Image 2|2K|low":     {1: 8},
        "Gpt Image 2|2K|medium":   {1: 30},
        "Gpt Image 2|2K|high":     {1: 100},
        "Gpt Image 2|4K|low":     {1: 10},
        "Gpt Image 2|4K|medium":   {1: 50},
        "Gpt Image 2|4K|high":     {1: 180},
        # Other models
        "Nano Banana 2|2K":   {1: 6},
        "Nano Banana 2|4K":   {1: 10},
        "Nano Banana Pro|2K": {1: 10},
        "Nano Banana Pro|4K": {1: 16},
        "Seedream 5.0|2K":    {1: 6},
        "Seedream 5.0|3K":    {1: 10},
    },
}

MODEL_MAP = {
    "Gpt Image 2": "gpt-image-2",
    "Nano Banana 2": "nano-banana-2",
    "Nano Banana Pro": "nano-banana-pro",
    "Seedream 5.0": "seedream-5.0-lite",
}

def get_model_id_by_name(model_name: str) -> str | None:
    """
    根据模型名称获取对应的模型 ID（忽略大小写比较）。
    
    Args:
        model_name: 模型名称
        
    Returns:
        模型 ID，如果未找到则返回 None
    """
    model_name_lower = model_name.lower()
    for name, model_id in MODEL_MAP.items():
        if name.lower() == model_name_lower:
            return model_id
    
    return None


def get_picture_scale_value(aspect_ratio: str) -> int | None:
    """
    根据宽高比字符串获取对应的 picture_scale value 值。
    
    Args:
        aspect_ratio: 宽高比字符串,如 '1:1', '9:16', '16:9', '3:4', '4:3', '2:3', '3:2'
        
    Returns:
        对应的 value 值,如果未找到则返回 None
        
    Examples:
        >>> get_picture_scale_value('1:1')
        1
        >>> get_picture_scale_value('4:3')
        5
        >>> get_picture_scale_value('9:16')
        2
    """
    scale_map = {
        '1:1': 1,
        '9:16': 2,
        '16:9': 3,
        '3:4': 4,
        '4:3': 5,
        '3:2': 6,
        '2:3': 7,
        '5:4': 8,
        '4:5': 9,
        '21:9': 10,
    }
    
    return scale_map.get(aspect_ratio)

def get_image_definition_value(quality: str) -> int | None:
    """
    根据质量字符串获取对应的 image_definition value 值。
    
    Args:
        quality: 质量字符串,如 '1K', '2K', '3K', '4K'
        
    Returns:
        对应的 value 值,如果未找到则返回 None
        
    Examples:
        >>> get_image_definition_value('1K')
        1
        >>> get_image_definition_value('2K')
        2
        >>> get_image_definition_value('4K')
        4
        >>> get_image_definition_value('3K')
        3
    """
    definition_map = {
        '1K': 1,
        '2K': 2,
        '3K': 4,
        '4K': 3,
    }
    
    # 转换为大写以支持大小写不敏感匹配
    quality_upper = quality.upper() if quality else None

    return definition_map.get(quality_upper)

def get_quality_level_value(quality: str) -> str | None:
    """
    根据品质字符串获取对应的 quality_level value 值。

    Args:
        quality: 品质字符串, 如 'low', 'medium', 'high'

    Returns:
        对应的 value 值,如果未找到则返回 None

    Examples:
        >>> get_quality_level_value('low')
        1
        >>> get_quality_level_value('medium')
        2
        >>> get_quality_level_value('high')
        3
    """
    quality_map = {
        'low': 'low',
        'medium': 'medium',
        'high': 'high',
    }

    quality_lower = quality.lower() if quality else None

    return quality_map.get(quality_lower)

def estimate_cost(task_type: str, model: str, resolution: str | None, quality: str | None = None) -> float | None:
    """Return estimated total cost in credits, or None if model/params unknown.

    Uses exact lookup table based on model + resolution + quality.
    For models without quality support, quality is ignored.
    """
    registry = MODEL_REGISTRY.get(task_type, {})
    model_spec = registry.get(model, {})
    model_quality = model_spec.get("quality")
    model_resolution = model_spec.get("resolution")

    # Use actual resolution if model supports it, else "default"
    res_key = resolution if (model_resolution and resolution) else "default"

    if model_quality and quality:
        pricing_key = f"{model}|{res_key}|{quality}"
    else:
        pricing_key = f"{model}|{res_key}"

    prices = _PRICING.get(task_type, {}).get(pricing_key)
    if not prices:
        return None

    return float(prices.get(1))

def get_model_id(task_type: str, model: str, quiet: bool) -> int:
    """Warn on stderr if parameters are incompatible with model constraints."""
    model_id = 9
    registry = MODEL_REGISTRY.get(task_type, {})
    if model not in registry:
        if not quiet:
            known = ", ".join(sorted(registry.keys()))
            print(
                f"Warning: unknown model '{model}' for {task_type}. "
                f"Known models: {known}",
                file=sys.stderr,
            )
        return model_id

    spec = registry[model]
    return spec.get("model_id", 9)

def validate_model_params(task_type: str, model: str, aspect_ratio: str | None,
                          resolution: str | None, quality: str | None, quiet: bool) -> None:
    """Warn on stderr if parameters are incompatible with model constraints."""
    registry = MODEL_REGISTRY.get(task_type, {})
    if model not in registry:
        if not quiet:
            known = ", ".join(sorted(registry.keys()))
            print(
                f"Warning: unknown model '{model}' for {task_type}. "
                f"Known models: {known}",
                file=sys.stderr,
            )
        return

    spec = registry[model]

    if aspect_ratio and aspect_ratio not in spec["aspectRatio"]:
        if not quiet:
            print(
                f"Warning: model '{model}' supports aspectRatio "
                f"{spec['aspectRatio']}, got '{aspect_ratio}'.",
                file=sys.stderr,
            )

    if resolution and spec["resolution"] is None:
        if not quiet:
            print(
                f"Warning: model '{model}' does not support resolution "
                f"(got '{resolution}'). Do NOT send this parameter.",
                file=sys.stderr,
            )
    elif resolution and spec["resolution"] and resolution not in spec["resolution"]:
        if not quiet:
            print(
                f"Warning: model '{model}' supports resolution "
                f"{spec['resolution']}, got '{resolution}'.",
                file=sys.stderr,
            )
    elif not resolution and spec["resolution"] is not None:
        if not quiet:
            print(
                f"Warning: model '{model}' requires resolution "
                f"(one of {spec['resolution']}). Please provide --resolution.",
                file=sys.stderr,
            )

    # Validate quality
    model_quality = spec.get("quality")
    if quality and model_quality is None:
        if not quiet:
            print(
                f"Warning: model '{model}' does not support quality parameter "
                f"(got '{quality}'). This parameter will be ignored.",
                file=sys.stderr,
            )
    elif quality and model_quality and quality not in model_quality:
        if not quiet:
            print(
                f"Warning: model '{model}' supports quality "
                f"{model_quality}, got '{quality}'.",
                file=sys.stderr,
            )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resolve_file(client: ChatArtClient, file_ref: str, quiet: bool) -> str:
    """If file_ref looks like a local path, upload it and return fileId."""
    return resolve_local_file(file_ref, quiet=quiet, client=client)


def build_text2image_body(args, model_id) -> dict:
    body = {
        "style": 10,
        "scene_id": 4,
        "reference_image": [],
        "gen_content": "",
        "content": {
            "text": "",
            "site_url": ""
        },
        "description": args.prompt,
        "picture_counts": 1,
    }

    if args.aspect_ratio:
        body["picture_scale"] = get_picture_scale_value(args.aspect_ratio)

    if args.model:
        body["gpt_type"] = get_model_id_by_name(args.model)

    if args.resolution:
        body["image_definition"] = get_image_definition_value(args.resolution)

    # Gpt Image 2 supports quality levels
    if getattr(args, "quality", None):
        registry = MODEL_REGISTRY.get("text2image", {})
        model_spec = registry.get(args.model, {})
        if model_spec.get("quality"):
            body["quality"] = get_quality_level_value(args.quality)

    return body


def build_image_edit_body(args, model_id, client: ChatArtClient) -> dict:
    body = {
        "style": 0,
        "scene_id": 13,
        "reference_image": [],
        "gen_content": "",
        "content": {
            "text": "",
            "site_url": ""
        },
        "description": args.prompt,
        "picture_counts": 1,
    }

    image_urls = []
    if args.input_images:
        # body["img_url"] = resolve_file(client, args.input_images, args.quiet)
        # 多张图遍历
        for ref in args.input_images:
            if os.path.isfile(ref):
                image_urls.append(resolve_file(client, ref, args.quiet))
            else:
                image_urls.append(ref)

    if image_urls:
        body["reference_image"] = image_urls

    if args.aspect_ratio:
        body["picture_scale"] = get_picture_scale_value(args.aspect_ratio)

    if args.model:
        body["gpt_type"] = get_model_id_by_name(args.model)

    if args.resolution:
        body["image_definition"] = get_image_definition_value(args.resolution)

    # Gpt Image 2 supports quality levels
    if getattr(args, "quality", None):
        registry = MODEL_REGISTRY.get("image_edit", {})
        model_spec = registry.get(args.model, {})
        if model_spec.get("quality"):
            body["quality"] = get_quality_level_value(args.quality)

    return body


def build_body(args, client: ChatArtClient) -> dict:
    """Dispatch to the type-specific body builder, with model constraint checks."""
    validate_model_params(
        args.type, args.model,
        getattr(args, "aspect_ratio", None),
        getattr(args, "resolution", None),
        getattr(args, "quality", None),
        args.quiet,
    )

    model_id = get_model_id(args.type, args.model, args.quiet)
    if args.type == "text2image":
        return build_text2image_body(args, model_id)
    elif args.type == "image_edit":
        return build_image_edit_body(args, model_id, client)
    raise ValueError(f"Unknown type: {args.type}")


def do_submit(client: ChatArtClient, task_type: str, body: dict, quiet: bool) -> str:
    """POST submit task, return taskId."""
    path = ENDPOINTS[task_type]["submit"]
    label = {"text2image": "text-to-image", "image_edit": "image-edit"}
    if not quiet:
        print(f"Submitting {label[task_type]} task...", file=sys.stderr)
    result = client.post(path, json=body)
    # 打印result
    # print(f"result: {result}", file=sys.stderr)

    task_id = result["question_id"]
    if not quiet:
        print(f"Task submitted. taskId: {task_id}", file=sys.stderr)
    return task_id


def do_poll(client: ChatArtClient, task_type: str, task_id: str,
            timeout: float, interval: float, quiet: bool) -> dict:
    """Poll until status is terminal or timeout is exceeded."""
    path = ENDPOINTS[task_type]["query"] + f"?question_id={task_id}"
    if not quiet:
        print(
            f"Polling task {task_id} (timeout={timeout}s, interval={interval}s)...",
            file=sys.stderr,
        )
    return client.poll_task(
        path,
        task_id,
        interval=interval,
        timeout=timeout,
        verbose=not quiet,
    )


def download_image(url: str, output: str, quiet: bool) -> None:
    """Download an image from URL to a local file."""
    import requests as req

    if not quiet:
        print(f"Downloading image to {output}...", file=sys.stderr)

    resp = req.get(url, stream=True)
    resp.raise_for_status()

    with open(output, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    if not quiet:
        size_kb = os.path.getsize(output) / 1024
        print(f"Downloaded: {output} ({size_kb:.1f} KB)", file=sys.stderr)


def print_result(result: dict, args, client: ChatArtClient) -> None:
    """Print final result: image URLs by default, full JSON with --json."""

    status = result.get("status", 0)
    
    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
        return
    
    cost = result.get("cost_credit", "N/A")
    print(f"status: {status}  cost: {cost} credits")
    
    # Extract images from message array
    message = result.get("message", [])
    if not isinstance(message, list):
        message = []
    
    if status == 1 and message:
        for i, img in enumerate(message):
            url = img.get("url", "")
            
            if url:
                if args.output_dir:
                    os.makedirs(args.output_dir, exist_ok=True)
                    ext = "png"
                    time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    out_path = os.path.join(args.output_dir, f"image_{time_name}_{i+1}.{ext}")
                    download_image(url, out_path, args.quiet)
                
                print(f" [{i+1}] image_url:{url}")
    elif status != 1:
        error_msg = result.get("error", "") or result.get("real_error", "") or result.get("output_message", "")
        print(f"  [1] failed: {error_msg or 'Unknown error'}")



# ---------------------------------------------------------------------------
# Argument definitions
# ---------------------------------------------------------------------------

def add_common_args(p):
    """Add arguments shared by all task types."""
    p.add_argument("--type", required=True, choices=TASK_TYPES,
                   help="Task type: text2image or image_edit")
    p.add_argument("--model", required=True,
                   help='Model display name, e.g. "Nano Banana", "Seedream 5.0"')
    p.add_argument("--prompt", required=True,
                   help="Text prompt describing the image to generate or the edit to apply")
    p.add_argument("--aspect-ratio", required=True,
                   help='Aspect ratio, e.g. "16:9", "1:1"')
    p.add_argument("--resolution", default="1K",
                   help='Resolution: "1K", "2K", "4K" (model-dependent, some require it, some forbid it)')
    p.add_argument("--quality", default="medium", choices=["low", "medium", "high"],
                   help='Image quality: "low", "medium", "high" (only Gpt Image 2 supports this; other models ignore it)')

def add_image_edit_args(p):
    """Add image-edit specific arguments."""
    p.add_argument("--input-images", nargs="+", default=None,
                   help="Reference image urls or local paths for image editing (supports multiple images)")


def add_poll_args(p):
    """Add polling control arguments."""
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Max polling time in seconds (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                   help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})")


def add_output_args(p):
    """Add output/download arguments."""
    p.add_argument("--output-dir", default=None,
                   help="Download result images to this directory")
    p.add_argument("--json", action="store_true",
                   help="Output full JSON response")
    p.add_argument("-q", "--quiet", action="store_true",
                   help="Suppress status messages on stderr")


def validate_args(args, parser):
    """Validate type-specific required arguments."""
    if args.type == "image_edit":
        if not args.input_images:
            parser.error("--input-images is required for image_edit")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_list_models(args, parser):
    """Print supported models and their parameter constraints."""
    task_type = args.type
    registry = MODEL_REGISTRY.get(task_type, {})
    if not registry:
        print(f"No models registered for type '{task_type}'.")
        return

    if args.json:
        print(json_mod.dumps(registry, indent=2, ensure_ascii=False))
        return

    type_label = {"text2image": "Text-to-Image", "image_edit": "Image Edit"}
    print(f"\n{type_label.get(task_type, task_type)} - Supported Models\n")

    if task_type == "image_edit":
        print(f"{'Model':<22} {'Aspect Ratio':<45} {'Resolution':<22} {'Quality':<15}")
        print("-" * 110)
        for name, spec in registry.items():
            ar = ", ".join(spec["aspectRatio"])
            res = ", ".join(spec["resolution"]) if spec["resolution"] else "N/A (forbidden)"
            qual = ", ".join(spec["quality"]) if spec["quality"] else "N/A"
            print(f"{name:<22} {ar:<45} {res:<22} {qual:<15}")
    else:
        print(f"{'Model':<22} {'Aspect Ratio':<45} {'Resolution':<22} {'Quality':<15}")
        print("-" * 110)
        for name, spec in registry.items():
            ar = ", ".join(spec["aspectRatio"])
            res = ", ".join(spec["resolution"]) if spec["resolution"] else "N/A (forbidden)"
            qual = ", ".join(spec["quality"]) if spec["quality"] else "N/A"
            print(f"{name:<22} {ar:<45} {res:<22} {qual:<15}")
    print()


def cmd_estimate_cost(args, parser):
    """Print estimated cost for a given model + parameters."""
    cost = estimate_cost(args.type, args.model, args.resolution, args.quality)
    if cost is None:
        print(f"Cannot estimate cost for model '{args.model}' with given parameters.", file=sys.stderr)
        print("Use list-models to see available models, or check references/api-docs.md.", file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(json_mod.dumps({"type": args.type, "model": args.model,
                               "resolution": args.resolution or "default",
                               "quality": args.quality,
                               "totalCost": cost}))
    else:
        print(f"type: {args.type}  model: {args.model}  "
              f"resolution: {args.resolution or 'default'}  quality: {args.quality or 'N/A'}")
        print(f"estimated cost: {cost} credits")


def cmd_run(args, parser):
    """Submit task then poll until done — full flow (default)."""
    validate_args(args, parser)
    client = ChatArtClient()
    body = build_body(args, client)
    task_id = do_submit(client, args.type, body, args.quiet)
    result = do_poll(client, args.type, task_id, args.timeout, args.interval, args.quiet)
    # print(f"result: {result}")
    print_result(result, args, client)


def cmd_submit(args, parser):
    """Submit task only — print taskId and exit immediately."""
    validate_args(args, parser)
    client = ChatArtClient()
    body = build_body(args, client)
    task_id = do_submit(client, args.type, body, args.quiet)
    print(task_id)


def cmd_query(args, parser):
    """Poll an existing task by taskId until done or timeout."""
    client = ChatArtClient()
    try:
        result = do_poll(
            client, args.type, args.task_id,
            args.timeout, args.interval, args.quiet,
        )
        print_result(result, args, client)
    except TimeoutError as e:
        if not args.quiet:
            print(f"Timeout reached: {e}", file=sys.stderr)
            print("Fetching last known status...", file=sys.stderr)
        path = ENDPOINTS[args.type]["query"]
        last = client.get(path, json={"create_id": args.task_id})
        status = last.get("status")
        task_id = last.get("taskId", args.task_id)
        if args.json:
            print(json_mod.dumps(last, indent=2, ensure_ascii=False))
        else:
            print(f"status: {status}  taskId: {task_id}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ChatArt AI Image — text-to-image and image editing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
AGENT WORKFLOW RULES:
  1. ALWAYS start with `run` — it submits and polls automatically.
  2. Only use `query` if `run` timed out and you have a taskId to resume.
  3. `query` polls continuously (not once) until done or --timeout.
  4. NEVER hand a pending taskId back to the user — always poll to completion.

Task types:
  text2image  Text-to-Image  (model + prompt → images)
  image_edit  Image Edit     (model + prompt + reference images → edited images)

Examples:
  # List available models for a task type
  python ai_image.py list-models --type text2image

  # Text-to-image
  python ai_image.py run --type text2image --model "Nano Banana" \\
      --prompt "A futuristic city" --aspect-ratio "16:9"

  # Image editing
  python ai_image.py run --type image_edit --model "Nano Banana" \\
      --prompt "Change background to a beach" --aspect-ratio "16:9"\\
      --input-images photo.jpg

  # Estimate cost
  python ai_image.py estimate-cost --type text2image --model "Nano Banana" \\
      --resolution "2K"

  # Query a timed-out task
  python ai_image.py query --type text2image --task-id <taskId>
""",
    )

    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # -- run (default full flow) --
    p_run = sub.add_parser("run", help="[DEFAULT] Submit task and poll until done")
    add_common_args(p_run)
    add_image_edit_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    # -- submit only --
    p_submit = sub.add_parser("submit", help="Submit task only, print taskId and exit")
    add_common_args(p_submit)
    add_image_edit_args(p_submit)
    add_output_args(p_submit)

    # -- query / poll existing task --
    p_query = sub.add_parser("query", help="Poll existing taskId until done or timeout")
    p_query.add_argument("--type", required=True, choices=TASK_TYPES,
                         help="Task type (needed to select correct query endpoint)")
    p_query.add_argument("--task-id", required=True,
                         help="taskId returned by 'submit' or a previous 'run'")
    add_poll_args(p_query)
    add_output_args(p_query)

    # -- list-models --
    p_list = sub.add_parser("list-models", help="Show supported models and parameter constraints")
    p_list.add_argument("--type", required=True, choices=TASK_TYPES,
                        help="Task type to list models for")
    p_list.add_argument("--json", action="store_true",
                        help="Output as JSON")

    # -- estimate-cost --
    p_cost = sub.add_parser("estimate-cost", help="Estimate credit cost before running a task")
    p_cost.add_argument("--type", required=True, choices=TASK_TYPES,
                        help="Task type")
    p_cost.add_argument("--model", required=True, help="Model display name")
    p_cost.add_argument("--resolution", default=None, help="Resolution (e.g. 1K, 2K, 4K)")
    p_cost.add_argument("--quality", default=None, choices=["low", "medium", "high"],
                        help='Quality: "low", "medium", "high" (only Gpt Image 2)')
    p_cost.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.subcommand == "run":
        cmd_run(args, p_run)
    elif args.subcommand == "submit":
        cmd_submit(args, p_submit)
    elif args.subcommand == "query":
        cmd_query(args, p_query)
    elif args.subcommand == "list-models":
        cmd_list_models(args, p_list)
    elif args.subcommand == "estimate-cost":
        cmd_estimate_cost(args, p_cost)


if __name__ == "__main__":
    main()
