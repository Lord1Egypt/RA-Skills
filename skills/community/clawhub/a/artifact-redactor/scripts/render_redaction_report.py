#!/usr/bin/env python3
"""Render a markdown report from Artifact Redactor JSON outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: str) -> dict[str, object]:
    return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))


def top_findings(payload: dict[str, object], limit: int = 5) -> list[dict[str, object]]:
    findings = payload.get("findings") or []
    findings = sorted(
        findings,
        key=lambda item: (0 if item.get("severity") == "error" else 1, str(item.get("file", "")), int(item.get("line", 0) or 0)),
    )
    return findings[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scan", required=True, help="Path to original scan JSON.")
    parser.add_argument("--redaction", required=True, help="Path to redaction JSON.")
    parser.add_argument("--check", required=True, help="Path to output-check JSON.")
    parser.add_argument("--out", required=True, help="Output markdown path.")
    args = parser.parse_args()

    scan = load_json(args.scan)
    redaction = load_json(args.redaction)
    check = load_json(args.check)

    manual_review_count = int(check.get("manual_review_count", 0) or 0)
    if check.get("finding_count", 0):
        recommendation = "Fix before sharing"
    elif manual_review_count:
        recommendation = "Manual review before sharing"
    else:
        recommendation = "Share"
    counts = redaction.get("redaction_counts", {})
    skipped_files = redaction.get("skipped_files") or []

    lines = [
        "# Artifact Redaction Report",
        "",
        f"- Recommendation: **{recommendation}**",
        f"- Original findings: **{scan.get('finding_count', 0)}**",
        f"- Output findings: **{check.get('finding_count', 0)}**",
        f"- Processed text files: **{redaction.get('processed_files', 0)}**",
        f"- Manual-review files: **{manual_review_count}**",
        f"- Skipped files: **{len(skipped_files)}**",
        "",
        "## Redactions Applied",
        "",
        f"- Private URLs: **{counts.get('private_url', 0)}**",
        f"- Public URL query removals: **{counts.get('public_url_query', 0)}**",
        f"- Private paths: **{counts.get('private_path', 0)}**",
        f"- Secret-like strings: **{counts.get('secret_like', 0)}**",
        f"- Emails: **{counts.get('email', 0)}**",
        f"- Phones: **{counts.get('phone', 0)}**",
        "",
        "## Top Original Findings",
        "",
    ]

    original_findings = top_findings(scan)
    if original_findings:
        for item in original_findings:
            lines.append(f"- `{item.get('severity')}` `{item.get('code')}` {item.get('file')}:{item.get('line')}: {item.get('snippet')}")
    else:
        lines.append("- No obvious sensitive text patterns detected in supported text files.")

    lines.extend(["", "## Output Check", ""])
    if check.get("finding_count", 0):
        for item in top_findings(check):
            lines.append(f"- `{item.get('severity')}` `{item.get('code')}` {item.get('file')}:{item.get('line')}: {item.get('snippet')}")
    else:
        lines.append("- No obvious sensitive text patterns remain in processed text files.")
        if manual_review_count:
            lines.append(f"- {manual_review_count} skipped file(s) still require manual review before sharing the full bundle.")

    lines.extend(["", "## Manual Review", ""])
    if skipped_files:
        for item in skipped_files[:10]:
            lines.append(f"- `{item.get('file')}` skipped: {item.get('reason')}")
        if len(skipped_files) > 10:
            lines.append(f"- ... plus {len(skipped_files) - 10} more skipped files")
    else:
        lines.append("- No binary or unsupported files were skipped.")

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
