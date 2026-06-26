#!/usr/bin/env python3
"""
token-stats — 选个 Agent 看它的 token 消耗

用法:
  token-stats                    交互式菜单：选 Agent → 看统计
  token-stats -a hermes          直接查看 Hermes
  token-stats -w / --watch            交互式菜单 → 实时监控
  token-stats --all              查看本机所有 Agent 的统计
  token-stats -a hermes --now    同默认（显式快照）

  时间段查询:
  token-stats -a hermes -t / --today
  token-stats -a hermes --yesterday
  token-stats -a hermes --week
  token-stats -a hermes --last-7d
  token-stats -a hermes -m / --month
  token-stats -a hermes -y / --year
  token-stats -a hermes --from 2025-01-01 --to 2025-01-31

  导出:
  token-stats -a hermes -e / --export
  token-stats -a hermes -t -e

  对比:
  token-stats -a hermes --compare --a today --b yesterday
  token-stats -a hermes --compare --a this-week --b last-week
  token-stats -a hermes --compare --a 2025-01-01 --b 2025-01-15
  token-stats -a hermes --compare --a 2025-01-01~2025-01-07 --b 2025-01-08~2025-01-14

  详细模式:
  token-stats -a hermes --detail

安装:
  python3 token-stats.py setup                   安装到 ~/.token-stats，并将 ~/.token-stats/bin 加入 PATH
  token-stats --uninstall                        删除全局命令、安装目录并清理 PATH
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import quote

from . import compare, installer, snapshot
from .pricing import (
    calc_cost,
    calc_total_cost,
    fmt_cost,
    fmt_total_cost,
    get_model_price,
    load_model_prices,
    to_cny,
)
from .exporters import export_interactive, export_multi
from .dates import label_to_display, parse_date, parse_time_label, split_months
from .contexts import DEFAULT_CONTEXT, detect_context
from .menu import show_menu
from .paths import (
    CONFIG_DIR,
    codex_collect_via_wsl as _codex_collect_via_wsl,
    get_wsl_homes as _get_wsl_homes,
    hermes_collect_via_wsl as _hermes_collect_via_wsl,
    is_wsl_unc as _is_wsl_unc,
    load_agent_paths as _load_agent_paths,
    resolve_path as _resolve_path,
    save_agent_paths as _save_agent_paths,
    scan_all_agent_paths as _scan_all_agent_paths,
    wsl_unc_to_linux as _wsl_unc_to_linux,
)
from .rendering import (
    build_aligned_raw,
    fmt_today_lines as render_today_lines,
    format_model_line as render_model_line,
)
from .formatting import (
    align_rows as _align_rows,
    calc_cache_rate as _calc_cache_rate,
    display_width as _display_width,
    fmt_cache_val as _fmt_cache_val,
    fmt_num,
    progress_bar as _progress_bar,
    skip_model as _skip_model,
    strip_ansi as _strip_ansi,
)

VERSION = "2.7.13"
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PACKAGE_DIR)

# 强制 stdout 行缓冲 + UTF-8，使 --watch 模式的输出实时可见
try:
    sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
except Exception:
    try:
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    except Exception:
        pass

# ═══════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════

def _load_model_prices() -> dict:
    return load_model_prices(PROJECT_ROOT, os.getcwd())


def _get_model_price(model: str) -> dict | None:
    return get_model_price(model, _load_model_prices())


def _calc_cost(inp: int, out: int, cache: int, price: dict) -> float:
    return calc_cost(inp, out, cache, price)


def _fmt_cost(inp: int, out: int, cache: int, price: dict) -> str:
    return fmt_cost(inp, out, cache, price)


def _calc_total_cost(per_model_list: list) -> dict[str, float]:
    return calc_total_cost(per_model_list, _get_model_price)


def _to_cny(cost: float, currency: str) -> float:
    return to_cny(cost, currency)


def _fmt_total_cost(totals: dict[str, float]) -> str:
    return fmt_total_cost(totals)


def _has_any_price(per_model_data: list) -> bool:
    """检查 per_model 列表中是否至少有一个模型配置了价格"""
    for pm in (per_model_data or []):
        if pm.get("token_mode") == "total":
            continue
        mn = pm.get("model", "")
        if _get_model_price(mn):
            return True
    return False


def _compare_helpers():
    return {
        "parse_time_label": parse_time_label,
        "label_to_display": label_to_display,
        "skip_model": _skip_model,
        "fmt_num": fmt_num,
        "calc_cache_rate": _calc_cache_rate,
        "get_model_price": _get_model_price,
        "calc_cost": _calc_cost,
        "to_cny": _to_cny,
        "align_rows": _align_rows,
        "display_width": _display_width,
        "strip_ansi": _strip_ansi,
    }


def _export_helpers():
    return {
        "version": VERSION,
        "split_months": split_months,
        "skip_model": _skip_model,
        "calc_cache_rate": _calc_cache_rate,
        "fmt_num": fmt_num,
        "detect_context": detect_context,
        "project_root": PROJECT_ROOT,
    }

def _monitor_helpers():
    return {
        "fmt_num": fmt_num,
        "calc_cache_rate": _calc_cache_rate,
        "fmt_cache_val": _fmt_cache_val,
        "get_model_price": _get_model_price,
        "calc_cost": _calc_cost,
        "calc_total_cost": _calc_total_cost,
        "fmt_cost": _fmt_cost,
        "fmt_total_cost": _fmt_total_cost,
        "to_cny": _to_cny,
        "has_any_price": _has_any_price,
        "align_rows": _align_rows,
        "progress_bar": _progress_bar,
    }


def _snapshot_helpers():
    return {
        "skip_model": _skip_model,
        "fmt_num": fmt_num,
        "fmt_cache_val": _fmt_cache_val,
        "get_model_price": _get_model_price,
        "calc_cost": _calc_cost,
        "fmt_total_cost": _fmt_total_cost,
    }


def _render_helpers():
    return {
        "get_model_price": _get_model_price,
        "calc_total_cost": _calc_total_cost,
        "fmt_cost": _fmt_cost,
        "fmt_total_cost": _fmt_total_cost,
        "has_any_price": _has_any_price,
    }


def fmt_today_lines(per_model: list, fmt_num_fn) -> list:
    return render_today_lines(per_model, fmt_num_fn, _render_helpers())


def format_model_line(model_name: str, inp: int, out: int, cache: int, calls: int,
                      context_window: int = None, session_count: int = None,
                      extra: str = None) -> str:
    return render_model_line(model_name, inp, out, cache, calls, _render_helpers(),
                             context_window=context_window, session_count=session_count, extra=extra)


def _build_aligned_raw(agent_display: str, per_model_list: list,
                        has_context: bool = False,
                        extra_footer: str = None,
                        token_mode: str = "split") -> str:
    return build_aligned_raw(agent_display, per_model_list, _render_helpers(),
                             has_context=has_context, extra_footer=extra_footer,
                             token_mode=token_mode)


# ═══════════════════════════════════════════════════
#  Agent 基类与数据模型
# ═══════════════════════════════════════════════════

@dataclass
class AgentData:
    """单个 Agent 的统计数据"""
    name: str
    display_name: str
    stats: dict
    raw: str
    per_model: list = None  # [{"model": ..., "input": N, "output": N, "calls": N, "cache": N}, ...]
    token_mode: str = "split"  # "split" = 区分入/出, "total" = 仅有总计（回退/WSL）


class BaseAgent(ABC):
    """Agent 检测器基类"""

    # 支持实时上下文占比显示（会话型 Agent 为 True，累计型为 False）
    _has_live_context = False

    @staticmethod
    @abstractmethod
    def name() -> str: ...

    @staticmethod
    @abstractmethod
    def display_name() -> str: ...

    @staticmethod
    @abstractmethod
    def detect() -> bool: ...

    @abstractmethod
    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData: ...

    def watch(self, interval: int = 5) -> None:
        """实时监控模式"""
        from .monitor import watch_agent

        watch_agent(self, interval, _monitor_helpers())

# ═══════════════════════════════════════════════════
#  Hermes
# ═══════════════════════════════════════════════════

def _find_hermes_db() -> str:
    """获取 Hermes 数据库路径，优先从配置读取"""
    cfg = _load_agent_paths()
    if "hermes_db" in cfg:
        return cfg["hermes_db"]
    return _resolve_path(".hermes/state.db")


def _find_hermes_sessions() -> str:
    """获取 Hermes sessions 文件路径，优先从配置读取"""
    cfg = _load_agent_paths()
    if "hermes_sessions" in cfg:
        return cfg["hermes_sessions"]
    return _resolve_path(".hermes/sessions/sessions.json")


def _hermes_current_session_id() -> str | None:
    """从 sessions.json 读取当前活跃会话 ID。"""
    sessions_path = _find_hermes_sessions()
    try:
        with open(sessions_path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        for key, val in data.items():
            if isinstance(val, dict) and val.get("session_id"):
                return val["session_id"]
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return None


def _open_hermes_sqlite(hermes_db: str) -> sqlite3.Connection:
    """Open Hermes DB, falling back to immutable read for retained/offline data."""
    conn = None
    try:
        conn = sqlite3.connect(hermes_db, timeout=10)
        conn.row_factory = sqlite3.Row
        # Force SQLite to touch the database now; some retained Hermes DBs connect
        # but fail on the first schema/query read without immutable mode.
        conn.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
        return conn
    except sqlite3.OperationalError as e:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
        if "unable to open database file" not in str(e).lower():
            raise

    path = quote(os.path.abspath(hermes_db), safe="/:")
    conn = sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


class HermesAgent(BaseAgent):
    _has_live_context = True  # 有当前会话概念，上下文占比有意义

    @staticmethod
    def name() -> str:
        return "hermes"

    @staticmethod
    def display_name() -> str:
        return "Hermes"

    @staticmethod
    def detect() -> bool:
        db = _find_hermes_db()
        if os.path.exists(db):
            return True
        # WSL 路径可能 UNC 不通但 wsl.exe 已验证存在（_resolve_path 已处理）
        return db != os.path.join(os.path.expanduser("~"), ".hermes", "state.db")

    def _try_wsl_fallback(self, hermes_db, error_msg, from_ts=None, to_ts=None):
        """WSL 路径 DB 不可用时，通过 wsl.exe 在 WSL 内读取。"""
        distro, _ = _wsl_unc_to_linux(hermes_db)
        if not distro:
            return None
        if "locked" not in error_msg.lower() and "unable to open" not in error_msg.lower():
            return None
        result = _hermes_collect_via_wsl(hermes_db, from_ts, to_ts)
        if not result:
            return None
        if not result.get("rows"):
            # WSL 查询成功但该时段无数据，返回空 AgentData
            label = "Hermes (WSL)"
            return AgentData(name="hermes", display_name=label,
                             stats={}, raw=f"{label}: 该时间段内无会话记录", per_model=[])
        rows = result["rows"]
        per_model_list = []
        ti = to = tc = tca = tsess = 0
        for r in rows:
            m = r.get("model") or "unknown"
            inp = int(r.get("inp") or 0)
            out = int(r.get("out") or 0)
            cache = int(r.get("cache") or 0)
            calls = int(r.get("calls") or 0)
            cnt = int(r.get("cnt") or 0)
            ti += inp; to += out; tc += cache; tca += calls; tsess += cnt
            per_model_list.append({"model": m, "input": inp, "output": out, "calls": calls, "cache": cache})
        extra_footer = f"  会话: {tsess} 轮"
        raw = _build_aligned_raw("Hermes (WSL)", per_model_list,
                                 has_context=True,
                                 extra_footer=extra_footer)
        stats = {
            "model": ", ".join(sorted({(r.get("model") or "unknown") for r in rows})),
            "input_tokens": ti, "output_tokens": to, "cache_read": tc,
            "api_calls": tca, "total_tokens": ti + to, "session_count": tsess,
        }
        return AgentData(name="hermes", display_name="Hermes", stats=stats, raw=raw, per_model=per_model_list)

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        hermes_db = _find_hermes_db()
        # WSL UNC 路径跳过直连（通过 UNC 打开 SQLite 极慢，timeout 会被放大到 ~30s）
        if _is_wsl_unc(hermes_db):
            fb = self._try_wsl_fallback(hermes_db, "database is locked (WSL UNC)", from_ts, to_ts)
            if fb:
                return fb
            # WSL fallback 不可用，回退到直连尝试
        try:
            return self._collect_impl(hermes_db, from_ts, to_ts)
        except Exception as e:
            fb = self._try_wsl_fallback(hermes_db, str(e), from_ts, to_ts)
            if fb:
                return fb
            raise

    def _collect_impl(self, hermes_db, from_ts, to_ts):
        conn = _open_hermes_sqlite(hermes_db)

        # ── schema 兼容：检测旧版 Hermes 缺少的列 ──
        has_api_calls = True
        has_tool_calls = True
        try:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(sessions)").fetchall()}
            if "api_call_count" not in cols:
                has_api_calls = False
            if "tool_call_count" not in cols:
                has_tool_calls = False
        except Exception:
            pass

        if from_ts is not None or to_ts is not None:
            # ── 时间段统计 ──
            where = []
            params = []
            if from_ts is not None:
                # ended_at IS NULL 仅对 1 天内的会话放行，避免旧会话 ended_at 残留 NULL
                grace = from_ts - 86400
                where.append("(started_at >= ? OR (ended_at IS NULL AND started_at >= ?) OR (ended_at IS NOT NULL AND ended_at >= ?))")
                params.append(from_ts)
                params.append(grace)
                params.append(from_ts)
            if to_ts is not None:
                where.append("started_at <= ?")
                params.append(to_ts)
            clause = " AND ".join(where)

            calls_expr = "SUM(api_call_count)" if has_api_calls else "0"
            tools_expr = "SUM(tool_call_count)" if has_tool_calls else "0"
            cur = conn.execute(
                f"SELECT model, SUM(input_tokens) as inp, SUM(output_tokens) as out, "
                f"SUM(cache_read_tokens) as cache, {calls_expr} as calls, "
                f"{tools_expr} as tools, COUNT(*) as cnt "
                f"FROM sessions WHERE {clause} GROUP BY model",
                params
            )
            rows = cur.fetchall()
            conn.close()

            if not rows:
                return AgentData(
                    name="hermes", display_name="Hermes",
                    stats={}, raw="Hermes: 该时间段内无会话记录"
                )

            total_inp = sum(r["inp"] or 0 for r in rows)
            total_out = sum(r["out"] or 0 for r in rows)
            total_cache = sum(r["cache"] or 0 for r in rows)
            total_calls = sum(r["calls"] or 0 for r in rows)
            total_sessions = sum(r["cnt"] or 0 for r in rows)

            per_model_list = []
            for r in rows:
                m = r["model"] or "unknown"
                inp = r["inp"] or 0
                out = r["out"] or 0
                cache = r["cache"] or 0
                calls = r["calls"] or 0
                per_model_list.append({"model": m, "input": inp, "output": out,
                                        "calls": calls, "cache": cache})

            extra_footer = f"  会话: {total_sessions} 轮"
            raw = _build_aligned_raw("Hermes", per_model_list,
                                     has_context=True,
                                     extra_footer=extra_footer)

            stats = {
                "model": ", ".join(sorted({r["model"] or "unknown" for r in rows})),
                "input_tokens": total_inp,
                "output_tokens": total_out,
                "cache_read": total_cache,
                "api_calls": total_calls,
                "total_tokens": total_inp + total_out,
                "session_count": total_sessions,
            }

            return AgentData(name="hermes", display_name="Hermes",
                             stats=stats, raw=raw, per_model=per_model_list)

        # ── 全部会话统计（无时间筛选）──
        calls_expr = "SUM(api_call_count)" if has_api_calls else "0"
        tools_expr = "SUM(tool_call_count)" if has_tool_calls else "0"
        cur = conn.execute(
            f"SELECT model, SUM(input_tokens) as inp, SUM(output_tokens) as out, "
            f"SUM(cache_read_tokens) as cache, {calls_expr} as calls, "
            f"{tools_expr} as tools, COUNT(*) as cnt "
            f"FROM sessions GROUP BY model"
        )
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return AgentData(
                name="hermes", display_name="Hermes",
                stats={}, raw="Hermes: 尚无会话记录"
            )

        total_inp = sum(r["inp"] or 0 for r in rows)
        total_out = sum(r["out"] or 0 for r in rows)
        total_cache = sum(r["cache"] or 0 for r in rows)
        total_calls = sum(r["calls"] or 0 for r in rows)
        total_sessions = sum(r["cnt"] or 0 for r in rows)

        per_model_list = []
        for r in rows:
            m = r["model"] or "unknown"
            inp = r["inp"] or 0
            out = r["out"] or 0
            cache = r["cache"] or 0
            calls = r["calls"] or 0
            per_model_list.append({"model": m, "input": inp, "output": out,
                                    "calls": calls, "cache": cache})

        extra_footer = f"  会话: {total_sessions} 轮"
        raw = _build_aligned_raw("Hermes", per_model_list,
                                 has_context=True,
                                 extra_footer=extra_footer)

        stats = {
            "model": ", ".join(sorted({r["model"] or "unknown" for r in rows})),
            "input_tokens": total_inp,
            "output_tokens": total_out,
            "cache_read": total_cache,
            "api_calls": total_calls,
            "total_tokens": total_inp + total_out,
            "session_count": total_sessions,
        }

        return AgentData(name="hermes", display_name="Hermes",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  Claude Code
# ═══════════════════════════════════════════════════

def _find_claude_dir() -> str:
    """获取 Claude Code 目录，优先从配置读取"""
    cfg = _load_agent_paths()
    if "claude_dir" in cfg:
        return cfg["claude_dir"]
    return _resolve_path(".claude")


class ClaudeCodeAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "claude-code"

    @staticmethod
    def display_name() -> str:
        return "Claude Code"

    @staticmethod
    def detect() -> bool:
        cd = _find_claude_dir()
        if os.path.isdir(os.path.join(cd, "projects")):
            return True
        native = os.path.join(os.path.expanduser("~"), ".claude")
        return cd != native

    def _find_sessions(self, from_ts: float = None, to_ts: float = None):
        projects_dir = os.path.join(_find_claude_dir(), "projects")
        if not os.path.isdir(projects_dir):
            return []
        sessions = []
        for proj in os.listdir(projects_dir):
            proj_dir = os.path.join(projects_dir, proj)
            if not os.path.isdir(proj_dir):
                continue
            for root, _dirs, files in os.walk(proj_dir):
                for fname in files:
                    if fname.endswith(".jsonl") and not fname.endswith(".trajectory.jsonl"):
                        fpath = os.path.join(root, fname)
                        sessions.append((proj, fname, fpath))
        return sorted(sessions, key=lambda x: os.path.getmtime(x[2]), reverse=True)

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        # 缓存策略：带时间筛选时优先用缓存；无筛选时从磁盘重读并更新缓存
        want_cache = from_ts is not None or to_ts is not None

        if want_cache and hasattr(self, '_cache') and self._cache is not None:
            # 带时间筛选 + 缓存存在 → 直接复用（导出场景按月拆分、watch 今日合计）
            messages = self._cache
        else:
            # 从磁盘重新读取并更新缓存
            sessions = self._find_sessions()
            self._cached_session_count = len(sessions)
            self._cached_sub_count = 0
            self._cached_project_count = 0
            messages = []
            _seen = set()  # 去重同一 JSONL 文件内重复写入的同一条 assistant 消息
            projects = set()

            if sessions:
                for proj, fname, fpath in sessions:
                    projects.add(proj)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            for line_no, line in enumerate(f, 1):
                                line = line.strip()
                                if not line:
                                    continue
                                try:
                                    msg = json.loads(line)
                                except json.JSONDecodeError:
                                    continue
                                if msg.get("toolUseResult") and "usage" in msg["toolUseResult"]:
                                    self._cached_sub_count += 1
                                if msg.get("type") != "assistant":
                                    continue
                                model = msg.get("message", {}).get("model") or msg.get("model", "unknown")
                                usage = msg.get("message", {}).get("usage") or msg.get("usage", {})
                                ts_str = msg.get("timestamp", "")
                                try:
                                    dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                                    msg_ts = dt.timestamp()
                                except (ValueError, TypeError):
                                    msg_ts = None
                                inp = usage.get('input_tokens', 0)
                                out = usage.get('output_tokens', 0)
                                cache = usage.get('cache_read_input_tokens', 0)
                                key = (fpath, model, inp, out, cache)
                                if key in _seen:
                                    continue
                                _seen.add(key)
                                messages.append({
                                    'ts': msg_ts,
                                    'model': model,
                                    'input': inp,
                                    'output': out,
                                    'cache': cache,
                                    'project': proj,
                                    'file': fpath,
                                })
                    except Exception:
                        continue
                self._cached_project_count = len(projects)
            # 总是缓存，方便后续复用（如 watch 模式的今日合计查询）
            self._cache = messages

        # 按时间范围过滤
        per_model_data = {}
        filtered_projects = set()
        filtered_files = set()
        for msg in messages:
            if msg['ts'] is not None:
                if from_ts is not None and msg['ts'] < from_ts:
                    continue
                if to_ts is not None and msg['ts'] > to_ts:
                    continue
            model = msg['model']
            if model.startswith("<"):
                model = "subagent"
            if model not in per_model_data:
                per_model_data[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
            per_model_data[model]["input"] += msg['input']
            per_model_data[model]["output"] += msg['output']
            per_model_data[model]["cache"] += msg['cache']
            per_model_data[model]["calls"] += 1
            if msg.get("project"):
                filtered_projects.add(msg["project"])
            if msg.get("file"):
                filtered_files.add(msg["file"])

        if not per_model_data:
            return AgentData(
                name="claude-code", display_name="Claude Code",
                stats={}, raw="Claude Code: 会话文件中未解析到有效数据"
            )

        total_calls = sum(d["calls"] for d in per_model_data.values())
        total_input = sum(d["input"] for d in per_model_data.values())
        total_output = sum(d["output"] for d in per_model_data.values())
        total_cache = sum(d["cache"] for d in per_model_data.values())
        models_sorted = sorted(per_model_data.keys())

        meaningful_models = [
            mn for mn in models_sorted
            if per_model_data[mn]["input"] + per_model_data[mn]["output"] > 0
        ]

        per_model_list = []
        for mn in meaningful_models:
            md = per_model_data[mn]
            per_model_list.append({
                "model": mn,
                "input": md["input"],
                "output": md["output"],
                "calls": md["calls"],
                "cache": md["cache"],
            })

        if from_ts is not None or to_ts is not None:
            session_count = len(filtered_files)
            project_count = len(filtered_projects)
        else:
            session_count = self._cached_session_count
            project_count = self._cached_project_count
        extra_footer = f"  子代理: {self._cached_sub_count} 次 | 会话: {session_count} 个 | 项目: {project_count} 个"
        raw = _build_aligned_raw("Claude Code", per_model_list,
                                 has_context=False,
                                 extra_footer=extra_footer)

        stats = {
            "model": ", ".join(models_sorted),
            "input_tokens": total_input,
            "output_tokens": total_output,
            "cache_read": total_cache,
            "api_calls": total_calls,
            "sub_calls": self._cached_sub_count,
            "total_tokens": total_input + total_output,
            "session_count": session_count,
            "projects": project_count,
        }

        return AgentData(name="claude-code", display_name="Claude Code",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  CodeX
# ═══════════════════════════════════════════════════

# JSONL parse cache: {rollout_path: (mtime, [delta_event, ...])}
_codex_jsonl_cache = {}


def _codex_usage_parts(usage: dict) -> tuple[int, int, int]:
    """Return cumulative (input_total, cache_total, output_total) from a CodeX usage dict."""
    inp = int(usage.get("input_tokens", 0) or 0)
    cache = int(usage.get("cached_input_tokens", 0) or 0)
    out = int(usage.get("output_tokens", 0) or 0) + int(usage.get("reasoning_output_tokens", 0) or 0)
    return inp, cache, out


def _codex_delta_from_totals(current: tuple[int, int, int], previous: tuple[int, int, int] | None):
    """Convert cumulative CodeX totals into a single event delta.

    CodeX may emit token_count events with unchanged totals or info=null. Those are
    progress/rate-limit updates, not API usage increments, so callers skip zero deltas.
    """
    if previous is None:
        delta = current
    else:
        delta = tuple(cur - prev for cur, prev in zip(current, previous))
        if any(v < 0 for v in delta):
            # Defensive reset handling: if a future schema restarts totals mid-file,
            # treat the current total as a new segment rather than emitting negatives.
            delta = current
    if not any(v > 0 for v in delta):
        return None
    inp_total, cache_tok, out_tok = delta
    return {
        "input": max(0, inp_total - cache_tok),
        "output": max(0, out_tok),
        "cache": max(0, cache_tok),
        "calls": 1,
    }


def _load_codex_session_deltas(rollout_path):
    """Parse a CodeX rollout JSONL into timestamped token deltas.

    Returns None only when the file cannot be parsed as a CodeX token stream. An
    empty list means the file was readable but had no billable usage deltas.
    """
    if not rollout_path or not os.path.exists(rollout_path):
        return None

    mtime = os.path.getmtime(rollout_path)
    cached = _codex_jsonl_cache.get(rollout_path)
    if cached and cached[0] == mtime:
        return list(cached[1])

    deltas = []
    saw_token_event = False
    prev_total = None
    try:
        with open(rollout_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if (
                    obj.get("type") != "event_msg"
                    or obj.get("payload", {}).get("type") != "token_count"
                ):
                    continue
                saw_token_event = True
                ts_str = obj.get("timestamp", "")
                try:
                    evt_ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).timestamp()
                except Exception:
                    continue
                info = obj.get("payload", {}).get("info") or {}
                total = info.get("total_token_usage")
                if not isinstance(total, dict) or not total:
                    continue
                current = _codex_usage_parts(total)
                delta = _codex_delta_from_totals(current, prev_total)
                prev_total = current
                if delta is None:
                    continue
                delta["ts"] = evt_ts
                deltas.append(delta)
    except Exception:
        return None

    if not saw_token_event:
        return None
    _codex_jsonl_cache[rollout_path] = (mtime, list(deltas))
    return deltas


def _parse_codex_session_jsonl(rollout_path, from_ts=None, to_ts=None):
    """解析 CodeX session JSONL 文件，提取 token 消耗（含 I/O 拆分和调用次数）。

    返回 {"input": N, "output": N, "cache": N, "calls": N, "_parsed": True}
    或 None（文件缺失/不可读/不是 CodeX token stream）。
    calls = 有真实 token 增量的 token_count 事件数；info=null 或累计值不变的
    progress/rate-limit 事件不计入调用。
    """
    deltas = _load_codex_session_deltas(rollout_path)
    if deltas is None:
        return None

    result = {"input": 0, "output": 0, "cache": 0, "calls": 0, "_parsed": True}
    for evt in deltas:
        evt_ts = evt.get("ts")
        if from_ts is not None and evt_ts is not None and evt_ts < from_ts:
            continue
        if to_ts is not None and evt_ts is not None and evt_ts > to_ts:
            continue
        result["input"] += evt.get("input", 0)
        result["output"] += evt.get("output", 0)
        result["cache"] += evt.get("cache", 0)
        result["calls"] += evt.get("calls", 0)
    return result


def _find_codex_db() -> Optional[str]:
    """获取 CodeX 数据库路径，优先从配置读取。

    CodeX 官方订阅可能把 state DB 放在 ~/.codex/sqlite/ 子目录，
    而中转/旧版直接放在 ~/.codex/ 下。
    """
    cfg = _load_agent_paths()
    codex_dir = cfg.get("codex_dir") if "codex_dir" in cfg else _resolve_path(".codex")
    if not os.path.isdir(codex_dir):
        return None

    # state_*.sqlite 可能在 codex_dir 或 codex_dir/sqlite/ 下
    candidates: list[tuple[str, str]] = []
    for root in (codex_dir, os.path.join(codex_dir, "sqlite")):
        if not os.path.isdir(root):
            continue
        for f in os.listdir(root):
            if re.match(r'^state_\d+\.sqlite$', f):
                candidates.append((root, f))

    # 优先 state 编号最大，同编号选 mtime 最新
    best: str | None = None
    best_state = -1
    best_mtime = 0.0
    for dir_path, f in candidates:
        m = re.match(r'^state_(\d+)\.sqlite$', f)
        if not m:
            continue
        state = int(m.group(1))
        full = os.path.join(dir_path, f)
        try:
            mtime = os.path.getmtime(full)
        except OSError:
            mtime = 0.0
        if state > best_state or (state == best_state and mtime > best_mtime):
            best_state = state
            best_mtime = mtime
            best = full
    return best


class CodeXAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "codex"

    @staticmethod
    def display_name() -> str:
        return "CodeX"

    @staticmethod
    def detect() -> bool:
        db = _find_codex_db()
        if db is not None:
            return os.path.exists(db)
        return False

    def _codex_wsl_fallback(self, db, from_ts, to_ts):
        """WSL UNC 路径：通过 wsl.exe 在 WSL 内查询 CodeX 数据库。"""
        result = _codex_collect_via_wsl(db, from_ts, to_ts)
        if not result or not result.get("rows"):
            return AgentData(
                name="codex", display_name="CodeX (WSL)",
                stats={}, raw="CodeX (WSL): 该时间段内无会话记录", per_model=[], token_mode="total"
            )
        rows = result["rows"]
        per_model_list = []
        total_tok = total_cnt = 0
        for r in rows:
            model = r.get("model") or r.get("model_provider") or "codex-default"
            ts = int(r.get("tokens") or 0)
            cnt = int(r.get("cnt") or 0)
            per_model_list.append({"model": model, "input": ts, "output": 0, "calls": cnt, "cache": 0, "token_mode": "total"})
            total_tok += ts
            total_cnt += cnt
        stats = {
            "model": ", ".join(sorted({pm["model"] for pm in per_model_list})),
            "total_tokens": total_tok, "session_count": total_cnt,
        }
        raw = _build_aligned_raw("CodeX (WSL)", per_model_list, token_mode="total")
        return AgentData(name="codex", display_name="CodeX", stats=stats, raw=raw, per_model=per_model_list, token_mode="total")

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        db = _find_codex_db()
        if not db:
            return AgentData(
                name="codex", display_name="CodeX",
                stats={}, raw="CodeX: 未检测到数据库文件", token_mode="split"
            )
        # WSL UNC 路径跳过直连
        if _is_wsl_unc(db):
            return self._codex_wsl_fallback(db, from_ts, to_ts)
        try:
            conn = sqlite3.connect(db, timeout=5)
            conn.row_factory = sqlite3.Row

            # 先读取候选线程，再用 rollout JSONL 内的事件时间精筛。
            # 仅没有 JSONL 明细时，才回退到 threads.updated_at。
            query = "SELECT id, model, model_provider, tokens_used, rollout_path, updated_at FROM threads WHERE tokens_used > 0"
            thread_rows = conn.execute(query).fetchall()
            conn.close()

            # 按模型聚合（仅按 model 分组，合并不同 provider）
            per_model: dict[str, dict[str, int]] = {}
            total_sessions = 0

            for tr in thread_rows:
                model = tr["model"] or tr["model_provider"] or "codex-default"
                rollout = tr["rollout_path"]

                # 尝试从 session JSONL 读取 I/O 拆分
                jd = _parse_codex_session_jsonl(rollout, from_ts, to_ts)

                if jd is not None:
                    # JSONL 可读时即采用 JSONL 事件时间精筛；即便该时间段无
                    # token delta，也不能回退到整条 threads.tokens_used。
                    if not (jd["input"] or jd["output"] or jd["cache"] or jd["calls"]):
                        continue
                    if model not in per_model:
                        per_model[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0, "mode": "split"}
                    per_model[model]["input"] += jd["input"]
                    per_model[model]["output"] += jd["output"]
                    per_model[model]["cache"] += jd["cache"]
                    per_model[model]["calls"] += jd.get("calls", 1)
                    total_sessions += 1
                else:
                    # 回退：使用 tokens_used 作为总计
                    updated_at = tr["updated_at"]
                    if from_ts is not None and updated_at is not None and updated_at < int(from_ts):
                        continue
                    if to_ts is not None and updated_at is not None and updated_at > int(to_ts):
                        continue
                    ts = tr["tokens_used"] or 0
                    if ts <= 0:
                        continue
                    if model not in per_model:
                        per_model[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0, "mode": "total"}
                    per_model[model]["input"] += ts
                    per_model[model]["calls"] += 1
                    total_sessions += 1

            if not per_model:
                return AgentData(
                    name="codex", display_name="CodeX",
                    stats={}, raw="CodeX: 该时间段内无会话记录", token_mode="split"
                )

            per_model_list = []
            for model, data in per_model.items():
                per_model_list.append({
                    "model": model,
                    "input": data["input"],
                    "output": data["output"],
                    "calls": data["calls"],
                    "cache": data["cache"],
                    "token_mode": data.get("mode", "split"),
                })

            has_total_only_data = any(data.get("mode") == "total" for data in per_model.values())
            raw = _build_aligned_raw("CodeX", per_model_list,
                                     token_mode="total" if has_total_only_data else "split")

            stats = {
                "model": ", ".join(sorted(per_model.keys())),
                "total_tokens": sum(pm["input"] + pm["output"] for pm in per_model_list),
                "session_count": total_sessions,
            }
            # 只要混入 tokens_used fallback，就不能声称是完整 I/O 拆分。
            token_mode = "total" if has_total_only_data else "split"
            return AgentData(name="codex", display_name="CodeX",
                             stats=stats, raw=raw, per_model=per_model_list, token_mode=token_mode)

        except Exception as e:
            return AgentData(
                name="codex", display_name="CodeX",
                stats={}, raw=f"CodeX: 读取失败 — {e}", token_mode="split"
            )


# ═══════════════════════════════════════════════════
#  OpenClaw
# ═══════════════════════════════════════════════════

def _find_openclaw_sessions_dir() -> Optional[str]:
    """获取 OpenClaw 会话目录（含 .jsonl 文件），优先从配置读取"""
    cfg = _load_agent_paths()
    if "openclaw_sessions" in cfg:
        p = cfg["openclaw_sessions"]
        # 可能是 sessions.json 路径（取父目录）或目录路径
        if p.endswith(".json"):
            d = os.path.dirname(p)
            if os.path.isdir(d):
                return d
        elif os.path.isdir(p):
            return p
    candidates = [
        _resolve_path(".openclaw/agents/main/sessions"),
    ]
    for d in candidates:
        if os.path.isdir(d):
            return d
    return None


def _find_openclaw_sessions() -> Optional[str]:
    """检测 OpenClaw 会话索引文件（sessions.json），用于 detect()"""
    cfg = _load_agent_paths()
    if "openclaw_sessions" in cfg:
        p = cfg["openclaw_sessions"]
        if os.path.exists(p):
            return p
    candidates = [
        _resolve_path(".openclaw/agents/main/sessions/sessions.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _openclaw_parse_jsonl(fpath: str, from_ts: float = None, to_ts: float = None) -> dict:
    """解析单个 OpenClaw .jsonl 文件，返回 {model: {input, output, cache, calls}}"""
    per_model = {}
    current_model = "unknown"
    current_provider = ""
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = msg.get("type", "")

                # 跟踪模型切换
                if t == "model_change":
                    p = msg.get("provider", "")
                    m = msg.get("modelId", "")
                    if m:
                        current_model = f"{m} ({p})" if p else m
                        current_provider = p
                    continue

                # 仅处理 assistant 消息
                if t != "message":
                    continue
                mrole = msg.get("message", {}).get("role", "")
                if mrole != "assistant":
                    continue

                # 时间过滤
                ts_str = msg.get("timestamp", "")
                if ts_str and (from_ts is not None or to_ts is not None):
                    try:
                        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        msg_ts = dt.timestamp()
                        if from_ts is not None and msg_ts < from_ts:
                            continue
                        if to_ts is not None and msg_ts > to_ts:
                            continue
                    except (ValueError, TypeError):
                        pass

                usage = msg.get("message", {}).get("usage", {})
                inp = usage.get("input", 0) or 0
                out = usage.get("output", 0) or 0
                cache = usage.get("cacheRead", 0) or 0

                # 获取本次消息的模型名（优先级：msg.model > current_model）
                model = msg.get("message", {}).get("model", "") or current_model
                if model not in per_model:
                    per_model[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                per_model[model]["input"] += inp
                per_model[model]["output"] += out
                per_model[model]["cache"] += cache
                per_model[model]["calls"] += 1
    except Exception:
        return {}
    return per_model


class OpenClawAgent(BaseAgent):
    _has_live_context = True  # 有当前会话概念，上下文占比有意义

    @staticmethod
    def name() -> str:
        return "openclaw"

    @staticmethod
    def display_name() -> str:
        return "OpenClaw"

    @staticmethod
    def detect() -> bool:
        sd = _find_openclaw_sessions_dir()
        sf = _find_openclaw_sessions()
        if sd is not None and os.path.isdir(sd):
            return True
        if sf is not None and os.path.exists(sf):
            return True
        native = os.path.join(os.path.expanduser("~"), ".openclaw")
        if sd and sd != os.path.join(native, "agents", "main", "sessions"):
            return True
        if sf and sf != os.path.join(native, "agents", "main", "sessions", "sessions.json"):
            return True
        return False

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        # ── 模式 A：优先从 .jsonl 文件解析（含真实 usage 数据） ──
        sess_dir = _find_openclaw_sessions_dir()
        if sess_dir is not None:
            try:
                jsonl_files = sorted(
                    [f for f in os.listdir(sess_dir)
                     if f.endswith(".jsonl") and not f.endswith(".trajectory.jsonl")]
                )
            except OSError:
                jsonl_files = []
            if jsonl_files:
                per_model_data = {}
                for fname in jsonl_files:
                    fpath = os.path.join(sess_dir, fname)
                    pm = _openclaw_parse_jsonl(fpath, from_ts, to_ts)
                    for model, d in pm.items():
                        if model not in per_model_data:
                            per_model_data[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                        per_model_data[model]["input"] += d["input"]
                        per_model_data[model]["output"] += d["output"]
                        per_model_data[model]["calls"] += d["calls"]
                        per_model_data[model]["cache"] += d["cache"]

                if not per_model_data:
                    return AgentData(
                        name="openclaw", display_name="OpenClaw",
                        stats={}, raw="OpenClaw: 尚无会话" if from_ts is None else "OpenClaw: 该时间段内无会话"
                    )

                total_input = sum(d["input"] for d in per_model_data.values())
                total_output = sum(d["output"] for d in per_model_data.values())
                total_cache = sum(d["cache"] for d in per_model_data.values())
                total_calls = sum(d["calls"] for d in per_model_data.values())

                models_sorted = sorted(per_model_data.keys())
                per_model_list = []
                raw_lines = ["📊 OpenClaw"]
                for mn in models_sorted:
                    md = per_model_data[mn]
                    per_model_list.append({
                        "model": mn, "input": md["input"], "output": md["output"],
                        "calls": md["calls"], "cache": md["cache"],
                    })
                    cw = detect_context(mn)
                    if from_ts is not None or to_ts is not None:
                        line = format_model_line(mn, md["input"], md["output"], md["cache"],
                                                  md["calls"], session_count=md["calls"])
                    else:
                        line = format_model_line(mn, md["input"], md["output"], md["cache"],
                                                  md["calls"], context_window=cw)
                    if line:
                        raw_lines.append(line)

                raw = "\n".join(raw_lines)
                model_list = ", ".join(models_sorted)
                stats = {
                    "model": model_list,
                    "input_tokens": total_input,
                    "output_tokens": total_output,
                    "cache_read": total_cache,
                    "api_calls": total_calls,
                    "total_tokens": total_input + total_output,
                    "session_count": len(jsonl_files),
                }
                if from_ts is None and to_ts is None:
                    first_model = models_sorted[0] if models_sorted else "unknown"
                    cw = detect_context(first_model)
                    stats["context_window"] = cw
                    stats["context_pct"] = round((total_input + total_output) / cw * 100, 1) if cw else 0

                return AgentData(name="openclaw", display_name="OpenClaw",
                                 stats=stats, raw=raw, per_model=per_model_list)
            # 有目录但无 .jsonl → 降级读 sessions.json

        # ── 模式 B：从 sessions.json 读取（回退方案） ──
        oc_path = _find_openclaw_sessions()
        if oc_path is None:
            return AgentData(
                name="openclaw", display_name="OpenClaw",
                stats={}, raw="OpenClaw: 数据文件不存在"
            )
        try:
            with open(oc_path, encoding="utf-8") as f:
                data = json.load(f)

            agents = []
            if isinstance(data, dict):
                for agent_key, session in data.items():
                    if isinstance(session, dict):
                        if from_ts is not None or to_ts is not None:
                            ts = session.get("startedAt", 0) or session.get("updatedAt", 0)
                            if from_ts is not None and ts < from_ts:
                                continue
                            if to_ts is not None and ts > to_ts:
                                continue
                        agents.append(session)
            elif isinstance(data, list):
                for session in data:
                    if isinstance(session, dict):
                        if from_ts is not None or to_ts is not None:
                            ts = session.get("startedAt", 0) or session.get("updatedAt", 0)
                            if from_ts is not None and ts < from_ts:
                                continue
                            if to_ts is not None and ts > to_ts:
                                continue
                        agents.append(session)

            if not agents:
                return AgentData(
                    name="openclaw", display_name="OpenClaw",
                    stats={}, raw="OpenClaw: 尚无会话" if from_ts is None else "OpenClaw: 该时间段内无会话"
                )

            # 按模型分组聚合（sessions.json 中每个 session 有 model 字段）
            per_model_data = {}
            for s in agents:
                model = s.get("model", "unknown")
                provider = s.get("modelProvider", "")
                model_display = f"{model} ({provider})" if provider else model
                inp = s.get("inputTokens", 0) or 0
                out = s.get("outputTokens", 0) or 0
                cache = s.get("cacheRead", 0) or 0
                if model_display not in per_model_data:
                    per_model_data[model_display] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                per_model_data[model_display]["input"] += inp
                per_model_data[model_display]["output"] += out
                per_model_data[model_display]["cache"] += cache
                per_model_data[model_display]["calls"] += 1

            total_input = sum(d["input"] for d in per_model_data.values())
            total_output = sum(d["output"] for d in per_model_data.values())
            total_cache = sum(d["cache"] for d in per_model_data.values())

            latest = max(agents, key=lambda s: s.get("startedAt", 0) or s.get("updatedAt", 0))
            context = latest.get("contextTokens", DEFAULT_CONTEXT)

            models_sorted = sorted(per_model_data.keys())
            per_model_list = []
            raw_lines = ["📊 OpenClaw"]
            for mn in models_sorted:
                md = per_model_data[mn]
                per_model_list.append({
                    "model": mn, "input": md["input"], "output": md["output"],
                    "calls": md["calls"], "cache": md["cache"],
                })
                cw = context
                if from_ts is not None or to_ts is not None:
                    line = format_model_line(mn, md["input"], md["output"], md["cache"],
                                              md["calls"], session_count=md["calls"])
                else:
                    line = format_model_line(mn, md["input"], md["output"], md["cache"],
                                              md["calls"], context_window=cw)
                if line:
                    raw_lines.append(line)

            raw = "\n".join(raw_lines)
            model_list = ", ".join(models_sorted)
            stats = {
                "model": model_list,
                "input_tokens": total_input,
                "output_tokens": total_output,
                "cache_read": total_cache,
                "total_tokens": total_input + total_output,
                "context_window": context,
                "agent_count": len(agents),
            }
            if from_ts is None and to_ts is None:
                stats["context_pct"] = round((total_input + total_output) / context * 100, 1) if context else 0

            return AgentData(name="openclaw", display_name="OpenClaw",
                             stats=stats, raw=raw, per_model=per_model_list)

        except Exception as e:
            return AgentData(
                name="openclaw", display_name="OpenClaw",
                stats={}, raw=f"OpenClaw: 读取失败 — {e}"
            )


# ═══════════════════════════════════════════════════
#  Reasonix
# ═══════════════════════════════════════════════════
# Reasonix 有两套存储：
#   1. CLI 版 (npm 安装)          → ~/.reasonix/usage.jsonl（含 token 用量）
#   2. 桌面版 (Wails app, 0.53+) → ~/Library/Application Support/reasonix/
#      桌面版暂不持久化 token 用量到 usage.jsonl，仅可从 session JSONL 中统计
#      会话数/轮次数/模型名称，无精确 token 数据。


def _reasonix_cli_usage_path() -> Optional[str]:
    """CLI 版: ~/.reasonix/usage.jsonl"""
    p = os.path.join(os.path.expanduser("~"), ".reasonix", "usage.jsonl")
    return p if os.path.isfile(p) else None


def _reasonix_desktop_data_dir() -> Optional[str]:
    """桌面版: ~/Library/Application Support/reasonix"""
    p = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "reasonix")
    return p if os.path.isdir(p) else None


# 桌面版 session 文件名正则: YYYYMMDD-HHMMSS.nanoseconds-MODEL.jsonl
_REASONIX_DESKTOP_SESSION_RE = re.compile(r'^\d{8}-\d{6}\.\d+-(.+)\.jsonl$')


def _reasonix_desktop_sessions(from_ts: float = None, to_ts: float = None) -> dict:
    """扫描桌面版 session 目录，返回 per_model_data 和 session_names。

    桌面版 session JSONL 文件中不含 token usage 数据，
    因此只统计会话数、轮次数（user 消息数）和模型名称。
    返回:
      {
        "per_model": {model: {"sessions": 0, "turns": 0, "input": 0, "output": 0, "calls": 0, "cache": 0, "no_usage": True}},
        "session_names": set(),
        "total_sessions": 0,
        "source_label": "桌面版",
      }
    """
    data_dir = _reasonix_desktop_data_dir()
    if not data_dir:
        return {"per_model": {}, "session_names": set(), "total_sessions": 0, "source_label": "桌面版"}

    per_model: dict[str, dict] = {}
    session_names: set[str] = set()

    # 数据目录结构：
    #   ~/Library/Application Support/reasonix/
    #     sessions/                     ← 全局会话（从 CLI 导入或桌面创建的临时会话）
    #     projects/<hash>/sessions/     ← 项目级会话
    session_dirs = []

    # 全局 sessions
    global_sessions = os.path.join(data_dir, "sessions")
    if os.path.isdir(global_sessions):
        session_dirs.append(global_sessions)

    # 项目级 sessions
    projects_dir = os.path.join(data_dir, "projects")
    if os.path.isdir(projects_dir):
        for proj_name in os.listdir(projects_dir):
            proj_sessions = os.path.join(projects_dir, proj_name, "sessions")
            if os.path.isdir(proj_sessions):
                session_dirs.append(proj_sessions)

    for sd in session_dirs:
        for entry in os.listdir(sd):
            if not entry.endswith(".jsonl"):
                continue
            # 跳过 telemetry / meta / subagent 文件
            if ".telemetry." in entry or entry.endswith(".meta") or "/subagents/" in sd:
                continue
            # 跳过子代理目录中的文件
            if "subagents" in entry:
                continue

            fpath = os.path.join(sd, entry)
            if not os.path.isfile(fpath):
                continue

            # 从文件名提取模型:  <date>-<time>.<ns>-<model>.jsonl
            # e.g. 20260614-015453.575684000-deepseek-v4-pro.jsonl → deepseek-v4-pro
            # 旧式 CLI 导入的会话（如 code-xxx.jsonl）不含模型名，跳过以避免与 usage.jsonl 重复
            _m = _REASONIX_DESKTOP_SESSION_RE.match(entry)
            if not _m:
                # 旧式会话，CLI usage.jsonl 已有其数据，跳过
                continue
            model = _m.group(1)

            # 读取 meta 文件获取时间
            meta_path = fpath + ".meta"
            created_ts = None
            if os.path.isfile(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as mf:
                        meta = json.loads(mf.read() or "{}")
                    created_str = meta.get("created_at", "")
                    if created_str:
                        dt = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                        created_ts = dt.timestamp()
                except Exception:
                    pass

            # 时间过滤
            if created_ts is not None:
                if from_ts is not None and created_ts < from_ts:
                    continue
                if to_ts is not None and created_ts > to_ts:
                    continue

            # 统计 user 消息数作为 turn 数
            turns = 0
            try:
                with open(fpath, "r", encoding="utf-8") as sf:
                    for line in sf:
                        if '"role":"user"' in line:
                            turns += 1
            except Exception:
                pass

            session_name = entry[:-6]  # strip .jsonl
            session_names.add(session_name)

            if model not in per_model:
                per_model[model] = {"sessions": 0, "turns": 0, "input": 0, "output": 0, "calls": 0, "cache": 0, "no_usage": True}
            per_model[model]["sessions"] += 1
            per_model[model]["turns"] += turns
            per_model[model]["calls"] += turns  # chat turns ≈ model API calls

    return {
        "per_model": per_model,
        "session_names": session_names,
        "total_sessions": len(session_names),
        "source_label": "桌面版",
    }


class ReasonixAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "reasonix"

    @staticmethod
    def display_name() -> str:
        return "Reasonix"

    @staticmethod
    def detect() -> bool:
        """检测 CLI 或桌面版任一存在即可"""
        return _reasonix_cli_usage_path() is not None or _reasonix_desktop_data_dir() is not None

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        # ── 1. CLI 版：从 usage.jsonl 读取（含精确 token 数据）──
        cli_path = _reasonix_cli_usage_path()
        cli_per_model: dict[str, dict] = {}
        cli_sessions: set[str] = set()
        cli_total_records = 0

        if cli_path:
            try:
                with open(cli_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                        except json.JSONDecodeError:
                            continue

                        cli_total_records += 1

                        # 时间过滤（ts 是 epoch 毫秒）
                        rec_ts = rec.get("ts", 0) / 1000.0
                        if from_ts is not None and rec_ts < from_ts:
                            continue
                        if to_ts is not None and rec_ts > to_ts:
                            continue

                        model = rec.get("model", "unknown")
                        cli_sessions.add(rec.get("session", ""))

                        if model not in cli_per_model:
                            cli_per_model[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                        cli_per_model[model]["input"] += rec.get("promptTokens", 0)
                        cli_per_model[model]["output"] += rec.get("completionTokens", 0)
                        cli_per_model[model]["cache"] += rec.get("cacheHitTokens", 0)
                        cli_per_model[model]["calls"] += 1
            except Exception as e:
                return AgentData(
                    name="reasonix", display_name="Reasonix",
                    stats={}, raw=f"Reasonix (CLI): 读取失败 — {e}"
                )

        # ── 2. 桌面版：从 session JSONL 统计（无 token 数据）──
        desktop_data = _reasonix_desktop_sessions(from_ts=from_ts, to_ts=to_ts)
        desktop_per_model = desktop_data["per_model"]
        desktop_sessions = desktop_data["session_names"]

        # ── 3. 合并 CLI + 桌面版数据 ──
        all_sessions = cli_sessions | desktop_sessions

        # 合并 per_model：以 CLI 数据为准（有 token），桌面版补充会话数
        merged: dict[str, dict] = {}
        for model, md in cli_per_model.items():
            merged[model] = dict(md)
            merged[model].setdefault("desktop_sessions", 0)
            merged[model].setdefault("desktop_turns", 0)
        for model, md in desktop_per_model.items():
            if model in merged:
                merged[model]["desktop_sessions"] = md.get("sessions", 0)
                merged[model]["desktop_turns"] = md.get("turns", 0)
                # 桌面版 turns 也算入总 calls（保守估计：1 turn ≈ 1 API 调用）
                merged[model]["calls"] = merged[model].get("calls", 0) + md.get("turns", 0)
            else:
                merged[model] = {
                    "input": 0,
                    "output": 0,
                    "calls": md.get("turns", 0),
                    "cache": 0,
                    "desktop_sessions": md.get("sessions", 0),
                    "desktop_turns": md.get("turns", 0),
                    "no_usage": True,  # 标记：无精确 token 数据
                }

        # 无数据时的处理
        if not merged:
            if cli_total_records > 0:
                msg = f"Reasonix: 指定时间范围内无有效数据（CLI usage.jsonl 共 {cli_total_records} 条记录）"
                if desktop_data["total_sessions"] > 0:
                    msg += f"，桌面版 {desktop_data['total_sessions']} 个会话也无匹配"
                return AgentData(
                    name="reasonix", display_name="Reasonix",
                    stats={}, raw=msg
                )
            if desktop_data["total_sessions"] > 0:
                return AgentData(
                    name="reasonix", display_name="Reasonix",
                    stats={}, raw=f"Reasonix: 指定时间范围内无有效数据（桌面版 {desktop_data['total_sessions']} 个会话均不匹配）"
                )
            has_any_source = cli_path is not None or _reasonix_desktop_data_dir() is not None
            return AgentData(
                name="reasonix", display_name="Reasonix",
                stats={}, raw="Reasonix: usage.jsonl 中无有效数据" if cli_path else "Reasonix: 未找到 usage.jsonl 或桌面版数据"
            )

        # ── 4. 构建输出 ──
        total_calls = sum(d.get("calls", 0) for d in merged.values())
        total_input = sum(d.get("input", 0) for d in merged.values())
        total_output = sum(d.get("output", 0) for d in merged.values())
        total_cache = sum(d.get("cache", 0) for d in merged.values())
        total_desktop_sessions = sum(d.get("desktop_sessions", 0) for d in merged.values())

        models_sorted = sorted(merged.keys())

        per_model_list = []
        has_token_data = any(d.get("input", 0) + d.get("output", 0) + d.get("cache", 0) > 0 for d in merged.values())

        for mn in models_sorted:
            md = merged[mn]
            entry = {
                "model": mn,
                "input": md.get("input", 0),
                "output": md.get("output", 0),
                "calls": md.get("calls", 0),
                "cache": md.get("cache", 0),
            }
            if md.get("no_usage"):
                entry["token_mode"] = "total"  # 无法区分入/出
                entry["input"] = 0
                entry["output"] = 0
                entry["cache"] = 0
            per_model_list.append(entry)

        # 构建 footer 信息
        footer_parts = []
        if cli_sessions:
            footer_parts.append(f"  CLI: {len(cli_sessions)} 个会话 ({cli_total_records} 次模型调用)")
        if desktop_sessions:
            footer_parts.append(f"  桌面版: {len(desktop_sessions)} 个会话 ({total_desktop_sessions} 次加载)")
            if not has_token_data:
                footer_parts.append("  ⚠️ 桌面版不持久化 token 用量，仅统计会话/轮次数")
        if total_cache > 0:
            cache_rate = (total_cache / (total_input + total_cache) * 100) if (total_input + total_cache) > 0 else 0
            footer_parts.insert(0, f"  缓存命中率: {cache_rate:.1f}%")

        raw = _build_aligned_raw("Reasonix", per_model_list, has_context=False,
                                 extra_footer="\n".join(footer_parts) if footer_parts else None)
        stats = {
            "model": ", ".join(models_sorted),
            "input_tokens": total_input,
            "output_tokens": total_output,
            "cache_read": total_cache,
            "total_tokens": total_input + total_output,
            "api_calls": total_calls,
            "session_count": len(all_sessions),
            "cli_sessions": len(cli_sessions),
            "desktop_sessions": len(desktop_sessions),
        }

        return AgentData(name="reasonix", display_name="Reasonix",
                         stats=stats, raw=raw, per_model=per_model_list)

# ═══════════════════════════════════════════════════
#  DeepSeek TUI
# ═══════════════════════════════════════════════════

def _find_deepseek_tui_sessions() -> Optional[str]:
    """获取 DeepSeek TUI sessions 目录"""
    p = os.path.join(os.path.expanduser("~"), ".deepseek", "sessions")
    return p if os.path.isdir(p) else None


class DeepSeekTUIAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "deepseek-tui"

    @staticmethod
    def display_name() -> str:
        return "DeepSeek TUI"

    @staticmethod
    def detect() -> bool:
        d = _find_deepseek_tui_sessions()
        if not d:
            return False
        # 检查是否有 .json 会话文件
        for fname in os.listdir(d):
            if fname.endswith(".json"):
                return True
        return False

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        sessions_dir = _find_deepseek_tui_sessions()
        if not sessions_dir:
            return AgentData(
                name="deepseek-tui", display_name="DeepSeek TUI",
                stats={}, raw="DeepSeek TUI: 未找到 sessions 目录"
            )

        per_model_data: dict[str, dict] = {}
        total_sessions = 0
        total_tool_calls = 0
        total_cost_usd = 0.0
        total_cost_cny = 0.0

        try:
            for fname in sorted(os.listdir(sessions_dir)):
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(sessions_dir, fname)
                if not os.path.isfile(fpath):
                    continue
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    continue

                metadata = data.get("metadata")
                if not metadata:
                    continue

                # 时间过滤
                created_str = metadata.get("created_at", "")
                try:
                    created_ts = datetime.fromisoformat(created_str.replace("Z", "+00:00")).timestamp()
                except (ValueError, TypeError):
                    created_ts = None

                if from_ts is not None and created_ts is not None and created_ts < from_ts:
                    continue
                if to_ts is not None and created_ts is not None and created_ts > to_ts:
                    continue

                model = metadata.get("model", "unknown")
                tokens = metadata.get("total_tokens", 0) or 0

                # 统计工具调用次数（messages 中 type=tool_use）
                tool_count = 0
                for msg in data.get("messages", []):
                    for item in msg.get("content", []):
                        if isinstance(item, dict) and item.get("type") == "tool_use":
                            tool_count += 1

                # 提取费用
                cost = metadata.get("cost", {}) or {}
                session_cost_usd = cost.get("session_cost_usd", 0) or 0
                session_cost_cny = cost.get("session_cost_cny", 0) or 0

                if model not in per_model_data:
                    per_model_data[model] = {"tokens": 0, "sessions": 0, "tool_calls": 0,
                                              "cost_usd": 0.0, "cost_cny": 0.0}
                per_model_data[model]["tokens"] += tokens
                per_model_data[model]["sessions"] += 1
                per_model_data[model]["tool_calls"] += tool_count
                per_model_data[model]["cost_usd"] += session_cost_usd
                per_model_data[model]["cost_cny"] += session_cost_cny
                total_sessions += 1
                total_tool_calls += tool_count
                total_cost_usd += session_cost_usd
                total_cost_cny += session_cost_cny
        except Exception as e:
            return AgentData(
                name="deepseek-tui", display_name="DeepSeek TUI",
                stats={}, raw=f"DeepSeek TUI: 读取失败 — {e}"
            )

        if not per_model_data:
            return AgentData(
                name="deepseek-tui", display_name="DeepSeek TUI",
                stats={}, raw="DeepSeek TUI: 尚无会话记录"
            )

        models_sorted = sorted(per_model_data.keys())
        per_model_list = []
        raw_lines = ["📊 DeepSeek TUI"]
        total_tok = 0
        total_cnt = 0
        model_count = 0

        for mn in models_sorted:
            md = per_model_data[mn]
            ts = md["tokens"]
            cnt = md["sessions"]
            per_model_list.append({"model": mn, "input": ts, "output": 0,
                                    "calls": cnt, "cache": 0})
            if ts > 0 or cnt > 0:
                parts = [f"总计 {fmt_num(ts)}"] if ts > 0 else []
                parts.append(f"{cnt} 轮会话")
                if md["tool_calls"] > 0:
                    parts.append(f"工具调用 {md['tool_calls']} 次")
                if md["cost_cny"] > 0:
                    parts.append(f"≈¥{md['cost_cny']:.4f}")
                raw_lines.append(f"  {mn} | {' | '.join(parts)}")
                model_count += 1
            total_tok += ts
            total_cnt += cnt

        if model_count > 1:
            raw_lines.append(f"  {'─' * 36}")
            cost_part = f" | ≈¥{total_cost_cny:.4f}" if total_cost_cny > 0 else ""
            raw_lines.append(f"  合计 | 总计 {fmt_num(total_tok)} | {total_cnt} 轮会话{cost_part}")

        raw = "\n".join(raw_lines)
        stats = {
            "model": ", ".join(models_sorted),
            "total_tokens": total_tok,
            "session_count": total_sessions,
            "tool_calls": total_tool_calls,
            "cost_usd": round(total_cost_usd, 6),
            "cost_cny": round(total_cost_cny, 4),
        }

        return AgentData(name="deepseek-tui", display_name="DeepSeek TUI",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  Agent 注册表
# ═══════════════════════════════════════════════════

ALL_AGENTS: list[type[BaseAgent]] = [
    ClaudeCodeAgent,
    CodeXAgent,
    HermesAgent,
    OpenClawAgent,
    ReasonixAgent,
    DeepSeekTUIAgent,
]


def detect_installed() -> list[type[BaseAgent]]:
    return [cls for cls in ALL_AGENTS if cls.detect()]


def get_agent(name: str) -> BaseAgent:
    for cls in ALL_AGENTS:
        if cls.name() == name.lower().strip():
            return cls()
    raise ValueError(f"不支持的 Agent: {name}")


# ═══════════════════════════════════════════════════
#  全部统计 (--all)
# ═══════════════════════════════════════════════════

def show_all(*, from_ts: float = None, to_ts: float = None):
    """显示本机所有 Agent 的统计"""
    snapshot.show_all(ALL_AGENTS, detect_installed, _snapshot_helpers(), from_ts=from_ts, to_ts=to_ts)

# ═══════════════════════════════════════════════════
#  CLI 入口
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="token-stats — 选个 Agent 看它的 token 消耗",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
命令大全:
  基础:
    token-stats                       交互式菜单选择 Agent → 查看统计
    token-stats -a <name>             直接指定 Agent: hermes/claude-code/codex/openclaw
    token-stats -v / --version        显示版本号
    token-stats -a <name> --detail    详细模式（同默认）
    token-stats -a <name> --now       当前快照（同默认）

  快速时间段:
    token-stats -a <name> -t / --today     今日统计
    token-stats -a <name> --yesterday 昨日统计
    token-stats -a <name> --week      本周统计（周一起）
    token-stats -a <name> --last-7d   最近 7 天
    token-stats -a <name> -m / --month 本月统计
    token-stats -a <name> -y / --year 本年统计
    token-stats -a <name> --from 2025-01-01 --to 2025-01-31  自定义时间段

  对比:
    token-stats -a <name> --compare --a today --b yesterday
        快捷标签对比
    token-stats -a <name> --compare --a 2025-01-01~2025-01-07 --b 2025-01-08~2025-01-14
        自定义时间段对比
    标签支持: today / yesterday / this-week / last-week / this-month / last-month / this-year / last-year / YYYY-MM-DD / YYYY-MM-DD~YYYY-MM-DD

  导出:
    token-stats -a <name> -e / --export    导出当前统计（交互式选目录和格式）
    token-stats -a <name> -t -e            导出今日统计

  实时监控:
    token-stats -a <name> -w / --watch     实时监控，默认 5 秒刷新 (Ctrl+C 停止)
    token-stats -a <name> -w 10            自定义间隔秒数
    停止后自动展示监控时间段内的完整统计数据（模型、输入、输出、缓存、调用次数）

  多 Agent:
    token-stats --all                 查看本机所有 Agent 统计
    token-stats --list-backends       列出已安装的 Agent

  安装与更新:
    python3 token-stats.py setup                   安装到 ~/.token-stats，并将 ~/.token-stats/bin 加入 PATH
    token-stats update                             更新（ClawHub 用户）
    token-stats --uninstall                        删除全局命令、安装目录并自动清理 PATH
        """,
    )
    parser.add_argument("-v", "--version", action="store_true", help="显示版本号")
    parser.add_argument("-l", "--list-backends", action="store_true", help="列出本机已安装的 Agent")
    parser.add_argument("--list-prices", action="store_true", help="列出 model_prices.toml 中已配置价格的模型")
    parser.add_argument("-a", "--agent", help="直接指定 Agent: claude-code/codex/hermes/openclaw/reasonix/deepseek-tui")

    def _positive_int(val):
        ival = int(val)
        if ival < 1:
            raise argparse.ArgumentTypeError(f"监控间隔必须 ≥1 秒，收到: {val}")
        return ival

    parser.add_argument("-w", "--watch", nargs="?", type=_positive_int, const=5, default=None, metavar="秒",
                        help="实时监控模式（默认每 5 秒轮询）")
    parser.add_argument("setup_pos", nargs="?", const=True, help=argparse.SUPPRESS)

    # 时间段
    parser.add_argument("-t", "--today", action="store_true", help="今日统计")
    parser.add_argument("--yesterday", action="store_true", help="昨日统计")
    parser.add_argument("--week", action="store_true", help="本周统计")
    parser.add_argument("--last-7d", action="store_true", help="最近 7 天统计")
    parser.add_argument("-m", "--month", action="store_true", help="本月统计")
    parser.add_argument("-y", "--year", action="store_true", help="本年统计")
    parser.add_argument("--from", dest="from_date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", help="结束日期 (YYYY-MM-DD)")

    # 功能
    parser.add_argument("-e", "--export", nargs="?", const=True, default=None, metavar="目录",
                        help="导出统计（交互式选择目录和格式）")
    parser.add_argument("--compare", action="store_true", help="对比模式")
    parser.add_argument("--a", help="对比时间段 A（today/yesterday/this-week/last-week/日期/日期段）")
    parser.add_argument("--b", help="对比时间段 B")
    parser.add_argument("--detail", action="store_true", help="详细信息模式")
    parser.add_argument("--now", action="store_true", help="当前快照（同默认）")
    parser.add_argument("--all", action="store_true", help="查看本机所有 Agent 统计")
    parser.add_argument("--setup", action="store_true", help="安装到 ~/.token-stats，创建 ~/.token-stats/bin/token-stats 并自动加入 PATH")
    parser.add_argument("--uninstall", action="store_true", help="删除全局命令、安装目录并清理 PATH")
    parser.add_argument("--update", action="store_true", help="通过 clawhub update 更新到最新版本")
    parser.add_argument("--install-dir", default=None, help="指定安装目录（默认 ~/.token-stats）")

    args = parser.parse_args()

    # 兼容旧用法：token-stats setup / uninstall / update → 当作对应 flag
    if args.setup_pos is True or args.setup_pos == "setup":
        args.setup = True
    if args.setup_pos == "uninstall":
        args.uninstall = True
    if args.setup_pos == "update":
        args.update = True

    # ── version ──
    if args.version:
        print(f"token-stats v{VERSION}")
        return

    # ── setup ──
    if args.setup:
        installer.run_setup(PROJECT_ROOT, args.install_dir, _scan_all_agent_paths, _save_agent_paths)
        return

    # ── uninstall ──
    if args.uninstall:
        installer.run_uninstall(PROJECT_ROOT, args.install_dir, CONFIG_DIR)
        return

    # ── update ──
    if getattr(args, 'update', False):
        installer.run_update(PROJECT_ROOT, VERSION, args.install_dir)
        return

    # ── list-backends ──
    if args.list_backends:
        print("\n本机已安装的 AI 助手：")
        for cls in ALL_AGENTS:
            ok = "✅" if cls.detect() else "❌"
            print(f"  {ok} {cls.display_name()}")
        print()
        return

    # ── list-prices ──
    if args.list_prices:
        prices = _load_model_prices()
        if not prices:
            print("\n未找到 model_prices.toml 或无有效配置\n")
            return
        # 按 provider 分组
        groups: dict[str, list[tuple[str, dict]]] = {}
        for model, cfg in prices.items():
            if not isinstance(cfg, dict):
                continue
            provider = cfg.get("provider", "Other")
            groups.setdefault(provider, []).append((model, cfg))
        print(f"\n模型价格配置 (model_prices.toml) — {len(prices)} 个模型\n")
        for provider in sorted(groups.keys()):
            print(f"── {provider} ──")
            for model, cfg in groups[provider]:
                cur = cfg.get("currency", "CNY")
                sym = "¥" if cur == "CNY" else "$"
                no_cache = cfg.get("input_no_cache_price", "-")
                cache_p = cfg.get("input_cache_price", "-")
                out_p = cfg.get("output_price", "-")
                note = cfg.get("note", "")
                parts = [
                    f"  {model}",
                    f"输入 {sym}{no_cache}" if no_cache != "-" and no_cache != 0 else None,
                    f"缓存命中 {sym}{cache_p}" if cache_p != "-" and cache_p != 0 else None,
                    f"输出 {sym}{out_p}",
                ]
                line = " | ".join(p for p in parts if p)
                if note:
                    line += f"  ({note})"
                print(line)
            print()
        print("  价格单位: 每百万 (1M) tokens | USD 模型展示按 $，实际计算按 ¥7.25 换算")
        print()
        return

    # ── 解析时间段参数 ──
    from_ts = None
    to_ts = None

    if args.from_date:
        if args.to_date:
            from_ts, _ = parse_date(args.from_date)
            _, to_ts = parse_date(args.to_date)
        else:
            from_ts, _ = parse_date(args.from_date)
            to_ts = from_ts + 86399  # end of that day
    elif args.to_date and not args.from_date:
        _, to_ts = parse_date(args.to_date)
        # no from_ts means "from beginning"

    if args.today:
        from_ts, to_ts = parse_time_label("today")
    elif args.yesterday:
        from_ts, to_ts = parse_time_label("yesterday")
    elif args.week:
        from_ts, to_ts = parse_time_label("this-week")
    elif args.last_7d:
        from_ts, to_ts = parse_time_label("last-7d")
    elif args.month:
        from_ts, to_ts = parse_time_label("this-month")
    elif args.year:
        from_ts, to_ts = parse_time_label("this-year")

    # 导出目录：-e /path 时直接使用，否则 None（函数内会交互式询问）
    export_dir = args.export if isinstance(args.export, str) else None

    # ── Helper: collect agent data ──
    def _collect_agent_data(agents_list):
        results = []
        for agent in agents_list:
            try:
                print(f"  ⏳ 正在收集 {agent.display_name()} 数据...", end="\r", flush=True)
                data = agent.collect(from_ts=from_ts, to_ts=to_ts)
                print(" " * 40, end="\r")
                results.append((agent, data))
            except Exception as e:
                print(f"❌ {agent.display_name()}: {e}")
        return results

    # ── --all (所有 Agent) ──
    if args.all:
        if args.watch is not None:
            print("⚠️ --watch 仅支持单个 Agent，请使用 -a <name> --watch")
            return
        if args.compare:
            print("⚠️ --compare 仅支持单个 Agent")
            return
        installed = detect_installed()
        if not installed:
            print("❌ 本机未检测到任何支持的 AI 助手")
            return
        agents = [cls() for cls in ALL_AGENTS if cls.detect()]
        if args.export:
            results = _collect_agent_data(agents)
            if results:
                export_multi(results, **_export_helpers(), is_year=args.year, from_ts=from_ts, to_ts=to_ts,
                             export_dir=export_dir)
        else:
            show_all(from_ts=from_ts, to_ts=to_ts)
        return

    # ── 选择 Agent(s) ──
    installed = detect_installed()
    if not installed:
        print("❌ 本机未检测到任何支持的 AI 助手")
        print("   支持的 Agent: Hermes, Claude Code, CodeX, OpenClaw")
        print("   请先使用并运行一个 Agent 后再来查看统计。")
        return

    if args.agent:
        backends = [b.strip() for b in args.agent.split(',')]
        agents = []
        for name in backends:
            try:
                agents.append(get_agent(name))
            except ValueError as e:
                print(f"❌ {e}")
                print(f"   可选: {', '.join(cls.name() for cls in ALL_AGENTS)}")
                return
        if len(agents) > 1:
            if args.watch is not None:
                print("⚠️ --watch 仅支持单个 Agent")
                return
            if args.compare:
                print("⚠️ --compare 仅支持单个 Agent")
                return
            results = _collect_agent_data(agents)
            if args.export:
                export_multi(results, **_export_helpers(), is_year=args.year, from_ts=from_ts, to_ts=to_ts,
                             export_dir=export_dir)
            else:
                for agent, data in results:
                    print(f"\n{'─'*50}")
                    print(f"  {agent.display_name()}")
                    print(f"{'─'*50}")
                    print(data.raw)
                if len(results) > 1:
                    gti = gto = gtc = gtca = 0
                    gt_costs: dict[str, float] = {}
                    for _, d in results:
                        for pm in (d.per_model or []):
                            if _skip_model(pm):
                                continue
                            inp = pm.get("input", 0) or 0
                            out = pm.get("output", 0) or 0
                            cache = pm.get("cache", 0) or 0
                            gti += inp
                            gto += out
                            gtc += cache
                            gtca += pm.get("calls", 0) or 0
                            pc = None if pm.get("token_mode") == "total" else _get_model_price(pm.get("model", ""))
                            if pc:
                                cur = pc.get('currency', 'CNY')
                                gt_costs[cur] = gt_costs.get(cur, 0.0) + _calc_cost(inp, out, cache, pc)
                    gtt = gti + gto
                    print(f"\n{'═'*50}")
                    print("  全部 Agent 总计")
                    parts = f"  入 {fmt_num(gti)} | 出 {fmt_num(gto)} | {_fmt_cache_val(gtc, gti)} | 总计/+缓存 {fmt_num(gtt)}/{fmt_num(gtt + gtc)} | 调用 {gtca} 次"
                    gt_cost_str = _fmt_total_cost(gt_costs)
                    if gt_cost_str:
                        parts += f" | {gt_cost_str} (仅供参考)"
                    print(parts)
            return
        agent = agents[0]
    elif len(installed) == 1:
        agent = installed[0]()
        print(f"\n（本机仅安装了 {agent.display_name()}，直接显示统计）")
    else:
        agent = show_menu(installed, allow_all=args.watch is None)
        if agent == "all":
            show_all(from_ts=from_ts, to_ts=to_ts)
            return
        if agent is None:
            print("再见 👋")
            return

    # ── --compare (对比) ──
    if args.compare:
        a_label = args.a
        b_label = args.b
        if not a_label or not b_label:
            print("❌ --compare 需要 --a 和 --b 参数")
            print("   示例: token-stats -a hermes --compare --a today --b yesterday")
            return
        compare.run_compare(agent, a_label, b_label, _compare_helpers())
        return

    # ── --watch (实时监控) ──
    if args.watch is not None:
        agent.watch(args.watch)
        return

    # ── 收集并展示 ──
    # 年度导出时跳过初始全量收集，由 export_interactive 统一收集月度数据
    if args.export and args.year:
        data = None
    else:
        try:
            print("  ⏳ 正在收集数据...", end="\r", flush=True)
            data = agent.collect(from_ts=from_ts, to_ts=to_ts)
            print(" " * 30, end="\r")  # clear progress line
            print()
            print(data.raw)
            print()
        except Exception as e:
            print(f"❌ 获取 {agent.display_name()} 统计失败: {e}")
            return

    # ── --export (导出) ──
    if args.export:
        export_interactive(data, agent, **_export_helpers(), from_ts=from_ts, to_ts=to_ts,
                            is_year=args.year, export_dir=export_dir)

    # --detail 在下一步也可能有用，但当前 collect() 已含 per_model 详情
    # detail 主要用于 watch/collect 输出内容更丰富，当前 collect 实现已包含
    # 后续可通过 stats 或 per_model 扩展
