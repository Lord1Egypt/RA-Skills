# -*- coding: utf-8 -*-
# ca_aggregate.py — 采集器子模块（从 collect_usage_data.py 拆分，2026-09-02）

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
    ensure_custom_models_discovered,
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

__all__ = ['_detect_daily_anomalies', '_detect_session_anomalies', '_fmt_anom_val', '_normalize_model_key', '_percentile', 'aggregate_by_exec_model', 'aggregate_by_model', 'aggregate_by_session', 'aggregate_by_tier', 'aggregate_traces_by', 'build_savings_insights', 'build_savings_insights_from_official', 'detect_cost_anomalies']

def aggregate_traces_by(traces, key_field, resolve_key_fn=None, resolve_billing_key_fn=None):
    """按 key_field 聚合模型维度。

    key_field 取值：
      - "model_key"  → 接口/通道维度（trace 关联的 session 配置接口标识，如
                       "custom-local:glm-4.6v" 与裸 "glm-4.6v" 分两行，用于准确计费）
      - "model_name" → 实际执行模型维度（API 实际执行的裸模型名，如 "glm-5.2"，
                       反映你真实使用了哪些模型、各多少次）
      - None         → 使用 resolve_key_fn 自定义键解析函数

    resolve_key_fn: 可选回调，接收 trace 字典，返回**显示键**（用于分组与报告展示）。
    用于处理特殊修正逻辑（如 hy3/hy3-x 误标修正、display_merge 显示层合并）。

    resolve_billing_key_fn: 可选回调，接收 trace 字典，返回**计费键**，默认与显示键相同。
    仅 display_merge 合并场景需要分离二者：显示键是合并后的基础模型名（报告只显示一行），
    计费键仍是该 trace 的实际执行模型（exec_model）。否则合并行会把「收费版」的用量
    也按「免费额度版」的限免价算成 ¥0，导致花费凭空消失。

    返回列表（已配置单价的模型按花费降序在前）。每条：
      model / channel / calls / total_tokens / input_tokens / output_tokens / cached_tokens /
      effective_tokens / input_cost / output_cost / total_cost / effective_cost /
      configured(bool) / unit_price_input / unit_price_output
    单价取自 price_of（通道感知：openrouter-free=0；custom-local 默认对齐同名网关价/可覆盖；
    gateway 取 MODEL_PRICING）；未配置单价的模型 configured=False，其 unit_price_* 为 None、
    cost 字段为 0（不瞎算，交由报告显示「未配置」）。
    """
    # 计费口径统一：exec_model 维度（§3.1 账单口径）直接汇总 trace 级已算好的
    # effective_cost / total_cost 等字段 —— 与概览头条、每日表、§4 同源（均来自 collect_traces
    # 的逐 trace 计价，含 auto 的 router_avg、default 的 resolve_model 映射），因此 §3.1 合计
    # ≡ 概览「实际成本」必然对账一致，消除「报告自己矛盾」。
    # model_key 维度（§3.2 入口/使用视图）仍按价重算（入口免费就记 0，反映「你请求了哪个免费入口」）。
    sum_trace_cost = (key_field == "exec_model")
    agg = {}
    for t in traces:
        if resolve_key_fn is not None:
            m = resolve_key_fn(t)
        else:
            m = t.get(key_field)
        # 计费键：默认与显示键相同；display_merge 合并场景下取该 trace 的实际执行模型，
        # 保证「免费额度版记 ¥0 / 收费版按刊例价」的口径不被显示层合并破坏。
        bm = resolve_billing_key_fn(t) if resolve_billing_key_fn is not None else m
        if not m or m == "default":
            # 接口维度允许回退到裸名；实际执行维度严格只用 model_name
            if key_field == "model_key":
                m = t.get("model_name") or "default"
            else:
                continue
        if m == "default":
            continue
        # GLM-5.2 变体不再合并：glm-5.2-x / glm-5.2x 与 glm-5.2 各自独立成行
        ip, op = price_of(m)
        configured = (ip is not None and op is not None)
        ch = parse_channel(m)[0]
        a = agg.setdefault(m, {
            "model": m, "channel": ch, "calls": 0,
            "total_tokens": 0, "input_tokens": 0, "output_tokens": 0, "cached_tokens": 0,
            "effective_tokens": 0,
            "input_cost": 0.0, "output_cost": 0.0, "total_cost": 0.0, "effective_cost": 0.0,
            "configured": configured,
            "unit_price_input": ip if configured else None,
            "unit_price_output": op if configured else None,
            # 本行是否配置了时段定价规则（夜间免费 / 峰谷双档 / 限期促销）——
            # 只是「有规则」的静态标记（供报告打 ⏱），真实是否命中按每次调用时刻判定。
            "scheduled": bool(SCHEDULED_PRICING.get(normalize_model(m))
                              or SCHEDULED_PRICING.get(normalize_model(bm))),
            "free_calls": 0,
        })
        a["calls"] += 1
        a["total_tokens"] += t.get("total_tokens", 0)
        a["input_tokens"] += t.get("input_tokens", 0)
        a["output_tokens"] += t.get("output_tokens", 0)
        a["cached_tokens"] += t.get("cached_tokens", 0)
        a["effective_tokens"] += t.get("effective_tokens", 0)
        # 限免调用计数（与计价分支无关）：用于两种口径都能正确标注「限时免费」，
        # 避免账单口径下限免模型的 ¥0 被渲染器误判为「未配置单价」。
        # ⚠️ 用计费键 bm 而非显示键 m：合并行里只有真正落在限免期内的调用才算，
        # 否则含收费调用的合并行会被整体误标为「限时免费」。
        if is_timed_free(bm, t.get("date")):
            a["timed_free_calls"] = a.get("timed_free_calls", 0) + 1
        if sum_trace_cost:
            # 账单口径：直接累加 trace 已算成本（含 auto router_avg / 限免 ¥0），必然与头条一致
            a["input_cost"] += t.get("input_cost", 0.0)
            a["output_cost"] += t.get("output_cost", 0.0)
            a["total_cost"] += t.get("total_cost", 0.0)
            a["effective_cost"] += t.get("effective_cost", 0.0)
        else:
            # 入口/使用视图：按本模型在本 trace 日期的真实单价重算（免费入口记 0）
            # ⚠️ 用计费键 bm：合并行内各 trace 按「自己实际执行的模型」计价，
            # 否则 hy4-preview-x 的用量会被 hy4-preview 的限免价算成 ¥0，花费凭空消失。
            # 传入调用时刻（日期 + 小时 + 星期）→ 夜间免费 / 峰谷双档 / 限期促销生效。
            tip, top = price_of(bm, **call_time_of(t.get("started_at"), t.get("date")))
            if tip is not None and top is not None:
                inp = t.get("input_tokens", 0)
                out = t.get("output_tokens", 0)
                # GLM-5.2 夜猫子计划：按模型名定率（与 §3.1 同源）
                _mult = glm52_discount_multiplier(bm)
                a["input_cost"] += (inp / PER_MILLION) * tip * _mult
                a["output_cost"] += (out / PER_MILLION) * top * _mult
                a["total_cost"] += ((inp / PER_MILLION) * tip + (out / PER_MILLION) * top) * _mult
                eff_in = max(inp - t.get("cached_tokens", 0) * (1 - CACHE_DISCOUNT), 0)
                a["effective_cost"] += ((eff_in / PER_MILLION) * tip + (out / PER_MILLION) * top) * _mult
                # 免费判定基于「本模型在本 trace 日期的实际单价是否为 0」（而非 trace 级 is_free，
                # 因 is_free 基于 raw_model，无法覆盖「走 auto 路由实际执行 hy3」这类 trace）
                if tip == 0 and top == 0:
                    a["free_calls"] += 1
    rows = list(agg.values())
    if not sum_trace_cost:
        # 限时免费：仅入口视图需要（按入口免费判定）；账单口径已按 trace 实际成本汇总，无需再标
        for r in rows:
            if r["calls"] > 0 and r["free_calls"] == r["calls"] and normalize_model(r["model"]) in TIMED_FREE:
                r["unit_price_input"] = 0.0
                r["unit_price_output"] = 0.0
                r["configured"] = True
                r["timed_free"] = True
            else:
                r["timed_free"] = False
        # 路由别名（如 auto）：无单一单价，用「所有计费模型（单价>0）的均价」做代表性估算
        # ⚠️ 排除路由类别名（含三档）：它们自身无单一单价，混入会抬高 auto 的估算均价
        paid = [(r["unit_price_input"], r["unit_price_output"]) for r in rows
                if r["configured"] and (r["unit_price_input"] or 0) > 0
                and not is_router_like(r["model"])]
        avg_ip, avg_op = _router_avg_unit_price(paid)
        for r in rows:
            if r["model"] in ROUTER_ALIASES and not r["configured"] and avg_ip is not None:
                r["unit_price_input"] = round(avg_ip, 4)
                r["unit_price_output"] = round(avg_op, 4)
                r["configured"] = True
                r["is_router"] = True
                inp = r["input_tokens"]
                out = r["output_tokens"]
                r["input_cost"] = (inp / PER_MILLION) * avg_ip
                r["output_cost"] = (out / PER_MILLION) * avg_op
                r["total_cost"] = r["input_cost"] + r["output_cost"]
                eff_in = max(inp - r["cached_tokens"] * (1 - CACHE_DISCOUNT), 0)
                r["effective_cost"] = (eff_in / PER_MILLION) * avg_ip + (out / PER_MILLION) * avg_op
            else:
                r.setdefault("is_router", is_router_like(r["model"]))
    else:
        # 账单口径：auto 等路由别名已按 trace 实际成本汇总，仅打标 is_router 便于显示「原生路由」。
        # timed_free 仍需如实标注：本期全部调用都落在限免期内的模型，其 ¥0 是「限时免费」而非「未配置」。
        # 此处保留刊例单价（不清零），让报告能同时呈现「原价 X / 实付 ¥0」的对比。
        for r in rows:
            r["timed_free"] = bool(
                r["calls"] > 0 and r.get("timed_free_calls", 0) == r["calls"]
            )
            r.setdefault("is_router", is_router_like(r["model"]))
    for r in rows:
        # ── delisted vs custom 的边界（依据用户定义，二者必须分开）──
        #  - delisted（官方已下架）：曾由 WorkBuddy 官方提供、现已下架的模型。
        #    仅当底层模型名命中官方下架名单、且走的是官方通道（非用户自建）时才成立。
        #  - custom（用户自定义）：用户后来通过外部 API 接口自建 / 接入的模型，
        #    表现为 model_key 带 `custom-local:` 前缀或走 openrouter-free 免费档。
        #  判定顺序：① 前缀信号 ② custom-local 通道 ③ openrouter-free 通道
        #  ④ 名称命中自定义集（ALL_CUSTOM_MODELS = 运行时从 models.json 自动发现 ∪ user_custom_models 人工兜底），
        #     专治「撞名官方模型但走官方 gateway」的误识别（如 GLM-4.7-Flash）。
        base = normalize_model(r["model"].split("custom-local:", 1)[-1])
        is_custom = (
            r["model"].lower().startswith("custom-local:")
            or r["channel"] == "custom-local"
            or r["channel"] == "openrouter-free"
            or base in ALL_CUSTOM_MODELS
        )
        # 本地模型（Ollama / localhost:11434）：零 API 成本，标 🏠、单价归零、不计入账单总额。
        # 它同时属于 is_custom（用户自建），但优先按「本地」识别，且绝不误标为官方下架。
        is_local = base in ALL_LOCAL_MODELS
        r["is_custom"] = is_custom
        r["is_local"] = is_local
        # 智能路由 / 聚合网关（外部 API）：标 🔀，提示单价 / 花费为粗略参考。
        # 判定：① 名称命中自动发现的路由模型集；② 走 openrouter-free 免费网关（本身即路由）。
        r["is_router_api"] = (base in ALL_ROUTER_MODELS) or (r["channel"] == "openrouter-free")
        if is_local:
            r["unit_price_input"] = 0.0
            r["unit_price_output"] = 0.0
            r["configured"] = True
            r["input_cost"] = 0.0
            r["output_cost"] = 0.0
            r["total_cost"] = 0.0
            r["effective_cost"] = 0.0
            r["free_calls"] = r["calls"]
        r["is_delisted"] = (not is_custom) and (base in DELISTED_MODELS)
        r["input_cost"] = round(r["input_cost"], 4)
        r["output_cost"] = round(r["output_cost"], 4)
        r["total_cost"] = round(r["total_cost"], 2)
        # 不在此处对 effective_cost 四舍五入：保留全精度，使各模型 effective_cost 之和
        # ≡ 概览「实际成本」总额（summary.total_effective_cost，二者同源、仅分组方式不同），
        # 消除逐行四舍五入导致的 1 分钱漂移（对账目标）。显示端仍按 :.2f 取整。
        r["effective_cost"] = r["effective_cost"]
    # 已配置按估算花费降序在前；未配置排后，仍按调用次数降序
    rows.sort(key=lambda x: (x["configured"], x["effective_cost"], x["calls"]), reverse=True)
    return rows

def aggregate_by_model(traces):
    """按「接口/通道」维度聚合（配置维度，用于准确计费）。

    与 aggregate_by_exec_model 的区别：此处按 trace 的 model_key（用户配置的入口标识）聚合，
    反映你实际请求了哪些入口、各多少次。

    注意：WorkBuddy 在 2026-08-21 之前存在 trace 标签误标问题 —— hy3 调用被错误标记为
    model_key=hy3-x，但 exec_model=hy3。为消除此误标，当 model_key=hy3-x 而 exec_model=hy3 时，
    强制将其归入 hy3 行（与账单口径一致）。

    display_merge（见 pricing.json）：把「收费版变体」（如 hy4-preview-x / hy3-x）在显示层
    合并到基础模型名（hy4-preview / hy3），报告里只出现一行。合并**只改显示分组**，
    计费键仍取各 trace 的 exec_model —— 故免费额度版用量记 ¥0、收费版用量按刊例价计费，
    合并行的花费即「其中收费版那部分的费用」。
    """
    # 仅当报告实际涉及自建模型（custom-local）时才按需发现用户模型配置，
    # 避免在生成其它产品报告时越权读取 ~/.workbuddy/models.json
    if any(
        (t.get("model", "") or "").lower().startswith("custom-local:")
        or (t.get("channel") == "custom-local")
        or (t.get("model_key", "") or "").lower().startswith("custom-local:")
        for t in (traces or [])
    ):
        ensure_custom_models_discovered()

    def _resolve_key(t):
        mk = t.get("model_key", "")
        em = t.get("exec_model", "")
        # hy3-x 误标修正：model_key=hy3-x 但 exec_model=hy3 的 trace 实际是 hy3 调用
        if mk.lower() == "hy3-x" and em.lower() == "hy3":
            return "hy3"
        # display_merge：收费版变体并入基础模型名显示
        return merge_display_key(mk)

    def _resolve_billing_key(t):
        mk = t.get("model_key", "")
        # 仅合并行需要分离：按 trace 实际执行的模型计费，避免限免价吃掉收费版的费用
        if normalize_model(mk) in DISPLAY_MERGE:
            return t.get("exec_model") or mk
        return mk
    return aggregate_traces_by(traces, None, resolve_key_fn=_resolve_key,
                               resolve_billing_key_fn=_resolve_billing_key)

def aggregate_by_exec_model(traces):
    """按「实际执行模型」维度聚合（API 实际执行的裸模型名，反映真实使用分布）。

    与 aggregate_by_model 的区别：此处按 trace 的 exec_model（来自 modelInfo.models[0]，
    即 API 真实执行的底层模型）聚合，因此走 auto 路由实际执行 glm-5.2 的调用、以及
    custom-local 通道的 GLM 调用，都会归到对应裸模型行，而非被 auto / custom-local:* 吸收。
    用于回答「我到底实际用了哪些模型、各多少次」。
    花费按裸名单价估算；自建接口（custom-local）实际单价未知，仅供粗略参考。

    display_merge：与 aggregate_by_model 同样把收费版变体合并到基础模型名显示。
    本口径为账单口径（sum_trace_cost），费用直接累加各 trace 已算好的成本，
    因此合并显示不会改变任何金额——合并行的花费天然等于其中收费版部分的费用。
    """
    def _resolve_key(t):
        return merge_display_key(t.get("exec_model", ""))

    def _resolve_billing_key(t):
        # 保持「原始 exec_model」用于限免判定：合并行里若夹着收费版调用，
        # 绝不能被整体标成「限时免费」——否则报告会显示「限免」却挂着一笔真实花费。
        # 本口径费用直接累加 trace 成本，故此处只影响 timed_free 标注，不影响金额。
        return t.get("exec_model") or ""
    return aggregate_traces_by(traces, "exec_model", resolve_key_fn=_resolve_key,
                               resolve_billing_key_fn=_resolve_billing_key)

def aggregate_by_tier(traces):
    """按「档位（路由三档）」维度聚合（新增分析维度）。

    档位（快速/均衡/极致）在 trace 中只以路由别名出现，真实底层模型从不落盘，
    故只能做纯档位聚合，无法做「档位 × 真实模型」交叉表。
    档位倍率是「积分维度」，与 ¥ 刊例价正交——其单价为按积分倍率锚定的**估算值**
    （见 pricing.json 的 mode_rates），仅供横向对比，且显式标注 is_router=True。

    采用账单口径（sum_trace_cost，同 §3.1）以与概览/§3.1/§3.2 金额一致。
    非档位 trace 在 resolve_key 返回空串被跳过（档位维度独立于会话维度——
    档位 trace 的 session_id 为空，无法走 session 聚合）。
    """
    def _resolve_key(t):
        em = t.get("exec_model", "")
        if em not in TIER_ALIASES:
            return ""  # 非档位 trace 不参与档位维度
        return canonical_tier(em)  # extreme-model -> deep-model（规范键）
    return aggregate_traces_by(traces, "exec_model", resolve_key_fn=_resolve_key,
                               resolve_billing_key_fn=_resolve_key)

def aggregate_by_session(traces, sessions):
    """按会话聚合成本（计费等效 effective_cost）、实际消耗 Token、调用次数、底层模型集合。

    用于回答「哪些会话/任务最烧钱」——这是行业调研中 Agent 使用者最关心的维度（每任务/每会话成本）。
    返回 dict：rows（按 effective_cost 降序的会话明细）、buckets（成本分桶分布）。
    """
    sid_to_title = _build_sid_to_title(sessions)
    sid_to_type = {s["id"]: s.get("task_type", "其他") for s in sessions}
    known_ids = set(sid_to_title)
    agg = {}
    for t in traces:
        sid = t.get("session_id")
        if not sid:
            continue
        key = sid if sid in known_ids else ORPHAN_KEY
        a = agg.setdefault(key, {
            "session_id": key,
            "title": ORPHAN_LABEL if key == ORPHAN_KEY else sid_to_title[key],
            "task_type": "其他" if key == ORPHAN_KEY else sid_to_type.get(key, "其他"),
            "total_tokens": 0, "effective_tokens": 0, "effective_cost": 0.0,
            "calls": 0, "models": set(), "dates": set(),
        })
        a["total_tokens"] += t.get("total_tokens", 0)
        a["effective_tokens"] += t.get("effective_tokens", 0)
        a["effective_cost"] += t.get("effective_cost", 0.0)
        a["calls"] += t.get("call_count", 0)
        em = t.get("exec_model")
        if em and em != "default":
            # GLM-5.2 变体不再合并，原始裸名入集
            a["models"].add(em)
        d = t.get("date")
        if d:
            a["dates"].add(d)
    rows = []
    for sid, a in agg.items():
        date_list = sorted(a["dates"])
        rows.append({
            "session_id": ORPHAN_LABEL if sid == ORPHAN_KEY else sid,
            "title": a["title"],
            "task_type": a["task_type"],
            "total_tokens": a["total_tokens"],
            "effective_tokens": a["effective_tokens"],
            "effective_cost": round(a["effective_cost"], 2),
            "calls": a["calls"],
            "models": sorted(a["models"]),
            "first_date": date_list[0] if date_list else "",
            "last_date": date_list[-1] if date_list else "",
        })
    rows.sort(key=lambda x: x["effective_cost"], reverse=True)
    # 成本分桶分布（按 effective_cost，元）
    buckets = [
        (0, 1, "¥0–1"), (1, 5, "¥1–5"), (5, 20, "¥5–20"),
        (20, 50, "¥20–50"), (50, float("inf"), "¥50+"),
    ]
    dist = []
    for lo, hi, label in buckets:
        cnt = sum(1 for r in rows if lo <= r["effective_cost"] < hi)
        cost = sum(r["effective_cost"] for r in rows if lo <= r["effective_cost"] < hi)
        dist.append({"label": label, "count": cnt, "cost": round(cost, 2)})
    return {"rows": rows, "buckets": dist}

def _percentile(sorted_vals, p):
    """线性插值百分位（sorted_vals 已升序）。"""
    n = len(sorted_vals)
    if n == 0:
        return 0.0
    if n == 1:
        return float(sorted_vals[0])
    idx = (p / 100.0) * (n - 1)
    lo = int(idx)
    hi = min(lo + 1, n - 1)
    frac = idx - lo
    return float(sorted_vals[lo]) * (1 - frac) + float(sorted_vals[hi]) * frac

def _fmt_anom_val(v, is_cost):
    """异常数值格式化：成本用 ¥，Token 用千分位 + token。"""
    return f"¥{v:.2f}" if is_cost else f"{v:,.0f} token"

def _detect_daily_anomalies(series, is_cost):
    """通用日级阈值 / 环比异常检测。series: list of (date, value)。

    返回 (daily_anom_list, thresholds{p50,p95})；daily_anom 每项 {date, value, reasons}。
    - 超阈值：value > p95；
    - 环比突增：value >= 2× 前一日 且 value > p50。
    """
    vals = [v for _, v in series]
    if not vals:
        return [], {"p50": 0, "p95": 0}
    p50 = _percentile(sorted(vals), 50)
    p95 = _percentile(sorted(vals), 95)
    daily = []
    prev = None
    for d, v in series:
        reasons = []
        if p95 > 0 and v > p95:
            reasons.append(f"超过 p95（{_fmt_anom_val(p95, is_cost)}）")
        if prev is not None and prev > 0 and v >= 2 * prev and v > p50:
            reasons.append(f"环比突增 {(v / prev * 100 - 100):.0f}%（前一日 {_fmt_anom_val(prev, is_cost)}）")
        if reasons:
            daily.append({"date": d, "value": v, "reasons": reasons})
        prev = v
    return daily, {"p50": p50, "p95": p95}

def _detect_session_anomalies(session_stats, metric):
    """会话级异常。metric='cost' 用 effective_cost；metric='tokens' 用 calls（调用次数）。

    返回 (session_anom_list[:10], session_p95)。session_anom 每项含 session_id/title/value/
    models，tokens 口径另含 calls。
    """
    srows = session_stats.get("rows", []) if isinstance(session_stats, dict) else session_stats
    if metric == "cost":
        vals = sorted(r["effective_cost"] for r in srows) if srows else []
        sp95 = _percentile(vals, 95)
        anom = [{"session_id": r["session_id"], "title": r["title"], "value": r["effective_cost"],
                 "models": r["models"]} for r in srows if sp95 > 0 and r["effective_cost"] > sp95]
    else:
        vals = sorted(r.get("calls", 0) for r in srows) if srows else []
        sp95 = _percentile(vals, 95)
        anom = [{"session_id": r["session_id"], "title": r["title"], "value": r.get("effective_tokens", 0),
                 "calls": r.get("calls", 0), "models": r["models"]}
                for r in srows if sp95 > 0 and r.get("calls", 0) > sp95]
    anom.sort(key=lambda x: x["value"], reverse=True)
    return anom[:10], round(sp95, 2 if metric == "cost" else 1)

def detect_cost_anomalies(daily_tokens, session_stats):
    """双口径异常检测：同时以「成本」与「Token 消耗」两个**独立**口径检测异常日 / 会话。

    动机：免费 / 限时免费模型会拉低「成本」口径，可能漏报 Token 峰值（如 0726-0801 中
    7/30 的 48.81M token 峰值——当日成本极低却消耗巨大）。Token 口径始终独立检测，
    确保真实峰值被标记；成本口径仅在存在真实成本数据时启用。

    返回 dict：
      - cost_all_zero (bool)：本期实际成本是否全为 ¥0.00（幽灵 / 全免费 / 限时免费）。
      - cost_note (str)：cost_all_zero 时解释成本口径为何不适用。
      - cost (dict|None)：成本口径异常块（cost_all_zero 时为 None）。
      - token (dict)：Token 口径异常块（始终存在）。
      每个块含 daily / session 列表与 thresholds{p50, p95, session_p95}。
    """
    days = sorted(daily_tokens.keys())
    cost_series = [(d, daily_tokens[d].get("effective_cost", 0.0)) for d in days]
    token_series = [(d, daily_tokens[d].get("effective", 0)) for d in days]

    # Token 口径：始终检测（与成本独立），避免免费拉低成本口径而漏报 Token 峰值
    tok_daily, tok_thr = _detect_daily_anomalies(token_series, is_cost=False)
    tok_session, tok_sp95 = _detect_session_anomalies(session_stats, metric="tokens")
    token_block = {
        "daily": tok_daily, "session": tok_session,
        "thresholds": {**tok_thr, "session_p95": tok_sp95},
    }

    costs = [c for _, c in cost_series]
    total_cost = sum(costs)
    if total_cost <= 0 or not any(c > 0 for c in costs):
        # 成本未解析（幽灵 / 全免费 / 限时免费）→ 仅 Token 口径有效
        return {
            "cost_all_zero": True,
            "cost_note": ("本期实际成本为 ¥0.00（多为幽灵 / 空 trace，或全免费 / 限时免费模型，"
                          "见 §1 / §4 顶部提示），成本口径异常检测不适用；"
                          "以下 Token 口径异常基于实际消耗 token，峰值仍值得关注。"),
            "cost": None,
            "token": token_block,
        }

    # 成本口径：在正常成本数据上检测
    cost_daily, cost_thr = _detect_daily_anomalies(cost_series, is_cost=True)
    cost_session, cost_sp95 = _detect_session_anomalies(session_stats, metric="cost")
    cost_block = {
        "daily": cost_daily, "session": cost_session,
        "thresholds": {**cost_thr, "session_p95": cost_sp95},
    }
    return {
        "cost_all_zero": False,
        "cost_note": "",
        "cost": cost_block,
        "token": token_block,
    }

def _normalize_model_key(name):
    """归一化模型名用于替代映射匹配：去掉通道前缀、变体后缀、:free 标签。

    例：openrouter/glm-5.2-x → glm-5.2；gateway:hy3 → hy3；cohere/north-mini-code:free → north-mini-code
    """
    if not name:
        return ""
    n = name.strip().lower()
    n = n.split("/")[-1]          # 去掉通道前缀（openrouter/、gateway: 等）
    n = n.split(":")[0]           # 去掉 :free / :xxx 标签
    n = re.sub(r"-(x|flash|air|mini|pro|plus|turbo|preview|lite|ultra)$", "", n)  # 去掉变体后缀
    return n

def build_savings_insights(exec_stats, low_confidence_filter=True):
    """基于实际执行维度（model_exec_stats），找出高占比付费模型，给出更便宜替代与预计月省（估算）。

    估算口径（保守、透明）：
      - 取该模型 effective_cost 的 30% 作为「可迁移到更便宜模型的简单任务」比例；
      - 用输出单价比 price_alt/price_model 作为替代性价比；
      - 预计月省 = 该模型 effective_cost × 30% × (1 - 价格比)。
    仅当存在已知更便宜替代且单价可解析时给出建议。

    low_confidence_filter（默认 True）：是否剔除低置信度模型（L2 估算不可信）。
      在 L1 真值模式（官方真实积分 by_model）下传 False —— 官方积分已是真值，折扣 / 时段模型
      给出「迁走」建议不会误导用户多花钱。
    """
    paid = [m for m in exec_stats
            if m.get("configured") and m.get("effective_cost", 0) > 0
            and not m.get("is_router")
            # 低置信度模型（夜间免费 / 促销 / 峰谷，L2 数字不可信）
            # 不参与省钱建议，避免「建议从折扣模型迁走」反而让用户多花钱。
            # L1 真值模式（low_confidence_filter=False）下不过滤：官方积分已是真值。
            and (not low_confidence_filter or not low_confidence_reason(m["model"]))]
    total_paid = sum(m["effective_cost"] for m in paid) or 1
    items = []
    total_save = 0.0
    for m in sorted(paid, key=lambda x: x["effective_cost"], reverse=True):
        alt = _CHEAPER_ALT.get(_normalize_model_key(m["model"])) or _CHEAPER_ALT.get(m["model"])
        if not alt:
            continue
        alt_model, note = alt
        ip_a, op_a = price_of(alt_model)
        ip_m, op_m = price_of(m["model"])
        if ip_a is None or op_a is None or ip_m is None or op_m is None:
            continue
        if op_m <= 0:
            continue
        ratio = op_a / op_m
        offload_ratio = 0.30  # 假设 30% 的使用场景可迁移到更便宜模型
        save = m["effective_cost"] * offload_ratio * (1 - ratio)
        if save <= 0:
            continue
        total_save += save
        items.append({
            "model": m["model"],
            "cost": round(m["effective_cost"], 2),
            "cost_share": round(m["effective_cost"] / total_paid * 100, 1),
            "alternative": alt_model,
            "note": note,
            "estimated_monthly_save": round(save, 2),
        })
    items.sort(key=lambda x: x["estimated_monthly_save"], reverse=True)
    return {"items": items, "total_estimated_monthly_save": round(total_save, 2)}


def build_savings_insights_from_official(official_by_model, alias_map=None):
    """L1 真值模式：用官方用量导出 by_model 的**真实积分**构造省钱建议。

    与 build_savings_insights 同构，但成本基准取自官方 `credits`（真值），而非 trace 估算的
    effective_cost。官方积分已是成本真值，故复用同款算法时跳过低置信度过滤（low_confidence_filter=False）——
    折扣 / 时段模型给出「迁走」建议不会误导用户多花钱（与 L2 下的处理相反）。

    :param official_by_model: collect_official_usage() 的 by_model 列表
                              [{name, requests, credits, ...}]（按 credits 降序）
    :param alias_map: DISPLAY_MERGE 归并映射（hy3-x→hy3 等），使 §4.4 与 §3.5 对账口径一致
    :return: {"items": [...], "total_estimated_monthly_save": ...}（与 build_savings_insights 同构）
    """
    alias_map = alias_map or {}
    merged = {}
    for m in official_by_model or []:
        base = m.get("name")
        if base is None:
            continue
        # 按 alias_map 归并变体（hy4-preview-x→hy4-preview 等），与 §3.5 显示口径对齐
        key = alias_map.get(normalize_model(base), alias_map.get(base, base))
        slot = merged.setdefault(key, {"name": key, "requests": 0, "credits": 0.0})
        slot["requests"] += m.get("requests", 0)
        slot["credits"] += float(m.get("credits", 0) or 0)
    exec_stats = []
    for base, g in merged.items():
        ip, op = price_of(base)
        exec_stats.append({
            "model": base,
            # 真实积分即成本真值（L1）
            "effective_cost": g["credits"],
            "configured": ip is not None and op is not None,
            "is_router": is_router_like(base),
        })
    # 官方真值：跳过低置信度过滤（折扣 / 时段模型的建议不会误导）
    return build_savings_insights(exec_stats, low_confidence_filter=False)
