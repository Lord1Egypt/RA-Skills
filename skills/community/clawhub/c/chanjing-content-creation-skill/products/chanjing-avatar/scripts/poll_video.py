#!/usr/bin/env python3
"""
轮询视频合成任务状态，直到完成或失败。与 chanjing-credentials-guard 使用同一配置文件获取 Token。
用法: poll_video.py --id <视频任务id> [--interval 10]
输出: 成功时打印 video_url（一行），失败时打印错误到 stderr 并 exit 1

注意：视频合成（create_video.py）的状态码与对口型（video_lip_sync）不同！
  视频合成: 10=生成中, 30=成功, 4X=参数异常, 5X=服务异常
  对口型:   0=待处理, 10=生成中, 20=成功, 30=失败
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _auth import resolve_chanjing_access_token

API_BASE = __import__("os").environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")


def main():
    parser = argparse.ArgumentParser(description="轮询视频合成任务直到完成")
    parser.add_argument("--id", required=True, help="视频任务 ID（来自 create_video.py）")
    parser.add_argument("--interval", type=int, default=10, help="轮询间隔秒数，默认 10")
    args = parser.parse_args()

    token, err = resolve_chanjing_access_token()
    if err:
        print(err, file=sys.stderr)
        sys.exit(1)

    url = f"{API_BASE}/open/v1/video?id={urllib.parse.quote(args.id)}"

    while True:
        req = urllib.request.Request(url, headers={"access_token": token}, method="GET")
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))

        if body.get("code") != 0:
            print(body.get("msg", body), file=sys.stderr)
            sys.exit(1)

        data = body.get("data", {})
        status = data.get("status")
        progress = data.get("progress", 0)

        print(f"status={status} progress={progress}%", file=sys.stderr)

        if status == 30:
            video_url = data.get("video_url")
            if video_url:
                print(video_url)
                return 0
            print("任务成功但无 video_url", file=sys.stderr)
            sys.exit(1)

        if status is not None and status >= 40:
            msg = data.get("msg", "unknown")
            print(f"任务异常 (status={status}): {msg}", file=sys.stderr)
            sys.exit(1)

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
