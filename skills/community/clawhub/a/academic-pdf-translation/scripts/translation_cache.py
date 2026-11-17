"""翻译批次缓存。

小单元继续负责检查，批次负责执行。缓存以批次为单位，键里同时绑定原文内容、
目标语言、术语表、提示版本、模型标识和翻译策略版本；任一项变化都不会命中
旧结果。

缓存只是加速手段，不是验收依据：命中后仍然走同一套写入校验。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import perf_trace
from _common import SkillError, load_json, write_json

CACHE_SCHEMA_VERSION = "1.0"
TRANSLATION_STRATEGY_VERSION = "batched-units-v1"
DEFAULT_PROMPT_VERSION = "batch-prompt-v1"
CACHE_FILE_NAME = "translation-cache.json"


def _digest(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def unit_content_hash(unit: dict[str, Any]) -> str:
    """单个冻结原文单元的内容哈希。"""

    return _digest(
        json.dumps(
            {
                "id": str(unit.get("id") or ""),
                "source": str(unit.get("source") or ""),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def terminology_hash(terminology: Any) -> str:
    return _digest(
        json.dumps(terminology or [], ensure_ascii=False, sort_keys=True)
    )


def batch_cache_key(
    *,
    unit_hashes: list[str],
    target_language: str,
    terminology_sha256: str,
    prompt_version: str = DEFAULT_PROMPT_VERSION,
    model: str | None = None,
    strategy_version: str = TRANSLATION_STRATEGY_VERSION,
) -> str:
    return _digest(
        json.dumps(
            {
                "unit_hashes": list(unit_hashes),
                "target_language": target_language,
                "terminology_sha256": terminology_sha256,
                "prompt_version": prompt_version,
                "model": model or "",
                "strategy_version": strategy_version,
                "cache_schema_version": CACHE_SCHEMA_VERSION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


class TranslationCache:
    """作业内的批次结果缓存。"""

    def __init__(self, job_dir: Path) -> None:
        self.path = Path(job_dir).resolve() / CACHE_FILE_NAME

    def _load(self) -> dict[str, Any]:
        if not self.path.is_file():
            return {
                "schema_version": CACHE_SCHEMA_VERSION,
                "entries": {},
            }
        data = load_json(self.path)
        if not isinstance(data.get("entries"), dict):
            raise SkillError("translation-cache.json 的 entries 必须是对象")
        return data

    def get(self, cache_key: str) -> list[dict[str, Any]] | None:
        entry = self._load()["entries"].get(cache_key)
        if not isinstance(entry, dict):
            return None
        results = entry.get("results")
        if not isinstance(results, list):
            return None
        perf_trace.count("translation_cache_hit")
        return results

    def metadata(self, cache_key: str) -> dict[str, Any]:
        entry = self._load()["entries"].get(cache_key)
        if not isinstance(entry, dict):
            return {}
        value = entry.get("metadata")
        return value if isinstance(value, dict) else {}

    def put(
        self,
        cache_key: str,
        results: list[dict[str, Any]],
        *,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        data = self._load()
        data["entries"][cache_key] = {
            "results": results,
            "metadata": metadata or {},
        }
        write_json(self.path, data)

    def drop(self, cache_key: str) -> None:
        data = self._load()
        if data["entries"].pop(cache_key, None) is not None:
            write_json(self.path, data)
