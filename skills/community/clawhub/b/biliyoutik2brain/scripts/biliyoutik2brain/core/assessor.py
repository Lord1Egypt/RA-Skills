"""
BiliYouTik2Brain — 自适应预检系统

三点采样(随机位置) → 质量评分 → 模型选择 → 音频结构地图
"""

import os, json, random, subprocess, re
from typing import Optional, Tuple, List, Dict

from .schemas import AudioResult, RouteDecision


def _sample_audio_segment(
    audio_path: str,
    start_sec: int,
    sample_sec: int = 8,
    output_path: Optional[str] = None
) -> Optional[str]:
    """提取音频片段"""
    if output_path is None:
        import uuid, tempfile
        tmpdir = tempfile.gettempdir()
        output_path = os.path.join(tmpdir, f"sample_{uuid.uuid4().hex[:8]}.wav")
    
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(start_sec), "-t", str(sample_sec),
             "-i", audio_path, "-ac", "1", "-ar", "16000", output_path],
            capture_output=True, timeout=30
        )
        if os.path.exists(output_path) and os.path.getsize(output_path) > 500:
            return output_path
    except Exception:
        pass
    return None


def _test_model(
    sample_path: str,
    duration_s: int,
    model: str,
    cache_dir: Optional[str] = None
) -> Tuple[str, float]:
    """用指定模型快速测试一小段音频的质量
    
    使用 workspace 本地 faster_transcriber 的 detailed 接口，
    获取transcribe文本和平均置信度。
    
    返回: (转录文本, 质量分 0~1)
    """
    import importlib
    ws_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _ft_path = os.path.join(ws_path, "extra", "faster_transcriber.py")
    _spec = importlib.util.spec_from_file_location("_faster_transcriber", _ft_path)
    _ft = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_ft)
    
    try:
        text, low_conf_words, segments = _ft.transcribe_full_audio_detailed(
            sample_path, language="zh", confidence_threshold=0.5
        )
        
        # 平均置信度 = 1 - 低置信词比例
        # segments 可能有、可能无，用总词数估算
        total_words = len(text.split()) if text.strip() else 0
        low_conf_count = len(low_conf_words)
        avg_prob = max(0, 1.0 - (low_conf_count / max(total_words, 1) * 0.5))
        
        # 质量分 = 有内容 (0.4) + 置信度 (0.6)
        has_content = 0.4 if len(text.strip()) > 5 else 0
        quality = has_content + avg_prob * 0.6
        
        return text, min(1.0, quality)
    except Exception as e:
        print(f"  [预检] 转录失败: {e}")
        return "", 0.0


def _has_valid_content(text: str, min_chars: int = 5) -> bool:
    """检查转录文本是否有实际内容"""
    return len(text.strip()) >= min_chars


def _quality_score(text: str) -> float:
    """基于文本内容的质量评分"""
    text = text.strip()
    if not text:
        return 0.0
    return min(1.0, len(text) / 50.0)


def _detect_speech_segments(audio_path: str, duration_s: int) -> List[Dict]:
    """快速静音检测 → 说话段地图
    
    用 ffmpeg silencedetect 找出活跃说话段，
    返回 [{start, end, duration}]，按 start 排序。
    近零开销（<1s for 30min).
    """
    segments = []
    try:
        # 检测 -50dB 以上、持续 0.3s 以上的说话段
        result = subprocess.run(
            ["ffmpeg", "-i", audio_path, "-af",
             "silencedetect=noise=-50dB:d=0.3",
             "-f", "null", "-"],
            capture_output=True, text=True, timeout=30
        )
        stderr = result.stderr
        
        # 解析 silencedetect 输出
        # silence_start: 123.4  → 静音开始
        # silence_end: 125.6 | silence_duration: 2.2  → 静音结束（说话重新开始）
        starts = []
        ends = []
        for line in stderr.split("\n"):
            if "silence_start" in line:
                m = re.search(r"silence_start:\s*([\d.]+)", line)
                if m:
                    starts.append(float(m.group(1)))
            if "silence_end" in line:
                m = re.search(r"silence_end:\s*([\d.]+)", line)
                if m:
                    ends.append(float(m.group(1)))
        
        if not ends and not starts:
            # 没有静音段 → 整段都是说话
            segments.append({"start": 0, "end": duration_s, "duration": duration_s})
        else:
            # 说话段 = 两个静音段之间的区域
            prev_end = 0.0
            for i in range(min(len(ends), len(starts))):
                speech_start = prev_end
                speech_end = starts[i]
                if speech_end - speech_start > 0.5:
                    segments.append({
                        "start": round(speech_start, 1),
                        "end": round(speech_end, 1),
                        "duration": round(speech_end - speech_start, 1),
                    })
                prev_end = ends[i]
            
            # 最后一个说话段
            if prev_end < duration_s:
                segments.append({
                    "start": round(prev_end, 1),
                    "end": duration_s,
                    "duration": round(duration_s - prev_end, 1),
                })
        
        # 过滤掉过短的段落（<2s 可能是误报）
        segments = [s for s in segments if s["duration"] >= 2.0]
        
        if segments:
            print(f"  [静音检测] {len(segments)}个说话段, "
                  f"总说话={sum(s['duration'] for s in segments):.0f}s/{duration_s}s")
        else:
            segments.append({"start": 0, "end": duration_s, "duration": duration_s})
            
    except Exception as e:
        print(f"  [静音检测] 失败, 回退全段: {e}")
        segments.append({"start": 0, "end": duration_s, "duration": duration_s})
    
    return segments


def choose_model(
    audio_path: str,
    duration_s: int,
    cache_dir: Optional[str] = None
) -> Tuple[str, List[Dict]]:
    """自适应模型选择（三点采样只在说话段内，避免静音区无效采样）
    
    Returns:
        (model_name: str, sample_texts: List[Dict])
        sample_texts 每一项: {"pos": int, "text": str, "quality": float}
    """
    sample_texts = []
    
    # 超短视频：直接tiny，无需预检
    if duration_s < 15:
        return "tiny", sample_texts
    
    # 短音频：直接base，无需预检
    if duration_s < 60:
        return "base", sample_texts
    
    # 长音频：先做静音检测找说话段，然后在说话段内采样
    speech_segments = _detect_speech_segments(audio_path, duration_s)
    if not speech_segments:
        return "base", sample_texts
    
    # 在说话段内均匀取3点（有说话内容才值得采样）
    random.seed(hash(audio_path) & 0xffffffff)
    
    # 总说话时长
    total_speech = sum(s["duration"] for s in speech_segments)
    
    # 按说话段时长加权选点
    candidate_ranges = []
    for seg in speech_segments:
        if seg["duration"] >= 5:
            candidate_ranges.append((int(seg["start"]), int(seg["end"])))
    
    if not candidate_ranges:
        return "base", sample_texts
    
    sample_positions = []
    for _ in range(3):
        if not candidate_ranges:
            break
        # 随机选一个段
        chosen = random.choice(candidate_ranges)
        pos = random.randint(chosen[0], max(chosen[0] + 5, chosen[1] - 8))
        sample_positions.append(pos)
    
    sample_positions = sorted(sample_positions)
    
    for pos in sample_positions:
        sample = _sample_audio_segment(audio_path, pos, 8)
        if not sample:
            continue
        
        text, quality = _test_model(sample, 8, "tiny", cache_dir)
        try:
            os.remove(sample)
        except Exception:
            pass
        
        # P1: 收集采样文本供内容预览
        if _has_valid_content(text):
            sample_texts.append({"pos": pos, "text": text, "quality": quality})
        
        if not _has_valid_content(text):
            print(f"  [预检] 采样点 {pos}s: 无内容 (quality={quality:.2f})")
            continue
        
        if _quality_score(text) < 0.3:
            print(f"  [预检] 采样点 {pos}s: 内容稀疏 (quality={quality:.2f})")
            continue
        
        print(f"  [预检] 采样点 {pos}s: 内容可读 (quality={quality:.2f})")
        return "base", sample_texts
    
    # 三点都失败，用base全量试试
    print(f"  [预检] 三点采样均不合格，仍用base全量尝试")
    return "base", sample_texts


def assess_audio(
    audio_path: str,
    duration_s: int,
    cache_dir: Optional[str] = None
) -> dict:
    """完整音频评估（兼顾三点采样和模型选择）
    
    Returns:
        包含 model, sample_texts, speech_segments 等字段的dict
    """
    
    result = {"duration_s": duration_s}
    
    # 静音检测 → 说话段地图（无论长短都做，供P2决策用）
    speech_segments = _detect_speech_segments(audio_path, duration_s)
    result["speech_segments"] = speech_segments
    
    # 模型选择 + 采样文本
    model_name, sample_texts = choose_model(audio_path, duration_s, cache_dir)
    result["model"] = model_name
    result["sample_texts"] = sample_texts
    
    # 基于说话段的内容判断
    total_speech = sum(s["duration"] for s in speech_segments)
    result["has_content"] = total_speech > 10  # 有10s以上说话才算有内容
    result["speech_ratio"] = min(1.0, total_speech / duration_s) if duration_s > 0 else 0
    
    # 平均音质分：取speech_segments内采样点的平均quality
    qualities = [s.get("quality", 0) for s in sample_texts if s.get("quality", 0) > 0]
    result["avg_quality"] = sum(qualities) / len(qualities) if qualities else 0.0
    
    print(f"  [评估] 说话率={result['speech_ratio']:.0%}, "
          f"平均音质={result['avg_quality']:.2f}, "
          f"路由={model_name}")
    
    return result
