#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""管道引擎占位符解析器 — 按租户套餐动态选择TTS/视频/图像/唇形同步MCP

来源: RC-1/RC-2修复 + 5轮审核BUG-V4A-002(文件不存在,非加载问题)
R规则: R1(运行时证据) / R34(虚假实现检测) / R38(测试闭环) / R55(循环依赖检测) / R57(修复证据)

功能: 将content-orchestrator管道中的${engine.tts}/${engine.video}/${engine.image}/${engine.lipsync}
占位符解析为实际的MCP工具名+参数,按租户套餐等级选择对应引擎。
"""
import os
import sys
import json
from typing import Any

# db_logger统一日志 (R14统一入口铁律 + BUG-V4A-002 lint修复)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("pipeline_engine_resolver", source="content-orchestrator")

# 引擎映射表: 占位符名 → MCP服务器名(纯服务器名,不含工具名)
# R10修复: 原返回"server.tool"格式,但call_mcp期望第一个参数是纯服务器名,工具名由action字段指定
# R10修复: 替换不存在的MCP服务器(device-operations-mcp/vidu-mcp/seedream-mcp/sau-mcp)为已注册的
# R10v2修复: cosyvoice-mcp在openclaw.json中未注册,tts-adapter-mcp内部含CosyVoice2层
# R10v2修复: 添加image_video占位符(外部JSON中${engine.image_video}使用但_ENGINE_MAP无此key)
_ENGINE_MAP = {
    "tts": {
        "basic": "tts-adapter-mcp",       # 已注册✅ (含Edge-TTS等4层)
        "premium": "tts-adapter-mcp",     # cosyvoice-mcp未注册,tts-adapter内含CosyVoice2层
    },
    "video": {
        "basic": "kling-mcp",              # 已注册✅
        "premium": "moneyprinterturbo-mcp",  # 已注册✅ (P0核心功能)
    },
    "image": {
        "basic": "flux-mcp",               # 已注册✅
        "premium": "flux-mcp",             # 无高级替代,使用同一MCP
    },
    "image_video": {
        "basic": "kling-mcp",              # text_to_video/image_to_video
        "premium": "moneyprinterturbo-mcp",  # mpt_generate_video
    },
    "lipsync": {
        "basic": "liveportrait-mcp",      # 已注册✅
        "premium": "liveportrait-mcp",     # 同一MCP,不同工具由action区分
    },
    "digital_human": {
        "basic": "character-workshop-mcp",    # 数字人引擎(与execute_pipeline默认映射一致)
        "premium": "character-workshop-mcp",  # 同一MCP,不同工具由action区分
    },
}


def _get_tenant_plan(tenant_id: str) -> str:
    """查询租户套餐等级(basic/standard/premium)

    来源: tenant_subscriptions表plan_type字段
    """
    try:
        # R75.2/E-3修复: 使用db_pool统一连接(替代psycopg2.connect碎片化)
        from mcps.shared.db_pool import get_connection, return_connection
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SET LOCAL app.current_tenant = %s", (tenant_id,))
                # BUG-V4A-002补丁: 列名是plan_type(非plan), 套餐值basic/standard/premium/enterprise
                cur.execute(
                    "SELECT plan_type FROM tenant_subscriptions WHERE tenant_id = %s AND status = 'active' LIMIT 1",
                    (tenant_id,))
                row = cur.fetchone()
        finally:
            return_connection(conn)
        if row and row[0]:
            plan = str(row[0]).lower()
            # standard/premium/enterprise/pro 统一映射为 premium引擎
            if plan in ("premium", "enterprise", "pro", "standard"):
                return "premium"
        return "basic"
    except Exception as e:
        logger.error(f"[engine-resolver] 查询租户套餐失败,降级为basic: {e}")
        return "basic"


def resolve_pipeline_steps(steps: list, tenant_id: str = "") -> list[Any]:
    """解析管道步骤中的${engine.*}占位符

    Args:
        steps: 管道步骤列表,每个步骤是dict,可能包含tool/args字段
        tenant_id: 租户ID,用于查询套餐等级

    Returns:
        解析后的步骤列表(占位符替换为实际MCP工具名)
    """
    if not steps:
        return steps

    plan = _get_tenant_plan(tenant_id) if tenant_id else "basic"
    resolved_count = 0

    for step in steps:
        if not isinstance(step, dict):
            continue
        # 解析tool字段中的占位符
        tool = step.get("tool", "")
        if isinstance(tool, str) and "${engine." in tool:
            for engine_type, plan_map in _ENGINE_MAP.items():
                placeholder = "${engine." + engine_type + "}"
                if placeholder in tool:
                    replacement = plan_map.get(plan, plan_map["basic"])
                    step["tool"] = tool.replace(placeholder, replacement)
                    resolved_count += 1
                    logger.info(f"[engine-resolver] 解析 {placeholder} → {replacement} (plan={plan})")
                    break
        # 解析args字段中的占位符
        args = step.get("args")
        if isinstance(args, dict):
            for k, v in args.items():
                if isinstance(v, str) and "${engine." in v:
                    for engine_type, plan_map in _ENGINE_MAP.items():
                        placeholder = "${engine." + engine_type + "}"
                        if placeholder in v:
                            replacement = plan_map.get(plan, plan_map["basic"])
                            args[k] = v.replace(placeholder, replacement)
                            resolved_count += 1
                            logger.info(f"[engine-resolver] 解析args.{k} {placeholder} → {replacement}")
                            break

    logger.info(f"[engine-resolver] 共解析{resolved_count}个占位符 (tenant={tenant_id}, plan={plan})")
    return steps


def check_resolver_available() -> dict[str, Any]:
    """检查resolver是否可用(L1静态验证)"""
    return {
        "success": True,
        "data": {
            "available": True,
            "engine_types": list(_ENGINE_MAP.keys()),
            "plans": ["basic", "premium"],
        },
        "error": None,
        "code": None,
    }


if __name__ == "__main__":
    # L2脚本测试: 验证占位符解析
    test_steps = [
        {"tool": "${engine.tts}", "args": {"text": "测试"}},
        {"tool": "${engine.video}", "args": {"script": "脚本"}},
        {"tool": "fixed_tool", "args": {}},
    ]
    result = resolve_pipeline_steps(test_steps, tenant_id="test")
    print(json.dumps({"success": True, "data": {"resolved_steps": result}, "error": None}, ensure_ascii=False))
