"""Assistant skill entry for DataPulse."""

from __future__ import annotations

import os

from datapulse.core.utils import extract_urls, run_sync
from datapulse.reader import DataPulseReader


def run(text: str, **_kwargs) -> str:
    urls = extract_urls(text)
    if not urls:
        return "🔍 No URL detected in your message."

    reader = DataPulseReader()
    min_conf = float(os.getenv("DATAPULSE_MIN_CONFIDENCE", "0.35"))
    result_items = run_sync(reader.read_batch(urls, min_confidence=min_conf))

    if not result_items:
        return "⚠️ No URLs could be confidently processed."

    parts = [f"📚 DataPulse processed {len(result_items)} URL(s):\n"]
    for item in result_items:
        parts.append(f"- [{item.source_type.value}] {item.title}\n  {item.url}\n  confidence={item.confidence:.3f}")
    return "\n".join(parts)


__all__ = ["run"]
