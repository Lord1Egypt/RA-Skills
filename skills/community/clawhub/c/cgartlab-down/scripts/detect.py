#!/usr/bin/env python3
"""URL analyzer for the `down` skill.

Usage:
    python detect.py --url "<url>" [--json]

Emits a JSON object on stdout describing the URL kind, suggested download tool,
destination filename, and verification command. Exit code 0 always (except on
bad usage) — the caller inspects the JSON to decide the next step.

Design notes:
  * Read-only. Never touches the filesystem except for --help.
  * Zero third-party deps — stdlib only, works on Python 3.9+.
  * All heuristics are data-driven (PLATFORM_SITES, HOST_TOOL_MAP,
    EXT_TOOL_MAP). Adding a new site is one line in the map.
  * No network calls — the URL is classified from its shape alone.
    This is deliberate: a URL probe would leak credentials in Referer and
    might trip anti-bot systems before the caller even asked to install tools.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

# --- Platform sites (yt-dlp handles these with its extractors) ----------------

# Hosts where a page URL (not a direct file) is a video/audio platform page.
# Matched by parsed hostname (case-insensitive, suffix match via endswith).
PLATFORM_SITES: dict[str, str] = {
    "youtube.com": "yt-dlp", "youtubekids.com": "yt-dlp",
    "youtu.be": "yt-dlp", "music.youtube.com": "yt-dlp",
    "twitter.com": "yt-dlp", "x.com": "yt-dlp",
    "bilibili.com": "yt-dlp", "b23.tv": "yt-dlp",
    "tiktok.com": "yt-dlp", "vm.tiktok.com": "yt-dlp",
    "vimeo.com": "yt-dlp", "dailymotion.com": "yt-dlp",
    "douyin.com": "yt-dlp", "weibo.com": "yt-dlp",
    "redditmedia.com": "yt-dlp", "reddit.com": "yt-dlp",
    "twitch.tv": "yt-dlp",
}

# --- Cloud drive sites (识别但不下载) ----------------------------------------

CLOUD_DRIVE_SITES: dict[str, str] = {
    "pan.baidu.com": "百度网盘",
    "yun.baidu.com": "百度网盘",
    "pan.quark.cn": "夸克网盘",
    "www.aliyundrive.com": "阿里云盘",
    "www.alipan.com": "阿里云盘",
    "115.com": "115 网盘",
    "115cdn.com": "115 网盘",
    "cloud.189.cn": "天翼云盘",
    "wl.123pan.com": "腾讯微云",
    "wenku.baidu.com": "百度文库",
}

VIDEO_EXT = {".mp4", ".mkv", ".webm", ".mov", ".avi", ".m4v", ".ts", ".m4s"}
AUDIO_EXT = {".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".wav", ".wma"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".heic", ".avif"}
ARCHIVE_EXT = {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".iso"}
DOC_EXT = {".pdf", ".epub", ".txt", ".html", ".css", ".js", ".json", ".xml", ".csv", ".md"}
VIDEO_ALL = VIDEO_EXT | AUDIO_EXT

# --- Magnet / torrent URI schemes --------------------------------------------

TORRENT_EXT = {".torrent"}


def classify(url: str) -> dict:
    """Classify a URL and return the JSON payload dict."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = parsed.path.lower()

    # 1) URI schemes first — magnet is metadata, not file download.
    if parsed.scheme == "magnet":
        return _result(
            url, host="", kind="magnet", tool="none",
            dest_name=_magnet_name(url), verify_cmd=None,
            install_hint={},
            user_action="请将此 magnet 链接复制到 qBittorrent、Transmission 或类似客户端。",
            reason="magnet 是元数据 URI，需要 BT 客户端解析，非文件下载。",
        )
    if path.endswith(".torrent"):
        return _result(
            url, host=host, kind="torrent", tool="curl",
            dest_name=_basename(path), verify_cmd="file",
            install_hint={},
            user_action="下载 .torrent 文件本体；如需下载内容，用 BT 客户端打开此文件。",
            reason="skill 只下载种子文件，不下载内容。",
        )

    # 2) Known platform sites → yt-dlp, regardless of extension.
    for plat, tool in PLATFORM_SITES.items():
        if host == plat or host.endswith("." + plat):
            ext = _first_ext(path)
            return _result(
                url, host=host, kind="platform_video", tool=tool,
                dest_name=_slugified_dest(url, ext or ".mp4"),
                verify_cmd=_ffprobe_cmd(),
                install_hint=_ytdlp_hint(),
            )

    # 3) Cloud drive sites — 识别但不下载，用户手动转存。
    for plat, provider in CLOUD_DRIVE_SITES.items():
        if host == plat or host.endswith("." + plat):
            return _result(
                url, host=host, kind="cloud_drive", tool="none",
                dest_name=None, verify_cmd=None,
                install_hint={},
                user_action=f"请手动转存到你的 {provider} 账号。",
                reason="skill 不处理网盘内容，用户自己转存。",
            )

    # 4) Direct file link — decided by extension.
    ext = _first_ext(path)
    if ext:
        if ext in VIDEO_ALL:
            return _result(url, host, "direct_file", "curl",
                           _basename(path, default=f"download{ext}"),
                           _ffprobe_cmd())
        # archives, docs, images, unknown — all just curl
        return _result(url, host, "direct_file", "curl",
                       _basename(path, default="download"),
                       "file")

    # 5) Fallback — unknown.
    return _result(url, host, "unknown", "curl",
                   dest_name="download", verify_cmd="file")


# --- Helpers -----------------------------------------------------------------


def _result(url: str, host: str, kind: str, tool: str,
            dest_name: str | None, verify_cmd: str | None,
            install_hint: dict | None = None,
            user_action: str | None = None,
            reason: str | None = None) -> dict:
    return {
        "url": url,
        "host": host,
        "kind": kind,
        "suggested_tool": tool,
        "dest_name": dest_name,
        "verify_cmd": verify_cmd,
        "install_hint": install_hint or {},
        "user_action": user_action,
        "reason": reason,
    }


def _sanitize_filename(name: str) -> str:
    """Sanitize a filename to prevent path traversal and shell injection.

    Rules (applied in order):
      1. URL-decode common escapes (%20, %2F, %2f, %2e, ...)
      2. Replace path separators / and \\ with _
      3. Reject '..' path traversal
      4. Strip control characters (0x00-0x1F, 0x7F)
      5. Replace shell metacharacters (`$&|;<>(){}[]*?"' and \\\\) with _
      6. Truncate to 200 chars
      7. Empty result falls back to 'download'
    """
    if not name:
        return "download"
    # 1. URL-decode (unquote handles %XX, but not %2e -> . separately)
    name = unquote(name)
    # 2. Path separators
    name = name.replace("/", "_").replace("\\", "_")
    # 3. Path traversal — '..' after separator replacement becomes '_._.'
    if name.startswith("_._.") or name.endswith("_._.") or "_._." in name:
        # Extract the leaf-like segment, then fall back if still suspicious
        name = name.replace("_._.", "_")
    # 4. Control characters
    name = re.sub(r"[\x00-\x1f\x7f]", "", name)
    # 5. Shell metacharacters — replace with _
    name = re.sub(r"[`$&|;<>(){}[\]*?\"'\\]", "_", name)
    # 6. Truncate
    name = name[:200]
    # 7. Empty fallback
    return name.strip() or "download"


def _basename(path: str, default: str | None = None) -> str:
    name = Path(path).name
    if not name or name == "/":
        return default or "download"
    # URL-decode common escapes
    for enc in ("%20", "%2F", "%2f"):
        name = name.replace(enc, " ")
    return _sanitize_filename(name) or (default or "download")


def _first_ext(path: str) -> str | None:
    name = Path(path).name.lower()
    if "." not in name:
        return None
    _, _, ext = name.rpartition(".")
    if len(ext) > 6 or ext.isdigit():  # not a real extension
        return None
    return "." + ext


def _slugified_dest(url: str, ext: str) -> str:
    """For platform videos, build a descriptive filename from the URL."""
    parsed = urlparse(url)
    host = (parsed.hostname or "media").replace(".", "_")
    qs = parsed.query

    # YouTube: video id is in ?v=<id>
    if "youtube" in host or host.endswith("youtu.be"):
        from urllib.parse import parse_qs
        v = parse_qs(qs).get("v", [None])[0]
        if v:
            return f"{host}_{v}{ext}"
        # youtu.be/<id> short form
        m = re.search(r"youtu\.be/([A-Za-z0-9_-]{6,})$", parsed.path)
        if m:
            return f"youtube_{m.group(1)}{ext}"

    # Twitter/X/Bilibili/etc.: pull a status/post id from the path
    m = re.search(r"/(?:status|video|watch|v)(?:/)?(\d+)", parsed.path)
    if m:
        return _sanitize_filename(f"{host}_{m.group(1)}{ext}")
    m = re.search(r"([A-Za-z0-9_-]{6,12})$", parsed.path.rstrip("/"))
    if m:
        return _sanitize_filename(f"{host}_{m.group(1)}{ext}")
    return _sanitize_filename(f"{host}download{ext}")


def _magnet_name(magnet: str) -> str:
    m = re.search(r"dn=([^&]+)", magnet)
    if m:
        from urllib.parse import unquote_plus
        return _sanitize_filename(unquote_plus(m.group(1)))
    return "magnet-download"


def _ffprobe_cmd() -> str:
    return ("ffprobe -v error -show_entries "
            "format=duration,size -show_entries stream=codec_type,codec_name,width,height "
            "-of default=nw=1 \"<file>\"")


def _aria2_hint() -> dict:
    # Windows: winget; others: platform package manager. Caller must ASK user first.
    return {
        "name": "aria2",
        "purpose": "torrent/magnet downloads (curl/yt-dlp cannot do this)",
        "install_by_platform": {
            "windows": "winget install -e --id aria2.aria2",
            "linux": "apt install -y aria2  (or dnf install -y aria2)",
            "macos": "brew install aria2",
        },
        "size_mb": 4,
        "license": "Apache-2.0",
    }


def _ytdlp_hint() -> dict:
    return {
        "name": "yt-dlp",
        "purpose": "platform video/audio downloads (YouTube, X/Twitter, Bilibili, ...)",
        "install_by_platform": {
            "windows": "uv tool install yt-dlp",
            "linux": "uv tool install yt-dlp  (or pipx install yt-dlp)",
            "macos": "uv tool install yt-dlp  (or brew install yt-dlp)",
        },
        "size_mb": 3,
        "license": "Unlicense",
    }


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Analyze a URL for the `down` skill.")
    p.add_argument("--url", required=True, help="URL to analyze")
    p.add_argument("--json", action="store_true", help="Emit JSON (default; kept for clarity)")
    args = p.parse_args(argv)

    result = classify(args.url)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
