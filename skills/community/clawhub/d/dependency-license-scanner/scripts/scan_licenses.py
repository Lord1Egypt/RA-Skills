#!/usr/bin/env python3
import sys
from pathlib import Path
def main(path: str) -> None:
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            pkg, lic = line.split("|", 1)
            print(f"{pkg.strip()} | {lic.strip()}")
        else:
            print(f"{line} | UNKNOWN")
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "deps.txt")
