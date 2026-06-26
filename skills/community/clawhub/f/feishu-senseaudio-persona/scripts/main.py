from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from asr import transcribe_audio
from feishu_api import send_audio_message, upload_opus_file
from persona_store import DEFAULT_PERSONA, load_persona, persona_exists, save_persona
from tts import convert_wav_to_opus, synthesize

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def cmd_setup(_: argparse.Namespace) -> None:
    print("=== Feishu Persona Voice Reply setup ===")
    print(f"python3: {shutil.which('python3') or '未找到'}")
    print(f"ffmpeg: {shutil.which('ffmpeg') or '未找到'}")
    print(f"FEISHU_APP_ID: {'已设置' if os.getenv('FEISHU_APP_ID') else '未设置'}")
    print(f"FEISHU_APP_SECRET: {'已设置' if os.getenv('FEISHU_APP_SECRET') else '未设置'}")
    print(f"SENSEAUDIO_API_KEY: {'已设置' if os.getenv('SENSEAUDIO_API_KEY') else '未设置'}")
    print(f"persona.json: {'已存在' if persona_exists() else '不存在'}")
    print("\n如果缺少 API Key：")
    print("1. 前往 SenseAudio 平台创建 API Key")
    print("2. 设置环境变量：export SENSEAUDIO_API_KEY=... ")
    print("3. 飞书应用配置 App ID / App Secret，并发布应用")


def cmd_persona_init(args: argparse.Namespace) -> None:
    persona = load_persona()
    persona.update(
        {
            "name": args.name,
            "relationship": args.relationship,
            "personality": args.personality,
            "speaking_style": args.speaking_style,
            "catchphrase": args.catchphrase,
            "voice_id": args.voice_id,
            "speed": float(args.speed),
            "pitch": int(round(float(args.pitch))),
            "vol": float(args.vol),
            "emotion": args.emotion,
            "boundaries": args.boundaries,
        }
    )
    path = save_persona(persona)
    print(f"人设已保存到: {path}")
    print(json.dumps(persona, ensure_ascii=False, indent=2))


def cmd_persona_show(_: argparse.Namespace) -> None:
    persona = load_persona()
    print(json.dumps(persona, ensure_ascii=False, indent=2))


def cmd_persona_prompt(args: argparse.Namespace) -> None:
    persona = load_persona()
    user_message = args.user_message.strip()
    prompt = f"""
你现在扮演一个固定虚拟角色，请严格保持人设一致。

角色名称：{persona['name']}
角色定位：{persona['relationship']}
性格关键词：{persona['personality']}
说话风格：{persona['speaking_style']}
常用口头禅：{persona.get('catchphrase', '')}
角色边界：{persona.get('boundaries', '')}

要求：
1. 使用自然中文回复，不要变成客服口吻。
2. 语气要符合这个角色，不要跑出设定。
3. 回复适合被 TTS 念出来，默认 2~5 句，不要过长。
4. 对危险、违法、医疗、财务等高风险内容要温和收缩，不要直接给专业决策。
5. 可以表现亲近感，但不要越界。

用户刚刚说：{user_message}

现在请直接生成这个角色会说的话，只输出回复正文，不要输出解释。
""".strip()
    print(prompt)


def cmd_transcribe(args: argparse.Namespace) -> None:
    result = transcribe_audio(args.audio)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["text"])


def cmd_send_voice(args: argparse.Namespace) -> None:
    persona = load_persona()
    chat_id = args.chat_id or os.getenv("FEISHU_CHAT_ID")
    if not chat_id:
        raise RuntimeError("缺少 chat_id，请通过 --chat-id 传入，或设置 FEISHU_CHAT_ID")

    reply_text = args.reply_text.strip()
    if not reply_text:
        raise RuntimeError("reply_text 不能为空")

    base_name = args.file_name or f"{persona['name']}_reply"
    wav_path = OUTPUT_DIR / f"{base_name}.wav"
    opus_path = OUTPUT_DIR / f"{base_name}.opus"

    tts_result = synthesize(
        text=reply_text,
        voice_id=args.voice_id or persona["voice_id"],
        speed=args.speed if args.speed is not None else persona["speed"],
        pitch=args.pitch if args.pitch is not None else persona["pitch"],
        vol=args.vol if args.vol is not None else persona["vol"],
        emotion=args.emotion or persona.get("emotion"),
        output_wav=str(wav_path),
    )
    convert_wav_to_opus(tts_result["wav_path"], str(opus_path))
    upload = upload_opus_file(str(opus_path), file_name=f"{base_name}.opus")
    send = send_audio_message(chat_id=chat_id, file_key=upload["file_key"])

    result = {
        "text": reply_text,
        "wav_path": str(wav_path),
        "opus_path": str(opus_path),
        "file_key": upload["file_key"],
        "send_result": send,
    }
    # print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Feishu persona voice reply via SenseAudio")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("setup", help="检查环境")
    p.set_defaults(func=cmd_setup)

    p = sub.add_parser("persona-init", help="初始化/更新人设")
    p.add_argument("--name", default=DEFAULT_PERSONA["name"])
    p.add_argument("--relationship", default=DEFAULT_PERSONA["relationship"])
    p.add_argument("--personality", default=DEFAULT_PERSONA["personality"])
    p.add_argument("--speaking-style", default=DEFAULT_PERSONA["speaking_style"])
    p.add_argument("--catchphrase", default=DEFAULT_PERSONA["catchphrase"])
    p.add_argument("--voice-id", default=DEFAULT_PERSONA["voice_id"])
    p.add_argument("--speed", type=float, default=DEFAULT_PERSONA["speed"])
    p.add_argument("--pitch", type=float, default=DEFAULT_PERSONA["pitch"])
    p.add_argument("--vol", type=float, default=DEFAULT_PERSONA["vol"])
    p.add_argument("--emotion", default=DEFAULT_PERSONA["emotion"])
    p.add_argument("--boundaries", default=DEFAULT_PERSONA["boundaries"])
    p.set_defaults(func=cmd_persona_init)

    p = sub.add_parser("persona-show", help="查看当前人设")
    p.set_defaults(func=cmd_persona_show)

    p = sub.add_parser("persona-prompt", help="根据当前人设生成角色回复提示词")
    p.add_argument("--user-message", required=True)
    p.set_defaults(func=cmd_persona_prompt)

    p = sub.add_parser("transcribe", help="用 SenseAudio ASR 转写音频")
    p.add_argument("--audio", required=True)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_transcribe)

    p = sub.add_parser("send-voice", help="将已生成的回复文本变成飞书语音条并发送")
    p.add_argument("--reply-text", required=True)
    p.add_argument("--chat-id", help="飞书 chat_id；不传则读取 FEISHU_CHAT_ID")
    p.add_argument("--file-name", help="输出文件名前缀")
    p.add_argument("--voice-id")
    p.add_argument("--speed", type=float)
    p.add_argument("--pitch", type=float)
    p.add_argument("--vol", type=float)
    p.add_argument("--emotion")
    p.set_defaults(func=cmd_send_voice)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
