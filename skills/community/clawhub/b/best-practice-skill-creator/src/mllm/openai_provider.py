"""OpenAI-compatible MLLM provider (GPT-5.4 and compatible APIs)."""

import httpx

from .base import MLLMProvider, MLLMResponse


class OpenAIProvider(MLLMProvider):
    """Provider for OpenAI Chat Completions API (GPT-5.4+)."""

    def analyze_images(
        self, images_base64: list[str], prompt: str
    ) -> MLLMResponse:
        content = [{"type": "text", "text": prompt}]
        for img_b64 in images_base64:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_b64}",
                        "detail": "high",
                    },
                }
            )

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": content}],
            "max_tokens": 4096,
        }

        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=120) as client:
            resp = client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        choice = data["choices"][0]
        return MLLMResponse(
            text=choice["message"]["content"],
            model=data.get("model", self.model),
            usage=data.get("usage"),
        )
