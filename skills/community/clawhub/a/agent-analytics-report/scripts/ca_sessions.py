# -*- coding: utf-8 -*-
# ca_sessions.py — 采集器子模块（从 collect_usage_data.py 拆分，2026-09-02）

import argparse
import calendar
import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from ca_core import (  # 共享常量与纯函数
    ALL_CUSTOM_MODELS,
    ALL_LOCAL_MODELS,
    ALL_ROUTER_MODELS,
    CACHE_DISCOUNT,
    CUSTOM_LOCAL_PRICING,
    DB_PATH,
    DEFAULT_BLENDED_PER_MILLION,
    DEFAULT_MODEL,
    DELISTED_MODELS,
    DISCOVERED_EXTERNAL,
    DISCOVERED_LOCAL,
    DISCOVERED_ROUTER,
    DISPLAY_MERGE,
    GLM52_FAMILY,
    GLM52_RATE,
    HOME,
    LOW_CONFIDENCE,
    LOW_CONFIDENCE_BIAS,
    MEDIA_EXTS,
    MODEL_PRICING,
    MODE_RATES_META,
    ORPHAN_KEY,
    ORPHAN_LABEL,
    PERIOD_DAYS,
    PERIOD_LABELS,
    PERIOD_NEXT,
    PERIOD_SHORT,
    PER_MILLION,
    PROJECTS_DIR,
    ROUTER_ALIASES,
    ROUTER_HOSTS,
    ROUTER_VENDORS,
    SCHEDULED_PRICING,
    SESSIONS_DIR,
    SILICONFLOW_VENDOR_PREFIXES,
    SYSTEM_REMINDER_RE,
    TASK_RULES_PATH,
    TASK_TYPE_RULES,
    TIER_ALIASES,
    TIER_CANON,
    TIER_LABELS,
    TIMED_FREE,
    TRACES_DIR,
    TZ,
    UNNAMED_LABEL,
    USAGE_LOG_PATH,
    USER_CUSTOM_MODELS,
    WB_DIR,
    WORKBUDDY_SESSIONS,
    _CHEAPER_ALT,
    _PRICING,
    _PRICING_LOCAL_LOADED,
    _build_sid_to_title,
    _load_acc_product_config,
    _load_pricing_config,
    _to_num,
    call_time_of,
    canonical_tier,
    compute_cost,
    discover_custom_models,
    effective_tokens_of,
    glm52_discount_multiplier,
    is_router_like,
    is_scheduled_free,
    is_timed_free,
    iso_to_date,
    iso_to_dt,
    load_task_rules,
    low_confidence_reason,
    low_confidence_bias,
    merge_display_key,
    normalize_model,
    parse_channel,
    parse_date_range,
    price_of,
    resolve_date_range,
    resolve_model,
    score_task_types,
    trace_cost,
    ts_to_date,
    ts_to_dt,
    _router_avg_unit_price,
)
from ca_sources import get_session_content, get_session_artifact_fingerprint
# ↑ 修复：collect_task_types 依赖这两个 ca_sources 函数。拆分时漏了导入，
#   实际运行 collect_usage_data.py（WorkBuddy 源）会 NameError——e2e 测试只覆盖了
#   generate_report 与 claude-code 分支，未触达此路径，故长期未被发现。

__all__ = ['aggregate_task_token_stats', 'aggregate_top_tasks', 'classify_task', 'collect_task_types']

def classify_task(session_text):
    """根据会话文本推断任务类型（加权评分版）。

    传入的 session_text 通常已由 collect_task_types 拼接为
    「对话内容 + 生成物指纹 + 会话标题」三部分。

    算法：所有规则参与加权评分（signal 密度 + 权重 + 长度加分 + 重复衰减），
    取总分最高者；同分按规则 priority 打破平局（保持旧版首匹配的稳定性）。
    规则与评分参数见 scripts/task_rules.json（可编辑），缺失时回退内置规则。
    """
    result = score_task_types(session_text)
    if result["top"] is not None:
        return result["top"]
    return "其他"

def collect_task_types(sessions, classifier=None):
    """为每个会话分配任务类型

    classifier: 可选 callable(text) -> task_type（如 LLM 分类器）；
                缺省用内置加权启发式 classify_task。

    分类依据（按优先级合并，全面覆盖「对话内容 + 生成物（含已删除）」）：
      1. 后台自动化会话（is_background_automation）直接归为「自动化配置」；
      2. 其余会话的候选文本 = 对话内容 + 生成物指纹 + 会话标题 + 自定义标题：
         a) 对话内容：user/assistant 消息 + reasoning（剥离 system-reminder）；
         b) 生成物指纹：transcript 中的 ImageGen/VideoGen 调用、以及
            file-history-snapshot 保留的「已删除」文件键名（见 get_session_artifact_fingerprint）；
         c) 对话内容/生成物指纹均缺失时，回退到会话标题，保证分类稳定可复现。

    透明度：启发式模式下把置信度写入 s["_task_confidence"]（0~1，
    「最高分 − 次高分」占最高分的比例；0 = 平票不确定，1 = 一边倒）。
    """
    task_map = {}
    for s in sessions:
        if s.get("is_background_automation"):
            task_type = "自动化配置"
            s["_task_confidence"] = 1.0
        else:
            content = get_session_content(s["id"], s.get("cwd", ""))
            artifacts = get_session_artifact_fingerprint(s["id"], s.get("cwd", ""))
            title = (s.get("title", "") + " " + s.get("custom_title", "")).strip()
            dialogue = s.get("_dialogue_text", "") or ""  # claude-code 适配器的对话兜底
            combined = " ".join(p for p in (content, artifacts, dialogue, title) if p)
            text = combined if combined.strip() else (s.get("title", "") + " " + s.get("custom_title", ""))
            if classifier is not None:
                # classifier 自带失败兜底（见 task_classifier_llm.build_llm_classifier）：
                # 返回 falsy 时回退启发式
                task_type = classifier(text) or classify_task(text)
            else:
                task_type = classify_task(text)
                scored = score_task_types(text)
                s["_task_confidence"] = scored.get("confidence", 0.0)
        s["task_type"] = task_type
        task_map[s["id"]] = task_type
    return task_map

def aggregate_task_token_stats(traces, sessions):
    """按任务类型聚合 token 消耗（join traces.session_id → session.task_type）"""
    sid_to_type = {s["id"]: s.get("task_type", "其他") for s in sessions}
    tt_agg = defaultdict(lambda: {"sessions": set(), "total": 0, "input": 0,
                                  "output": 0, "cached": 0, "cost": 0.0, "calls": 0,
                                  "effective": 0, "effective_cost": 0.0})
    for t in traces:
        tt = sid_to_type.get(t.get("session_id"), "其他")
        a = tt_agg[tt]
        a["sessions"].add(t.get("session_id"))
        a["total"] += t["total_tokens"]
        a["input"] += t["input_tokens"]
        a["output"] += t["output_tokens"]
        a["cached"] += t["cached_tokens"]
        a["cost"] += t.get("total_cost", 0.0)
        a["calls"] += t.get("call_count", 0)
        a["effective"] += t.get("effective_tokens", 0)
        a["effective_cost"] += t.get("effective_cost", 0.0)
    stats = []
    for tt, a in tt_agg.items():
        stats.append({
            "task_type": tt,
            "session_count": len(a["sessions"]),
            "total_tokens": a["total"],
            "input_tokens": a["input"],
            "output_tokens": a["output"],
            "cached_tokens": a["cached"],
            "effective_tokens": a["effective"],
            "cost": round(a["cost"], 2),
            "effective_cost": round(a["effective_cost"], 2),
            "calls": a["calls"],
        })
    stats.sort(key=lambda x: x["effective_tokens"], reverse=True)
    return stats

def aggregate_top_tasks(traces, sessions, top_n=10):
    """按会话聚合 token 消耗，返回最吃 token 的 Top N 个任务对话框。

    单个会话可能对应多天的 traces，需先按 session_id 汇总；
    会话标题/任务类型取自 sessions（collect_task_types 已写入 task_type）。
    返回字段：session_id、title、task_type、total_tokens、input_tokens、
    output_tokens、cached_tokens、cost、calls。
    """
    sid_to_type = {s["id"]: s.get("task_type", "其他") for s in sessions}
    sid_to_title = _build_sid_to_title(sessions)
    known_ids = set(sid_to_title)
    agg = defaultdict(lambda: {"total": 0, "input": 0, "output": 0,
                               "cached": 0, "cost": 0.0, "calls": 0,
                               "effective": 0, "effective_cost": 0.0})
    for t in traces:
        sid = t.get("session_id")
        if not sid:
            continue
        key = sid if sid in known_ids else ORPHAN_KEY
        a = agg[key]
        a["total"] += t["total_tokens"]
        a["input"] += t["input_tokens"]
        a["output"] += t["output_tokens"]
        a["cached"] += t["cached_tokens"]
        a["cost"] += t.get("total_cost", 0.0)
        a["calls"] += t.get("call_count", 0)
        a["effective"] += t.get("effective_tokens", 0)
        a["effective_cost"] += t.get("effective_cost", 0.0)
    rows = []
    for key, a in agg.items():
        if key == ORPHAN_KEY:
            rows.append({
                "session_id": ORPHAN_LABEL,
                "title": ORPHAN_LABEL,
                "task_type": "其他",
                "total_tokens": a["total"],
                "input_tokens": a["input"],
                "output_tokens": a["output"],
                "cached_tokens": a["cached"],
                "effective_tokens": a["effective"],
                "cost": round(a["cost"], 2),
                "effective_cost": round(a["effective_cost"], 2),
                "calls": a["calls"],
            })
        else:
            rows.append({
                "session_id": key,
                "title": sid_to_title[key],
                "task_type": sid_to_type.get(key, "其他"),
                "total_tokens": a["total"],
                "input_tokens": a["input"],
                "output_tokens": a["output"],
                "cached_tokens": a["cached"],
                "effective_tokens": a["effective"],
                "cost": round(a["cost"], 2),
                "effective_cost": round(a["effective_cost"], 2),
                "calls": a["calls"],
            })
    rows.sort(key=lambda x: x["effective_tokens"], reverse=True)
    return rows[:top_n]
