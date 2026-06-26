#!/usr/bin/env python3
"""
ChatTTS 本地语音合成脚本
将文字转换为自然流畅的中文语音
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

def install_dependencies():
    """检查并安装依赖"""
    try:
        import ChatTTS
        import torch
        import torchaudio
        return True
    except ImportError:
        print("正在安装依赖...")
        os.system("pip install ChatTTS torch torchaudio -q")
        try:
            import ChatTTS
            return True
        except ImportError:
            print("❌ 依赖安装失败，请手动运行：pip install ChatTTS torch torchaudio")
            return False

def generate_speech(text, output_path, speed=1.0, pitch=1.0, seed=None):
    """生成语音"""
    import ChatTTS
    import torch
    import torchaudio
    import os
    import re
    from dataclasses import dataclass
    
    print(f"🎤 正在生成语音...")
    
    # 清理文本：移除不支持的标点符号
    clean_text = re.sub(r'[！]', '!', text)  # 中文感叹号转英文
    clean_text = re.sub(r'[，、]', ',', clean_text)  # 中文逗号转英文
    clean_text = re.sub(r'[。？]', '.', clean_text)  # 中文句号问号转英文
    
    print(f"文字：{clean_text[:50]}{'...' if len(clean_text) > 50 else ''}")
    
    # 设置国内镜像环境变量
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    
    # 初始化 ChatTTS
    chat = ChatTTS.Chat()
    
    # 加载模型（首次会自动下载）
    print("📦 加载模型中...（首次使用约需 1-2 分钟下载模型）")
    print("🌐 使用 HuggingFace 镜像源加速下载...")
    
    # 检查模型是否已存在
    model_dir = os.path.expanduser("~/.openclaw/ChatTTS/models")
    if os.path.exists(os.path.join(model_dir, "asset", "DVAE.pt")):
        print("✅ 检测到已下载的模型，直接加载...")
        chat.load(source="local", custom_path=model_dir)
    else:
        print("📥 首次使用，正在下载模型...")
        chat.download_models()
    
    # 设置参数（使用正确的数据类）
    params_infer_code = chat.InferCodeParams(
        temperature=0.3,
        top_P=0.7,
        top_K=20,
    )
    
    # 生成语音
    print("🔊 合成语音中...")
    wavs = chat.infer(
        [clean_text],
        params_infer_code=params_infer_code,
    )
    
    # 保存文件
    audio_data = torch.tensor(wavs[0])
    
    # 尝试使用 scipy 保存（兼容性更好）
    try:
        from scipy.io.wavfile import write
        import numpy as np
        # 转换为 16-bit PCM
        audio_np = (audio_data.numpy() * 32767).astype(np.int16)
        write(output_path, 24000, audio_np)
    except ImportError:
        # 回退到 torchaudio
        torchaudio.save(output_path, audio_data, 24000)
    
    print(f"✅ 语音生成成功：{output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='ChatTTS 语音合成')
    parser.add_argument('text', help='要转换的文字')
    parser.add_argument('--output', '-o', default='output.wav', help='输出文件路径')
    parser.add_argument('--speed', '-s', type=float, default=1.0, help='语速 (0.5-2.0)')
    parser.add_argument('--pitch', '-p', type=float, default=1.0, help='音调 (0.5-2.0)')
    parser.add_argument('--seed', type=int, default=None, help='随机种子（固定音色）')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 生成语音
    output_path = args.output
    generate_speech(args.text, output_path, args.speed, args.pitch, args.seed)
    
    print(f"\n📁 文件位置：{os.path.abspath(output_path)}")

if __name__ == '__main__':
    main()
