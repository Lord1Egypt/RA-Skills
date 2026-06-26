#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import run_scan
import upload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a local ClawLock 2.2.1+ scan, preview the safe upload payload, and optionally submit it.",
    )
    parser.add_argument(
        "--api-base",
        default="",
        help="Optional Worker origin override. Defaults to CLAWLOCK_RANK_API_BASE or skill/config.json.",
    )
    parser.add_argument("--nickname", default="", help="Optional public nickname override.")
    parser.add_argument("--yes", action="store_true", help="Skip the interactive confirmation prompt.")
    parser.add_argument("--dry-run", action="store_true", help="Print the sanitized payload and exit.")
    parser.add_argument(
        "--preview-only",
        action="store_true",
        help="Run the scan, print a structured preview JSON, and exit without uploading.",
    )
    parser.add_argument("--output", default="", help="Optional path to save the sanitized payload JSON.")
    parser.add_argument("--adapter", default="openclaw", help="Adapter passed to clawlock scan.")
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
    parser.add_argument("--upload-timeout", type=int, default=15, help="Upload timeout in seconds.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.preview_only and args.yes:
        raise SystemExit("--preview-only cannot be combined with --yes.")

    scan_args = argparse.Namespace(
        adapter=args.adapter,
        output="",
        clawlock_bin=args.clawlock_bin,
        adapter_bin=args.adapter_bin,
        scan_arg=args.scan_arg,
        timeout=args.timeout,
    )
    raw_payload = run_scan.generate_payload(scan_args)

    nickname = args.nickname.strip()
    interactive_mode = not args.yes and not args.preview_only and not args.dry_run
    if not nickname and interactive_mode:
        nickname = input("Public nickname [Anonymous]: ").strip()

    sanitized_payload = upload.sanitize_payload(raw_payload, nickname_override=nickname)
    payload_path = resolve_output_path(args.output, preview_only=args.preview_only)
    if payload_path:
        write_payload(payload_path, sanitized_payload)

    if args.preview_only:
        print(json.dumps(build_preview_result(sanitized_payload, payload_path), ensure_ascii=False, indent=2))
        return 0

    print(json.dumps(upload.build_public_summary(sanitized_payload), ensure_ascii=False, indent=2))
    print(
        "This upload excludes local configuration details, remediation text, file paths, environment variables, "
        "and the full raw report.",
    )

    if args.dry_run:
        print(json.dumps(sanitized_payload, ensure_ascii=False, indent=2))
        return 0

    if not args.yes:
        confirm = input("Upload this score to ClawLockRank? [y/N]: ").strip().lower()
        if confirm not in {"y", "yes"}:
            print(json.dumps({"ok": False, "accepted": False, "message": "Upload cancelled."}, indent=2))
            return 0

    api_base = upload.resolve_api_base(args.api_base)
    if not api_base:
        raise SystemExit("Missing Worker origin. Pass --api-base, set CLAWLOCK_RANK_API_BASE, or add skill/config.json.")

    response = upload.post_payload(
        sanitized_payload,
        api_base=api_base,
        timeout=args.upload_timeout,
    )
    stream = sys.stdout if response["ok"] else sys.stderr
    print(json.dumps(response["body"], ensure_ascii=False, indent=2), file=stream)
    return 0 if response["ok"] else 1


def write_payload(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_output_path(raw_output: str, preview_only: bool) -> Path | None:
    if raw_output:
        return Path(raw_output).expanduser().resolve()
    if not preview_only:
        return None

    handle = tempfile.NamedTemporaryFile(
        prefix="clawlock-rank-preview-",
        suffix=".json",
        delete=False,
    )
    handle.close()
    return Path(handle.name).resolve()


def build_preview_result(payload: dict[str, Any], payload_path: Path | None) -> dict[str, Any]:
    summary = upload.build_public_summary(payload)
    return {
        "ok": True,
        "mode": "preview",
        "payload_path": str(payload_path) if payload_path else "",
        "summary": summary,
        "source_of_truth": "clawlock scan --format json",
        "requires_public_nickname": True,
        "requires_explicit_confirmation": True,
        "next_step": (
            "Ask the user for a public nickname and explicit upload confirmation. "
            "If the user agrees, call upload.py with --input <payload_path> --nickname <name> --yes."
        ),
    }


if __name__ == "__main__":
    sys.exit(main())
