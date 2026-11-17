"""
两条腿帧采样器 v2 — 场景检测 + 字幕时间轴驱动 + teaching_patterns 类型化
=====================================================================
v2 核心改进：
  1. 不做固定位置分区——用音频转录交叉验证来判断字幕位置（调查一次，全局复用）
  2. 不做关键词列表——用 teaching_patterns 类型驱动采样策略
  3. 不做全帧 OCR——用 PySceneDetect 画面差异检测找到"教学内容变化"时刻
  
采样策略（三层）：
  L1 基础采样: 字幕段切换时，每个场景截 1-3 帧（三等分）
  L2 加密采样: teaching_patterns 指示型 UP 主 + 指代型语句 → 场景内 3-5fps 加密
  L3 关键帧保留: OCR 交叉验证后，教学焦点分数高的帧保留为 keyframe
"""

import os

def _seg_val(seg, key, default=0):
    """兼容 dataclass 和 dict 两种段格式的值获取"""
    if hasattr(seg, 'get'):
        return seg.get(key, default)
    return getattr(seg, key, default)
import re
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field


@dataclass
class SceneSegment:
    """PySceneDetect 输出的场景段"""
    start_sec: float
    end_sec: float
    start_frame: int
    end_frame: int
    
    @property
    def duration(self) -> float:
        return self.end_sec - self.start_sec


@dataclass
class SamplePlan:
    """采样计划：哪些时间点需要截帧"""
    timestamp_sec: float
    frame_number: int
    priority: str = "normal"  # "normal" | "dense" | "keyframe_candidate"
    trigger_reason: str = ""  # 为什么触发这次采样
    

def detect_scenes(
    video_path: str,
    min_scene_len_sec: float = 1.0,
    threshold: float = 27.0,
) -> List[SceneSegment]:
    """
    用 PySceneDetect 的 ContentDetector 做场景切换检测
    
    ContentDetector 基于 HSV 色彩空间帧间差异——
    能检测到：白板写字、PPT翻页、行情图切换、画面大幅变化
    
    Returns:
        场景段列表，每个包含起止时间和帧号
    """
    try:
        from scenedetect import detect, ContentDetector
    except ImportError:
        # 降级：用 OpenCV 直方图差异做简易场景检测
        return _fallback_scene_detect(video_path, min_scene_len_sec, threshold)
    
    try:
        scene_list = detect(video_path, ContentDetector(threshold=threshold))
    except Exception:
        return _fallback_scene_detect(video_path, min_scene_len_sec, threshold)
    
    scenes = []
    for scene in scene_list:
        start = scene[0].get_seconds()
        end = scene[1].get_seconds()
        start_frame = scene[0].frame_num
        end_frame = scene[1].frame_num
        
        if end - start >= min_scene_len_sec:
            scenes.append(SceneSegment(
                start_sec=start,
                end_sec=end,
                start_frame=start_frame,
                end_frame=end_frame,
            ))
    
    return scenes


def _fallback_scene_detect(
    video_path: str,
    min_scene_len: float = 1.0,
    threshold: float = 20.0,
    sample_every_n_frames: int = 24,
) -> List[SceneSegment]:
    """
    PySceneDetect 不可用时的简易场景检测（OpenCV 直方图差异）
    每 N 帧采样一次，比较画面中部区域的变化
    """
    import cv2
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    prev_hist = None
    scenes = []
    current_scene_start = 0.0
    current_scene_start_frame = 0
    
    for frame_idx in range(0, total_frames, sample_every_n_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        
        # 只看画面中部（教学内容区，排除上下边缘的字幕/水印等）
        h, w = frame.shape[:2]
        mid_frame = frame[int(h * 0.2):int(h * 0.85), :, :]
        
        # HSV 直方图
        hsv = cv2.cvtColor(mid_frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [8, 8], [0, 180, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        if prev_hist is not None:
            diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CHISQR)
            timestamp = frame_idx / fps
            
            if diff > threshold:
                # 场景切换
                if timestamp - current_scene_start >= min_scene_len:
                    scenes.append(SceneSegment(
                        start_sec=current_scene_start,
                        end_sec=timestamp,
                        start_frame=current_scene_start_frame,
                        end_frame=frame_idx,
                    ))
                current_scene_start = timestamp
                current_scene_start_frame = frame_idx
        
        prev_hist = hist
    
    # 最后一个场景
    last_timestamp = total_frames / fps
    if last_timestamp - current_scene_start >= min_scene_len:
        scenes.append(SceneSegment(
            start_sec=current_scene_start,
            end_sec=last_timestamp,
            start_frame=current_scene_start_frame,
            end_frame=total_frames - 1,
        ))
    
    cap.release()
    return scenes


def align_scenes_to_subtitles(
    scenes: List[SceneSegment],
    subtitle_segments: List[Dict],
) -> Dict[int, List[SceneSegment]]:
    """
    将场景段按字幕时间轴分组
    
    返回 {subtitle_index: [scenes_in_this_subtitle]}
    一个字幕段可能跨越多个场景（老师讲一句话翻了三次PPT）
    """
    alignment = {}
    
    for si, seg in enumerate(subtitle_segments):
        # 兼容 dataclass 和 dict 两种格式
        if hasattr(seg, 'get'):
            seg_start = seg.get('start', 0)
            seg_end = seg.get('end', 0)
        else:
            seg_start = getattr(seg, 'start', 0)
            seg_end = getattr(seg, 'end', 0)
        
        matching_scenes = [
            sc for sc in scenes
            if sc.start_sec < seg_end and sc.end_sec > seg_start  # 有重叠
        ]
        
        if matching_scenes:
            alignment[si] = matching_scenes
    
    return alignment


def generate_sample_plan(
    scenes: List[SceneSegment],
    subtitle_segments: List[Dict],
    speaker_profile: Optional[Dict] = None,
    fps: float = 30.0,
) -> List[SamplePlan]:
    """
    生成采样计划：哪些帧需要截取跑 OCR
    
    策略：
    1. 每个场景截 1-3 帧（基础采样）
    2. 如果 teaching_patterns 指示型 → 场景内 3fps 加密
    3. 如果字幕被 LLM 分类为指代型语句 → 所在场景加密
    
    Args:
        scenes: 场景检测结果
        subtitle_segments: 字幕时间轴（API 字幕 + VTT/Whisper）
        speaker_profile: 说话人知识库 profile（含 teaching_patterns）
        fps: 视频帧率
    
    Returns:
        采样计划列表
    """
    plans = []
    
    # 判断 UP 主教学类型
    teaching_type = _get_teaching_type(speaker_profile)
    
    alignment = align_scenes_to_subtitles(scenes, subtitle_segments)
    
    # ── 字幕段为空回退: 场景驱动粗采样 ──
    if not subtitle_segments:
        if scenes:
            for scene in scenes:
                mid_time = scene.start_sec + scene.duration / 2
                plans.append(SamplePlan(
                    timestamp_sec=mid_time,
                    frame_number=int(mid_time * fps),
                    priority="normal",
                    trigger_reason="scene_fallback_no_subtitles",
                ))
        else:
            plans.append(SamplePlan(
                timestamp_sec=1.0, frame_number=int(fps),
                priority="low", trigger_reason="uniform_fallback",
            ))
            plans.append(SamplePlan(
                timestamp_sec=5.0, frame_number=int(5 * fps),
                priority="low", trigger_reason="uniform_fallback",
            ))
        return plans
    
    for si, seg in enumerate(subtitle_segments):
        seg_start = _seg_val(seg, 'start', 0)
        seg_end = _seg_val(seg, 'end', 0)
        seg_text = _seg_val(seg, 'text', '')
        
        related_scenes = alignment.get(si, [])
        
        if not related_scenes:
            # 没有场景切换 → 字幕段中间截一帧
            mid_time = (seg_start + seg_end) / 2
            plans.append(SamplePlan(
                timestamp_sec=mid_time,
                frame_number=int(mid_time * fps),
                priority="normal",
                trigger_reason="subtitle_segment_only",
            ))
            continue
        
        # 判断是否需要加密
        is_deictic = _detect_deictic_reference(seg_text)
        use_dense = (
            teaching_type == "spatial_pointing" 
            or (teaching_type == "live_demonstration" and is_deictic)
        )
        
        for scene in related_scenes:
            scene_dur = scene.duration
            
            if use_dense:
                # 加密采样：3fps
                n_samples = max(3, int(scene_dur * 3))
            elif teaching_type == "static_explanation":
                # 稀疏：每个场景只取 1 帧
                n_samples = 1
            else:
                # 默认：三等分采样
                n_samples = min(3, max(1, int(scene_dur)))
            
            for i in range(n_samples):
                frac = (i + 0.5) / n_samples if n_samples > 1 else 0.5
                t = scene.start_sec + frac * scene_dur
                plans.append(SamplePlan(
                    timestamp_sec=t,
                    frame_number=int(t * fps),
                    priority="dense" if use_dense else "normal",
                    trigger_reason=(
                        "deictic_reference" if (use_dense and is_deictic)
                        else "scene_change"
                    ),
                ))
    
    # 按时间排序 + 去重（相近帧合并）
    plans.sort(key=lambda p: p.timestamp_sec)
    plans = _deduplicate_plans(plans, min_interval_sec=0.5)
    
    return plans


def _get_teaching_type(profile: Optional[Dict]) -> str:
    """从 speaker_profile 提取教学类型"""
    if not profile:
        return "unknown"
    
    patterns = profile.get('teaching_patterns', {})
    indicator = patterns.get('indicator_style', '')
    if indicator:
        return indicator
    
    # 从 common_topics 推断
    topics = profile.get('common_topics', [])
    trading_keywords = ['交易', '行情', 'K线', '图表', '盘面']
    teaching_keywords = ['策略', '方法', '教学', '技巧', '原理']
    
    is_trading = any(any(kw in t for kw in trading_keywords) for t in topics)
    is_teaching = any(any(kw in t for kw in teaching_keywords) for t in topics)
    
    if is_trading:
        return "spatial_pointing"
    elif is_teaching:
        return "sequential_scroll"
    return "unknown"


def _detect_deictic_reference(text: str) -> bool:
    """
    检测字幕是否含指代型语句
    
    不用词表匹配，用 LLM 分类语义。这里提供轻量规则作为 fallback。
    
    指代特征：
    - "这个X" "那个X" "这里" "那里" "这儿"
    - "你看" "看到没有" "注意看"
    - "刚才说的" "前面提到的"
    """
    if not text:
        return False
    
    deictic_patterns = [
        r'这个\S', r'那个\S', r'这里', r'那里', r'这儿', r'那儿',
        r'你看', r'看到没', r'注意看', r'注意这里',
        r'刚才说', r'前面提', r'指\S*这个',
        r'像这样', r'这么做', r'举个例子',
    ]
    
    for pat in deictic_patterns:
        if re.search(pat, text):
            return True
    return False


def _deduplicate_plans(
    plans: List[SamplePlan],
    min_interval_sec: float = 0.5,
) -> List[SamplePlan]:
    """合并时间间隔太近的采样计划"""
    if not plans:
        return []
    
    deduped = [plans[0]]
    for p in plans[1:]:
        if p.timestamp_sec - deduped[-1].timestamp_sec >= min_interval_sec:
            deduped.append(p)
        elif p.priority == "dense" and deduped[-1].priority != "dense":
            # 如果新的更密集（加密采样），替换旧的
            deduped[-1] = p
    
    return deduped


def capture_frames(
    video_path: str,
    sample_plan: List[SamplePlan],
    output_dir: str,
    video_id: str = "",
) -> List[str]:
    """
    按采样计划截取视频帧
    
    Returns:
        截取的帧文件路径列表
    """
    os.makedirs(output_dir, exist_ok=True)
    import cv2
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    
    captured = []
    video_hash = hashlib.md5(video_id.encode()).hexdigest()[:8] if video_id else "unknown"
    
    for plan in sample_plan:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        frame_num = plan.frame_number
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            continue
        
        # 以帧号为文件名
        filename = f"{video_hash}_f{frame_num:06d}_t{plan.timestamp_sec:.1f}s.jpg"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        captured.append(filepath)
    
    cap.release()
    return captured


def compute_frame_change_score(
    frame_path_a: str,
    frame_path_b: str,
) -> float:
    """
    计算两帧之间的画面变化程度（0-1）
    只看画面中部，排除字幕/水印区
    """
    try:
        a = cv2.imread(frame_path_a)
        b = cv2.imread(frame_path_b)
        if a is None or b is None:
            return 0.0
        
        h, w = a.shape[:2]
        # 只看中部 60%（排除上下 20%）
        a_mid = a[int(h*0.2):int(h*0.8), :, :]
        b_mid = b[int(h*0.2):int(h*0.8), :, :]
        
        diff = cv2.absdiff(a_mid, b_mid)
        return float(diff.mean()) / 255.0
    except Exception:
        return 0.0
