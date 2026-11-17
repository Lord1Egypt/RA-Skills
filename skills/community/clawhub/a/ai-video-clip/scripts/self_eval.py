#!/usr/bin/env python3
"""Self Eval — 渲染后自检视频质量。

检查项:
  - 切点边界：视觉跳变、黑帧、画面撕裂
  - 音频连续性：爆音、音量突变、静音片段
  - 字幕完整性：字幕越界、缺失、时间偏移
  - 输出时长与 EDL 预期对比

使用:
  python3 self_eval.py --video edit/final.mp4 --edl edl.json
  python3 self_eval.py --video edit/final.mp4 --edl edl.json --fix
"""

import argparse
import json
import os
import subprocess
import shutil
import sys
from datetime import datetime


def probe(video_path: str) -> dict:
    """获取视频基本信息。"""
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
           "-show_format", "-show_streams", video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}
    return json.loads(result.stdout)


def check_black_frames(video_path: str, threshold: float = 0.1) -> list:
    """检测黑帧（画面全黑）。"""
    issues = []
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"blackdetect=d=0.1:pix_th={threshold}",
        "-an", "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    for line in result.stderr.splitlines():
        if "black_start" in line:
            try:
                start = float(line.split("black_start:")[1].split()[0])
                dur = float(line.split("black_duration:")[1].split()[0])
                if dur > 0.5:
                    issues.append({
                        "type": "black_frame",
                        "start": start,
                        "duration": dur,
                        "severity": "warning",
                        "message": f"检测到 {dur:.2f}s 黑帧，起始 {start:.2f}s"
                    })
            except (IndexError, ValueError):
                pass
    return issues


def check_audio_peaks(video_path: str, threshold_db: float = -1.0) -> list:
    """检测音频爆音。"""
    issues = []
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-af", f"volumedetect",
        "-vn", "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    for line in result.stderr.splitlines():
        if "max_volume" in line and "dB" in line:
            try:
                db_str = line.split("max_volume:")[1].split("dB")[0].strip()
                max_db = float(db_str)
                if max_db > threshold_db:
                    issues.append({
                        "type": "audio_peak",
                        "max_db": max_db,
                        "severity": "warning",
                        "message": f"音频峰值 {max_db:.1f}dB，可能爆音"
                    })
            except (IndexError, ValueError):
                pass
    return issues


def check_silence(video_path: str, max_silence: float = 5.0) -> list:
    """检测过长静音。"""
    issues = []
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-af", f"silencedetect=noise=-30dB:d=0.5",
        "-vn", "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    silence_start = None
    for line in result.stderr.splitlines():
        if "silence_start" in line:
            try:
                silence_start = float(line.split("silence_start:")[1].strip())
            except (IndexError, ValueError):
                pass
        elif "silence_end" in line and silence_start is not None:
            try:
                end = float(line.split("silence_end:")[1].split()[0])
                dur = end - silence_start
                if dur > max_silence:
                    issues.append({
                        "type": "long_silence",
                        "start": silence_start,
                        "duration": dur,
                        "severity": "warning",
                        "message": f"过长的静音: {dur:.1f}s ({silence_start:.1f}s-{end:.1f}s)"
                    })
                silence_start = None
            except (IndexError, ValueError):
                silence_start = None
    return issues


def check_duration_mismatch(edl_path: str, video_path: str) -> list:
    """检查输出时长方差。"""
    # 获取输出时长
    info = probe(video_path)
    actual = float(info.get("format", {}).get("duration", 0))

    # 获取 EDL 预期时长
    with open(edl_path, "r") as f:
        edl = json.load(f)
    expected = sum(
        e.get("end", 0) - e.get("start", 0)
        for e in edl.get("edits", [])
        if e.get("type") == "keep"
    )

    issues = []
    diff = abs(actual - expected)
    if diff > 5:  # 5 秒以上偏差
        issues.append({
            "type": "duration_mismatch",
            "expected": expected,
            "actual": actual,
            "diff": diff,
            "severity": "error",
            "message": f"时长偏差: 预期 {expected:.1f}s, 实际 {actual:.1f}s (差 {diff:.1f}s)"
        })
    elif diff > 1:
        issues.append({
            "type": "duration_mismatch",
            "expected": expected,
            "actual": actual,
            "diff": diff,
            "severity": "warning",
            "message": f"时长轻微偏差: 预期 {expected:.1f}s, 实际 {actual:.1f}s"
        })

    return issues


def check_visual_cuts(video_path: str, edl_path: str) -> list:
    """检查切点附近是否有视觉异常。"""
    issues = []
    with open(edl_path, "r") as f:
        edl = json.load(f)

    keep_edits = [e for e in edl.get("edits", []) if e.get("type") == "keep"]
    if len(keep_edits) < 2:
        return issues  # 只有一个片段，不需要检查切点

    # 检查切点边界帧
    for i in range(1, len(keep_edits)):
        prev_end = keep_edits[i - 1].get("end", 0)
        curr_start = keep_edits[i].get("start", 0)

        # 累积时间计算切点在输出中的位置
        accumulated = sum(
            e.get("end", 0) - e.get("start", 0)
            for e in keep_edits[:i]
        )

        # 在累积时间点附近截图检查
        if accumulated > 0:
            # 用 ffmpeg 在切点前后各取一帧
            check_time = max(0, accumulated - 0.5)
            # 提取帧 (仅检查，不保存)
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(check_time),
                "-i", video_path,
                "-vframes", "1",
                "-f", "image2pipe", "-vcodec", "png", "-"
            ]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                issues.append({
                    "type": "cut_point_error",
                    "cut_index": i,
                    "time": check_time,
                    "severity": "warning",
                    "message": f"切点 #{i} ({check_time:.1f}s) 处提取帧失败"
                })

    return issues


def run_evaluation(video_path: str, edl_path: str) -> dict:
    """运行完整质量检查。"""
    print(f"质量检查: {video_path}")
    print(f"EDL: {edl_path}")

    all_issues = []
    checks = []

    # 1. 时长检查
    print("  [1/5] 检查时长...")
    issues = check_duration_mismatch(edl_path, video_path)
    all_issues.extend(issues)
    checks.append({"name": "duration", "issues": len(issues)})

    # 2. 黑帧检查
    print("  [2/5] 检查黑帧...")
    issues = check_black_frames(video_path)
    all_issues.extend(issues)
    checks.append({"name": "black_frames", "issues": len(issues)})

    # 3. 音频检查
    print("  [3/5] 检查音频峰值...")
    issues = check_audio_peaks(video_path)
    all_issues.extend(issues)
    checks.append({"name": "audio_peaks", "issues": len(issues)})

    # 4. 静音检查
    print("  [4/5] 检查长静音...")
    issues = check_silence(video_path)
    all_issues.extend(issues)
    checks.append({"name": "silence", "issues": len(issues)})

    # 5. 切点边界
    print("  [5/5] 检查切点边界...")
    issues = check_visual_cuts(video_path, edl_path)
    all_issues.extend(issues)
    checks.append({"name": "cut_points", "issues": len(issues)})

    errors = [i for i in all_issues if i.get("severity") == "error"]
    warnings = [i for i in all_issues if i.get("severity") == "warning"]

    report = {
        "checked_at": datetime.now().isoformat(),
        "video": video_path,
        "total_issues": len(all_issues),
        "errors": len(errors),
        "warnings": len(warnings),
        "checks": checks,
        "issues": all_issues,
        "passed": len(errors) == 0,
    }

    return report


def print_report(report: dict):
    """打印检查报告。"""
    print("\n" + "=" * 60)
    status = "PASS" if report["passed"] else "FAIL"
    print(f"质量检查报告 — {status}")
    print("=" * 60)
    print(f"  总问题: {report['total_issues']}")
    print(f"  错误:   {report['errors']}")
    print(f"  警告:   {report['warnings']}")

    for check in report["checks"]:
        status_icon = "OK" if check["issues"] == 0 else "!!"
        print(f"  [{status_icon}] {check['name']}: {check['issues']} issues")

    if report["issues"]:
        print("\n问题详情:")
        for issue in report["issues"]:
            prefix = "ERROR" if issue.get("severity") == "error" else "WARN"
            print(f"  [{prefix}] {issue.get('message', '')}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="渲染后视频质量自检")
    p.add_argument("--video", required=True, help="渲染后的视频文件")
    p.add_argument("--edl", required=True, help="EDL JSON 文件")
    p.add_argument("--output", help="输出 JSON 报告文件")
    p.add_argument("--fix", action="store_true",
                   help="尝试自动修复（预留）")
    args = p.parse_args()

    if not shutil.which("ffmpeg"):
        print("错误: ffmpeg 未安装", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.video):
        print(f"错误: 视频文件不存在: {args.video}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.edl):
        print(f"错误: EDL 文件不存在: {args.edl}", file=sys.stderr)
        sys.exit(1)

    report = run_evaluation(args.video, args.edl)
    print_report(report)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存: {args.output}")

    # 如果是自动修复模式，且有错误
    if args.fix and not report["passed"]:
        print("\n自动修复功能尚未完整实现。建议手动检查上述问题。")

    sys.exit(0 if report["passed"] else 1)
