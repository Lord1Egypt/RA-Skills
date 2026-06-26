"""Aliyun voice provider (Qwen3-TTS-Flash)."""

import json

from common import api_post, extract_url


def generate(api_key, text):
    payload = {
        "model": "qwen3-tts-flash",
        "input": {"text": text, "voice": "Chelsie", "language_type": "Chinese"},
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    code, body = api_post(
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
        headers, payload,
    )
    print(f"Aliyun response ({code}): {json.dumps(body)[:500]}")
    if code < 200 or code >= 300:
        return None
    return extract_url(body)
