"""
BiliYouTik2Brain — 时间线对齐融合器 (Phase 3.4)

设计目标：
  Whisper/OCR/字幕三家时间戳统一到同一坐标轴。
  时间对不上不硬塞，标记为"未对齐"单独处理。

核心策略：
  1. 统一坐标轴（秒级浮点数，00:00:00.000 格式）
  2. 对齐判别：同一段内容时间差 < 1.5s 判为对齐
  3. 未对齐内容单独标记，不参与交叉验证
  4. 提供对齐报告供下游使用
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class AlignedSegment:
    """对齐后的单一信息段"""
    start_s: float = 0.0
    end_s: float = 0.0
    text: str = ""
    source: str = "whisper"        # whisper | subtitle | ocr
    is_aligned: bool = True         # 是否与其他源成功对齐
    aligned_with: List[str] = field(default_factory=list)  # 与哪些源对齐
    conflict: bool = False          # 对齐源之间有内容冲突


@dataclass
class AlignmentResult:
    """对齐结果"""
    segments: List[AlignedSegment] = field(default_factory=list)
    aligned_count: int = 0
    unaligned_count: int = 0
    conflict_count: int = 0
    report: str = ""


# ═══════════════════════════════════════════════════════════════
# 时间戳标准化
# ═══════════════════════════════════════════════════════════════

def normalize_timestamp(ts) -> float:
    """将各种时间戳格式统一为秒级浮点数"""
    if isinstance(ts, (int, float)):
        return float(ts)
    
    if isinstance(ts, str):
        ts = ts.strip()
        # HH:MM:SS.mmm 格式
        m = re.match(r'(\d+):(\d+):(\d+)(?:\.(\d+))?', ts)
        if m:
            h, mnt, s, ms = m.groups()
            total = int(h) * 3600 + int(mnt) * 60 + int(s)
            if ms:
                total += float(f"0.{ms}")
            return total
        # MM:SS.mmm 格式
        m = re.match(r'(\d+):(\d+)(?:\.(\d+))?', ts)
        if m:
            mnt, s, ms = m.groups()
            total = int(mnt) * 60 + int(s)
            if ms:
                total += float(f"0.{ms}")
            return total
    
    return 0.0


def format_timestamp(seconds: float) -> str:
    """将秒数格式化为 HH:MM:SS.mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


# ═══════════════════════════════════════════════════════════════
# 对齐引擎
# ═══════════════════════════════════════════════════════════════

def _extract_segments_from_source(
    source: str,
    text: str,
    segments: List[Dict],
) -> List[Dict]:
    """从不同源提取有时间戳的信息段"""
    result = []
    
    if segments:
        for seg in segments:
            st = normalize_timestamp(seg.get("start", 0))
            et = normalize_timestamp(seg.get("end", 0))
            if et <= st:
                et = st + 1.0
            result.append({
                "start": st,
                "end": et,
                "text": seg.get("text", "").strip(),
                "source": source,
            })
    elif text:
        # 无分段信息时，将整个文本视为一个段
        result.append({
            "start": 0,
            "end": 3600,
            "text": text.strip(),
            "source": source,
        })
    
    # 过滤空文本
    return [r for r in result if r["text"]]


def _merge_overlapping(segments: List[Dict], max_gap: float = 1.5) -> List[Dict]:
    """合并时间上重叠或接近的同一源段"""
    if not segments:
        return []
    
    sorted_segs = sorted(segments, key=lambda s: s["start"])
    merged = [sorted_segs[0]]
    
    for seg in sorted_segs[1:]:
        last = merged[-1]
        # 重叠或接近
        if seg["start"] <= last["end"] + max_gap:
            last["end"] = max(last["end"], seg["end"])
            if seg["text"] not in last["text"]:
                last["text"] += " " + seg["text"]
        else:
            merged.append(seg)
    
    return merged


def align_sources(
    whisper_segments: List[Dict] = None,
    subtitle_segments: List[Dict] = None,
    ocr_timeline: List[Dict] = None,
    alignment_window: float = 1.5,
) -> AlignmentResult:
    """多源时间线对齐
    
    流程：
    1. 从各源提取有时间戳的段
    2. 归一化到同一坐标轴（秒）
    3. 按时间窗口对齐
    4. 标记对齐/未对齐/冲突
    
    Args:
        whisper_segments: [{start, end, text}, ...]
        subtitle_segments: [{start, end, text}, ...]
        ocr_timeline: [{timestamp, text}, ...]
        alignment_window: 对齐时间窗口（秒）
    
    Returns:
        AlignmentResult
    """
    # ── 1. 提取各源段 ──
    whisper_items = _extract_segments_from_source("whisper", "", whisper_segments or [])
    subtitle_items = _extract_segments_from_source("subtitle", "", subtitle_segments or [])
    
    ocr_items = []
    if ocr_timeline:
        for frame in ocr_timeline:
            ts = normalize_timestamp(frame.get("timestamp", 0))
            text = frame.get("text", "").strip()
            if text:
                ocr_items.append({
                    "start": ts,
                    "end": ts + 1.0,  # OCR帧是一个时间点
                    "text": text,
                    "source": "ocr",
                })
    
    # ── 2. 按源合并 ──
    whisper_items = _merge_overlapping(whisper_items)
    subtitle_items = _merge_overlapping(subtitle_items)
    
    # ── 3. 对齐 ──
    all_sources = [
        ("whisper", whisper_items),
        ("subtitle", subtitle_items),
        ("ocr", ocr_items),
    ]
    
    result = AlignmentResult()
    
    # 先基于 whisper 的时间线创建基座
    combined_timeline = []
    for src_name, items in all_sources:
        for item in items:
            combined_timeline.append(item)
    
    # 按时间排序
    combined_timeline.sort(key=lambda x: (x["start"], x["source"]))
    
    # 分组：时间窗口内的归为一组
    groups = []
    current_group = []
    
    for item in combined_timeline:
        if not current_group:
            current_group.append(item)
            continue
        
        # 该段是否可以加入当前组（时间窗口）
        belongs = False
        for existing in current_group:
            if (abs(item["start"] - existing["start"]) <= alignment_window or
                abs(item["end"] - existing["end"]) <= alignment_window):
                belongs = True
                break
        
        if belongs:
            current_group.append(item)
        else:
            groups.append(current_group)
            current_group = [item]
    
    if current_group:
        groups.append(current_group)
    
    # ── 4. 为每组创建对齐段 ──
    for group in groups:
        sources_in_group = list(set(s["source"] for s in group))
        
        # 取最早的 start 和最晚的 end
        start_s = min(s["start"] for s in group)
        end_s = max(s["end"] for s in group)
        
        # 合并文本
        texts_by_source = {}
        for s in group:
            if s["source"] not in texts_by_source:
                texts_by_source[s["source"]] = s["text"]
            elif s["text"] not in texts_by_source[s["source"]]:
                texts_by_source[s["source"]] += " | " + s["text"]
        
        # 主文本选择策略：whisper > subtitle > ocr
        main_text = texts_by_source.get("whisper", 
                     texts_by_source.get("subtitle",
                     texts_by_source.get("ocr", "")))
        
        # 冲突检测：不同源内容不一致
        has_conflict = False
        unique_texts = set(v.strip().lower() for v in texts_by_source.values())
        if len(unique_texts) > 1 and len(sources_in_group) > 1:
            has_conflict = True
        
        is_aligned = len(sources_in_group) > 1
        
        seg = AlignedSegment(
            start_s=round(start_s, 3),
            end_s=round(end_s, 3),
            text=main_text,
            source=sources_in_group[0] if len(sources_in_group) == 1 else "multi",
            is_aligned=is_aligned,
            aligned_with=sources_in_group,
            conflict=has_conflict,
        )
        result.segments.append(seg)
        
        if is_aligned:
            result.aligned_count += 1
        else:
            result.unaligned_count += 1
        if has_conflict:
            result.conflict_count += 1
    
    # 生成报告
    report_parts = [
        f"时间线对齐: {result.aligned_count}段对齐 / {result.unaligned_count}段未对齐"
    ]
    if result.conflict_count > 0:
        report_parts.append(f"⚠️ {result.conflict_count}段有内容冲突")
    
    alignment_ratio = result.aligned_count / max(len(result.segments), 1) * 100
    report_parts.append(f"对齐率: {alignment_ratio:.0f}%")
    
    result.report = " | ".join(report_parts)
    
    return result


# ═══════════════════════════════════════════════════════════════
# 用于 enhance 的辅助函数
# ═══════════════════════════════════════════════════════════════

def align_for_enhancement(
    raw_segments: List[Dict],
    subtitle_segments: List[Dict],
    ocr_timeline: List[Dict],
) -> Dict:
    """简化接口：返回 enhance 需要的对齐信息"""
    result = align_sources(
        whisper_segments=raw_segments,
        subtitle_segments=subtitle_segments,
        ocr_timeline=ocr_timeline,
    )
    
    # 提取未对齐段的内容
    unaligned_texts = [
        seg.text for seg in result.segments if not seg.is_aligned and seg.text.strip()
    ]
    
    conflict_texts = [
        seg.text for seg in result.segments if seg.conflict
    ]
    
    return {
        "alignment_result": result,
        "aligned_count": result.aligned_count,
        "unaligned_count": result.unaligned_count,
        "conflict_count": result.conflict_count,
        "unaligned_texts": unaligned_texts,
        "conflict_texts": conflict_texts,
        "alignment_report": result.report,
    }
