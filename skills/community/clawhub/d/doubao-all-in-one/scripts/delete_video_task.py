# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
import json
import time

from common import create_client, delete_video_task, get_trace_id, log_params, setup_logging

setup_logging()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="取消或删除豆包 Seedance 视频任务")
    parser.add_argument("--task-id", required=True, help="视频任务 ID（cgt-xxxx）")
    return parser.parse_args()


def main() -> None:
    pipeline_start = time.monotonic()
    args = parse_args()
    client = create_client()

    trace_id = get_trace_id()
    log_params("删除视频任务", task_id=args.task_id)
    print(f"正在取消/删除任务: {args.task_id}")
    api_start = time.monotonic()
    delete_video_task(client, args.task_id)
    api_elapsed = time.monotonic() - api_start

    total_elapsed = time.monotonic() - pipeline_start
    log_params("删除完成", task_id=args.task_id, api_elapsed=round(api_elapsed, 3), total_elapsed=round(total_elapsed, 3))
    print(json.dumps({
        "trace_id": trace_id,
        "task_id": args.task_id,
        "status": "deleted",
        "timing": {
            "total_elapsed": round(total_elapsed, 3),
            "api_elapsed": round(api_elapsed, 3),
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
