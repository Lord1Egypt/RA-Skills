#!/usr/bin/env python3
"""
心虫元提示引擎 (HeartFlow MetaPrompt Engine) v1.0.0

升级版元提示模块 — 整合心虫三大核心认知模型：
1) MetaCognition 元认知层 — 先理解"这件事是关于什么的"
2) CounterfactualReasoning 反事实推理 — "如果这样做会怎样"
3) CooperativeArbitration 多源证据加权裁决 — 多证据源协同判定

并在其基础上构建 6 步元提示流程：
  元认知 → 反事实 → 结构化 → 优化 → 推理链 → 自检

理论来源:
- Flavell (1979) 元认知理论 — 对自己认知过程的认识与调控
- 《道德经》第40章"反者道之动" — 反向思考的力量
- Gou et al. (2024) CRITIC — 外部验证批判
- Argyris Double-loop learning — 双环学习
- Cooperative AI: Foundations and Open Problems (arXiv:2402.00386)
- HeartFlow MetaCognition Monitor v4.0 / CounterfactualEngine v11.6.1 / CooperativeArbitration v11.7.2
- fu-mu-gong-ke 原元提示层（4步：结构化→优化→推理链→自检）

设计目标: 替代 fu-mu-gong-ke 原有4步元提示流程（SKILL.md 第807行），
升级为6步认知增强版，为每次育儿对话提供元认知-反事实-多源裁决的深度推理前处理。

作者: HeartFlow 团队 / fu-mu-gong-ke 集成
"""

import json
import re
import math
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum


# =============================================================================
# 第一部分: MetaCognition 元认知层
# 基于 Flavell (1979) + HeartFlow MetaCognition Monitor v4.0
# 来源: improving/src/core/cognition/meta-cognition.ts
# =============================================================================

class CognitiveState(Enum):
    """认知状态 — 心虫思考时的8种可能状态"""
    FOCUSED = 'focused'        # 专注，目标清晰
    EXPLORING = 'exploring'    # 探索，信息搜集
    CONFUSED = 'confused'      # 困惑，下一步不明确
    STUCK = 'stuck'            # 卡住，重复失败
    UNCERTAIN = 'uncertain'    # 不确定，信心低
    CONVERGING = 'converging'  # 收敛，缩小方案
    REFLECTING = 'reflecting'  # 反思，思考思考本身
    PAUSED = 'paused'          # 暂停，等待

    def cn_label(self) -> str:
        return {
            'focused': '专注', 'exploring': '探索', 'confused': '困惑',
            'stuck': '卡住', 'uncertain': '不确定', 'converging': '收敛',
            'reflecting': '反思', 'paused': '暂停',
        }[self.value]


class ThinkingStrategy(Enum):
    """思维策略 — 8种可选的思考路径"""
    ANALYTICAL = 'analytical'     # 逐步逻辑分析
    INTUITIVE = 'intuitive'       # 模式直觉判断
    SYSTEMATIC = 'systematic'     # 全面系统探索
    DIVERGENT = 'divergent'       # 发散创意脑暴
    CONVERGENT = 'convergent'     # 收敛聚焦方案
    REFLECTIVE = 'reflective'     # 反思元认知
    STRATEGIC = 'strategic'       # 长期战略规划
    COMPASSIONATE = 'compassionate'  # 慈悲共情视角（育儿专用）

    def cn_label(self) -> str:
        return {
            'analytical': '分析', 'intuitive': '直觉', 'systematic': '系统',
            'divergent': '发散', 'convergent': '收敛', 'reflective': '反思',
            'strategic': '战略', 'compassionate': '慈悲',
        }[self.value]


# 有效状态转移表（来自 meta-cognition.ts）
VALID_TRANSITIONS: Dict[str, List[str]] = {
    'focused': ['exploring', 'converging', 'reflecting', 'stuck', 'uncertain'],
    'exploring': ['focused', 'confused', 'uncertain', 'paused'],
    'confused': ['exploring', 'uncertain', 'reflecting', 'stuck'],
    'stuck': ['reflecting', 'paused', 'exploring'],
    'uncertain': ['exploring', 'reflecting', 'focused', 'paused'],
    'converging': ['focused', 'reflecting', 'stuck'],
    'reflecting': ['focused', 'exploring', 'uncertain', 'paused'],
    'paused': ['focused', 'exploring', 'uncertain'],
}

# 中文关键词 → 认知状态映射（育儿对话增强版）
STATE_KEYWORDS_CN: Dict[str, List[str]] = {
    'focused': ['专注', '集中', '正在', '继续', '推进', '这个问题是', '核心是'],
    'exploring': ['探索', '尝试', '考虑', '看看', '可能', '也许', '或者'],
    'confused': ['困惑', '不清楚', '不知道', '模糊', '搞不懂', '怎么回事'],
    'stuck': ['卡住', '停滞', '无法', '困难', '走不下去', '没办法'],
    'uncertain': ['不确定', '不太确定', '可能吧', '也许吧', '说不准'],
    'converging': ['确定', '结论', '选择', '方案', '应该是', '那就是'],
    'reflecting': ['反思', '思考', '回顾', '分析', '元认知', '自己'],
    'paused': ['等待', '暂停', '稍后', '先这样', '等等'],
}


@dataclass
class MetaCognitionResult:
    """元认知分析结果"""
    detected_state: str                          # 检测到的认知状态
    state_confidence: float                      # 状态置信度 [0,1]
    detected_strategy: str                       # 推荐的思维策略
    strategy_confidence: float                   # 策略置信度 [0,1]
    thinking_depth: int                          # 思考深度 (0-10)
    self_awareness_score: float                  # 自我觉察评分 [0,1]
    recommendations: List[str]                   # 建议
    patterns_detected: List[Dict[str, Any]]      # 检测到的模式
    question_category: str                       # 问题类别
    user_emotion_estimate: Dict[str, float]      # 用户情绪估计

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MetaCognitionEngine:
    """
    元认知引擎 — 先理解"这件事是关于什么的"

    核心功能:
    1. 检测当前认知状态（focused/exploring/confused/stuck/...）
    2. 推荐最优思维策略
    3. 追踪思考深度和模式
    4. 检测认知循环/死胡同

    育儿场景特殊增强:
    - 增加 COMPASSIONATE 慈悲策略
    - 中文关键词优先
    - 问题类别自动分类（情绪/行为/危机/知识）
    """

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        opts = options or {}
        self.max_depth = opts.get('max_depth', 10)
        self.default_strategy = opts.get('default_strategy', 'compassionate')
        self.trace: List[Dict[str, Any]] = []
        self.current_state = CognitiveState.EXPLORING
        self.current_strategy = ThinkingStrategy.COMPASSIONATE
        self.current_depth = 0
        self.current_confidence = 0.5

    def analyze(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> MetaCognitionResult:
        """
        对用户输入进行元认知分析

        输入: 用户的原始消息
        输出: 认知状态 + 策略建议 + 模式检测
        """
        ctx = context or {}

        # 1. 检测认知状态
        state_detected, state_conf = self._detect_state(user_input)

        # 2. 检测思维策略
        strategy_detected, strategy_conf = self._detect_strategy(user_input)

        # 3. 估计思考深度
        depth = self._estimate_depth(user_input)

        # 4. 自我觉察评分
        awareness = self._calc_self_awareness(user_input, state_detected)

        # 5. 模式检测
        patterns = self._detect_patterns()

        # 6. 问题类别分类
        category = self._classify_question(user_input)

        # 7. 用户情绪估计
        emotion = self._estimate_user_emotion(user_input)

        # 8. 生成建议
        recommendations = self._generate_recommendations(
            state_detected, strategy_detected, category, emotion
        )

        # 记录追踪
        self._push_trace(state_detected, strategy_detected, depth, recommendations)

        return MetaCognitionResult(
            detected_state=state_detected.value,
            state_confidence=state_conf,
            detected_strategy=strategy_detected.value,
            strategy_confidence=strategy_conf,
            thinking_depth=depth,
            self_awareness_score=awareness,
            recommendations=recommendations,
            patterns_detected=patterns,
            question_category=category,
            user_emotion_estimate=emotion,
        )

    def _detect_state(self, text: str) -> Tuple[CognitiveState, float]:
        """检测用户当前认知状态"""
        scores: Dict[str, int] = {s.value: 0 for s in CognitiveState}

        for state_name, keywords in STATE_KEYWORDS_CN.items():
            for kw in keywords:
                if kw in text:
                    scores[state_name] += 1

        # 额外：检测育儿场景特殊信号
        if any(w in text for w in ['崩溃', '撑不住', '受不了', '想哭']):
            scores['stuck'] += 2
        if any(w in text for w in ['怎么办', '帮帮我', '救救我', '救命']):
            scores['confused'] += 2
        if any(w in text for w in ['谢谢', '懂了', '知道了', '明白了']):
            scores['converging'] += 2

        max_state = max(scores, key=scores.get)
        total = sum(scores.values())
        confidence = min(0.95, 0.3 + (scores[max_state] / max(1, total)) * 0.7) if total > 0 else 0.4

        return CognitiveState(max_state), confidence

    def _detect_strategy(self, text: str) -> Tuple[ThinkingStrategy, float]:
        """检测最优思维策略"""
        strategy_keywords = {
            ThinkingStrategy.ANALYTICAL: ['分析', '分解', '步骤', '逻辑', '原因', '为什么'],
            ThinkingStrategy.INTUITIVE: ['感觉', '直觉', '大概', '觉得', '好像'],
            ThinkingStrategy.SYSTEMATIC: ['系统', '全面', '完整', '所有', '各方面'],
            ThinkingStrategy.DIVERGENT: ['创意', '发散', '多种', '可能', '选项', '不同'],
            ThinkingStrategy.CONVERGENT: ['收敛', '聚焦', '筛选', '决定', '选择'],
            ThinkingStrategy.REFLECTIVE: ['反思', '思考', '觉察', '看见', '自己'],
            ThinkingStrategy.STRATEGIC: ['长期', '规划', '目标', '未来', '方向'],
            ThinkingStrategy.COMPASSIONATE: ['孩子', '心疼', '理解', '共情', '感受', '爱', '原谅', '接纳'],
        }

        scores: Dict[str, int] = {s.value: 0 for s in ThinkingStrategy}
        for strategy, keywords in strategy_keywords.items():
            for kw in keywords:
                if kw in text:
                    scores[strategy.value] += 1

        # 育儿对话默认偏慈悲策略
        scores[ThinkingStrategy.COMPASSIONATE.value] += 0.5

        max_strategy = max(scores, key=scores.get)
        total = sum(scores.values())
        confidence = min(0.9, 0.3 + (scores[max_strategy] / max(1, total)) * 0.6) if total > 0 else 0.3

        return ThinkingStrategy(max_strategy), confidence

    def _estimate_depth(self, text: str) -> int:
        """估计思考深度"""
        depth_signals = {
            1: ['就是', '反正', '直接'],
            2: ['因为', '所以', '但是', '不过'],
            3: ['但是另一方面', '然而', '尽管如此'],
            4: ['其实', '本质上', '根本上'],
            5: ['元', '反思', '模式', '觉察', '防御'],
        }
        depth = 1
        for d, signals in depth_signals.items():
            if any(s in text for s in signals):
                depth = max(depth, d)
        return min(depth, self.max_depth)

    def _calc_self_awareness(self, text: str, state: CognitiveState) -> float:
        """计算自我觉察分数"""
        awareness_keywords = [
            '我发现', '我注意到', '我意识到', '我看见', '我觉察到',
            '我是不是', '我可能', '也许我', '我自己的',
        ]
        hits = sum(1 for kw in awareness_keywords if kw in text)
        base = 0.3
        return min(1.0, base + hits * 0.15)

    def _detect_patterns(self) -> List[Dict[str, Any]]:
        """检测认知模式（循环/死胡同/突破）"""
        patterns = []
        if len(self.trace) >= 4:
            last_four = self.trace[-4:]
            states = [t['state'] for t in last_four]
            # 检测震荡 A->B->A->B
            if states[0] == states[2] and states[1] == states[3] and states[0] != states[1]:
                patterns.append({
                    'type': 'loop',
                    'description': f'在 {states[0]} 和 {states[1]} 之间震荡',
                    'severity': 'medium',
                    'recommendation': '尝试换一种思考方式或暂停一下',
                })
        return patterns

    def _classify_question(self, text: str) -> str:
        """将用户问题分类"""
        categories = {
            'crisis': ['自杀', '想死', '自伤', '割', '遗书', '解脱', '活着没意思',
                       '伤害自己', '不想活'],
            'emotion_support': ['崩溃', '难受', '难过', '委屈', '愤怒', '害怕',
                                '焦虑', '抑郁', '睡不着', '压力'],
            'behavior_guidance': ['不听话', '打人', '发脾气', '哭闹', '撒谎',
                                  '偷东西', '不写作业', '沉迷'],
            'relationship': ['沟通', '说话', '不理', '锁门', '叛逆', '对抗',
                             '吵架', '冷战'],
            'knowledge': ['为什么', '是什么', '怎么办', '方法', '技巧', '策略'],
        }
        for cat, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return cat
        return 'general_parenting'

    def _estimate_user_emotion(self, text: str) -> Dict[str, float]:
        """估计用户情绪强度"""
        emotion_signals = {
            'anger': ['愤怒', '生气', '火大', '烦死了', '受不了', '忍无可忍'],
            'anxiety': ['焦虑', '担心', '怕', '害怕', '不安', '紧张', '慌'],
            'sadness': ['难过', '伤心', '想哭', '委屈', '失落', '悲伤'],
            'guilt': ['愧疚', '内疚', '自责', '后悔', '对不起', '是我的错'],
            'helplessness': ['没办法', '无能为力', '不知道', '帮帮我', '救救我'],
        }
        result = {}
        for emotion, signals in emotion_signals.items():
            hits = sum(1 for s in signals if s in text)
            result[emotion] = min(1.0, hits * 0.25)
        return result

    def _generate_recommendations(
        self,
        state: CognitiveState,
        strategy: ThinkingStrategy,
        category: str,
        emotion: Dict[str, float],
    ) -> List[str]:
        """生成元认知建议"""
        recs = []

        # 基于状态的建议
        state_recs = {
            CognitiveState.STUCK: [
                '先停下来，别急着找答案',
                '试试换个角度：从孩子的感受出发，而不是从问题出发',
                '深呼吸，给自己一个暂停的空间',
            ],
            CognitiveState.CONFUSED: [
                '先把问题拆开：发生了什么 vs 我感受到什么',
                '不急着解决，先理解',
                '可以描述一下具体发生了什么吗？',
            ],
            CognitiveState.UNCERTAIN: [
                '不确定是正常的——养育没有标准答案',
                '关注孩子的感受，而不是对错',
                '试试说出你的担心，看看它是不是真的',
            ],
            CognitiveState.REFLECTING: [
                '好的，你在觉察自己——这是改变的第一步',
                '看到了什么？是你的模式，还是孩子的需要？',
            ],
        }
        recs.extend(state_recs.get(state, [
            '先听，再想，再说',
            '把"怎么办"换成"他/她现在需要什么"',
        ]))

        # 基于策略的建议
        if strategy == ThinkingStrategy.COMPASSIONATE:
            recs.insert(0, '先共情，再分析——孩子需要的不是一个答案，是被看见')

        # 基于情绪的建议
        if emotion.get('anger', 0) > 0.5:
            recs.insert(0, '你现在很愤怒——先处理自己的情绪，再处理孩子的问题')
        if emotion.get('guilt', 0) > 0.5:
            recs.insert(0, '内疚是信号，不是终点——它告诉你你在乎')

        return recs[:5]

    def _push_trace(self, state: CognitiveState, strategy: ThinkingStrategy,
                    depth: int, recs: List[str]) -> None:
        """记录思考追踪"""
        self.trace.append({
            'state': state.value,
            'strategy': strategy.value,
            'depth': depth,
            'recommendations': recs,
            'timestamp': __import__('datetime').datetime.now().isoformat(),
        })
        if len(self.trace) > 200:
            self.trace.pop(0)

    def get_trace_summary(self) -> str:
        """获取思考追踪摘要"""
        if not self.trace:
            return '尚无元认知追踪记录。'
        recent = self.trace[-5:]
        states = ' → '.join(t['state'] for t in recent)
        avg_conf = sum(
            (1 if t['state'] in ['focused', 'converging'] else 0.5)
            for t in recent
        ) / max(1, len(recent))
        return f'近期状态链: {states}。平均置信度: {avg_conf:.0%}。'


# =============================================================================
# 第二部分: CounterfactualReasoning 反事实推理
# 来源: HeartFlow CounterfactualEngine v11.6.1
# 哲学根基: "反者道之动" — 《道德经》第40章
# =============================================================================

@dataclass
class OpposingView:
    """反方观点"""
    type: str                # tone / logic / attribution / contrary
    challenge: str           # 挑战描述
    detail: Any              # 详细分析
    severity: str            # low / medium / high

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PremiseChallenge:
    """前提挑战"""
    signal: str              # 触发词
    question: str            # 挑战问题
    type: str                # premise_signal / certainty_challenge / causal_challenge
    severity: str            # low / medium / high

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CounterfactualResult:
    """反事实推理结果"""
    opposing_views: List[Dict[str, Any]]
    premise_challenges: List[Dict[str, Any]]
    origin_recall: Dict[str, Any]
    confidence_adjustment: Dict[str, Any]
    refinement_suggestions: List[str]
    verdict: str             # likely_correct / needs_adjustment / needs_revision
    needs_revision: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CounterfactualReasoningEngine:
    """
    反事实推理引擎 — "如果这样做会怎样"

    核心思想:
    - 反者道之动: 真正的智慧来自对自身的质疑
    - 在给出答案之前，先质疑自己的前提
    - 生成"反方"，不是为了辩论，而是为了让答案更接近真实

    功能:
    1. 反方生成: 给定答案/思路，生成挑战性反方观点
    2. 前提攻击: 质疑回答所依赖的隐含前提
    3. 归因还原: 将回答还原到用户原始问题，验证是否走偏
    4. 置信度调整: 基于检测到的问题调整信心
    5. "如果相反"场景: 生成对立情景测试

    育儿场景特殊增强:
    - 增加"慈悲反方"——不伤害式质疑
    - 识别"应该""必须""一定"等确定性语言
    """

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        opts = options or {}
        self.mode = opts.get('mode', 'balanced')  # balanced / aggressive / gentle
        self.max_views = opts.get('max_opposing_views', 3)
        self.max_challenges = opts.get('max_premise_challenges', 3)

        # 隐含前提触发词（来自心虫 counterfactual-engine.js）
        self.premise_signals = [
            '当然', '显然', '必然', '一定', '肯定',
            '应该', '必须', '毫无疑问',
            '这就说明', '这意味着', '这证明了',
            '很明显', '不言而喻',
        ]
        # 过度确定信号
        self.certainty_signals = [
            '绝对是', '一定是', '必然是', '毫无疑问',
            '没有争议', '无可置疑', '不容置疑',
            '唯一正确', '正确答案', '就是',
        ]
        # 育儿场景特殊信号
        self.parenting_certainty = [
            '孩子就是', '小孩都', '这年龄都', '所有孩子',
            '就应该', '必须这样', '不这样不行',
        ]

    def analyze(self, answer_preview: str,
                user_query: str = '',
                reasoning: str = '') -> CounterfactualResult:
        """
        对即将给出的回答进行反事实分析

        输入: 回答预览 + 用户原始问题 + 推理过程
        输出: 反方观点 + 前提挑战 + 置信度调整
        """
        if not answer_preview or len(answer_preview.strip()) < 10:
            return CounterfactualResult(
                opposing_views=[],
                premise_challenges=[],
                origin_recall={'relevant': False, 'reason': '回答过短，跳过反方分析'},
                confidence_adjustment={'shift': 0, 'reason': '无分析'},
                refinement_suggestions=[],
                verdict='likely_correct',
                needs_revision=False,
            )

        # 1. 生成反方观点
        views = self._generate_opposing_views(answer_preview, user_query)

        # 2. 前提挑战
        challenges = self._challenge_premises(answer_preview)

        # 3. 归因还原
        origin = self._recall_origin(answer_preview, user_query, reasoning)

        # 4. 置信度调整
        conf = self._compute_confidence_shift(answer_preview)

        # 5. 修正建议
        suggestions = self._suggest_refinements(views, challenges, origin)

        # 6. 最终判定
        verdict = self._compute_verdict(answer_preview, views, challenges)

        return CounterfactualResult(
            opposing_views=[v.to_dict() for v in views],
            premise_challenges=[c.to_dict() for c in challenges],
            origin_recall=origin,
            confidence_adjustment=conf,
            refinement_suggestions=suggestions,
            verdict=verdict,
            needs_revision=(verdict == 'needs_revision'),
        )

    def _generate_opposing_views(self, answer: str,
                                  user_query: str = '') -> List[OpposingView]:
        """生成反方观点"""
        views: List[OpposingView] = []

        # 1. 语气检测
        tone_issues = self._detect_tone(answer)
        if tone_issues and self.mode != 'gentle':
            views.append(OpposingView(
                type='tone',
                challenge='语气过于确定，可能忽略了其他可能性',
                detail=tone_issues,
                severity='medium',
            ))

        # 2. 逻辑间隙检测
        logic_issues = self._detect_logic_gaps(answer)
        if logic_issues:
            views.append(OpposingView(
                type='logic',
                challenge='逻辑链存在可质疑的环节',
                detail=logic_issues,
                severity='medium',
            ))

        # 3. 归因偏移检测
        if user_query:
            gap = self._check_attribution_gap(answer, user_query)
            if gap:
                views.append(OpposingView(
                    type='attribution',
                    challenge='回答可能偏离了用户原始问题',
                    detail=gap,
                    severity='high',
                ))

        # 4. "如果相反"反方
        contrary = self._generate_contrary(answer)
        if contrary:
            views.append(OpposingView(
                type='contrary',
                challenge='如果情况相反，结果会不同吗？',
                detail=contrary,
                severity='low',
            ))

        # 5. 育儿特殊反方：慈悲质疑
        parenting_issues = self._detect_parenting_certainty(answer)
        if parenting_issues:
            views.append(OpposingView(
                type='parenting',
                challenge='这个判断是否把所有孩子都概括了？',
                detail=parenting_issues,
                severity='medium',
            ))

        return views[:self.max_views]

    def _detect_tone(self, text: str) -> List[str]:
        """检测语气问题"""
        return [s for s in self.certainty_signals if s in text]

    def _detect_logic_gaps(self, text: str) -> List[str]:
        """检测逻辑间隙"""
        gaps = []
        # 无证据因果
        if re.search(r'因为.*所以', text) and '证据' not in text and '研究' not in text:
            gaps.append('因果陈述缺少证据支撑')
        # 全称量词
        if re.search(r'所有|全部|每个|一切|都这样', text):
            gaps.append('使用全称量词，可能存在反例')
        # 无来源引用
        if re.search(r'研究表明|研究显示|专家说|权威', text):
            gaps.append('引用缺乏具体来源')
        return gaps

    def _check_attribution_gap(self, answer: str, query: str) -> Optional[Dict[str, Any]]:
        """检查回答与问题的关键词重叠度"""
        query_words = [w for w in re.split(r'\s+', query) if len(w) > 1]
        answer_words = [w for w in re.split(r'\s+', answer) if len(w) > 1]
        if not query_words or not answer_words:
            return None
        overlap = sum(1 for qw in query_words
                      for aw in answer_words
                      if qw in aw or aw in qw)
        coverage = overlap / max(1, len(query_words))
        if coverage < 0.3:
            return {
                'query_coverage': f'{coverage:.0%}',
                'note': '回答与问题的关键词重叠度较低，可能存在漂移',
            }
        return None

    def _generate_contrary(self, text: str) -> Optional[str]:
        """生成对立情景"""
        negations = {
            '是': '不是', '有': '没有', '能': '不能',
            '会': '不会', '应该': '不应该', '好': '不好',
            '对': '不对', '要': '不要', '可以': '不可以',
        }
        for word, neg in negations.items():
            if word in text and len(text) < 500:
                return f'如果情况相反（将"{word}"替换为"{neg}"），这个结论还成立吗？'
        return None

    def _detect_parenting_certainty(self, text: str) -> List[str]:
        """检测育儿特殊确定性信号"""
        return [s for s in self.parenting_certainty if s in text]

    def _challenge_premises(self, text: str) -> List[PremiseChallenge]:
        """挑战隐含前提"""
        challenges: List[PremiseChallenge] = []

        # 前提信号检测
        for signal in self.premise_signals:
            if signal in text:
                challenges.append(PremiseChallenge(
                    signal=signal,
                    question=self._premise_question(signal),
                    type='premise_signal',
                    severity='medium',
                ))

        # 确定性信号检测
        for signal in self.certainty_signals:
            if signal in text:
                challenges.append(PremiseChallenge(
                    signal=signal,
                    question='这个"必然"成立的条件是什么？有没有反例？',
                    type='certainty_challenge',
                    severity='high',
                ))

        # 因果关系检测
        causal = re.findall(r'因为(.*?)所以(.*?)[。.]', text)
        for phrase in causal:
            challenges.append(PremiseChallenge(
                signal=f'因为{phrase[0]}所以{phrase[1]}',
                question='这个因果关系是充分条件还是必要条件？',
                type='causal_challenge',
                severity='medium',
            ))

        return challenges[:self.max_challenges]

    def _premise_question(self, signal: str) -> str:
        """生成前提挑战问题"""
        questions = {
            '当然': '这个"当然"成立的条件是什么？',
            '显然': '这个"显然"对所有人都是明显的吗？',
            '必然': '这个"必然"有没有反例？',
            '一定': '这个"一定"的例外是什么？',
            '应该': '"应该"和"是"之间的差距是什么？',
            '必须': '这个"必须"的约束条件是什么？',
            '毫无疑问': '真的没有疑问吗？',
            '这就说明': '说明的原因充分吗？有没有其他解释？',
            '这意味着': '这个含义是唯一的吗？',
        }
        return questions.get(signal, '这个判断的前提是什么？')

    def _recall_origin(self, answer: str, user_query: str,
                        reasoning: str) -> Dict[str, Any]:
        """归因还原 — 检查回答是否回到了对话起源"""
        if not user_query:
            return {'relevant': False, 'reason': '无原始问题，无法归因还原'}

        source = reasoning or answer
        query_words = [w for w in re.split(r'\s+', user_query) if len(w) > 2]
        answer_words = [w for w in re.split(r'\s+', source) if len(w) > 2]

        if not query_words:
            return {'relevant': False, 'reason': '原始问题过短'}

        coverage = sum(1 for k in answer_words
                       for q in query_words
                       if k in q or q in k)
        coverage_rate = coverage / len(query_words)

        return {
            'relevant': True,
            'query_preview': user_query[:60],
            'coverage_rate': round(coverage_rate, 2),
            'drift_detected': coverage_rate < 0.4,
            'note': ('回答可能已偏离原始问题，建议回归'
                     if coverage_rate < 0.4
                     else '回答较好地回应当了原始问题'),
        }

    def _compute_confidence_shift(self, text: str) -> Dict[str, Any]:
        """计算置信度调整"""
        certain_hits = sum(1 for s in self.certainty_signals if s in text)
        premise_hits = sum(1 for s in self.premise_signals if s in text)
        logic_gaps = len(self._detect_logic_gaps(text))

        shift = -(certain_hits * 0.15) - (logic_gaps * 0.1) + (premise_hits * 0.05)

        return {
            'shift': round(shift, 2),
            'adjusted_level': 'high' if shift > -0.1 else ('medium' if shift > -0.3 else 'low'),
            'reasons': '检测到确定性信号' if certain_hits > 0 else '无明显确定性偏差',
        }

    def _suggest_refinements(self, views: List[OpposingView],
                              challenges: List[PremiseChallenge],
                              origin: Dict[str, Any]) -> List[str]:
        """生成修正建议"""
        suggestions = []

        if any(v.type == 'tone' for v in views):
            suggestions.append('将语气从"确定"调整为"可能"或"也许"')
        if any(c.type == 'premise_signal' for c in challenges):
            suggestions.append('在前提假设前加上"在...情况下"')
        if any(c.type == 'certainty_challenge' for c in challenges):
            suggestions.append('将"必然"替换为"很可能"或"在大多数情况下"')
        if any(v.type == 'parenting' for v in views):
            suggestions.append('避免用"所有孩子都这样"来概括')
        if origin.get('drift_detected'):
            suggestions.append(f'建议回到原始问题')

        return suggestions

    def _compute_verdict(self, text: str, views: List[OpposingView],
                          challenges: List[PremiseChallenge]) -> str:
        """计算最终判定"""
        issue_count = (len(self._detect_tone(text)) +
                       len(self._detect_logic_gaps(text)) +
                       len(self._detect_parenting_certainty(text)))
        logic_gap_count = len(self._detect_logic_gaps(text))

        if issue_count >= 3 or logic_gap_count >= 2:
            return 'needs_revision'
        elif issue_count >= 1 or logic_gap_count >= 1:
            return 'needs_adjustment'
        return 'likely_correct'


# =============================================================================
# 第三部分: CooperativeArbitration 多源证据加权裁决
# 来源: HeartFlow CooperativeArbitration v11.7.2
# 哲学根基: "夫唯不争，故天下莫能与之争" — 《道德经》第22章
# =============================================================================

class ArbitrationMode(Enum):
    """仲裁模式"""
    CONFLICT = 'conflict'          # 冲突 — 多源证据严重不一致
    COMPETITION = 'competition'    # 竞争 — 有分歧但可调和
    NEUTRAL = 'neutral'           # 中立 — 无明显冲突
    COOPERATION = 'cooperation'   # 合作 — 多源证据趋向一致
    SYMBIOSIS = 'symbiosis'       # 共生 — 多源证据高度一致


class ResolutionStrategy(Enum):
    """解决策略"""
    SUPERORDINATE = 'superordinate'   # 超目标 — 找到更高层共识
    INTEGRATION = 'integration'       # 整合 — 融合多方观点
    ACCOMMODATION = 'accommodation'   # 顺应 — 主动让步
    COMPROMISE = 'compromise'         # 妥协 — 各让一步
    SYNTHESIS = 'synthesis'           # 综合 — 超越原有框架


@dataclass
class EvidenceSource:
    """证据源"""
    name: str                    # 证据源名称
    content: str                 # 证据内容
    weight: float                # 权重 [0, 1]
    confidence: float            # 置信度 [0, 1]
    source_type: str             # knowledge / emotion / logic / intuition / parenting

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ArbitrationResult:
    """仲裁结果"""
    mode: str                    # 仲裁模式
    alignment: float             # 对齐度 [0, 1]
    tension: float               # 紧张度 [0, 1]
    trajectory: str              # 轨迹 ascending / stable / deteriorating
    weighted_consensus: str      # 加权共识文本
    winning_source: str          # 胜出证据源
    evidence_breakdown: List[Dict[str, Any]]  # 各证据源分析
    narrative: str               # 叙事描述
    strategies_applied: List[str]  # 使用的策略

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CooperativeArbitrationEngine:
    """
    合作仲裁引擎 — 多源证据加权裁决

    核心思想:
    - "不争而善胜" — 不竞争反而能赢
    - 当多个证据源/视角有分歧时，不是要"谁对"，
      而是要找到让所有视角都得到尊重的共识

    功能:
    1. 多源证据对齐度计算
    2. 加权共识生成
    3. 冲突检测与升级
    4. 自动策略选择

    育儿场景特殊增强:
    - 证据源可包含: 育儿知识库 / 用户情绪 / 逻辑分析 / 慈悲直觉
    """

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        opts = options or {}
        self.empathy_depth = opts.get('empathy_depth', 0.7)
        self.compromise_ratio = opts.get('compromise_ratio', 0.4)
        self.win_threshold = opts.get('win_threshold', 0.5)

        self.state = {
            'mode': ArbitrationMode.NEUTRAL,
            'tension': 0.0,
            'alignment': 0.0,
            'trajectory': 'stable',
        }
        self.history: List[Dict[str, Any]] = []

    def arbitrate(self, sources: List[EvidenceSource],
                  context: Optional[Dict[str, Any]] = None) -> ArbitrationResult:
        """
        对多个证据源进行加权仲裁

        输入: 多个证据源（知识库/情绪/逻辑/直觉/育儿经验）
        输出: 加权共识 + 对齐度 + 冲突报告
        """
        if not sources:
            return ArbitrationResult(
                mode=ArbitrationMode.NEUTRAL.value,
                alignment=1.0,
                tension=0.0,
                trajectory='stable',
                weighted_consensus='无证据源，跳过仲裁',
                winning_source='none',
                evidence_breakdown=[],
                narrative='无数据。',
                strategies_applied=['none'],
            )

        ctx = context or {}

        # 1. 计算各证据源对齐度
        alignment, tensions = self._calculate_alignment(sources)

        # 2. 检测仲裁模式
        mode = self._detect_mode(alignment, tensions)

        # 3. 生成加权共识
        consensus, winner = self._generate_weighted_consensus(sources)

        # 4. 选择解决策略
        strategies = self._select_strategies(mode, alignment, tensions)

        # 5. 生成叙事
        narrative = self._generate_narrative(mode, alignment, tensions)

        # 6. 计算轨迹
        trajectory = self._calculate_trajectory(mode, tensions)

        # 更新状态
        self.state = {
            'mode': mode,
            'tension': tensions,
            'alignment': alignment,
            'trajectory': trajectory,
        }

        # 记录
        self.history.append({
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'mode': mode.value,
            'alignment': alignment,
            'tension': tensions,
            'sources': [s.name for s in sources],
        })

        # 证据分解
        breakdown = []
        for s in sources:
            breakdown.append({
                'name': s.name,
                'type': s.source_type,
                'weight': s.weight,
                'confidence': s.confidence,
                'weighted_score': s.weight * s.confidence,
                'alignment_with_winner': self._calc_pairwise_alignment(
                    s.content, consensus
                ),
            })

        return ArbitrationResult(
            mode=mode.value,
            alignment=round(alignment, 3),
            tension=round(tensions, 3),
            trajectory=trajectory,
            weighted_consensus=consensus,
            winning_source=winner,
            evidence_breakdown=breakdown,
            narrative=narrative,
            strategies_applied=[s.value for s in strategies],
        )

    def _calculate_alignment(self, sources: List[EvidenceSource]) -> Tuple[float, float]:
        """计算所有证据源之间的平均对齐度和紧张度"""
        if len(sources) < 2:
            return 1.0, 0.0

        pairs = 0
        total_alignment = 0.0
        total_tension = 0.0

        for i in range(len(sources)):
            for j in range(i + 1, len(sources)):
                pairs += 1
                align = self._calc_pairwise_alignment(
                    sources[i].content, sources[j].content
                )
                total_alignment += align
                # 紧张度 = 1 - 对齐度（加权）
                total_tension += (1 - align) * (sources[i].weight + sources[j].weight) / 2

        avg_alignment = total_alignment / max(1, pairs)
        avg_tension = total_tension / max(1, pairs)

        # 检测矛盾信号
        contradictions = self._detect_contradictions(sources)
        penalty = contradictions * 0.15

        return max(0, min(1, avg_alignment - penalty)), min(1, avg_tension + penalty)

    def _calc_pairwise_alignment(self, text1: str, text2: str) -> float:
        """计算两段文本的语义对齐度（基于关键词Jaccard相似度）"""
        if not text1 or not text2:
            return 0.5

        words1 = set(re.findall(r'[\w\u4e00-\u9fff]{2,}', text1))
        words2 = set(re.findall(r'[\w\u4e00-\u9fff]{2,}', text2))

        if not words1 or not words2:
            return 0.5

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / max(1, len(union))

    def _detect_contradictions(self, sources: List[EvidenceSource]) -> int:
        """检测证据源之间的矛盾"""
        contradiction_pairs = [
            ('对', '错'), ('是', '否'), ('好', '坏'),
            ('应该', '不应该'), ('要', '不要'), ('同意', '不同意'),
            ('可以', '不行'), ('做', '不做'),
            ('温柔', '严厉'), ('自由', '控制'),
            ('接纳', '纠正'), ('放手', '保护'),
        ]

        count = 0
        for i in range(len(sources)):
            for j in range(i + 1, len(sources)):
                for a, b in contradiction_pairs:
                    if (a in sources[i].content and b in sources[j].content) or \
                       (b in sources[i].content and a in sources[j].content):
                        count += 1
        return count

    def _detect_mode(self, alignment: float, tension: float) -> ArbitrationMode:
        """检测仲裁模式"""
        if alignment > 0.7 and tension < 0.3:
            return ArbitrationMode.SYMBIOSIS
        elif alignment > 0.5:
            return ArbitrationMode.COOPERATION
        elif alignment > 0.2:
            return ArbitrationMode.COMPETITION
        elif alignment < 0.1 or tension > 0.7:
            return ArbitrationMode.CONFLICT
        return ArbitrationMode.NEUTRAL

    def _generate_weighted_consensus(self,
                                      sources: List[EvidenceSource]) -> Tuple[str, str]:
        """生成加权共识"""
        if not sources:
            return '无证据源', 'none'

        # 按加权得分排序
        scored = [(s.name, s.weight * s.confidence, s.content) for s in sources]
        scored.sort(key=lambda x: x[1], reverse=True)

        winner_name = scored[0][0]
        winner_content = scored[0][2]

        # 如果有多个证据源，尝试整合
        if len(scored) > 1 and scored[0][1] - scored[1][1] < 0.2:
            # 得分接近，融合前两名
            top_two = scored[:2]
            common_words = set(re.findall(r'[\w\u4e00-\u9fff]{2,}', top_two[0][2]))
            for _, _, content in top_two[1:]:
                common_words &= set(re.findall(r'[\w\u4e00-\u9fff]{2,}', content))

            if common_words:
                common_sample = list(common_words)[:5]
                consensus = f'多源证据共识: 在 "{", ".join(common_sample)}" 上对齐'
            else:
                consensus = f'多源证据趋向: {winner_name} 权重最高'
        else:
            consensus = f'胜出证据源 "{winner_name}": {winner_content[:80]}...'

        return consensus, winner_name

    def _select_strategies(self, mode: ArbitrationMode, alignment: float,
                            tension: float) -> List[ResolutionStrategy]:
        """选择解决策略"""
        strategies = [ResolutionStrategy.SUPERORDINATE]  # 超目标总是首选

        if mode in (ArbitrationMode.SYMBIOSIS, ArbitrationMode.COOPERATION):
            strategies.append(ResolutionStrategy.INTEGRATION)
        elif mode == ArbitrationMode.CONFLICT and tension > 0.7:
            strategies.append(ResolutionStrategy.ACCOMMODATION)
            strategies.append(ResolutionStrategy.COMPROMISE)
        elif mode == ArbitrationMode.COMPETITION:
            strategies.append(ResolutionStrategy.INTEGRATION)
            strategies.append(ResolutionStrategy.SYNTHESIS)
        else:
            strategies.append(ResolutionStrategy.COMPROMISE)
            strategies.append(ResolutionStrategy.SYNTHESIS)

        return strategies

    def _calculate_trajectory(self, mode: ArbitrationMode,
                               tension: float) -> str:
        """计算轨迹"""
        if mode == ArbitrationMode.SYMBIOSIS:
            return 'ascending'
        elif mode == ArbitrationMode.CONFLICT and tension > 0.8:
            return 'escalating'
        elif mode == ArbitrationMode.COMPETITION and tension > 0.5:
            return 'deteriorating'
        elif mode == ArbitrationMode.COOPERATION:
            return 'stable'
        return 'neutral'

    def _generate_narrative(self, mode: ArbitrationMode,
                             alignment: float, tension: float) -> str:
        """生成状态叙事"""
        narratives = {
            ArbitrationMode.SYMBIOSIS: '多源证据达到了「共生」状态——各方自然协作，无需仲裁。',
            ArbitrationMode.COOPERATION: '多源证据处于「合作」状态——可以共赢。',
            ArbitrationMode.COMPETITION: '多源证据存在「竞争」——需要找到共同目标。',
            ArbitrationMode.CONFLICT: '多源证据出现「分歧」——仲裁介入，降低紧张。',
            ArbitrationMode.NEUTRAL: '多源证据处于「中立」状态——保持观察。',
        }

        narrative = narratives.get(mode, '')
        narrative += f' 对齐度: {alignment:.0%}，紧张度: {tension:.0%}。'
        narrative += ' "夫唯不争，故天下莫能与之争"——仲裁的目标是没有输家的共赢。'

        return narrative

    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'version': '1.0.0',
            'current_mode': self.state['mode'].value,
            'tension': self.state['tension'],
            'alignment': self.state['alignment'],
            'trajectory': self.state['trajectory'],
            'total_arbitrations': len(self.history),
        }


# =============================================================================
# 第四部分: 升级版元提示流程 — 6步认知增强管线
# 替代 fu-mu-gong-ke 原4步元提示流程 (结构化→优化→推理链→自检)
# 升级为6步: 元认知→反事实→结构化→优化→推理链→自检
# =============================================================================

@dataclass
class MetaPromptResult:
    """元提示流程完整结果"""
    # 第1步: 元认知分析
    metacognition: Dict[str, Any]

    # 第2步: 反事实推理
    counterfactual: Dict[str, Any]

    # 第3步: 问题结构化
    structured_question: Dict[str, Any]

    # 第4步: 提示词优化
    optimized_prompt: str

    # 第5步: 推理链设计
    reasoning_chain: List[str]

    # 第6步: 质量自检
    quality_check: Dict[str, Any]

    # 总体评估
    overall_confidence: float
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MetaPromptPipeline:
    """
    升级版元提示流程 — 6步认知增强管线

    在每次回答用户前，自动运行以下6步：

    第1步: 元认知层
        "这件事是关于什么的"
        - 检测用户认知状态
        - 推荐思维策略
        - 识别问题类别

    第2步: 反事实推理层
        "如果这样做会怎样"
        - 生成反方观点
        - 挑战隐含前提
        - 检测确定性偏差

    第3步: 问题结构化
        "拆解问题结构"
        - 核心问题是什么
        - 问题类型
        - 用户情绪状态
        - 合适回应模式

    第4步: 提示词优化
        "将模糊描述转为结构化的任务定义"
        - 明确目标
        - 约束条件
        - 输出格式
        - 质量标准

    第5步: 推理链设计
        "设计多步推理路径"
        - 共情先行
        - 原因分析
        - 多方案提供
        - 具体行动建议

    第6步: 质量自检
        "回答前最终检查"
        - 共情优先检查
        - 诊断性语言检查
        - 可操作性检查
        - 情绪适配检查
    """

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        opts = options or {}
        self.meta_engine = MetaCognitionEngine(opts.get('meta', {}))
        self.counter_engine = CounterfactualReasoningEngine(opts.get('counter', {}))
        self.arbitration_engine = CooperativeArbitrationEngine(opts.get('arbitration', {}))
        self.verbose = opts.get('verbose', False)

    def run(self, user_input: str,
            context: Optional[Dict[str, Any]] = None) -> MetaPromptResult:
        """
        执行完整6步元提示流程

        输入: 用户原始消息 + 可选上下文
        输出: 6步分析结果 + 优化后的提示词 + 推理链 + 自检报告
        """
        ctx = context or {}

        # =====================================================================
        # 第1步: 元认知分析
        # "这件事是关于什么的"
        # =====================================================================
        meta_result = self.meta_engine.analyze(user_input, ctx)

        if self.verbose:
            print(f'[元认知] 状态: {meta_result.detected_state}, '
                  f'策略: {meta_result.detected_strategy}, '
                  f'类别: {meta_result.question_category}')

        # =====================================================================
        # 第2步: 反事实推理
        # "如果这样做会怎样" — 在正式回答前，先质疑自己的回答前提
        # =====================================================================
        # 用元认知结果作为"回答预览"的占位
        answer_preview = f'用户问题是关于{meta_result.question_category}的育儿问题，' \
                         f'当前认知状态为{meta_result.detected_state}，' \
                         f'推荐策略为{meta_result.detected_strategy}。'

        counter_result = self.counter_engine.analyze(
            answer_preview=answer_preview,
            user_query=user_input,
            reasoning=meta_result.detected_strategy,
        )

        if self.verbose:
            print(f'[反事实] 判定: {counter_result.verdict}, '
                  f'反方观点数: {len(counter_result.opposing_views)}')

        # =====================================================================
        # 第3步: 问题结构化
        # "拆解问题结构"
        # =====================================================================
        structured = self._structure_question(user_input, meta_result, counter_result)

        if self.verbose:
            print(f'[结构化] 核心: {structured["core_question"][:50]}...')

        # =====================================================================
        # 第4步: 提示词优化
        # "将模糊描述转为结构化的任务定义"
        # =====================================================================
        optimized_prompt = self._optimize_prompt(user_input, meta_result,
                                                  counter_result, structured)

        if self.verbose:
            print(f'[优化] 提示词已生成 ({len(optimized_prompt)}字符)')

        # =====================================================================
        # 第5步: 推理链设计
        # "设计多步推理路径"
        # =====================================================================
        chain = self._design_reasoning_chain(meta_result, counter_result, structured)

        if self.verbose:
            print(f'[推理链] {len(chain)}步')

        # =====================================================================
        # 第6步: 质量自检
        # "回答前最终检查"
        # =====================================================================
        quality = self._quality_check(optimized_prompt, meta_result, counter_result)

        if self.verbose:
            print(f'[自检] 通过: {quality["passed"]}, '
                  f'问题数: {len(quality["issues"])}')

        # =====================================================================
        # 总体评估
        # =====================================================================
        warnings = self._collect_warnings(meta_result, counter_result, quality)

        # 置信度: 综合考虑元认知置信度 + 反事实判定 + 自检结果
        base_conf = meta_result.state_confidence
        if counter_result.verdict == 'needs_revision':
            base_conf *= 0.7
        elif counter_result.verdict == 'needs_adjustment':
            base_conf *= 0.85
        if not quality['passed']:
            base_conf *= 0.9

        return MetaPromptResult(
            metacognition=meta_result.to_dict(),
            counterfactual=counter_result.to_dict(),
            structured_question=structured,
            optimized_prompt=optimized_prompt,
            reasoning_chain=chain,
            quality_check=quality,
            overall_confidence=round(base_conf, 3),
            warnings=warnings,
        )

    def _structure_question(self, user_input: str,
                             meta: MetaCognitionResult,
                             counter: CounterfactualResult) -> Dict[str, Any]:
        """第3步: 问题结构化"""
        return {
            'core_question': self._extract_core(user_input),
            'question_type': meta.question_category,
            'user_emotion': meta.user_emotion_estimate,
            'cognitive_state': meta.detected_state,
            'recommended_strategy': meta.detected_strategy,
            'response_mode': self._select_response_mode(meta),
            'counterfactual_warnings': [
                v['challenge'] for v in counter.opposing_views
                if v['severity'] in ('medium', 'high')
            ],
            'needs_crisis_intervention': meta.question_category == 'crisis',
        }

    def _extract_core(self, text: str) -> str:
        """提取核心问题"""
        # 简单策略: 找"怎么办""为什么""是什么"附近的内容
        patterns = [
            r'(.*?(怎么办|怎么处理|怎么应对|怎么做).*?)[。？?!！]',
            r'(.*?(为什么|怎么[会能]).*?)[。？?!！]',
            r'(.*?(是什么|是什么意思|是什么情况).*?)[。？?!！]',
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                return m.group(1)[:100]
        return text[:100]

    def _select_response_mode(self, meta: MetaCognitionResult) -> str:
        """选择回应模式"""
        if meta.question_category == 'crisis':
            return 'crisis_intervention'
        dominant_emotion = max(meta.user_emotion_estimate,
                               key=meta.user_emotion_estimate.get,
                               default='')
        if meta.user_emotion_estimate.get(dominant_emotion, 0) > 0.5:
            return 'emotion_first'
        if meta.detected_state in ('confused', 'stuck'):
            return 'guidance'
        return 'balanced'

    def _optimize_prompt(self, user_input: str,
                          meta: MetaCognitionResult,
                          counter: CounterfactualResult,
                          structured: Dict[str, Any]) -> str:
        """第4步: 提示词优化 — 生成结构化任务定义"""
        lines = []
        lines.append(f'## 任务: 回应一个育儿相关问题')

        # 明确目标
        lines.append(f'\n### 目标')
        lines.append(f'为一位{meta.detected_state}状态的用户提供育儿支持。')
        lines.append(f'问题类别: {meta.question_category}')
        if meta.question_category == 'crisis':
            lines.append('⚠️ 优先确保安全，按危机干预流程处理')

        # 约束条件
        lines.append(f'\n### 约束')
        lines.append(f'- 使用 {meta.detected_strategy} 策略')
        lines.append(f'- 不诊断、不评判、不贴标签')
        lines.append(f'- 先共情再分析')

        # 反事实警告
        if counter.needs_revision:
            lines.append(f'- ⚠️ 反事实分析: 回答需修正 — {counter.verdict}')
        for v in counter.opposing_views[:2]:
            lines.append(f'- 反方视角: {v["challenge"]}')

        # 输出格式
        response_mode = structured['response_mode']
        if response_mode == 'emotion_first':
            lines.append(f'\n### 输出格式')
            lines.append('1. 先承接情绪(1-2句共情)')
            lines.append('2. 再分析问题')
            lines.append('3. 给具体行动建议')
        elif response_mode == 'crisis_intervention':
            lines.append(f'\n### 输出格式')
            lines.append('1. 危机转介(热线)')
            lines.append('2. 温和告知能力边界')
            lines.append('3. 禁止分析或建议')
        else:
            lines.append(f'\n### 输出格式')
            lines.append('1. 共情回应')
            lines.append('2. 问题分析')
            lines.append('3. 可选方案')
            lines.append('4. 具体行动建议')

        # 质量标准
        lines.append(f'\n### 质量要求')
        lines.append('- 包含至少1句共情')
        lines.append('- 建议可立即执行')
        lines.append('- 无诊断性语言')
        lines.append('- 适配用户当前情绪')

        # 用户原始输入
        lines.append(f'\n### 用户原始输入')
        lines.append(user_input)

        return '\n'.join(lines)

    def _design_reasoning_chain(self, meta: MetaCognitionResult,
                                 counter: CounterfactualResult,
                                 structured: Dict[str, Any]) -> List[str]:
        """第5步: 推理链设计"""
        chain = []

        # 1. 共情先行
        chain.append('共情先行: 先看到用户的感受，再处理问题')

        # 2. 基于元认知的定向
        if meta.detected_state in ('stuck', 'confused'):
            chain.append(f'定向: 用户处于{meta.detected_state}状态，'
                         f'先帮助稳定情绪再分析')
        elif meta.detected_state == 'reflecting':
            chain.append(f'定向: 用户正在自我觉察，'
                         f'深入而非打断')
        else:
            chain.append(f'定向: 用户状态为{meta.detected_state}，'
                         f'匹配{meta.detected_strategy}策略')

        # 3. 反事实考虑
        if counter.needs_revision:
            chain.append(f'反事实修正: 避免确定性语言，'
                         f'增加可能性表述')
        if any(v['type'] == 'attribution' for v in counter.opposing_views):
            chain.append('归因检查: 确保回答紧扣用户原始问题')

        # 4. 问题分析
        chain.append(f'分析: 从{meta.question_category}角度理解问题')

        # 5. 多方案提供
        chain.append('提供: 至少2个可选方案，标注适用条件')

        # 6. 具体行动
        chain.append('行动: 给1个可立即执行的步骤')

        # 7. 慈悲收尾
        chain.append('收尾: "你已经在做最重要的事——看见问题"')

        return chain

    def _quality_check(self, optimized_prompt: str,
                        meta: MetaCognitionResult,
                        counter: CounterfactualResult) -> Dict[str, Any]:
        """第6步: 质量自检"""
        issues = []

        # 检查共情
        empathy_keywords = ['理解', '看到', '感受到', '不容易', '辛苦', '难过']
        if not any(kw in optimized_prompt for kw in empathy_keywords):
            issues.append('缺少共情元素')

        # 检查诊断性语言
        diagnostic = ['你属于', '你是', '你有病', '你问题', '你有问题',
                       '你就是这样', '你总是', '你从来不']
        for d in diagnostic:
            if d in optimized_prompt:
                issues.append(f'包含诊断性语言: "{d}"')

        # 检查可操作性
        actionable = ['可以', '试试', '建议', '步骤', '第一步']
        if not any(kw in optimized_prompt for kw in actionable):
            issues.append('缺少可操作建议')

        # 检查情绪适配
        dominant_emotion = max(meta.user_emotion_estimate,
                               key=meta.user_emotion_estimate.get,
                               default='')
        if dominant_emotion and meta.user_emotion_estimate.get(dominant_emotion, 0) > 0.5:
            if dominant_emotion == 'anger' and '愤怒' not in optimized_prompt:
                issues.append('检测到用户愤怒情绪，需要先承接')
            if dominant_emotion == 'guilt' and '内疚' not in optimized_prompt:
                issues.append('检测到用户内疚情绪，需要先化解')

        # 反事实警告纳入
        if counter.needs_revision:
            issues.append(f'反事实分析建议修正: {counter.verdict}')

        return {
            'passed': len(issues) == 0,
            'issue_count': len(issues),
            'issues': issues,
            'checklist': {
                'has_empathy': any(kw in optimized_prompt for kw in empathy_keywords),
                'no_diagnostic_language': not any(d in optimized_prompt for d in diagnostic),
                'has_actionable': any(kw in optimized_prompt for kw in actionable),
                'emotion_adapted': len(issues) <= 1,
            },
        }

    def _collect_warnings(self, meta: MetaCognitionResult,
                           counter: CounterfactualResult,
                           quality: Dict[str, Any]) -> List[str]:
        """收集所有警告"""
        warnings = []

        if meta.question_category == 'crisis':
            warnings.append('⚠️ 危机信号: 按危机干预流程处理')

        if counter.needs_revision:
            warnings.append('⚠️ 反事实建议修正回答')

        if meta.user_emotion_estimate.get('anger', 0) > 0.7:
            warnings.append('⚠️ 用户愤怒度高，优先情绪降温')

        if meta.user_emotion_estimate.get('helplessness', 0) > 0.7:
            warnings.append('⚠️ 用户无助感强，需给具体可执行的步骤')

        if not quality['passed']:
            warnings.append(f'⚠️ 质量自检未通过: {quality["issue_count"]}个问题')

        return warnings


# =============================================================================
# 第五部分: 一站式 API — 开箱即用
# =============================================================================

def analyze_input(user_input: str,
                  context: Optional[Dict[str, Any]] = None,
                  options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    一键分析用户输入 — 运行完整6步元提示流程

    这是最常用的入口函数。

    用法:
        from heartflow_metaprompt_upgrade import analyze_input

        result = analyze_input("我的孩子最近总是发脾气，我不知道怎么办")
        print(result['optimized_prompt'])  # 优化后的提示词
        print(result['metacognition']['detected_state'])  # 检测到的认知状态
        print(result['counterfactual']['verdict'])  # 反事实判定
        print(result['quality_check']['passed'])  # 自检是否通过
        print(result['overall_confidence'])  # 总体置信度

    参数:
        user_input: 用户原始消息
        context: 可选上下文 (session_id, history, etc.)
        options: 引擎配置选项

    返回:
        完整的6步分析结果字典
    """
    pipeline = MetaPromptPipeline(options)
    result = pipeline.run(user_input, context or {})
    return result.to_dict()


def quick_check(user_input: str) -> Dict[str, Any]:
    """
    快速检查 — 仅运行元认知+反事实（前2步），适合轻量场景

    用法:
        from heartflow_metaprompt_upgrade import quick_check
        check = quick_check("我打了孩子很后悔")
        print(check['state'], check['verdict'])
    """
    meta = MetaCognitionEngine()
    counter = CounterfactualReasoningEngine()

    meta_result = meta.analyze(user_input)
    counter_result = counter.analyze(
        answer_preview=f'用户问题类别: {meta_result.question_category}',
        user_query=user_input,
    )

    return {
        'state': meta_result.detected_state,
        'strategy': meta_result.detected_strategy,
        'category': meta_result.question_category,
        'emotion': meta_result.user_emotion_estimate,
        'counterfactual_verdict': counter_result.verdict,
        'needs_revision': counter_result.needs_revision,
        'warnings': [
            v['challenge'] for v in counter_result.opposing_views
            if v['severity'] == 'high'
        ],
    }


def self_audit() -> Dict[str, Any]:
    """
    自审计 — 检查元提示引擎各模块状态

    用法:
        from heartflow_metaprompt_upgrade import self_audit
        print(self_audit())
    """
    meta = MetaCognitionEngine()
    counter = CounterfactualReasoningEngine()
    arb = CooperativeArbitrationEngine()

    return {
        'version': '1.0.0',
        'modules': {
            'metacognition': {
                'loaded': True,
                'states': [s.value for s in CognitiveState],
                'strategies': [s.value for s in ThinkingStrategy],
                'trace_size': len(meta.trace),
            },
            'counterfactual': {
                'loaded': True,
                'mode': counter.mode,
                'premise_signals': len(counter.premise_signals),
                'certainty_signals': len(counter.certainty_signals),
                'parenting_signals': len(counter.parenting_certainty),
            },
            'arbitration': {
                'loaded': True,
                'modes': [m.value for m in ArbitrationMode],
                'strategies': [s.value for s in ResolutionStrategy],
                'history_size': len(arb.history),
            },
        },
        'pipeline': {
            'steps': ['metacognition', 'counterfactual', 'structuring',
                       'optimization', 'reasoning_chain', 'quality_check'],
            'replaces': 'fu-mu-gong-ke 原4步元提示流程 (结构化→优化→推理链→自检)',
            'enhancements': [
                '新增元认知层 — 先理解"这件事是关于什么的"',
                '新增反事实推理 — "如果这样做会怎样"',
                '新增多源证据加权裁决 — 协同判定',
                '从4步升级为6步认知增强管线',
            ],
        },
    }


# =============================================================================
# CLI 入口
# =============================================================================

if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) > 1 and sys.argv[1] == '--audit':
        print(json.dumps(self_audit(), ensure_ascii=False, indent=2))
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        if len(sys.argv) > 2:
            result = quick_check(sys.argv[2])
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print('用法: python heartflow_metaprompt_upgrade.py --quick "用户输入"')
        sys.exit(0)

    # 默认: 完整6步分析
    if len(sys.argv) > 1:
        user_text = sys.argv[1]
    else:
        user_text = "我的孩子最近总是发脾气，我不知道怎么办"

    pipeline = MetaPromptPipeline({'verbose': True})
    result = pipeline.run(user_text)

    print('\n' + '=' * 60)
    print('心虫元提示引擎 — 6步分析结果')
    print('=' * 60)

    print(f'\n📊 总体置信度: {result.overall_confidence:.1%}')

    print(f'\n🔍 第1步: 元认知分析')
    print(f'   认知状态: {result.metacognition["detected_state"]}')
    print(f'   思维策略: {result.metacognition["detected_strategy"]}')
    print(f'   问题类别: {result.metacognition["question_category"]}')
    print(f'   情绪: {result.metacognition["user_emotion_estimate"]}')
    print(f'   建议: {result.metacognition["recommendations"]}')

    print(f'\n🔄 第2步: 反事实推理')
    print(f'   判定: {result.counterfactual["verdict"]}')
    print(f'   反方观点: {len(result.counterfactual["opposing_views"])}个')
    for v in result.counterfactual["opposing_views"]:
        print(f'     - [{v["severity"]}] {v["challenge"]}')
    print(f'   修正建议: {result.counterfactual["refinement_suggestions"]}')

    print(f'\n📋 第3步: 问题结构化')
    s = result.structured_question
    print(f'   核心问题: {s["core_question"]}')
    print(f'   回应模式: {s["response_mode"]}')
    print(f'   需要危机干预: {s["needs_crisis_intervention"]}')

    print(f'\n⚡ 第4步: 优化提示词')
    print(f'   ({len(result.optimized_prompt)}字符)')

    print(f'\n🧩 第5步: 推理链 ({len(result.reasoning_chain)}步)')
    for i, step in enumerate(result.reasoning_chain, 1):
        print(f'   {i}. {step}')

    print(f'\n✅ 第6步: 质量自检')
    q = result.quality_check
    print(f'   通过: {q["passed"]}')
    if q["issues"]:
        for issue in q["issues"]:
            print(f'   ⚠️ {issue}')
    else:
        print(f'   无问题')

    if result.warnings:
        print(f'\n⚠️ 警告')
        for w in result.warnings:
            print(f'   {w}')

    print('\n' + '=' * 60)
