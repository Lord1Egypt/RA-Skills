"""Douyin CLI invocation template.

Assumes social-auto-upload was cloned to SAU_HOME and `uv sync --python 3.12`
has already been run. See references/runtime-requirements.md for setup steps.
"""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

# Where OPclaw clones social-auto-upload by convention.
SAU_HOME = Path.home() / ".openclaw" / "social-auto-upload"

# Prefix every sau_cli.py invocation with `uv run --project <SAU_HOME>`.
SAU_PREFIX = ["uv", "run", "--project", str(SAU_HOME), "python", "sau_cli.py"]


def run_command(command: list[str]) -> None:
    print("Running:", " ".join(shlex.quote(part) for part in command))
    subprocess.run(command, check=True)


def main() -> None:
    account = "account_a"
    # account_name is user-defined. One account_name maps to one account file.
    # You can prepare multiple account names and run them in parallel.

    commands = [
        SAU_PREFIX + ["douyin", "login", "--account", account, "--headless"],
        SAU_PREFIX + ["douyin", "check", "--account", account],
        SAU_PREFIX + [
            "douyin", "upload-video",
            "--account", account,
            "--file", "videos/demo.mp4",
            "--title", "Douyin video from Python",
            "--desc", "Douyin video description from Python",
            "--tags", "cli,video",
            "--thumbnail", "videos/demo.png",
            "--headless",
        ],
        SAU_PREFIX + [
            "douyin", "upload-note",
            "--account", account,
            "--images", "videos/1.png", "videos/2.png",
            "--title", "Douyin note title from Python",
            "--note", "Douyin note from Python",
            "--tags", "cli,note",
            "--headless",
        ],
    ]

    for command in commands:
        run_command(command)


if __name__ == "__main__":
    main()
