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
import os
import subprocess
from pathlib import Path
from logger_manager import LoggerManager
import env_manager
import ensure_package
ensure_package.pip("chardet")
ensure_package.pip("ftfy")
ensure_package.pip("gradio")
ensure_package.pip("phonemizer")
ensure_package.pip("progressbar")
ensure_package.pip("progressbar2")
ensure_package.pip("timm")
ensure_package.pip("unidecode")
ensure_package.pip("GitPython")
ensure_package.pip("streamlit>=1.12.0")
ensure_package.pip("git+https://github.com/qiuqiangkong/torchlibrosa.git",fallback_zip="torchlibrosa-master.zip")
ensure_package.pip("matplotlib")
ensure_package.pip("ffmpeg-downloader")
ensure_package.pip("pydub", "pydub", "AudioSegment")
ensure_package.pip("transformers")
import argparse
from pydub import AudioSegment
import ffmpeg_downloader as ffdl
import importlib

logger = LoggerManager.setup_logger(logger_name="audio-enhancement-engine")

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
    
def main():
    global args  # 批量模式需要访问

    if args.re:
        import run_resemble_enhance
        input_path = Path(args.input)
        if input_path.is_file():
            logger.info(f" {args.re} Resemble-Enhance 增强-单文件模式")
            # 单文件模式
            run_resemble_enhance.enhance_speech(
                input_audio=args.input,
                output_path=args.output,
                nfe=args.nfe,
                solver=args.solver,
                lambd=args.lambd,
                tau=args.tau
            )            
        else:
            logger.info(f" {args.re} Resemble-Enhance 增强-批量目录模式")
            # 批量目录模式
            run_resemble_enhance.batch_enhance(
                input_dir=args.input,
                output_dir=args.output,
                nfe=args.nfe,
                solver=args.solver,
                lambd=args.lambd,
                tau=args.tau
            )
    else:
        if args.hifi:
            import hifi_audio_enhance
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
            import voice_enhance
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
    ensure_ffmpeg()

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

    #run_resemble_enhance.py 专业级语音增强工具
    parser.add_argument("--re", action="store_true", help="Resemble-Enhance 模型构建的专业级语音增强工具")
    parser.add_argument("--nfe", type=int, default=64, help="推理步数：32更快，128效果更好，默认64")
    parser.add_argument("--solver", type=str, default="euler", choices=["euler", "midpoint", "rk4"], help="求解器：euler最快，rk4效果最好")
    parser.add_argument("--lambd", type=float, default=0.75, help="去噪强度 0~1，建议0.6~0.9")
    parser.add_argument("--tau", type=float, default=0.5, help="音质阈值，默认0.5")

    args = parser.parse_args()

    main()