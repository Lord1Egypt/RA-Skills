#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""manage_checkpoint.py - 工作流检查点管理exec脚本 (ARCH-5)

通过命令行调用checkpoint-mcp的MCP工具函数。
支持: save/get/list/cache/cached_get/rebuild/verify/healthcheck

用法:
  python manage_checkpoint.py --action save --workflow_id wf_001 --step_id step_1 --state_data '{"progress":30}'
  python manage_checkpoint.py --action get --workflow_id wf_001 --step_id step_1
  python manage_checkpoint.py --action list --workflow_id wf_001
  python manage_checkpoint.py --action cache --workflow_id wf_001 --step_id step_1 --state_data '{"progress":30}'
  python manage_checkpoint.py --action cached_get --workflow_id wf_001 --step_id step_1
  python manage_checkpoint.py --action rebuild --tenant_id default
  python manage_checkpoint.py --action verify --workflow_id wf_001
  python manage_checkpoint.py --action healthcheck
"""
import argparse

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# 加载项目scripts路径以使用统一入口
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "mcps" / "checkpoint-mcp"))

from mcps.shared.db_logger import get_logger

import logging
logger = get_logger("system", source="skills/checkpoint-manager/scripts/manage_checkpoint.py")

logger = get_logger("checkpoint-manager", source="skills/checkpoint-manager/scripts/manage_checkpoint.py")

async def _call(action: str, workflow_id: Optional[str], step_id: Optional[str],
                tenant_id: str, state_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """异步调用MCP工具函数。直接import server模块,避免stdio通信开销。"""
    try:
        import server as cp_server  # type: ignore
    except ImportError as e:
        logger.error(f"异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": f"无法加载checkpoint-mcp server: {e}", "code": "IMPORT_ERROR"}

    try:
        if action == "save":
            if not workflow_id or not step_id or state_data is None:
                return {"success": False, "data": {}, "error": "save需要--workflow_id --step_id --state_data", "code": "INVALID_ARG"}
            result = await cp_server.save_checkpoint(
                workflow_id=workflow_id, step_id=step_id,
                state_data=state_data, tenant_id=tenant_id
            )
        elif action == "get":
            if not workflow_id or not step_id:
                return {"success": False, "data": {}, "error": "get需要--workflow_id --step_id", "code": "INVALID_ARG"}
            result = await cp_server.get_checkpoint(workflow_id=workflow_id, step_id=step_id)
        elif action == "list":
            if not workflow_id:
                return {"success": False, "data": {}, "error": "list需要--workflow_id", "code": "INVALID_ARG"}
            result = await cp_server.list_checkpoints(workflow_id=workflow_id, tenant_id=tenant_id)
        elif action == "cache":
            if not workflow_id or not step_id or state_data is None:
                return {"success": False, "data": {}, "error": "cache需要--workflow_id --step_id --state_data", "code": "INVALID_ARG"}
            result = await cp_server.cache_to_sqlite(
                workflow_id=workflow_id, step_id=step_id, state_data=state_data
            )
        elif action == "cached_get":
            if not workflow_id or not step_id:
                return {"success": False, "data": {}, "error": "cached_get需要--workflow_id --step_id", "code": "INVALID_ARG"}
            result = await cp_server.get_cached_state(workflow_id=workflow_id, step_id=step_id)
        elif action == "rebuild":
            result = await cp_server.rebuild_sqlite_cache(tenant_id=tenant_id)
        elif action == "verify":
            result = await cp_server.verify_checkpoint_integrity(workflow_id=workflow_id or "")
        elif action == "healthcheck":
            result = await cp_server.healthcheck()
        else:
            return {"success": False, "data": {}, "error": f"未知action: {action}", "code": "UNKNOWN_ACTION"}
        return json.loads(result)
    except Exception as e:
        logger.error(f"manage_checkpoint调用失败: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "CALL_ERROR"}

def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    parser = argparse.ArgumentParser(description="工作流检查点管理exec脚本(ARCH-5)")
    parser.add_argument("--action", required=True,
                        choices=["save", "get", "list", "cache", "cached_get", "rebuild", "verify", "healthcheck"],
                        help="操作类型")
    parser.add_argument("--workflow_id", default=None, help="工作流ID(除healthcheck/rebuild外必填)")
    parser.add_argument("--step_id", default=None, help="步骤ID(save/get/cache/cached_get必填)")
    parser.add_argument("--tenant_id", default="default", help="租户ID(默认default)")
    parser.add_argument("--state_data", default=None, help="状态数据JSON字符串(save/cache必填)")
    args = parser.parse_args()

    state_data: Optional[Dict[str, Any]] = None
    if args.state_data:
        try:
            state_data = json.loads(args.state_data)
        except json.JSONDecodeError as e:
            logger.error(f"Exception in except block: {e}");
            logger.error(json.dumps({
                "success": False, "data": {},
                "error": f"state_data不是有效JSON: {e}", "code": "INVALID_JSON"
            }, ensure_ascii=False))
            return 1

    result = asyncio.run(_call(args.action, args.workflow_id, args.step_id, args.tenant_id, state_data))
    print(json.dumps(result, ensure_ascii=False, default=str))
    return 0 if result.get("success") else 1

if __name__ == "__main__":
    sys.exit(main())
