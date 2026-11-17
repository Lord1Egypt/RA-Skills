#!/usr/bin/env python3
"""Collect local agent activity into a compact digest for a daily journal writer.

A "window" is `day 04:00 -> next day 04:00` by default (`day_start_hour` in config).
Coverage is recorded *inside the journal file itself* as HTML-comment window markers,
so the journal is the single source of truth: whatever is not marked is still owed.

Pipeline (all local, zero cloud tokens):

  1. state.db, opened read-only -> sessions, prompts, assistant outcomes, tool histogram
  2. workspace mtimes -> files touched in the window
  3. local Ollama, when reachable -> embedding dedupe of prompts + optional compression
  4. print one compact markdown digest per missing window, oldest first

The digest is *material*, never prose: the writer decides the voice. See
`references/collector-design.md` for the queries and knobs, and `references/writer-and-prompt.md`
for the writer-side contract.

Usage:
    python journal_collect.py                        # config from env / ./config/journal.json
    python journal_collect.py --config cfg.json
    python journal_collect.py --journal ./journal.md --json
    python journal_collect.py --only 2026-10-25      # force one window, ignore markers
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULTS: dict = {
    "state_db": None,            # default: <hermes_home>/state.db
    "hermes_home": None,         # default: $HERMES_HOME or %LOCALAPPDATA%/hermes on Windows, ~/.hermes elsewhere
    "workspace": None,           # default: $JOURNAL_WORKSPACE or the journal's parent
    "journal": None,             # default: <workspace>/memory/journal/journal.md
    "day_start_hour": 4,
    "max_windows": 4,
    "digest_chars": 2600,        # per-window ceiling, keeps the writer's prompt cheap
    "max_sessions": 10,
    "max_prompts": 6,
    "prompt_chars": 150,
    "max_outcomes": 2,
    "outcome_chars": 110,
    "max_files": 8,
    "max_tools": 6,
    "dedupe_cosine": 0.88,
    "skip_dirs": [".git", "node_modules", "__pycache__", ".venv", "venv", "archive", "memory", "tmp"],
    "ollama_url": "http://127.0.0.1:11434",
    "embed_model": "qwen3-embedding:0.6b",
    "local_model": "qwen3:1.7b",
    "local_mode": "auto",        # auto | on | off
    "labels": {
        "no_update": "Nothing owed: the journal already covers {latest}.",
        "header": "# Windows to write: {days} ({total} owed, {batch} in this run)",
        "header_more": "; {rest} older windows wait for the next run",
        "model_note": "<!-- local models: embedding {embed}, compression {compress} -->",
        "window": "## Window {day} ({weekday}) {start_hour}:00 -> next day {start_hour}:00 ({n} sessions)",
        "empty_window": "(no sessions and no file changes in this window.)",
        "prompt": "- said: {text}",
        "tools": "- tools: {text}",
        "key_points": "- key points: {text}",
        "outcome": "- outcome: {text}",
        "files": "### Files touched",
        "truncated": "… (digest truncated)",
        "footer": (
            "Write one entry per window, appended to the end of the journal file. "
            "End every entry with this exact HTML comment: <!-- window:YYYY-MM-DD --> "
            "using the window's start date."
        ),
        "compress_prompt": (
            "Compress the following work log into 1-2 bullet points, each under 40 characters. "
            "Keep proper nouns, file names, tool names and numbers. No commentary, no preamble, "
            "no markdown.\n\n"
        ),
        "weekdays": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
}

CN_LABELS = {
    "no_update": "无需更新：日记已覆盖到最近一个完整窗口（{latest}）。",
    "header": "# 待写日记窗口：{days}（共 {total} 个待补，本次处理 {batch} 个）",
    "header_more": "；更早的 {rest} 个留到下次运行。",
    "model_note": "<!-- 本地模型：embedding {embed}，压缩 {compress} -->",
    "window": "## 窗口 {day}（{weekday}）{start_hour}:00 → 次日 {start_hour}:00（{n} 段会话）",
    "empty_window": "（这一段时间没有任何会话，也没改动文件。）",
    "prompt": "- 说：{text}",
    "tools": "- 工具：{text}",
    "key_points": "- 要点：{text}",
    "outcome": "- 结论：{text}",
    "files": "### 改动过的文件",
    "truncated": "…（摘要已截断）",
    "footer": "每个窗口单独写一条，追加到 journal.md 末尾。每条末尾必须原样写这一行（HTML 注释）："
              "<!-- window:YYYY-MM-DD -->，DATE 换成该窗口起始日。",
    "compress_prompt": (
        "把下面这段工作记录压成 1-2 条中文要点，每条不超过 40 字。"
        "保留专有名词、文件名、工具名、数字。不要评论、不要总起句、不要 markdown。\n\n"
    ),
    "weekdays": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
}


# ---------------------------------------------------------------- config
def _default_hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env)
    win = Path.home() / "AppData" / "Local" / "hermes"
    return win if win.exists() else Path.home() / ".hermes"


def load_config(path: str | None) -> dict:
    cfg = json.loads(json.dumps(DEFAULTS))  # deep copy, labels dict included
    candidates = [path, os.environ.get("JOURNAL_CONFIG")]
    for cand in candidates:
        if cand and Path(cand).exists():
            raw = json.loads(Path(cand).read_text(encoding="utf-8"))
            if str(raw.get("language", "")).lower() in {"zh", "cn", "chinese", "中文"}:
                cfg["labels"].update(CN_LABELS)
            for key, value in raw.items():
                if key == "labels":
                    cfg["labels"].update(value)
                elif key in cfg:
                    cfg[key] = value
            break

    # environment overrides (kept for backwards compatibility with hand-wired cron jobs)
    env_map = {
        "JOURNAL_FILE": "journal",
        "JOURNAL_WORKSPACE": "workspace",
        "JOURNAL_DAY_START_HOUR": "day_start_hour",
        "JOURNAL_MAX_WINDOWS": "max_windows",
        "JOURNAL_OLLAMA_URL": "ollama_url",
        "JOURNAL_EMBED_MODEL": "embed_model",
        "JOURNAL_LOCAL_MODEL": "local_model",
        "JOURNAL_LOCAL": "local_mode",
        "JOURNAL_STATE_DB": "state_db",
    }
    for env_key, cfg_key in env_map.items():
        if os.environ.get(env_key):
            cfg[cfg_key] = os.environ[env_key]

    hermes_home = Path(cfg["hermes_home"]) if cfg["hermes_home"] else _default_hermes_home()
    cfg["state_db"] = Path(cfg["state_db"]) if cfg["state_db"] else hermes_home / "state.db"
    if cfg["journal"]:
        cfg["journal"] = Path(cfg["journal"])
    else:
        workspace = Path(cfg["workspace"]) if cfg["workspace"] else Path.cwd()
        cfg["workspace"] = workspace
        cfg["journal"] = workspace / "memory" / "journal" / "journal.md"
    if not cfg["workspace"]:
        cfg["workspace"] = cfg["journal"].parent
    cfg["workspace"] = Path(cfg["workspace"])
    cfg["day_start_hour"] = int(cfg["day_start_hour"])
    cfg["max_windows"] = int(cfg["max_windows"])
    return cfg


# ---------------------------------------------------------------- ollama helpers
def ollama_models(cfg: dict) -> set[str]:
    try:
        with urllib.request.urlopen(f"{cfg['ollama_url']}/api/tags", timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return set()
    return {m.get("name", "") for m in (data or {}).get("models", [])}


def has_model(models: set[str], name: str) -> bool:
    if name in models or f"{name}:latest" in models:
        return True
    if ":" not in name:
        return any(m.split(":")[0] == name for m in models)
    return False


def _post(cfg: dict, path: str, payload: dict, timeout: float) -> dict | None:
    try:
        req = urllib.request.Request(
            f"{cfg['ollama_url']}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return None


def embed(cfg: dict, texts: list[str]) -> list[list[float]] | None:
    if not texts:
        return []
    data = _post(cfg, "/api/embed", {"model": cfg["embed_model"], "input": texts}, 20)
    if not data:
        return None
    vectors = data.get("embeddings") or []
    return vectors if len(vectors) == len(texts) else None


def local_compress(cfg: dict, raw: str) -> str | None:
    prompt = cfg["labels"]["compress_prompt"] + raw[:1200]
    data = _post(
        cfg,
        "/api/generate",
        {
            "model": cfg["local_model"],
            "prompt": prompt,
            "stream": False,
            "think": False,  # qwen3 hybrids: skip the thinking block, the summary is what we want
            "options": {"temperature": 0.2, "num_predict": 160, "num_ctx": 2048},
        },
        60,
    )
    if not data:
        return None
    text = " ".join((data.get("response") or "").split())
    return text if 8 <= len(text) <= 400 else None


# ---------------------------------------------------------------- text utilities
def clip(text: str, limit: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def clean(text: str) -> str:
    """Strip markdown/code/attachment noise so the digest reads like prose, not a transcript."""
    text = text or ""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)       # fenced code blocks
    text = re.sub(r"`[^`]{0,200}`", " ", text)               # inline code
    text = re.sub(r"@file:\s*[^\n]{0,300}", " ", text)       # attachment preamble
    text = re.sub(r"[A-Za-z]:\\\\[^\s\"']{6,}", " ", text)    # windows paths
    text = re.sub(r"^\s{0,3}#{1,6}\s*", " ", text, flags=re.M)
    text = re.sub(r"^\s{0,3}[-*+]\s+", " ", text, flags=re.M)
    text = re.sub(r"[*_>|]{1,}", " ", text)
    text = re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", "", text)  # emoji
    return " ".join(text.split())


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def dedupe_lines(lines: list[str], use_embeddings: bool, cfg: dict) -> list[str]:
    """Drop near-duplicate prompts. Embeddings when Ollama is up, character overlap otherwise."""
    if len(lines) <= 1:
        return lines
    vectors = embed(cfg, lines) if use_embeddings else None
    kept: list[str] = []
    kept_vecs: list[list[float]] = []
    for i, line in enumerate(lines):
        duplicate = False
        if vectors:
            for vec in kept_vecs:
                if cosine(vectors[i], vec) >= float(cfg["dedupe_cosine"]):
                    duplicate = True
                    break
        else:
            words = set(line)
            for prev in kept:
                other = set(prev)
                if len(words & other) / max(1, len(words | other)) >= 0.8:
                    duplicate = True
                    break
        if not duplicate:
            kept.append(line)
            if vectors:
                kept_vecs.append(vectors[i])
    return kept


# ---------------------------------------------------------------- windows
def window_bounds(day: dt.date, cfg: dict) -> tuple[float, float]:
    start = dt.datetime.combine(day, dt.time(cfg["day_start_hour"]))
    return start.timestamp(), (start + dt.timedelta(days=1)).timestamp()


def latest_complete_day(now: dt.datetime, cfg: dict) -> dt.date:
    return (now - dt.timedelta(hours=cfg["day_start_hour"])).date() - dt.timedelta(days=1)


def covered_days(cfg: dict) -> set[dt.date]:
    journal = Path(cfg["journal"])
    if not journal.exists():
        return set()
    found: set[dt.date] = set()
    for match in re.finditer(r"window:(\d{4}-\d{2}-\d{2})", journal.read_text(encoding="utf-8", errors="replace")):
        try:
            found.add(dt.date.fromisoformat(match.group(1)))
        except ValueError:
            continue
    return found


def missing_days(now: dt.datetime, cfg: dict) -> list[dt.date]:
    latest = latest_complete_day(now, cfg)
    done = covered_days(cfg)
    if done:
        oldest = min(done)
    else:
        baseline = os.environ.get("JOURNAL_START")
        try:
            oldest = dt.date.fromisoformat(baseline) if baseline else latest - dt.timedelta(days=1)
        except ValueError:
            oldest = latest - dt.timedelta(days=1)
    missing: list[dt.date] = []
    day = oldest
    while day <= latest:
        if day not in done:
            missing.append(day)
        day += dt.timedelta(days=1)
    return missing


# ---------------------------------------------------------------- collection
def fetch_sessions(start: float, end: float, cfg: dict) -> list[dict]:
    state_db = Path(cfg["state_db"])
    if not state_db.exists():
        return []
    con = sqlite3.connect(f"file:{state_db}?mode=ro", uri=True, timeout=10)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(
            """
            SELECT id, title, display_name, source, model, started_at, last_activity_at,
                   message_count, tool_call_count, cwd, hidden
            FROM sessions
            WHERE COALESCE(last_activity_at, started_at, 0) >= ?
              AND COALESCE(started_at, last_activity_at, 0) < ?
              AND COALESCE(hidden, 0) = 0
              AND COALESCE(source, '') <> 'cron'
            ORDER BY COALESCE(started_at, last_activity_at, 0) ASC
            """,
            (start, end),
        ).fetchall()
        sessions: list[dict] = []
        for row in rows:
            item = dict(row)
            span = con.execute(
                """
                SELECT COUNT(*) AS n, MIN(timestamp) AS first_ts, MAX(timestamp) AS last_ts
                FROM messages
                WHERE session_id = ? AND COALESCE(timestamp, 0) >= ? AND COALESCE(timestamp, 0) < ?
                """,
                (row["id"], start, end),
            ).fetchone()
            item["n_in_window"] = int(span["n"] or 0)
            item["first_ts"] = span["first_ts"]
            item["last_ts"] = span["last_ts"]
            item["tool_n"] = con.execute(
                """
                SELECT COUNT(*) FROM messages
                WHERE session_id = ? AND role = 'tool'
                  AND COALESCE(timestamp, 0) >= ? AND COALESCE(timestamp, 0) < ?
                """,
                (row["id"], start, end),
            ).fetchone()[0]
            if item["n_in_window"] == 0:
                continue  # touched the window boundary only, no real activity inside
            prompts = [
                clip(clean(m["content"]), cfg["prompt_chars"])
                for m in con.execute(
                    """
                    SELECT content FROM messages
                    WHERE session_id = ? AND role = 'user' AND COALESCE(active, 1) = 1
                      AND content IS NOT NULL AND TRIM(content) <> ''
                      AND COALESCE(timestamp, 0) >= ? AND COALESCE(timestamp, 0) < ?
                    ORDER BY timestamp ASC
                    """,
                    (row["id"], start, end),
                ).fetchall()
                if m["content"]
            ]
            item["prompts"] = [
                p for p in prompts
                if p and not p.startswith("[IMPORTANT: Background process")
                and not p.startswith("[ASYNC DELEGATION")
            ]
            outcomes = [
                clip(clean(m["content"]), cfg["outcome_chars"])
                for m in con.execute(
                    """
                    SELECT content FROM messages
                    WHERE session_id = ? AND role = 'assistant'
                      AND content IS NOT NULL AND TRIM(content) <> ''
                      AND COALESCE(timestamp, 0) >= ? AND COALESCE(timestamp, 0) < ?
                    ORDER BY timestamp DESC LIMIT 8
                    """,
                    (row["id"], start, end),
                ).fetchall()
                if m["content"]
            ]
            item["outcomes"] = [o for o in outcomes if o][: cfg["max_outcomes"]]
            item["tools"] = [
                r[0]
                for r in con.execute(
                    """
                    SELECT tool_name FROM messages
                    WHERE session_id = ? AND role = 'tool' AND tool_name IS NOT NULL
                      AND COALESCE(timestamp, 0) >= ? AND COALESCE(timestamp, 0) < ?
                    GROUP BY tool_name ORDER BY COUNT(*) DESC LIMIT ?
                    """,
                    (row["id"], start, end, cfg["max_tools"]),
                ).fetchall()
                if r[0]
            ]
            sessions.append(item)
        return sessions
    finally:
        con.close()


def fetch_touched_files(start: float, end: float, cfg: dict) -> list[str]:
    workspace = Path(cfg["workspace"])
    if not workspace.exists():
        return []
    skip = set(cfg["skip_dirs"])
    hits: list[tuple[str, float]] = []
    for root, dirs, files in os.walk(workspace):
        dirs[:] = [d for d in dirs if d not in skip and not d.startswith(".")]
        for name in files:
            path = Path(root) / name
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            if start <= mtime < end:
                try:
                    hits.append((str(path.relative_to(workspace)).replace("\\", "/"), mtime))
                except ValueError:
                    continue
    hits.sort(key=lambda item: item[1], reverse=True)
    return [rel for rel, _ in hits[: cfg["max_files"]]]


def hm(epoch: float | None) -> str:
    return dt.datetime.fromtimestamp(epoch).strftime("%H:%M") if epoch else "?"


def build_digest(day: dt.date, use_embeddings: bool, use_local: bool, claimed: set[str], cfg: dict) -> str:
    labels = cfg["labels"]
    start, end = window_bounds(day, cfg)
    sessions = [s for s in fetch_sessions(start, end, cfg) if s["id"] not in claimed][: cfg["max_sessions"]]
    files = fetch_touched_files(start, end, cfg)
    weekday = labels["weekdays"][day.weekday()]
    head = dict(day=day.isoformat(), weekday=weekday, start_hour=cfg["day_start_hour"], n=len(sessions))
    if not sessions and not files:
        return labels["window"].format(**head) + "\n" + labels["empty_window"]

    lines = [labels["window"].format(**head)]
    for item in sessions:
        claimed.add(item["id"])
        title = clip(item.get("title") or item.get("display_name") or "untitled", 60)
        lines.append(
            f"### {hm(item.get('first_ts'))}-{hm(item.get('last_ts'))} {title} "
            f"[{item.get('n_in_window') or 0} msgs / {item.get('tool_n') or 0} tool calls]"
        )
        prompts = dedupe_lines(item["prompts"], use_embeddings, cfg)[: cfg["max_prompts"]]
        raw_for_local = "; ".join(prompts) + " | tools: " + ", ".join(item["tools"])
        compressed = local_compress(cfg, raw_for_local) if (use_local and prompts) else None
        if compressed:
            lines.append(labels["key_points"].format(text=compressed))
        else:
            for prompt in prompts:
                lines.append(labels["prompt"].format(text=prompt))
            if item["tools"]:
                lines.append(labels["tools"].format(text=", ".join(item["tools"])))
        for outcome in item["outcomes"]:
            lines.append(labels["outcome"].format(text=outcome))
        lines.append("")
    if files:
        lines.append(labels["files"])
        lines.append("- " + "\n- ".join(files))
    digest = "\n".join(lines)
    if len(digest) > cfg["digest_chars"]:
        digest = digest[: cfg["digest_chars"] - 30].rsplit("\n", 1)[0] + "\n" + labels["truncated"]
    return digest


def window_events(digest: str, cfg: dict | None = None) -> list[str]:
    """The `###` headings of one digest block that are real events.

    The touched-files section is a `###` heading too, but it is not an event — the writer owes
    nothing for it, so it must not inflate the coverage count.
    """
    skip = {cfg["labels"]["files"].lstrip("# ").strip()} if cfg else {"Files touched", "改动过的文件"}
    headings = [line[4:].strip() for line in digest.splitlines() if line.startswith("### ")]
    return [heading for heading in headings if heading not in skip]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect local agent activity into journal digests.")
    parser.add_argument("--config", help="path to a journal.json config file")
    parser.add_argument("--journal", help="override the journal file path")
    parser.add_argument("--state-db", help="override the Hermes state.db path")
    parser.add_argument("--workspace", help="override the workspace root scanned for touched files")
    parser.add_argument("--day-start-hour", type=int, help="hour the day window starts (default 4)")
    parser.add_argument("--max-windows", type=int, help="max windows per run")
    parser.add_argument("--only", action="append", metavar="YYYY-MM-DD",
                        help="force this window regardless of markers (repeatable, for tests)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--quiet-model-note", action="store_true", help="omit the local-model comment line")
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    for attr, key in [("journal", "journal"), ("state_db", "state_db"), ("workspace", "workspace"),
                      ("day_start_hour", "day_start_hour"), ("max_windows", "max_windows")]:
        value = getattr(args, attr)
        if value is not None:
            cfg[key] = Path(value) if key in {"journal", "state_db", "workspace"} else value
    if not cfg.get("workspace"):
        cfg["workspace"] = Path(cfg["journal"]).parent

    now = dt.datetime.now()
    if args.only:
        try:
            batch = [dt.date.fromisoformat(value) for value in args.only]
        except ValueError:
            print(f"bad --only date: {args.only}", file=sys.stderr)
            return 2
        owed: list[dt.date] = []
    else:
        owed = missing_days(now, cfg)
        if not owed:
            latest = latest_complete_day(now, cfg).isoformat()
            if args.json:
                print(json.dumps({"owed": 0, "windows": [], "message": cfg["labels"]["no_update"].format(latest=latest)},
                                 ensure_ascii=False))
            else:
                print(cfg["labels"]["no_update"].format(latest=latest))
            return 0
        batch = owed[: cfg["max_windows"]]

    models = ollama_models(cfg)
    use_embeddings = cfg["local_mode"] != "off" and has_model(models, cfg["embed_model"])
    use_local = cfg["local_mode"] != "off" and has_model(models, cfg["local_model"])

    claimed: set[str] = set()
    windows = []
    for day in batch:
        digest = build_digest(day, use_embeddings, use_local, claimed, cfg)
        windows.append({"day": day.isoformat(), "digest": digest,
                        "events": window_events(digest, cfg)})

    if args.json:
        print(json.dumps({
            "owed": len(owed),
            "local": {"embeddings": use_embeddings, "compression": use_local},
            "windows": windows,
        }, ensure_ascii=False, indent=2))
        return 0

    labels = cfg["labels"]
    header = labels["header"].format(
        days=", ".join(d.isoformat() for d in batch), total=len(owed), batch=len(batch)
    )
    if len(owed) > len(batch):
        header += labels["header_more"].format(rest=len(owed) - len(batch))
    print(header)
    if not args.quiet_model_note:
        print(labels["model_note"].format(embed="on" if use_embeddings else "off",
                                         compress="on" if use_local else "off"))
    print()
    for window in windows:
        print(window["digest"])
        print()
    print(labels["footer"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
