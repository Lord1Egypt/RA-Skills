#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check weight conservation: bullets per section must not exceed the source's KU count.

The rule (editorial-qa 门 3.6) says one source subsection contributes at most one
bullet. Prose can state that; only a script can enforce it. The source-side KU
counts are declared by the author when scoring KUs, so this script needs a
manifest.


Manifest (either inline in the HTML, or a sidecar .json passed with --manifest):

    <!-- weight-manifest {"sections":[{"heading":"一 · 定位","ku":3,"bullets":3}]} -->

    {
      "source": "RAG评测黄金集怎么建设解析.docx",
      "sections": [
        {"heading": "一 · 定位", "ku": 3, "bullets": 3},
        {"heading": "二 · 第一问", "ku": 3, "bullets": 3}
      ]
    }

ku      = 该节在原文里的可独立成条单元数（打分选点产物，人工填）
bullets = 成稿该节的要点条数（可选；填了就和实际条数比对，防漂移）

Exit codes: 0 = pass, 1 = violation, 2 = cannot run (no manifest / bad file).
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

MANIFEST_RE = re.compile(r"<!--\s*weight-manifest\s*(\{.*?\})\s*-->", re.S)


def disp_width(text: str) -> int:
    """Terminal width: CJK glyphs occupy two columns."""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def pad(text: str, width: int) -> str:
    """Left-align by display width (str.ljust counts CJK as one)."""
    return text + " " * max(0, width - disp_width(text))


def strip_tags(fragment: str) -> str:
    return re.sub(r"<[^>]+>", "", fragment)


def sections_of(html: str):
    """Split body into (heading, slice) pairs following each <h2>."""
    body = re.sub(r"(?s)<head>.*?</head>", " ", html)
    parts = re.split(r"(?i)(?=<h2\b)", body)
    out = []
    for part in parts:
        m = re.match(r"(?is)<h2\b[^>]*>(.*?)</h2>", part)
        if not m:
            continue
        heading = re.sub(r"\s+", " ", strip_tags(m.group(1))).strip()
        slice_ = part[m.end():]
        # stop at the next section/page boundary
        cut = re.search(r"(?i)</section>|<section\b", slice_)
        if cut:
            slice_ = slice_[:cut.start()]
        out.append((heading, slice_))
    return out


def count_bullets(slice_: str) -> int:
    return len(re.findall(r"(?i)<li\b", slice_))


def load_manifest(args, html: str):
    if args.manifest:
        p = Path(args.manifest)
        if not p.is_file():
            return None, f"manifest not found: {p}"
        return json.loads(p.read_text(encoding="utf-8")), None
    m = MANIFEST_RE.search(html)
    if m:
        return json.loads(m.group(1)), None
    return None, ("no manifest found (inline <!-- weight-manifest ... --> "
                  "or --manifest file). Run with --init to print a skeleton.")


def skeleton(sections):
    data = {
        "source": "<原文标题或路径>",
        "sections": [{"heading": h, "ku": None, "bullets": n} for h, n in sections],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def check(path, manifest_path=None) -> dict:
    """Run the gate; return {code, rows, violations, warnings, error}."""
    p = Path(path)
    if not p.is_file():
        return {"code": 2, "rows": [], "violations": [], "warnings": [],
                "error": f"file not found: {p}"}
    html = p.read_text(encoding="utf-8")
    sections = sections_of(html)
    if not sections:
        return {"code": 2, "rows": [], "violations": [], "warnings": [],
                "error": "no <h2> section found"}

    class _Args:
        pass

    a = _Args()
    a.manifest = manifest_path
    manifest, err = load_manifest(a, html)
    if manifest is None:
        return {"code": 2, "rows": [], "violations": [], "warnings": [], "error": err}

    by_heading = {re.sub(r"\s+", "", s.get("heading", "")): s
                  for s in manifest.get("sections", [])}
    rows, violations, warnings, seen = [], [], [], set()

    for heading, slice_ in sections:
        key = re.sub(r"\s+", "", heading)
        entry = by_heading.get(key)
        actual = count_bullets(slice_)
        if entry is None:
            if actual:
                warnings.append(f"「{heading}」不在清单里，但有 {actual} 条要点")
            rows.append({"heading": heading, "ku": None, "bullets": actual,
                         "declared": None, "verdict": "no manifest entry"})
            continue
        seen.add(key)
        ku = entry.get("ku")
        declared = entry.get("bullets")
        if ku is None:
            violations.append(f"「{heading}」ku 未填，无法判定")
            rows.append({"heading": heading, "ku": None, "bullets": actual,
                         "declared": declared, "verdict": "ku missing"})
            continue
        over = actual > ku
        drift = declared is not None and declared != actual
        if over:
            violations.append(f"「{heading}」要点 {actual} 条 > 原文单元 {ku} 条（重心偏移）")
        if drift:
            warnings.append(f"「{heading}」清单记 {declared} 条，实际 {actual} 条")
        rows.append({"heading": heading, "ku": ku, "bullets": actual,
                     "declared": declared,
                     "verdict": "FAIL over-split" if over else ("WARN drift" if drift else "ok")})

    for key, entry in by_heading.items():
        if key not in seen:
            warnings.append(f"清单里的「{entry.get('heading')}」在文档中找不到对应 h2")

    return {"code": 1 if violations else 0, "rows": rows,
            "violations": violations, "warnings": warnings, "error": None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--init", action="store_true",
                    help="print a skeleton manifest (ku left empty for you to fill)")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"[FAIL] file not found: {path}", file=sys.stderr)
        return 2

    if args.init:
        html = path.read_text(encoding="utf-8")
        sections = sections_of(html)
        if not sections:
            print("[FAIL] no <h2> section found", file=sys.stderr)
            return 2
        print(skeleton([(h, count_bullets(s)) for h, s in sections]))
        return 0

    result = check(path, args.manifest)
    if result["error"]:
        print(f"[FAIL] {result['error']}", file=sys.stderr)
        return 2

    print("== check_weight ==")
    print(f"file: {path.name}")
    print()
    print(f"{'section':<34}{'ku':>4}{'bullets':>9}{'decl':>6}   verdict")
    for r in result["rows"]:
        ku = r["ku"] if r["ku"] is not None else "-"
        decl = r["declared"] if r["declared"] is not None else "-"
        print(f"{pad(r['heading'][:32], 34)}{str(ku):>4}{r['bullets']:>9}{str(decl):>6}   {r['verdict']}")

    print()
    for w in result["warnings"]:
        print(f"[WARN] {w}")
    for v in result["violations"]:
        print(f"[FAIL] {v}")

    if result["code"]:
        print("\nRESULT: FAIL")
        return 1
    print("RESULT: PASS" + (" (with warnings)" if result["warnings"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
