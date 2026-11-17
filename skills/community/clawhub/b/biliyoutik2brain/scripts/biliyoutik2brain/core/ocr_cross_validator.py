"""
两条腿交叉验证器 — OCR 文字块 vs 音频转录文本
==============================================
核心原理：OCR 出画面上的所有文字，同时刻的音频转录告诉你"说话人在说什么"。
两条腿踩同一时间点——重叠的是字幕，不重叠的是教学画面文字。

v2.1: 相似度算法从 Jaccard 升级为三路融合（SequenceMatcher + 编辑距离 + n-gram Jaccard）
"""

import re
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from difflib import SequenceMatcher


@dataclass
class OCRBlock:
    """OCR 单个文字块"""
    text: str
    score: float          # OCR 置信度
    box: List[List[float]]  # [[x1,y1],[x2,y2],[x3,y3],[x4,y4]] 四点坐标
    center_x: float = 0.0
    center_y: float = 0.0
    area: float = 0.0
    
    def __post_init__(self):
        if self.box and len(self.box) == 4:
            xs = [p[0] for p in self.box]
            ys = [p[1] for p in self.box]
            self.center_x = sum(xs) / 4
            self.center_y = sum(ys) / 4
            w = max(xs) - min(xs)
            h = max(ys) - min(ys)
            self.area = w * h


@dataclass
class OCRTimelineFrame:
    """时间轴上的一帧 OCR 结果"""
    timestamp_sec: float
    image_path: str            # 截帧文件路径
    blocks: List[OCRBlock] = field(default_factory=list)
    # 交叉验证分类结果
    subtitle_blocks: List[OCRBlock] = field(default_factory=list)   # 与音频重叠=字幕
    teaching_blocks: List[OCRBlock] = field(default_factory=list)   # 与音频不重叠=教学内容
    # 教学焦点
    teaching_focus_score: float = 0.0
    teaching_focus_region: Optional[Dict] = None  # {x,y,w,h,block_count}


def _clean_text(text: str) -> str:
    """清洗文本：去标点空格，保留纯字符"""
    return re.sub(r'[\s，,。\.！!？?、；;：:""''「」（）()【】\[\]『』～~—\-—・·]', '', text)


def _char_ngrams(text: str, n: int = 3) -> set:
    """字符 n-gram 集合（中文字符级）"""
    chars = _clean_text(text)
    if len(chars) < n:
        return {chars}
    return {chars[i:i+n] for i in range(len(chars) - n + 1)}


def _jaccard_similarity(text_a: str, text_b: str) -> float:
    """基于字符 3-gram 的 Jaccard 相似度（保留作为三路融合的一路）"""
    if not text_a or not text_b:
        return 0.0
    set_a = _char_ngrams(text_a, 3)
    set_b = _char_ngrams(text_b, 3)
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def _sequence_matcher_similarity(text_a: str, text_b: str) -> float:
    """SequenceMatcher 最长公共子序列相似度
    对中文 OCR 比 Jaccard 更准——能捕捉字符顺序和连续匹配
    """
    if not text_a or not text_b:
        return 0.0
    clean_a = _clean_text(text_a)
    clean_b = _clean_text(text_b)
    if not clean_a or not clean_b:
        return 0.0
    return SequenceMatcher(None, clean_a, clean_b).ratio()


def _edit_distance_similarity(text_a: str, text_b: str) -> float:
    """归一化编辑距离相似度（Levenshtein）
    等同度 = 1 - (编辑距离 / max(lenA, lenB))
    """
    if not text_a or not text_b:
        return 0.0
    clean_a = _clean_text(text_a)
    clean_b = _clean_text(text_b)
    if not clean_a or not clean_b:
        return 0.0
    
    m, n = len(clean_a), len(clean_b)
    # 滚动数组 O(min(m,n)) 空间
    if m < n:
        clean_a, clean_b = clean_b, clean_a
        m, n = n, m
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            cost = 0 if clean_a[i-1] == clean_b[j-1] else 1
            curr[j] = min(prev[j] + 1, curr[j-1] + 1, prev[j-1] + cost)
        prev = curr
    distance = prev[n]
    return 1.0 - (distance / max(m, n))


def _fused_similarity(text_a: str, text_b: str) -> float:
    """三路融合相似度：取 SequenceMatcher / 编辑距离 / Jaccard 中的最大值
    
    理由：
    - SequenceMatcher 擅长捕捉连续子串匹配（字幕常是转录的子串）
    - 编辑距离 擅长捕捉 OCR 少量错字的相似（"文 本" vs "文本"）
    - Jaccard 擅长捕捉词袋重叠（即使顺序不同）
    取最大值不会误杀——三路都低才是真的不相似
    """
    if not text_a or not text_b:
        return 0.0
    return max(
        _sequence_matcher_similarity(text_a, text_b),
        _edit_distance_similarity(text_a, text_b),
        _jaccard_similarity(text_a, text_b),
    )


def _substring_overlap_ratio(short_text: str, long_text: str) -> float:
    """短文本在长文本中的子串覆盖率
    更准确判断"OCR文字块是否来源于字幕内容"
    """
    if not short_text or not long_text:
        return 0.0
    short_clean = _clean_text(short_text)
    long_clean = _clean_text(long_text)
    if not short_clean or not long_clean:
        return 0.0
    
    # 滑动窗口：看短文本的字符有多少出现在长文本的连续子串中
    matched = 0
    i = 0
    while i < len(short_clean):
        best_match = 0
        for wlen in range(min(len(short_clean) - i, 20), 1, -1):
            sub = short_clean[i:i+wlen]
            if sub in long_clean:
                best_match = wlen
                break
        if best_match > 0:
            matched += best_match
            i += best_match
        else:
            i += 1
    return matched / len(short_clean) if short_clean else 0.0


def classify_ocr_blocks(
    ocr_blocks: List[OCRBlock],
    transcript_at_timestamp: str,
    subtitle_similarity_threshold: float = 0.3,
) -> Tuple[List[OCRBlock], List[OCRBlock]]:
    """
    两条腿交叉验证：OCR 文字块 vs 同步音频转录
    
    原理：
    - 如果 OCR 块与转录文本高度相似 → 这是字幕（说话人说的东西打在画面上）
    - 如果 OCR 块与转录文本不相似 → 这是教学画面文字（白板/PPT/行情图上的东西）
    
    v2.1: 用三路融合相似度（SequenceMatcher + 编辑距离 + Jaccard 取 max）
    
    Args:
        ocr_blocks: OCR 识别出的所有文字块
        transcript_at_timestamp: 此刻的音频转录文本
        subtitle_similarity_threshold: 融合相似度阈值
    
    Returns:
        (subtitle_blocks, teaching_blocks)
    """
    if not transcript_at_timestamp:
        return [], ocr_blocks
    
    subtitle_blocks = []
    teaching_blocks = []
    
    for block in ocr_blocks:
        # 三路融合相似度 → 比对 OCR 文字块和转录文本
        fused = _fused_similarity(block.text, transcript_at_timestamp)
        
        if fused >= subtitle_similarity_threshold:
            subtitle_blocks.append(block)
        else:
            teaching_blocks.append(block)
    
    return subtitle_blocks, teaching_blocks


def compute_teaching_focus_score(
    teaching_blocks: List[OCRBlock],
    image_width: int = 1280,
    image_height: int = 720,
) -> Tuple[float, Optional[Dict]]:
    """
    计算教学焦点：教学文字块的密度分布
    
    原理：
    - 在画面上做网格分区
    - 统计每个分区的教学文字块数量+置信度
    - 密度最高的区域 = 教学焦点区
    
    Returns:
        (focus_score, focus_region) — 分数 0-1 和焦点区域坐标
    """
    if not teaching_blocks:
        return 0.0, None
    
    # 4x4 网格分区
    grid_cols, grid_rows = 4, 4
    cell_w = image_width / grid_cols
    cell_h = image_height / grid_rows
    
    grid = np.zeros((grid_rows, grid_cols))
    for block in teaching_blocks:
        col = min(int(block.center_x / cell_w), grid_cols - 1)
        row = min(int(block.center_y / cell_h), grid_rows - 1)
        grid[row][col] += block.score  # 按置信度加权
    
    # 找最大密度的格子
    max_row, max_col = np.unravel_index(grid.argmax(), grid.shape)
    max_density = grid[max_row][max_col]
    
    # 全局焦点分数（归一化）
    max_possible = len(teaching_blocks) * 1.0
    focus_score = max_density / max_possible if max_possible > 0 else 0.0
    
    focus_region = {
        'x': max_col * cell_w,
        'y': max_row * cell_h,
        'w': cell_w,
        'h': cell_h,
        'block_count': int(max_density),
    }
    
    return focus_score, focus_region


def is_keyframe_worthy(
    frame: OCRTimelineFrame,
    teaching_block_min: int = 2,
    focus_score_min: float = 0.15,
) -> bool:
    """
    判断一帧是否值得作为 keyframe 截图
    
    条件：
    1. 有至少 N 个教学文字块
    2. 教学焦点分数超过阈值
    
    这是"说明画面"的选取标准。
    """
    if len(frame.teaching_blocks) < teaching_block_min:
        return False
    
    # 计算焦点
    score, _ = compute_teaching_focus_score(frame.teaching_blocks)
    frame.teaching_focus_score = score
    
    return score >= focus_score_min


def select_best_keyframe(
    frames: List[OCRTimelineFrame],
    window_start: float,
    window_end: float,
) -> Optional[OCRTimelineFrame]:
    """
    在时间窗口 [window_start, window_end] 内选最佳 keyframe
    
    评分 = teaching_block_count × 2 + focus_score × 5
    取最高分。
    """
    candidates = [
        f for f in frames 
        if window_start <= f.timestamp_sec <= window_end
        and f.teaching_focus_score > 0
    ]
    
    if not candidates:
        # 放宽条件：只要有教学块就算
        candidates = [
            f for f in frames
            if window_start <= f.timestamp_sec <= window_end
            and len(f.teaching_blocks) > 0
        ]
    
    if not candidates:
        return None
    
    # 按综合分排序
    def score(f):
        return len(f.teaching_blocks) * 2 + f.teaching_focus_score * 5
    
    candidates.sort(key=score, reverse=True)
    return candidates[0]


def merge_ocr_to_subtitle_timeline(
    subtitle_segments: List[Dict],
    ocr_frames: List[OCRTimelineFrame],
) -> List[Dict]:
    """
    将 OCR 教学文字和 keyframe 合并到字幕时间轴
    
    输出格式：
    [{
        'start': float, 'end': float,
        'subtitle_text': str,
        'teaching_texts': [str, ...],     # 教学画面上的文字
        'teaching_focus_region': {...},
        'keyframe_path': str,              # 说明画面截图
        'topic_words': [str, ...],         # 关键词
    }]
    """
    merged = []
    
    for seg in subtitle_segments:
        seg_start = getattr(seg, "start", 0) if not hasattr(seg, "get") else seg.get("start", 0)
        seg_end = getattr(seg, "end", 0) if not hasattr(seg, "get") else seg.get("end", 0)
        seg_text = seg.get('text', '')
        
        # 找到这个字幕段对应的 OCR 帧
        related_frames = [
            f for f in ocr_frames
            if seg_start - 0.5 <= f.timestamp_sec <= seg_end + 0.5
        ]
        
        # 收集该段内的所有教学文字（去重）
        teaching_texts = []
        seen = set()
        for f in related_frames:
            for b in f.teaching_blocks:
                txt = b.text.strip()
                if txt and txt not in seen:
                    teaching_texts.append(txt)
                    seen.add(txt)
        
        # 选最佳 keyframe
        best_frame = select_best_keyframe(related_frames, seg_start, seg_end)
        
        merged.append({
            'start': seg_start,
            'end': seg_end,
            'subtitle_text': seg_text,
            'teaching_texts': teaching_texts,
            'teaching_focus_region': best_frame.teaching_focus_region if best_frame else None,
            'keyframe_path': getattr(best_frame, 'image_path', None) if best_frame else None,
            'ocr_frame_count': len(related_frames),
        })
    
    return merged
