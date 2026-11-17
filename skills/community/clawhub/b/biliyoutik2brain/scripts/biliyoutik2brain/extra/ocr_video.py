"""
OCR 视频画面文字 — 辅助语音转录纠错（零安装，使用系统 tesseract）
v2.1: 精准打击版 — 只在低置信词的时间窗口抽帧OCR，不做全视频扫描
"""

import subprocess, os, re, json, tempfile, shutil, sys
from typing import List, Optional, Dict, Tuple

# ── 跨平台 Tesseract 自动检测 ──
def _detect_tesseract() -> str:
    """多级检测 tesseract 路径：环境变量 → 平台候选路径 → PATH → 字面量兜底"""
    # 1. 环境变量（最高优先级）
    env_cmd = os.environ.get("TESSERACT_CMD", "")
    if env_cmd and (os.path.exists(env_cmd) or shutil.which(env_cmd)):
        return env_cmd
    # 2. 平台候选安装路径
    if sys.platform == "win32":
        candidates = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
    elif sys.platform == "darwin":
        candidates = [
            "/opt/homebrew/bin/tesseract",
            "/usr/local/bin/tesseract",
        ]
    else:
        candidates = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract",
        ]
    for p in candidates:
        if os.path.exists(p):
            return p
    # 3. PATH 搜索
    found = shutil.which("tesseract") or shutil.which("tesseract.exe")
    if found:
        return found
    # 4. 兜底（保留可读错误信息）
    return "tesseract"

tesseract_cmd = _detect_tesseract()
TMP_DIR = os.path.join(tempfile.gettempdir(), "bili_ocr")
PERSISTENCE_CHECK_FRAMES = 5  # 检查持久文字时的抽帧数


def _run_tesseract(image_path: str) -> str:
    """对单张图片运行 tesseract OCR，返回纯文本"""
    try:
        r = subprocess.run(
            [tesseract_cmd, image_path, "stdout", "-l", "chi_sim+eng", "--psm", "6"],
            capture_output=True, text=True, timeout=30
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception as e:
        print(f"  ⚠️ OCR失败: {e}")
        return ""


def _extract_frame(video_path: str, timestamp_s: float, output_path: str) -> bool:
    """ffmpeg 抽取指定时间戳的视频帧"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        r = subprocess.run(
            ["ffmpeg", "-ss", str(timestamp_s), "-i", video_path,
             "-vframes", "1", "-q:v", "2", "-y", output_path],
            capture_output=True, text=True, timeout=30
        )
        return r.returncode == 0 and os.path.exists(output_path)
    except Exception as e:
        print(f"  ⚠️ 抽帧失败 @{timestamp_s}s: {e}")
        return False


def _is_valid_ocr_line(line: str) -> bool:
    """判断单行OCR结果是否有效：≥2中文字符且中文占比≥60%"""
    line = re.sub(r'\s+', '', line).strip()
    if len(line) < 3:
        return False
    cn_count = sum(1 for c in line if '\u4e00' <= c <= '\u9fff')
    if cn_count < 2 or cn_count / max(len(line), 1) < 0.6:
        return False
    punct = sum(1 for c in line if c in '—|:;[]{}<>«»·•,./?\\\'\"')
    if punct / max(len(line), 1) > 0.4:
        return False
    return True


def _get_duration(video_path: str) -> float:
    """ffprobe 获取视频时长（秒）"""
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
             video_path],
            capture_output=True, text=True, timeout=15
        )
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def ocr_video(video_path: str, num_frames: int = 6, duration_s: Optional[float] = None) -> str:
    """(v1 兼容) — delegate to v2.1"""
    result = ocr_video_targeted(video_path, timestamps=[])
    all_lines = list(result.get("persistent", []))
    for entry in result.get("timeline", []):
        for line in entry.get("text", "").split("\n"):
            line = line.strip()
            if line and line not in all_lines:
                all_lines.append(line)
    return "\n".join(all_lines)


def _detect_persistent_text(video_path: str, duration_s: float) -> List[str]:
    """
    快速检测全视频持久文字：抽头/中/尾 5帧 → OCR → 在所有帧中出现≥60%的文字
    耗时：~3s（5帧抽帧+OCR）
    """
    if duration_s < 10:
        timestamps = [duration_s / 2]
    else:
        # 头/中/尾 5帧均匀分布
        timestamps = []
        for i in range(PERSISTENCE_CHECK_FRAMES):
            ts = duration_s * (i + 1) / (PERSISTENCE_CHECK_FRAMES + 1)
            timestamps.append(ts)

    results_per_frame = []
    for ts in timestamps:
        out_path = os.path.join(TMP_DIR, f"_persist_{len(results_per_frame):02d}.png")
        ok = _extract_frame(video_path, ts, out_path)
        if not ok:
            continue
        ocr_raw = _run_tesseract(out_path)
        try:
            os.remove(out_path)
        except OSError:
            pass

        frame_lines = []
        if ocr_raw:
            for line in ocr_raw.split("\n"):
                line_clean = re.sub(r'\s+', '', line).strip()
                if _is_valid_ocr_line(line_clean):
                    frame_lines.append(line_clean)
        results_per_frame.append(frame_lines)

    if not results_per_frame:
        return []

    # 统计每条文字的出现次数
    line_count: Dict[str, int] = {}
    for frame in results_per_frame:
        seen_this_frame = set()
        for line in frame:
            cn_only = re.sub(r'[^\u4e00-\u9fff]', '', line)
            if cn_only not in seen_this_frame:
                seen_this_frame.add(cn_only)
                line_count[cn_only] = line_count.get(cn_only, 0) + 1

    total_frames = len(results_per_frame)
    threshold = max(1, int(total_frames * 0.6))
    persistent = sorted([
        text for text, count in line_count.items()
        if count >= threshold
    ])

    return persistent


def ocr_at_timestamps(
    video_path: str,
    timestamps: List[float],
    window_pad: float = 1.0,
) -> List[Dict]:
    """
    在指定时间戳精准抽帧+OCR

    Args:
        video_path: 视频文件路径
        timestamps: 需要OCR的时间戳列表（秒）
        window_pad: 每个时间戳前后放宽秒数

    Returns:
        [{"timestamp": 12.0, "text": "行文字"}, ...]
        每个时间戳独立返回（去重后）
    """
    if not os.path.exists(video_path) or not timestamps:
        return []

    os.makedirs(TMP_DIR, exist_ok=True)

    # 生成实际抽帧时间点：每个低置信词时间戳 ± window_pad 的范围采 2 帧
    actual_snapshots = []
    for ts in timestamps:
        if window_pad <= 0:
            actual_snapshots.append(round(ts, 1))
        else:
            actual_snapshots.append(round(max(0, ts - window_pad), 1))
            if window_pad > 0.1:
                actual_snapshots.append(round(ts + window_pad, 1))

    # 去重+排序
    actual_snapshots = sorted(set(actual_snapshots))

    results = []
    for i, ts in enumerate(actual_snapshots):
        out_path = os.path.join(TMP_DIR, f"_target_{i:04d}.png")
        ok = _extract_frame(video_path, ts, out_path)
        if not ok:
            continue
        ocr_raw = _run_tesseract(out_path)
        try:
            os.remove(out_path)
        except OSError:
            pass

        if not ocr_raw:
            continue

        valid_lines = []
        for line in ocr_raw.split("\n"):
            line_clean = re.sub(r'\s+', '', line).strip()
            if _is_valid_ocr_line(line_clean):
                valid_lines.append(line_clean)

        if valid_lines:
            # 合并同帧文字，去重
            unique_lines = list(dict.fromkeys(valid_lines))
            results.append({
                "timestamp": ts,
                "text": "\n".join(unique_lines),
            })

    return results


def ocr_video_targeted(
    video_path: str,
    timestamps: Optional[List[float]] = None,
    duration_s: Optional[float] = None,
    window_pad: float = 1.0,
) -> Dict:
    """
    精准OCR：只对指定时间戳抽帧 + 快速检测持久文字

    Args:
        video_path: 视频文件路径
        timestamps: 需要OCR的精准时间戳（来自低置信词的segment时间）
        duration_s: 视频时长（自动获取）
        window_pad: 每个时间戳前后放宽秒数

    Returns:
        {
            "persistent": ["line1", ...],  # 头中尾5帧检测得到的全视频固定文字
            "timeline": [{"timestamp":, "text":}, ...],  # 目标时间戳的OCR结果
            "duration_s": 172.0,
        }
    """
    if not os.path.exists(video_path):
        return {"persistent": [], "timeline": [], "duration_s": 0}

    if not duration_s:
        duration_s = _get_duration(video_path)
    if duration_s <= 0:
        return {"persistent": [], "timeline": [], "duration_s": 0}

    # Step 1: 快速检测持久文字（头中尾5帧，~3s）
    persistent = _detect_persistent_text(video_path, duration_s)

    # Step 2: 只在低置信词的时间窗口精准OCR
    timeline = []
    if timestamps:
        timeline = ocr_at_timestamps(video_path, timestamps, window_pad=window_pad)

    if persistent:
        print(f"  [OCR] 持久文字 {len(persistent)}条: {persistent}")
    if timeline:
        print(f"  [OCR] 精准抽帧 {len(timeline)}帧 (目标{len(timestamps)}个时间戳)")

    return {
        "persistent": persistent,
        "timeline": timeline,
        "duration_s": duration_s,
    }


def ocr_video_timeline(
    video_path: str,
    interval_s: float = 5.0,
    num_frames: Optional[int] = None,
    duration_s: Optional[float] = None
) -> Dict:
    """
    (v2.0 兼容) — delegate to v2.1 targeted approach
    如果传了 timestamps 就精准打击，否则用 interval_s 但只抽均匀帧
    """
    return ocr_video_targeted(video_path, timestamps=[], interval_s=interval_s, duration_s=duration_s)


def cleanup():
    """清理临时帧文件"""
    if os.path.isdir(TMP_DIR):
        for f in os.listdir(TMP_DIR):
            if f.startswith("_persist_") or f.startswith("_target_") or f.startswith("frame_"):
                try:
                    os.remove(os.path.join(TMP_DIR, f))
                except OSError:
                    pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 ocr_video.py <video.mp4> [t1,t2,t3...]")
        sys.exit(1)
    video = sys.argv[1]
    if len(sys.argv) > 2:
        timestamps = [float(x) for x in sys.argv[2].split(",")]
    else:
        timestamps = []
    result = ocr_video_targeted(video, timestamps=timestamps)
    print(f"\n=== 持久文字 === ({len(result['persistent'])}条)")
    for line in result['persistent']:
        print(f"  [{line}]")
    print(f"\n=== 目标OCR === ({len(result['timeline'])}帧)")
    for entry in result['timeline'][:10]:
        print(f"  @{entry['timestamp']:5.1f}s: [{entry['text'][:60]}]")
    if len(result['timeline']) > 10:
        print(f"  ... +{len(result['timeline'])-10}")
    cleanup()
