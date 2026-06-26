#!/usr/bin/env python3
"""Download Douyin videos by extracting video source URLs via headless browser.

Usage:
    python3 scripts/douyin_download.py <douyin_url> [--output-dir DIR] [--filename NAME]

Requires: agent-browser (npm i -g agent-browser)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse


def run(cmd: str, timeout: int = 30) -> str:
    """Run a shell command and return stdout."""
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()


def run_check(cmd: str, timeout: int = 30) -> str:
    """Run a shell command and raise on failure."""
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{r.stderr}")
    return r.stdout.strip()


def normalize_url(url: str) -> tuple[str, str | None]:
    """Normalize Douyin URL → (direct_video_url, video_id).

    Supports:
    - https://www.douyin.com/video/<id>
    - https://www.douyin.com/search/...?modal_id=<id>
    - https://v.douyin.com/<short_code>  (share links)
    - https://www.douyin.com/note/<id>
    """
    parsed = urllib.parse.urlparse(url)

    # Direct video URL
    m = re.search(r'/video/(\d+)', parsed.path)
    if m:
        return f"https://www.douyin.com/video/{m.group(1)}", m.group(1)

    # Note URL
    m = re.search(r'/note/(\d+)', parsed.path)
    if m:
        return f"https://www.douyin.com/note/{m.group(1)}", m.group(1)

    # Search page with modal_id
    qs = urllib.parse.parse_qs(parsed.query)
    if 'modal_id' in qs:
        vid = qs['modal_id'][0]
        return f"https://www.douyin.com/video/{vid}", vid

    # Short share link (v.douyin.com) — open as-is, browser will redirect
    if 'v.douyin.com' in parsed.netloc:
        return url, None

    # Fallback: try as-is
    return url, None


def extract_video_src(timeout: int = 30) -> str | None:
    """Extract video source URL from the current browser page."""
    js = r'JSON.stringify([...document.querySelectorAll("video")].map(v=>({src:v.src,currentSrc:v.currentSrc})))'
    out = run(f'agent-browser eval \'{js}\'', timeout=timeout)
    try:
        videos = json.loads(json.loads(out))  # double-parsed: CLI wraps in quotes
    except (json.JSONDecodeError, TypeError):
        try:
            videos = json.loads(out)
        except (json.JSONDecodeError, TypeError):
            return None

    for v in videos:
        src = v.get('currentSrc') or v.get('src')
        if src and ('douyinvod.com' in src or 'bytevcloudcdn.com' in src or '.mp4' in src):
            return src
    return None


def sanitize_filename(name: str) -> str:
    """Remove illegal filename characters and truncate."""
    name = re.sub(r'[\\/:*?"<>|\n\r\t]', '', name)
    name = name.strip('. ')
    return name[:80] if name else 'douyin_video'


def main():
    parser = argparse.ArgumentParser(description='Download Douyin short videos')
    parser.add_argument('url', help='Douyin video URL (supports various formats)')
    parser.add_argument('--output-dir', '-o', default=os.path.expanduser('~/Downloads'),
                        help='Output directory (default: ~/Downloads)')
    parser.add_argument('--filename', '-f', default=None,
                        help='Output filename without extension (auto-detected from page title if omitted)')
    parser.add_argument('--timeout', '-t', type=int, default=60,
                        help='Browser page load timeout in seconds (default: 60)')
    args = parser.parse_args()

    url, video_id = normalize_url(args.url)
    print(f"📎 URL: {url}")
    if video_id:
        print(f"🆔 Video ID: {video_id}")

    # Step 1: Open page in headless browser
    print("🌐 Opening page in browser...")
    try:
        out = run_check(f"agent-browser open '{url}'", timeout=args.timeout)
        print(f"   Page loaded: {out[:100]}...")
    except RuntimeError as e:
        print(f"❌ Failed to open page: {e}", file=sys.stderr)
        sys.exit(1)

    # Step 2: Wait for video element
    print("🔍 Extracting video source...")
    video_src = None
    for attempt in range(3):
        video_src = extract_video_src(timeout=15)
        if video_src:
            break
        print(f"   Retry {attempt + 1}/3...")
        time.sleep(2)

    if not video_src:
        print("❌ Could not find video source URL on page", file=sys.stderr)
        run("agent-browser close")
        sys.exit(1)

    print(f"✅ Video source found ({len(video_src)} chars)")

    # Step 3: Get page title for filename
    if not args.filename:
        title_out = run("agent-browser get title")
        title = title_out.replace(' - 抖音', '').strip()
        filename = sanitize_filename(title) if title else f"douyin_{video_id or 'video'}"
    else:
        filename = args.filename

    # Step 4: Close browser
    run("agent-browser close")

    # Step 5: Download with curl
    output_path = os.path.join(args.output_dir, f"{filename}.mp4")
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"⬇️  Downloading to: {output_path}")
    dl_cmd = (
        f"curl -L -o '{output_path}' "
        f"-H 'Referer: https://www.douyin.com/' "
        f"-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' "
        f"'{video_src}'"
    )
    r = subprocess.run(dl_cmd, shell=True, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print(f"❌ Download failed: {r.stderr}", file=sys.stderr)
        sys.exit(1)

    # Verify
    size = os.path.getsize(output_path)
    if size < 1024:
        print(f"⚠️  File too small ({size} bytes), download may have failed", file=sys.stderr)
        sys.exit(1)

    size_mb = size / (1024 * 1024)
    print(f"✅ Done! {output_path} ({size_mb:.1f} MB)")


if __name__ == '__main__':
    main()
