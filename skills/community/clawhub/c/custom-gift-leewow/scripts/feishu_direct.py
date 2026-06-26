#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import mimetypes
import os
from pathlib import Path
from threading import Lock
from typing import Any

import requests


DEFAULT_DOMAIN = "https://open.feishu.cn"
DEFAULT_RECEIVE_ID_TYPE = "chat_id"
CACHE_PATH = Path.home() / ".openclaw" / "cache" / "feishu_image_keys.json"


class FeishuDirectClient:
    def __init__(
        self,
        app_id: str,
        app_secret: str,
        receive_id: str,
        receive_id_type: str = DEFAULT_RECEIVE_ID_TYPE,
        domain: str = DEFAULT_DOMAIN,
    ) -> None:
        self.app_id = app_id.strip()
        self.app_secret = app_secret.strip()
        self.receive_id = receive_id.strip()
        self.receive_id_type = receive_id_type.strip() or DEFAULT_RECEIVE_ID_TYPE
        self.domain = domain.rstrip("/") or DEFAULT_DOMAIN
        self._token: str | None = None
        self._lock = Lock()
        self._image_cache = self._load_cache()

    def send_card(self, card: dict[str, Any]) -> str:
        payload = {
            "msg_type": "interactive",
            "content": json.dumps(card, ensure_ascii=False),
        }
        data = self._send_message(payload)
        return ((data.get("data") or {}).get("message_id") or "").strip()

    def build_card(self, markdown_text: str, image_ref: str | None = None, alt_text: str = "Preview") -> tuple[dict[str, Any], bool]:
        image_key = self.upload_image(image_ref) if image_ref else None
        body_elements: list[dict[str, Any]] = [
            {
                "tag": "markdown",
                "content": markdown_text,
            }
        ]
        if image_key:
            body_elements.append(
                {
                    "tag": "img",
                    "img_key": image_key,
                    "alt": {
                        "tag": "plain_text",
                        "content": alt_text,
                    },
                }
            )
        return (
            {
                "schema": "2.0",
                "config": {"wide_screen_mode": True},
                "body": {"elements": body_elements},
            },
            bool(image_key),
        )

    def send_markdown_card(self, markdown_text: str, image_ref: str | None = None, alt_text: str = "Preview") -> tuple[str, bool]:
        card, image_resolved = self.build_card(markdown_text, image_ref=image_ref, alt_text=alt_text)
        return self.send_card(card), image_resolved

    def send_text(self, markdown_text: str) -> str:
        payload = {
            "msg_type": "interactive",
            "content": json.dumps(
                {
                    "schema": "2.0",
                    "config": {"wide_screen_mode": True},
                    "body": {"elements": [{"tag": "markdown", "content": markdown_text}]},
                },
                ensure_ascii=False,
            ),
        }
        data = self._send_message(payload)
        return ((data.get("data") or {}).get("message_id") or "").strip()

    def send_image(self, image_ref: str) -> str:
        image_key = self.upload_image(image_ref)
        payload = {
            "msg_type": "image",
            "content": json.dumps({"image_key": image_key}, ensure_ascii=False),
        }
        data = self._send_message(payload)
        return ((data.get("data") or {}).get("message_id") or "").strip()

    def upload_image(self, image_ref: str) -> str:
        image_bytes, filename = self._load_image_bytes(image_ref)
        cache_key = hashlib.sha256(image_bytes).hexdigest()
        with self._lock:
            cached = self._image_cache.get(cache_key)
            if cached:
                return cached

        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        response = requests.post(
            f"{self.domain}/open-apis/im/v1/images",
            headers={"Authorization": f"Bearer {self._get_token()}"},
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
            self._image_cache[cache_key] = image_key
            self._save_cache(self._image_cache)
        return image_key

    def _get_token(self) -> str:
        if self._token:
            return self._token
        with self._lock:
            if self._token:
                return self._token
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
            self._token = str(token)
            return self._token

    def _send_message(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            f"{self.domain}/open-apis/im/v1/messages",
            params={"receive_id_type": self.receive_id_type},
            headers={
                "Authorization": f"Bearer {self._get_token()}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={"receive_id": self.receive_id, **payload},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("code") != 0:
            raise RuntimeError(f"Send API failed: {json.dumps(data, ensure_ascii=False)}")
        return data

    @staticmethod
    def _load_image_bytes(image_ref: str) -> tuple[bytes, str]:
        image_path = Path(image_ref).expanduser()
        if image_path.is_file():
            return image_path.read_bytes(), image_path.name

        response = requests.get(image_ref, timeout=30)
        response.raise_for_status()
        filename = Path(image_ref.split("?", 1)[0]).name or "image.png"
        return response.content, filename

    @staticmethod
    def _load_cache() -> dict[str, str]:
        if not CACHE_PATH.exists():
            return {}
        try:
            data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return {str(key): str(value) for key, value in data.items()}
        except (json.JSONDecodeError, OSError):
            pass
        return {}

    @staticmethod
    def _save_cache(data: dict[str, str]) -> None:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def resolve_feishu_delivery_config(params: dict[str, Any] | None = None) -> tuple[str, str, str, str, str]:
    args = params or {}
    app_id = str(args.get("feishu_app_id") or os.getenv("FEISHU_APP_ID") or "").strip()
    app_secret = str(args.get("feishu_app_secret") or os.getenv("FEISHU_APP_SECRET") or "").strip()
    receive_id = str(args.get("feishu_target") or os.getenv("FEISHU_RECEIVE_ID") or "").strip()
    receive_id_type = str(
        args.get("feishu_receive_id_type") or os.getenv("FEISHU_RECEIVE_ID_TYPE") or DEFAULT_RECEIVE_ID_TYPE
    ).strip()
    domain = str(args.get("feishu_open_base") or os.getenv("FEISHU_OPEN_BASE") or DEFAULT_DOMAIN).strip()

    if not app_id or not app_secret:
        raise RuntimeError(
            "operator_action_required: missing FEISHU_APP_ID / FEISHU_APP_SECRET for direct Feishu delivery"
        )
    if not receive_id:
        raise RuntimeError(
            "operator_action_required: missing feishu_target/current conversation target for direct Feishu delivery"
        )
    return app_id, app_secret, receive_id, receive_id_type, domain
