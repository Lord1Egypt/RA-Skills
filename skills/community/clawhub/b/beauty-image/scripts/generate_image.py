#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Generate images using Beauty Image API (Alibaba Cloud DashScope).

作者: 圆规
GitHub: https://github.com/xyva-yuangui/beauty-image
License: MIT

Usage:
    uv run generate_image.py --prompt "your image description" --filename "output.png" [--model wan2.6-t2i|wan2.5-t2i-preview] [--size 1280*1280|1696*960|960*1696] [--api-key KEY]
"""

import argparse
import os
import sys
import json
import time
import base64
from pathlib import Path


def _read_openclaw_config_key() -> str | None:
    """Read API key from ~/.openclaw/openclaw.json → models.providers.wanxiang.apiKey."""
    try:
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        with open(config_path) as f:
            config = json.load(f)
        key = config.get("models", {}).get("providers", {}).get("wanxiang", {}).get("apiKey")
        if key and not key.startswith("sk-sp-"):
            return key
    except Exception:
        pass
    return None


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from provided arg, env var, or openclaw config.
    
    查找顺序:
      1. --api-key 参数 (跳过 sk-sp- 前缀的百炼 Key)
      2. 环境变量 DASHSCOPE_API_KEY
      3. ~/.openclaw/openclaw.json 配置
    
    获取地址: https://dashscope.console.aliyun.com/apiKey
    """
    if provided_key and not provided_key.startswith("sk-sp-"):
        return provided_key
    if provided_key and provided_key.startswith("sk-sp-"):
        print(f"⚠️ 忽略传入的百炼Key (sk-sp- 不支持万相图片生成)")
    
    env_key = os.environ.get("DASHSCOPE_API_KEY")
    if env_key:
        return env_key
    
    return _read_openclaw_config_key()


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Beauty Image API"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        help="Output filename (optional, if not provided will only return URL)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=[
            # 万相 2.6 系列（支持同步调用，推荐）
            "wan2.6-t2i",           # 最新版，支持自定义分辨率
            # 万相 2.5 及以下（异步调用）
            "wan2.5-t2i-preview",   # 预览版
            "wan2.2-t2i-flash",     # 极速版，性价比之王
            "wan2.2-t2i-plus",      # 专业版
            "wanx2.1-t2i-turbo",    # 2.1 极速版
            "wanx2.1-t2i-plus",     # 2.1 专业版
        ],
        default="wan2.6-t2i",
        help="Model to use: wan2.6-t2i (recommended), wan2.2-t2i-flash (best value)"
    )
    parser.add_argument(
        "--size", "-s",
        choices=["1664*928", "1024*1024", "720*1280", "1280*720"],
        default="1664*928",
        help="Output size (default: 1664*928 for 16:9 ratio)"
    )
    parser.add_argument(
        "--negative-prompt", "-n",
        default="低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
        help="Negative prompt to avoid unwanted elements"
    )
    parser.add_argument(
        "--no-prompt-extend",
        action="store_true",
        help="Disable automatic prompt enhancement"
    )
    parser.add_argument(
        "--watermark",
        action="store_true",
        help="Add watermark to generated image"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="DashScope API key (overrides DASHSCOPE_API_KEY env var)"
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        help="Disable SSL certificate verification (use with caution)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: 缺少通义万相 API Key (DASHSCOPE_API_KEY)", file=sys.stderr)
        print("请通过以下方式之一配置:", file=sys.stderr)
        print("  1. 设置环境变量: export DASHSCOPE_API_KEY=your-key", file=sys.stderr)
        print("  2. 传入参数: --api-key your-key", file=sys.stderr)
        print("  3. 在 ~/.openclaw/openclaw.json 中配置: models.providers.wanxiang.apiKey", file=sys.stderr)
        print("获取地址: https://dashscope.console.aliyun.com/apiKey", file=sys.stderr)
        sys.exit(1)

    # Import here after checking API key
    import requests

    # Set up output path

    print(f"Generating image with {args.model}...")
    print(f"Size: {args.size}")
    print(f"Prompt: {args.prompt}")

    # Determine API endpoint and build payload based on model series
    # wan2.6 uses synchronous multimodal-generation API (new protocol)
    # wan2.5 and below use asynchronous text2image API (old protocol)
    if args.model.startswith("wan2.6"):
        # Wanx 2.6 - Synchronous API (new protocol)
        api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
        payload = {
            "model": args.model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": args.prompt
                            }
                        ]
                    }
                ]
            },
            "parameters": {
                "negative_prompt": args.negative_prompt,
                "prompt_extend": not args.no_prompt_extend,
                "watermark": args.watermark,
                "size": args.size,
                "n": 1  # Default to 1 image for testing
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    else:
        # Wanx 2.5 and below - Asynchronous API (old protocol)
        api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
        payload = {
            "model": args.model,
            "input": {
                "prompt": args.prompt
            },
            "parameters": {
                "negative_prompt": args.negative_prompt,
                "prompt_extend": not args.no_prompt_extend,
                "watermark": args.watermark,
                "size": args.size,
                "n": 1  # Default to 1 image for testing
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "X-DashScope-Async": "enable"  # Required for async API
        }
    
    try:
        # Make API request
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=120,
            verify=True
        )

        response.raise_for_status()
        result = response.json()

        # Check for errors
        if result.get("code"):
            error_msg = result.get("message", "Unknown error")
            print(f"API Error: {error_msg}", file=sys.stderr)
            sys.exit(1)

        # Handle async API (wan2.5 and below) - need to poll for result
        if args.model.startswith("wan2.6"):
            # Synchronous API (wan2.6) - direct response with image URL
            output_data = result.get("output", {})
            choices = output_data.get("choices", [])
            
            if not choices:
                print("Error: No choices in response", file=sys.stderr)
                print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
                sys.exit(1)

            # Get image URL from first choice
            message = choices[0].get("message", {})
            content = message.get("content", [])
            
            if not content or not content[0].get("image"):
                print("Error: No image URL in response", file=sys.stderr)
                print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
                sys.exit(1)

            image_url = content[0]["image"]
            print(f"\nImage URL: {image_url}")
        else:
            # Asynchronous API (wan2.5 and below) - get task_id and poll
            output_data = result.get("output", {})
            task_id = output_data.get("task_id")
            
            if not task_id:
                print("Error: No task_id in response", file=sys.stderr)
                print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
                sys.exit(1)
            
            print(f"Task ID: {task_id}")
            print("Polling for result...")
            
            # Poll for task result
            image_url = None
            max_attempts = 30
            poll_interval = 10  # seconds
            
            for attempt in range(max_attempts):
                time.sleep(poll_interval)
                
                # Query task status
                task_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
                task_response = requests.get(
                    task_url,
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=30,
                    verify=True
                )
                task_response.raise_for_status()
                task_result = task_response.json()
                
                task_output = task_result.get("output", {})
                task_status = task_output.get("task_status", "UNKNOWN")
                
                print(f"Attempt {attempt + 1}/{max_attempts}: Status = {task_status}")
                
                if task_status == "SUCCEEDED":
                    # Extract image URL from result
                    # Async API uses "results" array, sync API uses "choices"
                    results = task_output.get("results", [])
                    if results and results[0].get("url"):
                        image_url = results[0]["url"]
                        print(f"\nImage URL: {image_url}")
                        break
                    
                    # Fallback to sync API format
                    choices = task_output.get("choices", [])
                    if choices:
                        message = choices[0].get("message", {})
                        content = message.get("content", [])
                        if content and content[0].get("image"):
                            image_url = content[0]["image"]
                            print(f"\nImage URL: {image_url}")
                            break
                    
                    print("Error: Task succeeded but no image URL found", file=sys.stderr)
                    print(f"Response: {json.dumps(task_result, indent=2, ensure_ascii=False)}", file=sys.stderr)
                    sys.exit(1)
                elif task_status == "FAILED":
                    print(f"Task failed: {task_result.get('message', 'Unknown error')}", file=sys.stderr)
                    sys.exit(1)
                elif task_status in ["PENDING", "RUNNING"]:
                    continue
                else:
                    print(f"Unknown task status: {task_status}", file=sys.stderr)
                    sys.exit(1)
            
            if not image_url:
                print("Error: Task timed out", file=sys.stderr)
                sys.exit(1)

        # If filename is provided, download and save the image
        if args.filename:
            output_path = Path(args.filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            print("Downloading image...")
            img_response = requests.get(image_url, timeout=30, verify=not args.no_verify_ssl)
            img_response.raise_for_status()

            # Save the image
            with open(output_path, "wb") as f:
                f.write(img_response.content)

            full_path = output_path.resolve()
            print(f"Image saved: {full_path}")
            # Clawdbot parses MEDIA tokens and will attach the file on supported providers.
            print(f"MEDIA: {full_path}")
        else:
            # Just return the URL for Clawdbot to display
            print(f"MEDIA_URL: {image_url}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        try:
            error_detail = response.json()
            print(f"Error details: {json.dumps(error_detail, indent=2, ensure_ascii=False)}", file=sys.stderr)
        except:
            print(f"Response text: {response.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
