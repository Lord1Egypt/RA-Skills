"""B站API封装 — 收藏夹、视频信息、字幕、评论、弹幕获取"""

import json
import subprocess
import requests
from typing import Optional
from dataclasses import dataclass


@dataclass
class VideoInfo:
    bvid: str
    aid: int
    cid: int
    title: str
    desc: str
    owner: str
    duration: int  # 秒
    view: int
    danmaku: int
    like: int
    coin: int
    favorite: int
    subtitle_url: Optional[str] = None


@dataclass
class Comment:
    uname: str
    content: str
    like: int
    reply_count: int


@dataclass
class Danmaku:
    content: str
    send_time: float  # 秒


@dataclass
class FavoriteFolder:
    id: int
    title: str
    media_count: int


class BilibiliAPI:
    BASE_URL = "https://api.bilibili.com"

    def __init__(self, sessdata: str, bili_jct: str, buvid3: str):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com",
        })
        self.session.cookies.set("SESSDATA", sessdata, domain=".bilibili.com")
        self.session.cookies.set("bili_jct", bili_jct, domain=".bilibili.com")
        self.session.cookies.set("buvid3", buvid3, domain=".bilibili.com")

    def _get(self, url: str, params: dict = None) -> dict:
        """GET请求，requests失败时自动fallback到curl"""
        try:
            resp = self.session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except (requests.ConnectionError, requests.Timeout, requests.exceptions.RequestException):
            # DNS不通时fallback到curl
            data = self._curl_get(url, params)
        if data.get("code") != 0:
            raise Exception(f"B站API错误: {data.get('message', 'unknown')} (code={data.get('code')})")
        return data.get("data", {})

    def _curl_get(self, url: str, params: dict = None) -> dict:
        """用curl发送GET请求（绕过Python DNS问题）"""
        if params:
            qs = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{qs}"
        cookie_str = "; ".join([
            f"SESSDATA={self.session.cookies.get('SESSDATA', '')}",
            f"bili_jct={self.session.cookies.get('bili_jct', '')}",
            f"buvid3={self.session.cookies.get('buvid3', '')}",
        ])
        result = subprocess.run(
            ["curl", "-s", "--connect-timeout", "15", url,
             "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
             "-H", "Referer: https://www.bilibili.com",
             "-H", f"Cookie: {cookie_str}"],
            capture_output=True, text=True, timeout=30,
        )
        if not result.stdout.strip():
            raise Exception(f"curl请求无响应: {url}")
        return json.loads(result.stdout)

    def _curl_get_raw(self, url: str) -> bytes:
        """用curl获取原始二进制数据（用于弹幕等）"""
        result = subprocess.run(
            ["curl", "-s", "--connect-timeout", "15", url],
            capture_output=True, timeout=30,
        )
        return result.stdout

    def get_user_mid(self) -> int:
        """获取当前登录用户的mid"""
        data = self._get(f"{self.BASE_URL}/x/web-interface/nav")
        return data["mid"]

    def get_favorites_list(self) -> list[FavoriteFolder]:
        """获取用户所有收藏夹"""
        mid = self.get_user_mid()
        data = self._get(
            f"{self.BASE_URL}/x/v3/fav/folder/created/list-all",
            {"up_mid": mid},
        )
        return [
            FavoriteFolder(id=f["id"], title=f["title"], media_count=f["media_count"])
            for f in data.get("list", [])
        ]

    def get_videos_from_folder(self, folder_id: int, page: int = 1, page_size: int = 20, order: str = "time") -> list[VideoInfo]:
        """获取收藏夹内的视频列表

        Args:
            order: 排序方式，"time"=按收藏时间倒序（最新收藏在前），默认time
        """
        data = self._get(
            f"{self.BASE_URL}/x/v3/fav/resource/list",
            {"media_id": folder_id, "pn": page, "ps": page_size, "order": order},
        )
        videos = []
        for item in data.get("medias", []) or []:
            if item.get("type") != 2:  # 2=视频
                continue
            videos.append(VideoInfo(
                bvid=item["bvid"],
                aid=item["id"],
                cid=item.get("ugc", {}).get("first_cid", 0),
                title=item["title"],
                desc=item.get("intro", ""),
                owner=item.get("upper", {}).get("name", ""),
                duration=item.get("duration", 0),
                view=item.get("cnt_info", {}).get("view", 0),
                danmaku=item.get("cnt_info", {}).get("danmaku", 0),
                like=item.get("cnt_info", {}).get("like", 0),
                coin=item.get("cnt_info", {}).get("coin", 0),
                favorite=item.get("cnt_info", {}).get("favorite", 0),
            ))
        return videos

    def _get_subtitle_from_player(self, aid: int, cid: int) -> Optional[str]:
        """通过 /x/player/wbi/v2 接口获取字幕URL（含UP主上传字幕）"""
        try:
            data = self._get(
                f"{self.BASE_URL}/x/player/wbi/v2",
                {"aid": aid, "cid": cid},
            )
            subtitles = data.get("subtitle", {}).get("subtitles", [])
            if not subtitles:
                return None
            # 优先选中文字幕 (zh-CN, zh-Hans, zh 等)
            for sub in subtitles:
                lan = sub.get("lan", "")
                if "zh" in lan:
                    url = sub.get("subtitle_url", "")
                    return "https:" + url if url.startswith("//") else url
            # 没有中文就取第一个
            url = subtitles[0].get("subtitle_url", "")
            return "https:" + url if url.startswith("//") else url
        except Exception:
            return None

    def get_video_detail(self, bvid: str) -> VideoInfo:
        """获取视频详情（含字幕URL）"""
        data = self._get(
            f"{self.BASE_URL}/x/web-interface/view",
            {"bvid": bvid},
        )

        # 方法1: 从 view 接口获取字幕（AI生成的CC字幕）
        subtitle_url = None
        subtitles = data.get("subtitle", {}).get("list", [])
        if subtitles:
            for sub in subtitles:
                if "zh" in sub.get("lan", ""):
                    subtitle_url = sub["subtitle_url"]
                    break
            if not subtitle_url:
                subtitle_url = subtitles[0]["subtitle_url"]

        # 方法2: 如果 view 接口没拿到字幕，尝试 player 接口（含UP主上传字幕）
        if not subtitle_url:
            aid = data["aid"]
            cid = data["cid"]
            subtitle_url = self._get_subtitle_from_player(aid, cid)

        if subtitle_url and subtitle_url.startswith("//"):
            subtitle_url = "https:" + subtitle_url

        return VideoInfo(
            bvid=data["bvid"],
            aid=data["aid"],
            cid=data["cid"],
            title=data["title"],
            desc=data.get("desc", ""),
            owner=data.get("owner", {}).get("name", ""),
            duration=data.get("duration", 0),
            view=data.get("stat", {}).get("view", 0),
            danmaku=data.get("stat", {}).get("danmaku", 0),
            like=data.get("stat", {}).get("like", 0),
            coin=data.get("stat", {}).get("coin", 0),
            favorite=data.get("stat", {}).get("favorite", 0),
            subtitle_url=subtitle_url,
        )

    def get_subtitles(self, subtitle_url: str) -> list[dict]:
        """下载并解析字幕，返回 [{from, to, content}, ...]"""
        try:
            resp = self.session.get(subtitle_url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except (requests.ConnectionError, requests.Timeout, requests.exceptions.RequestException):
            raw = self._curl_get_raw(subtitle_url)
            data = json.loads(raw)
        return data.get("body", [])

    def get_top_comments(self, aid: int, limit: int = 10) -> list[Comment]:
        """获取高赞评论"""
        data = self._get(
            f"{self.BASE_URL}/x/v2/reply/main",
            {"type": 1, "oid": aid, "mode": 3},  # mode=3=按热度
        )
        comments = []
        for reply in (data.get("replies") or [])[:limit]:
            comments.append(Comment(
                uname=reply["member"]["uname"],
                content=reply["content"]["message"],
                like=reply["like"],
                reply_count=reply.get("rcount", 0),
            ))
        return comments

    def get_danmakus(self, cid: int, limit: int = 50) -> list[Danmaku]:
        """获取弹幕（解析protobuf格式）"""
        from .danmaku_pb2 import parse_danmaku_protobuf
        url = f"{self.BASE_URL}/x/v2/dm/web/seg.so"
        try:
            resp = self.session.get(url, params={"oid": cid, "segment_index": 1}, timeout=15)
            resp.raise_for_status()
            content = resp.content
        except (requests.ConnectionError, requests.Timeout, requests.exceptions.RequestException):
            content = self._curl_get_raw(f"{url}?oid={cid}&segment_index=1")
        return parse_danmaku_protobuf(content, limit)
