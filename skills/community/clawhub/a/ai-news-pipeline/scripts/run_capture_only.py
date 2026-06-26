from __future__ import annotations

import argparse
import os
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run capture only for the AI news pipeline.")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Workspace root containing config, data, reports, and state directories.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    os.environ["AI_NEWS_WORKSPACE"] = str(workspace)

    import collect_feeds

    return collect_feeds.main()


if __name__ == "__main__":
    raise SystemExit(main())
