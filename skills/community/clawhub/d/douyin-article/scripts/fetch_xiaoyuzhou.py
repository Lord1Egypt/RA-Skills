#!/usr/bin/env python3
"""小宇宙播客音频获取模块（v3.0 新增）。

实现思路：
- 小宇宙 episode 页面含 <audio src="https://media.xyzcdn.net/..."> 直链
- 用 curl 抓 HTML → 正则提取 audio src → curl 下载音频
- ffmpeg 转 16kHz 单声道 MP3 → 走 Whisper 转录
- 不依赖 yt-dlp（yt-dlp 未原生支持小宇宙）
- 同时从 HTML 提取标题/作者/简介等元数据

参考：https://blog.eddiehe.top/article/download-a-podcast-from-xiaoyuzhou
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import (
    find_command, md5_file, run_cmd, probe_media_duration,
    extract_xiaoyuzhou_id,
)


# 提取 <audio src="..."> 的正则（小宇宙 v3.0 实测：audio 标签 src 经常为空，需 fallback 到 og:audio）
AUDIO_SRC_RE = re.compile(r'<audio[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
# og:audio meta 标签（小宇宙把音频直链放在这里：<meta property="og:audio" content="https://media.xyzcdn.net/...m4a">）
OG_AUDIO_RE = re.compile(r'<meta\s+property="og:audio"\s+content="([^"]+)"', re.IGNORECASE)
# 页面 JSON-LD 元数据（小宇宙在 HTML 中嵌入 schema:podcast-show / schema:podcast-episode）
JSONLD_RE = re.compile(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', re.DOTALL)
# <title> 标签
TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
# og:title / og:description 元数据
OG_TITLE_RE = re.compile(r'<meta\s+property="og:title"\s+content="([^"]+)"', re.IGNORECASE)
OG_DESC_RE = re.compile(r'<meta\s+property="og:description"\s+content="([^"]+)"', re.IGNORECASE)
# v3.1: og:audio:artist / og:audio:album 标签（小宇宙在 og:audio 周边提供主播信息）
OG_AUDIO_ARTIST_RE = re.compile(r'<meta\s+property="og:audio:artist"\s+content="([^"]+)"', re.IGNORECASE)
OG_AUDIO_ALBUM_RE = re.compile(r'<meta\s+property="og:audio:album"\s+content="([^"]+)"', re.IGNORECASE)
# v3.1: 小宇宙页面内嵌的 __NEXT_DATA__ / window.__INITIAL_STATE__ 中的 podcast 信息
# 注意：JSON-LD 通常包含 PodcastShow 但 author 字段在小宇宙中可能叫 by / podcastName
PODCAST_NAME_RE = re.compile(r'"podcastName"\s*:\s*"([^"]+)"', re.IGNORECASE)
PODCAST_BY_RE = re.compile(r'"by"\s*:\s*"([^"]+)"')
# v3.1: 小宇宙 Next.js SSR 数据结构（最稳的主播信息源）
NEXT_DATA_RE = re.compile(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL)
# v3.1: 全文兜底 - 从 HTML 中直接 grep "author" / "nickname" 字段
AUTHOR_FIELD_RE = re.compile(r'"author"\s*:\s*"([^"]+)"')
NICKNAME_FIELD_RE = re.compile(r'"nickname"\s*:\s*"([^"]+)"')


def _extract_audio_url(html: str) -> Optional[str]:
    """从 HTML 中提取音频直链。

    优先级：og:audio meta > <audio src="非空"> > JSON-LD contentUrl
    小宇宙页面实测（2026-07）：<audio src=""> 标签存在但 src 为空，
    真实音频 URL 在 <meta property="og:audio" content="https://media.xyzcdn.net/...m4a">
    """
    # 1. og:audio meta 标签（最稳）
    m = OG_AUDIO_RE.search(html)
    if m:
        url = m.group(1)
        if url.startswith("http"):
            return url

    # 2. <audio src="非空"> 标签
    for match in AUDIO_SRC_RE.finditer(html):
        url = match.group(1)
        if url.startswith("http"):
            return url

    # 3. JSON-LD 中的 contentUrl（schema:podcast-episode）
    for jsonld_match in JSONLD_RE.finditer(html):
        try:
            import json as _json
            data = _json.loads(jsonld_match.group(1).strip())
            if isinstance(data, dict):
                content_url = data.get("contentUrl") or data.get("associatedMedia", {}).get("contentUrl")
                if content_url and content_url.startswith("http"):
                    return content_url
        except Exception:
            pass

    # 4. 兜底：直接 grep media.xyzcdn.net 的 URL
    xyz_match = re.search(r'(https?://media\.xyzcdn\.net/[^\s"\'<>]+)', html)
    if xyz_match:
        return xyz_match.group(1)

    return None


def _fetch_html(url: str, timeout: int = 30) -> Optional[str]:
    """用 curl 获取页面 HTML。"""
    cmd = [
        find_command("curl"),
        "-L",  # 跟随重定向
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "-H", "Accept: text/html,application/xhtml+xml",
        "-s",
        "--max-time", str(timeout),
        url,
    ]
    ok, out = run_cmd(cmd, timeout=timeout + 10)
    if not ok or not out:
        return None
    return out


def _extract_metadata(html: str, url: str) -> dict:
    """从 HTML 中提取元数据：title / author / description。

    优先级：JSON-LD（schema:podcast-*）> og: 标签 > <title>
    """
    meta = {"title": None, "author": "未知", "description": ""}

    # 1. JSON-LD（小宇宙用 schema:podcast-show 和 schema:podcast-episode）
    for jsonld_match in JSONLD_RE.finditer(html):
        try:
            data = json.loads(jsonld_match.group(1).strip())
            if isinstance(data, dict):
                # 优先 PodcastEpisode
                if data.get("@type") in ("PodcastEpisode", "AudioObject", "Article", "Podcast"):
                    meta["title"] = meta["title"] or data.get("name") or data.get("title")
                    author = data.get("author")
                    if isinstance(author, dict):
                        meta["author"] = author.get("name", "未知")
                    elif isinstance(author, str) and author:
                        meta["author"] = author
                    description = data.get("description", "")
                    if description and not meta["description"]:
                        meta["description"] = description[:500]
                # PodcastShow（拿作者名）
                elif data.get("@type") in ("PodcastSeries", "PodcastShow", "Podcast"):
                    if meta["author"] == "未知":
                        author = data.get("author")
                        if isinstance(author, dict):
                            meta["author"] = author.get("name", "未知")
                        elif isinstance(author, str) and author:
                            meta["author"] = author
                    if not meta["description"]:
                        meta["description"] = (data.get("description", "") or "")[:500]
        except Exception:
            pass

    # 2. og:title 兜底
    if not meta["title"]:
        m = OG_TITLE_RE.search(html)
        if m:
            meta["title"] = m.group(1)

    # 3. <title> 兜底
    if not meta["title"]:
        m = TITLE_RE.search(html)
        if m:
            # 去掉网站名后缀（如 " - 问题青年 | 小宇宙"）
            title = m.group(1).strip()
            for sep in [" - 小宇宙", " | 小宇宙", " _ 小宇宙", " – 小宇宙"]:
                if sep in title:
                    title = title.split(sep)[0].strip()
                    break
            # 进一步清理 " - podcast_name"
            if " - " in title:
                title = title.split(" - ")[0].strip()
            meta["title"] = title

    # 4. og:description
    if not meta["description"]:
        m = OG_DESC_RE.search(html)
        if m:
            meta["description"] = m.group(1)[:500]

    # v3.1: 多重兜底提取主播名（按优先级）
    # 5a. __NEXT_DATA__ 中的 episode.author / episode.nickname（最精确的主播名）
    if meta["author"] == "未知":
        m = NEXT_DATA_RE.search(html)
        if m:
            try:
                next_data = json.loads(m.group(1).strip())
                page_props = next_data.get("props", {}).get("pageProps", {})
                episode = page_props.get("episode", {})

                # 优先：episode 内的 author / nickname 字段
                for field in ["author", "nickname"]:
                    val = episode.get(field)
                    if val and isinstance(val, str):
                        meta["author"] = val
                        break

                # 次选：podcast 内的 author / nickname / podcastName 字段（podcast.title 是 podcast 名，太宽泛，不放这）
                if meta["author"] == "未知":
                    podcast = episode.get("podcast", {}) if isinstance(episode, dict) else {}
                    for field in ["author", "nickname", "podcastName"]:
                        val = podcast.get(field)
                        if val and isinstance(val, str) and val != podcast.get("title"):
                            meta["author"] = val
                            break
            except (json.JSONDecodeError, AttributeError, TypeError):
                pass

    # 5b. og:audio:artist（OpenGraph 音频作者标签）
    if meta["author"] == "未知":
        m = OG_AUDIO_ARTIST_RE.search(html)
        if m:
            meta["author"] = m.group(1)
    # 5c. og:audio:album（专辑名 = podcast 名，作为兜底）
    if meta["author"] == "未知":
        m = OG_AUDIO_ALBUM_RE.search(html)
        if m:
            meta["author"] = m.group(1)
    # 5d. 全文兜底 grep "author":"..." 字段（小宇宙在 __NEXT_DATA__ 或 comments 中常有）
    if meta["author"] == "未知":
        m = AUTHOR_FIELD_RE.search(html)
        if m:
            meta["author"] = m.group(1)
    # 5e. 全文兜底 grep "nickname":"..." 字段
    if meta["author"] == "未知":
        m = NICKNAME_FIELD_RE.search(html)
        if m:
            meta["author"] = m.group(1)

    # 兜底标题
    eid = extract_xiaoyuzhou_id(url)
    if not meta["title"]:
        meta["title"] = f"小宇宙播客_{eid or 'unknown'}"

    return meta


def _download_audio(url: str, output_path: Path, timeout: int = 180) -> bool:
    """用 curl 下载音频文件。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        find_command("curl"),
        "-L",
        "-H", "User-Agent: Mozilla/5.0",
        "-H", "Referer: https://www.xiaoyuzhoufm.com/",
        "-o", str(output_path),
        "-s",
        "--max-time", str(timeout),
        url,
    ]
    ok, _ = run_cmd(cmd, timeout=timeout + 10)
    return ok and output_path.is_file() and output_path.stat().st_size > 1024


def _extract_mp3(input_path: Path, output_path: Path) -> bool:
    """用 ffmpeg 转 16kHz 单声道 MP3。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        find_command("ffmpeg"),
        "-y",
        "-i", str(input_path),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "libmp3lame",
        "-q:a", "5",
        str(output_path),
    ]
    ok, _ = run_cmd(cmd, timeout=120)
    return ok and output_path.is_file() and output_path.stat().st_size > 1024


def fetch_one_xiaoyuzhou(
    idx: int,
    item: dict,
    audio_dir: Path,
    raw_dir: Path,
    seen_md5: set[str],
) -> dict:
    """下载单个小宇宙 episode 并提取 16kHz 单声道 MP3。

    流程：curl HTML → 正则提取 audio src → curl 下载音频 → ffmpeg 转 MP3 → MD5 去重
    """
    url = item["url"]
    eid = extract_xiaoyuzhou_id(url) or ""
    print(f"\n[{idx}] 小宇宙处理: episode={eid}", flush=True)
    print(f"     URL: {url}", flush=True)

    # 1. 抓 HTML 页面
    print(f"     抓取 episode 页面...", flush=True)
    html = _fetch_html(url, timeout=30)
    if not html:
        return {"idx": idx, "success": False, "error": "抓取 HTML 失败（网络问题或 URL 无效）"}

    # 2. 提取 audio URL（og:audio 优先，audio src fallback）
    audio_url = _extract_audio_url(html)
    if not audio_url:
        return {"idx": idx, "success": False, "error": "HTML 中未找到 audio URL（og:audio / <audio src> / JSON-LD 均未命中，页面结构可能已变更）"}
    print(f"     音频直链: {audio_url[:80]}...", flush=True)

    # 3. 提取元数据
    meta = _extract_metadata(html, url)
    title = meta["title"]
    author = meta["author"]
    print(f"     标题: {title}", flush=True)
    print(f"     主播: {author}", flush=True)

    # 4. 下载音频
    raw_path = raw_dir / f"raw_{idx}.mp3"  # 小宇宙直链通常就是 mp3/m4a
    print(f"     下载音频...", flush=True)
    if not _download_audio(audio_url, raw_path, timeout=300):
        return {"idx": idx, "success": False, "error": "下载音频失败"}

    # 5. 转 16kHz 单声道 MP3
    mp3_path = audio_dir / f"audio_{idx}.mp3"
    if not _extract_mp3(raw_path, mp3_path):
        return {"idx": idx, "success": False, "error": "ffmpeg 转换 16kHz MP3 失败"}

    # 6. MD5 去重
    file_md5 = md5_file(mp3_path)
    if file_md5 in seen_md5:
        return {"idx": idx, "success": False, "error": "MD5 重复，疑似下载到相同文件"}
    seen_md5.add(file_md5)

    # 7. 探测时长
    duration = probe_media_duration(mp3_path)
    size_kb = mp3_path.stat().st_size // 1024
    print(f"     ✅ 完成: {mp3_path.name} ({size_kb} KB, {duration:.1f}s)", flush=True)

    return {
        "idx": idx,
        "success": True,
        "title": title,
        "author": author,
        "source_url": url,
        "platform": "xiaoyuzhou",
        "episode_id": eid,
        "audio_path": str(mp3_path),
        "duration_sec": float(duration),
        "md5": file_md5,
        "description": meta["description"],
    }
