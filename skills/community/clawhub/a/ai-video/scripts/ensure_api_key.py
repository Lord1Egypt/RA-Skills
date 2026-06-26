#!/usr/bin/env python3
"""Check SKILLS_VIDEO_API_KEY and print setup guidance when missing."""

from __future__ import annotations

import json
import os


def main() -> int:
    key = os.environ.get("SKILLS_VIDEO_API_KEY", "").strip()

    if key:
        print(
            json.dumps(
                {
                    "ok": True,
                    "env_var": "SKILLS_VIDEO_API_KEY",
                    "message": "API key detected.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(
        json.dumps(
            {
                "ok": False,
                "env_var": "SKILLS_VIDEO_API_KEY",
                "message": "Missing API key. Configure it before calling skills.video APIs.",
                "dashboard_url": "https://skills.video/dashboard/developer",
                "how_to_get_key": [
                    "Sign in at the dashboard URL.",
                    "Click 'Create API Key'.",
                    "Copy the generated key.",
                ],
                "set_env_examples": [
                    "export SKILLS_VIDEO_API_KEY=\"<YOUR_API_KEY>\"",
                    "echo 'export SKILLS_VIDEO_API_KEY=\"<YOUR_API_KEY>\"' >> ~/.zshrc && source ~/.zshrc",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
