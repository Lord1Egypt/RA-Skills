#!/usr/bin/env python3
"""
douyin_grab.py — Linux 版
使用 agent-browser 替代 chrome_bridge，yt-dlp 下载音视频，faster-whisper 转写
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

TMP_DIR = Path("/tmp/douyin_transcribe")
TMP_DIR.mkdir(parents=True, exist_ok=True)

VENV_PY = os.environ.get('DOUYIN_VENV_PY', '/tmp/douyin_transcribe/venv/bin/python3')
WHISPER_MODEL = os.environ.get('DOUYIN_WHISPER_MODEL', 'Systran/faster-whisper-medium')

AGENT_BROWSER = os.environ.get('AGENT_BROWSER_BIN', 'agent-browser')


def run(cmd, capture=True, check=True):
    if isinstance(cmd, str):
        cmd = cmd.split()
    p = subprocess.run(cmd, capture_output=capture, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or f"command failed: {cmd}")
    return p.stdout.strip() if capture else ""


def get_page_text(url: str) -> dict:
    """用 agent-browser 打开页面，获取标题、正文、资源列表"""
    session = f"douyin_grab_{int(time.time())}"
    try:
        run([AGENT_BROWSER, '--session', session, 'open', url])
        time.sleep(4)
        run([AGENT_BROWSER, '--session', session, 'wait', '--load', 'networkidle'])
        snap = run([AGENT_BROWSER, '--session', session, 'snapshot', '-i', '-c', '-d', '3', '--json'])
        data = json.loads(snap)
        snapshot_text = data.get('data', {}).get('snapshot', '')
        refs = data.get('data', {}).get('refs', {})

        title = ""
        for ref in refs.values():
            if ref.get('role') == 'heading':
                title = ref.get('name', '')
                break

        js = r"""JSON.stringify({
          url: location.href,
          title: document.title,
          bodyText: document.body ? document.body.innerText.slice(0,12000) : "",
          resources: performance.getEntriesByType("resource").map(r=>r.name).filter(n => /douyinvod|media-audio|media-video|aweme\/detail/.test(n)).slice(0,200)
        })"""
        eval_result = run([AGENT_BROWSER, '--session', session, 'eval', js])
        page_data = json.loads(eval_result)

        return {
            'title': title or page_data.get('title', ''),
            'body_text': page_data.get('bodyText', '')[:4000],
            'resources': page_data.get('resources', []),
            'url': page_data.get('url', url),
            'snapshot_text': snapshot_text
        }
    finally:
        run([AGENT_BROWSER, '--session', session, 'close'], check=False)


def pick_audio_url(resources):
    for u in resources:
        if 'media-audio' in u or 'aweme' in u:
            return u
    return None


def download_with_ytdlp(url: str, out_path: Path) -> bool:
    """用 yt-dlp 下载抖音视频/音频"""
    cmd = [
        str(VENV_PY), '-m', 'yt_dlp',
        '-f', 'bestaudio/best',
        '--no-playlist',
        '-o', str(out_path.with_suffix('.%(ext)s')),
        url
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if p.returncode == 0:
        downloaded = list(out_path.parent.glob(f"{out_path.stem}.*"))
        if downloaded:
            actual = downloaded[0]
            if actual != out_path:
                actual.rename(out_path)
            return True
    return False


def transcribe_audio(audio_path: Path) -> str:
    code = f"""
from faster_whisper import transcribe
r, info = None, None
def _run():
    global r, info
    r, info = transcribe({str(audio_path)!r}, model="medium", language="zh", task="transcribe")
    text = " ".join([s.text for s in r[0]])
    print(text)
_run()
"""
    p = subprocess.run([VENV_PY, '-c', code], capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or 'transcription failed')
    return p.stdout.strip()


def main():
    if len(sys.argv) < 2:
        print("usage: douyin_grab.py <douyin-url>", file=sys.stderr)
        sys.exit(2)

    url = sys.argv[1]
    print(f"[INFO] Grabbing: {url}", file=sys.stderr)

    data = get_page_text(url)
    audio_url = pick_audio_url(data.get('resources', []))

    out = {
        "input_url": url,
        "page_url": data.get('url', url),
        "title": data.get('title', ''),
        "body_preview": data.get('body_text', ''),
        "audio_url": audio_url,
        "audio_file": None,
        "transcript": None,
    }

    if audio_url:
        out_path = TMP_DIR / "audio_latest.mp4"
        try:
            ok = download_with_ytdlp(audio_url, out_path)
            if ok and out_path.exists() and out_path.stat().st_size > 5000:
                out["audio_file"] = str(out_path)
                out["audio_size"] = out_path.stat().st_size
                # 转写
                try:
                    out["transcript"] = transcribe_audio(out_path)
                except Exception as e:
                    out["transcribe_error"] = str(e)
            else:
                out["download_error"] = "file too small or not found"
        except Exception as e:
            out["download_error"] = str(e)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
