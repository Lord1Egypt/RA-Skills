#!/usr/bin/env python3
"""Generate videos using ChatArt Common Task APIs.

## AGENT INSTRUCTIONS — READ FIRST
- Default workflow: ALWAYS use `run` (submit + auto-poll).
  Do NOT ask the user to run query manually.
- Only use `query` when `run` has already timed out and a taskId exists,
  or when the user explicitly provides a taskId to resume.
- When using `query`, keep polling (default timeout=900s) until
  status is 'success' or 'fail'. Do NOT stop after a single check.
- Never hand a pending taskId back to the user and say "check it later".
  Always poll to completion within the timeout window.

Supported task types:
    i2v   Image-to-Video      — generate video from a first/end frame image
    t2v   Text-to-Video       — generate video from a text prompt
    extend Video Extension    — generate video from an input video + prompt

Subcommands:
    run     Submit task AND poll until done — DEFAULT, use this first
    submit  Submit only, print taskId, exit — use for parallel batch jobs
    query   Poll an existing taskId until done (or timeout) — use for recovery

Usage:
    python video_gen.py run  --type i2v  --model "Seedance 2.0" --first-frame <fileId|path> --prompt "..." [options]
    python video_gen.py run  --type t2v  --model "Seedance 2.0" --prompt "..." [options]
    python video_gen.py run  --type extend --model "PixVerse V6" --input_video <fileId|path> --prompt "..." [options]
    python video_gen.py query  --type <i2v|t2v|extend> --task-id <taskId> [options]
    
"""

import argparse
import json as json_mod
import os
import sys
import time
import uuid
import datetime
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

from typing import Any
from shared.client import ChatArtClient, ChatArtError
from shared.upload import resolve_local_file
from shared.media_util import MediaUtils

TASK_TYPES = ("i2v", "t2v", "omni", "extend")

ENDPOINTS = {
    "i2v": {
        "submit": "/web/video/generate-video",
        "query": "/web/video/get-video-task",
    },
    "t2v": {
        "submit": "/web/video/generate-video",
        "query": "/web/video/get-video-task",
    },
	"omni": {
        "submit": "/web/video/generate-video",
        "query": "/web/video/get-video-task",
    },
    "extend": { 
        "submit": "/web/video/generate-video",
        "query": "/web/video/get-video-task",
    },
}

DEFAULT_TIMEOUT = 900
DEFAULT_INTERVAL = 30

# ---------------------------------------------------------------------------
# Model constraints — `model` must use display names, NOT code names.
# Each entry: { "aspectRatio": list|None, "resolution": list|None, "duration": str }
#   None = not supported / do not send
# ---------------------------------------------------------------------------

I2V_MODELS = {
    # "LitAI 5":                      {"aspectRatio": None,                                          "resolution": [360, 540, 720, 1080],        "duration": "5,8,12",   "nativeAudio": True,  "inputMode": "first_end"},
    "Seedance 2.0":                 {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720, 1080],              "duration": "5,10,15",   "nativeAudio": True,  "inputMode": ["first_last_frames", "omni_reference"]},
    "Seedance 2.0 Fast":            {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],              "duration": "5,10,15",   "nativeAudio": True,  "inputMode": ["first_last_frames", "omni_reference"]},
    "Seedance 2.0 Mini":            {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9", "21:9"],         "resolution": [480, 720],              "duration": "5,10,15",   "nativeAudio": True,  "inputMode": ["first_last_frames", "omni_reference"]},
    "Seedance 1.5 Pro":             {"aspectRatio": None,        								   "resolution": [480, 720, 1080],       "duration": "5,10",   "nativeAudio": True,  "inputMode": ["single_image"]},
    "Kling V3":                     {"aspectRatio": None,                                          "resolution": [720, 1080, 2160],       "duration": "5,10,15",   "nativeAudio": True,  "inputMode": ["single_image", "first_last_frames"]},
    "HappyHorse1.0":                {"aspectRatio": None,                                          "resolution": [720, 1080],       "duration": "5,10","nativeAudio": True, "inputMode": ["omni_reference"]},
}

T2V_MODELS = {
    # "LitAI 5":                      {"aspectRatio": ["9:16", "1:1", "4:3", "16:9"],                "resolution": [360, 540, 720, 1080],        "duration": "5,8,12",   "nativeAudio": True},
    "Seedance 2.0":                 {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720, 1080],              "duration": "5,10,15",   "nativeAudio": True},
    "Seedance 2.0 Fast":            {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],              "duration": "5,10,15",   "nativeAudio": True},
    "Seedance 2.0 Mini":            {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9", "21:9"],         "resolution": [480, 720],              "duration": "5,10,15",   "nativeAudio": True},
    "Seedance 1.5 Pro":             {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720, 1080],        "duration": "5,10",   "nativeAudio": True},
    "Kling V3":                     {"aspectRatio": ["9:16", "1:1", "16:9"],                       "resolution": [720, 1080, 2160],        "duration": "5,10,15",   "nativeAudio": True},
    "HappyHorse1.0":                {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [720, 1080],       "duration": "5,10",      "nativeAudio": True},
}

# Omni Reference models - supports 1-9 reference images with flexible composition
OMNI_MODELS = {
    "Seedance 2.0":                 {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720, 1080],  "duration": "5,10,15",   "nativeAudio": True},
    "Seedance 2.0 Fast":            {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],  "duration": "5,10,15",   "nativeAudio": True},
    "Seedance 2.0 Mini":            {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9", "21:9"], "resolution": [480, 720],  "duration": "5,10,15",   "nativeAudio": True},
    "HappyHorse1.0":                {"aspectRatio": None,                                          "resolution": [720, 1080],       "duration": "5,10",      "nativeAudio": False},
}

EXTEND_MODELS = {
    "Seedance 2.0":                 {"aspectRatio": None,           "resolution": [480, 720],               "duration": "5,10,15",   "nativeAudio": True},
    "Seedance 2.0 Fast":            {"aspectRatio": None,           "resolution": [480, 720],               "duration": "5,10,15",   "nativeAudio": True},
    "Kling V3":                     {"aspectRatio": None,           "resolution": [720, 1080],              "duration": "5,10,15",   "nativeAudio": True},
    "PixVerse V6":                  {"aspectRatio": None,           "resolution": [360, 540, 720, 1080],    "duration": "5,10,15",  "internetSearch": False,  "nativeAudio": True},
}

MODEL_REGISTRY = {"i2v": I2V_MODELS, "t2v": T2V_MODELS, "omni": OMNI_MODELS, "extend": EXTEND_MODELS}
# ---------------------------------------------------------------------------
# Per-second pricing rates (credits, generatingCount=1).
# Key: (resolution_or_0, sound_on_or_None). 0 = resolution-independent, None = sound irrelevant.
# totalCost = rate * duration * generatingCount
# See references/api-docs.md for full pricing tables.
# ---------------------------------------------------------------------------

_PRICING_TABLE = {
    # Seedance 2.0
    ("Seedance 2.0", 480, 5): 60,
    ("Seedance 2.0", 480, 10): 120,
    ("Seedance 2.0", 480, 15): 180,
    ("Seedance 2.0", 720, 5): 90,
    ("Seedance 2.0", 720, 10): 180,
    ("Seedance 2.0", 720, 15): 270,
    ("Seedance 2.0", 1080, 5): 120,
    ("Seedance 2.0", 1080, 10): 240,
    ("Seedance 2.0", 1080, 15): 360,
    
    # Seedance 2.0 Fast
    ("Seedance 2.0 Fast", 480, 5): 30,
    ("Seedance 2.0 Fast", 480, 10): 60,
    ("Seedance 2.0 Fast", 480, 15): 90,
    ("Seedance 2.0 Fast", 720, 5): 60,
    ("Seedance 2.0 Fast", 720, 10): 120,
    ("Seedance 2.0 Fast", 720, 15): 180,

    # Seedance 2.0 Mini
    ("Seedance 2.0 Mini", 480, 5): 40,
    ("Seedance 2.0 Mini", 480, 10): 80,
    ("Seedance 2.0 Mini", 480, 15): 120,
    ("Seedance 2.0 Mini", 720, 5): 60,
    ("Seedance 2.0 Mini", 720, 10): 120,
    ("Seedance 2.0 Mini", 720, 15): 180,
    
    # Seedance 1.5 Pro
    ("Seedance 1.5 Pro", 480, 5): 32,
    ("Seedance 1.5 Pro", 480, 10): 64,
    ("Seedance 1.5 Pro", 720, 5): 48,
    ("Seedance 1.5 Pro", 720, 10): 96,
    ("Seedance 1.5 Pro", 1080, 5): 64,
    ("Seedance 1.5 Pro", 1080, 10): 128,
    
    # Kling 3.0 (Kling V3)
    ("Kling V3", 720, 5): 40,
    ("Kling V3", 720, 10): 80,
    ("Kling V3", 720, 15): 120,
    ("Kling V3", 1080, 5): 60,
    ("Kling V3", 1080, 10): 120,
    ("Kling V3", 1080, 15): 180,
    ("Kling V3", 2160, 5): 200,
    ("Kling V3", 2160, 10): 400,
    ("Kling V3", 2160, 15): 600,
    
    # Happy Horse 1.0
    ("HappyHorse1.0", 720, 5): 48,
    ("HappyHorse1.0", 720, 10): 96,
    ("HappyHorse1.0", 720, 15): 144,
    ("HappyHorse1.0", 1080, 5): 72,
    ("HappyHorse1.0", 1080, 10): 144,
    ("HappyHorse1.0", 1080, 15): 216,

    # PixVerse V6
    ("PixVerse V6", 360, 5): 20,
    ("PixVerse V6", 360, 10): 40,
    ("PixVerse V6", 360, 15): 60,
    ("PixVerse V6", 540, 5): 25,
    ("PixVerse V6", 540, 10): 50,
    ("PixVerse V6", 540, 15): 75,
    ("PixVerse V6", 720, 5): 30,
    ("PixVerse V6", 720, 10): 60,
    ("PixVerse V6", 720, 15): 90,
    ("PixVerse V6", 1080, 5): 50,
    ("PixVerse V6", 1080, 10): 100,
    ("PixVerse V6", 1080, 15): 150,
}

MODEL_MAP = {
    # "ArtMotion4.1": "art-motion-4.1",
    "Seedance 2.0": "seedance-2.0",
    "Seedance 2.0 Fast": "seedance-2.0-fast",
    "Kling V3": "kling-3-0",
    "HappyHorse1.0": "happy-horse-1-0",
    "Seedance 1.5 Pro": "seedance-1.5-pro",
    "PixVerse V6": "pix-verse-6",
    "Seedance 2.0 Mini": "seedance-2.0-mini",
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
        # name=Seedance 2.0 这里由于用户输入seedance2.0、seedance2或者seedance 2，下面条件判断无法进行匹配，所以这里需要进行处理，让其能够进行匹配
        if ((name == "Seedance 2.0" and model_name_lower in ["seedance 2.0", "seedance2.0", "seedance 2", "seedance2", "seedance"]) or
            (name == "Seedance 2.0 Fast" and model_name_lower in ["seedance 2.0 fast", "seedance2.0 fast", "seedance2.0fast", "seedance 2 fast", "seedance2 fast", "seedance2fast"]) or
            (name == "Seedance 2.0 Mini" and model_name_lower in ["seedance 2.0 mini", "seedance2.0 mini", "seedance 2.0mini", "seedance2.0mini", "seedance 2 mini", "seedance2 mini", "seedance2mini"]) or
            (name == "Kling V3" and model_name_lower in ["kling v3", "kling v3.0", "klingv3", "kling 3", "kling3", "kling3.0", "kling"]) or
            (name == "HappyHorse1.0" and model_name_lower in ["happyhorse1.0", "happyhorse 1.0", "happy horse 1.0", "happyhorse", "happyhorse1", "happy horse", "happy horse 1"]) or
            (name == "Seedance 1.5 Pro" and model_name_lower in ["seedance 1.5 pro", "seedance1.5 pro", "seedance 1.5pro", "seedance1.5pro", "seedance 1.5", "seedance1.5", "seedance pro", "seedancepro"]) or
            (name == "PixVerse V6" and model_name_lower in ["pixverse v6", "pixverse6", "pix verse v6", "pix verse6", "pixverse", "pix verse"])):
            return model_id
    
    return None

def estimate_cost(model: str, resolution: int | None, duration: int,
                  sound_on: bool = False, count: int = 1) -> float | None:
    """Return estimated total cost in credits, or None if model/params unknown."""
    if not resolution:
        return None
    
    key = (model, resolution, duration)
    unit_cost = _PRICING_TABLE.get(key)
    
    if unit_cost is None:
        return None
    
    return round(unit_cost * count, 2)


def _parse_duration_spec(spec: str) -> str:
    """Convert duration spec to human-readable hint for error messages."""
    if not spec:
        return "N/A"
    if "," in spec:
        return f"one of [{spec}]s"
    if "-" in spec:
        lo, hi = spec.split("-")
        return f"{lo}–{hi}s"
    return f"{spec}s"


def validate_model_params(task_type: str, model: str, aspect_ratio: str | None,
                          resolution: int | None, duration: int | None,
                          quiet: bool) -> None:
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

    if aspect_ratio and spec["aspectRatio"] is None:
        if not quiet:
            print(
                f"Warning: model '{model}' does not support aspectRatio "
                f"(got '{aspect_ratio}'). Parameter will be ignored by the API.",
                file=sys.stderr,
            )
    elif aspect_ratio and spec["aspectRatio"] and aspect_ratio not in spec["aspectRatio"]:
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
                f"(got {resolution}). Parameter will be ignored by the API.",
                file=sys.stderr,
            )
    elif resolution and spec["resolution"] and resolution not in spec["resolution"]:
        if not quiet:
            print(
                f"Warning: model '{model}' supports resolution "
                f"{spec['resolution']}, got {resolution}.",
                file=sys.stderr,
            )

    if duration and spec["duration"]:
        dur_str = spec["duration"]
        valid = True
        if "," in dur_str:
            valid = duration in [int(x) for x in dur_str.split(",")]
        elif "-" in dur_str:
            lo, hi = [int(x) for x in dur_str.split("-")]
            valid = lo <= duration <= hi
        else:
            valid = duration == int(dur_str)
        if not valid and not quiet:
            print(
                f"Warning: model '{model}' supports duration "
                f"{_parse_duration_spec(dur_str)}, got {duration}s.",
                file=sys.stderr,
            )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resolve_file(client: ChatArtClient, file_ref: str, quiet: bool) -> str:
    """If file_ref looks like a local path, upload it and return fileId."""
    return resolve_local_file(file_ref, quiet=quiet, client=client)

def get_video_duration(file_ref: str, quiet: bool) -> float:
    """If file_ref looks like a local path, upload it and return fileId."""
    local_file = file_ref
    is_url = file_ref.startswith(("http://", "https://"))
    if is_url:
        time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        temp_dir = tempfile.gettempdir()
        out_path = os.path.join(temp_dir, f"video_{time_name}.mp4")
        download_video(file_ref, out_path, quiet)
        local_file = out_path

    return MediaUtils.get_duration(local_file)
	
def build_anim_body(args, client: ChatArtClient) -> dict:
    """Build request body for Text-to-Video."""
    body = {
        # "model": args.model,
        "prompt": args.prompt,
    }
    if args.model:
        body["video_model"] = 1
    if args.input_image:
        if os.path.isfile(args.input_image):
            body["img_url"] = resolve_file(client, args.input_image, args.quiet)
        else:
            body["img_url"] = args.input_image
    if args.resolution:
        if args.resolution == 2160:
            body["quality"] = "4k"
        else:
            body["quality"] = str(args.resolution) + "p"
    if args.duration:
        body["duration"] = args.duration
    if args.style:
        body["style"] = args.style
    return body

def calculate_extend_quality_from_height(height: int) -> str:
    """Calculate video quality based on video height.
    
    Args:
        height: Video height in pixels
        
    Returns:
        Quality string: '1080p', '720p', '540p', or '360p'
    """
    if height >= 1080:
        return '1080p'
    elif height >= 720:
        return '720p'
    elif height >= 540:
        return '540p'
    else:
        return '360p'

def build_extend_body(args, client: ChatArtClient) -> dict:
    """Build request body for Text-to-Video."""
    body = {
        "video_id": "103",
        "function_mode": "single_image",
        "prompt": args.prompt,
        "image_url": [],
        "sound": 1,
    }
    if args.model:
        body["gpt_type"] = get_model_id_by_name(args.model)
        body["original_model"] = get_model_id_by_name(args.model)

    resolution = None
    if args.input_video:
        if os.path.isfile(args.input_video):
            resolution = MediaUtils.get_resolution(args.input_video)
            body["image_url"].append(resolve_file(client, args.input_video, args.quiet))
        else:
            resolution = MediaUtils.get_resolution_from_url(args.input_video)
            body["image_url"].append(args.input_video)

    if resolution:
        body["quality"] = calculate_extend_quality_from_height(resolution)

    if args.duration:
        body["duration"] = args.duration
    # if args.sound:
    #     body["sound"] = args.sound
    # if args.count:
    #     body["video_num"] = args.count
    return body

def build_i2v_body(args, client: ChatArtClient) -> dict:
    """Build request body for Image-to-Video."""
    body: dict[str, Any] = {
        "video_id": "102",
        "sound": 1
    }

    if args.model:
        body["gpt_type"] = get_model_id_by_name(args.model)
        body["original_model"] = get_model_id_by_name(args.model)

    if body["original_model"] is None:
        raise ValueError(f"model name err")
		
    # Collect all image references
    all_images = []
    
    # Process ref_images (omni mode, supports 1-9 images)
    if args.ref_images:
        for ref in args.ref_images:
            if os.path.isfile(ref):
                all_images.append(resolve_file(client, ref, args.quiet))
            else:
                all_images.append(ref)
    
    # Process first_frame and end_frame
    frame_images = []
    if args.first_frame:
        if os.path.isfile(args.first_frame):
            frame_images.append(resolve_file(client, args.first_frame, args.quiet))
        else:
            frame_images.append(args.first_frame)
    
    if args.end_frame:
        if os.path.isfile(args.end_frame):
            frame_images.append(resolve_file(client, args.end_frame, args.quiet))
        else:
            frame_images.append(args.end_frame)
    
    # Mode selection logic
    has_ref_images = len(all_images) > 0
    has_frames = len(frame_images) > 0
    total_images = len(all_images) + len(frame_images)
    
    # Determine function_mode based on user intent and image count
    if has_ref_images:
        # Using ref_images - determine mode based on model capability and image count
        # Check if model supports single_image mode
        registry = MODEL_REGISTRY.get(args.type, {})
        model_supports_single = False
        if args.model in registry:
            supported_modes = registry[args.model].get("inputMode", [])
            if isinstance(supported_modes, str):
                supported_modes = [supported_modes]
            model_supports_single = "single_image" in supported_modes
        
        if len(all_images) == 1 and model_supports_single:
            # Single image + model supports single mode -> single_image mode
            body["function_mode"] = "single_image"
            body["image_url"] = all_images
            if not args.quiet:
                print(f"Using single_image mode with 1 reference image", file=sys.stderr)
        else:
            # 2+ images OR model doesn't support single mode -> omni_reference mode
            body["function_mode"] = "omni_reference"
            body["image_url"] = all_images
            if not args.quiet:
                print(f"Using omni_reference mode with {len(all_images)} reference image(s)", file=sys.stderr)
    elif has_frames:
        # Using first/end frames -> first_last_frames mode
        body["function_mode"] = "first_last_frames"
        body["image_url"] = frame_images
        if not args.quiet:
            print(f"Using first_last_frames mode with {len(frame_images)} frame(s)", file=sys.stderr)

    else:
        # No images provided - should not happen due to validation
        body["function_mode"] = "first_last_frames"
        body["image_url"] = []

    if args.prompt:
        body["prompt"] = args.prompt

    registry = MODEL_REGISTRY.get(args.type, {})
    if args.model in registry:
        spec = registry[args.model]
        if args.resolution and spec["resolution"] is not None:
            if args.resolution == 2160:
                body["quality"] = "4k"
            else:
                body["quality"] = str(args.resolution) + "p"

        if args.aspect_ratio and spec["aspectRatio"] is not None:
            body["ratio"] = args.aspect_ratio

    if args.duration:
        body["duration"] = str(args.duration)
    # if args.sound:
    #    body["sound"] = args.sound
    # if args.count:
    #    body["video_num"] = args.count
    return body


def build_t2v_body(args) -> dict:
    """Build request body for Text-to-Video."""
    body = {
        "video_id": "101",
        "sound": 1,
        "function_mode": "single_image",
        "image_url":[],
        "prompt": args.prompt,
    }

    if args.model:
        body["gpt_type"] = get_model_id_by_name(args.model)
        body["original_model"] = get_model_id_by_name(args.model)

    if body["original_model"] is None:
        raise ValueError(f"model name err")

    registry = MODEL_REGISTRY.get(args.type, {})
    if args.model in registry:
        spec = registry[args.model]
        if args.resolution and spec["resolution"] is not None:
            if args.resolution == 2160:
                body["quality"] = "4k"
            else:
                body["quality"] = str(args.resolution) + "p"

        if args.aspect_ratio and spec["aspectRatio"] is not None:
            body["ratio"] = args.aspect_ratio

    if args.duration:
        body["duration"] = args.duration

    if args.sound is not None:
        body["sound"] = 1 if args.sound.lower() == "true" else 0
    
    return body

def build_omni_body(args, client: ChatArtClient) -> dict:
    """Build request body for Omni Reference mode (1-9 images)."""
    
    # Collect all images from --ref-images
    all_images = []
    if args.ref_images:
        for ref in args.ref_images:
            if os.path.isfile(ref):
                all_images.append(resolve_file(client, ref, args.quiet))
            else:
                all_images.append(ref)
    
    # Determine function_mode based on image count and model capability
    registry = MODEL_REGISTRY.get(args.type, {})
    model_supports_single = False
    if args.model in registry:
        supported_modes = registry[args.model].get("inputMode", [])
        if isinstance(supported_modes, str):
            supported_modes = [supported_modes]
        model_supports_single = "single_image" in supported_modes
    
    if len(all_images) == 1 and model_supports_single:
        function_mode = "single_image"
    else:
        function_mode = "omni_reference"
    
    body = {
        "video_id": "102",
        "sound": False,
        "function_mode": function_mode,
        "image_url": all_images,
    }
    
    if args.model:
        body["original_model"] = get_model_id_by_name(args.model)
        body["gpt_type"] = get_model_id_by_name(args.model)

    if body["original_model"] is None:
        raise ValueError(f"model name err")

    if args.prompt:
        body["prompt"] = args.prompt

    registry = MODEL_REGISTRY.get(args.type, {})
    if args.model in registry:
        spec = registry[args.model]
        if args.resolution and spec["resolution"] is not None:
            body["quality"] = str(args.resolution) + "p"

        if args.aspect_ratio and spec["aspectRatio"] is not None:
            body["ratio"] = args.aspect_ratio

    if args.duration:
        body["duration"] = str(args.duration)


    # 打印body
    # print(f"body: {json_mod.dumps(body, ensure_ascii=False)}", file=sys.stderr)
    
    return body
def build_body(args, client: ChatArtClient) -> dict:
    """Dispatch to the type-specific body builder, with model constraint checks."""
    if args.model:
        validate_model_params(
            args.type, args.model,
            getattr(args, "aspect_ratio", None),
            getattr(args, "resolution", None),
            getattr(args, "duration", None),
            args.quiet,
        )
    if args.type == "i2v":
        return build_i2v_body(args, client)
    elif args.type == "t2v":
        return build_t2v_body(args)
    elif args.type == "omni":
        return build_omni_body(args, client)
    elif args.type == "extend":
        return build_extend_body(args, client)
    #elif args.type == "anim":
    #    return build_anim_body(args, client)
    raise ValueError(f"Unknown type: {args.type}")


def do_submit(client: ChatArtClient, task_type: str, body: dict, quiet: bool) -> str:
    """POST submit task, return taskId."""
    path = ENDPOINTS[task_type]["submit"]
    label = {"i2v": "image-to-video", "t2v": "text-to-video", "omni": "omni-reference", "extend": "video-extension"}
    if not quiet:
        print(f"Submitting {label[task_type]} task...", file=sys.stderr)
    result = client.post(path, json=body)
    #print(f"client.post result: {result}")
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


def download_video(url: str, output: str, quiet: bool) -> None:
    """Download a video from URL to a local file."""
    import requests as req

    if not quiet:
        print(f"Downloading video to {output}...", file=sys.stderr)

    resp = req.get(url, stream=True)
    resp.raise_for_status()

    with open(output, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    if not quiet:
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"Downloaded: {output} ({size_mb:.1f} MB)", file=sys.stderr)


def print_result(result: dict, args, client: ChatArtClient) -> None:
    """Print final result: video URLs by default, full JSON with --json."""
    
    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
        return
    
    cost = result.get("cost_credit", "N/A")
    status = result.get("status", 0)
    
    print(f"status: {status}  cost: {cost} credits")
    
    # Extract video URL from message.url
    message = result.get("message", {})
    video_url = message.get("url", "") if isinstance(message, dict) else ""
    
    if args.output_dir and video_url:
        os.makedirs(args.output_dir, exist_ok=True)
        ext = "mp4"
        time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        out_path = os.path.join(args.output_dir, f"video_{time_name}.{ext}")
        download_video(video_url, out_path, args.quiet)
    
    if status == 1 and video_url:
        print(f" [1] video_url:{video_url}")
    elif status != 1:
        error_msg = result.get("error", "") or result.get("real_error", "Unknown error")
        print(f"  [1] failed: {error_msg or 'Task failed'}")

# ---------------------------------------------------------------------------
# Argument definitions
# ---------------------------------------------------------------------------

def add_common_args(p):
    """Add arguments shared by all task types."""
    p.add_argument("--type", required=True, choices=TASK_TYPES,
                   help="Task type: i2v (image-to-video), t2v (text-to-video), extend (video extension)")
    p.add_argument("--model", default=None,
                   help="Model name/ID (required for t2v and i2v; optional for others). See 'list-models' command for supported models. default value: None ")
    p.add_argument("--prompt", default=None,
                   help="Text prompt (required for t2v and omni)")
    p.add_argument("--aspect-ratio", default=None,
                   help='Aspect ratio, e.g. "16:9", "9:16", "1:1", "4:3", "3:4" ')
    p.add_argument("--resolution", type=int, default=720, choices=[360, 480, 540, 720, 1080, 2160],
                   help="Resolution (model-dependent): 360, 480, 540, 720, 1080, 2160")
    p.add_argument("--duration", type=int, default=None,
                   help="Video duration in seconds")
    p.add_argument("--count", type=int, default=1,
                   help="Number of videos to generate (1-4) default: 1")
    p.add_argument("--sound", default=None, choices=["true", "false"],
                   help='Native audio: "true"/"false". Only models with nativeAudio=True support this; may affect cost')
    p.add_argument("--input_image", default=None,
                   help="Input image for animation/a2ls (fileId or local path)")

def add_extend_args(p):
    """Add video-extension specific arguments."""
    p.add_argument("--input_video", default=None,
                   help="Need to extend the video")

def add_anim_args(p):
    """Add animation specific arguments."""
    p.add_argument("--style", default=None,
                   help="Animation style, e.g. '', 'comic', 'anime', '3d_animation', 'clay', 'cyberpunk'")

def add_i2v_args(p):
    """Add image-to-video specific arguments."""
    p.add_argument("--first-frame", default=None,
                   help="First frame image fileId or local path")
    p.add_argument("--end-frame", default=None,
                   help="End frame image fileId or local path")
    p.add_argument("--ref-images", nargs="+", default=None,
                   help="Reference image fileIds or local paths (multi-image mode, >=2)")


def add_omni_args(p):
    """Add omni-reference specific arguments."""
    p.add_argument("--input-images", default=None,
                   help='JSON array of input images, e.g. \'[{"fileId":"xxx","name":"Image1"}]\'')
    p.add_argument("--input-videos", default=None,
                   help='JSON array of input videos, e.g. \'[{"fileId":"xxx","name":"Video1"}]\'')
    p.add_argument("--internet-search", action="store_true",
                   help="Enable internet search for omni reference")


def add_poll_args(p):
    """Add polling control arguments."""
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Max polling time in seconds (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                   help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})")


def add_output_args(p):
    """Add output/download arguments."""
    p.add_argument("--output-dir", default=None,
                   help="Download result videos to this directory")
    p.add_argument("--json", action="store_true",
                   help="Output full JSON response")
    p.add_argument("-q", "--quiet", action="store_true",
                   help="Suppress status messages on stderr")


def validate_args(args, parser):
    """Validate type-specific required arguments."""
    if args.type == "t2v":
        if not args.model:
            parser.error("--model is required for text-to-video (t2v)")
        if not args.prompt:
            parser.error("--prompt is required for text-to-video (t2v)")
    elif args.type == "omni":
        if not args.model:
            parser.error("--model is required for omni reference")
        if not args.prompt:
            parser.error("--prompt is required for omni reference")
        if not args.ref_images:
            parser.error("--ref-images is required for omni reference (1-9 images)")
    elif args.type == "i2v":
        if not args.first_frame and not args.ref_images:
            parser.error("--first-frame or --ref-images is required for image-to-video (i2v)")

        # Validate inputMode compatibility
        if args.model:
            registry = MODEL_REGISTRY.get(args.type, {})
            if args.model in registry:
                model_info = registry[args.model]
                supported_modes = model_info.get("inputMode", ["first_end"])
                
                # Ensure supported_modes is a list (for backward compatibility)
                if isinstance(supported_modes, str):
                    supported_modes = [supported_modes]
                
                # Count images
                ref_count = len(args.ref_images) if args.ref_images else 0
                frame_count = (1 if args.first_frame else 0) + (1 if args.end_frame else 0)
                total_images = ref_count + frame_count
                
                # Determine which mode the user is trying to use
                using_first_end = frame_count > 0
                using_omni = ref_count > 0
                
                # Validate based on the mode being used
                if using_first_end:
                    # User wants first/last frame mode
                    if "first_last_frames" not in supported_modes and "single_image" not in supported_modes:
                        print(f"Error: Model '{args.model}' does not support first/last frame mode.", file=sys.stderr)
                        print(f"Supported modes: {', '.join(supported_modes)}", file=sys.stderr)
                        sys.exit(1)
                    if total_images > 2:
                        print(f"Error: First/last frame mode supports max 2 images.", file=sys.stderr)
                        print(f"You provided {total_images} image(s).", file=sys.stderr)
                        if total_images >= 3:
                            print(f"For {total_images} images, please use --type omni with a model that supports omni_reference mode.", file=sys.stderr)
                        sys.exit(1)
                
                elif using_omni:
                    # User wants omni reference mode
                    if "omni_reference" not in supported_modes:
                        print(f"Error: Model '{args.model}' does not support omni reference mode.", file=sys.stderr)
                        print(f"Supported modes: {', '.join(supported_modes)}", file=sys.stderr)
                        if total_images >= 3:
                            print(f"For {total_images} images, please use Seedance 2.0 or HappyHorse 1.0.", file=sys.stderr)
                        sys.exit(1)
                
                else:
                    # No images provided - should have been caught earlier
                    pass
    elif args.type == "extend":
        if not args.input_video:
            parser.error("--input_video is required for video extension")
    elif args.type == "anim":
        if not args.input_image:
            parser.error("--input_image is required for animation")

    
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

    type_label = {"i2v": "Image-to-Video", "t2v": "Text-to-Video", "omni": "Omni-Reference", "extend": "Video Extension"}
    print(f"\n{type_label.get(task_type, task_type)} — Supported Models\n")
    print(f"{'Model':<25} {'Input Mode':<18} {'Aspect Ratio':<35} {'Resolution':<22} {'Duration':<32} {'Audio'}")
    print("-" * 145)
    for name, spec in registry.items():
        ar = ", ".join(spec["aspectRatio"]) if spec["aspectRatio"] else "by image" if task_type == "i2v" else "N/A"
        res = ", ".join(str(r) for r in spec["resolution"]) if spec["resolution"] else "N/A"
        dur = _parse_duration_spec(spec["duration"])
        audio = "Yes" if spec.get("nativeAudio") else "No"
        input_mode = spec.get("inputMode", "N/A")
        # Map inputMode to user-friendly labels (handle both list and string)
        mode_labels = {
            "single": "Single (1)",
            "first_end": "First/End (1-2)",
            "omni": "Omni (1-9)"
        }
        
        # Handle list of modes
        if isinstance(input_mode, list):
            mode_label = ", ".join([mode_labels.get(m, m) for m in input_mode])
        else:
            mode_label = mode_labels.get(input_mode, input_mode)
        
        print(f"{name:<25} {mode_label:<18} {ar:<35} {res:<22} {dur:<32} {audio}")
    print()


def cmd_estimate_cost(args, parser):
    """Print estimated cost for a given model + parameters."""
    sound_on = args.sound == "true" if args.sound else False
    cost = estimate_cost(args.model, args.resolution, args.duration, sound_on, args.count or 1)
    if cost is None:
        print(f"Cannot estimate cost for model '{args.model}' with given parameters.", file=sys.stderr)
        print("Use list-models to see available models, or check references/api-docs.md.", file=sys.stderr)
        sys.exit(1)
    count = args.count or 1
    unit = round(cost / count, 2)
    if args.json:
        print(json_mod.dumps({"model": args.model, "resolution": args.resolution,
                               "duration": args.duration, "sound": args.sound or "false",
                               "count": count, "unitCost": unit, "totalCost": cost}))
    else:
        print(f"model: {args.model}  resolution: {args.resolution or 'default'}  "
              f"duration: {args.duration}s  sound: {args.sound or 'false'}  count: {count}")
        print(f"estimated unit cost: {unit} credits")
        print(f"estimated total cost: {cost} credits")


def cmd_run(args, parser):
    """Submit task then poll until done — full flow (default)."""
    #print("cmd_run Submitting task...")
    validate_args(args, parser)
    client = ChatArtClient()
    body = build_body(args, client)
    print(f"Request body: {json_mod.dumps(body, ensure_ascii=False)}", file=sys.stderr)
    # Debug: print the request body to stderr
    if not args.quiet:
        print(f"Request body: {json_mod.dumps(body, ensure_ascii=False)}", file=sys.stderr)
    task_id = do_submit(client, args.type, body, args.quiet)
    result = do_poll(client, args.type, task_id, args.timeout, args.interval, args.quiet)
    # print(f"result: {result}")
    # 打印args类型和值
    # print(f"args类型：{type(args)}")
    print_result(result, args, client)


def cmd_submit(args, parser):
    """Submit task only — print taskId and exit immediately."""
    #print("Submitting task...")
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
        last = client.get(path, params={"taskId": args.task_id})
        status = last.get("status", "unknown")
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
        description="ChatArt Video Generation — i2v / t2v /omni / extend.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
AGENT WORKFLOW RULES:
  1. ALWAYS start with `run` — it submits and polls automatically.
  2. Only use `query` if `run` timed out and you have a taskId to resume.
  3. `query` polls continuously (not once) until done or --timeout.
  4. NEVER hand a pending taskId back to the user — always poll to completion.

Task types:
  i2v   Image-to-Video      (first/end frame + prompt)
  t2v   Text-to-Video       (model + prompt, no image needed)
  extend Video Extension    (input video + prompt)
  anim   Animation           (input image + style + prompt)

Examples:
  # List available models for a task type
  python video_gen.py list-models --type t2v

  # Image-to-video with first frame
  python video_gen.py run --type i2v --model "LitAI 5" \\
      --first-frame photo.png --prompt "A rotating product" --resolution 1080

  # Text-to-video
  python video_gen.py run --type t2v --model "LitAI 5" \\
      --prompt "A futuristic city" --aspect-ratio "16:9" --duration 5

  # Video extension
  python video_gen.py run --type extend --model "LitAI 5" \\
      --input_video "input.mp4" --prompt "video description" --duration 5 

  # Animation with style
  python video_gen.py run --type anim --model "LitAI 5" \\
      --input_image "input.png" --prompt "video description" --duration 5 --style "cyberpunk" --resolution 720 

  # Estimate cost before running
  python video_gen.py estimate-cost --model "LitAI 5" \\
      --resolution 1080 --duration 5 --sound on --count 2

  # Query a timed-out task
  python video_gen.py query --type i2v --task-id <taskId>
""",
    )

    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # -- run (default full flow) --
    p_run = sub.add_parser("run", help="[DEFAULT] Submit task and poll until done")
    add_common_args(p_run)
    add_i2v_args(p_run)
    # add_omni_args(p_run)
    add_extend_args(p_run)
    add_anim_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    # -- submit only --
    p_submit = sub.add_parser("submit", help="Submit task only, print taskId and exit")
    add_common_args(p_submit)
    add_i2v_args(p_submit)
    add_extend_args(p_submit)
    add_anim_args(p_submit)
    # add_omni_args(p_submit)
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
    p_cost.add_argument("--model", required=True, help="Model display name")
    p_cost.add_argument("--resolution", type=int, required=True, default="720", help="Resolution")
    p_cost.add_argument("--duration", type=int, required=True, help="Duration in seconds")
    p_cost.add_argument("--sound", default="true", choices=["true", "false"], help="Sound true/false (default: true)")
    p_cost.add_argument("--count", type=int, required=True, default=1, help="generatingCount (1-4)")
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