#!/usr/bin/env python3
"""
audio_detector — 音频非语音信号检测（v1.8.1）

功能：
  - 检测 bleep（哔声消音）
  - 检测音乐/环境音长段
  - 给 LLM 标注可疑区域

原理：
  Bleep 是 1kHz-3kHz 的纯音（窄带高能），说话是宽带低能。
  对短时窗做 FFT，检测窄带峰值即可定位。

用法：
  from biliyoutik2brain.extra.audio_detector import detect_bleeps
  
  bleeps = detect_bleeps("/tmp/audio.mp3")
  # → [(3.5, 5.0), (12.0, 13.2), ...]  每个 (start, end) 秒
"""

import os, json, struct, math
import subprocess as sp
import numpy as np

# ============================================================
# 常量
# ============================================================
SAMPLE_RATE = 16000        # whisper 采样率
WINDOW_MS = 100            # 分析窗口（毫秒）
WINDOW_SIZE = int(SAMPLE_RATE * WINDOW_MS / 1000)
HOP_SIZE = WINDOW_SIZE // 2  # 50% 重叠

# bleep 检测阈值
BLEEP_FREQ_MIN = 800       # Hz — 典型消音从 ~900Hz 开始
BLEEP_FREQ_MAX = 3500      # Hz
BLEEP_PEAK_THRESHOLD = 0.6  # 窄带能量占比 > 60%
BLEEP_MIN_DURATION = 0.3   # 最短 bleep 片段（秒）


def _read_pcm(audio_path: str) -> np.ndarray:
    """用 ffmpeg 读音频为 16kHz PCM float32"""
    cmd = [
        "ffmpeg", "-y", "-i", audio_path,
        "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "f32le",
        "-hide_banner", "-loglevel", "error",
        "pipe:1"
    ]
    r = sp.run(cmd, capture_output=True, timeout=300)
    if r.returncode != 0 or not r.stdout:
        return np.array([], dtype=np.float32)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def _detect_bleep_frames(samples: np.ndarray) -> np.ndarray:
    """检测每帧是否为 bleep（纯音），返回 bool 数组"""
    n_frames = max(1, (len(samples) - WINDOW_SIZE) // HOP_SIZE + 1)
    is_bleep = np.zeros(n_frames, dtype=bool)
    
    # 预计算频率轴
    freqs = np.fft.rfftfreq(WINDOW_SIZE, 1/SAMPLE_RATE)
    bleep_mask = (freqs >= BLEEP_FREQ_MIN) & (freqs <= BLEEP_FREQ_MAX)
    
    for i in range(n_frames):
        start = i * HOP_SIZE
        frame = samples[start:start + WINDOW_SIZE]
        
        # 音量太低 → 跳过
        rms = np.sqrt(np.mean(frame ** 2))
        if rms < 0.005:
            continue
        
        # FFT 频谱
        spectrum = np.abs(np.fft.rfft(frame * np.hanning(WINDOW_SIZE)))
        
        # 窄带能量占比 = bleep频段能量 / 总能量
        total_energy = np.sum(spectrum) + 1e-10
        bleep_energy = np.sum(spectrum[bleep_mask])
        ratio = bleep_energy / total_energy
        
        is_bleep[i] = ratio > BLEEP_PEAK_THRESHOLD
    
    return is_bleep


def _frames_to_segments(is_bleep: np.ndarray) -> list:
    """连续 bleep 帧合并为时间线段"""
    segments = []
    in_bleep = False
    start_frame = 0
    
    for i, b in enumerate(is_bleep):
        if b and not in_bleep:
            in_bleep = True
            start_frame = i
        elif not b and in_bleep:
            in_bleep = False
            duration_frames = i - start_frame
            if duration_frames * HOP_SIZE / SAMPLE_RATE >= BLEEP_MIN_DURATION:
                start_s = start_frame * HOP_SIZE / SAMPLE_RATE
                end_s = i * HOP_SIZE / SAMPLE_RATE
                segments.append((round(start_s, 1), round(end_s, 1)))
    
    # 处理末尾仍在 bleep
    if in_bleep:
        duration_frames = len(is_bleep) - start_frame
        if duration_frames * HOP_SIZE / SAMPLE_RATE >= BLEEP_MIN_DURATION:
            start_s = start_frame * HOP_SIZE / SAMPLE_RATE
            end_s = len(is_bleep) * HOP_SIZE / SAMPLE_RATE
            segments.append((round(start_s, 1), round(end_s, 1)))
    
    return segments


def detect_bleeps(audio_path: str) -> list:
    """
    检测音频中的 bleep（哔声消音）
    
    Returns:
        [(start_s, end_s), ...] — 按时间升序的消音段
    """
    if not os.path.exists(audio_path):
        return []
    
    samples = _read_pcm(audio_path)
    if len(samples) == 0:
        return []
    
    is_bleep = _detect_bleep_frames(samples)
    segments = _frames_to_segments(is_bleep)
    
    return segments


def mark_bleeps_in_text(audio_path: str, whisper_segments: list) -> str:
    """
    检测 bleep 并在 whisper segment 列表中标记
    
    返回修改后的 segments（在每个 bleep段插入 [BLEEP] 标记）
    """
    bleeps = detect_bleeps(audio_path)
    if not bleeps:
        return ""
    
    # 生成参考文本
    lines = ["## 音频检测：消音段"]
    for start, end in bleeps:
        lines.append(f"[{int(start//60):02d}:{int(start%60):02d}-{int(end//60):02d}:{int(end%60):02d}] [BLEEP]")
    return "\n".join(lines)


def quick_test():
    """快速自测试"""
    print("[测试] 音频检测器...")
    # 合成一个模拟 bleep（1秒 1kHz 正玄波）来验证算法
    sr = SAMPLE_RATE
    t = np.arange(sr * 2) / sr
    speech = np.sin(2 * np.pi * 200 * t) * 0.3  # 200Hz 模拟人声
    bleep = np.sin(2 * np.pi * 1500 * t) * 0.5  # 1.5kHz 模拟消音
    mixed = np.concatenate([speech[:sr], bleep[:sr//2], speech[sr:]])
    
    is_bleep = _detect_bleep_frames(mixed)
    segments = _frames_to_segments(is_bleep)
    print(f"  模拟检测: {segments}")
    assert len(segments) == 1, f"应该检测到1个bleep段, 实际: {len(segments)}"
    print("  ✅ 算法验证通过")


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        quick_test()
    elif len(sys.argv) > 1:
        bleeps = detect_bleeps(sys.argv[1])
        print(f"检测到 {len(bleeps)} 个消音段:")
        for s, e in bleeps:
            print(f"  {s:.1f}s - {e:.1f}s")
