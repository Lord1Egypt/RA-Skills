"""Render analysis result as Markdown."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def render(result: dict) -> str:
    lines = ["# Financial Report Analysis", ""]
    comp = result.get("company") or {}
    period = result.get("period") or {}
    lines.append(f"**Company:** {comp.get('name','?')}  ")
    lines.append(f"**Period:** FY{period.get('fiscal_year','?')} ({period.get('reporting_basis','?')})")
    lines.append("")
    if "executive_summary" in result:
        lines.append("## Executive Summary"); lines.append(""); lines.append(result["executive_summary"]); lines.append("")
    if "ratios" in result:
        lines.append("## Key Ratios"); lines.append("")
        for group, vals in result["ratios"].items():
            lines.append(f"### {group}")
            for k, v in vals.items():
                pct = f"{v*100:.2f}%" if isinstance(v, float) and -10 < v < 10 else str(v)
                lines.append(f"- **{k}**: {pct}")
            lines.append("")
    if "red_flags" in result:
        lines.append("## Red Flags"); lines.append("")
        if not result["red_flags"]:
            lines.append("_None detected._")
        for f in result["red_flags"]:
            lines.append(f"- {f['severity']} **{f['code']}** {f['title']} — {f['evidence']}")
    return "\n".join(lines)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render(data))
