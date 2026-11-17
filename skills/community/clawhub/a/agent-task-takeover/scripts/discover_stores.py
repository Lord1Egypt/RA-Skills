#!/usr/bin/env python3
"""Discover which AI coding agents have session stores on this machine.

Scans the known roots from references/agent-stores.md (CLI and Electron
agents alike) and prints what exists, the newest file inside, and when it
was last touched. Everything is read-only; nothing outside the listed
candidate roots is opened. An opt-in artifact mode collects task evidence
without opening any file, for cases where no transcript is available.

Usage:
  python discover_stores.py            # human-readable table
  python discover_stores.py --json     # machine-readable
  python discover_stores.py --days 14  # only stores touched in the last N days
  python discover_stores.py --artifacts --artifact-root PATH [--json]
      --artifact-root / --source-glob / --deliverable-glob / --evidence-glob
      are repeatable; roots may also come from
      AGENT_TAKEOVER_ARTIFACT_ROOTS (pathsep-separated)
      --gate-failed marks the pipeline stale despite a newer deliverable
"""
import argparse
import glob
import json
import os
import sys
import time
from pathlib import Path

from session_utils import ensure_utf8_stdout
from state_model import UNKNOWN, classify_pipeline

HOME = Path.home()


def _app_support(app):
    """Per-platform config root for Electron (VS Code-family) apps."""
    if sys.platform == "darwin":
        return HOME / "Library" / "Application Support" / app / "User"
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", HOME / "AppData/Roaming")) / app / "User"
    return HOME / ".config" / app / "User"


def _claude_root():
    # Claude Code honours CLAUDE_CONFIG_DIR; default ~/.claude.
    return Path(os.environ.get("CLAUDE_CONFIG_DIR", HOME / ".claude"))


# (agent, kind, human note, candidate glob patterns)
def candidates():
    vscode_family = ["Cursor", "Trae", "Code", "Kiro", "Windsurf", "Antigravity"]
    out = [
        ("opencode", "cli", "SQLite DB",
         [str(HOME / ".local/share/opencode/opencode.db"),
          str(HOME / ".local/share/opencode/project/*/storage/*.db")]),
        ("zcode", "cli", "rollout JSONL",
         [str(HOME / ".zcode/cli/rollout/*.jsonl")]),
        ("codex", "cli", "rollout JSONL",
         [str(HOME / ".codex/sessions/**/*.jsonl"),
          str(HOME / ".codex/sessions/*.jsonl")]),
        ("claude-code", "cli", "projects JSONL",
         [str(_claude_root() / "projects/*/*.jsonl")]),
        ("gemini-cli", "cli", "chats JSON",
         [str(HOME / ".gemini/tmp/*/chats/session-*.json")]),
        ("aider", "cli", "chat history md",
         [str(HOME / ".aider.chat.history.md")]),
        ("workbuddy", "electron", "app dir (store unconfirmed)",
         [str(HOME / ".workbuddy/workbuddy.db"),
          str(HOME / ".workbuddy/sessions")]),
    ]
    for app in vscode_family:
        user = _app_support(app)
        out.append((
            app.lower(), "electron", "state.vscdb / chatSessions",
            [str(user / "workspaceStorage/*/state.vscdb"),
             str(user / "workspaceStorage/*/chatSessions/*.json"),
             str(user / "globalStorage/state.vscdb")],
        ))
    return out


def scan(days):
    now = time.time()
    found = []
    for agent, kind, note, patterns in candidates():
        files = []
        for pattern in patterns:
            files.extend(p for p in glob.glob(pattern, recursive=True) if os.path.isfile(p))
        dirs = [p for pattern in patterns for p in glob.glob(pattern) if os.path.isdir(p)]
        if not files and not dirs:
            continue
        newest = None
        for path in files:
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if newest is None or mtime > newest[1]:
                newest = (path, mtime)
        for path in dirs:
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if newest is None or mtime > newest[1]:
                newest = (path + os.sep, mtime)
        if days and newest and (now - newest[1]) > days * 86400:
            continue
        found.append({
            "agent": agent,
            "kind": kind,
            "note": note,
            "files": len(files),
            "newest": newest[0] if newest else None,
            "mtime": newest[1] if newest else None,
        })
    found.sort(key=lambda item: item["mtime"] or 0, reverse=True)
    return found


# --- Artifact evidence (opt-in) -------------------------------------------
# No product-specific directory names are baked in: callers supply roots and
# globs. This mode only stats files; it never opens or parses their contents.

ARTIFACT_ENV = "AGENT_TAKEOVER_ARTIFACT_ROOTS"
EVIDENCE_GLOBS = ("**/*.log", "**/*.report.json", "**/*quality*.json")


def artifact_roots(explicit):
    """Resolve configured roots; default to the current directory only."""
    roots = [Path(p) for p in explicit]
    env = os.environ.get(ARTIFACT_ENV, "")
    roots.extend(Path(p) for p in env.split(os.pathsep) if p.strip())
    return roots or [Path.cwd()]


def _newest(root, globs):
    newest = None
    for pattern in globs:
        for path in glob.glob(str(root / pattern), recursive=True):
            if not os.path.isfile(path):
                continue
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if newest is None or mtime > newest:
                newest = mtime
    return newest


def scan_artifacts(roots, source_globs=(), deliverable_globs=(),
                   evidence_globs=EVIDENCE_GLOBS, gate_ok=None):
    """Collect freshness evidence and detect a stale export pipeline.

    A root that does not exist is reported with exists=False instead of
    silently producing an all-None row that looks like "nothing to see".
    """
    results = []
    for root in roots:
        root = Path(root)
        exists = root.is_dir()
        if not exists:
            results.append({
                "root": str(root),
                "exists": False,
                "source_mtime": None,
                "deliverable_mtime": None,
                "evidence_mtime": None,
                "pipeline": UNKNOWN,
            })
            continue
        src = _newest(root, source_globs) if source_globs else None
        deliv = _newest(root, deliverable_globs) if deliverable_globs else None
        evidence = _newest(root, evidence_globs)
        results.append({
            "root": str(root),
            "exists": True,
            "source_mtime": src,
            "deliverable_mtime": deliv,
            "evidence_mtime": evidence,
            "pipeline": classify_pipeline(src, deliv, gate_ok)
            if (src or deliv) else UNKNOWN,
        })
    return results


def _fmt(ts):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts)) if ts else "?"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--days", type=int, default=0,
                        help="only stores touched within the last N days")
    parser.add_argument("--artifacts", action="store_true",
                        help="scan artifact roots instead of session stores (opt-in)")
    parser.add_argument("--artifact-root", action="append", default=[],
                        help="artifact root to scan (repeatable)")
    parser.add_argument("--source-glob", action="append", default=[],
                        help="glob for source artifacts (repeatable)")
    parser.add_argument("--deliverable-glob", action="append", default=[],
                        help="glob for exported deliverables (repeatable)")
    parser.add_argument("--evidence-glob", action="append", default=[],
                        help="glob for logs/reports used as evidence "
                             "(repeatable; defaults to common log and report names)")
    parser.add_argument("--gate-failed", action="store_true",
                        help="treat a failed validation gate as stale even when "
                             "the deliverable is newer than the source")
    args = parser.parse_args()
    ensure_utf8_stdout()

    if args.artifacts:
        results = scan_artifacts(
            artifact_roots(args.artifact_root),
            args.source_glob,
            args.deliverable_glob,
            evidence_globs=tuple(args.evidence_glob) or EVIDENCE_GLOBS,
            gate_ok=False if args.gate_failed else None,
        )
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return
        for item in results:
            if not item["exists"]:
                print(item["root"])
                print("    not found (check the path, or set "
                      f"{ARTIFACT_ENV})")
                continue
            print(item["root"])
            print("    pipeline: {p} | source: {s} | deliverable: {d} | evidence: {e}".format(
                p=item["pipeline"], s=_fmt(item["source_mtime"]),
                d=_fmt(item["deliverable_mtime"]), e=_fmt(item["evidence_mtime"])))
        return

    found = scan(args.days)
    if args.json:
        print(json.dumps(found, ensure_ascii=False, indent=2))
        return
    if not found:
        print("no known agent stores found on this machine")
        return
    for item in found:
        when = time.strftime("%Y-%m-%d %H:%M", time.localtime(item["mtime"])) if item["mtime"] else "?"
        print(f"{item['agent']:<14} [{item['kind']:>8}]  {item['files']:>4} file(s)  "
              f"last touched {when}")
        print(f"{'':<14}  {item['note']}")
        if item["newest"]:
            print(f"{'':<14}  newest: {item['newest']}")


if __name__ == "__main__":
    main()
