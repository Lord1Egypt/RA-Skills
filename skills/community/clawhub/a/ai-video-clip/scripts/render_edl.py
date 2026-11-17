#!/usr/bin/env python3
"""Render EDL — 按照 Edit Decision List 渲染最终视频。

支持:
  - 按 keep/cut/transition/overlay 等指令调用 FFmpeg
  - 自动音频 crossfade (30ms at cut points)
  - 字幕烧录、色彩校正
  - 视频连接 concat 渲染

使用:
  python3 render_edl.py --edl edl.json --output edit/final.mp4
  python3 render_edl.py --edl edl.json --output edit/ --segments
"""

import argparse
import json
import os
import subprocess
import shutil
import sys
import tempfile
from typing import Optional


def _run_ffmpeg(cmd: list, description: str = "") -> bool:
    """执行 FFmpeg 命令。"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  错误 [{description}]: {result.stderr[:300]}", file=sys.stderr)
        return False
    return True


def get_video_info(path: str) -> dict:
    """获取视频基本信息。"""
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
           "-show_format", "-show_streams", path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {}
    try:
        data = json.loads(result.stdout)
        info = {"duration": float(data.get("format", {}).get("duration", 0)),
                "width": 0, "height": 0, "fps": 0}
        for s in data.get("streams", []):
            if s.get("codec_type") == "video":
                info["width"] = s.get("width", 0)
                info["height"] = s.get("height", 0)
                parts = s.get("r_frame_rate", "0/1").split("/")
                info["fps"] = int(parts[0]) / int(parts[1]) if len(parts) == 2 else 0
                break
        return info
    except Exception:
        return {}


def extract_segment(input_path: str, start: float, end: float,
                    output: str, crossfade: float = 0.03) -> bool:
    """提取视频片段（带音频 crossfade）。"""
    duration = end - start
    if duration <= 0:
        return False

    vf_parts = []
    af_parts = []

    if crossfade > 0:
        af_parts.append(f"afade=t=in:st=0:d={crossfade}")
        af_parts.append(f"afade=t=out:st={duration - crossfade}:d={crossfade}")

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", input_path,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-avoid_negative_ts", "make_zero",
    ]

    if af_parts:
        cmd += ["-af", ",".join(af_parts)]

    cmd.append(output)
    return _run_ffmpeg(cmd, f"extract {start}-{end}")


def apply_color_grade(input_path: str, output: str, lut: str = "warm",
                       strength: float = 0.8) -> bool:
    """应用色彩校正。"""
    filters = {
        "warm": f"eq=brightness=0.02:saturation=1.15:contrast=1.05",
        "cool": f"eq=brightness=-0.02:saturation=0.9:contrast=1.05:gamma_r=0.95:gamma_b=1.05",
        "cinematic": f"eq=contrast=1.15:saturation=0.85:brightness=-0.05",
        "vivid": f"eq=saturation=1.4:contrast=1.1:brightness=0.03",
    }
    vf = filters.get(lut, filters["warm"])
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "copy",
        output,
    ]
    return _run_ffmpeg(cmd, f"color grade: {lut}")


def burn_subtitles_on_segment(input_path: str, srt_path: str, output: str,
                               style: Optional[dict] = None) -> bool:
    """给片段烧录字幕。"""
    if not srt_path or not os.path.exists(srt_path):
        # 无字幕，直接复制
        shutil.copy(input_path, output)
        return True

    style = style or {}
    font = style.get("font", "Arial")
    size = style.get("size", 20)
    color = style.get("color", "white")
    outline = style.get("outline", 1)
    position = style.get("position", "center")

    margin_v = 50
    if position == "top":
        margin_v = 30
    elif position == "bottom":
        margin_v = 80

    force_style = (
        f"FontName={font},FontSize={size},"
        f"PrimaryColour=&H{color}&,Outline={outline},"
        f"Alignment=2,MarginV={margin_v}"
    )

    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"subtitles='{srt_path}':force_style='{force_style}'",
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        output,
    ]
    return _run_ffmpeg(cmd, "burn subtitles")


def concat_segments(segment_paths: list, output: str) -> bool:
    """使用 FFmpeg concat demuxer 拼接片段。"""
    if not segment_paths:
        print("错误: 没有片段可拼接", file=sys.stderr)
        return False

    # 写 concat file list
    list_file = output + ".concat.txt"
    with open(list_file, "w") as f:
        for sp in segment_paths:
            f.write(f"file '{sp}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        output,
    ]
    ok = _run_ffmpeg(cmd, "concat segments")
    os.remove(list_file) if os.path.exists(list_file) else None
    return ok


def render_edl(edl: dict, output: str, keep_segments: bool = False) -> bool:
    """按 EDL 渲染最终视频。"""
    edits = edl.get("edits", [])
    sources = {s["id"]: s for s in edl.get("sources", [])}

    if not edits:
        print("错误: EDL 没有编辑指令", file=sys.stderr)
        return False

    print(f"EDL 包含 {len(edits)} 条编辑指令")

    output_dir = os.path.dirname(os.path.abspath(output))
    os.makedirs(output_dir, exist_ok=True)

    tmp_dir = tempfile.mkdtemp(prefix="edl_render_")
    segment_files = []

    try:
        for i, edit in enumerate(edits):
            edit_type = edit.get("type", "keep")

            if edit_type not in ("keep",):
                # 跳过非 keep 类型的编辑（transition/overlay 等高级功能）
                print(f"  [{i+1}/{len(edits)}] 跳过 {edit_type} (暂不支持)")
                continue

            source_id = edit.get("source", edit.get("source_id", "src0"))
            src_info = sources.get(source_id, {})
            src_path = src_info.get("path", "")
            start = edit.get("start", 0)
            end = edit.get("end", 0)
            reason = edit.get("reason", "")
            params = edit.get("params", {})

            if not src_path or end <= start:
                continue

            seg_file = os.path.join(tmp_dir, f"seg_{i:04d}.mp4")
            print(f"  [{i+1}/{len(edits)}] {start:.1f}s-{end:.1f}s ({end - start:.1f}s)"
                  f" — {reason[:50]}")

            # Step 1: 提取片段
            if not extract_segment(src_path, start, end, seg_file):
                continue

            current = seg_file

            # Step 2: 色彩校正（如果有）
            if params.get("color_grade"):
                graded = os.path.join(tmp_dir, f"seg_{i:04d}_graded.mp4")
                if apply_color_grade(current, graded, params["color_grade"]):
                    current = graded

            # Step 3: 字幕（如果有）
            if params.get("srt_path"):
                subtitled = os.path.join(tmp_dir, f"seg_{i:04d}_sub.mp4")
                if burn_subtitles_on_segment(current, params["srt_path"], subtitled):
                    current = subtitled

            segment_files.append(current)

        if not segment_files:
            print("错误: 没有成功渲染任何片段", file=sys.stderr)
            return False

        print(f"\n拼接 {len(segment_files)} 个片段...")

        # 如果只要独立片段
        if keep_segments:
            for i, sf in enumerate(segment_files):
                final_name = os.path.join(output_dir, f"segment_{i+1:02d}.mp4")
                shutil.copy(sf, final_name)
                print(f"  segment_{i+1:02d}.mp4")
            return True

        # 拼接为最终视频
        ok = concat_segments(segment_files, output)
        if ok:
            total_seconds = sum(
                e.get("end", 0) - e.get("start", 0)
                for e in edits if e.get("type") == "keep"
            )
            print(f"\n渲染完成: {output}")
            print(f"  总片段数: {len(segment_files)}")
            print(f"  总时长: {total_seconds:.1f}s")
        return ok

    finally:
        # 清理临时文件
        import shutil as _sh
        _sh.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="按 EDL 渲染视频")
    p.add_argument("--edl", required=True, help="EDL JSON 文件路径")
    p.add_argument("--output", default="edit/final.mp4", help="输出文件路径")
    p.add_argument("--segments", action="store_true",
                   help="输出独立片段而非拼接")
    p.add_argument("--dry-run", action="store_true",
                   help="仅打印将执行的操作")
    args = p.parse_args()

    if not shutil.which("ffmpeg"):
        print("错误: ffmpeg 未安装", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.edl):
        print(f"错误: EDL 文件不存在: {args.edl}", file=sys.stderr)
        sys.exit(1)

    with open(args.edl, "r", encoding="utf-8") as f:
        edl = json.load(f)

    if args.dry_run:
        edits = edl.get("edits", [])
        print(f"EDL: {len(edits)} edits, strategy={edl.get('strategy', {}).get('name')}")
        for i, edit in enumerate(edits):
            print(f"  [{i+1}] {edit.get('type')}: "
                  f"{edit.get('start', 0):.1f}s-{edit.get('end', 0):.1f}s "
                  f"({edit.get('reason', '')[:40]})")
        total = sum(e.get("end", 0) - e.get("start", 0) for e in edits)
        print(f"\n预估总时长: {total:.1f}s")
        sys.exit(0)

    ok = render_edl(edl, args.output, args.segments)
    sys.exit(0 if ok else 1)
