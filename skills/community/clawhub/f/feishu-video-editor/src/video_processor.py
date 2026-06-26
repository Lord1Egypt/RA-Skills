#!/usr/bin/env python3
"""
AI 视频剪辑核心处理模块
支持：静音删除、视频裁剪、字幕生成、音频提取
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from datetime import timedelta

# 音频分析
import librosa
import numpy as np
from pydub import AudioSegment

# 字幕生成
import pysrt


class VideoEditor:
    """视频编辑器"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.whisper_model = self.config.get('whisper_model', 'base')
        self.silent_threshold = self.config.get('silent_threshold', -50)
        self.min_silent_duration = self.config.get('min_silent_duration', 1.0)
        self.ffmpeg_preset = self.config.get('ffmpeg_preset', 'medium')
        
    def trim_silence(self, video_path: str, output_path: str = None) -> dict:
        """
        删除视频中的静音片段
        
        Args:
            video_path: 输入视频路径
            output_path: 输出视频路径
            
        Returns:
            处理结果字典
        """
        if output_path is None:
            output_path = self._get_output_path(video_path, '_trimmed')
        
        print(f"🎬 开始处理视频：{video_path}")
        
        # 步骤 1: 提取音频
        audio_path = self._extract_audio(video_path)
        print(f"📊 音频已提取：{audio_path}")
        
        # 步骤 2: 检测静音片段
        silent_ranges = self._detect_silence(audio_path)
        print(f"📊 检测到 {len(silent_ranges)} 段静音")
        
        # 步骤 3: 计算保留的片段
        audio_duration = len(AudioSegment.from_file(audio_path)) / 1000.0
        keep_ranges = self._calculate_keep_ranges(silent_ranges, audio_duration)
        print(f"✂️ 将保留 {len(keep_ranges)} 个片段")
        
        # 步骤 4: 使用 FFmpeg 剪辑
        if len(keep_ranges) == 1:
            # 单一片段，直接裁剪
            self._crop_video(video_path, output_path, keep_ranges[0])
        else:
            # 多个片段，需要合并
            self._concat_video_clips(video_path, output_path, keep_ranges)
        
        # 清理临时文件
        os.remove(audio_path)
        
        # 获取输出信息
        output_info = self._get_video_info(output_path)
        
        return {
            'success': True,
            'output_path': output_path,
            'original_duration': audio_duration,
            'output_duration': output_info.get('duration', 0),
            'silent_parts_removed': len(silent_ranges),
            'message': f"✅ 剪辑完成！删除了 {len(silent_ranges)} 段静音，总时长从 {audio_duration:.1f}s 缩短到 {output_info.get('duration', 0):.1f}s"
        }
    
    def crop_video(self, video_path: str, start_time: str, end_time: str, 
                   output_path: str = None) -> dict:
        """
        按时间戳裁剪视频
        
        Args:
            video_path: 输入视频路径
            start_time: 开始时间 (HH:MM:SS 或 SS)
            end_time: 结束时间
            output_path: 输出路径
            
        Returns:
            处理结果
        """
        if output_path is None:
            output_path = self._get_output_path(video_path, '_cropped')
        
        print(f"✂️ 裁剪视频：{start_time} - {end_time}")
        
        # 构建 FFmpeg 命令
        cmd = [
            'ffmpeg', '-i', video_path,
            '-ss', start_time,
            '-to', end_time,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', self.ffmpeg_preset,
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return {
                'success': False,
                'error': f"FFmpeg 错误：{result.stderr}"
            }
        
        output_info = self._get_video_info(output_path)
        
        return {
            'success': True,
            'output_path': output_path,
            'duration': output_info.get('duration', 0),
            'message': f"✅ 裁剪完成！时长：{output_info.get('duration', 0):.1f}s"
        }
    
    def generate_subtitles(self, video_path: str, output_path: str = None,
                          language: str = 'zh') -> dict:
        """
        生成视频字幕（使用 Whisper）
        
        Args:
            video_path: 输入视频路径
            output_path: 输出字幕路径
            language: 语言代码
            
        Returns:
            处理结果
        """
        if output_path is None:
            output_path = self._get_output_path(video_path, '_subtitles', '.srt')
        
        print(f"🎤 开始语音识别：{video_path}")
        
        try:
            import whisper
        except ImportError:
            return {
                'success': False,
                'error': 'Whisper 未安装，请运行：pip install openai-whisper'
            }
        
        # 加载模型
        print(f"📦 加载 Whisper 模型：{self.whisper_model}")
        model = whisper.load_model(self.whisper_model)
        
        # 转录
        print("🎙️ 转录中...")
        result = model.transcribe(video_path, language=language if language != 'zh' else 'chinese')
        
        # 生成 SRT 字幕
        subs = pysrt.SubRipFile()
        
        for i, segment in enumerate(result['segments']):
            start = self._seconds_to_srt_time(segment['start'])
            end = self._seconds_to_srt_time(segment['end'])
            text = segment['text'].strip()
            
            sub = pysrt.SubRipItem(
                index=i + 1,
                start=start,
                end=end,
                text=text
            )
            subs.append(sub)
        
        # 保存字幕
        subs.save(output_path, encoding='utf-8')
        print(f"✅ 字幕已保存：{output_path}")
        
        return {
            'success': True,
            'output_path': output_path,
            'segments_count': len(result['segments']),
            'message': f"✅ 字幕生成完成！共 {len(result['segments'])} 条字幕"
        }
    
    def extract_audio(self, video_path: str, output_path: str = None) -> dict:
        """
        提取视频音频
        
        Args:
            video_path: 输入视频路径
            output_path: 输出音频路径
            
        Returns:
            处理结果
        """
        if output_path is None:
            output_path = self._get_output_path(video_path, '_audio', '.mp3')
        
        print(f"🎵 提取音频：{video_path}")
        
        cmd = [
            'ffmpeg', '-i', video_path,
            '-q:a', '0', '-map', 'a',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return {
                'success': False,
                'error': f"FFmpeg 错误：{result.stderr}"
            }
        
        return {
            'success': True,
            'output_path': output_path,
            'message': f"✅ 音频提取完成：{output_path}"
        }
    
    # ========== 内部方法 ==========
    
    def _extract_audio(self, video_path: str) -> str:
        """提取音频到临时文件"""
        audio_path = tempfile.mktemp(suffix='.wav')
        
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', '16000', '-ac', '1',
            '-y', audio_path
        ]
        
        subprocess.run(cmd, capture_output=True)
        return audio_path
    
    def _detect_silence(self, audio_path: str) -> list:
        """
        检测音频中的静音片段
        
        Returns:
            [(start1, end1), (start2, end2), ...] 秒
        """
        # 加载音频
        y, sr = librosa.load(audio_path, sr=16000)
        
        # 计算音频能量 (RMS)
        rms = librosa.feature.rms(y=y)[0]
        
        # 转换为 dB
        rms_db = 20 * np.log10(rms + 1e-10)
        
        # 找出静音片段
        silent_ranges = []
        in_silence = False
        silence_start = 0
        
        for i, db in enumerate(rms_db):
            if db < self.silent_threshold:
                if not in_silence:
                    in_silence = True
                    silence_start = i / sr  # 转换为秒
            else:
                if in_silence:
                    in_silence = False
                    silence_end = i / sr
                    duration = silence_end - silence_start
                    
                    # 只记录超过最小时长的静音
                    if duration >= self.min_silent_duration:
                        silent_ranges.append((silence_start, silence_end))
        
        # 处理结尾的静音
        if in_silence:
            silence_end = len(y) / sr
            duration = silence_end - silence_start
            if duration >= self.min_silent_duration:
                silent_ranges.append((silence_start, silence_end))
        
        return silent_ranges
    
    def _calculate_keep_ranges(self, silent_ranges: list, total_duration: float) -> list:
        """
        根据静音片段计算需要保留的片段
        
        Returns:
            [(start1, end1), (start2, end2), ...]
        """
        if not silent_ranges:
            return [(0, total_duration)]
        
        keep_ranges = []
        current_start = 0
        
        for silence_start, silence_end in silent_ranges:
            if silence_start > current_start:
                keep_ranges.append((current_start, silence_start))
            current_start = silence_end
        
        # 最后一段
        if current_start < total_duration:
            keep_ranges.append((current_start, total_duration))
        
        return keep_ranges
    
    def _crop_video(self, video_path: str, output_path: str, 
                    time_range: tuple) -> None:
        """裁剪单个视频片段"""
        start, end = time_range
        
        cmd = [
            'ffmpeg', '-i', video_path,
            '-ss', str(start),
            '-to', str(end),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', self.ffmpeg_preset,
            '-y', output_path
        ]
        
        subprocess.run(cmd, capture_output=True)
    
    def _concat_video_clips(self, video_path: str, output_path: str,
                           ranges: list) -> None:
        """合并多个视频片段"""
        # 先裁剪出所有片段
        temp_files = []
        for i, (start, end) in enumerate(ranges):
            temp_path = tempfile.mktemp(suffix=f'_{i}.mp4')
            temp_files.append(temp_path)
            
            cmd = [
                'ffmpeg', '-i', video_path,
                '-ss', str(start),
                '-to', str(end),
                '-c', 'copy',  # 快速复制，不重新编码
                '-y', temp_path
            ]
            subprocess.run(cmd, capture_output=True)
        
        # 创建文件列表
        list_file = tempfile.mktemp(suffix='.txt')
        with open(list_file, 'w') as f:
            for temp_path in temp_files:
                f.write(f"file '{temp_path}'\n")
        
        # 合并
        cmd = [
            'ffmpeg', '-f', 'concat', '-safe', '0',
            '-i', list_file,
            '-c', 'copy',
            '-y', output_path
        ]
        subprocess.run(cmd, capture_output=True)
        
        # 清理临时文件
        os.remove(list_file)
        for temp_path in temp_files:
            os.remove(temp_path)
    
    def _get_video_info(self, video_path: str) -> dict:
        """获取视频信息"""
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip())
            return {'duration': duration}
        except:
            return {'duration': 0}
    
    def _get_output_path(self, input_path: str, suffix: str = '', 
                        extension: str = None) -> str:
        """生成输出文件路径"""
        path = Path(input_path)
        if extension is None:
            extension = path.suffix
        output_name = f"{path.stem}{suffix}{extension}"
        output_dir = self.config.get('output_dir', str(path.parent))
        return str(Path(output_dir) / output_name)
    
    def _seconds_to_srt_time(self, seconds: float) -> pysrt.SubRipTime:
        """将秒数转换为 SRT 时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return pysrt.SubRipTime(hours, minutes, secs, millis)


# ========== CLI 入口 ==========

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 视频剪辑工具')
    parser.add_argument('command', choices=['trim_silence', 'crop', 'subtitle', 'extract_audio'],
                       help='命令类型')
    parser.add_argument('input', help='输入视频文件')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--start', help='开始时间 (crop 命令)')
    parser.add_argument('--end', help='结束时间 (crop 命令)')
    parser.add_argument('--config', help='配置文件路径')
    
    args = parser.parse_args()
    
    # 加载配置
    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config) as f:
            config = json.load(f)
    
    editor = VideoEditor(config)
    
    # 执行命令
    if args.command == 'trim_silence':
        result = editor.trim_silence(args.input, args.output)
    elif args.command == 'crop':
        if not args.start or not args.end:
            print("❌ crop 命令需要 --start 和 --end 参数")
            sys.exit(1)
        result = editor.crop_video(args.input, args.start, args.end, args.output)
    elif args.command == 'subtitle':
        result = editor.generate_subtitles(args.input, args.output)
    elif args.command == 'extract_audio':
        result = editor.extract_audio(args.input, args.output)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if not result['success']:
        sys.exit(1)
