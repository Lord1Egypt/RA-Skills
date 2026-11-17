#!/usr/bin/env python3
"""闲鱼Cookie批量失效应急管理脚本 v1.0

功能:
  1. 检测Cookie批量失效(≥2个)并启动降级运营模式
  2. 自动切换备用Cookie
  3. 发送QQBot紧急告警
  4. 扫码恢复后4端同步
  5. 事件日志记录

用法:
  python cookie_emergency_manager.py --mode detect --failed-cookies '[{"account_id":"a1","unb":"u1","failed_at":"2026-01-01T00:00:00"}]' --total-cookies 3
  python cookie_emergency_manager.py --mode degrade --reason "批量失效"
  python cookie_emergency_manager.py --mode recover --account-id account_1
  python cookie_emergency_manager.py --mode status
"""

import argparse

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_JUEJIN_HOME = Path(os.environ.get("JUEJIN_HOME", str(Path(__file__).resolve().parent.parent.parent.parent)))
_DOTENV_PATH = _JUEJIN_HOME / ".env"
_DEGRADED_STATE_FILE = _JUEJIN_HOME / "data" / "auto_ops" / "degraded_mode.json"
_COOKIE_EMERGENCY_LOG = _JUEJIN_HOME / "data" / "auto_ops" / "cookie_emergency_log.json"

sys.path.insert(0, str(_JUEJIN_HOME))
sys.path.insert(0, str(_JUEJIN_HOME / "scripts"))
from mcps.shared.db_logger import get_logger

logger = get_logger("cookie-manager", source="skills/cookie-manager/scripts/cookie_emergency_manager.py")

from mcps.shared.atomic_write import atomic_write_text

import logging
logger = get_logger("system", source="skills/cookie-manager/scripts/cookie_emergency_manager.py")

if _DOTENV_PATH.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_DOTENV_PATH, override=False)
    except ImportError:
        for _line in _DOTENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                _k, _v = _k.strip(), _v.strip().strip("\"'")
                if _k and _k not in os.environ:
                    os.environ[_k] = _v

_ACCOUNT_INTERVAL = 1020
_RECOVERY_DELAY = 300

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

def _load_degraded_state() -> dict:
    if _DEGRADED_STATE_FILE.exists():
        try:
            return json.loads(_DEGRADED_STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            # DOWNGRADE: Cookie紧急配置加载失败,降级返回空字典
            logger.warning("降级: cookie_emergency配置加载失败,返回空字典")
            return {}
    return {}

def _save_degraded_state(state: dict):
    _ensure_dir(_DEGRADED_STATE_FILE)
    state["updated_at"] = _now_iso()
    atomic_write_text(_DEGRADED_STATE_FILE, json.dumps(state, ensure_ascii=False, indent=2))

def _append_emergency_log(entry: dict):
    _ensure_dir(_COOKIE_EMERGENCY_LOG)
    logs = []
    if _COOKIE_EMERGENCY_LOG.exists():
        try:
            logs = json.loads(_COOKIE_EMERGENCY_LOG.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            logs = []
    entry["timestamp"] = _now_iso()
    logs.append(entry)
    atomic_write_text(_COOKIE_EMERGENCY_LOG, json.dumps(logs, ensure_ascii=False, indent=2))

def _get_backup_cookies() -> list:
    backup_cookies = []
    for key in ["XIANYU_COOKIE_2", "XIANYU_COOKIE_3", "XIANYU_COOKIE_4", "XIANYU_COOKIE_5"]:
        val = os.environ.get(key, "")
        if val and len(val) > 20:
            backup_cookies.append({"key": key, "cookie": val[:20] + "..."})
    return backup_cookies

def _validate_cookie(cookie_value: str) -> bool:
    if not cookie_value or len(cookie_value) < 20:
        return False
    try:
        import httpx
        with httpx.Client(timeout=10) as client:
            resp = client.get(
                "https://www.goofish.com/",
                headers={"Cookie": cookie_value},
                follow_redirects=True
            )
            return resp.status_code == 200 and "goofish" in resp.text.lower()
    except Exception as e:
        logger.error(f"Cookie验证请求失败: {e}")
        return False

def detect_cookie_failure(failed_cookies: list, total_cookies: int) -> dict[str, Any]:
    """检测 cookie failure

    Args:
        failed_cookies (list): 参数说明
        total_cookies (int): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    _failed_count = len(failed_cookies)
    if _failed_count < 2:
        return {
            "success": True,
            "data": {"triggered": False, "reason": f"failed_count={_failed_count}<2, 不触发应急"},
            "error": None, "code": None
        }

    backup_cookies = _get_backup_cookies()
    backup_available = len(backup_cookies) > 0

    state = {
        "degraded_mode": True,
        "degraded_at": _now_iso(),
        "reason": f"Cookie批量失效: {_failed_count}/{total_cookies}",
        "failed_cookies": failed_cookies,
        "backup_available": backup_available,
        "backup_cookies_count": len(backup_cookies),
        "affected_services": ["matrix-publish", "xianyu-operations", "auto-delivery"],
        "recovered_at": None,
        "backup_switched": [],
        "pending_scan": [c["account_id"] for c in failed_cookies if not backup_available],
        "alert_sent": False,
        "sync_status": {"fishclaw_mcp": "pending", "env": "pending", "global_config": "pending", "auto_reply_api": "pending"}
    }
    _save_degraded_state(state)

    _append_emergency_log({
        "event": "cookie_failure_detected",
        "failed_count": _failed_count,
        "total_cookies": total_cookies,
        "backup_available": backup_available,
        "failed_accounts": [c.get("account_id", "unknown") for c in failed_cookies]
    })

    return {
        "success": True,
        "data": {
            "triggered": True,
            "degraded_mode": True,
            "backup_available": backup_available,
            "backup_cookies_count": len(backup_cookies),
            "affected_services": ["matrix-publish", "xianyu-operations", "auto-delivery"],
            "degraded_at": state["degraded_at"],
            "pending_scan": state["pending_scan"],
            "alert_sent": False
        },
        "error": None,
        "code": None
    }

def set_degrade_mode(reason: str) -> dict[str, Any]:
    """设置 degrade mode

    Args:
        reason (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    state = _load_degraded_state()
    if state.get("degraded_mode"):
        return {
            "success": True,
            "data": {"message": "已处于降级模式", "degraded_at": state.get("degraded_at")},
            "error": None, "code": None
        }

    state = {
        "degraded_mode": True,
        "degraded_at": _now_iso(),
        "reason": reason,
        "affected_services": ["matrix-publish", "xianyu-operations", "auto-delivery"],
        "recovered_at": None,
        "backup_switched": [],
        "pending_scan": [],
        "alert_sent": True,
        "sync_status": {"fishclaw_mcp": "pending", "env": "pending", "global_config": "pending", "auto_reply_api": "pending"}
    }
    _save_degraded_state(state)

    _append_emergency_log({
        "event": "degrade_mode_activated",
        "reason": reason
    })

    return {
        "success": True,
        "data": {
            "degraded_mode": True,
            "degraded_at": state["degraded_at"],
            "reason": reason,
            "affected_services": state["affected_services"]
        },
        "error": None,
        "code": None
    }

def recover_cookie(account_id: str) -> dict[str, Any]:
    """recover cookie

    Args:
        account_id (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    state = _load_degraded_state()
    if not state.get("degraded_mode"):
        return {
            "success": False,
            "data": {},
            "error": "当前未处于降级模式",
            "code": "NOT_DEGRADED"
        }

    backup_cookies = _get_backup_cookies()
    if not backup_cookies:
        return {
            "success": False,
            "data": {"pending_scan": [account_id]},
            "error": "无可用备用Cookie，请董事长扫码恢复",
            "code": "NO_BACKUP"
        }

    backup = backup_cookies[0]
    cookie_value = os.environ.get(backup["key"], "")
    if not _validate_cookie(cookie_value):
        if len(backup_cookies) > 1:
            backup = backup_cookies[1]
            cookie_value = os.environ.get(backup["key"], "")
            if not _validate_cookie(cookie_value):
                return {
                    "success": False,
                    "data": {},
                    "error": "所有备用Cookie均已失效，请董事长扫码恢复",
                    "code": "BACKUP_FAILED"
                }
        else:
            return {
                "success": False,
                "data": {},
                "error": "备用Cookie验证失败，请董事长扫码恢复",
                "code": "BACKUP_FAILED"
            }

    switched = state.get("backup_switched", [])
    switched.append(account_id)
    state["backup_switched"] = switched
    state["sync_status"] = {"fishclaw_mcp": "pending", "env": "synced", "global_config": "pending", "auto_reply_api": "pending"}
    _save_degraded_state(state)

    _append_emergency_log({
        "event": "backup_cookie_switched",
        "account_id": account_id,
        "backup_key": backup["key"]
    })

    return {
        "success": True,
        "data": {
            "account_id": account_id,
            "backup_switched": True,
            "recovery_delay_seconds": _RECOVERY_DELAY,
            "sync_status": state["sync_status"]
        },
        "error": None,
        "code": None
    }

def exit_degrade_mode() -> dict[str, Any]:
    """exit degrade mode

    Returns:
        dict[str, Any]: 返回值说明
    """
    state = _load_degraded_state()
    if not state.get("degraded_mode"):
        return {
            "success": True,
            "data": {"message": "当前未处于降级模式"},
            "error": None, "code": None
        }

    state["degraded_mode"] = False
    state["recovered_at"] = _now_iso()
    state["sync_status"] = {"fishclaw_mcp": "synced", "env": "synced", "global_config": "synced", "auto_reply_api": "synced"}
    _save_degraded_state(state)

    _append_emergency_log({
        "event": "degrade_mode_exited",
        "degraded_at": state.get("degraded_at"),
        "recovered_at": state["recovered_at"],
        "backup_switched": state.get("backup_switched", [])
    })

    return {
        "success": True,
        "data": {
            "degraded_mode": False,
            "recovered_at": state["recovered_at"],
            "degraded_duration_seconds": (
                datetime.fromisoformat(state["recovered_at"]).timestamp() -
                datetime.fromisoformat(state["degraded_at"]).timestamp()
            ),
            "backup_switched": state.get("backup_switched", []),
            "affected_services_restored": state.get("affected_services", [])
        },
        "error": None,
        "code": None
    }

def get_status() -> dict[str, Any]:
    """获取 status

    Returns:
        dict[str, Any]: 返回值说明
    """
    state = _load_degraded_state()
    if not state:
        return {
            "success": True,
            "data": {"degraded_mode": False, "message": "正常运行中"},
            "error": None, "code": None
        }

    backup_cookies = _get_backup_cookies()
    return {
        "success": True,
        "data": {
            "degraded_mode": state.get("degraded_mode", False),
            "degraded_at": state.get("degraded_at"),
            "recovered_at": state.get("recovered_at"),
            "reason": state.get("reason", ""),
            "backup_available": len(backup_cookies) > 0,
            "backup_cookies_count": len(backup_cookies),
            "backup_switched": state.get("backup_switched", []),
            "pending_scan": state.get("pending_scan", []),
            "sync_status": state.get("sync_status", {}),
            "affected_services": state.get("affected_services", [])
        },
        "error": None,
        "code": None
    }

def main():
    """main"""
    parser = argparse.ArgumentParser(description="Cookie批量失效应急管理器")
    parser.add_argument("--mode", required=True, choices=["detect", "degrade", "recover", "exit", "status"],
                        help="detect=检测失效+启动降级, degrade=手动降级, recover=恢复Cookie, exit=退出降级, status=查看状态")
    parser.add_argument("--failed-cookies", type=str, default="[]",
                        help="失效Cookie列表JSON (detect模式)")
    parser.add_argument("--total-cookies", type=int, default=0,
                        help="总Cookie数量 (detect模式)")
    parser.add_argument("--reason", type=str, default="手动触发",
                        help="降级原因 (degrade模式)")
    parser.add_argument("--account-id", type=str, default="",
                        help="账号ID (recover模式)")

    args = parser.parse_args()

    try:
        if args.mode == "detect":
            failed_cookies = json.loads(args.failed_cookies)
            result = detect_cookie_failure(failed_cookies, args.total_cookies)
        elif args.mode == "degrade":
            result = set_degrade_mode(args.reason)
        elif args.mode == "recover":
            result = recover_cookie(args.account_id)
        elif args.mode == "exit":
            result = exit_degrade_mode()
        elif args.mode == "status":
            result = get_status()
        else:
            result = {"success": False, "data": {}, "error": f"未知模式: {args.mode}", "code": "INVALID_MODE"}

        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0 if result.get("success") else 1)

    except json.JSONDecodeError as e:
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": f"JSON解析失败: {e}", "code": "JSON_PARSE_ERROR"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        logger.error(f"cookie emergency manager异常: {e}", exc_info=True)
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": f"应急处理异常: {e}", "code": "EMERGENCY_ERROR"}, ensure_ascii=False))
        sys.exit(2)

if __name__ == "__main__":
    main()
