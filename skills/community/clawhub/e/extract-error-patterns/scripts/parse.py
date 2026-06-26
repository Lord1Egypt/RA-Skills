#!/usr/bin/env python3
"""
Extract error patterns from log text and generate alert rules.
"""
import re, sys, json, argparse
from collections import Counter

KNOWN_ERRORS = [
    (r"(?i)exception", "EXCEPTION", "High"),
    (r"(?i)error", "ERROR", "High"),
    (r"(?i)warning", "WARNING", "Medium"),
    (r"(?i)timeout", "TIMEOUT", "Medium"),
    (r"(?i)failed to|failed:", "FAILURE", "High"),
    (r"(?i)refused", "CONNECTION_REFUSED", "High"),
    (r"(?i)memory|cpu|disk", "RESOURCE", "Medium"),
]

def extract_patterns(log_text):
    lines = [l.strip() for l in log_text.split("\n") if l.strip()]
    counters = {label: Counter() for _, label, _ in KNOWN_ERRORS}

    for line in lines:
        for pattern, label, _ in KNOWN_ERRORS:
            if re.search(pattern, line):
                counters[label][line[:120]] += 1

    rules = []
    for pattern, label, default_sev in KNOWN_ERRORS:
        count = sum(counters[label].values())
        if count > 0:
            top = counters[label].most_common(3)
            rules.append({
                "name": f"alert_{label.lower()}",
                "type": label,
                "count": count,
                "severity": default_sev,
                "pattern": pattern,
                "top_samples": [s for s, _ in top],
            })
    return rules

def to_markdown_alerts(rules):
    lines = ["# Alert Rules\n"]
    for r in rules:
        lines.append(f"## {r['name']} (`{r['type']}`)\n")
        lines.append(f"- **Severity:** {r['severity']}")
        lines.append(f"- **Occurrences:** {r['count']}")
        lines.append(f"- **Regex:** ````{r['pattern']}````")
        lines.append(f"- **Samples:**")
        for s in r["top_samples"]:
            lines.append(f"  ```\n  {s}\n  ```")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("file", help="Log file path")
    p.add_argument("-f", "--format", default="markdown", choices=["markdown", "json"])
    p.add_argument("-o", "--output", help="Output file path")
    args = p.parse_args()

    with open(args.file) as f:
        text = f.read()

    rules = extract_patterns(text)
    out = to_markdown_alerts(rules) if args.format == "markdown" else json.dumps(rules, indent=2)

    if args.output:
        open(args.output, "w").write(out)
        print(f"✅ Written to {args.output}")
    else:
        print(out)