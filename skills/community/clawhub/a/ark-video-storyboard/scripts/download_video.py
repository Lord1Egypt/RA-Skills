#!/usr/bin/env python3
"""Download a generated Ark video to a local file."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# 默认输出目录
DEFAULT_OUTPUT_DIR = Path.home() / ".openclaw" / "media"


def get_output_dir(base_dir: Path | None = None) -> Path:
    """自动创建以当前时间命名的目录，如 20260318152844"""
    if base_dir is None:
        base_dir = DEFAULT_OUTPUT_DIR
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = base_dir / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def download(url: str, output_path: str | None = None, create_dated_dir: bool = True, output_dir: Path | None = None) -> str:
    """
    下载视频到指定路径。

    Args:
        url: 视频链接
        output_path: 输出文件路径（不含目录部分）
        create_dated_dir: 是否自动创建日期目录（默认 True）
        output_dir: 指定输出目录路径，若指定则忽略 create_dated_dir，直接使用该目录

    Returns:
        下载后的本地文件路径
    """
    if output_dir is not None:
        out_dir = Path(output_dir)
    elif create_dated_dir:
        out_dir = get_output_dir()
    else:
        out_dir = Path(DEFAULT_OUTPUT_DIR)

    out_dir.mkdir(parents=True, exist_ok=True)

    if output_path:
        out = out_dir / output_path
    else:
        out = out_dir / "video.mp4"

    cmd = ["curl", "-L", "-sS", url, "-o", str(out)]
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "curl download failed")
    return str(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--output', default=None, help='输出文件名（不含目录）')
    parser.add_argument('--dir', default=None, help='指定输出目录路径，所有任务统一使用该目录（优先于 --no-dated-dir）')
    parser.add_argument('--no-dated-dir', action='store_true', help='不创建日期目录，直接存到 output 目录')
    args = parser.parse_args()
    try:
        out_dir = Path(args.dir) if args.dir else None
        path = download(args.url, args.output, create_dated_dir=not args.no_dated_dir, output_dir=out_dir)
        print(path)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
