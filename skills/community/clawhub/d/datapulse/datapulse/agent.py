"""Agent wrapper for DataPulse: text -> URLs -> routed ingestion -> ranked results."""

from __future__ import annotations

import logging

from datapulse.core.utils import extract_urls

from .reader import DataPulseReader

logger = logging.getLogger("datapulse.agent")


class DataPulseAgent:
    def __init__(self, min_confidence: float = 0.25):
        self.reader = DataPulseReader()
        self.min_confidence = min_confidence

    async def handle(self, message: str) -> dict:
        urls = extract_urls(message)
        if not urls:
            return {
                "status": "empty",
                "message": "No URL detected.",
                "items": [],
            }

        items = await self.reader.read_batch(urls, min_confidence=self.min_confidence)
        return {
            "status": "ok",
            "count": len(items),
            "items": [i.to_dict() for i in items],
            "message": f"processed {len(items)} URLs",
        }

    async def health(self) -> dict:
        return {
            "status": "ready",
            "parsers": self.reader.router.available_parsers,
            "stored": len(self.reader.inbox.items),
        }
