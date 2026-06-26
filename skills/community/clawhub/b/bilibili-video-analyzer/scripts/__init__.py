"""
B站学术视频分析器

专业的学术视频内容分析工具
"""

__version__ = "1.0.0"
__author__ = "KC"

from .srt_parser import SubtitleSegment, parse_srt_file, parse_timestamp, format_timestamp
from .screenshot_tool import capture_screenshot, batch_capture, check_ffmpeg
from .llm_analyzer import build_analysis_prompt, interactive_analyze, parse_llm_response
from .report_generator import generate_markdown

__all__ = [
    'SubtitleSegment',
    'parse_srt_file',
    'parse_timestamp',
    'format_timestamp',
    'capture_screenshot',
    'batch_capture',
    'check_ffmpeg',
    'build_analysis_prompt',
    'interactive_analyze',
    'parse_llm_response',
    'generate_markdown',
]
