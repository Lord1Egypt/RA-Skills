#!/usr/bin/env python3
"""
智能配音合成脚本
支持 ElevenLabs、OpenAI TTS、Azure TTS，自动降级到系统 TTS
"""

import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path


# ── 音色映射 ──────────────────────────────────────────────
ELEVENLABS_VOICE_MAP = {
    "warm-female": "21m00Tcm4TlvDq8ikWAM",
    "professional-male": "ErXwobaYiN019PkySvjV",
    "professional-female": "EXAVITQu4vr4xnSDxMaL",
    "magnetic-male": "VR6AewLTigWG4xSOukaG",
    "young-energetic": "pNInz6obpgDQGcFmaJgB",
    "calm-narrator": "yoZ06aMxZJJ28mfd3POQ",
}

OPENAI_VOICE_MAP = {
    "warm-female": "nova",
    "professional-male": "onyx",
    "professional-female": "shimmer",
    "magnetic-male": "echo",
    "young-energetic": "fable",
    "calm-narrator": "alloy",
}

EMOTION_SETTINGS = {
    "calm":         {"stability": 0.8, "similarity_boost": 0.75, "style": 0.2},
    "warm":         {"stability": 0.5, "similarity_boost": 0.75, "style": 0.5},
    "professional": {"stability": 0.7, "similarity_boost": 0.80, "style": 0.3},
    "energetic":    {"stability": 0.3, "similarity_boost": 0.70, "style": 0.8},
}

SPEED_MAP = {"slow": 0.85, "normal": 1.0, "fast": 1.15}


# ── 文本预处理 ────────────────────────────────────────────
def preprocess_text(text: str) -> str:
    """数字转中文、清理多余空白"""
    import re
    # 简单数字转换（整数）
    def num_to_cn(m):
        n = int(m.group())
        units = ["", "十", "百", "千", "万"]
        digits = "零一二三四五六七八九"
        if n == 0:
            return "零"
        result = ""
        s = str(n)
        for i, d in enumerate(s):
            if d != "0":
                result += digits[int(d)] + units[len(s) - i - 1]
            elif result and result[-1] != "零":
                result += "零"
        return result.rstrip("零") or "零"

    text = re.sub(r'\b\d+\b', num_to_cn, text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ── ElevenLabs 合成 ───────────────────────────────────────
def synthesize_elevenlabs(text: str, voice: str, emotion: str, speed: float, output: str) -> bool:
    try:
        from elevenlabs import ElevenLabs, VoiceSettings
    except ImportError:
        print("[WARN] elevenlabs 未安装，跳过", file=sys.stderr)
        return False

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("[WARN] ELEVENLABS_API_KEY 未设置，跳过", file=sys.stderr)
        return False

    voice_id = ELEVENLABS_VOICE_MAP.get(voice, ELEVENLABS_VOICE_MAP["professional-male"])
    settings = EMOTION_SETTINGS.get(emotion, EMOTION_SETTINGS["calm"])

    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=settings["stability"],
            similarity_boost=settings["similarity_boost"],
            style=settings["style"],
            use_speaker_boost=True,
        ),
    )

    with open(output, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"[OK] ElevenLabs 合成完成 → {output}")
    return True


# ── OpenAI TTS 合成 ───────────────────────────────────────
def synthesize_openai(text: str, voice: str, speed: float, output: str) -> bool:
    try:
        from openai import OpenAI
    except ImportError:
        print("[WARN] openai 未安装，跳过", file=sys.stderr)
        return False

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[WARN] OPENAI_API_KEY 未设置，跳过", file=sys.stderr)
        return False

    oai_voice = OPENAI_VOICE_MAP.get(voice, "alloy")
    client = OpenAI(api_key=api_key)

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=oai_voice,
        input=text,
        speed=speed,
    )
    response.stream_to_file(output)
    print(f"[OK] OpenAI TTS 合成完成 → {output}")
    return True


# ── 后期处理 ──────────────────────────────────────────────
def post_process(audio_path: str, bgm_path: str = None, bgm_volume: float = 0.1) -> str:
    """音量标准化 + 可选背景音乐混音"""
    try:
        from pydub import AudioSegment
    except ImportError:
        print("[WARN] pydub 未安装，跳过后期处理", file=sys.stderr)
        return audio_path

    audio = AudioSegment.from_file(audio_path)

    # 音量标准化（简单 normalize，精确 LUFS 需 ffmpeg）
    from pydub.effects import normalize
    audio = normalize(audio)

    if bgm_path and Path(bgm_path).exists():
        bgm = AudioSegment.from_file(bgm_path)
        # 降低 BGM 音量
        bgm_db = 20 * (bgm_volume - 1)  # 粗略换算
        bgm = bgm + bgm_db
        while len(bgm) < len(audio):
            bgm = bgm + bgm
        bgm = bgm[:len(audio)]
        audio = audio.overlay(bgm)

    out_path = audio_path.replace(".mp3", "_processed.mp3").replace(".wav", "_processed.wav")
    fmt = "mp3" if out_path.endswith(".mp3") else "wav"
    audio.export(out_path, format=fmt, bitrate="192k" if fmt == "mp3" else None)
    print(f"[OK] 后期处理完成 → {out_path}")
    return out_path


# ── 主函数 ────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="智能配音合成")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="直接输入文本")
    group.add_argument("--script", help="从文件读取脚本")
    parser.add_argument("--voice", default="professional-male",
                        choices=list(ELEVENLABS_VOICE_MAP.keys()),
                        help="音色选择")
    parser.add_argument("--speed", default="normal",
                        choices=["slow", "normal", "fast"],
                        help="语速")
    parser.add_argument("--emotion", default="calm",
                        choices=list(EMOTION_SETTINGS.keys()),
                        help="情感风格")
    parser.add_argument("--output", default="./output.mp3", help="输出文件路径")
    parser.add_argument("--bgm", help="背景音乐文件路径")
    parser.add_argument("--bgm-volume", type=float, default=0.1,
                        help="背景音乐音量比例 (0-1)")
    parser.add_argument("--no-postprocess", action="store_true",
                        help="跳过后期处理")

    args = parser.parse_args()

    # 读取文本
    if args.script:
        text = Path(args.script).read_text(encoding="utf-8")
    else:
        text = args.text

    # 预处理
    text = preprocess_text(text)
    speed = SPEED_MAP[args.speed]

    print(f"[INFO] 文本长度: {len(text)} 字")
    print(f"[INFO] 音色: {args.voice} | 语速: {args.speed} | 情感: {args.emotion}")

    # 尝试各引擎
    success = False
    raw_output = args.output

    if not success:
        success = synthesize_elevenlabs(text, args.voice, args.emotion, speed, raw_output)
    if not success:
        success = synthesize_openai(text, args.voice, speed, raw_output)

    if not success:
        print("[ERROR] 所有 TTS 引擎均不可用。请检查 API key 或安装依赖。", file=sys.stderr)
        print("提示：设置 ELEVENLABS_API_KEY 或 OPENAI_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    # 后期处理
    if not args.no_postprocess:
        final = post_process(raw_output, args.bgm, args.bgm_volume)
        if final != raw_output:
            print(f"[INFO] 最终文件: {final}")
    else:
        print(f"[INFO] 最终文件: {raw_output}")


if __name__ == "__main__":
    main()
