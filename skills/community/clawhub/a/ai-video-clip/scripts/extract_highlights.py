#!/usr/bin/env python3
"""Extract Highlights — 视频精华片段提取 (v2: 音频能量+语义双维度)"""
import argparse, os, subprocess, shutil, sys, json
from datetime import datetime

def get_video_info(input_file: str) -> dict:
    """使用 ffprobe 获取视频信息。"""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", input_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {}
    try:
        data = json.loads(result.stdout)
        duration = float(data.get("format", {}).get("duration", 0))
        width = height = 0
        for s in data.get("streams", []):
            if s.get("codec_type") == "video":
                width = s.get("width", 0)
                height = s.get("height", 0)
                break
        return {"duration": duration, "width": width, "height": height}
    except:
        return {}

def detect_scenes(input_file: str, threshold: float = 30.0) -> list:
    """使用 FFmpeg scene detection 检测场景切换点。"""
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-vf", f"select='gt(scene,{1/threshold})',showinfo",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    scenes = []
    for line in result.stderr.splitlines():
        if "pts_time" in line:
            try:
                ts = line.split("pts_time:")[1].split()[0]
                scenes.append(float(ts))
            except:
                pass
    return scenes

def detect_audio_energy(input_file: str, window_size: float = 1.0) -> list:
    """使用 FFmpeg 检测音频能量峰值。返回 [(timestamp, energy_db), ...]"""
    cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-af", f"astats=metadata=1:reset=1",
        "-vn", "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    energy_peaks = []
    for line in result.stderr.splitlines():
        if "RMS" in line and "dB" in line:
            try:
                parts = line.split()
                for j, p in enumerate(parts):
                    if p == "RMS" and j + 1 < len(parts):
                        db_str = parts[j + 1].replace("dB", "").strip()
                        db_val = float(db_str)
                        # 归一化: 假设 -60dB 最低，0dB 最高
                        normalized = min(1.0, max(0.0, (db_val + 60) / 60))
                        energy_peaks.append(normalized)
                        break
            except (IndexError, ValueError):
                pass
    return energy_peaks


def score_clip(start: float, duration: float, scenes: list, energy: list,
               transcript: dict = None, info: dict = None) -> float:
    """综合评分: 场景切换权重 * 0.3 + 音频能量权重 * 0.3 + 语义权重 * 0.4"""
    score = 0.0
    total_dur = info.get("duration", 0) if info else 0

    # 场景评分: 越接近场景切换点分越高
    nearest_scene_dist = min((abs(s - start) for s in scenes), default=duration)
    score += 0.3 * max(0, 1 - nearest_scene_dist / (duration * 2))

    # 能量评分: 取片段内平均能量
    if energy and total_dur > 0:
        idx_start = int(start / total_dur * len(energy))
        idx_end = int((start + duration) / total_dur * len(energy))
        if idx_end > idx_start:
            clip_energy = sum(energy[idx_start:idx_end]) / (idx_end - idx_start)
            score += 0.3 * clip_energy

    # 语义评分: transcripts 中的高信息密度句
    if transcript:
        phrases = transcript.get("phrases", [])
        match_count = 0
        for ph in phrases:
            ph_mid = (ph.get("start", 0) + ph.get("end", 0)) / 2
            if start <= ph_mid <= start + duration:
                match_count += 1
        score += 0.4 * min(1.0, match_count / 10)

    return score


def extract_clip(input_file: str, start: float, duration: float, output: str) -> bool:
    cmd = [
        "ffmpeg", "-y", "-ss", str(start), "-i", input_file,
        "-t", str(duration), "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-avoid_negative_ts", "make_zero", output
    ]
    return subprocess.run(cmd, capture_output=True).returncode == 0

def extract_highlights(input_file: str, num_clips: int, min_duration: float,
                       output_dir: str, transcript: dict = None,
                       method: str = "hybrid") -> list:
    """综合维度高光提取。

    method:
      - "scene": 纯场景检测 (传统)
      - "audio": 纯音频能量
      - "hybrid": 场景 + 音频 + 语义 (推荐)
    """
    os.makedirs(output_dir, exist_ok=True)
    info = get_video_info(input_file)
    duration = info.get("duration", 0)
    print(f"视频时长: {duration:.1f}s, 分辨率: {info.get('width',0)}x{info.get('height',0)}")
    print(f"提取模式: {method}")

    # 检测场景切换点
    print("检测场景切换点...")
    scenes = detect_scenes(input_file)
    print(f"发现 {len(scenes)} 个场景切换点")

    # 检测音频能量
    energy = []
    if method in ("audio", "hybrid"):
        print("检测音频能量...")
        energy = detect_audio_energy(input_file)
        print(f"音频分析: {len(energy)} 窗口")

    if not scenes:
        scenes = [i * duration / (num_clips + 1) for i in range(1, num_clips + 1)]

    # 过滤距离太近的候选起点
    filtered = []
    last = -999
    for s in scenes:
        if s - last >= min_duration:
            filtered.append(s)
            last = s

    # 在候选点上按评分排序选最佳
    if method in ("audio", "hybrid") and len(filtered) > num_clips:
        print(f"从 {len(filtered)} 个候选点中综合评选 top-{num_clips}...")
        scored = []
        for s in filtered:
            sc = score_clip(s, min_duration, scenes, energy, transcript, info)
            scored.append((s, sc))
        scored.sort(key=lambda x: x[1], reverse=True)
        clips = [s for s, _ in scored[:num_clips]]
    else:
        clips = filtered[:num_clips]

    base = os.path.splitext(os.path.basename(input_file))[0]
    results = []
    for i, start in enumerate(clips):
        out = os.path.join(output_dir, f"{base}_highlight{i+1}.mp4")
        ok = extract_clip(input_file, start, min_duration, out)
        results.append((out, start, ok))
        print(f"  片段{i+1}: {start:.1f}s (评分:{score_clip(start, min_duration, scenes, energy, transcript, info):.2f}) -> {out} [{'OK' if ok else 'FAIL'}]")
    return results

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="视频精华片段提取 (v2: 双维度)")
    p.add_argument("--input", required=True)
    p.add_argument("--num-clips", type=int, default=3, help="提取片段数量")
    p.add_argument("--min-duration", type=float, default=30, help="每个片段最小秒数")
    p.add_argument("--output", required=True, help="输出目录")
    p.add_argument("--threshold", type=float, default=30.0, help="场景检测灵敏度(越高越灵敏)")
    p.add_argument("--transcript", default=None, help="transcript JSON (语义增强)")
    p.add_argument("--method", default="hybrid",
                   choices=["scene", "audio", "hybrid"],
                   help="提取方法: scene=纯场景, audio=纯音频, hybrid=综合")
    args = p.parse_args()

    if not shutil.which("ffmpeg"):
        print("错误: ffmpeg 未安装", file=sys.stderr)
        sys.exit(1)

    transcript = None
    if args.transcript and os.path.exists(args.transcript):
        with open(args.transcript, "r", encoding="utf-8") as f:
            transcript = json.load(f)
        print(f"已加载转录: {len(transcript.get('phrases', []))} phrases")

    print(f"从 {args.input} 提取 {args.num_clips} 个精华片段...")
    results = extract_highlights(args.input, args.num_clips,
                                  args.min_duration, args.output,
                                  transcript=transcript,
                                  method=args.method)
    ok = sum(1 for r in results if r[2])
    print(f"\n完成: {ok}/{len(results)} 成功")
