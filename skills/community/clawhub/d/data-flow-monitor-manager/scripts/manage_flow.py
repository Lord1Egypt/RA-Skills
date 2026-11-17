#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manage_flow.py | data-flow-monitor-manager SKILL exec脚本
功能: 跨租户数据流监控管理CLI入口,转发到data-flow-monitor-mcp或本地脚本
统一入口: db_logger
参数: --action + --tenant_id + --source + --target + --data_type + --volume
"""
import sys

import json
import argparse
from pathlib import Path
from typing import Any, Dict

# 统一入口规则R18
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger

import logging
logger = get_logger("system", source="skills/data-flow-monitor-manager/scripts/manage_flow.py")

logger = get_logger("manage_flow", source="skills/data-flow-monitor-manager/scripts/manage_flow")

def call_local_graph(tenant_id: str, hours: int) -> Dict[str, Any]:
    """本地数据流图构建(无MCP时降级)

    Args:
        tenant_id (str): 参数说明
        hours (int): 参数说明

    Returns:
        Dict[str, Any]: 返回值说明
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
        from data_flow_graph_builder import build_graph
        result = build_graph(tenant_id=tenant_id or None, hours=hours)
        return {"success": True, "data": result, "error": None, "code": "GRAPH_OK"}
    except Exception as e:
        logger.error(f"异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "GRAPH_FAIL"}

def call_local_scan(days: int, tenant_id: str) -> Dict[str, Any]:
    """本地泄露扫描(降级)

    Args:
        days (int): 参数说明
        tenant_id (str): 参数说明

    Returns:
        Dict[str, Any]: 返回值说明
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
        from leakage_scanner import scan_leakage
        result = scan_leakage(days=days, tenant_id=tenant_id or None)
        return {"success": True, "data": result, "error": None, "code": "SCAN_OK"}
    except Exception as e:
        logger.error(f"异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "SCAN_FAIL"}

def main() -> int:
    """main

    Returns:
        int: 返回值说明
    
    Raises:
        ValueError: 异常说明
    """
    parser = argparse.ArgumentParser(description="数据流监控管理 (data-flow-monitor-manager SKILL)")
    parser.add_argument("--action", required=True,
                        choices=["record", "graph", "detect", "metrics", "scan", "alerts", "threshold", "healthcheck"],
                        help="操作类型")
    parser.add_argument("--tenant_id", default="", help="租户ID")
    parser.add_argument("--source", default="", help="源租户ID(record时)")
    parser.add_argument("--target", default="", help="目标租户ID(record时)")
    parser.add_argument("--data_type", default="normal", help="数据类型")
    parser.add_argument("--volume", type=int, default=0, help="数据量(字节)")
    parser.add_argument("--flow_type", default="query", help="流类型")
    parser.add_argument("--hours", type=int, default=24, help="时间窗口(小时)")
    parser.add_argument("--days", type=int, default=1, help="扫描天数")
    parser.add_argument("--severity", default="L1", choices=["L1", "L2", "L3"], help="最低severity")
    parser.add_argument("--limit", type=int, default=100, help="告警查询条数")
    args = parser.parse_args()

    try:
        if args.action == "graph":
            result = call_local_graph(args.tenant_id, args.hours)
        elif args.action == "scan":
            result = call_local_scan(args.days, args.tenant_id)
        elif args.action == "record":
            if not args.source or not args.target:
                raise ValueError("record需要--source和--target")
            result = {
                "success": False,
                "data": {
                    "source_tenant": args.source,
                    "target_tenant": args.target,
                    "data_type": args.data_type,
                    "volume": args.volume,
                    "hint": "record_data_flow需通过MCP调用"
                },
                "error": "record action需Agent层调用mcp__data-flow-monitor-mcp",
                "code": "MCP_REQUIRED"
            }
        elif args.action == "detect":
            result = {
                "success": False,
                "data": {"hint": "detect_anomaly_flow需通过MCP调用"},
                "error": "detect action需Agent层调用mcp__data-flow-monitor-mcp",
                "code": "MCP_REQUIRED"
            }
        elif args.action == "metrics":
            result = {
                "success": False,
                "data": {"hint": "get_security_metrics需通过MCP调用"},
                "error": "metrics action需Agent层调用mcp__data-flow-monitor-mcp",
                "code": "MCP_REQUIRED"
            }
        elif args.action == "alerts":
            result = {
                "success": False,
                "data": {"hint": "get_leakage_alerts需通过MCP调用或查询leakage_alerts表"},
                "error": "alerts action需Agent层调用mcp__data-flow-monitor-mcp",
                "code": "MCP_REQUIRED"
            }
        elif args.action == "threshold":
            result = {
                "success": False,
                "data": {"hint": "set_flow_threshold需通过MCP调用"},
                "error": "threshold action需Agent层调用mcp__data-flow-monitor-mcp",
                "code": "MCP_REQUIRED"
            }
        elif args.action == "healthcheck":
            result = {
                "success": False,
                "data": {"status": "degraded", "hint": "完整healthcheck需通过MCP调用"},
                "error": "healthcheck action需Agent层调用mcp__data-flow-monitor-mcp",
                "code": "MCP_REQUIRED"
            }
        else:
            raise ValueError(f"未知action: {args.action}")

        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        return 0
    except ValueError as e:
        logger.error(f"参数错误: {e}")
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "INVALID_PARAM"}))
        return 1
    except Exception as e:
        logger.error(f"执行异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "EXEC_ERROR"}))
        return 2

if __name__ == "__main__":
    sys.exit(main())
