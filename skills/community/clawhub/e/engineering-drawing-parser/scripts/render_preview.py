"""Render a Markdown preview of an extraction result."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def render(data: dict) -> str:
    lines = ["# Engineering Drawing Extraction Preview", ""]
    tb = data.get("title_block", {})
    if tb:
        lines.append("## Title Block")
        for k, v in tb.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    bom = data.get("bom", [])
    if bom:
        lines.append("## BOM")
        lines.append("| No | Part No | Name | Qty | Material | Remark |")
        lines.append("|---|---|---|---|---|---|")
        for r in bom:
            lines.append(f"| {r['no']} | {r['part_no']} | {r['name']} | {r['qty']} | {r['material']} | {r.get('remark','') or ''} |")
        lines.append("")
    dims = data.get("dimensions", [])
    if dims:
        lines.append(f"## Dimensions ({len(dims)} items)")
        for d in dims[:20]:
            lines.append(f"- {d}")
    return "\n".join(lines)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    args = ap.parse_args()
    print(render(json.loads(Path(args.input).read_text(encoding="utf-8"))))
