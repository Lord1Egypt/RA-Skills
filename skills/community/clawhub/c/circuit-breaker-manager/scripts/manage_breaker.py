#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""manage_breaker.py - 熔断器管理exec脚本 (ARCH-10)

通过命令行调用resilience-mcp的MCP工具函数。
支持: register/graph/state/record_failure/record_success/check/reset/bulkhead/healthcheck

用法:
  python manage_breaker.py --action register --mcp_name content-publisher --depends_on multi-publisher-mcp sensitive-word-mcp
  python manage_breaker.py --action state --mcp_name xianyu-agent-mcp
  python manage_breaker.py --action check --mcp_name fishclaw-mcp
  python manage_breaker.py --action record_failure --mcp_name fishclaw-mcp --error_type timeout
  python manage_breaker.py --action reset --mcp_name fishclaw-mcp
  python manage_breaker.py --action graph
  python manage_breaker.py --action healthcheck
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# 加载项目scripts路径以使用统一入口
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "mcps" / "resilience-mcp"))

from mcps.shared.db_logger import get_logger

logger = get_logger("circuit-breaker-manager", source="skills/circuit-breaker-manager/scripts/manage_breaker.py")


async def _call(action: str, mcp_name: Optional[str], depends_on: Optional[list],
                error_type: str) -> Dict[str, Any]:
    """异步调用MCP工具函数。直接import server模块,避免stdio通信开销。"""
    try:
        import _circuit_breaker_module as cb_module  # type: ignore
        import server as resilience_server  # type: ignore
    except ImportError as e:
        logger.error(f"异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": f"无法加载resilience-mcp server: {e}", "code": "IMPORT_ERROR"}

    try:
        if action == "register":
            if not mcp_name or not depends_on:
                return {"success": False, "data": {}, "error": "register需要--mcp_name和--depends_on", "code": "INVALID_ARG"}
            result = await cb_module.register_mcp_dependency(mcp_name=mcp_name, depends_on=depends_on)
        elif action == "graph":
            result = await cb_module.get_dependency_graph()
        elif action == "state":
            if not mcp_name:
                return {"success": False, "data": {}, "error": "state需要--mcp_name", "code": "INVALID_ARG"}
            result = await cb_module.get_circuit_state(mcp_name=mcp_name)
        elif action == "record_failure":
            if not mcp_name:
                return {"success": False, "data": {}, "error": "record_failure需要--mcp_name", "code": "INVALID_ARG"}
            result = await cb_module.record_failure(mcp_name=mcp_name, error_type=error_type)
        elif action == "record_success":
            if not mcp_name:
                return {"success": False, "data": {}, "error": "record_success需要--mcp_name", "code": "INVALID_ARG"}
            result = await cb_module.record_success(mcp_name=mcp_name)
        elif action == "check":
            if not mcp_name:
                return {"success": False, "data": {}, "error": "check需要--mcp_name", "code": "INVALID_ARG"}
            result = await cb_module.check_circuit(mcp_name=mcp_name)
        elif action == "reset":
            if not mcp_name:
                return {"success": False, "data": {}, "error": "reset需要--mcp_name", "code": "INVALID_ARG"}
            result = await cb_module.reset_circuit(mcp_name=mcp_name)
        elif action == "bulkhead":
            if not mcp_name:
                return {"success": False, "data": {}, "error": "bulkhead需要--mcp_name", "code": "INVALID_ARG"}
            result = await cb_module.get_bulkhead_status(mcp_name=mcp_name)
        elif action == "healthcheck":
            result = await resilience_server.healthcheck()
        else:
            return {"success": False, "data": {}, "error": f"未知action: {action}", "code": "UNKNOWN_ACTION"}
        return json.loads(result)
    except Exception as e:
        logger.error(f"manage_breaker调用失败: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "CALL_ERROR"}


def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="熔断器管理exec脚本(ARCH-10)")
    parser.add_argument("--action", required=True,
                        choices=["register", "graph", "state", "record_failure", "record_success", "check", "reset", "bulkhead", "healthcheck"],
                        help="操作类型")
    parser.add_argument("--mcp_name", default=None, help="MCP服务名(除graph/healthcheck外必填)")
    parser.add_argument("--depends_on", nargs="*", default=None, help="依赖MCP列表(仅register)")
    parser.add_argument("--error_type", default="unknown", help="错误类型(仅record_failure)")
    args = parser.parse_args()

    result = asyncio.run(_call(args.action, args.mcp_name, args.depends_on, args.error_type))
    print(json.dumps(result, ensure_ascii=False, default=str))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
