"""main.py — 调用 track_latest 的同款全流程入口。"""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
load_dotenv(ROOT_DIR / ".env")

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from track_latest import parse_args, run_pipeline  # noqa: E402


def main(argv: list[str] | None = None):
    args = parse_args(argv)
    run_pipeline(limit=args.limit, skip_audio=args.no_audio, accounts_file=args.accounts_file)


if __name__ == "__main__":
    main()
