"""
fetch_subtitle.py — 自包含的 B 站视频字幕获取脚本

用法：
    python fetch_subtitle.py <BVID或B站链接> [--cookie <cookie文件路径>] [--output-dir <输出目录>]

输出：
    成功时打印 JSON，包含 txt/srt/vtt 文件路径及字幕总条数
    失败时打印错误信息并以非0退出码退出

依赖：
    pip install requests
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("❌ 缺少 requests 库，请运行: pip install requests", file=sys.stderr)
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════
# Cookie 管理
# ═══════════════════════════════════════════════════════════════════════

_user_cookie = None


def load_cookie(cookie_path="cookie.txt"):
    """从文件加载 Cookie。按优先级搜索：指定路径 → 当前目录 → 脚本目录。"""
    global _user_cookie

    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        cookie_path,
        os.path.join(os.getcwd(), "cookie.txt"),
        os.path.join(script_dir, "cookie.txt"),
    ]
    # 去重，保持顺序
    seen = set()
    unique = []
    for p in candidates:
        absp = os.path.abspath(p)
        if absp not in seen:
            seen.add(absp)
            unique.append(absp)

    for path in unique:
        try:
            with open(path, "r", encoding="utf-8") as f:
                _user_cookie = f.read().strip()
                if _user_cookie:
                    print(f"✅ 已加载Cookie文件: {path}")
                    return True
        except FileNotFoundError:
            continue
    print("⚠️  未找到 cookie.txt，将以未登录模式尝试（可能无法获取 AI 字幕）", file=sys.stderr)
    return False


def _get_headers(bvid):
    """构造带 Cookie 的请求头。"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Referer": f"https://www.bilibili.com/video/{bvid}",
        "Accept": "application/json, text/plain, */*",
    }
    if _user_cookie:
        headers["Cookie"] = _user_cookie
    return headers


# ═══════════════════════════════════════════════════════════════════════
# 格式转换
# ═══════════════════════════════════════════════════════════════════════

def _fmt_srt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _fmt_vtt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def generate_txt(subtitles):
    return "\n".join(sub["content"] for sub in subtitles)


def generate_srt(subtitles):
    lines = []
    for i, sub in enumerate(subtitles, 1):
        if "from" not in sub or "to" not in sub:
            continue
        start = _fmt_srt(float(sub["from"]))
        end = _fmt_srt(float(sub["to"]))
        lines.append(f"{i}\n{start} --> {end}\n{sub['content']}\n")
    return "\n".join(lines)


def generate_vtt(subtitles):
    lines = ["WEBVTT\n"]
    for sub in subtitles:
        if "from" not in sub or "to" not in sub:
            continue
        start = _fmt_vtt(float(sub["from"]))
        end = _fmt_vtt(float(sub["to"]))
        lines.append(f"{start} --> {end}\n{sub['content']}\n")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
# 字幕获取核心逻辑
# ═══════════════════════════════════════════════════════════════════════

def _get_ai_subtitle(bvid, cid, headers):
    """尝试获取 AI 自动生成的字幕。"""
    # 方法1: wbi/v2 接口
    try:
        url = f"https://api.bilibili.com/x/player/wbi/v2?bvid={bvid}&cid={cid}"
        data = requests.get(url, headers=headers, timeout=10).json()
        subtitles = data.get("data", {}).get("subtitle", {}).get("subtitles", [])
        for sub in subtitles:
            if sub.get("type") == 1:
                sub_url = sub.get("subtitle_url") or sub.get("subtitle_url_v2", "")
                if not sub_url:
                    continue
                if sub_url.startswith("//"):
                    sub_url = "https:" + sub_url
                body = requests.get(sub_url, headers=headers, timeout=10).json()
                if "body" in body:
                    return body["body"]
    except Exception:
        pass

    # 方法2: web-interface/view 接口
    try:
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        resp = requests.get(url, headers=headers, timeout=10).json()
        if resp.get("code") == 0:
            subs = resp.get("data", {}).get("subtitle", {}).get("subtitles", [])
            if subs:
                sub_url = subs[0].get("subtitle_url", "")
                if sub_url.startswith("//"):
                    sub_url = "https:" + sub_url
                if sub_url:
                    body = requests.get(sub_url, headers=headers, timeout=10).json()
                    if "body" in body:
                        return body["body"]
    except Exception:
        pass
    return None


def get_subtitle(bvid, prefer_ai=True):
    """
    获取 B 站视频字幕。

    返回: (subtitle_list, error_msg)
        成功: ([...], None)
        失败: (None, "错误描述")
    """
    headers = _get_headers(bvid)

    try:
        # 第一步：获取 cid
        print(f"📡 正在获取视频 {bvid} 的信息...")
        url_cid = f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}"
        res = requests.get(url_cid, headers=headers, timeout=10).json()
        if res["code"] != 0:
            return None, f"❌ 获取视频信息失败：{res.get('message', '未知错误')}"
        cid = res["data"][0]["cid"]
        print(f"✅ 获取到 cid: {cid}")

        body = None

        # 第二步：优先获取 AI 字幕
        if prefer_ai:
            print("🔍 正在查找 AI 字幕...")
            body = _get_ai_subtitle(bvid, cid, headers)
            if body:
                print("✅ 成功获取 AI 字幕")
            else:
                print("⚠️  未找到 AI 字幕，尝试查找 CC 字幕...")

        # 第三步：获取 CC 字幕
        if not body:
            print("🔍 正在查找 CC 字幕...")
            url = f"https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}"
            info = requests.get(url, headers=headers, timeout=10).json()
            subs = info.get("data", {}).get("subtitle", {}).get("subtitles", [])

            if not subs:
                return None, (
                    "❌ 该视频没有字幕（包括 AI 字幕和 CC 字幕）。\n"
                    "   提示：如果是硬字幕需使用 OCR 工具提取。\n"
                    "   如果视频有 AI 字幕，请配置 cookie.txt 登录 B 站账号。"
                )

            sub_url = subs[0].get("subtitle_url") or subs[0].get("subtitle_url_v2", "")

            # 备用接口
            if not sub_url:
                try:
                    fb_url = f"https://api.bilibili.com/x/player/wbi/v2?bvid={bvid}&cid={cid}"
                    fb = requests.get(fb_url, headers=headers, timeout=10).json()
                    fb_subs = fb.get("data", {}).get("subtitle", {}).get("subtitles", [])
                    if fb_subs:
                        sub_url = fb_subs[0].get("subtitle_url") or fb_subs[0].get("subtitle_url_v2", "")
                except Exception:
                    pass

            if not sub_url:
                return None, "❌ 无法获取字幕 URL，请尝试更新 Cookie。"

            if sub_url.startswith("//"):
                sub_url = "https:" + sub_url

            print("⬇️  正在下载字幕...")
            body = requests.get(sub_url, headers=headers, timeout=10).json().get("body")

        if not body:
            return None, "❌ 获取字幕失败：返回数据为空"

        print(f"✅ 成功获取 {len(body)} 条字幕")
        return body, None

    except requests.exceptions.Timeout:
        return None, "❌ 请求超时，请检查网络连接"
    except requests.exceptions.RequestException as e:
        return None, f"❌ 网络请求失败：{e}"
    except Exception as e:
        return None, f"❌ 发生未知错误：{e}"


# ═══════════════════════════════════════════════════════════════════════
# BVID 解析
# ═══════════════════════════════════════════════════════════════════════

def extract_bvid(text):
    """从文本中提取 BVID（支持链接或纯 BVID）。"""
    match = re.search(r"BV[a-zA-Z0-9]+", text)
    return match.group(0) if match else None


# ═══════════════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="获取 B 站视频字幕（自包含版本）")
    parser.add_argument("input", help="B 站视频链接或 BVID（如 BV1ZL411o7LZ）")
    parser.add_argument("--cookie", default="cookie.txt", help="Cookie 文件路径（默认: ./cookie.txt）")
    parser.add_argument("--output-dir", default="subtitles_output", help="输出目录（默认: ./subtitles_output）")
    args = parser.parse_args()

    # 解析 BVID
    bvid = extract_bvid(args.input)
    if not bvid:
        print(f"❌ 无法从输入中识别 BVID: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 加载 Cookie
    load_cookie(args.cookie)

    # 获取字幕
    subtitles, error = get_subtitle(bvid, prefer_ai=True)
    if error or not subtitles:
        print(error or "❌ 获取字幕失败", file=sys.stderr)
        sys.exit(1)

    # 保存三种格式
    out_dir = os.path.join(args.output_dir, bvid)
    os.makedirs(out_dir, exist_ok=True)

    paths = {}
    for fmt, gen in [("txt", generate_txt), ("srt", generate_srt), ("vtt", generate_vtt)]:
        filepath = os.path.join(out_dir, f"{bvid}.{fmt}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(gen(subtitles))
        paths[fmt] = os.path.abspath(filepath)

    # 输出结果
    result = {"bvid": bvid, "subtitle_count": len(subtitles), "files": paths}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
