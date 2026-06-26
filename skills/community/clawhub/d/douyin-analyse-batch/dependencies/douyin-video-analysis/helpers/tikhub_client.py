#!/usr/bin/env python3
"""
TikHub API 客户端 - 获取视频信息和下载链接
"""
import json
import os
import re
import requests

TIKHUB_API_BASE = "https://api.tikhub.dev"

def load_config():
    config_path = os.path.expanduser("~/.openclaw/config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}

def get_token():
    config = load_config()
    token = config.get("tikhub_api_token")
    if not token:
        raise ValueError("缺少 TikHub API Token，请在 ~/.openclaw/config.json 中配置")
    return token

def get_video_info(aweme_id: str) -> dict:
    """
    通过 aweme_id 获取视频详情（标题、下载链接等）
    """
    token = get_token()
    url = f"{TIKHUB_API_BASE}/api/v1/douyin/web/fetch_one_video"
    params = {"aweme_id": aweme_id, "need_anchor_info": "false"}
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def get_video_url(aweme_id: str) -> str | None:
    """
    通过 aweme_id 获取视频直接播放链接
    """
    try:
        result = get_video_info(aweme_id)
        ad = result.get("data", {}).get("aweme_detail", {})
        if not ad:
            return None
        # 尝试从 stream URL 获取
        video = ad.get("video", {})
        # play_addr 里有 url_list
        play = video.get("play_addr", {}) or video.get("download_addr", {})
        urls = play.get("url_list", []) if play else []
        for u in urls:
            if u and ("v11-cold" in u or "v19" in u or "douyinvod" in u):
                return u
        return urls[0] if urls else None
    except Exception as e:
        print(f"[WARN] get_video_url failed for {aweme_id}: {e}")
        return None

def get_aweme_id_from_topic(keyword: str, token: str) -> list[dict]:
    """
    用话题关键词搜索视频，返回 [{aweme_id, title, item_url}]
    注意：此接口需要付费额度
    """
    url = f"{TIKHUB_API_BASE}/api/v1/douyin/search/fetch_video_search_v2"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"keyword": keyword, "count": 3}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 200:
        return []
    items = data.get("data", {}).get("video_list", [])
    return [
        {"aweme_id": v.get("aweme_id"), "title": v.get("title", ""), "item_url": v.get("play_url", "")}
        for v in items if v.get("aweme_id")
    ]

def get_hot_video_list(page: int = 1, page_size: int = 15, sub_type: int = 1001) -> dict:
    """
    获取视频热榜（含 item_id + item_url 直接下载链接）
    返回 {"item_id": ..., "item_title": ..., "item_url": ..., ...}
    """
    token = get_token()
    url = f"{TIKHUB_API_BASE}/api/v1/douyin/billboard/fetch_hot_total_video_list"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"page": page, "page_size": page_size, "sub_type": sub_type}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 200:
        raise RuntimeError(f"fetch_hot_total_video_list failed: {data.get('message')}")
    # TikHub 返回结构是双层嵌套: data.data.objs
    inner_data = data.get("data", {})
    objs = inner_data.get("data", {}).get("objs", []) if isinstance(inner_data, dict) else []
    return objs

if __name__ == "__main__":
    # 测试
    token = get_token()
    print(f"Token: {token[:10]}...")

    # 测试热榜视频列表
    print("\n=== 测试 fetch_hot_total_video_list ===")
    videos = get_hot_video_list(page=1, page_size=3)
    for v in videos:
        print(f"item_id: {v.get('item_id')}")
        print(f"title: {v.get('item_title', '')[:60]}")
        print(f"item_url: {v.get('item_url', '')[:100]}")
        print()
