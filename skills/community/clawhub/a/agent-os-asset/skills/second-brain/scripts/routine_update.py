#!/usr/bin/env python3
"""Run a safe incremental update. English is normative; ZH-CN is paired. / 安全运行增量更新；英文为规范文本，简体中文为配对译文。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))

import build_index  # noqa: E402
import asset_index_registry  # noqa: E402
import runtime_paths  # noqa: E402
import validate_privacy  # noqa: E402


DEFAULT_PATHS = runtime_paths.DEFAULT_PATHS
DEFAULT_VAULT = DEFAULT_PATHS.vault
DEFAULT_OUT = DEFAULT_PATHS.index_dir
DEFAULT_LOG = DEFAULT_PATHS.log_path
DEFAULT_LOCK = DEFAULT_PATHS.lock_path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def append_log(log_path: Path, fields: dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    parts = [f"{key}={value}" for key, value in fields.items()]
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(" ".join(parts) + "\n")


def acquire_lock(lock_path: Path) -> None:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise RuntimeError(f"Routine update already running / 常规更新已在运行: {lock_path}") from exc
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(f"pid={os.getpid()} started_at={utc_now()}\n")


def release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


def run_update(
    *,
    vault: Path = DEFAULT_VAULT,
    out_dir: Path = DEFAULT_OUT,
    log_path: Path = DEFAULT_LOG,
    lock_path: Path = DEFAULT_LOCK,
    force: bool = False,
    use_lock: bool = True,
    llm_workers: int = build_index.DEFAULT_LLM_WORKERS,
    source_mode: str = build_index.DEFAULT_SOURCE_MODE,
    registry_path: Path | None = None,
) -> dict[str, Any]:
    started_at = utc_now()
    if use_lock:
        acquire_lock(lock_path)
    try:
        summary = build_index.build_index(
            vault,
            out_dir,
            force=force,
            llm_workers=llm_workers,
            source_mode=source_mode,
        )
        privacy_errors = validate_privacy.validate_generated(out_dir)
        if privacy_errors:
            raise RuntimeError("; ".join(privacy_errors))
        asset_registry: dict[str, Any] | None = None
        if source_mode == build_index.SOURCE_MODE_ASSET_MANIFEST:
            asset_registry = asset_index_registry.upsert_asset_index(
                vault,
                out_dir,
                registry_path or asset_index_registry.DEFAULT_REGISTRY_PATH,
            )
        result = {
            "status": "ok",
            "started_at": started_at,
            "finished_at": utc_now(),
            "vault": vault.as_posix(),
            "out_dir": out_dir.as_posix(),
            "source_mode": source_mode,
            "summary": summary.as_dict(),
            "asset_index_registry": asset_registry,
        }
        append_log(
            log_path,
            {
                "ts": result["finished_at"],
                "status": "ok",
                "source_mode": source_mode,
                "asset_index_registry": asset_registry.get("workspace_id", "") if asset_registry else "",
                **summary.as_dict(),
            },
        )
        return result
    except Exception as exc:
        append_log(
            log_path,
            {
                "ts": utc_now(),
                "status": "error",
                "error": json.dumps(str(exc), ensure_ascii=False),
            },
        )
        raise
    finally:
        if use_lock:
            release_lock(lock_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=DEFAULT_VAULT, help="Vault root path. / 知识库根路径。")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Index output directory. / 索引输出目录。")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG, help="Routine log path. / 常规更新日志路径。")
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK, help="Routine lock path. / 常规更新锁路径。")
    parser.add_argument("--force", action="store_true", help="Rebuild all records. / 重建全部记录。")
    parser.add_argument("--llm-workers", type=int, default=build_index.DEFAULT_LLM_WORKERS, help="Concurrent summary workers. / 并发摘要 worker 数。")
    parser.add_argument(
        "--source-mode",
        choices=sorted(build_index.SOURCE_MODES),
        default=build_index.DEFAULT_SOURCE_MODE,
        help="Source scan policy. / 来源扫描策略。",
    )
    parser.add_argument(
        "--asset-index-registry",
        type=Path,
        default=asset_index_registry.DEFAULT_REGISTRY_PATH,
        help="Registry updated after a ready asset-manifest index build. / asset-manifest 索引就绪后更新的注册表。",
    )
    parser.add_argument("--no-lock", action="store_true", help="Disable the routine lock. / 禁用常规更新锁。")
    parser.add_argument("--json", action="store_true", help="Print JSON output. / 打印 JSON 输出。")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_update(
        vault=args.vault,
        out_dir=args.out,
        log_path=args.log,
        lock_path=args.lock,
        force=args.force,
        use_lock=not args.no_lock,
        llm_workers=args.llm_workers,
        source_mode=args.source_mode,
        registry_path=args.asset_index_registry,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        summary = result["summary"]
        print(
            "Update completed / 更新完成: status=ok "
            f"source_mode={result['source_mode']} "
            f"total_documents={summary['total_documents']} "
            f"indexed_documents={summary['indexed_documents']} "
            f"reused_documents={summary['reused_documents']} "
            f"removed_documents={summary['removed_documents']} "
            f"excluded_pii_documents={summary['excluded_pii_documents']}"
        )


if __name__ == "__main__":
    main()
