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

from common import create_client, get_trace_id, log_params, query_video_task, setup_logging

setup_logging()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查询豆包 Seedance 视频任务状态")
    parser.add_argument("--task-id", required=True, help="视频任务 ID（cgt-xxxx）")
    return parser.parse_args()


def main() -> None:
    pipeline_start = time.monotonic()
    args = parse_args()
    client = create_client()

    trace_id = get_trace_id()
    log_params("查询视频任务", task_id=args.task_id)
    api_start = time.monotonic()
    result = query_video_task(client, args.task_id)
    api_elapsed = time.monotonic() - api_start
    log_params("查询完成", task_id=args.task_id, status=result.get("status", ""), api_elapsed=round(api_elapsed, 3))
    status = result.get("status", "unknown")
    content = result.get("content", {})

    output: dict = {
        "trace_id": trace_id,
        "task_id": args.task_id,
        "model": result.get("model", ""),
        "status": status,
        "created_at": result.get("created_at"),
        "updated_at": result.get("updated_at"),
        "service_tier": result.get("service_tier", ""),
        "resolution": result.get("resolution", ""),
        "ratio": result.get("ratio", ""),
        "seed": result.get("seed"),
    }

    if isinstance(content, dict):
        video_url = content.get("video_url", "")
        last_frame_url = content.get("last_frame_url", "")
        if video_url:
            output["video_url"] = video_url
        if last_frame_url:
            output["last_frame_url"] = last_frame_url
    else:
        video_url = getattr(content, "video_url", "")
        last_frame_url = getattr(content, "last_frame_url", "")
        if video_url:
            output["video_url"] = str(video_url)
        if last_frame_url:
            output["last_frame_url"] = str(last_frame_url)

    # duration 和 frames 只返回其中一个
    if result.get("duration") is not None:
        output["duration"] = result["duration"]
    if result.get("frames") is not None:
        output["frames"] = result["frames"]
    if result.get("framespersecond") is not None:
        output["framespersecond"] = result["framespersecond"]

    # 1.5 pro 专属字段
    if "generate_audio" in result:
        output["generate_audio"] = result["generate_audio"]
    if "draft" in result:
        output["draft"] = result["draft"]
    if "draft_task_id" in result:
        output["draft_task_id"] = result["draft_task_id"]
    if "execution_expires_after" in result:
        output["execution_expires_after"] = result["execution_expires_after"]

    # usage 信息
    usage = result.get("usage")
    if usage:
        if isinstance(usage, dict):
            output["usage"] = usage
        else:
            output["usage"] = {
                "completion_tokens": getattr(usage, "completion_tokens", 0),
                "total_tokens": getattr(usage, "total_tokens", 0),
            }

    if status == "failed":
        error = result.get("error")
        if error:
            if isinstance(error, dict):
                output["error"] = error
            else:
                output["error"] = {
                    "code": getattr(error, "code", ""),
                    "message": getattr(error, "message", ""),
                }

    total_elapsed = time.monotonic() - pipeline_start
    output["timing"] = {
        "total_elapsed": round(total_elapsed, 3),
        "api_elapsed": round(api_elapsed, 3),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
