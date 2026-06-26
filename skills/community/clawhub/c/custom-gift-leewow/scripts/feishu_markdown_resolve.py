#!/usr/bin/env python3
from __future__ import annotations

"""Resolve Markdown image refs to Feishu message image_key for IM markdown.

Mirrors leewow-skills/scripts/channel_messaging/feishu.py upload/replace logic.
On missing credentials or per-image failure, callers can fall back to safe
preview links instead of broken markdown images.
"""

import hashlib
import json
import mimetypes
import os
import re
import threading
from pathlib import Path
from typing import Dict

import requests

DEFAULT_DOMAIN = "https://open.feishu.cn"
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
CACHE_PATH = Path.home() / ".openclaw" / "cache" / "feishu_image_keys.json"


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else value


def feishu_resolve_credentials_ready() -> bool:
    return bool(_env("FEISHU_APP_ID") and _env("FEISHU_APP_SECRET"))


def _load_cache() -> dict[str, str]:
    if not CACHE_PATH.exists():
        return {}
    try:
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def _save_cache(data: dict[str, str]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _looks_like_remote_url(ref: str) -> bool:
    return ref.startswith("http://") or ref.startswith("https://")


def _looks_like_feishu_image_key(ref: str) -> bool:
    # Already resolved keys should not be fetched/uploaded again
    return ref.startswith("img_")


class FeishuMarkdownImageResolver:
    """One instance per browse batch: reuses tenant token and upload cache."""

    def __init__(self) -> None:
        self.domain = (_env("FEISHU_OPEN_BASE", DEFAULT_DOMAIN) or DEFAULT_DOMAIN).rstrip("/")
        self.app_id = _env("FEISHU_APP_ID") or ""
        self.app_secret = _env("FEISHU_APP_SECRET") or ""
        self.token: str | None = None
        self.image_cache = _load_cache()
        self._enabled = bool(self.app_id and self.app_secret)
        self._lock = threading.Lock()

    def resolve(self, markdown: str) -> tuple[str, bool]:
        """Return (markdown, True) if any ![](...) was replaced with image_key."""
        if not self._enabled or not markdown:
            return markdown, False
        try:
            token = self._get_token()
        except Exception:
            return markdown, False

        replacements: Dict[str, str] = {}
        any_changed = False

        def replace(match: re.Match[str]) -> str:
            nonlocal any_changed
            alt = match.group(1)
            image_ref = match.group(2).strip()
            if _looks_like_feishu_image_key(image_ref):
                return match.group(0)
            if not _looks_like_remote_url(image_ref):
                p = Path(image_ref).expanduser()
                if not p.is_file():
                    return match.group(0)

            if image_ref not in replacements:
                try:
                    replacements[image_ref] = self._upload_image(token, image_ref)
                except Exception:
                    replacements[image_ref] = image_ref

            new_ref = replacements[image_ref]
            if new_ref != image_ref:
                any_changed = True
            return f"![{alt}]({new_ref})"

        out = MARKDOWN_IMAGE_RE.sub(replace, markdown)
        return out, any_changed

    def resolve_image_ref(self, image_ref: str) -> str | None:
        """Resolve one local/remote image reference to a Feishu image_key.

        Returns None when credentials are unavailable or the upload fails.
        """
        if not self._enabled:
            return None
        try:
            token = self._get_token()
            return self._upload_image(token, image_ref)
        except Exception:
            return None

    def _get_token(self) -> str:
        if self.token:
            return self.token
        with self._lock:
            if self.token:
                return self.token
            response = requests.post(
                f"{self.domain}/open-apis/auth/v3/tenant_access_token/internal",
                json={"app_id": self.app_id, "app_secret": self.app_secret},
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            if payload.get("code") != 0:
                raise RuntimeError(f"Token API failed: {json.dumps(payload, ensure_ascii=False)}")
            token = payload.get("tenant_access_token")
            if not token:
                raise RuntimeError("tenant_access_token missing from Feishu response")
            self.token = str(token)
            return self.token

    def _upload_image(self, token: str, image_ref: str) -> str:
        image_bytes, filename = self._load_image_bytes(image_ref)
        cache_key = hashlib.sha256(image_bytes).hexdigest()
        with self._lock:
            cached = self.image_cache.get(cache_key)
            if cached:
                return cached

        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        response = requests.post(
            f"{self.domain}/open-apis/im/v1/images",
            headers={"Authorization": f"Bearer {token}"},
            data={"image_type": "message"},
            files={"image": (filename, image_bytes, content_type)},
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise RuntimeError(f"Image upload failed: {json.dumps(payload, ensure_ascii=False)}")
        image_key = ((payload.get("data") or {}).get("image_key") or "").strip()
        if not image_key:
            raise RuntimeError(f"Image upload missing image_key: {json.dumps(payload, ensure_ascii=False)}")

        with self._lock:
            cached = self.image_cache.get(cache_key)
            if cached:
                return cached
            self.image_cache[cache_key] = image_key
            _save_cache(self.image_cache)
        return image_key

    @staticmethod
    def _load_image_bytes(image_ref: str) -> tuple[bytes, str]:
        image_path = Path(image_ref).expanduser()
        if image_path.is_file():
            return image_path.read_bytes(), image_path.name

        response = requests.get(image_ref, timeout=30)
        response.raise_for_status()
        filename = Path(image_ref.split("?", 1)[0]).name or "image.png"
        return response.content, filename


def resolve_feishu_markdown_images(markdown: str) -> tuple[str, bool]:
    """Convenience: one-shot resolve using a fresh resolver (prefer batch FeishuMarkdownImageResolver)."""
    return FeishuMarkdownImageResolver().resolve(markdown)


def fallback_markdown_images_to_links(markdown: str) -> str:
    """Replace markdown images with plain preview links.

    This avoids shipping broken `![...](https://...)` markdown to Feishu when
    image_key resolution is unavailable.
    """

    def replace(match: re.Match[str]) -> str:
        alt = match.group(1).strip() or "Preview"
        image_ref = match.group(2).strip()
        if _looks_like_feishu_image_key(image_ref):
            return match.group(0)
        return f"[Preview: {alt}]({image_ref})"

    return MARKDOWN_IMAGE_RE.sub(replace, markdown)
