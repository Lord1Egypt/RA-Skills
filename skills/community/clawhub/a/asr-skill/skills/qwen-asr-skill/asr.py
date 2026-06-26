#!/usr/bin/env python3
"""
Qwen3 ASR 推理模块
支持CPU端侧运行，支持多语言和方言识别
"""

import os
import sys
import time
import torch
import argparse
import base64
import numpy as np
from io import BytesIO
from typing import Optional, List, Dict, Any
# 导入CPU优化模块
try:
    from cpu_optimization import optimize_for_cpu, optimize_model_for_cpu, warmup_model
    OPTIMIZE_CPU = True
except ImportError:
    OPTIMIZE_CPU = False

# 配置环境变量
os.environ.setdefault('TRANSFORMERS_CACHE', './models')
os.environ.setdefault('HF_HOME', './models')

# 延迟导入，加快启动速度
_qwen_model = None
_forced_aligner = None

def get_model(
    model_name: str = "Qwen/Qwen3-ASR-0.6B",
    device: str = "cpu",
    dtype: str = "float32",
    max_new_tokens: int = 1024,
    batch_size: int = 4,
    enable_forced_aligner: bool = False,
    forced_aligner_model: str = "Qwen/Qwen3-ForcedAligner-0.6B"
):
    """获取或初始化ASR模型"""
    global _qwen_model, _forced_aligner
    
    # CPU优化
    if device == 'cpu' and OPTIMIZE_CPU:
        optimize_for_cpu()
    
    if _qwen_model is None:
        from qwen_asr import Qwen3ASRModel
        
        # 转换dtype
        torch_dtype = torch.float32
        if dtype == "bfloat16" and torch.cpu.is_bf16_supported():
            torch_dtype = torch.bfloat16
        elif dtype == "float16":
            torch_dtype = torch.float16
        
        # 初始化模型
        model_kwargs = {
            "dtype": torch_dtype,
            "device_map": device,
            "max_inference_batch_size": batch_size,
            "max_new_tokens": max_new_tokens,
        }
        
        if enable_forced_aligner:
            model_kwargs["forced_aligner"] = forced_aligner_model
            model_kwargs["forced_aligner_kwargs"] = {
                "dtype": torch_dtype,
                "device_map": device,
            }
        
        _qwen_model = Qwen3ASRModel.from_pretrained(
            model_name,
            **model_kwargs
        )
    
    return _qwen_model

def transcribe_audio(
    audio_input: str,
    language: Optional[str] = None,
    return_timestamps: bool = False,
    model_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    转录音频为文字
    
    Args:
        audio_input: 音频路径、URL、base64数据或(numpy array, sample rate)元组
        language: 指定语言/方言，None则自动检测
        return_timestamps: 是否返回时间戳
        model_config: 模型配置参数
    
    Returns:
        转录结果字典
    """
    if model_config is None:
        model_config = {}
    
    start_time = time.time()
    
    # 获取模型
    model = get_model(**model_config)
    
    # 处理base64输入
    if isinstance(audio_input, str) and audio_input.startswith('data:audio'):
        # 提取base64数据
        if ';base64,' in audio_input:
            audio_input = audio_input.split(';base64,')[1]
        audio_data = base64.b64decode(audio_input)
        # 转换为BytesIO对象
        audio_input = BytesIO(audio_data)
    
    # 执行转录
    results = model.transcribe(
        audio=audio_input,
        language=language,
        return_time_stamps=return_timestamps,
    )
    
    result = results[0] if results else None
    
    if result is None:
        return {
            "success": False,
            "error": "No transcription result",
            "duration": time.time() - start_time
        }
    
    # 构建返回结果
    response = {
        "success": True,
        "data": {
            "text": result.text.strip(),
            "language": result.language,
            "confidence": getattr(result, 'confidence', 0.9),  # 如果没有置信度则默认0.9
            "duration": time.time() - start_time
        }
    }
    
    # 添加时间戳
    if return_timestamps and hasattr(result, 'time_stamps') and result.time_stamps:
        response["data"]["timestamps"] = [
            {
                "text": ts.text,
                "start": ts.start_time,
                "end": ts.end_time
            }
            for ts in result.time_stamps
        ]
    
    return response

def align_audio_text(
    audio_input: str,
    text: str,
    language: str,
    model_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    音频和文本强制对齐
    
    Args:
        audio_input: 音频输入
        text: 对应的文本
        language: 语言
        model_config: 模型配置
    
    Returns:
        对齐结果
    """
    global _forced_aligner
    
    if model_config is None:
        model_config = {}
    
    start_time = time.time()
    
    if _forced_aligner is None:
        from qwen_asr import Qwen3ForcedAligner
        
        torch_dtype = torch.float32
        if model_config.get('dtype') == "bfloat16" and torch.cpu.is_bf16_supported():
            torch_dtype = torch.bfloat16
        
        _forced_aligner = Qwen3ForcedAligner.from_pretrained(
            model_config.get('forced_aligner_model', "Qwen/Qwen3-ForcedAligner-0.6B"),
            dtype=torch_dtype,
            device_map=model_config.get('device', 'cpu'),
        )
    
    results = _forced_aligner.align(
        audio=audio_input,
        text=text,
        language=language,
    )
    
    if not results:
        return {
            "success": False,
            "error": "No alignment result",
            "duration": time.time() - start_time
        }
    
    alignment = results[0]
    
    return {
        "success": True,
        "data": {
            "alignment": [
                {
                    "text": item.text,
                    "start": item.start_time,
                    "end": item.end_time
                }
                for item in alignment
            ],
            "duration": time.time() - start_time
        }
    }

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='Qwen3 ASR 命令行工具')
    parser.add_argument('audio', help='音频文件路径或URL')
    parser.add_argument('--language', help='指定语言/方言')
    parser.add_argument('--model', default='Qwen/Qwen3-ASR-0.6B', help='模型名称或路径')
    parser.add_argument('--device', default='cpu', help='运行设备 (cpu/cuda)')
    parser.add_argument('--dtype', default='float32', help='数据类型 (float32/bfloat16/float16)')
    parser.add_argument('--timestamps', action='store_true', help='返回时间戳')
    parser.add_argument('--align-text', help='用于强制对齐的文本')
    
    args = parser.parse_args()
    
    model_config = {
        "model_name": args.model,
        "device": args.device,
        "dtype": args.dtype,
    }
    
    try:
        if args.align_text:
            # 强制对齐模式
            result = align_audio_text(
                audio_input=args.audio,
                text=args.align_text,
                language=args.language,
                model_config=model_config
            )
        else:
            # 转录模式
            result = transcribe_audio(
                audio_input=args.audio,
                language=args.language,
                return_timestamps=args.timestamps,
                model_config=model_config
            )
        
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "duration": 0
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()