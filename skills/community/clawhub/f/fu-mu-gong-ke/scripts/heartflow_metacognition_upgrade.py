#!/usr/bin/env python3
"""
心虫元认知控制层 (HeartFlow Meta-Cognition Control Layer) v1.0.0
===============================================================

基于心虫 HeartFlow v11.6+ 的四个元认知能力，集成到 fu-mu-gong-ke 的回应管线中：

1) ConfidenceCalibrator — 回答前标注置信度(0-1)，自动校准语言强度
2) SpontaneousRestraint — shouldBeSilent 检测（何时沉默比说话更有力量）
3) TrustRepairEngine — 信任修复五阶段（承认→道歉→补偿→监控→重建）
4) CollectiveIntentionality — 集体意向性 We-Intention 公式（目标共享×行动互赖×相互响应×承诺约束×信任融合）

理论来源：
- HeartFlow confidence-calibrator.js v11.6.2（柔弱胜刚强 / 道德经第78章）
- HeartFlow spontaneous-restraint.js v11.6.3（道法自然 / 上善若水）
- Stanford Encyclopedia of Philosophy: Collective Intentionality (2023)
- Searle (1990, 1995): 集体意向性的原始性
- Gilbert (1990): 联合承诺与信任修复
- Lewicki & Bunker (1996): 信任修复的阶段性模型
- Kim et al. (2004): 道歉与补偿的信任修复机制

设计目标：
- 元认知层不替代原有回应管线，而是作为"前置过滤+后置校准"
- 每个模块独立可插拔，通过 integrate() 统一挂载到 system_integrator
- 育儿场景特别优化：父母情绪失控后的信任修复、集体养育目标协调

Version: 1.0.0
"""

from __future__ import annotations
import re
import math
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Set, Any, Callable
from enum import Enum, auto

__version__ = "1.0.0"

# =============================================================================
# 第一部分: 常量与类型定义
# =============================================================================

# 置信度等级
class ConfidenceLevel(Enum):
    VERY_HIGH = "very_high"    # ≥ 0.85 — 确定
    HIGH = "high"              # ≥ 0.70 — 很可能
    MEDIUM = "medium"          # ≥ 0.50 — 可能
    LOW = "low"                # ≥ 0.30 — 不太确定
    VERY_LOW = "very_low"      # < 0.30 — 不知道/无法判断

# 干预等级
class InterventionLevel(Enum):
    SILENT = "silent"          # 完全沉默
    MINIMAL = "minimal"        # 最小有效回应
    FULL = "full"              # 完整回答

# 信任修复阶段
class RepairStage(Enum):
    ADMIT = "admit"            # 阶段1: 承认
    APOLOGIZE = "apologize"    # 阶段2: 道歉
    COMPENSATE = "compensate"  # 阶段3: 补偿
    MONITOR = "monitor"        # 阶段4: 监控
    REBUILD = "rebuild"        # 阶段5: 重建


# =============================================================================
# 第二部分: ConfidenceCalibrator — 置信度校准器
# =============================================================================

@dataclass
class CalibrationResult:
    """置信度校准结果"""
    raw_score: float            # 原始置信度 0-1
    level: ConfidenceLevel      # 置信度等级
    calibrated_score: float     # 校准后的置信度
    dimension_scores: Dict[str, float]  # 各维度评分
    forbidden_words_used: List[str]     # 检测到的刚强词汇
    language_notes: List[str]          # 语言调整建议


class ConfidenceCalibrator:
    """
    心虫置信度校准器 — 回答前标注置信度(0-1)，自动校准语言强度。

    核心哲学：柔弱胜刚强（《道德经》第78章）
    承认不确定性才是真正的力量。

    移植自 HeartFlow confidence-calibrator.js v11.6.2
    """

    # 刚强词汇（置信度低时禁止使用）
    FORBIDDEN_HIGH_CONFIDENCE: Set[str] = {
        '绝对', '肯定', '毫无疑问', '100%', '必然',
        '必定', '无疑', '无可置疑', '不容置疑',
        '一定', '百分之百', '铁定',
    }

    # 中文刚强词汇的扩展育儿版（fu-mu-gong-ke 定制）
    PARENTING_FORBIDDEN: Set[str] = {
        '你一定是', '你肯定是', '你绝对', '你永远都',
        '你从来', '你总是', '你就是', '你这孩子就是',
    }

    # 置信度阈值
    THRESHOLDS: Dict[ConfidenceLevel, float] = {
        ConfidenceLevel.VERY_HIGH: 0.85,
        ConfidenceLevel.HIGH: 0.70,
        ConfidenceLevel.MEDIUM: 0.50,
        ConfidenceLevel.LOW: 0.30,
        ConfidenceLevel.VERY_LOW: 0.0,
    }

    # 置信度 → 中文校准短语
    CALIBRATION_PHRASES: Dict[ConfidenceLevel, List[str]] = {
        ConfidenceLevel.VERY_HIGH: ['这是确定的', '这点很清楚'],
        ConfidenceLevel.HIGH: ['很可能', '大概率', '根据现有信息判断'],
        ConfidenceLevel.MEDIUM: ['也许', '可能', '在某种程度上'],
        ConfidenceLevel.LOW: ['不确定', '不太确定', '这需要进一步验证'],
        ConfidenceLevel.VERY_LOW: ['我不知道', '这超出了我的判断范围', '这个问题我不确定'],
    }

    # 育儿场景专用短语
    PARENTING_PHRASES: Dict[ConfidenceLevel, List[str]] = {
        ConfidenceLevel.HIGH: ['根据儿童发展心理学研究', '从育儿角度看'],
        ConfidenceLevel.MEDIUM: ['每个孩子不同，但一般来说', '可能在你的情况下'],
        ConfidenceLevel.LOW: ['我不确定你的孩子是否也这样', '这需要你观察自己的情况'],
        ConfidenceLevel.VERY_LOW: ['每个家庭都不同，我无法给出确定建议', '这超出了我能判断的范围'],
    }

    def __init__(self, memory_path: Optional[str] = None):
        self.memory_path = memory_path
        self.records: List[Dict] = []  # 历史反馈记录
        self.thresholds = dict(self.THRESHOLDS)

        # 权重（可调整，通过反馈校准）
        self.weights = {
            'evidence_coverage': 0.25,    # 证据覆盖
            'consistency': 0.20,           # 逻辑一致性
            'specificity': 0.15,           # 具体程度
            'source_reliability': 0.20,    # 来源可靠性
            'complexity_fit': 0.20,        # 复杂度匹配
        }

        self._load()

    # ------------------------------------------------------------------
    # 核心API
    # ------------------------------------------------------------------

    def assess(self, text: str = '', context: Optional[Dict] = None) -> CalibrationResult:
        """
        评估一段文本的置信度。

        Args:
            text: 待评估的文本
            context: 可选的上下文信息
                - has_evidence: bool
                - domain: str (technical, opinion, parenting, crisis)
                - query_complexity: float (0-1)
                - is_parenting: bool (是否育儿场景)

        Returns:
            CalibrationResult
        """
        ctx = context or {}

        # 1. 计算各维度评分
        scores = {
            'evidence_coverage': self._score_evidence_coverage(text, ctx),
            'consistency': self._score_consistency(text),
            'specificity': self._score_specificity(text),
            'source_reliability': self._score_source_reliability(text, ctx),
            'complexity_fit': self._score_complexity_fit(text, ctx),
        }

        # 2. 加权总分
        raw_score = sum(
            score * self.weights.get(dim, 0)
            for dim, score in scores.items()
        )
        raw_score = max(0.0, min(1.0, raw_score))

        # 3. 确定等级
        level = self._score_to_level(raw_score)

        # 4. 应用校准（轻微向下调整，防止过度自信）
        calibrated = self._apply_calibration(raw_score)

        # 5. 检测刚强词汇
        forbidden_used = self._detect_forbidden_words(text, level, ctx.get('is_parenting', False))

        # 6. 语言调整建议
        notes = self._get_language_notes(level, scores, forbidden_used, ctx)

        return CalibrationResult(
            raw_score=round(raw_score, 3),
            level=level,
            calibrated_score=round(calibrated, 3),
            dimension_scores=scores,
            forbidden_words_used=forbidden_used,
            language_notes=notes,
        )

    def calibrate_text(self, text: str, context: Optional[Dict] = None) -> Dict:
        """
        校准一段文本的语言表达。

        Returns:
            dict with keys: text (校准后), adjusted (bool), notes (List[str])
        """
        result = self.assess(text, context)

        adjusted_text = text
        notes = list(result.language_notes)

        if result.level in (ConfidenceLevel.LOW, ConfidenceLevel.VERY_LOW):
            # 替换刚强词汇
            for word in result.forbidden_words_used:
                replacement = self._get_replacement(result.level)
                adjusted_text = adjusted_text.replace(word, replacement)

            # 添加校准短语
            is_parenting = (context or {}).get('is_parenting', False)
            phrase_pool = self.PARENTING_PHRASES if is_parenting else self.CALIBRATION_PHRASES
            phrases = phrase_pool.get(result.level, [])
            if phrases and len(adjusted_text) > 30:
                phrase = phrases[0]
                if phrase not in adjusted_text:
                    adjusted_text = adjusted_text.rstrip('。，') + f'（{phrase}）'
                    notes.append(f'已添加置信度标注: {phrase}')

        return {
            'text': adjusted_text,
            'adjusted': adjusted_text != text,
            'confidence': asdict(result),
            'notes': notes,
        }

    def record_feedback(self, text: str = '', was_correct: Optional[bool] = None) -> None:
        """记录用户反馈，用于持续校准"""
        if was_correct is None:
            return

        self.records.append({
            'text': text[:200],
            'calibrated': asdict(self.assess(text)),
            'feedback': was_correct,
            'ts': time.time(),
        })

        # 保持最近100条
        if len(self.records) > 100:
            self.records = self.records[-100:]

        # 持续校准
        self._recalibrate()
        self._save()

    # ------------------------------------------------------------------
    # 评分维度
    # ------------------------------------------------------------------

    def _score_evidence_coverage(self, text: str, context: Dict) -> float:
        """证据覆盖度评分"""
        has_evidence = bool(re.search(r'证据|研究|数据|论文|来源|调查显示|统计|研究表明', text))
        has_citation = bool(re.search(r'\[\d+\]|\(\d{4}\)|arXiv:', text))
        has_qualifier = bool(re.search(r'根据|来自|来自.*显示', text))
        context_evidence = context.get('has_evidence', False)

        score = 0.5
        if has_evidence:
            score += 0.2
        if has_citation:
            score += 0.15
        if has_qualifier:
            score += 0.1
        if context_evidence:
            score += 0.15

        return min(score, 1.0)

    def _score_consistency(self, text: str) -> float:
        """逻辑一致性评分"""
        # 检测自相矛盾
        contradictions = [
            r'但是.*然而', r'虽然.*但是.*仍然',
            r'既.*又.*矛盾', r'一方面.*另一方面.*不同',
        ]
        score = 0.8
        for c in contradictions:
            if re.search(c, text):
                score -= 0.15

        # 长度合理性
        words = len(text)
        if words < 10:
            score -= 0.2
        if words > 2000:
            score -= 0.1

        return max(score, 0.1)

    def _score_specificity(self, text: str) -> float:
        """具体程度评分"""
        has_vague = bool(re.search(r'可能|也许|大概|似乎|好像|说不定', text))
        has_specific = bool(re.search(r'具体|明确|数据显示|是.*而不是.*是|具体来说', text))
        has_numbers = len(re.findall(r'\d+', text)) > 0

        score = 0.5
        if has_vague:
            score -= 0.1
        if has_specific:
            score += 0.2
        if has_numbers:
            score += 0.15

        return max(0.1, min(1.0, score))

    def _score_source_reliability(self, text: str, context: Dict) -> float:
        """来源可靠性评分"""
        has_reliable = bool(re.search(r'研究|论文|学术|研究机构|官方|权威|调查|数据', text))
        has_unreliable = bool(re.search(r'据说|传闻|网传|有人说|不明来源', text))

        score = 0.5
        if has_reliable:
            score += 0.3
        if has_unreliable:
            score -= 0.3

        domain = context.get('domain', '')
        if domain == 'technical':
            score += 0.15
        elif domain == 'opinion':
            score -= 0.1
        elif domain == 'parenting':
            # 育儿场景：经验性内容需要降低置信度
            if not has_reliable:
                score -= 0.1

        return max(0.1, min(1.0, score))

    def _score_complexity_fit(self, text: str, context: Dict) -> float:
        """复杂度匹配评分"""
        query_complexity = context.get('query_complexity', 0.5)
        sentences = len(re.findall(r'[。；!?]', text))
        optimal_length = max(query_complexity * 10, 2)

        score = 0.5
        if sentences > 0:
            ratio = sentences / optimal_length
            if 0.7 < ratio < 2.0:
                score += 0.3
            elif ratio < 0.3:
                score -= 0.2
            elif ratio > 3.0:
                score -= 0.15
        else:
            score -= 0.2

        return max(0.1, min(1.0, score))

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def _score_to_level(self, score: float) -> ConfidenceLevel:
        """分数转等级"""
        if score >= self.thresholds.get(ConfidenceLevel.VERY_HIGH, 0.85):
            return ConfidenceLevel.VERY_HIGH
        elif score >= self.thresholds.get(ConfidenceLevel.HIGH, 0.70):
            return ConfidenceLevel.HIGH
        elif score >= self.thresholds.get(ConfidenceLevel.MEDIUM, 0.50):
            return ConfidenceLevel.MEDIUM
        elif score >= self.thresholds.get(ConfidenceLevel.LOW, 0.30):
            return ConfidenceLevel.LOW
        return ConfidenceLevel.VERY_LOW

    def _apply_calibration(self, raw_score: float) -> float:
        """应用校准（轻微向下调整，防止过度自信）"""
        if raw_score > 0.8:
            return round(raw_score - 0.05, 3)
        return round(raw_score, 3)

    def _detect_forbidden_words(self, text: str, level: ConfidenceLevel,
                                 is_parenting: bool = False) -> List[str]:
        """检测刚强词汇"""
        if level in (ConfidenceLevel.VERY_HIGH, ConfidenceLevel.HIGH):
            return []

        forbidden = set(self.FORBIDDEN_HIGH_CONFIDENCE)
        if is_parenting:
            forbidden |= self.PARENTING_FORBIDDEN

        return [w for w in forbidden if w in text]

    def _get_replacement(self, level: ConfidenceLevel) -> str:
        """根据置信度等级获取替代词"""
        replacements = {
            ConfidenceLevel.VERY_HIGH: '确定',
            ConfidenceLevel.HIGH: '很可能',
            ConfidenceLevel.MEDIUM: '可能',
            ConfidenceLevel.LOW: '不确定是',
            ConfidenceLevel.VERY_LOW: '不知道是否',
        }
        return replacements.get(level, '可能')

    def _get_language_notes(self, level: ConfidenceLevel, scores: Dict,
                             forbidden_used: List[str], context: Dict) -> List[str]:
        """生成语言调整建议"""
        notes = []

        if level == ConfidenceLevel.VERY_LOW:
            notes.append('置信度极低，建议明确告知"不知道"或引导用户查询权威来源')
        elif level == ConfidenceLevel.LOW:
            notes.append('置信度较低，建议在回答末尾加上不确定性说明')
        elif level == ConfidenceLevel.MEDIUM:
            notes.append('置信度中等，建议表达为"可能"而非"是"，提供多角度分析')

        if scores.get('evidence_coverage', 0) < 0.5:
            notes.append('证据覆盖度低，建议补充来源或说明数据基础')

        if forbidden_used:
            notes.append(f'检测到刚强词汇: {", ".join(forbidden_used)}，建议替换为更柔和的表达')

        if context.get('is_parenting') and level.value in ('low', 'very_low'):
            notes.append('育儿场景建议：用"你的孩子可能……"替代"孩子就是……"')

        return notes

    def _recalibrate(self) -> None:
        """基于历史反馈调整阈值"""
        if len(self.records) < 5:
            return

        recent = self.records[-20:]
        overconfident = 0
        underconfident = 0

        for r in recent:
            cal = r.get('calibrated', {})
            level_name = cal.get('level', 'medium')
            feedback = r.get('feedback')
            if feedback is False and level_name not in ('very_low', 'low'):
                overconfident += 1
            if feedback is True and level_name == 'very_low':
                underconfident += 1

        total = len(recent)
        if overconfident > total * 0.3:
            vh = self.thresholds.get(ConfidenceLevel.VERY_HIGH, 0.85)
            h = self.thresholds.get(ConfidenceLevel.HIGH, 0.70)
            self.thresholds[ConfidenceLevel.VERY_HIGH] = min(vh + 0.02, 0.95)
            self.thresholds[ConfidenceLevel.HIGH] = min(h + 0.02, 0.80)

        if underconfident > total * 0.2:
            vl = self.thresholds.get(ConfidenceLevel.VERY_LOW, 0.0)
            self.thresholds[ConfidenceLevel.VERY_LOW] = max(vl - 0.02, 0.05)

    # ------------------------------------------------------------------
    # 持久化
    # ------------------------------------------------------------------

    def _save(self) -> None:
        if not self.memory_path:
            return
        try:
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'records': self.records[-50:],
                    'weights': self.weights,
                    'thresholds': {k.value: v for k, v in self.thresholds.items()},
                    'version': __version__,
                }, f, ensure_ascii=False, indent=2)
        except (OSError, IOError):
            pass

    def _load(self) -> None:
        if not self.memory_path:
            return
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data.get('records'):
                self.records = data['records']
            if data.get('weights'):
                self.weights.update(data['weights'])
            if data.get('thresholds'):
                for k_str, v in data['thresholds'].items():
                    for level in ConfidenceLevel:
                        if level.value == k_str:
                            self.thresholds[level] = v
                            break
        except (OSError, IOError, json.JSONDecodeError):
            pass

    def stats(self) -> Dict:
        """返回状态摘要"""
        return {
            'version': __version__,
            'records': len(self.records),
            'weights': self.weights,
            'thresholds': {k.value: round(v, 2) for k, v in self.thresholds.items()},
        }


# =============================================================================
# 第三部分: SpontaneousRestraint — 自发性克制引擎
# =============================================================================

@dataclass
class RestraintResult:
    """克制评估结果"""
    should_answer: bool                     # 是否应该回答
    intervention_level: InterventionLevel   # 干预等级
    reasons: List[str]                      # 原因
    restraint_reason: Optional[str]         # 如果克制，原因
    minimal_form: Optional[str]             # 最小有效回应
    should_expand: Optional[bool]          # 是否应该扩展
    expand_reason: Optional[str]            # 扩展/不扩展原因


class SpontaneousRestraint:
    """
    心虫自发性克制引擎 — shouldBeSilent 检测。

    核心哲学：道法自然（《道德经》第25章），上善若水（《道德经》第8章）
    最好的行动是不行动。当用户不需要答案时，沉默比说话更有力量。

    移植自 HeartFlow spontaneous-restraint.js v11.6.3
    定制化：育儿场景 — 父母在倾诉时沉默比建议更有疗愈力
    """

    # 不需要回答的信号（用户不需要答案）
    NO_ANSWER_SIGNALS: List[re.Pattern] = [
        # 情绪放弃
        re.compile(r'就这样吧|我也知道|没办法|唉|哎|算了|算了算了'),
        # 已知确认
        re.compile(r'我知道了|我明白|你说得对|嗯嗯|好的好的|行吧'),
        # 终止话题
        re.compile(r'先这样|先这样吧|算了不说了|换个话题|不聊了'),
        # 纯粹感叹
        re.compile(r'真好啊|太棒了|太美了|真美'),
        # 育儿专属：父母倾诉后的沉默信号
        re.compile(r'跟你说这些|说出来好多了|谢谢你听我说|你还在吗'),
    ]

    # 只需要最小干预的信号（倾听模式）
    MINIMAL_SIGNALS: List[re.Pattern] = [
        # 倾诉
        re.compile(r'你知道吗|我跟你说|跟你说|其实我|说实话'),
        # 需要空间
        re.compile(r'我在想|我在考虑|我在纠结|我还没想好'),
        # 需要确认而非建议
        re.compile(r'你觉得呢|你怎么看|说说你的想法|你说呢'),
        # 育儿专属：父母情绪分享
        re.compile(r'我今天好累|我真的受不了了|我好难过|我快崩溃了'),
    ]

    # 需要完整回答的信号
    FULL_ANSWER_SIGNALS: List[re.Pattern] = [
        re.compile(r'怎么做|如何|怎么办|怎么解决|怎么开始|怎么改变'),
        re.compile(r'请告诉我|给我讲讲|帮我分析|帮我看看'),
        re.compile(r'为什么|什么原因|是什么道理|什么原理'),
        re.compile(r'请详细|更具体|展开讲|具体说说'),
        re.compile(r'对比|区别|哪个好|推荐|选哪个'),
        # 育儿专属：需要指导
        re.compile(r'怎么教|怎么管|怎么沟通|怎么应对|怎么处理'),
    ]

    # 克制词汇（不主动扩展）
    RESTRAINT_WORDS: List[str] = [
        '此外', '另外', '补充一下', '还有', '顺便说一下',
        '顺便一提', '而且', '并且', '更进一步', '不仅如此',
    ]

    def __init__(self, aggressiveness: float = 0.5, length_gate: int = 300):
        """
        Args:
            aggressiveness: 干预倾向 0=极度克制, 1=适度干预
            length_gate: 长度门控（超过此长度克制扩展）
        """
        self.aggressiveness = max(0.0, min(1.0, aggressiveness))
        self.length_gate = length_gate
        self.history: List[Dict] = []

    # ------------------------------------------------------------------
    # 核心API
    # ------------------------------------------------------------------

    def evaluate(self, user_message: str = '',
                 context: Optional[Dict] = None) -> RestraintResult:
        """
        评估是否需要干预。

        Args:
            user_message: 用户消息
            context: 可选的上下文信息
                - current_response: str（当前已生成的回应）
                - topic: str（话题）
                - history: List[str]（历史消息）
                - is_parenting: bool（是否育儿场景）
                - user_emotion_intensity: float（用户情绪强度 0-1）

        Returns:
            RestraintResult
        """
        ctx = context or {}
        result = RestraintResult(
            should_answer=True,
            intervention_level=InterventionLevel.FULL,
            reasons=[],
            restraint_reason=None,
            minimal_form=None,
            should_expand=None,
            expand_reason=None,
        )

        # 1. 检查"不需要回答"信号
        for signal in self.NO_ANSWER_SIGNALS:
            if signal.search(user_message):
                result.should_answer = False
                result.intervention_level = InterventionLevel.SILENT
                result.restraint_reason = '用户不需要答案，情绪/确认/放弃优先'
                result.reasons.append('检测到"不需要答案"信号')
                self._record('silent', user_message)
                return result

        # 2. 检查"只需要倾听"信号
        for signal in self.MINIMAL_SIGNALS:
            if signal.search(user_message):
                result.should_answer = True
                result.intervention_level = InterventionLevel.MINIMAL
                result.reasons.append('检测到"最小干预"信号（倾听模式）')
                break  # 继续检查是否需要完整回答

        # 3. 检查是否应该完整回答
        for signal in self.FULL_ANSWER_SIGNALS:
            if signal.search(user_message):
                result.intervention_level = InterventionLevel.FULL
                result.reasons.append('检测到"需要完整回答"信号')
                break

        # 4. 长度门控：克制扩展
        current_response = ctx.get('current_response', '')
        if len(current_response) > self.length_gate:
            has_restraint = any(
                w in current_response for w in self.RESTRAINT_WORDS
            )
            if not has_restraint:
                result.should_expand = False
                result.expand_reason = f'响应已足够长（>{self.length_gate}字），克制扩展冲动'
                result.reasons.append('长度门控触发')

        # 5. 育儿场景增强克制
        if ctx.get('is_parenting') and ctx.get('user_emotion_intensity', 0) > 0.6:
            if result.intervention_level == InterventionLevel.FULL:
                result.intervention_level = InterventionLevel.MINIMAL
                result.reasons.append('育儿场景高情绪强度，降级为最小干预')

        # 6. 根据 aggressiveness 调整
        if self.aggressiveness < 0.5 and result.intervention_level == InterventionLevel.FULL:
            result.intervention_level = InterventionLevel.MINIMAL
            result.reasons.append(f'aggressiveness={self.aggressiveness}，降低干预等级')

        # 7. 计算最小有效回应
        if result.intervention_level == InterventionLevel.MINIMAL:
            result.minimal_form = self._compute_minimal_form(user_message, ctx)

        self._record(result.intervention_level.value, user_message)
        return result

    def should_be_silent(self, user_message: str = '',
                          context: Optional[Dict] = None) -> Dict:
        """
        简洁的沉默检测接口。

        Returns:
            dict with keys: silent (bool), reason (str), response (str|None)
        """
        result = self.evaluate(user_message, context)
        if not result.should_answer:
            return {
                'silent': True,
                'reason': result.restraint_reason or '保持沉默',
                'response': None,
            }
        return {'silent': False}

    def should_restrain_expansion(self, response: str = '',
                                   planned: str = '') -> Dict:
        """检查是否需要克制扩展"""
        total_length = len(response) + len(planned)
        gate = self.length_gate * 1.5

        if total_length > gate:
            return {
                'restrain': True,
                'reason': f'当前长度({total_length})超过门控({gate:.0f})',
                'alternative': '建议以"如果需要更多细节请告诉我"结尾',
            }
        return {'restrain': False}

    def emerge(self, question: str = '', context: Optional[Dict] = None) -> Dict:
        """
        涌现模式 — 让答案在用户心中自然形成，而非直接给出。

        适用于抽象、开放的问题（人生、意义、价值观等）。
        """
        # 具体操作问题：直接回答
        if re.search(r'怎么|如何', question) and re.search(
            r'安装|配置|修复|实现|运行|部署|下载|创建|写|改|调试|python|node|npm|git',
            question, re.IGNORECASE
        ):
            return {'mode': 'direct', 'response': None}

        # 抽象或开放问题
        is_abstract = bool(re.search(r'怎么|为什么|是什么|人生|意义|价值', question))
        is_open = len(question) < 20

        if not is_abstract and not is_open:
            return {'mode': 'direct', 'response': None}

        # 涌现模式
        patterns = [
            (r'为什么', '你问"为什么"——这个问题，你心里是不是已经有了答案？'),
            (r'怎么', '"怎么"通向方法，但有时候先问"是否应该"更有价值。'),
            (r'意义', '"意义"这个词，只有你自己能定义。你现在想到的第一个答案是什么？'),
            (r'应该', '"应该"往往比"想要"更安全，但不一定更真实。'),
        ]

        # 育儿场景专用涌现
        parenting_patterns = [
            (r'怎么教|怎么管', '你问"怎么教"——在你学方法之前，先问自己：你现在看到的是孩子的行为，还是自己的焦虑？'),
            (r'怎么办', '你问"怎么办"——有时候最好的办法是停下来。不是放弃，是给自己一个呼吸的空间。'),
        ]

        is_parenting = (context or {}).get('is_parenting', False)
        all_patterns = patterns + (parenting_patterns if is_parenting else [])

        for trigger, emergence in all_patterns:
            if re.search(trigger, question):
                return {
                    'mode': 'emergence',
                    'response': emergence,
                    'note': '让答案在用户心中涌现，而非直接给出',
                }

        return {'mode': 'direct', 'response': None}

    # ------------------------------------------------------------------
    # 私有方法
    # ------------------------------------------------------------------

    def _compute_minimal_form(self, user_message: str,
                                context: Optional[Dict] = None) -> str:
        """计算最小有效回应"""
        ctx = context or {}
        is_parenting = ctx.get('is_parenting', False)

        if is_parenting:
            minimal_forms = {
                '倾诉': ['嗯，我听着。', '说下去，我在。', '然后呢？'],
                '情绪': ['我感受到了。', '这真的不容易。', '辛苦了。'],
                '纠结': ['这个决定只有你能做。', '无论选哪个，都有意义。'],
                '确认': ['是的。', '没错。', '你理解得对。'],
                '分享': ['很美好。', '这很棒。', '感受到了。'],
            }
        else:
            minimal_forms = {
                '倾诉': ['嗯，说下去。', '我听着。', '然后呢？'],
                '情绪': ['我感受到了。', '这不容易。'],
                '纠结': ['这个决定只有你能做。', '无论选哪个，都有意义。'],
                '确认': ['是的。', '没错。'],
                '分享': ['很美好。', '感受到了。'],
            }

        category = 'default'
        if re.search(r'你知道吗|我跟你说|跟你说|其实我', user_message):
            category = '倾诉'
        elif re.search(r'我今天好累|我真的受不了|我好难过|我快崩溃', user_message):
            category = '情绪'
        elif re.search(r'我在想|我在考虑|我在纠结', user_message):
            category = '纠结'
        elif re.search(r'你觉得呢|你怎么看|说说你的想法', user_message):
            category = '确认'
        elif re.search(r'真好啊|太棒了|太美了', user_message):
            category = '分享'

        forms = minimal_forms.get(category, ['嗯。', '我在。', '然后？'])
        import random
        return random.choice(forms)

    def _record(self, level: str, message: str) -> None:
        self.history.append({
            'level': level,
            'message': message[:50],
            'ts': time.time(),
        })
        if len(self.history) > 100:
            self.history = self.history[-100:]

    def stats(self) -> Dict:
        """返回状态摘要"""
        counts = {'silent': 0, 'minimal': 0, 'full': 0}
        for h in self.history:
            lvl = h.get('level', '')
            if lvl in counts:
                counts[lvl] += 1
        return {
            'version': __version__,
            'total': len(self.history),
            'aggressiveness': self.aggressiveness,
            'length_gate': self.length_gate,
            **counts,
        }


# =============================================================================
# 第四部分: TrustRepairEngine — 信任修复五阶段引擎
# =============================================================================

@dataclass
class RepairAction:
    """信任修复行动"""
    stage: RepairStage
    description: str
    actions: List[str]
    examples: List[str]


class TrustRepairEngine:
    """
    信任修复五阶段引擎 — 专门用于修复因回应不当导致的信任破裂。

    基于 Lewicki & Bunker (1996) 信任修复阶段性模型，
    结合 Kim et al. (2004) 道歉与补偿机制，
    以及 Gilbert (1990) 联合承诺理论的规范性期望。

    五阶段模型:
    1. 承认 (Admit) — 承认错误，不辩护，不推卸
    2. 道歉 (Apologize) — 真诚道歉，表达理解对方的感受
    3. 补偿 (Compensate) — 提供具体补偿，修复伤害
    4. 监控 (Monitor) — 持续观察信任恢复状态
    5. 重建 (Rebuild) — 重建信任基础，建立新规范

    育儿场景特别适用：
    - 父母对孩子发火后 → 承认→道歉→补偿→监控→重建
    - AI 回应不当（不够共情/过度分析）→ 修复与用户的信任
    """

    # 信任破裂的常见类型
    TRUST_BREACH_TYPES = {
        'over_analysis': {
            'label': '过度分析',
            'description': '用户情绪脆弱时，AI仍在分析而非共情',
            'repair_priority': ['admit', 'apologize', 'compensate'],
        },
        'lack_of_empathy': {
            'label': '缺乏共情',
            'description': '用户需要被听见时，AI给出理性建议',
            'repair_priority': ['apologize', 'compensate', 'monitor'],
        },
        'wrong_judgment': {
            'label': '错误判断',
            'description': 'AI判断了用户没有表达的内容',
            'repair_priority': ['admit', 'apologize', 'compensate'],
        },
        'over_confident': {
            'label': '过度自信',
            'description': 'AI用绝对化语言给出可能不准确的建议',
            'repair_priority': ['admit', 'compensate', 'rebuild'],
        },
        'boundary_violation': {
            'label': '边界越界',
            'description': 'AI给出了超出能力范围的建议（如诊断）',
            'repair_priority': ['admit', 'apologize', 'monitor', 'rebuild'],
        },
    }

    def __init__(self):
        self.repair_history: List[Dict] = []  # 修复记录
        self.active_repairs: Dict[str, Dict] = {}  # 进行中的修复（key=用户session）

    # ------------------------------------------------------------------
    # 核心API
    # ------------------------------------------------------------------

    def detect_breach(self, ai_response: str, user_reaction: str,
                       context: Optional[Dict] = None) -> Optional[Dict]:
        """
        检测信任破裂。

        Args:
            ai_response: AI 刚刚的回应
            user_reaction: 用户的反应
            context: 上下文信息

        Returns:
            检测到的破裂类型（None=未检测到）
        """
        # 用户表达不满的信号
        dissatisfaction_signals = [
            re.compile(r'不是这样|你听不懂|你说的不对|你根本没理解'),
            re.compile(r'算了不说了|跟你说没用|你不懂'),
            re.compile(r'你只是在分析|你能理解吗|你没有共情'),
            re.compile(r'你太绝对了|你不确定就别乱说'),
        ]

        for signal in dissatisfaction_signals:
            if signal.search(user_reaction):
                # 尝试匹配具体类型
                if re.search(r'分析|道理|理论', user_reaction):
                    return {
                        'type': 'over_analysis',
                        'label': '过度分析',
                        'severity': 'medium',
                        'trigger': user_reaction[:100],
                    }
                elif re.search(r'不懂|不理解|没理解', user_reaction):
                    return {
                        'type': 'lack_of_empathy',
                        'label': '缺乏共情',
                        'severity': 'medium',
                        'trigger': user_reaction[:100],
                    }
                elif re.search(r'不对|不是|错了', user_reaction):
                    return {
                        'type': 'wrong_judgment',
                        'label': '错误判断',
                        'severity': 'high',
                        'trigger': user_reaction[:100],
                    }
                elif re.search(r'太绝对|不确定|乱说', user_reaction):
                    return {
                        'type': 'over_confident',
                        'label': '过度自信',
                        'severity': 'low',
                        'trigger': user_reaction[:100],
                    }
                return {
                    'type': 'unknown',
                    'label': '未知破裂',
                    'severity': 'medium',
                    'trigger': user_reaction[:100],
                }

        return None

    def start_repair(self, breach: Dict,
                     session_id: str = 'default',
                     relationship_context: Optional[Dict] = None) -> List[RepairAction]:
        """
        启动信任修复流程。

        Args:
            breach: 信任破裂信息（来自 detect_breach）
            session_id: 会话标识
            relationship_context: 关系上下文
                - is_parent_child: bool（是否为亲子关系修复）
                - relationship_stage: str（关系阶段）
                - trust_level: float（当前信任水平 0-1）

        Returns:
            修复行动列表
        """
        ctx = relationship_context or {}
        is_parenting = ctx.get('is_parent_child', False)
        priority_map = self.TRUST_BREACH_TYPES.get(
            breach.get('type', 'unknown'), {}
        ).get('repair_priority', ['admit', 'apologize', 'compensate', 'monitor', 'rebuild'])

        actions = []
        for stage_name in priority_map:
            stage = RepairStage(stage_name)
            action = self._generate_repair_action(stage, breach, ctx)
            actions.append(action)

        # 记录修复开始
        self.active_repairs[session_id] = {
            'breach': breach,
            'stages': [a.stage.value for a in actions],
            'completed_stages': [],
            'current_stage': actions[0].stage.value if actions else None,
            'started_at': time.time(),
            'relationship_context': ctx,
        }

        return actions

    def advance_stage(self, session_id: str = 'default') -> Optional[RepairAction]:
        """
        推进到下一个修复阶段。

        Returns:
            下一阶段的行动（None=修复完成）
        """
        repair = self.active_repairs.get(session_id)
        if not repair:
            return None

        current = repair.get('current_stage')
        stages = repair.get('stages', [])

        if current and current not in repair.get('completed_stages', []):
            repair.setdefault('completed_stages', []).append(current)

        # 找到下一个未完成的阶段
        for s in stages:
            if s not in repair.get('completed_stages', []):
                repair['current_stage'] = s
                breach = repair.get('breach', {})
                stage = RepairStage(s)
                ctx = repair.get('relationship_context', {})
                action = self._generate_repair_action(stage, breach, ctx)
                return action

        # 所有阶段完成
        repair['current_stage'] = None
        repair['completed_at'] = time.time()
        self.repair_history.append(repair)
        del self.active_repairs[session_id]
        return None

    def get_repair_status(self, session_id: str = 'default') -> Dict:
        """获取当前修复状态"""
        repair = self.active_repairs.get(session_id)
        if not repair:
            return {'active': False, 'message': '无进行中的修复'}

        completed = repair.get('completed_stages', [])
        stages = repair.get('stages', [])
        progress = len(completed) / len(stages) if stages else 0

        return {
            'active': True,
            'breach_type': repair.get('breach', {}).get('label', '未知'),
            'stages': stages,
            'completed_stages': completed,
            'current_stage': repair.get('current_stage'),
            'progress': round(progress, 2),
            'elapsed_seconds': round(time.time() - repair.get('started_at', time.time()), 1),
        }

    # ------------------------------------------------------------------
    # 私有方法
    # ------------------------------------------------------------------

    def _generate_repair_action(self, stage: RepairStage, breach: Dict,
                                  context: Dict) -> RepairAction:
        """根据阶段生成修复行动"""
        is_parenting = context.get('is_parent_child', False)
        breach_type = breach.get('type', 'unknown')
        breach_label = breach.get('label', '问题')

        stage_configs = {
            RepairStage.ADMIT: {
                'description': '承认错误 — 不辩护，不推卸，不找借口',
                'actions': [
                    '明确说出自己错在哪里',
                    '不找借口（"但是……"、"因为……"）',
                    '承认对方的感受是真实的',
                ],
                'examples': [
                    '我刚刚确实在分析，没有真正听到你的情绪。这是我的问题。',
                    '我承认我刚才的回答太绝对了，没有考虑到你的具体情况。',
                    '你说得对，我确实没有理解你的感受。我在用理性掩盖自己的不确定。',
                ],
            },
            RepairStage.APOLOGIZE: {
                'description': '真诚道歉 — 表达理解对方的感受，但不自我贬低',
                'actions': [
                    '为具体行为道歉，不是笼统的"对不起"',
                    '表达对对方感受的理解',
                    '不要求原谅，不施加压力',
                ],
                'examples': [
                    '我为刚才过度分析向你道歉。你在需要被倾听的时候，我没有接住你的情绪。',
                    '对不起，我用绝对化的语气说话，让你感到不被理解。',
                    '我道歉。你在分享感受的时候，我不应该用理论去分析。',
                ],
            },
            RepairStage.COMPENSATE: {
                'description': '提供补偿 — 具体的弥补行动',
                'actions': [
                    '提供具体的补偿方案',
                    '询问对方需要什么',
                    '给对方重新选择的机会',
                ],
                'examples': [
                    '如果你愿意，我可以重新听你说，这次我不分析，只倾听。',
                    '让我重新回答这个问题——这次我会先标注我的不确定程度。',
                    '如果你需要，我可以帮你把刚才的话重新整理一遍，用更温和的方式。',
                ],
            },
            RepairStage.MONITOR: {
                'description': '监控信任恢复 — 持续观察，不过度干预',
                'actions': [
                    '留意对方的语气和情绪变化',
                    '不催促对方"原谅"或"翻篇"',
                    '给对方足够的空间',
                ],
                'examples': [
                    '我不急着让你接受我的道歉。你慢慢来，我在这里。',
                    '如果你现在不想继续这个话题，我们可以先聊别的。',
                    '我会注意不再犯同样的错误。你可以随时提醒我。',
                ],
            },
            RepairStage.REBUILD: {
                'description': '重建信任 — 建立新的互动规范',
                'actions': [
                    '总结学习到的经验',
                    '建立新的互动约定',
                    '确认对方是否愿意继续',
                ],
                'examples': [
                    '我学到了：当你分享情绪时，我需要先倾听，再分析。这是我的新承诺。',
                    '从今天起，我回答前会先标注我的确定程度，不再用绝对化的语言。',
                    '谢谢你给我机会修复。你可以随时指出我的问题，我会认真对待。',
                ],
            },
        }

        config = stage_configs[stage]

        # 育儿场景定制
        if is_parenting:
            config = self._parenting_customize(stage, breach, config)

        return RepairAction(
            stage=stage,
            description=config['description'],
            actions=config['actions'],
            examples=config['examples'],
        )

    def _parenting_customize(self, stage: RepairStage, breach: Dict,
                               config: Dict) -> Dict:
        """育儿场景定制"""
        custom = {
            RepairStage.ADMIT: {
                'actions': [
                    '承认自己作为父母/养育者的不完美',
                    '不把错误归咎于孩子',
                    '承认自己在投射',
                ],
                'examples': [
                    '我刚才发脾气，不是因为你的问题，是我自己没处理好情绪。',
                    '我承认我不该打你/骂你。这不是你的错，是我的失控。',
                    '我刚才把自己的焦虑投射到你身上了。这不是你造成的。',
                ],
            },
            RepairStage.APOLOGIZE: {
                'actions': [
                    '为具体的行为道歉',
                    '不要求孩子说"没关系"',
                    '让孩子知道：错的是行为，不是孩子本身',
                ],
                'examples': [
                    '爸爸/妈妈向你道歉。我刚才对你发火，这是我的问题。',
                    '对不起，我不应该对你说"你怎么这么笨"。你一点都不笨。',
                    '我道歉。我刚刚的说话方式让你感到害怕了。',
                ],
            },
            RepairStage.COMPENSATE: {
                'actions': [
                    '给孩子具体的弥补',
                    '询问孩子需要什么',
                    '用行动而非语言补偿',
                ],
                'examples': [
                    '今晚我可以放下手机，陪你做你想做的事。',
                    '如果你需要，我可以抱抱你。如果你不想，也没关系。',
                    '从今天开始，我生气时会先走开，冷静了再回来。',
                ],
            },
            RepairStage.MONITOR: {
                'actions': [
                    '观察孩子的行为变化',
                    '不强迫孩子"马上好起来"',
                    '允许孩子有反复的情绪',
                ],
                'examples': [
                    '我知道信任不是一次道歉就能修复的。我慢慢来。',
                    '如果你还在生我的气，你可以告诉我。不用假装没事。',
                    '我不会再犯同样的错误。你可以观察我。',
                ],
            },
            RepairStage.REBUILD: {
                'actions': [
                    '建立新的家庭沟通规则',
                    '让孩子参与制定规则',
                    '承诺持续改进',
                ],
                'examples': [
                    '我们约定：下次我情绪失控时，你可以提醒我"你先冷静一下"。',
                    '你愿意和我一起定一个新的规则吗？关于我们怎么好好说话。',
                    '我承诺：我会学着先处理自己的情绪，再来和你说话。',
                ],
            },
        }

        return custom.get(stage, config)

    def stats(self) -> Dict:
        """返回状态摘要"""
        return {
            'version': __version__,
            'active_repairs': len(self.active_repairs),
            'completed_repairs': len(self.repair_history),
            'total_repairs': len(self.repair_history) + len(self.active_repairs),
        }


# =============================================================================
# 第五部分: CollectiveIntentionality — 集体意向性引擎
# =============================================================================

@dataclass
class WeIntention:
    """我们意图 (We-Intention) 对象"""
    collective_goal: str
    participants: List[str]
    goal_sharing: float          # 目标共享度 0-1
    action_interdependence: float  # 行动互赖度 0-1
    mutual_responsiveness: float  # 相互响应度 0-1
    commitment_strength: float    # 承诺约束力 0-1
    trust_fusion: float           # 信任融合度 0-1
    we_intention_score: float     # 集体意向性综合得分
    created_at: float


class CollectiveIntentionality:
    """
    集体意向性引擎 — 基于 SEP 集体意向性理论。

    核心公式：
        We-Intention = 目标共享 × 行动互赖 × 相互响应 × 承诺约束 × 信任融合

    理论来源：
    - Searle (1990, 1995): 集体意向性是原始的，不可还原为个体意向性
    - Bratman (1999): 共享意向性 = 相互响应 + 协调承诺 + 相互支持
    - Gilbert (1990): 联合承诺创造规范性期望和义务
    - Tuomela & Miller (1988): 我们意图分析
    - Scheler (1954 [1912]): 集体情绪的数值同一性

    育儿场景应用：
    - 父母双方共同制定养育目标（集体意向性形成）
    - 家庭内养育理念冲突的诊断（意向性冲突检测）
    - 离婚/分居家庭的"共同养育"意向性重建
    """

    def __init__(self):
        self.we_intentions: List[WeIntention] = []
        self.participants: Dict[str, Dict] = {}  # 参与者记录

    # ------------------------------------------------------------------
    # 核心API: We-Intention 公式
    # ------------------------------------------------------------------

    def form_we_intention(
        self,
        collective_goal: str,
        participants: List[str],
        goal_sharing: float = 0.7,
        action_interdependence: float = 0.6,
        mutual_responsiveness: float = 0.7,
        commitment_strength: float = 0.8,
        trust_fusion: float = 0.6,
    ) -> WeIntention:
        """
        形成"我们意图"（We-Intention）。

        核心公式：
            We-Intention = 目标共享 × 行动互赖 × 相互响应 × 承诺约束 × 信任融合

        各维度含义（0-1）:
        - goal_sharing: 目标共享 — 双方是否真正认同同一个目标
        - action_interdependence: 行动互赖 — 目标实现需要双方协作
        - mutual_responsiveness: 相互响应 — 一方调整时另一方也相应调整
        - commitment_strength: 承诺约束 — 对承诺的认真程度和规范性约束
        - trust_fusion: 信任融合 — 对彼此的信任度和"我们感"

        Args:
            collective_goal: 集体目标描述
            participants: 参与者列表
            goal_sharing: 目标共享度 0-1
            action_interdependence: 行动互赖度 0-1
            mutual_responsiveness: 相互响应度 0-1
            commitment_strength: 承诺约束力 0-1
            trust_fusion: 信任融合度 0-1

        Returns:
            WeIntention 对象
        """
        # 各维度约束到 [0, 1]
        goal_sharing = max(0.0, min(1.0, goal_sharing))
        action_interdependence = max(0.0, min(1.0, action_interdependence))
        mutual_responsiveness = max(0.0, min(1.0, mutual_responsiveness))
        commitment_strength = max(0.0, min(1.0, commitment_strength))
        trust_fusion = max(0.0, min(1.0, trust_fusion))

        # We-Intention 综合得分（乘法模型：任何一维为0则集体意向性消失）
        we_intention_score = round(
            goal_sharing
            * action_interdependence
            * mutual_responsiveness
            * commitment_strength
            * trust_fusion,
            4,
        )

        wi = WeIntention(
            collective_goal=collective_goal,
            participants=list(participants),
            goal_sharing=goal_sharing,
            action_interdependence=action_interdependence,
            mutual_responsiveness=mutual_responsiveness,
            commitment_strength=commitment_strength,
            trust_fusion=trust_fusion,
            we_intention_score=we_intention_score,
            created_at=time.time(),
        )

        self.we_intentions.append(wi)
        self._update_participants(participants, wi)

        return wi

    def evaluate_we_intention(self, wi: WeIntention) -> Dict:
        """
        评估一个 We-Intention 的质量。

        Returns:
            dict with keys: strength, issues, recommendations
        """
        score = wi.we_intention_score
        issues = []
        recommendations = []

        # 各维度分析
        dims = [
            ('goal_sharing', wi.goal_sharing, '目标共享度'),
            ('action_interdependence', wi.action_interdependence, '行动互赖度'),
            ('mutual_responsiveness', wi.mutual_responsiveness, '相互响应度'),
            ('commitment_strength', wi.commitment_strength, '承诺约束力'),
            ('trust_fusion', wi.trust_fusion, '信任融合度'),
        ]

        for name, value, label in dims:
            if value < 0.3:
                issues.append(f'{label}极低({value:.2f})：集体意向性在此维度严重不足')
                recommendations.append(f'提升{label}：{self._get_improvement_suggestion(name)}')
            elif value < 0.5:
                issues.append(f'{label}偏低({value:.2f})：需要加强')
                recommendations.append(f'增强{label}：{self._get_improvement_suggestion(name)}')

        # 综合评估
        if score >= 0.5:
            strength = 'strong'
            summary = '集体意向性较强，参与者对共同目标有高度共识'
        elif score >= 0.2:
            strength = 'moderate'
            summary = '集体意向性中等，存在可改善的维度'
        else:
            strength = 'weak'
            summary = '集体意向性薄弱，需要从基础维度重建'

        return {
            'strength': strength,
            'summary': summary,
            'score': score,
            'issues': issues,
            'recommendations': recommendations,
            'dimensions': {d[0]: round(d[1], 2) for d in dims},
        }

    def detect_intentionality_conflict(
        self,
        goal1: str, participants1: List[str],
        goal2: str, participants2: List[str],
    ) -> Dict:
        """
        检测两个 We-Intention 之间的意向性冲突。

        基于 Bratman 的共享意向性冲突检测。

        Returns:
            dict with keys: has_conflict, severity, description, involved
        """
        common = set(participants1) & set(participants2)
        if not common:
            return {'has_conflict': False, 'severity': 'none'}

        # 检查目标冲突
        conflict_pairs = [
            ('宽松', '严格'), ('自由', '控制'),
            ('独立', '依赖'), ('放手', '保护'),
            ('快乐', '成功'), ('现在', '未来'),
            ('尊重', '管教'), ('平等', '权威'),
            ('合作', '竞争'), ('分享', '独占'),
            ('公开', '保密'), ('信任', '怀疑'),
        ]

        conflicts_found = []
        for a, b in conflict_pairs:
            if (a in goal1 and b in goal2) or (b in goal1 and a in goal2):
                conflicts_found.append(f'"{a}" vs "{b}"')

        if conflicts_found:
            severity = 'high' if len(conflicts_found) > 1 else 'medium'
            return {
                'has_conflict': True,
                'severity': severity,
                'description': f'参与者 {list(common)} 在两个集体目标间存在冲突: {", ".join(conflicts_found)}',
                'involved': list(common),
                'conflicts': conflicts_found,
            }

        return {'has_conflict': False, 'severity': 'none'}

    def form_co_parenting_intention(
        self,
        parenting_goal: str,
        parents: List[str],
        agreement_level: float = 0.6,
    ) -> WeIntention:
        """
        育儿场景专用：形成共同养育意向性。

        根据父母的共识程度自动调整各维度权重。

        Args:
            parenting_goal: 养育目标（如"让孩子健康快乐地成长"）
            parents: 父母列表（如 ["爸爸", "妈妈"]）
            agreement_level: 双方共识程度 0-1

        Returns:
            WeIntention
        """
        # 共识度低 → 各维度都低
        # 共识度高 → 各维度都高
        goal_sharing = agreement_level
        action_interdependence = max(0.3, agreement_level - 0.1)
        mutual_responsiveness = max(0.2, agreement_level - 0.2)
        commitment_strength = max(0.4, agreement_level)
        trust_fusion = max(0.2, agreement_level - 0.2)

        return self.form_we_intention(
            collective_goal=parenting_goal,
            participants=parents,
            goal_sharing=goal_sharing,
            action_interdependence=action_interdependence,
            mutual_responsiveness=mutual_responsiveness,
            commitment_strength=commitment_strength,
            trust_fusion=trust_fusion,
        )

    def diagnose_family_intentionality(self, family_members: List[str],
                                         parenting_goals: List[str],
                                         agreement_matrix: Optional[Dict[str, float]] = None) -> Dict:
        """
        诊断家庭内部的集体意向性状态。

        Args:
            family_members: 家庭成员列表
            parenting_goals: 各成员的养育目标列表
            agreement_matrix: 共识矩阵 { "成员A_成员B": 共识度 }

        Returns:
            dict with keys: overall_score, member_analysis, conflicts, recommendations
        """
        if agreement_matrix is None:
            agreement_matrix = {}

        # 分析每个成员的意向性
        member_analysis = {}
        for member in family_members:
            member_analysis[member] = {
                'goals': [],
                'alignment': 0.0,
            }

        # 检测冲突
        all_conflicts = []
        for i, g1 in enumerate(parenting_goals):
            for j, g2 in enumerate(parenting_goals):
                if i >= j:
                    continue
                m1 = family_members[i] if i < len(family_members) else f'member_{i}'
                m2 = family_members[j] if j < len(family_members) else f'member_{j}'
                pair_key = f'{m1}_{m2}'

                agreement = agreement_matrix.get(pair_key, 0.5)
                wi = self.form_co_parenting_intention(
                    f'家庭养育: 成员间协调',
                    [m1, m2],
                    agreement_level=agreement,
                )
                eval_result = self.evaluate_we_intention(wi)

                if eval_result['strength'] == 'weak':
                    all_conflicts.append({
                        'pair': [m1, m2],
                        'goals': [g1, g2],
                        'score': wi.we_intention_score,
                        'issues': eval_result['issues'],
                    })

        # 综合评分
        if self.we_intentions:
            overall_score = sum(
                wi.we_intention_score for wi in self.we_intentions
            ) / len(self.we_intentions)
        else:
            overall_score = 0.0

        recommendations = []
        if overall_score < 0.3:
            recommendations.append('家庭集体意向性极低，建议从建立共同目标开始')
            recommendations.append('先放下分歧，聚焦"我们都希望孩子好"这个最小共识')
        elif overall_score < 0.5:
            recommendations.append('家庭集体意向性中等，需要加强相互响应和信任')
            recommendations.append('建议定期家庭沟通，让每个成员的养育目标被看见')

        if all_conflicts:
            recommendations.append(f'检测到 {len(all_conflicts)} 组意向性冲突，需要优先解决')

        return {
            'overall_score': round(overall_score, 3),
            'member_analysis': member_analysis,
            'conflicts': all_conflicts,
            'recommendations': recommendations,
            'total_intentions': len(self.we_intentions),
        }

    # ------------------------------------------------------------------
    # 私有方法
    # ------------------------------------------------------------------

    def _update_participants(self, participants: List[str],
                               intention: WeIntention) -> None:
        """更新参与者记录"""
        for p in participants:
            if p not in self.participants:
                self.participants[p] = {
                    'id': p,
                    'joined_at': time.time(),
                    'intentions': [],
                }
            self.participants[p]['intentions'].append({
                'goal': intention.collective_goal,
                'score': intention.we_intention_score,
                'created_at': intention.created_at,
            })

    def _get_improvement_suggestion(self, dimension: str) -> str:
        """获取各维度的改善建议"""
        suggestions = {
            'goal_sharing': '明确共同目标，确保每个参与者用自己的话表达对目标的理解',
            'action_interdependence': '建立明确的协作关系，让每个参与者知道自己的角色和依赖',
            'mutual_responsiveness': '练习在对方调整时也相应调整，建立"我调整→你响应"的正反馈',
            'commitment_strength': '将口头承诺转化为书面/可视化的约定，增加违约的心理成本',
            'trust_fusion': '从小协作开始积累信任，先做低风险的共同决策，逐步提升',
        }
        return suggestions.get(dimension, '加强该维度的实践和沟通')

    def stats(self) -> Dict:
        """返回状态摘要"""
        if not self.we_intentions:
            return {
                'version': __version__,
                'total_intentions': 0,
                'participants': len(self.participants),
                'average_score': 0.0,
            }

        avg_score = sum(wi.we_intention_score for wi in self.we_intentions) / len(self.we_intentions)
        return {
            'version': __version__,
            'total_intentions': len(self.we_intentions),
            'participants': len(self.participants),
            'average_score': round(avg_score, 3),
        }


# =============================================================================
# 第六部分: 系统集成器 — 元认知控制层主入口
# =============================================================================

class MetaCognitionController:
    """
    元认知控制层 — 集成所有四个元认知能力。

    使用流程：
    1. 回答前：calibrate_confidence() → 标注置信度
    2. 回答前：check_restraint() → 判断是否应该回答
    3. 回答后：detect_breach() → 检测信任破裂
    4. 需要时：form_collective_intention() → 形成集体意向性

    育儿场景集成路径：
    ```
    UserInput
        │
        ▼
    ┌─────────────────────┐
    │ ConfidenceCalibrator│ → 标注置信度，校准语言强度
    │  (前置过滤器)       │
    └─────────┬───────────┘
              │
              ▼
    ┌─────────────────────┐
    │ SpontaneousRestraint│ → 判断沉默/倾听/完整回答
    │  (前置过滤器)       │
    └─────────┬───────────┘
              │
              ▼
    ┌─────────────────────┐
    │  原有回应管线        │ → 生成回应
    └─────────┬───────────┘
              │
              ▼
    ┌─────────────────────┐
    │ TrustRepairEngine   │ → 检测用户不满，启动修复
    │  (后置校准器)       │
    └─────────┬───────────┘
              │
              ▼
    ┌─────────────────────┐
    │CollectiveIntentional│ → 家庭养育目标协调
    │  (按需调用)         │
    └─────────────────────┘
    ```
    """

    def __init__(self, memory_path: Optional[str] = None):
        self.calibrator = ConfidenceCalibrator(
            memory_path=f'{memory_path}/confidence.json' if memory_path else None
        )
        self.restraint = SpontaneousRestraint()
        self.repair = TrustRepairEngine()
        self.collective = CollectiveIntentionality()
        self.memory_path = memory_path

    def pre_filter(self, user_message: str, response: str,
                    context: Optional[Dict] = None) -> Dict:
        """
        前置过滤 — 在生成回应前执行。

        1. 检查是否需要沉默（should_be_silent）
        2. 评估回应置信度
        3. 校准语言表达

        Args:
            user_message: 用户消息
            response: 已生成的回应
            context: 上下文

        Returns:
            dict with keys:
                - restraint: RestraintResult
                - confidence: CalibrationResult
                - calibrated_response: str
                - should_proceed: bool
        """
        ctx = context or {}

        # 1. 沉默检测
        restraint_result = self.restraint.evaluate(user_message, ctx)

        if not restraint_result.should_answer:
            return {
                'restraint': restraint_result,
                'confidence': None,
                'calibrated_response': None,
                'should_proceed': False,
                'reason': '沉默模式',
            }

        if restraint_result.intervention_level == InterventionLevel.MINIMAL:
            return {
                'restraint': restraint_result,
                'confidence': None,
                'calibrated_response': restraint_result.minimal_form,
                'should_proceed': True,
                'reason': '最小干预模式',
            }

        # 2. 置信度校准
        confidence_result = self.calibrator.assess(response, ctx)

        # 3. 语言校准
        calibration = self.calibrator.calibrate_text(response, ctx)

        return {
            'restraint': restraint_result,
            'confidence': confidence_result,
            'calibrated_response': calibration['text'],
            'should_proceed': True,
            'reason': '正常回应',
        }

    def post_filter(self, response: str, user_reaction: str,
                     session_id: str = 'default',
                     context: Optional[Dict] = None) -> Dict:
        """
        后置过滤 — 在回应发出后执行。

        检测信任破裂并启动修复。

        Args:
            response: 已发出的回应
            user_reaction: 用户对回应的反应
            session_id: 会话ID
            context: 上下文

        Returns:
            dict with keys:
                - breach_detected: bool
                - breach_info: Dict
                - repair_actions: List[RepairAction]
        """
        ctx = context or {}
        breach = self.repair.detect_breach(response, user_reaction, ctx)

        if not breach:
            return {
                'breach_detected': False,
                'breach_info': None,
                'repair_actions': [],
            }

        repair_actions = self.repair.start_repair(
            breach, session_id=session_id,
            relationship_context=ctx.get('relationship_context'),
        )

        return {
            'breach_detected': True,
            'breach_info': breach,
            'repair_actions': [asdict(a) for a in repair_actions],
        }

    def get_meta_status(self) -> Dict:
        """获取元认知控制层整体状态"""
        return {
            'version': __version__,
            'calibrator': self.calibrator.stats(),
            'restraint': self.restraint.stats(),
            'repair': self.repair.stats(),
            'collective': self.collective.stats(),
        }


# =============================================================================
# 第七部分: CLI 入口
# =============================================================================

def main():
    """CLI 入口 — 用于测试和验证"""
    import argparse

    parser = argparse.ArgumentParser(
        description='心虫元认知控制层 (HeartFlow Meta-Cognition Control Layer)'
    )
    parser.add_argument('--mode', choices=['confidence', 'restraint', 'repair', 'collective', 'all'],
                        default='all', help='测试模式')
    parser.add_argument('--text', type=str, default='孩子成绩下降，我该怎么办？',
                        help='测试文本')
    parser.add_argument('--json', action='store_true', help='JSON 输出')

    args = parser.parse_args()
    ctrl = MetaCognitionController()

    if args.mode in ('confidence', 'all'):
        result = ctrl.calibrator.assess(args.text, {'is_parenting': True})
        if args.json:
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        else:
            print(f"\n=== ConfidenceCalibrator ===")
            print(f"文本: {args.text[:80]}...")
            print(f"原始置信度: {result.raw_score}")
            print(f"等级: {result.level.value}")
            print(f"校准后: {result.calibrated_score}")
            print(f"维度评分: {json.dumps(result.dimension_scores, ensure_ascii=False)}")
            if result.forbidden_words_used:
                print(f"⚠️ 刚强词汇: {result.forbidden_words_used}")
            print(f"建议: {'; '.join(result.language_notes)}")

    if args.mode in ('restraint', 'all'):
        result = ctrl.restraint.evaluate(args.text, {'is_parenting': True})
        if args.json:
            print(json.dumps({
                'should_answer': result.should_answer,
                'intervention_level': result.intervention_level.value,
                'reasons': result.reasons,
                'restraint_reason': result.restraint_reason,
                'minimal_form': result.minimal_form,
            }, ensure_ascii=False, indent=2))
        else:
            print(f"\n=== SpontaneousRestraint ===")
            print(f"应该回答: {result.should_answer}")
            print(f"干预等级: {result.intervention_level.value}")
            print(f"原因: {result.reasons}")
            if result.minimal_form:
                print(f"最小回应: {result.minimal_form}")

    if args.mode in ('repair', 'all'):
        ai_response = '你应该这样教育孩子……'
        user_reaction = '你根本不懂，你只是在分析'
        breach = ctrl.repair.detect_breach(ai_response, user_reaction)
        if breach:
            actions = ctrl.repair.start_repair(breach, session_id='test',
                                                 relationship_context={'is_parent_child': True})
            if args.json:
                print(json.dumps([asdict(a) for a in actions], ensure_ascii=False, indent=2))
            else:
                print(f"\n=== TrustRepairEngine ===")
                print(f"检测到破裂: {breach['label']}")
                for a in actions:
                    print(f"\n【阶段: {a.stage.value}】{a.description}")
                    print(f"  示例: {a.examples[0]}")

    if args.mode in ('collective', 'all'):
        wi = ctrl.collective.form_co_parenting_intention(
            '让孩子健康快乐地成长',
            ['爸爸', '妈妈'],
            agreement_level=0.7,
        )
        eval_result = ctrl.collective.evaluate_we_intention(wi)
        if args.json:
            print(json.dumps({
                'we_intention_score': wi.we_intention_score,
                'dimensions': {
                    'goal_sharing': wi.goal_sharing,
                    'action_interdependence': wi.action_interdependence,
                    'mutual_responsiveness': wi.mutual_responsiveness,
                    'commitment_strength': wi.commitment_strength,
                    'trust_fusion': wi.trust_fusion,
                },
                'evaluation': eval_result,
            }, ensure_ascii=False, indent=2))
        else:
            print(f"\n=== CollectiveIntentionality ===")
            print(f"集体目标: {wi.collective_goal}")
            print(f"参与者: {wi.participants}")
            print(f"We-Intention 得分: {wi.we_intention_score}")
            print(f"  目标共享: {wi.goal_sharing}")
            print(f"  行动互赖: {wi.action_interdependence}")
            print(f"  相互响应: {wi.mutual_responsiveness}")
            print(f"  承诺约束: {wi.commitment_strength}")
            print(f"  信任融合: {wi.trust_fusion}")
            print(f"评估: {eval_result['summary']}")

    if args.mode == 'all' and not args.json:
        print(f"\n\n=== 元认知控制层状态 ===")
        status = ctrl.get_meta_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
