#!/usr/bin/env python3
"""
mimo_tts.py — 小米 MiMo V2.5 TTS（OpenAI 兼容接口，限时免费）。

3 种模式（自动路由）:
  1. 预置音色:   --voice 冰糖|茉莉|苏打|白桦|Mia|Chloe|Milo|Dean
  2. 文本设计音色: --design "低沉磁性的中年男性，深夜电台主播风格"
  3. 音频克隆:   --clone-audio "声音.mp3"（mp3/wav，≤7MB，每次请求传、不存模型）

风格控制:
  --style "(东北话)哎呀妈呀" → 音频标签放在文本开头
  --instruction "用温柔的语气慢慢说" → 自然语言指令（user message）

用法:
    python mimo_tts.py --text "你好" --voice 冰糖 --output out.wav
    python mimo_tts.py --text "你好" --clone-audio me.mp3 --output out.wav
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
import wave
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "https://api.xiaomimimo.com/v1"
VOICES_CN = ["冰糖", "茉莉", "苏打", "白桦"]
VOICES_EN = ["Mia", "Chloe", "Milo", "Dean"]
ALL_VOICES = VOICES_CN + VOICES_EN
MIME_MAP = {".mp3": "audio/mpeg", ".wav": "audio/wav"}
CLONE_MAX_BYTES = 7 * 1024 * 1024  # base64 后 ≤10MB → 原文 ≤7.5MB，留余量


def get_api_key() -> str:
    key = os.environ.get("MIMO_API_KEY", "").strip()
    if not key:
        print("✗ 环境变量 MIMO_API_KEY 未设置", file=sys.stderr)
        print("  → https://platform.xiaomimimo.com/#/console/api-keys 创建 key，然后:", file=sys.stderr)
        print("    python setup.py set-mimo", file=sys.stderr)
        sys.exit(1)
    return key


def mask(key: str) -> str:
    return f"{key[:4]}***{key[-4:]}" if len(key) > 8 else "***"


def call_chat_completions(api_key: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"✗ MiMo API {e.code} {e.reason}: {body[:400]}", file=sys.stderr)
        if e.code in (401, 403):
            print("  💡 MIMO_API_KEY 无效 → setup.py test-mimo 验证", file=sys.stderr)
        elif e.code == 429:
            print("  💡 限流 — 等 30 秒重试", file=sys.stderr)
        elif e.code == 400:
            print("  💡 检查: 音频 base64 是否过大（克隆音频 ≤7MB）/ 参数格式", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"✗ 网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)


def pcm16_to_wav(pcm_bytes: bytes, out_path: Path, sample_rate: int = 24000):
    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_bytes)


def main():
    ap = argparse.ArgumentParser(description="小米 MiMo V2.5 TTS — 预置音色 / 文本设计音色 / 音频克隆")
    ap.add_argument("--text", required=True, help="要合成的文本")
    ap.add_argument("--text-file", help="从文件读取文本（与 --text 二选一）")
    ap.add_argument("--voice", choices=ALL_VOICES, help="预置音色（模式 1）")
    ap.add_argument("--design", help="音色描述文本（模式 2，中文英文都行）")
    ap.add_argument("--clone-audio", help="克隆参考音频 .mp3/.wav ≤7MB（模式 3）")
    ap.add_argument("--style", help="音频标签风格，自动加到文本开头，如 '(东北话)' 或 '(开心 活泼)'")
    ap.add_argument("--instruction", help="自然语言风格指令（user message），如 '用温柔的语气慢慢说'")
    ap.add_argument("--output", required=True, help="输出音频路径 (.wav)")
    ap.add_argument("--model", help="强制指定模型（默认按模式自动选）")
    ap.add_argument("--optimize-text", action="store_true",
                    help="voicedesign 模式: 允许模型润色文本（可不传 --text 用模型生成）")
    ap.add_argument("--sample-rate", type=int, default=24000, help="pcm16→wav 采样率（默认 24000）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    text = args.text
    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8").strip()

    # 模式路由
    modes = sum(bool(x) for x in [args.voice, args.design, args.clone_audio])
    if modes == 0:
        args.voice = "冰糖"
        print("ℹ️ 未指定音色模式，默认用预置音色 '冰糖'（中文女声）", file=sys.stderr)
    elif modes > 1:
        print("✗ --voice / --design / --clone-audio 三选一", file=sys.stderr)
        sys.exit(1)

    if args.voice:
        model = args.model or "mimo-v2.5-tts"
        audio_cfg = {"format": "pcm16", "voice": args.voice}
        voice_desc = f"预置音色 '{args.voice}'"
    elif args.design:
        model = args.model or "mimo-v2.5-tts-voicedesign"
        audio_cfg = {"format": "pcm16", "optimize_text_preview": args.optimize_text}
        voice_desc = f"文本设计音色: {args.design[:40]}"
    else:
        model = args.model or "mimo-v2.5-tts-voiceclone"
        clone_path = Path(args.clone_audio)
        if not clone_path.exists():
            print(f"✗ 克隆音频不存在: {args.clone_audio}", file=sys.stderr)
            sys.exit(1)
        suffix = clone_path.suffix.lower()
        if suffix not in MIME_MAP:
            print(f"✗ 克隆音频仅支持 .mp3/.wav，当前: {suffix}", file=sys.stderr)
            sys.exit(1)
        size = clone_path.stat().st_size
        if size > CLONE_MAX_BYTES:
            print(f"✗ 克隆音频 {size/1024/1024:.1f}MB 超限（≤7MB），用 ffmpeg 压缩/截短后重试", file=sys.stderr)
            sys.exit(1)
        b64 = base64.b64encode(clone_path.read_bytes()).decode("ascii")
        audio_cfg = {"format": "pcm16", "voice": f"data:{MIME_MAP[suffix]};base64,{b64}"}
        voice_desc = f"音频克隆: {clone_path.name} ({size/1024:.0f}KB)"

    # 风格标签 → 拼在文本开头（assistant content）
    content = text
    if args.style:
        style = args.style.strip()
        if not style.startswith(("(", "（", "[")):
            style = f"({style})"
        content = style + content

    # messages 组装：要合成的文本在 assistant，风格指令/音色描述在 user
    messages = []
    if args.design:
        messages.append({"role": "user", "content": args.design})
        if text:
            messages.append({"role": "assistant", "content": content})
    else:
        user_content = args.instruction or ""
        messages.append({"role": "user", "content": user_content})
        messages.append({"role": "assistant", "content": content})

    api_key = get_api_key()
    if not args.json:
        print(f"📱 MiMo TTS: model={model} | {len(content)} 字 | {voice_desc} | key={mask(api_key)}")

    payload = {"model": model, "messages": messages, "audio": audio_cfg}
    result = call_chat_completions(api_key, payload)

    try:
        message = result["choices"][0]["message"]
        audio_data = message["audio"]["data"]
        transcript = message.get("audio", {}).get("transcript", "")
    except (KeyError, IndexError, TypeError):
        print(f"✗ 响应结构异常: {json.dumps(result, ensure_ascii=False)[:400]}", file=sys.stderr)
        sys.exit(1)

    pcm = base64.b64decode(audio_data)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pcm16_to_wav(pcm, out_path, args.sample_rate)
    duration = len(pcm) / 2 / args.sample_rate  # 16bit mono

    info = {
        "output": str(out_path.resolve()),
        "size_bytes": out_path.stat().st_size,
        "duration_seconds": round(duration, 1),
        "voice_used": voice_desc,
        "model": model,
        "format": "wav (pcm16 24kHz mono)",
        "engine": "xiaomi-mimo",
        "transcript": transcript,
    }
    if args.json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print(f"✅ 已保存: {out_path.resolve()} ({out_path.stat().st_size/1024:.1f} KB, ~{duration:.1f}s)")


if __name__ == "__main__":
    main()
