
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Name: audio-enhancement-engine
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 这是一个基于 AudioSR 的音频超级分辨率（Audio Super-Resolution）增强工具模块，
主要用于将低采样率或低质量的音频提升到更高音质（默认输出 48kHz）。
核心功能
    单文件增强：使用 AudioSR 模型对单个音频文件进行超级分辨率处理，显著提升音频的清晰度、细节和高频表现。
    目录批量处理：支持传入一个文件夹，自动识别并处理其中所有常见音频文件（.wav、.mp3、.flac、.ogg、.m4a、.aac 等）。
    灵活输出：可指定输出路径或输出目录，未指定时自动在输入文件同目录生成带 _enhanced_48k 后缀的新文件。
"""

from pathlib import Path
import ensure_package
import os
import numpy as np
import torch
from config import MODEL_DIR, SKILL_ROOT, VENV_DIR
from logger_manager import LoggerManager

# 安装依赖
ensure_package.pip("torch")
ensure_package.pip("torchaudio")
ensure_package.pip("torchvision")
ensure_package.pip("git+https://github.com/haoheliu/versatile_audio_super_resolution.git",
                   fallback_zip="versatile_audio_super_resolution-main.zip")
ensure_package.pip("huggingface_hub")

from audiosr import build_model, super_resolution, save_wave
import importlib.metadata

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"   # 禁用高速下载器，避免锁文件错误
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# 日志与版本信息
logger = LoggerManager.setup_logger(logger_name="audio-enhancement-engine")

"""
使用 AudioSR 进行音频超级分辨率增强（支持返回 numpy 的版本）
"""
def enhance_audio_with_audiosr(
    input_path: str,
    output_path: str = None,
    model_name: str = "basic",
    ckpt_path: str = None,
    device: str = None,
    ddim_steps: int = 50,
    guidance_scale: float = 3.5,
    seed: int = 42
):
    # ================== NumPy 兼容补丁 ==================
    import numpy as np
    if not hasattr(np, 'float'):
        np.float = float
    if not hasattr(np, 'int'):
        np.int = int
    if not hasattr(np, 'complex'):
        np.complex = complex
    # ===================================================
    #     
    logger.info(f"正在增强音频: {input_path}")
    
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"使用设备: {device.upper()}")
    
    MODEL_DIR.mkdir(exist_ok=True)  # 确保模型目录存在

    model = build_model(ckpt_path=MODEL_DIR, model_name=model_name, device=device)

    # 自动生成输出路径（如果未指定）
    if output_path is None:
        input_path = Path(input_path)
        base_name = input_path.stem
        output_dir = input_path.parent
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{base_name}_enhanced_48k.wav"# 默认输出到输入目录自动加 _enhanced_48k 后缀
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"开始超级分辨率增强... (steps={ddim_steps}, guidance={guidance_scale})")
    
    # 执行增强
    waveform = super_resolution(
        model,
        str(input_path),
        ddim_steps=ddim_steps,
        guidance_scale=guidance_scale,
        seed=seed
    )
    
    # 兼容 numpy 和 tensor 输出
    if isinstance(waveform, np.ndarray):
        if waveform.ndim == 1:
            waveform = waveform[None, None, :]          # (1, 1, time)
        elif waveform.ndim == 2:
            if waveform.shape[0] > waveform.shape[1]:   # (time, channels) → (channels, time)
                waveform = waveform.T
            waveform = waveform[None, :, :]             # (1, channels, time)
        waveform = torch.from_numpy(waveform).float()
    elif isinstance(waveform, torch.Tensor):
        waveform = waveform.cpu()

    # 保存音频
    save_wave(
        waveform,
        inputpath=str(input_path),
        savepath=str(output_path.parent),
        name=output_path.stem,
        samplerate=48000
    )
    
    logger.info(f"✅ 增强完成！输出文件：{output_path}")
    return str(output_path)


def process_directory(input_dir: str, output_dir: str = None, **kwargs):
    """处理整个目录下的所有音频文件"""
    input_path = Path(input_dir)
    if not input_path.is_dir():
        logger.info(f"❌ 错误：{input_dir} 不是一个有效的目录")
        return

    # 支持的音频格式（可自行扩展）
    audio_extensions = {'.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac'}

    audio_files = [f for f in input_path.iterdir() 
                   if f.is_file() and f.suffix.lower() in audio_extensions]

    if not audio_files:
        logger.info(f"⚠️ 目录 {input_dir} 中没有找到支持的音频文件")
        return

    logger.info(f"找到 {len(audio_files)} 个音频文件，开始批量处理...")

    for audio_file in audio_files:
        try:
            if output_dir:
                out_path = Path(output_dir) / f"{audio_file.stem}_enhanced_48k.wav"
            else:
                out_path = input_path.parent / f"{input_path.name}_enhanced_48k"# 默认输出到输入目录自动加 _enhanced_48k 后缀
            
            enhance_audio_with_audiosr(
                input_path=str(audio_file),
                output_path=str(out_path) if out_path else None,
                **kwargs
            )
        except Exception as e:
            logger.info(f"❌ 处理文件 {audio_file} 时出错: {e}")


def run_audio_enhancement(
    input_path: str,
    output_dir: str = None,
    model_name: str = "basic",
    ddim_steps: int = 50,
    guidance_scale: float = 3.5,
    seed: int = 42,
    device: str = None
):
    """
    OpenClaw 技能推荐调用的主入口函数
    - input_path: 单个音频文件路径 或 目录路径
    - output_dir: 输出目录（可选）
    """
    common_kwargs = {
        "model_name": model_name,
        "ddim_steps": ddim_steps,
        "guidance_scale": guidance_scale,
        "seed": seed,
        "device": device
    }

    path_obj = Path(input_path)

    if path_obj.is_file():
        logger.info("模式：单个文件增强")
        return enhance_audio_with_audiosr(
            input_path=input_path,
            output_path=output_dir,   # 这里传入的是具体文件路径或目录
            **common_kwargs
        )
    elif path_obj.is_dir():
        logger.info("模式：目录批量增强")
        process_directory(
            input_dir=input_path,
            output_dir=output_dir,
            **common_kwargs
        )
        return "目录批量处理完成"
    else:
        error_msg = f"❌ 错误：输入路径 {input_path} 不存在或无法访问"
        logger.info(error_msg)
        return error_msg