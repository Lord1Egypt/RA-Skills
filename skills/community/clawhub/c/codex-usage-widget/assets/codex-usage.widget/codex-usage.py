#!/usr/bin/env python3
import datetime as dt
import json
import re
import sqlite3
import time
from pathlib import Path

HOME = Path.home()
STATE = HOME / ".codex" / "state_5.sqlite"
LOGS = HOME / ".codex" / "logs_2.sqlite"
ROLLOUT_ROOTS = [
    HOME / ".codex" / "sessions",
    HOME / ".codex" / "archived_sessions",
]
USAGE_CACHE = HOME / ".codex" / "codex-usage-rollup-cache.json"
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
CACHE_VERSION = 6
ACTIVE_WINDOW_MS = 10 * 60 * 1000
RECENT_LIMIT = 8
CTX_WINDOW = 200000
CTX_BIG_WINDOW = 1000000

LAST_MS_EXPR = """
max(
    coalesce(nullif(recency_at_ms,0), 0),
    coalesce(updated_at_ms, updated_at * 1000, 0),
    coalesce(created_at_ms, created_at * 1000, 0)
)
"""

T_LAST_MS_EXPR = """
max(
    coalesce(nullif(t.recency_at_ms,0), 0),
    coalesce(t.updated_at_ms, t.updated_at * 1000, 0),
    coalesce(t.created_at_ms, t.created_at * 1000, 0)
)
"""


def connect(path):
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=1)


def ms(dt_obj):
    return int(dt_obj.timestamp() * 1000)


def title(s):
    s = " ".join((s or "").split())
    return s[:42] + "…" if len(s) > 43 else s


def source_label(source, thread_source="", parent_source="", originator=""):
    source = (source or "").strip()
    thread_source = (thread_source or "").strip()
    parent_source = (parent_source or "").strip()
    originator = (originator or "").strip().lower()

    if "vscode" in originator:
        return "VSCode"
    if "desktop" in originator:
        return "Client"
    if "terminal" in originator or "cli" in originator:
        return "Terminal"

    if thread_source == "subagent" or source.startswith("{"):
        return source_label(parent_source) if parent_source else "Client"
    if source == "vscode":
        return "VSCode"
    if source in {"terminal", "cli"}:
        return "Terminal"
    if source in {"codex", "desktop"} or not source:
        return "Client"
    return "Client"


def ctx_info(tokens):
    tokens = max(0, int(tokens or 0))
    window = CTX_BIG_WINDOW if tokens > CTX_WINDOW else CTX_WINDOW
    pct = round((tokens / window) * 100) if window else 0
    return tokens, window, min(999, max(0, pct))


def thread_id_from_path(path):
    m = UUID_RE.search(path.name)
    return m.group(0) if m else str(path)


def iter_rollout_paths():
    seen = set()
    for root in ROLLOUT_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.jsonl"):
            key = str(path)
            if key not in seen:
                seen.add(key)
                yield path


def parse_rollout(path):
    thread_id = thread_id_from_path(path)
    events = []
    originator = ""
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            payload = obj.get("payload") or {}
            if obj.get("type") == "session_meta" and isinstance(payload, dict):
                originator = str(payload.get("originator") or originator or "")
            if payload.get("type") != "token_count":
                continue
            last = ((payload.get("info") or {}).get("last_token_usage") or {})
            try:
                tokens = int(last.get("total_tokens") or 0)
                input_tokens = int(last.get("input_tokens") or 0)
            except Exception:
                continue
            if tokens <= 0:
                continue
            ts = obj.get("timestamp") or ""
            try:
                day = dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone().date().isoformat()
            except Exception:
                continue
            events.append([day, tokens, thread_id, ts, input_tokens])
    return {"events": events, "originator": originator}


def load_usage_cache():
    try:
        data = json.load(USAGE_CACHE.open("r", encoding="utf-8"))
        if data.get("version") == CACHE_VERSION and isinstance(data.get("files"), dict):
            return data
    except Exception:
        pass
    return {"version": CACHE_VERSION, "files": {}}


def save_usage_cache(cache):
    try:
        tmp = USAGE_CACHE.with_suffix(".tmp")
        json.dump(cache, tmp.open("w", encoding="utf-8"), ensure_ascii=False)
        tmp.replace(USAGE_CACHE)
    except Exception:
        pass


def strict_usage_rollup(week0):
    try:
        cache = load_usage_cache()
        files = cache.setdefault("files", {})
        seen_paths = set()

        for path in iter_rollout_paths():
            try:
                st = path.stat()
            except OSError:
                continue
            key = str(path)
            seen_paths.add(key)
            entry = files.get(key) or {}
            if entry.get("mtime_ns") == st.st_mtime_ns and entry.get("size") == st.st_size:
                continue
            parsed = parse_rollout(path)
            files[key] = {
                "mtime_ns": st.st_mtime_ns,
                "size": st.st_size,
                "events": parsed["events"],
                "originator": parsed["originator"],
            }

        for key in list(files):
            if key not in seen_paths:
                del files[key]
        save_usage_cache(cache)

        today = dt.datetime.now().date()
        days = [week0.date() + dt.timedelta(days=i) for i in range(7)]
        buckets = {d: 0 for d in days}
        threads_by_day = {d: set() for d in days}
        seen_events = set()
        total_tokens = 0
        ctx_by_thread = {}
        originator_by_thread = {}

        for entry in files.values():
            entry_thread_id = ""
            key = next((k for k, v in files.items() if v is entry), "")
            if key:
                entry_thread_id = thread_id_from_path(Path(key))
                if entry.get("originator"):
                    originator_by_thread[entry_thread_id] = entry.get("originator") or ""
            for event in entry.get("events", []):
                if len(event) < 4:
                    continue
                day_s, tokens, thread_id, ts = event[:4]
                input_tokens = event[4] if len(event) >= 5 else 0
                try:
                    day = dt.date.fromisoformat(day_s)
                    tokens = int(tokens or 0)
                    input_tokens = int(input_tokens or 0)
                except Exception:
                    continue
                if tokens <= 0:
                    continue
                prev = ctx_by_thread.get(thread_id)
                if input_tokens > 0 and (not prev or ts >= prev["ts"]):
                    ctx_by_thread[thread_id] = {"tokens": input_tokens, "ts": ts}
                event_key = (thread_id, ts, tokens)
                if event_key in seen_events:
                    continue
                seen_events.add(event_key)
                total_tokens += tokens
                if day not in buckets:
                    continue
                buckets[day] += tokens
                threads_by_day[day].add(thread_id)

        return {
            "ok": True,
            "total_tokens": total_tokens,
            "today_tokens": buckets.get(today, 0),
            "today_threads": len(threads_by_day.get(today, set())),
            "ctx_by_thread": {k: v["tokens"] for k, v in ctx_by_thread.items()},
            "originator_by_thread": originator_by_thread,
            "days": [
                {"label": ["一", "二", "三", "四", "五", "六", "日"][d.weekday()], "tokens": buckets[d]}
                for d in days
            ],
        }
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def main():
    now = dt.datetime.now()
    today0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week0 = today0 - dt.timedelta(days=6)
    now_ms = int(time.time() * 1000)
    today_ms = ms(today0)
    week_ms = ms(week0)

    out = {
        "ok": True,
        "now": now.strftime("%H:%M"),
        "thread_count": 0,
        "today_threads": 0,
        "active_threads": 0,
        "total_tokens": 0,
        "today_tokens": 0,
        "recent": [],
        "days": [],
        "log_bytes": 0,
        "usage_basis": "thread_totals",
    }

    try:
        db = connect(STATE)
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        strict = strict_usage_rollup(week0)
        ctx_by_thread = strict.get("ctx_by_thread", {}) if strict.get("ok") else {}
        originator_by_thread = strict.get("originator_by_thread", {}) if strict.get("ok") else {}

        cur.execute(f"""
            select t.id, coalesce(e.parent_thread_id, t.id) as root_id,
                   t.title, t.source, t.thread_source, t.model, t.tokens_used,
                   p.title as parent_title, p.source as parent_source, p.archived as parent_archived,
                   {T_LAST_MS_EXPR} as last_ms
            from threads t
            left join thread_spawn_edges e on e.child_thread_id = t.id
            left join threads p on p.id = e.parent_thread_id
            where t.archived=0
            order by last_ms desc
        """)
        groups = {}
        for r in cur.fetchall():
            root_id = r["root_id"]
            if int(r["parent_archived"] or 0):
                continue
            last = int(r["last_ms"] or 0)
            g = groups.setdefault(root_id, {
                "title": title(r["parent_title"] or r["title"]),
                "source": source_label(
                    r["parent_source"] or r["source"],
                    originator=originator_by_thread.get(root_id, originator_by_thread.get(r["id"], "")),
                ),
                "model": r["model"] or "",
                "last_ms": 0,
                "tokens_sum": 0,
                "ctx_tokens": 0,
            })
            g["last_ms"] = max(g["last_ms"], last)
            g["tokens_sum"] += int(r["tokens_used"] or 0)
            g["ctx_tokens"] = max(g["ctx_tokens"], int(ctx_by_thread.get(r["id"], 0) or 0))

        out["thread_count"] = len(groups)
        out["total_tokens"] = sum(g["tokens_sum"] for g in groups.values())
        out["today_threads"] = sum(1 for g in groups.values() if g["last_ms"] >= today_ms)
        out["today_tokens"] = sum(g["tokens_sum"] for g in groups.values() if g["last_ms"] >= today_ms)
        out["active_threads"] = sum(1 for g in groups.values() if g["last_ms"] >= now_ms - ACTIVE_WINDOW_MS)

        for g in sorted(groups.values(), key=lambda x: x["last_ms"], reverse=True)[:RECENT_LIMIT]:
            ctx_tokens, ctx_window, ctx_pct = ctx_info(g["ctx_tokens"])
            out["recent"].append({
                "title": g["title"],
                "source": g["source"],
                "model": g["model"],
                "ctx_tokens": ctx_tokens,
                "ctx_window": ctx_window,
                "ctx_pct": ctx_pct,
                "age_sec": max(0, int((now_ms - g["last_ms"]) / 1000)),
            })

        cur.execute(f"""
            select tokens_used,
                   {LAST_MS_EXPR} as last_ms
            from threads
            where archived=0 and {LAST_MS_EXPR} >= ?
        """, (week_ms,))
        buckets = {}
        for i in range(7):
            d = week0 + dt.timedelta(days=i)
            buckets[d.date()] = 0
        for r in cur.fetchall():
            d = dt.datetime.fromtimestamp(int(r["last_ms"]) / 1000).date()
            if d in buckets:
                buckets[d] += int(r["tokens_used"] or 0)
        out["days"] = [
            {"label": ["一", "二", "三", "四", "五", "六", "日"][d.weekday()], "tokens": tok}
            for d, tok in buckets.items()
        ]
        db.close()

        if strict.get("ok"):
            out["total_tokens"] = int(strict["total_tokens"])
            out["today_tokens"] = int(strict["today_tokens"])
            out["days"] = strict["days"]
            out["usage_basis"] = "token_count_events"
        else:
            out["usage_error"] = strict.get("error", "")
    except Exception as e:
        out = {"ok": False, "error": f"state db: {type(e).__name__}: {e}"}

    if out.get("ok"):
        try:
            db = connect(LOGS)
            cur = db.cursor()
            cur.execute("select coalesce(sum(estimated_bytes),0) from logs where ts >= ?", (int(today0.timestamp()),))
            out["log_bytes"] = int(cur.fetchone()[0] or 0)
            db.close()
        except Exception:
            pass

    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
