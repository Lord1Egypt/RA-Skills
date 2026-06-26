import base64
import io
import os
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

import requests
from google import genai
from google.genai import types
from PIL import Image

ROOT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = ROOT_DIR / "output"


def _normalize_env_value(value: str) -> str:
    value = (value or "").strip()
    # tolerate accidental wrapping quotes in .env, e.g. "https://..."
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("\"", "'"):
        value = value[1:-1].strip()
    return value


def _resolve_existing_image_path(image_path: str) -> Optional[Path]:
    path = Path(image_path)
    if path.exists():
        return path

    root_relative = ROOT_DIR / image_path
    if root_relative.exists():
        return root_relative

    return None


def build_image_part(image_path: str):
    path = _resolve_existing_image_path(image_path)
    if not path:
        return None

    with Image.open(path) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buf = io.BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)
        return types.Part.from_bytes(mime_type="image/png", data=buf.getvalue())


def image_to_data_url(image_path: str) -> str:
    path = _resolve_existing_image_path(image_path)
    if not path:
        return ""

    with Image.open(path) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buf = io.BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)

    b64_data = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_data}"


def save_images(response, output_dir: Path | None = None, prefix: str = "") -> List[str]:
    dest = output_dir or OUTPUT_DIR
    dest.mkdir(exist_ok=True)
    files: List[str] = []

    # Gemini response object
    if hasattr(response, "candidates") and response.candidates:
        for part in response.candidates[0].content.parts:
            inline_data = getattr(part, "inline_data", None)
            if not inline_data:
                continue

            filename = f"{prefix}ellya_{os.getpid()}_{len(files)}.png"
            file_path = dest / filename
            with open(file_path, "wb") as f:
                f.write(inline_data.data)
            files.append(str(file_path))
            print(f"Saved image: {file_path}")

        return files

    # Minimax response data structure (dict)
    if isinstance(response, dict):
        image_urls = response.get("image_urls", [])
        image_base64s = response.get("image_base64", [])

        for url in image_urls:
            try:
                r = requests.get(url)
                r.raise_for_status()
                filename = f"{prefix}ellya_{os.getpid()}_{len(files)}.png"
                file_path = dest / filename
                with open(file_path, "wb") as f:
                    f.write(r.content)
                files.append(str(file_path))
                print(f"Saved image from URL: {file_path}")
            except Exception as exc:
                print(f"Failed to download image from URL {url}: {exc}")

        for b64_data in image_base64s:
            try:
                image_data = base64.b64decode(b64_data)
                filename = f"{prefix}ellya_{os.getpid()}_{len(files)}.png"
                file_path = dest / filename
                with open(file_path, "wb") as f:
                    f.write(image_data)
                files.append(str(file_path))
                print(f"Saved image from base64: {file_path}")
            except Exception as exc:
                print(f"Failed to decode base64 image: {exc}")

        return files

    print("No recognizable image response found")
    return files


class BaseImageProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_images(self, prompt: str, input_images: Optional[List[str]] = None) -> List[str]:
        raise NotImplementedError


class GeminiProvider(BaseImageProvider):
    def generate_images(self, prompt: str, input_images: Optional[List[str]] = None) -> List[str]:
        client = genai.Client(api_key=self.api_key)

        image_parts = []
        for image_path in input_images or []:
            part = build_image_part(image_path)
            if part:
                image_parts.append(part)
                print(f"Loaded reference image: {image_path}")
            else:
                print(f"Reference image not found: {image_path}")

        final_prompt = prompt.strip() or ""
        print(f"Final prompt: {final_prompt}")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[*image_parts, final_prompt],
        )

        return save_images(response)


MAX_MINIMAX_PROMPT_LENGTH = 1500
MINIMAX_TEXT_MODEL = "MiniMax-M2.7"
MINIMAX_IMAGE_MODEL = "image-01"
MINIMAX_IMAGE_ASPECT_RATIO = "1:1"
MINIMAX_IMAGE_RESPONSE_FORMAT = "url"
MINIMAX_IMAGE_N = 1
MINIMAX_IMAGE_PROMPT_OPTIMIZER = True


class MinimaxProvider(BaseImageProvider):
    @staticmethod
    def _require_env(name: str) -> str:
        value = _normalize_env_value(os.environ.get(name, ""))
        if not value:
            raise RuntimeError(f"{name} is not configured")
        return value

    def _resolve_base_url(self) -> str:
        base_url = self._require_env("MINIMAX_BASE_URL").rstrip("/")
        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise RuntimeError(f"MINIMAX_BASE_URL is invalid: {base_url}")
        return base_url

    def _resolve_text_url(self) -> str:
        text_url = _normalize_env_value(os.environ.get("MINIMAX_TEXT_LLM_URL", ""))
        if text_url:
            parsed = urlparse(text_url)
            if not parsed.scheme or not parsed.netloc:
                raise RuntimeError(f"MINIMAX_TEXT_LLM_URL is invalid: {text_url}")
            return text_url.rstrip("/")
        return f"{self._resolve_base_url()}/anthropic"

    def _resolve_image_url(self) -> str:
        image_url = _normalize_env_value(os.environ.get("MINIMAX_IMAGE_URL", ""))
        if image_url:
            parsed = urlparse(image_url)
            if not parsed.scheme or not parsed.netloc:
                raise RuntimeError(f"MINIMAX_IMAGE_URL is invalid: {image_url}")
            return image_url
        return f"{self._resolve_base_url()}/v1/image_generation"

    @classmethod
    def validate_config(cls) -> None:
        base_url = _normalize_env_value(os.environ.get("MINIMAX_BASE_URL", ""))
        api_key = _normalize_env_value(os.environ.get("MINIMAX_API_KEY", ""))
        if not api_key:
            raise RuntimeError("MINIMAX_API_KEY is not configured")
        if not base_url:
            raise RuntimeError("MINIMAX_BASE_URL is not configured")
        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise RuntimeError(f"MINIMAX_BASE_URL is invalid: {base_url}")

    def _prepare_reference(self, input_images: Optional[List[str]] = None) -> Optional[List[dict]]:
        if not input_images:
            return None
        refs = []
        for img in input_images:
            if img.startswith("http") or img.startswith("data:"):
                refs.append({"type": "character", "image_file": img})
            else:
                data_url = image_to_data_url(img)
                if data_url:
                    refs.append({"type": "character", "image_file": data_url})
                else:
                    print(f"Failed to convert reference image to data URL: {img}")
        return refs or None

    def _optimize_prompt_llm(self, prompt: str) -> str:
        max_prompt_len = MAX_MINIMAX_PROMPT_LENGTH
        prompt = (prompt or "").strip()
        if len(prompt) <= max_prompt_len:
            return prompt

        minimax_text_url = self._resolve_text_url()
        minimax_model = MINIMAX_TEXT_MODEL

        rewrite_instruction = (
            "Rewrite this image generation prompt so the final text is <=1500 characters. "
            "Hard constraint: the final output MUST be 1500 characters or fewer. "
            "Preserve original content, order, and wording as much as possible. "
            "Only optimize, shorten, or generalize facial-feature details (face shape, eyes, nose, mouth, skin texture, identity-specific facial traits). "
            "Do not remove or simplify non-facial details such as subject, pose, outfit, scene, composition, lighting, camera, style, mood, color, and effects. "
            "Do not rewrite the full prompt into a summary. "
            "Avoid over-compression; keep output length close to 1500 characters (prefer 1450-1500 when possible). "
            "Output only the rewritten prompt.\n\n"
            f"{prompt}"
        )

        system_instruction = (
            "You are a strict prompt editor. Keep almost all original wording and structure, "
            "only reduce facial-feature details when needed to fit <=1500 characters. "
            "Hard constraint: never output more than 1500 characters. "
            "Do not over-compress. Preserve non-facial details."
        )

        # Prefer Anthropic-compatible SDK against Minimax-compatible endpoint.
        try:
            import anthropic

            client = anthropic.Anthropic(
                api_key=self.api_key,
                base_url=minimax_text_url,
            )
            response = client.messages.create(
                model=minimax_model,
                max_tokens=1000,
                system=system_instruction,
                messages=[
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": rewrite_instruction}],
                    }
                ],
            )

            optimized = ""
            for block in response.content:
                if getattr(block, "type", "") == "text":
                    optimized += block.text
            optimized = optimized.strip()

            if optimized:
                if len(optimized) > max_prompt_len:
                    print(
                        f"Minimax prompt optimization returned {len(optimized)} chars; "
                        f"truncate to {max_prompt_len} chars."
                    )
                    optimized = optimized[:max_prompt_len].rstrip()
                return optimized
        except Exception as exc:
            print(f"Anthropic SDK optimization failed: {exc}")

        # Fallback to direct HTTP in case SDK is unavailable/incompatible.
        http_payload = {
            "model": minimax_model,
            "max_tokens": 1000,
            "system": system_instruction,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": rewrite_instruction}],
                }
            ],
        }
        http_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }

        for url in (f"{minimax_text_url}/v1/messages", f"{minimax_text_url}/messages", minimax_text_url):
            try:
                resp = requests.post(url, headers=http_headers, json=http_payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                blocks = data.get("content", [])
                optimized = "".join(
                    b.get("text", "")
                    for b in blocks
                    if isinstance(b, dict) and b.get("type") == "text"
                ).strip()
                if optimized:
                    if len(optimized) > max_prompt_len:
                        print(
                            f"HTTP prompt optimization returned {len(optimized)} chars; "
                            f"truncate to {max_prompt_len} chars."
                        )
                        optimized = optimized[:max_prompt_len].rstrip()
                    return optimized
            except Exception as exc:
                print(f"HTTP optimization failed ({url}): {exc}")

        print(
            "Minimax prompt optimization unavailable; "
            "keep original prompt unchanged."
        )
        return prompt

    def generate_images(self, prompt: str, input_images: Optional[List[str]] = None) -> List[str]:
        print(f"Original prompt length: {len(prompt)}")
        original_prompt = prompt
        prompt = self._optimize_prompt_llm(prompt)
        if prompt != original_prompt:
            print(f"Optimized prompt length: {len(prompt)}")
        else:
            print(f"Prompt length after check: {len(prompt)}")
        payload = {
            "model": MINIMAX_IMAGE_MODEL,
            "prompt": prompt,
            "aspect_ratio": MINIMAX_IMAGE_ASPECT_RATIO,
            "response_format": MINIMAX_IMAGE_RESPONSE_FORMAT,
            "n": MINIMAX_IMAGE_N,
            "prompt_optimizer": MINIMAX_IMAGE_PROMPT_OPTIMIZER,
        }

        subject_reference = self._prepare_reference(input_images)
        if subject_reference:
            payload["subject_reference"] = subject_reference

        response = requests.post(
            self._resolve_image_url(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("base_resp", {}).get("status_code") != 0:
            raise RuntimeError(f"Minimax API error: {data}")

        return save_images(data.get("data", {}))


def create_provider(provider: str) -> BaseImageProvider:
    provider = provider.lower()
    if provider == "minimax":
        MinimaxProvider.validate_config()
        api_key = _normalize_env_value(os.environ.get("MINIMAX_API_KEY", ""))
        return MinimaxProvider(api_key)

    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        return GeminiProvider(api_key)

    raise ValueError(f"Unknown provider: {provider}")


def available_providers() -> list[str]:
    providers = []
    if os.environ.get("MINIMAX_API_KEY", "").strip() and os.environ.get("MINIMAX_BASE_URL", "").strip():
        providers.append("minimax")
    if os.environ.get("GEMINI_API_KEY"):
        providers.append("gemini")
    return providers


def resolve_provider(provider: str | None = None) -> str:
    if provider:
        if provider.lower() not in ["minimax", "gemini"]:
            raise ValueError(f"Unknown provider: {provider}")
        return provider.lower()

    configured = available_providers()
    if not configured:
        raise RuntimeError("No provider is configured. Set MINIMAX_API_KEY + MINIMAX_BASE_URL, or GEMINI_API_KEY.")

    if "minimax" in configured:
        return "minimax"
    return "gemini"




