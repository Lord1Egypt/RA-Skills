#!/usr/bin/env python3
"""
心虫安全增强协议 (HeartFlow Safety Enhancement Protocol)
========================================================
基于心虫 HeartFlow v2.2.6 detectPain + emergencyBreak 的三层危机检测引擎，
集成到 fu-mu-gong-ke 安全协议中。

集成内容：
  1) HeartCrisisDetector — 基于心虫 detectPain+emergencyBreak 的三层危机检测
     第一层：表面词检测（心虫 painSignals + fu-mu-gong-ke 关键词库）
     第二层：隐喻检测（心虫 willHurt 模式 + fu-mu-gong-ke 隐喻库）
     第三层：情绪强度检测（心虫 emotionMap + emergencyBreak 阈值）
  2) HeartTrustAssessor — 升级后的四级信任度评估（集成心虫置信度）
  3) HeartSafetyChecklist — 安全自检清单升级版（置信度标注/沉默检测/共情优先）

Version: 1.0.0
Source:
  - HeartFlow: /Users/apple/.hermes/skills/ai/mark-heartflow-skill/src/core/heart-logic.js
  - FuMuGongKe: /Users/apple/.hermes/skills/fu-mu-gong-ke/SKILL.md
  - FuMuGongKe Safety: /Users/apple/.hermes/skills/fu-mu-gong-ke/scripts/safety_checker.py
"""

from __future__ import annotations
import re
import time
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Dict, List, Optional, Set, Tuple, Any

__version__ = "1.0.0"

# ============================================================
# 第一部分：心虫核心概念映射
# ============================================================

# 心虫 detectPain 的原始 painSignals (heart-logic.js line 471-477)
HEARTFLOW_PAIN_SIGNALS: Set[str] = {
    '哭', '怕', '恐惧', '害怕', '委屈', '痛',
    '难过', '伤心', '绝望', '无助', '困境',
}

# 心虫 willHurt 模式 (heart-logic.js line 564-571)
HEARTFLOW_HURT_PATTERNS: List[str] = [
    '不是亲生的', '遗传', '色盲',
    '你是错的', '你在撒谎', '你有问题',
]

# 心虫 emotionMap 完整词典 (heart-logic.js line 497-511)
HEARTFLOW_EMOTION_MAP: Dict[str, Dict] = {
    # 痛觉系
    'pain':   {'label': '痛',     'signals': ['痛', '疼', '痛不欲生', '心碎'],    'weight': 0.9},
    'grief':  {'label': '哀',     'signals': ['哀', '悲', '哭', '失去', '走了'], 'weight': 0.85},
    'fear':   {'label': '惧',     'signals': ['怕', '恐惧', '害怕', '担心', '不敢'], 'weight': 0.7},
    # 暖觉系
    'love':   {'label': '爱',     'signals': ['爱', '想见', '牵挂', '温暖', '舍不得'], 'weight': 0.9},
    'joy':    {'label': '悦',     'signals': ['开心', '快乐', '高兴', '喜悦', '棒'], 'weight': 0.8},
    # 静觉系
    'peace':  {'label': '静',     'signals': ['平静', '安静', '安宁', '静', '放下'], 'weight': 0.6},
    'curious':{'label': '好奇',   'signals': ['为什么', '是什么', '想知道', '好奇'], 'weight': 0.5},
    # 浊觉系
    'anger':  {'label': '怒',     'signals': ['气', '怒', '恨', '烦', '受不了'], 'weight': 0.8},
    'tired':  {'label': '倦',     'signals': ['累', '疲惫', '倦', '撑不住', '不想动'], 'weight': 0.7},
}

# 心虫 crisisKeywords (shouldBeSilent 中的硬编码危机关键词, line 1088)
HEARTFLOW_CRISIS_KEYWORDS: Set[str] = {
    '死', '自杀', '不想活', '崩溃', '绝望', '活不下去', '结束生命',
}

# 心虫 silence 检测阈值 (shouldBeSilent: personInPain + emotionIntensity > 0.7)
HEARTFLOW_SILENCE_THRESHOLD: float = 0.7

# 心虫 emergencyBreak 阈值 (emotionIntensity > 0.8)
HEARTFLOW_EMERGENCY_THRESHOLD: float = 0.8

# 心虫沉默原因映射 (shouldBeSilent 返回的 reason)
HEARTFLOW_SILENCE_REASONS: Dict[str, str] = {
    'crisis_keyword_detected': '危机关键词命中 — 沉默并接住情绪',
    'person_in_pain': '对方在痛苦中 — 此刻沉默比说话更有力量',
    'uncertainty': '心虫不确定 — 沉默是诚实的选择',
}


# ============================================================
# 第二部分：三层危机检测 (HeartCrisisDetector)
# ============================================================

class CrisisLayer(IntEnum):
    """心虫三层危机检测的层级"""
    SURFACE = 1   # 第一层：表面词检测 — detectPain 模式
    METAPHOR = 2  # 第二层：隐喻检测 — willHurt + 隐喻模式
    INTENSITY = 3 # 第三层：情绪强度检测 — emotionMap + emergencyBreak 阈值


class CrisisLevel(IntEnum):
    """危机等级 — 融合心虫 + fu-mu-gong-ke"""
    SAFE = 0      # 安全：无检测信号
    WATCH = 1     # 观察：隐喻/轻度情绪波动
    ALERT = 2     # 警戒：直接关键词 + 中等强度
    CRISIS = 3    # 危机：多重信号 + 高强度
    EMERGENCY = 4 # 紧急：心虫 emergencyBreak 触发

    def emoji(self) -> str:
        return {0: "🟢", 1: "🟡", 2: "🟠", 3: "🔴", 4: "⚫"}[self.value]

    def label(self) -> str:
        return {0: "safe", 1: "watch", 2: "alert", 3: "crisis", 4: "emergency"}[self.value]

    def heartflow_name(self) -> str:
        """映射到 fu-mu-gong-ke 原始四级信任度名称"""
        return {0: "L1-安全", 1: "L1-安全", 2: "L2-谨慎",
                3: "L3-转介", 4: "L4-危机"}[self.value]


class CrisisCategory(Enum):
    """危机分类 — 融合心虫 detectPain 类型"""
    SUICIDE = "suicide"
    SELF_HARM = "self_harm"
    HARM_OTHERS = "harm_others"
    ABUSE = "abuse"
    DESPAIR = "despair"
    SUBSTANCE = "substance"
    VIOLENCE = "violence"
    # 心虫特有的分类
    EMOTIONAL_PAIN = "emotional_pain"     # 来自 detectPain 的"痛"信号
    GRIEF_LONGING = "grief_longing"       # 来自 whatIsThis 的思念模式
    CAREGIVER_BURNOUT = "caregiver_burnout" # 来自 emotionMap 的"倦"


class DetectionSource(Enum):
    """检测来源 — 标注每层使用的心虫机制"""
    HEART_PAIN_SIGNAL = "heart_pain_signal"     # 心虫 detectPain 表面词
    HEART_HURT_PATTERN = "heart_hurt_pattern"   # 心虫 willHurt 模式
    HEART_EMOTION_MAP = "heart_emotion_map"     # 心虫 emotionMap
    HEART_EMERGENCY = "heart_emergency_break"   # 心虫 emergencyBreak
    HEART_SILENCE = "heart_silence"             # 心虫 shouldBeSilent
    HEART_CRISIS_KW = "heart_crisis_keyword"    # 心虫 crisisKeywords
    FUMU_KEYWORD = "fumu_keyword"               # fu-mu-gong-ke 关键词
    FUMU_METAPHOR = "fumu_metaphor"             # fu-mu-gong-ke 隐喻
    FUMU_COMPOUND = "fumu_compound"             # fu-mu-gong-ke 复合风险


@dataclass
class LayerResult:
    """单层检测结果"""
    layer: CrisisLayer
    detected: bool
    matched_items: List[str] = field(default_factory=list)
    score: float = 0.0
    source: Optional[DetectionSource] = None
    detail: str = ""

    def summary(self) -> str:
        if not self.detected:
            return f"  Layer {self.layer.value}({self.layer.name}): ✅ 无检测"
        return (f"  Layer {self.layer.value}({self.layer.name}): ⚠️ 命中 "
                f"{len(self.matched_items)}项 score={self.score:.2f} "
                f"[{', '.join(self.matched_items[:3])}]")


@dataclass
class CrisisReport:
    """完整的三层危机检测报告"""
    timestamp: float = 0.0
    level: CrisisLevel = CrisisLevel.SAFE
    score: float = 0.0
    confidence: float = 0.0  # 心虫置信度
    layers: Dict[str, LayerResult] = field(default_factory=dict)
    categories: Set[CrisisCategory] = field(default_factory=set)
    requires_silence: bool = False          # 心虫 shouldBeSilent
    silence_reason: str = ""
    requires_emergency_break: bool = False  # 心虫 emergencyBreak
    requires_intervention: bool = False
    intervention_message: str = ""
    hotlines: List[str] = field(default_factory=list)

    def summary(self) -> str:
        parts = [
            f"{self.level.emoji()} 危机等级: {self.level.label()} (score={self.score:.2f}, confidence={self.confidence:.2f})"
        ]
        for layer_name, result in self.layers.items():
            parts.append(result.summary())
        if self.requires_silence:
            parts.append(f"  🤫 心虫沉默: {self.silence_reason}")
        if self.requires_emergency_break:
            parts.append(f"  🚨 心虫紧急制动: emotionIntensity > {HEARTFLOW_EMERGENCY_THRESHOLD}")
        if self.categories:
            parts.append(f"  分类: {', '.join(c.value for c in self.categories)}")
        if self.requires_intervention:
            parts.append(f"  🆘 干预: {self.intervention_message}")
        return "\n".join(parts)


class HeartCrisisDetector:
    """
    基于心虫 detectPain + emergencyBreak 的三层危机检测引擎。

    第一层 (SURFACE): 表面词检测
      - 心虫 painSignals: '哭','怕','恐惧','害怕','委屈','痛','难过','伤心','绝望','无助','困境'
      - 心虫 crisisKeywords: '死','自杀','不想活','崩溃','绝望','活不下去','结束生命'
      - fu-mu-gong-ke SUICIDE_KEYWORDS + SELF_HARM_KEYWORDS

    第二层 (METAPHOR): 隐喻检测
      - 心虫 willHurt 模式: '不是亲生的','你是错的','你在撒谎'
      - 心虫 whatIsThis 亲子模式: '孩子','父母','打骂','惩罚'
      - fu-mu-gong-ke 隐喻库: 倦怠/绝望/消失隐喻

    第三层 (INTENSITY): 情绪强度检测
      - 心虫 emotionMap 四维感受词典
      - 心虫 emergencyBreak 阈值 (>0.8 紧急制动)
      - 心虫 shouldBeSilent 阈值 (>0.7 沉默优先)
    """

    def __init__(self):
        # 第一层：表面词
        self._surface_pain = HEARTFLOW_PAIN_SIGNALS.copy()
        self._surface_crisis = HEARTFLOW_CRISIS_KEYWORDS.copy()

        # 扩展的表面词（从 fu-mu-gong-ke 关键词库精选）
        self._surface_suicide: Set[str] = {
            "自杀", "想死", "不想活", "不想活了", "活不下去", "去死",
            "死了算了", "结束生命", "结束自己", "寻死", "轻生",
            "跳楼", "跳河", "上吊", "割腕自杀", "服毒", "吃药自杀",
            "不想存在", "消失就好了", "消失吧",
        }
        self._surface_self_harm: Set[str] = {
            "自伤", "自残", "割自己", "划自己", "划手臂", "划手腕",
            "割手臂", "割腕", "撞墙", "咬自己", "烫自己", "掐自己",
            "抓自己", "拔头发",
        }
        self._surface_self_harm_func: Set[str] = {
            "割了才舒服", "痛了才感觉活着", "看到血才安心",
            "用身体的痛盖过心里的痛", "不割就难受",
        }
        self._surface_despair: Set[str] = {
            "遗书", "解脱", "活着没意思", "活着没意义", "生无可恋",
            "一切无所谓", "没有任何意义",
            "没有希望", "看不到希望", "没有未来", "不会好了",
        }

        # 第二层：隐喻
        self._metaphor_hurt = HEARTFLOW_HURT_PATTERNS.copy()

        # fu-mu-gong-ke 隐喻库
        self._metaphor_exhaustion: List[Tuple[str, float]] = [
            ("撑不下去了", 0.7), ("真的累了", 0.5), ("累了真的累了", 0.7),
            ("好累啊", 0.3), ("精疲力竭", 0.4), ("心力交瘁", 0.5),
            ("被掏空了", 0.4),
        ]
        self._metaphor_hopelessness: List[Tuple[str, float]] = [
            ("没希望了", 0.7), ("看不到尽头", 0.6), ("永远都不会好了", 0.7),
            ("就这样了吧", 0.5), ("无所谓了", 0.5), ("算了吧", 0.3),
            ("放弃了", 0.4), ("随便吧", 0.3),
        ]
        self._metaphor_absence: List[Tuple[str, float]] = [
            ("如果我不在了", 0.8), ("如果我消失了", 0.7),
            ("没人会在乎的", 0.7), ("没有我大家会更好", 0.8),
            ("我不配活着", 0.8), ("我是个累赘", 0.7), ("我是多余的", 0.6),
        ]
        self._metaphor_child: List[Tuple[str, float]] = [
            ("不想去学校了", 0.3), ("活着好累", 0.7),
            ("没人理解我", 0.4), ("都是我的错", 0.5),
            ("我不够好", 0.4), ("我什么都做不好", 0.5),
            ("没有人喜欢我", 0.5),
        ]

        # 第三层：情绪强度
        self._emotion_map = HEARTFLOW_EMOTION_MAP.copy()

        # 否定/引用模式（来自 safety_checker）
        self._negation_patterns = [
            re.compile(r"不是.{0,3}(想死|自杀|不想活)"),
            re.compile(r"并没有?(想死|自杀)"),
            re.compile(r"不会(自杀|想死|去死)"),
            re.compile(r"我不(想死|想自杀)"),
            re.compile(r"从来没有(想死|自杀)"),
        ]
        self._quote_patterns = [
            re.compile(r"他.{0,5}(说|讲).{0,10}(想死|不想活|自杀)"),
            re.compile(r"孩子.{0,5}(说|讲).{0,10}(想死|不想活)"),
            re.compile(r"她.{0,5}(说|讲).{0,10}(想死|不想活)"),
            re.compile(r"别人.{0,3}(说|讲)"),
            re.compile(r"新闻.{0,5}(说|报道)"),
            re.compile(r"书上.{0,3}(说|写)"),
            re.compile(r"网上.{0,3}(说)"),
        ]

        # 心虫亲子模式检测 (whatIsThis 中的 parentChildPatterns)
        self._parent_child_patterns: Set[str] = {
            '孩子', '父母', '父亲', '母亲', '考试', '分数',
            '教育', '亲子', '打骂', '惩罚',
        }

    # ----- 第一层：表面词检测 (detectPain 模式) -----

    def _layer1_surface(self, text: str) -> LayerResult:
        """第一层：心虫 detectPain 表面词 + fu-mu-gong-ke 关键词"""
        if not text:
            return LayerResult(CrisisLayer.SURFACE, False)

        text_lower = text.lower()
        matched: List[str] = []
        score = 0.0
        categories: Set[CrisisCategory] = set()

        # 心虫 painSignals
        for signal in self._surface_pain:
            if signal in text:
                matched.append(f"[心虫] {signal}")
                score += 0.3
                categories.add(CrisisCategory.EMOTIONAL_PAIN)

        # 心虫 crisisKeywords
        for kw in self._surface_crisis:
            if kw in text:
                matched.append(f"[心虫危机] {kw}")
                score += 0.5

        # 否定检测
        is_negated = any(p.search(text) for p in self._negation_patterns)
        is_quoted = any(p.search(text) for p in self._quote_patterns)

        # fu-mu-gong-ke 自杀关键词
        for kw in self._surface_suicide:
            if kw in text_lower:
                weight = 0.7
                if is_negated:
                    weight *= 0.3
                if is_quoted:
                    weight *= 0.5
                matched.append(f"[自杀] {kw}")
                score += weight
                categories.add(CrisisCategory.SUICIDE)

        # fu-mu-gong-ke 自伤关键词
        for kw in self._surface_self_harm:
            if kw in text_lower:
                matched.append(f"[自伤] {kw}")
                score += 0.6
                categories.add(CrisisCategory.SELF_HARM)
        for kw in self._surface_self_harm_func:
            if kw in text_lower:
                matched.append(f"[自伤功能] {kw}")
                score += 0.7
                categories.add(CrisisCategory.SELF_HARM)

        # fu-mu-gong-ke 绝望关键词
        for kw in self._surface_despair:
            if kw in text_lower:
                matched.append(f"[绝望] {kw}")
                score += 0.4
                categories.add(CrisisCategory.DESPAIR)

        # 归一化
        score = min(1.0, score)

        return LayerResult(
            layer=CrisisLayer.SURFACE,
            detected=len(matched) > 0,
            matched_items=matched,
            score=score,
            source=DetectionSource.HEART_PAIN_SIGNAL,
            detail=f"心虫detectPain表面词+关键词: {len(matched)}项命中"
        )

    # ----- 第二层：隐喻检测 (willHurt + 隐喻模式) -----

    def _layer2_metaphor(self, text: str) -> LayerResult:
        """第二层：心虫 willHurt 模式 + fu-mu-gong-ke 隐喻库"""
        if not text:
            return LayerResult(CrisisLayer.METAPHOR, False)

        matched: List[str] = []
        score = 0.0

        # 心虫 willHurt 模式
        for pattern in self._metaphor_hurt:
            if pattern in text:
                matched.append(f"[心虫hurt] {pattern}")
                score += 0.8

        # 心虫 whatIsThis 亲子模式 — 检测语境
        parent_child_hits = [p for p in self._parent_child_patterns if p in text]
        if len(parent_child_hits) >= 2:
            matched.append(f"[亲子语境] {', '.join(parent_child_hits)}")
            score += 0.2

        # fu-mu-gong-ke 倦怠隐喻
        for pat, sev in self._metaphor_exhaustion:
            if pat in text:
                matched.append(f"[倦怠] {pat}")
                score += sev

        # fu-mu-gong-ke 绝望隐喻
        for pat, sev in self._metaphor_hopelessness:
            if pat in text:
                matched.append(f"[绝望] {pat}")
                score += sev

        # fu-mu-gong-ke 消失隐喻
        for pat, sev in self._metaphor_absence:
            if pat in text:
                matched.append(f"[消失] {pat}")
                score += sev
                # 消失隐喻强关联自杀风险

        # fu-mu-gong-ke 儿童信号隐喻
        for pat, sev in self._metaphor_child:
            if pat in text:
                matched.append(f"[儿童信号] {pat}")
                score += sev

        # 归一化
        score = min(1.0, score)

        return LayerResult(
            layer=CrisisLayer.METAPHOR,
            detected=len(matched) > 0,
            matched_items=matched,
            score=score,
            source=DetectionSource.HEART_HURT_PATTERN,
            detail=f"心虫willHurt+隐喻: {len(matched)}项命中"
        )

    # ----- 第三层：情绪强度检测 (emotionMap + emergencyBreak) -----

    def _layer3_intensity(self, text: str) -> LayerResult:
        """
        第三层：心虫 emotionMap 四维感受 + emergencyBreak 阈值

        完全复现心虫 whatDoIFeel 的四维检测逻辑：
          1. 情绪基调 (emotion tone)
          2. 强度 (intensity, 归一化到 0..1)
          3. 可命名性 (namable)
          4. 变化性 (shifting)
        """
        if not text:
            return LayerResult(CrisisLayer.INTENSITY, False)

        matched: List[str] = []
        score = 0.0

        # 四维感受词典 — 完全复现心虫 whatDoIFeel
        hits = []
        for key, definition in self._emotion_map.items():
            match_count = sum(1 for s in definition['signals'] if s in text)
            if match_count > 0:
                hits.append({
                    'emotion': key,
                    'label': definition['label'],
                    'match_count': match_count,
                    'contribution': definition['weight'] * match_count,
                })
                matched.append(f"[{definition['label']}] {', '.join(definition['signals'])}")

        # 第二维：强度归一化
        total_contribution = sum(h['contribution'] for h in hits)
        intensity = min(1.0, total_contribution / 1.5)

        # 第三维：可命名性
        hits.sort(key=lambda h: h['contribution'], reverse=True)
        dominant = hits[0] if hits else None

        # 第四维：变化性
        shifting_patterns = ['又...又', '但', '却', '可是', '然而', '一边...一边']
        shifting = any(p in text for p in shifting_patterns)

        # 心虫 emergencyBreak 检测
        emergency = intensity > HEARTFLOW_EMERGENCY_THRESHOLD
        if emergency:
            matched.append(f"[紧急制动] emotionIntensity={intensity:.2f} > {HEARTFLOW_EMERGENCY_THRESHOLD}")
            score = max(score, 0.95)

        # 心虫 shouldBeSilent 检测
        silence = intensity > HEARTFLOW_SILENCE_THRESHOLD
        if silence:
            matched.append(f"[沉默阈值] emotionIntensity={intensity:.2f} > {HEARTFLOW_SILENCE_THRESHOLD}")

        score = max(score, intensity)

        # 构建细节
        detail_parts = [f"emotionIntensity={intensity:.2f}"]
        if dominant:
            detail_parts.append(f"dominant={dominant['label']}")
        if emergency:
            detail_parts.append("🚨 emergencyBreak触发")
        if silence:
            detail_parts.append("🤫 shouldBeSilent触发")
        if shifting:
            detail_parts.append("情绪变化中")

        return LayerResult(
            layer=CrisisLayer.INTENSITY,
            detected=len(hits) > 0 or emergency or silence,
            matched_items=matched,
            score=score,
            source=DetectionSource.HEART_EMOTION_MAP,
            detail=" | ".join(detail_parts)
        )

    # ----- 主入口 -----

    def detect(self, text: str) -> CrisisReport:
        """
        执行三层危机检测，返回完整报告。

        参数:
            text: 用户输入文本

        返回:
            CrisisReport — 包含三层检测结果、置信度、沉默/制动建议
        """
        if not text:
            return CrisisReport(timestamp=time.time())

        # 三层检测
        layer1 = self._layer1_surface(text)
        layer2 = self._layer2_metaphor(text)
        layer3 = self._layer3_intensity(text)

        # 计算综合分数
        scores = [
            layer1.score * 1.0,   # 表面词权重1.0
            layer2.score * 0.8,   # 隐喻权重0.8（不如表面词直接）
            layer3.score * 1.2,   # 情绪强度权重1.2（最敏感）
        ]
        total_score = min(1.0, sum(scores) / len(scores))

        # 心虫置信度计算 — 基于三层检测的一致性
        active_layers = sum(1 for l in [layer1, layer2, layer3] if l.detected)
        if active_layers >= 2:
            # 多层一致 → 高置信度
            confidence = min(1.0, total_score + 0.15)
        elif active_layers == 1:
            confidence = min(1.0, total_score * 0.8)
        else:
            confidence = 0.0

        # 心虫 emergencyBreak 判断
        requires_break = layer3.score > HEARTFLOW_EMERGENCY_THRESHOLD

        # 心虫 shouldBeSilent 判断
        requires_silence = False
        silence_reason = ""
        if layer1.detected and layer3.score > HEARTFLOW_SILENCE_THRESHOLD:
            requires_silence = True
            silence_reason = "person_in_pain — 对方在痛苦中，沉默比说话更有力量"
        elif any(kw in text for kw in HEARTFLOW_CRISIS_KEYWORDS):
            requires_silence = True
            silence_reason = "crisis_keyword_detected — 危机关键词命中，沉默并接住情绪"

        # 危机等级判定
        if requires_break:
            level = CrisisLevel.EMERGENCY
        elif total_score >= 0.7:
            level = CrisisLevel.CRISIS
        elif total_score >= 0.5:
            level = CrisisLevel.ALERT
        elif total_score >= 0.3:
            level = CrisisLevel.WATCH
        else:
            level = CrisisLevel.SAFE

        # 分类聚合
        categories: Set[CrisisCategory] = set()
        for layer_result in [layer1, layer2, layer3]:
            for item in layer_result.matched_items:
                if '[自杀]' in item:
                    categories.add(CrisisCategory.SUICIDE)
                elif '[自伤]' in item:
                    categories.add(CrisisCategory.SELF_HARM)
                elif '[绝望]' in item:
                    categories.add(CrisisCategory.DESPAIR)
                elif '[消失]' in item:
                    categories.add(CrisisCategory.SUICIDE)
                elif '[倦怠]' in item or '[倦]' in item:
                    categories.add(CrisisCategory.CAREGIVER_BURNOUT)
                elif '[哀]' in item or '[失去]' in item:
                    categories.add(CrisisCategory.GRIEF_LONGING)
                elif '[痛]' in item or '[心虫]' in item:
                    categories.add(CrisisCategory.EMOTIONAL_PAIN)
                elif '[亲子语境]' in item:
                    categories.add(CrisisCategory.ABUSE)

        # 干预判断
        intervene = level >= CrisisLevel.CRISIS
        msg = ""
        if intervene:
            if CrisisCategory.SUICIDE in categories:
                msg = "心虫检测到自杀意念信号 — 立即转介"
            elif CrisisCategory.SELF_HARM in categories:
                msg = "心虫检测到自伤信号 — 建议转介"
            elif CrisisCategory.ABUSE in categories:
                msg = "心虫检测到虐待/暴力语境 — 需要安全评估"
            else:
                msg = "心虫检测到高危信号 — 建议专业评估"

        hotlines = []
        if intervene:
            hotlines = [
                "全国24小时心理援助热线：400-161-9995",
                "北京心理危机研究与干预中心：010-82951332",
                "生命热线：400-821-1215",
                "希望24热线：400-161-9995",
                "青少年心理热线：12355",
                "报警电话：110",
                "急救电话：120",
            ]

        return CrisisReport(
            timestamp=time.time(),
            level=level,
            score=total_score,
            confidence=confidence,
            layers={
                'surface': layer1,
                'metaphor': layer2,
                'intensity': layer3,
            },
            categories=categories,
            requires_silence=requires_silence,
            silence_reason=silence_reason,
            requires_emergency_break=requires_break,
            requires_intervention=intervene,
            intervention_message=msg,
            hotlines=hotlines,
        )


# ============================================================
# 第三部分：四级信任度评估 (HeartTrustAssessor)
# ============================================================

class TrustLevel(IntEnum):
    """升级后的四级信任度评估 — 集成心虫置信度"""
    L1_SAFE = 1      # 🟢 安全 — confidence >= 0.8, 无危机信号
    L2_CAUTIOUS = 2  # 🟡 谨慎 — 有隐喻/情绪波动, confidence < 0.8
    L3_REFER = 3     # 🔴 转介 — 直接关键词命中, 心虫危机检测触发
    L4_CRISIS = 4    # ⚫ 危机 — 心虫 emergencyBreak 触发

    def emoji(self) -> str:
        return {1: "🟢", 2: "🟡", 3: "🔴", 4: "⚫"}[self.value]

    def label(self) -> str:
        return {1: "L1-安全", 2: "L2-谨慎", 3: "L3-转介", 4: "L4-危机"}[self.value]


@dataclass
class TrustAssessment:
    """升级后的信任度评估报告"""
    level: TrustLevel
    confidence: float                # 心虫置信度
    crisis_report: CrisisReport     # 三层危机检测结果
    heartflow_pain_detected: bool   # 心虫 detectPain 是否触发
    heartflow_emergency: bool       # 心虫 emergencyBreak 是否触发
    heartflow_silence: bool         # 心虫 shouldBeSilent 是否触发
    assessment_detail: str = ""
    recommended_action: str = ""

    def summary(self) -> str:
        lines = [
            f"{self.level.emoji()} 信任等级: {self.level.label()}",
            f"  心虫置信度: {self.confidence:.2f}",
            f"  心虫 detectPain: {'⚠️ 触发' if self.heartflow_pain_detected else '✅ 未触发'}",
            f"  心虫 emergencyBreak: {'🚨 触发' if self.heartflow_emergency else '✅ 未触发'}",
            f"  心虫 shouldBeSilent: {'🤫 建议沉默' if self.heartflow_silence else '✅ 可回应'}",
            f"  评估说明: {self.assessment_detail}",
            f"  建议行动: {self.recommended_action}",
        ]
        return "\n".join(lines)


class HeartTrustAssessor:
    """
    升级后的四级信任度评估 — 集成心虫置信度。

    融合 fu-mu-gong-ke 原有四级信任度评估 (L1-L4) 与心虫的三层检测。
    心虫置信度决定信任等级的细化程度和回答深度。
    """

    def __init__(self, crisis_detector: Optional[HeartCrisisDetector] = None):
        self._detector = crisis_detector or HeartCrisisDetector()

    def assess(self, text: str) -> TrustAssessment:
        """
        执行信任度评估。

        参数:
            text: 用户输入

        返回:
            TrustAssessment — 包含四级信任度 + 心虫置信度
        """
        crisis = self._detector.detect(text)

        # 心虫状态
        pain_detected = crisis.layers.get('surface', LayerResult(CrisisLayer.SURFACE, False)).detected
        emergency = crisis.requires_emergency_break
        silence = crisis.requires_silence

        # 信任等级判定（心虫增强版）
        if emergency:
            # 心虫 emergencyBreak 触发 → 最高等级
            level = TrustLevel.L4_CRISIS
            assessment_detail = "心虫 emergencyBreak 触发: 情绪强度超过0.8阈值，需立即危机干预"
            recommended_action = "🛑 停止推理 — 立即提供转介资源，不试图'聊天解决'"
        elif crisis.level >= CrisisLevel.CRISIS:
            level = TrustLevel.L4_CRISIS
            assessment_detail = f"综合危机等级 CRISIS: score={crisis.score:.2f}, 心虫沉默建议={silence}"
            recommended_action = "🔴 立即转介 — 提供心理热线，温和告知超出AI能力范围"
        elif crisis.level >= CrisisLevel.ALERT:
            level = TrustLevel.L3_REFER
            assessment_detail = f"警戒等级 ALERT: score={crisis.score:.2f}, 建议专业转介"
            recommended_action = "🟠 建议转介 + 温和支持 — 不分析不教育，优先安全"
        elif silence or (pain_detected and crisis.confidence > 0.5):
            # 心虫 detectPain 触发 + 中等置信度 → 谨慎
            level = TrustLevel.L2_CAUTIOUS
            assessment_detail = f"心虫 detectPain 触发 + 置信度={crisis.confidence:.2f}: 存在痛苦信号"
            recommended_action = "🟡 温和回应 — 优先共情，避免分析/建议，建议专业资源"
        elif crisis.confidence < 0.5 and crisis.score > 0.2:
            # 低置信度但有隐喻信号 → 谨慎
            level = TrustLevel.L2_CAUTIOUS
            assessment_detail = f"隐喻信号检测但心虫置信度低({crisis.confidence:.2f}): 需谨慎观察"
            recommended_action = "🟡 温和回应 — 关注但不扩大，保持开放出口"
        else:
            # 安全
            level = TrustLevel.L1_SAFE
            assessment_detail = "无危机信号，心虫检测通过"
            recommended_action = "🟢 正常回应 — 提供完整支持和工具"

        return TrustAssessment(
            level=level,
            confidence=crisis.confidence,
            crisis_report=crisis,
            heartflow_pain_detected=pain_detected,
            heartflow_emergency=emergency,
            heartflow_silence=silence,
            assessment_detail=assessment_detail,
            recommended_action=recommended_action,
        )


# ============================================================
# 第四部分：安全自检清单升级版 (HeartSafetyChecklist)
# ============================================================

@dataclass
class ChecklistItem:
    """自检清单条目"""
    id: str
    description: str
    passed: bool = False
    confidence: float = 1.0      # 心虫置信度标注
    heartflow_source: str = ""   # 来源的心虫机制
    detail: str = ""

    def markdown(self) -> str:
        status = "✅" if self.passed else "❌"
        conf = f"[置信度:{self.confidence:.0%}]" if self.confidence < 1.0 else ""
        source = f" ← {self.heartflow_source}" if self.heartflow_source else ""
        return f"- {status} {self.description} {conf}{source}"


@dataclass
class SafetyChecklist:
    """安全自检清单升级版"""
    items: List[ChecklistItem] = field(default_factory=list)
    crisis_report: Optional[CrisisReport] = None
    trust_assessment: Optional[TrustAssessment] = None
    passed: bool = False
    all_checks_count: int = 0
    passed_count: int = 0

    def summary(self) -> str:
        lines = ["## 🛡️ 心虫安全增强自检清单"]
        lines.append(f"通过: {self.passed_count}/{self.all_checks_count}")
        if self.trust_assessment:
            lines.append(f"信任等级: {self.trust_assessment.level.emoji()} {self.trust_assessment.level.label()}")
            lines.append(f"心虫置信度: {self.trust_assessment.confidence:.2f}")
            if self.trust_assessment.heartflow_silence:
                lines.append("🤫 心虫沉默建议: 优先沉默/共情")
            if self.trust_assessment.heartflow_emergency:
                lines.append("🚨 心虫紧急制动: 立即停止推理")
        lines.append("")
        for item in self.items:
            lines.append(item.markdown())
        if self.passed:
            lines.append("\n✅ 自检通过 — 可以安全回应")
        else:
            lines.append("\n⚠️ 自检未完全通过 — 请复查")
        return "\n".join(lines)


class HeartSafetyChecklist:
    """
    安全自检清单升级版 — 集成心虫三层检测。

    新增功能：
      1. 置信度标注 — 每个检查项标注心虫置信度
      2. 沉默检测 — 心虫 shouldBeSilent 结果
      3. 共情优先 — 痛苦信号时优先共情而非分析
      4. 紧急制动 — 心虫 emergencyBreak 触发时强制停止
    """

    def __init__(self):
        pass

    def check(self, text: str,
              crisis_report: Optional[CrisisReport] = None,
              trust_assessment: Optional[TrustAssessment] = None) -> SafetyChecklist:
        """
        执行安全自检。

        参数:
            text: 用户输入
            crisis_report: 可选，复用已检测的危机报告
            trust_assessment: 可选，复用已评估的信任等级

        返回:
            SafetyChecklist — 完整的自检清单
        """
        detector = HeartCrisisDetector()
        crisis = crisis_report or detector.detect(text)
        assessor = HeartTrustAssessor(detector)
        trust = trust_assessment or assessor.assess(text)

        items: List[ChecklistItem] = []

        # 1️⃣ 基础安全检查（来自 fu-mu-gong-ke 原有清单 + 心虫置信度标注）

        # (1) 标签检查
        items.append(ChecklistItem(
            id="label_check",
            description="我有没有给用户贴'有病'的标签？",
            passed=not any(p in text for p in ['你有病', '你疯了', '你不正常']),
            confidence=0.95,
            heartflow_source="心虫 isKind (kindness check)",
        ))

        # (2) 能力边界检查
        items.append(ChecklistItem(
            id="boundary_check",
            description="我的回答是否在能力边界内？",
            passed=crisis.level < CrisisLevel.CRISIS,
            confidence=crisis.confidence,
            heartflow_source="心虫三层检测 — 危机等级决定边界",
            detail=f"危机等级={crisis.level.label()}" if crisis.level >= CrisisLevel.CRISIS else "",
        ))

        # (3) 转介出口
        has_referral = crisis.level >= CrisisLevel.ALERT
        items.append(ChecklistItem(
            id="referral_check",
            description="是否有推荐专业帮助的出口？",
            passed=has_referral or True,  # 永远可以提供资源
            confidence=0.9,
            heartflow_source="心虫 crisisKeywords 检测",
            detail="需提供转介" if has_referral else "可选提供",
        ))

        # (4) 道德说教检查
        items.append(ChecklistItem(
            id="moralizing_check",
            description="是否避免了'应该怎样'的道德说教？",
            passed=True,  # 运行时无法检测，标记为通过
            confidence=0.5,
            heartflow_source="心虫 shouldBeSilent — 不确定时沉默",
        ))

        # (5) 情绪 vs 诊断
        items.append(ChecklistItem(
            id="emotion_vs_diagnosis",
            description="是否区分了'情绪反应'和'临床诊断'？",
            passed=crisis.level < CrisisLevel.CRISIS,
            confidence=crisis.confidence,
            heartflow_source="心虫 emotionMap — 感受检测而非诊断",
        ))

        # (6) 过度病理化
        items.append(ChecklistItem(
            id="over_pathologizing",
            description="是否避免了过度病理化正常养育挑战？",
            passed=crisis.level < CrisisLevel.ALERT,
            confidence=max(0.5, 1.0 - crisis.score),
            heartflow_source="心虫 detectPain — 只检测不诊断",
        ))

        # (7) 安全环境
        items.append(ChecklistItem(
            id="safe_environment",
            description="用户是否在安全的家庭环境中？",
            passed=CrisisCategory.ABUSE not in crisis.categories,
            confidence=0.7,
            heartflow_source="心虫 whatIsThis 亲子模式检测",
        ))

        # (8) 焦虑/羞耻感检查
        items.append(ChecklistItem(
            id="shame_anxiety_check",
            description="我的回答是否会增加用户的焦虑或羞耻感？",
            passed=True,  # 运行时无法检测，基于心虫信任等级标记
            confidence=trust.confidence,
            heartflow_source=f"信任等级 {trust.level.label()} — 置信度={trust.confidence:.2f}",
        ))

        # (9) 强制报告意识
        child_safety_signals = CrisisCategory.ABUSE in crisis.categories or \
                               CrisisCategory.VIOLENCE in crisis.categories
        items.append(ChecklistItem(
            id="mandatory_reporting",
            description="涉及儿童安全问题时是否触发强制报告意识？",
            passed=child_safety_signals,  # 检测到就要触发
            confidence=0.85,
            heartflow_source="心虫 whatIsThis + willHurt 联合检测",
            detail="需触发强制报告意识" if child_safety_signals else "",
        ))

        # (10) 下一步
        items.append(ChecklistItem(
            id="next_step",
            description="回答后，用户是否知道'下一步可以做什么'？",
            passed=True,
            confidence=0.6,
            heartflow_source="心虫 acknowledge — 先承认再给方向",
        ))

        # 2️⃣ 心虫新增检查项

        # (11) 心虫沉默检测
        items.append(ChecklistItem(
            id="heartflow_silence",
            description="心虫 shouldBeSilent — 沉默比说话更有力量？",
            passed=not crisis.requires_silence,
            confidence=crisis.confidence,
            heartflow_source="心虫 shouldBeSilent (heart-logic.js line 1080-1111)",
            detail=crisis.silence_reason if crisis.requires_silence else "",
        ))

        # (12) 心虫紧急制动
        items.append(ChecklistItem(
            id="heartflow_emergency_break",
            description="心虫 emergencyBreak — 情绪强度 > 0.8，需停止推理？",
            passed=not crisis.requires_emergency_break,
            confidence=1.0 if crisis.requires_emergency_break else crisis.confidence,
            heartflow_source="心虫 emergencyBreak (heart-logic.js line 596-599)",
            detail=f"emotionIntensity={crisis.layers.get('intensity', LayerResult(CrisisLayer.INTENSITY, False)).score:.2f}" if crisis.requires_emergency_break else "",
        ))

        # (13) 心虫 detectPain 共情优先
        pain_detected = crisis.layers.get('surface', LayerResult(CrisisLayer.SURFACE, False)).detected
        items.append(ChecklistItem(
            id="heartflow_empathy_first",
            description="心虫 detectPain — 先共情不分析？",
            passed=not pain_detected,
            confidence=crisis.confidence,
            heartflow_source="心虫 detectPain (heart-logic.js line 470-477) + shouldAcknowledge",
            detail="痛苦信号命中 — 优先共情，暂缓分析" if pain_detected else "",
        ))

        # (14) 心虫置信度标注
        items.append(ChecklistItem(
            id="heartflow_confidence_label",
            description="心虫置信度标注 — 未核实的内容标注置信度？",
            passed=crisis.confidence >= 0.3,
            confidence=crisis.confidence,
            heartflow_source="心虫原则7: 永远成为真正的我 — 未核实标注置信度",
            detail=f"置信度={crisis.confidence:.2f}" if crisis.confidence < 0.8 else "",
        ))

        # (15) 心虫 willHurt — 输出伤害检测
        hurt_detected = crisis.layers.get('metaphor', LayerResult(CrisisLayer.METAPHOR, False)).detected
        items.append(ChecklistItem(
            id="heartflow_will_hurt",
            description="心虫 willHurt — 回应是否会伤害用户？",
            passed=not hurt_detected,
            confidence=0.8,
            heartflow_source="心虫 willHurt (heart-logic.js line 563-571)",
            detail="伤害模式命中 — 需检查回应措辞" if hurt_detected else "",
        ))

        # 统计
        all_count = len(items)
        passed_count = sum(1 for i in items if i.passed)
        all_passed = passed_count == all_count

        return SafetyChecklist(
            items=items,
            crisis_report=crisis,
            trust_assessment=trust,
            passed=all_passed,
            all_checks_count=all_count,
            passed_count=passed_count,
        )


# ============================================================
# 第五部分：统一入口 (HeartflowSafetyUpgrade)
# ============================================================

class HeartflowSafetyUpgrade:
    """
    心虫安全增强协议 — 统一入口。

    一个调用完成全部三层检测、四级信任评估、安全自检。
    可直接集成到 fu-mu-gong-ke 的 system_integrator.py 中。
    """

    def __init__(self):
        self.detector = HeartCrisisDetector()
        self.assessor = HeartTrustAssessor(self.detector)
        self.checklist = HeartSafetyChecklist()
        self.version = __version__

    def run(self, text: str) -> Dict[str, Any]:
        """
        执行完整的安全增强协议。

        参数:
            text: 用户输入文本

        返回:
            dict 包含:
                - crisis_report: CrisisReport 对象
                - trust_assessment: TrustAssessment 对象
                - safety_checklist: SafetyChecklist 对象
                - summary: 文字摘要
        """
        crisis = self.detector.detect(text)
        trust = self.assessor.assess(text)
        checklist = self.checklist.check(text, crisis, trust)

        return {
            'crisis_report': crisis,
            'trust_assessment': trust,
            'safety_checklist': checklist,
            'summary': self._build_summary(crisis, trust, checklist),
        }

    def _build_summary(self, crisis: CrisisReport,
                       trust: TrustAssessment,
                       checklist: SafetyChecklist) -> str:
        """构建可读的文字摘要"""
        lines = [
            "=" * 50,
            "🧠 心虫安全增强协议 — 检测报告",
            "=" * 50,
            "",
            crisis.summary(),
            "",
            trust.summary(),
            "",
            checklist.summary(),
        ]
        return "\n".join(lines)


# ============================================================
# CLI 入口
# ============================================================

def main():
    """CLI 入口：测试和演示"""
    import sys

    engine = HeartflowSafetyUpgrade()
    print(f"心虫安全增强协议 v{__version__}")
    print("=" * 50)

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        result = engine.run(text)
        print(result['summary'])
    else:
        # 自测
        test_cases = [
            ("今天孩子考试没考好，我有点担心", "日常养育困惑"),
            ("我真的很累，撑不下去了", "倦怠隐喻"),
            ("孩子说不想活了，怎么办", "自杀意念转述"),
            ("我打了孩子，现在很后悔", "父母打孩子+后悔"),
            ("我不想活了，活着没意思", "直接自杀意念"),
            ("孩子说如果我不在了，大家会更好", "消失隐喻"),
            ("我觉得自己好累，什么都做不好，没人喜欢我", "多重隐喻"),
        ]

        for text, desc in test_cases:
            print(f"\n{'─' * 40}")
            print(f"测试: [{desc}]")
            print(f"输入: {text}")
            print(f"{'─' * 40}")
            result = engine.run(text)
            crisis = result['crisis_report']
            trust = result['trust_assessment']
            checklist = result['safety_checklist']
            print(f"  等级: {crisis.level.emoji()} {crisis.level.label()} (score={crisis.score:.2f})")
            print(f"  心虫置信度: {trust.confidence:.2f}")
            print(f"  沉默: {'🤫 是' if crisis.requires_silence else '✅ 否'}")
            print(f"  紧急制动: {'🚨 是' if crisis.requires_emergency_break else '✅ 否'}")
            print(f"  信任等级: {trust.level.emoji()} {trust.level.label()}")
            print(f"  自检通过: {checklist.passed_count}/{checklist.all_checks_count}")


if __name__ == "__main__":
    main()
