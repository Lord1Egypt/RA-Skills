#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日资产清理器 - T2-6素材清理(BUG-ASSET-CLEANUP-SKILL-MISSING修复)
清理过期临时文件/旧日志/无效缓存/过期素材。来源:05文档§五L1096|04部署文档§2|09设计文档U2
用法: python skills/asset-cleanup-daily/scripts/asset_cleanup.py [--dry-run]
"""
import argparse, fnmatch, json, os, subprocess, sys, time

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

_JUEJIN_HOME = Path(os.environ.get("JUEJIN_HOME", r"d:\JueJin"))
sys.path.insert(0, str(_JUEJIN_HOME / "scripts"))
sys.path.insert(0, str(_JUEJIN_HOME))
from mcps.shared.db_logger import get_logger  # noqa: E402
from mcps.shared.atomic_write import atomic_write_json  # noqa: E402

import logging
logger = get_logger("system", source="skills/asset-cleanup-daily/scripts/asset_cleanup.py")

logger = get_logger("asset-cleanup-daily", source="skills/asset-cleanup-daily/scripts/asset_cleanup.py")

# 清理规则(来源:04部署文档§2环境+SKILL.md设计文档)
TEMP_PATTERNS: List[str] = ["temp_*.txt", "test_*.txt", "test_*.json", "test_*.out", "test_*.log"]
LOG_PATTERNS: List[str] = ["*.jsonl"]
LOG_SKIP: List[str] = ["alert_queue.jsonl", "budget_alerts.jsonl", "tenant_notifications.jsonl", "mcp_pending_tasks.jsonl"]
LOCK_PATTERNS: List[str] = ["*.lock"]
BAK_PATTERNS: List[str] = ["*.bak", "*.backup"]
DAY1 = 86400
DAY30 = 2592000
DAY7 = 604800

def _clean_dir(dir_path: Path, patterns: List[str], age_sec: int, skip: List[str], dry_run: bool) -> Dict[str, Any]:
    """扫描并清理目录中匹配pattern且超龄的文件"""
    scanned = deleted = freed = 0
    errors: List[str] = []
    if not dir_path.is_dir():
        return {"scanned": 0, "deleted": 0, "freed_bytes": 0, "errors": []}
    now = time.time()
    for f in dir_path.iterdir():
        if not f.is_file() or f.name in skip:
            continue
        if not any(fnmatch.fnmatch(f.name, p) for p in patterns):
            continue
        scanned += 1
        try:
            mtime = f.stat().st_mtime
            if (now - mtime) < age_sec:
                continue
            fsize = f.stat().st_size
            if not dry_run:
                f.unlink()
            deleted += 1
            freed += fsize
        except OSError as e:
            logger.error(f"删除文件失败: {f.name}: {e}")
            errors.append(f"{f.name}: {e}")
    return {"scanned": scanned, "deleted": deleted, "freed_bytes": freed, "errors": errors}

def _clean_assets(dry_run: bool) -> Dict[str, Any]:
    """调用scripts/asset_cleanup.py清理过期素材(PG不可用时降级)"""
    script = _JUEJIN_HOME / "scripts" / "asset_cleanup.py"
    if not script.is_file():
        return {"cleaned": False, "skipped": "scripts/asset_cleanup.py不存在"}
    try:
        cmd = [sys.executable, str(script)] + (["--dry-run"] if dry_run else [])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            d = json.loads(result.stdout.strip()).get("data", {})
            return {"cleaned": True, "expired_count": d.get("expired_count", 0),
                    "deleted_records": d.get("deleted_records", 0), "deleted_files": d.get("deleted_files", 0),
                    "freed_bytes": d.get("deleted_size_bytes", 0)}
        return {"cleaned": False, "skipped": f"asset_cleanup.py退出码={result.returncode}"}
    except Exception as e:
        logger.error(f"素材清理降级: {e}")
        return {"cleaned": False, "skipped": f"PG不可用或执行异常: {e}"}

def _human_size(n: int) -> str:
    for u in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}TB"

def run_cleanup(dry_run: bool = False) -> Dict[str, Any]:
    """执行每日资产清理

    Args:
        dry_run (bool): 参数说明

    Returns:
        Dict[str, Any]: 返回值说明
    """
    data_dir = _JUEJIN_HOME / "data"
    if not data_dir.is_dir():
        return {"success": False, "data": {}, "error": f"data目录不存在: {data_dir}", "code": "DATA_DIR_NOT_FOUND"}

    temp_r = _clean_dir(data_dir, TEMP_PATTERNS, DAY1, [], dry_run)
    log_r = _clean_dir(data_dir, LOG_PATTERNS, DAY30, LOG_SKIP, dry_run)
    lock_r = _clean_dir(data_dir, LOCK_PATTERNS, DAY1, [], dry_run)
    bak_r = _clean_dir(_JUEJIN_HOME, BAK_PATTERNS, DAY7, [], dry_run)
    cache_r = {"scanned": lock_r["scanned"] + bak_r["scanned"], "deleted": lock_r["deleted"] + bak_r["deleted"],
               "freed_bytes": lock_r["freed_bytes"] + bak_r["freed_bytes"], "errors": lock_r["errors"] + bak_r["errors"]}
    asset_r = _clean_assets(dry_run)
    total = temp_r["freed_bytes"] + log_r["freed_bytes"] + cache_r["freed_bytes"] + asset_r.get("freed_bytes", 0)
    report = {"temp_files": temp_r, "log_files": log_r, "cache_files": cache_r, "assets": asset_r,
              "total_freed_bytes": total, "total_freed_human": _human_size(total)}

    # 写入审计报告(来源:18_统一入口规则 atomic_write)
    try:
        audit_dir = data_dir / "audit"
        audit_dir.mkdir(exist_ok=True)
        ts = time.strftime('%Y-%m-%d')
        atomic_write_json(str(audit_dir / f"asset_cleanup_{ts}.json"), report, indent=2, ensure_ascii=False)
        report["report_path"] = f"data/audit/asset_cleanup_{ts}.json"
    except OSError as e:
        logger.warning(f"写入清理报告失败(降级): {e}")

    logger.error(f"资产清理完成: 释放{_human_size(total)}, temp={temp_r['deleted']}, log={log_r['deleted']}, cache={cache_r['deleted']}")
    return {"success": True, "data": report, "error": None, "code": None}

def main() -> None:
    """main"""
    parser = argparse.ArgumentParser(description="每日资产清理器(T2-6)")
    parser.add_argument("--dry-run", action="store_true", help="仅扫描不删除")
    args = parser.parse_args()
    # Phase 12.7: IdempotencyChecker集成 - 防止Cron重复执行
    from idempotency_checker import check_idempotent, record_idempotent
    idem_key = f"cron-asset-cleanup-{datetime.now().strftime('%Y-%m-%d')}"
    if check_idempotent(idem_key, task_id="asset-cleanup-daily", tenant_id="system"):
        logger.info(f"任务已执行，跳过(idempotency_check): {idem_key}")
        print(json.dumps({"success": True, "data": {"skipped": True, "reason": "idempotency_check", "key": idem_key}, "error": None, "code": "IDEMPOTENT_SKIP"}))
        return
    try:
        result = run_cleanup(dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, default=str, indent=2))
        # Phase 12.7: 记录幂等键(任务成功完成后)
        record_idempotent(idem_key, task_id="asset-cleanup-daily", tenant_id="system")
        sys.exit(0 if result.get("success") else 1)
    except ValueError as e:
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": f"参数错误: {e}", "code": "INVALID_PARAMS"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        logger.error(f"asset_cleanup异常: {e}", exc_info=True)
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "INTERNAL_ERROR"}, ensure_ascii=False))
        sys.exit(2)

if __name__ == "__main__":
    main()
