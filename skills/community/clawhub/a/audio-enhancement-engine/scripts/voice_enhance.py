#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Name: audio-enhancement-engine
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 这是一个基于 VoiceFixer 的音频修复与增强工具模块，主要用于修复和提升音频的质量，尤其适合处理带噪、失真、低清晰度的语音、录音或老旧音频文件。
核心功能
    单文件增强：对单个音频文件进行 VoiceFixer 修复处理，提升语音清晰度、抑制背景噪声、修复轻微失真。
    目录批量处理：支持处理整个文件夹下的音频文件，可选择是否递归子目录。
    智能输出：自动为处理后的文件添加 _enhanced 后缀，并统一输出为 .wav 格式（VoiceFixer 推荐格式）。
    灵活配置：支持三种增强模式（mode 0/1/2）、是否使用 GPU 加速，以及是否递归处理子文件夹。
"""

from pathlib import Path
import os
import ensure_package
from logger_manager import LoggerManager
import soundfile as sf
from tqdm import tqdm
ensure_package.pip("packaging","packaging","version")
ensure_package.pip("audio-separator==0.30.2",force=True)
ensure_package.pip("numpy==1.26.4",force=True)
ensure_package.pip("librosa==0.10.2",force=True)
ensure_package.pip("git+https://github.com/haoheliu/voicefixer.git",fallback_zip="voicefixer-main.zip")
ensure_package.pip("hf_transfer")
from packaging import version
from voicefixer import VoiceFixer

logger = LoggerManager.setup_logger(logger_name="audio-enhancement-engine")

def is_audio_file(file_path: Path) -> bool:
    """检查是否为支持的音频文件"""
    audio_extensions = {'.wav', '.flac', '.mp3', '.m4a', '.ogg'}
    return file_path.suffix.lower() in audio_extensions

def enhance_single_file(vf: VoiceFixer, input_path: Path, output_path: Path, mode: int = 1, use_cuda: bool = False):
    """处理单个音频文件"""
    # ================== NumPy 兼容补丁 ==================
    import numpy as np
    if not hasattr(np, 'float'):
        np.float = float
    if not hasattr(np, 'int'):
        np.int = int
    if not hasattr(np, 'complex'):
        np.complex = complex
    # ===================================================

    logger.info(f"🎵 处理文件: {input_path}")
    try:
        vf.restore(
            input=str(input_path),
            output=str(output_path),
            mode=mode,
            cuda=use_cuda
        )
        logger.info(f"✅ 处理完成 → {output_path}")
        return True
    except Exception as e:
        logger.info(f"❌ 处理失败 {input_path}: {e}")
        return False
    
def is_same_path(input_dir: Path, output_dir: Path) -> bool:
    return input_dir.resolve(strict=False) == output_dir.resolve(strict=False)

def enhance_directory(vf: VoiceFixer, input_dir: Path, output_dir: Path, 
                     mode: int = 1, use_cuda: bool = False, recursive: bool = False):
    """批量处理目录下的音频文件"""
    pattern = "**/*" if recursive else "*"
    audio_files = [f for f in input_dir.glob(pattern) if f.is_file() and is_audio_file(f)]

    if not audio_files:
        logger.info(f"⚠️ 在 {input_dir} 中未找到支持的音频文件")
        return

    logger.info(f"找到 {len(audio_files)} 个音频文件，开始批量增强...")

    success_count = 0
    for audio_file in tqdm(audio_files, desc="增强音频"):
        relative = audio_file.relative_to(input_dir)
        if is_same_path(input_dir, output_dir):
            out_file = output_dir / relative.with_stem(relative.stem + "_enhanced")
        else:
            out_file = output_dir / relative.with_stem(relative.stem)
        out_file = out_file.with_suffix(".wav")   # VoiceFixer 输出推荐使用 wav

        out_file.parent.mkdir(parents=True, exist_ok=True)

        if enhance_single_file(vf, audio_file, out_file, mode, use_cuda):
            success_count += 1

    logger.info(f"✅ 批量处理完成！成功 {success_count}/{len(audio_files)} 个文件")


def enhance_audio(
    input_path: str,
    output_path: str = None,
    mode: int = 1,
    use_cuda: bool = False,
    recursive: bool = False
):
    """
    OpenClaw 技能核心函数 - 外部调用入口
    
    参数:
        input_path: 输入文件或目录路径
        output_path: 输出路径（单个文件时为文件路径，目录时为目录路径）
        mode: 增强模式 0/1/2 （推荐使用 1）
        use_cuda: 是否使用 GPU
        recursive: 目录模式下是否递归子目录
    """
    input_path = Path(input_path).expanduser().resolve()

    # ====================== 初始化缓存和模型 ======================
    cache_dir = Path(os.environ.get("VOICEFIXER_CACHE_DIR", str(Path.home() / ".cache/voicefixer")))
    logger.info(f"当前使用的缓存目录：{cache_dir}")

    vocoder_path = cache_dir / "synthesis_module" / "44100" / "model.ckpt-1490000_trimed.pt"
    if vocoder_path.exists():
        logger.info(f"✅ Vocoder 文件存在，大小: {vocoder_path.stat().st_size / (1024*1024):.1f} MB")
    else:
        logger.info("⚠️ Vocoder 文件不存在！首次运行会自动下载。")

    # 初始化 VoiceFixer
    logger.info("正在初始化 VoiceFixer 模型...")
    vf = VoiceFixer()
    logger.info("✅ VoiceFixer 初始化完成")

    # ====================== 处理逻辑 ======================
    if input_path.is_file():
        if not is_audio_file(input_path):
            logger.info(f"❌ 输入不是支持的音频文件: {input_path}")
            return False

        if output_path:
            out_path = Path(output_path).expanduser().resolve()
        else:
            out_path = input_path.with_stem(input_path.stem + "_enhanced").with_suffix(".wav")

        out_path.parent.mkdir(parents=True, exist_ok=True)

        return enhance_single_file(vf, input_path, out_path, mode, use_cuda)

    elif input_path.is_dir():
        if output_path:
            out_dir = Path(output_path).expanduser().resolve()
        else:
            out_dir = input_path.parent / f"{input_path.name}_enhanced"# 默认输出到输入目录自动加 _enhanced 后缀
        # 确保目录存在
        out_dir.mkdir(parents=True, exist_ok=True)

        enhance_directory(vf, input_path, out_dir, mode, use_cuda, recursive)
        return True

    else:
        logger.info(f"❌ 输入路径不存在: {input_path}")
        return False