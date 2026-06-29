"""
Video chapter segmentation.
- Detects natural chapter boundaries from subtitle gaps and transition words
- Generates chapter titles using LLM
- Supports Bilibili native chapter info when available
"""
import re
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


# Chinese transition words indicating a new section
TRANSITION_WORDS = [
    "接下来", "然后", "最后", "另外", "此外", "还有一个",
    "第一", "第二", "第三", "首先", "其次", "再次",
    "第一个", "第二个", "第三个",
    "首先我们", "接下来我们", "最后我们",
    "好那我们", "好了", "好的那么",
    "所以总结", "总结一下", "简单总结",
    "我们来谈谈", "再来看看", "接下来看",
]

# English transition words
ENG_TRANSITION_WORDS = [
    "next", "then", "finally", "lastly", "first", "second", "third",
    "another", "additionally", "moreover", "in summary", "to sum up",
    "let's talk about", "moving on", "now let's",
]

ALL_TRANSITION_WORDS = TRANSITION_WORDS + ENG_TRANSITION_WORDS


def detect_chapters_from_subtitles(
    segments: list,
    min_chapter_duration: int = 60,
    gap_threshold: float = 5.0,
) -> List[Dict]:
    """
    Detect chapter boundaries from subtitle segments.
    
    Strategy:
    1. Use Bilibili native chapter markers if available
    2. Detect long pauses (>5s) as potential chapter boundaries
    3. Detect transition words as chapter starts
    
    Args:
        segments: List of SubtitleSegment objects.
        min_chapter_duration: Minimum chapter length in seconds.
        gap_threshold: Gap in seconds indicating a new chapter.
        
    Returns:
        List of chapter dicts with start, end, tentative title.
    """
    if not segments:
        return []
    
    # Find boundary candidates
    boundaries = []
    
    # Gap detection
    for i in range(1, len(segments)):
        gap = segments[i].start - segments[i-1].end
        if gap >= gap_threshold:
            boundaries.append({
                "type": "gap",
                "seconds": segments[i].start,
                "confidence": min(gap / 10.0, 1.0),  # higher gap = higher confidence
            })
    
    # Transition word detection
    for seg in segments:
        content = seg.content.lower()
        for word in ALL_TRANSITION_WORDS:
            if word.lower() in content:
                boundaries.append({
                    "type": "transition_word",
                    "seconds": seg.start,
                    "word": word,
                    "confidence": 0.7,
                })
                break
    
    # Sort and deduplicate boundaries
    boundaries.sort(key=lambda b: b["seconds"])
    deduped = []
    seen_times = set()
    for b in boundaries:
        bucket = int(b["seconds"] / 10) * 10
        if bucket not in seen_times:
            seen_times.add(bucket)
            deduped.append(b)
    
    # Build chapters
    chapters = []
    video_end = segments[-1].end if segments else 0
    
    prev_boundary = 0
    for i, boundary in enumerate(deduped):
        if boundary["seconds"] - prev_boundary >= min_chapter_duration:
            chapters.append({
                "index": i + 1,
                "start_seconds": prev_boundary,
                "end_seconds": boundary["seconds"],
                "confidence": boundary["confidence"],
                "title": f"Chapter {i + 1}",
                "summary": "",
            })
            prev_boundary = boundary["seconds"]
    
    # Last chapter
    if video_end - prev_boundary >= min_chapter_duration:
        chapters.append({
            "index": len(chapters) + 1,
            "start_seconds": prev_boundary,
            "end_seconds": video_end,
            "confidence": 0.5,
            "title": f"Chapter {len(chapters) + 1}",
            "summary": "",
        })
    
    # If no chapters detected, create one big chapter
    if not chapters and video_end > 0:
        chapters.append({
            "index": 1,
            "start_seconds": 0,
            "end_seconds": video_end,
            "confidence": 1.0,
            "title": "Full Video",
            "summary": "",
        })
    
    return chapters


def get_chapter_context(segments: list, chapter: Dict) -> str:
    """Get the subtitle text for a specific chapter."""
    chapter_text = []
    for seg in segments:
        if chapter["start_seconds"] <= seg.start <= chapter["end_seconds"]:
            chapter_text.append(seg.content)
        elif seg.start > chapter["end_seconds"]:
            break
    return " ".join(chapter_text)


def build_chapter_prompt(chapters: List[Dict], segments: list, video_title: str) -> str:
    """
    Build an LLM prompt to generate chapter titles and summaries.
    """
    prompt = f"""Video title: {video_title}

Below are the detected chapter boundaries. For each chapter, provide:
1. A concise, informative chapter title (in Chinese or English matching the video)
2. A 1-sentence summary of what this chapter covers

Chapters:
"""
    for ch in chapters:
        context = get_chapter_context(segments, ch)
        context_preview = context[:200] + "..." if len(context) > 200 else context
        prompt += f"""
Chapter {ch['index']}: {_format_time(ch['start_seconds'])} - {_format_time(ch['end_seconds'])}
Content preview: "{context_preview}"
---
"""
    
    prompt += """
Respond in JSON format:
[
  {"index": 1, "title": "...", "summary": "..."},
  ...
]"""
    return prompt


def _format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def classify_video_type(segments: list, title: str, description: str) -> str:
    """
    Classify video content type based on structure and keywords.
    
    Returns: "tutorial", "lecture", "review", "vlog", "other"
    """
    from subtitle import estimate_content_type
    full_text = " ".join(s.content for s in segments[:50])
    return estimate_content_type(description, title, full_text)
