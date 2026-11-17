"""
OCR 抽帧科学算法
==============
参考: 小哲讲算法 — 快排 partition + 滑动窗口

三个核心步骤:
1. 滑动窗口合并 — 相邻低置信segment去重
2. 快排partition加权 — 置信度平方逆权分配帧数
3. 三等分+内点采样 — 覆盖段首/段中/段尾
"""

from typing import List, Dict, Optional


def ocr_sample_plan(
    segments: List[Dict],
    max_frames: int = 20,
    gap_threshold: float = 2.0,
    confidence_threshold: float = 0.6,
    weight_exponent: float = 2.0,
) -> List[Dict]:
    """
    科学抽帧计划生成器

    Args:
        segments: [{start, end, confidence, text, ...}]
        max_frames: 单视频最大抽帧数
        gap_threshold: 合并相邻segment的最大间隔(秒)
        confidence_threshold: 触发OCR的最低置信度
        weight_exponent: 置信度加权指数(2=平方)

    Returns:
        [{time, confidence, segment_range, words, ...}]
    """
    if not segments:
        return []

    # 过滤低置信段
    low_conf = [s for s in segments if s.get('confidence', 1.0) < confidence_threshold]
    if not low_conf:
        return []

    # Step 1: 滑动窗口合并
    merged = _merge_adjacent(low_conf, gap_threshold)

    # Step 2: 置信度加权分配
    allocated = _allocate_by_confidence(merged, max_frames, weight_exponent)

    # Step 3: 三等分+内点采样
    plan = []
    for seg in allocated:
        points = _sample_in_segment(seg)
        for tp in points:
            plan.append({
                'time': round(tp, 1),
                'confidence': seg['confidence'],
                'segment_range': f"{seg['start']:.0f}-{seg['end']:.0f}",
                'words': seg.get('words', seg.get('text', ''))[:40],
                'frames_in_segment': seg.get('frames', 1),
            })

    return plan


def _merge_adjacent(segments: List[Dict], gap_threshold: float) -> List[Dict]:
    """滑动窗口合并：间隔≤gap_threshold秒的相邻段合并为一个抽帧区间"""
    if not segments:
        return []

    # 按时 start 排序
    sorted_segs = sorted(segments, key=lambda s: s['start'])

    merged = []
    current = dict(sorted_segs[0])
    current['words'] = sorted_segs[0].get('text', '')

    for seg in sorted_segs[1:]:
        if seg['start'] - current['end'] <= gap_threshold:
            # 合并
            current['end'] = max(current['end'], seg['end'])
            current['confidence'] = min(current['confidence'], seg['confidence'])
            current['words'] += ' ' + seg.get('text', '')
        else:
            merged.append(current)
            current = dict(seg)
            current['words'] = seg.get('text', '')

    merged.append(current)
    return merged


def _allocate_by_confidence(
    merged: List[Dict], max_frames: int, exponent: float
) -> List[Dict]:
    """快排partition思想：按 (1-confidence)^exponent 加权分配帧数"""
    if not merged:
        return []

    weights = [(1 - s['confidence']) ** exponent for s in merged]
    total = sum(weights)

    if total == 0:
        # 所有置信度=1，均匀分配
        n = len(merged)
        for i, s in enumerate(merged):
            s['frames'] = max(1, max_frames // n)
        return merged

    allocated = max_frames
    for i, s in enumerate(merged):
        raw = max_frames * weights[i] / total
        frames = max(1, round(raw))
        frames = min(frames, allocated)  # 不超出剩余预算
        s['frames'] = frames
        allocated -= frames

    # 如果还有剩余帧，分给最低置信度的段
    i = 0
    sorted_by_conf = sorted(enumerate(merged), key=lambda x: x[1]['confidence'])
    while allocated > 0 and i < len(sorted_by_conf):
        idx = sorted_by_conf[i][0]
        merged[idx]['frames'] += 1
        allocated -= 1
        i += 1

    return merged


def _sample_in_segment(seg: Dict) -> List[float]:
    """三等分+内点采样：确保覆盖段首/段中/段尾"""
    duration = seg['end'] - seg['start']
    n = seg.get('frames', 1)

    if duration <= 0:
        return [seg['start']]

    if n <= 1:
        # 单帧：段中点
        return [seg['start'] + duration / 2]
    elif n <= 4:
        # 2-4帧：三等分点采样（覆盖首/中/尾）
        step = duration / (n + 1)
        return [seg['start'] + step * (i + 1) for i in range(n)]
    else:
        # 5+帧：等距采样
        step = duration / (n + 1)
        return [seg['start'] + step * (i + 1) for i in range(n)]


def plan_stats(plan: List[Dict], input_count: int) -> Dict:
    """输出统计信息"""
    if not plan:
        return {'total_frames': 0, 'compression': 0, 'avg_confidence': 0}

    unique_ranges = len(set(p['segment_range'] for p in plan))
    avg_conf = sum(p['confidence'] for p in plan) / len(plan)

    return {
        'input_segments': input_count,
        'merged_intervals': unique_ranges,
        'total_frames': len(plan),
        'compression': f"{len(plan)/max(input_count,1)*100:.0f}%",
        'avg_confidence': round(avg_conf, 3),
        'savings': input_count - unique_ranges,
    }
