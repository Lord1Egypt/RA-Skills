"""
Danmaku (bullet comment) analysis.
- Density detection (high-density time segments)
- Sentiment grouping (positive/neutral/negative)
- Keyword extraction from high-density periods
"""
import re
import logging
from typing import List, Dict, Optional
from collections import Counter

logger = logging.getLogger(__name__)


class DanmakuEntry:
    """A single danmaku (bullet comment) entry."""
    
    def __init__(self, time_seconds: float, content: str, 
                 danmaku_id: Optional[str] = None, mode: int = 1):
        self.time_seconds = time_seconds
        self.content = content.strip()
        self.danmaku_id = danmaku_id
        self.mode = mode  # 1=scroll, 4=bottom, 5=top
    
    def __repr__(self):
        return f"[{_format_time(self.time_seconds)}] {self.content[:30]}"


def _format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def parse_danmaku_xml(xml_data: str) -> List[DanmakuEntry]:
    """
    Parse danmaku XML data (legacy format from Bilibili).
    
    Format: <d p="timestamp,type,font_size,color,...">content</d>
    """
    import html
    entries = []
    pattern = re.compile(r'<d p="([^"]*)"[^>]*>([^<]*)</d>')
    
    for match in pattern.finditer(xml_data):
        params = match.group(1).split(",")
        content = html.unescape(match.group(2).strip())
        
        if not content:
            continue
        
        try:
            time_seconds = float(params[0])
        except (ValueError, IndexError):
            continue
        
        try:
            mode = int(params[1]) if len(params) > 1 else 1
        except ValueError:
            mode = 1
        
        entries.append(DanmakuEntry(
            time_seconds=time_seconds,
            content=content,
            mode=mode,
        ))
    
    return entries


def parse_danmaku_json(danmaku_data: list) -> List[DanmakuEntry]:
    """
    Parse danmaku from JSON format (modern Bilibili API).
    
    Each entry: [progress, mode, fontsize, color, timestamp, pool, mid, content]
    """
    entries = []
    for item in danmaku_data:
        if not isinstance(item, list) or len(item) < 8:
            continue
        
        try:
            time_seconds = item[0] / 1000.0  # milliseconds to seconds
        except (TypeError, ValueError):
            continue
        
        content = str(item[7]).strip()
        if not content:
            continue
        
        entries.append(DanmakuEntry(
            time_seconds=time_seconds,
            content=content,
            mode=int(item[1]) if len(item) > 1 else 1,
        ))
    
    return entries


def detect_high_density_periods(entries: List[DanmakuEntry],
                                window_seconds: int = 30,
                                threshold_percentile: int = 90) -> List[Dict]:
    """
    Detect time periods with unusually high danmaku density.
    
    Args:
        entries: List of DanmakuEntry objects.
        window_seconds: Time window for density calculation.
        threshold_percentile: Percentile threshold for "high density."
        
    Returns:
        List of high-density periods with time range and top keywords.
    """
    if not entries:
        return []
    
    # Build time histogram
    max_time = max(e.time_seconds for e in entries)
    buckets = {}
    
    for entry in entries:
        bucket = int(entry.time_seconds // window_seconds) * window_seconds
        if bucket not in buckets:
            buckets[bucket] = []
        buckets[bucket].append(entry)
    
    # Calculate density per bucket
    density_data = []
    for bucket_start, bucket_entries in buckets.items():
        density_data.append({
            "start_seconds": bucket_start,
            "end_seconds": bucket_start + window_seconds,
            "count": len(bucket_entries),
            "entries": bucket_entries,
        })
    
    density_data.sort(key=lambda d: d["start_seconds"])
    
    if not density_data:
        return []
    
    # Find threshold
    counts = [d["count"] for d in density_data]
    counts.sort()
    threshold_idx = int(len(counts) * threshold_percentile / 100)
    threshold = counts[threshold_idx] if threshold_idx < len(counts) else counts[-1]
    
    # Filter high density periods
    highlights = []
    for d in density_data:
        if d["count"] >= threshold:
            keywords = _extract_keywords(d["entries"], top_n=5)
            highlights.append({
                "timestamp": _format_time(d["start_seconds"]),
                "start_seconds": d["start_seconds"],
                "end_seconds": d["end_seconds"],
                "density": d["count"],
                "keywords": keywords,
                "sentiment": _estimate_sentiment_keywords(keywords),
            })
    
    return highlights


def _extract_keywords(entries: List[DanmakuEntry], top_n: int = 5) -> List[str]:
    """Extract most common meaningful words from danmaku content."""
    # Filter out common stop words
    stop_words = set("的了在是和我有就也这那吧吗啊呢哈哦嗯诶哟哇哈哈嘻嘻".strip())
    
    words = []
    for entry in entries:
        # Simple Chinese word splitting by character for frequency analysis
        for char in entry.content:
            if char not in stop_words and len(char.strip()) > 0 and '\u4e00' <= char <= '\u9fff':
                words.append(char)
    
    # Also extract 2-char bigrams
    bigrams = []
    for entry in entries:
        text = entry.content
        for i in range(len(text) - 1):
            bigram = text[i:i+2]
            if all('\u4e00' <= c <= '\u9fff' for c in bigram):
                bigrams.append(bigram)
    
    counter = Counter(words)
    bigram_counter = Counter(bigrams)
    
    result = [w for w, _ in counter.most_common(top_n)]
    result.extend([w for w, _ in bigram_counter.most_common(top_n // 2)])
    
    return result[:top_n]


def _estimate_sentiment_keywords(keywords: List[str]) -> str:
    """Rough sentiment estimation based on keywords."""
    positive = {"好", "赞", "牛", "强", "妙", "厉害", "精彩", "绝了"}
    negative = {"差", "烂", "坑", "骗", "垃圾", "无语", "离谱"}
    
    pos_count = sum(1 for kw in keywords if kw in positive)
    neg_count = sum(1 for kw in keywords if kw in negative)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


def generate_danmaku_summary(entries: List[DanmakuEntry],
                              duration_seconds: int) -> Dict:
    """
    Generate a full danmaku analysis summary.
    """
    if not entries:
        return {"status": "no_data", "message": "No danmaku available"}
    
    highlights = detect_high_density_periods(entries)
    
    # Overall stats
    total_comments = len(entries)
    density_per_minute = total_comments / (duration_seconds / 60) if duration_seconds > 0 else 0
    
    return {
        "status": "success",
        "total_comments": total_comments,
        "density_per_minute": round(density_per_minute, 1),
        "highlights": highlights,
    }
