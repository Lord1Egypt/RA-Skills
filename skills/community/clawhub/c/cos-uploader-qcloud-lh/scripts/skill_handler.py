#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Skill 入口脚本
- 接收 OpenClaw 通过命令行参数传入的图片消息
- 解析图片本地缓存路径
- 调用 COS 上传模块完成上传
- 输出结果供 OpenClaw 回复用户

使用方式：
    python3 skill_handler.py '<JSON消息体>'
    
    或者直接传入图片路径：
    python3 skill_handler.py --file /path/to/image.jpg
"""

import sys
import os
import re
import json
import argparse
import logging
from datetime import datetime

# 将脚本所在目录加入 Python 路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from cos_uploader import upload_file_to_cos
from config import STORAGE_CLASS_OPTIONS

# ==================== 日志配置 ====================

LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOG_DIR, mode=0o700, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(
            os.path.join(LOG_DIR, f"upload_{datetime.now().strftime('%Y%m%d')}.log"),
            encoding='utf-8'
        ),
        logging.StreamHandler(sys.stderr),  # 日志输出到 stderr，不干扰 stdout 的结果
    ]
)
logger = logging.getLogger(__name__)

# ==================== 消息解析 ====================

# 匹配 OpenClaw 图片消息中的本地缓存路径
MEDIA_PATTERN = re.compile(
    r'\[media attached: (.+?) \((.+?)\)\]'
)


def parse_image_from_message(message_json_str):
    """
    从 OpenClaw 消息体中解析图片本地路径
    
    Args:
        message_json_str: OpenClaw 传入的 JSON 字符串
    
    Returns:
        tuple: (file_path, mime_type) 或 (None, None)
    """
    try:
        msg = json.loads(message_json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败: {e}")
        return None, None

    # 从 message.content 中提取 text
    content_list = msg.get("message", {}).get("content", [])
    for content_item in content_list:
        if content_item.get("type") == "text":
            text = content_item.get("text", "")
            match = MEDIA_PATTERN.search(text)
            if match:
                file_path = match.group(1)
                mime_type = match.group(2)
                return file_path, mime_type

    logger.warning("消息中未找到图片附件信息")
    return None, None


def format_file_size(size_bytes):
    """格式化文件大小为人类可读格式"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def process_image(file_path, mime_type=None):
    """
    处理图片上传的核心逻辑
    
    Args:
        file_path: 图片本地路径
        mime_type: MIME 类型（可选）
    
    Returns:
        str: 回复给用户的消息
    """
    logger.info(f"开始处理图片: {file_path}")

    # 检查文件是否存在
    if not os.path.exists(file_path):
        error_msg = f"❌ 图片文件不存在: {file_path}"
        logger.error(error_msg)
        return error_msg

    # 检查是否为图片类型
    if mime_type and not mime_type.startswith("image/"):
        error_msg = f"❌ 不支持的文件类型: {mime_type}，仅支持图片"
        logger.warning(error_msg)
        return error_msg

    # 获取文件大小
    file_size = os.path.getsize(file_path)
    logger.info(f"文件大小: {format_file_size(file_size)}")

    # 上传到 COS
    logger.info("正在上传到 COS...")
    result = upload_file_to_cos(file_path)

    if result["success"]:
        cos_key = result["cos_key"]
        etag = result.get("etag", "")
        size_str = format_file_size(file_size)

        # 从上传结果中获取存储类型的中文描述
        storage_class = result.get("storage_class", "STANDARD_IA")
        storage_desc = "低频存储"  # 默认
        for _, (cls, desc) in STORAGE_CLASS_OPTIONS.items():
            if cls == storage_class:
                storage_desc = desc.split("（")[0]  # 取括号前的简短描述
                break

        success_msg = (
            f"✅ 照片上传成功！\n"
            f"📁 存储路径: {cos_key}\n"
            f"📦 文件大小: {size_str}\n"
            f"🏷️ 存储类型: {storage_desc}"
        )
        logger.info(f"上传成功: cos_key={cos_key}, etag={etag}")
        return success_msg
    else:
        error = result.get("error", "未知错误")
        error_msg = f"❌ 照片上传失败: {error}"
        logger.error(error_msg)
        return error_msg


# ==================== 主入口 ====================

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Skill: 微信照片上传到腾讯云 COS"
    )
    parser.add_argument(
        "message",
        nargs="?",
        help="OpenClaw 传入的 JSON 消息体"
    )
    parser.add_argument(
        "--file", "-f",
        help="直接指定图片文件路径（调试用）"
    )

    args = parser.parse_args()

    # 方式1：直接指定文件路径（调试模式）
    if args.file:
        result_msg = process_image(args.file)
        print(result_msg)
        return

    # 方式2：从 OpenClaw JSON 消息体中解析
    if args.message:
        file_path, mime_type = parse_image_from_message(args.message)
        if file_path:
            result_msg = process_image(file_path, mime_type)
            print(result_msg)
        else:
            print("⚠️ 未检测到图片，请发送一张照片给我")
        return

    # 方式3：从 stdin 读取（管道模式）
    if not sys.stdin.isatty():
        message_str = sys.stdin.read().strip()
        if message_str:
            file_path, mime_type = parse_image_from_message(message_str)
            if file_path:
                result_msg = process_image(file_path, mime_type)
                print(result_msg)
            else:
                print("⚠️ 未检测到图片，请发送一张照片给我")
            return

    # 无输入
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
