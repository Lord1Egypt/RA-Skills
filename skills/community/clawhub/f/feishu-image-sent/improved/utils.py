#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书图片发送工具函数
智能图片处理和发送
"""

import os
import sys
import subprocess
import shutil
from PIL import Image
import json

# 配置
MAX_SIZE_MB = 10
COMPRESS_SIZE_MB = 5
COMPRESS_QUALITY = 85
KEEP_ORIGINAL = True
WORKSPACE_DIR = "/Users/bornforthis/.openclaw/workspace"
TEMP_DIR = "/tmp"
LOG_LEVEL = 1
SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "gif", "webp", "bmp", "tiff"]
OUTPUT_FORMAT = "jpg"

def log(message, level=1):
    """日志输出"""
    if LOG_LEVEL >= level:
        print(f"[{level}] {message}")

def get_file_size_mb(file_path):
    """获取文件大小（MB）"""
    if not os.path.exists(file_path):
        return 0
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def check_file_format(file_path):
    """检查文件格式是否支持"""
    if not os.path.exists(file_path):
        return False
    
    filename = os.path.basename(file_path)
    extension = filename.lower().split('.')[-1]
    
    return extension in SUPPORTED_FORMATS

def compress_image(input_path, quality=85, max_size_mb=10):
    """
    智能图片压缩
    :param input_path: 输入图片路径
    :param quality: JPEG质量 (1-100)
    :param max_size_mb: 最大文件大小(MB)
    :return: 压缩后的图片路径
    """
    try:
        # 获取文件信息
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        
        # 打开图片
        with Image.open(input_path) as img:
            # 转换为RGB模式
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 获取原始尺寸
            original_width, original_height = img.size
            aspect_ratio = original_width / original_height
            
            log(f"原始图片尺寸: {original_width}x{original_height}")
            
            # 计算目标大小
            target_size_bytes = max_size_mb * 1024 * 1024
            current_size = os.path.getsize(input_path)
            
            # 如果需要调整尺寸
            if current_size > target_size_bytes:
                scale_ratio = (target_size_bytes / current_size) ** 0.5
                new_width = int(original_width * scale_ratio)
                new_height = int(original_height * scale_ratio)
                
                log(f"调整尺寸: {original_width}x{original_height} -> {new_width}x{new_height}")
                
                # 调整尺寸
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存压缩后的图片
            compressed_path = os.path.join(TEMP_DIR, f"compressed_{name}.{OUTPUT_FORMAT}")
            img.save(compressed_path, OUTPUT_FORMAT.upper(), quality=quality, optimize=True)
            
            # 检查压缩后的大小
            compressed_size = os.path.getsize(compressed_path)
            compressed_size_mb = compressed_size / (1024 * 1024)
            log(f"压缩后大小: {compressed_size_mb:.2f} MB")
            
            return compressed_path
    
    except Exception as e:
        log(f"压缩图片失败: {e}")
        return input_path

def send_image_to_feishu(image_path, version="original"):
    """发送图片到飞书"""
    try:
        # 确保工作空间目录存在
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        
        filename = os.path.basename(image_path)
        workspace_path = os.path.join(WORKSPACE_DIR, filename)
        
        # 复制到工作空间
        shutil.copy2(image_path, workspace_path)
        
        # 发送到飞书
        result = subprocess.run([
            sys.executable, "-c", 
            f"from message import message; message(action='send', media='{workspace_path}')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            log(f"✅ {version}版本已发送到飞书: {filename}")
            return True
        else:
            log(f"❌ 发送失败: {result.stderr}")
            return False
            
    except Exception as e:
        log(f"❌ 发送图片失败: {e}")
        return False

def process_image(input_path, base_name):
    """
    智能处理图片
    :param input_path: 输入图片路径
    :param base_name: 基础文件名
    """
    # 检查文件是否存在
    if not os.path.exists(input_path):
        return "错误: 文件不存在"
    
    # 检查文件格式
    if not check_file_format(input_path):
        return f"错误: 不支持的文件格式，支持的格式: {', '.join(SUPPORTED_FORMATS)}"
    
    # 获取文件大小
    file_size_mb = get_file_size_mb(input_path)
    log(f"📏 检测到图片大小: {file_size_mb:.2f} MB")
    
    # 小图片直接发送
    if file_size_mb <= COMPRESS_SIZE_MB:
        log("🟢 小图片，直接发送")
        send_image_to_feishu(input_path, "original")
        return "小图片，直接发送"
    
    # 大图片，双版本发送（压缩版 + 原图）
    else:
        log("🔴 图片过大，发送压缩版和原图版")
        
        # 发送压缩版
        compressed_path = compress_image(input_path, COMPRESS_QUALITY, MAX_SIZE_MB)
        send_image_to_feishu(compressed_path, "compressed")
        
        # 发送原图版
        send_image_to_feishu(input_path, "original")
        
        # 清理压缩文件
        if os.path.exists(compressed_path):
            os.remove(compressed_path)
        
        return "图片过大，已发送压缩版和原图版"

def main():
    """主函数"""
    if len(sys.argv) != 3:
        print("使用方法: python3 utils.py process_image <input_path> <base_name>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    base_name = sys.argv[2]
    
    result = process_image(input_path, base_name)
    print(f"处理结果: {result}")

if __name__ == "__main__":
    main()