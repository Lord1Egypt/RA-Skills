#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨对话框轮数 + token 使用量监测：扫描 .codex/sessions rollouts + app sqlite 目录。

数据来源（2026-10-18~20 实测）：
- 轮数：rollout jsonl 的 response_item message/user，或 event_msg item_completed 的
  item.type == "UserMessage" 代表一次用户提问；按消息/turn id 去重；
- token：token_usage_record.payload.thread_token_usage.total_tokens（缺省回退 usage.total_tokens），
  event_msg.payload.info.total_token_usage.total_tokens 作为兜底（均为真实 usage，非字符估算）；
- local_thread_catalog 提供 thread_id -> display_title/cwd（用于区分项目）。
触发规则：轮数 >= threshold 或 token >= token_threshold，二者哪个先到先触发（互补）。
默认只监测"正在执行任务"的对话框（thread_turns.status == inProgress）；已停止/已完成/归档的对话框不计数、不提醒、不续接。
只读，不写会话日志；--write-state 才把统计快照写回 .codex/memory/state.json。
纯 stdlib（Python 3.9 可用）。
"""

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import json
import os
import re
import sqlite3
import time
from pathlib import Path

def _codex_home():
    # 跨平台：shell 用 ~，Windows 用 %USERPROFILE%/.codex；CODEX_HOME 环境变量可覆盖
    c = os.environ.get("CODEX_HOME") or os.environ.get("OPENAI_CODEX_HOME")
    if c:
        return Path(c)
    return Path.home() / ".codex"


CODEX_HOME = _codex_home()
# 会话目录兼容两层契约：1) CLI/桌面统一 .codex/sessions；2) Windows %USERPROFILE%\.codex\sessions
SESSIONS_DEFAULT = CODEX_HOME / "sessions"
DB_DEFAULT = CODEX_HOME / "sqlite" / "codex-dev.db"
STATE = Path(os.environ.get("CODEX_MEMORY_STATE", CODEX_HOME / "memory" / "state.json"))

DEFAULTS = {"active_project": "", "turn_count": 0, "last_checkpoint": "", "last_action": ""}
THRESHOLD = 8
WARN_AT = 7
TOKEN_THRESHOLD = 150000
TOKEN_WARN_AT = 130000
_META_RE = re.compile(r"rollout-\d{4}-\d{2}-\d{2}T[\d-]+_?((?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(?:_(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}))*)$")


def _resolve_thread_id(path, fallback):
    # session_meta 的显式 ID 优先；fork 文件名可能带 parent_child 两段，不能用首段冒充子会话。
    if fallback and not str(fallback).startswith("rollout-"):
        return str(fallback)
    m = _META_RE.search(path.stem)
    if not m:
        return fallback
    head = m.group(1).split("_")[0]
    return head


def read_rollout(path):
    """返回 (thread_id, user_turns, tokens)。同一 rollout 内按 turn_id 去重。

    tokens 取该对话内已出现的最大累计 total_tokens（thread_token_usage / usage /
    event_msg.info.total_token_usage），为真实 usage 而非字符估算。
    """
    sid = None
    seen = set()
    turns = 0
    tokens = 0

    def _update_total(*srcs):
        nonlocal tokens
        for s in srcs:
            if not isinstance(s, dict):
                continue
            try:
                t = int(s.get("total_tokens") or 0)
            except Exception:
                continue
            if t > tokens:
                tokens = t

    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            if obj.get("type") == "session_meta":
                p = obj.get("payload") or {}
                sid = p.get("session_id") or p.get("id")
                if sid:
                    seen.clear()  # sid 此时才可信；此前可能的计数仅在无 meta 时受影响
                continue
            p = obj.get("payload")
            if not isinstance(p, dict):
                continue
            otype = obj.get("type")
            if otype == "token_usage_record":
                _update_total(p.get("thread_token_usage"), p.get("turn_token_usage"), p.get("usage"))
                continue
            if otype == "response_item" and p.get("type") == "message" and p.get("role") == "user":
                mid = p.get("id") or p.get("turn_id")
                key = (sid, mid)
                if mid and key in seen:
                    continue
                if mid:
                    seen.add(key)
                turns += 1
                continue
            if p.get("type") == "item_completed":
                it = p.get("item") or {}
                if it.get("type") != "UserMessage":
                    continue
                tid = p.get("turn_id") or it.get("id")
                key = (sid, tid)
                if tid and key in seen:
                    continue
                seen.add(key)
                turns += 1
                continue
            if otype == "event_msg":
                info = p.get("info") or {}
                _update_total(info.get("total_token_usage"), info.get("last_token_usage"))
    return (_resolve_thread_id(path, sid or path.stem), turns, tokens)


def load_catalog(db_path=None):
    d = {}
    db = db_path or (CODEX_HOME / "sqlite" / "codex-dev.db")
    if not Path(db).exists():
        return d
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    except Exception:
        return d
    try:
        cur = con.execute(
            "SELECT thread_id, display_title, cwd, project_id, source_recency_at "
            "FROM local_thread_catalog"
        )
        for tid, title, cwd, pid, rec in cur.fetchall():
            d[tid] = {"title": title or tid, "cwd": cwd or "", "project_id": pid or "",
                      "recency": rec or 0}
    finally:
        con.close()
    return d


def load_active_threads(thread_history_db=None, state_db=None):
    """返回正在执行的 thread_id 集合。

    优先从 thread_history_1.sqlite 的 thread_turns(status='inProgress') 取；
    为空/不可用时降级从 state_5.sqlite 的 threads(archived=0) 取（仍只包含未归档）。
    """
    active = set()
    th = thread_history_db or (CODEX_HOME / "thread_history_1.sqlite")
    if Path(th).exists():
        try:
            con = sqlite3.connect(f"file:{th}?mode=ro", uri=True)
            for (tid,) in con.execute(
                    "SELECT DISTINCT thread_id FROM thread_turns WHERE status='inProgress'"):
                active.add(tid)
            con.close()
        except Exception:
            pass
    if active:
        return active
    sd = state_db or (CODEX_HOME / "state_5.sqlite")
    if Path(sd).exists():
        try:
            con = sqlite3.connect(f"file:{sd}?mode=ro", uri=True)
            for (tid,) in con.execute("SELECT id FROM threads WHERE archived=0"):
                active.add(tid)
            con.close()
        except Exception:
            pass
    return active


def load_state():
    d = dict(DEFAULTS)
    if STATE.exists():
        try:
            d.update(json.loads(STATE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return d


def save_state(d):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    d["updated_at"] = time.strftime("%Y-%m-%d %H:%M")
    STATE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def _prev_overwarned(st):
    idx = st.get("index") or {}
    return set(idx.get("over_warned_ids") or [])


def _write_index(st, rows, over, warn, threshold, warn_at, token_th, token_wa,
                  full_scan, overwarned_ids):
    idx = dict(st.get("index") or {})
    now = time.strftime("%Y-%m-%d %H:%M")
    idx.update({
        "scanned_files": len(rows),
        "generated_at": now,
        "threshold": threshold,
        "warn_at": warn_at,
        "token_threshold": token_th,
        "token_warn_at": token_wa,
        "over_warned_ids": sorted(overwarned_ids),
        "sessions": [
            {"id": r["thread_id"], "title": r["title"], "cwd": r["cwd"],
             "turns": r["turns"], "tokens": r["tokens"],
             "over_warned": r["thread_id"] in overwarned_ids} for r in rows
        ],
    })
    if full_scan:
        idx["last_full_scan"] = now
    st["index"] = idx


def _fmt(r):
    proj = (r["cwd"] or r["thread_id"]).split("/")[-1]
    extra = f"，{r.get('tokens') or 0} token"
    return f"{r['title']}（{proj}）[{r['thread_id'][:12]}] {r['turns']} 轮{extra}"


def main():
    ap = argparse.ArgumentParser(description="跨对话框轮数监测")
    ap.add_argument("--threshold", type=int, default=THRESHOLD)
    ap.add_argument("--warn-at", type=int, default=WARN_AT)
    ap.add_argument("--token-threshold", type=int, default=TOKEN_THRESHOLD,
                    help="token 硬阈值（默认 %d），与轮数阈值互补，先到先触发" % TOKEN_THRESHOLD)
    ap.add_argument("--token-warn-at", type=int, default=TOKEN_WARN_AT)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--days", type=int, default=14, help="只统计最近 N 天的会话文件")
    g.add_argument("--all", action="store_true", help="关闭时间过滤，全量扫描历史（与 --days 互斥；安装后首跑/存量全量检测用）")
    ap.add_argument("--sessions-dir", default=str(SESSIONS_DEFAULT), help="Codex 会话目录（跨平台可覆盖）")
    ap.add_argument("--catalog-db", default=str(DB_DEFAULT), help="local_thread_catalog 数据库（找不到时降级用文件元数据）")
    ap.add_argument("--thread-id", default=None, help="只读取文件名匹配该 thread_id 的 rollout，避免扫描无关会话正文")
    ap.add_argument("--write-state", action="store_true", help="把统计快照写回 state.json（并记录 over_warned 去重标记）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--active-only", dest="active_only", action="store_true",
                    help="只监测正在执行任务的对话框（thread_turns inProgress），默认开启")
    ap.add_argument("--no-active-only", dest="active_only", action="store_false",
                    help="关闭 active 过滤，监测全部（含历史/停止）")
    ap.set_defaults(active_only=True)
    args = ap.parse_args()

    full_scan = bool(args.all)
    sessions_dir = Path(args.sessions_dir)
    files = list(sessions_dir.rglob("rollout-*.jsonl")) if sessions_dir.exists() else []
    cutoff = None if full_scan else time.time() - args.days * 86400

    st = load_state()
    prev_overwarned = _prev_overwarned(st)

    catalog = load_catalog(Path(args.catalog_db))
    active_ids = load_active_threads() if args.active_only else None
    rows = []
    for f in files:
        try:
            if args.thread_id and args.thread_id not in f.name:
                continue
            if cutoff is not None and f.stat().st_mtime < cutoff:
                continue
            thread_id, turns, tokens = read_rollout(f)
        except Exception:
            continue
        if active_ids is not None and thread_id not in active_ids:
            continue
        meta = catalog.get(thread_id, {})
        rows.append({
            "file": str(f), "thread_id": thread_id,
            "title": meta.get("title", thread_id), "cwd": meta.get("cwd", ""),
            "project_id": meta.get("project_id", ""), "turns": turns,
            "tokens": tokens,
            "mtime": f.stat().st_mtime,
        })
    rows.sort(key=lambda r: r["mtime"], reverse=True)

    def _reason(r):
        st_list = []
        if r["turns"] >= args.threshold:
            st_list.append("over_turns")
        elif r["turns"] >= args.warn_at:
            st_list.append("warn_turns")
        if (r["tokens"] or 0) >= args.token_threshold:
            st_list.append("over_tokens")
        elif (r["tokens"] or 0) >= args.token_warn_at:
            st_list.append("warn_tokens")
        return "+".join(st_list) if st_list else ""

    over = [r for r in rows if r["turns"] >= args.threshold or (r["tokens"] or 0) >= args.token_threshold]
    warn = [r for r in rows
            if r not in over and
            (args.warn_at <= r["turns"] < args.threshold or
             args.token_warn_at <= (r["tokens"] or 0) < args.token_threshold)]
    for r in over:
        r["metric"] = _reason(r)
    for r in warn:
        r["metric"] = _reason(r)
    # 已在 state 中标记过 over_warned 的同一对话框不再重复提醒
    new_over = [r for r in over if r["thread_id"] not in prev_overwarned]
    new_warn = [r for r in warn if r["thread_id"] not in prev_overwarned]

    if args.write_state:
        overwarned_ids = prev_overwarned | {r["thread_id"] for r in new_over} | {r["thread_id"] for r in new_warn}
        _write_index(st, rows, over, warn, args.threshold, args.warn_at,
                     args.token_threshold, args.token_warn_at, full_scan, overwarned_ids)
        save_state(st)

    if args.json:
        print(json.dumps({
            "scanned": len(rows), "threshold": args.threshold, "warn_at": args.warn_at,
            "token_threshold": args.token_threshold, "token_warn_at": args.token_warn_at,
            "full_scan": full_scan, "new_reminders": len(new_over) + len(new_warn),
            "warn_sessions": [{"thread_id": r["thread_id"], "title": r["title"], "turns": r["turns"],
                               "tokens": r["tokens"] or 0, "metric": r.get("metric", "")} for r in warn],
            "over_sessions": [{"thread_id": r["thread_id"], "title": r["title"], "turns": r["turns"],
                               "tokens": r["tokens"] or 0, "metric": r.get("metric", "")} for r in over],
            "reported_warn_sessions": [{"thread_id": r["thread_id"], "title": r["title"], "turns": r["turns"],
                                        "tokens": r["tokens"] or 0, "metric": r.get("metric", "")} for r in new_warn],
            "reported_over_sessions": [{"thread_id": r["thread_id"], "title": r["title"], "turns": r["turns"],
                                        "tokens": r["tokens"] or 0, "metric": r.get("metric", "")} for r in new_over],
            "total_user_turns": sum(r["turns"] for r in rows),
        }, ensure_ascii=False, indent=2))
        return

    scope = "全量历史" if full_scan else f"最近 {args.days} 天"
    print(f"扫描会话文件: {len(rows)}（{scope}）；轮数阈值 {args.threshold}/{args.warn_at}，token 阈值 {args.token_threshold}/{args.token_warn_at}")
    if new_warn:
        print("⚠️ 接近阈值：")
        for r in new_warn:
            print(f"  - {_fmt(r)}")
    if new_over:
        print("🔴 已超阈值：")
        for r in new_over:
            print(f"  - {_fmt(r)}")
    if not new_over and not new_warn and not over and not warn:
        print("✅ 未发现超阈值或接近阈值的对话")
    elif not new_over and not new_warn:
        print("（已在本机 state.json 标记过的超阈值/接近阈值对话框不再重复提醒）")


if __name__ == "__main__":
    main()
