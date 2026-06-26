"""
Local 字幕压制：生成 ASS 字幕文件 → ffmpeg 硬压到视频。
适配自 video-translation/scripts/base/burn_subtitle.py。
"""
from __future__ import annotations

import math
import tempfile
from pathlib import Path
from typing import Any

from ffmpeg_utils import burn_ass_subtitle, probe_video_info


def _sec_to_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _to_ass_color(hex_color: str) -> str:
    c = hex_color.strip().lstrip("#")
    if len(c) == 8:
        rr, gg, bb, aa = c[0:2], c[2:4], c[4:6], c[6:8]
    elif len(c) == 6:
        rr, gg, bb = c[0:2], c[2:4], c[4:6]
        aa = "00"
    else:
        return "&H00FFFFFF"
    return f"&H{aa}{bb}{gg}{rr}"


def _auto_font_size(width: int, height: int) -> int:
    short_edge = min(width, height)
    return max(24, int(short_edge * 0.045))


def _auto_margin_v(height: int) -> int:
    return max(24, int(height * 0.10))


def _auto_margin_h(width: int) -> int:
    return max(24, int(width * 0.05))


def build_ass(
    segments: list[dict[str, Any]],
    width: int,
    height: int,
    *,
    font_name: str = "Arial",
    font_size: int = 0,
    font_color: str = "#FFFFFF",
    outline_color: str = "#000000",
    shadow_color: str = "#000000",
    outline: float = 1.5,
    shadow: float = 2.0,
    margin_l: int = 0,
    margin_r: int = 0,
    margin_v: int = 0,
    max_lines: int = 2,
) -> str:
    """生成 ASS 字幕文本"""
    font_size = font_size if font_size > 0 else _auto_font_size(width, height)
    margin_l = margin_l if margin_l > 0 else _auto_margin_h(width)
    margin_r = margin_r if margin_r > 0 else _auto_margin_h(width)
    margin_v = margin_v if margin_v > 0 else _auto_margin_v(height)

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {width}",
        f"PlayResY: {height}",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{font_name},{font_size},{_to_ass_color(font_color)},{_to_ass_color(font_color)},"
        f"{_to_ass_color(outline_color)},{_to_ass_color(shadow_color)},"
        f"0,0,0,0,100,100,0,0,1,{outline:.1f},{shadow:.1f},2,{margin_l},{margin_r},{margin_v},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for seg in segments:
        start = _sec_to_ass_time(float(seg.get("start", seg.get("start_time", 0))))
        end = _sec_to_ass_time(float(seg.get("end", seg.get("end_time", 0))))
        text = str(seg.get("text", seg.get("Text", ""))).strip()
        if text:
            lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")
    return "\n".join(lines) + "\n"


def burn_subtitles(
    video_in: Path,
    segments: list[dict[str, Any]],
    video_out: Path,
    **style_kwargs,
) -> Path:
    """生成 ASS 并硬压到视频"""
    info = probe_video_info(video_in)
    width = info.get("Width", 1280)
    height = info.get("Height", 720)

    ass_text = build_ass(segments, width, height, **style_kwargs)

    with tempfile.TemporaryDirectory(prefix="burn_sub_") as td:
        ass_path = Path(td) / "subtitle.ass"
        ass_path.write_text(ass_text, encoding="utf-8")
        burn_ass_subtitle(video_in, ass_path, video_out)

    return video_out
