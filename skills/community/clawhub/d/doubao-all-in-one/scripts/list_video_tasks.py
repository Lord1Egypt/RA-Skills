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

from common import create_client, get_trace_id, list_video_tasks, log_params, setup_logging

setup_logging()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="批量查询豆包 Seedance 视频任务")
    parser.add_argument("--page-num", type=int, help="页码，范围 [1, 500]")
    parser.add_argument("--page-size", type=int, help="每页数量，范围 [1, 500]")
    parser.add_argument("--status", help="按状态过滤：queued, running, cancelled, succeeded, failed")
    parser.add_argument("--task-id", action="append", dest="task_ids", help="按任务 ID 过滤，可多次传")
    parser.add_argument("--model", help="按模型/接入点 ID 过滤")
    parser.add_argument("--service-tier", choices=["default", "flex"], help="按推理模式过滤")
    return parser.parse_args()


def main() -> None:
    pipeline_start = time.monotonic()
    args = parse_args()
    client = create_client()

    trace_id = get_trace_id()
    log_params("批量查询视频任务", status=args.status, model=args.model)
    api_start = time.monotonic()
    result = list_video_tasks(
        client,
        page_num=args.page_num,
        page_size=args.page_size,
        status=args.status,
        task_ids=args.task_ids,
        model=args.model,
        service_tier=args.service_tier,
    )
    api_elapsed = time.monotonic() - api_start

    items = result.get("items", [])
    total = result.get("total", 0)

    total_elapsed = time.monotonic() - pipeline_start
    log_params("批量查询完成", total=total, count=len(items), api_elapsed=round(api_elapsed, 3))
    output = {
        "trace_id": trace_id,
        "total": total,
        "count": len(items),
        "items": items,
        "timing": {
            "total_elapsed": round(total_elapsed, 3),
            "api_elapsed": round(api_elapsed, 3),
        },
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
