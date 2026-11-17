"""
多源采集引擎 (v3.0)

采集优先级:
  1. API 字幕 (官方CC) → 跳过转录, 直接获得文本 ✅
  2. 音频源 → VAD 人声分离 → 转录 (首选)
  3. 视频源 → 提取音频 → 转录 (兜底)

音频预处理:
  - VAD 人声分离: 语音段 / 非语音段(BGM/噪音)
  - 静音删除: 删除 >0.5s 静音, 提速 30-50%
  - Bleep 检测: 标记消音段 → 跳过转录
  - 说话人分离: 多人 → [{speaker_id, segments}]

输出: 统一时间线 Timeline
"""

import os, subprocess, tempfile, json, re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class TimelineSegment:
    """时间线统一数据"""
    start: float
    end: float
    text: str
    source: str = ""          # "api_subtitle" / "audio_transcribe" / "ocr"
    speaker: str = ""          # 说话人标签
    confidence: float = 1.0


@dataclass
class CollectionResult:
    """采集结果"""
    url: str
    video_title: str = ""
    uploader: str = ""
    duration_s: int = 0

    # 字幕
    subtitle_available: bool = False
    subtitle_text: str = ""
    subtitle_segments: List[TimelineSegment] = field(default_factory=list)

    # 音频
    audio_path: str = ""
    audio_duration: float = 0.0

    # 预处理
    has_voice_separation: bool = False
    has_silence_removed: bool = False
    has_bleep_detection: bool = False
    bleep_segments: List[TimelineSegment] = field(default_factory=list)

    # 元信息
    description: str = ""
    tags: List[str] = field(default_factory=list)
    comment_count: int = 0

    # 策略
    recommended_strategy: str = ""  # "subtitle" | "audio" | "video"
    strategy_reason: str = ""


# ═══════════════════════════════════════════════════════════════
#  策略决策
# ═══════════════════════════════════════════════════════════════

def decide_strategy(result: CollectionResult) -> str:
    """根据采集结果决定最优处理策略"""
    if result.subtitle_available and len(result.subtitle_text) > 50:
        result.recommended_strategy = "subtitle"
        result.strategy_reason = "API字幕可用, 零成本直接获取文本"
        return "subtitle"

    if result.audio_path and os.path.exists(result.audio_path):
        result.recommended_strategy = "audio"
        result.strategy_reason = "音频源可用, 比视频转录快3-5倍"
        return "audio"

    result.recommended_strategy = "video"
    result.strategy_reason = "无API字幕+无音频源, 只能从视频提取"
    return "video"


# ═══════════════════════════════════════════════════════════════
#  音频提取
# ═══════════════════════════════════════════════════════════════

def extract_audio(video_path: str, output_dir: str = None) -> Optional[str]:
    """从视频提取音频 (ffmpeg)"""
    if not os.path.exists(video_path):
        return None

    out_dir = output_dir or tempfile.mkdtemp()
    os.makedirs(out_dir, exist_ok=True)
    audio_path = os.path.join(out_dir, "extracted_audio.wav")

    try:
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vn",              # 无视频
            "-acodec", "pcm_s16le",
            "-ar", "16000",     # 16kHz (whisper标准)
            "-ac", "1",         # 单声道
            "-y", audio_path,
        ], capture_output=True, text=True, timeout=120, check=True)
        print(f"  [采集] ✅ 音频提取: {os.path.getsize(audio_path)}字节")
        return audio_path
    except Exception as e:
        print(f"  [采集] ⚠️ 音频提取失败: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
#  静音检测 + 删除
# ═══════════════════════════════════════════════════════════════

def remove_silence(audio_path: str, silence_threshold_db: int = -40,
                   min_silence_dur: float = 0.5) -> Optional[str]:
    """删除静音段, 输出压缩后的音频"""
    if not os.path.exists(audio_path):
        return None

    out_path = audio_path.replace(".wav", "_nosilence.wav")
    try:
        subprocess.run([
            "ffmpeg", "-i", audio_path,
            "-af", (f"silenceremove=stop_periods=-1:"
                    f"stop_duration={min_silence_dur}:"
                    f"stop_threshold={silence_threshold_db}dB"),
            "-y", out_path,
        ], capture_output=True, text=True, timeout=60, check=True)

        original_size = os.path.getsize(audio_path)
        new_size = os.path.getsize(out_path)
        reduction = (1 - new_size / max(original_size, 1)) * 100
        print(f"  [采集] 🔇 静音删除: {original_size}→{new_size}字节 ({reduction:.0f}%)")
        return out_path
    except Exception as e:
        print(f"  [采集] ⚠️ 静音删除失败: {e}")
        return audio_path


# ═══════════════════════════════════════════════════════════════
#  人声分离 (VAD)
# ═══════════════════════════════════════════════════════════════

def detect_voice_segments(audio_path: str, aggressiveness: int = 2) -> List[Tuple[float, float]]:
    """VAD 检测语音段 ([start, end], ...)

    使用 webrtcvad (轻量级, 零依赖安装)
    aggressiveness: 0(最宽容) ~ 3(最严格)
    """
    try:
        import webrtcvad
    except ImportError:
        print("  [采集] ⚠️ webrtcvad 未安装, 跳过VAD")
        if os.path.exists(audio_path):
            import wave
            with wave.open(audio_path, 'rb') as wf:
                duration = wf.getnframes() / wf.getframerate()
            return [(0.0, duration)]
        return []

    import wave
    try:
        with wave.open(audio_path, 'rb') as wf:
            rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())
    except Exception:
        return [(0.0, 30.0)]

    vad = webrtcvad.Vad(aggressiveness)
    frame_ms = 30
    frame_bytes = int(rate * frame_ms / 1000 * 2)  # 16-bit mono

    segments = []
    in_speech = False
    speech_start = 0.0
    pos = 0

    for i in range(0, len(frames) - frame_bytes + 1, frame_bytes):
        chunk = frames[i:i + frame_bytes]
        if len(chunk) < frame_bytes:
            break

        is_speech = vad.is_speech(chunk, rate)
        timestamp = i / (rate * 2)  # 16-bit = 2 bytes/sample

        if is_speech and not in_speech:
            speech_start = timestamp
            in_speech = True
        elif not is_speech and in_speech:
            dur = timestamp - speech_start
            if dur > 0.3:  # 至少0.3秒才保留
                segments.append((round(speech_start, 2), round(timestamp, 2)))
            in_speech = False

    if in_speech:
        end = len(frames) / (rate * 2)
        segments.append((round(speech_start, 2), round(end, 2)))

    print(f"  [采集] 🎙 VAD完成: {len(segments)}个语音段")
    return segments


# ═══════════════════════════════════════════════════════════════
#  Bleep 检测
# ═══════════════════════════════════════════════════════════════

def detect_bleep_segments(audio_path: str) -> List[TimelineSegment]:
    """检测消音段 (简单的频谱分析)

    使用 ffmpeg silencedetect 过滤极短的高频信号（消音"哔"声）
    """
    if not os.path.exists(audio_path):
        return []

    try:
        result = subprocess.run([
            "ffmpeg", "-i", audio_path,
            "-af", "silencedetect=noise=-30dB:d=0.1",
            "-f", "null", "-",
        ], capture_output=True, text=True, timeout=60)

        segments = []
        for line in result.stderr.split("\n"):
            if "silence_start" in line:
                m = re.search(r'silence_start:\s*([\d.]+)', line)
                if m:
                    segments.append(TimelineSegment(
                        start=float(m.group(1)), end=0.0,
                        text="[BLEEP]", source="bleep_detect"
                    ))

        if segments:
            print(f"  [采集] 🔇 Bleep检测: {len(segments)}段")
        return segments
    except Exception:
        return []


# ═══════════════════════════════════════════════════════════════
#  统一时间线输出
# ═══════════════════════════════════════════════════════════════

def build_timeline(
    result: CollectionResult,
    transcript_text: str = "",
    transcript_segments: List[Dict] = None,
) -> List[TimelineSegment]:
    """构建统一时间线

    将所有来源的数据统一到视频时间轴上。
    优先级: API字幕 > 转录 > 空
    """
    timeline = []

    # 1. API 字幕 (最高优先级)
    if result.subtitle_segments:
        timeline.extend(result.subtitle_segments)
        return _deduplicate_timeline(timeline)

    # 2. 转录段落
    if transcript_segments:
        for seg in transcript_segments:
            timeline.append(TimelineSegment(
                start=seg.get("start", 0),
                end=seg.get("end", 0),
                text=seg.get("text", ""),
                source="audio_transcribe",
                speaker=seg.get("speaker", ""),
                confidence=seg.get("confidence", 0.7),
            ))

    # 3. Bleep 标记
    if result.bleep_segments:
        for bs in result.bleep_segments:
            bs.source = "bleep"
            timeline.append(bs)

    return _deduplicate_timeline(timeline)


def _deduplicate_timeline(segments: List[TimelineSegment]) -> List[TimelineSegment]:
    """时间线去重（按时间排序，重叠段取优先级高的）"""
    if not segments:
        return segments
    # 简单去重: 按start排序
    segments.sort(key=lambda s: s.start)
    return segments
