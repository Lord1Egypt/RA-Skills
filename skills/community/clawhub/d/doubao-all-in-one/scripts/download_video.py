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
from pathlib import Path

from common import OUTPUT_ROOT, default_output_path, download_file, get_trace_id, log_params, setup_logging

setup_logging()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="下载豆包 Seedance 视频到本地")
    parser.add_argument("--url", required=True, help="视频下载 URL")
    parser.add_argument("--output", help="输出文件路径，默认写入 outputs/doubao/videos/")
    parser.add_argument("--scene", default="text_to_video", help="场景子目录")
    parser.add_argument("--name", default="", help="文件名描述，不超过 10 个中文字")
    return parser.parse_args()


def main() -> None:
    pipeline_start = time.monotonic()
    args = parse_args()
    trace_id = get_trace_id()
    log_params("下载视频开始", url=args.url, name=args.name)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = default_output_path("videos", args.scene, suffix=".mp4", name=args.name)

    download_start = time.monotonic()
    download_file(args.url, output_path)
    download_elapsed = time.monotonic() - download_start

    total_elapsed = time.monotonic() - pipeline_start
    log_params("下载视频完成", path=str(output_path.name), download_elapsed=round(download_elapsed, 3))
    result = {
        "type": "video",
        "provider": "doubao",
        "trace_id": trace_id,
        "local_path": str(output_path.relative_to(OUTPUT_ROOT)),
        "source_url": args.url,
        "timing": {
            "total_elapsed": round(total_elapsed, 3),
            "download_elapsed": round(download_elapsed, 3),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
