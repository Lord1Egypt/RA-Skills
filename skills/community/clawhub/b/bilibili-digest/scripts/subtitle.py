"""
Subtitle extraction and cleaning.
Processes Bilibili CC subtitle JSON into clean, readable transcript text
with timestamp markers.
"""
import json
import re
import logging
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class SubtitleSegment:
    """A single subtitle segment with timing and text."""
    
    def __init__(self, start: float, end: float, content: str):
        self.start = start
        self.end = end
        self.content = content.strip()
    
    @property
    def duration(self) -> float:
        return self.end - self.start
    
    @property
    def start_time_str(self) -> str:
        return _seconds_to_timestamp(self.start)
    
    @property
    def end_time_str(self) -> str:
        return _seconds_to_timestamp(self.end)
    
    def to_dict(self) -> Dict:
        return {
            "start": self.start,
            "end": self.end,
            "start_time": self.start_time_str,
            "content": self.content,
        }


def _seconds_to_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def parse_subtitle_json(subtitle_data: Dict) -> List[SubtitleSegment]:
    """
    Parse the subtitle JSON from Bilibili API into a list of segments.
    
    Bilibili subtitle format (JSON):
    {
      "body": [
        {"from": 0.0, "to": 2.5, "content": "Hello", "location": 0},
        ...
      ]
    }
    
    Args:
        subtitle_data: Raw subtitle JSON dict from Bilibili API.
        
    Returns:
        List of SubtitleSegment objects sorted by start time.
    """
    if not subtitle_data:
        return []
    
    body = subtitle_data.get("body", [])
    if not body:
        return []
    
    segments = []
    for item in body:
        start = float(item.get("from", 0))
        end = float(item.get("to", 0))
        content = item.get("content", "").strip()
        if content:
            segments.append(SubtitleSegment(start, end, content))
    
    # Sort by start time and merge overlapping/consecutive segments
    segments.sort(key=lambda s: s.start)
    return _merge_segments(segments)


def _merge_segments(segments: List[SubtitleSegment], gap_threshold: float = 0.3) -> List[SubtitleSegment]:
    """
    Merge consecutive subtitle segments that overlap or have very small gaps.
    
    Args:
        segments: List of SubtitleSegment objects.
        gap_threshold: Max gap (seconds) to consider as consecutive.
        
    Returns:
        Merged list of segments.
    """
    if not segments:
        return []
    
    merged = [segments[0]]
    for seg in segments[1:]:
        last = merged[-1]
        if seg.start - last.end <= gap_threshold:
            # Merge: extend end time, append content
            merged[-1] = SubtitleSegment(last.start, max(last.end, seg.end),
                                          last.content + " " + seg.content)
        else:
            merged.append(seg)
    return merged


def segment_by_sentence(segments: List[SubtitleSegment]) -> List[SubtitleSegment]:
    """
    Group subtitle segments into sentence-level chunks.
    Detects sentence endings (。！？.!?) and paragraph breaks.
    """
    if not segments:
        return []
    
    SENTENCE_END = re.compile(r'[。！？.!?\n]')
    
    result = []
    current_segments = []
    current_text = ""
    
    for seg in segments:
        current_segments.append(seg)
        current_text += seg.content
        
        if SENTENCE_END.search(seg.content):
            # End of sentence
            start = current_segments[0].start
            end = current_segments[-1].end
            result.append(SubtitleSegment(start, end, current_text.strip()))
            current_segments = []
            current_text = ""
    
    # Handle trailing text without sentence ending
    if current_text.strip():
        start = current_segments[0].start
        end = current_segments[-1].end
        result.append(SubtitleSegment(start, end, current_text.strip()))
    
    return result


def get_full_transcript(segments: List[SubtitleSegment],
                        include_timestamps: bool = True) -> str:
    """
    Generate a full transcript text from subtitle segments.
    
    Args:
        segments: List of SubtitleSegment objects.
        include_timestamps: Whether to include timestamp markers.
        
    Returns:
        Full transcript as a string.
    """
    if not segments:
        return ""
    
    lines = []
    for seg in segment_by_sentence(segments):
        if include_timestamps:
            lines.append(f"[{seg.start_time_str}] {seg.content}")
        else:
            lines.append(seg.content)
    
    return "\n".join(lines)


def get_segments_with_timestamps(segments: List[SubtitleSegment]) -> List[Dict]:
    """Return a list of dicts suitable for JSON output."""
    return [seg.to_dict() for seg in segments]


def estimate_content_type(description: str, title: str, subtitle_text: str) -> str:
    """
    Heuristic to estimate video content type from available text.
    
    Returns one of: "tutorial", "lecture", "review", "vlog", "entertainment", "other"
    """
    combined = (title + " " + description + " " + subtitle_text[:500]).lower()
    
    # Common keywords for each type
    if any(w in combined for w in ["教程", "教学", "指南", "how to", "tutorial", "step", "步骤"]):
        return "tutorial"
    if any(w in combined for w in ["讲解", "深入", "原理", "分析", "lecture", "课程"]):
        return "lecture"
    if any(w in combined for w in ["测评", "评测", "review", "推荐", "vs", "对比"]):
        return "review"
    if any(w in combined for w in ["vlog", "日常", "生活"]):
        return "vlog"
    
    return "other"


def extract_resources_from_description(description: str) -> List[Dict]:
    """
    Extract resource links (GitHub, documents, websites) from video description.
    """
    resources = []
    url_pattern = re.compile(r'https?://[^\s]+')
    
    links = url_pattern.findall(description)
    for link in links:
        resource_type = "link"
        if "github.com" in link:
            resource_type = "reference"
        elif "bilibili.com" in link or "b23.tv" in link:
            resource_type = "link"
        
        resources.append({
            "name": link.split("/")[-1].replace("-", " ").replace("_", " ")[:50],
            "url": link,
            "type": resource_type,
        })
    
    return resources
