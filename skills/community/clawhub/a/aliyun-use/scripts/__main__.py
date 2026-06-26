#!/usr/bin/env python3
"""
AliYun Bailian LLM - Chat and translation tools.

Usage:
    python -m scripts chat --model qwen-plus --messages '[{"role": "user", "content": "Hello"}]'
    python -m scripts translate --text "Hello" --target-lang zh

Environment:
    ALIYUN_BAILIAN_API_KEY - Your Alibaba Cloud API key
    ALIYUN_BAILIAN_API_HOST - API base URL (default: https://coding.dashscope.aliyuncs.com/v1)
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional


# API Configuration
DEFAULT_BASE_URL = os.environ.get("ALIYUN_BAILIAN_API_HOST", "https://coding.dashscope.aliyuncs.com/apps/anthropic")

# Language map
LANG_MAP = {
    "en": "English", "zh": "Chinese", "ja": "Japanese", "ko": "Korean",
    "es": "Spanish", "fr": "French", "de": "German", "ru": "Russian",
    "ar": "Arabic", "pt": "Portuguese", "it": "Italian", "th": "Thai",
    "vi": "Vietnamese", "id": "Indonesian", "auto": "auto-detect"
}


def _get_credentials(api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL):
    key = api_key or os.environ.get("ALIYUN_BAILIAN_API_KEY")
    if not key:
        return None, None
    return key, base_url


def chat(
    messages: list,
    model: str = "qwen3.5-plus",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    stream: bool = False,
    api_key: Optional[str] = None,
    base_url: str = DEFAULT_BASE_URL
) -> dict:
    """
    General-purpose chat completion via DashScope Anthropic API.

    Args:
        messages: Array of {role, content}. Roles: system, user, assistant
        model: Model name. Default: qwen-plus
        temperature: Sampling temperature 0-1. Default: 0.7
        max_tokens: Max tokens to generate. Default: 2048
        stream: Enable streaming. Default: False
        api_key: ALIYUN_BAILIAN_API_KEY (or set env var)
        base_url: DashScope API base URL

    Returns:
        Success: {"success": True, "result": {"content": "...", "model": "...", "usage": {...}}}
        Failure: {"success": False, "error": "error message"}
    """
    key, url = _get_credentials(api_key, base_url)
    if not key:
        return {"success": False, "error": "ALIYUN_BAILIAN_API_KEY not set. Get one at: https://bailian.console.aliyun.com/"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "x-api-key": key,
        "anthropic-version": "2023-06-01"
    }

    # Convert messages to Anthropic format
    anthropic_messages = []
    system_content = None
    for msg in messages:
        if msg.get("role") == "system":
            system_content = msg.get("content", "")
        else:
            anthropic_messages.append({
                "role": msg.get("role"),
                "content": msg.get("content", "")
            })

    payload = {
        "model": model,
        "messages": anthropic_messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    if system_content:
        payload["system"] = system_content
    if stream:
        payload["stream"] = True

    api_url = f"{url}/v1/messages"

    try:
        if stream:
            response = requests.post(api_url, headers=headers, json=payload, stream=True, timeout=60)
            if not response.ok:
                return {"success": False, "error": f"{response.status_code}: {response.text}"}
            result = {"choices": [], "model": model}
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data:"):
                        data = json.loads(line[5:].strip())
                        if data.get("type") == "content_block_delta":
                            content = data.get("delta", {}).get("text", "")
                            if content:
                                print(content, end="", flush=True)
                                result["choices"].append({"delta": {"content": content}})
            print()
            return {"success": True, "result": result}
        else:
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            if not response.ok:
                return {"success": False, "error": f"{response.status_code}: {response.text}"}
            data = response.json()

            if data.get("type") == "error":
                return {"success": False, "error": data.get("error", {}).get("message", "Unknown error")}

            # Extract text content, skipping thinking blocks
            content = ""
            for block in data.get("content", []):
                if block.get("type") == "text":
                    content = block.get("text", "")
                    break
            return {
                "success": True,
                "result": {
                    "content": content,
                    "model": data.get("model", model),
                    "stop_reason": data.get("stop_reason"),
                    "usage": {
                        "input_tokens": data.get("usage", {}).get("input_tokens"),
                        "output_tokens": data.get("usage", {}).get("output_tokens")
                    }
                }
            }
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def translate(
    text: str,
    target_lang: str,
    source_lang: str = "auto",
    model: str = "qwen3.5-plus",
    api_key: Optional[str] = None,
    base_url: str = DEFAULT_BASE_URL
) -> dict:
    """
    Translate text between languages using the LLM.

    Args:
        text: Text to translate
        target_lang: Target language code (en, zh, ja, es, fr, de, etc.)
        source_lang: Source language. Default: auto (detect automatically)
        model: Model name. Default: qwen-plus
        api_key: ALIYUN_BAILIAN_API_KEY (or set env var)
        base_url: DashScope API base URL

    Returns:
        Success: {"success": True, "result": {"translated_text": "...", "source_lang": "...", "target_lang": "..."}}
        Failure: {"success": False, "error": "error message"}
    """
    key, url = _get_credentials(api_key, base_url)
    if not key:
        return {"success": False, "error": "ALIYUN_BAILIAN_API_KEY not set. Get one at: https://bailian.console.aliyun.com/"}

    source_display = LANG_MAP.get(source_lang, source_lang)
    target_display = LANG_MAP.get(target_lang, target_lang)

    system_prompt = (
        f"You are a professional translator. Translate the following text from "
        f"{source_display} to {target_display}. Only output the translated text, "
        f"nothing else. Do not include quotes or explanations."
    )

    anthropic_messages = [{"role": "user", "content": text}]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "x-api-key": key,
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": model,
        "messages": anthropic_messages,
        "system": system_prompt,
        "temperature": 0.3,
        "max_tokens": 4096
    }

    api_url = f"{url}/v1/messages"

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        if not response.ok:
            return {"success": False, "error": f"{response.status_code}: {response.text}"}
        data = response.json()

        if data.get("type") == "error":
            return {"success": False, "error": data.get("error", {}).get("message", "Unknown error")}

        # Extract text content, skipping thinking blocks
        translated = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                translated = block.get("text", "").strip()
                break

        return {
            "success": True,
            "result": {
                "translated_text": translated,
                "source_lang": source_lang if source_lang != "auto" else "detected",
                "target_lang": target_lang
            }
        }
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def models(api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL) -> dict:
    """List available models."""
    return {
        "success": True,
        "result": {
            "flagship": ["qwen3.5-plus", "qwen3-max-2026-01-23"],
            "coder": ["qwen3-coder-next", "qwen3-coder-plus"],
            "other": ["glm-5", "glm-4.7", "kimi-k2.5", "MiniMax-M2.5"]
        }
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "chat":
        parser = argparse.ArgumentParser(description="AliYun Bailian LLM Chat")
        parser.add_argument("--model", default="qwen-plus")
        parser.add_argument("--messages", required=True, help='JSON array of messages, e.g., [{\"role\": \"user\", \"content\": \"Hello\"}]')
        parser.add_argument("--temperature", type=float, default=0.7)
        parser.add_argument("--max-tokens", type=int, default=2048)
        parser.add_argument("--stream", action="store_true")
        parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
        args = parser.parse_args(sys.argv[2:])

        try:
            msgs = json.loads(args.messages)
        except json.JSONDecodeError as e:
            print(json.dumps({"success": False, "error": f"Invalid JSON: {e}"}))
            sys.exit(1)

        result = chat(
            messages=msgs,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            stream=args.stream,
            base_url=args.base_url
        )
        if args.stream:
            print(f"[Usage: {result.get('result', {}).get('usage', {})}]", file=sys.stderr)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "translate":
        parser = argparse.ArgumentParser(description="AliYun Bailian LLM Translation")
        parser.add_argument("--text", required=True, help="Text to translate")
        parser.add_argument("--target-lang", default="en", help="Target language code")
        parser.add_argument("--source-lang", default="auto", help="Source language code (default: auto)")
        parser.add_argument("--model", default="qwen-plus")
        parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
        args = parser.parse_args(sys.argv[2:])

        result = translate(
            text=args.text,
            target_lang=args.target_lang,
            source_lang=args.source_lang,
            model=args.model,
            base_url=args.base_url
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "models":
        result = models()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(json.dumps({"success": False, "error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
