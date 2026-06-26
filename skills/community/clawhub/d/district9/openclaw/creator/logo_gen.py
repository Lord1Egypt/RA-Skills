"""Logo generation for tokens via image generation APIs."""

import base64
import os
import tempfile
import time

from ..utils.logger import log

# OpenRouter image models (ordered by cost-effectiveness)
OPENROUTER_IMAGE_MODELS = [
    "google/gemini-3.1-flash-image-preview",
    "google/gemini-2.5-flash-image",
    "google/gemini-3-pro-image-preview",
    "openai/gpt-5-image-mini",
]


class LogoGenerator:
    """Generate token logos using LLM image generation."""

    def __init__(self, provider: str, api_key: str, base_url: str | None = None):
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url

    def generate(self, token_name: str, narrative: str, logo_prompt: str) -> str:
        """
        Generate a token PFP logo matching the narrative.

        Returns local file path, or empty string on failure.
        """
        prompt = self._build_prompt(token_name, narrative, logo_prompt)

        try:
            if self.provider == "openrouter":
                return self._generate_openrouter(prompt)
            else:
                return self._generate_openai(prompt)
        except Exception as e:
            log.warning(f"Logo generation failed: {e}")
            return ""

    def _build_prompt(self, token_name: str, narrative: str, logo_prompt: str) -> str:
        return (
            f"Generate a 1:1 square token profile picture (PFP) for a meme coin called '{token_name}'. "
            f"Concept: {logo_prompt}. "
            f"Context: {narrative[:200]}. "
            f"Requirements: "
            f"- Circular token logo style, centered subject "
            f"- Vivid, saturated colors with clean edges "
            f"- Bold, iconic, instantly recognizable at small sizes "
            f"- NO text, NO letters, NO words anywhere in the image "
            f"- Flat or semi-flat illustration style, suitable as a crypto token icon "
            f"- Single subject/character on a solid or gradient background"
        )

    def _generate_openai(self, prompt: str) -> str:
        """Generate via OpenAI DALL-E."""
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        resp = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
            response_format="b64_json",
        )

        b64 = resp.data[0].b64_json
        return self._save_image(base64.b64decode(b64))

    def _generate_openrouter(self, prompt: str, max_retries: int = 3) -> str:
        """Generate via OpenRouter image model with retry logic."""
        import requests

        base = self.base_url or "https://openrouter.ai/api/v1"
        url = f"{base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        for model in OPENROUTER_IMAGE_MODELS:
            for attempt in range(1, max_retries + 1):
                try:
                    log.info(f"Logo gen attempt {attempt}/{max_retries} ({model})...")
                    resp = requests.post(
                        url,
                        headers=headers,
                        json={
                            "model": model,
                            "messages": [{"role": "user", "content": prompt}],
                            "modalities": ["image", "text"],
                        },
                        timeout=90,
                    )
                    resp.raise_for_status()
                    data = resp.json()

                    message = data.get("choices", [{}])[0].get("message", {})
                    img_b64 = self._extract_image_b64(message)
                    if img_b64:
                        return self._save_image(base64.b64decode(img_b64))

                    log.warning(f"No image in response (attempt {attempt})")

                except requests.exceptions.HTTPError as e:
                    if e.response is not None and e.response.status_code == 429:
                        log.warning(f"Rate limited, waiting 5s...")
                        time.sleep(5)
                    else:
                        log.warning(f"HTTP error: {e}")
                except Exception as e:
                    log.warning(f"Attempt {attempt} error: {e}")

                if attempt < max_retries:
                    time.sleep(2)

            log.warning(f"All retries failed for {model}, trying next model...")

        return ""

    @staticmethod
    def _extract_image_b64(message: dict) -> str:
        """Extract base64 image data from an OpenRouter response message."""
        # Format: images: [{"type": "image_url", "image_url": {"url": "data:...;base64,XXX"}}]
        for img in message.get("images", []):
            if isinstance(img, dict):
                url = img.get("image_url", {}).get("url", "")
                if url.startswith("data:") and ";base64," in url:
                    return url.split(";base64,", 1)[1]
            elif isinstance(img, str):
                return img

        # Fallback: check content parts
        content = message.get("content")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:") and ";base64," in url:
                        return url.split(";base64,", 1)[1]

        return ""

    def _save_image(self, image_bytes: bytes) -> str:
        """Save image bytes to a temp file, return path."""
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False, prefix="openclaw_logo_")
        tmp.write(image_bytes)
        tmp.close()
        log.info(f"Logo saved: {tmp.name}")
        return tmp.name
