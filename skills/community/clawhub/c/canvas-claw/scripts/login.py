#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from canvas_claw.auth import login_and_extract_session
from canvas_claw.client import CanvasClawClient
from canvas_claw.config import RuntimeConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Login to AI-video-agent")
    parser.add_argument("--base-url", required=True, help="AI-video-agent base URL")
    parser.add_argument("--site-id", required=True, type=int, help="Site ID")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = RuntimeConfig(base_url=args.base_url.rstrip("/"), token="", site_id=args.site_id)
    client = CanvasClawClient(config)
    session = login_and_extract_session(
        client,
        username=args.username,
        password=args.password,
    )
    print(f"AI_VIDEO_AGENT_BASE_URL={args.base_url.rstrip('/')}")
    print(f"AI_VIDEO_AGENT_SITE_ID={args.site_id}")
    print(f"AI_VIDEO_AGENT_TOKEN={session.get('token', '')}")


if __name__ == "__main__":
    main()
