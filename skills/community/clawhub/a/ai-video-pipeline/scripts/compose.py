"""视频合成: 流式帧读取 + frame_map 方案 (v16 - 变速适配 + 720P默认)"""
import os
import numpy as np
import cv2
from PIL import Image
from typing import List, Tuple, Optional
from moviepy import AudioFileClip, VideoClip


def best_frames(duration: float, fps: int = 24) -> int:
    """返回 ≥ ceil(duration*fps) 的最小有效帧数 (即梦AI: frames%24==1, 121~241)"""
    import math
    needed = math.ceil(duration * fps)
    k = (needed - 1 + 23) // 24
    frames = 24 * k + 1
    return max(121, min(241, frames))


class StreamClipReader:
    """流式读取视频片段帧，LRU 缓存最近使用的帧避免重复解码"""

    def __init__(self, clip_path: str, target_size: Tuple[int, int] = (1920, 1080)):
        self.cap = cv2.VideoCapture(clip_path)
        self.target_w, self.target_h = target_size
        self._total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._cache: dict[int, np.ndarray] = {}
        self._max_cache = 60

    def read_frame(self, idx: int) -> Optional[np.ndarray]:
        if idx < 0 or idx >= self._total_frames:
            return None
        if idx in self._cache:
            return self._cache[idx]
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, bgr = self.cap.read()
        if not ret:
            return None
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        h, w = rgb.shape[:2]
        if h != self.target_h or w != self.target_w:
            rgb = cv2.resize(rgb, (self.target_w, self.target_h))
        if len(self._cache) >= self._max_cache:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        self._cache[idx] = rgb
        return rgb

    @property
    def total_frames(self) -> int:
        return self._total_frames

    def close(self):
        self.cap.release()
        self._cache.clear()


def compose(work_dir, audio_path, subs, output_path,
            width=1280, height=720, fps=24, bg_color=(12, 12, 29),
            font_path=None, font_size=44, y_ratio=0.85, max_chars=20,
            video_clips=None, mixed_audio_path=None, verbose=True):
    """
    视频合成 v16: 流式帧读取 + LRU缓存 + frame_map + 字幕叠加
    内存优化: 默认 720P，不再预提取所有帧，按需流式读取
    """
    from subtitle import prerender_subtitles

    actual_audio = mixed_audio_path or audio_path
    audio = AudioFileClip(actual_audio)
    total_dur = subs[-1]["end"] if subs else audio.duration
    video_clips = video_clips or []

    if verbose:
        print(f"  音频: {audio.duration:.1f}s, 总时长: {total_dur:.1f}s")
        print(f"  字幕: {len(subs)}段, 视频片段: {len(video_clips)}个")

    # 预渲染字幕
    if verbose: print("  预渲染字幕帧...")
    text_overlays = prerender_subtitles(subs, width, height, font_path, font_size, y_ratio, max_chars)

    # 计算每个 clip 的时间范围
    clip_ranges = []
    for i in range(len(video_clips)):
        cs = 0.0 if i == 0 else clip_ranges[i - 1][1]
        if i < len(video_clips) - 1:
            ce = video_clips[i + 1][1]
        else:
            ce = subs[-1]["end"]
        clip_ranges.append((cs, ce))

    # 打开视频流式读取器
    readers: List[Optional[StreamClipReader]] = []
    for i, (clip_path, _, _) in enumerate(video_clips):
        if not os.path.exists(clip_path):
            readers.append(None)
            if verbose: print(f"    ⚠️ 片段 {i+1} 不存在")
            continue
        reader = StreamClipReader(clip_path, (width, height))
        readers.append(reader)
        if verbose:
            print(f"    片段 {i+1}: {reader.total_frames}帧 "
                  f"({clip_ranges[i][0]:.1f}s - {clip_ranges[i][1]:.1f}s)")

    # 构建 frame_map (只存索引，不存实际帧)
    total_output_frames = int(total_dur * fps) + 1
    frame_map: List[Tuple[int, int]] = []
    for fi in range(total_output_frames):
        t = fi / fps
        mapped = False
        for ci in range(len(video_clips)):
            if readers[ci] is None: continue
            cs, ce = clip_ranges[ci]
            if cs <= t <= ce:
                local_fi = int((t - cs) * fps)
                local_fi = max(0, min(local_fi, readers[ci].total_frames - 1))
                frame_map.append((ci, local_fi))
                mapped = True
                break
        if not mapped:
            fallback_ci = -1
            for ci in range(len(readers) - 1, -1, -1):
                if readers[ci] is not None:
                    fallback_ci = ci
                    break
            if fallback_ci >= 0:
                frame_map.append((fallback_ci, readers[fallback_ci].total_frames - 1))
            else:
                frame_map.append((-1, -1))

    if verbose:
        print(f"  frame_map: {len(frame_map)} 帧, {len(video_clips)} 个 clip")

    # make_frame: 流式读取
    target_size = (width, height)

    def make_frame(t):
        fi = min(int(t * fps), len(frame_map) - 1)
        fi = max(fi, 0)
        ci, local_fi = frame_map[fi]

        if ci >= 0 and readers[ci] is not None:
            frame = readers[ci].read_frame(local_fi)
            if frame is not None:
                frame = frame.copy()
            else:
                frame = np.full((height, width, 3), bg_color, dtype=np.uint8)
        else:
            frame = np.full((height, width, 3), bg_color, dtype=np.uint8)

        # 安全: 确保 frame 是 uint8 且尺寸正确
        if frame.dtype != np.uint8:
            frame = frame.astype(np.uint8)
        if frame.shape[0] != height or frame.shape[1] != width:
            frame = cv2.resize(frame, (width, height))

        # 字幕叠加
        current_sub = None
        for s in subs:
            if s["start"] <= t <= s["end"]:
                current_sub = s
                break

        if current_sub:
            text_key = current_sub["text"]
            if text_key in text_overlays:
                overlay = text_overlays[text_key]
                try:
                    if overlay.size == target_size:
                        frame_pil = Image.fromarray(frame).convert('RGBA')
                        frame_pil = Image.alpha_composite(frame_pil, overlay)
                        frame = np.array(frame_pil.convert('RGB'))
                except Exception:
                    pass  # 字幕叠加失败时静默跳过

        return frame

    # 合成
    if verbose: print(f"  合成中 ({total_dur:.1f}s, {fps}fps)...")
    video = VideoClip(make_frame, duration=total_dur)
    final = video.with_audio(audio)
    final.write_videofile(output_path, fps=fps, codec="libx264",
                          audio_codec="aac", audio_bitrate="192k",
                          preset="fast", threads=4, logger="bar" if verbose else None)
    audio.close()

    # 关闭所有读取器
    for r in readers:
        if r: r.close()

    size_kb = os.path.getsize(output_path) // 1024
    if verbose: print(f"✅ 视频: {output_path} ({size_kb}KB, {total_dur:.1f}s)")
