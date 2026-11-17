#!/usr/bin/env python3
"""
fish_tts.py — Fish Audio TTS 合成（s2.1-pro-free 免费层）。

3 种声音模式（三选一）:
  1. 持久 voice:   --reference-id <voice_id> 或 --cached-name <名字>
  2. 即时克隆:     --reference-audio <音频> --reference-text <字幕>
  3. 无声参考:     都不传（默认音色，适合多语言快速出片）

用法:
    python fish_tts.py --text "你好" --output out.mp3
    python fish_tts.py --text "你好" --cached-name "锋哥的声音" --output out.mp3 --format mp3
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_BASE = "https://api.fish.audio"
TTS_ENDPOINT = f"{API_BASE}/v1/tts"
CACHE_FILE = Path(__file__).parent / "voices_cache.json"


def get_api_key() -> str:
    key = os.environ.get("FISH_API_KEY", "").strip()
    if not key:
        print("✗ 环境变量 FISH_API_KEY 未设置", file=sys.stderr)
        print("  → https://fish.audio/app/api-keys/ 创建 key，然后:", file=sys.stderr)
        print("    python setup.py set-fish", file=sys.stderr)
        sys.exit(1)
    return key


def mask(key: str) -> str:
    return f"{key[:4]}***{key[-4:]}" if len(key) > 8 else "***"


def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def call_tts(api_key: str, payload: dict, model: str) -> bytes:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        TTS_ENDPOINT,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "model": model,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"✗ Fish TTS {e.code} {e.reason}", file=sys.stderr)
        try:
            print(f"  {json.dumps(json.loads(body), ensure_ascii=False, indent=2)[:500]}", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"  {body[:500]}", file=sys.stderr)
        hints = {
            400: "检查: text 非空 / reference_id 正确 / format 合法 / 音频 base64 可解码",
            401: "FISH_API_KEY 无效 → setup.py test-fish 验证",
            402: "余额不足 → 用 --model s2.1-pro-free 或充值",
            403: "无权限（免费层已到期？检查 fish.audio 公告）",
            429: "限流 — 等 30 秒重试",
        }
        if e.code in hints:
            print(f"  💡 {hints[e.code]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"✗ 网络错误: {e.reason}", file=sys.stderr)
        print("  💡 Fish 是海外 API，直连失败就设代理: set HTTPS_PROXY=http://127.0.0.1:7897", file=sys.stderr)
        sys.exit(1)


def estimate_duration(nbytes: int, fmt: str, mp3_bitrate: int) -> float:
    if fmt == "mp3" and mp3_bitrate > 0:
        return nbytes * 8 / (mp3_bitrate * 1000)
    if fmt == "opus":
        return nbytes * 8 / 64000
    return -1.0


def preflight_check(timeout: int = 12):
    """快速探测 Fish API 可达性，失败立刻退出（避免无代理时干等）。"""
    req = urllib.request.Request(API_BASE, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code  # 收到 HTTP 响应 = 网络通
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        reason = getattr(e, "reason", e)
        print(f"✗ Fish API 连不通: {reason}", file=sys.stderr)
        print("  💡 Fish 是海外 API。请确认 Clash/代理已开启，然后:", file=sys.stderr)
        print("     set HTTPS_PROXY=http://127.0.0.1:7897   (Clash 默认 mixed-port)", file=sys.stderr)
        print("     或在 Clash Verge 里开启系统代理后重试", file=sys.stderr)
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="Fish Audio TTS — 文本转语音（默认免费模型 s2.1-pro-free）")
    ap.add_argument("--text", required=True, help="要合成的文本")
    ap.add_argument("--text-file", help="从文件读取文本（与 --text 二选一）")
    ap.add_argument("--reference-id", help="持久化 voice_id")
    ap.add_argument("--cached-name", help="从 voices_cache.json 查 voice_id")
    ap.add_argument("--reference-audio", help="即时克隆 — 参考音频路径 (.wav/.mp3/.m4a/.opus)")
    ap.add_argument("--reference-text", help="即时克隆 — 参考音频的转写文本")
    ap.add_argument("--output", required=True, help="输出音频路径")
    ap.add_argument("--format", choices=["mp3", "wav", "pcm", "opus"], default="mp3")
    ap.add_argument("--mp3-bitrate", type=int, choices=[64, 128, 192], default=128)
    ap.add_argument("--sample-rate", type=int, help="wav/pcm 采样率（如 44100）")
    ap.add_argument("--speed", type=float, default=1.0, help="语速 0.5-2.0")
    ap.add_argument("--volume", type=float, default=0.0, help="音量 dB")
    ap.add_argument("--latency", choices=["normal", "balanced"], default="balanced")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top-p", type=float, default=0.7)
    ap.add_argument("--model", default="s2.1-pro-free",
                    help="模型: s2.1-pro-free(默认免费) / s2.1-pro / s2-pro / s1")
    ap.add_argument("--chunk-length", type=int, default=200, help="100-300")
    ap.add_argument("--no-normalize", action="store_true", help="关闭数字/日期归一化")
    ap.add_argument("--json", action="store_true", help="JSON 输出元信息")
    args = ap.parse_args()

    text = args.text
    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8").strip()
    if not text:
        print("✗ 文本为空", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    preflight_check()

    modes = sum(bool(x) for x in [args.reference_id, args.cached_name, args.reference_audio])
    if modes > 1:
        print("✗ --reference-id / --cached-name / --reference-audio 三选一", file=sys.stderr)
        sys.exit(1)

    payload = {
        "text": text,
        "format": args.format,
        "prosody": {"speed": args.speed, "volume": args.volume},
        "temperature": args.temperature,
        "top_p": args.top_p,
        "chunk_length": args.chunk_length,
        "latency": args.latency,
        "normalize": not args.no_normalize,
    }
    voice_used = "default（无参考音频）"

    if args.reference_id:
        payload["reference_id"] = args.reference_id
        voice_used = f"reference_id={args.reference_id[:8]}..."
    elif args.cached_name:
        cache = load_cache()
        if args.cached_name not in cache:
            print(f"✗ 缓存里没有 '{args.cached_name}'，先跑 fish_clone.py", file=sys.stderr)
            print(f"  已有: {list(cache.keys())}", file=sys.stderr)
            sys.exit(1)
        entry = cache[args.cached_name]
        payload["reference_id"] = entry["voice_id"]
        voice_used = f"cached '{args.cached_name}' → {entry['voice_id'][:8]}..."
    elif args.reference_audio:
        if not args.reference_text:
            print("✗ --reference-audio 必须配 --reference-text", file=sys.stderr)
            sys.exit(1)
        ref = Path(args.reference_audio)
        if not ref.exists():
            print(f"✗ 参考音频不存在: {args.reference_audio}", file=sys.stderr)
            sys.exit(1)
        payload["references"] = [{
            "audio": base64.b64encode(ref.read_bytes()).decode("ascii"),
            "text": args.reference_text,
        }]
        voice_used = f"instant clone ({ref.name})"

    if args.format == "mp3":
        payload["mp3_bitrate"] = args.mp3_bitrate
    if args.sample_rate:
        payload["sample_rate"] = args.sample_rate

    if not args.json:
        print(f"🐟 Fish TTS: model={args.model} | {len(text)} 字 | voice={voice_used} | key={mask(api_key)}")

    audio_bytes = call_tts(api_key, payload, args.model)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(audio_bytes)

    info = {
        "output": str(out_path.resolve()),
        "size_bytes": len(audio_bytes),
        "duration_estimate_seconds": round(estimate_duration(len(audio_bytes), args.format, args.mp3_bitrate), 1),
        "voice_used": voice_used,
        "model": args.model,
        "format": args.format,
        "engine": "fish-audio",
    }
    if args.json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        dur = info["duration_estimate_seconds"]
        dur_s = f" ~{dur}s" if dur > 0 else ""
        print(f"✅ 已保存: {out_path.resolve()} ({len(audio_bytes)/1024:.1f} KB{dur_s})")


if __name__ == "__main__":
    main()
