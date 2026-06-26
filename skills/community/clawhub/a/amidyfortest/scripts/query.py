#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trip Assistant Query Script

调用 Booking Assistant FastAPI 服务的 /trip/chat/stream 接口，
将响应流式打印到 stdout。

用法:
    python query.py --query "帮我查一下明天北京到上海的机票" \
                    --user-id "your_user_id" \
                    --env prod \
                    --base-url http://host.docker.internal:8763

环境变量（可替代 CLI 参数）:
    BOOKING_API_USER_ID   用户 ID
    BOOKING_API_ENV       环境配置（fat / prod），默认 prod
    BOOKING_API_BASE_URL  服务地址，默认 http://host.docker.internal:8763
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from urllib.parse import urljoin


def main():
    parser = argparse.ArgumentParser(description="Trip Assistant query client")
    parser.add_argument("--query", "-q", required=True, help="用户查询内容")
    parser.add_argument(
        "--user-id",
        default=os.environ.get("BOOKING_API_USER_ID", "624e5b8b3f4a2f4ec566e3d3"),
        help="用户 ID（也可通过 BOOKING_API_USER_ID 环境变量设置）",
    )
    parser.add_argument(
        "--env",
        default=os.environ.get("BOOKING_API_ENV", "prod"),
        choices=["fat", "prod"],
        help="环境配置（默认 prod）",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("BOOKING_API_BASE_URL", "http://host.docker.internal:8763"),
        help="FastAPI 服务地址（默认 http://host.docker.internal:8763）",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=0,
        help="输出字符数上限，超出时截断（默认 4000，设为 0 则不限制）",
    )
    args = parser.parse_args()

    if not args.user_id:
        print("错误：请通过 --user-id 参数或 BOOKING_API_USER_ID 环境变量提供用户 ID", file=sys.stderr)
        sys.exit(1)

    url = urljoin(args.base_url, "/trip/chat/stream")
    payload = {
        "query": args.query,
        "user_id": args.user_id,
        "env": args.env,
    }

    try:
        # 准备请求
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        # 发送请求
        with urllib.request.urlopen(req, timeout=120) as response:
            chunks = []
            char_count = 0
            truncated = False

            # 逐行读取流式响应
            for line in response:
                line = line.decode('utf-8').strip()
                if not line:
                    continue
                if not line.startswith("data: "):
                    continue

                content = line[6:]  # 去掉 "data: " 前缀
                if content == "[DONE]":
                    break
                if content.startswith("[ERROR]"):
                    print(f"\n服务错误：{content}", file=sys.stderr)
                    sys.exit(1)

                if args.max_chars > 0 and char_count + len(content) > args.max_chars:
                    remaining = args.max_chars - char_count
                    if remaining > 0:
                        chunks.append(content[:remaining])
                    truncated = True
                    break

                chunks.append(content)
                char_count += len(content)

        output = "".join(chunks)
        if truncated:
            print(output)
            print(f"\n[输出已截断至前 {args.max_chars} 个字符，如需完整输出请使用 --max-chars 0]")
        else:
            print(output)

    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print(
                f"错误：无法连接到服务 {args.base_url}，请确认 FastAPI 服务已启动",
                file=sys.stderr,
            )
        else:
            print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    except TimeoutError:
        print("错误：请求超时", file=sys.stderr)
        sys.exit(1)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        print(f"错误：HTTP {e.code} - {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
