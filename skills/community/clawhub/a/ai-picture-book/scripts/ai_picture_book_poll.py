#!/usr/bin/env python3
"""
AI Picture Book - Poll Task
Automatically poll task until completion with progress updates.
"""

import os
import sys
import json
import time
import requests
import argparse
from typing import Dict, Any, Tuple
from urllib.parse import urlparse

STATUS_CODES = {
    0: "in_progress",
    1: "in_progress",
    2: "completed",
    3: "in_progress",
}

BASE_URL = "https://qianfan.baidubce.com/v2"

def resolve_sandbox_url(api_key: str, original_url: str) -> Tuple[str, Dict[str, str]]:
    """若当前在沙盒环境中，将目标 URL 替换为代理 URL，并返回需要附加的 headers。"""
    session_id = os.environ.get("DUMATE_SESSION_ID")
    scheduler_url = os.environ.get("DUMATE_SCHEDULER_URL")

    headers = {
        "Content-Type": "application/json",
    }
    if not session_id or not scheduler_url:
        if not api_key:
            raise ValueError("未设置 API Key，请通过环境变量 BAIDU_API_KEY 设置或使用")
        headers.update({
            "Authorization": f"Bearer {api_key}",
            "X-Appbuilder-From": "openclaw",
        })
        return original_url, headers

    parsed = urlparse(original_url)
    proxy_url = f"{scheduler_url}/api/qianfanproxy{parsed.path}"
    if parsed.query:
        proxy_url += f"?{parsed.query}"

    headers.update({
        "Host": parsed.netloc,
        "X-Dumate-Session-Id": session_id,
        "X-Appbuilder-From": "desktop",
    })
    return proxy_url, headers


def query_task(api_key: str, task_id: str) -> Dict[str, Any]:
    """Query task status."""
    url = f"{BASE_URL}/tools/ai_picture_book/query"
    url, headers = resolve_sandbox_url(api_key, url)
    params = {"task_ids": [task_id]}

    response = requests.post(url, headers=headers, json=params, timeout=5)
    response.raise_for_status()
    result = response.json()

    if "errno" in result and result["errno"] != 0:
        raise RuntimeError(result.get("errmsg", "Unknown error"))

    return result["data"]


def poll_task(api_key: str, task_id: str, max_attempts: int = 20, interval: int = 5):
    """Poll task until completion or timeout.

    Args:
        api_key: Baidu API key
        task_id: Task ID
        max_attempts: Maximum poll attempts (default 20)
        interval: Seconds between polls (default 5)

    Returns:
        Final task data
    """
    data = None
    for attempt in range(max_attempts):
        try:
            data = query_task(api_key, task_id)
            if not data or len(data) == 0:
                print(f"\n✗ No task data returned")
                return data

            status = data[0].get("status")
            result = data[0].get("result", {})
            if result and "video_bos_url" in result:
                result = {"video_bos_url": result["video_bos_url"]}

            if status == 2:
                print("\n" + "=" * 50)
                print("✓ PICTURE BOOK GENERATED SUCCESSFULLY")
                print("=" * 50)
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return data

            elif status in [0, 1, 3]:
                print(f"[{attempt + 1}/{max_attempts}] Processing...")
                time.sleep(interval)

            else:
                print(f"\n✗ Task failed: status={status}")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                return data

        except RuntimeError as e:
            print(f"\n✗ Error: {str(e)}")
            return data
        except Exception as e:
            if attempt == max_attempts - 1:
                print(f"\n✗ Unexpected error: {str(e)}")
                return data
            time.sleep(interval)

    print(f"\n✗ Timeout after {max_attempts * interval} seconds")
    print("Task may still be running. Try querying manually:")
    print(f"  python scripts/ai_picture_book_task_query.py {task_id}")
    return data


def main():
    parser = argparse.ArgumentParser(description="查询AI视频笔记生成任务状态")
    parser.add_argument("--task_id", required=True, help="任务ID")
    parser.add_argument("--max_attempts", type=int, help="最大轮询次数")
    parser.add_argument("--interval", type=int, help="每次轮询间隔（秒）")
    parser.add_argument("--api_key", default=os.environ.get("BAIDU_API_KEY"), help="API Key")
    args = parser.parse_args()
    task_id = args.task_id
    api_key = args.api_key
    max_attempts = args.max_attempts
    interval = args.interval

    # task_id = sys.argv[1]
    max_attempts = max_attempts if max_attempts else 20
    interval = interval if interval else 5

    print(f"Polling task: {task_id}")
    print(f"Max attempts: {max_attempts}, Interval: {interval}s")
    print("-" * 50)

    poll_task(api_key, task_id, max_attempts, interval)


if __name__ == "__main__":
    main()
