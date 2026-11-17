#!/usr/bin/env python3
"""Heuristic scan of a Markdown rulebook. Suggests tiers; humans decide."""
import json, re, sys, csv

MUST = re.compile(r"(必须|不得|禁止|务必|must|shall|required|never|do not|don't)", re.I)
INTERCEPT = re.compile(r"(禁止|不得|block|deny|forbid|permission|sandbox|拒绝|拦截)", re.I)
GATE = re.compile(r"(退出码|exit code|exit non-zero|lint|checker|gate|校验|检查脚本)", re.I)
DETECT = re.compile(r"(审计|检测|audit|scan|report|日志|log)", re.I)


def main(path):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            s = line.strip()
            if not s or not MUST.search(s):
                continue
            if INTERCEPT.search(s):
                tier = "interception"
            elif GATE.search(s):
                tier = "gate"
            elif DETECT.search(s):
                tier = "detection"
            else:
                tier = "prompt"
            rows.append({"line": i, "suggested_tier": tier, "text": s[:200]})

    counts = {"interception": 0, "gate": 0, "detection": 0, "prompt": 0}
    for r in rows:
        counts[r["suggested_tier"]] += 1
    total = len(rows) or 1
    summary = {
        "file": path,
        "must_clauses": len(rows),
        "suggested_counts": counts,
        "blocking_coverage_suggested": round((counts["interception"] + counts["gate"]) / total, 3),
        "note": "Heuristic only. Review every row; keyword hits are not tier verdicts.",
    }

    out = path.rsplit(".", 1)[0] + "-tiers.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["line", "suggested_tier", "final_tier", "text"])
        w.writeheader()
        for r in rows:
            w.writerow({**r, "final_tier": ""})
    summary["csv"] = out
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: rule_scan.py <rules.md>")
        raise SystemExit(2)
    main(sys.argv[1])
