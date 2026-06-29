#!/usr/bin/env python3
"""
downloader.py - 抖音视频下载 helper
====================================

职责(单一):
  1. fetch_video_url(aweme_id)  → 拿无水印 play_addr(1080p) 或带水印 download_addr(720p)
  2. download_to(url, dest)     → 流式下载到本地,带 douyin 必须的 Referer 头

被 douyin-fetch.py (video 子命令) 和 comments-harvest.py 复用。
所有产物落盘路径由调用方决定 —— 本模块只负责"把流拉到 dest",不决定 dest 在哪。

注意:
  - 抖音视频 URL 带 dy_q= 过期戳(默认 ~2 小时有效),fetch_url → download 必须连贯
  - 必须 Referer: https://www.douyin.com/ 否则 403
  - 大文件(1080p 通常 100~200MB)必须 stream + chunk,不要一次性 read()
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode

import requests

# 与 douyin-fetch.py 的 UA / 通用参数保持一致
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REFERER = "https://www.douyin.com/"
DETAIL_BASE = "https://www.douyin.com/aweme/v1/web/aweme/detail/"
COMMON_PARAMS = {
    "device_platform": "webapp", "aid": "6383", "channel": "channel_pc_web",
    "pc_client_type": "1", "version_code": "170400", "version_name": "17.4.0",
    "cookie_enabled": "true", "screen_width": "1536", "screen_height": "864",
    "browser_language": "zh-CN", "browser_platform": "Linux+x86_64",
    "browser_name": "Chrome", "browser_version": "120.0.0.0",
    "browser_online": "true", "engine_name": "Blink", "engine_version": "120.0.0.0",
    "os_name": "Linux", "os_version": "x86_64", "device_memory": "16",
    "platform": "PC", "downlink": "10", "effective_type": "4g",
    "round_trip_time": "50",
}


def _err(msg: str):
    print(f"❌ {msg}", file=sys.stderr)


def _ok(msg: str):
    print(f"✅ {msg}")


def _safe_filename(s: str, max_len: int = 40) -> str:
    """把视频标题变成 filesystem 安全的 slug"""
    if not s:
        return "untitled"
    # 去掉 hashtag / emoji / 路径分隔符 / 不可见字符
    out = []
    for ch in s:
        if ch.isalnum() or ch in ("-", "_", "."):
            out.append(ch)
        elif ch in (" ", "\n", "\t"):
            out.append("_")
        # 其他(中文 / emoji / 标点)保留 — 现代 fs 都支持
        else:
            out.append(ch)
    slug = "".join(out).strip("._-")
    if len(slug) > max_len:
        slug = slug[:max_len].rstrip("._-")
    return slug or "untitled"


def build_dest_path(dest_dir: Path, aweme_id: str, title: str,
                    quality: str = "play") -> Path:
    """构造 <dest_dir>/<aweme_id>_<slug>_<quality>.mp4"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    slug = _safe_filename(title)
    return dest_dir / f"{aweme_id}_{slug}_{quality}.mp4"


def fetch_video_url(aweme_id: str, cookie: str,
                    quality: str = "play") -> Optional[dict]:
    """从 detail API 拿视频 URL。

    quality:
      - "play"     → play_addr     1080p 无水印(默认)
      - "download" → download_addr 720p  带水印

    返回 dict: {url, height, data_size, quality, uri}
    返回 None 表示拿不到(视频不存在 / detail API 不可用)
    """
    params = {"aweme_id": aweme_id, **COMMON_PARAMS}
    url = f"{DETAIL_BASE}?{urlencode(params)}"
    try:
        r = requests.get(
            url, headers={
                "User-Agent": UA, "Referer": REFERER,
                "Cookie": cookie, "Accept": "application/json",
            },
            timeout=15,
        )
    except Exception as e:
        _err(f"detail API 请求失败 (aweme_id={aweme_id}): {e}")
        return None
    if r.status_code != 200:
        _err(f"detail API HTTP {r.status_code} (aweme_id={aweme_id})")
        return None
    try:
        resp = r.json()
    except Exception as e:
        _err(f"detail API 响应非 JSON (aweme_id={aweme_id}): {e}")
        return None
    detail = (resp or {}).get("aweme_detail") or {}
    if not detail:
        _err(f"detail API 返回空 (aweme_id={aweme_id})")
        return None
    v = detail.get("video") or {}
    if quality == "download":
        addr = v.get("download_addr") or {}
    else:
        addr = v.get("play_addr") or {}
    urls = addr.get("url_list") or []
    if not urls:
        _err(f"视频无 {quality}_addr URL(可能视频被删 / 转私密 / live 重放)")
        return None
    return {
        "url": urls[0],
        "height": addr.get("height"),
        "data_size": addr.get("data_size"),
        "quality": quality,
        "uri": addr.get("uri"),
        "title": detail.get("desc", ""),
        "author": (detail.get("author") or {}).get("nickname", ""),
        "duration_ms": v.get("duration"),
    }


def download_to(url: str, dest: Path, label: str = "video",
                timeout: int = 300, chunk_size: int = 1024 * 256) -> dict:
    """流式下载到 dest(覆盖已存在的)。返回 {path, size, time_sec, http_code}。

    必须 Referer 才能拿到 200,否则 403。
    """
    if dest.exists():
        _ok(f"{label} 已存在,跳过下载: {dest}")
        return {
            "path": str(dest), "size": dest.stat().st_size,
            "time_sec": 0.0, "http_code": 200, "cached": True,
        }
    t0 = time.time()
    try:
        with requests.get(
            url, headers={"User-Agent": UA, "Referer": REFERER},
            stream=True, timeout=timeout,
        ) as r:
            if r.status_code != 200:
                _err(f"{label} 下载失败: HTTP {r.status_code}")
                # 删掉可能的半成品
                if dest.exists():
                    dest.unlink()
                return {
                    "path": None, "size": 0, "time_sec": time.time() - t0,
                    "http_code": r.status_code, "cached": False,
                }
            written = 0
            with dest.open("wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        written += len(chunk)
            elapsed = time.time() - t0
            speed_mb = (written / 1024 / 1024) / elapsed if elapsed > 0 else 0
            _ok(f"{label} 下载完成: {dest.name}  "
                f"({written/1024/1024:.1f}MB / {elapsed:.1f}s / {speed_mb:.1f}MB/s)")
            return {
                "path": str(dest), "size": written, "time_sec": elapsed,
                "http_code": 200, "cached": False,
            }
    except Exception as e:
        _err(f"{label} 下载异常: {e}")
        if dest.exists():
            dest.unlink()
        return {
            "path": None, "size": 0, "time_sec": time.time() - t0,
            "http_code": -1, "cached": False, "error": str(e),
        }


def download_for_aweme(aweme_id: str, dest_dir: Path, cookie: str,
                       title_hint: str = "", quality: str = "play") -> dict:
    """一键:fetch_url → build_dest → download_to。

    title_hint: 备选标题(若 fetch_video_url 拿不到);通常不必传,detail 自带
    返回:完整的 download 记录(直接放进 JSON / CSV 都行)
    """
    info = fetch_video_url(aweme_id, cookie, quality=quality)
    if not info:
        return {"aweme_id": aweme_id, "ok": False, "error": "fetch_video_url 返回空"}
    title = info.get("title") or title_hint or aweme_id
    dest = build_dest_path(dest_dir, aweme_id, title, quality=quality)
    dl = download_to(info["url"], dest, label=f"{aweme_id} ({quality})")
    return {
        "aweme_id": aweme_id,
        "ok": dl.get("path") is not None,
        "title": title,
        "author": info.get("author", ""),
        "quality": quality,
        "height": info.get("height"),
        "expected_bytes": info.get("data_size"),
        "downloaded_bytes": dl.get("size", 0),
        "download_time_sec": dl.get("time_sec", 0),
        "http_code": dl.get("http_code"),
        "cached": dl.get("cached", False),
        "path": dl.get("path"),  # 落本地路径(None = 失败)
        "url_remote": info["url"],  # 远端 URL(可能已过期,debug 用)
    }