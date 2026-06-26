#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKILL_VERSION = "1.1.0"
VERSION_PATTERN = re.compile(r"\b\d+\.\d+\.\d+(?:[-+._][0-9A-Za-z.-]+)?\b")
MIN_CLAWLOCK_VERSION = (2, 2, 1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a local ClawLock scan and convert it into a minimal ClawLockRank upload payload.",
    )
    parser.add_argument(
        "--adapter",
        default="openclaw",
        help="Adapter passed to clawlock scan. Defaults to openclaw for the current leaderboard scope.",
    )
    parser.add_argument("--output", required=True, help="Where to write the normalized payload JSON.")
    parser.add_argument("--clawlock-bin", default="clawlock", help="Path to the clawlock executable.")
    parser.add_argument(
        "--adapter-bin",
        default="",
        help="Optional adapter executable used to detect adapter version. Defaults to the adapter name.",
    )
    parser.add_argument(
        "--scan-arg",
        action="append",
        default=[],
        help="Extra argument forwarded to clawlock scan. Can be used multiple times.",
    )
    parser.add_argument("--timeout", type=int, default=180, help="Scan timeout in seconds.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output).expanduser().resolve()
    payload = generate_payload(args)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "ok": True,
        "output": str(output_path),
        "clawlock_version": payload["submission"]["clawlock_version"],
        "score": payload["submission"]["score"],
        "grade": payload["submission"]["grade"],
        "adapter": payload["submission"]["adapter"],
        "adapter_version": payload["submission"]["adapter_version"],
        "findings": len(payload["submission"]["findings"]),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def generate_payload(args: argparse.Namespace) -> dict[str, Any]:
    ensure_command_exists(args.clawlock_bin, "clawlock")
    scan_report = run_scan(args)
    return build_payload(scan_report, args)


def ensure_command_exists(command: str, label: str) -> None:
    if resolve_command(command):
        return
    raise SystemExit(f"{label} executable not found: {command}")


def run_scan(args: argparse.Namespace) -> dict[str, Any]:
    command = [args.clawlock_bin, "scan", "--format", "json"]
    if args.adapter:
        command.extend(["--adapter", args.adapter])
    command.extend(args.scan_arg)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=args.timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise SystemExit(f"Unable to execute clawlock: {exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise SystemExit(f"clawlock scan timed out after {args.timeout} seconds.") from exc

    document = extract_json_document(result.stdout) or extract_json_document(result.stderr)
    if isinstance(document, dict):
        return document

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise SystemExit(f"clawlock scan failed: {message}")

    raise SystemExit("Could not parse JSON output from `clawlock scan --format json`.")


def extract_json_document(text: str) -> dict[str, Any] | None:
    if not text:
        return None

    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            candidate, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            return candidate
    return None


def build_payload(scan_report: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    device_fingerprint = clean_text(scan_report.get("device") or scan_report.get("device_fingerprint"), 128)
    if not device_fingerprint:
        raise SystemExit("Scan output did not include a device fingerprint.")

    score = coerce_int(scan_report.get("score"))
    if score is None:
        raise SystemExit("Scan output did not include a numeric score.")

    tool = clean_text(scan_report.get("tool"), 32) or "ClawLock"
    clawlock_version = clean_text(scan_report.get("version"), 32)
    if not clawlock_version:
        raise SystemExit("Scan output did not include a ClawLock version.")
    ensure_supported_clawlock_version(clawlock_version)

    adapter = clean_text(scan_report.get("adapter"), 64) or clean_text(args.adapter, 64) or "openclaw"
    adapter_version = clean_text(scan_report.get("adapter_version"), 32) or detect_adapter_version(
        args.adapter_bin or args.adapter or infer_adapter_bin(adapter)
    )
    timestamp = normalize_timestamp(scan_report.get("time") or scan_report.get("timestamp"))
    findings = normalize_findings(scan_report.get("findings"))
    grade = clean_text(scan_report.get("grade"), 2).upper() or infer_grade(score)

    return {
        "submission": {
            "tool": tool,
            "clawlock_version": clawlock_version,
            "adapter": adapter,
            "adapter_version": adapter_version,
            "device_fingerprint": device_fingerprint,
            "evidence_hash": build_evidence_hash(scan_report),
            "score": score,
            "grade": grade,
            "nickname": "",
            "findings": findings,
            "timestamp": timestamp,
        },
        "meta": {
            "source": "clawlock-rank-skill",
            "skill_version": SKILL_VERSION,
        },
    }


def normalize_findings(raw_findings: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    if not isinstance(raw_findings, list):
        return findings

    for item in raw_findings[:200]:
        if not isinstance(item, dict):
            continue
        scanner = clean_text(item.get("scanner"), 64)
        title = clean_text(item.get("title"), 160)
        level = clean_text(item.get("level"), 16).lower()
        if level == "warn":
            level = "medium"
        elif level == "low":
            level = "info"
        if level not in {"critical", "high", "medium", "info"}:
            continue
        if not scanner or not title:
            continue
        finding_key = (scanner, level, title)
        if finding_key in seen:
            continue
        seen.add(finding_key)
        findings.append(
            {
                "scanner": scanner,
                "level": level,
                "title": title,
            }
        )

    return findings


def ensure_supported_clawlock_version(version: str) -> None:
    parsed = parse_version_tuple(version)
    if parsed is None:
        return
    if parsed < MIN_CLAWLOCK_VERSION:
        expected = ".".join(str(part) for part in MIN_CLAWLOCK_VERSION)
        raise SystemExit(
            f"ClawLockRank skill requires clawlock>={expected}. Current scan report version: {version}."
        )


def parse_version_tuple(version: str) -> tuple[int, int, int] | None:
    match = VERSION_PATTERN.search(version)
    if not match:
        return None
    raw = match.group(0)
    numbers: list[int] = []
    for part in re.split(r"[^0-9]+", raw):
        if part:
            numbers.append(int(part))
        if len(numbers) == 3:
            break
    if len(numbers) < 3:
        return None
    return (numbers[0], numbers[1], numbers[2])


def build_evidence_hash(scan_report: dict[str, Any]) -> str:
    canonical = canonicalize_json_value(scan_report)
    serialized = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def canonicalize_json_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): canonicalize_json_value(child) for key, child in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, list):
        return [canonicalize_json_value(item) for item in value]
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value).strip()
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return unicodedata.normalize("NFC", str(value)).strip()


def detect_adapter_version(adapter_bin: str) -> str:
    candidate = adapter_bin.strip()
    if not candidate:
        return ""
    executable = resolve_command(candidate)
    if not executable:
        return ""

    for command in ([executable, "--version"], [executable, "version"]):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

        output = "\n".join(part for part in [result.stdout, result.stderr] if part).strip()
        match = VERSION_PATTERN.search(output)
        if match:
            return match.group(0)

    return ""


def infer_adapter_bin(adapter: str) -> str:
    normalized = adapter.strip().lower().replace("_", "-")
    aliases = {
        "openclaw": "openclaw",
        "zeroclaw": "zeroclaw",
        "claude-code": "claude",
        "claude code": "claude",
    }
    return aliases.get(normalized, "")


def normalize_timestamp(value: Any) -> str:
    if isinstance(value, str):
        text = value.strip()
        if text:
            parsed = parse_datetime(text)
            if parsed is not None:
                return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_datetime(value: str) -> datetime | None:
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        parsed = None

    if parsed is None:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
            try:
                parsed = datetime.strptime(value, fmt)
                break
            except ValueError:
                continue

    if parsed is None:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return parsed


def coerce_int(value: Any) -> int | None:
    try:
        number = int(round(float(value)))
    except (TypeError, ValueError):
        return None
    return max(0, min(100, number))


def infer_grade(score: int) -> str:
    if score >= 95:
        return "S"
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def clean_text(value: Any, max_length: int) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFC", value)
    collapsed = " ".join(normalized.strip().split())
    return collapsed[:max_length]


def resolve_command(command: str) -> str | None:
    candidate = command.strip()
    if not candidate:
        return None
    direct_path = Path(candidate).expanduser()
    if direct_path.exists():
        return str(direct_path)
    return shutil.which(candidate)


if __name__ == "__main__":
    sys.exit(main())
