#!/usr/bin/env python3
"""
音频/视频分析器
提取声音特征、语言习惯等
"""

import argparse
import json
import sys
from pathlib import Path


def analyze_audio_simple(audio_path):
    """简单分析音频文件（无需复杂依赖）"""
    result = {
        'filename': audio_path.name,
        'size_bytes': audio_path.stat().st_size,
        'format': audio_path.suffix.lower()
    }
    
    # 尝试获取音频元数据（如果有 mutagen）
    try:
        from mutagen import File
        audio = File(audio_path)
        if audio:
            result['duration'] = getattr(audio.info, 'length', None)
            result['bitrate'] = getattr(audio.info, 'bitrate', None)
            result['sample_rate'] = getattr(audio.info, 'sample_rate', None)
    except ImportError:
        pass
    
    return result


def analyze_video_simple(video_path):
    """简单分析视频文件（无需复杂依赖）"""
    result = {
        'filename': video_path.name,
        'size_bytes': video_path.stat().st_size,
        'format': video_path.suffix.lower()
    }
    
    # 尝试获取视频元数据（如果有 ffmpeg-python）
    try:
        import ffmpeg
        probe = ffmpeg.probe(str(video_path))
        
        # 视频流信息
        video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
        if video_stream:
            result['width'] = video_stream.get('width')
            result['height'] = video_stream.get('height')
            result['duration'] = float(video_stream.get('duration', 0))
            result['fps'] = eval(video_stream.get('r_frame_rate', '0/1'))
        
        # 音频流信息
        audio_stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
        if audio_stream:
            result['has_audio'] = True
            result['audio_codec'] = audio_stream.get('codec_name')
        
    except ImportError:
        result['note'] = 'ffmpeg-python not installed'
    except Exception as e:
        result['error'] = str(e)
    
    return result


def extract_audio_from_video(video_path, output_audio_path):
    """从视频中提取音频"""
    try:
        import ffmpeg
        (
            ffmpeg
            .input(str(video_path))
            .output(str(output_audio_path), acodec='mp3', vn=None)
            .run(quiet=True, overwrite_output=True)
        )
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"Error extracting audio: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='分析音频/视频文件')
    parser.add_argument('--dir', required=True, help='媒体文件目录路径')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--extract-audio', action='store_true', help='从视频中提取音频')
    
    args = parser.parse_args()
    
    media_dir = Path(args.dir)
    if not media_dir.exists():
        print(f"Error: Directory not found: {media_dir}", file=sys.stderr)
        sys.exit(1)
    
    # 支持的格式
    audio_extensions = {'.mp3', '.wav', '.m4a', '.aac', '.ogg', '.wma'}
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'}
    
    # 分析所有媒体文件
    audio_files = []
    video_files = []
    
    # 分析音频
    for ext in audio_extensions:
        for audio_path in media_dir.rglob(f'*{ext}'):
            result = analyze_audio_simple(audio_path)
            audio_files.append(result)
    
    # 分析视频
    for ext in video_extensions:
        for video_path in media_dir.rglob(f'*{ext}'):
            result = analyze_video_simple(video_path)
            video_files.append(result)
            
            # 可选：提取音频
            if args.extract_audio:
                output_audio = video_path.with_suffix('.mp3')
                if extract_audio_from_video(video_path, output_audio):
                    result['extracted_audio'] = str(output_audio)
    
    # 输出
    output = {
        'directory': str(media_dir),
        'audio_count': len(audio_files),
        'video_count': len(video_files),
        'audio_files': audio_files,
        'video_files': video_files
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"分析完成:")
    print(f"  音频文件: {len(audio_files)}")
    print(f"  视频文件: {len(video_files)}")
    print(f"输出文件: {args.output}")
    
    # 提示安装可选依赖
    if not any('duration' in a for a in audio_files):
        print("\n提示: 如需更详细的音频分析，请安装:")
        print("  pip install mutagen")
    
    if not any('width' in v for v in video_files):
        print("\n提示: 如需视频分析，请安装:")
        print("  pip install ffmpeg-python")
        print("  并安装 ffmpeg 工具")


if __name__ == '__main__':
    main()
