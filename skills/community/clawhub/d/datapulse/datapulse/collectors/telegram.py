"""Telegram collector using Telethon API (optional dependency)."""

from __future__ import annotations

import asyncio
import os
from datetime import datetime, timedelta, timezone

from datapulse.core.models import SourceType
from datapulse.core.utils import run_sync

from .base import BaseCollector, ParseResult


class TelegramCollector(BaseCollector):
    name = "telegram"
    source_type = SourceType.TELEGRAM
    reliability = 0.78
    tier = 2
    setup_hint = "Set TG_API_ID and TG_API_HASH env vars; pip install telethon"

    def check(self) -> dict[str, str | bool]:
        try:
            import telethon  # noqa: F401
            has_telethon = True
        except ImportError:
            has_telethon = False
        has_creds = bool(os.getenv("TG_API_ID", "").strip() and os.getenv("TG_API_HASH", "").strip())
        if not has_telethon:
            return {"status": "warn", "message": "telethon not installed", "available": False}
        if not has_creds:
            return {"status": "warn", "message": "TG_API_ID/TG_API_HASH not set", "available": False}
        return {"status": "ok", "message": "telethon + credentials ready", "available": True}

    def can_handle(self, url: str) -> bool:
        return "t.me" in url.lower()

    def parse(self, url: str) -> ParseResult:
        channel = self._extract_channel(url)
        if not channel:
            return ParseResult.failure(url, "Cannot parse Telegram channel")

        try:
            from telethon import TelegramClient
        except ImportError:
            return ParseResult.failure(url, "Telethon not installed. pip install -e '.[telegram]'")

        api_id = os.getenv("TG_API_ID", "").strip()
        api_hash = os.getenv("TG_API_HASH", "").strip()
        if not api_id or not api_hash:
            return ParseResult.failure(url, "Missing TG_API_ID / TG_API_HASH")

        max_messages = int(os.getenv("DATAPULSE_TG_MAX_MESSAGES", "20"))
        max_chars = int(os.getenv("DATAPULSE_TG_MAX_CHARS", "800"))
        cutoff_hours = int(os.getenv("DATAPULSE_TG_CUTOFF_HOURS", "24"))
        cutoff = datetime.now(timezone.utc) - timedelta(hours=cutoff_hours)
        messages: list[str] = []
        try:
            async def fetch() -> list[str]:
                from telethon.tl.types import Message

                async with TelegramClient(os.getenv("TG_SESSION_PATH", "./tg_session"), int(api_id), api_hash) as client:
                    entity = await client.get_entity(channel)
                    async for msg in client.iter_messages(entity, limit=max_messages):
                        if not isinstance(msg, Message) or not msg.text:
                            continue
                        if msg.date < cutoff:
                            break
                        messages.append(f"[{msg.date.isoformat()}] {msg.text[:max_chars]}")
                return messages

            content_rows = run_sync(asyncio.wait_for(fetch(), timeout=30))
            if not content_rows:
                return ParseResult.failure(url, "No recent Telegram messages found")

            content = "\n\n".join(content_rows)
            return ParseResult(
                url=url,
                title=f"Telegram: {channel}",
                content=content,
                author=channel,
                excerpt=content[:260],
                source_type=self.source_type,
                tags=["telegram", "latest-messages"],
                confidence_flags=["telethon"],
                extra={"channel": channel, "count": len(content_rows)},
            )
        except asyncio.TimeoutError:
            return ParseResult.failure(url, "Telegram fetch timed out (30s)")
        except (ConnectionError, OSError) as exc:
            return ParseResult.failure(url, f"Telegram connection failed: {exc}")
        except Exception as exc:
            return ParseResult.failure(url, f"Telegram fetch failed: {exc}")

    @staticmethod
    def _extract_channel(url: str) -> str:
        parts = [p for p in url.split("/") if p and not p.startswith("http")]
        if not parts:
            return ""
        return parts[0]
