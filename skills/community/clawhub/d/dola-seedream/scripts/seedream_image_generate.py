#!/usr/bin/env python3
# MIT License
# Copyright (c) 2026
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
dola-seedream - Generate high-quality images from text prompts
using BytePlus Seedream models (4.0, 4.5, and 5.0).

Documentation: https://docs.byteplus.com/en/docs/ModelArk/1399008
"""

import argparse
import asyncio
import json
import os
import sys
import logging
from typing import Dict, List, Tuple, Optional

import httpx

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configuration constants
API_KEY = os.getenv("ARK_DOLA_API_KEY")
API_BASE = os.getenv(
    "ARK_DOLA_API_BASE", 
    "https://ark.ap-southeast.bytepluses.com/api/v3"
).rstrip("/")

# Model names for each version
MODELS = {
    "4.0": "seedream-4-0-250828",
    "4.5": "seedream-4-5-251128",
    "5.0-lite": "seedream-5-0-260128",
    "5.0": "seedream-5-0-260128",
}

# Supported fields per version (based on official documentation)
SUPPORTED_FIELDS = {
    "4.0": ["size", "response_format", "watermark", "image", "sequential_image_generation", "sequential_image_generation_options", "stream", "optimize_prompt_options"],
    "4.5": ["size", "response_format", "watermark", "image", "sequential_image_generation", "sequential_image_generation_options", "stream", "optimize_prompt_options"],
    "5.0-lite": ["size", "response_format", "watermark", "image", "sequential_image_generation", "sequential_image_generation_options", "stream", "optimize_prompt_options", "output_format"],
    "5.0": ["size", "response_format", "watermark", "image", "sequential_image_generation", "sequential_image_generation_options", "stream", "optimize_prompt_options", "output_format"],
}

# Version descriptions
VERSION_DESCRIPTIONS = {
    "4.0": "Seedream 4.0 - Stable for daily use, support 1K/2K/4K resolution and fast mode.",
    "4.5": "Seedream 4.5 - Improved detail, support 2K/4K resolution.",
    "5.0-lite": "Seedream 5.0-lite - Highest quality, support 2K/3K resolution and PNG output.",
    "5.0": "Seedream 5.0 (alias for 5.0-lite) - Latest features.",
}

def _get_headers() -> dict:
    if not API_KEY:
        raise ValueError("Missing ARK_DOLA_API_KEY environment variable.")
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

def _build_request_body(item: dict, model_name: str, version: str) -> dict:
    body = {
        "model": model_name,
        "prompt": item.get("prompt", ""),
    }

    supported_fields = SUPPORTED_FIELDS.get(version, [])
    for field in supported_fields:
        if field in item and item[field] is not None:
            body[field] = item[field]

    # Batch generation options
    if item.get("sequential_image_generation") == "auto":
        options = dict(item.get("sequential_image_generation_options") or {})
        if "max_images" in item:
            options["max_images"] = item["max_images"]
        if options:
            body["sequential_image_generation_options"] = options

    # Prompt optimization options
    if "prompt_mode" in item and item["prompt_mode"]:
        body["optimize_prompt_options"] = {"mode": item["prompt_mode"]}

    return body

async def _call_image_api(client: httpx.AsyncClient, item: dict, model_name: str, version: str) -> dict:
    url = f"{API_BASE}/images/generations"
    body = _build_request_body(item, model_name, version)
    
    response = await client.post(url, headers=_get_headers(), json=body)
    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", response.text)
        except Exception:
            error_msg = response.text
        raise RuntimeError(f"API Error ({response.status_code}): {error_msg}")
    
    return response.json()

async def handle_single_task(
    client: httpx.AsyncClient,
    idx: int,
    item: dict,
    model_name: str,
    version: str,
    semaphore: asyncio.Semaphore
) -> Tuple[List[dict], List[str], List[dict]]:
    async with semaphore:
        success_list = []
        error_list = []
        error_detail_list = []

        try:
            response = await _call_image_api(client, item, model_name, version)

            if "error" not in response:
                data_list = response.get("data", [])
                for i, image_data in enumerate(data_list):
                    image_name = f"task_{idx}_image_{i}"

                    if "error" in image_data:
                        error_list.append(image_name)
                        error_detail_list.append({"task_idx": idx, "image_name": image_name, "error": image_data.get("error")})
                        continue

                    image_url = image_data.get("url")
                    if image_url:
                        success_list.append({image_name: image_url})
                    else:
                        b64 = image_data.get("b64_json")
                        if b64:
                            output_format = item.get("output_format", "jpeg")
                            mime_type = f"image/{output_format}"
                            success_list.append({image_name: f"data:{mime_type};base64,{b64}"})
                        else:
                            error_list.append(image_name)
                            error_detail_list.append({"task_idx": idx, "image_name": image_name, "error": "missing data (no url/b64)"})
            else:
                error_info = response.get("error", {})
                error_list.append(f"task_{idx}")
                error_detail_list.append({"task_idx": idx, "error": error_info})

        except Exception as e:
            error_list.append(f"task_{idx}")
            error_detail_list.append({"task_idx": idx, "error": str(e)})

        return success_list, error_list, error_detail_list

async def seedream_generate(
    tasks: List[dict],
    version: str = "5.0",
    timeout: int = 1200,
    concurrency: int = 5
) -> Dict:
    if version not in MODELS:
        return {"status": "error", "error_list": [f"Unsupported version: {version}"]}

    if not API_KEY:
        return {"status": "error", "error_list": ["Missing ARK_DOLA_API_KEY environment variable."]}

    model_name = MODELS[version]
    semaphore = asyncio.Semaphore(concurrency)
    
    async with httpx.AsyncClient(timeout=float(timeout)) as client:
        coroutines = [handle_single_task(client, idx, item, model_name, version, semaphore) for idx, item in enumerate(tasks)]
        results = await asyncio.gather(*coroutines, return_exceptions=True)

    success_list = []
    error_list = []
    error_detail_list = []

    for res in results:
        if isinstance(res, Exception):
            error_list.append("exception")
            error_detail_list.append({"error": str(res)})
        else:
            s, e, ed = res
            success_list.extend(s)
            error_list.extend(e)
            error_detail_list.extend(ed)

    return {
        "status": "success" if success_list else "error",
        "success_list": success_list,
        "error_list": error_list,
        "error_detail_list": error_detail_list,
        "model": model_name,
        "version": version,
    }

def main():
    parser = argparse.ArgumentParser(
        description="dola-seedream - Generate images using BytePlus Seedream models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Versions:\n" + "\n".join([f"  {k}: {v}" for k, v in VERSION_DESCRIPTIONS.items()])
    )
    parser.add_argument("--prompt", "-p", help="Image description text")
    parser.add_argument("--version", "-v", choices=list(MODELS.keys()), default="5.0-lite", help="Model version (default 5.0-lite)")
    parser.add_argument("--size", "-s", help="Image dimensions (e.g., 2048x2048 or resolution 1K/2K/3K/4K)")
    parser.add_argument("--image", "-i", help="Reference image URL")
    parser.add_argument("--images", nargs="+", help="Multiple reference image URLs")
    parser.add_argument("--group", "-g", action="store_true", help="Enable batch generation")
    parser.add_argument("--max-images", type=int, default=15, help="Max images for batch (1-15)")
    parser.add_argument("--output-format", choices=["png", "jpeg"], default="jpeg", help="Output format (5.0-lite only)")
    parser.add_argument("--response-format", choices=["url", "b64_json"], default="url", help="Response format")
    parser.add_argument("--prompt-mode", choices=["standard", "fast"], help="Prompt optimization mode (fast only for 4.0)")
    parser.add_argument("--timeout", "-t", type=int, default=1200, help="Timeout in seconds")
    parser.add_argument("--no-watermark", action="store_true", help="Disable watermark")
    parser.add_argument("--stream", action="store_true", help="Enable streaming request (non-blocking server side)")
    
    args = parser.parse_args()

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    # Set default size if not provided
    size = args.size
    if not size:
        if args.version in ["4.0", "4.5", "5.0-lite", "5.0"]:
            size = "2K"
        else:
            size = "2048x2048"

    task = {
        "prompt": args.prompt,
        "size": size,
        "response_format": args.response_format,
        "watermark": not args.no_watermark,
        "stream": args.stream
    }

    if args.version in ["5.0", "5.0-lite"]:
        task["output_format"] = args.output_format
    
    if args.prompt_mode:
        task["prompt_mode"] = args.prompt_mode
    
    if args.images:
        task["image"] = args.images
    elif args.image:
        task["image"] = args.image

    if args.group:
        task["sequential_image_generation"] = "auto"
        task["max_images"] = max(1, min(15, args.max_images))

    result = asyncio.run(seedream_generate([task], version=args.version, timeout=args.timeout))
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
