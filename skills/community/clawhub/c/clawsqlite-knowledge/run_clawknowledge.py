#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Runtime entry for the clawknowledge skill.

This script expects to be invoked by the ClawHub skill runtime with a JSON
payload on stdin and returns a JSON response on stdout.

It is intentionally a thin, auditable wrapper around the public
`clawsqlite` package and its `knowledge` CLI.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import Any, Dict


def _workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _site_packages(prefix: Path) -> Path:
    vars_map = {"base": str(prefix), "platbase": str(prefix)}
    return Path(sysconfig.get_path("purelib", vars=vars_map))


def _build_env() -> dict[str, str]:
    env = os.environ.copy()
    prefix = _workspace_root() / ".clawsqlite-venv"
    site_packages = _site_packages(prefix)
    if site_packages.exists():
        pythonpath = env.get("PYTHONPATH", "")
        paths = [p for p in pythonpath.split(os.pathsep) if p] if pythonpath else []
        if str(site_packages) not in paths:
            paths.insert(0, str(site_packages))
            env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def _extract_next_lines(stdout: str, stderr: str) -> list[str]:
    lines = (stderr or "").splitlines() + (stdout or "").splitlines()
    next_lines: list[str] = []
    capture = False
    for line in lines:
        if line.startswith("NEXT:"):
            capture = True
            content = line[len("NEXT:") :].strip()
            if content:
                next_lines.append(content)
            continue
        if capture:
            if not line.strip():
                capture = False
                continue
            if line.startswith(("ERROR:", "WARN:", "INFO:", "NEXT:")):
                capture = False
                continue
            next_lines.append(line.rstrip())
    return next_lines


def _classify_error(output_text: str) -> str:
    text = output_text.lower()
    if (
        "clawsqlite_scrape_cmd" in text
        or "requires a scraper" in text
        or "scrape failed" in text
    ):
        return "missing_scraper"
    if "no module named" in text and "clawsqlite" in text:
        return "missing_dependency"
    if "missing clawsqlite_vec_dim" in text or "embedding is not available" in text:
        return "missing_embedding"
    if "vec0 extension not loaded" in text or "vec index not available" in text:
        return "missing_vec_ext"
    if (
        "permission denied" in text
        or "eacces" in text
        or "read-only file system" in text
    ):
        return "permission"
    return "other"


def _detect_vec_issue(output_text: str) -> bool:
    text = output_text.lower()
    return any(
        key in text
        for key in (
            "clawsqlite_vec_dim",
            "clawsqlite_vec_ext",
            "embedding is not available",
            "vec0 extension not loaded",
            "vec index not available",
        )
    )


def _detect_scraper_issue(output_text: str) -> bool:
    text = output_text.lower()
    return any(
        key in text
        for key in (
            "clawsqlite_scrape_cmd",
            "requires a scraper",
            "scrape failed",
        )
    )


def _append_hint(next_lines: list[str], hint: list[str]) -> list[str]:
    if not hint:
        return next_lines
    if next_lines and hint[0] in next_lines:
        return next_lines
    return next_lines + hint


def _vec_hint_lines() -> list[str]:
    workspace = _workspace_root()
    prefix = workspace / ".sqlite-vec"
    site_packages = _site_packages(prefix)
    vec0_path = site_packages / "sqlite_vec" / "vec0.so"
    return [
        "Workspace-friendly vec0 setup:",
        f'  python -m pip install "sqlite-vec>=0.1.7" --prefix="{prefix}"',
        "  Then set:",
        f"    CLAWSQLITE_VEC_EXT={vec0_path}",
        "    CLAWSQLITE_VEC_DIM=<your-embedding-dim>",
    ]


def _scraper_hint_lines() -> list[str]:
    workspace = _workspace_root()
    clawfetch_js = workspace / "clawfetch" / "clawfetch.js"
    return [
        "OpenClaw workspace scraper example:",
        f'  CLAWSQLITE_SCRAPE_CMD="node {clawfetch_js} --auto-install"',
    ]


def _missing_dependency_hint_lines() -> list[str]:
    prefix = _workspace_root() / ".clawsqlite-venv"
    site_packages = _site_packages(prefix)
    return [
        "Install clawsqlite into the workspace prefix:",
        f'  python -m pip install "clawsqlite>=1.0.2" --prefix="{prefix}"',
        "Then ensure PYTHONPATH includes:",
        f"  {site_packages}",
    ]


def _run_knowledge_cli(args: list[str]) -> Dict[str, Any]:
    """Run `clawsqlite knowledge ...` and return parsed JSON when applicable.

    This relies on the `clawsqlite` package being installed in the same
    Python environment as this skill (typically via `bootstrap_deps.py`).
    It uses `python -m clawsqlite_cli knowledge ...` so that imports are
    resolved from the installed package, not from any local source tree.

    NOTE: `--json` should be part of *args* when JSON output is desired.
    """
    cmd = [sys.executable, "-m", "clawsqlite_cli", "knowledge"] + args
    proc = subprocess.run(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_build_env(),
    )
    output_text = f"{proc.stderr}\n{proc.stdout}"
    next_lines = _extract_next_lines(proc.stdout, proc.stderr)
    if _detect_vec_issue(output_text):
        next_lines = _append_hint(next_lines, _vec_hint_lines())
    if _detect_scraper_issue(output_text):
        next_lines = _append_hint(next_lines, _scraper_hint_lines())
    if proc.returncode != 0:
        error_kind = _classify_error(output_text)
        if error_kind == "missing_dependency":
            next_lines = _append_hint(next_lines, _missing_dependency_hint_lines())
        result = {
            "ok": False,
            "error": "knowledge_cli_failed",
            "error_kind": error_kind,
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
        if next_lines:
            result["next"] = next_lines
        return result
    # Try to parse JSON; fall back to raw text
    try:
        data = json.loads(proc.stdout)
    except Exception:
        data = {"raw": proc.stdout}
    result = {"ok": True, "data": data}
    if next_lines:
        result["next"] = next_lines
    return result


def handle_ingest_url(payload: Dict[str, Any]) -> Dict[str, Any]:
    url = payload["url"]
    title = payload.get("title")
    category = payload.get("category", "web")
    tags = payload.get("tags")
    gen_provider = payload.get("gen_provider", "openclaw")
    root = payload.get("root")  # optional override

    args: list[str] = [
        "ingest",
        "--url",
        url,
        "--category",
        category,
        "--gen-provider",
        gen_provider,
        "--json",
    ]
    if title:
        args += ["--title", title]
    if tags:
        args += ["--tags", tags]
    if root:
        args += ["--root", root]

    return _run_knowledge_cli(args)


def handle_ingest_text(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = payload["text"]
    title = payload.get("title")
    category = payload.get("category", "note")
    tags = payload.get("tags")
    gen_provider = payload.get("gen_provider", "openclaw")
    root = payload.get("root")

    args: list[str] = [
        "ingest",
        "--text",
        text,
        "--category",
        category,
        "--gen-provider",
        gen_provider,
        "--json",
    ]
    if title:
        args += ["--title", title]
    if tags:
        args += ["--tags", tags]
    if root:
        args += ["--root", root]

    return _run_knowledge_cli(args)


def handle_search(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = payload["query"]
    mode = payload.get("mode", "hybrid")
    topk = int(payload.get("topk", 10))
    category = payload.get("category")
    tag = payload.get("tag")
    include_deleted = bool(payload.get("include_deleted", False))
    root = payload.get("root")

    args: list[str] = [
        "search",
        query,
        "--mode",
        mode,
        "--topk",
        str(topk),
        "--json",
    ]
    if category:
        args += ["--category", category]
    if tag:
        args += ["--tag", tag]
    if include_deleted:
        args.append("--include-deleted")
    if root:
        args += ["--root", root]

    return _run_knowledge_cli(args)


def handle_show(payload: Dict[str, Any]) -> Dict[str, Any]:
    article_id = str(payload["id"])
    full = bool(payload.get("full", True))
    root = payload.get("root")

    args: list[str] = [
        "show",
        "--id",
        article_id,
        "--json",
    ]
    if full:
        args.append("--full")
    if root:
        args += ["--root", root]

    return _run_knowledge_cli(args)


def handle_report_interest(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Generate an interest report via `clawsqlite knowledge report-interest`.

    This wraps the CLI command and returns the report directory plus raw
    stdout. Markdown + PNG charts are always generated; PDF/HTML are
    best-effort depending on environment (pandoc/LaTeX).
    """
    root = payload.get("root")
    days = int(payload.get("days", 7))
    date_from = payload.get("date_from")
    date_to = payload.get("date_to")
    vec_dim = payload.get("vec_dim")
    out_dir = payload.get("out_dir")
    lang = payload.get("lang")
    fmt = payload.get("format") or payload.get("fmt")
    no_pdf = bool(payload.get("no_pdf", False))

    args: list[str] = [
        "report-interest",
        "--days",
        str(days),
    ]
    if date_from:
        args += ["--from", date_from]
    if date_to:
        args += ["--to", date_to]
    if vec_dim is not None:
        args += ["--vec-dim", str(vec_dim)]
    if out_dir:
        args += ["--out-dir", out_dir]
    if lang:
        args += ["--lang", lang]
    if fmt:
        args += ["--format", fmt]
    if no_pdf:
        args.append("--no-pdf")
    if root:
        args += ["--root", root]

    # We do not pass --json here; report-interest writes a human string to stdout.
    result = _run_knowledge_cli(args)
    if not result.get("ok"):
        return result

    data = result.get("data")
    raw: str | None = None
    if isinstance(data, dict):
        raw = data.get("raw")  # type: ignore[assignment]
    elif isinstance(data, str):
        raw = data

    report_dir: str | None = None
    if raw:
        for line in reversed(raw.splitlines()):
            line = line.strip()
            if not line:
                continue
            lower = line.lower()
            if lower.startswith("report written to"):
                report_dir = line[len("report written to") :].strip()
                break

    result["data"] = {
        "report_dir": report_dir,
        "stdout": raw,
    }
    return result


HANDLERS = {
    "ingest_url": handle_ingest_url,
    "ingest_text": handle_ingest_text,
    "search": handle_search,
    "show": handle_show,
    "report_interest": handle_report_interest,
}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception as e:
        json.dump({"ok": False, "error": "invalid_json", "detail": str(e)}, sys.stdout)
        return 1

    action = payload.get("action")
    if not action:
        json.dump({"ok": False, "error": "missing_action"}, sys.stdout)
        return 1

    handler = HANDLERS.get(action)
    if not handler:
        json.dump(
            {"ok": False, "error": "unknown_action", "action": action}, sys.stdout
        )
        return 1

    result = handler(payload)
    json.dump(result, sys.stdout, ensure_ascii=False)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
