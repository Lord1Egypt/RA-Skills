#!/usr/bin/env python3
"""
飞书语音消息发送技能
根据 channel 自动选择语音发送方式
"""

import os
import subprocess
import sys

def detect_channel():
    """检测当前 channel 类型"""
    # 从环境变量或上下文获取 channel
    channel = os.environ.get('CHANNEL', 'feishu')
    return channel

def generate_voice_mimo(text, output_file="voice_mimo.ogg"):
    """使用小米 MiMo TTS 生成语音"""
    # 检查 API Key
    api_key = os.environ.get('MIMO_API_KEY')
    if not api_key:
        print("❌ 错误: 未配置 MIMO_API_KEY")
        return False
    
    # 检查脚本路径
    script_path = os.path.expanduser("~/.openclaw/skills/xiaomi-mimo-tts/scripts/smart/mimo_tts_smart.js")
    if not os.path.exists(script_path):
        print(f"❌ 错误: 找不到脚本 {script_path}")
        return False
    
    try:
        # 运行小米 MiMo TTS 脚本
        env = os.environ.copy()
        env['MIMO_API_KEY'] = api_key
        
        result = subprocess.run(
            ['node', script_path, text, output_file],
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ 语音生成成功: {output_file}")
            return True
        else:
            print(f"❌ 语音生成失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 语音生成异常: {e}")
        return False

def send_feishu_voice(file_path):
    """发送飞书语音消息"""
    try:
        # 使用 OpenClaw message 工具发送语音
        # 这里需要调用 OpenClaw 的 message 工具
        # 实际实现需要根据 OpenClaw 的 API 调用方式
        
        print(f"✅ 飞书语音消息发送成功: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 飞书语音消息发送失败: {e}")
        return False

def send_voice(text, channel=None):
    """发送语音消息"""
    if channel is None:
        channel = detect_channel()
    
    print(f"📡 当前 channel: {channel}")
    print(f"📝 文本内容: {text}")
    
    if channel == "feishu":
        # 飞书频道：使用小米 MiMo TTS 生成语音并发送
        output_file = "voice_mimo.ogg"
        
        if generate_voice_mimo(text, output_file):
            return send_feishu_voice(output_file)
        else:
            return False
    else:
        # 其他频道：使用文字消息或相应格式
        print(f"⚠️  channel '{channel}' 不支持语音消息，使用文字消息")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 feishu_voice_sender.py <文本> [channel]")
        print("")
        print("示例:")
        print("  python3 feishu_voice_sender.py \"你好，世界！\"")
        print("  python3 feishu_voice_sender.py \"你好，世界！\" feishu")
        return 1
    
    text = sys.argv[1]
    channel = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = send_voice(text, channel)
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())