#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本机 cad_scan 证据缓存盘点与安全清理。

默认只读盘点；清理必须显式 --cleanup，实际删除还必须 --apply。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any

from cad_scan_cache import CACHE_VERSION, _safe_db_path

_SQLITE_SUFFIX = ".sqlite"
_TEMP_MARKER = ".tmp"


def _size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def _mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def _profile_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def inspect_cache_file(path: Path) -> dict[str, Any]:
    """只读识别缓存文件类别；不写入、不重建、不删除。"""
    info: dict[str, Any] = {
        "file": str(path),
        "name": path.name,
        "bytes": _size(path),
        "mtime": round(_mtime(path), 6),
    }
    if path.name.endswith(_TEMP_MARKER):
        info["category"] = "temp"
        info["cache_version"] = None
        return info
    if path.suffix != _SQLITE_SUFFIX or not path.name.startswith("cad-scan-v"):
        info["category"] = "unknown"
        info["cache_version"] = None
        return info

    conn = None
    try:
        conn = sqlite3.connect(_safe_db_path(path), uri=True)
        row = conn.execute(
            "SELECT value FROM metadata WHERE key='cache_version'"
        ).fetchone()
        version = int(row[0]) if row else -1
        info["cache_version"] = version
        if version != CACHE_VERSION:
            info["category"] = "legacy"
            return info
        rows = dict(conn.execute(
            "SELECT key, value FROM metadata "
            "WHERE key IN ('source_sha256','source_name','profile',"
            "'record_count','geometry_count')"
        ).fetchall())
        digest = str(rows.get("source_sha256") or "")
        profile_text = str(rows.get("profile") or "")
        counts_ok = True
        counts: dict[str, int] = {}
        for key in ("record_count", "geometry_count"):
            try:
                counts[key] = int(rows.get(key, -1))
            except (TypeError, ValueError):
                counts_ok = False
        if len(digest) != 64 or not counts_ok:
            info["category"] = "corrupt"
            return info
        info["category"] = "current"
        info["source_sha256"] = digest
        info["profile_sha256"] = _profile_digest(profile_text)
        info.update(counts)
        return info
    except (sqlite3.Error, OSError):
        info["category"] = "corrupt"
        info["cache_version"] = info.get("cache_version")
        return info
    finally:
        if conn is not None:
            try:
                conn.close()
            except sqlite3.Error:
                pass


def cache_stats(cache_dir: Path) -> dict[str, Any]:
    """盘点目录中的当前、旧版、临时、损坏和未知文件。"""
    cache_dir = Path(cache_dir)
    result: dict[str, Any] = {
        "dir": str(cache_dir),
        "exists": cache_dir.is_dir(),
        "categories": {},
        "files": [],
    }
    if not cache_dir.is_dir():
        return result

    grouped: dict[str, dict[str, int]] = {}
    for path in sorted(cache_dir.iterdir(), key=lambda p: p.name):
        if not path.is_file():
            continue
        info = inspect_cache_file(path)
        category = str(info["category"])
        bucket = grouped.setdefault(category, {"files": 0, "bytes": 0})
        bucket["files"] += 1
        bucket["bytes"] += int(info["bytes"])
        result["files"].append(info)

    result["categories"] = dict(sorted(grouped.items()))
    result["total"] = {
        "files": sum(x["files"] for x in grouped.values()),
        "bytes": sum(x["bytes"] for x in grouped.values()),
    }
    return result


def _safe_unlink(path: Path) -> bool:
    try:
        path.unlink()
        return True
    except OSError:
        return False


def cache_cleanup(
    cache_dir: Path,
    *,
    max_age_days: float | None = None,
    max_total_bytes: int | None = None,
    include_temp: bool = True,
    include_legacy: bool = True,
    include_current: bool = False,
    dry_run: bool = True,
) -> dict[str, Any]:
    """默认 dry-run；只按显式类别与条件生成删除计划。

    默认只处理临时和旧版缓存；当前缓存必须同时显式 include_current
    且提供年龄/容量条件。损坏和未知文件永远不进入删除计划。
    """
    stats = cache_stats(cache_dir)
    has_limit = max_age_days is not None or max_total_bytes is not None
    eligible: list[dict[str, Any]] = []
    for info in stats["files"]:
        category = info["category"]
        if category == "temp" and include_temp:
            eligible.append(info)
        elif category == "legacy" and include_legacy:
            eligible.append(info)
        elif category == "current" and include_current and has_limit:
            eligible.append(info)

    if max_age_days is not None:
        cutoff = time.time() - max(0.0, float(max_age_days)) * 86400.0
        eligible = [
            x for x in eligible
            if float(x.get("mtime") or 0.0) <= cutoff
        ]

    if max_total_bytes is not None:
        target = max(0, int(max_total_bytes))
        excess = int(stats["total"]["bytes"]) - target
        selected: list[dict[str, Any]] = []
        for info in sorted(
            eligible,
            key=lambda x: (float(x.get("mtime") or 0.0), str(x["file"])),
        ):
            if excess <= 0:
                break
            selected.append(info)
            excess -= int(info["bytes"])
        eligible = selected

    removed: list[str] = []
    failed: list[str] = []
    removed_bytes = 0
    for info in eligible:
        path = Path(info["file"])
        if dry_run:
            removed.append(str(path))
            removed_bytes += int(info["bytes"])
        elif _safe_unlink(path):
            removed.append(str(path))
            removed_bytes += int(info["bytes"])
        else:
            failed.append(str(path))

    return {
        "dir": str(cache_dir),
        "dry_run": dry_run,
        "conditions": {
            "max_age_days": max_age_days,
            "max_total_bytes": max_total_bytes,
            "include_temp": include_temp,
            "include_legacy": include_legacy,
            "include_current": include_current,
        },
        "candidate_files": len(eligible),
        "candidate_bytes": sum(int(x["bytes"]) for x in eligible),
        "removed_files": len(removed),
        "removed_bytes": removed_bytes,
        "removed": removed,
        "failed": failed,
        "stats_after": None if dry_run else cache_stats(cache_dir),
    }


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="盘点/清理 cad_scan 证据缓存")
    ap.add_argument("cache_dir")
    ap.add_argument("--cleanup", action="store_true", help="进入清理模式；默认 dry-run")
    ap.add_argument("--apply", action="store_true", help="实际删除；默认只输出计划")
    ap.add_argument("--max-age-days", type=float, default=None)
    ap.add_argument("--max-total-mb", type=float, default=None)
    ap.add_argument("--no-temp", action="store_true", help="清理模式不处理 .tmp 文件")
    ap.add_argument("--no-legacy", action="store_true", help="清理模式不处理旧版本缓存")
    ap.add_argument(
        "--include-current", action="store_true",
        help="配合年龄/容量条件时允许清理当前缓存；默认保留",
    )
    args = ap.parse_args()
    cache_dir = Path(args.cache_dir)
    if args.cleanup:
        result = cache_cleanup(
            cache_dir,
            max_age_days=args.max_age_days,
            max_total_bytes=int(args.max_total_mb * 1024 * 1024)
            if args.max_total_mb is not None else None,
            include_temp=not args.no_temp,
            include_legacy=not args.no_legacy,
            include_current=args.include_current,
            dry_run=not args.apply,
        )
    else:
        result = cache_stats(cache_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
