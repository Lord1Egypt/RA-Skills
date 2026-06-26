#!/usr/bin/env python3
"""build_deliverable.py — one-command banker pipeline for a CN listed company.

Chains the three existing scripts in order:

    bj_smoke_v2         →  analysis.md + data-provenance.md + raw-data/*.json
    extract_deck_numbers →  deck-numbers.json (numbers-lookup for slides/docx)
    build_deck           →  slides/slide-NN.js → compile.js → {ts_code}_deep_analysis.pptx
    md_to_docx           →  {slug}_memo.docx   (via aigroup-mdtoword-mcp converter)
    validate-delivery    →  7-gate --strict-mcp check

Usage:
    python3 build_deliverable.py <deliverable_dir> <ts_code> <name_cn> <fullname>
                                 <name_en> <industry> [memo_name]

Example:
    python3 build_deliverable.py ~/deliverables/boe 000725.SZ "京东方A" \\
        "京东方科技集团股份有限公司" "BOE Technology Group" "元器件" boe_memo.docx

Exit codes:
    0 — all 7 gates PASS, deck + memo shippable
    1 — any step failed (gate output goes to stderr)
"""
from __future__ import annotations
import argparse, pathlib, subprocess, sys


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
BJ_SMOKE_V2 = SCRIPT_DIR / "bj_smoke_v2.py"
BUILD_DECK = SCRIPT_DIR / "build_deck.py"
EXTRACT_DECK = SCRIPT_DIR / "extract_deck_numbers.py"
VALIDATE = SCRIPT_DIR / "validate-delivery.py"

# md_to_docx.mjs is a thin Node wrapper around aigroup-mdtoword-mcp's
# DocxMarkdownConverter. It ships at /tmp/md_to_docx.mjs on macmini during
# the v0.9.x smoke tests. When the banker workflow stabilises, this will
# move into scripts/ proper — for now we accept a path override via env.
MD_TO_DOCX = pathlib.Path(
    __import__("os").environ.get("MD_TO_DOCX_MJS", "/tmp/md_to_docx.mjs")
)


def run(label: str, argv: list[str], **kwargs) -> None:
    print(f"[{label}] {' '.join(str(a) for a in argv)}")
    r = subprocess.run(argv, **kwargs)
    if r.returncode != 0:
        sys.exit(f"[{label}] FAILED with exit {r.returncode}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("deliverable_dir", type=pathlib.Path)
    ap.add_argument("ts_code", help="A-share ticker, e.g. 000725.SZ")
    ap.add_argument("name_cn", help="Chinese short name, e.g. 京东方A")
    ap.add_argument("fullname", help="Legal registered name for PrimeMatrix lookup")
    ap.add_argument("name_en", help="English cover-page title")
    ap.add_argument("industry", help="Industry label for slide 07 credit view")
    ap.add_argument("memo_name", nargs="?", default=None,
                    help="Filename for Word memo (default: {ts_safe}_memo.docx)")
    ap.add_argument("--skip-validate", action="store_true",
                    help="Skip the final validate-delivery gate (not recommended)")
    args = ap.parse_args()

    d = args.deliverable_dir.resolve()
    d.mkdir(parents=True, exist_ok=True)
    ts_safe = args.ts_code.lower().replace(".", "_")
    memo = args.memo_name or f"{ts_safe}_memo.docx"

    # Stage 1: fetch raw-data + assemble analysis.md + data-provenance.md.
    # bj_smoke_v2 in single-company mode writes directly into `d`.
    run("bj_smoke_v2",
        ["python3", str(BJ_SMOKE_V2), str(d), args.ts_code,
         args.name_cn, args.fullname])

    run("extract_deck_numbers", ["python3", str(EXTRACT_DECK), str(d)])
    run("build_deck",
        ["python3", str(BUILD_DECK), str(d), args.ts_code,
         args.name_cn, args.name_en, args.industry])

    if not MD_TO_DOCX.exists():
        print(f"[md_to_docx] SKIPPED — {MD_TO_DOCX} missing "
              f"(set MD_TO_DOCX_MJS env or ship md_to_docx.mjs into scripts/)",
              file=sys.stderr)
    else:
        run("md_to_docx",
            ["node", str(MD_TO_DOCX), str(d / "analysis.md"), str(d / memo)])

    if args.skip_validate:
        print("[validate] SKIPPED (--skip-validate)")
        return 0

    run("validate-delivery",
        ["python3", str(VALIDATE), "--strict-mcp", str(d)])
    print(f"\n✓ {d} shippable — deck + memo pass all applicable gates under --strict-mcp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
