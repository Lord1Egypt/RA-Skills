from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline import DailyPipeline


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "topics.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run arXiv to Xiaohongshu daily pipeline")
    parser.add_argument("--topic", required=True, help="Topic key from config/topics.json")
    parser.add_argument("--publish", action="store_true", help="Publish generated notes to Xiaohongshu")
    parser.add_argument("--dry-run", action="store_true", help="Run collection and note rendering without publishing")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()
    if args.topic not in config.get("topics", {}):
        raise SystemExit(f"Unknown topic: {args.topic}")
    publish = bool(args.publish and not args.dry_run)
    result = DailyPipeline(PROJECT_ROOT, args.topic, config).run(publish=publish)
    print(f"notes={result.notes_path}")
    print(f"matched={result.matched_path}")
    print(f"post_draft={result.post_draft_path}")
    if result.publish_result_path:
        print(f"publish_result={result.publish_result_path}")
    print(f"matched_count={len(result.matched_papers)}")
    print(f"post_title={result.post_payload['title']}")


if __name__ == "__main__":
    main()
