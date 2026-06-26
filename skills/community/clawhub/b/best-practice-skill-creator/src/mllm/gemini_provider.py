"""Google Gemini MLLM provider (Gemini 3.1 Pro Preview and compatible)."""

import httpx

from .base import MLLMProvider, MLLMResponse


class GeminiProvider(MLLMProvider):
    """Provider for Google Gemini generateContent API."""

    def analyze_images(
        self, images_base64: list[str], prompt: str
    ) -> MLLMResponse:
        parts = [{"text": prompt}]
        for img_b64 in images_base64:
            parts.append(
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_b64,
                    }
                }
            )

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "maxOutputTokens": 4096,
                "temperature": 0.2,
            },
        }

        url = (
            f"{self.base_url.rstrip('/')}/models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )
        headers = {"Content-Type": "application/json"}

        with httpx.Client(timeout=120) as client:
            resp = client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        candidate = data["candidates"][0]
        text = candidate["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata")

        return MLLMResponse(
            text=text,
            model=self.model,
            usage=usage,
        )
