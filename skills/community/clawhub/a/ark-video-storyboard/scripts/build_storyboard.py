#!/usr/bin/env python3
"""Build a multi-segment storyboard skeleton for a target total duration."""

from __future__ import annotations

import json
import math
import sys
from typing import Any, Dict, List

DEFAULT_FUNCTIONS = ["establish", "deepen", "peak", "resolve", "transition", "resolve"]


def build_storyboard(scene: str, style: str = "cinematic", total_duration_seconds: int = 60, segment_count: int = 6) -> Dict[str, Any]:
    if segment_count <= 0:
        raise ValueError("segment_count must be > 0")
    per_segment = total_duration_seconds // segment_count
    segments: List[Dict[str, Any]] = []
    for idx in range(1, segment_count + 1):
        start = (idx - 1) * per_segment
        end = idx * per_segment
        fn = DEFAULT_FUNCTIONS[idx - 1] if idx - 1 < len(DEFAULT_FUNCTIONS) else "deepen"
        segments.append(
            {
                "segment_index": idx,
                "start_second": start,
                "end_second": end,
                "duration_seconds": per_segment,
                "story_function": fn,
                "visual_description": f"第{idx}段：基于场景描述继续扩写画面。原始场景：{scene}",
                "lighting_state": "根据剧情推进补充光照变化。",
                "continuity_notes": "与上一段和下一段保持主体、环境、风格连续。",
                "camera_language": "补充镜头视角、运动和节奏。",
                "voiceover_or_caption": "",
                "ai_prompt": f"Write a cinematic English video prompt for segment {idx} based on this scene: {scene}. Maintain visual continuity and {style} style.",
                "negative_prompt": "",
            }
        )
    return {
        "title": f"Untitled {total_duration_seconds}s Video",
        "theme": scene,
        "total_duration_seconds": total_duration_seconds,
        "segment_count": segment_count,
        "character_rule": "All human characters are East Asian unless explicitly specified otherwise.",
        "style_summary": style,
        "overall_story": scene,
        "segments": segments,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: build_storyboard.py <scene_description> [style] [total_duration_seconds] [segment_count]", file=sys.stderr)
        sys.exit(1)
    scene = sys.argv[1]
    style = sys.argv[2] if len(sys.argv) > 2 else "cinematic"
    total_duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    segment_count = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    print(json.dumps(build_storyboard(scene, style, total_duration, segment_count), ensure_ascii=False, indent=2))
