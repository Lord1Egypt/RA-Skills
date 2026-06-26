"""
视频信息提取器
只负责使用 ffprobe 提取视频基本信息
"""

import json
import subprocess
from typing import Dict


class VideoInfo:
    """视频信息数据类"""

    def __init__(self, raw_data: Dict):
        """
        初始化视频信息

        Args:
            raw_data: 原始视频数据字典
        """
        self.file_path = raw_data.get("file_path", "")
        self.file_size_mb = raw_data.get("file_size_mb", 0)
        self.duration = raw_data.get("duration", 0)
        self.format_name = raw_data.get("format_name", "")
        self.video = raw_data.get("video")
        self.audio = raw_data.get("audio")
        self.subtitles = raw_data.get("subtitles", [])
        self.raw_info = raw_data.get("raw_info", {})

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "file_path": self.file_path,
            "file_size_mb": self.file_size_mb,
            "duration": self.duration,
            "format_name": self.format_name,
            "video": self.video,
            "audio": self.audio,
            "subtitles": self.subtitles,
            "raw_info": self.raw_info,
        }


class VideoAnalyzer:
    """视频信息提取器"""

    def __init__(self):
        """初始化视频分析器"""

    def analyze(self, video_path: str) -> VideoInfo:
        """
        分析视频文件

        Args:
            video_path: 视频文件路径

        Returns:
            VideoInfo: 视频信息对象
        """
        # 使用 ffprobe 获取视频信息
        probe_cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            video_path,
        ]

        try:
            result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)

            # 提取视频流信息
            video_stream = None
            audio_stream = None
            subtitle_streams = []

            for stream in info.get("streams", []):
                if stream["codec_type"] == "video" and video_stream is None:
                    video_stream = stream
                elif stream["codec_type"] == "audio" and audio_stream is None:
                    audio_stream = stream
                elif stream["codec_type"] == "subtitle":
                    subtitle_streams.append(stream)

            # 提取格式信息
            format_info = info.get("format", {})

            # 构建返回结果
            analysis = {
                "file_path": video_path,
                "file_size_mb": float(format_info.get("size", 0)) / (1024 * 1024),
                "duration": float(format_info.get("duration", 0)),
                "format_name": format_info.get("format_name", ""),
                "video": self._parse_video_stream(video_stream) if video_stream else None,
                "audio": self._parse_audio_stream(audio_stream) if audio_stream else None,
                "subtitles": [self._parse_subtitle_stream(s) for s in subtitle_streams],
                "raw_info": info,
            }

            return VideoInfo(analysis)

        except subprocess.CalledProcessError as e:
            raise Exception(f"FFprobe 分析失败: {e.stderr}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析 ffprobe 输出失败: {e}")

    def _parse_video_stream(self, stream: Dict) -> Dict:
        """解析视频流信息"""
        return {
            "codec": stream.get("codec_name", ""),
            "codec_long_name": stream.get("codec_long_name", ""),
            "width": int(stream.get("width", 0)),
            "height": int(stream.get("height", 0)),
            "fps": self._parse_fps(stream.get("r_frame_rate", "0/1")),
            "bitrate": int(stream.get("bit_rate", 0)) if stream.get("bit_rate") else None,
            "profile": stream.get("profile", ""),
            "level": stream.get("level", ""),
            "pixel_format": stream.get("pix_fmt", ""),
            "bit_depth": int(stream.get("bits_per_raw_sample", 8)),
        }

    def _parse_audio_stream(self, stream: Dict) -> Dict:
        """解析音频流信息"""
        return {
            "codec": stream.get("codec_name", ""),
            "codec_long_name": stream.get("codec_long_name", ""),
            "sample_rate": int(stream.get("sample_rate", 0)),
            "channels": int(stream.get("channels", 0)),
            "bitrate": int(stream.get("bit_rate", 0)) if stream.get("bit_rate") else None,
        }

    def _parse_subtitle_stream(self, stream: Dict) -> Dict:
        """解析字幕流信息"""
        return {
            "index": stream.get("index", 0),
            "codec": stream.get("codec_name", ""),
            "language": stream.get("tags", {}).get("language", "unknown"),
            "title": stream.get("tags", {}).get("title", ""),
        }

    def _parse_fps(self, fps_str: str) -> float:
        """解析帧率"""
        try:
            num, den = fps_str.split("/")
            return float(num) / float(den)
        except (ValueError, ZeroDivisionError):
            return 0.0
