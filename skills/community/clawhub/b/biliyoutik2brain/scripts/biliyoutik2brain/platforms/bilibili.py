"""
BiliYouTik2Brain — B站平台适配器

职责: B站视频的元信息/音频直链/字幕/评论采集
不包含: 转录、修复、分析（这些在core/pipeline.py编排）
"""

import json, os, re, subprocess, time
from typing import Dict, List, Optional, Tuple
from collections import Counter

from .base import BaseExtractor
from ..core.schemas import (
    Platform, VideoInfo, AudioResult, SubtitleResult,
    CommentResult, CollectResult
)


class BilibiliExtractor(BaseExtractor):
    """B站视频采集适配器"""

    platform = Platform.BILIBILI
    domain_regex = r'(bilibili\.com|b23\.tv|BV[1-9]\w+)'

    # ─── 通用请求 ────────────────────────────────────────

    @staticmethod
    def _req(url: str, max_retries: int = 3, retry_delay: int = 5) -> Optional[Dict]:
        """带重试的B站API请求"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
        }
        for attempt in range(max_retries):
            result = subprocess.run(
                ["curl", "-s", url,
                 "-H", f"User-Agent: {headers['User-Agent']}",
                 "-H", f"Referer: {headers['Referer']}"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode != 0 or not result.stdout.strip():
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                continue
            try:
                data = json.loads(result.stdout)
                code = data.get("code", -1)
                if code == -799:
                    time.sleep(retry_delay * (attempt + 1) * 3)
                    continue
                return data
            except json.JSONDecodeError:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                continue
        return None

    # ─── URL解析 ─────────────────────────────────────────

    @staticmethod
    def resolve_short_link(url: str) -> Optional[str]:
        """解析 b23.tv 短链接"""
        result = subprocess.run(
            ["curl", "-sI", "-o", "/dev/null", "-w", "%{redirect_url}", url],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip()
        return None

    @staticmethod
    def extract_bv(full_url: str) -> Optional[str]:
        m = re.search(r'BV\w+', full_url)
        return m.group(0) if m else None

    # ─── 元信息 ──────────────────────────────────────────

    def extract_video_info(self, url: str) -> Optional[VideoInfo]:
        """从B站API获取视频元信息"""
        # 解析短链接
        if "b23.tv" in url:
            full = self.resolve_short_link(url)
            if full:
                url = full
        
        bvid = self.extract_bv(url)
        if not bvid:
            raise ValueError(f"无法从URL提取BV号: {url}")
        
        # 提取分页参数 ?p=N
        page_num = 1
        m_page = re.search(r'[?&]p=(\d+)', url)
        if m_page:
            page_num = int(m_page.group(1))
        
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        data = self._req(api_url)
        if not data or data.get("code") != 0:
            raise ValueError(f"B站API返回异常: {data}")
        
        d = data["data"]
        duration = d.get("duration", 0)
        
        # 多页视频: 从 pages 数组查出正确分页的 duration 和 cid
        pages = d.get("pages", [])
        correct_cid = d.get("cid", 0)
        if page_num > 1 and pages:
            for pg in pages:
                if pg.get("page") == page_num:
                    duration = pg.get("duration", duration)
                    correct_cid = pg.get("cid", correct_cid)
                    break
        
        # 构造视频信息，用正确的 duration 和 raw.cid
        video_url = f"https://www.bilibili.com/video/{bvid}"
        if page_num > 1:
            video_url += f"?p={page_num}"
        
        vi = VideoInfo(
            platform=Platform.BILIBILI,
            video_id=bvid,
            title=d.get("title", ""),
            duration=duration,
            uploader=d.get("owner", {}).get("name", ""),
            uploader_id=str(d.get("owner", {}).get("mid", "")),
            url=video_url,
            description=d.get("desc", ""),
            view_count=d.get("stat", {}).get("view", 0),
            like_count=d.get("stat", {}).get("like", 0),
            publish_time=None,
            tags=[],
            raw=data["data"],
        )
        # 将正确 cid 注入 raw，让下游 extract_audio() 拿到正确分页
        vi.raw["cid"] = correct_cid
        
        return vi

    # ─── 音频 ────────────────────────────────────────────

    def extract_audio(self, video: VideoInfo) -> AudioResult:
        """获取B站音频直链并下载"""
        cid = video.raw.get("cid", 0)
        if not cid:
            return AudioResult(success=False, error="无cid")
        
        # 获取音频直链（dash audio，跳过视频）
        api_url = (
            f"https://api.bilibili.com/x/player/playurl"
            f"?bvid={video.video_id}&cid={cid}&qn=64&otype=json"
            f"&platform=web&fnver=0&fnval=4048"
        )
        data = self._req(api_url)
        audio_url = None
        if data and data.get("code") == 0:
            dash = data["data"].get("dash", {})
            audio_list = dash.get("audio", [])
            if audio_list:
                audio_url = audio_list[0].get("baseUrl") or audio_list[0].get("base_url", "")
        
        if not audio_url:
            # 回退: 获取视频下载URL（非dash）
            play_url = (
                f"https://api.bilibili.com/x/player/playurl"
                f"?bvid={video.video_id}&cid={cid}&qn=64&otype=json&platform=web&high_quality=1"
            )
            data2 = self._req(play_url)
            if data2 and data2.get("code") == 0:
                durls = data2["data"].get("durl", [])
                if durls:
                    audio_url = durls[0].get("url")
        
        if not audio_url:
            return AudioResult(success=False, error="无法获取音频直链")
        
        # 下载到临时文件
        tmp_dir = "/tmp/bili_work"
        os.makedirs(tmp_dir, exist_ok=True)
        save_path = os.path.join(tmp_dir, f"{video.video_id}.m4s")
        
        try:
            result = subprocess.run(
                ["curl", "-sL", "-o", save_path, "-w", "%{http_code}",
                 "-H", "Referer: https://www.bilibili.com/",
                 "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
                 audio_url],
                capture_output=True, text=True, timeout=300
            )
            if result.stdout.strip() == "200" and os.path.getsize(save_path) > 500:
                return AudioResult(
                    success=True,
                    file_path=save_path,
                    duration_s=video.duration,
                    format="m4s"
                )
        except Exception as e:
            return AudioResult(success=False, error=str(e))
        
        return AudioResult(success=False, error="下载失败")

    # ─── 字幕 ────────────────────────────────────────────

    def extract_subtitle(self, video: VideoInfo) -> SubtitleResult:
        """从B站获取字幕（如果有）
        
        注意: 交易类/时评类UP主视频通常无字幕，此路径在业务上很少触发
        """
        bvid = video.video_id
        cid = video.raw.get("cid", 0)
        if not cid:
            return SubtitleResult(success=False, error="无cid")
        
        # 尝试 player/wbi/v2 接口
        url = f"https://api.bilibili.com/x/player/wbi/v2?bvid={bvid}&cid={cid}"
        data = self._req(url)
        if not data or data.get("code") != 0:
            return SubtitleResult(success=False, error="字幕API无返回")
        
        subtitle_data = data.get("data", {})
        subtitle_list = subtitle_data.get("subtitle", {}).get("subtitles", [])
        
        if not subtitle_list:
            return SubtitleResult(success=False, error="无字幕")
        
        # 取第一个字幕
        sub_info = subtitle_list[0]
        sub_url = sub_info.get("subtitle_url", "")
        if not sub_url.startswith("http"):
            sub_url = "https:" + sub_url if sub_url.startswith("//") else sub_url
        
        # 下载字幕JSON
        try:
            result = subprocess.run(
                ["curl", "-s", sub_url],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and result.stdout.strip():
                sub_json = json.loads(result.stdout)
                body = sub_json.get("body", [])
                text = "\n".join(
                    item.get("content", "") for item in body
                )
                quality = min(1.0, len(text) / (video.duration * 0.3))
                return SubtitleResult(
                    success=True,
                    text=text,
                    quality=max(0.6, quality),
                    segments=body,
                    source="api"
                )
        except Exception as e:
            return SubtitleResult(success=False, error=str(e))
        
        return SubtitleResult(success=False, error="字幕下载失败")

    # ─── 评论 ────────────────────────────────────────────

    def extract_comments(self, video: VideoInfo) -> CommentResult:
        """获取B站评论（B站评论API无风控）"""
        aid = video.raw.get("aid", 0)
        if not aid:
            return CommentResult(success=False, error="无aid")
        
        hot_comments = []
        new_comments = []
        
        # 热门评论
        url_hot = f"https://api.bilibili.com/x/v2/reply/main?type=1&oid={aid}&mode=3"
        data = self._req(url_hot)
        if data and data.get("code") == 0 and data.get("data"):
            for reply in (data["data"].get("replies") or []):
                hot_comments.append({
                    "content": reply["content"]["message"],
                    "likes": reply.get("like", 0),
                    "name": reply["member"]["uname"],
                })
        
        # 最新评论
        url_new = f"https://api.bilibili.com/x/v2/reply?type=1&oid={aid}&sort=1&pn=1&ps=20"
        data2 = self._req(url_new)
        if data2 and data2.get("code") == 0 and data2.get("data"):
            for reply in (data2["data"].get("replies") or []):
                new_comments.append({
                    "content": reply["content"]["message"],
                    "likes": reply.get("like", 0),
                    "name": reply["member"]["uname"],
                })
        
        if not hot_comments and not new_comments:
            return CommentResult(success=False, error="无评论")
        
        # 评论分析
        insights = self._analyze_comments(hot_comments, new_comments, video)
        
        return CommentResult(
            success=True,
            hot=hot_comments,
            new=new_comments,
            total=len(hot_comments) + len(new_comments),
            insights=insights,
        )

    @staticmethod
    def _analyze_comments(
        hot: List[Dict], new: List[Dict],
        video: VideoInfo
    ) -> List[str]:
        """分析评论，提取洞察"""
        insights = []
        all_texts = [c["content"] for c in hot] + [c["content"] for c in new]
        
        if not all_texts:
            return []
        
        # 关键词库
        negative_kw = [
            "骗子", "卖课", "韭菜", "智商税", "忽悠", "割", "假", "无语",
            "反向", "坑人", "别信", "垃圾", "骗人", "割韭菜", "培训",
            "带单", "收费", "诈骗", "没用", "扯淡", "传销",
        ]
        thoughtful_kw = [
            "请问", "求教", "谢谢", "分享", "干货", "有道理", "收藏",
            "请教", "受教", "学到了", "赞", "确实", "点醒", "受益",
        ]
        high_value_kw = [
            "亲身", "经历", "我做过", "我试过", "实战", "真实",
            "复盘", "总结", "反思", "我犯过", "学费", "教训",
        ]
        
        full_text = " ".join(all_texts)
        total = len(all_texts)
        
        # 质疑比
        neg_count = sum(1 for t in all_texts if any(k in t for k in negative_kw))
        thoughtful_count = sum(1 for t in all_texts if any(k in t for k in thoughtful_kw))
        hv_count = sum(1 for t in all_texts if any(k in t for k in high_value_kw))
        
        neg_ratio = neg_count / total if total > 0 else 0
        if neg_ratio > 0.3:
            insights.append(f"⚠️ 质疑比 {neg_ratio:.0%}（{neg_count}/{total}），内容存在争议")
        elif neg_ratio > 0.1:
            insights.append(f"质疑比 {neg_ratio:.0%}，有一定负面评价")
        else:
            insights.append(f"负面评价占比 {neg_ratio:.0%}，口碑较好")
        
        if thoughtful_count > 2:
            insights.append(f"有 {thoughtful_count} 条高质量讨论（求教/分享/感谢）")
        if hv_count > 0:
            insights.append(f"有 {hv_count} 条高价值评论（实战经历/复盘反思）")
        
        # 高赞评论
        all_sorted = sorted(hot + new, key=lambda x: x.get("likes", 0), reverse=True)
        top_likes = [c for c in all_sorted if c.get("likes", 0) > 5][:3]
        if top_likes:
            insights.append("高赞评论:")
            for c in top_likes[:3]:
                insights.append(f"  👍{c['likes']}: {c['content'][:60]}")
        
        return insights


    # ─── 合集解析 ──────────────────────────────────────────

    @staticmethod
    def list_collection(bvid: str) -> List[Dict]:
        """解析合集（ugc_season），返回所有分集信息
        
        B站 view API 返回的 raw.ugc_season 包含合集元数据和所有分集。
        此函数直接从 API 查询，适用于手动传 BVID 场景。
        
        返回:
            [{"bvid": "...", "title": "...", "duration": int}, ...]
            非合集 → []
        """
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        data = BilibiliExtractor._req(api_url)
        if not data or data.get("code") != 0:
            return []
        
        d = data.get("data", {})
        season = d.get("ugc_season")
        if not season:
            return []
        
        episodes = []
        for section in season.get("sections", []):
            for ep in section.get("episodes", []):
                episodes.append({
                    "bvid": ep["bvid"],
                    "title": ep.get("title", ""),
                    "duration": ep.get("duration", 0),
                })
        return episodes


# ─── 注册到平台注册表 ────────────────────────────────────

from ..core.config import PlatformRegistry
PlatformRegistry.register(BilibiliExtractor)
