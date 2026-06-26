"""长期记忆模块 — 记录已处理视频，避免重复"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .summarizer import VideoSummary


@dataclass
class ProcessedVideo:
    bvid: str
    title: str
    processed_at: str
    genre: str = ""
    tldr_cn: str = ""
    tldr_en: str = ""
    key_points_cn: list[str] = field(default_factory=list)
    key_points_en: list[str] = field(default_factory=list)
    summary_cn: str = ""
    summary_en: str = ""
    owner: str = ""
    duration_str: str = ""


class Memory:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self._data = self._load()

    def _load(self) -> dict:
        if self.data_path.exists():
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"processed": [], "stats": {"total_processed": 0, "last_processed_at": None}}

    def _save(self):
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def is_processed(self, bvid: str) -> bool:
        return any(v["bvid"] == bvid for v in self._data["processed"])

    def mark_processed(self, bvid: str, title: str, summary: VideoSummary | None = None):
        now = datetime.now().isoformat()
        entry = {
            "bvid": bvid,
            "title": title,
            "processed_at": now,
        }
        if summary is not None:
            entry.update({
                "genre": summary.genre or "",
                "tldr_cn": summary.tldr_cn or "",
                "tldr_en": summary.tldr_en or "",
                "key_points_cn": summary.key_points_cn or [],
                "key_points_en": summary.key_points_en or [],
                "summary_cn": summary.summary_cn or "",
                "summary_en": summary.summary_en or "",
                "owner": summary.owner or "",
                "duration_str": summary.duration_str or "",
            })
        self._data["processed"].append(entry)
        self._data["stats"]["total_processed"] = len(self._data["processed"])
        self._data["stats"]["last_processed_at"] = now
        self._save()

    def get_stats(self) -> dict:
        return self._data["stats"]

    def get_all_processed(self) -> list[ProcessedVideo]:
        return [
            ProcessedVideo(**v) for v in self._data["processed"]
        ]

    def get_processed_count(self) -> int:
        return len(self._data["processed"])

    def search_by_keyword(self, keyword: str) -> list[ProcessedVideo]:
        """在 title/tldr/key_points 中搜索关键词（大小写不敏感）"""
        kw = keyword.lower()
        results = []
        for v in self._data["processed"]:
            searchable = " ".join([
                v.get("title", ""),
                v.get("tldr_cn", ""),
                v.get("tldr_en", ""),
                " ".join(v.get("key_points_cn", [])),
                " ".join(v.get("key_points_en", [])),
            ]).lower()
            if kw in searchable:
                results.append(ProcessedVideo(**v))
        return results

    def filter_by_genre(self, genre: str) -> list[ProcessedVideo]:
        """按体裁过滤已处理视频"""
        genre_lower = genre.lower()
        return [
            ProcessedVideo(**v)
            for v in self._data["processed"]
            if genre_lower in v.get("genre", "").lower()
        ]

    def get_recent(self, n: int = 10) -> list[ProcessedVideo]:
        """返回最近 n 条已处理记录"""
        return [ProcessedVideo(**v) for v in self._data["processed"][-n:]]
