#!/usr/bin/env python3
"""
video_fetcher.py - 视频信息与字幕提取工具（支持B站 + 抖音 + YouTube + 小红书）

用法:
    python3 video_fetcher.py <视频链接>

支持的链接格式:
    - B站: bilibili.com/video/BVxxx 或 BVxxx
    - 抖音: douyin.com/video/xxx 或 v.douyin.com/xxx
    - YouTube: youtube.com/watch?v=xxx 或 youtu.be/xxx
    - 小红书: xiaohongshu.com/explore/xxx 或 xhslink.com/xxx

输出:
    JSON 格式的视频信息 + 字幕内容（打印到 stdout）
"""

import sys
import os
import re
import json
import time
import subprocess
import shutil
import urllib.request
import urllib.parse
import urllib.error

# ---------- 工具函数 ----------

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def http_get(url: str, params: dict = None, extra_headers: dict = None) -> dict:
    """发起 GET 请求并返回解析后的 JSON"""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    headers = {**HEADERS, **(extra_headers or {})}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def detect_platform(text: str) -> str:
    """识别链接平台：bilibili / douyin / youtube / xiaohongshu / unknown"""
    t = text.lower()
    if "bilibili.com" in t or re.search(r"(BV[0-9A-Za-z]{10})", t, re.IGNORECASE):
        return "bilibili"
    if "douyin.com" in t or "tiktok.com" in t:
        return "douyin"
    if "youtube.com" in t or "youtu.be" in t:
        return "youtube"
    if "xiaohongshu.com" in t or "xhslink.com" in t or "xhs.cn" in t:
        return "xiaohongshu"
    return "unknown"


def generate_video_id(text: str, platform: str) -> str:
    """为视频生成唯一 ID（用于缓存等）"""
    if platform == "bilibili":
        m = re.search(r"(BV[0-9A-Za-z]{10})", text, re.IGNORECASE)
        if m:
            return m.group(1).upper()
    if platform == "douyin":
        m = re.search(r"/video/(\d+)", text)
        if m:
            return f"dy_{m.group(1)}"
        m = re.search(r"note/(\d+)", text)
        if m:
            return f"dy_{m.group(1)}"
    if platform == "youtube":
        m = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", text)
        if m:
            return f"yt_{m.group(1)}"
    if platform == "xiaohongshu":
        m = re.search(r"/(?:explore|discovery/item)/([a-f0-9]+)", text)
        if m:
            return f"xhs_{m.group(1)}"
        m = re.search(r"xhslink\.com/([a-zA-Z0-9]+)", text)
        if m:
            return f"xhs_{m.group(1)}"
    return f"{platform}_{hash(text) % 100000000:08d}"


# ---------- B站相关 ----------

def extract_bvid(text: str) -> str:
    """从 URL 或原始字符串中提取 BV 号"""
    m = re.search(r"(BV[0-9A-Za-z]{10})", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    raise ValueError(f"无法从 '{text}' 中提取 BV 号，请确认链接格式正确。")


def fetch_bilibili_info(bvid: str) -> dict:
    """获取B站视频基本信息"""
    data = http_get(
        "https://api.bilibili.com/x/web-interface/view",
        {"bvid": bvid}
    )
    if data.get("code") != 0:
        raise RuntimeError(f"API 错误: {data.get('message', '未知错误')}")
    v = data["data"]
    return {
        "platform": "bilibili",
        "video_id": bvid,
        "title": v.get("title", ""),
        "desc": v.get("desc", ""),
        "owner": v.get("owner", {}).get("name", ""),
        "duration_sec": v.get("duration", 0),
        "view": v.get("stat", {}).get("view", 0),
        "like": v.get("stat", {}).get("like", 0),
        "coin": v.get("stat", {}).get("coin", 0),
        "favorite": v.get("stat", {}).get("favorite", 0),
        "share": v.get("stat", {}).get("share", 0),
        "danmaku": v.get("stat", {}).get("danmaku", 0),
        "reply": v.get("stat", {}).get("reply", 0),
        "pubdate": v.get("pubdate", 0),
        "pic": v.get("pic", ""),
        "tags": [],
        "extra": {
            "aid": v.get("aid"),
            "cid": v["pages"][0]["cid"] if v.get("pages") else None,
        },
    }


def fetch_bilibili_tags(aid: int) -> list:
    """获取B站视频标签"""
    try:
        data = http_get(
            "https://api.bilibili.com/x/tag/archive/tags",
            {"aid": aid}
        )
        if data.get("code") == 0:
            return [t.get("tag_name", "") for t in data.get("data", [])]
    except Exception:
        pass
    return []


def fetch_bilibili_subtitle_list(bvid: str, cid: int) -> list:
    """获取B站字幕列表"""
    data = http_get(
        "https://api.bilibili.com/x/player/v2",
        {"bvid": bvid, "cid": cid}
    )
    if data.get("code") != 0:
        return []
    subtitle_info = data.get("data", {}).get("subtitle", {})
    return subtitle_info.get("subtitles", [])


def fetch_subtitle_content(subtitle_url: str) -> list:
    """下载并解析字幕 JSON，返回字幕段列表"""
    if subtitle_url.startswith("//"):
        subtitle_url = "https:" + subtitle_url
    req = urllib.request.Request(subtitle_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    return data.get("body", [])


def subtitles_to_text(body: list) -> str:
    """将字幕段列表转换为带时间戳的文本"""
    lines = []
    for seg in body:
        t_from = seg.get("from", 0)
        content = seg.get("content", "").strip()
        if content:
            mm = int(t_from // 60)
            ss = int(t_from % 60)
            lines.append(f"[{mm:02d}:{ss:02d}] {content}")
    return "\n".join(lines)


def subtitles_to_plain(body: list) -> str:
    """纯文本（无时间戳），用于信息密度分析"""
    return " ".join(
        seg.get("content", "").strip()
        for seg in body
        if seg.get("content", "").strip()
    )


# ---------- 抖音相关 ----------

def resolve_douyin_url(short_url: str) -> str:
    """解析抖音短链接，获取重定向后的实际 URL"""
    try:
        req = urllib.request.Request(short_url, headers={
            "User-Agent": HEADERS["User-Agent"],
        })
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        resp = opener.open(req, timeout=10)
        return resp.url
    except Exception as e:
        print(f"[!] 解析短链接失败: {e}", file=sys.stderr)
        return short_url


def fetch_douyin_info(url: str) -> dict:
    """获取抖音视频基本信息（通过网页解析，无需API Key）"""
    if "v.douyin.com" in url:
        url = resolve_douyin_url(url)
        print(f"[*] 抖音实际链接: {url}", file=sys.stderr)

    video_id = ""
    m = re.search(r"/video/(\d+)", url)
    if m:
        video_id = m.group(1)

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": HEADERS["User-Agent"],
            "Referer": "https://www.douyin.com/",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")

        title = ""
        desc = ""
        author = ""
        duration = 0

        title_m = re.search(r'<title[^>]*>([^<]+)</title>', html)
        if title_m:
            title = title_m.group(1).strip()
            if " | " in title:
                title = title.split(" | ")[0].strip()
            if " - " in title:
                title = title.split(" - ")[0].strip()

        render_match = re.search(r'self\.__pace_f\.push\(\[.*?"desc"\s*:\s*"([^"]*)"', html, re.DOTALL)
        if render_match:
            desc = render_match.group(1).replace("\\n", " ").strip()
        if not desc:
            desc_match = re.search(r'"desc"\s*:\s*"([^"]*)"', html)
            if desc_match:
                desc = desc_match.group(1).replace("\\n", " ").strip()

        author_match = re.search(r'"nickname"\s*:\s*"([^"]*)"', html)
        if author_match:
            author = author_match.group(1)

        dur_match = re.search(r'"duration"\s*:\s*(\d+)', html)
        if dur_match:
            duration = int(dur_match.group(1)) // 1000

        pic = ""
        pic_match = re.search(r'"cover"\s*:\s*\{[^}]*"url_list"\s*:\s*\["([^"]*)"', html)
        if pic_match:
            pic = pic_match.group(1)
        else:
            pic_match = re.search(r'"originCover"\s*:\s*"([^"]*)"', html)
            if pic_match:
                pic = pic_match.group(1)

        return {
            "platform": "douyin",
            "video_id": f"dy_{video_id}" if video_id else f"dy_{hash(url) % 100000000:08d}",
            "title": title,
            "desc": desc,
            "owner": author,
            "duration_sec": duration,
            "view": 0,
            "like": 0,
            "coin": 0,
            "favorite": 0,
            "share": 0,
            "danmaku": 0,
            "reply": 0,
            "pubdate": 0,
            "pic": pic,
            "tags": [],
            "extra": {"url": url},
        }
    except Exception as e:
        print(f"[!] 获取抖音视频信息失败: {e}", file=sys.stderr)
        return {
            "platform": "douyin",
            "video_id": f"dy_{video_id}" if video_id else f"dy_{hash(url) % 100000000:08d}",
            "title": "",
            "desc": "",
            "owner": "",
            "duration_sec": 0,
            "view": 0, "like": 0, "coin": 0, "favorite": 0,
            "share": 0, "danmaku": 0, "reply": 0,
            "pubdate": 0, "pic": "",
            "tags": [],
            "extra": {"url": url},
        }


# ---------- YouTube 相关 ----------

def fetch_youtube_info(url: str) -> dict:
    """获取 YouTube 视频基本信息（通过 yt-dlp）"""
    ytdlp = shutil.which("yt-dlp") or "/opt/homebrew/bin/yt-dlp"
    if not ytdlp or not os.path.exists(ytdlp):
        raise RuntimeError("yt-dlp 未安装。请运行: brew install yt-dlp")

    print("[*] 使用 yt-dlp 获取 YouTube 视频信息...", file=sys.stderr)
    cmd = [ytdlp, "--no-playlist", "--dump-json", "--skip-download", url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        raise RuntimeError(f"获取YouTube信息失败: {result.stderr[-300:]}")

    data = json.loads(result.stdout)
    return {
        "platform": "youtube",
        "video_id": data.get("id", ""),
        "title": data.get("title", ""),
        "desc": data.get("description", "")[:500],
        "owner": data.get("uploader", ""),
        "duration_sec": data.get("duration", 0),
        "view": data.get("view_count", 0) or 0,
        "like": data.get("like_count", 0) or 0,
        "coin": 0,
        "favorite": 0,
        "share": 0,
        "danmaku": 0,
        "reply": 0,
        "pubdate": 0,
        "pic": data.get("thumbnail", ""),
        "tags": data.get("tags", [])[:20],
        "extra": {
            "url": url,
            "channel_id": data.get("channel_id", ""),
            "upload_date": data.get("upload_date", ""),
        },
    }


def fetch_youtube_subtitle(url: str, lang: str = "zh-CN") -> list:
    """尝试获取 YouTube 字幕（通过 yt-dlp）"""
    ytdlp = shutil.which("yt-dlp") or "/opt/homebrew/bin/yt-dlp"
    if not ytdlp or not os.path.exists(ytdlp):
        return []

    print("[*] 尝试获取 YouTube 字幕...", file=sys.stderr)

    # 优先中文自动生成字幕，然后英文，最后任意字幕
    for sub_lang in [f"{lang}", "zh", "zh-Hans", "en", "en-US", None]:
        cmd = [ytdlp, "--no-playlist", "--skip-download",
               "--write-sub", "--write-auto-sub",
               "--sub-lang", sub_lang or "",
               "--sub-format", "json3",
               "-o", os.path.join(
                   os.path.dirname(os.path.abspath(__file__)),
                   "..", "cache", "subtitle_cache_%(id)s.%(ext)s"
               ),
               "--dump-json", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        # Note: yt-dlp subtitle download is complex, fallback to ASR
        # We'll try to get auto-sub via --print-json with subtitles
        break

    # YouTube auto-sub extraction is unreliable, recommend ASR
    print("[*] YouTube 字幕获取不可靠，建议使用 ASR", file=sys.stderr)
    return []


# ---------- 小红书相关 ----------

def resolve_xiaohongshu_url(url: str) -> str:
    """解析小红书短链接，获取重定向后的实际 URL"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": HEADERS["User-Agent"],
        })
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        resp = opener.open(req, timeout=10)
        return resp.url
    except Exception as e:
        print(f"[!] 解析小红书短链接失败: {e}", file=sys.stderr)
        return url


def fetch_xiaohongshu_info(url: str) -> dict:
    """获取小红书视频信息（通过网页解析，无需API Key）"""
    # 短链接解析
    if "xhslink.com" in url or "xhs.cn" in url:
        url = resolve_xiaohongshu_url(url)
        print(f"[*] 小红书实际链接: {url}", file=sys.stderr)

    note_id = ""
    m = re.search(r"/(?:explore|discovery/item)/([a-f0-9]+)", url)
    if m:
        note_id = m.group(1)

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": HEADERS["User-Agent"],
            "Referer": "https://www.xiaohongshu.com/",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")

        title = ""
        desc = ""
        author = ""
        duration = 0
        pic = ""

        # 提取标题
        title_m = re.search(r'<title[^>]*>([^<]+)</title>', html)
        if title_m:
            title = title_m.group(1).strip()
            # 清理小红书标题后缀
            for suffix in [" - 小红书", "| 小红书", "- 小红书"]:
                if suffix in title:
                    title = title.split(suffix)[0].strip()

        # 从 SSR 数据提取详细信息
        # 小红书使用 self.__pace_f.push 注入初始数据
        desc_match = re.search(r'"desc"\s*:\s*"([^"]*(?:\\.[^"]*)*)"', html)
        if desc_match:
            desc = desc_match.group(1).replace("\\n", " ").replace('\\"', '"').strip()

        author_match = re.search(r'"nickname"\s*:\s*"([^"]*)"', html)
        if author_match:
            author = author_match.group(1)

        dur_match = re.search(r'"duration"\s*:\s*(\d+)', html)
        if dur_match:
            duration = int(dur_match.group(1)) // 1000

        pic_match = re.search(r'"urlDefault"\s*:\s*"([^"]*)"', html)
        if pic_match:
            pic = pic_match.group(1)

        # 尝试提取标签
        tags = []
        tag_matches = re.findall(r'"name"\s*:\s*"#?([^"]+)"', html)
        if tag_matches:
            tags = list(set(t for t in tag_matches if len(t) > 1 and len(t) < 20))[:10]

        return {
            "platform": "xiaohongshu",
            "video_id": f"xhs_{note_id}" if note_id else f"xhs_{hash(url) % 100000000:08d}",
            "title": title,
            "desc": desc,
            "owner": author,
            "duration_sec": duration,
            "view": 0,
            "like": 0,
            "coin": 0,
            "favorite": 0,
            "share": 0,
            "danmaku": 0,
            "reply": 0,
            "pubdate": 0,
            "pic": pic,
            "tags": tags,
            "extra": {"url": url},
        }
    except Exception as e:
        print(f"[!] 获取小红书视频信息失败: {e}", file=sys.stderr)
        return {
            "platform": "xiaohongshu",
            "video_id": f"xhs_{note_id}" if note_id else f"xhs_{hash(url) % 100000000:08d}",
            "title": "",
            "desc": "",
            "owner": "",
            "duration_sec": 0,
            "view": 0, "like": 0, "coin": 0, "favorite": 0,
            "share": 0, "danmaku": 0, "reply": 0,
            "pubdate": 0, "pic": "",
            "tags": [],
            "extra": {"url": url},
        }


# ---------- 主流程 ----------

def run(url_or_id: str):
    print(f"[*] 正在处理: {url_or_id}", file=sys.stderr)

    platform = detect_platform(url_or_id)
    print(f"[*] 平台: {platform}", file=sys.stderr)

    if platform == "unknown":
        print("[!] 无法识别链接平台。支持：bilibili.com / douyin.com / youtube.com / xiaohongshu.com", file=sys.stderr)
        sys.exit(1)

    # 1. 获取视频信息
    print("[*] 获取视频信息...", file=sys.stderr)

    if platform == "bilibili":
        bvid = extract_bvid(url_or_id)
        print(f"[*] BV号: {bvid}", file=sys.stderr)
        info = fetch_bilibili_info(bvid)
        if info["extra"].get("aid"):
            info["tags"] = fetch_bilibili_tags(info["extra"]["aid"])

    elif platform == "douyin":
        info = fetch_douyin_info(url_or_id)

    elif platform == "youtube":
        info = fetch_youtube_info(url_or_id)

    elif platform == "xiaohongshu":
        info = fetch_xiaohongshu_info(url_or_id)

    # 2. 获取字幕（B站支持API字幕，YouTube尝试但不可靠）
    subtitle_text = ""
    subtitle_plain = ""
    subtitle_status = "无字幕"
    used_lang = ""

    if platform == "bilibili":
        cid = info.get("extra", {}).get("cid")
        if cid:
            print("[*] 获取字幕列表...", file=sys.stderr)
            subtitle_list = fetch_bilibili_subtitle_list(info["video_id"], cid)

            preferred_order = ["zh-CN", "zh-Hans", "zh", "ai-zh", "en", "ai-en"]
            chosen = None
            for lang in preferred_order:
                for sub in subtitle_list:
                    if sub.get("lan", "").lower().startswith(lang.lower()):
                        chosen = sub
                        break
                if chosen:
                    break
            if not chosen and subtitle_list:
                chosen = subtitle_list[0]

            if chosen:
                print(f"[*] 下载字幕: {chosen.get('lan_doc', chosen.get('lan'))}", file=sys.stderr)
                try:
                    body = fetch_subtitle_content(chosen["subtitle_url"])
                    subtitle_text = subtitles_to_text(body)
                    subtitle_plain = subtitles_to_plain(body)
                    subtitle_status = "已提取"
                    used_lang = chosen.get("lan_doc", chosen.get("lan", ""))
                except Exception as e:
                    subtitle_status = f"下载失败: {e}"
            else:
                subtitle_status = "该视频暂无字幕（可能需要登录或UP主未上传）"

    elif platform == "douyin":
        subtitle_status = "抖音无公开字幕API，需通过ASR语音识别获取字幕"

    elif platform == "youtube":
        subtitle_status = "YouTube字幕需通过ASR语音识别获取（API提取不稳定）"

    elif platform == "xiaohongshu":
        subtitle_status = "小红书无公开字幕API，需通过ASR语音识别获取字幕"

    result = {
        "info": info,
        "subtitle": {
            "status": subtitle_status,
            "lang": used_lang,
            "timed_text": subtitle_text,
            "plain_text": subtitle_plain,
            "char_count": len(subtitle_plain),
            "segment_count": subtitle_text.count("\n") + 1 if subtitle_text else 0,
        }
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 video_fetcher.py <视频链接>", file=sys.stderr)
        print("支持: bilibili.com/video/BVxxx | douyin.com/video/xxx | youtube.com/watch?v=xxx | xiaohongshu.com/explore/xxx", file=sys.stderr)
        sys.exit(1)
    run(sys.argv[1])
