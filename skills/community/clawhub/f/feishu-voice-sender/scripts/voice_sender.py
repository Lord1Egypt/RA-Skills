#!/usr/bin/env python3
"""
飞书语音发送器 - 极简版
仅支持 Edge TTS，一键发送语音到飞书

支持两种发送场景：
1. 回复场景：不传 --target，自动发回当前群
2. 主动发送：传入 --target 指定群ID
"""
import subprocess
import tempfile
import os
import asyncio
import sys
import argparse

# Edge TTS
try:
    import edge_tts
except ImportError:
    print("请先安装: pip install edge-tts")
    sys.exit(1)

# 默认语音
DEFAULT_VOICE = "xiaoxiao"

# Edge TTS 可用语音
VOICES = {
    "xiaoxiao": "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)",
    "yunyang": "Microsoft Server Speech Text to Speech Voice (zh-CN, YunyangNeural)",
    "yunxi": "Microsoft Server Speech Text to Speech Voice (zh-CN, YunxiNeural)",
    "xiaoyi": "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoyiNeural)",
    "yunjian": "Microsoft Server Speech Text to Speech Voice (zh-CN, YunJianNeural)",
    "xiaobei": "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaobeiNeural)",
}


async def generate_audio(text: str, voice: str = DEFAULT_VOICE) -> bytes:
    """使用 Edge TTS 生成音频"""
    if voice not in VOICES:
        print(f"⚠️ 未知语音 {voice}，使用默认 xiaoxiao")
        voice = DEFAULT_VOICE
    
    tts_voice = VOICES[voice]
    
    communicate = edge_tts.Communicate(text, tts_voice)
    audio_data = b""
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    
    return audio_data


import uuid

def text_to_opus(text: str, voice: str = DEFAULT_VOICE) -> str:
    """文字转 OPUS 文件"""
    # 1. 生成音频
    audio_bytes = asyncio.run(generate_audio(text, voice))
    
    if not audio_bytes:
        raise Exception("TTS 生成失败")
    
    # 2. 保存临时 MP3（加时间戳防止竞争）
    timestamp = uuid.uuid4().hex[:8]
    mp3_file = f"/tmp/feishu_voice_{timestamp}.mp3"
    with open(mp3_file, "wb") as f:
        f.write(audio_bytes)
    
    # 3. 转换为 OPUS
    opus_file = f"/tmp/feishu_voice_{timestamp}.opus"
    cmd = [
        "ffmpeg", "-y", "-i", mp3_file,
        "-acodec", "libopus",
        "-ac", "1", "-ar", "16000",
        opus_file
    ]
    result = subprocess.run(cmd, capture_output=True)
    
    os.remove(mp3_file)  # 清理 MP3
    
    if result.returncode != 0:
        raise Exception(f"OPUS 转换失败: {result.stderr.decode()}")
    
    return opus_file


def send_voice(text: str, voice: str = DEFAULT_VOICE, target: str = None) -> bool:
    """发送语音到飞书
    
    Args:
        text: 要转语音的文字
        voice: 语音音色
        target: 目标群ID（可选）
               - 不传/None: 使用当前群ID（从环境变量或默认值）
               - 传值: 主动发送到这个群
    """
    # 如果没传 target，尝试从环境变量获取当前群ID
    # 否则使用当前群作为默认值（回复场景）
    if not target:
        import uuid as uuid_module
        target = os.environ.get("FEISHU_CHAT_ID") or os.environ.get("OC_CHAT_ID")
        print(f"📤 未指定目标，使用当前群: {target}")
    
    print(f"📝 文字: {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"🎤 语音: {voice}")
    print(f"📤 发送到群: {target}")
    
    try:
        opus_file = text_to_opus(text, voice)
        print(f"✅ 语音生成: {opus_file}")
        
        # 复制到允许的目录（加时间戳防止竞争）
        import shutil
        timestamp = uuid.uuid4().hex[:8]
        outbound_dir = os.path.expanduser("~/.openclaw/media/outbound")
        os.makedirs(outbound_dir, exist_ok=True)
        target_file = os.path.join(outbound_dir, f"feishu_voice_{timestamp}.opus")
        shutil.copy(opus_file, target_file)
        
        # 构建发送命令
        cmd = ["openclaw", "message", "send", "--channel", "feishu"]
        
        # 只有传入 target 时才加 --target 参数
        # 不传 = 回复场景，OpenClaw 自动发回当前群
        if target:
            cmd.extend(["--target", target])
        
        cmd.extend(["--media", target_file, "--message", "语音消息"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 发送成功！")
            return True
        else:
            print(f"⚠️ 发送失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="飞书语音发送器 (Edge TTS)")
    parser.add_argument("text", nargs="?", help="要转语音的文字")
    parser.add_argument("voice", nargs="?", default=DEFAULT_VOICE, help="语音音色")
    parser.add_argument("-t", "--target", default=None, 
                        help="目标群ID（可选，不传则为回复模式）")
    
    args = parser.parse_args()
    
    if not args.text:
        print("飞书语音发送器 (Edge TTS)")
        print(f"用法: {sys.argv[0]} '文字' [语音] [-t 群ID]")
        print("  - 不传 -t: 回复模式，自动发回当前群")
        print("  - 传 -t: 主动发送到指定群")
        print(f"语音: xiaoxiao(默认), yunyang, yunxi, xiaoyi, yunjian, xiaobei")
        sys.exit(1)
    
    send_voice(args.text, args.voice, args.target)


if __name__ == "__main__":
    main()
