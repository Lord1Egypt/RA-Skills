"""
P2 触发决策引擎 — 六维动态阈值

评估是否值得对残留犹豫词做重转录（双模型交叉验证）。
从固定的 `len(unresolved) >= 3` 升级为动态决策。

六维公式:

    有效权重 = 犹豫词占比 × 类型权重 ÷ (领域系数 × 说话人系数 × 位置权重 × 音质系数)
    触发条件: 有效权重 > 动态阈值(默认0.05%)
"""

from __future__ import annotations

import os
import math
from typing import Dict, List, Optional, Tuple

# ── 语音/助词/填充词（这些词即使猜错也不影响核心信息） ──
FILLER_WORDS = {
    "嗯", "啊", "呃", "哦", "嘛", "啦", "哇", "哎", "哟",
    "这个", "那个", "就是", "然后", "那个啥", "就", "还",
    "的话", "那个", "应该", "可能", "大概", "好像", "差不多",
    "我们", "你们", "他们", "咱们",
    "是吧", "对吧", "好吧", "好了", "对", "好",
}

# ── 普通过渡/非关键实体（语境相关但不构成独立概念） ──
COMMON_WORDS = set()


def _has_chinese(s: str) -> bool:
    """检测是否包含中文字符"""
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def _classify_word(word: str) -> str:
    """将犹豫词分为三类: filler / common / proper
    
    - filler: 填充词、语气词，猜错影响极小
    - common: 常见名词/动词，猜错影响有限
    - proper: 专有名词、技术术语、人名、工具名 → 猜错可能丢信息
    
    注意事项:
    - 中文2字词（止损、交易、策略）不等同于填充词
    - 英文词用字母数和大小写判断
    """
    if not word:
        return "filler"
    
    word_clean = word.strip("【】[]（）()《》【】『』「」\"'").strip()
    if not word_clean:
        return "filler"
    
    word_lower = word_clean.lower()
    
    # 填充词字典
    if word_lower in FILLER_WORDS:
        return "filler"
    
    # 中文字符处理
    if _has_chinese(word_clean):
        # 中文单字: 很可能是语气词（嗯、啊、对）
        if len(word_clean) <= 1:
            return "filler"
        # 中文2字词: 不能一概而论，大部分是实词
        if len(word_clean) == 2:
            return "common"  # 止损、交易、策略等，猜错有影响但不致命
        # 中文长词: 通常是术语/概念
        return "proper"
    
    # 英文/混合处理
    # 专有名词特征：首字母大写（英文）
    if any(c.isupper() for c in word_clean[1:]) if word_clean else False:
        return "proper"
    
    # 含特殊字符（工具名、产品名特征）
    if any(c in word_clean for c in "_-/\\@"):
        return "proper"
    
    # 长英文词: 通常是术语/专有名词
    if len(word_clean) >= 6:
        return "proper"
    
    # 很短的英文词: 介词/代词/连词等常见词
    if len(word_clean) <= 2:
        return "filler"
    
    # 默认保守: 未知词当专有名词
    return "proper"


def _type_weight(word: str) -> float:
    """犹豫词的类型权重
    
    - proper (专有名词): 1.0 — 猜错可能丢关键信息
    - common (普通词): 0.5 — 影响有限
    - filler (填充词): 0.1 — 猜错无所谓
    """
    t = _classify_word(word)
    return {"proper": 1.0, "common": 0.5, "filler": 0.1}[t]


def _domain_coefficient(domain_hint: str, uploader: str,
                        knowledge_dir: str) -> float:
    """领域熟识度系数
    
    依靠知识库中该领域的条目数判断。
    越熟越容忍（系数大），越新越敏感（系数小）。
    
    Returns: 0.3 ~ 2.0
    """
    total_entries = 0
    
    # 按上传者名匹配
    if uploader:
        try:
            kd = knowledge_dir or os.path.expanduser(
                "~/openclaw/workspace/biliyoutik2brain/knowledge")
            if os.path.isdir(kd):
                for fname in os.listdir(kd):
                    if uploader.lower() in fname.lower() or \
                       (domain_hint and domain_hint.lower() in fname.lower()):
                        try:
                            total_entries += 1  # 每个匹配文件算一条
                        except Exception:
                            pass
        except Exception:
            pass
    
    # sigmoid 映射: 0条目→0.5, 10条目→1.0, 50条目→1.8
    x = total_entries / 10.0
    coeff = 1.0 / (1.0 + math.exp(-x + 0.5)) * 1.7 + 0.3
    return round(min(2.0, max(0.3, coeff)), 2)


def _speaker_coefficient(uploader: str,
                         speaker_knowledge_dir: str) -> float:
    """说话人熟识度 — 基于UP主历史视频数
    
    Returns: 0.3 ~ 2.0
    """
    video_count = 0
    
    if uploader:
        skd = speaker_knowledge_dir or os.path.expanduser(
            "~/openclaw/workspace/storage")
        try:
            if os.path.isdir(skd):
                base = uploader.split("/")[-1].strip()
                transcript_dir = os.path.join(skd, "transcripts")
                if os.path.isdir(transcript_dir):
                    for fname in os.listdir(transcript_dir):
                        if fname.lower().startswith(base.lower()):
                            video_count += 1
        except Exception:
            pass
    
    # sigmoid: 0视频→0.3, 5视频→0.8, 20视频→1.5, 50视频→1.9
    x = video_count / 5.0
    coeff = 1.0 / (1.0 + math.exp(-x + 0.5)) * 1.7 + 0.3
    return round(min(2.0, max(0.3, coeff)), 2)


def _position_weight(unresolved_words: List[str],
                     speech_segments: List[Dict],
                     chapters: Optional[List[Dict]] = None) -> float:
    """位置权重
    
    核心段（中间段） = 1.0
    开头/结尾 = 0.3 (寒暄/总结段通常不丢信息)
    
    如果无章节信息，按说话段分布猜段落: 
    - 第一个说话段（开头）: 权重0.3
    - 最后一个说话段（结尾）: 权重0.3
    - 中间段: 权重1.0
    
    Returns: 0.3 ~ 1.0
    """
    if not speech_segments or len(speech_segments) <= 1:
        return 1.0
    
    # 简化: 默认中段 = 1.0
    # 如果大多数犹豫词出现在首/末段，降低权重
    total_segments = len(speech_segments)
    first_range = range(int(speech_segments[0]["start"]),
                        int(speech_segments[0]["end"]))
    last_range = range(int(speech_segments[-1]["start"]),
                       int(speech_segments[-1]["end"]))
    
    # 我们没有每个犹豫词的具体时间位置，无法精准定位
    # 保守起见: 返回1.0（认为所有犹豫词都可能重要）
    # 后续可精进
    return 1.0


def _quality_coefficient(avg_quality: float) -> float:
    """音质系数
    
    音质分0~1，越低音质越好（转录置信度高）。
    音质差的视频犹豫词多的概率大，阈值放宽不折腾。
    
    Returns: 0.5 ~ 1.5
        - 音质好 (>=0.6): 系数1.0 (正常)，犹豫词少但出现了就是真有问题
        - 音质差 (<0.4): 系数0.5 (更容忍)，犹豫词多是常态不值得逐字核
    """
    if avg_quality <= 0:
        return 0.5  # 无音质数据，保守容忍
    if avg_quality >= 0.6:
        return 1.0  # 音质好 → 正常触发
    # 中间线性
    return round(0.5 + (avg_quality - 0.0) / 0.6 * 0.5, 2)


def should_retranscribe(
    unresolved_words: List[str],
    total_chars: int,
    speech_segments: List[Dict],
    avg_quality: float,
    domain_hint: str = "",
    uploader: str = "",
    chapters: Optional[List[Dict]] = None,
    knowledge_dir: str = "",
    speaker_knowledge_dir: str = "",
    base_threshold: float = 0.05,
) -> Tuple[bool, Dict]:
    """六维动态阈值决策
    
    Args:
        unresolved_words: L5残留的犹豫词列表
        total_chars: 转录总字数
        speech_segments: 说话段地图 [{start, end, duration}]
        avg_quality: assess阶段测到的平均音质 (0~1)
        domain_hint: 领域提示（assess阶段自动推断）
        uploader: UP主名
        chapters: 章节划分（来自结构化分析）
        base_threshold: 默认触发阈值 (%)，0.05 = 0.05%
    
    Returns:
        (should_trigger: bool, debug: Dict)
    """
    if not unresolved_words or total_chars <= 0:
        return False, {"reason": "no unresolved words or empty text", "trigger": 0.0}
    
    # 维度①: 比例
    ratio = len(unresolved_words) / total_chars * 100  # 百分比
    if ratio == 0:
        return False, {"reason": "ratio=0", "trigger": 0.0}
    
    # 维度②: 类型权重 — 取均值
    type_weights = [_type_weight(w) for w in unresolved_words]
    type_weight = sum(type_weights) / len(type_weights)
    
    # 按类型分解
    proper_count = sum(1 for tw in type_weights if tw >= 1.0)
    
    # 维度③: 领域系数
    domain_coeff = _domain_coefficient(domain_hint, uploader, knowledge_dir)
    
    # 维度④: 说话人系数
    speaker_coeff = _speaker_coefficient(uploader, speaker_knowledge_dir)
    
    # 维度⑤: 位置权重
    position_weight = _position_weight(unresolved_words, speech_segments, chapters)
    
    # 维度⑥: 音质系数
    quality_coeff = _quality_coefficient(avg_quality)
    
    # 合成决策值
    if domain_coeff <= 0 or speaker_coeff <= 0:
        return False, {"reason": "coefficient zero", "trigger": 0.0}
    
    effective = (ratio * type_weight) / (domain_coeff * speaker_coeff * position_weight * quality_coeff)
    
    trigger = effective > base_threshold
    
    debug = {
        "ratio": round(ratio, 4),
        "type_weight": round(type_weight, 2),
        "proper_count": proper_count,
        "domain_coeff": domain_coeff,
        "speaker_coeff": speaker_coeff,
        "position_weight": position_weight,
        "quality_coeff": quality_coeff,
        "effective": round(effective, 4),
        "threshold": base_threshold,
        "should_trigger": trigger,
        "unresolved_words": unresolved_words,
    }
    
    return trigger, debug
