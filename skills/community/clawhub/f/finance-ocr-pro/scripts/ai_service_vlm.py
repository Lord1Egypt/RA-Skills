"""VLM (Vision-Language Model) service client.

Sends text + image requests to an OpenAI-compatible API and returns
clean Markdown with any outer code fences stripped automatically.

Each call creates a fresh HTTP connection to avoid timeouts during
long-running batch OCR jobs (e.g. hundreds or thousands of pages).

Configuration (environment variables or .env beside this script):
    API_KEY   – API key
    BASE_URL  – API base URL
    VLM_MODEL – Model identifier
"""

from __future__ import annotations

import base64
import logging
import mimetypes
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent

_dotenv = _SKILL_ROOT / ".env"
if not _dotenv.exists():
    _dotenv = _SCRIPT_DIR / ".env"
load_dotenv(dotenv_path=_dotenv if _dotenv.exists() else None)

logger = logging.getLogger(__name__)

_OUTER_FENCE_RE = re.compile(
    r"\A\s*```(?:markdown|md)?\s*\n(.*)\n\s*```\s*\Z",
    re.DOTALL,
)


def image_encode(image_path: str | Path) -> str:
    """Encode a local image as a ``data:<mime>;base64,…`` URL."""
    path = Path(image_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _resolve_image(source: str | Path | None) -> str | None:
    """Normalise *source* to a URL the API accepts (local path, http(s), or data URL)."""
    if source is None:
        return None
    text = str(source).strip()
    if text.lower().startswith(("http://", "https://", "data:")):
        return text
    return image_encode(text)


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise OSError(f"Missing required environment variable: {name}")
    return value


def _make_client() -> tuple[OpenAI, str]:
    """Create a fresh OpenAI client and return *(client, model)*.

    A new client (and underlying HTTP connection) is created on every
    call so that long-running batch jobs never hit idle-connection
    timeouts imposed by the API provider or intermediate proxies.
    """
    api_key  = _require_env("API_KEY")
    base_url = _require_env("BASE_URL")
    model    = _require_env("VLM_MODEL")

    client = OpenAI(api_key=api_key, base_url=base_url)
    logger.debug("OpenAI client created for model=%s", model)
    return client, model


def _mock_response() -> str | None:
    """Return a configured mock OCR response for local smoke tests, if any."""
    mock_path = os.getenv("OCR_MOCK_RESPONSE_FILE")
    if mock_path:
        text = Path(mock_path).expanduser().read_text(encoding="utf-8")
        return strip_outer_fence(text)

    mock_text = os.getenv("OCR_MOCK_RESPONSE_TEXT")
    if mock_text:
        return strip_outer_fence(mock_text)

    return None


def strip_outer_fence(text: str) -> str:
    """Remove a single outer ``markdown`` / ``md`` / bare code fence.

    Internal fences (e.g. ``mermaid``) are preserved because the regex
    only matches fences tagged ``markdown``, ``md``, or with no tag.
    A greedy inner group ensures the *last* closing fence at EOF is
    matched, so nested fences are never consumed.
    """
    m = _OUTER_FENCE_RE.match(text)
    return m.group(1) if m else text


def ai_request(prompt: str, image_url: str | Path | None = None) -> str:
    """Send *prompt* (with optional image) to the VLM and return clean Markdown.

    A fresh HTTP connection is established for each call to prevent
    timeout issues during long-running batch OCR operations.

    The response is automatically unwrapped if the model enclosed it in a
    single outer ``markdown`` code fence.
    """
    prompt = (prompt or "").strip()
    if not prompt:
        raise ValueError("prompt must be a non-empty string.")

    mocked = _mock_response()
    if mocked is not None:
        logger.debug("Using mock OCR response from environment.")
        return mocked

    client, model = _make_client()

    content: list[dict] = [{"type": "text", "text": prompt}]
    image = _resolve_image(image_url)
    if image:
        content.insert(0, {"type": "image_url", "image_url": {"url": image}})

    logger.debug("Sending request to %s (image=%s)", model, image is not None)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
            temperature=0.3,
        )
    except APIError as exc:
        status_code = getattr(exc, "status_code", None)
        message = getattr(exc, "message", None) or str(exc)
        if status_code is None:
            raise RuntimeError(f"API request failed: {message}") from exc
        raise RuntimeError(f"API request failed ({status_code}): {message}") from exc

    if not response.choices:
        raise RuntimeError("Model returned no choices.")

    raw = response.choices[0].message.content or ""
    return strip_outer_fence(raw)


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Send a text+image request to a VLM and print the response.",
    )
    parser.add_argument(
        "-p", "--prompt",
        default="Please extract the contents from the page.",
        help="Prompt to send (default: OCR extraction prompt)",
    )
    parser.add_argument(
        "-i", "--image",
        default=None,
        help="Path or URL of the image to send (default: $VLM_TEST_IMAGE env var)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    image = args.image or os.getenv("VLM_TEST_IMAGE")
    print("Prompt:", args.prompt)
    print("Image: ", image or "(none)")
    print("\n----------- Answer -----------")
    print(ai_request(prompt=args.prompt, image_url=image))


if __name__ == "__main__":
    _cli()
