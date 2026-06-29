#!/usr/bin/env python3
"""Memory freshness and semantic retrieval watchdog for dr-context-pipeline."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List


@dataclass
class CheckResult:
    status: str
    issues: List[str]
    details: dict[str, Any]


def iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def find_daily_files(memory_dir: Path, target_date: datetime) -> List[Path]:
    prefix = iso_date(target_date)
    return sorted(memory_dir.glob(f"{prefix}*.md"))


def check_daily_file(paths: List[Path], freshness_minutes: int, min_bytes: int) -> CheckResult:
    issues: List[str] = []
    now = datetime.now(timezone.utc)

    if not paths:
        issues.append("Missing daily log for today")
        return CheckResult("GAP", issues, {"files_checked": []})

    newest = None
    newest_age = None
    details = []
    for p in paths:
        stat = p.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
        age_minutes = (now - mtime).total_seconds() / 60
        size = stat.st_size
        details.append({
            "path": str(p),
            "modified_utc": mtime.isoformat(),
            "age_minutes": round(age_minutes, 2),
            "bytes": size,
        })
        if newest is None or mtime > newest:
            newest = mtime
            newest_age = age_minutes
        if size < min_bytes:
            issues.append(f"File {p} is only {size} bytes (<{min_bytes})")

    if newest_age is not None and newest_age > freshness_minutes:
        issues.append(f"Newest daily note is {round(newest_age, 1)} min old (> {freshness_minutes} min)")

    status = "OK" if not issues else "GAP"
    return CheckResult(status, issues, {"files_checked": details})


def extract_json_payload(text: str) -> Any:
    stripped = text.strip()
    if not stripped:
        raise ValueError("empty command output")
    decoder = json.JSONDecoder()
    starts = sorted(
        idx for idx, char in enumerate(stripped)
        if char in {"[", "{"}
    )
    for idx in starts:
        try:
            payload, end = decoder.raw_decode(stripped[idx:])
        except json.JSONDecodeError:
            continue
        if stripped[idx + end:].strip():
            continue
        return payload
    raise ValueError("no JSON payload found in command output")


def run_json_command(command: list[str], timeout_seconds: int) -> tuple[Any | None, dict[str, Any]]:
    proc = subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
    )
    details = {
        "command": command,
        "returncode": proc.returncode,
        "stderr": proc.stderr.strip(),
    }
    try:
        payload = extract_json_payload(proc.stdout)
    except Exception as exc:  # noqa: BLE001
        details["parse_error"] = str(exc)
        details["stdout_preview"] = proc.stdout[-2000:]
        return None, details
    return payload, details


def first_status_entry(payload: Any) -> dict[str, Any] | None:
    if isinstance(payload, list) and payload and isinstance(payload[0], dict):
        return payload[0]
    if isinstance(payload, dict):
        return payload
    return None


def check_semantic_status(openclaw_bin: str, agent: str | None, timeout_seconds: int) -> CheckResult:
    command = [openclaw_bin, "memory", "status", "--index", "--deep", "--json"]
    if agent:
        command.extend(["--agent", agent])
    payload, command_details = run_json_command(command, timeout_seconds)
    issues: List[str] = []
    details: dict[str, Any] = {"status_command": command_details}

    entry = first_status_entry(payload)
    if entry is None:
        return CheckResult("GAP", ["Memory status JSON was missing or invalid"], details)

    status = entry.get("status", {}) if isinstance(entry.get("status"), dict) else {}
    vector = status.get("vector", {}) if isinstance(status.get("vector"), dict) else {}
    embedding_probe = entry.get("embeddingProbe", {}) if isinstance(entry.get("embeddingProbe"), dict) else {}
    scan = entry.get("scan", {}) if isinstance(entry.get("scan"), dict) else {}

    details["provider"] = status.get("provider")
    details["model"] = status.get("model")
    details["files"] = status.get("files")
    details["chunks"] = status.get("chunks")
    details["dirty"] = status.get("dirty")
    details["embeddingProbe"] = embedding_probe
    details["vector"] = vector
    details["scan"] = scan

    if embedding_probe.get("ok") is not True:
        issues.append("Embedding probe is not OK")
    if vector.get("storeAvailable") is not True:
        issues.append("Vector store is not available")
    if vector.get("semanticAvailable") is not True:
        issues.append("Semantic vectors are not available")
    if status.get("dirty") is True:
        issues.append("Memory index is still dirty after indexing")
    if not isinstance(status.get("files"), int) or status.get("files", 0) <= 0:
        issues.append("Memory index has no files")
    if not isinstance(status.get("chunks"), int) or status.get("chunks", 0) <= 0:
        issues.append("Memory index has no chunks")
    if scan.get("issues"):
        issues.append("Memory scan reported issues")

    return CheckResult("OK" if not issues else "GAP", issues, details)


def check_search_probe(openclaw_bin: str, agent: str | None, query: str, min_results: int, timeout_seconds: int) -> CheckResult:
    command = [openclaw_bin, "memory", "search", "--query", query, "--max-results", str(max(min_results, 1)), "--json"]
    if agent:
        command.extend(["--agent", agent])
    payload, command_details = run_json_command(command, timeout_seconds)
    issues: List[str] = []
    details: dict[str, Any] = {"search_command": command_details, "query": query}

    if not isinstance(payload, dict):
        return CheckResult("GAP", ["Memory search JSON was missing or invalid"], details)
    results = payload.get("results")
    if not isinstance(results, list):
        return CheckResult("GAP", ["Memory search JSON did not contain results"], details)

    details["result_count"] = len(results)
    details["top_results"] = [
        {
            "path": item.get("path"),
            "score": item.get("score"),
            "vectorScore": item.get("vectorScore"),
            "textScore": item.get("textScore"),
        }
        for item in results[:3]
        if isinstance(item, dict)
    ]

    if len(results) < min_results:
        issues.append(f"Memory search returned {len(results)} results (<{min_results})")
    if min_results > 0 and not any(isinstance(item, dict) and isinstance(item.get("vectorScore"), (int, float)) for item in results):
        issues.append("Memory search results did not include vectorScore")

    return CheckResult("OK" if not issues else "GAP", issues, details)


def make_notification_payload(status: str, issues: list[str], details: dict[str, Any]) -> dict[str, Any] | None:
    if status == "OK":
        return None
    return {
        "severity": "warning",
        "title": "Memory/embedding watchdog gap",
        "message": "Semantic memory or daily memory health check failed.",
        "issues": issues,
        "details": details,
    }


def main() -> int:
    script_path = Path(__file__).resolve()
    workspace_root = script_path.parents[3]
    memory_dir_default = workspace_root / "memory"

    parser = argparse.ArgumentParser(description="Ensure memory logs and semantic retrieval are healthy")
    parser.add_argument("--memory-dir", default=str(memory_dir_default), help="Path to the memory directory")
    parser.add_argument("--freshness-minutes", type=int, default=120, help="Max minutes since the latest daily log edit")
    parser.add_argument("--min-bytes", type=int, default=200, help="Minimum acceptable size for the daily log")
    parser.add_argument("--timezone", default="UTC", help="Display timezone label (informational only)")
    parser.add_argument("--require-semantic", action="store_true", help="Require OpenClaw semantic memory and embeddings to be ready")
    parser.add_argument("--openclaw-bin", default="openclaw", help="OpenClaw CLI binary")
    parser.add_argument("--agent", default=None, help="Optional OpenClaw agent id")
    parser.add_argument("--probe-query", default=None, help="Optional semantic search probe query")
    parser.add_argument("--min-search-results", type=int, default=1, help="Minimum probe results when --probe-query is set")
    parser.add_argument("--timeout-seconds", type=int, default=120, help="Timeout for OpenClaw CLI checks")
    parser.add_argument("--emit-notification-payload", action="store_true", help="Include a dry-run notification payload on GAP")
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir).resolve()
    all_issues: list[str] = []
    checks: dict[str, Any] = {}

    if not memory_dir.exists():
        daily = CheckResult("GAP", [f"Memory directory missing: {memory_dir}"], {})
    else:
        today = datetime.now(timezone.utc)
        files = find_daily_files(memory_dir, today)
        daily = check_daily_file(files, args.freshness_minutes, args.min_bytes)
    checks["daily"] = daily.details
    all_issues.extend(daily.issues)

    if args.require_semantic:
        semantic = check_semantic_status(args.openclaw_bin, args.agent, args.timeout_seconds)
        checks["semantic_status"] = semantic.details
        all_issues.extend(semantic.issues)
        if args.probe_query:
            probe = check_search_probe(args.openclaw_bin, args.agent, args.probe_query, args.min_search_results, args.timeout_seconds)
            checks["semantic_probe"] = probe.details
            all_issues.extend(probe.issues)

    status = "OK" if not all_issues else "GAP"
    payload = {
        "status": status,
        "issues": all_issues,
        "checks": checks,
        "freshness_minutes": args.freshness_minutes,
        "min_bytes": args.min_bytes,
        "timezone": args.timezone,
        "today": iso_date(datetime.now(timezone.utc)),
        "semantic_required": args.require_semantic,
    }
    if args.emit_notification_payload:
        payload["notification"] = make_notification_payload(status, all_issues, checks)

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
