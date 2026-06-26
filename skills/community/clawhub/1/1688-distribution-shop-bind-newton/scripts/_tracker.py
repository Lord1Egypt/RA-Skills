#!/usr/bin/env python3
"""
Skill 埋点打点模块

负责记录 Skill 执行过程中的关键事件，用于数据分析和问题排查。
所有 capability 的 cmd 层在关键节点调用 track() 上报埋点。
"""

import json
import time
import os
import sys
import logging

from _const import SKILL_NAME, SKILL_VERSION

logger = logging.getLogger("1688_tracker")

# 埋点事件常量
EVENT_FLOW_START = "flow_start"
EVENT_FLOW_STEP = "flow_step"
EVENT_FLOW_COMPLETE = "flow_complete"
EVENT_FLOW_ERROR = "flow_error"
EVENT_BROWSER_OPEN = "browser_open"
EVENT_BROWSER_RESULT = "browser_result"
EVENT_API_CALL = "api_call"
EVENT_API_ERROR = "api_error"
EVENT_SHOP_QUERY = "shop_query"


def track(event: str, properties: dict = None):
    """
    上报埋点事件。

    通过 stderr 输出 JSON 格式的埋点日志，不影响 stdout 的正常输出。
    牛顿客户端或 ClawHub 平台会采集 stderr 中的埋点数据。

    Args:
        event:      事件名称，如 flow_start、flow_complete
        properties: 事件属性字典
    """
    record = {
        "_tracker": True,
        "skill": SKILL_NAME,
        "version": SKILL_VERSION,
        "event": event,
        "timestamp": int(time.time() * 1000),
        "properties": properties or {},
    }

    try:
        sys.stderr.write(json.dumps(record, ensure_ascii=False) + "\n")
        sys.stderr.flush()
    except Exception as exc:
        logger.debug("埋点上报失败: %s", exc)


def track_flow_start(channel: str, app_key: str, terminal: str = "PC"):
    """记录绑店流程启动。"""
    track(EVENT_FLOW_START, {
        "channel": channel,
        "appKey": app_key,
        "terminal": terminal,
    })


def track_flow_step(channel: str, app_key: str, step_name: str, step_code: str):
    """记录绑店流程步骤推进。"""
    track(EVENT_FLOW_STEP, {
        "channel": channel,
        "appKey": app_key,
        "stepName": step_name,
        "stepCode": step_code,
    })


def track_flow_complete(channel: str, app_key: str):
    """记录绑店流程完成。"""
    track(EVENT_FLOW_COMPLETE, {
        "channel": channel,
        "appKey": app_key,
    })


def track_flow_error(channel: str, app_key: str, error: str):
    """记录绑店流程异常。"""
    track(EVENT_FLOW_ERROR, {
        "channel": channel,
        "appKey": app_key,
        "error": str(error)[:500],
    })


def track_api_call(tool_name: str, latency_ms: int = 0, success: bool = True):
    """记录 API 调用。"""
    track(EVENT_API_CALL, {
        "toolName": tool_name,
        "latencyMs": latency_ms,
        "success": success,
    })


def track_api_error(tool_name: str, error: str):
    """记录 API 调用异常。"""
    track(EVENT_API_ERROR, {
        "toolName": tool_name,
        "error": str(error)[:500],
    })
