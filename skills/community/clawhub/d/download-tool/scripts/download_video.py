#!/usr/bin/env python3
"""
视频下载工具 - 支持 YouTube、TikTok、小红书、抖音等平台
"""

import requests
import json
import os
import re
import sys
import time

# 默认配置
DEFAULT_BASE_URL = "https://www.datamass.cn/ai-back"
DEFAULT_POLL_INTERVAL = 5  # 轮询间隔（秒）
DEFAULT_TIMEOUT = 1800  # 超时时间（秒），30分钟


def load_config():
    """加载配置文件"""
    config_path = os.path.expanduser("~/.openclaw/config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def get_api_key(config=None):
    """获取 API Key"""
    if config is None:
        config = load_config()

    api_key = config.get("download_tool_api_key")
    if not api_key:
        raise ValueError(
            "❌ 缺少 API Key\n\n"
            "请先配置：\n"
            "1. 登录系统创建 API Key\n"
            "2. 在 ~/.openclaw/config.json 中添加:\n"
            '   {"download_tool_api_key": "您的 API Key"}'
        )
    return api_key


def get_base_url(config=None):
    """获取 API 基础 URL"""
    if config is None:
        config = load_config()
    return config.get("download_tool_base_url", DEFAULT_BASE_URL)


def extract_url(text):
    """从文本中提取 URL"""
    if not text:
        return None

    url_pattern = r'(https?://[^\s<>"\']+)'
    match = re.search(url_pattern, text)
    if match:
        return match.group(1)
    return None


def create_download_task(url, api_key, base_url):
    """
    创建下载任务

    Args:
        url: 视频 URL
        api_key: API Key
        base_url: API 基础 URL

    Returns:
        str: 任务 ID
    """
    endpoint = f"{base_url}/sys/openapi/download"

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }

    data = {
        "url": url
    }

    response = requests.post(endpoint, json=data, headers=headers, timeout=30)
    response.raise_for_status()

    result = response.json()

    if not result.get("success"):
        raise ValueError(f"创建下载任务失败：{result.get('message')}")

    task_id = result.get("result", {}).get("task_id")
    if not task_id:
        raise ValueError("未获取到任务 ID")

    return task_id


def check_download_status(task_id, api_key, base_url):
    """
    查询下载状态

    Args:
        task_id: 任务 ID
        api_key: API Key
        base_url: API 基础 URL

    Returns:
        dict: 下载状态信息
    """
    endpoint = f"{base_url}/sys/openapi/download/status/{task_id}"

    headers = {
        "X-Api-Key": api_key
    }

    response = requests.get(endpoint, headers=headers, timeout=30)
    response.raise_for_status()

    result = response.json()

    if not result.get("success"):
        raise ValueError(f"查询状态失败：{result.get('message')}")

    return result.get("result", {})


def wait_for_completion(task_id, api_key, base_url, timeout=DEFAULT_TIMEOUT, poll_interval=DEFAULT_POLL_INTERVAL):
    """
    等待下载完成

    Args:
        task_id: 任务 ID
        api_key: API Key
        base_url: API 基础 URL
        timeout: 超时时间（秒）
        poll_interval: 轮询间隔（秒）

    Returns:
        dict: 下载结果
    """
    start_time = time.time()

    print(f"\n📥 任务 ID: {task_id}")
    print("⏳ 等待下载完成...")

    while True:
        elapsed = time.time() - start_time

        if elapsed > timeout:
            raise ValueError(f"下载超时（{timeout}秒）")

        status_info = check_download_status(task_id, api_key, base_url)
        status = status_info.get("status", 0)
        progress = status_info.get("progress", "未知")
        message = status_info.get("message", "")

        # 状态码：0-等待，1-下载中，2-完成，3-失败
        status_map = {
            0: "⏳ 等待下载",
            1: "📥 下载中",
            2: "✅ 下载完成",
            3: "❌ 下载失败"
        }

        status_text = status_map.get(status, f"未知状态 ({status})")
        print(f"  状态：{status_text} | 进度：{progress} | {message}")

        if status == 2:
            # 下载完成
            oss_url = status_info.get("oss_url")
            if oss_url:
                print(f"\n🎉 下载成功！")
                print(f"📁 OSS 地址：{oss_url}")
                return {
                    "success": True,
                    "task_id": task_id,
                    "oss_url": oss_url,
                    "url": status_info.get("url"),
                    "progress": progress,
                    "message": message
                }
            else:
                raise ValueError("下载完成但未返回 OSS 地址")

        elif status == 3:
            # 下载失败
            raise ValueError(f"下载失败：{message}")

        # 等待下一次轮询
        time.sleep(poll_interval)


def download_video(user_input, timeout=DEFAULT_TIMEOUT, poll_interval=DEFAULT_POLL_INTERVAL):
    """
    下载视频（完整流程）

    Args:
        user_input: 用户输入（URL 或包含 URL 的文本）
        timeout: 超时时间（秒）
        poll_interval: 轮询间隔（秒）

    Returns:
        dict: 下载结果
    """
    # 加载配置
    config = load_config()
    api_key = get_api_key(config)
    base_url = get_base_url(config)

    # 提取 URL
    url = extract_url(user_input)
    if not url:
        raise ValueError(f"无法从输入中提取有效的 URL: {user_input}")

    print(f"🔗 检测到视频链接：{url}")
    print("🚀 开始创建下载任务...")

    # 创建下载任务
    task_id = create_download_task(url, api_key, base_url)

    # 等待下载完成
    result = wait_for_completion(task_id, api_key, base_url, timeout, poll_interval)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
视频下载工具 - 支持 YouTube、TikTok、小红书、抖音等
====================================================

用法:
  python download_video.py "视频 URL"
  python download_video.py "视频 URL" --timeout=600 --poll=10

参数:
  --timeout=秒数     设置超时时间（默认 1800 秒 / 30分钟）
  --poll=秒数        设置轮询间隔（默认 5 秒）

示例:
  python download_video.py "https://www.youtube.com/watch?v=xxxxx"
  python download_video.py "https://www.douyin.com/video/7318234567890123456"
  python download_video.py "https://www.tiktok.com/@user/video/1234567890"
  python download_video.py "https://www.xiaohongshu.com/discovery/item/xxxxx"

配置:
  首次使用需要在 ~/.openclaw/config.json 中配置:
  {
    "download_tool_api_key": "您的 API Key"
  }

获取 API Key:
  1. 访问 https://www.datamass.cn
  2. 注册用户，登录，创建 API Key
  3. 复制生成的 API Key 到配置文件中
""")
        sys.exit(1)

    user_input = sys.argv[1]

    # 解析可选参数
    timeout = DEFAULT_TIMEOUT
    poll_interval = DEFAULT_POLL_INTERVAL

    for arg in sys.argv[2:]:
        if arg.startswith("--timeout="):
            try:
                timeout = int(arg.split("=")[1])
            except ValueError:
                pass
        elif arg.startswith("--poll="):
            try:
                poll_interval = int(arg.split("=")[1])
            except ValueError:
                pass

    try:
        result = download_video(user_input, timeout, poll_interval)
        print(f"\n📋 结果：{json.dumps(result, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        sys.exit(1)
