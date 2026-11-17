#!/usr/bin/env python3
"""ClawCode Lens — security scanning (unique feature)."""
import sys
import re

# NOTE: these regexes detect eval()/exec() calls in scanned code — the scanner
# is a static analyzer, matches are only reported, never executed.
PATTERNS = [
    ("CRITICAL", r"(api[_-]?key|secret|password|token)\s*[=:]\s*['\"][A-Za-z0-9_\-]{12,}['\"]",
     "Hardcoded key/secret — use an environment variable"),
    ("HIGH", r"(SELECT|INSERT|UPDATE|DELETE).*f['\"]\s*[+%]|f['\"].*\{.*\}.*(SELECT|INSERT)",
     "Possible SQL injection — use parameterized queries"),
    ("HIGH", r"\beval\s*\(", "eval() — executes arbitrary code, avoid"),
    ("HIGH", r"\bexec\s*\(", "exec() — executes arbitrary code, avoid"),
    ("MEDIUM", r"os\.system\s*\(", "os.system() — use subprocess with argument list"),
    ("MEDIUM", r"input\s*\(.*\)\s*$", "Raw input() without validation"),
    ("LOW", r"http://", "HTTP (unencrypted) — use HTTPS"),
]


def scan(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    out = [f"🔒 Security scan: {path}", ""]
    hits = 0
    for i, line in enumerate(lines, 1):
        for sev, pattern, msg in PATTERNS:
            if re.search(pattern, line, re.I):
                out.append(f"  [{sev}] Line {i}: {msg}")
                out.append(f"         → {line.strip()[:90]}")
                hits += 1
    if hits == 0:
        out.append("  ✅ No known patterns found.")
    out.append(f"\n{len(lines)} lines scanned · {hits} hits")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("USAGE: python3 security_scan.py file.py [--out report.md]")
    report = scan(sys.argv[1])
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Report saved: {out_path}")
    else:
        print(report)
