#!/usr/bin/env python3
"""
抖音视频搜索器 - TikHub API
基于官方文档实现：支持关键词搜索、分页、多种排序和筛选
"""

import requests
import json
import os
import sys
import argparse

# API端点（来自文档）
TIKHUB_SEARCH_URL = "https://api.tikhub.io/api/v1/douyin/search/fetch_general_search_v1"


def load_config():
    """加载配置文件，与douyin-downloader保持一致"""
    config_path = os.path.expanduser("~/.openclaw/config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # 如果没有配置文件，尝试从环境变量读取（备用方案）
    token = os.environ.get("TIKHUB_API_TOKEN")
    if token:
        return {"tikhub_api_token": token}
    # 如果都没有，返回空字典，后续会报错
    return {}


def get_token():
    """获取 TikHub Token"""
    config = load_config()
    token = config.get("tikhub_api_token")
    if not token:
        raise ValueError(
            "❌ 缺少TikHub API Token\n\n"
            "请配置 Token：\n"
            "1. 在 ~/.openclaw/config.json 中添加：\n"
            "   {\"tikhub_api_token\": \"你的Token\"}\n"
            "2. 或设置环境变量 TIKHUB_API_TOKEN"
        )
    return token


def search_videos(
        keyword,
        cursor=0,
        sort_type="0",
        publish_time="0",
        filter_duration="0",
        content_type="0",
        search_id="",
        backtrace="",
        token=None
):
    """
    调用搜索 API
    参数含义（根据文档）：
    - cursor: 分页游标，第一页传0，后续使用返回的 cursor
    - sort_type: 0综合 1最多点赞 2最新发布
    - publish_time: 0不限 1最近一天 7最近一周 180最近半年
    - filter_duration: 0不限 0-1一分钟内 1-5 1-5分钟 5-10000 5分钟以上
    - content_type: 0不限 1视频 2图片 3文章
    - search_id, backtrace: 分页追踪参数，第一页传空字符串
    """
    if token is None:
        token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 严格按照文档示例构建请求体
    payload = {
        "keyword": keyword,
        "cursor": cursor,
        "sort_type": str(sort_type),
        "publish_time": str(publish_time),
        "filter_duration": str(filter_duration),
        "content_type": str(content_type),
        "search_id": search_id,
        "backtrace": backtrace
    }

    try:
        # 文档明确指定使用 POST 方法
        resp = requests.post(TIKHUB_SEARCH_URL, json=payload, headers=headers, timeout=30)
        print(f"DEBUG: status_code={resp.status_code}")
        print(f"DEBUG: response_text={resp.text[:500]}")
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API请求失败: {e}")
    except json.JSONDecodeError:
        raise RuntimeError("API返回非JSON格式")


def format_video_item(item):
    """格式化单个视频信息为可读文本"""
    # 根据文档，结果在 data 列表中，每个 item 包含 type 和 aweme_info
    aweme = item.get("aweme_info", {})
    if not aweme:
        return "（数据格式异常）"
    # print(aweme)
    video_id = aweme.get("aweme_id", "未知ID")
    desc = aweme.get("desc", "无描述")[:50]  # 截断过长描述
    author = aweme.get("author", {})
    author_name = author.get("nickname", "未知作者")

    # 统计信息
    stats = aweme.get("statistics", {})
    play_count = stats.get("play_count", 0)
    digg_count = stats.get("digg_count", 0)

    # 视频时长（毫秒转秒）
    duration_ms = aweme.get("video", {}).get("duration", 0)
    duration_sec = duration_ms // 1000

    # 提取第一个视频播放地址（如果有）
    video_url = ""
    play_addr = aweme.get("video", {}).get("play_addr", {})
    url_list = play_addr.get("url_list", [])
    if url_list:
        video_url = url_list[0]


    return (
        f"📹 ID: {video_id}\n"
        f"📝 标题: {desc}\n"
        f"👤 作者: {author_name}\n"
        f"▶️ 播放: {play_count}  👍 点赞: {digg_count}  ⏱️ 时长: {duration_sec}秒\n"
        f"🔗 播放地址: {video_url}\n"
        f"🔗 分享链接: https://www.douyin.com/video/{video_id}\n"
    )


def format_search_result(data, show_raw=False):
    """格式化整个搜索结果"""
    if show_raw:
        return json.dumps(data, indent=2, ensure_ascii=False)
    print(1111)
    # 根据文档，结果在 data 字段中
    items = data.get("data", []).get("data", [])
    # print(type(items))
    if not items:
        return "没有找到相关视频。"
    print(2222)
    # 提取分页信息（文档中说明返回包含 cursor, search_id, backtrace 用于下一页）
    next_cursor = data.get("cursor", 0)
    has_more = data.get("has_more", False)
    print(333)
    lines = [f"找到 {len(items)} 个视频（下一页游标: {next_cursor}，还有更多: {has_more}）\n"]
    for idx, item in enumerate(items, 1):
        lines.append(f"--- 第 {idx} 个 ---")
        lines.append(format_video_item(item))
    print(444)
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="抖音视频搜索（TikHub）")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("--cursor", type=int, default=0, help="分页游标，默认0")
    parser.add_argument("--sort", choices=["0", "1", "2"], default="0",
                        help="排序: 0综合 1最多点赞 2最新发布")
    parser.add_argument("--publish", choices=["0", "1", "7", "180"], default="0",
                        help="发布时间: 0不限 1一天 7一周 180半年")
    parser.add_argument("--duration", choices=["0", "0-1", "1-5", "5-10000"], default="0",
                        help="时长: 0不限 0-1一分钟内 1-5 1-5分钟 5-10000 5分钟以上")
    parser.add_argument("--type", choices=["0", "1", "2", "3"], default="0",
                        help="内容类型: 0不限 1视频 2图片 3文章")
    parser.add_argument("--search-id", default="", help="分页search_id（通常不需要手动指定）")
    parser.add_argument("--backtrace", default="", help="分页backtrace（通常不需要手动指定）")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON数据")

    args = parser.parse_args()

    try:
        result = search_videos(
            keyword=args.keyword,
            cursor=args.cursor,
            sort_type=args.sort,
            publish_time=args.publish,
            filter_duration=args.duration,
            content_type=args.type,
            search_id=args.search_id,
            backtrace=args.backtrace
        )
        # print(result)
        # print(format_search_result(result, show_raw=args.raw))
        # Use sys.stdout.buffer.write to output UTF-8 directly
        output = format_search_result(result, show_raw=args.raw)
        sys.stdout.buffer.write(output.encode('utf-8'))
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)