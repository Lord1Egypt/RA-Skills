#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FunAudioDenoise CLI Tool
智能音频降噪命令行工具

Usage:
    python denoise_cli.py <input_audio> [output_audio] [options]

Example:
    python denoise_cli.py input.wav output_denoised.wav
    python denoise_cli.py input.mp3 --format mp3 --sample-rate 16000
"""

import os
import sys
import time
import argparse
import threading
from pathlib import Path

# Add current directory to path for importing audio_process
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dashscope
from audio_process import Denoise, DenoiseParam, DenoiseResult, ResultCallback


class DenoiseCallback(ResultCallback):
    """回调处理类，用于接收降噪结果"""
    
    def __init__(self, output_path: str, verbose: bool = True):
        self.output_path = output_path
        self.verbose = verbose
        self.complete_event = threading.Event()
        self.file_handle = None
        self.audio_count = 0
        self.total_bytes = 0
        self.error_message = None
        self.output_info = None
        self.usage_info = None
        
    def on_open(self) -> None:
        if self.verbose:
            print("[INFO] WebSocket 连接已建立")
        try:
            self.file_handle = open(self.output_path, "wb")
        except Exception as e:
            print(f"[ERROR] 无法创建输出文件: {e}")
            self.error_message = str(e)
    
    def on_complete(self) -> None:
        if self.verbose:
            print("[INFO] 降噪处理完成")
        if self.file_handle:
            self.file_handle.close()
        self.complete_event.set()
    
    def on_error(self, message) -> None:
        print(f"[ERROR] 处理出错: {message}")
        self.error_message = message
        if self.file_handle:
            self.file_handle.close()
        self.complete_event.set()
    
    def on_close(self) -> None:
        if self.verbose:
            print("[INFO] WebSocket 连接已关闭")
    
    def on_event(self, result: DenoiseResult) -> None:
        if result.audio_frame is not None:
            if self.file_handle:
                self.file_handle.write(result.audio_frame)
            self.audio_count += 1
            self.total_bytes += len(result.audio_frame)
            if self.verbose and self.audio_count % 10 == 0:
                print(f"  已接收音频帧 #{self.audio_count}: {self.total_bytes} 字节")
        
        if result.output is not None:
            self.output_info = result.output
            if self.verbose:
                print(f"  [元数据] {result.output}")
        
        if result.usage is not None:
            self.usage_info = result.usage


def get_audio_format(file_path: str) -> str:
    """根据文件扩展名推断音频格式"""
    ext = Path(file_path).suffix.lower()
    format_map = {
        '.wav': 'wav',
        '.mp3': 'mp3',
        '.pcm': 'pcm',
        '.aac': 'aac',
        '.opus': 'opus',
        '.amr': 'amr',
    }
    return format_map.get(ext, 'wav')


def denoise_audio(
    input_path: str,
    output_path: str = None,
    audio_format: str = None,
    sample_rate: int = 16000,
    enable_denoise: bool = True,
    verbose: bool = True,
    chunk_size: int = 3200,
    chunk_delay: float = 0.1
) -> dict:
    """
    对音频文件进行降噪处理
    
    Args:
        input_path: 输入音频文件路径
        output_path: 输出音频文件路径（默认为 input_denoised.wav）
        audio_format: 音频格式（自动检测或手动指定）
        sample_rate: 采样率
        enable_denoise: 是否启用降噪
        verbose: 是否显示详细日志
        chunk_size: 分块大小（字节）
        chunk_delay: 分块发送间隔（秒）
    
    Returns:
        处理结果字典
    """
    
    # 检查输入文件
    if not os.path.exists(input_path):
        return {"success": False, "error": f"输入文件不存在: {input_path}"}
    
    # 自动推断输出路径
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = str(input_path_obj.parent / f"{input_path_obj.stem}_denoised.wav")
    
    # 自动推断音频格式
    if audio_format is None:
        audio_format = get_audio_format(input_path)
    
    if verbose:
        print(f"[INFO] 输入文件: {input_path}")
        print(f"[INFO] 输出文件: {output_path}")
        print(f"[INFO] 音频格式: {audio_format}")
        print(f"[INFO] 采样率: {sample_rate}Hz")
        print(f"[INFO] 降噪启用: {enable_denoise}")
        print("[INFO] 开始降噪处理...")
    
    # 配置参数
    param = DenoiseParam(
        model="fun-audio-denoising",
        format=audio_format,
        sample_rate_in=sample_rate,
        enable_denoise=enable_denoise,
    )
    
    # 创建回调
    callback = DenoiseCallback(output_path, verbose=verbose)
    
    # 创建降噪处理器
    denoise = Denoise(param=param, callback=callback)
    
    start_time = time.time()
    
    try:
        # 启动任务
        denoise.start_task()
        
        # 读取并发送音频文件
        with open(input_path, "rb") as f:
            chunk_num = 0
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                denoise.send_audio_frame(data)
                chunk_num += 1
                if chunk_delay > 0:
                    time.sleep(chunk_delay)
        
        if verbose:
            print(f"[INFO] 已发送 {chunk_num} 个音频块")
        
        # 停止任务并等待完成
        denoise.sync_stop_task(complete_timeout_millis=120000)
        
        elapsed_time = time.time() - start_time
        
        # 检查结果
        if callback.error_message:
            return {
                "success": False,
                "error": callback.error_message,
                "output_path": output_path,
                "elapsed_time": elapsed_time
            }
        
        # 验证输出文件
        if not os.path.exists(output_path):
            return {
                "success": False,
                "error": "输出文件未生成",
                "elapsed_time": elapsed_time
            }
        
        output_size = os.path.getsize(output_path)
        input_size = os.path.getsize(input_path)
        
        result = {
            "success": True,
            "input_path": input_path,
            "output_path": output_path,
            "input_size": input_size,
            "output_size": output_size,
            "audio_frames": callback.audio_count,
            "elapsed_time": elapsed_time,
            "output_info": callback.output_info,
            "usage_info": callback.usage_info
        }
        
        if verbose:
            print(f"\n[INFO] 处理成功!")
            print(f"  输入大小: {input_size} 字节")
            print(f"  输出大小: {output_size} 字节")
            print(f"  音频帧数: {callback.audio_count}")
            print(f"  处理耗时: {elapsed_time:.2f} 秒")
            if callback.output_info:
                print(f"  输出采样率: {callback.output_info.get('sample_rate_out', 'N/A')}Hz")
                print(f"  音频质量: {callback.output_info.get('voice_quality', 'N/A')}")
                print(f"  有效语音: {callback.output_info.get('valid_speech_ms', 'N/A')}ms")
            if callback.usage_info:
                print(f"  计费时长: {callback.usage_info.get('duration', 'N/A')} 秒")
        
        return result
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        return {
            "success": False,
            "error": str(e),
            "output_path": output_path,
            "elapsed_time": elapsed_time
        }
    finally:
        denoise.close()


def main():
    parser = argparse.ArgumentParser(
        description="FunAudioDenoise - 智能音频降噪工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python denoise_cli.py input.wav                    # 基础使用
  python denoise_cli.py input.mp3 output.wav         # 指定输出文件
  python denoise_cli.py input.wav --format wav --sample-rate 16000
  python denoise_cli.py input.wav --no-denoise       # 仅转换格式
        """
    )
    
    parser.add_argument("input", help="输入音频文件路径")
    parser.add_argument("output", nargs="?", help="输出音频文件路径（可选）")
    parser.add_argument("--format", help="音频格式 (wav, mp3, pcm, aac, opus, amr)")
    parser.add_argument("--sample-rate", type=int, default=16000, help="采样率 (默认: 16000)")
    parser.add_argument("--no-denoise", action="store_true", help="禁用降噪（仅转换格式）")
    parser.add_argument("--chunk-size", type=int, default=3200, help="分块大小（默认: 3200）")
    parser.add_argument("--chunk-delay", type=float, default=0.1, help="分块发送间隔（默认: 0.1秒）")
    parser.add_argument("-q", "--quiet", action="store_true", help="静默模式")
    
    args = parser.parse_args()
    
    result = denoise_audio(
        input_path=args.input,
        output_path=args.output,
        audio_format=args.format,
        sample_rate=args.sample_rate,
        enable_denoise=not args.no_denoise,
        verbose=not args.quiet,
        chunk_size=args.chunk_size,
        chunk_delay=args.chunk_delay
    )
    
    if not result["success"]:
        print(f"[FAILED] {result['error']}")
        sys.exit(1)
    else:
        print(f"[SUCCESS] 降噪完成: {result['output_path']}")
        sys.exit(0)


if __name__ == "__main__":
    main()
