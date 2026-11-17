# -*- coding: utf-8 -*-
"""adapters/codex.py — OpenAI Codex CLI 数据源适配器

把 Codex CLI 的会话 rollout 记录（~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl）
映射到 agent-analytics-report 的统一 trace / session schema，复用同一套聚合与
报告渲染逻辑，无需 WorkBuddy 环境。

Codex CLI JSONL 行格式（每行一个事件，append-only，按日期分目录）：
  {"type":"session_meta","timestamp":"...","payload":{"id":"...","cwd":"...",
   "cli_version":"0.134.0","model_provider":"openai","model":"gpt-5-codex",
   "source":"cli"}}                       # 首行：会话元数据
  {"type":"turn.started", ...}
  {"type":"turn.completed","timestamp":"...","usage":{            # ⭐ token 在此
     "input_tokens":24763,"cached_input_tokens":24448,
     "output_tokens":122,"reasoning_output_tokens":512}}
  {"type":"response_item","payload":{"type":"message","role":"user",
     "content":[{"type":"input_text","text":"帮我写个快排"}]}}
  {"type":"item.completed","item":{"type":"command_execution",...}}

关键约定（与 claude_code.py 对齐）：
  - token 以「每轮」为单位，集中在 turn.completed 事件的 usage 里（Claude Code 是在
    assistant 消息里，两者位置不同）。本适配器每条 turn.completed → 1 条 trace。
  - 成本口径与 WorkBuddy / Claude Code 一致：成本 = 输入×单价 + 输出×单价；缓存命中
    按 CACHE_DISCOUNT 折扣计入「计费等效」（effective_tokens / effective_cost）。
  - 模型名从 session_meta.payload.model / turn_context.payload.model / response_item
    消息的 model 字段抓取（不同版本位置不一），按文件扫描顺序取最近一次已知值。
  - 跨版本兼容：事件类型字段可能是 `type`（新）或 `item_type`（旧）；reasoning token
    字段可能是 `reasoning_output_tokens`（v0.131+）或 `reasoning_tokens`（旧）。

⚠️ MVP 限制：
  - reasoninig token 成本未单独计入（与 Claude Code 一致：total_cost 仅按
    input_tokens + output_tokens 计价，reasoning_output_tokens 仅记为透明字段），
    reasoning 重的模型实际账单可能略高于本报告估算。
  - duration_ms 恒为 0（rollout 无可靠端到端耗时字段）。
  - 子 agent（source=subagent）平级混在同一日期目录，不单独拆目录；其 token 已含在
    各自的 turn.completed 里，按会话独立统计。
"""

import hashlib
import json
import os
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS = _HERE.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ca_core import (
    CACHE_DISCOUNT,
    call_time_of,
    effective_tokens_of,
    is_scheduled_free,
    is_timed_free,
    iso_to_date,
    normalize_model,
    price_of,
    resolve_model,
)
from ca_sessions import classify_task

__all__ = [
    "CODEX_CHANNEL",
    "collect_codex",
    "collect_codex_sessions",
    "collect_codex_traces",
    "resolve_codex_sessions_root",
]

# 本适配器产出的 trace 统一走此通道（parse_channel 已识别，price_of 走 OpenAI 刊例价）
CODEX_CHANNEL = "codex"

_UNKNOWN_MODEL = "codex-default"


_REDACT_RE = re.compile(r"(sk-[A-Za-z0-9]{12,}|https?://\S+|[\w.+-]+@[\w-]+\.[\w.-]+)")


def _minimize_dialogue(parts, limit=120):
    """把会话对话正文压成短样本（任务分类输入），不保留完整消息体，并对明显凭据脱敏。"""
    text = " ".join(p for p in parts if p)[:limit]
    return _REDACT_RE.sub("[REDACTED]", text)


def resolve_codex_sessions_root():
    """定位 Codex CLI sessions 根目录（其下为 YYYY/MM/DD/rollout-*.jsonl）。

    优先级：
      1. 环境变量 CODEX_HOME —— 直接指向 Codex 主目录，取其下 sessions/；
      2. 平台默认候选（取第一个存在的）：
         - Windows: %APPDATA%/codex/sessions、%USERPROFILE%/.codex/sessions
         - macOS / Linux: ~/.codex/sessions
    返回 Path；目录可能不存在（本机未装 Codex / 无会话），调用方负责判空。
    """
    env = os.environ.get("CODEX_HOME")
    if env:
        return Path(env).expanduser() / "sessions"
    home = Path.home()
    candidates = []
    if os.name == "nt":  # Windows
        appdata = Path(os.environ.get("APPDATA", str(home / "AppData" / "Roaming")))
        candidates.append(appdata / "codex" / "sessions")
        candidates.append(home / ".codex" / "sessions")
    else:
        candidates.append(home / ".codex" / "sessions")
    for c in candidates:
        if c.exists():
            return c
    # 都不存在时返回首要默认路径（调用方据此判断「无数据」）
    return candidates[0]


def _iter_jsonl_files(sessions_root):
    """递归遍历 sessions 根下所有 *.jsonl（含嵌套 YYYY/MM/DD 与 archived_sessions）。"""
    if not sessions_root or not sessions_root.exists():
        return
    for f in sessions_root.rglob("*.jsonl"):
        yield f


def _extract_text(content):
    """从 message.content（str 或 content block 列表）抽取纯文本，供任务分类使用。"""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for blk in content:
        if isinstance(blk, dict):
            txt = blk.get("text") or blk.get("content") or blk.get("input_text") \
                or blk.get("output_text") or ""
            if txt:
                parts.append(txt)
        elif isinstance(blk, str):
            parts.append(blk)
    return " ".join(parts)


def _stable_pid(seed):
    """从字符串生成稳定非负 int（模拟 WorkBuddy 的 pid_dir.name → int）。"""
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def _read_jsonl_lines(path):
    """逐行读取 JSONL，容错跳过损坏行（与 collect_traces 的容错一致）。"""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, IOError):
        return
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            yield json.loads(ln)
        except (json.JSONDecodeError, TypeError):
            continue


def _to_int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _ts_to_ms(iso_str):
    """ISO 8601 → Unix 毫秒时间戳（失败返回 0）。"""
    if not iso_str:
        return 0
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000)
    except (ValueError, TypeError):
        return 0


def _get(obj, key):
    """取字段：优先顶层，其次 payload 内（不同版本 schema 位置不一）。"""
    if not isinstance(obj, dict):
        return None
    if key in obj and obj[key] is not None:
        return obj[key]
    payload = obj.get("payload")
    if isinstance(payload, dict) and key in payload and payload[key] is not None:
        return payload[key]
    return None


def _parse_codex_file(path, start_date, end_date):
    """解析单个 Codex rollout JSONL，产出 (traces, session_meta)。

    traces: 本文件内在日期范围内的 turn.completed 用量记录（统一 schema）。
    session_meta: 该会话的元信息（id / cwd / title / model / 时间窗 / 对话文本）。
    """
    session_id = path.stem
    traces = []
    cwd = ""
    first_user_text = ""
    first_model = ""
    created_ms = None
    updated_ms = None
    dialogue_parts = []
    current_model = ""
    # 会话级累计基线：用于 total_token_usage 增量去重，避免把累计快照当逐轮重复计入
    _cum = {}

    for obj in _read_jsonl_lines(path):
        if not isinstance(obj, dict):
            continue
        # 兼容旧版本 item_type 字段
        typ = obj.get("type") or obj.get("item_type") or ""
        ts = obj.get("timestamp") or (obj.get("payload") or {}).get("timestamp") or ""
        ms = _ts_to_ms(ts)
        if created_ms is None or (ms and ms < created_ms):
            created_ms = ms
        if updated_ms is None or (ms and ms > updated_ms):
            updated_ms = ms

        # 会话元数据（首行）
        if typ == "session_meta":
            meta_payload = obj.get("payload") or {}
            sid = meta_payload.get("id") or session_id
            session_id = sid
            c = meta_payload.get("cwd") or ""
            if c:
                cwd = c
            m = meta_payload.get("model") or ""
            if m and not first_model:
                first_model = m
                current_model = m
            continue

        # 逐轮配置（含模型）
        if typ == "turn_context":
            m = _get(obj, "model") or ""
            if m:
                current_model = m
                if not first_model:
                    first_model = m
            continue

        # 对话内容（user / assistant 文本）→ 任务分类输入 + title
        if typ in ("response_item", "message", "event_msg"):
            p = obj.get("payload") or {}
            ptype = p.get("type") or ""
            # event_msg 的子类型在 payload.type（user_message / agent_message / token_count）
            if ptype in ("user_message", "message") and p.get("role") == "user":
                txt = _extract_text(p.get("content") or p.get("message"))
                if txt and not first_user_text:
                    first_user_text = txt
                dialogue_parts.append(txt)
            elif ptype == "agent_message" or (p.get("role") == "assistant"):
                # response_item 的 assistant 消息可能带 model 字段（部分版本）
                m = p.get("model") or ""
                if m:
                    current_model = m
                    if not first_model:
                        first_model = m
                dialogue_parts.append(_extract_text(p.get("content")))
            elif ptype == "token_count":
                # 累计 token 事件（部分版本用它而非 turn.completed）
                info = p.get("info") or {}
                last = info.get("last_token_usage") or {}
                total = info.get("total_token_usage") or {}
                if last:
                    # 逐轮语义（last_token_usage）：直接发，不重复计
                    _emit_trace(traces, session_id, cwd, ts, current_model or first_model,
                                last, start_date, end_date)
                elif total:
                    # 累计快照（total_token_usage）：按会话基线算增量，避免把整段历史当一轮重复计入
                    base = _cum.setdefault(session_id, {})
                    prev_in = _to_int(base.get("input_tokens"))
                    prev_out = _to_int(base.get("output_tokens"))
                    cur_in = _to_int(total.get("input_tokens"))
                    cur_out = _to_int(total.get("output_tokens"))
                    base.clear()
                    base.update(total)
                    d_in = cur_in - prev_in
                    d_out = cur_out - prev_out
                    if d_in < 0 or d_out < 0:
                        # 计数重置：基线已更新，本快照不再计入，避免把历史重复算入窗口
                        continue
                    if d_in > 0 or d_out > 0:
                        _emit_trace(traces, session_id, cwd, ts, current_model or first_model,
                                    {"input_tokens": d_in, "output_tokens": d_out,
                                     "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
                                    start_date, end_date)

        # 逐轮完成事件（⭐ 主用量来源）
        if typ == "turn.completed":
            usage = _get(obj, "usage") or {}
            if not usage:
                continue
            _emit_trace(traces, session_id, cwd, ts, current_model or first_model,
                        usage, start_date, end_date)

    title = (first_user_text[:60].strip() if first_user_text
             else (Path(cwd).name if cwd else session_id))
    session_meta = {
        "id": session_id,
        "cwd": cwd,
        "title": title,
        "custom_title": "",
        "status": "completed",
        "created_at": created_ms or 0,
        "created_date": iso_to_date(_ms_to_iso(created_ms)),
        "updated_at": updated_ms or 0,
        "mode": CODEX_CHANNEL,
        "model": f"{CODEX_CHANNEL}:{first_model}" if first_model else CODEX_CHANNEL,
        "is_background_automation": False,
        "version": _UNKNOWN_MODEL,
        "_dialogue_text": _minimize_dialogue(dialogue_parts),
    }
    return traces, session_meta


def _emit_trace(traces, session_id, cwd, ts, model, usage, start_date, end_date):
    """从单轮 usage 产出一条统一 schema trace（日期窗口内才计入）。"""
    date = iso_to_date(ts)
    if not date or date < start_date or date > end_date:
        return
    in_tok = _to_int(usage.get("input_tokens"))
    out_tok = _to_int(usage.get("output_tokens"))
    cache_read = _to_int(usage.get("cached_input_tokens"))
    if cache_read == 0:
        cache_read = _to_int(usage.get("cache_read_input_tokens"))
    reasoning = _to_int(usage.get("reasoning_output_tokens"))
    if reasoning == 0:
        reasoning = _to_int(usage.get("reasoning_tokens"))
    # 已计费的输出 = output_tokens（reasoning token 成本记透明字段，MVP 不单独计价）
    # 透明口径：raw total 含缓存读，便于账单对账；eff_tokens 仍按下方原口径，不改变费用数值
    total = in_tok + out_tok + cache_read
    bare = normalize_model(model) if model else _UNKNOWN_MODEL
    model_key = f"{CODEX_CHANNEL}:{bare}"
    pricing_model = resolve_model(bare)
    # v1.7.1：传调用时刻（日期 + 小时 + 星期），让时段定价规则（夜间免费 / 峰谷 / 促销）生效
    _when = call_time_of(ts, date)
    ip, op = price_of(model_key, **_when)
    if ip is not None and op is not None:
        input_cost = (in_tok / 1_000_000) * ip
        output_cost = (out_tok / 1_000_000) * op
        cost = input_cost + output_cost
        eff_in = max(in_tok - cache_read * (1 - CACHE_DISCOUNT), 0)
        eff_cost = (eff_in / 1_000_000) * ip + (out_tok / 1_000_000) * op
    else:
        input_cost = output_cost = cost = eff_cost = 0.0
    eff_tokens = effective_tokens_of(in_tok + out_tok, cache_read)
    is_free = is_timed_free(pricing_model, date) or is_scheduled_free(pricing_model, **_when)
    traces.append({
        "trace_id": f"{session_id}:{ts}:{len(traces)}",
        "pid": _stable_pid(cwd or session_id),
        "date": date,
        "started_at": ts,
        "ended_at": ts,
        "duration_ms": 0,
        "status": "success",
        "session_id": session_id,
        "total_tokens": total,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "cached_tokens": cache_read,
        "call_count": 1,
        "models": [bare],
        "model_name": bare,
        "exec_model": bare,
        "model_key": model_key,
        "channel": CODEX_CHANNEL,
        "raw_model": model_key,
        "total_cost": round(cost, 4),
        "input_cost": round(input_cost, 4),
        "output_cost": round(output_cost, 4),
        "effective_tokens": eff_tokens,
        "effective_cost": round(eff_cost, 4),
        "is_free": is_free,
        # 透明字段：保留原始 reasoning 拆分，便于后续做更精细的 OpenAI 推理计价
        "_reasoning_output_tokens": reasoning,
    })


def _ms_to_iso(ms):
    """Unix 毫秒 → ISO 8601（用于 created_date 兜底）。"""
    if not ms:
        return ""
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()
    except (ValueError, TypeError, OSError):
        return ""


def collect_codex_traces(start_date, end_date, sessions_root=None):
    """读取 Codex 会话历史，返回统一 schema 的 trace 列表（含成本字段）。"""
    root = Path(sessions_root) if sessions_root else resolve_codex_sessions_root()
    traces = []
    for f in _iter_jsonl_files(root):
        file_traces, _ = _parse_codex_file(f, start_date, end_date)
        traces.extend(file_traces)
    traces.sort(key=lambda x: x.get("started_at") or "")
    return traces


def _session_in_window(meta, file_traces, start_date, end_date):
    """隐私边界：仅纳入「created_date 落在窗口内」或「窗口内有 trace」的会话。

    越窗（或日期未知且无窗内活动）的会话元数据不进报告，防止越权收集。
    合并 collector（collect_codex）与分表 collector（collect_codex_sessions）
    共用此判断，避免两者隐私口径漂移（SDI-4 修复点）。
    """
    cd = meta.get("created_date") or ""
    return (bool(cd) and start_date <= cd <= end_date) or bool(file_traces)


def collect_codex_sessions(start_date, end_date, sessions_root=None):
    """读取 Codex 会话历史，返回合成 db_data（sessions 已预分类 task_type）。"""
    root = Path(sessions_root) if sessions_root else resolve_codex_sessions_root()
    sessions = []
    for f in _iter_jsonl_files(root):
        file_traces, meta = _parse_codex_file(f, start_date, end_date)
        # 契约：仅纳入「created_date 落在窗口内」或「窗口内有 trace」的会话；
        # 越窗（或日期未知且无窗内活动）的会话元数据不进报告，防止越权收集。
        if not _session_in_window(meta, file_traces, start_date, end_date):
            continue
        text = meta.get("_dialogue_text", "")
        meta["task_type"] = classify_task(text)
        meta.pop("_dialogue_text", None)
        sessions.append(meta)
    return {
        "sessions": sessions,
        "automation_runs": [],
        "session_credits": [],
    }


def collect_codex(start_date, end_date, sessions_root=None):
    """一次性返回 (traces, db_data)，供 collect_usage_data.py --source codex 直接使用。

    隐私边界与 collect_codex_sessions 完全一致：越窗会话（无窗内 trace 且
    created_date 不在窗口内）整体跳过，不进 traces 也不进 sessions 元数据
    （SDI-1 / SDI-4 修复点：合并 collector 原先漏做窗口过滤）。
    """
    root = Path(sessions_root) if sessions_root else resolve_codex_sessions_root()
    traces = []
    sessions = []
    for f in _iter_jsonl_files(root):
        file_traces, meta = _parse_codex_file(f, start_date, end_date)
        if not _session_in_window(meta, file_traces, start_date, end_date):
            continue
        traces.extend(file_traces)
        text = meta.get("_dialogue_text", "")
        meta["task_type"] = classify_task(text)
        meta.pop("_dialogue_text", None)
        sessions.append(meta)
    traces.sort(key=lambda x: x.get("started_at") or "")
    return traces, {
        "sessions": sessions,
        "automation_runs": [],
        "session_credits": [],
    }
