"""
BiliYouTik2Brain — 关键帧语义分析器 (v4.0)

LLM 驱动：理解转录内容的观点、关键句、论证逻辑，
判断"这里需要配一张画面图帮助理解"，输出关键帧需求列表。

不是简单的关键词匹配，而是语义理解后的判断。
"""

import re
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════
#  触发类型
# ═══════════════════════════════════════════════════════════

class KeyFrameTrigger:
    """关键帧触发类型"""
    VIEWPOINT = "viewpoint"       # 观点支撑：复杂观点需要画面辅助
    DATA_COMPARE = "data_compare" # 数据对比：多个数据/指标需要图表
    VISUAL_GUIDE = "visual_guide" # 引导词：明确说"看图""图上"
    DEMO = "demo"                 # 操作演示：步骤需要截图
    CONCLUSION = "conclusion"     # 结论展示：总结性陈述配关键帧
    CHART_REFERENCE = "chart_ref" # 图表引用：提到具体图表/指标

    ALL = [VIEWPOINT, DATA_COMPARE, VISUAL_GUIDE, DEMO, CONCLUSION, CHART_REFERENCE]

    LABELS = {
        VIEWPOINT: "观点支撑",
        DATA_COMPARE: "数据对比",
        VISUAL_GUIDE: "引导词",
        DEMO: "操作演示",
        CONCLUSION: "结论展示",
        CHART_REFERENCE: "图表引用",
    }


@dataclass
class KeyFrameRequest:
    """单个关键帧需求"""
    timestamp: float               # 时间戳（秒）
    trigger: str                   # 触发类型
    reason: str                    # 为什么需要（LLM 生成的人类可读解释）
    quoted_text: str = ""          # 触发该需求的原文引用
    priority: float = 0.5          # 优先级 0-1
    expected_content: str = ""     # 期望画面内容描述（如"MA889 指标图"）


# ═══════════════════════════════════════════════════════════
#  规则层兜底（零成本快速扫描）
# ═══════════════════════════════════════════════════════════

# 视觉引导词（关键词兜底）
_VISUAL_GUIDE_WORDS = [
    "看图", "图上", "这个图", "这张图", "这个坐标", "这个位置",
    "我们来看", "大家看", "请看", "如下图", "如图所示",
    "图上的", "画面里", "画面中", "截图",
    "这个价格", "这个点位", "这个指标",
    "可以看到", "大家可以看到",
]

# 数据/图表引用词
_CHART_REF_WORDS = [
    "MA889", "EMA", "SMA", "MACD", "RSI", "KDJ",
    "支撑位", "阻力位", "压力位",
    "布林", "斐波那契",
    "K线", "蜡烛图", "分时图",
    "收益率", "回撤", "夏普",
    "对比", "比较", "分别是",
]


def _rule_based_scan(transcript: str, segments: List[Dict]) -> List[KeyFrameRequest]:
    """规则层快速扫描（零成本）

    扫描转录文本中的关键词，标记明显需要 OCR 的点。
    这是兜底策略，LLM 分析前的快速预检。
    """
    requests = []

    for seg in segments:
        text = seg.get("text", "")
        start = seg.get("start", 0)

        # 视觉引导词
        for word in _VISUAL_GUIDE_WORDS:
            if word in text:
                requests.append(KeyFrameRequest(
                    timestamp=start,
                    trigger=KeyFrameTrigger.VISUAL_GUIDE,
                    reason=f"包含视觉引导词「{word}」",
                    quoted_text=text[:100],
                    priority=0.8,
                    expected_content="画面截图",
                ))
                break

        # 图表引用
        for word in _CHART_REF_WORDS:
            if word in text:
                requests.append(KeyFrameRequest(
                    timestamp=start,
                    trigger=KeyFrameTrigger.CHART_REFERENCE,
                    reason=f"提到技术指标「{word}」，可能需要图表辅助",
                    quoted_text=text[:100],
                    priority=0.5,
                    expected_content=f"含 {word} 的图表",
                ))
                break

    return requests


# ═══════════════════════════════════════════════════════════
#  LLM 语义分析
# ═══════════════════════════════════════════════════════════

_SEMANTIC_ANALYSIS_PROMPT = """你是一个视频内容分析助手。分析以下视频转录文本，判断哪些时间点需要配上画面截图来帮助观众理解。

## 视频信息
标题: {video_title}
UP主: {uploader}
领域: {domain}
时长: {duration_min} 分钟

## 转录文本（分段带时间戳）
{segments_text}

## 分析维度

请从以下 6 个维度判断是否需要画面辅助：

1. **观点支撑 (viewpoint)**：讲了复杂观点/方法论/逻辑推理，配画面帮助理解
2. **数据对比 (data_compare)**：提到多个数据/指标/价格对比，需要图表佐证
3. **引导词 (visual_guide)**：明确说"看图""图上""这个坐标"等，指向画面
4. **操作演示 (demo)**：讲操作步骤/使用教程，需要截图展示步骤
5. **结论展示 (conclusion)**：总结性陈述/关键结论，配关键帧强化记忆
6. **图表引用 (chart_ref)**：提到具体图表/指标名称（MA/EMA/MACD等）

## 要求

返回 JSON 数组，每个元素包含:
- timestamp: 时间戳（秒，从 segments 中获取）
- trigger: 触发类型（viewpoint / data_compare / visual_guide / demo / conclusion / chart_ref）
- reason: 为什么需要画面（人类可读的解释，1-2句话）
- quoted_text: 触发该需求的原文引用（不超过100字）
- priority: 优先级 0-1（该帧对理解内容的重要程度）
- expected_content: 期望画面描述（如"MA889指标图，标注支撑位"）

**关键规则**:
- 只返回真正需要画面的点，不要每个段落都标记
- 优先标记：观众只看文字理解不了的点
- 如果只是简单陈述，不需要画面
- 最多返回 15 个关键帧需求

返回格式:
[
  {{
    "timestamp": 120.5,
    "trigger": "viewpoint",
    "reason": "讲解了 MA889 支撑位判断方法，观众需要看具体图表位置才能理解",
    "quoted_text": "我们看到 MA889 在这里形成了一个明显的支撑位...",
    "priority": 0.9,
    "expected_content": "MA889 指标图，标注 4366 附近的支撑区域"
  }},
  ...
]

只返回 JSON 数组，不要其他文字。
"""


def _build_segments_text(segments: List[Dict], max_chars: int = 8000) -> str:
    """构建分段文本（截断到 max_chars）"""
    parts = []
    total = 0
    for seg in segments:
        text = seg.get("text", "")[:200]
        start = seg.get("start", 0)
        end = seg.get("end", 0)
        line = f"[{start:.0f}s-{end:.0f}s] {text}"
        if total + len(line) > max_chars:
            parts.append(f"[{start:.0f}s-{end:.0f}s] ...（截断）")
            break
        parts.append(line)
        total += len(line)
    return "\n".join(parts)


def analyze_keyframe_needs(
    transcript: str,
    segments: List[Dict],
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
    duration_min: float = 0,
    llm_call_fn: Optional[callable] = None,
) -> List[KeyFrameRequest]:
    """分析关键帧需求

    两层扫描：
    1. 规则层：关键词快速匹配（零成本）
    2. LLM 层：语义理解补充（小 token）

    Args:
        transcript: 完整转录文本
        segments: 分段列表 [{start, end, text, tokens}]
        video_title: 视频标题
        uploader: UP主
        domain: 领域（交易/技术/教育等）
        duration_min: 视频时长（分钟）
        llm_call_fn: LLM 调用函数（默认用内置）

    Returns:
        KeyFrameRequest 列表
    """
    # 1. 规则层快速扫描
    rule_requests = _rule_based_scan(transcript, segments)

    # 2. LLM 语义分析
    llm_requests = []
    try:
        segments_text = _build_segments_text(segments)

        prompt = _SEMANTIC_ANALYSIS_PROMPT.format(
            video_title=video_title or "(未知)",
            uploader=uploader or "(未知)",
            domain=domain or "(自动推断)",
            duration_min=f"{duration_min:.0f}",
            segments_text=segments_text,
        )

        if llm_call_fn:
            result_text = llm_call_fn([{"role": "user", "content": prompt}])
        else:
            result_text = _call_llm_default(prompt)

        # 解析 JSON
        llm_requests = _parse_llm_result(result_text)

    except Exception:
        # LLM 分析失败，只用规则层结果
        pass

    # 3. 合并去重（时间戳相近的合并，取高优先级）
    merged = _merge_requests(rule_requests + llm_requests)

    # 4. 排序（优先级降序）
    merged.sort(key=lambda r: r.priority, reverse=True)

    return merged[:15]  # 最多 15 个


def _parse_llm_result(text: str) -> List[KeyFrameRequest]:
    """解析 LLM 返回的 JSON"""
    # 提取 JSON 数组
    json_match = re.search(r'\[[\s\S]*\]', text)
    if not json_match:
        return []

    try:
        data = json.loads(json_match.group(0))
    except json.JSONDecodeError:
        return []

    requests = []
    for item in data:
        if not isinstance(item, dict):
            continue
        ts = item.get("timestamp", 0)
        trigger = item.get("trigger", "viewpoint")
        if trigger not in KeyFrameTrigger.ALL:
            trigger = "viewpoint"

        requests.append(KeyFrameRequest(
            timestamp=float(ts),
            trigger=trigger,
            reason=item.get("reason", ""),
            quoted_text=item.get("quoted_text", "")[:100],
            priority=float(item.get("priority", 0.5)),
            expected_content=item.get("expected_content", ""),
        ))

    return requests


def _merge_requests(requests: List[KeyFrameRequest]) -> List[KeyFrameRequest]:
    """合并时间戳相近的重复请求"""
    if not requests:
        return []

    merged = []
    used = set()

    for i, req in enumerate(requests):
        if i in used:
            continue

        best = req
        for j, other in enumerate(requests):
            if j in used or j == i:
                continue
            # 时间戳相差 < 5 秒视为同一点
            if abs(other.timestamp - req.timestamp) < 5:
                used.add(j)
                # 取高优先级
                if other.priority > best.priority:
                    best = other

        used.add(i)
        merged.append(best)

    return merged


# ═══════════════════════════════════════════════════════════
#  LLM 调用（默认实现）
# ═══════════════════════════════════════════════════════════

def _call_llm_default(prompt: str) -> str:
    """默认 LLM 调用"""
    try:
        from .secrets import get_llm_config
        import requests
        import time

        key, base, model = get_llm_config()
        if not (key and base and model):
            return "[]"

        start = time.time()
        resp = requests.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2048,
                "temperature": 0.3,
            },
            timeout=60,
        )
        elapsed_ms = (time.time() - start) * 1000

        if resp.status_code == 200:
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "[]")

        return "[]"

    except Exception:
        return "[]"


# ═══════════════════════════════════════════════════════════
#  格式化输出
# ═══════════════════════════════════════════════════════════

def format_keyframe_report(requests: List[KeyFrameRequest]) -> str:
    """格式化关键帧需求报告"""
    if not requests:
        return "📷 关键帧分析：无需额外画面辅助"

    lines = [
        f"📷 关键帧分析（{len(requests)} 个需求点）",
        "",
    ]

    for i, req in enumerate(requests, 1):
        ts_min = int(req.timestamp // 60)
        ts_sec = int(req.timestamp % 60)
        trigger_label = KeyFrameTrigger.LABELS.get(req.trigger, req.trigger)
        priority_icon = "🔴" if req.priority > 0.7 else "🟡" if req.priority > 0.4 else "🟢"

        lines.append(f"{i}. [{ts_min:02d}:{ts_sec:02d}] {priority_icon} {trigger_label}")
        lines.append(f"   原因: {req.reason}")
        if req.quoted_text:
            lines.append(f"   原文: \"{req.quoted_text[:80]}...\"")
        if req.expected_content:
            lines.append(f"   期望: {req.expected_content}")
        lines.append("")

    return "\n".join(lines)
