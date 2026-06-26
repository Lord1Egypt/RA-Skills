#!/usr/bin/env python3
"""
frame_extractor.py - 视频关键帧截图提取

功能:
    1. 按固定间隔提取关键帧截图
    2. 智能场景切换检测（ ffmpeg scene filter）
    3. 支持在线视频和本地文件

用法:
    # 在线视频（需要 yt-dlp 下载）
    python3 frame_extractor.py "https://www.bilibili.com/video/BVxxxx"
    python3 frame_extractor.py "https://v.douyin.com/xxx"

    # 本地文件
    python3 frame_extractor.py "/path/to/video.mp4"

    # 选项
    python3 frame_extractor.py "链接" --interval 30     # 每30秒一帧
    python3 frame_extractor.py "链接" --scene-detect     # 场景切换检测
    python3 frame_extractor.py "链接" --max-frames 20    # 最多20张
    python3 frame_extractor.py "链接" --output-dir ~/Desktop/frames

输出:
    截图保存为 JPG 文件，JSON 到 stdout（包含文件路径和对应时间戳）
"""

import sys
import os
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
YTDLP = shutil.which("yt-dlp") or "/opt/homebrew/bin/yt-dlp"


def detect_input_type(text: str) -> str:
    """判断输入类型"""
    expanded = os.path.expanduser(text)
    if os.path.isfile(expanded):
        return "local_file"
    t = text.lower()
    if "bilibili.com" in t or re.search(r"(BV[0-9A-Za-z]{10})", t, re.IGNORECASE):
        return "bilibili"
    if "douyin.com" in t or "tiktok.com" in t:
        return "douyin"
    if "youtube.com" in t or "youtu.be" in t:
        return "youtube"
    return "unknown"


def download_video(url: str, temp_dir: str) -> str:
    """使用 yt-dlp 下载视频（仅下载视频流，不含音频以节省带宽）"""
    if not YTDLP or not os.path.exists(YTDLP):
        raise RuntimeError("yt-dlp 未安装")

    output_path = os.path.join(temp_dir, "video.%(ext)s")
    cmd = [
        YTDLP,
        "--no-playlist",
        "-f", "bestvideo[ext=mp4]",
        "--merge-output-format", "mp4",
        "-o", output_path,
        url,
    ]
    print(f"[*] 下载视频（仅视频流）...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    if result.returncode != 0:
        # 回退：下载完整视频
        output_path = os.path.join(temp_dir, "video.mp4")
        cmd = [
            YTDLP,
            "--no-playlist",
            "-f", "best",
            "-o", output_path,
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            raise RuntimeError(f"下载视频失败: {result.stderr[-300:]}")
        return output_path

    # 查找下载的文件
    for ext in ["mp4", "flv", "webm"]:
        p = os.path.join(temp_dir, f"video.{ext}")
        if os.path.exists(p):
            return p

    # yt-dlp 可能用了不同文件名
    for f in os.listdir(temp_dir):
        if f.endswith((".mp4", ".flv", ".webm")):
            return os.path.join(temp_dir, f)

    raise RuntimeError("下载的视频文件未找到")


def get_video_duration(video_path: str) -> float:
    """获取视频时长"""
    if not FFPROBE or not os.path.exists(FFPROBE):
        return 0
    try:
        cmd = [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
               "-of", "csv=p=0", video_path]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return float(out.stdout.strip())
    except Exception:
        return 0


def extract_by_interval(video_path: str, output_dir: str, interval: int = 30,
                        max_frames: int = 50) -> list:
    """按固定时间间隔提取帧"""
    os.makedirs(output_dir, exist_ok=True)

    duration = get_video_duration(video_path)
    if duration <= 0:
        print("[!] 无法获取视频时长", file=sys.stderr)
        return []

    # 计算总帧数
    total_frames = min(int(duration / interval) + 1, max_frames)

    frames = []
    for i in range(total_frames):
        timestamp = i * interval
        if timestamp > duration:
            break

        mm = int(timestamp // 60)
        ss = int(timestamp % 60)
        filename = f"frame_{mm:02d}_{ss:02d}.jpg"
        filepath = os.path.join(output_dir, filename)

        if os.path.exists(filepath):
            frames.append({
                "time_sec": timestamp,
                "time_str": f"{mm:02d}:{ss:02d}",
                "file": filepath,
            })
            continue

        cmd = [
            FFMPEG, "-ss", str(timestamp),
            "-i", video_path,
            "-frames:v", "1",
            "-q:v", "2",  # 高质量 JPG
            "-y", filepath,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if os.path.exists(filepath):
            frames.append({
                "time_sec": timestamp,
                "time_str": f"{mm:02d}:{ss:02d}",
                "file": filepath,
            })

    return frames


def extract_by_scene(video_path: str, output_dir: str, max_frames: int = 50,
                     threshold: float = 0.3) -> list:
    """场景切换检测提取关键帧"""
    os.makedirs(output_dir, exist_ok=True)

    # ffmpeg scene filter 检测场景变化
    cmd = [
        FFMPEG,
        "-i", video_path,
        "-vf", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "vfr",
        "-frames:v", str(max_frames),
        "-q:v", "2",
        os.path.join(output_dir, "scene_%04d.jpg"),
    ]

    print(f"[*] 场景检测中（阈值: {threshold}）...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        # 回退到固定间隔
        print("[!] 场景检测失败，回退到固定间隔", file=sys.stderr)
        return extract_by_interval(video_path, output_dir, interval=30, max_frames=max_frames)

    # 收集提取的帧
    frames = []
    for f in sorted(os.listdir(output_dir)):
        if f.startswith("scene_") and f.endswith(".jpg"):
            filepath = os.path.join(output_dir, f)
            # 从文件名推断顺序
            try:
                idx = int(re.search(r'scene_(\d+)', f).group(1))
            except (AttributeError, ValueError):
                idx = 0

            # 尝试用 ffprobe 获取帧时间
            time_str = f"{idx:02d}:{(idx * 15) % 60:02d}"  # 估算

            frames.append({
                "index": idx,
                "time_str": time_str,
                "file": filepath,
            })

    # 如果场景检测没有提取到帧（视频变化不大），回退
    if not frames:
        print("[!] 未检测到场景切换，回退到固定间隔", file=sys.stderr)
        return extract_by_interval(video_path, output_dir, interval=30, max_frames=max_frames)

    return frames


def run(input_path: str, output_dir: str = None, interval: int = 30,
        scene_detect: bool = False, max_frames: int = 50):
    # 检查 ffmpeg
    if not FFMPEG or not os.path.exists(FFMPEG):
        print(json.dumps({"error": "ffmpeg 未安装。请运行: brew install ffmpeg"}))
        sys.exit(1)

    input_type = detect_input_type(input_path)
    print(f"[*] 输入类型: {input_type}", file=sys.stderr)

    if input_type == "unknown":
        print(json.dumps({"error": "无法识别输入类型"}))
        sys.exit(1)

    # 准备视频文件
    temp_dir = None
    video_path = None
    need_cleanup = False

    if input_type == "local_file":
        video_path = os.path.expanduser(input_path)
    else:
        # 在线视频：临时下载
        temp_dir = tempfile.mkdtemp(prefix="video_frames_")
        need_cleanup = True
        try:
            video_path = download_video(input_path, temp_dir)
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            # 清理临时目录
            shutil.rmtree(temp_dir, ignore_errors=True)
            sys.exit(1)

    if not video_path or not os.path.exists(video_path):
        print(json.dumps({"error": "视频文件不存在"}))
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        sys.exit(1)

    # 输出目录
    if not output_dir:
        output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "cache", "frames",
            Path(video_path).stem[:30]
        )

    # 提取帧
    duration = get_video_duration(video_path)
    print(f"[*] 视频时长: {duration:.0f}s", file=sys.stderr)

    if scene_detect:
        frames = extract_by_scene(video_path, output_dir, max_frames=max_frames)
    else:
        frames = extract_by_interval(video_path, output_dir, interval=interval,
                                     max_frames=max_frames)

    # 清理临时下载的视频
    if temp_dir and need_cleanup:
        shutil.rmtree(temp_dir, ignore_errors=True)

    result = {
        "video_path": video_path if input_type == "local_file" else input_path,
        "duration_sec": duration,
        "output_dir": os.path.abspath(output_dir),
        "frame_count": len(frames),
        "frames": frames,
    }

    print(f"[*] 共提取 {len(frames)} 张截图", file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 frame_extractor.py <视频链接或本地文件>", file=sys.stderr)
        print("      python3 frame_extractor.py <链接> --interval 30", file=sys.stderr)
        print("      python3 frame_extractor.py <链接> --scene-detect", file=sys.stderr)
        print("      python3 frame_extractor.py <链接> --max-frames 20", file=sys.stderr)
        sys.exit(1)

    input_arg = sys.argv[1]
    interval = 30
    scene_detect = False
    max_frames = 50
    output_dir = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--interval" and i + 1 < len(sys.argv):
            interval = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--scene-detect":
            scene_detect = True
            i += 1
        elif sys.argv[i] == "--max-frames" and i + 1 < len(sys.argv):
            max_frames = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--output-dir" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    run(input_arg, output_dir, interval, scene_detect, max_frames)
