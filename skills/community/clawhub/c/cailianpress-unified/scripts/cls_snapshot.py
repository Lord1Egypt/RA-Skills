#!/usr/bin/env python3
"""Snapshot current CLS telegraph window into local JSONL storage."""

from __future__ import annotations

import json

from cls_service import ClsService
from storage import append_snapshot


def main():
    service = ClsService()
    result = service.get_telegraph(limit=100)
    count = append_snapshot(result.items)
    print(json.dumps({
        "ok": True,
        "stored": count,
        "source": result.source_used,
        "fallback_used": result.fallback_used,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
