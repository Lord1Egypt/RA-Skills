import re
import sys
from pathlib import Path

ERROR_PATTERNS = [
    re.compile(r"! LaTeX Error:"),
    re.compile(r"! Emergency stop"),
    re.compile(r"Fatal error occurred"),
    re.compile(r"Citation .* undefined", re.IGNORECASE),
    re.compile(r"Reference .* undefined", re.IGNORECASE),
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python check_latex_log.py <main.log>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"LaTeX log not found: {path}")
        return 1

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    matches = []
    for index, line in enumerate(lines, start=1):
        if any(pattern.search(line) for pattern in ERROR_PATTERNS):
            matches.append((index, line.strip()))

    if matches:
        print("LaTeX log issues found:")
        for index, line in matches[:50]:
            print(f"{index}: {line}")
        return 1

    print("LaTeX log sanity check ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
