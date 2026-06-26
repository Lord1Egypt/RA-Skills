#!/usr/bin/env python3
"""
FxTwitter Extract - 从 X (Twitter) 提取内容的脚本
使用 FxTwitter API (https://api.fxtwitter.com)

支持：
- 提取单个推文
- 提取推文线程
- 提取用户资料
- 支持文本、图片、视频、投票等

API 文档：https://docs.fxtwitter.com/
GitHub: https://github.com/FxEmbed/FxEmbed
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

# API 基础 URL
API_BASE = "https://api.fxtwitter.com"

# 必需的用户代理
USER_AGENT = "FxTwitterExtract/1.0 (+https://github.com/FxEmbed/FxEmbed)"


def make_request(endpoint: str) -> Dict[str, Any]:
    """
    向 FxTwitter API 发送请求
    
    Args:
        endpoint: API 端点（如 /2/status/123456）
    
    Returns:
        API 响应字典
    """
    url = f"{API_BASE}{endpoint}"
    
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {
            "error": f"HTTP Error {e.code}",
            "message": e.read().decode('utf-8') if e.fp else str(e),
            "code": e.code
        }
    except urllib.error.URLError as e:
        return {
            "error": "Network Error",
            "message": str(e.reason),
            "code": 0
        }
    except Exception as e:
        return {
            "error": "Unknown Error",
            "message": str(e),
            "code": 0
        }


def extract_status(status_id: str, include_thread: bool = False) -> Dict[str, Any]:
    """
    提取单个推文内容
    
    Args:
        status_id: 推文 ID
        include_thread: 是否包含整个线程
    
    Returns:
        提取的推文数据
    """
    endpoint = f"/2/thread/{status_id}" if include_thread else f"/2/status/{status_id}"
    return make_request(endpoint)


def extract_profile(handle: str) -> Dict[str, Any]:
    """
    提取用户资料
    
    Args:
        handle: 用户名（不含 @）
    
    Returns:
        用户资料数据
    """
    return make_request(f"/2/profile/{handle}")


def format_status(data: Dict[str, Any]) -> str:
    """
    格式化推文数据为可读文本
    
    Args:
        data: API 响应数据
    
    Returns:
        格式化的文本
    """
    if data.get("code") != 200:
        return f"❌ 错误：{data.get('message', '未知错误')} (代码：{data.get('code')})"
    
    result = []
    
    # 作者信息
    author = data.get("author", {})
    if author:
        result.append(f"👤 {author.get('name', 'Unknown')} (@{author.get('screen_name', 'unknown')})")
    
    # 推文文本
    status = data.get("status", {})
    if status:
        text = status.get("text", "")
        if text:
            result.append(f"\n📝 {text}")
        
        # 创建时间
        created = status.get("created_at", "")
        if created:
            result.append(f"\n🕐 {created}")
        
        # 统计数据
        stats = []
        if status.get("replies", 0):
            stats.append(f"💬 {status['replies']}")
        if status.get("retweets", 0):
            stats.append(f"🔁 {status['retweets']}")
        if status.get("likes", 0):
            stats.append(f"❤️ {status['likes']}")
        if status.get("views", 0):
            stats.append(f"👁️ {status['views']}")
        
        if stats:
            result.append(f"\n📊 {' | '.join(stats)}")
        
        # 媒体
        media = status.get("media", {})
        if media:
            result.append("\n📎 媒体:")
            for photo in media.get("photos", []):
                result.append(f"  🖼️ {photo.get('url', '')}")
            for video in media.get("videos", []):
                result.append(f"  🎥 {video.get('url', '')}")
        
        # 投票
        poll = status.get("poll", {})
        if poll:
            result.append("\n📊 投票:")
            for option in poll.get("options", []):
                result.append(f"  - {option.get('label', '')}: {option.get('votes', 0)} 票")
    
    # 线程
    thread = data.get("thread", [])
    if thread and len(thread) > 1:
        result.append(f"\n🧵 线程：共 {len(thread)} 条推文")
    
    return "\n".join(result)


def format_profile(data: Dict[str, Any]) -> str:
    """
    格式化用户资料为可读文本
    
    Args:
        data: API 响应数据
    
    Returns:
        格式化的文本
    """
    if data.get("code") != 200:
        return f"❌ 错误：{data.get('message', '未知错误')} (代码：{data.get('code')})"
    
    user = data.get("user", {})
    if not user:
        return "❌ 未找到用户"
    
    result = [
        f"👤 {user.get('name', 'Unknown')} (@{user.get('screen_name', 'unknown')})",
        f"🔗 {user.get('url', '')}",
    ]
    
    if user.get("description"):
        result.append(f"📝 {user['description']}")
    
    result.append(f"\n📊 统计:")
    result.append(f"  关注者：{user.get('followers', 0):,}")
    result.append(f"  关注中：{user.get('following', 0):,}")
    result.append(f"  推文数：{user.get('tweets', 0):,}")
    result.append(f"  喜欢数：{user.get('likes', 0):,}")
    result.append(f"  媒体数：{user.get('media_count', 0):,}")
    
    if user.get("location"):
        result.append(f"\n📍 {user['location']}")
    
    if user.get("joined"):
        result.append(f"🕐 加入时间：{user['joined']}")
    
    if user.get("verification", {}).get("verified"):
        result.append("\n✅ 已认证")
    
    return "\n".join(result)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法:")
        print("  python fxtwitter_extract.py status <推文 ID> [--thread]")
        print("  python fxtwitter_extract.py profile <用户名>")
        print("  python fxtwitter_extract.py url <X 文章 URL>")
        print("\n示例:")
        print("  python fxtwitter_extract.py status 1234567890")
        print("  python fxtwitter_extract.py profile elonmusk")
        print("  python fxtwitter_extract.py url https://x.com/elonmusk/status/1234567890")
        print("\n选项:")
        print("  --json    输出原始 JSON")
        print("  --thread  包含整个线程")
        sys.exit(1)
    
    command = sys.argv[1]
    include_thread = "--thread" in sys.argv
    output_json = "--json" in sys.argv
    
    if command == "status":
        if len(sys.argv) < 3:
            print("❌ 错误：请提供推文 ID")
            sys.exit(1)
        status_id = sys.argv[2]
        data = extract_status(status_id, include_thread)
        
        if output_json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(format_status(data))
    
    elif command == "profile":
        if len(sys.argv) < 3:
            print("❌ 错误：请提供用户名")
            sys.exit(1)
        handle = sys.argv[2].lstrip('@')
        data = extract_profile(handle)
        
        if output_json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(format_profile(data))
    
    elif command == "url":
        if len(sys.argv) < 3:
            print("❌ 错误：请提供 X 文章 URL")
            sys.exit(1)
        
        url = sys.argv[2]
        # 从 URL 提取推文 ID
        # 支持格式：
        # - https://x.com/<user>/status/<id>
        # - https://twitter.com/<user>/status/<id>
        # - https://fxtwitter.com/<user>/status/<id>
        
        import re
        match = re.search(r'/status/(\d+)', url)
        if not match:
            print("❌ 错误：无法从 URL 中提取推文 ID")
            sys.exit(1)
        
        status_id = match.group(1)
        data = extract_status(status_id, include_thread)
        
        if output_json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(format_status(data))
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
