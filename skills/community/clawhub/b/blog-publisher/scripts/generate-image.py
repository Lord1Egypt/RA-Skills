#!/usr/bin/env python3
"""
AI 이미지 생성 스크립트 (Google AI Studio 또는 OpenRouter 지원).

Usage:
    # Google AI Studio 사용 (기본값 - GOOGLE_API_KEY 필요)
    python3 generate-image.py --prompt "이미지 설명" --output /path/to/output.png
    
    # OpenRouter 사용 (OPENROUTER_API_KEY 필요)
    python3 generate-image.py --prompt "이미지 설명" --output /path/to/output.png --provider openrouter
    
    # 스타일 추가
    python3 generate-image.py --prompt "이미지 설명" --output /path/to/output.png --style "스타일 설명"

Environment:
    GOOGLE_API_KEY       - Google AI Studio API key (provider=google 사용시)
    OPENROUTER_API_KEY   - OpenRouter API key (provider=openrouter 사용시)
    IMAGE_PROVIDER       - 기본 제공자 설정 (google 또는 openrouter, 기본값: google)
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

# Load .env from skill directory
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                if key not in os.environ:
                    os.environ[key] = value

# Provider settings
DEFAULT_PROVIDER = os.environ.get("IMAGE_PROVIDER", "openrouter")  # "openrouter" 또는 "google"

# Google AI Studio settings
GOOGLE_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
GOOGLE_MODEL = "gemini-3-pro-image-preview"  # 또는 "gemini-2.0-flash-exp-image-generation"

# OpenRouter settings
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "google/gemini-3-pro-image-preview"


def generate_image_google(prompt: str, output: str, model: str = GOOGLE_MODEL, style: str = None):
    """Google AI Studio를 사용하여 이미지 생성"""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if style:
        prompt = f"{prompt} {style}"

    url = f"{GOOGLE_BASE_URL}/{model}:generateContent?key={api_key}"

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"ERROR: Google API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Google 응답에서 이미지 추출
    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            img_bytes = base64.b64decode(part["inlineData"]["data"])
            with open(output, "wb") as f:
                f.write(img_bytes)
            print(f"OK: {output} ({len(img_bytes)} bytes) [Google AI Studio]")
            return
        elif "text" in part:
            print(f"TEXT: {part['text'][:200]}")

    print("ERROR: No image in Google response", file=sys.stderr)
    sys.exit(1)


def generate_image_openrouter(prompt: str, output: str, model: str = OPENROUTER_MODEL, style: str = None):
    """OpenRouter를 사용하여 이미지 생성"""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if style:
        prompt = f"{prompt} {style}"

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"]
    }).encode()

    req = urllib.request.Request(
        OPENROUTER_BASE_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://sonim1.com",
            "X-Title": "Blog Publisher"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"ERROR: OpenRouter API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    # OpenRouter 응답에서 이미지 추출
    if data.get("choices"):
        message = data["choices"][0].get("message", {})
        
        if message.get("images"):
            for image in message["images"]:
                image_url = image.get("image_url", {}).get("url", "")
                if image_url.startswith("data:image"):
                    match = re.match(r"data:image/[^;]+;base64,(.+)", image_url)
                    if match:
                        img_bytes = base64.b64decode(match.group(1))
                        with open(output, "wb") as f:
                            f.write(img_bytes)
                        print(f"OK: {output} ({len(img_bytes)} bytes) [OpenRouter]")
                        return
        
        if message.get("content"):
            print(f"TEXT: {message['content'][:200]}")

    print("ERROR: No image in OpenRouter response", file=sys.stderr)
    sys.exit(1)


def generate_image(prompt: str, output: str, provider: str = None, model: str = None, style: str = None):
    """설정된 제공자로 이미지 생성"""
    provider = provider or DEFAULT_PROVIDER
    
    if provider == "google":
        model = model or GOOGLE_MODEL
        # Google 모델은 접두사 없이 사용
        if model.startswith("google/"):
            model = model.replace("google/", "")
        generate_image_google(prompt, output, model, style)
    elif provider == "openrouter":
        model = model or OPENROUTER_MODEL
        generate_image_openrouter(prompt, output, model, style)
    else:
        print(f"ERROR: Unknown provider: {provider}. Use 'google' or 'openrouter'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate image via AI API (Google AI Studio or OpenRouter)")
    parser.add_argument("--prompt", required=True, help="Image prompt")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--provider", default=DEFAULT_PROVIDER, choices=["google", "openrouter"],
                        help=f"API provider to use (default: {DEFAULT_PROVIDER})")
    parser.add_argument("--model", default=None, help="Model name (provider-specific)")
    parser.add_argument("--style", default=None, help="Style suffix appended to prompt")
    args = parser.parse_args()

    generate_image(args.prompt, args.output, args.provider, args.model, args.style)
