"""Continuous Telegram typing indicator.

Telegram's `sendChatAction(typing)` sets the status for up to 5 seconds (or
until the bot sends a message, whichever comes first). For operations that
take longer, the indicator must be re-posted every ~4 seconds or the user
sees silence — which research shows breaks the "bot is working" illusion
within ~3 seconds of lag.

This module wraps a small background thread around the bot-API call. Start
the loop at the top of any long-running operation and stop it before
returning. Failures are swallowed: a dropped Telegram request should never
take down the negotiation.

Direct Bot API calls here (not `openclaw message send`) because:
  * sendChatAction isn't exposed by the CLI at v2026.4.12
  * Skipping the Node subprocess saves ~800ms per renewal, which matters
    at a 4s interval
"""
from __future__ import annotations

import json
import os
import threading
import urllib.request
from pathlib import Path
from typing import Callable


_DEFAULT_OPENCLAW_CONFIG = Path("/root/.openclaw/openclaw.json")
_DEFAULT_INTERVAL_SECONDS = 4.0
_TOKEN_CACHE: dict[str, str | None] = {}


def get_bot_token(
    config_path: Path = _DEFAULT_OPENCLAW_CONFIG,
    force_reload: bool = False,
) -> str | None:
    """Read the Telegram bot token from openclaw.json, cached per-process."""
    cache_key = str(config_path)
    if not force_reload and cache_key in _TOKEN_CACHE:
        return _TOKEN_CACHE[cache_key]
    try:
        body = config_path.read_text()
        cfg = json.loads(body)
        token = cfg.get("channels", {}).get("telegram", {}).get("botToken") or None
    except (OSError, json.JSONDecodeError, AttributeError):
        token = None
    _TOKEN_CACHE[cache_key] = token
    return token


def send_typing_once(
    chat_id: str,
    bot_token: str,
    opener: Callable = urllib.request.urlopen,
    timeout: float = 2.0,
) -> bool:
    """POST sendChatAction(typing) once. Return True on success, False on any failure."""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendChatAction"
        target = str(chat_id).strip()
        if ":" in target:
            target = target.rsplit(":", 1)[-1].strip()
        payload = json.dumps({"chat_id": target, "action": "typing"}).encode()
        req = urllib.request.Request(
            url, data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with opener(req, timeout=timeout) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False


class TypingLoop:
    """Background thread that re-posts `typing` every `interval` seconds.

    Usage:
        loop = TypingLoop(chat_id="12345", bot_token="...")
        loop.start()
        try:
            do_slow_thing()
        finally:
            loop.stop()

    Or as a context manager:
        with TypingLoop(chat_id="12345", bot_token="...") as loop:
            do_slow_thing()
    """

    def __init__(
        self,
        chat_id: str,
        bot_token: str | None,
        interval: float = _DEFAULT_INTERVAL_SECONDS,
        send_fn: Callable[[str, str], bool] = send_typing_once,
    ):
        self.chat_id = str(chat_id).strip() if chat_id is not None else ""
        if ":" in self.chat_id:
            self.chat_id = self.chat_id.rsplit(":", 1)[-1].strip()
        self.bot_token = bot_token
        self.interval = interval
        self._send = send_fn
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    @property
    def is_active(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        if not self.chat_id or not self.bot_token:
            return  # disabled if we can't send
        if self.is_active:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, name="typing-loop", daemon=True)
        self._thread.start()

    def stop(self, join_timeout: float = 1.0) -> None:
        self._stop_event.set()
        thread = self._thread
        if thread is not None:
            thread.join(timeout=join_timeout)
        self._thread = None

    def _run(self) -> None:
        # Fire immediately; don't wait for the first interval tick.
        while not self._stop_event.is_set():
            self._send(self.chat_id, self.bot_token)
            # `wait` returns early when stop() is called — no dangling sleep.
            self._stop_event.wait(self.interval)

    def __enter__(self) -> "TypingLoop":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()


def _reset_token_cache_for_tests() -> None:
    """Test-only helper: force the next get_bot_token() call to re-read disk."""
    _TOKEN_CACHE.clear()
