#!/usr/bin/env python3
"""v4.1 新增：B站公共 API 字幕直连探测。

为什么需要这个模块：
- yt-dlp --list-subs 在 B站未登录时可能返回空（或只有 danmaku）
- B站公共 API（api.bilibili.com/x/web-interface/view + x/player/v2）
  可以无需登录直接探测 CC 字幕
- 公共 API 是 B站字幕探测最可靠的方式

策略（三层回退）：
1. 公共 API 探测字幕列表（无需登录，最快）
2. 探测到字幕 → 用 yt-dlp 下载字幕文件
3. 探测无字幕 → fallback 到音频下载 + Whisper

参考：
- B站 API 文档: https://socialsisteryi.github.io/bilibili-API-collect/
"""
from __future__ import annotations
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from common import write_json, detect_language


# B站公共 API 端点
BILI_VIEW_API = "https://api.bilibili.com/x/web-interface/view"
BILI_PLAYER_API = "https://api.bilibili.com/x/player/v2"

# 请求头（模拟浏览器，避免被识别为爬虫）
BILI_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.bilibili.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def _http_get_json(url: str, timeout: int = 15) -> Optional[dict]:
    """HTTP GET 请求并解析 JSON。"""
    req = urllib.request.Request(url, headers=BILI_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"   ⚠️ HTTP 请求失败: {e}", file=sys.stderr)
        return None


def get_video_metadata(bvid: str, p: int = 1) -> Optional[dict]:
    """通过 B站公共 API 获取视频元数据（aid, cid, title, duration）。

    Args:
        bvid: B站视频 BV 号
        p: 分 P 编号（从 1 开始）

    Returns:
        {
            "aid": int, "cid": int, "title": str,
            "uploader": str, "duration_sec": float,
            "bvid": str, "p": int,
        }
        失败返回 None
    """
    url = f"{BILI_VIEW_API}?bvid={bvid}"
    data = _http_get_json(url)
    if not data or data.get("code") != 0:
        # 412 错误（反爬虫）时 code != 0
        code = data.get("code") if data else -1
        msg = data.get("message", "") if data else "请求失败"
        if code == -412:
            print(f"   ⚠️ B站公共 API 返回 412（反爬虫），需 fallback 到 yt-dlp", file=sys.stderr)
        else:
            print(f"   ⚠️ B站 view API 错误: code={code} msg={msg}", file=sys.stderr)
        return None

    result = data.get("data", {})
    aid = result.get("aid")
    title = result.get("title", "")
    uploader = result.get("owner", {}).get("name", "")
    duration = float(result.get("duration", 0))
    pages = result.get("pages", [])

    # 获取指定分 P 的 cid
    if p <= len(pages):
        cid = pages[p - 1].get("cid", aid)
    else:
        cid = result.get("cid", aid)

    return {
        "aid": aid,
        "cid": cid,
        "title": title,
        "uploader": uploader,
        "duration_sec": duration,
        "bvid": bvid,
        "p": p,
    }


def probe_subtitle_list(aid: int, cid: int) -> list[dict]:
    """通过 B站 player/v2 API 探测可用字幕列表。

    无需登录即可探测 CC 字幕（包括 UP 主上传的手动字幕
    和 B站 AI 生成的自动字幕）。

    Args:
        aid: 视频 aid
        cid: 视频 cid

    Returns:
        字幕列表，每个元素格式：
        {
            "lan": str,          # 语言代码（zh-Hans, en, ai-zh 等）
            "lan_doc": str,      # 语言显示名（简体中文, English 等）
            "subtitle_url": str, # 字幕 JSON URL（完整 URL）
            "ai_type": int,      # 0=手动字幕，1=AI 字幕
        }
        无字幕返回空列表
    """
    url = f"{BILI_PLAYER_API}?aid={aid}&cid={cid}"
    data = _http_get_json(url)

    if not data or data.get("code") != 0:
        code = data.get("code") if data else -1
        if code == -412:
            print(f"   ⚠️ B站 player API 返回 412（反爬虫）", file=sys.stderr)
        elif code != 0:
            msg = data.get("message", "") if data else "请求失败"
            print(f"   ⚠️ B站 player API 错误: code={code} msg={msg}", file=sys.stderr)
        return []

    subtitle_info = data.get("data", {}).get("subtitle", {})
    subtitles = subtitle_info.get("subtitles", [])

    result = []
    for sub in subtitles:
        lan = sub.get("lan", "")
        lan_doc = sub.get("lan_doc", "")
        sub_url = sub.get("subtitle_url", "")
        ai_type = sub.get("ai_type", 0)

        # 补全 URL（B站 API 返回的是 // 开头）
        if sub_url and not sub_url.startswith("http"):
            sub_url = "https:" + sub_url

        result.append({
            "lan": lan,
            "lan_doc": lan_doc,
            "subtitle_url": sub_url,
            "ai_type": ai_type,
        })

    return result


def pick_best_subtitle(subtitles: list[dict]) -> Optional[dict]:
    """从字幕列表中选出最佳字幕（语言优先级）。"""
    if not subtitles:
        return None

    # 语言优先级
    priority = ["zh-Hans", "zh-CN", "zh", "zh-Hant", "ai-zh", "en", "en-US", "ja", "ko"]

    for lang in priority:
        for sub in subtitles:
            if sub["lan"] == lang:
                return sub

    # fallback: 选第一个
    return subtitles[0]


def download_bilibili_subtitle(subtitle_url: str, output_path: Path) -> bool:
    """下载 B站字幕 JSON 并转换为 SRT 格式。

    B站字幕 JSON 格式：
    {
        "body": [
            {"from": 0.5, "to": 2.1, "content": "字幕内容"},
            ...
        ]
    }

    Args:
        subtitle_url: 字幕 JSON URL
        output_path: 输出 SRT 文件路径

    Returns:
        成功返回 True
    """
    data = _http_get_json(subtitle_url)
    if not data:
        return False

    body = data.get("body", [])
    if not body:
        return False

    # 转换为 SRT 格式
    srt_lines = []
    for i, item in enumerate(body, 1):
        start = float(item.get("from", 0))
        end = float(item.get("to", start + 1))
        content = item.get("content", "").strip()
        if not content:
            continue

        srt_lines.append(str(i))
        srt_lines.append(f"{_format_srt_time(start)} --> {_format_srt_time(end)}")
        srt_lines.append(content)
        srt_lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(srt_lines), encoding="utf-8")
    return True


def _format_srt_time(seconds: float) -> str:
    """秒数 → SRT 时间码 (HH:MM:SS,mmm)。"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def fetch_bilibili_subtitle_via_api(
    bvid: str,
    p: int,
    video_id: str,
    transcript_dir: Path,
) -> Optional[dict]:
    """v4.1：通过 B站公共 API 拉取字幕。

    完整流程：
    1. get_video_metadata(bvid, p) → 获取 aid, cid, title, uploader
    2. probe_subtitle_list(aid, cid) → 探测字幕列表
    3. pick_best_subtitle → 选最佳字幕
    4. download_bilibili_subtitle → 下载并转 SRT
    5. SRT → transcript_N.json（复用 srt_to_transcript）

    Args:
        bvid: B站视频 BV 号
        p: 分 P 编号
        video_id: 视频编号（用于文件命名）
        transcript_dir: transcript 输出目录

    Returns:
        成功返回 dict（含 transcript_path, title, uploader, language 等）
        失败返回 None
    """
    # 1. 获取元数据
    meta = get_video_metadata(bvid, p)
    if not meta:
        return None

    aid = meta["aid"]
    cid = meta["cid"]
    title = meta["title"]
    uploader = meta["uploader"]
    duration = meta["duration_sec"]

    print(f"   📺 标题: {title[:60]}", flush=True)
    print(f"   👤 UP主: {uploader}", flush=True)
    print(f"   ⏱ 时长: {duration:.1f}s", flush=True)

    # 2. 探测字幕
    print(f"   🔍 探测 B站 CC 字幕（公共 API）...", flush=True)
    subtitles = probe_subtitle_list(aid, cid)
    if not subtitles:
        print(f"   ℹ️ 无 CC 字幕（UP主未上传，B站 AI 也未生成）", flush=True)
        return None

    print(f"   📝 找到 {len(subtitles)} 条字幕:", flush=True)
    for s in subtitles:
        kind = "AI" if s["ai_type"] else "手动"
        print(f"      - [{kind}] {s['lan_doc']} (lan={s['lan']})", flush=True)

    # 3. 选最佳字幕
    best = pick_best_subtitle(subtitles)
    if not best:
        return None

    print(f"   ✅ 选用: {best['lan_doc']}", flush=True)

    # 4. 下载字幕
    subs_dir = transcript_dir.parent / "subs"
    subs_dir.mkdir(parents=True, exist_ok=True)
    srt_path = subs_dir / f"subtitle_{video_id}.srt"

    if not download_bilibili_subtitle(best["subtitle_url"], srt_path):
        print(f"   ⚠️ 字幕下载失败", flush=True)
        return None

    print(f"   💾 SRT 已保存: {srt_path.name}", flush=True)

    # 5. SRT → transcript
    from srt_to_transcript import srt_to_transcript

    # 判断字幕来源类型
    subtitle_kind = "ai" if best["ai_type"] else "manual"
    model_name = f"bilibili-{subtitle_kind}"

    # 判断字幕语言
    lang_code = best["lan"]
    if lang_code.startswith("zh") or lang_code == "ai-zh":
        language = "zh"
    elif lang_code.startswith("en"):
        language = "en"
    elif lang_code.startswith("ja"):
        language = "ja"
    elif lang_code.startswith("ko"):
        language = "ko"
    else:
        language = detect_language("")

    try:
        transcript = srt_to_transcript(
            srt_path=srt_path,
            title=title,
            author=uploader,
            source_url=f"https://www.bilibili.com/video/{bvid}?p={p}",
            source_type="subtitle",
            model=model_name,
            duration_sec=duration,
            video_id=video_id,  # v4.0 bug 修复
        )
    except Exception as e:
        print(f"   ⚠️ SRT→transcript 转换失败: {e}", flush=True)
        return None

    # 写入 transcript_N.json
    transcript_path = transcript_dir / f"transcript_{video_id}.json"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(transcript_path, transcript)

    # 重新检测语言（srt_to_transcript 可能已检测）
    actual_language = transcript.get("language", language)

    print(
        f"   ✅ 字幕转录完成: {transcript_path.name} "
        f"({len(transcript['segments'])} segments, lang={actual_language})",
        flush=True,
    )

    return {
        "success": True,
        "transcript_path": transcript_path,
        "srt_path": srt_path,
        "title": title,
        "author": uploader,
        "duration_sec": duration,
        "language": actual_language,
        "source_type": "subtitle",
        "subtitle_kind": subtitle_kind,
        "subtitle_lang": lang_code,
    }


if __name__ == "__main__":
    # 自测
    import argparse
    parser = argparse.ArgumentParser(description="B站公共 API 字幕探测测试")
    parser.add_argument("bvid", help="B站视频 BV 号")
    parser.add_argument("--p", type=int, default=1, help="分 P 编号")
    args = parser.parse_args()

    print(f"测试 BVID: {args.bvid} p={args.p}")
    meta = get_video_metadata(args.bvid, args.p)
    if meta:
        print(f"元数据: {meta}")
        subs = probe_subtitle_list(meta["aid"], meta["cid"])
        print(f"字幕数: {len(subs)}")
        for s in subs:
            print(f"  - {s}")
    else:
        print("获取元数据失败")
