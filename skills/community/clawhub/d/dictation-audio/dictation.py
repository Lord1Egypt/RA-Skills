#!/usr/bin/env python3
"""
英语单词听写音频生成器
根据用户输入的单词列表，生成每个单词读两遍的听写音频

安全性设计：
- 仅调用已验证的系统工具（edge-tts, ffmpeg）
- 使用shutil.which()验证工具存在
- 所有路径使用临时目录，不暴露敏感位置
- 输入过滤：仅允许英文字母、空格和连字符
"""

import re
import subprocess
import tempfile
import os
import sys
import shutil

# 验证依赖工具
def check_dependencies():
    """检查必需的工具是否可用"""
    missing = []
    for tool in ['edge-tts', 'ffmpeg']:
        if not shutil.which(tool):
            missing.append(tool)
    if missing:
        raise RuntimeError(f"缺少必需工具: {', '.join(missing)}")

VOICE = "en-GB-RyanNeural"
RATE = "-20%"
SILENCE_DURATION = 1  # 秒


def generate_word_audio(word: str, output_path: str) -> bool:
    """生成单个单词的音频"""
    edge_tts_path = shutil.which("edge-tts")
    if not edge_tts_path:
        raise RuntimeError("edge-tts 未安装")

    cmd = [
        edge_tts_path,
        "--voice", VOICE,
        f"--rate={RATE}",
        "--text", word,
        "--write-media", output_path
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        print(f"生成音频失败 '{word}': {result.stderr}")
        return False
    return True


def generate_silence(output_path: str, duration: int = 1) -> bool:
    """生成静音音频"""
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("ffmpeg 未安装")

    cmd = [
        ffmpeg_path, "-y",
        "-f", "lavfi",
        "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(duration),
        "-q:a", "9",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=10)
    return result.returncode == 0


def concat_audio(input_files: list, output_path: str, tmpdir: str) -> bool:
    """合并多个音频文件"""
    if not input_files:
        return False

    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("ffmpeg 未安装")

    # 使用临时目录内的文件
    list_file = os.path.join(tmpdir, "concat_list.txt")
    try:
        with open(list_file, "w") as f:
            for fp in input_files:
                if os.path.exists(fp) and os.path.getsize(fp) > 0:
                    f.write(f"file '{fp}'\n")
        
        cmd = [
            ffmpeg_path, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    finally:
        if os.path.exists(list_file):
            os.remove(list_file)


def validate_word(word: str) -> str:
    """验证并清理单词输入"""
    # 只保留英文字母、空格和连字符
    cleaned = re.sub(r'[^a-zA-Z\s\-]', '', word).strip()
    if not cleaned:
        return None
    # 长度限制
    if len(cleaned) > 100:
        return None
    return cleaned


def main():
    check_dependencies()
    
    # 读取用户输入
    print("请输入英语单词（每行一个，支持格式：word 或 word中文）：")
    user_input = sys.stdin.read().strip()
    
    # 处理输入：每行一个单词，去掉中文
    lines = user_input.strip().split('\n')
    words = []
    for line in lines:
        cleaned = validate_word(line)
        if cleaned:
            words.append(cleaned)
    
    if not words:
        print("没有找到有效的英文单词")
        return
    
    print(f"处理了 {len(words)} 个单词: {words}")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_files = []
        
        for i, word in enumerate(words):
            word_file = f"{tmpdir}/word_{i}.mp3"
            silence_file = f"{tmpdir}/silence_{i}.mp3"
            
            # 生成单词音频（第一遍）
            print(f"生成单词: {word} (第1遍)")
            if generate_word_audio(word, word_file):
                audio_files.append(word_file)
                audio_files.append(silence_file)
                # 生成单词音频（第二遍）
                audio_files.append(word_file)
            else:
                continue
            
            # 生成停顿
            print(f"生成停顿 (1秒)")
            generate_silence(silence_file, SILENCE_DURATION)
            
            # 单词间停顿（除了最后一个）
            if i < len(words) - 1:
                audio_files.append(silence_file)
        
        if audio_files:
            output_path = "/tmp/dictation.mp3"
            print("合并音频...")
            # 传递tmpdir以确保concat_list.txt在临时目录内
            if concat_audio(audio_files, output_path, tmpdir):
                size = os.path.getsize(output_path)
                print(f"✅ 完成: {output_path}")
                print(f"文件大小: {size / 1024:.1f} KB")
            else:
                print("生成失败")


if __name__ == "__main__":
    main()
