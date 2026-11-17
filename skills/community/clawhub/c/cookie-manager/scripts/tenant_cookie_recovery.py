#!/usr/bin/env python3
"""Cookie多租户恢复SOP (DEF-66)

修复(DEF-66): 多租户Cookie失效后的标准化恢复流程

功能:
  1. 检测所有租户的Cookie状态(从tenant_cookie_map.json)
  2. 识别失效/即将过期的租户Cookie
  3. 自动恢复路径:
     a. 优先: 从备份恢复(每个租户保留2份历史Cookie)
     b. 次选: 切换备用账号Cookie(每租户预留1-2个备用)
     c. 最后: 触发cookie-manager紧急修复 + QQBot告警+人工介入
  4. 恢复结果记录到recovery_log.jsonl

用法:
  python tenant_cookie_recovery.py --check-all      # 检查所有租户
  python tenant_cookie_recovery.py --recover T01    # 恢复指定租户
  python tenant_cookie_recovery.py --auto           # 自动恢复(无人值守)
  python tenant_cookie_recovery.py --status         # 查看状态

输出: JSON格式, 符合fix-tips 9.json规范
  {success: bool, data: dict, error: str|null, code: str|null}
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# P1-1迁移: logging.basicConfig → db_logger统一日志(loguru+PostgreSQL)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("cookie-manager", source="skills/cookie-manager/scripts/tenant_cookie_recovery.py")

# 路径解析
_JUEJIN_HOME = Path(os.environ.get("JUEJIN_HOME", str(Path(__file__).resolve().parent.parent.parent.parent)))
_DATA_DIR = _JUEJIN_HOME / "data" / "openclaw"
_TENANT_MAP = _DATA_DIR / "tenant_cookie_map.json"
_BACKUP_DIR = _JUEJIN_HOME / "data" / "tenant_cookies" / "backup"
_RECOVERY_LOG = _DATA_DIR / "recovery_log.jsonl"

# 阈值常量(可被env覆盖)
_WARNING_DAYS = int(os.environ.get("COOKIE_WARN_DAYS", "7"))
_CRITICAL_DAYS = int(os.environ.get("COOKIE_CRITICAL_DAYS", "1"))


def _load_tenant_map() -> dict:
    """加载tenant_id -> cookie_paths映射"""
    if not _TENANT_MAP.exists():
        logger.warning("tenant_cookie_map.json 不存在, 返回空映射")
        return {"tenants": {}, "schema_version": "1.0"}
    try:
        return json.loads(_TENANT_MAP.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error("tenant_cookie_map.json 解析失败: %s", e)
        return {"tenants": {}, "error": str(e)}


def _check_single_tenant(tenant_id: str, cookie_paths: list) -> dict:
    """检查单个租户Cookie状态"""
    from datetime import datetime
    result = {
        "tenant_id": tenant_id,
        "cookie_count": len(cookie_paths),
        "valid_count": 0,
        "expired_count": 0,
        "warning_count": 0,
        "missing_count": 0,
        "details": [],
    }
    now = datetime.now(timezone.utc)
    for path in cookie_paths:
        detail = {"path": str(path), "status": "unknown", "days_remaining": None}
        try:
            p = Path(path)
            if not p.exists():
                detail["status"] = "missing"
                result["missing_count"] += 1
            else:
                mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
                age = (now - mtime).days
                detail["days_remaining"] = -age  # 负数表示已过天数
                if age < 0:
                    detail["status"] = "future_dated"
                elif age >= 30:
                    detail["status"] = "expired"
                    result["expired_count"] += 1
                elif age >= 7:
                    detail["status"] = "warning"
                    result["warning_count"] += 1
                else:
                    detail["status"] = "valid"
                    result["valid_count"] += 1
        except Exception as e:
            logger.error(f"tenant cookie recovery异常: {e}", exc_info=True)
            detail["status"] = "error"
            detail["error"] = str(e)
        result["details"].append(detail)
    return result


def _recover_from_backup(tenant_id: str, primary_path: str) -> dict:
    """从备份恢复Cookie(优先策略)"""
    backup_path = _BACKUP_DIR / tenant_id
    if not backup_path.exists():
        return {"success": False, "method": "backup", "error": "no_backup_directory"}

    # 找最新的备份
    backups = sorted(backup_path.glob("*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not backups:
        return {"success": False, "method": "backup", "error": "no_backup_files"}

    latest = backups[0]
    try:
        target = Path(primary_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        # 使用atomic_write防中断
        from mcps.shared.atomic_write import atomic_write_text
        atomic_write_text(target, latest.read_text(encoding="utf-8", errors="ignore"))
        return {
            "success": True,
            "method": "backup",
            "restored_from": str(latest),
            "to": str(target),
            "backup_age_hours": (time.time() - latest.stat().st_mtime) / 3600,
        }
    except Exception as e:
        logger.error(f"tenant cookie recovery异常: {e}", exc_info=True)
        return {"success": False, "method": "backup", "error": str(e)}


def _recover_from_secondary(tenant_id: str, primary_path: str, secondary_paths: list) -> dict:
    """切换备用Cookie(次选策略)"""
    for sec_path in secondary_paths:
        sp = Path(sec_path)
        if sp.exists():
            try:
                target = Path(primary_path)
                target.parent.mkdir(parents=True, exist_ok=True)
                from mcps.shared.atomic_write import atomic_write_text
                atomic_write_text(target, sp.read_text(encoding="utf-8", errors="ignore"))
                return {
                    "success": True,
                    "method": "secondary",
                    "switched_from": str(primary_path),
                    "to": str(sp),
                }
            except Exception as e:
                logger.error(f"tenant cookie recovery异常: {e}", exc_info=True)
                continue
    return {"success": False, "method": "secondary", "error": "no_valid_secondary"}


def _trigger_emergency(tenant_id: str, reason: str) -> dict:
    """触发cookie-manager紧急修复(最后手段)"""
    try:
        from notification import send_alert_async
        msg = f"DEF-66 紧急: 租户 {tenant_id} Cookie恢复失败, 原因={reason}"
        result = send_alert_async(msg, level="CRITICAL")
        return {"success": True, "method": "emergency", "alert": result}
    except Exception as e:
        logger.error(f"tenant cookie recovery异常: {e}", exc_info=True)
        return {"success": False, "method": "emergency", "error": str(e)}


def recover_tenant(tenant_id: str, primary_path: str, secondary_paths: Optional[list] = None) -> dict[str, Any]:
    """恢复单个租户Cookie - 三级降级策略

    Args:
        tenant_id (str): 参数说明
        primary_path (str): 参数说明
        secondary_paths (Optional[list]): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    if secondary_paths is None:
        secondary_paths = []
    recovery_chain = []

    # 1. 先尝试备份恢复
    r1 = _recover_from_backup(tenant_id, primary_path)
    recovery_chain.append(r1)
    if r1["success"]:
        _log_recovery(tenant_id, "backup", True, recovery_chain)
        return {"success": True, "method": "backup", "chain": recovery_chain}

    # 2. 尝试备用Cookie
    r2 = _recover_from_secondary(tenant_id, primary_path, secondary_paths)
    recovery_chain.append(r2)
    if r2["success"]:
        _log_recovery(tenant_id, "secondary", True, recovery_chain)
        return {"success": True, "method": "secondary", "chain": recovery_chain}

    # 3. 触发紧急告警
    r3 = _trigger_emergency(tenant_id, f"backup_fail={r1.get('error')}, secondary_fail={r2.get('error')}")
    recovery_chain.append(r3)
    _log_recovery(tenant_id, "all_failed", False, recovery_chain)
    return {"success": False, "method": "all_failed", "chain": recovery_chain}


def _log_recovery(tenant_id: str, method: str, success: bool, chain: list) -> None:
    """记录恢复操作到日志"""
    try:
        _RECOVERY_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tenant_id": tenant_id,
            "method": method,
            "success": success,
            "chain": chain,
        }
        with _RECOVERY_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error("日志记录失败: %s", e)


def cmd_check_all() -> int:
    """检查所有租户状态

    Returns:
        int: 返回值说明
    """
    tenant_map = _load_tenant_map()
    tenants = tenant_map.get("tenants", {})
    if not tenants:
        return _output({"success": False, "error": "no_tenants_configured", "code": "NO_TENANTS"})

    results = []
    for tid, tdata in tenants.items():
        paths = tdata.get("cookie_paths", [])
        check = _check_single_tenant(tid, paths)
        results.append(check)

    summary = {
        "total_tenants": len(results),
        "healthy_tenants": sum(1 for r in results if r["expired_count"] == 0 and r["missing_count"] == 0),
        "expired_tenants": sum(1 for r in results if r["expired_count"] > 0),
        "warning_tenants": sum(1 for r in results if r["warning_count"] > 0),
    }
    return _output({"success": True, "data": {"summary": summary, "details": results}, "code": "OK"})


def cmd_recover(tenant_id: str) -> int:
    """恢复指定租户

    Args:
        tenant_id (str): 参数说明

    Returns:
        int: 返回值说明
    """
    tenant_map = _load_tenant_map()
    tdata = tenant_map.get("tenants", {}).get(tenant_id)
    if not tdata:
        return _output({"success": False, "error": f"tenant_not_found: {tenant_id}", "code": "TENANT_NOT_FOUND"})

    primary = tdata.get("primary_path")
    secondary = tdata.get("secondary_paths", [])
    if not primary:
        return _output({"success": False, "error": "no_primary_path", "code": "NO_PATH"})

    result = recover_tenant(tenant_id, primary, secondary)
    return _output({"success": result["success"], "data": result, "code": "OK" if result["success"] else "RECOVERY_FAILED"})


def cmd_status() -> int:
    """查看状态概览

    Returns:
        int: 返回值说明
    """
    if not _RECOVERY_LOG.exists():
        return _output({"success": True, "data": {"total_recoveries": 0, "recent": []}})

    lines = _RECOVERY_LOG.read_text(encoding="utf-8").strip().splitlines()[-20:]
    entries = []
    for line in lines:
        try:
            entries.append(json.loads(line))
        except Exception as e:
            logger.error(f"恢复日志行解析失败: {e}")

    return _output({
        "success": True,
        "data": {
            "total_recoveries": len(entries),
            "success_count": sum(1 for e in entries if e.get("success")),
            "recent": entries[-5:],
        }
    })


def _output(payload: dict) -> int:
    """统一JSON输出"""
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("success") else 1


def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="Cookie多租户恢复SOP (DEF-66)")
    parser.add_argument("--check-all", action="store_true", help="检查所有租户")
    parser.add_argument("--recover", metavar="TENANT_ID", help="恢复指定租户")
    parser.add_argument("--auto", action="store_true", help="自动恢复(检查+恢复失败租户)")
    parser.add_argument("--status", action="store_true", help="查看状态")
    args = parser.parse_args()

    # P1-1迁移: logging.basicConfig已移至模块级db_logger,此处无需重复配置

    try:
        if args.check_all:
            return cmd_check_all()
        elif args.recover:
            return cmd_recover(args.recover)
        elif args.status:
            return cmd_status()
        elif args.auto:
            # 检查+自动恢复
            tenant_map = _load_tenant_map()
            tenants = tenant_map.get("tenants", {})
            auto_results = []
            for tid, tdata in tenants.items():
                paths = tdata.get("cookie_paths", [])
                check = _check_single_tenant(tid, paths)
                if check["expired_count"] > 0 or check["missing_count"] > 0:
                    r = recover_tenant(tid, tdata.get("primary_path"), tdata.get("secondary_paths", []))
                    auto_results.append({"tenant_id": tid, "action": "recovered", "result": r})
                else:
                    auto_results.append({"tenant_id": tid, "action": "skipped", "status": "healthy"})
            return _output({"success": True, "data": {"auto_results": auto_results}})
        else:
            parser.print_help()
            return 2
    except Exception as e:
        logger.exception("未捕获异常")
        return _output({"success": False, "error": str(e), "code": "UNCAUGHT"})


if __name__ == "__main__":
    sys.exit(main())
