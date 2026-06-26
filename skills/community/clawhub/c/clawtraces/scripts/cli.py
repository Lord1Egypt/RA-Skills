#!/usr/bin/env python3
# FILE_META
# INPUT:  CLI flags (--limit, --since, --all) or no args (default: list 20)
# OUTPUT: interactive terminal flow: list → select → scan → submit
# POS:    skill scripts — standalone CLI entry point, depends on all other scripts
# MISSION: Pure CLI interactive tool: list sessions, pick by number, auto-process and submit.
"""Interactive CLI tool for ClawTraces data collection.

Simplified flow: list sessions → pick by number → auto-process → submit.

Usage:
    python cli.py        # 默认过滤模型不符的 session
    python cli.py --all  # 显示全部（含模型不符）
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))

from lib.auth import (
    get_stored_key, check_key_valid, get_server_url,
    send_code, verify_code, save_key,
)
from lib.paths import get_default_output_dir
from lib.session_index import find_openclaw_sessions_dirs
from pathlib import Path

from lib.adapters.openclaw._list_ui import list_qualifying_sessions
import scan_adapter
from submit import submit_all, query_count, fetch_recollections, resubmit_one
from query import query_submissions
from sync import sync_manifest_from_server
from workspace_bundle import discover_workspaces, create_workspace_bundle, upload_workspace

DEFAULT_OUTPUT_DIR = get_default_output_dir()
PAGE_SIZE = 20

DOMAIN_LABELS = {
    "development": "软件开发",
    "system_admin": "系统运维",
    "data_analysis": "数据分析",
    "research": "研究检索",
    "content_creation": "内容创作",
    "communication": "通信消息",
    "media_processing": "多媒体处理",
    "automation": "工作流编排",
    "monitoring": "系统监控",
    "scheduling": "日程管理",
    "knowledge_mgmt": "知识管理",
    "finance": "金融量化",
    "crm": "客户运营",
}

# ── Helpers ──────────────────────────────────────────────────


import unicodedata


def _display_width(text: str) -> int:
    """Calculate terminal display width of a string.

    CJK characters and most emoji occupy 2 columns; ASCII occupies 1.
    """
    w = 0
    for ch in text:
        cat = unicodedata.east_asian_width(ch)
        w += 2 if cat in ("W", "F") else 1
    return w


def _print_header(text: str):
    print(f"\n{'━' * 56}")
    print(f"  {text}")
    print(f"{'━' * 56}")


def _prompt(message: str, default: str = "") -> str:
    if default:
        raw = input(f"  {message} [{default}]: ").strip()
        return raw if raw else default
    return input(f"  {message}: ").strip()


def _confirm(message: str, default_yes: bool = True) -> bool:
    suffix = "[Y/n]" if default_yes else "[y/N]"
    raw = input(f"  {message} {suffix}: ").strip().lower()
    if not raw:
        return default_yes
    return raw in ("y", "yes")


def _parse_selection(raw: str, max_index: int, default_count: int = 5) -> list[int] | None:
    """Parse user selection input into a list of 1-based indices.

    Supports: "1,3,5", "1-5", "1,3-5,8", empty (= first default_count).
    Returns None on invalid input.
    """
    raw = raw.strip().lower()
    if not raw:
        return list(range(1, min(default_count, max_index) + 1))

    indices = set()
    for part in raw.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            bounds = part.split("-", 1)
            try:
                start, end = int(bounds[0]), int(bounds[1])
            except ValueError:
                return None
            if start < 1 or end > max_index or start > end:
                return None
            indices.update(range(start, end + 1))
        else:
            try:
                n = int(part)
            except ValueError:
                return None
            if n < 1 or n > max_index:
                return None
            indices.add(n)

    return sorted(indices) if indices else None


# ── Phase 0: Menu ────────────────────────────────────────────


def show_menu() -> str:
    """Display main menu and return selected mode."""
    _print_header("请选择操作")
    print()
    print("  1. 采集提交数据")
    print("  2. 查看提交记录")
    print("  3. 提交 Harness")
    print("  4. 自动重新补录")
    print()

    while True:
        raw = _prompt("选择", default="1")
        if raw in ("1", "2", "3", "4"):
            return {"1": "submit", "2": "query", "3": "workspace", "4": "recollect"}[raw]
        print("  ⚠️  请输入 1、2、3 或 4")


# ── Phase 1: Auth ────────────────────────────────────────────


def ensure_auth() -> tuple[str, str]:
    """Ensure user is authenticated. Returns (server_url, api_key)."""
    print("\n🔑 检查认证...")
    server_url = get_server_url()
    key = get_stored_key()

    if key and check_key_valid(server_url, key):
        print(f"  ✅ 已认证 (key: {key[:12]}...)")
        return server_url, key

    print("  ⚠️  未认证，需要登录")

    while True:
        phone = _prompt("请输入手机号（11位）")
        if not phone:
            continue
        result = send_code(server_url, phone)
        if "error" in result:
            print(f"  ❌ {result['error']}")
            continue
        print("  📱 验证码已发送")
        break

    while True:
        code = _prompt("请输入验证码")
        if not code:
            continue
        result = verify_code(server_url, phone, code)
        if "error" in result:
            print(f"  ❌ {result['error']}")
            if not _confirm("重试?"):
                print("认证取消。")
                sys.exit(1)
            continue
        key = result.get("key", "")
        if key:
            save_key(key)
            print(f"  ✅ 认证成功 (key: {key[:12]}...)")
            return server_url, key
        print("  ❌ 服务端未返回 key")
        sys.exit(1)


# ── Phase 2: Env Check ───────────────────────────────────────


def check_env() -> bool:
    """Run environment check. Returns True if ready."""
    print("\n📡 检查环境...")
    script = os.path.join(os.path.dirname(__file__), "env_check.py")

    try:
        proc = subprocess.run(
            [sys.executable, script],
            capture_output=True, text=True, timeout=30,
        )
        result = json.loads(proc.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as e:
        print(f"  ⚠️  环境检查失败: {e}")
        return True

    if result.get("parse_error"):
        print(f"  ❌ openclaw.json 解析失败: {result['parse_error']}")
        print("  请手动检查配置文件后重试。")
        sys.exit(1)

    if result.get("changed"):
        print("  🔧 已自动修复配置:")
        for fix in result.get("fixes", []):
            print(f"     - {fix}")
        print("\n  ⚠️  需要重启 OpenClaw 使配置生效。")
        print("  请运行: openclaw gateway restart")
        print("  cache-trace 仅记录重启后的新对话，请使用一段时间后再来采集。")
        return False
    else:
        print("  ✅ 环境正常")
        return True


# ── Phase 3: List & Select ──────────────────────────────────


def _build_row(i: int, s: dict, status_tags: dict) -> tuple[str, ...]:
    """Build a display row tuple for one session."""
    start = s.get("started_at") or ""
    end = s.get("ended_at") or ""
    start_date, end_date = start[:10], end[:10]
    start_hm, end_hm = start[11:16], end[11:16]
    if start_date and end_date and start_date == end_date:
        time_str = f"{start_date[5:]} {start_hm} ~ {end_hm}"
    elif start_date and end_date:
        time_str = f"{start_date[5:]} {start_hm} ~ {end_date[5:]} {end_hm}"
    else:
        time_str = start[:16] or end[:16]

    sid = s.get("session_id") or ""
    short_sid = f"{sid[:8]}..{sid[-4:]}" if len(sid) > 12 else sid

    model = s.get("model") or ""
    for prefix in ("anthropic/", "openai/"):
        if model.startswith(prefix):
            model = model[len(prefix):]
            break
    if len(model) > 20:
        model = model[:18] + ".."

    turns = str(s.get("turns", ""))
    if s.get("has_compaction"):
        turns = f"{turns}📦"

    status = status_tags.get(s.get("status") or "", "")
    topic = (s.get("topic") or "").replace("\n", " ")
    return (str(i), short_sid, time_str, model, turns, status, topic)


def list_and_select(
    sessions_dirs: list[str],
    output_dir: str,
    show_all: bool = False,
) -> list[str]:
    """List sessions with pagination, let user pick by number. Returns selected session_ids."""

    sessions = list_qualifying_sessions(sessions_dirs, output_dir)

    # Default: hide model_mismatch sessions
    if not show_all:
        sessions = [s for s in sessions if s.get("status") != "model_mismatch"]

    if not sessions:
        print("\n  没有可处理的对话记录。")
        return []

    STATUS_TAGS = {
        "active": "⚡正在活跃",
        "rejected": "🚫预审被拒",
        "model_mismatch": "⚠️ 模型不符",
        "cron_task": "🤖自动任务",
        "turns_too_low": "⛔轮次不足",
        "tool_use_too_low": "⛔工具不足",
        "reasoning_too_low": "⛔推理不足",
        "no_cache_trace": "⛔缺 cache",
    }

    HEADERS = ("#", "Session", "时间", "模型", "轮次", "状态", "摘要")

    # Pre-build ALL rows for consistent column widths across pages
    all_rows = [_build_row(i, s, STATUS_TAGS) for i, s in enumerate(sessions, 1)]

    widths = [max(_display_width(h), max((_display_width(r[ci]) for r in all_rows), default=0))
              for ci, h in enumerate(HEADERS)]

    def _pad(text: str, width: int, right_align: bool = False) -> str:
        dw = _display_width(text)
        padding = width - dw
        if padding <= 0:
            return text
        return (" " * padding + text) if right_align else (text + " " * padding)

    def _fmt_row(cols: tuple[str, ...]) -> str:
        parts = [_pad(val, widths[ci], right_align=(ci == 0)) for ci, val in enumerate(cols)]
        return "  " + "  ".join(parts)

    header_line = _fmt_row(HEADERS)
    separator = "  " + "  ".join("─" * w for w in widths)

    # ── Paginated display + selection loop ──
    total = len(sessions)
    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE
    current_page = 0  # 0-based

    def _show_page(page: int):
        start = page * PAGE_SIZE
        end = min(start + PAGE_SIZE, total)
        page_label = f"第 {page + 1}/{total_pages} 页" if total_pages > 1 else ""
        _print_header(f"对话记录（共 {total} 条，已提交的不显示）{' — ' + page_label if page_label else ''}")
        print()
        print(header_line)
        print(separator)
        for row in all_rows[start:end]:
            print(_fmt_row(row))

    _show_page(current_page)

    # Selection loop with pagination
    while True:
        default_n = min(5, total)
        default_label = f"1-{default_n}" if default_n > 1 else "1"
        if total <= 5:
            hint = f"直接回车 = 处理全部 {total} 条"
        else:
            hint = f"直接回车 = 处理前 {default_n} 条"

        print()
        nav_parts = []
        if current_page > 0:
            nav_parts.append("p 上一页")
        if current_page < total_pages - 1:
            nav_parts.append("n 下一页")
        nav_parts.append("q 退出")
        print(f"  {hint}，输入序号，或 {' / '.join(nav_parts)}")
        print()

        raw = _prompt("选择", default=default_label)
        cmd = raw.strip().lower()

        if cmd == "n":
            if current_page < total_pages - 1:
                current_page += 1
                _show_page(current_page)
            else:
                print("  已经是最后一页")
            continue
        if cmd == "p":
            if current_page > 0:
                current_page -= 1
                _show_page(current_page)
            else:
                print("  已经是第一页")
            continue
        if cmd == "q":
            sys.exit(0)

        selected = _parse_selection(raw, total)
        if selected is not None:
            break
        print(f"  ⚠️  无效输入，请输入 1-{total} 之间的序号")

    selected_sessions = [sessions[i - 1] for i in selected]

    # Classify selected sessions by status
    HARD_BLOCKED = {
        "model_mismatch": "模型不符",
        "cron_task": "自动任务",
        "turns_too_low": "轮次不足",
        "tool_use_too_low": "工具不足",
        "reasoning_too_low": "推理不足",
        "no_cache_trace": "缺 cache",
    }
    FORCE_LABELS = {"active": "正在活跃", "rejected": "预审被拒"}

    processable = []
    force_candidates = []
    blocked_counts: dict[str, int] = {}

    for s in selected_sessions:
        st = s.get("status") or ""
        if st in HARD_BLOCKED:
            blocked_counts[st] = blocked_counts.get(st, 0) + 1
        elif st in FORCE_LABELS:
            force_candidates.append((s, FORCE_LABELS[st]))
        else:
            processable.append(s["session_id"])

    if blocked_counts:
        parts = [f"{HARD_BLOCKED[k]} {v} 条" for k, v in blocked_counts.items()]
        print(f"\n  ⚠️  跳过: {', '.join(parts)}")

    if force_candidates:
        # Only allow force-submit when user selected exactly one session
        if len(selected_sessions) == 1:
            s, label = force_candidates[0]
            sid = s.get("session_id", "")
            short_sid = f"{sid[:8]}..{sid[-4:]}" if len(sid) > 12 else sid
            topic = (s.get("topic") or "无主题").replace("\n", " ")[:40]
            print(f"\n  ⚠️  [{label}] {short_sid} {topic}")
            if _confirm("是否强制提交该对话？", default_yes=False):
                processable.append(s["session_id"])
                print(f"  ✅ 已加入强制提交")
            else:
                print(f"  已跳过")
        else:
            counts: dict[str, int] = {}
            for s, _ in force_candidates:
                st = s.get("status") or ""
                counts[st] = counts.get(st, 0) + 1
            parts = [f"{FORCE_LABELS[k]} {v} 条" for k, v in counts.items()]
            print(f"\n  ⚠️  跳过: {', '.join(parts)}（单条选择时可强制提交）")

    if processable:
        print(f"  已选择 {len(processable)} 条可处理记录")
    else:
        print("\n  所选对话全部无法处理。")

    return processable


# ── Phase 4: Scan & Convert ─────────────────────────────────


def do_scan(
    output_dir: str,
    session_ids: list[str],
) -> list[dict]:
    """Run the openclaw adapter for selected sessions. Returns emitted entries."""
    print(f"\n⚙️  处理 {len(session_ids)} 条对话...")

    result = scan_adapter.run(
        "openclaw",
        Path(output_dir),
        explicit_session_ids=set(session_ids),
    )
    emitted = result["emitted"]
    filtered = result["filtered"]

    if filtered:
        reasons: dict[str, int] = {}
        for f in filtered:
            r = f["reason"]
            reasons[r] = reasons.get(r, 0) + 1
        print(f"  {len(emitted)} 条通过，{len(filtered)} 条未通过:")
        for reason, count in reasons.items():
            print(f"     - {reason}: {count}")
    else:
        print(f"  {len(emitted)} 条全部通过")

    return emitted


# ── Phase 5: Submit ──────────────────────────────────────────


def do_submit(
    output_dir: str,
    server_url: str,
    key: str,
    session_ids: list[str],
) -> dict:
    """Submit trajectories for the given session_ids. Returns result dict."""
    if not session_ids:
        print("\n没有可提交的记录。")
        return {}

    filenames = [f"{sid}.trajectory.json" for sid in session_ids]

    print("\n📤 提交中...")
    result = submit_all(output_dir, server_url, key, filenames=filenames)

    success = result.get("success_count", 0)
    errors = result.get("error_count", 0)
    total = result.get("server_total", "?")

    status = f"✅ 本次提交 {success} 条"
    if errors:
        status += f"，{errors} 条失败"
    status += f"，累计已提交 {total} 条"
    print(f"\n{status}")

    daily_limit = result.get("daily_submission_limit", 0)
    total_limit = result.get("total_submission_limit", 0)
    if daily_limit > 0:
        print(f"   每日额度: {result.get('daily_count', '?')}/{daily_limit}")
    if total_limit > 0:
        print(f"   总额度: {total}/{total_limit}")

    return result


# ── Phase 6: Query ──────────────────────────────────────────


def do_query(server_url: str, key: str, output_dir: str):
    """Query and display previously submitted sessions with pagination.

    On entry, runs a full sweep of ``/submissions`` and merges server session_ids
    into the local manifest so future scans don't re-surface already-submitted
    sessions — even ones uploaded from another machine.
    """
    print("\n📊 查询提交记录...")

    sync_manifest_from_server(server_url, key, output_dir)

    page = 1
    while True:
        result = query_submissions(server_url, key, page=page, page_size=PAGE_SIZE)

        if "error" in result:
            print(f"  ❌ 查询失败: {result.get('message') or result['error']}")
            return

        items = result.get("items", [])
        total = result.get("total", 0)
        recollection_total = result.get("recollection_total", 0)
        total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE if total > 0 else 1

        if not items and page == 1:
            print("\n  暂无提交记录。")
            return

        HEADERS = ("#", "标题", "领域", "模型", "轮次", "状态", "提交时间")

        rows = []
        for i, item in enumerate(items, (page - 1) * PAGE_SIZE + 1):
            title = (item.get("title") or "无标题").replace("\n", " ")
            if _display_width(title) > 30:
                # Truncate to ~28 display width
                truncated = ""
                w = 0
                for ch in title:
                    cw = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
                    if w + cw > 28:
                        break
                    truncated += ch
                    w += cw
                title = truncated + ".."

            domain_raw = item.get("domain") or ""
            domain = DOMAIN_LABELS.get(domain_raw, domain_raw)

            model = item.get("model") or ""
            for prefix in ("anthropic/", "openai/"):
                if model.startswith(prefix):
                    model = model[len(prefix):]
                    break
            if len(model) > 20:
                model = model[:18] + ".."

            turns = str(item.get("turns") or "")

            status = "需重采" if item.get("recollection_required") else ""

            submitted_at = item.get("submitted_at") or ""
            time_str = ""
            if submitted_at:
                # Server returns UTC ISO 8601 (e.g. "2026-04-10T03:20:15Z");
                # convert to local time for display.
                try:
                    from datetime import datetime, timezone
                    iso = submitted_at.replace("Z", "+00:00")
                    dt_utc = datetime.fromisoformat(iso)
                    if dt_utc.tzinfo is None:
                        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
                    time_str = dt_utc.astimezone().strftime("%Y-%m-%d %H:%M")
                except (ValueError, TypeError):
                    time_str = submitted_at[:16].replace("T", " ")

            rows.append((str(i), title, domain, model, turns, status, time_str))

        widths = [max(_display_width(h), max((_display_width(r[ci]) for r in rows), default=0))
                  for ci, h in enumerate(HEADERS)]

        def _pad(text: str, width: int, right_align: bool = False) -> str:
            dw = _display_width(text)
            padding = width - dw
            if padding <= 0:
                return text
            return (" " * padding + text) if right_align else (text + " " * padding)

        def _fmt_row(cols: tuple[str, ...]) -> str:
            parts = [_pad(val, widths[ci], right_align=(ci == 0)) for ci, val in enumerate(cols)]
            return "  " + "  ".join(parts)

        page_label = f"第 {page}/{total_pages} 页" if total_pages > 1 else ""
        recollect_suffix = f"，其中 {recollection_total} 条需重采" if recollection_total else ""
        _print_header(f"提交记录（共 {total} 条{recollect_suffix}）{' — ' + page_label if page_label else ''}")
        print()
        print(_fmt_row(HEADERS))
        print("  " + "  ".join("─" * w for w in widths))
        for row in rows:
            print(_fmt_row(row))

        if total_pages <= 1:
            return

        print()
        nav_parts = []
        if page > 1:
            nav_parts.append("p 上一页")
        if page < total_pages:
            nav_parts.append("n 下一页")
        nav_parts.append("q 退出")
        print(f"  {' / '.join(nav_parts)}")
        print()

        raw = _prompt("操作", default="q")
        cmd = raw.strip().lower()
        if cmd == "n" and page < total_pages:
            page += 1
        elif cmd == "p" and page > 1:
            page -= 1
        elif cmd == "q" or cmd == "":
            return
        else:
            print("  ⚠️  无效输入")


# ── Phase 6b: Recollect ─────────────────────────────────────


def _collect_local_session_ids(sessions_dirs: list[str]) -> set[str]:
    """Scan every sessions_dir and return the set of session_ids that have
    at least one local .jsonl file (live or .reset.* archived).

    Handles all OpenClaw filename shapes (plain / topic / fork-timestamped)
    by reading the ``{"type":"session","id":...}`` header; falls back to
    the filename stem for legacy files with no header.
    """
    from lib.parse.session_index import read_session_id_from_header

    local_ids: set[str] = set()
    for d in sessions_dirs:
        try:
            entries = os.listdir(d)
        except OSError:
            continue
        for fn in entries:
            if ".jsonl" not in fn:
                continue
            file_path = os.path.join(d, fn)
            sid = read_session_id_from_header(file_path)
            if not sid:
                # Legacy fallback for pre-header files: name may be
                # "<sid>.jsonl" or "<sid>.jsonl.reset.<...>".
                sid = fn.split(".jsonl", 1)[0]
            if sid:
                local_ids.add(sid)
    return local_ids


def do_recollect(
    server_url: str,
    key: str,
    sessions_dirs: list[str],
    output_dir: str,
):
    """Re-collect sessions the server has flagged for re-collection.

    Flow: pull /recollections → intersect with local JSONL files → confirm →
    scan+convert via explicit-session-ids (pipeline bypasses the "already
    submitted" filter in explicit mode) → force-resubmit each one.
    """
    print("\n🔄 查找需要重采的数据列表...")
    result = fetch_recollections(server_url, key)
    if "error" in result:
        print(f"  ❌ 拉取失败: {result.get('message') or result['error']}")
        return

    server_ids = result.get("session_ids", []) or []
    server_total = result.get("total", len(server_ids))

    if not server_ids:
        print("  ✅ 暂无待重采数据。")
        return

    local_ids = _collect_local_session_ids(sessions_dirs)
    available = [sid for sid in server_ids if sid in local_ids]
    skipped = server_total - len(available)

    print(f"  找到了 {server_total} 条标记为待重采的记录，本地有对应数据 {len(available)} 条")
    if skipped > 0:
        print(f"  （本地无对应 JSONL 的 {skipped} 条将被跳过）")

    if not available:
        print("\n  本地暂无可重采的数据。")
        return

    print()
    if not _confirm(
        f"本次有 {len(available)} 条数据可以自动重新采集，是否继续？",
        default_yes=False,
    ):
        print("  已取消。")
        return

    # Re-scan — explicit_session_ids bypasses pipeline's "already submitted" filter
    emitted = do_scan(output_dir, available)
    if not emitted:
        print("\n所选对话全部未通过重采筛选。")
        return

    passed_ids = [e["session_id"] for e in emitted]

    # Force re-upload each (overwrites server record, clears
    # recollection_required, stamps last_resubmit_at)
    print(f"\n📤 重新提交 {len(passed_ids)} 条...")
    success = 0
    failed = 0
    for sid in passed_ids:
        res = resubmit_one(sid, output_dir, server_url, key)
        if "error" in res:
            failed += 1
            if res.get("error") == "unauthorized":
                break
        else:
            success += 1

    status = f"\n✅ 重采完成: {success} 条成功"
    if failed:
        status += f"，{failed} 条失败"
    print(status)


# ── Phase 7: Workspace ─────────────────────────────────────


def do_workspace(
    server_url: str,
    key: str,
    output_dir: str,
    silent_skip: bool = False,
    allow_resubmit: bool = False,
) -> bool:
    """Bundle and upload workspace configuration.

    Returns True if workspace was submitted successfully, False otherwise.

    When ``allow_resubmit`` is True and a harness is already on record, the
    user is offered an explicit "覆盖提交" entry point (for when local config
    has changed). Gate / side-trigger call sites leave it False so they stay
    silent on already-submitted state.
    """
    # Check if already submitted
    count_result = query_count(server_url, key)
    if "error" in count_result:
        print(f"  ❌ 查询状态失败: {count_result.get('message') or count_result['error']}")
        return False

    if count_result.get("workspace_submitted"):
        if silent_skip:
            return True
        if not allow_resubmit:
            print("\n  ✅ Harness 已提交，无需重复操作。")
            return True
        print("\n  ✅ Harness 已提交。如本地配置已变化，可重新提交覆盖。")
        if not _confirm("是否重新提交？", default_yes=False):
            return True

    print("\n📦 提交 Harness...")

    # Discover workspaces
    workspaces = discover_workspaces(output_dir)
    if not workspaces:
        print("  ⚠️  未发现可用的 Harness（需要先提交过对话数据）。")
        return False

    # Bundle each workspace
    bundles: list[tuple[str, str, dict]] = []  # (agent_id, zip_path, scrub_report)
    for ws in workspaces:
        agent_id = ws["agent_id"]
        cwd = ws["cwd"]

        if not os.path.isdir(cwd):
            print(f"  ⚠️  工作区目录不存在，跳过: {cwd}")
            continue

        zip_path, scrub_report = create_workspace_bundle(agent_id, cwd, output_dir)
        if not zip_path:
            print(f"  ⚠️  未找到配置文件，跳过: {cwd}")
            continue

        zip_size = os.path.getsize(zip_path)
        print(f"  已打包: workspace-{agent_id}.zip ({zip_size} bytes)")
        bundles.append((agent_id, zip_path, scrub_report))

    if not bundles:
        print("  ❌ 没有可提交的 Harness。")
        return False

    # Show PII scrub report
    total_redactions = sum(r.get("total_redactions", 0) for _, _, r in bundles)
    if total_redactions > 0:
        print(f"\n  🔒 已自动脱敏 {total_redactions} 处敏感信息：")
        for _, _, report in bundles:
            for f in report.get("files_scrubbed", []):
                redactions = f.get("redactions", {})
                if redactions:
                    parts = [f"{k} x{v}" for k, v in redactions.items()]
                    print(f"     {f['file']}: {', '.join(parts)}")
        print("  原始内容不会上传。")
    else:
        print("\n  未检测到需要脱敏的敏感信息。")

    if not _confirm("是否确认提交 Harness？"):
        # Clean up zips
        for _, zip_path, _ in bundles:
            try:
                os.remove(zip_path)
            except OSError:
                pass
        print("  已取消。")
        return False

    # Upload
    success = 0
    for agent_id, zip_path, _ in bundles:
        print(f"  上传 workspace-{agent_id}.zip...", end=" ", flush=True)
        result = upload_workspace(server_url, key, zip_path, agent_id)
        if "error" in result:
            print(f"失败 ({result.get('error')})")
        else:
            print("OK")
            success += 1
        # Clean up
        try:
            os.remove(zip_path)
        except OSError:
            pass

    if success > 0:
        print(f"\n  ✅ Harness 提交完成（{success} 个）")
        return True
    else:
        print("\n  ❌ Harness 提交失败")
        return False


def check_workspace_gate(server_url: str, key: str, output_dir: str) -> bool:
    """Check if workspace submission is required before continuing.

    Returns True if user can proceed, False if blocked.
    """
    count_result = query_count(server_url, key)
    if "error" in count_result:
        # If we can't check, don't block — server will catch it
        return True

    force_required = count_result.get("workspace_force_required", False)
    threshold = count_result.get("workspace_threshold", 5)
    ws_submitted = count_result.get("workspace_submitted", False)
    count = count_result.get("count", 0)

    if not force_required or threshold <= 0 or count < threshold or ws_submitted:
        return True

    print(f"\n  ⚠️  你已提交 {count} 条数据（达到 {threshold} 条阈值），")
    print(f"  需要先提交 Harness 才能继续采集。")
    print(f"  Harness 包含你的 SOUL.md、USER.md 等配置文件，")
    print(f"  所有文件会在本地自动脱敏后再提交。")
    print()

    if do_workspace(server_url, key, output_dir):
        return True
    else:
        print("\n  ❌ 未完成 Harness 提交，无法继续采集。")
        return False


def maybe_trigger_workspace(result: dict, server_url: str, key: str, output_dir: str):
    """Conditionally trigger workspace upload after successful submit."""
    threshold = result.get("workspace_threshold", 5)
    ws_submitted = result.get("workspace_submitted", False)
    server_total = result.get("server_total", 0)

    if ws_submitted or not isinstance(server_total, int) or server_total < threshold or threshold <= 0:
        return

    print(f"\n{'━' * 56}")
    print(f"  你已提交 {server_total} 条数据（达到 {threshold} 条阈值）。")
    print(f"  为提升数据质量，我们希望采集你的 Harness")
    print(f"  （SOUL.md、USER.md 等配置文件）。这是一次性采集，所有")
    print(f"  文件会在本地自动脱敏后再提交。")
    print(f"{'━' * 56}")
    print()

    if _confirm("是否同意提交 Harness？"):
        do_workspace(server_url, key, output_dir, silent_skip=True)


# ── Main ─────────────────────────────────────────────────────


def main():
    show_all = "--all" in sys.argv
    output_dir = DEFAULT_OUTPUT_DIR

    # Phase 1: Auth
    server_url, key = ensure_auth()

    # Phase 2: Env check
    if not check_env():
        sys.exit(0)

    # Phase 0: Menu
    mode = show_menu()

    if mode == "query":
        os.makedirs(output_dir, exist_ok=True)
        do_query(server_url, key, output_dir)
        return

    if mode == "workspace":
        os.makedirs(output_dir, exist_ok=True)
        do_workspace(server_url, key, output_dir, allow_resubmit=True)
        return

    if mode == "recollect":
        os.makedirs(output_dir, exist_ok=True)
        sessions_dirs = find_openclaw_sessions_dirs()
        if not sessions_dirs:
            print("\n❌ 未找到 OpenClaw sessions 目录。")
            sys.exit(1)
        do_recollect(server_url, key, sessions_dirs, output_dir)
        return

    # mode == "submit"
    os.makedirs(output_dir, exist_ok=True)

    # Workspace gate check (forced mode)
    if not check_workspace_gate(server_url, key, output_dir):
        return

    # Find sessions dirs
    sessions_dirs = find_openclaw_sessions_dirs()
    if not sessions_dirs:
        print("\n❌ 未找到 OpenClaw sessions 目录。")
        sys.exit(1)

    # Phase 3: List & select
    selected_ids = list_and_select(sessions_dirs, output_dir, show_all=show_all)
    if not selected_ids:
        return

    # Phase 4: Scan & convert selected sessions
    emitted = do_scan(output_dir, selected_ids)
    if not emitted:
        print("\n所选对话全部未通过质量检查，无法提交。")
        return

    # Phase 5: Submit (stats/domain/title use heuristic values directly)
    passed_ids = [e["session_id"] for e in emitted]
    result = do_submit(output_dir, server_url, key, passed_ids)

    # Phase 6: Maybe trigger workspace
    if result:
        maybe_trigger_workspace(result, server_url, key, output_dir)


if __name__ == "__main__":
    main()
