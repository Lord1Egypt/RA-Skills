#!/usr/bin/env python3
"""
VAD语音活动检测预处理工具
功能: 检测音频中静音段 → 按自然停顿切分 → 合并成密集chunk → 供whisper转录
"""
import os, re, subprocess, json, math, time

def detect_speech_segments(audio_path: str,
                           min_silence_dur: float = 0.8,
                           noise_thresh: str = "-30dB"):
    """
    用ffmpeg silencedetect检测静音，计算说话段
    返回: [(start_sec, end_sec), ...] 每个说话段的起止
    """
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-af", f"silencedetect=noise={noise_thresh}:d={min_silence_dur}",
        "-f", "null", "-"
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    output = r.stderr  # ffmpeg写stderr
    
    # 解析 silence_start / silence_end
    silences = []  # [(start, end), ...]
    for line in output.split("\n"):
        if "silence_start:" in line:
            s = float(line.split("silence_start:")[1].strip())
            silences.append([s, None])
        elif "silence_end:" in line:
            e = float(line.split("silence_end:")[1].split()[0].strip())
            if silences and silences[-1][1] is None:
                silences[-1][1] = e
    
    # 补全未闭合的沉默段
    for s in silences:
        if s[1] is None:
            s[1] = s[0] + 0.5
    
    # 获取音频总时长
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    dur_r = subprocess.run(dur_cmd, capture_output=True, text=True, timeout=10)
    total_dur = float(dur_r.stdout.strip()) if dur_r.stdout.strip() else 0
    
    # 反转得到说话段
    # 说话段 = 从0到第一个silence_start, silence_end到下一个silence_start, 最后一个silence_end到结束
    segments = []
    prev_end = 0.0
    for s_start, s_end in silences:
        if s_start > prev_end + 0.3:  # 至少0.3s说话才保留
            segments.append([prev_end, s_start])
        prev_end = s_end
    if total_dur > prev_end + 0.3:
        segments.append([prev_end, total_dur])
    
    # 过滤极短段（< 0.5秒的噪声）
    segments = [s for s in segments if s[1] - s[0] >= 0.5]
    
    # 统计
    speech_dur = sum(s[1] - s[0] for s in segments)
    silence_dur = total_dur - speech_dur
    print(f"  VAD检测: {total_dur:.0f}s 音频 → {len(segments)}个说话段")
    print(f"    说话: {speech_dur:.0f}s ({speech_dur/total_dur*100:.0f}%)")
    print(f"    静音: {silence_dur:.0f}s ({silence_dur/total_dur*100:.0f}%)")
    
    return segments


def merge_neighbor_segments(segments: list, max_gap: float = 3.0):
    """合并间隔小于max_gap秒的相邻说话段"""
    if not segments:
        return []
    merged = [segments[0][:]]
    for seg in segments[1:]:
        if seg[0] - merged[-1][1] < max_gap:
            merged[-1][1] = seg[1]
        else:
            merged.append(seg[:])
    print(f"  合并相邻段 (gap<{max_gap}s): {len(segments)} → {len(merged)}")
    return merged


def group_into_batches(segments: list, target_dur: float = 600):
    """
    将说话段分组为batch，每batch总说话时长 ≈ target_dur秒
    返回: [[[s1_start,s1_end], [s2_start,s2_end], ...], ...] 每个batch内的说话段列表
    """
    batches = []
    current = []
    current_dur = 0.0
    
    for seg in segments:
        seg_dur = seg[1] - seg[0]
        if current_dur + seg_dur > target_dur * 1.2 and current:
            batches.append(current)
            current = [seg]
            current_dur = seg_dur
        else:
            current.append(seg)
            current_dur += seg_dur
    
    if current:
        batches.append(current)
    
    print(f"  分组batch (target={target_dur:.0f}s/batch): {len(segments)}段 → {len(batches)}个batch")
    for i, b in enumerate(batches):
        dur = sum(s[1] - s[0] for s in b)
        print(f"    batch{i}: {len(b)}段, 总说话{dur:.0f}s ({dur/60:.1f}min)")
    
    return batches


def extract_batch_audio(audio_path: str, batch: list, output_path: str,
                        pad_s: float = 0.3):
    """
    从原始音频提取一个batch的所有说话段，拼接成一个文件
    段间加pad_s秒静音（避免whisper产生奇怪边界）
    """
    # 生成concat描述文件
    concat_lines = []
    for i, (start, end) in enumerate(batch):
        part_path = f"{output_path}.part{i}.wav"
        dur = end - start
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_path, "-ss", str(start),
            "-t", str(dur), "-ar", "16000", "-ac", "1",
            "-sample_fmt", "s16", part_path
        ], capture_output=True, text=True, timeout=30)
        concat_lines.append(f"file '{part_path}'")
    
    # 生成list文件
    list_path = f"{output_path}.list"
    with open(list_path, "w") as f:
        f.write("\n".join(concat_lines))
    
    # 拼接
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_path, "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1", output_path
    ], capture_output=True, text=True, timeout=60)
    
    # 清理临时文件
    for i in range(len(batch)):
        part_path = f"{output_path}.part{i}.wav"
        if os.path.exists(part_path):
            os.remove(part_path)
    if os.path.exists(list_path):
        os.remove(list_path)


def vad_process(audio_path: str, out_dir: str, target_batch_dur: float = 600):
    """
    完整VAD预处理流程
    返回: [{"path": batch_path, "segments": [...], "speech_dur": s}, ...]
    """
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    
    print(f"[VAD] 静音检测: {audio_path}")
    segments = detect_speech_segments(audio_path)
    
    segments = merge_neighbor_segments(segments)
    batches = group_into_batches(segments, target_batch_dur)
    
    print(f"\n[VAD] 提取batch音频...")
    results = []
    for i, batch in enumerate(batches):
        out = os.path.join(out_dir, f"batch_{i:03d}.wav")
        speech_dur = sum(s[1] - s[0] for s in batch)
        extract_batch_audio(audio_path, batch, out)
        kb = os.path.getsize(out) // 1024 if os.path.exists(out) else 0
        print(f"  batch{i}: {os.path.basename(out)} {kb}KB ({speech_dur:.0f}s说话)")
        results.append({
            "batch_id": i,
            "path": out,
            "segments": batch,
            "speech_dur": speech_dur,
            "num_segments": len(batch),
        })
    
    total_speech = sum(r["speech_dur"] for r in results)
    total_elapsed = time.time() - t0
    print(f"\n[VAD] 完成! {len(batches)}个batch, 总说话{total_speech:.0f}s / {total_speech/60:.1f}min")
    print(f"  VAD处理耗时: {total_elapsed:.0f}s")
    
    return results


if __name__ == "__main__":
    # 测试: 用胖杰克P1
    audio = "/tmp/bili_work/pangjieki_parallel/audio/P01.m4s"
    out = "/tmp/bili_work/vad_test"
    res = vad_process(audio, out, target_batch_dur=600)
