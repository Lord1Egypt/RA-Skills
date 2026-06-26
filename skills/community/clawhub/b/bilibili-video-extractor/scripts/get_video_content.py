#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站视频内容提取脚本 - 优化版
功能: 提取视频元数据、简介、弹幕、评论，支持多种模式
"""

import argparse
import json
import re
import sys
import time
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import requests

# 全局缓存目录
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache')
os.makedirs(CACHE_DIR, exist_ok=True)


class BilibiliExtractor:
    """B站视频内容提取器"""

    def __init__(self, use_cache: bool = True, cache_ttl: int = 86400):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com"
        })
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl  # 缓存有效期（秒）

    def _get_cache_path(self, video_id: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(CACHE_DIR, f"{video_id}.json")

    def _read_cache(self, video_id: str) -> Optional[Dict]:
        """读取缓存"""
        if not self.use_cache:
            return None

        cache_path = self._get_cache_path(video_id)
        if not os.path.exists(cache_path):
            return None

        # 检查是否过期
        if time.time() - os.path.getmtime(cache_path) > self.cache_ttl:
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def _write_cache(self, video_id: str, data: Dict) -> None:
        """写入缓存"""
        if not self.use_cache:
            return

        cache_path = self._get_cache_path(video_id)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def extract_video_id(self, url: str) -> Optional[str]:
        """从B站链接中提取视频ID"""
        # 处理短链接
        if "b23.tv" in url:
            try:
                response = self.session.head(url, allow_redirects=True, timeout=10)
                url = response.url
            except Exception as e:
                print(f"[警告] 无法解析短链接: {e}", file=sys.stderr)
                return None

        # 提取BV号
        bv_match = re.search(r'BV[a-zA-Z0-9]{10}', url)
        if bv_match:
            return bv_match.group(0)

        # 提取AV号
        av_match = re.search(r'av(\d+)', url)
        if av_match:
            return f"av{av_match.group(1)}"

        return None

    def get_video_info(self, video_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """获取视频基本信息"""
        # 尝试从缓存读取
        if not force_refresh:
            cached = self._read_cache(video_id)
            if cached and 'info' in cached:
                print(f"[缓存] 使用缓存数据: {video_id}")
                return cached['info']

        # 构建API URL
        if video_id.startswith("BV"):
            api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={video_id}"
        else:
            aid = video_id.replace("av", "")
            api_url = f"https://api.bilibili.com/x/web-interface/view?aid={aid}"

        try:
            response = self.session.get(api_url, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get("code") != 0:
                raise Exception(f"API错误: {data.get('message')}")

            video_data = data["data"]

            # 格式化时间
            pubdate = video_data.get("pubdate", 0)
            pubdate_str = datetime.fromtimestamp(pubdate).strftime("%Y-%m-%d %H:%M") if pubdate else "未知"

            result = {
                "bvid": video_data.get("bvid"),
                "aid": video_data.get("aid"),
                "title": video_data.get("title"),
                "desc": video_data.get("desc"),
                "owner": {
                    "name": video_data.get("owner", {}).get("name"),
                    "mid": video_data.get("owner", {}).get("mid"),
                    "face": video_data.get("owner", {}).get("face")
                },
                "stat": video_data.get("stat", {}),
                "duration": video_data.get("duration"),
                "pubdate": pubdate,
                "pubdate_str": pubdate_str,
                "pages": video_data.get("pages", []),
                "tname": video_data.get("tname"),  # 视频分区
                "tags": self._extract_tags(video_data)
            }

            return result

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")

    def _extract_tags(self, video_data: Dict) -> List[str]:
        """提取视频标签"""
        tags = video_data.get("tags", [])
        if isinstance(tags, list):
            return [tag.get("tag_name", "") for tag in tags if tag.get("tag_name")]
        return []

    def get_danmaku(self, video_id: str, pages: str = "first") -> List[Dict]:
        """获取视频弹幕

        Args:
            video_id: 视频ID
            pages: 获取模式 - "first"(仅第一P), "all"(全部P)
        """
        video_info = self.get_video_info(video_id)
        pages_list = video_info.get("pages", [])

        if not pages_list:
            return []

        danmaku_list = []
        if pages == "first":
            pages_to_fetch = [pages_list[0]]
        else:
            pages_to_fetch = pages_list

        for page in pages_to_fetch:
            cid = page.get("cid")
            page_title = page.get("part", f"P{page.get('page', 1)}")

            try:
                api_url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
                response = self.session.get(api_url, timeout=15)
                response.raise_for_status()

                # 解析XML格式弹幕
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)

                for d in root.findall("d"):
                    p_attrs = d.get("p", "").split(",")
                    if len(p_attrs) >= 5 and d.text:
                        danmaku_list.append({
                            "time": float(p_attrs[0]),
                            "text": d.text.strip(),
                            "type": int(p_attrs[1]) if len(p_attrs) > 1 else 1,
                            "color": p_attrs[2] if len(p_attrs) > 2 else "16777215",
                            "timestamp": int(p_attrs[4]) if len(p_attrs) > 4 else 0,
                            "page": page_title
                        })

                time.sleep(0.3)  # 避免请求过快

            except Exception as e:
                print(f"[警告] 获取 {page_title} 弹幕失败: {e}", file=sys.stderr)
                continue

        # 按时间排序
        danmaku_list.sort(key=lambda x: x["time"])
        return danmaku_list[:1000]  # 限制数量

    def get_comments(self, video_id: str, limit: int = 50) -> List[Dict]:
        """获取视频热门评论"""
        # 先获取aid
        video_info = self.get_video_info(video_id)
        aid = video_info.get("aid")

        if not aid:
            return []

        api_url = f"https://api.bilibili.com/x/v2/reply?type=1&oid={aid}&mode=3&ps={limit}"

        try:
            response = self.session.get(api_url, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get("code") != 0:
                return []

            replies = data.get("data", {}).get("replies", []) or []

            comments = []
            for reply in replies[:limit]:
                comments.append({
                    "id": reply.get("rpid"),
                    "uid": reply.get("member", {}).get("uname"),
                    "content": reply.get("content", {}).get("message", ""),
                    "like": reply.get("like", 0),
                    "ctime": reply.get("ctime"),
                    "reply_count": reply.get("rcount", 0)
                })

            return comments

        except Exception as e:
            print(f"[警告] 获取评论失败: {e}", file=sys.stderr)
            return []

    def get_summary(self, video_id: str) -> Dict[str, Any]:
        """获取摘要信息（最快速模式）"""
        info = self.get_video_info(video_id)

        return {
            "bvid": info.get("bvid"),
            "title": info.get("title"),
            "owner": info.get("owner", {}).get("name"),
            "duration": self._format_duration(info.get("duration", 0)),
            "pubdate": info.get("pubdate_str"),
            "分区": info.get("tname"),
            "标签": info.get("tags", [])[:5],  # 只取前5个标签
            "stat": {
                "播放": info.get("stat", {}).get("view", 0),
                "点赞": info.get("stat", {}).get("like", 0),
                "收藏": info.get("stat", {}).get("favorite", 0),
                "弹幕": info.get("stat", {}).get("danmaku", 0)
            }
        }

    def _format_duration(self, seconds: int) -> str:
        """格式化时长"""
        if not seconds:
            return "00:00"
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def extract(self, url: str, mode: str = "basic", **kwargs) -> Dict[str, Any]:
        """主提取方法

        Args:
            url: 视频链接
            mode: 提取模式 - basic/full/summary
            **kwargs: 其他参数
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError(f"无法从链接中提取视频ID: {url}")

        print(f"[信息] 视频ID: {video_id}")
        print(f"[信息] 提取模式: {mode}")

        result = {
            "video_id": video_id,
            "url": url,
            "mode": mode,
            "timestamp": datetime.now().isoformat()
        }

        # 摘要模式 - 最快
        if mode == "summary":
            result["summary"] = self.get_summary(video_id)
            return result

        # 获取视频信息
        print("[进度] 1/4 获取视频信息...")
        result["info"] = self.get_video_info(video_id)

        # 基础模式
        if mode == "basic":
            return result

        # 完整模式
        print("[进度] 2/4 获取弹幕...")
        pages = kwargs.get("pages", "first")
        result["danmaku"] = self.get_danmaku(video_id, pages=pages)

        print("[进度] 3/4 获取评论...")
        result["comments"] = self.get_comments(video_id, limit=50)

        print("[进度] 4/4 数据整理完成")

        # 更新缓存
        self._write_cache(video_id, result)

        return result


def format_output(data: Dict, format_type: str = "json") -> str:
    """格式化输出"""
    if format_type == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    elif format_type == "markdown":
        return format_as_markdown(data)
    else:
        return json.dumps(data, ensure_ascii=False, indent=2)


def format_as_markdown(data: Dict) -> str:
    """格式化为Markdown"""
    info = data.get("info", {})
    stat = info.get("stat", {})

    lines = [
        "# B站视频分析",
        "",
        "## 基本信息",
        f"- **标题**: {info.get('title', '未知')}",
        f"- **链接**: {data.get('url', '')}",
        f"- **UP主**: {info.get('owner', {}).get('name', '未知')}",
        f"- **时长**: {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}",
        f"- **发布时间**: {info.get('pubdate_str', '未知')}",
        f"- **分区**: {info.get('tname', '未知')}",
        "",
        "## 数据表现",
        f"- 播放: {stat.get('view', 0):,}",
        f"- 点赞: {stat.get('like', 0):,}",
        f"- 收藏: {stat.get('favorite', 0):,}",
        f"- 弹幕: {stat.get('danmaku', 0):,}",
        "",
    ]

    if info.get('tags'):
        lines.append(f"**标签**: {' | '.join(info['tags'][:8])}")
        lines.append("")

    if data.get('danmaku'):
        lines.append("## 弹幕精选 (前20)")
        for i, d in enumerate(data['danmaku'][:20], 1):
            lines.append(f"{i}. {d['text']}")
        lines.append("")

    if data.get('comments'):
        lines.append("## 热门评论 (前10)")
        for c in sorted(data['comments'], key=lambda x: x.get('like', 0), reverse=True)[:10]:
            lines.append(f"- [{c.get('like', 0)}赞] {c.get('content', '')}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="B站视频内容提取工具 - 优化版")
    parser.add_argument("--url", required=True, help="B站视频链接")
    parser.add_argument("--mode", default="basic",
                        choices=["basic", "full", "summary"],
                        help="提取模式: basic(基础信息) / full(弹幕+评论) / summary(快速摘要)")
    parser.add_argument("--format", default="json",
                        choices=["json", "markdown"],
                        help="输出格式")
    parser.add_argument("--no-cache", action="store_true",
                        help="禁用缓存")
    parser.add_argument("--pages", default="first",
                        choices=["first", "all"],
                        help="弹幕获取: first(仅第一P) / all(全部P)")

    args = parser.parse_args()

    # 执行提取
    extractor = BilibiliExtractor(use_cache=not args.no_cache)

    try:
        result = extractor.extract(args.url, mode=args.mode, pages=args.pages)
        output = format_output(result, args.format)
        print(output)

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
