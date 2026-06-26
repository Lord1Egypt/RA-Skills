"""Bilibili upload-video CLI invocation template.

Assumes social-auto-upload was cloned to SAU_HOME and `uv sync --python 3.12`
has already been run. See references/runtime-requirements.md for setup steps.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

# Where OPclaw clones social-auto-upload by convention.
SAU_HOME = Path.home() / ".openclaw" / "social-auto-upload"


def main() -> None:
    account = "account_a"
    # account_name is user-defined. One account_name maps to one account file.
    # You can prepare multiple account names and run them in parallel.

    # Bilibili category id (--tid). 249 = SPORTS_FOOTBALL.
    # See <SAU_HOME>/utils/constant.py (VideoZoneTypes) for the full list.
    tid = "249"

    command = [
        "uv", "run", "--project", str(SAU_HOME), "python", "sau_cli.py",
        "bilibili", "upload-video",
        "--account", account,
        "--file", str(SAU_HOME / "videos" / "demo.mp4"),
        "--title", "Bilibili CLI Demo",
        "--desc", "Bilibili CLI Demo",
        "--tid", tid,
        "--tags", "足球,测试",
        "--schedule", "2026-03-26 16:00",
    ]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
