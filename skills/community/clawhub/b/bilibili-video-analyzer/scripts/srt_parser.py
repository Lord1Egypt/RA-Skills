"""
SRT 字幕文件解析器

功能:
- 解析 SRT 格式字幕文件
- 提取时间戳和文本内容
- 时间戳格式转换(HH:MM:SS,mmm <-> 秒数)
"""

import re
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class SubtitleSegment:
    """字幕片段数据类"""
    index: int          # 序号
    start_time: float   # 开始时间(秒)
    end_time: float     # 结束时间(秒)
    text: str          # 字幕文本
    
    def __repr__(self):
        return (f"SubtitleSegment(index={self.index}, "
                f"start={self.start_time:.2f}s, "
                f"end={self.end_time:.2f}s, "
                f"text='{self.text[:30]}...')")
    
    def duration(self) -> float:
        """获取片段时长(秒)"""
        return self.end_time - self.start_time
    
    def format_time_range(self) -> str:
        """格式化时间范围为可读字符串"""
        return f"{format_timestamp(self.start_time)} --> {format_timestamp(self.end_time)}"


def parse_timestamp(timestamp_str: str) -> float:
    """将 SRT 时间戳格式转换为秒数
    
    Args:
        timestamp_str: SRT 时间戳字符串,格式为 "HH:MM:SS,mmm"
                      例如: "00:01:23,456"
    
    Returns:
        float: 秒数,例如: 83.456
    
    Examples:
        >>> parse_timestamp("00:00:00,000")
        0.0
        >>> parse_timestamp("00:01:23,456")
        83.456
        >>> parse_timestamp("01:30:45,789")
        5445.789
    """
    # 匹配格式: HH:MM:SS,mmm
    pattern = r'(\d{2}):(\d{2}):(\d{2}),(\d{3})'
    match = re.match(pattern, timestamp_str.strip())
    
    if not match:
        raise ValueError(f"无效的时间戳格式: {timestamp_str}")
    
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    
    total_seconds = (
        hours * 3600 +
        minutes * 60 +
        seconds +
        milliseconds / 1000.0
    )
    
    return total_seconds


def format_timestamp(seconds: float) -> str:
    """将秒数转换为 SRT 时间戳格式
    
    Args:
        seconds: 秒数,例如: 83.456
    
    Returns:
        str: SRT 时间戳字符串,格式为 "HH:MM:SS,mmm"
            例如: "00:01:23,456"
    
    Examples:
        >>> format_timestamp(0.0)
        '00:00:00,000'
        >>> format_timestamp(83.456)
        '00:01:23,456'
        >>> format_timestamp(5445.789)
        '01:30:45,789'
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def parse_srt_file(srt_path: Path) -> List[SubtitleSegment]:
    """解析 SRT 字幕文件
    
    Args:
        srt_path: SRT 文件路径
    
    Returns:
        List[SubtitleSegment]: 字幕片段列表
    
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件格式错误
    
    SRT 格式示例:
        1
        00:00:00,000 --> 00:00:02,500
        这是第一句字幕
        
        2
        00:00:02,500 --> 00:00:05,000
        这是第二句字幕
        可以有多行
    """
    srt_path = Path(srt_path)
    
    if not srt_path.exists():
        raise FileNotFoundError(f"SRT 文件不存在: {srt_path}")
    
    # 读取文件内容
    try:
        content = srt_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # 尝试其他编码
        try:
            content = srt_path.read_text(encoding='gbk')
        except UnicodeDecodeError:
            content = srt_path.read_text(encoding='latin-1')
    
    # 分割成字幕块(以空行分隔)
    blocks = re.split(r'\n\s*\n', content.strip())
    
    segments = []
    
    for block in blocks:
        if not block.strip():
            continue
        
        lines = block.strip().split('\n')
        
        if len(lines) < 3:
            # 格式不完整,跳过
            continue
        
        try:
            # 第一行: 序号
            index = int(lines[0].strip())
            
            # 第二行: 时间范围
            time_range = lines[1].strip()
            time_match = re.match(
                r'([\d:,]+)\s*-->\s*([\d:,]+)',
                time_range
            )
            
            if not time_match:
                continue
            
            start_str, end_str = time_match.groups()
            start_time = parse_timestamp(start_str)
            end_time = parse_timestamp(end_str)
            
            # 第三行及之后: 字幕文本(可能多行)
            text = '\n'.join(lines[2:]).strip()
            
            segment = SubtitleSegment(
                index=index,
                start_time=start_time,
                end_time=end_time,
                text=text
            )
            
            segments.append(segment)
            
        except (ValueError, IndexError) as e:
            # 解析失败,跳过这个块
            print(f"警告: 跳过无效字幕块: {e}")
            continue
    
    return segments


def get_text_at_time(segments: List[SubtitleSegment], time: float) -> Optional[str]:
    """获取指定时间点的字幕文本
    
    Args:
        segments: 字幕片段列表
        time: 时间点(秒)
    
    Returns:
        Optional[str]: 该时间点的字幕文本,如果没有则返回 None
    """
    for segment in segments:
        if segment.start_time <= time <= segment.end_time:
            return segment.text
    return None


def get_full_transcript(segments: List[SubtitleSegment], include_timestamps: bool = False) -> str:
    """获取完整转录文本
    
    Args:
        segments: 字幕片段列表
        include_timestamps: 是否包含时间戳
    
    Returns:
        str: 完整转录文本
    """
    lines = []
    
    for segment in segments:
        if include_timestamps:
            timestamp = format_timestamp(segment.start_time)
            lines.append(f"[{timestamp}] {segment.text}")
        else:
            lines.append(segment.text)
    
    return '\n'.join(lines)


def search_text(segments: List[SubtitleSegment], keyword: str) -> List[SubtitleSegment]:
    """在字幕中搜索关键词
    
    Args:
        segments: 字幕片段列表
        keyword: 搜索关键词
    
    Returns:
        List[SubtitleSegment]: 包含关键词的字幕片段列表
    """
    keyword_lower = keyword.lower()
    results = []
    
    for segment in segments:
        if keyword_lower in segment.text.lower():
            results.append(segment)
    
    return results


def get_segment_by_index(segments: List[SubtitleSegment], index: int) -> Optional[SubtitleSegment]:
    """根据序号获取字幕片段
    
    Args:
        segments: 字幕片段列表
        index: 字幕序号
    
    Returns:
        Optional[SubtitleSegment]: 对应的字幕片段,如果不存在则返回 None
    """
    for segment in segments:
        if segment.index == index:
            return segment
    return None


def export_segments_to_text(segments: List[SubtitleSegment], output_path: Path) -> None:
    """导出字幕片段为纯文本文件
    
    Args:
        segments: 字幕片段列表
        output_path: 输出文件路径
    """
    output_path = Path(output_path)
    
    lines = []
    for segment in segments:
        lines.append(f"[{segment.format_time_range()}]")
        lines.append(segment.text)
        lines.append("")  # 空行分隔
    
    content = '\n'.join(lines)
    output_path.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    # 测试代码
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python srt_parser.py <srt文件路径>")
        sys.exit(1)
    
    srt_file = Path(sys.argv[1])
    
    try:
        segments = parse_srt_file(srt_file)
        
        print(f"✅ 成功解析 {len(segments)} 个字幕片段")
        print(f"\n前 5 个片段:")
        
        for segment in segments[:5]:
            print(f"\n{segment.index}. [{segment.format_time_range()}]")
            print(f"   {segment.text}")
        
        # 统计信息
        total_duration = sum(s.duration() for s in segments)
        avg_duration = total_duration / len(segments) if segments else 0
        
        print(f"\n统计信息:")
        print(f"- 总片段数: {len(segments)}")
        print(f"- 总时长: {format_timestamp(total_duration)}")
        print(f"- 平均片段时长: {avg_duration:.2f}秒")
        
        # 获取完整文本
        full_text = get_full_transcript(segments)
        print(f"- 总字符数: {len(full_text)}")
        
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        sys.exit(1)
