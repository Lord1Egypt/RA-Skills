#!/usr/bin/env python3
"""
下载文生数字人生成结果到本地。
用法:
  download_result --url https://example.com/output.png
  download_result --url https://example.com/output.mp4 --output output/text-to-digital-person/demo.mp4
输出: 本地文件路径
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from asset_download import download_chanjing_result_url, print_downloaded_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="下载蝉镜文生数字人生成结果到本地目录")
    parser.add_argument("--url", required=True, help="图片或视频输出地址")
    parser.add_argument(
        "--output",
        help="输出文件路径；默认保存到 skills/chanjing-content-creation-skill/output/text-to-digital-person/<文件名>",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out = Path(args.output) if args.output else None
    try:
        path = download_chanjing_result_url(
            args.url,
            outputs_subdir="text-to-digital-person",
            user_agent="chanjing-text-to-digital-person-downloader",
            default_basename="text-to-digital-person.bin",
            output_path=out,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    print_downloaded_path(path)


if __name__ == "__main__":
    main()
