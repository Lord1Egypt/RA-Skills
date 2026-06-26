#!/usr/bin/env python3
"""
bilibili_fetcher.py - 哔哩哔哩视频信息与字幕提取工具

用法:
    python3 bilibili_fetcher.py <bilibili_url_or_bvid>

输出:
    JSON 格式的视频信息 + 字幕内容（打印到 stdout）

依赖:
    - requests（标准 pip 包）
    - 无需登录，但部分视频需要登录才有字幕（会提示）

示例:
    python3 bilibili_fetcher.py https://www.bilibili.com/video/BV1xx411c7mD
    python3 bilibili_fetcher.py BV1xx411c7mD
"""

import sys
import re
import json
import time
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


def http_get(url: str, params: dict = None) -> dict:
    """发起 GET 请求并返回解析后的 JSON"""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def extract_bvid(text: str) -> str:
    """从 URL 或原始字符串中提取 BV 号"""
    # 支持格式: BVxxxxxxxx / /video/BVxxxx / ?bvid=BVxxxx
    m = re.search(r"(BV[0-9A-Za-z]{10})", text)
    if m:
        return m.group(1)
    raise ValueError(f"无法从 '{text}' 中提取 BV 号，请确认链接格式正确。")


# ---------- 视频基本信息 ----------

def fetch_video_info(bvid: str) -> dict:
    """获取视频基本信息"""
    data = http_get(
        "https://api.bilibili.com/x/web-interface/view",
        {"bvid": bvid}
    )
    if data.get("code") != 0:
        raise RuntimeError(f"API 错误: {data.get('message', '未知错误')}")
    v = data["data"]
    return {
        "bvid": bvid,
        "aid": v.get("aid"),
        "cid": v["pages"][0]["cid"] if v.get("pages") else None,
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
        "tags": [],  # 后续填充
    }


def fetch_tags(aid: int) -> list:
    """获取视频标签"""
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


# ---------- 字幕提取 ----------

def fetch_subtitle_list(bvid: str, cid: int) -> list:
    """获取字幕列表（返回可用字幕的 URL 列表）"""
    data = http_get(
        "https://api.bilibili.com/x/player/v2",
        {"bvid": bvid, "cid": cid}
    )
    if data.get("code") != 0:
        return []
    subtitle_info = data.get("data", {}).get("subtitle", {})
    subtitles = subtitle_info.get("subtitles", [])
    return subtitles  # [{lan, lan_doc, subtitle_url}, ...]


def fetch_subtitle_content(subtitle_url: str) -> list:
    """下载并解析字幕 JSON，返回字幕段列表"""
    # B站字幕 URL 可能是 // 开头
    if subtitle_url.startswith("//"):
        subtitle_url = "https:" + subtitle_url
    req = urllib.request.Request(subtitle_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    return data.get("body", [])  # [{from, to, content}, ...]


def subtitles_to_text(body: list) -> str:
    """将字幕段列表转换为纯文本（按时间顺序拼接）"""
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


# ---------- 主流程 ----------

def run(url_or_bvid: str):
    print(f"[*] 正在处理: {url_or_bvid}", file=sys.stderr)

    bvid = extract_bvid(url_or_bvid)
    print(f"[*] BV号: {bvid}", file=sys.stderr)

    # 1. 视频基本信息
    print("[*] 获取视频信息...", file=sys.stderr)
    info = fetch_video_info(bvid)

    # 2. 标签
    if info.get("aid"):
        info["tags"] = fetch_tags(info["aid"])

    # 3. 字幕
    subtitle_text = ""
    subtitle_plain = ""
    subtitle_status = "无字幕"
    used_lang = ""

    cid = info.get("cid")
    if cid:
        print("[*] 获取字幕列表...", file=sys.stderr)
        subtitle_list = fetch_subtitle_list(bvid, cid)

        # 优先选中文字幕
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
        print("用法: python3 bilibili_fetcher.py <B站链接或BV号>", file=sys.stderr)
        sys.exit(1)
    run(sys.argv[1])
