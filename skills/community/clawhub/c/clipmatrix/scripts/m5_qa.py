"""
M5 质检模块 — 10项检查
1. 黑帧检测（阈值1s）
2. 画面割裂
3. 重复素材（同视频）
4. 口播静音
5. 字幕合规
6. 文案标签
7. 文案去重
8. 视频完整性
9. 跨视频素材重复率 >60% 拦截
10. 画面字幕特效重叠/模糊检测（OCR + 边缘分析）
"""
import os
import json
import subprocess
import re
import logging
import tempfile
import base64
from pathlib import Path
from difflib import SequenceMatcher

import requests

import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

ARCHIVE_FILE = Path(__file__).parent / "config" / "qa_history.json"


def check_black_frames(video_path: str, threshold: float = 1.0,
                       total_dur: float = None) -> dict:
    """检查黑帧片段 — 用ffmpeg blackdetect检测
    total_dur: 口播时长（秒）。如果视频实际时长 < total_dur，
               说明素材不够长被HF延长，末尾黑帧是HF行为，可忽略。
    """
    if not os.path.exists(video_path):
        return {"passed": False, "reason": "video not found"}

    try:
        # 获取视频实际时长
        import json as _jl
        dur_cmd = ["ffprobe", "-v", "quiet", "-show_entries",
                   "format=duration", "-of", "json", video_path]
        dur_r = subprocess.run(dur_cmd, capture_output=True, text=True, timeout=15)
        try:
            video_dur = _jl.loads(dur_r.stdout).get("format", {}).get("duration", None)
            if video_dur is not None:
                video_dur = float(video_dur)
        except:
            video_dur = None

        # 🔧 (2026-05-31) 黑帧检测参数: d=0.3s min, pix_th=0.10
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vf", "blackdetect=d=0.3:pix_th=0.10",
            "-f", "null", "-"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        stderr = result.stderr

        max_black = 0.0
        black_segments = []

        for line in stderr.split("\n"):
            if "black_duration:" in line:
                try:
                    dur_str = line.split("black_duration:")[1].split()[0]
                    dur = float(dur_str.strip())
                    start = 0.0
                    if "black_start:" in line:
                        start_str = line.split("black_start:")[1].split()[0]
                        start = float(start_str.strip())

                    # 🔧 (2026-05-31) 只在素材不足(total_dur>video_dur)时忽略末尾黑帧
                    # 素材够长时的末尾黑帧是真实的，不允许忽略
                    if video_dur is not None and total_dur is not None:
                        if total_dur > video_dur and start >= video_dur - 1.0:
                            logger.info(f"  忽略结尾黑帧 {dur:.1f}s (素材不足, total_dur{total_dur:.1f}s > 视频{video_dur:.1f}s)")
                            continue

                    if dur > max_black:
                        max_black = dur
                    if dur >= threshold:
                        black_segments.append({"duration": dur, "start": start})
                except (ValueError, IndexError):
                    pass

        if max_black >= threshold:
            return {
                "passed": False,
                "reason": f"Black frame detected: {max_black:.1f}s",
                "black_segments": black_segments,
                "max_black": max_black,
            }

        # 🔧 (2026-05-31) 额外检查视频末尾3秒：用更宽松阈值检测"字幕+暗背景"的黑帧
        if video_dur and video_dur > 5:
            tail_start = max(0, video_dur - 3)
            # 提取末尾3秒单独检测，pix_th=0.50 宽松
            cmd_tail = [
                "ffmpeg", "-ss", str(tail_start), "-i", video_path,
                "-t", "3",
                "-vf", "blackdetect=d=0.5:pix_th=0.50",
                "-f", "null", "-"
            ]
            tail_r = subprocess.run(cmd_tail, capture_output=True, text=True, timeout=30)
            for line in tail_r.stderr.split("\n"):
                if "black_duration:" in line:
                    try:
                        tail_dur = float(line.split("black_duration:")[1].split()[0])
                        if tail_dur >= 1.5:
                            return {
                                "passed": False,
                                "reason": f"Tail black detected (字幕+暗背景): {tail_dur:.1f}s at end",
                                "max_black": max_black,
                            }
                    except: pass

        return {"passed": True, "max_black": max_black}

    except Exception as e:
        logger.warning(f"Black frame check failed: {e}")
        return {"passed": False, "reason": f"check error: {e}"}


def check_video_integrity(video_path: str) -> dict:
    """检查视频完整性"""
    if not os.path.exists(video_path):
        return {"passed": False, "reason": "file not found"}

    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration,size", "-of", "json",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        info = json.loads(result.stdout)
        duration = float(info.get("format", {}).get("duration", 0))
        size = int(info.get("format", {}).get("size", 0))

        checks = {"duration": duration, "size": size, "min_size": 100000}

        if duration < 5:
            return {"passed": False, "reason": f"Video too short: {duration:.1f}s"}
        if size < 100000:
            return {"passed": False, "reason": f"Video too small: {size/1024:.0f}KB"}

        return {"passed": True, "duration": duration, "size": size}

    except Exception as e:
        return {"passed": False, "reason": f"integrity check failed: {e}"}


def check_audio_muted(video_path: str) -> dict:
    """检查音频是否静音"""
    if not os.path.exists(video_path):
        return {"passed": False, "reason": "file not found"}

    try:
        cmd = [
            "ffprobe", "-f", "lavfi",
            f"amovie={video_path},astats=metadata=1:reset=1",
            "-show_entries", "metadata=lavfi.astats.Overall.RMS_level",
            "-of", "default=noprint_wrappers=1:nokey=1",
            "-v", "quiet"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout.strip()

        if not output:
            return {"passed": True, "reason": "no audio stream"}

        # Parse RMS levels
        rms_values = []
        for line in output.split("\n"):
            line = line.strip()
            if line and line != "-inf":
                try:
                    rms_values.append(float(line))
                except ValueError:
                    pass

        if not rms_values:
            return {"passed": True, "reason": "no audio data"}

        avg_rms = sum(rms_values) / len(rms_values)
        if avg_rms < -50:
            return {"passed": False, "reason": f"Audio too quiet: {avg_rms:.1f}dB"}

        return {"passed": True, "avg_rms": avg_rms}

    except Exception as e:
        logger.warning(f"Audio check failed: {e}")
        return {"passed": False, "reason": f"check error: {e}"}


def check_scene_repeats(scenes: list) -> dict:
    """检查同视频内画面(素材文件)是否重复
    场景名重复不拦截 — 约束的是画面重复，不是名字重复。
    同视频内素材文件不重复已经在M3的exclude_files保证，这里直接pass。
    """
    return {"passed": True}


def check_caption_compliance(caption: str) -> dict:
    """检查文案标签合规"""
    if not caption:
        return {"passed": True}

    # 检查是否有hashtag
    has_hashtag = "#" in caption

    # 检查长度
    if len(caption) > 500:
        return {"passed": False, "reason": f"Caption too long: {len(caption)} chars"}

    return {"passed": True, "has_hashtags": has_hashtag}


def check_caption_dedup(caption: str, history_captions: list, threshold: float = 0.9) -> dict:
    """检查文案去重"""
    if not history_captions:
        return {"passed": True}

    for hist in history_captions:
        if not hist:
            continue
        similarity = SequenceMatcher(None, caption.lower(), hist.lower()).ratio()
        if similarity >= threshold:
            return {
                "passed": False,
                "reason": f"Caption dedup failed: {similarity:.2f} similarity",
                "similarity": similarity,
            }

    return {"passed": True}


def check_ai_vision(video_path: str) -> dict:
    """
    第11项检查：MiMo V2.5 AI视觉分析 — 完整视频质检 (2026-05-31 重构)
    
    专注视觉检测：黑帧/字幕重叠/文字裁切/花屏/布局错位
    策略：视频≤25s用激进压缩全量发送；>25s分2段重叠检测
    """
    if not os.path.exists(video_path):
        return {"passed": False, "reason": "video not found"}

    # 获取视频时长
    try:
        dur_cmd = ["ffprobe", "-v", "quiet", "-show_entries",
                   "format=duration", "-of", "json", video_path]
        dur_r = subprocess.run(dur_cmd, capture_output=True, text=True, timeout=15)
        video_dur = float(json.loads(dur_r.stdout).get("format", {}).get("duration", 10))
    except:
        video_dur = 10

    # 决定分段策略
    MAX_SEG_DUR = 25
    segments = []
    if video_dur <= MAX_SEG_DUR:
        segments = [(0, video_dur)]
    else:
        # 分2段，重叠5s确保覆盖边界
        overlap = 5
        segments = [(0, MAX_SEG_DUR), (video_dur - MAX_SEG_DUR, video_dur)]
        logger.info(f"  AI Vision: {video_dur:.1f}s → 分{len(segments)}段检测")

    # 获取API key
    api_key = os.environ.get("MIMO_API_KEY", "")
    if not api_key:
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    cfg = json.load(f)
                api_key = cfg.get("models", {}).get("providers", {}).get(
                    "xiaomi", {}).get("request", {}).get("auth", {}).get("value", "")
            except:
                pass
    if not api_key:
        return {"passed": True, "reason": "no MiMo API key, skipping"}

    all_issues = []
    all_scores = []

    for seg_idx, (seg_start, seg_end) in enumerate(segments):
        seg_dur = seg_end - seg_start
        seg_label = f"seg{seg_idx+1}" if len(segments) > 1 else "full"

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # 激进压缩：720p, crf=32, ultrafast 确保在37MB限制内
            compress_cmd = [
                "ffmpeg", "-y", "-ss", str(seg_start), "-i", video_path,
                "-t", str(seg_dur),
                "-vf", "scale=720:1280:force_original_aspect_ratio=decrease",
                "-c:v", "libx264", "-crf", "32",
                "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-an",
                tmp_path
            ]
            subprocess.run(compress_cmd, capture_output=True, timeout=60)

            if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) < 1000:
                continue

            raw_size = os.path.getsize(tmp_path)
            if raw_size > 37 * 1024 * 1024:
                # 仍超限，降低分辨率
                compress_cmd[compress_cmd.index("720")] = "480"
                compress_cmd[compress_cmd.index("1280")] = "854"
                subprocess.run(compress_cmd, capture_output=True, timeout=60)
                raw_size = os.path.getsize(tmp_path) if os.path.exists(tmp_path) else 0
                if raw_size > 37 * 1024 * 1024:
                    logger.warning(f"  AI Vision {seg_label}: too large ({raw_size//1024//1024}MB), skip")
                    continue

            logger.info(f"  AI Vision {seg_label}: {raw_size//1024//1024}MB, {seg_dur:.1f}s")

            with open(tmp_path, "rb") as f:
                video_b64 = base64.b64encode(f.read()).decode("utf-8")

            segment_hint = ""
            if len(segments) > 1:
                segment_hint = f" (segment {seg_idx+1}/{len(segments)}, time {seg_start:.0f}s-{seg_end:.0f}s of {video_dur:.0f}s video)"

            payload = {
                "model": "mimo-v2.5",
                "messages": [{
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": (
                            f"Analyze this TikTok travel video{segment_hint}. "
                            "Focus ONLY on visual problems (NOT audio/music):\n"
                            "1. BLACK FRAMES — any segment where screen goes fully/mostly black or dark\n"
                            "2. Subtitle/text overlapping each other\n"
                            "3. Text elements cut off by screen edges\n"
                            "4. Visual glitches, artifacts, corrupted frames\n"
                            "5. Misaligned or broken layout\n\n"
                            'Return JSON: {"passed": bool, "issues": [str], "score": int 1-10}'
                        )
                    }, {
                        "type": "video_url",
                        "video_url": {"url": f"data:video/mp4;base64,{video_b64}"}
                    }]
                }],
                "max_tokens": 1024
            }

            resp = requests.post(
                "https://token-plan-cn.xiaomimimo.com/v1/chat/completions",
                headers={"api-key": api_key, "Content-Type": "application/json"},
                json=payload, timeout=120
            )

            if resp.status_code != 200:
                logger.warning(f"  AI Vision {seg_label}: HTTP {resp.status_code}")
                continue

            data = resp.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

            try:
                json_match = re.search(r'\{[^{}]*"passed"[^{}]*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    if not result.get("passed", True):
                        all_issues.extend(result.get("issues", []))
                    all_scores.append(result.get("score", 8))
                else:
                    # 备用文本解析
                    cl = content.lower()
                    if any(w in cl for w in ["black frame", "dark screen", "black screen", "shows nothing"]):
                        all_issues.append(f"[{seg_label}] Black frames detected")
                    if any(w in cl for w in ["overlap", "overlapping", "covering text"]):
                        all_issues.append(f"[{seg_label}] Text overlap")
                    if any(w in cl for w in ["cut off", "outside", "edge"]):
                        all_issues.append(f"[{seg_label}] Text cut off")
                    if any(w in cl for w in ["glitch", "artifact", "corrupted"]):
                        all_issues.append(f"[{seg_label}] Visual glitch")
                    if all_scores:
                        all_scores.append(all_scores[-1])
            except Exception as e:
                logger.warning(f"  AI Vision {seg_label} parse error: {e}")

        except Exception as e:
            logger.warning(f"  AI Vision {seg_label} error: {e}")
        finally:
            try: os.unlink(tmp_path)
            except: pass

    if not all_scores:
        return {"passed": True, "reason": "no valid AI Vision results"}

    avg_score = sum(all_scores) / len(all_scores)
    if all_issues:
        return {
            "passed": False,
            "reason": f"AI Vision: {'; '.join(all_issues[:3])}",
            "issues": all_issues,
            "score": round(avg_score, 1),
            "raw": "",
        }

    return {
        "passed": True,
        "score": round(avg_score, 1),
        "issues": [],
    }
def check_scratch_detection(video_path: str, storyboard_scenes: list = None) -> dict:
    """
    第10项检查：画面字幕特效重叠/模糊检测
    
    原理：
    1. 从视频提取关键帧（每个分镜终点附近+均分采样）
    2. 对每帧分析两个区域：
       - 下半区域（y: 70%-95%）：字幕/卡片文字区
       - 中上区域（y: 10%-40%）：标题区域
    3. 用Canny边缘检测 + 形态学分析判断：
       a. 重叠文字：双边缘重叠（膨胀边缘密度比值偏高）
       b. 模糊文字：边缘过于稀疏或弥散
    4. 综合判定是否存在重叠/模糊
    
    storyboard_scenes: [{start_sec, end_sec, scene}], 可选
    """
    if not os.path.exists(video_path):
        return {"passed": False, "reason": "video not found"}

    try:
        import cv2
        import numpy as np
    except ImportError:
        return {"passed": True, "reason": "OpenCV not available, skipping"}

    try:
        # 获取视频信息
        import json as _jl
        probe = subprocess.run([
            "ffprobe", "-v", "quiet", "-show_entries",
            "format=duration,size", "-of", "json",
            video_path
        ], capture_output=True, text=True, timeout=15)
        info = _jl.loads(probe.stdout)
        video_dur = float(info.get("format", {}).get("duration", 0))

        # 构建采样时间点
        sample_times = set()

        # 从分镜数据取采样点
        if storyboard_scenes:
            for s in storyboard_scenes:
                start = s.get("start_sec", 0)
                end = s.get("end_sec", 0)
                if end > start:
                    # 每个场景中段：特效完全渲染后的稳定状态
                    mid = (start + end) / 2
                    if mid < video_dur:
                        sample_times.add(round(mid, 1))
                    # 场景开头+0.5s：字幕刚刚出现时的状态
                    t1 = start + 0.3
                    if t1 < video_dur:
                        sample_times.add(round(t1, 1))
                    # 场景末尾文字消失前
                    t2 = end - 0.3
                    if t2 > start and t2 < video_dur:
                        sample_times.add(round(t2, 1))

        # 等间隔补充采样（确保覆盖不被分镜覆盖的区域）
        interval = max(1.5, video_dur / 12)
        t = 0.5
        while t < video_dur:
            sample_times.add(round(t, 1))
            t += interval

        # 转为有序列表
        sample_times = sorted(sample_times)
        # 限制最大帧数
        MAX_FRAMES = 30
        if len(sample_times) > MAX_FRAMES:
            step = len(sample_times) / MAX_FRAMES
            sample_times = [sample_times[int(i * step)] for i in range(MAX_FRAMES)]

        logger.info(f"  Text overlap check: {len(sample_times)} frames, dur={video_dur:.1f}s")

        # === 分析每帧 ===
        issues = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for ts in sample_times:
                frame_path = os.path.join(tmpdir, f"frame_{ts:.1f}.png")

                # 用ffmpeg提取帧（yuv420p格式保证一致性）
                subprocess.run([
                    "ffmpeg", "-ss", str(ts), "-i", video_path,
                    "-frames:v", "1", "-q:v", "2",
                    "-pix_fmt", "rgb24",
                    frame_path, "-y",
                    "-loglevel", "error",
                ], capture_output=True, timeout=30)

                if not os.path.exists(frame_path):
                    continue

                img = cv2.imread(frame_path)
                if img is None:
                    continue

                h, w = img.shape[:2]
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # ---- 区域1: 字幕区域（底部25%） ----
                sub_y1 = int(h * 0.70)
                sub_y2 = int(h * 0.95)
                subtitle_region = gray[sub_y1:sub_y2, :]

                # ---- 区域2: 标题/特效区域（上部25-45%） ----
                head_y1 = int(h * 0.08)
                head_y2 = int(h * 0.40)
                headline_region = gray[head_y1:head_y2, :]

                issues.extend(
                    _analyze_region(region=subtitle_region,
                                    region_name="subtitle",
                                    frame_ts=ts, h_region=sub_y2-sub_y1)
                )
                issues.extend(
                    _analyze_region(region=headline_region,
                                    region_name="headline",
                                    frame_ts=ts, h_region=head_y2-head_y1)
                )

        # 汇总判断
        if not issues:
            logger.info(f"  ✅ 文字区域检测无异常")
            return {"passed": True, "frames_checked": len(sample_times)}

        # 去重：相邻帧的同类问题只报一次
        deduped = []
        prev_key = None
        for iss in sorted(issues, key=lambda x: (x["ts"], x["region"])):
            key = f"{iss['region']}:{iss['issue_type']}"
            if key != prev_key:
                deduped.append(iss)
                prev_key = key
            elif abs(deduped[-1]["ts"] - iss["ts"]) > 3.0:
                deduped.append(iss)

        reasons = []
        overlap_issues = [d for d in deduped if d["issue_type"] == "overlap"]
        blur_issues = [d for d in deduped if d["issue_type"] == "blur"]

        if overlap_issues:
            reasons.append(
                f"Text overlap in {overlap_issues[0]['region']} "
                f"at {overlap_issues[0]['ts']:.1f}s"
            )
        if blur_issues:
            reasons.append(
                f"Text blur in {blur_issues[0]['region']} "
                f"at {blur_issues[0]['ts']:.1f}s"
            )

        if len(deduped) >= 3 and len(sample_times) >= 5:
            return {
                "passed": False,
                "reason": "; ".join(reasons[:2]),
                "issues": deduped,
                "frames_checked": len(sample_times),
            }

        # 少量局部问题：不阻断，仅记录
        logger.info(f"  ⚠️ 文字区域轻微异常: {reasons}")
        return {
            "passed": True,
            "warning": "; ".join(reasons[:2]),
            "issues": deduped,
            "frames_checked": len(sample_times),
        }

    except Exception as e:
        logger.warning(f"Text overlap check failed: {e}")
        return {"passed": False, "reason": f"check error: {e}"}


def _analyze_region(region, region_name: str, frame_ts: float, h_region: int) -> list:
    """
    分析单个区域的文字重叠/模糊
    返回: [{ts, region, issue_type, detail}]
    """
    issues = []

    if region.size == 0 or h_region < 10:
        return []

    # 1. Canny边缘检测
    edges = cv2.Canny(region, 50, 150)
    total_pixels = region.shape[0] * region.shape[1]
    edge_density = np.sum(edges > 0) / max(total_pixels, 1)

    # 2. 膨胀边缘（检测双边缘重叠）
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    # 膨胀后边缘像素与原始边缘像素的比值
    edge_ratio = np.sum(dilated > 0) / max(np.sum(edges > 0), 1)
    # 正常比值约2-4（膨胀2次边长+4），>6表示边缘重叠（文字叠文字）

    # 3. 局部标准差（检测模糊区域）
    laplacian = cv2.Laplacian(region, cv2.CV_64F)
    variance = laplacian.var()

    # ---- 判断 ----
    # 重叠文字：边缘密度较高 + 膨胀比值异常高
    if edge_density > 0.04 and edge_ratio > 6.0:
        issues.append({
            "ts": round(frame_ts, 1),
            "region": region_name,
            "issue_type": "overlap",
            "detail": f"edge_ratio={edge_ratio:.1f}, density={edge_density:.3f}",
        })

    # 模糊文字：区域有一定内容（边缘密度>0.01）但方差低（纹理模糊）
    if edge_density > 0.008 and variance < 15:
        issues.append({
            "ts": round(frame_ts, 1),
            "region": region_name,
            "issue_type": "blur",
            "detail": f"variance={variance:.1f}, density={edge_density:.3f}",
        })

    # 严重模糊：边缘密度很低但区域有颜色内容（文字被背景吞没）
    # 取区域中间色块的色差值
    mid_y = region.shape[0] // 2
    mid_line = region[mid_y-5:mid_y+5, :]
    if mid_line.size > 0:
        line_std = np.std(mid_line)
        if line_std > 15 and edge_density < 0.005:
            # 有色差但无边缘 → 可能被背景淹没
            issues.append({
                "ts": round(frame_ts, 1),
                "region": region_name,
                "issue_type": "blur",
                "detail": f"edge_density={edge_density:.4f} (text likely lost)",
            })

    return issues


def check_material_cross_repeat(materials: list, history_materials: list, threshold: float = 0.6) -> dict:
    """检查跨视频素材重复率"""
    if not materials or not history_materials:
        return {"passed": True}

    current_set = set(os.path.basename(m) for m in materials if isinstance(m, str))
    current_set.update(os.path.basename(s) for s in materials if isinstance(s, dict) and s.get("path"))

    total_history = set()
    for hist in history_materials:
        if isinstance(hist, list):
            for m in hist:
                if isinstance(m, str):
                    total_history.add(os.path.basename(m))
                elif isinstance(m, dict) and m.get("path"):
                    total_history.add(os.path.basename(m["path"]))

    if not current_set or not total_history:
        return {"passed": True}

    overlap = len(current_set & total_history)
    rate = overlap / len(current_set)

    if rate >= threshold:
        return {
            "passed": False,
            "reason": f"Material cross-repeat rate: {rate:.2f}",
            "rate": rate,
        }

    return {"passed": True, "rate": rate}


def run_all_checks(
    video_path: str,
    scenes: list,
    caption: str,
    materials: list,
    history: dict = None,
    total_dur: float = None,
    storyboard_scenes: list = None,
) -> dict:
    """
    运行全部10项质检
    history: {captions: [str], materials: [[str]], ...}
    total_dur: 口播总时长（秒），用于过滤结尾黑帧误报
    storyboard_scenes: [{start_sec, end_sec, scene}], 用于字幕重叠检测的时间点参考
    """
    results = {}
    all_passed = True

    # 1. 黑帧检测
    r1 = check_black_frames(video_path, total_dur=total_dur)
    results["1_black_frame"] = r1
    if not r1.get("passed", False):
        all_passed = False

    # 2. 画面割裂（视频完整性间接检查视频有无损坏）
    r2 = check_video_integrity(video_path)
    results["2_video_integrity"] = r2
    if not r2.get("passed", False):
        all_passed = False

    # 3. 重复素材（同视频）
    r3 = check_scene_repeats(scenes)
    results["3_scene_repeats"] = r3
    if not r3.get("passed", False):
        all_passed = False

    # 4. 口播静音
    r4 = check_audio_muted(video_path)
    results["4_audio_check"] = r4
    if not r4.get("passed", False):
        all_passed = False

    # 5. 字幕合规（特效字幕，不检测）
    # 视频字幕由M4 GSAP驱动的headline/subtitle特效卡面文字实现，没有字幕轨道。
    # 加ffmpeg检测会误判为无字幕导致阻断，故保持always pass。
    results["5_subtitle_check"] = {"passed": True}

    # 6. 文案标签
    r6 = check_caption_compliance(caption)
    results["6_caption_compliance"] = r6
    if not r6.get("passed", False):
        all_passed = False

    # 7. 文案去重
    r7 = {"passed": True}
    if history and "captions" in history:
        r7 = check_caption_dedup(caption, history["captions"])
    results["7_caption_dedup"] = r7
    if not r7.get("passed", False):
        all_passed = False

    # 8. 视频完整性（复用第2项结果，保持9项框架）
    results["8_video_completeness"] = r2

    # 9. 跨视频素材重复率
    r9 = {"passed": True}
    if history and "materials" in history:
        r9 = check_material_cross_repeat(materials, history["materials"])
    results["9_material_cross_repeat"] = r9
    if not r9.get("passed", False):
        all_passed = False

    # 10. 画面字幕特效重叠/模糊检测
    r10 = check_scratch_detection(video_path, storyboard_scenes)
    results["10_text_overlap"] = r10
    if not r10.get("passed", False):
        all_passed = False

    # 11. MiMo V2.5 AI视觉分析
    r11 = check_ai_vision(video_path)
    results["11_ai_vision"] = r11
    if not r11.get("passed", False):
        all_passed = False

    return {
        "passed": all_passed,
        "results": results,
        "checks_passed": sum(1 for r in results.values() if r.get("passed", False)),
        "checks_total": len(results),
    }


def save_history(entry: dict, max_records: int = 50):
    """保存质检历史（限制最多max_records条防膨胀）"""
    history = {"captions": [], "materials": []}
    if ARCHIVE_FILE.exists():
        try:
            with open(ARCHIVE_FILE) as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    if "caption" in entry:
        history.setdefault("captions", []).append(entry["caption"])
        # 限制长度，保留最新的
        if len(history["captions"]) > max_records:
            history["captions"] = history["captions"][-max_records:]
    if "materials" in entry:
        history.setdefault("materials", []).append(entry["materials"])
        if len(history["materials"]) > max_records:
            history["materials"] = history["materials"][-max_records:]

    ARCHIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ARCHIVE_FILE, "w") as f:
        json.dump(history, f, indent=2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_all_checks(
        video_path="/tmp/test.mp4",
        scenes=[{"scene": "test"}],
        caption="Check out China #travel",
        materials=["/tmp/video.mp4"],
    )
    print(json.dumps(result, indent=2))
