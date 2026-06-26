from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(script_dir))
    from cninfo_annual_reports.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
