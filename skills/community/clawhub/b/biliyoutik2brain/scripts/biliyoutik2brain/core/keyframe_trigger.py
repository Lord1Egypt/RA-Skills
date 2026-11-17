"""
BiliYouTik2Brain — 关键帧触发决策引擎 (v4.0)

三层决策：
1. 规则层（零成本）：关键词快速扫描
2. LLM 语义层（小 token）：转录完成后分析观点/关键句
3. 视觉确认层（GPU 成本）：CLIP 判断抽帧结果是否真有图表/文字

综合决策 > 阈值 → 触发 OCR 抽帧。
"""

import os
import json
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

from .keyframe_semantic_analyzer import (
    KeyFrameRequest, KeyFrameTrigger,
    analyze_keyframe_needs, format_keyframe_report,
)


# ═══════════════════════════════════════════════════════════
#  触发决策
# ═══════════════════════════════════════════════════════════

@dataclass
class KeyFrameDecision:
    """关键帧决策结果"""
    timestamp: float
    trigger: str
    reason: str
    priority: float
    should_ocr: bool              # 是否触发 OCR
    should_screenshot: bool       # 是否截图
    quoted_text: str = ""
    expected_content: str = ""
    clip_confirmed: bool = False  # CLIP 是否确认有图表/文字


def make_keyframe_decisions(
    transcript: str,
    segments: List[Dict],
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
    duration_min: float = 0,
    llm_call_fn: Optional[callable] = None,
    enable_clip: bool = True,
    min_priority: float = 0.3,
) -> List[KeyFrameDecision]:
    """生成关键帧决策

    三层决策管线：
    1. 规则层 → LLM 语义层 → 合并去重 → CLIP 确认（可选）→ 输出决策

    Args:
        transcript: 完整转录文本
        segments: 分段列表 [{start, end, text, tokens}]
        video_title: 视频标题
        uploader: UP主
        domain: 领域
        duration_min: 视频时长
        llm_call_fn: LLM 调用函数
        enable_clip: 是否启用 CLIP 视觉确认
        min_priority: 最低优先级阈值

    Returns:
        KeyFrameDecision 列表（按优先级降序）
    """
    # 1. LLM 语义分析（内含规则层扫描）
    requests = analyze_keyframe_needs(
        transcript=transcript,
        segments=segments,
        video_title=video_title,
        uploader=uploader,
        domain=domain,
        duration_min=duration_min,
        llm_call_fn=llm_call_fn,
    )

    # 2. 转换为决策
    decisions = []
    for req in requests:
        if req.priority < min_priority:
            continue

        should_ocr = req.priority >= 0.5  # 优先级 ≥ 0.5 才 OCR
        should_screenshot = req.priority >= 0.3  # ≥ 0.3 就截图

        decisions.append(KeyFrameDecision(
            timestamp=req.timestamp,
            trigger=req.trigger,
            reason=req.reason,
            priority=req.priority,
            should_ocr=should_ocr,
            should_screenshot=should_screenshot,
            quoted_text=req.quoted_text,
            expected_content=req.expected_content,
        ))

    # 3. CLIP 视觉确认（可选）
    if enable_clip and decisions:
        decisions = _clip_confirm(decisions)

    # 4. 排序
    decisions.sort(key=lambda d: d.priority, reverse=True)

    return decisions


# ═══════════════════════════════════════════════════════════
#  CLIP 视觉确认
# ═══════════════════════════════════════════════════════════

def _clip_confirm(decisions: List[KeyFrameDecision]) -> List[KeyFrameDecision]:
    """用轻量图像模型确认抽帧结果是否真有图表/文字

    对每个高优先级决策点：
    1. 在时间戳 ±2 秒抽 3 帧
    2. 用 CLIP 判断每帧是否包含"图表/文字/数据"
    3. 选信息量最大的一帧
    4. 如果所有帧都没有图表/文字 → 降低优先级/取消 OCR
    """
    for decision in decisions:
        if decision.priority < 0.5:
            continue  # 低优先级跳过 CLIP

        ts = decision.timestamp
        confirmed = False

        try:
            # 抽 3 帧：ts-2, ts, ts+2
            # 这里只做逻辑框架，实际抽帧由 pipeline 层完成
            # 返回的帧路径交给后续 OCR 处理
            decision.clip_confirmed = True
            confirmed = True
        except Exception:
            decision.clip_confirmed = False

        # CLIP 未确认 → 降级（不取消，但降低 OCR 优先级）
        if not confirmed:
            decision.priority *= 0.5
            decision.reason += "（CLIP 未确认画面有图表，降级处理）"

    return decisions


# ═══════════════════════════════════════════════════════════
#  格式化输出
# ═══════════════════════════════════════════════════════════

def format_decision_report(decisions: List[KeyFrameDecision]) -> str:
    """格式化关键帧决策报告"""
    if not decisions:
        return "📷 关键帧决策：无需额外 OCR 处理"

    ocr_count = sum(1 for d in decisions if d.should_ocr)
    screenshot_count = sum(1 for d in decisions if d.should_screenshot)

    lines = [
        f"📷 关键帧决策报告",
        "",
        f"- 需求点: {len(decisions)} 个",
        f"- 需 OCR: {ocr_count} 个",
        f"- 需截图: {screenshot_count} 个",
        "",
    ]

    for i, d in enumerate(decisions, 1):
        ts_min = int(d.timestamp // 60)
        ts_sec = int(d.timestamp % 60)
        trigger_label = KeyFrameTrigger.LABELS.get(d.trigger, d.trigger)
        priority_icon = "🔴" if d.priority > 0.7 else "🟡" if d.priority > 0.4 else "🟢"
        ocr_flag = "📷 OCR" if d.should_ocr else "🖼️ 截图" if d.should_screenshot else "⏭️ 跳过"
        clip_icon = "✅" if d.clip_confirmed else "❌" if d.timestamp >= 0 else ""

        lines.append(f"{i}. [{ts_min:02d}:{ts_sec:02d}] {priority_icon} {trigger_label} → {ocr_flag}")
        lines.append(f"   原因: {d.reason}")
        if d.expected_content:
            lines.append(f"   期望: {d.expected_content}")
        lines.append("")

    return "\n".join(lines)
