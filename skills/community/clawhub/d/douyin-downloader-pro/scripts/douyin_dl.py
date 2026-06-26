#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
douyin_dl.py — 抖音视频/图集下载器

用法:
    python3 douyin_dl.py "<分享文本/短链/URL>" [-o OUTPUT] [--zip]

特性:
    - 视频: 下载默认 CDN 上的 mp4（原始带水印）
    - 图集: 把所有图片下载到 <标题>_<aweme_id>/ 目录，可选 --zip 打包
    - 自动从分享口令中提取链接，自动跟随短链重定向

实现说明:
    - 解析 iesdouyin.com share 页面里的 window._ROUTER_DATA JSON
    - data path: loaderData["<video|note>_(id)/page"].videoInfoRes.item_list[0]
    - 视频字段: item.video.play_addr.url_list
    - 图集字段: item.images[*].url_list
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile
from pathlib import Path

try:
    import requests
except ImportError:
    sys.stderr.write("[ERROR] 缺少依赖 requests，请执行: pip install requests\n")
    sys.exit(1)


# ---------- 常量 ----------

UA_MOBILE = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
)
UA_PC = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# 如遇风控可在此填入登录后的 cookie 等
EXTRA_HEADERS: dict[str, str] = {
    # "Cookie": "ttwid=...; sessionid=...",
}


# ---------- 工具函数 ----------

def log(msg: str) -> None:
    print(f"[douyin] {msg}", flush=True)


def extract_link(text: str) -> str | None:
    patterns = [
        r"https?://v\.douyin\.com/[A-Za-z0-9_\-]+/?",
        r"https?://(?:www\.)?douyin\.com/(?:video|note)/\d+",
        r"https?://(?:www\.)?iesdouyin\.com/share/(?:video|note|slides)/\d+",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(0).rstrip("/")
    return None


def extract_aweme_id(url: str) -> str | None:
    m = re.search(r"/(?:video|note|slides)/(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"modal_id=(\d+)", url)
    if m:
        return m.group(1)
    return None


def detect_kind(url: str) -> str:
    if "/note/" in url:
        return "note"
    if "/slides/" in url:
        return "note"
    return "video"


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": UA_MOBILE,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        **EXTRA_HEADERS,
    })
    # 先访问首页，让服务器下发 ttwid cookie
    try:
        s.get("https://www.iesdouyin.com/", timeout=10)
    except Exception:
        pass
    return s


def fetch_router_data(session: requests.Session, aweme_id: str, kind: str) -> dict | None:
    url = f"https://www.iesdouyin.com/share/{kind}/{aweme_id}/"
    r = session.get(url, timeout=15, allow_redirects=True)
    if r.status_code != 200:
        return None
    html = r.text
    # window._ROUTER_DATA = { ... }</script>
    m = re.search(r"window\._ROUTER_DATA\s*=\s*({.+?})\s*</script>", html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def find_item(router_data: dict) -> dict | None:
    """从 _ROUTER_DATA 中提取 item_list[0]。"""
    if not isinstance(router_data, dict):
        return None
    loader = router_data.get("loaderData") or {}
    # 1) 优先找 videoInfoRes/item_list 的 key
    for key, val in loader.items():
        if not isinstance(val, dict):
            continue
        info = val.get("videoInfoRes") or val.get("noteInfoRes") or val.get("info")
        if isinstance(info, dict):
            items = info.get("item_list") or info.get("itemList") or []
            if items:
                return items[0]
    # 2) 兜底递归找 item_list
    def _walk(node):
        if isinstance(node, dict):
            if "item_list" in node and isinstance(node["item_list"], list) and node["item_list"]:
                return node["item_list"][0]
            for v in node.values():
                r = _walk(v)
                if r:
                    return r
        elif isinstance(node, list):
            for v in node:
                r = _walk(v)
                if r:
                    return r
        return None
    return _walk(router_data)


def diagnose(router_data: dict) -> str:
    """从 _ROUTER_DATA 中提取风控/不存在等错误描述。"""
    try:
        loader = router_data.get("loaderData") or {}
        for val in loader.values():
            if not isinstance(val, dict):
                continue
            info = val.get("videoInfoRes") or val.get("noteInfoRes")
            if isinstance(info, dict):
                fl = info.get("filter_list") or []
                if fl:
                    reasons = ", ".join(
                        f"{x.get('filter_reason','?')}({x.get('aweme_id','?')})" for x in fl
                    )
                    return f"接口返回 filter_list: {reasons}"
                if info.get("status_code") not in (0, None):
                    return f"接口 status_code={info.get('status_code')}"
        if router_data.get("errors"):
            return f"errors: {router_data.get('errors')}"
    except Exception:
        pass
    return ""


def sanitize_name(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|\r\n\t]", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return (name[:80] or "douyin").rstrip(". ")


def download_file(session: requests.Session, url: str, dest: Path, retries: int = 3) -> bool:
    headers = {"User-Agent": UA_PC, "Referer": "https://www.douyin.com/"}
    for attempt in range(1, retries + 1):
        try:
            with session.get(url, headers=headers, stream=True, timeout=60) as r:
                r.raise_for_status()
                tmp = dest.with_suffix(dest.suffix + ".part")
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(1 << 16):
                        if chunk:
                            f.write(chunk)
                tmp.replace(dest)
            return True
        except Exception as e:
            log(f"  下载失败({attempt}/{retries}): {e}")
    return False


def guess_image_ext(url: str) -> str:
    low = url.lower().split("?", 1)[0]
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".heic"):
        if low.endswith(ext):
            return ext
    return ".jpg"


# ---------- 主处理 ----------

def handle_item(session: requests.Session, item: dict, output_dir: Path, do_zip: bool) -> list[str]:
    desc = item.get("desc") or "douyin"
    aweme_id = str(item.get("aweme_id") or item.get("awemeId") or "unknown")
    title = sanitize_name(desc)

    images = item.get("images")
    saved: list[str] = []

    if images:
        log(f"识别为图集 · 共 {len(images)} 张 · 标题: {title}")
        item_dir = output_dir / f"{title}_{aweme_id}"
        item_dir.mkdir(parents=True, exist_ok=True)
        for idx, img in enumerate(images, 1):
            urls = img.get("url_list") or img.get("urlList") or []
            if not urls:
                log(f"  [{idx:02d}] 无 url_list，跳过")
                continue
            ext = guess_image_ext(urls[0])
            dest = item_dir / f"{idx:02d}{ext}"
            ok = False
            for u in urls:
                if download_file(session, u, dest):
                    ok = True
                    break
            if ok:
                saved.append(str(dest))
                log(f"  [{idx:02d}] {dest.name} OK")
            else:
                log(f"  [{idx:02d}] 全部 url 都失败")

        if do_zip and saved:
            zip_path = output_dir / f"{title}_{aweme_id}.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for fp in saved:
                    zf.write(fp, arcname=Path(fp).relative_to(output_dir))
            log(f"已打包: {zip_path}")
            return [str(zip_path)]
        return saved

    # 视频
    video = item.get("video") or {}
    play_addr = (
        video.get("play_addr")
        or video.get("playAddr")
        or video.get("download_addr")
        or {}
    )
    urls = play_addr.get("url_list") or play_addr.get("urlList") or []
    if not urls:
        log("未找到视频地址（play_addr 为空）")
        return []
    log(f"识别为视频 · 标题: {title}")
    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / f"{title}_{aweme_id}.mp4"
    for u in urls:
        if download_file(session, u, dest):
            saved.append(str(dest))
            log(f"已保存: {dest}")
            return saved
    log("视频下载全部失败")
    return saved


def main() -> int:
    ap = argparse.ArgumentParser(description="抖音视频/图集下载器")
    ap.add_argument("input", help="抖音分享文本、v.douyin.com 短链或 douyin.com URL")
    ap.add_argument("-o", "--output", default="./downloads", help="输出目录（默认 ./downloads）")
    ap.add_argument("--zip", action="store_true", help="图集下载完成后打包为 zip")
    args = ap.parse_args()

    link = extract_link(args.input)
    if not link:
        log("未识别到链接，请检查输入是否包含 v.douyin.com / douyin.com URL")
        return 2
    log(f"提取链接: {link}")

    session = make_session()

    # 跟随重定向
    try:
        r0 = session.get(link, timeout=15, allow_redirects=True)
        final_url = r0.url
    except Exception as e:
        log(f"重定向失败: {e}")
        return 3
    log(f"重定向后: {final_url}")

    aweme_id = extract_aweme_id(final_url)
    if not aweme_id:
        log("无法从最终 URL 提取 aweme_id")
        return 3
    log(f"aweme_id: {aweme_id}")

    primary_kind = detect_kind(final_url)
    candidates = [primary_kind] + (["note"] if primary_kind == "video" else ["video"])

    item: dict | None = None
    last_diag = ""
    for kind in candidates:
        try:
            data = fetch_router_data(session, aweme_id, kind)
        except Exception as e:
            log(f"通过 {kind} 接口请求失败: {e}")
            continue
        if not data:
            log(f"通过 {kind} 接口未拿到 _ROUTER_DATA")
            continue
        item = find_item(data)
        if item:
            log(f"通过 {kind} 接口解析成功")
            break
        last_diag = diagnose(data)
        log(f"通过 {kind} 接口未找到 item_list" + (f" · {last_diag}" if last_diag else ""))

    if not item:
        log("解析失败：" + (last_diag or "可能被风控或 aweme_id 不存在"))
        log("提示：可在脚本顶部 EXTRA_HEADERS 中填入登录后的 Cookie 重试")
        return 4

    output_dir = Path(args.output).expanduser().resolve()
    saved = handle_item(session, item, output_dir, do_zip=args.zip)
    if saved:
        log(f"完成，输出 {len(saved)} 个文件")
        for s in saved:
            print(s)
        return 0
    log("未保存任何文件")
    return 5


if __name__ == "__main__":
    sys.exit(main())
