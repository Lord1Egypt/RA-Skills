"""ZAI voice provider (GLM-TTS)."""

import json

from common import api_post, extract_url


def generate(api_key, text):
    payload = {
        "model": "glm-tts",
        "input": {
            "text": text, "voice": "female",
            "speed": 1.0, "volume": 1.0, "response_format": "wav",
        },
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    code, body = api_post(
        "https://open.bigmodel.cn/api/paas/v4/audio/speech",
        headers, payload,
    )
    print(f"ZAI response ({code}): {json.dumps(body)[:500]}")
    if code < 200 or code >= 300:
        return None
    return extract_url(body)
