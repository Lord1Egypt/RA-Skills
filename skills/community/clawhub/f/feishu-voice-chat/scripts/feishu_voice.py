#!/usr/bin/env python3
"""
飞书语音对话 - OpenClaw 友好封装 / Feishu Voice Chat - OpenClaw Friendly Wrapper
提供简化的语音识别和语音合成接口 / Provides simplified ASR and TTS interfaces
"""

import os
import sys
import subprocess
import json
import pathlib

SKILL_DIR = pathlib.Path.home() / ".openclaw" / "workspace" / "skills" / "feishu-voice-chat"
SCRIPT_PATH = SKILL_DIR / "scripts" / "volc_voice.py"


def transcribe_voice(audio_path):
    """
    语音识别（ASR）：将音频文件转换为文本 / Speech Recognition: convert audio file to text

    Args:
        audio_path: 音频文件绝对路径 / Absolute path to audio file

    Returns:
        识别出的文本，失败返回 None / Recognized text, or None on failure
    """
    print(f"🎙️ 正在识别语音: {audio_path}", flush=True)

    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "asr", audio_path],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            json_line = [line for line in output_lines if line.strip().startswith('{') and line.strip().endswith('}')]

            if json_line:
                response = json.loads(json_line[-1])
                if response.get("status") == "success":
                    text = response.get("text", "")
                    print(f"✅ 识别成功: {text[:50]}...", flush=True)
                    return text
                else:
                    print(f"❌ 识别失败", flush=True)
            else:
                print(f"⚠️ 未找到标准 JSON 输出", flush=True)
                print(f"原始输出: {result.stdout[:200]}", flush=True)

        print(f"❌ 命令执行失败，返回码: {result.returncode}", flush=True)
        print(result.stderr, flush=True)
        return None

    except subprocess.TimeoutExpired:
        print("❌ 识别超时（120秒）", flush=True)
        return None
    except Exception as e:
        print(f"❌ 识别异常: {e}", flush=True)
        return None


def synthesize_speech(text, output_path=None, reply_to=None):
    """
    语音合成（TTS）：将文本转换为音频文件（.ogg 格式，适配飞书语音消息）/ TTS: convert text to .ogg audio file

    Args:
        text: 要合成的文本 / Text to synthesize
        output_path: 输出文件路径（可选，默认生成到 /tmp/openclaw/voice-tts/）/ Output file path (optional)
        reply_to: 回复目标消息 ID（可选，用于话题内回复）/ Message ID to reply to (optional, for threaded replies)

    Returns:
        包含 audio_file 路径的字典，失败返回 None / Dict with audio_file path, or None on failure
    """
    if not output_path:
        import uuid
        import time
        unique_id = uuid.uuid4().hex[:8]
        timestamp = int(time.time())
        output_dir = pathlib.Path("/tmp/openclaw/voice-tts")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / f"reply_{timestamp}_{unique_id}.ogg")

    print(f"🔊 正在合成语音: {text[:50]}...", flush=True)

    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "tts", text, output_path],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            json_line = [line for line in output_lines if line.strip().startswith('{') and line.strip().endswith('}')]

            if json_line:
                response = json.loads(json_line[-1])
                if response.get("status") == "success":
                    file_path = response.get("file_path", "")
                    print(f"✅ 合成成功: {file_path}", flush=True)
                    # 返回结构化结果供 Agent 调用 message 工具 / Return structured result for Agent to call message tool
                    result_obj = {
                        "status": "success",
                        "audio_file": file_path,
                        "message_cmd": f'message(action="send", channel="feishu", msg_type="audio", media="{file_path}")'
                    }
                    if reply_to:
                        result_obj["message_cmd"] = f'message(action="reply", channel="feishu", message_id="{reply_to}", msg_type="audio", media="{file_path}")'
                    print(json.dumps(result_obj), flush=True)
                    return result_obj

            print(f"⚠️ 未找到标准 JSON 输出", flush=True)
            print(f"原始输出: {result.stdout[:200]}", flush=True)

        print(f"❌ 命令执行失败，返回码: {result.returncode}", flush=True)
        print(result.stderr, flush=True)
        return None

    except subprocess.TimeoutExpired:
        print("❌ 合成超时（120秒）", flush=True)
        return None
    except Exception as e:
        print(f"❌ 合成异常: {e}", flush=True)
        return None


def main():
    """主函数入口 / Main entry point"""
    if len(sys.argv) < 2:
        print("🐰 飞书语音对话 - OpenClaw 友好封装", flush=True)
        print()
        print("用法 / Usage:", flush=True)
        print("  # 语音识别（ASR） 语音→文字", flush=True)
        print("  python3 feishu_voice.py transcribe <音频文件路径>", flush=True)
        print()
        print("  # 语音合成（TTS） 文字→语音  /  Text → voice (auto-reply via message tool)", flush=True)
        print("  python3 feishu_voice.py speak \"要说的内容\" [输出文件路径] [reply_to消息ID]", flush=True)
        print()
        print("示例 / Examples:", flush=True)
        print("  python3 feishu_voice.py transcribe /tmp/openclaw/media/inbound/voice.ogg", flush=True)
        print('  python3 feishu_voice.py speak "你好，这是语音回复"', flush=True)
        print('  python3 feishu_voice.py speak "回复这条" /tmp/reply.ogg om_xxx', flush=True)
        sys.exit(1)

    command = sys.argv[1]

    if command == "transcribe":
        if len(sys.argv) < 3:
            print("❌ 请提供音频文件路径 / Please provide audio file path", flush=True)
            sys.exit(1)

        audio_path = sys.argv[2]
        text = transcribe_voice(audio_path)

        if text:
            print()
            print("=" * 60, flush=True)
            print(f"识别结果 / Recognition result: {text}", flush=True)
            print("=" * 60, flush=True)
        else:
            print()
            print("❌ 识别失败 / Recognition failed", flush=True)
            sys.exit(1)

    elif command == "speak":
        if len(sys.argv) < 3:
            print("❌ 请提供要说的内容 / Please provide text to speak", flush=True)
            sys.exit(1)

        text = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else None
        reply_to = sys.argv[4] if len(sys.argv) > 4 else None

        result = synthesize_speech(text, output_path, reply_to)

        if result:
            print()
            print("=" * 60, flush=True)
            print(f"音频文件 / Audio file: {result['audio_file']}", flush=True)
            print(f"发送指令 / Send command: {result['message_cmd']}", flush=True)
            print("=" * 60, flush=True)
        else:
            print()
            print("❌ 合成失败 / Synthesis failed", flush=True)
            sys.exit(1)

    else:
        print(f"❌ 未知命令 / Unknown command: {command}", flush=True)
        print("可用命令 / Available commands: transcribe, speak", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
