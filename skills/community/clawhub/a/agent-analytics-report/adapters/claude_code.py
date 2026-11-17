# -*- coding: utf-8 -*-
"""adapters/claude_code.py — Claude Code 数据源适配器 (P2-1 MVP)

把 Claude Code 的会话历史（~/.claude/projects/ 下的 JSONL）映射到
agent-analytics-report 的统一 trace / session schema，使其能复用同一套聚合与
报告渲染逻辑，无需任何 WorkBuddy 专属依赖。

Claude Code JSONL 行格式（每行一个事件，append-only）：
  {
    "type": "assistant",
    "timestamp": "2026-01-14T04:51:53.996Z",
    "uuid": "msg_01ABC...",
    "sessionId": "uuid",
    "cwd": "/path/to/project",
    "version": "1.0.23",
    "message": {
      "role": "assistant",
      "model": "claude-sonnet-4-20250514",
      "content": [...],
      "usage": {
        "input_tokens": 12847,
        "output_tokens": 1523,
        "cache_creation_input_tokens": 8192,
        "cache_read_input_tokens": 41000
      }
    }
  }

关键约定：
  - 仅 assistant 消息带 usage（API 调用发生时才消耗 token）；user / system 行无 token 计数。
  - cwd 字段是权威项目路径；目录名（encoded-path）只是其无损编码，不作唯一来源。
  - 成本口径与 collect_traces 完全一致：成本 = 输入×单价 + 输出×单价；计费等效 token
    按 CACHE_DISCOUNT 折扣计入（见 effective_tokens_of）。Claude 缓存（cache_read /
    cache_creation）按折扣计入「计费等效」，但成本不直接打折（与 WorkBuddy 现有口径一致）。
"""

import hashlib
import json
import os
import re
import sys
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
    "CLAUDE_CHANNEL",
    "collect_claude_code",
    "collect_claude_code_sessions",
    "collect_claude_code_traces",
    "resolve_claude_projects_root",
]

# 本适配器产出的 trace 统一走此通道（parse_channel 已识别，price_of 走 gateway 计价）
CLAUDE_CHANNEL = "claude-code"

# Claude Code 官方 CLI 版本字段缺失时回退值
_UNKNOWN_VERSION = "unknown"


_REDACT_RE = re.compile(r"(sk-[A-Za-z0-9]{12,}|https?://\S+|[\w.+-]+@[\w-]+\.[\w.-]+)")


def _minimize_dialogue(parts, limit=120):
    """把会话对话正文压成短样本（任务分类输入），不保留完整消息体，并对明显凭据脱敏。"""
    text = " ".join(p for p in parts if p)[:limit]
    return _REDACT_RE.sub("[REDACTED]", text)


def resolve_claude_projects_root():
    """定位 Claude Code projects 根目录。

    优先级：
      1. 环境变量 CLAUDE_PROJECTS_DIR —— 测试 / 自定义覆盖，直接指向 projects/ 目录；
      2. 环境变量 CLAUDE_CONFIG_DIR —— Claude Code 官方配置根覆盖（其下含 projects/，
         可为逗号分隔的多个根，取第一个含 projects/ 者）；
      3. 平台默认：
         - Windows: %APPDATA%/Claude/projects
         - macOS / Linux: ~/.claude/projects
         - 另支持 ~/Library/Application Support/Claude/local-agent-mode-sessions 等
           Desktop agent 模式树（walk 时若发现 projects/ 子目录一并扫描）。
    返回 Path；目录可能不存在（本机未装 Claude Code），调用方负责判空。
    """
    env = os.environ.get("CLAUDE_PROJECTS_DIR")
    if env:
        return Path(env).expanduser()
    cfg = os.environ.get("CLAUDE_CONFIG_DIR")
    if cfg:
        for root in cfg.split(","):
            p = Path(root.strip()).expanduser() / "projects"
            if p.exists():
                return p
        return Path(cfg.split(",")[0].strip()).expanduser() / "projects"
    home = Path.home()
    if os.name == "nt":  # Windows
        appdata = Path(os.environ.get("APPDATA", str(home / "AppData" / "Roaming")))
        return appdata / "Claude" / "projects"
    # macOS / Linux 默认
    return home / ".claude" / "projects"


def _session_in_window(meta, file_traces, start_date, end_date):
    """隐私边界：仅纳入「created_date 落在窗口内」或「窗口内有 trace」的会话。

    越窗（或日期未知且无窗内活动）的会话元数据不进报告，防止越权收集。
    合并 collector（collect_claude_code）与分表 collector（collect_claude_code_sessions）
    共用此判断，避免两者隐私口径漂移（SDI-4 修复点）。
    """
    cd = meta.get("created_date") or ""
    return (bool(cd) and start_date <= cd <= end_date) or bool(file_traces)


def _iter_jsonl_files(projects_root):
    """遍历 projects 根下「直接一级子目录」中的 *.jsonl（仅一层，不递归更深）。

    隐私边界（与 SKILL.md 硬约束一致）：只枚举 projects_root 的一级子目录
    （即 c-<cwd哈希> 这类工程目录），在其内找 *.jsonl；**不**递归整棵树，
    也**不**搜索任意层级的 'projects' 子目录。Desktop agent 模式若为独立根目录，
    应由 CLAUDE_PROJECTS_DIR / CLAUDE_CONFIG_DIR 显式指向，而非靠盲目递归发现
    （SDI-1 修复点：移除原先的 rglob("projects") 二级递归）。
    """
    if not projects_root or not projects_root.exists():
        return
    if projects_root.is_dir():
        for sub in sorted(projects_root.iterdir()):
            if not sub.is_dir():
                continue
            for f in sub.glob("*.jsonl"):
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
            # 兼容 text / thinking / input_text / output_text 等块
            txt = blk.get("text") or blk.get("content") or ""
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


def _parse_claude_file(path, start_date, end_date):
    """解析单个 Claude Code 会话 JSONL，产出 (traces, session_meta)。

    traces: 本文件内在日期范围内的 assistant 用量记录（统一 schema，未含成本后的完整字段）。
    session_meta: 该会话的元信息（id / cwd / title / model / 时间窗 / 对话文本）。
    文件整体不在窗口内（无 assistant 行落窗）时 traces 仍可能为空列表，session_meta 仍返回。
    """
    session_id = path.stem
    traces = []
    cwd = ""
    first_user_text = ""
    first_model = ""
    created_ms = None
    updated_ms = None
    dialogue_parts = []

    for obj in _read_jsonl_lines(path):
        if not isinstance(obj, dict):
            continue
        typ = obj.get("type")
        ts = obj.get("timestamp", "")
        ms = _ts_to_ms(ts)
        if created_ms is None or (ms and ms < created_ms):
            created_ms = ms
        if updated_ms is None or (ms and ms > updated_ms):
            updated_ms = ms

        c = obj.get("cwd")
        if c:
            cwd = c

        if typ == "user":
            msg = obj.get("message") or {}
            txt = _extract_text(msg.get("content"))
            if txt and not first_user_text:
                first_user_text = txt
            dialogue_parts.append(txt)
        elif typ == "assistant":
            msg = obj.get("message") or {}
            usage = msg.get("usage") or {}
            if not usage:
                # 无 usage 的 assistant 行（纯 thinking 或工具结果回显）不计费
                continue
            model = msg.get("model") or "claude-default"
            if not first_model:
                first_model = model
            dialogue_parts.append(_extract_text(msg.get("content")))
            date = iso_to_date(ts)
            if not date or date < start_date or date > end_date:
                continue
            in_tok = _to_int(usage.get("input_tokens"))
            out_tok = _to_int(usage.get("output_tokens"))
            cache_read = _to_int(usage.get("cache_read_input_tokens"))
            cache_creation = _to_int(usage.get("cache_creation_input_tokens"))
            # cached_tokens：实际命中缓存读取的 token（享受折扣的部分）
            cached = cache_read
            # 透明口径：raw total 含全部 token（输入 + 输出 + 缓存读/写），
            # 便于「账单对账」；计费等效 eff_tokens/eff_cost 仍按下方原口径，不改变费用数值
            total = in_tok + out_tok + cache_read + cache_creation
            bare = normalize_model(model)
            model_key = f"{CLAUDE_CHANNEL}:{bare}"
            pricing_model = resolve_model(bare)
            # v1.7.1：传调用时刻（日期 + 小时 + 星期），让时段定价规则（夜间免费 / 峰谷 / 促销）生效
            _when = call_time_of(ts, date)
            ip, op = price_of(pricing_model, **_when)
            if ip is not None and op is not None:
                input_cost = (in_tok / 1_000_000) * ip
                output_cost = (out_tok / 1_000_000) * op
                cost = input_cost + output_cost
                eff_in = max(in_tok - cached * (1 - CACHE_DISCOUNT), 0)
                eff_cost = (eff_in / 1_000_000) * ip + (out_tok / 1_000_000) * op
            else:
                input_cost = output_cost = cost = eff_cost = 0.0
            eff_tokens = effective_tokens_of(in_tok + out_tok, cached)
            is_free = is_timed_free(pricing_model, date) or is_scheduled_free(pricing_model, **_when)
            traces.append({
                "trace_id": f"{session_id}:{obj.get('uuid', len(traces))}",
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
                "cached_tokens": cached,
                "call_count": 1,
                "models": [bare],
                "model_name": bare,
                "exec_model": bare,
                "model_key": model_key,
                "channel": CLAUDE_CHANNEL,
                "raw_model": model_key,
                "total_cost": round(cost, 4),
                "input_cost": round(input_cost, 4),
                "output_cost": round(output_cost, 4),
                "effective_tokens": eff_tokens,
                "effective_cost": round(eff_cost, 4),
                "is_free": is_free,
                # 透明字段：保留原始缓存拆分，便于后续做更精细的 Claude 缓存计价
                "_cache_creation_input_tokens": cache_creation,
            })

    title = (first_user_text[:60].strip() if first_user_text
             else (Path(cwd).name if cwd else session_id))
    session_meta = {
        "id": session_id,
        "cwd": cwd,
        "title": title,
        "custom_title": "",
        "status": "completed",
        "created_at": created_ms or 0,
        "created_date": iso_to_date(_ts_to_ms_to_iso(created_ms)),
        "updated_at": updated_ms or 0,
        "mode": CLAUDE_CHANNEL,
        "model": f"{CLAUDE_CHANNEL}:{first_model}" if first_model else CLAUDE_CHANNEL,
        "is_background_automation": False,
        "version": _UNKNOWN_VERSION,
        "_dialogue_text": _minimize_dialogue(dialogue_parts),
    }
    return traces, session_meta


def _ts_to_ms_to_iso(ms):
    """Unix 毫秒 → ISO 8601（用于 created_date 兜底）。"""
    if not ms:
        return ""
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()
    except (ValueError, TypeError, OSError):
        return ""


def collect_claude_code_traces(start_date, end_date, projects_root=None):
    """读取 Claude Code 会话历史，返回统一 schema 的 trace 列表（含成本字段）。

    参数：
      start_date / end_date: 'YYYY-MM-DD' 字符串，闭区间过滤。
      projects_root: 可选，覆盖默认 projects 根（测试用）；默认自动探测。
    返回：list[dict]，字段与 scripts/ca_sources.collect_traces 完全一致。
    """
    root = Path(projects_root) if projects_root else resolve_claude_projects_root()
    traces = []
    for f in _iter_jsonl_files(root):
        file_traces, _ = _parse_claude_file(f, start_date, end_date)
        traces.extend(file_traces)
    traces.sort(key=lambda x: x.get("started_at") or "")
    return traces


def collect_claude_code_sessions(start_date, end_date, projects_root=None):
    """读取 Claude Code 会话历史，返回合成 db_data（sessions 已预分类 task_type）。

    返回：{"sessions": [...], "automation_runs": [], "session_credits": []}
    sessions 字段与 WorkBuddy db_data["sessions"] 同源（含 task_type / title / model 等），
    供 aggregate_by_session / aggregate_task_token_stats / aggregate_top_tasks 直接使用。
    """
    root = Path(projects_root) if projects_root else resolve_claude_projects_root()
    sessions = []
    for f in _iter_jsonl_files(root):
        file_traces, meta = _parse_claude_file(f, start_date, end_date)
        cd = meta.get("created_date") or ""
        # 契约：仅纳入「created_date 落在窗口内」或「窗口内有 trace」的会话；
        # 越窗（或日期未知且无窗内活动）的会话元数据不进报告，防止越权收集。
        if not _session_in_window(meta, file_traces, start_date, end_date):
            continue
        # 任务类型分类：基于对话文本（复用统一 classify_task，与 WorkBuddy 同源）
        text = meta.get("_dialogue_text", "")
        meta["task_type"] = classify_task(text)
        # 移除内部辅助字段
        meta.pop("_dialogue_text", None)
        sessions.append(meta)
    return {
        "sessions": sessions,
        "automation_runs": [],
        "session_credits": [],
    }


def collect_claude_code(start_date, end_date, projects_root=None):
    """一次性返回 (traces, db_data)，供 collect_usage_data.py --source claude-code 直接使用。

    隐私边界与 collect_claude_code_sessions 完全一致：越窗会话（无窗内 trace 且
    created_date 不在窗口内）整体跳过，不进 traces 也不进 sessions 元数据
    （SDI-1 / SDI-4 修复点：合并 collector 原先漏做窗口过滤）。
    """
    root = Path(projects_root) if projects_root else resolve_claude_projects_root()
    traces = []
    sessions = []
    for f in _iter_jsonl_files(root):
        file_traces, meta = _parse_claude_file(f, start_date, end_date)
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
