#!/usr/bin/env python3
"""ClawCode Lens — forbedrings-forslag (unik feature)."""
import sys
import re
from collections import Counter


def analyze(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as f:
        code = f.read()
    lines = code.splitlines()
    out = [f"💡 Forbedrings-forslag: {path}", ""]
    suggestions = []

    # 1. Funktioner uden docstring
    funcs = [(i, l.strip()) for i, l in enumerate(lines, 1) if re.match(r"^\s*def \w+", l)]
    for i, l in funcs:
        nxt = lines[i] if i < len(lines) else ""
        if not nxt.strip().startswith(('"""', "'''", "#")):
            suggestions.append(f"  [{i}] `{l[:60]}` mangler docstring/kommentar")

    # 2. Gentagne linjer (duplikat-detektion)
    line_counts = Counter(l.strip() for l in lines if l.strip())
    dups = [(l, n) for l, n in line_counts.most_common(5) if n >= 3 and len(l) > 10]
    for l, n in dups:
        suggestions.append(f"  Linje gentaget {n}×: `{l[:60]}` — overvej at trække ud i funktion")

    # 3. Missing error handling
    if "try:" in code and "except" not in code:
        suggestions.append("  `try:` uden `except` — tilføj fejlhåndtering")
    if re.search(r"open\([^)]*\)", code) and "with open" not in code and "close()" not in code:
        suggestions.append("  `open()` uden context manager (`with`) — risiko for fil-læk")

    # 4. Print-debugging
    prints = sum(1 for l in lines if re.match(r"\s*print\(", l))
    if prints > 3:
        suggestions.append(f"  {prints} print()-kald — overvej logging-modul i stedet")

    # 5. Hardcodede værdier
    hardcoded = re.findall(r"=\s*['\"][^'\"]{5,}['\"]", code)
    if hardcoded:
        suggestions.append(f"  {len(hardcoded)} hardcodede strenge — overvej konstanter/config")

    if not suggestions:
        out.append("  ✅ Koden ser ren ud — ingen umiddelbare forbedringer fundet.")
    else:
        out.extend(suggestions)
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("BRUG: python3 improve.py fil.py [--out forslag.md]")
    report = analyze(sys.argv[1])
    if "--out" in sys.argv:
        p = sys.argv[sys.argv.index("--out") + 1]
        with open(p, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Forslag gemt: {p}")
    else:
        print(report)
