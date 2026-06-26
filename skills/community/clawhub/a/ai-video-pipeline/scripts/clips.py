"""即梦AI视频片段生成 — 变速适配 + 超2x自动拆分 (v16)"""
import os
import math
import subprocess
import cv2
from jimeng_video import JimengVideo
from compose import best_frames


def _get_clip_duration(clip_path):
    """获取视频文件实际时长（秒）"""
    cap = cv2.VideoCapture(clip_path)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frames / fps if fps > 0 else None


def _adjust_speed(clip_path, target_dur, verbose=False):
    """用 ffmpeg 调整 clip 播放速度以匹配目标时长"""
    actual_dur = _get_clip_duration(clip_path)
    if actual_dur is None or abs(actual_dur - target_dur) < 0.15:
        return

    factor = target_dur / actual_dur  # >1 减慢, <1 加快
    tmp_path = clip_path.replace('.mp4', '_speed.mp4')
    cmd = [
        'ffmpeg', '-y', '-i', clip_path,
        '-filter:v', f'setpts={factor:.4f}*PTS',
        '-r', '24', '-an',
        tmp_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode == 0 and os.path.exists(tmp_path):
        os.replace(tmp_path, clip_path)
        if verbose:
            print(f"    ⏩ 变速 {actual_dur:.1f}s → {target_dur:.1f}s ({factor:.2f}x)")
    else:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        if verbose:
            print(f"    ⚠️ 变速失败: {result.stderr[-100:]}")


def generate_video_clips(work_dir, clip_configs, subs, verbose=True,
                         max_speed_ratio=2.0):
    """
    使用即梦AI生成短视频片段，变速适配段落时长。

    - 速度比 ≤ max_speed_ratio: ffmpeg 变速（减慢/加快）
    - 速度比 > max_speed_ratio: 自动拆分为多段，每段 ≤ max_speed_ratio

    Returns:
        [(clip_path, start_time, end_time), ...]
    """
    ak = os.environ.get("VOLC_ACCESS_KEY_ID", "")
    sk = os.environ.get("VOLC_SECRET_KEY", "")
    if not ak or not sk:
        if verbose:
            print("  ⚠️ VOLC_ACCESS_KEY_ID/VOLC_SECRET_KEY 未设置，跳过即梦AI视频生成")
        return []

    jv = JimengVideo(ak, sk)
    clips = []

    for i, config in enumerate(clip_configs):
        prompt = config.get("prompt", "")
        mode = config.get("mode", "t2v_720p")
        after_para = config.get("after_paragraph", 0)

        # 计算时间段
        if after_para > 0 and after_para <= len(subs):
            start_time = subs[after_para - 1]["end"]
            end_para = min(after_para + 1, len(subs))
            end_time = subs[end_para - 1]["end"]
        elif i < len(subs):
            start_time = subs[i]["start"]
            end_time = subs[i]["end"]
        else:
            start_time = 0
            end_time = 5.0

        target_dur = end_time - start_time
        frames = best_frames(target_dur)
        clip_gen_dur = frames / 24  # 即梦AI实际生成的时长

        # 判断是否需要拆分
        speed_ratio = target_dur / clip_gen_dur if clip_gen_dur > 0 else 999

        if speed_ratio <= max_speed_ratio:
            # 单段 + 变速
            _generate_single_clip(jv, work_dir, i, prompt, mode, frames,
                                  start_time, end_time, clips, verbose)
        else:
            # 拆分为多段
            n_splits = math.ceil(speed_ratio / max_speed_ratio)
            seg_dur = target_dur / n_splits
            if verbose:
                print(f"  🔀 片段 {i+1} 速度比 {speed_ratio:.1f}x > {max_speed_ratio}x，拆分为 {n_splits} 段")
            for j in range(n_splits):
                seg_start = start_time + j * seg_dur
                seg_end = seg_start + seg_dur
                seg_frames = best_frames(seg_dur)
                _generate_single_clip(jv, work_dir, i, prompt, mode, seg_frames,
                                      seg_start, seg_end, clips, verbose,
                                      sub_index=j)

    if verbose and clips:
        print(f"  ✅ 成功生成 {len(clips)} 个视频片段")
    return clips


def _generate_single_clip(jv, work_dir, idx, prompt, mode, frames,
                          start_time, end_time, clips, verbose,
                          sub_index=None):
    """生成单个 clip 并变速适配"""
    suffix = f"_{sub_index+1}" if sub_index is not None else ""
    clip_path = os.path.join(work_dir, f"clip_{idx+1}{suffix}.mp4")
    target_dur = end_time - start_time

    if os.path.exists(clip_path):
        if verbose:
            label = f"{idx+1}{suffix}" if suffix else str(idx+1)
            print(f"  📹 片段 {label} 已存在，跳过")
        clips.append((clip_path, start_time, end_time))
        return

    if verbose:
        label = f"{idx+1}{suffix}" if suffix else str(idx+1)
        actual_dur = frames / 24
        speed_ratio = target_dur / actual_dur if actual_dur > 0 else 0
        print(f"  📹 生成片段 {label}: {prompt[:30]}... "
              f"({actual_dur:.1f}s → {target_dur:.1f}s, {speed_ratio:.2f}x)")

    try:
        jv.generate(prompt, clip_path, mode=mode, frames=frames,
                    aspect_ratio="16:9", timeout=300, verbose=verbose)
        # 变速适配
        _adjust_speed(clip_path, target_dur, verbose=verbose)
        clips.append((clip_path, start_time, end_time))
    except Exception as e:
        if verbose:
            print(f"  ⚠️ 片段生成失败: {e}")
