#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: Audio-Segmenter
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 支持单个音频文件或整个文件夹的智能切片，可保留原始目录结构，自动处理 ffmpeg 缺失问题，专为 OpenClaw 设计。
"""

# 基础用法
# 单个文件，每 30 秒切一片
# python scripts\audio_slicer.py -i "F:\命理学-音频\猴哥说易\月支月令如何看一个人事业！.mp3" -d 30 -o "F:\命理学-音频-切片" 
# 整个文件夹（递归）
# python scripts\audio_slicer.py -i "F:\命理学-音频" -d 60 -r -o "F:\命理学-音频-切片"

#在 OpenClaw 聊天中
# 请使用 audio-segmenter 技能，将 "F:\命理学-音频\猴哥说易\月支月令如何看一个人事业！.mp3" 文件进行切片，输出到 "F:\命理学-音频-切片"。
# 请使用 audio-segmenter 技能，将 "F:\命理学-音频" 目录下的所有MP3文件进行切片，输出到 "F:\命理学-音频-切片"。

import os
import argparse
import subprocess
from pathlib import Path
from logger_manager import LoggerManager
import env_manager
import ensure_package
ensure_package.pip("pydub", "pydub","AudioSegment")
ensure_package.pip("ffmpeg-downloader")
# 现在添加所有导入语句
from pydub import AudioSegment
from pydub.utils import make_chunks
import ffmpeg_downloader as ffdl
import importlib

# # --- 日志系统初始化 ---
logger = LoggerManager.setup_logger(logger_name="audio-segmenter")

def ensure_ffmpeg():
    """自动检测 + 下载 ffmpeg（已彻底修复 --quiet 错误 + 更稳定）"""
    # 关键修复：判断 None + 移除 --quiet
    if ffdl.ffmpeg_path is None or not os.path.exists(ffdl.ffmpeg_path):
        logger.info("⚠️  未检测到 ffmpeg，正在自动下载便携版到本地（只需一次，约 100-200MB）...")
        logger.info("   下载来源：Windows=gyan.dev | Linux=johnvansickle | macOS=evermeet")
        
        # 🔥 关键：自动输入 Y（默认 yes），彻底无交互
        logger.info("   自动确认下载中...")
        subprocess.run(["ffdl", "install"], input="Y\n", text=True, check=True)
        
        # 下载完后刷新模块
        importlib.reload(ffdl)
        
        logger.info("✅ 下载 + 安装完成！") 
        #C:\Users\Administrator\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin

    # 添加到 PATH + 强制 pydub 使用
    ffdl.add_path()
    AudioSegment.converter = ffdl.ffmpeg_path

    logger.info(f"✅ ffmpeg 已就绪 → {ffdl.ffmpeg_path}")
    return True


def process_file(file_path: str, duration_sec: int, target_dir: str):
    """处理单个音频文件，保存到指定目录"""
    try:
        audio = AudioSegment.from_file(file_path)
        chunk_length_ms = duration_sec * 1000
        chunks = make_chunks(audio, chunk_length_ms)

        base_name = os.path.splitext(os.path.basename(file_path))[0]
        ext = os.path.splitext(file_path)[1].lower()

        for i, chunk in enumerate(chunks):
            output_name = f"{base_name}_slice_{i+1:03d}{ext}"
            output_path = os.path.join(target_dir, output_name)

            format_name = ext[1:] if ext else "wav"
            chunk.export(output_path, format=format_name)
            logger.info(f"已生成：{output_path}  ({len(chunk)/1000:.1f}秒)")

    except Exception as e:
        logger.info(f"处理失败 {file_path}：{e}")

def main():
    global args

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)

    # 决定输出根目录
    if args.output is not None:
        output_root = os.path.abspath(args.output)
    else:
        if os.path.isfile(input_path):
            output_root = os.path.dirname(input_path)
        else:
            parent = os.path.dirname(input_path) or "."
            folder_name = os.path.basename(input_path.rstrip(os.sep))
            output_root = os.path.join(parent, f"{folder_name}_sliced_audio")

    os.makedirs(output_root, exist_ok=True)
    logger.info(f"输出根目录：{output_root}")

    if os.path.isfile(input_path):
        logger.info(f"处理单个文件：{input_path}")
        process_file(input_path, args.duration, output_root)

    elif os.path.isdir(input_path):
        logger.info(f"扫描文件夹：{input_path} （递归：{args.recursive}）")
        exts = ('.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.wma')

        for root, dirs, files in os.walk(input_path):
            if not args.recursive and root != input_path:
                continue

            # 计算相对路径，保持目录结构
            rel_path = os.path.relpath(root, input_path)
            target_dir = os.path.join(output_root, rel_path)
            os.makedirs(target_dir, exist_ok=True)

            for file in files:
                if file.lower().endswith(exts):
                    full_path = os.path.join(root, file)
                    process_file(full_path, args.duration, target_dir)

    else:
        logger.info("❌ 输入路径不存在")

if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()# 必须最先执行（包含 GPU 自动检测）
    ensure_ffmpeg()

    parser = argparse.ArgumentParser(description="OpenClaw 音频切片工具（自动处理 ffmpeg）")
    parser.add_argument("-i", "--input", required=True, help="输入文件或目录")
    parser.add_argument("-d", "--duration", type=int, default=60, help="切片时长（秒），默认 60")
    parser.add_argument("-o", "--output", default=None, help="输出目录（不传则：单文件→同目录，文件夹→原名_sliced_audio）")# ← 改成 None 作为标志
    parser.add_argument("-r", "--recursive", action="store_true", help="递归子文件夹")
    args = parser.parse_args()

    main()