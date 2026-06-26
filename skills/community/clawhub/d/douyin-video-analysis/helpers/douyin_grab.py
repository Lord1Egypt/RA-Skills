#!/usr/bin/env python3
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

CHROME_BRIDGE = "/Users/bobzhong/.openclaw/workspace/skills/browser-automation-bridge/scripts/chrome_bridge.py"
TMP_DIR = Path("/tmp/douyin_transcribe")
TMP_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip() or f"command failed: {cmd}")
    return p.stdout.strip()


def chrome_open(url: str):
    run(["python3", CHROME_BRIDGE, "open", url])


def chrome_eval(js: str) -> str:
    return run(["python3", CHROME_BRIDGE, "eval", js])


def fetch_page_snapshot():
    js = r'''JSON.stringify({
      url: location.href,
      title: document.title,
      bodyText: document.body ? document.body.innerText.slice(0,12000) : "",
      metas: Array.from(document.querySelectorAll("meta")).map(m=>({name:m.getAttribute("name"), property:m.getAttribute("property"), content:m.getAttribute("content")})).filter(x=>x.content).slice(0,80),
      resources: performance.getEntriesByType("resource").map(r=>r.name).filter(n => /douyinvod|media-audio|media-video|aweme\/detail/.test(n)).slice(0,400),
      cookie: document.cookie,
      ua: navigator.userAgent
    })'''
    return json.loads(chrome_eval(js))


def pick_audio_url(resources):
    for u in resources:
        if "media-audio" in u:
            return u
    return None


def sanitize_cookie(raw_cookie: str) -> str:
    # keep it simple; curl can take the raw cookie string
    return raw_cookie.strip()


def download_audio(audio_url: str, page_url: str, cookie: str, ua: str, out_path: Path):
    cmd = [
        "curl", "-L", audio_url,
        "-H", f"User-Agent: {ua}",
        "-H", f"Referer: {page_url}",
        "-H", "Origin: https://www.douyin.com",
        "-H", f"Cookie: {cookie}",
        "-H", "Accept: */*",
        "-o", str(out_path),
        "-sS",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip() or "curl failed")
    if not out_path.exists() or out_path.stat().st_size < 10000:
        raise RuntimeError("downloaded file missing or too small")
    return out_path


def main():
    if len(sys.argv) < 2:
        print("usage: douyin_grab.py <douyin-url>", file=sys.stderr)
        sys.exit(2)

    url = sys.argv[1]
    chrome_open(url)
    print("Opened in Chrome. Waiting for page to settle...", file=sys.stderr)
    subprocess.run(["sleep", "5"])

    data = fetch_page_snapshot()
    audio_url = pick_audio_url(data.get("resources", []))
    out = {
        "input_url": url,
        "page_url": data.get("url"),
        "title": data.get("title"),
        "metas": data.get("metas", []),
        "body_preview": data.get("bodyText", "")[:4000],
        "audio_url": audio_url,
        "audio_file": None,
    }

    if audio_url:
        cookie = sanitize_cookie(data.get("cookie", ""))
        ua = data.get("ua", "Mozilla/5.0")
        out_path = TMP_DIR / "audio_latest.mp4"
        try:
            download_audio(audio_url, data.get("url") or url, cookie, ua, out_path)
            out["audio_file"] = str(out_path)
            out["audio_size"] = out_path.stat().st_size
        except Exception as e:
            out["audio_error"] = str(e)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
