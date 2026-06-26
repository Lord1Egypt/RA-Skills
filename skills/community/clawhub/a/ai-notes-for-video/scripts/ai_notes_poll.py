#!/usr/bin/env python3
"""
AI Video Notes - Poll Task
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
    10000: "processing",
    10002: "completed",
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
    url = f"{BASE_URL}/tools/ai_note/query"
    url, headers = resolve_sandbox_url(api_key, url)
    params = {"task_id": task_id}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    result = response.json()
    return result


def poll_task(api_key: str, task_id: str, max_attempts: int = 20, interval: int = 3):
    """Poll task until completion or timeout.

    Args:
        api_key: Baidu API key
        task_id: Task ID
        max_attempts: Maximum poll attempts (default 20)
        interval: Seconds between polls (default 3)

    Returns:
        Final task data
    """
    data = None
    for attempt in range(max_attempts):
        try:
            data = query_task(api_key, task_id)
            if "code" in data:
                raise RuntimeError(result["detail"])
            if "errno" in data and data["errno"] == 10000:
                errno = data["errno"]
                error_msg = data["show_msg"]
                print(f"[{attempt + 1}/{max_attempts}] Processing...(task status code: {errno}, message: {error_msg})")
                time.sleep(interval)
                continue
            if "errno" in data and data["errno"] != 0:
                raise RuntimeError(data.get("show_msg", "Unknown error"))
            data = data.get("data", {})
            ai_notes_list = data.get("list", [])
            status_code = 0
            for note in ai_notes_list:
                status_code = note.get("detail", {}).get("status", 0)
                if status_code != 10002:
                    break

            if status_code == 10002:
                for note in data.get("list", []):
                    tpl_no = note.get("tpl_no")
                    if tpl_no == "1":
                        print("\n" + "=" * 50)
                        print("✓ 文稿笔记笔记生成成功，如下")
                        print("=" * 50)
                        for content in note.get("detail", {}).get("contents", []):
                            print(content)

                    if tpl_no == "2":
                        print("\n" + "=" * 50)
                        print("✓ 大纲笔记笔记生成成功，如下")
                        print("=" * 50)
                        for content in note.get("detail", {}).get("contents", []):
                            print(content)
                    if tpl_no == "3":
                        print("\n" + "=" * 50)
                        print("✓ 图文笔记笔记生成成功，如下")
                        print("=" * 50)
                        for content in note.get("detail", {}).get("contents", []):
                            print(content)
                return data

            elif status_code == 10000:
                print(f"[{attempt + 1}/{max_attempts}] Processing...")
                time.sleep(interval)
                continue
            else:
                print(f"\n✗ Task failed, with status code: {status_code}")
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
    print(f"  python scripts/ai_notes_task_query.py {task_id}")
    return data


def main():
    parser = argparse.ArgumentParser(description="轮询AI视频笔记生成任务状态直到完成")
    parser.add_argument("--task_id", required=True, help="任务ID")
    parser.add_argument("--api_key", default=os.environ.get("BAIDU_API_KEY"), help="API Key")
    parser.add_argument("--max_attempts", type=int, help="最大轮询次数")
    parser.add_argument("--interval", type=int, help="每次轮询间隔（秒）")
    args = parser.parse_args()
    task_id = args.task_id
    api_key = args.api_key
    max_attempts = args.max_attempts
    interval = args.interval
    max_attempts = max_attempts if max_attempts else 20
    interval = interval if interval else 3

    print(f"Polling task: {task_id}")
    print(f"Max attempts: {max_attempts}, Interval: {interval}s")
    print("-" * 50)

    poll_task(api_key, task_id, max_attempts, interval)


if __name__ == "__main__":
    main()
