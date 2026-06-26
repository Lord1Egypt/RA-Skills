#!/usr/bin/env python3
"""
Regenerate ~/ymind-ws/index.html from index.json.

Usage:
  python3 render-index.py
  python3 render-index.py --ws ~/ymind-ws
  python3 render-index.py --ws ~/ymind-ws --out ~/ymind-ws/index.html
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "templates" / "workspace-index.html"
DEFAULT_WS = Path.home() / "ymind-ws"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render YMind workspace index HTML.")
    parser.add_argument("--ws", default=str(DEFAULT_WS), help="Workspace directory (default: ~/ymind-ws)")
    parser.add_argument("--out", default=None, help="Output HTML path (default: <ws>/index.html)")
    parser.add_argument("--template", default=None, help="Custom template path")
    args = parser.parse_args()

    ws = Path(args.ws).expanduser()
    index_json = ws / "index.json"

    if not index_json.exists():
        print(f"Error: {index_json} not found", file=sys.stderr)
        return 1

    with open(index_json, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    tmpl_path = Path(args.template).expanduser() if args.template else TEMPLATE_PATH
    if not tmpl_path.exists():
        print(f"Error: template not found at {tmpl_path}", file=sys.stderr)
        return 1

    template = tmpl_path.read_text(encoding="utf-8")
    sessions_json = json.dumps(index_data, ensure_ascii=False, indent=2)
    html = template.replace("{{SESSIONS_JSON}}", sessions_json)

    out_path = Path(args.out).expanduser() if args.out else ws / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Rendered: {out_path}  ({len(index_data.get('runs', []))} sessions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
