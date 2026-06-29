"""
Cross-video merging engine.
Merges key points, viewpoints, and knowledge from multiple Bilibili videos
on the same topic into a single consolidated note.
"""
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def merge_results(results: List[Dict]) -> Dict:
    """
    Merge multiple video digests into a cross-video summary.
    
    Args:
        results: List of individual video result dicts.
        
    Returns:
        Cross-video summary dict with common themes, viewpoint comparisons,
        and merged knowledge.
    """
    if not results:
        return {}
    
    if len(results) == 1:
        return {
            "common_themes": [],
            "viewpoint_comparison": [],
            "merged_knowledge": results[0].get("content", {}).get("summary_overview", ""),
        }
    
    # Extract individual summaries
    summaries = []
    for r in results:
        meta = r.get("metadata", {})
        content = r.get("content", {})
        summaries.append({
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "url": r.get("url", ""),
            "one_liner": content.get("summary_one_liner", ""),
            "key_points": content.get("key_points", []),
            "overview": content.get("summary_overview", ""),
        })
    
    # Build consolidated key points (deduplication by simple text matching)
    all_points = []
    seen_points = set()
    for s in summaries:
        for kp in s.get("key_points", []):
            point_text = kp.get("point", kp.get("content", ""))
            if point_text and point_text[:30] not in seen_points:
                seen_points.add(point_text[:30])
                all_points.append({
                    "point": point_text,
                    "timestamp": kp.get("timestamp", ""),
                    "source": s["title"],
                    "author": s["author"],
                })
    
    # Build viewpoint comparison
    viewpoint_comparison = _build_viewpoint_comparison(summaries)
    
    # Build common themes (simple keyword overlap)
    common_themes = _extract_common_themes(summaries)
    
    # Build merged knowledge text
    merged = _build_merged_knowledge(summaries)
    
    return {
        "common_themes": common_themes,
        "viewpoint_comparison": viewpoint_comparison,
        "merged_knowledge": merged,
        "merged_key_points": all_points[:20],  # Limit to top 20
    }


def _build_viewpoint_comparison(summaries: List[Dict]) -> List[Dict]:
    """Compare viewpoints across different videos on same topics."""
    # This is a simplified version that groups by topic keywords
    topics = {}
    
    for s in summaries:
        for kp in s.get("key_points", []):
            point_text = kp.get("point", kp.get("content", ""))
            # Simple topic extraction: use first 10 chars as topic key
            if len(point_text) > 5:
                topic_key = point_text[:15]
                if topic_key not in topics:
                    topics[topic_key] = {"topic": point_text[:30], "perspectives": []}
                topics[topic_key]["perspectives"].append({
                    "author": s["author"],
                    "viewpoint": point_text[:100],
                })
    
    # Return topics with at least 2 perspectives
    result = []
    for topic_key, data in topics.items():
        if len(data["perspectives"]) >= 2:
            result.append(data)
        elif len(result) < 3:  # Include some single-source topics too
            result.append(data)
    
    return result[:10]  # Max 10 topics


def _extract_common_themes(summaries: List[Dict]) -> List[str]:
    """Extract themes that appear across multiple videos."""
    # Simplified: use one-liners as theme sources
    themes = []
    for s in summaries:
        one_liner = s.get("one_liner", "")
        if one_liner:
            # Take first sentence or key phrase
            import re
            sentences = re.split(r'[。！？，]', one_liner)
            for sent in sentences[:2]:
                sent = sent.strip()
                if sent and 5 <= len(sent) <= 80:
                    themes.append(sent)
    
    return themes[:8]  # Max 8 themes


def _build_merged_knowledge(summaries: List[Dict]) -> str:
    """Build a comprehensive merged knowledge text."""
    sections = []
    
    for i, s in enumerate(summaries):
        sections.append(f"### {i+1}. {s['title']} (by {s['author']})")
        
        overview = s.get("overview", "")
        if overview:
            sections.append(overview)
        
        points = s.get("key_points", [])
        if points:
            for j, kp in enumerate(points[:5]):
                point = kp.get("point", kp.get("content", ""))
                ts = kp.get("timestamp", "")
                ts_str = f" [{ts}]" if ts else ""
                sections.append(f"- {point}{ts_str}")
        
        sections.append("")
    
    return "\n".join(sections)
