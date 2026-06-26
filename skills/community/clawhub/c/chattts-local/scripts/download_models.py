#!/usr/bin/env python3
"""
ChatTTS 模型下载脚本 - 使用 HuggingFace 镜像
"""

import os
import sys

# 设置镜像源
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def download():
    try:
        from huggingface_hub import snapshot_download
        
        print("📦 开始下载 ChatTTS 模型...")
        print("🌐 使用 HuggingFace 镜像源：https://hf-mirror.com")
        
        # 下载模型到指定目录
        model_dir = os.path.expanduser("~/.openclaw/ChatTTS/models")
        os.makedirs(model_dir, exist_ok=True)
        
        print(f"📁 下载目标：{model_dir}")
        print("⏳ 首次下载约需 5-10 分钟（约 500MB）...")
        
        # 使用 snapshot_download 下载
        download_path = snapshot_download(
            repo_id="2Noise/ChatTTS",
            local_dir=model_dir,
            local_dir_use_symlinks=False,
            force_download=True
        )
        
        print("")
        print("✅ 模型下载完成！")
        print(f"📂 模型位置：{download_path}")
        
        # 列出下载的文件
        print("")
        print("下载的文件:")
        for root, dirs, files in os.walk(model_dir):
            level = root.replace(model_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files[:10]:  # 只显示前 10 个文件
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                size_str = f"{size/1024/1024:.1f}MB" if size > 1024*1024 else f"{size/1024:.1f}KB"
                print(f'{subindent}{file} ({size_str})')
        
        return download_path
        
    except Exception as e:
        print(f"❌ 下载失败：{e}")
        print("")
        print("建议:")
        print("1. 检查网络连接")
        print("2. 稍后再试（可能是临时网络问题）")
        print("3. 手动从 https://huggingface.co/2Noise/ChatTTS 下载模型文件")
        sys.exit(1)

if __name__ == '__main__':
    download()
