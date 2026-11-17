#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""manage_healing.py - 故障自愈管理exec脚本 (ARCH-8)

通过命令行调用resilience-mcp的MCP工具函数。
支持: trigger/diagnose/repair/verify/regression/history/healthcheck

用法:
  python manage_healing.py --action trigger --fault_type docker_container_stopped --context '{"container_name":"redis"}'
  python manage_healing.py --action diagnose --fault_type disk_full
  python manage_healing.py --action repair --fault_type llm_provider_429 --dry_run
  python manage_healing.py --action verify --fault_type gateway_no_response
  python manage_healing.py --action regression --fault_type redis_connection_failed --full
  python manage_healing.py --action history --limit 10 --status failed
  python manage_healing.py --action healthcheck
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# 加载项目scripts路径以使用统一入口(R18)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT / "mcps" / "resilience-mcp"))

from mcps.shared.db_logger import get_logger

logger = get_logger("auto-healing-manager", source="skills/auto-healing-manager/scripts/manage_healing.py")


async def _call(action: str, fault_type: Optional[str], context: Optional[str],
                force: bool, dry_run: bool, full: bool, limit: int,
                status: Optional[str]) -> Dict[str, Any]:
    """异步调用MCP工具函数。直接import server模块,避免stdio通信开销。"""
    try:
        import _auto_healing_module as ah_module  # type: ignore
        import server as resilience_server  # type: ignore
    except ImportError as e:
        logger.error(f"异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": f"无法加载resilience-mcp server: {e}", "code": "IMPORT_ERROR"}

    try:
        if action == "trigger":
            if not fault_type:
                return {"success": False, "data": {}, "error": "trigger需要--fault_type", "code": "INVALID_ARG"}
            result = await ah_module.trigger_healing(fault_type=fault_type, fault_context=context or "{}", force=force)
        elif action == "diagnose":
            if not fault_type:
                return {"success": False, "data": {}, "error": "diagnose需要--fault_type", "code": "INVALID_ARG"}
            result = await ah_module.diagnose_fault(fault_type=fault_type, fault_context=context or "{}")
        elif action == "repair":
            if not fault_type:
                return {"success": False, "data": {}, "error": "repair需要--fault_type", "code": "INVALID_ARG"}
            result = await ah_module.execute_repair(fault_type=fault_type, fault_context=context or "{}", dry_run=dry_run)
        elif action == "verify":
            result = await ah_module.verify_repair(fault_type=fault_type or "unknown", fault_context=context or "{}")
        elif action == "regression":
            result = await ah_module.run_regression(fault_type=fault_type or "unknown", fault_context=context or "{}", full=full)
        elif action == "history":
            result = await ah_module.get_healing_history(limit=limit, fault_type=fault_type or "", status=status or "")
        elif action == "healthcheck":
            result = await resilience_server.healthcheck()
        else:
            return {"success": False, "data": {}, "error": f"未知action: {action}", "code": "UNKNOWN_ACTION"}
        return json.loads(result)
    except Exception as e:
        logger.error(f"manage_healing调用失败: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "CALL_ERROR"}


def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="故障自愈管理exec脚本(ARCH-8)")
    parser.add_argument("--action", required=True,
                        choices=["trigger", "diagnose", "repair", "verify", "regression", "history", "healthcheck"],
                        help="操作类型")
    parser.add_argument("--fault_type", default=None, help="故障类型标识(除history/healthcheck外必填)")
    parser.add_argument("--context", default=None, help="故障上下文(JSON字符串)")
    parser.add_argument("--force", action="store_true", help="强制触发忽略冷却(仅trigger)")
    parser.add_argument("--dry_run", action="store_true", help="干跑模式(仅repair)")
    parser.add_argument("--full", action="store_true", help="全量验证(仅regression)")
    parser.add_argument("--limit", type=int, default=50, help="历史条数(仅history)")
    parser.add_argument("--status", default=None, help="按状态过滤(仅history)")
    args = parser.parse_args()

    result = asyncio.run(_call(args.action, args.fault_type, args.context, args.force,
                               args.dry_run, args.full, args.limit, args.status))
    print(json.dumps(result, ensure_ascii=False, default=str))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
