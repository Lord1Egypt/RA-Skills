#!/usr/bin/env python3
"""
Edge TTS - 微软免费文本转语音
无需 API Key，直接使用微软 Neural 语音
"""

import asyncio
import edge_tts
import sys

# 支持的语音
VOICES = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",   # 女声，活泼专业
    "xiaoyi": "zh-CN-XiaoyiNeural",      # 女声，温柔亲切
    "yunyang": "zh-CN-YunyangNeural",   # 男声，沉稳
    "yunxi": "zh-CN-YunxiNeural",        # 男声，北京话
    "yunze": "zh-CN-YunzeNeural",         # 男声，活力
}

async def text_to_speech(text, voice="zh-CN-XiaoxiaoNeural", output="output.mp3"):
    """生成语音"""
    print(f"🎤 使用声音: {voice}")
    print(f"📝 文本: {text}")
    print(f"📁 输出: {output}")
    print(f"⏳ 正在生成...")
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output)
        
        # 检查文件大小
        import os
        size = os.path.getsize(output)
        
        if size > 0:
            print(f"✅ 生成成功！文件大小: {size} 字节")
            return True
        else:
            print(f"❌ 生成失败：文件为空")
            return False
            
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False


async def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 edge_tts_async.py <文本> [声音] [输出文件]")
        print("")
        print("示例:")
        print("  python3 edge_tts_async.py \"你好\"")
        print("  python3 edge_tts_async.py \"你好\" xiaoxiao hello.mp3")
        print("")
        print("可用声音:")
        for name, voice in VOICES.items():
            print(f"  {name}: {voice}")
        return 1
    
    text = sys.argv[1]
    voice_name = sys.argv[2] if len(sys.argv) > 2 else "xiaoxiao"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "output.mp3"
    
    # 获取语音 ID
    voice_id = VOICES.get(voice_name, "zh-CN-XiaoxiaoNeural")
    
    success = await text_to_speech(text, voice_id, output_file)
    return 0 if success else 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
