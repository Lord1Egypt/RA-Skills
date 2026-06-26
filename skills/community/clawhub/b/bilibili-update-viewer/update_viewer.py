#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站UP主查看器 - 简化版

功能：
- 查看指定UP主的最新视频
- 查看指定UP主的最新动态

使用方法：
    # 查看最新视频
    python update_viewer.py --mid 946974 --videos

    # 查看最新动态
    python update_viewer.py --mid 946974 --dynamics

    # 同时查看视频和动态
    python update_viewer.py --mid 946974 --videos --dynamics
"""

import argparse
import json
import os
import re
import sys

from bilibili_api import BilibiliAPI, format_number, format_timestamp, format_duration

# 用户缓存文件路径（与脚本同目录）
USER_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_cache.json")


def load_user_cache() -> dict:
    """加载本地用户缓存"""
    if os.path.exists(USER_CACHE_FILE):
        try:
            with open(USER_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_user_cache(cache: dict):
    """保存用户缓存到本地 JSON 文件"""
    try:
        with open(USER_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"  [WARNING] 保存用户缓存失败: {e}")


def cache_search_results(keyword: str, users: list):
    """将搜索结果写入缓存（按用户名和 mid 双重索引）"""
    cache = load_user_cache()
    for user in users:
        mid = user.get("mid", 0)
        uname = re.sub(r'<[^>]+>', '', user.get("uname", ""))
        if mid and uname:
            entry = {
                "mid": mid,
                "uname": uname,
                "fans": user.get("fans", 0),
                "videos": user.get("videos", 0),
                "level": user.get("level", 0),
                "usign": user.get("usign", ""),
            }
            # 以用户名（小写）为 key 存储
            cache[uname.lower()] = entry
    save_user_cache(cache)


def lookup_cache(keyword: str) -> list:
    """从缓存中查找用户，支持模糊匹配"""
    cache = load_user_cache()
    keyword_lower = keyword.lower()

    # 精确匹配
    if keyword_lower in cache:
        return [cache[keyword_lower]]

    # mid 精确匹配
    if keyword in cache:
        return [cache[keyword]]

    # 模糊匹配：关键词包含在用户名中
    results = []
    seen_mids = set()
    for key, entry in cache.items():
        if not key.isdigit() and keyword_lower in key:
            mid = entry.get("mid", 0)
            if mid not in seen_mids:
                results.append(entry)
                seen_mids.add(mid)
    return results


def parse_cookies(cookies_str: str) -> dict:
    """解析cookies字符串"""
    result = {}
    for item in cookies_str.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            result[key.strip()] = value.strip()
    return result


def show_update_info(api: BilibiliAPI, mid: int):
    """显示UP主基本信息"""
    try:
        info = api.get_update_info(mid)
        name = info.get("name", "未知")
        sign = info.get("sign", "")
        face = info.get("face", "")
        
        print(f"\n{'='*60}")
        print(f"👤 UP主: {name}")
        print(f"   mid: {mid}")
        if sign:
            print(f"   签名: {sign[:50]}{'...' if len(sign) > 50 else ''}")
        print(f"{'='*60}")
        
        return info
    except Exception as e:
        print(f"[ERROR] 获取UP主信息失败: {e}")
        return None


def show_latest_videos(api: BilibiliAPI, mid: int, count: int = 10):
    """显示最新视频列表"""
    print(f"\n📹 最新视频 (最近{count}个)")
    print("-" * 60)
    
    try:
        data = api.get_update_videos(mid, page=1, page_size=count, order="pubdate")
        videos = data.get("list", {}).get("vlist", [])
        
        if not videos:
            print("  暂无视频")
            return []
        
        for i, video in enumerate(videos, 1):
            title = video.get("title", "")
            bvid = video.get("bvid", "")
            play = video.get("play", 0)
            pubdate = video.get("created", 0)
            length = video.get("length", "")
            comment = video.get("comment", 0)
            
            print(f"\n  {i}. {title}")
            print(f"     📊 播放: {format_number(play)} | 评论: {comment}")
            print(f"     ⏱️  时长: {length} | 发布: {format_timestamp(pubdate)}")
            print(f"     🔗 https://www.bilibili.com/video/{bvid}")
        
        print()
        return videos
        
    except Exception as e:
        print(f"  [ERROR] 获取视频列表失败: {e}")
        return []


def show_latest_dynamics(api: BilibiliAPI, mid: int, count: int = 10):
    """显示最新动态列表"""
    print(f"\n📢 最新动态 (最近{count}条)")
    print("-" * 60)
    
    try:
        data = api.get_update_dynamics(mid)
        items = data.get("items", [])
        
        if not items:
            print("  暂无动态")
            return []
        
        shown = 0
        for item in items:
            if shown >= count:
                break
            
            # 解析动态类型和内容
            dynamic_type = item.get("type", "")
            modules = item.get("modules", {})
            
            # 获取作者信息
            author_module = modules.get("module_author", {})
            pub_time = author_module.get("pub_time", "")
            pub_action = author_module.get("pub_action", "")
            
            # 获取动态内容
            dynamic_module = modules.get("module_dynamic", {})
            desc = dynamic_module.get("desc", {})
            text = desc.get("text", "") if desc else ""
            
            # 获取主体内容（如视频、专栏等）
            major = dynamic_module.get("major", {})
            major_type = major.get("type", "") if major else ""
            
            shown += 1
            print(f"\n  {shown}. [{pub_time}] {pub_action if pub_action else '发布动态'}")
            
            # 根据动态类型显示不同内容
            if dynamic_type == "DYNAMIC_TYPE_AV":
                # 视频动态
                archive = major.get("archive", {})
                title = archive.get("title", "")
                bvid = archive.get("bvid", "")
                play = archive.get("stat", {}).get("play", "")
                
                print(f"     📹 视频: {title}")
                if text:
                    print(f"     💬 {text[:80]}{'...' if len(text) > 80 else ''}")
                print(f"     🔗 https://www.bilibili.com/video/{bvid}")
                
            elif dynamic_type == "DYNAMIC_TYPE_DRAW":
                # 图文动态
                draw = major.get("draw", {})
                items_count = len(draw.get("items", []))
                
                if text:
                    print(f"     💬 {text[:100]}{'...' if len(text) > 100 else ''}")
                if items_count > 0:
                    print(f"     🖼️  包含 {items_count} 张图片")
                    
            elif dynamic_type == "DYNAMIC_TYPE_WORD":
                # 纯文字动态
                if text:
                    print(f"     💬 {text[:150]}{'...' if len(text) > 150 else ''}")
                    
            elif dynamic_type == "DYNAMIC_TYPE_ARTICLE":
                # 专栏文章
                article = major.get("article", {})
                title = article.get("title", "")
                
                print(f"     📝 专栏: {title}")
                if text:
                    print(f"     💬 {text[:80]}{'...' if len(text) > 80 else ''}")
                    
            elif dynamic_type == "DYNAMIC_TYPE_FORWARD":
                # 转发动态
                if text:
                    print(f"     🔄 转发: {text[:100]}{'...' if len(text) > 100 else ''}")
                    
            else:
                # 其他类型
                if text:
                    print(f"     💬 {text[:100]}{'...' if len(text) > 100 else ''}")
                else:
                    print(f"     📌 类型: {dynamic_type}")
        
        print()
        return items[:count]
        
    except Exception as e:
        print(f"  [ERROR] 获取动态列表失败: {e}")
        return []


def _print_user_list(users: list, source: str = ""):
    """统一格式化打印用户列表"""
    for i, user in enumerate(users, 1):
        mid = user.get("mid", 0)
        uname = re.sub(r'<[^>]+>', '', user.get("uname", ""))
        usign = user.get("usign", "")
        fans = user.get("fans", 0)
        videos = user.get("videos", 0)
        level = user.get("level", 0)

        print(f"\n  {i}. {uname}")
        print(f"     🆔 mid: {mid}")
        print(f"     👥 粉丝: {format_number(fans)} | 视频: {videos} | 等级: Lv{level}")
        if usign:
            print(f"     📝 签名: {usign[:60]}{'...' if len(usign) > 60 else ''}")
        print(f"     🔗 https://space.bilibili.com/{mid}")
    print()


def show_search_results(api: BilibiliAPI, keyword: str, count: int = 10):
    """搜索用户并显示结果（优先使用本地缓存）"""
    print(f"\n🔍 搜索用户: \"{keyword}\"")
    print("-" * 60)

    # 先查本地缓存
    cached = lookup_cache(keyword)
    if cached:
        print(f"  📦 命中本地缓存（共 {len(cached)} 条）")
        _print_user_list(cached[:count])
        return cached[:count]

    # 缓存未命中，调用 API 搜索
    try:
        data = api.search_user(keyword, page=1, page_size=count)
        users = data.get("result", [])

        if not users:
            print("  未找到匹配的用户")
            return []

        # 写入缓存
        cache_search_results(keyword, users)

        _print_user_list(users)
        return users

    except Exception as e:
        print(f"  [ERROR] 搜索用户失败: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description="B站UP主查看器 - 查看指定UP主的最新视频和动态",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 根据用户名搜索UP主（获取 mid）
  python update_viewer.py --search "影视飓风"

  # 查看UP主最新视频
  python update_viewer.py --mid 946974 --videos
  
  # 查看UP主最新动态
  python update_viewer.py --mid 946974 --dynamics
  
  # 同时查看视频和动态
  python update_viewer.py --mid 946974 --videos --dynamics
  
  # 指定显示数量
  python update_viewer.py --mid 946974 --videos --count 5
        """
    )
    
    parser.add_argument("--mid", type=int, help="UP主的 mid（用户ID）")
    parser.add_argument("--search", "-s", type=str, help="根据用户名搜索UP主（获取 mid）")
    parser.add_argument("--videos", "-v", action="store_true", help="显示最新视频")
    parser.add_argument("--dynamics", "-d", action="store_true", help="显示最新动态")
    parser.add_argument("--count", "-n", type=int, default=3, help="显示数量（默认3）")
    
    args = parser.parse_args()

    # 必须提供 --mid 或 --search 其中之一
    if not args.mid and not args.search:
        parser.error("必须提供 --mid 或 --search 参数")
    
    # 获取 cookies
    cookies_str = os.environ.get('BILIBILI_COOKIES', '')
    if not cookies_str:
        print("错误：必须提供 --cookies 参数或设置 BILIBILI_COOKIES 环境变量")
        print("\n获取方法：")
        print("  1. 登录 B站")
        print("  2. F12 打开开发者工具 → Network 选项卡")
        print("  3. 刷新页面，找到任意请求")
        print("  4. 复制 Request Headers 中的 Cookie 值")
        sys.exit(1)
    
    # 解析 cookies
    all_cookies = parse_cookies(cookies_str)
    
    # 创建 API 客户端
    api = BilibiliAPI(all_cookies=all_cookies)

    # 搜索模式
    if args.search:
        show_search_results(api, args.search, args.count)
        sys.exit(0)
    
    # 如果没有指定任何显示选项，默认显示视频
    if not args.videos and not args.dynamics:
        args.videos = True
    
    # 显示UP主信息
    info = show_update_info(api, args.mid)
    if not info:
        sys.exit(1)
    
    # 显示视频
    if args.videos:
        show_latest_videos(api, args.mid, args.count)
    
    # 显示动态
    if args.dynamics:
        show_latest_dynamics(api, args.mid, args.count)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
