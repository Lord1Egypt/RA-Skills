#!/usr/bin/env python3
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    capability = json.loads((root / "capability.json").read_text(encoding="utf-8"))
    print(json.dumps(capability, indent=2))


if __name__ == "__main__":
    main()
