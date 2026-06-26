#!/usr/bin/env python3
"""
上传视频合成所需文件并轮询直到就绪，最后输出 file_id。
与 chanjing-credentials-guard 使用同一配置文件获取 Token。
用法:
  upload_file --service make_video_audio --file /path/to/input.wav
  upload_file --service make_video_background --file /path/to/bg.png
输出: file_id（一行）或错误到 stderr
"""
import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_ROOT / "common"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _auth import resolve_chanjing_access_token
from file_upload import upload_local_file_via_chanjing

FILE_READY_STATUSES = {1}
FILE_FAILED_STATUSES = {98, 99, 100}
POLL_INTERVAL_DEFAULT = 5
POLL_TIMEOUT_DEFAULT = 300


def main():
    parser = argparse.ArgumentParser(description="上传视频合成文件并轮询直到就绪，返回 file_id")
    parser.add_argument(
        "--service",
        required=True,
        choices=["make_video_audio", "make_video_background", "ai_creation"],
        help="文件用途：音频、背景素材或 AI 创作",
    )
    parser.add_argument("--file", required=True, help="本地文件路径")
    parser.add_argument("--poll-interval", type=int, default=POLL_INTERVAL_DEFAULT, help="轮询间隔秒数")
    parser.add_argument("--poll-timeout", type=int, default=POLL_TIMEOUT_DEFAULT, help="轮询超时秒数")
    args = parser.parse_args()

    path = Path(args.file)
    token, err = resolve_chanjing_access_token()
    if err:
        print(err, file=sys.stderr)
        sys.exit(1)

    file_id, up_err = upload_local_file_via_chanjing(
        token,
        path,
        args.service,
        poll_interval=float(args.poll_interval),
        poll_timeout=float(args.poll_timeout),
        ready_statuses=FILE_READY_STATUSES,
        failed_statuses=FILE_FAILED_STATUSES,
        pending_statuses=None,
    )
    if up_err:
        print(up_err, file=sys.stderr)
        sys.exit(1)
    print(file_id)


if __name__ == "__main__":
    main()
