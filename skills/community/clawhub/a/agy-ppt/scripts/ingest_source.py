#!/usr/bin/env python3
"""Ingest one local source file into normalized extraction blocks (Phase 13.2).

Thin CLI adapter. It contains **no extraction logic of its own**: it parses
arguments and delegates entirely to ``source_ingestion.ingest_source()``.

Usage::

    python3 ingest_source.py --source <file> --source-id src_example
    python3 ingest_source.py --source <file> --source-id src_example --output out.json

Exit codes::

    0  extraction succeeded
    1  extraction failed deterministically (unsupported format, missing file,
       unreadable file, unsupported encoding, no extractable text layer, or a
       structurally broken document)
    2  usage error

The output is the normalized extraction result for AGY's semantic segmentation.
It is *not* a Phase 12 ``source_inventory.json``: promoting an extracted block
to a semantic source unit is an AGY decision, never this script's.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from source_ingestion import (  # noqa: E402
    SourceIngestionError,
    detect_source_format,
    ingest_source,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Deterministically extract normalized blocks and locators from a "
            "local PDF (with text layer), Markdown, plain-text, or DOCX source."
        )
    )
    parser.add_argument("--source", required=True, help="path to a local source file")
    parser.add_argument(
        "--source-id",
        required=True,
        help="stable source id, matching ^src_[A-Za-z0-9._-]+$",
    )
    parser.add_argument(
        "--output",
        help="write the extraction result JSON here (default: stdout)",
    )
    parser.add_argument(
        "--detect-only",
        action="store_true",
        help="report the detected format and exit without extracting",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.detect_only:
            print(
                json.dumps(
                    {"source_format": detect_source_format(args.source)}, indent=2
                )
            )
            return 0

        result = ingest_source(args.source, args.source_id)
    except SourceIngestionError as exc:
        # A deterministic, expected ingestion failure: concise diagnostic and a
        # stable error code, not a stack trace.
        print(f"{exc.error_code}: {exc}", file=sys.stderr)
        return 1

    payload = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)

    summary = {
        "source_id": result.source_id,
        "source_format": result.source_format,
        "source_digest": result.source_digest,
        "extractor_version": result.extractor_version,
        "block_count": result.block_count,
    }

    if args.output:
        out_path = Path(args.output).expanduser()
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(payload + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"SOURCE_READ_FAILED: could not write output: {exc}", file=sys.stderr)
            return 1
        summary["output"] = str(out_path)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
