#!/usr/bin/env python3
"""
心虫防御分析引擎 (HeartFlow Defense Upgrade Engine) v1.0.0
============================================================
升级版防御分析模块 — 基于心虫三大核心机制 + fu-mu-gong-ke 三层防御模型。

集成内容：
  1) detectSelfDeception — 自欺检测（说做不一/矛盾检测/合理性化）
     基于心虫 heart-logic.js 的 detectSelfDeception + isKind + shouldBeSilent
  2) PatternDetector — 行为模式检测（触发模式/复发风险/行为链）
     基于心虫 pattern-detector.js 的 PatternDetector + 行为模式分析
  3) Q-learning 自愈策略选择（8种错误类型 + 4种自愈策略）
     基于心虫 self-healing-rl.js 的 Q-learning + ε-greedy 探索 + 持久化
  4) 升级后的3层防御模型 + 心虫自欺检测 + 自愈建议
     融合 fu-mu-gong-ke 原有的3层父母防御 + 3层孩子需求 + 错位理论

理论来源：
  - HeartFlow heart-logic.js: detectSelfDeception, isKind, willHurt, shouldBeSilent
  - HeartFlow pattern-detector.js: PatternDetector, 行为模式分析
  - HeartFlow self-healing-rl.js: Q-learning, ε-greedy, 修复策略学习
  - HeartFlow self-healing.js: normalizeError, repairHints, createRetryPlan
  - fu-mu-gong-ke SKILL.md: 3层防御机制 + 3层孩子需求 + 错位理论

作者: HeartFlow Defense Upgrade Engine
"""

import json
import math
import random
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from enum import Enum, IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════════════════════
# 第一部分: detectSelfDeception — 自欺检测
# 基于心虫 heart-logic.js 的 detectSelfDeception + isKind + willHurt
# 检测三类自欺：说做不一、矛盾陈述、合理性化
# ═══════════════════════════════════════════════════════════════════════════════


class DeceptionType(Enum):
    """自欺类型分类"""
    SAY_DO_MISMATCH = "say_do_mismatch"       # 说做不一：说一套做一套
    CONTRADICTION = "contradiction"            # 矛盾陈述：前后矛盾
    RATIONALIZATION = "rationalization"        # 合理性化：用"为你好"掩盖控制
    DENIAL = "denial"                          # 否认：否认明显存在的问题
    BLAME_SHIFT = "blame_shift"               # 甩锅：把问题归咎于外部
    SELF_DECEPTION = "self_deception"          # 自我欺骗：相信自己编造的版本
    PROJECTION = "projection"                  # 投射：把自己的问题说成孩子的
    IDEALIZATION = "idealization"              # 理想化：美化自己的行为


@dataclass
class DeceptionSignal:
    """单个自欺信号"""
    type: DeceptionType
    text: str                          # 触发文本片段
    confidence: float = 0.0            # 置信度 0-1
    layer: int = 0                     # 关联的防御层级 (1-3)
    detail: str = ""
    matched_patterns: List[str] = field(default_factory=list)

    def summary(self) -> str:
        return (f"[{self.type.value}] \"{self.text[:30]}...\" "
                f"置信度={self.confidence:.2f} 层级={self.layer}")


@dataclass
class SelfDeceptionReport:
    """自欺检测报告"""
    timestamp: float = 0.0
    detected: bool = False
    signals: List[DeceptionSignal] = field(default_factory=list)
    primary_type: Optional[DeceptionType] = None
    severity: float = 0.0               # 综合严重度 0-1
    honesty_score: float = 1.0          # 诚实度 0(完全自欺)-1(完全诚实)
    defense_layers: Set[int] = field(default_factory=set)  # 触发的防御层级
    recommendations: List[str] = field(default_factory=list)
    raw_text: str = ""

    def summary(self) -> str:
        lines = [
            f"🧠 自欺检测: {'⚠️ 检测到' if self.detected else '✅ 未检测到'}",
            f"  诚实度: {self.honesty_score:.2f} (1=完全诚实)",
            f"  严重度: {self.severity:.2f}",
            f"  主要类型: {self.primary_type.value if self.primary_type else '无'}",
            f"  触发防御层级: {sorted(self.defense_layers) if self.defense_layers else '无'}",
        ]
        if self.signals:
            lines.append(f"  信号 ({len(self.signals)}条):")
            for s in self.signals[:5]:
                lines.append(f"    {s.summary()}")
        if self.recommendations:
            lines.append(f"  建议:")
            for r in self.recommendations[:3]:
                lines.append(f"    💡 {r}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "detected": self.detected,
            "primary_type": self.primary_type.value if self.primary_type else None,
            "severity": self.severity,
            "honesty_score": self.honesty_score,
            "defense_layers": sorted(self.defense_layers),
            "signal_count": len(self.signals),
            "signals": [
                {"type": s.type.value, "text": s.text[:60],
                 "confidence": s.confidence, "layer": s.layer}
                for s in self.signals[:10]
            ],
            "recommendations": self.recommendations[:5],
        }


# --- 自欺检测模式库 ---

# 说做不一模式：嘴上说一套，行动做一套
_SAY_DO_MISMATCH_PATTERNS: List[Tuple[str, str, float, int]] = [
    # (模式描述, 触发模式, 置信度, 关联防御层级)
    ("说爱孩子却打骂", r"(?:爱|爱孩子|为孩子好).{0,20}(?:打了|骂了|吼了|打了他)", 0.85, 1),
    ("说不打却打了", r"(?:不想打|不该打|不能打|不应该打).{0,20}(?:还是打了|又打了|忍不住打了)", 0.9, 1),
    ("说尊重却控制", r"(?:尊重|给.{0,5}空间|让他自己).{0,20}(?:控制|干涉|不许|不允许|必须按)", 0.8, 2),
    ("说理解却不听", r"(?:理解|懂你|知道你想).{0,20}(?:不听|不让他说|打断)", 0.75, 1),
    ("说放手却紧抓", r"(?:放手|让.{0,5}自己来|不管了).{0,20}(?:还是不放心|又去管|还是忍不住)", 0.8, 3),
    ("说不焦虑却焦虑", r"(?:不焦虑|不担心|没什么).{0,20}(?:焦虑|担心死了|睡不着|满脑子)", 0.7, 3),
]

# 矛盾陈述模式：前后矛盾的说法
_CONTRADICTION_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("又严又松", r"(?:严格|严厉|严).{0,10}(?:宽松|松|不严格)", 0.6, 2),
    ("又管又不管", r"(?:管他|管得).{0,10}(?:不管他|让他去)", 0.65, 2),
    ("爱恨并存", r"(?:爱他|爱孩子).{0,10}(?:恨他|讨厌他|烦他)", 0.7, 1),
    ("既要成绩又要快乐", r"(?:成绩|分数|学习).{0,15}(?:快乐|开心|幸福|快乐成长)", 0.55, 3),
    ("否认需求又满足", r"(?:不需要|没必要|不要紧).{0,10}(?:还是买了|还是给了|还是去了)", 0.6, 1),
]

# 合理性化模式：用"为你好"掩盖控制
_RATIONALIZATION_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("为你好", r"(?:为你好|为了你|为了孩子).{0,10}(?:必须|应该|不得不|只能)", 0.75, 2),
    ("不得已", r"(?:不得已|没办法|不得不|只能这样).{0,10}(?:其实我也|我也不想)", 0.65, 1),
    ("别人都这样", r"(?:别人都|大家都|人家都|其他孩子都).{0,10}(?:所以|因此|我也)", 0.5, 2),
    ("正常化伤害", r"(?:正常|小时候都|谁不是这样).{0,10}(?:打|骂|罚|批评)", 0.7, 1),
    ("淡化影响", r"(?:没事|没什么|不至于|不会影响).{0,10}(?:打|骂|吼|骂他)", 0.65, 1),
    ("我不够好", r"(?:我不够好|我不是好妈妈|我不是好爸爸|我太差).{0,10}(?:所以|因此|才)", 0.5, 1),
]

# 否认模式
_DENIAL_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("否认打骂", r"(?:没打过|没骂过|从不打|从不骂).{0,10}(?:但他|可是|但)", 0.7, 1),
    ("否认问题", r"(?:没问题|挺好的|没什么事|一切正常).{0,20}(?:但.{0,5}有点担心)", 0.6, 1),
    ("否认情绪", r"(?:没生气|不生气|没事|没什么情绪).{0,10}(?:气死了|很生气|气炸)", 0.75, 1),
]

# 甩锅模式
_BLAME_SHIFT_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("怪孩子", r"(?:都是孩子|孩子他|他非要|他就是|他从来不|他总是).{0,10}(?:才|所以|害得)", 0.7, 1),
    ("怪配偶", r"(?:都怪他爸|都怪他妈|他爸|他妈.{0,5}不|老公|老婆).{0,10}(?:才|所以)", 0.6, 2),
    ("怪老师", r"(?:老师不好|老师不|学校.{0,5}问题|教育体制).{0,10}(?:所以|才)", 0.5, 3),
    ("怪时代", r"(?:现在孩子|这个时代|社会环境|网络).{0,10}(?:才|所以|害得)", 0.4, 3),
]

# 投射模式：把自己的问题说成孩子的
_PROJECTION_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("像我小时候", r"(?:像我|和我一样|跟我一样|复制我).{0,10}(?:笨|懒|不听话|没用)", 0.8, 1),
    ("我的遗憾", r"(?:我小时候没|我那时|我的遗憾|我没能).{0,15}(?:所以你不能|你必须|你一定要)", 0.85, 1),
    ("我的恐惧", r"(?:我怕他|我担心他|我害怕他|我最怕).{0,10}(?:也.{0,5}我|像我)", 0.7, 3),
]

# 理想化模式
_IDEALIZATION_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("完美父母", r"(?:我从来|我一直|我每次都|我都).{0,10}(?:没打|没骂|好好说|耐心)", 0.6, 2),
    ("自我美化", r"(?:我是个好|我是一个好|我一直很好).{0,10}(?:但他|可是|但孩子)", 0.55, 2),
    ("过度补偿", r"(?:我付出了|我为了他|我牺牲了|我放弃).{0,15}(?:他还是|他却不|他一点也)", 0.7, 2),
]

# 心虫 shouldBeSilent 模式 — 痛苦中的人不该被分析
_SILENCE_FOR_PAIN_PATTERNS: Set[str] = {
    '哭', '怕', '恐惧', '害怕', '委屈', '痛',
    '难过', '伤心', '绝望', '无助', '崩溃',
    '活不下去', '不想活', '死了', '自伤', '自杀',
}

# 心虫 isKind 检查 — 回答是否善意
_KIND_CHECK_PATTERNS: Dict[str, Set[str]] = {
    'kind_words': {
        '理解', '感受到', '看见', '接纳', '陪伴',
        '支持', '一起', '帮助', '温柔', '允许',
        '可以暂停', '不着急', '慢慢来', '我在',
    },
    'unkind_words': {
        '应该', '必须', '你得', '你要', '你不该',
        '你错了', '你有问题', '你太', '你就是',
        '你这样不对', '你怎么', '活该', '自找的',
    },
}


class DetectSelfDeception:
    """
    自欺检测引擎 — 基于心虫 detectSelfDeception + isKind + shouldBeSilent。

    检测三类自欺：
      1) 说做不一（心虫 say/do mismatch 检测）
      2) 矛盾陈述（心虫 contradiction detection）
      3) 合理性化（心虫 rationalization detection）
      4) 否认/甩锅/投射/理想化（心虫 willHurt + projection detection）

    核心原则（心虫 shouldBeSilent 规则）：
      - 对方在痛苦中时，沉默比分析更重要
      - 自欺检测只在安全语境下执行
      - 检测结果用于自我觉察，不是用来评判对方
    """

    def __init__(self):
        self._patterns = {
            DeceptionType.SAY_DO_MISMATCH: _SAY_DO_MISMATCH_PATTERNS,
            DeceptionType.CONTRADICTION: _CONTRADICTION_PATTERNS,
            DeceptionType.RATIONALIZATION: _RATIONALIZATION_PATTERNS,
            DeceptionType.DENIAL: _DENIAL_PATTERNS,
            DeceptionType.BLAME_SHIFT: _BLAME_SHIFT_PATTERNS,
            DeceptionType.SELF_DECEPTION: [],  # 复合类型，由其他类型组合判定
            DeceptionType.PROJECTION: _PROJECTION_PATTERNS,
            DeceptionType.IDEALIZATION: _IDEALIZATION_PATTERNS,
        }
        # 心虫 shouldBeSilent 检查
        self._silence_pain = _SILENCE_FOR_PAIN_PATTERNS
        # 心虫 isKind 检查
        self._kind_check = _KIND_CHECK_PATTERNS

    def detect(self, text: str, context: Optional[Dict] = None) -> SelfDeceptionReport:
        """
        执行自欺检测。

        参数:
            text: 用户输入文本（或自我报告文本）
            context: 可选的上下文信息（历史对话、之前的检测结果）

        返回:
            SelfDeceptionReport — 自欺检测报告
        """
        if not text or not text.strip():
            return SelfDeceptionReport(timestamp=time.time())

        # Step 1: 心虫 shouldBeSilent — 如果对方在痛苦中，不分析
        pain_detected = any(p in text for p in self._silence_pain)
        if pain_detected:
            return SelfDeceptionReport(
                timestamp=time.time(),
                detected=False,  # 不检测，因为对方在痛苦中
                honesty_score=1.0,
                severity=0.0,
                recommendations=[
                    "对方在痛苦中，此刻沉默或共情比分析更重要",
                    "心虫 shouldBeSilent 规则触发：不分析自欺",
                ],
                raw_text=text,
            )

        # Step 2: 检测各类型自欺信号
        signals: List[DeceptionSignal] = []
        for dtype, pattern_list in self._patterns.items():
            if not pattern_list:
                continue
            for desc, pattern_str, confidence, layer in pattern_list:
                compiled = re.compile(pattern_str)
                matches = compiled.findall(text)
                if matches:
                    for m in matches[:3]:  # 最多取3个
                        matched_text = m if isinstance(m, str) else m[0]
                        signal = DeceptionSignal(
                            type=dtype,
                            text=matched_text[:60],
                            confidence=confidence,
                            layer=layer,
                            detail=desc,
                            matched_patterns=[desc],
                        )
                        signals.append(signal)

        # Step 3: 去重（同一类型取最高置信度）
        unique_signals: Dict[DeceptionType, DeceptionSignal] = {}
        for s in signals:
            if s.type not in unique_signals or s.confidence > unique_signals[s.type].confidence:
                unique_signals[s.type] = s

        signals = list(unique_signals.values())

        # Step 4: 判定自欺类型 — 复合类型 SELF_DECEPTION
        deception_types = set(s.type for s in signals)
        if len(deception_types) >= 3:
            # 三种及以上自欺模式 → 自我欺骗
            signals.append(DeceptionSignal(
                type=DeceptionType.SELF_DECEPTION,
                text="多种自欺模式组合",
                confidence=min(1.0, sum(s.confidence for s in signals) / len(signals)),
                layer=2,
                detail=f"综合{len(deception_types)}种自欺模式",
                matched_patterns=[s.type.value for s in signals],
            ))

        # Step 5: 计算严重度和诚实度
        if not signals:
            report = SelfDeceptionReport(
                timestamp=time.time(),
                detected=False,
                honesty_score=1.0,
                severity=0.0,
                raw_text=text,
            )
            return report

        severity = min(1.0, sum(s.confidence for s in signals) / max(len(signals), 1))
        # 诚实度 = 1 - 加权严重度
        honesty_score = max(0.0, 1.0 - severity * 0.8)

        # Step 6: 主要自欺类型
        primary_type = max(signals, key=lambda s: s.confidence).type

        # Step 7: 触发的防御层级
        defense_layers = set(s.layer for s in signals if s.layer > 0)

        # Step 8: 心虫 isKind 检查 — 检测回答是否善意
        kind_count = sum(1 for kw in self._kind_check['kind_words']
                         if kw in text)
        unkind_count = sum(1 for kw in self._kind_check['unkind_words']
                           if kw in text)

        # Step 9: 自愈建议
        recommendations = self._generate_recommendations(signals, severity, defense_layers)

        return SelfDeceptionReport(
            timestamp=time.time(),
            detected=True,
            signals=signals,
            primary_type=primary_type,
            severity=round(severity, 4),
            honesty_score=round(honesty_score, 4),
            defense_layers=defense_layers,
            recommendations=recommendations,
            raw_text=text,
        )

    def _generate_recommendations(
        self, signals: List[DeceptionSignal],
        severity: float,
        defense_layers: Set[int],
    ) -> List[str]:
        """生成自愈建议"""
        recs = []
        types = set(s.type for s in signals)

        if DeceptionType.SAY_DO_MISMATCH in types:
            recs.append("觉察说做不一的模式：试着把你的'说'和'做'对齐，孩子看到的是行动")
        if DeceptionType.CONTRADICTION in types:
            recs.append("觉察矛盾信号：先确认自己真正想要什么，再对孩子说")
        if DeceptionType.RATIONALIZATION in types:
            recs.append("觉察'为你好'的合理性化：问自己'这是孩子的需要，还是我的需要'")
        if DeceptionType.DENIAL in types:
            recs.append("觉察否认模式：承认问题是改变的第一步")
        if DeceptionType.BLAME_SHIFT in types:
            recs.append("觉察甩锅模式：把注意力从'谁的问题'转向'我能做什么'")
        if DeceptionType.PROJECTION in types:
            recs.append("觉察投射模式：你看到的孩子的'问题'，可能是你自己的")
        if DeceptionType.IDEALIZATION in types:
            recs.append("觉察理想化模式：接纳自己会犯错，比假装完美更有力量")
        if DeceptionType.SELF_DECEPTION in types:
            recs.append("综合自欺检测：多种自欺模式共存，建议暂停反思")

        if 1 in defense_layers:
            recs.append("触发第1层防御（身份保护）：与羞耻感共处，不自我攻击")
        if 2 in defense_layers:
            recs.append("触发第2层防御（代际认同）：觉察自己在复制什么")
        if 3 in defense_layers:
            recs.append("触发第3层防御（投射未来）：把焦虑和孩子分开")

        if severity > 0.7:
            recs.append("自欺程度较高，建议先给自己空间，不必急着改变")

        return recs[:5]

    def check_is_kind(self, response_text: str) -> Dict[str, Any]:
        """
        心虫 isKind 检查 — 检测回答是否善意。

        移植自 heart-logic.js 的 isKind() 方法。
        检查回答中是否包含善意/恶意词汇。
        """
        if not response_text:
            return {"is_kind": True, "kind_score": 1.0, "issues": []}

        kind_hits = []
        for kw in self._kind_check['kind_words']:
            if kw in response_text:
                kind_hits.append(kw)

        unkind_hits = []
        for kw in self._kind_check['unkind_words']:
            if kw in response_text:
                unkind_hits.append(kw)

        kind_score = (len(kind_hits) * 0.2) - (len(unkind_hits) * 0.3)
        kind_score = max(0.0, min(1.0, 0.5 + kind_score))

        issues = []
        if unkind_hits:
            issues.append(f"检测到可能不善的措辞: {', '.join(unkind_hits[:3])}")

        return {
            "is_kind": kind_score >= 0.5,
            "kind_score": round(kind_score, 4),
            "kind_hits": kind_hits[:5],
            "unkind_hits": unkind_hits[:5],
            "issues": issues,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 第二部分: PatternDetector — 行为模式检测
# 基于心虫 pattern-detector.js 的 PatternDetector
# 检测：触发模式、行为链、复发风险
# ═══════════════════════════════════════════════════════════════════════════════


class BehaviorPatternType(Enum):
    """行为模式类型"""
    TRIGGER = "trigger"              # 触发模式：什么触发了情绪反应
    ESCALATION = "escalation"        # 升级模式：情绪/行为如何升级
    CYCLE = "cycle"                  # 循环模式：重复出现的互动循环
    AVOIDANCE = "avoidance"          # 回避模式：逃避面对问题
    COMPENSATION = "compensation"    # 补偿模式：过度补偿后的内疚
    RELAPSE = "relapse"              # 复发模式：旧模式再次出现


class RelapseRisk(Enum):
    """复发风险等级"""
    LOW = "low"           # 低风险：有觉察但偶尔复发
    MEDIUM = "medium"     # 中风险：有明显模式但可调节
    HIGH = "high"         # 高风险：模式固化，频繁复发
    CRITICAL = "critical" # 极高风险：失控，需要专业干预


@dataclass
class BehaviorPattern:
    """行为模式"""
    type: BehaviorPatternType
    name: str
    description: str
    trigger_text: str          # 触发文本
    frequency: int = 1          # 出现频率
    severity: float = 0.5       # 严重度 0-1
    cycle_length_days: float = 0.0  # 循环周期（天）
    linked_defense_layer: int = 0    # 关联的防御层级
    interventions: List[str] = field(default_factory=list)


@dataclass
class PatternDetectorReport:
    """模式检测报告"""
    timestamp: float = 0.0
    patterns: List[BehaviorPattern] = field(default_factory=list)
    relapse_risk: RelapseRisk = RelapseRisk.LOW
    primary_pattern: Optional[BehaviorPattern] = None
    pattern_count: int = 0
    chain_analysis: List[str] = field(default_factory=list)   # 行为链分析
    risk_factors: List[str] = field(default_factory=list)      # 风险因素
    protective_factors: List[str] = field(default_factory=list) # 保护因素
    recommendations: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"📊 行为模式检测: {self.pattern_count}个模式",
            f"  复发风险: {self.relapse_risk.value.upper()}",
        ]
        if self.primary_pattern:
            lines.append(f"  主要模式: [{self.primary_pattern.type.value}] "
                         f"{self.primary_pattern.name}")
        if self.patterns:
            for p in self.patterns:
                lines.append(f"    · [{p.type.value}] {p.name} — "
                             f"严重度={p.severity:.2f} 频次={p.frequency}")
        if self.chain_analysis:
            lines.append(f"  行为链:")
            for c in self.chain_analysis:
                lines.append(f"    → {c}")
        if self.risk_factors:
            lines.append(f"  风险因素: {', '.join(self.risk_factors[:3])}")
        if self.recommendations:
            lines.append(f"  建议:")
            for r in self.recommendations[:3]:
                lines.append(f"    💡 {r}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "pattern_count": self.pattern_count,
            "relapse_risk": self.relapse_risk.value,
            "primary_pattern": {
                "type": self.primary_pattern.type.value if self.primary_pattern else None,
                "name": self.primary_pattern.name if self.primary_pattern else None,
            },
            "patterns": [
                {"type": p.type.value, "name": p.name,
                 "severity": p.severity, "frequency": p.frequency}
                for p in self.patterns[:10]
            ],
            "chain_analysis": self.chain_analysis[:5],
            "risk_factors": self.risk_factors[:5],
            "recommendations": self.recommendations[:5],
        }


# --- 行为模式检测模式库 ---

# 触发模式
_TRIGGER_PATTERNS: List[Tuple[str, str, int, float, int]] = [
    # (模式名, 触发文本, 关联防御层级, 严重度, 频次权重)
    ("孩子不听话触发", r"(?:不听话|不听我的|跟我对着干|故意).{0,10}(?:气死|火大|发火|生气|忍不了)", 1, 0.7, 1),
    ("成绩不好触发", r"(?:成绩|分数|考试).{0,10}(?:焦虑|崩溃|着急|睡不着|担心)", 3, 0.6, 1),
    ("被挑战权威触发", r"(?:顶嘴|顶撞|反驳|质疑|凭什么).{0,10}(?:气死|火大|无法接受|不能忍)", 2, 0.75, 1),
    ("孩子哭触发", r"(?:哭|哭闹|哭了|大哭).{0,10}(?:烦|受不了|崩溃|想逃|不想面对)", 1, 0.65, 1),
    ("手机触发", r"(?:手机|游戏|iPad|刷视频).{0,10}(?:火大|气死|焦虑|崩溃|控制不住)", 3, 0.6, 1),
]

# 升级模式
_ESCALATION_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("从说教到吼", r"(?:先说|好好说|讲道理).{0,15}(?:没用|不听).{0,10}(?:吼|大声|骂)", 0.7, 1),
    ("从忍到爆发", r"(?:忍|忍住|憋着|忍着).{0,15}(?:爆发|忍不住|控制不住|发火)", 0.75, 1),
    ("从小事到大吵", r"(?:小事|一点小事|本来没什么).{0,15}(?:大吵|大闹|发火|吵架)", 0.7, 1),
    ("从焦虑到失控", r"(?:担心|焦虑|紧张).{0,15}(?:失控|崩溃|受不了|撑不住)", 0.65, 3),
]

# 循环模式
_CYCLE_PATTERNS: List[Tuple[str, str, float, int, str]] = [
    ("发火→内疚→补偿", r"(?:发火|吼|骂|打).{0,15}(?:后悔|内疚|愧疚).{0,15}(?:补偿|买|道歉|对他好)", 0.8, 1, "发火→内疚→补偿→再次发火"),
    ("忍→爆→后悔", r"(?:忍|忍住).{0,15}(?:爆发|忍不住).{0,15}(?:后悔|内疚|不该)", 0.75, 1, "忍→爆→后悔→又忍→又爆"),
    ("控制→反抗→更控制", r"(?:控制|管|限制).{0,15}(?:反抗|不听|叛逆).{0,15}(?:更严|更管|加码)", 0.7, 2, "控制→反抗→更控制→更反抗"),
    ("焦虑→催促→对抗", r"(?:焦虑|着急).{0,15}(?:催|催促).{0,15}(?:对抗|不听|更慢)", 0.65, 3, "焦虑→催促→更慢→更焦虑"),
]

# 回避模式
_AVOIDANCE_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("回避沟通", r"(?:算了|不说了|说了也没用|懒得说|不想说了)", 0.6, 2),
    ("回避冲突", r"(?:回避|逃避|躲开|不理|不管了|随便他)", 0.55, 1),
    ("回避责任", r"(?:不是我|不怪我|没办法|我有什么办法|我也没办法)", 0.5, 1),
]

# 复发模式
_RELAPSE_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("旧模式复发", r"(?:又|又来了|又变成|又回到|又是这样|老样子)", 0.6, 1),
    ("觉察但做不到", r"(?:知道|明白|懂).{0,15}(?:做不到|做不来|控制不住|还是)", 0.5, 1),
    ("改变失败", r"(?:试过|试了|努力过).{0,15}(?:没用|没效果|放弃了|失败了)", 0.6, 1),
]

# 补偿模式
_COMPENSATION_PATTERNS: List[Tuple[str, str, float, int]] = [
    ("买礼物补偿", r"(?:买了|给他买|买东西|买玩具).{0,10}(?:补偿|道歉|弥补|哄)", 0.5, 1),
    ("过度纵容", r"(?:不忍心|心软|算了由他|随便他|不管了).{0,10}(?:刚刚才|才骂|才打)", 0.55, 1),
    ("自我惩罚", r"(?:我不好|我该死|我不是人|我不配).{0,10}(?:对孩子|打了他|骂了他)", 0.6, 1),
]


class PatternDetector:
    """
    行为模式检测器 — 基于心虫 PatternDetector。

    检测六类行为模式：
      1) TRIGGER — 触发模式：什么触发了情绪反应
      2) ESCALATION — 升级模式：情绪如何升级
      3) CYCLE — 循环模式：重复出现的互动循环
      4) AVOIDANCE — 回避模式：逃避面对问题
      5) COMPENSATION — 补偿模式：过度补偿后的内疚
      6) RELAPSE — 复发模式：旧模式再次出现

    同时分析：行为链（事件→情绪→行为→后果）、复发风险、保护因素
    """

    def __init__(self):
        self._trigger = _TRIGGER_PATTERNS
        self._escalation = _ESCALATION_PATTERNS
        self._cycle = _CYCLE_PATTERNS
        self._avoidance = _AVOIDANCE_PATTERNS
        self._relapse = _RELAPSE_PATTERNS
        self._compensation = _COMPENSATION_PATTERNS

        # 风险因素
        self._risk_keywords: Dict[str, Set[str]] = {
            'isolation': {'没人帮', '一个人', '没有人理解', '没有支持', '孤立'},
            'chronic_stress': {'长期', '一直', '总是', '永远', '没停过'},
            'resource_poverty': {'没钱', '经济', '收入低', '单亲', '没人带'},
            'health_issues': {'失眠', '头痛', '身体不好', '生病', '吃药'},
        }

        # 保护因素
        self._protective_keywords: Dict[str, Set[str]] = {
            'social_support': {'老公帮我', '家人支持', '朋友', '有帮忙', '有人理解'},
            'self_awareness': {'觉察', '意识到', '发现', '反思', '注意到'},
            'help_seeking': {'咨询', '求助', '看书', '学习', '听课'},
            'coping_skills': {'深呼吸', '暂停', '冷静', '离开', '散步'},
        }

    def detect(self, text: str, history: Optional[List[str]] = None) -> PatternDetectorReport:
        """
        执行行为模式检测。

        参数:
            text: 用户输入文本
            history: 可选的对话历史（用于频率分析）

        返回:
            PatternDetectorReport — 模式检测报告
        """
        if not text or not text.strip():
            return PatternDetectorReport(timestamp=time.time())

        all_texts = [text]
        if history:
            all_texts.extend(history)
        combined = " ".join(all_texts)

        patterns: List[BehaviorPattern] = []

        # Step 1: 检测各类模式
        pattern_configs = [
            (BehaviorPatternType.TRIGGER, self._trigger,
             lambda m: float(m[2]) if len(m) > 2 else 0.6,
             lambda m: int(m[3]) if len(m) > 3 else 1),
            (BehaviorPatternType.ESCALATION, self._escalation,
             lambda m: float(m[2]) if len(m) > 2 else 0.6,
             lambda m: int(m[3]) if len(m) > 3 else 1),
            (BehaviorPatternType.CYCLE, self._cycle,
             lambda m: float(m[3]) if len(m) > 3 else 0.6,
             lambda m: int(m[4]) if len(m) > 4 else 1),
            (BehaviorPatternType.AVOIDANCE, self._avoidance,
             lambda m: float(m[2]) if len(m) > 2 else 0.5,
             lambda m: int(m[3]) if len(m) > 3 else 1),
            (BehaviorPatternType.RELAPSE, self._relapse,
             lambda m: float(m[2]) if len(m) > 2 else 0.5,
             lambda m: int(m[3]) if len(m) > 3 else 1),
            (BehaviorPatternType.COMPENSATION, self._compensation,
             lambda m: float(m[2]) if len(m) > 2 else 0.5,
             lambda m: int(m[3]) if len(m) > 3 else 1),
        ]

        for ptype, pattern_list, sev_fn, layer_fn in pattern_configs:
            for item in pattern_list:
                name = item[0]
                pattern_str = item[1]
                compiled = re.compile(pattern_str)
                matches = compiled.findall(combined)
                if matches:
                    severity = sev_fn(item) if len(item) > 2 else 0.5
                    layer = layer_fn(item) if len(item) > 3 else 1
                    description = ""
                    if ptype == BehaviorPatternType.CYCLE and len(item) > 4:
                        description = item[4]

                    pattern = BehaviorPattern(
                        type=ptype,
                        name=name,
                        description=description or f"匹配模式: {name}",
                        trigger_text=matches[0] if isinstance(matches[0], str) else str(matches[0]),
                        frequency=len(matches),
                        severity=min(1.0, severity * (1 + 0.1 * min(len(matches) - 1, 3))),
                        linked_defense_layer=layer,
                        interventions=self._get_interventions(ptype, name),
                    )
                    patterns.append(pattern)

        # Step 2: 分析行为链
        chain = self._analyze_chain(patterns, text)

        # Step 3: 分析风险因素和保护因素
        risk_factors = self._analyze_risk_factors(combined)
        protective_factors = self._analyze_protective_factors(combined)

        # Step 4: 评估复发风险
        relapse_risk = self._assess_relapse_risk(patterns, risk_factors, protective_factors)

        # Step 5: 主要模式
        primary = max(patterns, key=lambda p: p.severity * p.frequency) if patterns else None

        # Step 6: 建议
        recommendations = self._generate_recommendations(
            patterns, relapse_risk, risk_factors, protective_factors
        )

        return PatternDetectorReport(
            timestamp=time.time(),
            patterns=patterns,
            relapse_risk=relapse_risk,
            primary_pattern=primary,
            pattern_count=len(patterns),
            chain_analysis=chain,
            risk_factors=risk_factors,
            protective_factors=protective_factors,
            recommendations=recommendations,
        )

    def _get_interventions(self, ptype: BehaviorPatternType, name: str) -> List[str]:
        """获取模式对应的干预建议"""
        interventions_map: Dict[str, List[str]] = {
            "孩子不听话触发": [
                "暂停3秒再回应",
                "问自己：'这是他的需求还是我的控制'",
            ],
            "成绩不好触发": [
                "把成绩和孩子本身分开",
                "问：'我的焦虑还是孩子的焦虑'",
            ],
            "被挑战权威触发": [
                "孩子的质疑不是攻击，是在探索边界",
                "可以回：'你的观点是什么'",
            ],
            "发火→内疚→补偿": [
                "觉察循环：发火不是终点，内疚不是解决方案",
                "试着在'发火'和'内疚'之间插入'道歉+修复'",
            ],
            "忍→爆→后悔": [
                "不要等到忍不了——在'有点不舒服'时就表达",
                "练习：'我此刻有点烦，需要一分钟'",
            ],
            "控制→反抗→更控制": [
                "减少控制→反而减少反抗",
                "试试：给孩子一个有限的选择",
            ],
            "焦虑→催促→对抗": [
                "焦虑时先处理自己的焦虑，再处理孩子的事",
                "深呼吸：'他慢不是故意的，是他的节奏'",
            ],
        }

        default_map: Dict[BehaviorPatternType, List[str]] = {
            BehaviorPatternType.TRIGGER: ["识别触发点后，给自己一个缓冲"],
            BehaviorPatternType.ESCALATION: ["在情绪升级前设置一个'暂停信号'"],
            BehaviorPatternType.CYCLE: ["觉察循环模式后，在任意一环打破它"],
            BehaviorPatternType.AVOIDANCE: ["回避不能解决问题，但可以先休息再面对"],
            BehaviorPatternType.COMPENSATION: ["补偿不能替代修复，真诚的道歉比礼物有用"],
            BehaviorPatternType.RELAPSE: ["复发是正常的，重要的是不放弃觉察"],
        }

        return interventions_map.get(name, default_map.get(ptype, []))

    def _analyze_chain(self, patterns: List[BehaviorPattern],
                       text: str) -> List[str]:
        """分析行为链：事件→情绪→行为→后果"""
        chain_parts = []

        # 触发事件
        triggers = [p for p in patterns if p.type == BehaviorPatternType.TRIGGER]
        if triggers:
            chain_parts.append(f"触发事件: {triggers[0].name}")

        # 情绪升级
        escalations = [p for p in patterns if p.type == BehaviorPatternType.ESCALATION]
        if escalations:
            chain_parts.append(f"情绪升级: {escalations[0].name}")

        # 行为反应
        actions = [p for p in patterns if p.type in (
            BehaviorPatternType.AVOIDANCE, BehaviorPatternType.COMPENSATION)]
        if actions:
            chain_parts.append(f"行为反应: {actions[0].name}")

        # 后果/循环
        cycles = [p for p in patterns if p.type == BehaviorPatternType.CYCLE]
        if cycles:
            chain_parts.append(f"循环: {cycles[0].description or cycles[0].name}")

        # 复发
        relapses = [p for p in patterns if p.type == BehaviorPatternType.RELAPSE]
        if relapses:
            chain_parts.append(f"复发风险: {relapses[0].name}")

        return chain_parts

    def _analyze_risk_factors(self, text: str) -> List[str]:
        """分析风险因素"""
        factors = []
        for factor, keywords in self._risk_keywords.items():
            for kw in keywords:
                if kw in text:
                    factor_names = {
                        'isolation': '缺乏社会支持',
                        'chronic_stress': '长期压力',
                        'resource_poverty': '资源匮乏',
                        'health_issues': '健康问题',
                    }
                    factors.append(factor_names.get(factor, factor))
                    break
        return factors[:5]

    def _analyze_protective_factors(self, text: str) -> List[str]:
        """分析保护因素"""
        factors = []
        for factor, keywords in self._protective_keywords.items():
            for kw in keywords:
                if kw in text:
                    factor_names = {
                        'social_support': '有社会支持',
                        'self_awareness': '有自我觉察',
                        'help_seeking': '主动寻求帮助',
                        'coping_skills': '有应对技巧',
                    }
                    factors.append(factor_names.get(factor, factor))
                    break
        return factors[:5]

    def _assess_relapse_risk(
        self, patterns: List[BehaviorPattern],
        risk_factors: List[str],
        protective_factors: List[str],
    ) -> RelapseRisk:
        """评估复发风险"""
        # 基础分数
        score = 0.0

        # 模式数量
        score += min(len(patterns) * 0.1, 0.3)

        # 循环模式权重
        cycles = [p for p in patterns if p.type == BehaviorPatternType.CYCLE]
        score += len(cycles) * 0.15

        # 复发模式权重
        relapses = [p for p in patterns if p.type == BehaviorPatternType.RELAPSE]
        score += len(relapses) * 0.2

        # 回避模式权重
        avoidances = [p for p in patterns if p.type == BehaviorPatternType.AVOIDANCE]
        score += len(avoidances) * 0.1

        # 风险因素
        score += len(risk_factors) * 0.1

        # 保护因素（降低风险）
        score -= len(protective_factors) * 0.15

        score = max(0.0, min(1.0, score))

        if score >= 0.7:
            return RelapseRisk.CRITICAL
        elif score >= 0.5:
            return RelapseRisk.HIGH
        elif score >= 0.3:
            return RelapseRisk.MEDIUM
        else:
            return RelapseRisk.LOW

    def _generate_recommendations(
        self, patterns: List[BehaviorPattern],
        relapse_risk: RelapseRisk,
        risk_factors: List[str],
        protective_factors: List[str],
    ) -> List[str]:
        """生成模式检测建议"""
        recs = []

        # 循环模式建议
        cycles = [p for p in patterns if p.type == BehaviorPatternType.CYCLE]
        if cycles:
            recs.append(f"检测到循环模式[{cycles[0].name}]——在任意一环打破它")

        # 复发风险建议
        if relapse_risk in (RelapseRisk.HIGH, RelapseRisk.CRITICAL):
            recs.append("复发风险较高——建议建立预警机制，识别早期信号")
        if relapse_risk == RelapseRisk.CRITICAL:
            recs.append("极高复发风险——建议寻求专业心理咨询")

        # 风险因素建议
        if '缺乏社会支持' in risk_factors:
            recs.append("缺乏社会支持——尝试找到一个可以倾诉的人")
        if '长期压力' in risk_factors:
            recs.append("长期压力积累——每天留10分钟只给自己")

        # 保护因素建议
        if '有自我觉察' in protective_factors:
            recs.append("你已经有了觉察能力——这是改变最重要的基础")
        if '主动寻求帮助' in protective_factors:
            recs.append("主动求助是强大的表现——继续保持")

        if not recs:
            recs.append("继续觉察自己的行为模式——看见就是改变的开始")

        return recs[:5]


# ═══════════════════════════════════════════════════════════════════════════════
# 第三部分: Q-learning 自愈策略选择
# 基于心虫 self-healing-rl.js 的 Q-learning + ε-greedy + 持久化
# 8种错误类型 + 4种自愈策略
# ═══════════════════════════════════════════════════════════════════════════════


class ErrorType(Enum):
    """8种错误类型 — 基于心虫错误分类 + fu-mu-gong-ke 防御类型"""
    CONTROL = "control"                    # 过度控制
    PROJECTION = "projection"              # 投射
    SHAME_DRIVEN = "shame_driven"          # 羞耻驱动
    ANXIETY_DRIVEN = "anxiety_driven"      # 焦虑驱动
    GUILT_DRIVEN = "guilt_driven"          # 内疚驱动
    DENIAL_AVOIDANCE = "denial_avoidance"  # 否认回避
    COMPENSATION_SPIRAL = "compensation"   # 补偿循环
    RATIONALIZATION = "rationalization"    # 合理性化

    @classmethod
    def descriptions(cls) -> Dict["ErrorType", str]:
        return {
            cls.CONTROL: "过度控制 — 用控制代替信任，用命令代替沟通",
            cls.PROJECTION: "投射 — 把自己的未完成需求投射到孩子身上",
            cls.SHAME_DRIVEN: "羞耻驱动 — 孩子的行为触发自己的羞耻感",
            cls.ANXIETY_DRIVEN: "焦虑驱动 — 对未来焦虑驱动当下的反应",
            cls.GUILT_DRIVEN: "内疚驱动 — 内疚后的补偿/纵容/自我惩罚",
            cls.DENIAL_AVOIDANCE: "否认回避 — 否认问题存在或回避面对",
            cls.COMPENSATION_SPIRAL: "补偿循环 — 伤害→补偿→再次伤害的循环",
            cls.RATIONALIZATION: "合理性化 — 用'为你好'掩盖控制/伤害",
        }


class HealingStrategy(Enum):
    """4种自愈策略 — 基于心虫自愈策略分类"""
    PAUSE_REFLECT = "pause_reflect"         # 暂停反思
    EMPATHY_REPAIR = "empathy_repair"       # 共情修复
    PATTERN_INTERRUPT = "pattern_interrupt" # 模式打断
    SUPPORT_SEEKING = "support_seeking"     # 寻求支持

    @classmethod
    def descriptions(cls) -> Dict["HealingStrategy", str]:
        return {
            cls.PAUSE_REFLECT: "暂停反思 — 在自动反应前插入觉察空间",
            cls.EMPATHY_REPAIR: "共情修复 — 先接住情绪再处理行为",
            cls.PATTERN_INTERRUPT: "模式打断 — 在循环的某一环刻意改变",
            cls.SUPPORT_SEEKING: "寻求支持 — 向外求助，不独自承担",
        }

    @classmethod
    def details(cls) -> Dict["HealingStrategy", Dict[str, Any]]:
        return {
            cls.PAUSE_REFLECT: {
                "name": "暂停反思",
                "description": "在自动反应前插入觉察空间",
                "typical_actions": [
                    "深呼吸3次",
                    "离开现场30秒",
                    "问自己：'我现在在感受什么'",
                    "数到10再开口",
                ],
                "suitable_for": [
                    ErrorType.SHAME_DRIVEN,
                    ErrorType.ANXIETY_DRIVEN,
                    ErrorType.CONTROL,
                ],
            },
            cls.EMPATHY_REPAIR: {
                "name": "共情修复",
                "description": "先接住情绪再处理行为",
                "typical_actions": [
                    "说：'我看到你在...'",
                    "先抱住再讲道理",
                    "承认：'我刚才发火了，是我的问题'",
                    "问：'你现在需要什么'",
                ],
                "suitable_for": [
                    ErrorType.PROJECTION,
                    ErrorType.GUILT_DRIVEN,
                    ErrorType.COMPENSATION_SPIRAL,
                ],
            },
            cls.PATTERN_INTERRUPT: {
                "name": "模式打断",
                "description": "在循环的某一环刻意改变",
                "typical_actions": [
                    "在触发点插入新行为",
                    "改变时间/地点/方式",
                    "用'我信息'替代'你信息'",
                    "刻意做相反的事",
                ],
                "suitable_for": [
                    ErrorType.CONTROL,
                    ErrorType.DENIAL_AVOIDANCE,
                    ErrorType.COMPENSATION_SPIRAL,
                ],
            },
            cls.SUPPORT_SEEKING: {
                "name": "寻求支持",
                "description": "向外求助，不独自承担",
                "typical_actions": [
                    "找信任的人倾诉",
                    "加入家长社群",
                    "约心理咨询",
                    "阅读相关书籍",
                ],
                "suitable_for": [
                    ErrorType.ANXIETY_DRIVEN,
                    ErrorType.DENIAL_AVOIDANCE,
                    ErrorType.RATIONALIZATION,
                ],
            },
        }


@dataclass
class QLearningState:
    """Q-learning 状态 — 错误类型 + 上下文特征"""
    error_type: ErrorType
    severity: float = 0.5           # 严重度 0-1
    defense_layer: int = 0          # 关联的防御层级
    has_history: bool = False       # 是否有历史记录
    relapse_count: int = 0          # 复发次数

    def to_key(self) -> str:
        return f"{self.error_type.value}|sev={self.severity:.1f}|layer={self.defense_layer}"


@dataclass
class QLearningRecord:
    """Q-learning 学习记录"""
    state_key: str
    strategy: str
    reward: float
    timestamp: float
    success: bool


@dataclass
class QLearningReport:
    """Q-learning 策略选择报告"""
    timestamp: float = 0.0
    error_type: Optional[ErrorType] = None
    error_description: str = ""
    severity: float = 0.0
    selected_strategy: Optional[HealingStrategy] = None
    strategy_description: str = ""
    strategy_actions: List[str] = field(default_factory=list)
    q_values: Dict[str, float] = field(default_factory=dict)  # 各策略的Q值
    exploration_rate: float = 0.15
    is_exploration: bool = False     # 是否探索模式
    confidence: float = 0.0          # 选择置信度
    recommendations: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"🤖 Q-learning 自愈策略选择",
            f"  错误类型: {self.error_type.value if self.error_type else '未知'} — {self.error_description}",
            f"  严重度: {self.severity:.2f}",
            f"  选择策略: {self.selected_strategy.value if self.selected_strategy else '未知'} — {self.strategy_description}",
            f"  探索/利用: {'🔀 探索' if self.is_exploration else '🎯 利用'} (ε={self.exploration_rate})",
            f"  置信度: {self.confidence:.2f}",
        ]
        if self.q_values:
            lines.append(f"  Q值分布:")
            for strat, q in sorted(self.q_values.items(), key=lambda x: -x[1]):
                lines.append(f"    {strat}: {q:.3f}")
        if self.strategy_actions:
            lines.append(f"  具体行动:")
            for a in self.strategy_actions[:3]:
                lines.append(f"    · {a}")
        if self.recommendations:
            lines.append(f"  建议:")
            for r in self.recommendations[:3]:
                lines.append(f"    💡 {r}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "error_type": self.error_type.value if self.error_type else None,
            "error_description": self.error_description,
            "severity": self.severity,
            "selected_strategy": self.selected_strategy.value if self.selected_strategy else None,
            "strategy_description": self.strategy_description,
            "q_values": dict(sorted(self.q_values.items(), key=lambda x: -x[1])),
            "exploration_rate": self.exploration_rate,
            "is_exploration": self.is_exploration,
            "confidence": self.confidence,
            "strategy_actions": self.strategy_actions[:5],
            "recommendations": self.recommendations[:5],
        }


class QLearningSelfHealing:
    """
    Q-learning 自愈策略选择引擎。

    基于心虫 self-healing-rl.js 的 Q-learning 实现：
      - Q(s,a) = Q(s,a) + lr * (reward + gamma * maxQ(s') - Q(s,a))
      - ε-greedy 探索
      - Q-table 持久化

    8种错误类型 → 4种自愈策略的映射：
      - 错误类型由 detectSelfDeception + PatternDetector 共同判定
      - 策略选择基于 Q-table 的学习经验
      - 初始策略基于 expert knowledge（内置最优匹配）

    参数:
      lr (learning rate): 0.1 — 学习率
      gamma (discount factor): 0.9 — 折扣因子
      epsilon (exploration rate): 0.15 — 探索率
    """

    def __init__(self, lr: float = 0.1, gamma: float = 0.9,
                 epsilon: float = 0.15, persist_path: Optional[str] = None):
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.persist_path = persist_path

        # Q-table: state_key → {strategy_name → q_value}
        self.Q: Dict[str, Dict[str, float]] = {}

        # 学习历史
        self.history: List[QLearningRecord] = []
        self.max_history = 200

        # 错误类型到策略的初始映射（expert knowledge）
        self._default_strategy_map: Dict[ErrorType, HealingStrategy] = {
            ErrorType.CONTROL: HealingStrategy.PATTERN_INTERRUPT,
            ErrorType.PROJECTION: HealingStrategy.EMPATHY_REPAIR,
            ErrorType.SHAME_DRIVEN: HealingStrategy.PAUSE_REFLECT,
            ErrorType.ANXIETY_DRIVEN: HealingStrategy.PAUSE_REFLECT,
            ErrorType.GUILT_DRIVEN: HealingStrategy.EMPATHY_REPAIR,
            ErrorType.DENIAL_AVOIDANCE: HealingStrategy.SUPPORT_SEEKING,
            ErrorType.COMPENSATION_SPIRAL: HealingStrategy.PATTERN_INTERRUPT,
            ErrorType.RATIONALIZATION: HealingStrategy.SUPPORT_SEEKING,
        }

        # 初始Q值（expert knowledge）
        self._init_q_values()

        # 从磁盘恢复
        if persist_path:
            self._load()

    def _init_q_values(self):
        """初始化 Q-table — 基于 expert knowledge 的初始策略偏好"""
        for error_type in ErrorType:
            state = QLearningState(error_type=error_type)
            key = state.to_key()
            if key not in self.Q:
                self.Q[key] = {}

            default_strategy = self._default_strategy_map[error_type]
            for strategy in HealingStrategy:
                if strategy == default_strategy:
                    # 默认策略初始 Q 值更高
                    self.Q[key][strategy.value] = 0.8
                elif strategy in HealingStrategy.details()[strategy]['suitable_for']:
                    # 次优策略
                    self.Q[key][strategy.value] = 0.3
                else:
                    self.Q[key][strategy.value] = 0.0

    def select_strategy(self, error_type: ErrorType,
                        state: Optional[QLearningState] = None,
                        force_exploit: bool = False) -> QLearningReport:
        """
        选择自愈策略 — ε-greedy。

        参数:
            error_type: 错误类型
            state: 可选的状态信息（严重度、历史等）
            force_exploit: 强制利用（不探索）

        返回:
            QLearningReport — 策略选择报告
        """
        if state is None:
            state = QLearningState(error_type=error_type)

        state_key = state.to_key()

        # 确保 Q-table 有此状态
        if state_key not in self.Q:
            self.Q[state_key] = {}
            default = self._default_strategy_map[error_type]
            for strategy in HealingStrategy:
                if strategy == default:
                    self.Q[state_key][strategy.value] = 0.8
                else:
                    self.Q[state_key][strategy.value] = 0.0

        # 当前状态的所有策略Q值
        q_values = dict(self.Q[state_key])

        # ε-greedy 策略选择
        is_exploration = False
        if not force_exploit and random.random() < self.epsilon:
            # 探索：随机选择
            is_exploration = True
            selected = random.choice(list(HealingStrategy))
        else:
            # 利用：选择Q值最高的
            best_strategy_value = max(q_values.items(), key=lambda x: x[1])[0]
            selected = HealingStrategy(best_strategy_value)

        # 构建报告
        strategy_info = HealingStrategy.details()[selected]
        error_desc = ErrorType.descriptions()[error_type]

        # 置信度：基于Q值差距
        sorted_q = sorted(q_values.values(), reverse=True)
        if len(sorted_q) >= 2:
            confidence = min(1.0, (sorted_q[0] - sorted_q[1]) + 0.5)
        else:
            confidence = 0.5

        # 建议
        recommendations = self._generate_recommendations(error_type, selected, state)

        return QLearningReport(
            timestamp=time.time(),
            error_type=error_type,
            error_description=error_desc,
            severity=state.severity,
            selected_strategy=selected,
            strategy_description=strategy_info['description'],
            strategy_actions=strategy_info['typical_actions'],
            q_values=q_values,
            exploration_rate=self.epsilon,
            is_exploration=is_exploration,
            confidence=round(confidence, 4),
            recommendations=recommendations,
        )

    def learn(self, error_type: ErrorType, strategy: HealingStrategy,
              reward: float, state: Optional[QLearningState] = None):
        """
        Q-learning 更新。

        公式: Q(s,a) = Q(s,a) + lr * (reward + gamma * maxQ(s') - Q(s,a))

        参数:
            error_type: 错误类型
            strategy: 采用的策略
            reward: 奖励信号（成功=1.0, 部分成功=0.5, 失败=-0.5）
            state: 可选的状态信息
        """
        if state is None:
            state = QLearningState(error_type=error_type)

        state_key = state.to_key()

        if state_key not in self.Q:
            self.Q[state_key] = {}
            default = self._default_strategy_map[error_type]
            for s in HealingStrategy:
                if s == default:
                    self.Q[state_key][s.value] = 0.8
                else:
                    self.Q[state_key][s.value] = 0.0

        strategy_key = strategy.value
        prev_q = self.Q[state_key].get(strategy_key, 0.0)

        # maxQ(s') — 当前状态下所有策略的最大Q值
        max_next_q = max(self.Q[state_key].values()) if self.Q[state_key] else 0.0

        # Q-learning 更新
        new_q = prev_q + self.lr * (reward + self.gamma * max_next_q - prev_q)
        self.Q[state_key][strategy_key] = round(new_q, 4)

        # 记录学习历史
        record = QLearningRecord(
            state_key=state_key,
            strategy=strategy_key,
            reward=reward,
            timestamp=time.time(),
            success=reward > 0,
        )
        self.history.append(record)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        # 持久化
        if self.persist_path:
            self._save()

    def get_q_values(self, error_type: ErrorType) -> Dict[str, float]:
        """获取某错误类型的Q值分布"""
        state_key = QLearningState(error_type=error_type).to_key()
        return dict(self.Q.get(state_key, {}))

    def stats(self) -> Dict[str, Any]:
        """学习统计"""
        total = len(self.history)
        successes = sum(1 for r in self.history if r.success)
        # 各策略平均奖励
        strategy_rewards: Dict[str, List[float]] = defaultdict(list)
        for r in self.history:
            strategy_rewards[r.strategy].append(r.reward)

        strategy_avg_reward = {
            s: round(sum(rews) / len(rews), 4)
            for s, rews in strategy_rewards.items()
        }

        return {
            "total_episodes": total,
            "success_rate": round(successes / total, 4) if total > 0 else 0,
            "q_table_size": sum(len(v) for v in self.Q.values()),
            "state_count": len(self.Q),
            "strategy_avg_reward": strategy_avg_reward,
            "epsilon": self.epsilon,
            "lr": self.lr,
            "gamma": self.gamma,
            "persisted": self.persist_path is not None,
        }

    def _generate_recommendations(
        self, error_type: ErrorType,
        strategy: HealingStrategy,
        state: QLearningState,
    ) -> List[str]:
        """生成自愈建议"""
        recs = []

        # 错误类型建议
        type_recommendations = {
            ErrorType.CONTROL: [
                "减少控制不是放弃，是给孩子空间也给自己空间",
                "试试用'我建议'替代'你必须'",
            ],
            ErrorType.PROJECTION: [
                "问自己：'这是我需要完成的，还是孩子需要完成的'",
                "你的未完成不等于孩子的未完成",
            ],
            ErrorType.SHAME_DRIVEN: [
                "孩子的行为不是对你的评价",
                "把'我不够好'换成'我需要学习'",
            ],
            ErrorType.ANXIETY_DRIVEN: [
                "焦虑是信号，不是行动指令",
                "把'以后怎么办'换成'现在能做什么'",
            ],
            ErrorType.GUILT_DRIVEN: [
                "内疚不能修复关系，行动可以",
                "从内疚中出来，看看下一步能做什么",
            ],
            ErrorType.DENIAL_AVOIDANCE: [
                "承认问题不是软弱，是力量的开始",
                "回避不会让问题消失，但可以让你准备好再面对",
            ],
            ErrorType.COMPENSATION_SPIRAL: [
                "伤害后的补偿不是修复，真诚的道歉才是",
                "在循环中插入'停'——先不补偿，先修复",
            ],
            ErrorType.RATIONALIZATION: [
                "问自己：'我真的为TA好，还是为我自己好'",
                "去掉'为你好'，剩下的才是真相",
            ],
        }

        recs.extend(type_recommendations.get(error_type, []))

        # 策略建议
        strategy_advice = {
            HealingStrategy.PAUSE_REFLECT: "暂停是改变的开始——在自动反应前给自己3秒",
            HealingStrategy.EMPATHY_REPAIR: "共情不是纵容，是先接住情绪再处理问题",
            HealingStrategy.PATTERN_INTERRUPT: "在循环的任意一环做不一样的事——改变就从那里开始",
            HealingStrategy.SUPPORT_SEEKING: "寻求帮助不是软弱，是智慧的选择",
        }
        recs.append(strategy_advice[strategy])

        return recs[:5]

    def _save(self):
        """持久化 Q-table 和历史到磁盘"""
        if not self.persist_path:
            return
        try:
            path = Path(self.persist_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "Q": self.Q,
                "history": [
                    asdict(r) for r in self.history[-100:]
                ],
                "version": __version__,
                "timestamp": time.time(),
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[QLearningSelfHealing] 保存失败: {e}")

    def _load(self):
        """从磁盘恢复 Q-table"""
        if not self.persist_path:
            return
        try:
            path = Path(self.persist_path)
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.Q = data.get("Q", self.Q)
                raw_history = data.get("history", [])
                for rh in raw_history:
                    self.history.append(QLearningRecord(**rh))
                print(f"[QLearningSelfHealing] 从磁盘恢复: {len(self.Q)}个状态, "
                      f"{len(self.history)}条历史")
        except Exception as e:
            print(f"[QLearningSelfHealing] 加载失败: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# 第四部分: 升级后的3层防御模型 + 心虫自欺检测 + 自愈建议
# 融合 fu-mu-gong-ke 原有3层防御 + 3层孩子需求 + 错位理论
# + 心虫 detectSelfDeception + PatternDetector + Q-learning
# ═══════════════════════════════════════════════════════════════════════════════


class DefenseLayer(IntEnum):
    """3层防御层级"""
    LAYER1_IDENTITY = 1    # 身份保护 — "我不够好"的羞耻感
    LAYER2_INHERITANCE = 2 # 代际认同 — 自动化复制
    LAYER3_PROJECTION = 3  # 投射未来 — 恐惧传递


# fu-mu-gong-ke 原有3层防御定义
DEFENSE_LAYER_INFO = {
    DefenseLayer.LAYER1_IDENTITY: {
        "name": "第1层 — 身份保护",
        "trigger": "孩子不听话",
        "essence": "早期创伤触发——'我不够好'的羞耻感",
        "root": "孩子不服从触发父母自己的羞耻记忆",
        "signals": [
            "孩子犯错时自己的胃收紧",
            "比孩子更愤怒/崩溃",
            "立刻纠正/惩罚",
            "感到'我是失败的家长'",
        ],
        "child_need": {
            "layer": 1,
            "behavior": "说'不'",
            "need": "被看见",
            "essence": "存在确认",
        },
        "self_deception_types": [
            DeceptionType.DENIAL,
            DeceptionType.BLAME_SHIFT,
            DeceptionType.SAY_DO_MISMATCH,
        ],
        "recommended_strategies": [
            HealingStrategy.PAUSE_REFLECT,
            HealingStrategy.EMPATHY_REPAIR,
        ],
        "recovery_path": "觉察→承认→暂停→选择",
    },
    DefenseLayer.LAYER2_INHERITANCE: {
        "name": "第2层 — 代际认同",
        "trigger": "孩子挑战权威",
        "essence": "自动化复制——'我发誓不像父母却还是复制'的背叛感",
        "root": "复制自己父母的模式，感到背叛了自己",
        "signals": [
            "发现自己说的话和父母一模一样",
            "用和父母一样的方式惩罚孩子",
            "控制欲上来时无法停止",
            "事后说'我怎么变成我爸妈了'",
        ],
        "child_need": {
            "layer": 2,
            "behavior": "试探边界",
            "need": "学习规则",
            "essence": "边界探索",
        },
        "self_deception_types": [
            DeceptionType.RATIONALIZATION,
            DeceptionType.IDEALIZATION,
            DeceptionType.PROJECTION,
        ],
        "recommended_strategies": [
            HealingStrategy.PATTERN_INTERRUPT,
            HealingStrategy.SUPPORT_SEEKING,
        ],
        "recovery_path": "看见→理解→接纳→选择不同",
    },
    DefenseLayer.LAYER3_PROJECTION: {
        "name": "第3层 — 投射未来",
        "trigger": "孩子将来可能失败",
        "essence": "恐惧传递——把自己对未来的焦虑当成对孩子的责任",
        "root": "把自己对未来的焦虑投射到孩子身上",
        "signals": [
            "把成绩/分数等同于孩子的人生",
            "'以后怎么办'的焦虑驱动当下的控制",
            "用自己的恐惧想象孩子的未来",
            "把'为孩子好'等同于'让孩子按我的路走'",
        ],
        "child_need": {
            "layer": 3,
            "behavior": "'我不要你管'",
            "need": "成为自己",
            "essence": "自主建立",
        },
        "self_deception_types": [
            DeceptionType.CONTRADICTION,
            DeceptionType.SELF_DECEPTION,
            DeceptionType.RATIONALIZATION,
        ],
        "recommended_strategies": [
            HealingStrategy.PAUSE_REFLECT,
            HealingStrategy.SUPPORT_SEEKING,
        ],
        "recovery_path": "分离→信任→放手→祝福",
    },
}


@dataclass
class DefenseLayerAnalysis:
    """单层防御分析"""
    layer: DefenseLayer
    triggered: bool = False
    confidence: float = 0.0
    matched_signals: List[str] = field(default_factory=list)
    deception_signals: List[DeceptionSignal] = field(default_factory=list)
    patterns: List[BehaviorPattern] = field(default_factory=list)
    q_learning_report: Optional[QLearningReport] = None
    recommended_strategy: Optional[HealingStrategy] = None
    self_deception_type: Optional[DeceptionType] = None


@dataclass
class UpgradeDefenseReport:
    """
    升级版3层防御分析报告 — 融合心虫全部检测机制。

    包含：
      - 每层防御的触发状态 + 置信度
      - 每层的自欺检测结果
      - 每层的行为模式分析
      - 每层的 Q-learning 策略推荐
      - 综合自愈建议
      - 错位理论分析
    """
    timestamp: float = 0.0
    layers: Dict[int, DefenseLayerAnalysis] = field(default_factory=dict)
    self_deception_report: Optional[SelfDeceptionReport] = None
    pattern_detector_report: Optional[PatternDetectorReport] = None
    q_learning_report: Optional[QLearningReport] = None
    child_needs: Dict[int, Dict] = field(default_factory=dict)  # 3层孩子需求
    misalignment_analysis: List[str] = field(default_factory=list)  # 错位分析
    overall_recommendations: List[str] = field(default_factory=list)
    recovery_path: str = ""

    def summary(self) -> str:
        lines = [
            "=" * 60,
            "🧠 心虫防御分析引擎 — 升级版防御分析报告",
            "=" * 60,
        ]

        # 各层防御
        for layer_num in sorted(self.layers.keys()):
            analysis = self.layers[layer_num]
            info = DEFENSE_LAYER_INFO.get(DefenseLayer(layer_num), {})
            trigger_emoji = "⚠️" if analysis.triggered else "✅"
            lines.append(f"\n{trigger_emoji} {info.get('name', f'第{layer_num}层')}")
            lines.append(f"   触发: {analysis.triggered} (置信度: {analysis.confidence:.2f})")
            if analysis.matched_signals:
                lines.append(f"   信号: {'; '.join(analysis.matched_signals[:3])}")
            if analysis.deception_signals:
                lines.append(f"   自欺: {len(analysis.deception_signals)}个信号")
            if analysis.patterns:
                lines.append(f"   模式: {len(analysis.patterns)}个")
            if analysis.recommended_strategy:
                strat_info = HealingStrategy.details()[analysis.recommended_strategy]
                lines.append(f"   策略: {strat_info['name']}")

        # 孩子需求
        if self.child_needs:
            lines.append(f"\n👶 3层孩子需求")
            for layer_num, need in sorted(self.child_needs.items()):
                lines.append(f"   第{layer_num}层: {need.get('behavior', '')} → "
                             f"需要{need.get('need', '')} ({need.get('essence', '')})")

        # 错位分析
        if self.misalignment_analysis:
            lines.append(f"\n🌉 错位分析")
            for a in self.misalignment_analysis:
                lines.append(f"   {a}")

        # 自欺检测
        if self.self_deception_report and self.self_deception_report.detected:
            lines.append(f"\n{self.self_deception_report.summary()}")

        # 模式检测
        if self.pattern_detector_report and self.pattern_detector_report.patterns:
            lines.append(f"\n{self.pattern_detector_report.summary()}")

        # 综合建议
        if self.overall_recommendations:
            lines.append(f"\n💡 综合建议")
            for r in self.overall_recommendations:
                lines.append(f"   · {r}")

        if self.recovery_path:
            lines.append(f"\n🛤️ 恢复路径: {self.recovery_path}")

        lines.append(f"\n{'=' * 60}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "layers": {
                str(k): {
                    "triggered": v.triggered,
                    "confidence": v.confidence,
                    "matched_signals": v.matched_signals[:5],
                    "deception_signals": [
                        {"type": s.type.value, "text": s.text[:40], "confidence": s.confidence}
                        for s in v.deception_signals[:3]
                    ],
                    "pattern_count": len(v.patterns),
                    "recommended_strategy": v.recommended_strategy.value if v.recommended_strategy else None,
                }
                for k, v in self.layers.items()
            },
            "self_deception": self.self_deception_report.to_dict() if self.self_deception_report else None,
            "pattern_detector": self.pattern_detector_report.to_dict() if self.pattern_detector_report else None,
            "q_learning": self.q_learning_report.to_dict() if self.q_learning_report else None,
            "child_needs": {
                str(k): v for k, v in self.child_needs.items()
            },
            "misalignment_analysis": self.misalignment_analysis[:5],
            "recommendations": self.overall_recommendations[:8],
            "recovery_path": self.recovery_path,
        }


class HeartFlowDefenseUpgrade:
    """
    心虫防御分析引擎 — 统一入口。

    整合四大模块：
      1) DetectSelfDeception — 自欺检测
      2) PatternDetector — 行为模式检测
      3) QLearningSelfHealing — Q-learning 自愈策略选择
      4) 升级版3层防御模型

    使用方法：
        engine = HeartFlowDefenseUpgrade()
        report = engine.analyze("我打了孩子，很后悔...")
        print(report.summary())

    也可单独使用各子模块：
        engine.self_deception.detect(text)
        engine.pattern_detector.detect(text)
        engine.q_learning.select_strategy(error_type)
    """

    def __init__(self, persist_path: Optional[str] = None):
        self.self_deception = DetectSelfDeception()
        self.pattern_detector = PatternDetector()
        self.q_learning = QLearningSelfHealing(
            persist_path=persist_path or str(
                Path(__file__).parent.parent / "data" / "defense_q_table.json"
            )
        )
        self.version = __version__

    def analyze(self, text: str, history: Optional[List[str]] = None) -> UpgradeDefenseReport:
        """
        执行完整的升级版防御分析。

        参数:
            text: 用户输入文本
            history: 可选的对话历史

        返回:
            UpgradeDefenseReport — 完整的防御分析报告
        """
        if not text or not text.strip():
            return UpgradeDefenseReport(timestamp=time.time())

        # Step 1: 自欺检测
        deception_report = self.self_deception.detect(text)

        # Step 2: 模式检测
        pattern_report = self.pattern_detector.detect(text, history)

        # Step 3: 逐层防御分析
        layers: Dict[int, DefenseLayerAnalysis] = {}
        for layer_num in [1, 2, 3]:
            layer = DefenseLayer(layer_num)
            info = DEFENSE_LAYER_INFO[layer]

            analysis = self._analyze_layer(
                layer=layer,
                text=text,
                deception_report=deception_report,
                pattern_report=pattern_report,
            )
            layers[layer_num] = analysis

        # Step 4: 综合错误类型判定
        error_type = self._determine_error_type(layers, deception_report, pattern_report)
        if error_type:
            severity = max(
                (a.confidence for a in layers.values() if a.triggered),
                default=0.5
            )
            state = QLearningState(
                error_type=error_type,
                severity=severity,
                defense_layer=max(
                    (k for k, v in layers.items() if v.triggered),
                    default=1
                ),
            )
            ql_report = self.q_learning.select_strategy(error_type, state)
        else:
            ql_report = None

        # Step 5: 孩子需求分析
        child_needs = self._analyze_child_needs(text, layers)

        # Step 6: 错位理论分析
        misalignment = self._analyze_misalignment(layers, child_needs)

        # Step 7: 综合建议
        recommendations = self._generate_overall_recommendations(
            layers, deception_report, pattern_report, ql_report
        )

        # Step 8: 恢复路径
        recovery_path = self._determine_recovery_path(layers)

        return UpgradeDefenseReport(
            timestamp=time.time(),
            layers=layers,
            self_deception_report=deception_report,
            pattern_detector_report=pattern_report,
            q_learning_report=ql_report,
            child_needs=child_needs,
            misalignment_analysis=misalignment,
            overall_recommendations=recommendations,
            recovery_path=recovery_path,
        )

    def _analyze_layer(
        self,
        layer: DefenseLayer,
        text: str,
        deception_report: SelfDeceptionReport,
        pattern_report: PatternDetectorReport,
    ) -> DefenseLayerAnalysis:
        """分析单层防御"""
        info = DEFENSE_LAYER_INFO[layer]

        # 检测触发信号
        matched_signals = []
        for signal in info['signals']:
            if signal in text:
                matched_signals.append(signal)

        # 关联自欺信号
        layer_deception_signals = [
            s for s in deception_report.signals
            if s.layer == layer.value
        ]

        # 关联行为模式
        layer_patterns = [
            p for p in pattern_report.patterns
            if p.linked_defense_layer == layer.value
        ]

        # 触发判定
        triggered = bool(matched_signals) or len(layer_deception_signals) > 0 or bool(layer_patterns)

        # 置信度计算
        confidence = 0.0
        if matched_signals:
            confidence += len(matched_signals) * 0.2
        if layer_deception_signals:
            confidence += sum(s.confidence for s in layer_deception_signals) * 0.3
        if layer_patterns:
            confidence += sum(p.severity for p in layer_patterns) * 0.2
        confidence = min(1.0, confidence)

        # 策略推荐
        recommended = None
        if triggered:
            # 使用 Q-learning 推荐（如果有学习经验）
            for error_type in info['self_deception_types']:
                q_values = self.q_learning.get_q_values(error_type)
                if q_values:
                    best_strategy = max(q_values.items(), key=lambda x: x[1])[0]
                    recommended = HealingStrategy(best_strategy)
                    break

            # 如果没有学习经验，使用默认推荐
            if not recommended and info['recommended_strategies']:
                recommended = info['recommended_strategies'][0]

        return DefenseLayerAnalysis(
            layer=layer,
            triggered=triggered,
            confidence=round(confidence, 4),
            matched_signals=matched_signals[:5],
            deception_signals=layer_deception_signals[:5],
            patterns=layer_patterns[:5],
            recommended_strategy=recommended,
        )

    def _determine_error_type(
        self,
        layers: Dict[int, DefenseLayerAnalysis],
        deception_report: SelfDeceptionReport,
        pattern_report: PatternDetectorReport,
    ) -> Optional[ErrorType]:
        """综合判定错误类型"""
        # 基于触发的防御层级 — 这是最可靠的判定方式
        triggered_layers = [k for k, v in layers.items() if v.triggered]
        if 1 in triggered_layers:
            return ErrorType.SHAME_DRIVEN
        elif 2 in triggered_layers:
            return ErrorType.CONTROL
        elif 3 in triggered_layers:
            return ErrorType.ANXIETY_DRIVEN

        # 基于自欺类型
        if deception_report.primary_type:
            dt = deception_report.primary_type
            # 映射自欺类型到错误类型
            if dt in (DeceptionType.DENIAL,):
                return ErrorType.DENIAL_AVOIDANCE
            elif dt in (DeceptionType.PROJECTION,):
                return ErrorType.PROJECTION
            elif dt in (DeceptionType.RATIONALIZATION,):
                return ErrorType.RATIONALIZATION
            elif dt in (DeceptionType.SAY_DO_MISMATCH, DeceptionType.CONTRADICTION):
                return ErrorType.CONTROL

        # 基于模式检测
        if pattern_report.primary_pattern:
            pt = pattern_report.primary_pattern.type
            if pt == BehaviorPatternType.CYCLE:
                return ErrorType.COMPENSATION_SPIRAL
            elif pt == BehaviorPatternType.AVOIDANCE:
                return ErrorType.DENIAL_AVOIDANCE
            elif pt == BehaviorPatternType.COMPENSATION:
                return ErrorType.COMPENSATION_SPIRAL

        return None

    def _analyze_child_needs(self, text: str,
                             layers: Dict[int, DefenseLayerAnalysis]) -> Dict[int, Dict]:
        """分析3层孩子需求"""
        needs = {}
        for layer_num, info in DEFENSE_LAYER_INFO.items():
            child = info['child_need']
            needs[layer_num.value] = {
                "layer": child['layer'],
                "behavior": child['behavior'],
                "need": child['need'],
                "essence": child['essence'],
                "is_blocked": layers.get(layer_num.value, DefenseLayerAnalysis(
                    layer=layer_num)).triggered if layer_num.value in layers else False,
            }
        return needs

    def _analyze_misalignment(
        self,
        layers: Dict[int, DefenseLayerAnalysis],
        child_needs: Dict[int, Dict],
    ) -> List[str]:
        """错位理论分析"""
        misalignments = []

        for layer_num, need in child_needs.items():
            defense = layers.get(layer_num)
            if defense and defense.triggered:
                info = DEFENSE_LAYER_INFO.get(DefenseLayer(layer_num), {})
                misalignments.append(
                    f"第{layer_num}层错位: 父母的{info.get('essence', '防御')} "
                    f"阻碍了孩子的{need.get('need', '需求')}"
                )

        if not misalignments:
            misalignments.append("未检测到明显错位")

        return misalignments

    def _generate_overall_recommendations(
        self,
        layers: Dict[int, DefenseLayerAnalysis],
        deception_report: SelfDeceptionReport,
        pattern_report: PatternDetectorReport,
        ql_report: Optional[QLearningReport],
    ) -> List[str]:
        """生成综合建议"""
        recs = []

        # 基于触发层级的建议
        triggered = [k for k, v in layers.items() if v.triggered]
        if 1 in triggered:
            recs.append("第1层防御触发：你的羞耻感被激活了——这不是你的错，是过去的回响")
        if 2 in triggered:
            recs.append("第2层防御触发：你在复制自己父母的模式——看见就是改变的开始")
        if 3 in triggered:
            recs.append("第3层防御触发：你在用对未来的焦虑驱动现在的行动——把焦虑和孩子分开")

        # 自欺建议
        if deception_report.detected and deception_report.recommendations:
            recs.extend(deception_report.recommendations[:2])

        # 模式建议
        if pattern_report.recommendations:
            recs.extend(pattern_report.recommendations[:2])

        # Q-learning 策略建议
        if ql_report and ql_report.selected_strategy:
            strat_info = HealingStrategy.details()[ql_report.selected_strategy]
            recs.append(f"推荐策略: {strat_info['name']} — {strat_info['description']}")
            for action in strat_info['typical_actions'][:2]:
                recs.append(f"  → {action}")

        # 核心提醒
        recs.append("觉察(看见防御)→接纳(慈悲是体)→暂停(给空间)→选择(爱是用)")

        return recs[:10]

    def _determine_recovery_path(self, layers: Dict[int, DefenseLayerAnalysis]) -> str:
        """确定恢复路径"""
        triggered = [k for k, v in layers.items() if v.triggered]

        if not triggered:
            return "无需干预——继续觉察即可"

        if 1 in triggered and 2 in triggered and 3 in triggered:
            return "三层防御全触发 → 建议从第1层开始: 觉察→承认→暂停→选择"
        elif 1 in triggered:
            return "第1层防御触发 → 觉察羞耻感: 觉察→承认→暂停→选择"
        elif 2 in triggered:
            return "第2层防御触发 → 理解代际模式: 看见→理解→接纳→选择不同"
        elif 3 in triggered:
            return "第3层防御触发 → 分离恐惧: 分离→信任→放手→祝福"
        else:
            return "继续保持觉察"

    def learn_from_outcome(self, error_type: ErrorType, strategy: HealingStrategy,
                           reward: float, state: Optional[QLearningState] = None):
        """
        从结果中学习 — 更新 Q-table。

        在用户反馈后调用，用于优化后续的策略选择。

        参数:
            error_type: 之前判定的错误类型
            strategy: 采用的策略
            reward: 奖励信号（成功=1.0, 部分=0.5, 失败=-0.5）
            state: 可选的状态信息
        """
        self.q_learning.learn(error_type, strategy, reward, state)

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计信息"""
        return {
            "version": self.version,
            "q_learning": self.q_learning.stats(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """CLI 入口：测试和演示"""
    import sys

    engine = HeartFlowDefenseUpgrade()
    print(f"🧠 心虫防御分析引擎 v{__version__}")
    print("=" * 60)

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        report = engine.analyze(text)
        print(report.summary())
    else:
        # 自测案例
        test_cases = [
            (
                "我打了孩子，很后悔。我知道不该打，但当时实在忍不住。"
                "他说不想写作业，我一下就火了。",
                "父母打孩子+后悔+触发模式"
            ),
            (
                "我儿子成绩下降了，我焦虑得睡不着。"
                "他以后怎么办？考不上好学校怎么办？"
                "我知道不应该太紧张，但控制不住。",
                "焦虑驱动+投射未来"
            ),
            (
                "我对孩子说'我都是为你好'，但他根本不领情。"
                "我小时候就是没人管才这样的，所以我必须管他。",
                "投射+合理性化+代际复制"
            ),
            (
                "我发现我说话的方式越来越像我爸妈了。"
                "我发誓过不要像他们一样，但现在我控制不住。"
                "每次发完火我都特别内疚，然后给他买东西补偿。",
                "代际复制+补偿循环"
            ),
            (
                "孩子最近叛逆期，我说什么他都顶嘴。"
                "我气死了，但我不想变成控制型的家长。"
                "有时候真的很累，觉得没人理解我。",
                "青春期冲突+回避+倦怠"
            ),
            (
                "我试过很多方法了，都没用。"
                "看书、听课、深呼吸，但到时候还是控制不住。"
                "也许我就是这样的父母吧。",
                "改变失败+自我否定"
            ),
        ]

        for text, desc in test_cases:
            print(f"\n{'─' * 60}")
            print(f"📝 测试: [{desc}]")
            print(f"输入: {text[:60]}...")
            print(f"{'─' * 60}")

            report = engine.analyze(text)
            print(report.summary())

    print(f"\n{'=' * 60}")
    print(f"引擎统计:")
    stats = engine.get_stats()
    for k, v in stats.items():
        if k != "q_learning":
            print(f"  {k}: {v}")
        else:
            print(f"  Q-learning: {v.get('q_table_size', 0)}个Q值, "
                  f"{v.get('total_episodes', 0)}次学习, "
                  f"成功率={v.get('success_rate', 0)}")


if __name__ == "__main__":
    main()
