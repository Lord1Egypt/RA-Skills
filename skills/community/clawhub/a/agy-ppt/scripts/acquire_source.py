#!/usr/bin/env python3
"""Acquire one explicit public source URL into a local payload (Phase 13.5).

Thin CLI adapter. It contains **no network logic of its own**: it parses
arguments and delegates entirely to ``source_acquisition``.

Usage::

    python3 acquire_source.py --url https://example.org/source.pdf \
        --source-id src_example --output-dir <workspace>

    python3 acquire_source.py --url https://example.org/notes.md \
        --source-id src_notes --output-dir <workspace> --ingest

Exit codes::

    0  acquisition (and, with --ingest, extraction) succeeded
    1  acquisition failed deterministically (invalid or unsupported URL,
       blocked destination, blocked or excessive redirects, HTTP error,
       timeout, oversized response, unsupported content encoding), or the
       subsequent ingestion failed
    2  usage error

Public unauthenticated sources only. There is no ``--header``, ``--cookie``,
``--user``, ``--token`` or ``--insecure`` option, and none will be added here:
Phase 13.5 does not support authenticated or private web sources, and it never
disables TLS verification.

The source body is never printed to the terminal; only provenance metadata is.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from source_acquisition import (  # noqa: E402
    DEFAULT_MAX_BYTES,
    DEFAULT_MAX_REDIRECTS,
    DEFAULT_TIMEOUT_SECONDS,
    SourceAcquisitionError,
    acquire_remote_source,
)
from source_ingestion import SourceIngestionError, ingest_source  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch one explicit public HTTP/HTTPS source into a local payload, "
            "then optionally run the existing deterministic ingestion on it. "
            "Public unauthenticated sources only: no crawling, no browser, no "
            "JavaScript, no authentication."
        )
    )
    parser.add_argument("--url", required=True, help="public http(s) source URL")
    parser.add_argument(
        "--source-id",
        required=True,
        help="stable source id, matching ^src_[A-Za-z0-9._-]+$",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="directory for the downloaded payload; keep it outside this repository",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=DEFAULT_MAX_BYTES,
        help=f"hard response-size limit in bytes (default: {DEFAULT_MAX_BYTES})",
    )
    parser.add_argument(
        "--max-redirects",
        type=int,
        default=DEFAULT_MAX_REDIRECTS,
        help=f"redirect hops to follow (default: {DEFAULT_MAX_REDIRECTS})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"socket timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="after acquisition, run the existing ingestion and report block count",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        result = acquire_remote_source(
            args.url,
            args.source_id,
            args.output_dir,
            max_bytes=args.max_bytes,
            max_redirects=args.max_redirects,
            timeout=args.timeout,
        )
    except SourceAcquisitionError as exc:
        print(f"{exc.error_code}: {exc}", file=sys.stderr)
        return 1

    summary = {
        "source_id": result.source_id,
        "requested_url": result.requested_url,
        "final_url": result.final_url,
        "content_type": result.content_type,
        "downloaded_bytes": result.downloaded_bytes,
        "source_digest": result.source_digest,
        "payload_path": result.local_payload_path,
        "redirect_count": result.redirect_count,
        "retrieved_at": result.retrieved_at,
    }

    if args.ingest:
        try:
            extraction = ingest_source(result.local_payload_path, args.source_id)
        except SourceIngestionError as exc:
            print(f"{exc.error_code}: {exc}", file=sys.stderr)
            return 1
        summary["source_format"] = extraction.source_format
        summary["block_count"] = extraction.block_count

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
