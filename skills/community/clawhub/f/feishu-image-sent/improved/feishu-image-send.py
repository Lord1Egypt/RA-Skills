#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书图片发送 - 主入口脚本
智能图片处理和发送
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent
UTILS_FILE = SCRIPT_DIR / "utils.py"
CONFIG_FILE = SCRIPT_DIR / "config" / "settings.sh"

def load_config():
    """加载配置文件"""
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
    
    # 设置默认值
    config.setdefault('MAX_SIZE_MB', '10')
    config.setdefault('COMPRESS_SIZE_MB', '5')
    config.setdefault('COMPRESS_QUALITY', '85')
    config.setdefault('KEEP_ORIGINAL', 'true')
    config.setdefault('WORKSPACE_DIR', '/Users/bornforthis/.openclaw/workspace')
    config.setdefault('TEMP_DIR', '/tmp')
    config.setdefault('LOG_LEVEL', '1')
    config.setdefault('SUPPORTED_FORMATS', 'png,jpg,jpeg,gif,webp,bmp,tiff')
    config.setdefault('OUTPUT_FORMAT', 'jpg')
    
    # 转换数据类型
    config['MAX_SIZE_MB'] = float(config['MAX_SIZE_MB'])
    config['COMPRESS_SIZE_MB'] = float(config['COMPRESS_SIZE_MB'])
    config['COMPRESS_QUALITY'] = int(config['COMPRESS_QUALITY'])
    config['KEEP_ORIGINAL'] = config['KEEP_ORIGINAL'].lower() == 'true'
    config['LOG_LEVEL'] = int(config['LOG_LEVEL'])
    
    return config

def check_dependencies():
    """检查依赖"""
    # 检查python3
    if not subprocess.run(['which', 'python3'], capture_output=True).returncode == 0:
        print("❌ python3 命令不可用")
        return False
    
    # 检查PIL
    try:
        import PIL
    except ImportError:
        print("❌ PIL库未安装，请运行: pip install Pillow")
        return False
    
    # 检查utils.py
    if not UTILS_FILE.exists():
        print(f"❌ 工具文件不存在: {UTILS_FILE}")
        return False
    
    return True

def send_image(image_path, config):
    """发送图片"""
    try:
        # 创建必要的目录
        os.makedirs(config['WORKSPACE_DIR'], exist_ok=True)
        os.makedirs(config['TEMP_DIR'], exist_ok=True)
        
        # 获取文件信息
        image_path = Path(image_path)
        filename = image_path.name
        name = image_path.stem
        timestamp = image_path.stat().st_mtime
        
        # 检查文件格式
        supported_formats = config['SUPPORTED_FORMATS'].split(',')
        extension = filename.lower().split('.')[-1]
        
        if extension not in supported_formats:
            print(f"❌ 不支持的图片格式: {extension}")
            print(f"支持的格式: {', '.join(supported_formats)}")
            return False
        
        # 检查文件大小
        file_size = image_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"📁 文件名: {filename}")
        print(f"📏 文件大小: {file_size_mb:.2f} MB")
        
        # 调用工具函数处理图片
        result = subprocess.run([
            'python3', str(UTILS_FILE), 'process_image', str(image_path), f"{name}_{int(timestamp)}"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"🎉 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ 处理失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='飞书图片发送 - 智能图片处理和发送')
    parser.add_argument('image_path', help='图片文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    
    # 设置日志级别
    if args.verbose:
        config['LOG_LEVEL'] = 2
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查文件是否存在
    image_path = Path(args.image_path)
    if not image_path.exists():
        print(f"❌ 文件不存在: {image_path}")
        sys.exit(1)
    
    # 发送图片
    print("🖼️  飞书图片发送 - 智能图片处理和发送")
    print("========================================")
    
    if send_image(image_path, config):
        print("✅ 图片发送完成")
        sys.exit(0)
    else:
        print("❌ 图片发送失败")
        sys.exit(1)

if __name__ == "__main__":
    main()