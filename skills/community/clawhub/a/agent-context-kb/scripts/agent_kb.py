#!/usr/bin/env python3
"""Manage a lightweight repository-local agent knowledge base."""

from __future__ import annotations

import argparse
from collections import deque
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

from transcript_reads import (
    KbReadEvent,
    TranscriptScan,
    claude_transcript_paths,
    parse_claude_transcript,
    parse_codex_transcript,
    resolve_path as resolve_transcript_path,
    transcript_mentions,
    transcript_paths,
)


# KB scaffold schema version. Bump only when the on-disk KB layout/templates
# change, so a future `upgrade` can tell what an existing KB was built with.
# Decoupled from any general skill release version.
SCHEMA_VERSION = 1
KB_META_FILE = ".kb-meta.yaml"
KB_MODES = {"nested", "shared", "local"}


RUNTIME_PROTOCOL = """## Project Knowledge Base

`.agent-kb/` is this project's memory for coding agents: read it before working,
update it when your work changes what a future agent needs to know.

At task start, before broad code search:
1. Read `.agent-kb/start.md`.
2. Read `.agent-kb/routes.yaml`; pick the routes relevant to this task.
3. Read those KB docs, then search code for gaps.

Before finishing:
- Did this work change what a future agent needs to know? If yes, update the
  relevant topic file, or add a note in `.agent-kb/inbox/` when the right place
  is unclear. `start.md` defines what belongs in the KB.
"""

PROTOCOL_SECTION_RE = re.compile(r"^## Project Knowledge Base\n.*?(?=^## |\Z)", re.M | re.S)

PROTOCOL_BODY_MARKER = "`.agent-kb/` is this project's memory for coding agents"

# Both harness entry files carry the full protocol; the canonical text lives in
# RUNTIME_PROTOCOL above and upgrade re-syncs each file from it.
PROTOCOL_FILES = ("AGENTS.md", "CLAUDE.md")

# Cross-reference line written into a freshly created entry file when the other one already exists.
COUNTERPART_NOTE_TMPL = "See [{other}]({other}) for repository instructions.\n\n"

# Legacy generated pointer-file sentence; upgrade trims its protocol claim now both files hold the protocol.
LEGACY_POINTER_LINE_RE = re.compile(
    r"See \[(AGENTS\.md|CLAUDE\.md)\]\(\1\) for repository instructions and the `\.agent-kb/` knowledge base protocol\."
)

START_MD = """# Agent KB Start

This directory is the project knowledge base for coding agents.
It is an agent-facing index and distilled knowledge layer, not a replacement
for human docs. When docs already exist, summarize only the durable facts agents
need and link back to the source.

## How To Read

1. Read this file first.
2. Read `routes.yaml` and choose only routes relevant to the current task.
   Use `map.md` only as the readable summary if that is faster.
3. Open candidate topic files and check `Summary` and `Read When`.
4. Continue into body text and related links only when they are clearly relevant.

## How To Write

Update this KB only when work creates or changes durable project knowledge:

- Architecture boundaries or module responsibilities
- Design decisions and reasons
- Project conventions, naming rules, or code style
- Debugging conclusions and known failures
- Local development, test, deployment, or integration workflows
- Constraints future agents should not rediscover

Prefer editing the relevant stable topic file. If the right location is unclear,
write a separate note in `inbox/`.

## Do Not Store

- Ordinary progress logs
- One-off chat summaries
- Secrets, tokens, cookies, credentials, or local-only state
- Unverified guesses unless clearly marked as pending verification
- Facts fully visible by opening a single file (cross-file structure, reasons,
  and decisions do belong here, even when the code "shows" them)
"""

DEFAULT_ROUTES = [
    {
        "id": "architecture",
        "task": "Architecture / module boundaries",
        "read_first": ["architecture/overview.md"],
        "also_consider": ["architecture/boundaries.md"],
    },
    {
        "id": "decisions",
        "task": "Design decisions",
        "read_first": ["decisions/active/project-decisions.md"],
        "also_consider": ["architecture/overview.md"],
    },
    {
        "id": "debugging",
        "task": "Debugging / known failures",
        "read_first": ["debugging/known-failures.md"],
        "also_consider": ["debugging/test-environment.md"],
    },
    {
        "id": "local-dev",
        "task": "Local dev / test / deploy",
        "read_first": ["workflows/local-dev.md"],
        "also_consider": ["workflows/deploy.md"],
    },
    {
        "id": "planning",
        "task": "Planning / current focus",
        "read_first": ["plans/current.md"],
        "also_consider": ["decisions/active/project-decisions.md"],
    },
    {
        "id": "code-style",
        "task": "Coding style / comments",
        "read_first": ["conventions/code-style.md"],
        "also_consider": ["conventions/comments.md"],
    },
]

ROUTES_YAML = """# Agent KB routes. Keep read_first narrow; use also_consider sparingly.
routes:
  - id: architecture
    task: Architecture / module boundaries
    read_first:
      - architecture/overview.md
    also_consider:
      - architecture/boundaries.md
  - id: decisions
    task: Design decisions
    read_first:
      - decisions/active/project-decisions.md
    also_consider:
      - architecture/overview.md
  - id: debugging
    task: Debugging / known failures
    read_first:
      - debugging/known-failures.md
    also_consider:
      - debugging/test-environment.md
  - id: local-dev
    task: Local dev / test / deploy
    read_first:
      - workflows/local-dev.md
    also_consider:
      - workflows/deploy.md
  - id: planning
    task: Planning / current focus
    read_first:
      - plans/current.md
    also_consider:
      - decisions/active/project-decisions.md
  - id: code-style
    task: Coding style / comments
    read_first:
      - conventions/code-style.md
    also_consider:
      - conventions/comments.md
"""

MAP_MD = """# KB Map

This is a readable view of `routes.yaml`. Keep routing narrow: one `Read First`
target and no more than two `Also Consider` targets per route.

## Task Routing

| Task Pattern | Read First | Also Consider |
| --- | --- | --- |
| Architecture / module boundaries | architecture/overview.md | architecture/boundaries.md |
| Design decisions | decisions/active/project-decisions.md | architecture/overview.md |
| Debugging / known failures | debugging/known-failures.md | debugging/test-environment.md |
| Local dev / test / deploy | workflows/local-dev.md | workflows/deploy.md |
| Planning / current focus | plans/current.md | decisions/active/project-decisions.md |
| Coding style / comments | conventions/code-style.md | conventions/comments.md |
"""

TOPIC_DOCS = {
    "architecture/overview.md": ("Architecture Overview", "Understanding the project structure or major components"),
    "architecture/boundaries.md": ("Architecture Boundaries", "Changing module responsibilities or cross-module behavior"),
    "decisions/active/project-decisions.md": ("Project Decisions", "Changing or relying on durable design decisions"),
    "debugging/known-failures.md": ("Known Failures", "Debugging recurring failures or surprising behavior"),
    "debugging/test-environment.md": ("Test Environment", "Running, fixing, or changing test setup"),
    "workflows/local-dev.md": ("Local Development", "Setting up or running the project locally"),
    "workflows/deploy.md": ("Deploy Workflow", "Changing release, deploy, or CI behavior"),
    "conventions/code-style.md": ("Code Style", "Changing code patterns, naming, or formatting conventions"),
    "conventions/comments.md": ("Comments", "Adding or changing project comment conventions"),
}

PLAN_CURRENT_MD = """# Current Plan

## Summary

No active plan recorded yet.

## Read When

- Continuing prior work or deciding the next project step

## Current Focus

None yet.

## Done

None yet.

## Next

{next}

## Open Questions

None yet.

## Related

None yet.

## Change Log

- {today} - Created initial lightweight plan.
"""

# Pending next step init records in plans/current.md so the distillation survives the init session.
DISTILLATION_NEXT_STEP = (
    "Run the one-time distillation pass to warm-start this KB: survey README/docs/git "
    "history, fill topic files with durable facts only, then remove this entry."
)

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_TEXTS = (
    "No durable knowledge recorded yet.",
    "Add durable project knowledge here.",
)
TRIM_PLACEHOLDER_TEXTS = PLACEHOLDER_TEXTS + (
    "No entries yet.",
    "None yet.",
)
TRIM_MAX_FILE_LINES = 120
TRIM_MAX_FILE_CHARS = 14000
TRIM_MAX_TOTAL_CHARS = 20000
TRIM_MAX_INBOX_NOTES = 5
TRIM_MAX_LINK_DEPTH = 3
TRIM_MAX_DOC_FANOUT = 10
TRIM_MAX_ROUTES = 15
# Char overage at or above this fraction is "major" (the file likely carries compactable bulk);
# anything else — including line-only overage — is "minor", an advisory the agent can stop on.
TRIM_MAJOR_OVERAGE = 0.10
TRANSCRIPT_CACHE_VERSION = 2


# Returns the repository root from an argparse namespace.
def repo_root(args: argparse.Namespace) -> Path:
    return Path(args.root).expanduser().resolve()


# Returns the `.agent-kb` directory for a repository root.
def kb_dir(root: Path) -> Path:
    return root / ".agent-kb"


# CLI params never logged: dispatch internals and the repo root (location, low signal).
LOG_DROP_ARGS = {"func", "command", "root"}
# Free-text params redacted to a length marker so the log never carries note content (secrets rule).
LOG_REDACT_ARGS = {"title", "body"}


# Builds a redacted dict of the CLI parameters: keeps structural flags, redacts free text, drops internals.
def redact_args(args: argparse.Namespace) -> dict:
    out: dict = {}
    for key, value in vars(args).items():
        if key in LOG_DROP_ARGS or value is None:
            continue
        if key in LOG_REDACT_ARGS:
            out[key] = f"<redacted:{len(str(value))}chars>"
        else:
            out[key] = value
    return out


# Appends one JSONL line per CLI run (params plus optional metrics); best-effort so logging never breaks a command.
def log_event(args: argparse.Namespace, command: str, exit_code: int, metrics: dict | None = None) -> None:
    try:
        kb = kb_dir(repo_root(args))
        if not kb.exists():
            return
        log_dir = kb / ".log"
        log_dir.mkdir(parents=True, exist_ok=True)
        event = {
            "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "event": "cli",
            "command": command,
            "exit": int(exit_code),
            "args": redact_args(args),
        }
        if metrics:
            event["metrics"] = metrics
        with (log_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")
    except Exception:
        return


# Reads JSONL events from the log, skipping blank or malformed lines.
def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


# Builds a stable dedupe key for transcript-backed KB read events.
def kb_read_event_key(event: dict) -> tuple[str, str, str]:
    return (str(event.get("session", "")), str(event.get("file", "")), str(event.get("ts", "")))


# Converts a transcript read into the shared events.jsonl record shape.
def kb_read_log_event(read: KbReadEvent) -> dict:
    return {
        "ts": read.timestamp,
        "event": "kb_read",
        "kind": "kb_read",
        "source": "backfill",
        "harness": read.harness,
        "session": read.session,
        "file": read.file,
        "chars": read.chars,
    }


# Appends new KB read events to events.jsonl while deduping by session/file/timestamp.
def append_kb_read_events(kb: Path, reads: list[KbReadEvent]) -> int:
    log_path = kb / ".log" / "events.jsonl"
    existing = {kb_read_event_key(event) for event in read_events(log_path) if event.get("event") == "kb_read"}
    new_events = []
    for read in reads:
        event = kb_read_log_event(read)
        key = kb_read_event_key(event)
        if key in existing:
            continue
        existing.add(key)
        new_events.append(event)
    if not new_events:
        return 0
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        for event in new_events:
            handle.write(json.dumps(event) + "\n")
    return len(new_events)


# Returns the local transcript backfill cache path inside the gitignored KB log directory.
def transcript_cache_path(kb: Path) -> Path:
    return kb / ".log" / "transcript-backfill-cache.json"


# Reads the local transcript backfill cache, dropping it when the schema version differs.
def read_transcript_cache(kb: Path) -> dict:
    path = transcript_cache_path(kb)
    if not path.exists():
        return {"version": TRANSCRIPT_CACHE_VERSION, "files": {}}
    try:
        cache = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"version": TRANSCRIPT_CACHE_VERSION, "files": {}}
    if not isinstance(cache, dict) or cache.get("version") != TRANSCRIPT_CACHE_VERSION:
        return {"version": TRANSCRIPT_CACHE_VERSION, "files": {}}
    if not isinstance(cache.get("files"), dict):
        cache["files"] = {}
    return cache


# Writes the local transcript backfill cache best-effort so stats never fails because of caching.
def write_transcript_cache(kb: Path, cache: dict) -> None:
    try:
        path = transcript_cache_path(kb)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cache, sort_keys=True) + "\n", encoding="utf-8")
    except OSError:
        return


# Builds a cheap file signature for deciding whether a transcript needs reparsing.
def transcript_signature(path: Path) -> dict | None:
    try:
        stat = path.stat()
    except OSError:
        return None
    return {"mtime_ns": stat.st_mtime_ns, "size": stat.st_size}


# Converts one transcript scan into a cache entry that keeps only denominator-safe session data.
def transcript_cache_entry(harness: str, signature: dict, scan: TranscriptScan) -> dict:
    return {
        "harness": harness,
        "mtime_ns": signature["mtime_ns"],
        "size": signature["size"],
        "sessions": sorted(scan.sessions),
    }


# Scans changed transcript files and reuses cached session ownership for unchanged files.
def scan_transcripts_incremental(root: Path, kb: Path, claude_dir: Path | None, codex_dir: Path | None) -> TranscriptScan:
    cache = read_transcript_cache(kb)
    cached_files = cache.get("files", {})
    next_files: dict[str, dict] = {}
    sessions: set[str] = set()
    reads: list[KbReadEvent] = []
    codex_needles = {str(root), root.name, ".agent-kb"}

    # Parses one transcript when changed, otherwise restores its cached root-owned sessions.
    def scan_path(path: Path, harness: str, needs_mention: bool) -> None:
        signature = transcript_signature(path)
        if signature is None:
            return
        key = str(path)
        cached = cached_files.get(key) if isinstance(cached_files, dict) else None
        if (
            isinstance(cached, dict)
            and cached.get("harness") == harness
            and cached.get("mtime_ns") == signature["mtime_ns"]
            and cached.get("size") == signature["size"]
        ):
            sessions.update(str(session) for session in cached.get("sessions", []))
            next_files[key] = cached
            return
        if needs_mention and not transcript_mentions(path, codex_needles):
            scan = TranscriptScan(set(), [])
        elif harness == "claude":
            scan = parse_claude_transcript(path, root)
        else:
            scan = parse_codex_transcript(path, root)
        sessions.update(scan.sessions)
        reads.extend(scan.reads)
        next_files[key] = transcript_cache_entry(harness, signature, scan)

    if claude_dir is not None:
        for path in claude_transcript_paths(claude_dir, root):
            scan_path(path, "claude", False)
    if codex_dir is not None:
        for path in transcript_paths(codex_dir):
            scan_path(path, "codex", True)

    write_transcript_cache(kb, {"version": TRANSCRIPT_CACHE_VERSION, "files": next_files})
    return TranscriptScan(sessions, reads)


# Scans transcripts for this repo and backfills KB read events into the local event log.
def backfill_kb_reads(root: Path, args: argparse.Namespace) -> tuple[TranscriptScan, int]:
    kb = kb_dir(root)
    claude_dir = None if args.no_backfill_claude else resolve_transcript_path(args.claude_dir)
    codex_dir = None if args.no_backfill_codex else resolve_transcript_path(args.codex_dir)
    scan = scan_transcripts_incremental(root, kb, claude_dir, codex_dir)
    added = append_kb_read_events(kb, scan.reads)
    return scan, added


# Treats a logged event as part of the current session if its timestamp falls within the recency window.
def event_is_recent(event: dict, window_seconds: int = 7200) -> bool:
    ts = event.get("ts")
    if not ts:
        return False
    try:
        when = dt.datetime.fromisoformat(ts)
    except ValueError:
        return False
    if when.tzinfo is None:
        when = when.replace(tzinfo=dt.timezone.utc)
    return (dt.datetime.now(dt.timezone.utc) - when).total_seconds() <= window_seconds


# Reports whether a recent trim diagnose already recommended compacting, so the loop can skip re-printing the full prompt.
def trim_loop_in_progress(kb: Path) -> bool:
    for event in reversed(read_events(kb / ".log" / "events.jsonl")):
        if event.get("command") != "trim":
            continue
        metrics = event.get("metrics") or {}
        # Only diagnose runs carry the "compact" signal; --write runs report deleted/husks instead.
        if "compact" not in metrics:
            continue
        return bool(metrics.get("compact")) and event_is_recent(event)
    return False


# Counts how often each KB file changed in git history; reads the nested .agent-kb repo when present, else the parent repo's .agent-kb path.
def git_churn(root: Path) -> list[tuple[str, int]]:
    kb = kb_dir(root)
    if (kb / ".git").exists():
        # KB is its own repo: every tracked file is a KB file, so no pathspec; paths come back relative to .agent-kb.
        cmd = ["git", "-C", str(kb), "log", "--format=", "--name-only"]
    else:
        cmd = ["git", "-C", str(root), "log", "--format=", "--name-only", "--", ".agent-kb"]
    try:
        result = subprocess.run(
            cmd,
            check=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    counts: dict[str, int] = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        counts[line] = counts.get(line, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


# Writes content only when the target file does not already exist.
def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


# Builds a stable topic document with the required lightweight sections.
def render_topic(title: str, read_when: str) -> str:
    today = dt.date.today().isoformat()
    return f"""# {title}

## Summary

No entries yet.

## Read When

- {read_when}

## Current Knowledge

None yet.

## Related

None yet.

## Change Log

- {today} - Created initial KB topic.
"""


# Builds the lightweight current plan document with today's date and an optional pending next step.
def render_current_plan(next_step: str | None = None) -> str:
    return PLAN_CURRENT_MD.format(
        today=dt.date.today().isoformat(), next=next_step or "None yet."
    )


# Builds the KB meta marker so tooling can read schema and mode without scanning topic files.
def render_kb_meta(mode: str) -> str:
    return render_kb_meta_record(SCHEMA_VERSION, mode, dt.date.today().isoformat())


# Builds a KB meta marker from explicit fields, preserving mode/created during upgrade rewrites.
def render_kb_meta_record(schema_version: int, mode: str, created: str) -> str:
    return (
        f"schema_version: {schema_version}\n"
        f"mode: {mode}\n"
        f"created: {created}\n"
    )


# Parses the tiny .kb-meta.yaml subset into string fields and format warnings.
def read_kb_meta(kb: Path) -> tuple[dict[str, str] | None, list[str]]:
    path = kb / KB_META_FILE
    if not path.exists():
        return None, []
    meta: dict[str, str] = {}
    warnings = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            warnings.append(f".agent-kb/{KB_META_FILE} line {line_number}: expected key: value")
            continue
        key, value = [part.strip() for part in stripped.split(":", 1)]
        meta[key] = value
    return meta, warnings


# Parses a schema_version field into a non-negative integer when it is well-formed.
def parse_schema_version(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        parsed = int(value)
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


# Checks whether the parent .gitignore already excludes .agent-kb/.
def parent_gitignores_kb(root: Path) -> bool:
    path = root / ".gitignore"
    if not path.exists():
        return False
    entries = {line.strip().rstrip("/") for line in path.read_text(encoding="utf-8").splitlines()}
    return ".agent-kb" in entries


# Infers the KB versioning mode from current files when older KBs lack metadata.
def infer_kb_mode(root: Path, kb: Path) -> str:
    if (kb / ".git").exists():
        return "nested"
    if parent_gitignores_kb(root):
        return "local"
    return "shared"


# Creates or refreshes .kb-meta.yaml while preserving existing mode and created fields when valid.
def upgrade_kb_meta(root: Path, kb: Path) -> tuple[str, dict[str, str], str | None]:
    meta, warnings = read_kb_meta(kb)
    inferred_note = None
    if meta is None:
        mode = infer_kb_mode(root, kb)
        created = dt.date.today().isoformat()
        (kb / KB_META_FILE).write_text(render_kb_meta_record(SCHEMA_VERSION, mode, created), encoding="utf-8")
        return "created", {"schema_version": str(SCHEMA_VERSION), "mode": mode, "created": created}, f"mode inferred as {mode}"

    schema_number = parse_schema_version(meta.get("schema_version"))
    if schema_number is not None and schema_number > SCHEMA_VERSION:
        return "current", meta, f"schema {schema_number} is newer than this skill; update the skill before upgrading"

    mode = meta.get("mode", "")
    if mode not in KB_MODES:
        mode = infer_kb_mode(root, kb)
        inferred_note = f"mode inferred as {mode}"
    created = meta.get("created") or dt.date.today().isoformat()
    desired = render_kb_meta_record(SCHEMA_VERSION, mode, created)
    path = kb / KB_META_FILE
    if path.read_text(encoding="utf-8") == desired and not warnings:
        return "current", {"schema_version": str(SCHEMA_VERSION), "mode": mode, "created": created}, None
    path.write_text(desired, encoding="utf-8")
    return "updated", {"schema_version": str(SCHEMA_VERSION), "mode": mode, "created": created}, inferred_note


# Warns when KB metadata is missing or stamped with a different scaffold schema.
def schema_drift_warnings(kb: Path) -> list[str]:
    meta, meta_warnings = read_kb_meta(kb)
    if meta is None:
        return [f"KB scaffold has no .agent-kb/{KB_META_FILE}; run upgrade to backfill schema metadata"]
    warnings = [f"{warning}; run upgrade to refresh schema metadata" for warning in meta_warnings]
    schema = meta.get("schema_version")
    schema_number = parse_schema_version(schema)
    if schema_number is None:
        warnings.append(f"KB scaffold schema is {schema or 'unknown'}; run upgrade to refresh schema metadata")
    elif schema_number < SCHEMA_VERSION:
        found = schema or "unknown"
        warnings.append(f"KB scaffold is schema {found}; this skill writes schema {SCHEMA_VERSION} - run upgrade")
    elif schema_number > SCHEMA_VERSION:
        warnings.append(f"KB scaffold is schema {schema_number}; this skill writes schema {SCHEMA_VERSION} - update this skill before modifying the KB")
    return warnings


# Formats a list of route paths for the Markdown routing table.
def format_route_paths(paths: list[str]) -> str:
    return ", ".join(paths) if paths else "-"


# Renders a Markdown routing table from route dictionaries.
def render_map(routes: list[dict[str, object]]) -> str:
    lines = [
        "# KB Map",
        "",
        "This is a readable view of `routes.yaml`. Keep routing narrow: one `Read First`",
        "target and no more than two `Also Consider` targets per route.",
        "",
        "## Task Routing",
        "",
        "| Task Pattern | Read First | Also Consider |",
        "| --- | --- | --- |",
    ]
    for route in routes:
        read_first = [str(path) for path in route.get("read_first", [])]
        also_consider = [str(path) for path in route.get("also_consider", [])]
        lines.append(f"| {route.get('task', '')} | {format_route_paths(read_first)} | {format_route_paths(also_consider)} |")
    return "\n".join(lines) + "\n"


# Renders route dictionaries into the supported routes.yaml subset.
def render_routes_yaml(routes: list[dict[str, object]]) -> str:
    lines = ["# Agent KB routes. Keep read_first narrow; use also_consider sparingly.", "routes:"]
    for route in routes:
        lines.append(f"  - id: {route.get('id', '')}")
        lines.append(f"    task: {route.get('task', '')}")
        for key in ["read_first", "also_consider"]:
            lines.append(f"    {key}:")
            for path in [str(path) for path in route.get(key, [])]:
                lines.append(f"      - {path}")
    return "\n".join(lines) + "\n"


# Parses the supported routes.yaml subset into route dictionaries.
def parse_routes_yaml(routes_path: Path) -> tuple[list[dict[str, object]], list[str]]:
    if not routes_path.exists():
        return [], ["missing .agent-kb/routes.yaml"]

    routes: list[dict[str, object]] = []
    errors = []
    current: dict[str, object] | None = None
    current_list: str | None = None
    saw_routes = False

    for line_number, line in enumerate(routes_path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "routes:":
            saw_routes = True
            continue
        if not saw_routes:
            errors.append(f"routes.yaml line {line_number}: expected routes:")
            continue
        if line.startswith("  - "):
            if current is not None:
                routes.append(current)
            current = {"read_first": [], "also_consider": []}
            current_list = None
            key_value = line[4:].strip()
            if not key_value:
                continue
            if ":" not in key_value:
                errors.append(f"routes.yaml line {line_number}: invalid route entry")
                continue
            key, value = [part.strip() for part in key_value.split(":", 1)]
            current[key] = value
            continue
        if current is None:
            errors.append(f"routes.yaml line {line_number}: route field before route entry")
            continue
        if line.startswith("    ") and not line.startswith("      - "):
            field = line[4:].strip()
            if ":" not in field:
                errors.append(f"routes.yaml line {line_number}: invalid field")
                continue
            key, value = [part.strip() for part in field.split(":", 1)]
            if key in {"read_first", "also_consider"}:
                current[key] = []
                current_list = key
            else:
                current[key] = value
                current_list = None
            continue
        if line.startswith("      - "):
            if current_list not in {"read_first", "also_consider"}:
                errors.append(f"routes.yaml line {line_number}: list item without list field")
                continue
            value = line[8:].strip()
            if not value:
                errors.append(f"routes.yaml line {line_number}: empty path")
                continue
            current[current_list].append(value)  # type: ignore[index, union-attr]
            continue
        errors.append(f"routes.yaml line {line_number}: unsupported YAML shape")

    if current is not None:
        routes.append(current)
    if not saw_routes:
        errors.append("routes.yaml is missing routes:")
    for index, route in enumerate(routes, 1):
        for key in ["id", "task", "read_first", "also_consider"]:
            if key not in route:
                errors.append(f"routes.yaml route {index} missing {key}")
    return routes, errors


# Converts route dictionaries into map-compatible routing rows.
def rows_from_routes(routes: list[dict[str, object]]) -> list[tuple[str, str, str]]:
    rows = []
    for route in routes:
        read_first = [str(path) for path in route.get("read_first", [])]
        also_consider = [str(path) for path in route.get("also_consider", [])]
        rows.append((str(route.get("task", "")), format_route_paths(read_first), format_route_paths(also_consider)))
    return rows


# Adds or refreshes the protocol section in one entry file, migrating legacy pointer text and preserving the rest.
def upsert_protocol_in_file(path: Path, counterpart_note: str) -> str:
    if not path.exists():
        path.write_text(counterpart_note + RUNTIME_PROTOCOL, encoding="utf-8")
        return "created"

    original = path.read_text(encoding="utf-8")
    text = LEGACY_POINTER_LINE_RE.sub(r"See [\1](\1) for repository instructions.", original)
    if PROTOCOL_SECTION_RE.search(text):
        updated = PROTOCOL_SECTION_RE.sub(RUNTIME_PROTOCOL.rstrip() + "\n\n", text).rstrip() + "\n"
        if updated == original:
            return "current"
        path.write_text(updated, encoding="utf-8")
        return "updated"

    index = protocol_insert_index(text)
    head, tail = text[:index], text[index:]
    head = head.rstrip("\n") + "\n\n" if head.strip() else head
    block = RUNTIME_PROTOCOL.rstrip() + "\n"
    block = block + "\n" + tail.lstrip("\n") if tail.strip() else block
    path.write_text((head + block).rstrip() + "\n", encoding="utf-8")
    return "appended"


# Finds where to slot a new protocol: under the file's lead section, not above it — after the
# H1/intro and the first `## ` section, before the second `## ` (or end of file as a fallback).
def protocol_insert_index(text: str) -> int:
    lines = text.splitlines(keepends=True)
    pos = 0
    i = 0
    # Skip a leading H1 title line if present, so the protocol sits under it, not above.
    if i < len(lines) and lines[i].lstrip().startswith("# "):
        pos += len(lines[i])
        i += 1
    # Skip the title's intro paragraph up to the first `## ` subheading.
    while i < len(lines) and not lines[i].lstrip().startswith("## "):
        pos += len(lines[i])
        i += 1
    # If a first section exists, skip past it so the protocol lands under it, not above the
    # consumer's lead section; with no `## ` at all this returns end-of-file (graceful append).
    if i < len(lines):
        pos += len(lines[i])
        i += 1
        while i < len(lines) and not lines[i].lstrip().startswith("## "):
            pos += len(lines[i])
            i += 1
    return pos


# Injects the canonical protocol into every entry file so each harness gets it pinned at session start.
def upsert_runtime_protocol(root: Path) -> list[tuple[str, str]]:
    preexisting = {name: (root / name).exists() for name in PROTOCOL_FILES}
    results = []
    for name in PROTOCOL_FILES:
        other = next(n for n in PROTOCOL_FILES if n != name)
        note = COUNTERPART_NOTE_TMPL.format(other=other) if preexisting[other] else ""
        results.append((name, upsert_protocol_in_file(root / name, note)))
    return results


# Keeps the best-effort event log out of git; lives inside the KB so it travels with the scaffold.
KB_GITIGNORE = ".log/\n"


# Picks the versioning mode from init flags; defaults to the personal nested repo.
def resolve_versioning_mode(args: argparse.Namespace) -> str:
    if getattr(args, "shared", False):
        return "shared"
    if getattr(args, "local", False):
        return "local"
    return "nested"


# Ensures the project root .gitignore keeps .agent-kb/ out of the parent repo; appends only when the entry is missing.
def ensure_parent_gitignore(root: Path) -> str:
    path = root / ".gitignore"
    entry = ".agent-kb/"
    if not path.exists():
        path.write_text(entry + "\n", encoding="utf-8")
        return "created"
    text = path.read_text(encoding="utf-8")
    existing = {line.strip().rstrip("/") for line in text.splitlines()}
    if ".agent-kb" in existing:
        return "present"
    separator = "" if text == "" or text.endswith("\n") else "\n"
    path.write_text(text + separator + entry + "\n", encoding="utf-8")
    return "updated"


# Reports whether the project root sits inside a git work tree, so init can word the .gitignore note honestly instead of asserting a parent repo that may not exist.
def parent_is_git_repo(root: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
    except FileNotFoundError:
        return False
    return result.returncode == 0 and result.stdout.strip() == "true"


# Makes .agent-kb/ its own git repo with an initial snapshot so KB history stays out of the parent repo; degrades to a warning if git is missing or unconfigured.
def init_nested_repo(kb: Path) -> str:
    if (kb / ".git").exists():
        return "exists"
    try:
        for command in (
            ["git", "init", "-q"],
            ["git", "add", "-A"],
            ["git", "commit", "-q", "-m", "initial KB snapshot"],
        ):
            subprocess.run(command, cwd=kb, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "failed"
    return "created"


# Initializes the KB scaffold, runtime protocol, versioning mode, and any just-in-time next-step hints.
def command_init(args: argparse.Namespace) -> int:
    root = repo_root(args)
    kb = kb_dir(root)
    mode = resolve_versioning_mode(args)
    created = []

    for directory in [
        kb / "inbox",
        kb / "architecture",
        kb / "decisions" / "active",
        kb / "decisions" / "superseded",
        kb / "debugging",
        kb / "workflows",
        kb / "conventions",
        kb / "plans",
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    for relative, content in {
        "start.md": START_MD,
        "routes.yaml": ROUTES_YAML,
        "map.md": MAP_MD,
        "plans/current.md": render_current_plan(DISTILLATION_NEXT_STEP),
        ".gitignore": KB_GITIGNORE,
        ".kb-meta.yaml": render_kb_meta(mode),
    }.items():
        if write_if_missing(kb / relative, content):
            created.append(str(Path(".agent-kb") / relative))

    for relative, (title, read_when) in TOPIC_DOCS.items():
        if write_if_missing(kb / relative, render_topic(title, read_when)):
            created.append(str(Path(".agent-kb") / relative))

    protocol_actions = upsert_runtime_protocol(root)

    # Set up the chosen versioning mode: nested/local keep the KB out of the parent
    # repo via .gitignore; nested additionally gives the KB its own git history.
    gitignore_action = None
    nested_status = None
    if mode in ("nested", "local"):
        gitignore_action = ensure_parent_gitignore(root)
    if mode == "nested":
        nested_status = init_nested_repo(kb)

    print(f"Initialized KB at {kb}")
    for name, action in protocol_actions:
        print(f"{name} protocol {action}.")
    if created:
        print("Created files:")
        for path in created:
            print(f"- {path}")

    print(f"Versioning mode: {mode}.")
    if gitignore_action is not None:
        if parent_is_git_repo(root):
            print(f"Root .gitignore {gitignore_action} (.agent-kb/ ignored by the parent repo).")
        else:
            print(f"Root .gitignore {gitignore_action}; .agent-kb/ is ignored and ready for when you git init the project.")
    if mode == "nested":
        if nested_status == "created":
            print("Nested KB repo initialized with an initial commit.")
            print("Commit future KB changes with: git -C .agent-kb add -A && git -C .agent-kb commit")
        elif nested_status == "exists":
            print("Nested KB repo already present; left as-is.")
        elif nested_status == "failed":
            print("WARNING: could not initialize the nested KB repo (git missing or unconfigured).")
            print("Set it up manually: git -C .agent-kb init && git -C .agent-kb add -A && git -C .agent-kb commit -m 'initial KB snapshot'")
    elif mode == "shared":
        print("KB will travel with the parent repo; commit .agent-kb/ alongside your code.")
    elif mode == "local":
        print("KB is local-only and git-ignored; it has no version history.")
    if kb_is_empty_scaffold(kb):
        print(
            "NEXT STEP - REQUIRED BEFORE YOU CLOSE OUT: this KB is an empty scaffold with no "
            "project knowledge yet. Tell the user it needs a one-time distillation pass to be "
            "useful, and offer to run it now: survey README/docs/git history, then fill topic "
            "files with durable facts only (decisions, boundaries, pitfalls, doc-vs-reality "
            "gaps), and mine git history for anomalies - silent dependency downgrades, version "
            "pins, reverts, fix commits - with `git log -p`, not just subjects; record each "
            "anomaly as a suspected workaround even when the reason is unrecorded. Not code "
            "summaries or obvious code facts. "
            "Only run it if the user confirms; if they decline, leave the scaffold as-is."
        )
    return 0, {"created": len(created), "mode": mode}


# Updates a scaffold file when missing or when explicit overwrite is allowed.
def upgrade_scaffold_file(path: Path, content: str, write_existing: bool) -> str:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return "created"
    if path.read_text(encoding="utf-8") == content:
        return "current"
    if write_existing:
        path.write_text(content, encoding="utf-8")
        return "updated"
    return "needs review"


# Upgrades generated protocol files while leaving project-specific KB content intact.
def command_upgrade(args: argparse.Namespace) -> int:
    root = repo_root(args)
    kb = kb_dir(root)
    if not kb.exists():
        print("ERROR: missing .agent-kb/; run init first")
        return 1

    if not (kb / "inbox").exists():
        (kb / "inbox").mkdir(parents=True)

    meta_action, meta, meta_note = upgrade_kb_meta(root, kb)
    protocol_actions = upsert_runtime_protocol(root)
    gitignore_action = upgrade_scaffold_file(kb / ".gitignore", KB_GITIGNORE, False)
    start_action = upgrade_scaffold_file(kb / "start.md", START_MD, args.write_start)
    routes_action = upgrade_scaffold_file(kb / "routes.yaml", ROUTES_YAML, args.write_routes)
    plan_action = upgrade_scaffold_file(kb / "plans" / "current.md", render_current_plan(), args.write_plan)
    routes, route_errors = parse_routes_yaml(kb / "routes.yaml")
    map_content = render_map(routes) if not route_errors else MAP_MD
    map_action = upgrade_scaffold_file(kb / "map.md", map_content, args.write_map)
    custom_routes_preserved = routes_action == "needs review" and not args.write_routes and not route_errors
    custom_plan_preserved = plan_action == "needs review" and not args.write_plan

    print(f"Upgraded KB at {kb}")
    print(f".agent-kb/{KB_META_FILE} {meta_action}.")
    if meta_note:
        print(f"Metadata {meta_note}.")
    for name, action in protocol_actions:
        print(f"{name} protocol {action}.")
    print(f".agent-kb/.gitignore {gitignore_action}.")
    print(f".agent-kb/start.md {start_action}.")
    if custom_routes_preserved:
        print(".agent-kb/routes.yaml custom routes preserved.")
    else:
        print(f".agent-kb/routes.yaml {routes_action}.")
    if custom_plan_preserved:
        print(".agent-kb/plans/current.md custom preserved.")
    else:
        print(f".agent-kb/plans/current.md {plan_action}.")
    print(f".agent-kb/map.md {map_action}.")
    if start_action == "needs review":
        print("Review .agent-kb/start.md manually or rerun with --write-start to replace it.")
    if custom_routes_preserved:
        if args.write_map:
            print("custom routes preserved; map generated from routes.yaml")
    elif routes_action == "needs review":
        print("Review .agent-kb/routes.yaml manually; use --write-routes only if you want the default routes.")
    if map_action == "needs review":
        print("Review .agent-kb/map.md manually; use --write-map only if you want the default routing table.")
    # Name the files awaiting review (routes are excluded when intentionally preserved) so stats/output need no second run.
    named_actions = [
        ("start.md", start_action),
        ("routes.yaml", "current" if custom_routes_preserved else routes_action),
        ("plans/current.md", "current" if custom_plan_preserved else plan_action),
        ("map.md", map_action),
    ]
    review_files = [name for name, action in named_actions if action == "needs review"]
    if review_files:
        print(f"needs review: {', '.join(review_files)}")
    if meta.get("mode") == "nested":
        print("Nested KB mode: verify with `git -C .agent-kb status` and `git -C .agent-kb diff`; commit KB changes when done.")
    return 0, {"needs_review": len(review_files), "review_files": review_files}


# Extracts the Task Routing rows from `.agent-kb/map.md` for legacy compatibility.
def parse_map_rows(map_path: Path) -> tuple[list[tuple[str, str, str]], list[str]]:
    if not map_path.exists():
        return [], ["missing .agent-kb/map.md"]

    rows = []
    errors = []
    lines = map_path.read_text(encoding="utf-8").splitlines()
    in_table = False
    header_seen = False
    for line in lines:
        stripped = line.strip()
        if stripped == "## Task Routing":
            in_table = True
            continue
        if in_table and stripped.startswith("## "):
            break
        if not in_table or not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells == ["Task Pattern", "Read First", "Also Consider"]:
            header_seen = True
            continue
        if all(set(cell) <= {"-", " "} for cell in cells):
            continue
        if len(cells) != 3:
            errors.append(f"invalid map row: {line}")
            continue
        rows.append((cells[0], cells[1], cells[2]))

    if not header_seen:
        errors.append("map.md is missing the required Task Routing header")
    return rows, errors


# Checks route shape rules that keep routing narrow and cheap to read.
def route_quality_warnings(routes: list[dict[str, object]]) -> list[str]:
    warnings = []
    for route in routes:
        route_id = str(route.get("id", "unknown"))
        read_first = route.get("read_first", [])
        also_consider = route.get("also_consider", [])
        if isinstance(read_first, list) and len(read_first) > 1:
            warnings.append(f"route {route_id} has more than one read_first path")
        if isinstance(also_consider, list) and len(also_consider) > 2:
            warnings.append(f"route {route_id} has more than two also_consider paths")
    return warnings


# Splits a map cell into candidate KB-relative paths.
def split_path_cell(value: str) -> list[str]:
    if value.strip().lower() in {"", "-", "none", "n/a"}:
        return []
    normalized = value.replace("<br>", ",").replace("<br/>", ",").replace("<br />", ",")
    return [part.strip() for part in re.split(r"[,;]", normalized) if part.strip()]


# Normalizes a KB-relative path and rejects unsafe or external values.
def normalize_kb_path(raw: str) -> Path | None:
    if "://" in raw or raw.startswith("#"):
        return None
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        return None
    return path


# Returns Markdown links from text while ignoring external URLs and anchors.
def markdown_links(text: str) -> list[str]:
    links = []
    for match in LINK_RE.finditer(text):
        target = match.group(1).split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        links.append(target)
    return links


# Resolves a document-relative Markdown link to a KB-relative path when it stays inside the KB.
def resolve_internal_link(source: Path, kb: Path, raw: str) -> Path | None:
    if Path(raw).is_absolute():
        return None
    candidate = (source.parent / raw).resolve()
    try:
        return candidate.relative_to(kb.resolve())
    except ValueError:
        return None


# Lists stable topic documents while excluding routing and inbox files.
def stable_topic_docs(kb: Path) -> list[Path]:
    docs = []
    for path in kb.rglob("*.md"):
        relative = path.relative_to(kb)
        if relative.parts[0] == "inbox" or relative in {Path("start.md"), Path("map.md")}:
            continue
        if ".generated." in path.name:
            continue
        docs.append(path)
    return sorted(docs)


# Checks whether a stable document has the sections agents need for skimming.
def topic_section_warnings(kb: Path) -> list[str]:
    warnings = []
    for path in stable_topic_docs(kb):
        relative = path.relative_to(kb)
        if relative.parts[0] == "plans":
            required = ["## Summary", "## Read When", "## Current Focus", "## Next"]
        else:
            required = ["## Summary", "## Read When", "## Current Knowledge"]
        text = path.read_text(encoding="utf-8")
        for section in required:
            if section not in text:
                warnings.append(f"{relative} missing {section}")
    return warnings


# Checks whether a topic document still contains starter placeholder text.
def topic_placeholder_warnings(kb: Path) -> list[str]:
    warnings = []
    for path in stable_topic_docs(kb):
        text = path.read_text(encoding="utf-8")
        for placeholder in PLACEHOLDER_TEXTS:
            if placeholder in text:
                warnings.append(f"{path.relative_to(kb)} still contains placeholder text: {placeholder}")
    return warnings


# Extracts the body of a second-level Markdown section by heading text.
def markdown_section_body(text: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", re.M | re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


# Checks whether a document contains a named second-level Markdown section.
def has_markdown_section(text: str, heading: str) -> bool:
    return bool(re.search(rf"^## {re.escape(heading)}\s*$", text, re.M))


# Checks whether a section body contains only starter placeholder text.
def is_placeholder_body(body: str) -> bool:
    normalized = body.strip()
    if not normalized:
        return True
    normalized_lines = [line.strip("- ").strip() for line in normalized.splitlines() if line.strip()]
    return bool(normalized_lines) and all(line in TRIM_PLACEHOLDER_TEXTS for line in normalized_lines)


# Checks whether a changelog only records initial scaffold creation.
def is_initial_changelog_only(body: str) -> bool:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    return len(lines) == 1 and "Created initial KB topic." in lines[0]


# Checks whether a stable topic has empty content sections and no links, ignoring its Change Log.
def is_content_empty_topic(path: Path, kb: Path) -> bool:
    relative = path.relative_to(kb)
    if relative in {Path("start.md"), Path("map.md"), Path("plans/current.md")}:
        return False
    if relative.parts[0] in {"inbox", "plans"}:
        return False
    text = path.read_text(encoding="utf-8")
    for heading in ["Summary", "Current Knowledge", "Related", "Change Log"]:
        if not has_markdown_section(text, heading):
            return False
    return (
        is_placeholder_body(markdown_section_body(text, "Summary"))
        and is_placeholder_body(markdown_section_body(text, "Current Knowledge"))
        and is_placeholder_body(markdown_section_body(text, "Related"))
        and not markdown_links(text)
    )


# Checks whether a stable topic is a pristine empty scaffold that can be safely deleted.
def is_empty_scaffold_topic(path: Path, kb: Path) -> bool:
    if not is_content_empty_topic(path, kb):
        return False
    return is_initial_changelog_only(markdown_section_body(path.read_text(encoding="utf-8"), "Change Log"))


# Checks whether the KB still has only starter topic scaffolds, using the same empty-topic test as trim.
def kb_is_empty_scaffold(kb: Path) -> bool:
    docs = stable_topic_docs(kb)
    topic_docs = [path for path in docs if path.relative_to(kb).parts[0] != "plans"]
    if not topic_docs:
        return False
    return all(is_empty_scaffold_topic(path, kb) for path in topic_docs)


# Checks whether a stable topic is an emptied husk: content gone, but its Change Log shows it once held knowledge.
def is_husk_after_merge_topic(path: Path, kb: Path) -> bool:
    if not is_content_empty_topic(path, kb):
        return False
    return not is_initial_changelog_only(markdown_section_body(path.read_text(encoding="utf-8"), "Change Log"))


# Maps internal Markdown link targets to the KB documents that reference them.
def incoming_link_sources(kb: Path) -> dict[Path, list[Path]]:
    incoming: dict[Path, list[Path]] = {}
    for source in kb.rglob("*.md"):
        source_relative = source.relative_to(kb)
        for raw in markdown_links(source.read_text(encoding="utf-8")):
            target = resolve_internal_link(source, kb, raw)
            if target is not None:
                incoming.setdefault(target, []).append(source_relative)
    return incoming


# Finds empty scaffold topic files that trim can remove without breaking links.
def empty_scaffold_topics(kb: Path) -> list[Path]:
    candidates = [path for path in stable_topic_docs(kb) if is_empty_scaffold_topic(path, kb)]
    candidate_relatives = {path.relative_to(kb) for path in candidates}
    incoming = incoming_link_sources(kb)
    safe = []
    for path in candidates:
        relative = path.relative_to(kb)
        linked_from_kept_docs = [source for source in incoming.get(relative, []) if source not in candidate_relatives]
        if not linked_from_kept_docs:
            safe.append(path)
    return safe


# Finds emptied husks left after a merge; trim only warns about them because deleting a file with history is a judged act.
def husk_after_merge_topics(kb: Path) -> list[Path]:
    return [path for path in stable_topic_docs(kb) if is_husk_after_merge_topic(path, kb)]


# Returns the path used to invoke this script so suggested commands copy-paste cleanly under symlinks.
def script_invocation() -> str:
    return sys.argv[0] or "agent_kb.py"


# Builds the agent handoff: the semantic step (agent judgment) plus the deterministic finisher commands to run after.
def trim_compact_prompt(args: argparse.Namespace) -> str:
    script = script_invocation()
    return (
        "  The size number is a PROXY for 'this file may be repeating itself or holding\n"
        "  dead detail'. Optimize the target, not the proxy: cut redundant and stale\n"
        "  INFORMATION. Shrinking bytes without removing information is not progress.\n"
        "  Remove: facts stated more than once (keep one canonical copy), detail that is\n"
        "  superseded or no longer durable, and routine Change Log churn (collapse\n"
        "  inbox-merge noise; keep entries that record a real decision). Merge\n"
        "  overlapping sections under the existing headings; do not change the schema.\n"
        "  Keep: every durable decision, constraint, failure, convention, and link, plus\n"
        "  the current conclusion and the traps. The reader is a future agent that must\n"
        "  still locate and trust each fact, so keep the structure (headings, distinct\n"
        "  lines, code blocks) that makes facts findable -- do not fuse content to save\n"
        "  space.\n"
        "  STOP when what remains is genuine and non-redundant, even if the file is still\n"
        "  over the size signal. A large file of real, distinct durable facts is a\n"
        "  correct end state -- report it and move on.\n"
        "  Then close the loop with the deterministic tools:\n"
        f"    python3 {script} upgrade --root {args.root} --write-map   # regenerate map.md if you changed routes.yaml\n"
        f"    python3 {script} trim --root {args.root} --recheck        # validate + re-diagnose in one step; stop once\n"
        "                                                              # the only thing over is genuine content."
    )


# Builds the rerun command from this script's actual invocation path so copy-paste works under symlinks.
def trim_write_command(args: argparse.Namespace) -> str:
    return f"python3 {script_invocation()} trim --root {args.root} --write"


# Lists stable topic docs with their char sizes (largest first) so size diagnostics can be shared.
def stable_doc_sizes(kb: Path) -> list[tuple[Path, int]]:
    sizes = [(path.relative_to(kb), len(path.read_text(encoding="utf-8"))) for path in stable_topic_docs(kb)]
    sizes.sort(key=lambda item: item[1], reverse=True)
    return sizes


# Measures stable-doc sizes (char- and line-based) and grades each oversize file by how far over budget it is.
def trim_size_report(
    kb: Path,
    max_file_lines: int = TRIM_MAX_FILE_LINES,
    max_file_chars: int = TRIM_MAX_FILE_CHARS,
    max_total_chars: int = TRIM_MAX_TOTAL_CHARS,
    max_inbox_notes: int = TRIM_MAX_INBOX_NOTES,
) -> dict:
    files = []
    total_chars = 0
    oversize = []
    for path in stable_topic_docs(kb):
        text = path.read_text(encoding="utf-8")
        chars = len(text)
        lines = len(text.splitlines())
        relative = path.relative_to(kb)
        files.append((relative, chars, lines))
        total_chars += chars
        # Char overage is the primary signal: joining short lines lowers the line count but not the chars.
        line_over = max(0, lines - max_file_lines)
        char_over = max(0, chars - max_file_chars)
        if line_over or char_over:
            line_pct = line_over / max_file_lines if max_file_lines else 0.0
            char_pct = char_over / max_file_chars if max_file_chars else 0.0
            # Only real bulk (chars) makes a file major; line-only overage stays advisory so the
            # agent compacts content instead of shaving lines/formatting to clear the signal.
            severity = "major" if char_pct >= TRIM_MAJOR_OVERAGE else "minor"
            oversize.append({
                "rel": relative,
                "lines": lines, "line_over": line_over, "line_pct": line_pct,
                "chars": chars, "char_over": char_over, "char_pct": char_pct,
                "worst_pct": max(line_pct, char_pct),
                "severity": severity,
            })
    files.sort(key=lambda item: item[1], reverse=True)
    oversize.sort(key=lambda item: item["worst_pct"], reverse=True)
    inbox_count = len(list((kb / "inbox").glob("*.md"))) if (kb / "inbox").exists() else 0
    inbox_over = inbox_count > max_inbox_notes
    major_oversize = [item for item in oversize if item["severity"] == "major"]
    return {
        "files": files,
        "total_chars": total_chars,
        "max_total_chars": max_total_chars,
        "max_file_lines": max_file_lines,
        "max_file_chars": max_file_chars,
        "oversize": oversize,
        "major_oversize": major_oversize,
        "inbox_count": inbox_count,
        "max_inbox_notes": max_inbox_notes,
        "inbox_over": inbox_over,
        "over_budget": total_chars > max_total_chars,
        # Only major overage or inbox backlog should drive another compaction pass; minor overage is optional.
        "compact_recommended": bool(major_oversize) or inbox_over,
        "minor_only": bool(oversize) and not major_oversize and not inbox_over,
    }


# Renders one oversize file's line/char overage and severity so the agent sees magnitude, not a binary trip.
def format_oversize_signal(item: dict) -> str:
    line_part = (
        f"{item['lines']} lines ({item['line_over']} over / {item['line_pct']:.0%})"
        if item["line_over"] else f"{item['lines']} lines (ok)"
    )
    char_part = (
        f"{item['chars']} chars ({item['char_over']} over / {item['char_pct']:.0%})"
        if item["char_over"] else f"{item['chars']} chars (ok)"
    )
    return f"{item['rel']}: {line_part}, {char_part} — {item['severity']}"


# Prints the per-file char/line breakdown trim counts toward its budget so agents never re-measure with wc.
def print_trim_size_breakdown(report: dict, indent: str = "  ") -> None:
    print("Budget scope (stable topic docs counted toward the char budget):")
    files = report["files"]
    if not files:
        print(f"{indent}(no stable topic docs)")
        return
    name_width = max(len(str(rel)) for rel, _, _ in files)
    name_width = max(name_width, len("total"))
    for rel, chars, lines in files:
        print(f"{indent}{str(rel):<{name_width}}  {chars:>6} chars  {lines:>4} lines")
    print(f"{indent}{'total':<{name_width}}  {report['total_chars']:>6} chars  (soft budget {report['max_total_chars']})")


# Removes deleted topic paths from routes and promotes remaining entries when needed.
def prune_routes(routes: list[dict[str, object]], deleted: set[Path]) -> tuple[list[dict[str, object]], bool]:
    changed = False
    pruned = []
    deleted_strings = {str(path) for path in deleted}
    for route in routes:
        read_first = [str(path) for path in route.get("read_first", []) if str(path) not in deleted_strings]
        also_consider = [str(path) for path in route.get("also_consider", []) if str(path) not in deleted_strings]
        if read_first != route.get("read_first", []) or also_consider != route.get("also_consider", []):
            changed = True
        if not read_first and also_consider:
            read_first = [also_consider.pop(0)]
            changed = True
        if not read_first and not also_consider:
            changed = True
            continue
        updated = dict(route)
        updated["read_first"] = read_first
        updated["also_consider"] = also_consider
        pruned.append(updated)
    return pruned, changed


# Runs KB validation without printing so maintenance commands can summarize it.
def validate_kb(kb: Path) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []

    if not kb.exists():
        return ["missing .agent-kb/"], warnings
    warnings.extend(schema_drift_warnings(kb))
    for relative in ["start.md", "routes.yaml", "map.md"]:
        if not (kb / relative).exists():
            errors.append(f"missing .agent-kb/{relative}")
    if not (kb / "inbox").is_dir():
        errors.append("missing .agent-kb/inbox/")

    routes, route_errors = parse_routes_yaml(kb / "routes.yaml")
    errors.extend(route_errors)
    rows = rows_from_routes(routes)
    if routes and (kb / "map.md").exists() and (kb / "map.md").read_text(encoding="utf-8") != render_map(routes):
        warnings.append("map.md differs from routes.yaml; update the readable view or rerun upgrade --write-map")
    warnings.extend(route_quality_warnings(routes))

    for _, read_first, also_consider in rows:
        for raw in split_path_cell(read_first) + split_path_cell(also_consider):
            normalized = normalize_kb_path(raw)
            if normalized is None:
                errors.append(f"invalid route path: {raw}")
            elif not (kb / normalized).exists():
                errors.append(f"route path does not exist: {raw}")

    for path in kb.rglob("*.md"):
        for raw in markdown_links(path.read_text(encoding="utf-8")):
            relative = resolve_internal_link(path, kb, raw)
            if relative is None:
                continue
            if not (kb / relative).exists():
                errors.append(f"broken link in {path.relative_to(kb)}: {raw}")

    reachable = reachable_docs(kb, rows)
    for path in stable_topic_docs(kb):
        relative = path.relative_to(kb)
        if relative not in reachable:
            warnings.append(f"stable topic is not reachable from routes/map/links: {relative}")
    warnings.extend(topic_section_warnings(kb))
    warnings.extend(topic_placeholder_warnings(kb))

    for note in sorted((kb / "inbox").glob("*.md")) if (kb / "inbox").exists() else []:
        text = note.read_text(encoding="utf-8")
        if "Suggested target:" not in text or "## Note" not in text:
            warnings.append(f"inbox note does not match template: {note.relative_to(kb)}")
    return errors, warnings


# Resolves internal Markdown links from a document to KB-relative Markdown paths.
def linked_docs_from(path: Path, kb: Path) -> list[Path]:
    links = []
    text = path.read_text(encoding="utf-8")
    for raw in markdown_links(text):
        relative = resolve_internal_link(path, kb, raw)
        if relative is None:
            continue
        if relative.suffix == ".md":
            links.append(relative)
    return links


# Computes each document's shallowest route-link depth by BFS from route entry paths.
def reachable_doc_depths(kb: Path, rows: list[tuple[str, str, str]]) -> dict[Path, int]:
    depths: dict[Path, int] = {}
    queue: deque[tuple[Path, int]] = deque()
    for _, read_first, also_consider in rows:
        for raw in split_path_cell(read_first) + split_path_cell(also_consider):
            normalized = normalize_kb_path(raw)
            if normalized and (kb / normalized).exists():
                queue.append((normalized, 0))

    while queue:
        relative, depth = queue.popleft()
        if relative in depths:
            continue
        depths[relative] = depth
        path = kb / relative
        if path.exists() and path.suffix == ".md":
            queue.extend((link, depth + 1) for link in linked_docs_from(path, kb))
    return depths


# Computes topic documents reachable from map routes and reachable Markdown links.
def reachable_docs(kb: Path, rows: list[tuple[str, str, str]]) -> set[Path]:
    return set(reachable_doc_depths(kb, rows))


# Builds trim-only structure advisories from graph depth, per-doc fanout, and route count budgets.
def trim_structure_report(kb: Path, routes: list[dict[str, object]]) -> dict:
    rows = rows_from_routes(routes)
    depths = reachable_doc_depths(kb, rows)
    stable_relatives = {path.relative_to(kb) for path in stable_topic_docs(kb)}
    deep_docs = [
        (relative, depths[relative])
        for relative in stable_relatives
        if relative in depths and depths[relative] > TRIM_MAX_LINK_DEPTH
    ]
    deep_docs.sort(key=lambda item: (item[1], str(item[0])), reverse=True)

    hubs = []
    for path in stable_topic_docs(kb):
        fanout = len(linked_docs_from(path, kb))
        if fanout > TRIM_MAX_DOC_FANOUT:
            hubs.append((path.relative_to(kb), fanout))
    hubs.sort(key=lambda item: (item[1], str(item[0])), reverse=True)

    route_count = len(routes)
    return {
        "deep_docs": deep_docs,
        "max_depth": TRIM_MAX_LINK_DEPTH,
        "hubs": hubs,
        "max_fanout": TRIM_MAX_DOC_FANOUT,
        "route_count": route_count,
        "max_routes": TRIM_MAX_ROUTES,
        "routes_over": route_count > TRIM_MAX_ROUTES,
        "has_signals": bool(deep_docs or hubs or route_count > TRIM_MAX_ROUTES),
    }


# Warns when an entry file (AGENTS.md/CLAUDE.md) is missing or lacks the current KB runtime protocol.
def protocol_presence_warnings(root: Path) -> list[str]:
    warnings = []
    for name in PROTOCOL_FILES:
        path = root / name
        if not path.exists():
            warnings.append(f"{name} is missing; run upgrade to create it with the KB runtime protocol")
        elif PROTOCOL_BODY_MARKER not in path.read_text(encoding="utf-8"):
            warnings.append(f"{name} does not carry the current KB runtime protocol; run upgrade")
    return warnings


# Prints scaffold validation results, adding runtime-protocol warnings that need the repo root.
def command_validate(args: argparse.Namespace) -> tuple[int, dict]:
    root = repo_root(args)
    kb = kb_dir(root)
    errors, warnings = validate_kb(kb)
    if kb.exists():
        warnings = warnings + protocol_presence_warnings(root)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    metrics = {"errors": len(errors), "warnings": len(warnings)}
    if errors:
        return 1, metrics
    print(f"OK: validated {kb}")
    if kb_is_empty_scaffold(kb):
        print(
            "ADVISORY: this KB is an empty scaffold (no distilled knowledge yet). "
            "If you just initialized it, offer the user the one-time distillation pass "
            "before closing out."
        )
    return 0, metrics


# Diagnoses or applies safe deterministic KB trimming, reporting advisory graph signals without making them blockers.
def command_trim(args: argparse.Namespace) -> int:
    root = repo_root(args)
    kb = kb_dir(root)
    if not kb.exists():
        print("ERROR: missing .agent-kb/")
        return 1

    routes, route_errors = parse_routes_yaml(kb / "routes.yaml")
    if route_errors:
        for error in route_errors:
            print(f"ERROR: {error}")
        return 1

    candidates = empty_scaffold_topics(kb)
    husks = husk_after_merge_topics(kb)
    report = trim_size_report(
        kb, args.max_file_lines, args.max_file_chars, args.max_total_chars, args.max_inbox_notes
    )
    structure_report = trim_structure_report(kb, routes)
    compact_recommended = report["compact_recommended"]

    if not args.write:
        if args.recheck:
            # --recheck folds the loop's validate step in so the agent runs one command per round, not two.
            errors, warnings = validate_kb(kb)
            summary = "OK" if not errors else f"{len(errors)} error(s)"
            if warnings:
                summary += f", {len(warnings)} warning(s)"
            print(f"Recheck (validate): {summary}.")
            for error in errors:
                print(f"  ERROR: {error}")
            for warning in warnings:
                print(f"  WARNING: {warning}")
            print()

        # Always show the breakdown so the agent trusts trim's count instead of re-running wc.
        print_trim_size_breakdown(report)
        print()

        cleanup = bool(candidates or husks)
        minor_only = report["minor_only"]
        structure_advisory = structure_report["has_signals"]
        if not (cleanup or compact_recommended or minor_only or structure_advisory):
            if report["over_budget"]:
                print("Trim diagnosis: lean (above soft budget).")
                print(f"  Structure is clean: no oversize files, husks, or inbox backlog. Total "
                      f"{report['total_chars']} chars is over the {report['max_total_chars']} soft budget, but that is")
                print("  likely legitimate durable content — do NOT compact to chase the number.")
            else:
                print("Trim diagnosis: KB is already lean.")
            print("No write step recommended.")
            return 0, {
                "candidates": 0,
                "husks": 0,
                "compact": False,
                "minor_only": False,
                "structure_advisory": False,
                "over_budget": report["over_budget"],
                "total_chars": report["total_chars"],
            }

        # Print the full compact prompt only on first detection (or with --verbose); later loop rounds get a pointer.
        show_full_prompt = args.verbose or not trim_loop_in_progress(kb)

        if compact_recommended:
            diagnosis = "cleanup + compact recommended" if cleanup else "compact recommended"
        elif cleanup:
            diagnosis = "cleanup recommended"
        elif structure_advisory:
            diagnosis = "structure advisories"
        else:
            diagnosis = "minor — optional"
        print(f"Trim diagnosis: {diagnosis}.")
        print()
        print("Details:")
        for path in candidates:
            print(f"- delete empty scaffold topic: {path.relative_to(kb)}")
        for path in husks:
            print(f"- husk after merge: {path.relative_to(kb)} (content empty, Change Log grown; delete manually)")
        for item in report["oversize"]:
            label = "compact signal" if item["severity"] == "major" else "minor signal"
            print(f"- {label}: {format_oversize_signal(item)}")
        if report["inbox_over"]:
            print(f"- compact signal: inbox has {report['inbox_count']} notes (max {report['max_inbox_notes']})")
        if report["over_budget"] and show_full_prompt:
            print(f"- soft signal: stable KB docs total {report['total_chars']} chars (above {report['max_total_chars']} soft budget; not a reason to over-compact)")
        for relative, depth in structure_report["deep_docs"]:
            print(f"- depth advisory: {relative} is depth {depth} from routes (budget {structure_report['max_depth']})")
        for relative, fanout in structure_report["hubs"]:
            print(f"- hub advisory: {relative} links to {fanout} docs (budget {structure_report['max_fanout']}); consider splitting if it mixes tasks")
        if structure_report["routes_over"]:
            print(f"- route-count advisory: routes.yaml has {structure_report['route_count']} routes (budget {structure_report['max_routes']})")
        if candidates:
            print()
            print("Next:")
            print(f"  {trim_write_command(args)}")
        if structure_advisory:
            print()
            print("Structure advisories are soft: adjust routes, split hubs, or lift deep docs only")
            print("when the structure hides recurring tasks; then rerun trim --recheck.")
        if compact_recommended:
            print()
            # Always-on guardrail so it survives even when the full prompt is suppressed in later loop rounds.
            print("Size is only a proxy: cut redundant or stale information, not bytes. Stop once")
            print("the rest is genuine, distinct durable facts, even if still over the signal.")
            print()
            if show_full_prompt:
                print("Agent compact prompt:")
                print(trim_compact_prompt(args))
            else:
                print("Agent compact prompt: omitted (already shown earlier this loop; rerun with --verbose for the full text).")
        elif minor_only:
            print()
            print("Minor overage only — optional. Safe to stop here; compact only if you can see real duplication above.")
        return 0, {
            "candidates": len(candidates),
            "husks": len(husks),
            "compact": compact_recommended,
            "minor_only": minor_only,
            "structure_advisory": structure_advisory,
            "over_budget": report["over_budget"],
            "total_chars": report["total_chars"],
        }

    deleted = set()
    for path in candidates:
        path.unlink()
        deleted.add(path.relative_to(kb))

    pruned_routes, routes_changed = prune_routes(routes, deleted)
    if deleted or routes_changed:
        (kb / "routes.yaml").write_text(render_routes_yaml(pruned_routes), encoding="utf-8")
        (kb / "map.md").write_text(render_map(pruned_routes), encoding="utf-8")

    errors, _ = validate_kb(kb)
    print("Trim complete.")
    print(f"- Deleted {len(deleted)} empty topic nodes.")
    print(f"- Updated routes.yaml: {'yes' if deleted or routes_changed else 'no'}.")
    print(f"- Regenerated map.md: {'yes' if deleted or routes_changed else 'no'}.")
    print(f"- Validate: {'OK' if not errors else 'FAILED'}.")
    if deleted:
        print("Deleted nodes:")
        for path in sorted(deleted):
            print(f"- {path}")
    if husks:
        print("Husks after merge (delete manually):")
        for path in sorted(husks):
            print(f"- {path.relative_to(kb)}")
    if compact_recommended:
        print("Agent compact still recommended for non-empty topics.")
    for error in errors:
        print(f"ERROR: {error}")
    return (1 if errors else 0), {"deleted": len(deleted), "husks": len(husks), "validate_errors": len(errors)}


# Converts a note title into a short filesystem-safe slug.
def slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    return slug[:48] or "note"


# Creates a separate inbox note for durable knowledge discovered during work.
def command_note(args: argparse.Namespace) -> int:
    root = repo_root(args)
    kb = kb_dir(root)
    inbox = kb / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    body = args.body if args.body is not None else sys.stdin.read().strip()
    if not body:
        print("ERROR: note body is empty", file=sys.stderr)
        return 1

    now = dt.datetime.now().strftime("%Y-%m-%dT%H%M%S")
    today = dt.date.today().isoformat()
    title = args.title.strip()
    target = args.target.strip() if args.target else "unsure"
    path = inbox / f"{now}-{slugify(title)}.md"
    content = f"""# {title}

Date: {today}
Suggested target: {target}

## Note

{body.rstrip()}
"""
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path}")
    return 0, {"target_unsure": target.lower() == "unsure"}


# Parses an inbox note into title, date, suggested target, and body fields.
def parse_inbox_note(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", text, re.M)
    date_match = re.search(r"^Date:\s*(.+)$", text, re.M)
    target_match = re.search(r"^Suggested target:\s*(.+)$", text, re.M)
    note_match = re.search(r"^## Note\s*\n(.*)\Z", text, re.M | re.S)
    return {
        "title": title_match.group(1).strip() if title_match else path.stem,
        "date": date_match.group(1).strip() if date_match else dt.date.today().isoformat(),
        "target": target_match.group(1).strip() if target_match else "unsure",
        "body": note_match.group(1).strip() if note_match else "",
    }


# Inserts text under a named Markdown heading, before the next same-level heading.
def insert_under_heading(text: str, heading: str, addition: str) -> tuple[str, bool]:
    pattern = re.compile(rf"(^## {re.escape(heading)}\s*$)(.*?)(?=^## |\Z)", re.M | re.S)
    match = pattern.search(text)
    if not match:
        return text.rstrip() + f"\n\n## {heading}\n\n{addition.rstrip()}\n", False
    existing = match.group(2).rstrip()
    replacement = f"{match.group(1)}{existing}\n\n{addition.rstrip()}\n\n"
    return text[: match.start()] + replacement + text[match.end() :], True


# Appends an inbox note to an existing stable target document.
def append_note_to_target(target: Path, note: dict[str, str], source_name: str) -> None:
    text = target.read_text(encoding="utf-8")
    addition = f"### {note['title']}\n\nDate: {note['date']}\nSource: `inbox/{source_name}`\n\n{note['body']}\n"
    text, _ = insert_under_heading(text, "Current Knowledge", addition)
    change = f"- {note['date']} - Merged inbox note `{source_name}`."
    text, _ = insert_under_heading(text, "Change Log", change)
    target.write_text(text.rstrip() + "\n", encoding="utf-8")


# Merges inbox notes with valid existing targets and leaves unresolved notes in place.
def command_compile(args: argparse.Namespace) -> int:
    root = repo_root(args)
    kb = kb_dir(root)
    inbox = kb / "inbox"
    merged = 0
    kept = []

    if not inbox.exists():
        print("ERROR: missing .agent-kb/inbox/")
        return 1

    for path in sorted(inbox.glob("*.md")):
        note = parse_inbox_note(path)
        target_raw = note["target"]
        target_rel = normalize_kb_path(target_raw)
        if target_raw.lower() == "unsure" or target_rel is None:
            kept.append((path.name, "target is unsure or invalid"))
            continue
        target = kb / target_rel
        if not target.is_file():
            kept.append((path.name, f"target is not an existing file: {target_raw}"))
            continue
        append_note_to_target(target, note, path.name)
        path.unlink()
        merged += 1

    print(f"Merged: {merged}")
    print(f"Deleted: {merged}")
    print(f"Unresolved: {len(kept)}")
    for name, reason in kept:
        print(f"- {name}: {reason}")
    return 0, {"merged": merged, "unresolved": len(kept)}


# Prints (label, value, suffix) rows as a proportional ASCII bar chart for quick visual scanning.
def print_bar_chart(rows: list[tuple[str, int, str]], indent: str = "  ", width: int = 24) -> None:
    max_value = max((value for _, value, _ in rows), default=0)
    label_width = max((len(label) for label, _, _ in rows), default=0)
    for label, value, suffix in rows:
        filled = max(1, round(value / max_value * width)) if max_value > 0 and value > 0 else 0
        bar = "█" * filled
        print(f"{indent}{label:<{label_width}}  {bar:<{width}}  {suffix}")


# Formats a numerator and denominator as both count and percentage.
def format_rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0/0 (n/a)"
    return f"{numerator}/{denominator} ({numerator / denominator * 100:.1f}%)"


# Prints read-observability metrics from transcript backfill and logged KB read events.
def print_kb_read_stats(
    kb: Path,
    events: list[dict],
    scan: TranscriptScan | None,
    top: int,
    dead_sessions: int,
    backfill_error: str | None = None,
) -> None:
    read_events = [event for event in events if event.get("event") == "kb_read"]
    print("KB read usage (transcript backfill):")
    if backfill_error:
        print(f"  (backfill failed: {backfill_error})")
    elif scan is None:
        print("  (backfill disabled)")
    else:
        hit_sessions = {str(event.get("session", "")) for event in read_events if str(event.get("session", "")) in scan.sessions}
        print(f"  scanned sessions: {len(scan.sessions)}")
        print(f"  KB hit rate: {format_rate(len(hit_sessions), len(scan.sessions))}")
    if not read_events:
        print("  (no KB reads logged yet)")
        return

    chars_by_session: dict[str, int] = {}
    reads_by_file: dict[str, int] = {}
    for event in read_events:
        session = str(event.get("session", ""))
        file = str(event.get("file", ""))
        chars = int(event.get("chars") or 0)
        chars_by_session[session] = chars_by_session.get(session, 0) + chars
        reads_by_file[file] = reads_by_file.get(file, 0) + 1
    session_count = max(1, len(chars_by_session))
    print(f"  estimated KB chars/session: {sum(chars_by_session.values()) // session_count}")
    rows = [(file, count, str(count)) for file, count in sorted(reads_by_file.items(), key=lambda kv: (-kv[1], kv[0]))]
    print("  Most-read KB files:")
    print_bar_chart(rows[:top], indent="    ")

    candidate_pool = scan.sessions if scan is not None else set(chars_by_session)
    if len(candidate_pool) >= dead_sessions:
        read_files = set(reads_by_file)
        dead = [str(path.relative_to(kb)) for path in stable_topic_docs(kb) if str(path.relative_to(kb)) not in read_files]
        print(f"  Dead knowledge candidates (unread across {len(candidate_pool)} scanned/logged sessions):")
        for file in dead[:top]:
            print(f"    - {file}")
        if not dead:
            print("    (none)")
    else:
        print(f"  Dead knowledge candidates: need at least {dead_sessions} scanned/logged sessions")


# Summarizes CLI usage from the event log and KB file churn from git history, drawn as bar charts.
def command_stats(args: argparse.Namespace) -> int:
    root = repo_root(args)
    kb = kb_dir(root)
    if not kb.exists():
        print("ERROR: missing .agent-kb/")
        return 1
    drift_warnings = schema_drift_warnings(kb)
    for warning in drift_warnings:
        print(f"WARN: {warning}")
    if drift_warnings:
        print()
    scan: TranscriptScan | None = None
    added = 0
    backfill_error = None
    if not args.no_backfill:
        try:
            scan, added = backfill_kb_reads(root, args)
        except Exception as err:
            backfill_error = str(err)
            scan, added = None, 0

    print("CLI command usage (.agent-kb/.log/events.jsonl):")
    events = read_events(kb / ".log" / "events.jsonl")
    cli_events = [event for event in events if event.get("event", "cli") == "cli"]
    if not cli_events:
        print("  (no events logged yet)")
    else:
        counts: dict[str, list[int]] = {}
        for event in cli_events:
            command = str(event.get("command", "?"))
            failed = 1 if event.get("exit", 0) != 0 else 0
            total, fails = counts.get(command, [0, 0])
            counts[command] = [total + 1, fails + failed]
        rows = []
        for command, (total, fails) in sorted(counts.items(), key=lambda kv: (-kv[1][0], kv[0])):
            suffix = f"{total}" + (f"  ({fails} failed)" if fails else "")
            rows.append((command, total, suffix))
        print_bar_chart(rows[: args.top])

    print()
    if scan is not None:
        print(f"Backfilled KB reads: {added} new event(s).")
    print_kb_read_stats(kb, events, scan, args.top, args.dead_sessions, backfill_error)

    print()
    print("KB file churn (git history):")
    churn = git_churn(root)
    if not churn:
        print("  (no git history for .agent-kb)")
    else:
        rows = [
            (path[len(".agent-kb/"):] if path.startswith(".agent-kb/") else path, count, str(count))
            for path, count in churn[: args.top]
        ]
        print_bar_chart(rows)

    print()
    print("Largest KB files (current chars):")
    sizes = stable_doc_sizes(kb)
    if not sizes:
        print("  (no stable topic docs)")
    else:
        rows = [(str(relative), chars, str(chars)) for relative, chars in sizes[: args.top]]
        print_bar_chart(rows)

    print()
    print("Latest outcomes (per command):")
    latest_by_command: dict[str, dict] = {}
    for event in cli_events:
        if "metrics" in event:
            latest_by_command[str(event.get("command", "?"))] = event
    if not latest_by_command:
        print("  (no command metrics logged yet)")
    else:
        label_width = max(len(command) for command in latest_by_command)
        for command in sorted(latest_by_command):
            metrics = latest_by_command[command]["metrics"]
            pairs = " ".join(f"{key}={value}" for key, value in metrics.items())
            print(f"  {command:<{label_width}}  {pairs}")
    return 0


# Builds the command-line parser for agent KB maintenance actions.
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a repository-local .agent-kb knowledge base.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize .agent-kb and the runtime protocol.")
    init_parser.add_argument("--root", default=".", help="Repository root to manage.")
    init_mode = init_parser.add_mutually_exclusive_group()
    init_mode.add_argument("--shared", action="store_true", help="Version the KB inside the parent repo instead of a personal nested repo.")
    init_mode.add_argument("--local", action="store_true", help="Keep the KB local-only and git-ignored, with no version history.")
    init_parser.set_defaults(func=command_init)

    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade generated KB protocol files conservatively.")
    upgrade_parser.add_argument("--root", default=".", help="Repository root to manage.")
    upgrade_parser.add_argument("--write-start", action="store_true", help="Replace .agent-kb/start.md with the current template.")
    upgrade_parser.add_argument("--write-routes", action="store_true", help="Replace .agent-kb/routes.yaml with the default routes.")
    upgrade_parser.add_argument("--write-map", action="store_true", help="Replace .agent-kb/map.md with the default routing table.")
    upgrade_parser.add_argument("--write-plan", action="store_true", help="Replace .agent-kb/plans/current.md with the default empty plan.")
    upgrade_parser.set_defaults(func=command_upgrade)

    validate_parser = subparsers.add_parser("validate", help="Validate the .agent-kb scaffold.")
    validate_parser.add_argument("--root", default=".", help="Repository root to manage.")
    validate_parser.set_defaults(func=command_validate)

    note_parser = subparsers.add_parser("note", help="Write a durable knowledge note into inbox.")
    note_parser.add_argument("--root", default=".", help="Repository root to manage.")
    note_parser.add_argument("--title", required=True, help="Inbox note title.")
    note_parser.add_argument("--target", default="unsure", help="Suggested KB-relative target path.")
    note_parser.add_argument("--body", help="Note body. Reads stdin when omitted.")
    note_parser.set_defaults(func=command_note)

    compile_parser = subparsers.add_parser("compile", help="Merge inbox notes with valid targets.")
    compile_parser.add_argument("--root", default=".", help="Repository root to manage.")
    compile_parser.set_defaults(func=command_compile)

    trim_parser = subparsers.add_parser("trim", help="Diagnose or apply safe KB trimming.")
    trim_parser.add_argument("--root", default=".", help="Repository root to manage.")
    trim_parser.add_argument("--write", action="store_true", help="Apply deterministic cleanup and validate.")
    trim_parser.add_argument("--recheck", action="store_true", help="Run validate first, then re-diagnose, so the compaction loop is one command per round.")
    trim_parser.add_argument("--max-file-lines", type=int, default=TRIM_MAX_FILE_LINES, help=f"Lines above which a topic is flagged for compacting (default {TRIM_MAX_FILE_LINES}).")
    trim_parser.add_argument("--max-file-chars", type=int, default=TRIM_MAX_FILE_CHARS, help=f"Chars above which a topic is flagged for compacting; the primary signal since it can't be gamed by joining lines (default {TRIM_MAX_FILE_CHARS}).")
    trim_parser.add_argument("--max-total-chars", type=int, default=TRIM_MAX_TOTAL_CHARS, help=f"Total stable-doc character budget before compacting is suggested (default {TRIM_MAX_TOTAL_CHARS}).")
    trim_parser.add_argument("--max-inbox-notes", type=int, default=TRIM_MAX_INBOX_NOTES, help=f"Inbox note count above which compacting is suggested (default {TRIM_MAX_INBOX_NOTES}).")
    trim_parser.add_argument("--verbose", action="store_true", help="Always print the full agent compact prompt and soft-budget note (default prints them only on first detection in a loop).")
    trim_parser.set_defaults(func=command_trim)

    stats_parser = subparsers.add_parser("stats", help="Summarize CLI usage, KB reads, and KB file churn.")
    stats_parser.add_argument("--root", default=".", help="Repository root to manage.")
    stats_parser.add_argument("--top", type=int, default=5, help="Show at most this many rows per section (default 5).")
    stats_parser.add_argument("--no-backfill", action="store_true", help="Do not scan local transcripts before rendering stats.")
    stats_parser.add_argument("--claude-dir", default="~/.claude/projects", help="Claude Code projects transcript directory.")
    stats_parser.add_argument("--codex-dir", default="~/.codex/sessions", help="Codex sessions transcript directory.")
    stats_parser.add_argument("--no-backfill-claude", action="store_true", help="Skip Claude Code transcript backfill.")
    stats_parser.add_argument("--no-backfill-codex", action="store_true", help="Skip Codex transcript backfill.")
    stats_parser.add_argument("--dead-sessions", type=int, default=20, help="Minimum scanned/logged sessions before listing unread stable docs (default 20).")
    stats_parser.set_defaults(func=command_stats)
    return parser


# Parses arguments and dispatches the selected command.
def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = args.func(args)
    # Commands return either an exit code or (exit code, metrics dict).
    if isinstance(result, tuple):
        exit_code, metrics = result
    else:
        exit_code, metrics = result, None
    log_event(args, args.command, exit_code, metrics)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
