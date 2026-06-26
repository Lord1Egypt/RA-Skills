#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Name: audio-enhancement-engine
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 本地音频增强与修复统一工具，集成 VoiceFixer（语音降噪/修复）和 AudioSR（高保真超级分辨率）。支持单文件与目录批量处理，自动适配最合适的增强模式，输出清晰、高质量的 48kHz WAV 文件。
提供了一个简洁、统一的命令行工具，用于实现两种不同的音频处理需求：
    高保真音频超分辨率增强（AudioSR）
    通用语音修复增强（VoiceFixer）
核心功能
    通过一个命令行工具，同时支持两种音频增强技术，并根据用户选择的模式自动调用对应的处理函数，实现“一个入口、两种能力”的设计目标。
"""

from pathlib import Path
from logger_manager import LoggerManager
import ensure_package
ensure_package.pip("chardet")
ensure_package.pip("ftfy")
ensure_package.pip("gradio")
ensure_package.pip("phonemizer")
ensure_package.pip("progressbar")
ensure_package.pip("timm")
ensure_package.pip("unidecode")
ensure_package.pip("git+https://github.com/qiuqiangkong/torchlibrosa.git",fallback_zip="torchlibrosa-master.zip")
ensure_package.pip("matplotlib")
import hifi_audio_enhance
import voice_enhance
import env_manager
import argparse

logger = LoggerManager.setup_logger(logger_name="audio-enhancement-engine")

def main():
    global args  # 批量模式需要访问

    if args.hifi:
        logger.info(f" {args.hifi} 高保真 audiosr（音频超分辨率到48kHz）")
        # 高保真 audiosr（音频超分辨率到48kHz）
        hifi_audio_enhance.run_audio_enhancement(
            input_path=args.input,
            output_dir=args.output,
            model_name=args.model_name,
            ddim_steps=args.ddim_steps,
            guidance_scale=args.guidance_scale,
            seed=args.seed,
            device=args.device
        )
    else:
        logger.info(f" {args.hifi} voicefixer（通用语音修复）")
        # voicefixer（通用语音修复）
        voice_enhance.enhance_audio(
            input_path=args.input,
            output_path=args.output,
            mode=args.mode,
            use_cuda=args.cuda,
            recursive=args.recursive
        )
    
if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()

    parser = argparse.ArgumentParser(description="OpenClaw Audio Skill - 音频超分辨率 & 语音修复 统一工具")
    parser.add_argument("-i", "--input", type=str, required=True,help="输入路径：单个音频文件 或 目录")
    parser.add_argument("-o", "--output", type=str, default=None,help="输出目录路径（可选）")      

    #voice_enhance.py voicefixer（通用语音修复）
    parser.add_argument("-m", "--mode", type=int, choices=[0, 1, 2], default=1,help="增强模式 (推荐 1)，默认=1")
    parser.add_argument("--cuda", action="store_true", default=False,help="是否使用 GPU")
    parser.add_argument("-r", "--recursive", action="store_true",help="递归处理子目录（仅目录模式有效）")

    #hifi_audio_enhance.py 高保真 audiosr（音频超分辨率到48kHz）
    parser.add_argument("--hifi", action="store_true", help="高保真 audiosr（音频超分辨率到48kHz）")
    parser.add_argument("--model_name", type=str, default="basic",choices=["basic", "speech"],help="模型名称，默认 basic")
    parser.add_argument("--ddim_steps", type=int, default=50,help="扩散步数，默认 50")
    parser.add_argument("--guidance_scale", type=float, default=3.5,help="引导尺度，默认 3.5")
    parser.add_argument("--seed", type=int, default=42,help="随机种子，默认 42")
    parser.add_argument("--device", type=str, default=None,choices=["cuda", "cpu"],help="运行设备")

    args = parser.parse_args()

    main()