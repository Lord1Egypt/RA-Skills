#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频合并工具
使用ffmpeg合并多个音频文件，添加静音间隔
替代pydub方案，解决Python 3.13 audioop缺失问题
"""

import os
import sys
import tempfile
import subprocess
import json
from pathlib import Path
from typing import List, Optional, Union, Tuple

class AudioMerger:
    """音频合并器（基于ffmpeg）"""
    
    def __init__(self):
        # 检查ffmpeg是否可用
        self.ffmpeg_path = self._find_ffmpeg()
        if not self.ffmpeg_path:
            raise RuntimeError("ffmpeg 未安装，请先安装: sudo apt install ffmpeg")
    
    def _find_ffmpeg(self) -> Optional[str]:
        """查找ffmpeg可执行文件"""
        import shutil
        ffmpeg_path = shutil.which("ffmpeg")
        return ffmpeg_path
    
    def _get_audio_duration(self, file_path: Union[str, Path]) -> float:
        """获取音频文件时长（秒）"""
        import json
        cmd = [
            self.ffmpeg_path, '-i', str(file_path),
            '-f', 'ffmetadata', '-'
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            # 从stderr中解析时长
            import re
            lines = result.stderr.split('\n')
            for line in lines:
                if 'Duration' in line:
                    match = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', line)
                    if match:
                        h, m, s = match.groups()
                        total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
                        return total_seconds
        except Exception as e:
            print(f"Warning: Failed to get audio duration: {e}", file=sys.stderr)
        # 如果无法获取，返回0
        return 0.0
    
    def merge_audio_files(self, file_paths: List[Union[str, Path]], 
                         pause_ms: int = 300,
                         output_format: str = "mp3",
                         bitrate: str = "192k") -> bytes:
        """
        合并多个音频文件
        
        Args:
            file_paths: 音频文件路径列表
            pause_ms: 文件间的静音间隔（毫秒）
            output_format: 输出格式（mp3, wav等）
            bitrate: MP3比特率（如 "192k", "128k"）
            
        Returns:
            合并后的音频二进制数据
        """
        if not file_paths:
            raise ValueError("没有要合并的音频文件")
        
        print(f"合并 {len(file_paths)} 个音频文件，间隔 {pause_ms}ms...")
        
        # 检查文件是否存在
        for file_path in file_paths:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"音频文件不存在: {file_path}")
        
        # 创建临时目录用于处理
        import tempfile
        temp_dir = tempfile.mkdtemp(prefix="audio_merge_")
        
        try:
            # 方法1: 使用concat协议（需要相同编码格式）
            # 先尝试使用concat协议，如果不兼容则使用filter_complex
            concat_list_file = Path(temp_dir) / "concat_list.txt"
            with open(concat_list_file, 'w', encoding='utf-8') as f:
                for file_path in file_paths:
                    f.write(f"file '{Path(file_path).absolute()}'\n")
            
            # 输出临时文件
            temp_output = Path(temp_dir) / f"merged.{output_format}"
            
            # 构建ffmpeg命令
            # 如果pause_ms > 0，需要在文件间插入静音
            # 使用filter_complex连接并添加静音
            if pause_ms > 0:
                # 构建复杂的filter_complex
                filter_parts = []
                inputs = []
                for i, file_path in enumerate(file_paths):
                    inputs.extend(['-i', str(file_path)])
                    # 每个输入流命名为a{i}
                    filter_parts.append(f'[{i}:a]')
                
                # 连接所有流，并在每个流之间插入静音
                concat_inputs = []
                for i in range(len(file_paths)):
                    concat_inputs.append(f'[{i}:a]')
                    if i < len(file_paths) - 1:
                        # 添加静音流
                        silence_duration = pause_ms / 1000.0  # 秒
                        filter_parts.append(f'aevalsrc=0:d={silence_duration}[silence{i}]')
                        concat_inputs.append(f'[silence{i}]')
                
                # 连接所有流
                concat_str = ''.join(concat_inputs)
                filter_complex = f"{''.join(filter_parts)}concat=n={len(concat_inputs)}:v=0:a=1[out]"
                
                cmd = [self.ffmpeg_path] + inputs + [
                    '-filter_complex', filter_complex,
                    '-map', '[out]',
                    '-c:a', 'libmp3lame' if output_format == 'mp3' else 'pcm_s16le',
                    '-b:a', bitrate if output_format == 'mp3' else None,
                    '-y', str(temp_output)
                ]
                cmd = [c for c in cmd if c is not None]
            else:
                # 无静音间隔，直接concat
                cmd = [
                    self.ffmpeg_path, '-f', 'concat', '-safe', '0',
                    '-i', str(concat_list_file),
                    '-c', 'copy',
                    '-y', str(temp_output)
                ]
            
            # 执行ffmpeg
            print(f"执行ffmpeg命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                # 如果失败，尝试使用filter_complex的备用方案
                print(f"concat协议失败，尝试备用方案: {result.stderr}")
                # 备用方案：逐个解码并连接
                self._merge_with_filter_complex(file_paths, temp_output, pause_ms, output_format, bitrate)
            
            # 读取合并后的音频数据
            if not temp_output.exists():
                raise RuntimeError("合并失败，输出文件未生成")
            
            with open(temp_output, 'rb') as f:
                audio_data = f.read()
            
            file_size = len(audio_data)
            print(f"合并完成，输出大小: {file_size} bytes")
            
            return audio_data
            
        finally:
            # 清理临时目录
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Warning: Failed to cleanup temp directory: {e}", file=sys.stderr)
    
    def _merge_with_filter_complex(self, file_paths, output_path, pause_ms, output_format, bitrate):
        """使用filter_complex合并音频（更可靠的方法）"""
        inputs = []
        for i, file_path in enumerate(file_paths):
            inputs.extend(['-i', str(file_path)])
        
        # 构建filter_complex
        filter_parts = []
        for i in range(len(file_paths)):
            filter_parts.append(f'[{i}:a]')
        
        # 如果需要静音间隔
        if pause_ms > 0:
            silence_streams = []
            for i in range(len(file_paths) - 1):
                silence_duration = pause_ms / 1000.0
                filter_parts.append(f'aevalsrc=0:d={silence_duration}[silence{i}]')
                silence_streams.append(f'[silence{i}]')
            
            # 交错排列：音频1，静音1，音频2，静音2...
            concat_inputs = []
            for i in range(len(file_paths)):
                concat_inputs.append(f'[{i}:a]')
                if i < len(file_paths) - 1:
                    concat_inputs.append(f'[silence{i}]')
        else:
            concat_inputs = [f'[{i}:a]' for i in range(len(file_paths))]
        
        filter_complex = f"{''.join(filter_parts)}concat=n={len(concat_inputs)}:v=0:a=1[out]"
        
        # 构建命令
        cmd = [self.ffmpeg_path] + inputs + [
            '-filter_complex', filter_complex,
            '-map', '[out]'
        ]
        
        # 设置编码参数
        if output_format == 'mp3':
            cmd.extend(['-c:a', 'libmp3lame', '-b:a', bitrate])
        elif output_format == 'wav':
            cmd.extend(['-c:a', 'pcm_s16le'])
        else:
            cmd.extend(['-c:a', 'copy'])
        
        cmd.extend(['-y', str(output_path)])
        
        print(f"备用合并命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg合并失败: {result.stderr}")
    
    def merge_and_save(self, file_paths: List[Union[str, Path]], 
                      output_path: Union[str, Path],
                      pause_ms: int = 300,
                      output_format: str = None,
                      bitrate: str = "192k"):
        """
        合并音频文件并保存到磁盘
        
        Args:
            file_paths: 音频文件路径列表
            output_path: 输出文件路径
            pause_ms: 文件间的静音间隔
            output_format: 输出格式（从文件扩展名推断）
            bitrate: MP3比特率
        """
        # 从输出路径推断格式
        if output_format is None:
            output_path_obj = Path(output_path)
            output_format = output_path_obj.suffix.lstrip(".").lower()
            if not output_format:
                output_format = "mp3"
        
        # 合并音频
        audio_data = self.merge_audio_files(file_paths, pause_ms, output_format, bitrate)
        
        # 保存文件
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        file_size = len(audio_data)
        print(f"合并完成: {output_path} ({file_size} bytes)")
    
    def batch_merge_directories(self, input_dir: Union[str, Path],
                               output_dir: Union[str, Path],
                               file_pattern: str = "*.mp3",
                               pause_ms: int = 300,
                               output_format: str = "mp3"):
        """
        批量合并目录中的音频文件
        
        Args:
            input_dir: 输入目录（包含多个子目录，每个子目录包含要合并的文件）
            output_dir: 输出目录
            file_pattern: 文件匹配模式
            pause_ms: 间隔毫秒数
            output_format: 输出格式
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 查找所有子目录
        subdirs = [d for d in input_dir.iterdir() if d.is_dir()]
        
        if not subdirs:
            print(f"在 {input_dir} 中没有找到子目录")
            return
        
        print(f"批量合并: {len(subdirs)} 个子目录")
        
        for subdir in subdirs:
            # 查找音频文件
            audio_files = list(subdir.glob(file_pattern))
            audio_files.sort()  # 按文件名排序
            
            if not audio_files:
                print(f"  跳过 {subdir.name}: 无 {file_pattern} 文件")
                continue
            
            # 输出文件路径
            output_file = output_dir / f"{subdir.name}_merged.{output_format}"
            
            print(f"  处理 {subdir.name}: {len(audio_files)} 个文件 -> {output_file.name}")
            
            try:
                self.merge_and_save(audio_files, output_file, pause_ms, output_format)
                print(f"  成功: {output_file.name}")
            except Exception as e:
                print(f"  失败: {e}")

def check_dependencies() -> bool:
    """检查依赖是否安装（仅检查ffmpeg）"""
    import shutil
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        print("错误: ffmpeg 未安装")
        print("Ubuntu/Debian: sudo apt install ffmpeg")
        print("macOS: brew install ffmpeg")
        print("Windows: 从 https://ffmpeg.org/download.html 下载")
        return False
    
    # 检查ffmpeg版本是否支持所需功能
    try:
        import subprocess
        result = subprocess.run([ffmpeg_path, '-version'], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"ffmpeg版本: {version_line}")
            return True
        else:
            print("Warning: ffmpeg version check failed", file=sys.stderr)
            return True  # 假设可用
    except Exception as e:
        print(f"Warning: Cannot check ffmpeg version, assuming available: {e}", file=sys.stderr)
        return True

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="音频合并工具")
    parser.add_argument("files", nargs="+", help="要合并的音频文件")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--pause", "-p", type=int, default=300, 
                       help="文件间的静音间隔（毫秒，默认: 300）")
    parser.add_argument("--format", "-f", help="输出格式（从扩展名推断）")
    parser.add_argument("--bitrate", "-b", default="192k", 
                       help="MP3比特率（默认: 192k）")
    parser.add_argument("--batch-dir", "-d", 
                       help="批量处理模式：合并输入目录下的所有子目录")
    parser.add_argument("--pattern", default="*.mp3",
                       help="批量模式的文件匹配模式（默认: *.mp3）")
    
    args = parser.parse_args()
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    try:
        merger = AudioMerger()
    except RuntimeError as e:
        print(f"初始化失败: {e}")
        sys.exit(1)
    
    # 批量模式
    if args.batch_dir:
        output_dir = args.output
        merger.batch_merge_directories(
            args.batch_dir, output_dir, 
            args.pattern, args.pause, args.format
        )
        return
    
    # 单次合并模式
    file_paths = args.files
    
    # 检查文件是否存在
    for file_path in file_paths:
        if not Path(file_path).exists():
            print(f"错误: 文件不存在 {file_path}")
            sys.exit(1)
    
    print(f"准备合并 {len(file_paths)} 个文件:")
    for i, file_path in enumerate(file_paths, 1):
        print(f"  {i}. {file_path}")
    
    try:
        merger.merge_and_save(
            file_paths, args.output,
            pause_ms=args.pause,
            output_format=args.format,
            bitrate=args.bitrate
        )
    except Exception as e:
        print(f"合并失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()