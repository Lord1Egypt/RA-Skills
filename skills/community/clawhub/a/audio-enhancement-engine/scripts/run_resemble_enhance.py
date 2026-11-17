#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Name: audio-enhancement-engine
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 这是一个基于 PyTorch 与 Resemble-Enhance 模型构建的专业级语音增强工具，采用纯自动化、开箱即用设计，
无需手动配置环境依赖与音频工具，可快速实现语音降噪、音质修复、人声增强等核心功能，支持单文件处理与批量文件夹处理，
兼顾普通用户的易用性与开发者的定制化需求。
核心定位
    专为人声音频优化打造的自动化处理引擎，解决录音杂音、背景噪音、音质模糊、音频失真等问题，适用于录音修复、语音素材整理、
自媒体音频处理、语音数据预处理等场景，全程自动适配 GPU/CPU 加速，无需专业音频知识即可使用。
"""

import os
import time
import subprocess
import ensure_package
import env_manager
ensure_package.pip("torch")
ensure_package.pip("soundfile")
ensure_package.pip("numpy==1.26.4")
ensure_package.pip("librosa==0.10.2")
ensure_package.pip("einops")
ensure_package.pip("torchdiffeq")
ensure_package.pip("ffmpeg-downloader")
ensure_package.pip("pydub", "pydub", "AudioSegment")
ensure_package.pip("torchaudio")
ensure_package.pip("celluloid")
ensure_package.pip("deepspeed")
ensure_package.pip("omegaconf")
ensure_package.pip("ptflops")
ensure_package.pip("resampy")
ensure_package.pip("tabulate")
ensure_package.pip("omegaconf")
ensure_package.pip("git+https://github.com/resemble-ai/resemble-enhance.git",fallback_zip="resemble-enhance-0.0.1.zip")
import torch
import soundfile as sf
import torchaudio
from pydub import AudioSegment
import ffmpeg_downloader as ffdl
import importlib
from logger_manager import LoggerManager
from resemble_enhance.enhancer.inference import enhance, denoise
import time
from pathlib import Path
from typing import Union, Optional, Tuple, List

logger = LoggerManager.setup_logger(logger_name="audio-enhancement-engine")

def ensure_ffmpeg():
    """自动检测 + 下载 ffmpeg（便携版）"""
    if ffdl.ffmpeg_path is None or not os.path.exists(ffdl.ffmpeg_path):
        logger.info("⚠️ 未检测到 ffmpeg，正在自动下载便携版到本地（只需一次）...")
        logger.info("下载来源：Windows=gyan.dev | Linux=johnvansickle | macOS=evermeet")

        # 自动确认下载（无交互）
        subprocess.run(["ffdl", "install"], input="Y\n", text=True, check=True)

        # 下载完后刷新模块
        importlib.reload(ffdl)
        logger.info("✅ 下载 + 安装完成！")

    # 添加到 PATH 并强制 pydub 使用
    ffdl.add_path()
    AudioSegment.converter = ffdl.ffmpeg_path

    # 额外把 ffmpeg 目录加入系统 PATH（对其他工具友好）
    ffmpeg_bin_dir = Path(ffdl.ffmpeg_path).parent
    os.environ["PATH"] = str(ffmpeg_bin_dir) + os.pathsep + os.environ.get("PATH", "")

    logger.info(f"✅ ffmpeg 已就绪 → {ffdl.ffmpeg_path}")
    return True

def get_device(device: Optional[str] = None) -> str:
    """
    智能获取推理设备
    优先级：用户指定 > CUDA（GPU）> CPU
    """
    if device is not None:
        # 验证用户指定的设备是否可用
        if device.startswith("cuda") and not torch.cuda.is_available():
            logger.warning(f"指定设备 {device} 不可用，回退到 CPU")
            return "cpu"
        return device
    
    # 自动检测
    if torch.cuda.is_available():
        device = "cuda"
        logger.info(f"✅ 检测到 GPU，使用设备: {device} ({torch.cuda.get_device_name(0)})")
    else:
        device = "cpu"
        logger.info("⚠️ 未检测到 GPU，使用 CPU 推理")
    return device

def enhance_speech(
    input_audio: Union[str, Path, torch.Tensor],
    output_path: Optional[Union[str, Path]] = None,
    use_enhance: bool = True,
    device: Optional[str] = None,
    nfe: int = 64,
    solver: str = "euler",
    lambd: float = 0.75,
    tau: float = 0.5,
    return_tensor: bool = False,
) -> Tuple[torch.Tensor, int]:
    """
    单文件语音增强函数（修复版：解决设备不匹配）
    """
    start_time = time.time()

    # 1. 智能获取设备（但不强制迁移数据，交给库内部处理）
    device = get_device(device)
    logger.info(f"使用设备: {device}")

    # 2. 加载音频（保持在 CPU，由库内部负责迁移）
    if isinstance(input_audio, (str, Path)):
        input_path = Path(input_audio)
        logger.info(f"加载音频: {input_path}")
        try:
            data, sample_rate = sf.read(str(input_path))
            waveform = torch.from_numpy(data).float()
            if waveform.dim() == 2:
                waveform = waveform.mean(dim=1)
            logger.info(f"音频加载成功 → 采样率: {sample_rate} Hz, 形状: {waveform.shape}")
        except Exception as e:
            logger.info(f"soundfile 加载失败: {e}")
            waveform, sample_rate = torchaudio.load(input_path)
            waveform = waveform.mean(dim=0).float()
    else:
        waveform = input_audio
        if waveform.dim() > 1:
            waveform = waveform.mean(dim=0).float()
        sample_rate = 44100
        logger.info("使用传入的 waveform tensor")

    # 【关键修复】：移除 waveform = waveform.to(device)
    # 原因：resemble_enhance 内部会根据 device 参数自动处理数据迁移，
    # 手动迁移会导致其内部计算 abs_max 等变量时出现 CPU/GPU 不匹配。

    # 3. 执行增强
    try:
        if use_enhance:
            logger.info(f"正在进行完整增强 (nfe={nfe}, solver={solver}, lambd={lambd})...")
            enhanced_wav, new_sr = enhance(
                waveform, sample_rate, device=device,
                nfe=nfe, solver=solver, lambd=lambd, tau=tau
            )
        else:
            logger.info("正在进行仅去噪...")
            enhanced_wav, new_sr = denoise(waveform, sample_rate, device=device)
    except Exception as e:
        logger.error(f"增强过程出错: {e}")
        raise

    # 4. 处理输出路径
    if output_path is None and isinstance(input_audio, (str, Path)):
        input_path = Path(input_audio)
        output_path = input_path.with_name(f"{input_path.stem}_resemble_enhance{input_path.suffix}")
    elif output_path is not None:
        output_path = Path(output_path)

    # 5. 保存文件
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 确保结果在 CPU 上（resemble_enhance 通常会自动移回，但为了保险）
        enhanced_np = enhanced_wav.cpu().numpy()
        if enhanced_np.ndim == 2:
            enhanced_np = enhanced_np.squeeze(0)
        
        # 保存为 32位浮点（推荐最高音质）或改成 'PCM_16'
        #'PCM_16' → 当前的 pcm_s16le
        #'PCM_24' → 24位 PCM
        #'FLOAT'  → 32位浮点（推荐，精度最高）
        #'PCM_32' → 32位整数（很少用）     
        sf.write(str(output_path), enhanced_np, new_sr, subtype='FLOAT')
        logger.info(f"✅ 已保存到: {output_path}")

    elapsed = time.time() - start_time
    logger.info(f"处理完成！耗时: {elapsed:.2f} 秒 | 输出采样率: {new_sr}Hz")

    if return_tensor:
        return enhanced_wav.cpu(), new_sr
    else:
        return (enhanced_wav.unsqueeze(0).cpu() if enhanced_wav.dim() == 1 else enhanced_wav.cpu(), new_sr)
        


def batch_enhance(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    use_enhance: bool = True,
    device: Optional[str] = None,  # 【关键改动 4】批量处理也支持设备参数
    nfe: int = 64,
    solver: str = "euler",
    lambd: float = 0.75,
    tau: float = 0.5,
    extensions: List[str] = None
):
    """
    批量处理指定目录下的所有音频文件（支持 GPU 推理）
    
    参数:
        input_dir: 输入音频目录
        output_dir: 输出目录（如果为None，则自动创建 input_dir_resemble_enhance 文件夹）
        extensions: 支持的音频扩展名，默认为常见格式
    """
    input_dir = Path(input_dir)
    if not input_dir.exists():
        raise FileNotFoundError(f"输入目录不存在: {input_dir}")

    # 如果未指定输出目录，则在同级创建 xxx_resemble_enhance 文件夹
    if output_dir is None:
        output_dir = input_dir.parent / f"{input_dir.name}_resemble_enhance"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"批量处理开始 → 输入: {input_dir} | 输出: {output_dir}")

    if extensions is None:
        extensions = [".wav", ".mp3", ".flac", ".m4a", ".ogg"]

    audio_files = []
    for ext in extensions:
        audio_files.extend(input_dir.glob(f"*{ext}"))
        audio_files.extend(input_dir.glob(f"*{ext.upper()}"))

    if not audio_files:
        logger.warning("目录中未找到支持的音频文件")
        return

    logger.info(f"共发现 {len(audio_files)} 个音频文件，开始处理...\n")

    for i, audio_file in enumerate(audio_files, 1):
        logger.info(f"[{i}/{len(audio_files)}] 正在处理: {audio_file.name}")
        try:
            # 输出文件放在输出目录，文件名保持原名
            output_file = output_dir / f"{audio_file.stem}{audio_file.suffix}"
            
            enhance_speech(
                input_audio=str(audio_file),
                output_path=output_file,
                use_enhance=use_enhance,
                device=device,  # 【关键改动 5】传递设备参数
                nfe=nfe,
                solver=solver,
                lambd=lambd,
                tau=tau,
                return_tensor=False
            )
            logger.info("-" * 60)
        except Exception as e:
            logger.error(f"处理 {audio_file.name} 失败: {e}")
            logger.error(f"❌ 处理失败: {audio_file.name}")
            logger.error("-" * 60)

    logger.info("批量处理完成！")
    logger.info(f"\n✅ 批量增强完成！输出目录: {output_dir}")