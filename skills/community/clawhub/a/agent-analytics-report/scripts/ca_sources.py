# -*- coding: utf-8 -*-
# ca_sources.py — 采集器子模块（从 collect_usage_data.py 拆分，2026-09-02）

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

__all__ = ['_extract_text_from_parts', '_find_session_jsonl', '_recover_model_info_from_spans', '_transform_cwd', 'collect_db_data', 'collect_session_outputs', 'collect_skill_usage', 'collect_traces', 'get_session_artifact_fingerprint', 'get_session_content']

def _recover_model_info_from_spans(trace_file_dict):
    """兜底：当 trace 顶层缺 modelInfo 时，从内部 generation span 的 toolOutput 还原模型与 Token。

    WorkBuddy 会发出两种 trace schema：
      1) 扁平 LLM 调用 trace：顶层带 modelInfo / sessionId / totalTokens（采集器主路径）。
      2) 'Agent workflow' trace：顶层只有 spanCount / metadata，模型与 Token 数据藏在
         每个 generation span 的 toolOutput（chat.completion JSON 字符串）里，顶层
         modelInfo 为空、totalTokens=0、sessionId 缺失。
    本函数解析后者，使这些真实工作流不被误判为「幽灵调用」而整批漏采。
    返回 None 表示无可用还原数据（仍走原 default 兜底）。
    """
    spans = (trace_file_dict or {}).get("spans", []) or []
    if not spans:
        return None
    models: list = []
    tot_in = tot_out = tot_cached = tot_calls = 0
    for s in spans:
        if s.get("name") != "generation":
            continue
        to = s.get("toolOutput")
        if not to:
            continue
        try:
            arr = json.loads(to) if isinstance(to, str) else to
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(arr, list):
            arr = arr[0] if arr else {}
        if not isinstance(arr, dict):
            continue
        m = arr.get("model")
        if m and m not in models:
            models.append(m)
        u = arr.get("usage")
        if isinstance(u, dict):
            tot_in += (u.get("prompt_tokens") or u.get("input_tokens") or 0)
            tot_out += (u.get("completion_tokens") or u.get("output_tokens") or 0)
            tot_calls += 1
            cd = (u.get("prompt_tokens_details") or {}).get("cached_tokens") or u.get("cached_tokens") or 0
            tot_cached += cd
    if not models:
        return None
    return {
        "models": models,
        "input": tot_in,
        "output": tot_out,
        "cached": tot_cached,
        "calls": max(tot_calls, 1),
        "total": tot_in + tot_out,
    }

def collect_traces(start_date, end_date, sid_to_rawmodel=None):
    """扫描 traces 目录，提取 token 消耗数据（含成本）。

    sid_to_rawmodel: {session_id: 带通道前缀的原始模型标识符}，来自 workbuddy.db 的
    sessions.model（如 "custom-local:glm-4.6v"）。用于把 trace 关联到真实 API 接口通道——
    因为 trace 的 modelInfo 会把前缀剥掉，只有 sessions.model 保留通道真相。

    成本口径统一规则（修复「概览 / 每日 / 模型章节总额互不一致」）：
      - 配置了单价的模型：输入 / 输出分别精确计价；
      - 路由别名（auto 等）：使用「本周期实际出现的已计费模型（单价>0）的均价」估算，
        与 aggregate_by_model 对 auto 行的计价完全一致 —— 故概览总额 ≡ 3.1 合计 ≡ 每日合计；
      - 未配置单价的模型：成本记 0（与模型章节「未配置」一致），不再用历史 blended 兜底，
        避免概览凭空多出一笔。
    缓存命中按 CACHE_DISCOUNT 折扣计入「实际消耗（计费等效）」。
    """
    if not TRACES_DIR.exists():
        return []
    sid_map = sid_to_rawmodel or {}

    # —— 第一遍：解析各 trace 元数据与 token，并收集本周期出现的模型以计算路由均价 ——
    parsed = []
    present_models = set()
    for pid_dir in TRACES_DIR.iterdir():
        if not pid_dir.is_dir():
            continue
        for trace_file in pid_dir.glob("trace_*.json"):
            try:
                with open(trace_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                trace = data.get("trace", {})
                trace_date = iso_to_date(trace.get("startedAt", ""))
                if not trace_date or trace_date < start_date or trace_date > end_date:
                    continue

                model_info = trace.get("modelInfo", {}) or {}
                models = model_info.get("models", []) or []
                # 兜底：扁平 trace 缺 modelInfo 时，尝试从 generation span 的 toolOutput 还原
                # （'Agent workflow' 类 trace 的真实模型/Token 在 span 内，顶层为空）。
                _recovered = None
                if not models:
                    _recovered = _recover_model_info_from_spans(data)
                    if _recovered:
                        models = _recovered["models"]
                        model_info = {
                            "models": models,
                            "totalInputTokens": _recovered["input"],
                            "totalOutputTokens": _recovered["output"],
                            "totalCachedTokens": _recovered["cached"],
                            "callCount": _recovered["calls"],
                        }
                bare_model = models[0] if models else "default"
                # token 三级回退：顶层 totalTokens → span 内 generation 还原 → modelInfo.totalTokens。
                # 顶层缺失但 modelInfo 有值时旧代码会落 0，连带把该 trace 的成本也算成 0。
                _top_tokens = _to_num(trace.get("totalTokens", 0))
                _mi_tokens = _to_num(model_info.get("totalTokens", 0)) or (
                    _to_num(model_info.get("totalInputTokens", 0))
                    + _to_num(model_info.get("totalOutputTokens", 0))
                )
                if _top_tokens:
                    _total_tokens, _token_source = _top_tokens, "trace"
                elif _recovered:
                    _total_tokens, _token_source = _recovered["total"], "span"
                elif _mi_tokens:
                    _total_tokens, _token_source = _mi_tokens, "fallback"
                else:
                    _total_tokens, _token_source = 0, "missing"
                # 通道感知：优先用 sessions.model 的原始（带前缀）标识符，否则退回 trace 裸名。
                # 但若 trace 实际执行模型带 SiliconFlow 等第三方 vendor 前缀（如 zai-org/GLM-5.2），
                # 说明 sessions.model 只是选了同名官方模型做入口，真实调用走的是外部 API；
                # 此时以 trace 实际模型为准，强制判为 custom-local，避免混入官方 gateway。
                # ⚠️ 仅当会话配置「未显式声明」custom-local: 时才触发该覆盖——否则会丢失用户
                # 显式选定的自建接口前缀，导致 custom-local:zai-org/glm-5.2 与裸 zai-org/glm-5.2
                # 在 §3.1 被误并为同一行（即「同一模型的不同接口」无法区分）。
                sid = trace.get("sessionId", "")
                raw_model = sid_map.get(sid, bare_model)
                raw_is_custom = raw_model.lower().startswith("custom-local:")
                if (not raw_is_custom) and \
                   any(bare_model.lower().startswith(p) for p in SILICONFLOW_VENDOR_PREFIXES):
                    raw_model = bare_model
                channel, base_model = parse_channel(raw_model)

                parsed.append({
                    "trace_id": trace.get("traceId", ""),
                    "pid": int(_to_num(pid_dir.name, 0)),
                    "date": trace_date,
                    "started_at": trace.get("startedAt", ""),
                    "ended_at": trace.get("endedAt", ""),
                    "duration_ms": _to_num(trace.get("duration", 0)),
                    "status": trace.get("status", "unknown"),
                    "session_id": sid,
                    "total_tokens": _total_tokens,
                    "token_source": _token_source,
                    "input_tokens": _to_num(model_info.get("totalInputTokens", 0)),
                    "output_tokens": _to_num(model_info.get("totalOutputTokens", 0)),
                    "cached_tokens": _to_num(model_info.get("totalCachedTokens", 0)),
                    "call_count": _to_num(model_info.get("callCount", 0)),
                    "models": models,
                    "model_name": base_model,   # 裸底层模型名（来自 session 配置去前缀）
                    "exec_model": bare_model,   # 裸底层模型名（来自 trace 的 modelInfo.models[0]，即 API 实际执行的真实模型）
                    "model_key": raw_model,     # 带通道前缀的原始标识符（模型维度聚合键）
                    "channel": channel,         # 接口通道
                    "raw_model": raw_model,
                })
                present_models.add(raw_model)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue

    # 路由均价：本周期出现的、已配置且单价>0 的模型（去重后等权平均），与 aggregate_by_model 一致
    # ⚠️ 排除路由类别名（auto / 三档）：它们自身无单一单价，若混入会抬高 auto 的估算均价
    paid = []
    for rm in present_models:
        if is_router_like(normalize_model(rm)):
            continue
        ip, op = price_of(rm)
        if ip is not None and op is not None and (ip > 0 or op > 0):
            paid.append((ip, op))
    router_avg_ip, router_avg_op = _router_avg_unit_price(paid)

    # —— 第二遍：统一口径计价 ——
    traces = []
    for p in parsed:
        channel = p["channel"]
        raw_model = p["raw_model"]
        input_tokens = p["input_tokens"]
        output_tokens = p["output_tokens"]
        cached_tokens = p["cached_tokens"]

        # 选定本 trace 的单价：路由别名用均价；限时免费模型按 trace 日期判 0；否则用模型真实单价
        # 把调用【时刻】（日期 + 小时 + 星期）一并传进 price_of，让「夜间免费 /
        # 峰谷双档 / 限期促销」这类按时段生效的服务端规则真正生效 —— 此前只传日期，
        # 夜间调用被当成白天计费，是低置信度模型被高估的根因。
        #
        # ⚠️ 未知模型必须记 0，不能落到 price_of 里：raw_model / exec_model 都是字面量
        # "default" 时，我们并不知道实际调了哪个模型，resolve_model 会把它映射成
        # DEFAULT_MODEL(glm-5.2) 并按其真实单价计价 —— 那是凭空编造出来的费用。
        # 判据取「两个来源都没有真名」：只要 trace.modelInfo 或 sessions.model 任一
        # 给出了真实模型名，就不算未知（此时按真实模型计价是对的）。
        _exec_nm = normalize_model(p.get("exec_model") or "")
        _raw_nm = normalize_model(p.get("raw_model") or "")
        is_unknown_model = (_exec_nm == "default" and _raw_nm == "default")
        # 档位名（fast-model / balanced-model / deep-model）是「路由档位」不是真模型名，
        # 单价来自倍率锚定估算，本身就该被标注口径；同时给出「按 hy3 刊例价」的对照金额，
        # 供报告显式呈现两种口径的差额，而不是让人以为档位单价是真实账单价。
        is_tier_name = (channel == "tier")
        pricing_model = resolve_model(p.get("exec_model") or p.get("raw_model"))
        _when = call_time_of(p.get("started_at"), p.get("date"))
        use_router_avg = (channel == "router" and router_avg_ip is not None)
        if is_unknown_model:
            ip, op = 0.0, 0.0
        elif use_router_avg:
            ip, op = router_avg_ip, router_avg_op
        elif is_timed_free(pricing_model, p.get("date")):
            ip, op = 0.0, 0.0
        else:
            ip, op = price_of(pricing_model, **_when)

        if ip is not None and op is not None:
            input_cost = (input_tokens / PER_MILLION) * ip
            output_cost = (output_tokens / PER_MILLION) * op
            cost = input_cost + output_cost
            eff_in = max(input_tokens - cached_tokens * (1 - CACHE_DISCOUNT), 0)
            eff_cost = (eff_in / PER_MILLION) * ip + (output_tokens / PER_MILLION) * op
            # GLM-5.2 夜猫子计划：按模型名定率（glm-5.2=0.79x / glm-5.2-x=0.5x）
            _mult = glm52_discount_multiplier(pricing_model)
            cost *= _mult
            eff_cost *= _mult
        else:
            input_cost = output_cost = cost = eff_cost = 0.0

        # 档位名的对照口径：同一批 token 若按 hy3 官方刊例价计，是多少。
        # 不改 total_cost（档位价仍是本采集器的口径），只把对照金额带出去给报告标注。
        alt_hy3_cost = None
        if is_tier_name and not is_unknown_model:
            _hip, _hop = price_of("hy3")
            if _hip is not None and _hop is not None:
                alt_hy3_cost = round(
                    (input_tokens / PER_MILLION) * _hip
                    + (output_tokens / PER_MILLION) * _hop, 4)

        # 计费等效 token：原始 token 减去缓存命中享受的折扣量（与 aggregate 口径一致）
        eff_tokens = effective_tokens_of(p["total_tokens"], cached_tokens)
        p.update({
            "total_cost": round(cost, 4),
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "effective_tokens": eff_tokens,
            "effective_cost": round(eff_cost, 4),
            # 时段规则（夜间免费等）同样算「本次调用免费」
            "is_free": is_timed_free(pricing_model, p.get("date"))
                       or is_scheduled_free(pricing_model, **_when),
            # 未知模型 / 档位名标记：报告据此调整文案与计价口径说明
            "is_unknown_model": is_unknown_model,
            "is_tier_name": is_tier_name,
            "alt_hy3_cost": alt_hy3_cost,
            # 失败调用单独标记：报告不把它算进「有效调用」，但成本/token 如实计入
            "is_error": p.get("status") == "error",
        })
        traces.append(p)

    traces.sort(key=lambda x: x["started_at"])
    return traces

def collect_db_data(start_date, end_date):
    """从 workbuddy.db 采集会话、自动化运行、信用消耗数据"""
    result = {"sessions": [], "automation_runs": [], "session_credits": []}
    if not DB_PATH.exists():
        return result

    # 只读打开：采集器对 workbuddy.db 只读。可写连接在 WAL 模式下会创建 / 持有
    # -wal / -shm 文件，客户端持锁时读数抛 SQLITE_BUSY。参照 adapters/qwenwork.py。
    uri = "file:" + str(DB_PATH).replace("\\", "/") + "?mode=ro"
    try:
        db = sqlite3.connect(uri, uri=True, timeout=1.0)
    except sqlite3.Error as e:
        print(f"[WARN] workbuddy.db open(read-only): {e}", file=sys.stderr)
        return result
    try:
        return _collect_db_queries(db, start_date, end_date, result)
    finally:
        db.close()


def _collect_db_queries(db, start_date, end_date, result):
    """在已打开的只读连接上跑全部查询，结果就地写入 result 后返回。

    独立成函数是为了让 collect_db_data 能用 try/finally 兜住 close()——
    否则中途异常时连接要等 GC 才释放。
    """
    db.row_factory = sqlite3.Row

    start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=TZ).timestamp() * 1000)
    end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=TZ).timestamp() * 1000) + 86400000

    # 会话
    try:
        rows = db.execute(
            "SELECT * FROM sessions WHERE created_at >= ? AND created_at < ? AND deleted_at IS NULL ORDER BY created_at",
            (start_ts, end_ts),
        ).fetchall()
        for r in rows:
            result["sessions"].append({
                "id": r["id"],
                "cwd": r["cwd"],
                "title": r["title"] or "",
                "custom_title": r["custom_title"] or "",
                "status": r["status"],
                "created_at": r["created_at"],
                "created_date": ts_to_date(r["created_at"]),
                "updated_at": r["updated_at"],
                "mode": r["mode"],
                "model": r["model"],
                "is_background_automation": bool(r["is_background_automation"]),
            })
    except (sqlite3.Error, OSError) as e:
        print(f"[WARN] sessions query: {e}", file=sys.stderr)

    # 自动化任务名称映射（用于报告展示，避免只显示任务 ID）
    # 注意：不过滤 deleted_at —— 已软删除的自动化仍可能留有历史运行记录，
    # 映射全部任务名才能保证报告里显示名称而非裸 ID。
    try:
        rows = db.execute("SELECT id, name, status, deleted_at FROM automations").fetchall()
        auto_names = {r["id"]: r["name"] for r in rows}
        # 记录每个自动化定义的状态：ACTIVE=执行中；PAUSED=已暂停；deleted_at 非空=已删除。
        # 用于报告层区分「正在执行的自动化」与「已停止的自动化」。
        auto_status = {}
        for r in rows:
            if r["deleted_at"]:
                auto_status[r["id"]] = "DELETED"
            else:
                auto_status[r["id"]] = (r["status"] or "UNKNOWN")
    except (sqlite3.Error, OSError) as e:
        print(f"[WARN] automations query: {e}", file=sys.stderr)
        auto_names = {}
        auto_status = {}

    # 自动化运行
    try:
        rows = db.execute(
            "SELECT * FROM automation_runs WHERE created_at >= ? AND created_at < ? ORDER BY created_at",
            (start_ts, end_ts),
        ).fetchall()
        for r in rows:
            result["automation_runs"].append({
                "thread_id": r["thread_id"],
                "automation_id": r["automation_id"],
                "automation_name": auto_names.get(r["automation_id"], ""),
                "status": r["status"],
                "result_success": r["result_success"],
                "auto_status": auto_status.get(r["automation_id"], "UNKNOWN"),
                "created_at": r["created_at"],
                "created_date": ts_to_date(r["created_at"]),
                "updated_at": r["updated_at"],
                "thread_title": (r["thread_title"] or "")[:500],
                "source_cwd": r["source_cwd"],
                "metadata_json": r["metadata_json"],
            })
    except (sqlite3.Error, OSError) as e:
        print(f"[WARN] automation_runs query: {e}", file=sys.stderr)

    # 会话信用消耗
    try:
        rows = db.execute(
            "SELECT * FROM session_usage WHERE updated_at >= ? AND updated_at < ? ORDER BY updated_at",
            (start_ts, end_ts),
        ).fetchall()
        for r in rows:
            credit = {}
            if r["credit_json"]:
                try:
                    credit = json.loads(r["credit_json"])
                except json.JSONDecodeError:
                    pass
            result["session_credits"].append({
                "session_id": r["session_id"],
                "used": r["used"],
                "size": r["size"],
                "updated_at": r["updated_at"],
                "updated_date": ts_to_date(r["updated_at"]),
                "credits": credit,
            })
    except (sqlite3.Error, OSError) as e:
        print(f"[WARN] session_usage query: {e}", file=sys.stderr)

    return result

def collect_skill_usage(start_date, end_date):
    """从 usage-log.json 采集技能使用数据"""
    if not USAGE_LOG_PATH.exists():
        return {"skills": {}, "active_days": []}

    with open(USAGE_LOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    skills = {}
    for sid, sdata in data.get("skills", {}).items():
        recent = [d for d in sdata.get("recentDates", []) if start_date <= d <= end_date]
        if recent or (sdata.get("lastUsedDate") and start_date <= sdata["lastUsedDate"] <= end_date):
            skills[sid] = {
                "last_used": sdata.get("lastUsedDate", ""),
                "first_seen": sdata.get("firstSeenDate", ""),
                "recent_dates_in_range": recent,
                "usage_count_in_range": len(recent),
            }

    active_days = [d for d in data.get("activeDays", []) if start_date <= d <= end_date]
    return {"skills": skills, "active_days": active_days}

def collect_session_outputs(start_date, end_date):
    """扫描 WorkBuddy 会话目录，提取产出文件和记忆日志"""
    outputs = []
    memory_logs = {}

    if not WORKBUDDY_SESSIONS.exists():
        return outputs, memory_logs

    # 从目录名解析日期
    dir_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})")

    for session_dir in WORKBUDDY_SESSIONS.iterdir():
        if not session_dir.is_dir():
            continue
        m = dir_pattern.match(session_dir.name)
        if not m:
            continue
        dir_date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        if dir_date < start_date or dir_date > end_date:
            continue

        # 产出文件（非隐藏文件）
        for item in session_dir.iterdir():
            if item.is_file() and not item.name.startswith("."):
                outputs.append({
                    "file_name": item.name,
                    "file_path": str(item),
                    "date": dir_date,
                    "size_bytes": item.stat().st_size,
                    "extension": item.suffix,
                })

        # 记忆日志
        mem_dir = session_dir / ".workbuddy" / "memory"
        if mem_dir.exists():
            for mem_file in mem_dir.glob("*.md"):
                try:
                    log_date = mem_file.stem  # YYYY-MM-DD
                    # ⚠️ 必须按记忆文件自身日期过滤：会话目录名日期 ≠ 记忆文件日期，
                    # 一个会话目录里可能躺着跨月的记忆。不加此过滤会把时间窗外的
                    # 个人记忆明文读进本次采集（越权），口径与上方 dir_date 一致。
                    if log_date < start_date or log_date > end_date:
                        continue
                    # 只落元信息，不读正文：下游（collect_usage_data / 报告渲染）
                    # 只需要 file + session_dir，content 在结果组装时就被剥掉了。
                    # 读正文等于把窗口内的个人记忆明文无谓地搬进内存。
                    memory_logs.setdefault(log_date, []).append({
                        "file": str(mem_file),
                        "has_content": True,
                        "content_chars": mem_file.stat().st_size,
                        "session_dir": session_dir.name,
                    })
                except (OSError, IOError):
                    continue

    outputs.sort(key=lambda x: x["date"])
    return outputs, memory_logs

def _transform_cwd(cwd):
    """cwd 路径 → projects 目录名（与 WorkBuddy 对话存档命名一致）"""
    return "c-" + cwd.replace(":", "").lower().replace("\\", "-").replace("/", "-")

def _find_session_jsonl(session_id, cwd):
    """根据 session id 与 cwd 定位对话 transcript JSONL 文件，失败返回 None"""
    # 1. 直接路径：projects/<cwd哈希>/<id>.jsonl（近期 session id 即 UUID）
    cand = PROJECTS_DIR / _transform_cwd(cwd) / f"{session_id}.jsonl"
    if cand.exists():
        return cand
    # 2. 旧体系：numeric id → SESSIONS_DIR/<id>.json 取 UUID 再定位
    sj = SESSIONS_DIR / f"{session_id}.json"
    if sj.exists():
        try:
            uuid = json.loads(sj.read_text(encoding="utf-8")).get("sessionId")
            if uuid:
                cand = PROJECTS_DIR / _transform_cwd(cwd) / f"{uuid}.jsonl"
                if cand.exists():
                    return cand
        except (json.JSONDecodeError, OSError):
            pass
    # 3. 兜底：仅探测 PROJECTS_DIR 下已知的一级子目录（c-<cwd哈希>），不递归整棵树
    #    ——避免 glob("**/...") 跨目录枚举无关会话工件（隐私面收敛，SDI-1）。
    #    只对一级子目录做 exact-name 匹配，找到即返回，找不到返回 None（不做更深递归）。
    if PROJECTS_DIR.is_dir():
        for sub in sorted(PROJECTS_DIR.iterdir()):
            if not sub.is_dir():
                continue
            cand = sub / f"{session_id}.jsonl"
            if cand.exists():
                return cand
    return None

def _extract_text_from_parts(raw):
    """从 content / rawContent 列表里抽取文本片段。

    兼容多种结构：
      - message.content: [{type: input_text/output_text, text: ...}]
      - reasoning.rawContent: [{type: reasoning_text, text: ...}]
      - 亦兼容裸字符串或 {content: ...} 形式
    """
    out = []
    if isinstance(raw, str):
        out.append(raw)
    elif isinstance(raw, list):
        for p in raw:
            if isinstance(p, dict):
                txt = p.get("text") or p.get("content") or ""
                if txt:
                    out.append(txt)
            elif isinstance(p, str):
                out.append(p)
    return out

def get_session_artifact_fingerprint(session_id, cwd):
    """抽取会话的「生成物指纹」，含**已删除**的生成物。

    生成物来源（即使产物文件已物理删除，以下记录在 transcript 里仍保留）：
      1. function_call 记录里的 ImageGen / VideoGen 工具调用 —— 确定性内容生成证据；
      2. file-history-snapshot.trackedFileBackups 的键名 —— 编辑器曾跟踪过的文件名，
         文件删除后键名仍保留，是「已删除生成物」的最佳来源（含 .png/.mp4/.html 等）。

    返回形如 "[artifacts] imagegen videogen file.png file.mp4 ..." 的归一词串，
    供 classify_task 作为对话内容的补充信号；无任何生成物时为 ""。
    """
    jl = _find_session_jsonl(session_id, cwd)
    if not jl:
        return ""
    gen_tools, media_files = [], []
    try:
        for ln in jl.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                m = json.loads(ln)
            except json.JSONDecodeError:
                continue
            if m.get("type") == "function_call":
                blob = json.dumps(m, ensure_ascii=False)
                if "ImageGen" in blob:
                    gen_tools.append("imagegen")
                if "VideoGen" in blob:
                    gen_tools.append("videogen")
            elif m.get("type") == "file-history-snapshot":
                tb = (m.get("snapshot") or {}).get("trackedFileBackups") or {}
                for fn in tb.keys():
                    if Path(fn).suffix.lower() in MEDIA_EXTS:
                        media_files.append(Path(fn).name.lower())
    except (OSError, IOError):
        pass
    if not gen_tools and not media_files:
        return ""
    parts = ["[artifacts]"]
    parts += gen_tools
    for fn in media_files[:30]:           # 限制长度，避免超大会话拖慢分类
        parts.append(fn)
    return " ".join(parts)

def get_session_content(session_id, cwd, max_chars=3000):
    """抽取会话对话文本（user/assistant 消息 + reasoning），截断以提速。

    对话内容存储于 ~/.workbuddy/projects/<cwd哈希>/<sessionId>.jsonl，
    每行一条记录：
      - type=message：role=user/assistant，content 为文本片段列表
      - type=reasoning：助手思考，真实文本在 rawContent（content 常为 []）

    关键：先把每段文本里的 <system-reminder> 注入块剥离，再计入长度并判断是否
    截断——否则首条 user 消息携带的巨型 system-reminder 会让 total 瞬间超额、
    循环在抽到任何有效内容前就 break，导致只剩裸 user_query。
    """
    jl = _find_session_jsonl(session_id, cwd)
    if not jl:
        return ""
    parts, total = [], 0
    try:
        for ln in jl.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                m = json.loads(ln)
            except json.JSONDecodeError:
                continue
            t = m.get("type")
            if t == "message":
                raw = m.get("content")
            elif t == "reasoning":
                # 真实思考文本在 rawContent，其次 content/text/reasoning
                raw = m.get("rawContent") or m.get("content") or m.get("text") or m.get("reasoning")
            else:
                continue
            for txt in _extract_text_from_parts(raw):
                # 先剥离系统注入块，再计入长度，避免污染分类与误触发截断
                txt = SYSTEM_REMINDER_RE.sub(" ", txt)
                if not txt.strip():
                    continue
                parts.append(txt)
                total += len(txt)
                if total >= max_chars:
                    break
            if total >= max_chars:
                break
    except (OSError, IOError):
        pass
    return " ".join(parts)[:max_chars]
