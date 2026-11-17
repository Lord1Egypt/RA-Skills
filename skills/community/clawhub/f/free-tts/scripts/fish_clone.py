#!/usr/bin/env python3
"""
fish_clone.py — Fish Audio 声音克隆：上传参考音频，训练持久化 voice 模型，拿回 voice_id。

用法:
    python fish_clone.py --audio "我的声音.m4a" --title "锋哥的声音"
    python fish_clone.py --audio a.wav b.wav --texts "字幕A" "字幕B" --title "锋哥 v2"

输出:
    JSON (--json): {"voice_id": "...", "state": "trained", "cache_name": "..."}
    本地缓存: scripts/voices_cache.json → 后续 fish_tts.py --cached-name 直接用
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import uuid
from pathlib import Path
from datetime import datetime, timezone

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_BASE = "https://api.fish.audio"
MODEL_ENDPOINT = f"{API_BASE}/model"
CACHE_FILE = Path(__file__).parent / "voices_cache.json"


def get_api_key() -> str:
    key = os.environ.get("FISH_API_KEY", "").strip()
    if not key:
        print("✗ 环境变量 FISH_API_KEY 未设置", file=sys.stderr)
        print("  → https://fish.audio/app/api-keys/ 创建 key，然后 python setup.py set-fish", file=sys.stderr)
        sys.exit(1)
    return key


def mask(key: str) -> str:
    return f"{key[:4]}***{key[-4:]}" if len(key) > 8 else "***"


def make_multipart(fields: dict, texts: list, audio_blobs: list) -> tuple:
    """构造 multipart/form-data。texts/audio 作为重复字段传。"""
    boundary = f"----FormBoundary{uuid.uuid4().hex[:16]}"
    body = b""
    for name, value in fields.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += str(value).encode("utf-8") + b"\r\n"
    for t in texts:
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="texts"\r\n\r\n'.encode()
        body += t.encode("utf-8") + b"\r\n"
    for blob in audio_blobs:
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="voices"; filename="audio.bin"\r\n'.encode()
        body += b"Content-Type: application/octet-stream\r\n\r\n"
        body += blob + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def load_audio(paths: list) -> list:
    blobs = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(f"音频文件不存在: {p}")
        if path.stat().st_size == 0:
            raise ValueError(f"音频文件为空: {p}")
        blobs.append(path.read_bytes())
    return blobs


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: dict):
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def call_clone(api_key: str, audio_blobs: list, title: str, description: str,
               visibility: str, texts: list, enhance: bool) -> dict:
    fields = {
        "type": "tts",
        "title": title,
        "description": description,
        "visibility": visibility,
        "train_mode": "fast",
        "enhance_audio_quality": "true" if enhance else "false",
    }
    body, content_type = make_multipart(fields, texts or [], audio_blobs)

    req = urllib.request.Request(
        MODEL_ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"✗ Fish API {e.code} {e.reason}: {err[:400]}", file=sys.stderr)
        if e.code == 401:
            print("  💡 key 无效 → setup.py test-fish 验证", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"✗ 网络错误: {e.reason}", file=sys.stderr)
        print("  💡 Fish 是海外 API，直连失败就设代理: set HTTPS_PROXY=http://127.0.0.1:7897", file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Fish Audio 声音克隆 — 上传音频训练持久化 voice 模型")
    ap.add_argument("--audio", nargs="+", required=True,
                    help="1-20 个音频文件 (.wav/.mp3/.m4a/.opus)，每段≥10秒，推荐 1-2 分钟")
    ap.add_argument("--texts", nargs="+", help="与音频一一对应的转写文本（提升发音准确度）")
    ap.add_argument("--title", default="Cloned Voice", help="voice 模型标题")
    ap.add_argument("--description", default="", help="voice 模型描述")
    ap.add_argument("--visibility", choices=["private", "unlist", "public"], default="private")
    ap.add_argument("--no-enhance", action="store_true", help="禁用自动降噪（音频已很干净时）")
    ap.add_argument("--cache-name", help="本地缓存别名（默认用 title）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    api_key = get_api_key()

    if len(args.audio) > 20:
        print("✗ 最多 20 个音频文件", file=sys.stderr)
        sys.exit(1)
    if args.texts and len(args.texts) != len(args.audio):
        print(f"✗ --texts 数量 ({len(args.texts)}) 必须与 --audio 数量 ({len(args.audio)}) 一致", file=sys.stderr)
        sys.exit(1)

    audio_blobs = load_audio(args.audio)
    total_kb = sum(len(b) for b in audio_blobs) / 1024
    if not args.json:
        print(f"🐟 克隆声音: {len(audio_blobs)} 个文件 (共 {total_kb:.1f} KB), title='{args.title}', key={mask(api_key)}")
        for p in args.audio:
            # 粗略时长提醒：<100KB 的 mp3 可能太短
            size_kb = Path(p).stat().st_size / 1024
            if size_kb < 100:
                print(f"  ⚠️ {Path(p).name} 只有 {size_kb:.0f}KB，可能 <10 秒 — 克隆效果会打折扣，建议补录 1-2 分钟")

    response = call_clone(
        api_key=api_key,
        audio_blobs=audio_blobs,
        title=args.title,
        description=args.description,
        visibility=args.visibility,
        texts=args.texts or [],
        enhance=not args.no_enhance,
    )

    voice_id = response.get("_id") or response.get("id")
    state = response.get("state", "created")
    if not voice_id:
        print(f"✗ 响应无 _id: {json.dumps(response, ensure_ascii=False)[:300]}", file=sys.stderr)
        sys.exit(1)

    cache_name = args.cache_name or args.title
    cache = load_cache()
    cache[cache_name] = {
        "voice_id": voice_id,
        "title": args.title,
        "state": state,
        "engine": "fish-audio",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "audio_sources": [str(Path(a).resolve()) for a in args.audio],
        "visibility": args.visibility,
    }
    save_cache(cache)

    out = {
        "voice_id": voice_id,
        "state": state,
        "title": args.title,
        "cache_name": cache_name,
        "engine": "fish-audio",
        "usage": f'python fish_tts.py --text "..." --cached-name "{cache_name}" --output out.mp3',
    }
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"\n✅ 声音克隆完成")
        print(f"   voice_id: {voice_id}")
        print(f"   state:    {state}{' ✓ 立即可用' if state == 'trained' else ' ⏳ 等待训练'}")
        print(f"   缓存:     '{cache_name}' → voices_cache.json")
        print(f"\n   下一步: python fish_tts.py --text \"你的文本\" --cached-name \"{cache_name}\" --output out.mp3")
        if state != "trained":
            print("   ⚠️ state 不是 trained，TTS 可能被拒 → 几秒后 python fish_voices.py list 复查")


if __name__ == "__main__":
    main()
