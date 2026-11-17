#!/usr/bin/env python3
"""Bind a golden-anchor reference rubric to a rendered v4 deck (plan B).

A trusted reference rubric needs three pieces:

  * the 6 dimension scores (0-3) + evidence strings    -- HUMAN/MODEL
  * review provenance (review_id, reviewed_at, method) -- HUMAN
  * byte-level evidence bindings (pptx + render report
    + per-slide image sha256)                          -- MECHANICAL (here)

This script does the mechanical part: optionally renders ``deck.pptx`` to
per-slide PNG images via LibreOffice + pdftoppm, builds the render report,
computes the three sha256 bindings plus the case/build/deck ids, and writes
a ``reference-rubric.json`` TEMPLATE with empty score/evidence/provenance
slots. Fill those slots, and the rubric harness (``scripts/score_v4.py``
with ``use_reference_rubric=True``) will honor the anchor exactly like the
v3 flow — bindings prove the scores apply to THIS exact deck, byte for byte.

Usage:
  python3 scripts/bind_golden_anchor.py --case-id product-launch \
      --pptx out/deck.pptx --render --work-dir /tmp/anchor \
      --output reference-rubric.json
  # then edit reference-rubric.json: fill dimensions[].score (0-3) +
  # dimensions[].evidence, and scorer.provenance.{review_id,reviewed_at,method}

Without ``--render``, pass ``--slides-dir`` containing one image per slide
(named with an embedded integer, e.g. page-1.png / slide_02.png).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from score_deck import build_evidence_binding, sha256_file  # noqa: E402

DIMENSIONS = [
    "title_role_and_message_quality",
    "content_fidelity",
    "expression_architecture",
    "page_composition",
    "component_craft",
    "editability_hygiene",
]

_SLIDE_NUM = re.compile(r"(\d+)")


def _render_to_images(pptx: Path, work_dir: Path) -> list[Path]:
    pdf = work_dir / (pptx.stem + ".pdf")
    subprocess.run(
        ["soffice", "--headless", "-env:UserInstallation=file:///tmp/lo-profile-anchor",
         "--convert-to", "pdf", "--outdir", str(work_dir), str(pptx)],
        check=True, capture_output=True,
    )
    if not pdf.is_file():
        raise SystemExit(f"LibreOffice did not produce {pdf}")
    subprocess.run(
        ["pdftoppm", "-png", "-r", "80", str(pdf), str(work_dir / "slide")],
        check=True, capture_output=True,
    )
    images = sorted(work_dir.glob("slide-*.png"), key=_slide_key)
    if not images:
        raise SystemExit("pdftoppm produced no slide images")
    return images


def _slide_key(path: Path) -> int:
    match = _SLIDE_NUM.search(path.stem)
    return int(match.group(1)) if match else 0


def _discover_images(slides_dir: Path) -> list[Path]:
    images = [p for p in slides_dir.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
    if not images:
        raise SystemExit(f"no slide images found under {slides_dir}")
    return sorted(images, key=_slide_key)


def _render_report(images: list[Path]) -> dict[str, Any]:
    return {
        "status": "passed",
        "renderer": "libreoffice-pdftoppm",
        "slides": [
            {"slide_index": i + 1, "image": str(image)}
            for i, image in enumerate(images)
        ],
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--pptx", required=True)
    render = parser.add_mutually_exclusive_group()
    render.add_argument("--render", action="store_true",
                        help="render deck.pptx to slide images via LibreOffice + pdftoppm")
    render.add_argument("--slides-dir", help="existing per-slide images directory")
    parser.add_argument("--work-dir", default=None, help="work dir for rendering")
    parser.add_argument("--output", required=True, help="output reference-rubric.json")
    parser.add_argument("--render-report-out", default=None,
                        help="also write the render-report.json consumed by score_v4")
    args = parser.parse_args(argv)

    pptx = Path(args.pptx)
    if not pptx.is_file():
        raise SystemExit(f"deck not found: {pptx}")

    work_dir = Path(args.work_dir) if args.work_dir else Path(args.output).parent
    work_dir.mkdir(parents=True, exist_ok=True)
    images = _render_to_images(pptx, work_dir) if args.render else _discover_images(Path(args.slides_dir))
    render_report = _render_report(images)

    case_id = args.case_id
    build_id = f"{case_id}-unknown-build"
    deck_id = case_id
    binding = build_evidence_binding(pptx, render_report)

    template: dict[str, Any] = {
        "schema_version": "1.0",
        "case_id": case_id,
        "build_id": build_id,
        "deck_id": deck_id,
        "dimensions": [
            {
                "dimension": dim,
                "score": None,          # TODO(human): 0-3
                "confidence": 0.85,
                "evidence": [],          # TODO(human): non-empty strings
            }
            for dim in DIMENSIONS
        ],
        "bindings": {
            "case_id": case_id,
            "build_id": build_id,
            "deck_id": deck_id,
            **binding,
        },
        "scorer": {
            "type": "human_reference",
            "name": "",                  # TODO(human)
            "version": "1.0",
            "provenance": {
                "review_id": "",         # TODO(human)
                "reviewed_at": "",       # TODO(human): ISO-8601
                "method": "",            # TODO(human): e.g. "visual review of rendered slides"
            },
        },
        "notes": [
            "Generated by bind_golden_anchor.py; scores and provenance are placeholders.",
            "Fill dimensions[].score (0-3 each) + evidence, then set scorer provenance;",
            "the evidence bindings above are already valid for THIS deck.",
        ],
    }
    template["notes"].append(f"generated_at: {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.render_report_out:
        rr_out = Path(args.render_report_out)
        rr_out.parent.mkdir(parents=True, exist_ok=True)
        rr_out.write_text(json.dumps(render_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {rr_out}")
    print(f"wrote {out}")
    print(f"slides: {len(images)} | pptx_sha256: {binding['pptx_sha256']}")
    print(f"render_report_sha256: {binding['render_report_sha256']}")
    print(f"render_evidence_sha256: {binding['render_evidence_sha256']}")
    print("TODO: fill dimensions[].score/evidence and scorer.provenance before use.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
