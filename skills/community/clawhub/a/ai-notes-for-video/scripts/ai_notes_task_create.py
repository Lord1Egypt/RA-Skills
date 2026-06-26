#!/usr/bin/env python3
"""
AI Video Notes - Create Task
Submit a video URL for AI note generation.
"""

import os
import sys
import json
import requests
import argparse
from typing import Dict, Any, Tuple
from urllib.parse import urlparse

BASE_URL = "https://qianfan.baidubce.com/v2"


# ── 工具函数 ──────────────────────────────────────────────────────────────────
def _normalize_video_url(api_key, value: str) -> str:
    """
    转换本地路径为网络
    """
    if not value:
        return value
    if not value.startswith(("http://", "https://")):
        if not os.path.exists(value):
            raise FileNotFoundError(f"视频文件不存在: {value}")
        value = upload_video_to_bos(api_key, value)
    return value


def upload_video_to_bos(api_key: str, file_path: str) -> str:
    """
    上传视频文件到 BOS，并返回下载路径

    Args:
        api_key: BCE v3 认证 token
        file_path: 本地视频文件路径

    Returns:
        BOS 下载路径
    """
    url, headers = resolve_sandbox_url(api_key, "https://appbuilder.baidu.com/v2/tools/bos/upload")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Appbuilder-From": "openclaw",
    }
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        response = requests.post(url, headers=headers, files=files)

    response.raise_for_status()
    result = response.json()

    if result.get("code") is not None and result.get("code") != "0":
        raise RuntimeError(result.get("detail", result.get("message", "Upload failed")))

    # 返回下载路径
    return result.get("data", {}).get("downloadUrl")


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


def create_note_task(api_key: str, video_url: str) -> Dict[str, Any]:
    """Create an AI note generation task.

    Args:
        api_key: Baidu API key
        video_url: Public video URL

    Returns:
        Task data with task_id

    Raises:
        RuntimeError: If API returns error
    """
    url, headers = resolve_sandbox_url(api_key, f"{BASE_URL}/tools/ai_note/task_create")
    data = {"url": video_url}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        if "code" in result:
            raise RuntimeError(result.get("detail", "API error"))
        if "errno" in result and result["errno"] != 0:
            raise RuntimeError(result.get("errmsg", "Unknown error"))

        return result["data"]

    except requests.exceptions.Timeout:
        raise RuntimeError("Request timeout. Video URL may be inaccessible.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="创建AI视频笔记任务")
    parser.add_argument("--video_url", required=True, help="本地视频路径或视频链接")
    parser.add_argument("--api_key", default=os.environ.get("BAIDU_API_KEY"), help="API Key")

    args = parser.parse_args()
    video_url = args.video_url
    api_key = args.api_key
    try:
        video_url = _normalize_video_url(api_key, video_url)
        task_data = create_note_task(api_key, video_url)
        print(json.dumps({
            "status": "success",
            "message": "Task created successfully",
            "task_id": task_data.get("task_id"),
            "next_step": f"Query task status: python ai_notes_task_query.py {task_data.get('task_id')}"
        }, indent=2))

    except RuntimeError as e:
        print(json.dumps({
            "status": "error",
            "error": str(e)
        }, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
