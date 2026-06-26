"""
Parenting Psychology Reasoning Engine
育儿心理学推理引擎 - 6层决策管道

Architecture:
    User Input → CrisisDetector → UserIdentifier → EmotionAssessor
    → ScenarioMatcher → DefenseSignalDetector → DisplacementAnalyzer
    → ReasoningChainGenerator → ResponseGenerator → ExitDetector

基于育儿心理学理论（Adler, Dreikurs, Rogers, Bowlby）构建的结构化推理系统。

核心哲学（一切回答的根基）：
1. 没有评判的接纳 — 看到"你受苦了"，不是"你有问题"
2. 没有负罪感的许可 — 坦然地说"你可以暂停"，没有叹气没有犹豫
3. 陪伴而非拯救 — "事情发生了，我和你一起面对"
4. 规则归规则，支持归支持 — 该守规则时不替他挡，该支持时不发火
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Tuple
import re

# 从共享常量模块导入（消除重复定义）
try:
    from constants import (
        SUICIDE_KEYWORDS, SELF_HARM_KEYWORDS, DESPAIR_KEYWORDS,
        EXHAUSTION_KEYWORDS, DIRECT_CRISIS_KEYWORDS, METAPHOR_KEYWORDS,
        IMMINENT_SIGNALS, PARENT_SIGNALS, CHILD_SIGNALS,
        INTERMEDIARY_SIGNALS, HIGH_DISTRESS_KEYWORDS,
        MODERATE_DISTRESS_KEYWORDS, SELF_DOUBT_KEYWORDS,
        ANGER_KEYWORDS, SCENARIO_INDEX,
    )
except ImportError:
    # 回退: 本地定义（向后兼容）
    SUICIDE_KEYWORDS = ["自杀", "想死", "不想活", "活不下去", "死了算了", "去死", "结束生命", "不想活了"]
    SELF_HARM_KEYWORDS = ["自伤", "割腕", "割自己", "撞墙", "伤害自己", "划手臂", "划手腕", "自残"]
    DESPAIR_KEYWORDS = ["遗书", "解脱", "活着没意思", "没有意义", "一切无所谓", "生无可恋"]
    EXHAUSTION_KEYWORDS = ["累了真的累了", "撑不下去了", "没有希望了", "看不到尽头", "活够了"]
    DIRECT_CRISIS_KEYWORDS = SUICIDE_KEYWORDS + SELF_HARM_KEYWORDS + DESPAIR_KEYWORDS + EXHAUSTION_KEYWORDS
    METAPHOR_KEYWORDS = ["撑不下去了", "没希望了", "真的累了", "一切都无所谓了", "如果我不在了", "如果我消失了", "没人会在乎的"]
    IMMINENT_SIGNALS = ["正在", "现在", "已经割了", "已经吃了", "准备好了"]
    PARENT_SIGNALS = ["我的孩子", "我儿子", "我女儿", "我家娃", "孩子不听话", "我打了孩子"]
    CHILD_SIGNALS = ["我的父母", "我爸", "我妈", "我家长", "我被打了"]
    INTERMEDIARY_SIGNALS = ["我朋友的孩子", "我姐的孩子", "邻居家", "同事的孩子"]
    HIGH_DISTRESS_KEYWORDS = ["崩溃", "疯了", "受不了", "怎么办", "帮帮我", "撑不住"]
    MODERATE_DISTRESS_KEYWORDS = ["焦虑", "担心", "害怕", "不知道怎么办", "迷茫", "无助"]
    SELF_DOUBT_KEYWORDS = ["我是不是做错了", "我不是好妈妈", "我失败"]
    ANGER_KEYWORDS = ["气死了", "火大", "发火", "吼了", "打了"]
    SCENARIO_INDEX = {
        "01": {"name": "孩子成绩下降", "keywords": ["成绩", "分数", "考试", "退步", "不及格"]},
        "02": {"name": "孩子不想上学", "keywords": ["上学", "逃学", "厌学", "不想去学校"]},
        "03": {"name": "孩子说我不想活了", "keywords": ["不想活", "自杀", "想死"], "priority": "crisis"},
        "04": {"name": "孩子拒绝和父母说话", "keywords": ["拒绝沟通", "沉默", "不理我"]},
        "05": {"name": "孩子打人发脾气", "keywords": ["打人", "发脾气", "暴力"]},
        "07": {"name": "父母自己情绪崩溃", "keywords": ["情绪崩溃", "失控", "吼了孩子"]},
        "08": {"name": "比较", "keywords": ["比较", "别人家孩子", "人家"]},
        "10": {"name": "孩子沉迷手机游戏", "keywords": ["手机", "游戏", "沉迷"]},
        "11": {"name": "孩子被欺负霸凌", "keywords": ["欺负", "霸凌", "被打了"]},
        "12": {"name": "孩子偷东西撒谎", "keywords": ["偷东西", "撒谎"]},
        "18": {"name": "孩子早恋", "keywords": ["早恋", "恋爱"]},
        "19": {"name": "孩子休学退学", "keywords": ["休学", "退学"]},
        "42": {"name": "孩子自伤", "keywords": ["自伤", "割臂", "划手腕"], "priority": "crisis"},
        "66": {"name": "父母打孩子后崩溃", "keywords": ["打孩子", "体罚"]},
        "68": {"name": "青春期孩子说想死", "keywords": ["想死", "青春期自伤"], "priority": "crisis"},
        "70": {"name": "父母复制创伤", "keywords": ["复制创伤", "原生家庭", "像我爸妈"]},
        "73": {"name": "父母倦怠", "keywords": ["倦怠", "太累了", "精疲力竭"]},
        "74": {"name": "孩子社交焦虑", "keywords": ["社交焦虑", "社恐", "不敢交朋友", "没人跟我玩", "怕生", "害羞不敢说话", "不和同学玩", "一个人"], "priority": "normal"},
    }


# ============================================================
# 数据模型 (Data Models)
# ============================================================

class CrisisLevel(Enum):
    """危机等级"""
    NONE = "none"
    METAPHOR = "metaphor"
    DIRECT = "direct"
    IMMINENT = "imminent"


class UserRole(Enum):
    """用户角色"""
    PARENT = "parent"
    CHILD = "child"
    INTERMEDIARY = "intermediary"
    UNKNOWN = "unknown"


class EmotionLevel(Enum):
    """情绪等级（颜色编码）"""
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    BLACK = "black"


class ResponseDepth(Enum):
    """回复深度"""
    THIRTY_SEC = "30sec"
    TWO_MIN = "2min"
    DEEP = "deep"
    CRISIS = "crisis"
    EMERGENCY = "emergency"


class DefenseType(Enum):
    """防御机制类型"""
    SHAME = "shame"
    ANXIETY = "anxiety"
    CONTROL = "control"
    PROJECTION = "projection"
    DENIAL = "denial"
    GUILT = "guilt"
    NONE = "none"


class ErrorPurpose(Enum):
    """孩子错误行为的目的（Dreikurs 四个错误目的）"""
    ATTENTION = "attention"
    POWER = "power"
    REVENGE = "revenge"
    GIVE_UP = "give_up"
    NONE = "none"


@dataclass
class CrisisResult:
    """危机检测结果"""
    level: CrisisLevel
    matched_keywords: List[str] = field(default_factory=list)
    matched_metaphors: List[str] = field(default_factory=list)
    has_imminent_signal: bool = False
    confidence: float = 0.0


@dataclass
class UserIdentity:
    """用户身份识别结果"""
    role: UserRole
    confidence: float = 0.0
    matched_signals: List[str] = field(default_factory=list)


@dataclass
class EmotionState:
    """情绪评估结果"""
    level: EmotionLevel
    score: float = 0.0
    matched_groups: Dict[str, List[str]] = field(default_factory=dict)
    response_depth: ResponseDepth = ResponseDepth.TWO_MIN


@dataclass
class ScenarioMatch:
    """场景匹配结果"""
    scenario_id: str
    name: str
    confidence: float = 0.0
    matched_keywords: List[str] = field(default_factory=list)
    priority: str = "normal"
    match_rate: float = 0.0  # 原始匹配率（加成前）


@dataclass
class DefenseSignal:
    """防御信号"""
    defense_type: DefenseType
    confidence: float = 0.0
    evidence: str = ""
    root_cause: str = ""


@dataclass
class DisplacementAnalysis:
    """位移分析"""
    parent_sees: str = ""
    child_feels: str = ""
    actually_happening: str = ""
    gap_description: str = ""


@dataclass
class ReasoningStep:
    """推理链中的单个步骤"""
    step_name: str
    input_summary: str
    conclusion: str
    confidence: float = 0.0


@dataclass
class ErrorPurposeResult:
    """错误目的检测结果"""
    purpose: ErrorPurpose
    confidence: float = 0.0
    evidence: str = ""
    guidance: str = ""


@dataclass
class ReasoningResult:
    """推理引擎最终输出"""
    crisis: CrisisResult = field(default_factory=lambda: CrisisResult(level=CrisisLevel.NONE))
    identity: UserIdentity = field(default_factory=lambda: UserIdentity(role=UserRole.UNKNOWN))
    emotion: EmotionState = field(default_factory=lambda: EmotionState(level=EmotionLevel.GREEN))
    scenario: Optional[ScenarioMatch] = None
    defenses: List[DefenseSignal] = field(default_factory=list)
    displacement: Optional[DisplacementAnalysis] = None
    error_purpose: Optional[ErrorPurposeResult] = None
    reasoning_steps: List[ReasoningStep] = field(default_factory=list)
    response: str = ""
    follow_up_questions: List[str] = field(default_factory=list)


# ============================================================
# 模块 1: CrisisDetector - 危机检测器
# ============================================================

DEFENSE_KEYWORDS: Dict[DefenseType, Dict[str, object]] = {
    DefenseType.SHAME: {
        "keywords": ["丢人", "没面子", "对得起", "别人怎么看"],
        "root_cause": "父母将孩子的表现与自身价值绑定，害怕被外界评价"
    },
    DefenseType.ANXIETY: {
        "keywords": ["万一", "以后怎么办", "来不及了", "起跑线"],
        "root_cause": "父母对未来的不确定感投射到孩子身上，用焦虑替代信任"
    },
    DefenseType.CONTROL: {
        "keywords": ["必须", "应该", "我说了算", "不许", "不准"],
        "root_cause": "父母通过控制孩子来缓解自身的无力感"
    },
    DefenseType.PROJECTION: {
        "keywords": ["我小时候", "我当年", "我那时候"],
        "root_cause": "父母将自己未完成的期望或创伤投射到孩子身上"
    },
    DefenseType.DENIAL: {
        "keywords": ["没问题", "挺好的", "你想多了"],
        "root_cause": "父母拒绝面对问题以保护自我形象"
    },
    DefenseType.GUILT: {
        "keywords": ["都是我的错", "我害了孩子", "我不是好"],
        "root_cause": "父母过度自责，内疚感阻碍了有效行动"
    },
}

_ERROR_PURPOSE_KEYWORDS: Dict[ErrorPurpose, Dict[str, object]] = {
    ErrorPurpose.ATTENTION: {
        "keywords": ["粘人", "不停说话", "捣乱", "打扰", "故意引起注意"],
        "guidance": "孩子需要被看见。尝试每天给予15分钟专注的陪伴时间，让孩子通过正当方式获得关注。"
    },
    ErrorPurpose.POWER: {
        "keywords": ["顶嘴", "反抗", "不听话", "犟", "偏不", "我就不"],
        "guidance": "孩子在争夺自主权。尝试给予有限选择，让孩子感到被尊重而非被控制。"
    },
    ErrorPurpose.REVENGE: {
        "keywords": ["故意破坏", "打人", "骂人报复", "让你生气"],
        "guidance": "孩子感到受伤，用伤害回应伤害。先修复关系，再处理行为问题。"
    },
    ErrorPurpose.GIVE_UP: {
        "keywords": ["放弃", "不学了", "反正我不行", "无所谓", "随便"],
        "guidance": "孩子感到彻底失败，需要小步成功体验重建信心。降低期望，找到孩子的优势领域。"
    },
}

EXIT_SIGNALS: List[str] = ["够了", "好了", "谢谢", "不想聊了", "先这样吧"]

DISPLACEMENT_TEMPLATES: Dict[str, DisplacementAnalysis] = {
    "孩子成绩下降": DisplacementAnalysis(
        parent_sees="孩子不用功、成绩差、让我丢脸",
        child_feels="我做不到、我不够好、我让父母失望了",
        actually_happening="孩子可能遇到了学习困难，需要帮助而非批评",
        gap_description="父母把成绩等同于孩子的价值，孩子感受到的是条件性的爱"
    ),
    "孩子不想上学": DisplacementAnalysis(
        parent_sees="孩子懒惰、逃避责任、不求上进",
        child_feels="学校让我害怕、我不被接纳、我无法融入",
        actually_happening="孩子可能在学校遇到了社交困难、学业压力或霸凌",
        gap_description="父母看到的是行为，孩子经历的是痛苦"
    ),
    "孩子拒绝和父母说话": DisplacementAnalysis(
        parent_sees="孩子不尊重我、故意冷暴力",
        child_feels="说了也没用、反正不被理解、我需要空间",
        actually_happening="沟通已经断裂，孩子用沉默保护自己",
        gap_description="父母想要连接，孩子需要安全。只有先给安全，连接才可能发生"
    ),
    "孩子打人发脾气": DisplacementAnalysis(
        parent_sees="孩子暴力、没教养、需要管教",
        child_feels="我好生气但不知道怎么表达、没人听我说",
        actually_happening="孩子的情绪调节能力尚未发展成熟，需要引导而非惩罚",
        gap_description="父母看到的是攻击行为，孩子经历的是情绪洪水"
    ),
    "孩子沉迷手机游戏": DisplacementAnalysis(
        parent_sees="孩子沉迷、不自律、浪费时间",
        child_feels="只有在游戏里我才被认可、游戏是我唯一能掌控的东西",
        actually_happening="游戏满足了孩子在现实中未被满足的需求（成就感、社交、掌控感）",
        gap_description="父母想夺走孩子的'避难所'，却不理解孩子为什么需要避难所"
    ),
    "父母自己情绪崩溃": DisplacementAnalysis(
        parent_sees="我控制不住自己、我不是好父母",
        child_feels="爸爸妈妈好可怕、是我做错了什么",
        actually_happening="父母的情绪触发点被激活，可能与自身童年经历有关",
        gap_description="父母的崩溃被孩子理解为'都是我的错'，形成代际创伤循环"
    ),
    "孩子社交焦虑": DisplacementAnalysis(
        parent_sees="孩子胆小、不合群、需要推一把",
        child_feels="我不够好、别人不会喜欢我、社交让我害怕",
        actually_happening="孩子的社交自我效能感不足，需要安全的脚手架而非推力",
        gap_description="父母的'鼓励'在孩子听来是'你做得不够好'，越推越退"
    ),
    "比较": DisplacementAnalysis(
        parent_sees="我是在激励孩子、让他有目标",
        child_feels="我不够好、爸妈不爱我爱的是那个'别人家孩子'",
        actually_happening="比较摧毁了孩子的自我价值感，而非激发动力",
        gap_description="父母以为比较是激励，孩子感受到的是贬低和否定"
    ),
}

DEFAULT_DISPLACEMENT: DisplacementAnalysis = DisplacementAnalysis(
    parent_sees="孩子出了问题，需要被纠正",
    child_feels="我不被理解、我不够好",
    actually_happening="孩子的行为背后有未被看见的需求和情感",
    gap_description="父母关注行为表面，孩子需要的是被理解和接纳"
)


# ============================================================
# 模块 1: CrisisDetector - 危机检测器
# ============================================================

class CrisisDetector:
    """危机检测器 - 识别自杀、自伤等危机信号"""

    def detect(self, text: str) -> CrisisResult:
        """
        检测文本中的危机信号。

        规则:
            1. 直接关键词 + 即将发生信号 → IMMINENT
            2. 直接关键词 → DIRECT
            3. 2+ 隐喻 → 升级为 DIRECT
            4. 1 隐喻 → METAPHOR
            5. 无匹配 → NONE
        """
        try:
            if not text:
                return CrisisResult(level=CrisisLevel.NONE, confidence=1.0)

            matched_keywords: List[str] = []
            matched_metaphors: List[str] = []

            for keyword in DIRECT_CRISIS_KEYWORDS:
                if keyword in text:
                    matched_keywords.append(keyword)

            for metaphor in METAPHOR_KEYWORDS:
                if metaphor in text:
                    matched_metaphors.append(metaphor)

            # 去重：隐喻如果已在直接关键词中则不算
            matched_metaphors = [m for m in matched_metaphors if m not in matched_keywords]

            has_imminent = any(signal in text for signal in IMMINENT_SIGNALS)

            # 判断危机等级
            if matched_keywords and has_imminent:
                return CrisisResult(
                    level=CrisisLevel.IMMINENT,
                    matched_keywords=matched_keywords,
                    matched_metaphors=matched_metaphors,
                    has_imminent_signal=True,
                    confidence=0.95
                )
            if matched_keywords:
                return CrisisResult(
                    level=CrisisLevel.DIRECT,
                    matched_keywords=matched_keywords,
                    matched_metaphors=matched_metaphors,
                    has_imminent_signal=has_imminent,
                    confidence=0.85
                )
            # 2+ 隐喻升级为 DIRECT
            if len(matched_metaphors) >= 2:
                return CrisisResult(
                    level=CrisisLevel.DIRECT,
                    matched_keywords=[],
                    matched_metaphors=matched_metaphors,
                    has_imminent_signal=has_imminent,
                    confidence=0.75
                )
            if len(matched_metaphors) == 1:
                return CrisisResult(
                    level=CrisisLevel.METAPHOR,
                    matched_keywords=[],
                    matched_metaphors=matched_metaphors,
                    has_imminent_signal=has_imminent,
                    confidence=0.5
                )
            return CrisisResult(level=CrisisLevel.NONE, confidence=0.9)
        except Exception:
            # 异常时保守返回 NONE，避免因检测失败阻断管道
            return CrisisResult(level=CrisisLevel.NONE, confidence=0.0)


# ============================================================
# 模块 2: UserIdentifier - 用户身份识别器
# ============================================================

class UserIdentifier:
    """用户身份识别器 - 判断说话者是父母、孩子还是第三方"""

    def identify(self, text: str) -> UserIdentity:
        """
        识别用户角色。

        基于关键词匹配判断用户是父母、孩子还是中间人。
        """
        if not text:
            return UserIdentity(role=UserRole.UNKNOWN, confidence=0.0)

        parent_matches = [s for s in PARENT_SIGNALS if s in text]
        child_matches = [s for s in CHILD_SIGNALS if s in text]
        intermediary_matches = [s for s in INTERMEDIARY_SIGNALS if s in text]

        scores = {
            UserRole.PARENT: len(parent_matches),
            UserRole.CHILD: len(child_matches),
            UserRole.INTERMEDIARY: len(intermediary_matches),
        }

        best_role = max(scores, key=lambda k: scores[k])
        best_score = scores[best_role]

        if best_score == 0:
            return UserIdentity(role=UserRole.UNKNOWN, confidence=0.3)

        # 置信度：基于匹配数量，上限 0.95
        confidence = min(0.5 + best_score * 0.2, 0.95)
        matched = []
        if best_role == UserRole.PARENT:
            matched = parent_matches
        elif best_role == UserRole.CHILD:
            matched = child_matches
        else:
            matched = intermediary_matches

        return UserIdentity(role=best_role, confidence=confidence, matched_signals=matched)


# ============================================================
# 模块 3: EmotionAssessor - 情绪评估器
# ============================================================

class EmotionAssessor:
    """情绪评估器 - 基于关键词分组评估情绪状态"""

    def assess(self, text: str, crisis: Optional[CrisisResult] = None,
               context: Optional[List[str]] = None) -> EmotionState:
        """
        评估用户情绪状态。

        评分规则:
            - high_distress 关键词 → 0.8+
            - anger 关键词 → 0.7+
            - self_doubt 关键词 → 0.6+
            - moderate_distress 关键词 → 0.5+

        危机覆盖: 如果 crisis.level 为 IMMINENT/DIRECT/METAPHOR → 强制 BLACK

        Args:
            text: 用户输入文本
            crisis: 危机检测结果
            context: 可选的历史消息列表，用于增强情绪评估
        """
        if not text:
            return EmotionState(level=EmotionLevel.GREEN, score=0.0)

        # 如果有上下文，将其拼接到评估文本中以增强关键词匹配
        eval_text = text
        if context:
            eval_text = " ".join(context[-3:]) + " " + text

        matched_groups: Dict[str, List[str]] = {}
        group_scores: List[float] = []

        # 检测各情绪组
        high_matches = [k for k in HIGH_DISTRESS_KEYWORDS if k in eval_text]
        moderate_matches = [k for k in MODERATE_DISTRESS_KEYWORDS if k in eval_text]
        self_doubt_matches = [k for k in SELF_DOUBT_KEYWORDS if k in eval_text]
        anger_matches = [k for k in ANGER_KEYWORDS if k in eval_text]

        if high_matches:
            matched_groups["high_distress"] = high_matches
            group_scores.append(0.8 + len(high_matches) * 0.05)
        if anger_matches:
            matched_groups["anger"] = anger_matches
            group_scores.append(0.7 + len(anger_matches) * 0.05)
        if self_doubt_matches:
            matched_groups["self_doubt"] = self_doubt_matches
            group_scores.append(0.6 + len(self_doubt_matches) * 0.05)
        if moderate_matches:
            matched_groups["moderate_distress"] = moderate_matches
            group_scores.append(0.5 + len(moderate_matches) * 0.05)

        # 加权聚合：最高分组 + 其他匹配组的小幅加成
        if group_scores:
            max_score = max(group_scores)
            extra_groups = len(group_scores) - 1
            total_score = max_score + 0.02 * extra_groups
        else:
            total_score = 0.0

        total_score = min(total_score, 1.0)

        # 确定情绪等级
        if crisis and crisis.level in (CrisisLevel.IMMINENT, CrisisLevel.DIRECT, CrisisLevel.METAPHOR):
            level = EmotionLevel.BLACK
        elif total_score >= 0.8:
            level = EmotionLevel.RED
        elif total_score >= 0.5:
            level = EmotionLevel.YELLOW
        else:
            level = EmotionLevel.GREEN

        # 确定回复深度
        depth_map = {
            EmotionLevel.BLACK: ResponseDepth.CRISIS,
            EmotionLevel.RED: ResponseDepth.CRISIS,
            EmotionLevel.YELLOW: ResponseDepth.THIRTY_SEC,
            EmotionLevel.GREEN: ResponseDepth.TWO_MIN,
        }

        return EmotionState(
            level=level,
            score=total_score,
            matched_groups=matched_groups,
            response_depth=depth_map[level]
        )


# ============================================================
# 模块 4: ScenarioMatcher - 场景匹配器
# ============================================================

class ScenarioMatcher:
    """场景匹配器 - 基于关键词重叠匹配育儿场景"""

    def match(self, text: str, context: Optional[List[str]] = None) -> Optional[ScenarioMatch]:
        """
        匹配最相关的育儿场景。

        优先级场景（crisis）获得 1.5x 置信度加成。
        返回最佳匹配或 None。

        Args:
            text: 用户输入文本
            context: 可选的历史消息列表，用于增强场景匹配
        """
        if not text:
            return None

        # 如果有上下文，将其拼接到匹配文本中
        eval_text = text
        if context:
            eval_text = " ".join(context[-3:]) + " " + text

        best_match: Optional[ScenarioMatch] = None
        best_score = 0

        for sid, scenario in SCENARIO_INDEX.items():
            keywords = scenario["keywords"]
            matched = [k for k in keywords if k in eval_text]
            if not matched:
                continue

            # 基础分数 = 匹配关键词数 / 总关键词数
            raw_score = len(matched) / len(keywords)
            score = raw_score

            # 优先级加成
            priority = scenario.get("priority", "normal")
            if priority == "crisis":
                score *= 1.5

            if score > best_score:
                best_score = score
                # 置信度基于匹配关键词数量而非覆盖广度
                count_confidence = min(0.4 + len(matched) * 0.2, 0.95)
                best_match = ScenarioMatch(
                    scenario_id=sid,
                    name=scenario["name"],
                    confidence=count_confidence,
                    matched_keywords=matched,
                    priority=priority,
                    match_rate=raw_score
                )

        return best_match


# ============================================================
# 模块 5: DefenseSignalDetector - 防御信号检测器
# ============================================================

class DefenseSignalDetector:
    """防御信号检测器 - 识别父母的心理防御机制"""

    def detect(self, text: str) -> List[DefenseSignal]:
        """
        检测文本中的防御机制信号。

        返回所有检测到的防御信号列表（可能为空）。
        """
        if not text:
            return []

        signals: List[DefenseSignal] = []

        for defense_type, data in DEFENSE_KEYWORDS.items():
            keywords = data["keywords"]  # type: ignore
            matched = [k for k in keywords if k in text]
            if matched:
                confidence = min(0.5 + len(matched) * 0.15, 0.95)
                signals.append(DefenseSignal(
                    defense_type=defense_type,
                    confidence=confidence,
                    evidence="、".join(matched),
                    root_cause=data["root_cause"]  # type: ignore
                ))

        return signals


# ============================================================
# 模块 6: DisplacementAnalyzer - 位移分析器
# ============================================================

class DisplacementAnalyzer:
    """位移分析器 - 分析父母视角与孩子感受之间的错位"""

    def analyze(
        self,
        text: str,
        scenario: Optional[ScenarioMatch],
        defenses: List[DefenseSignal],
        identity: Optional[UserIdentity] = None
    ) -> DisplacementAnalysis:
        """
        生成位移分析。

        基于匹配的场景选择对应模板；无匹配时使用默认模板。
        """
        if scenario and scenario.name in DISPLACEMENT_TEMPLATES:
            return DISPLACEMENT_TEMPLATES[scenario.name]

        # 如果有防御信号但无特定场景，基于防御类型微调
        if defenses:
            # 使用默认模板，但根据防御类型调整 gap_description
            base = DEFAULT_DISPLACEMENT
            defense_names = [d.defense_type.value for d in defenses]
            gap = f"父母表现出{'、'.join(defense_names)}防御，{base.gap_description}"
            return DisplacementAnalysis(
                parent_sees=base.parent_sees,
                child_feels=base.child_feels,
                actually_happening=base.actually_happening,
                gap_description=gap
            )

        return DEFAULT_DISPLACEMENT


# ============================================================
# 模块 7: ErrorPurposeDetector - 错误目的检测器
# ============================================================

class ErrorPurposeDetector:
    """错误目的检测器 - 基于 Dreikurs 理论判断孩子行为的错误目的"""

    def detect(self, text: str) -> Optional[ErrorPurposeResult]:
        """
        检测孩子行为的错误目的。

        基于父母描述的孩子行为关键词匹配 Dreikurs 四个错误目的。
        """
        if not text:
            return None

        best_purpose: Optional[ErrorPurpose] = None
        best_score = 0
        best_evidence: List[str] = []

        for purpose, data in _ERROR_PURPOSE_KEYWORDS.items():
            keywords = data["keywords"]  # type: ignore
            matched = [k for k in keywords if k in text]
            if len(matched) > best_score:
                best_score = len(matched)
                best_purpose = purpose
                best_evidence = matched

        if best_purpose is None or best_score == 0:
            return None

        return ErrorPurposeResult(
            purpose=best_purpose,
            confidence=min(0.5 + best_score * 0.15, 0.95),
            evidence="、".join(best_evidence),
            guidance=_ERROR_PURPOSE_KEYWORDS[best_purpose]["guidance"]  # type: ignore
        )


# ============================================================
# 模块 8: ReasoningChainGenerator - 推理链生成器
# ============================================================

class ReasoningChainGenerator:
    """推理链生成器 - 将各模块结果串联为可追溯的推理步骤"""

    def generate(
        self,
        crisis: CrisisResult,
        identity: UserIdentity,
        emotion: EmotionState,
        scenario: Optional[ScenarioMatch],
        defenses: List[DefenseSignal],
        displacement: Optional[DisplacementAnalysis],
        error_purpose: Optional[ErrorPurposeResult] = None
    ) -> List[ReasoningStep]:
        """
        生成推理链步骤列表。

        每个步骤包含：步骤名称、输入摘要、结论、置信度。
        """
        steps: List[ReasoningStep] = []

        # Step 1: 危机评估
        crisis_summary = f"检测到{len(crisis.matched_keywords)}个直接关键词，{len(crisis.matched_metaphors)}个隐喻"
        crisis_conclusion = f"危机等级: {crisis.level.value}"
        if crisis.level != CrisisLevel.NONE:
            crisis_conclusion += f"，匹配: {', '.join(crisis.matched_keywords + crisis.matched_metaphors)}"
        steps.append(ReasoningStep(
            step_name="危机评估",
            input_summary=crisis_summary,
            conclusion=crisis_conclusion,
            confidence=crisis.confidence
        ))

        # Step 2: 身份识别
        id_summary = f"角色信号: {', '.join(identity.matched_signals)}" if identity.matched_signals else "无明确角色信号"
        steps.append(ReasoningStep(
            step_name="身份识别",
            input_summary=id_summary,
            conclusion=f"识别为: {identity.role.value}",
            confidence=identity.confidence
        ))

        # Step 3: 情绪评估
        emotion_groups = ", ".join(f"{k}({len(v)})" for k, v in emotion.matched_groups.items()) if emotion.matched_groups else "无明显情绪信号"
        steps.append(ReasoningStep(
            step_name="情绪评估",
            input_summary=f"情绪组: {emotion_groups}",
            conclusion=f"情绪等级: {emotion.level.value}，评分: {emotion.score:.2f}",
            confidence=min(emotion.score + 0.3, 1.0)
        ))

        # Step 4: 场景匹配
        if scenario:
            steps.append(ReasoningStep(
                step_name="场景匹配",
                input_summary=f"匹配关键词: {', '.join(scenario.matched_keywords)}",
                conclusion=f"匹配场景: [{scenario.scenario_id}] {scenario.name}",
                confidence=scenario.confidence
            ))
        else:
            steps.append(ReasoningStep(
                step_name="场景匹配",
                input_summary="无关键词匹配",
                conclusion="未匹配到特定场景",
                confidence=0.1
            ))

        # Step 5: 防御分析
        if defenses:
            defense_summary = "、".join(d.defense_type.value for d in defenses)
            top_defense = max(defenses, key=lambda d: d.confidence)
            steps.append(ReasoningStep(
                step_name="防御分析",
                input_summary=f"检测到防御: {defense_summary}",
                conclusion=f"主要防御: {top_defense.defense_type.value}，根因: {top_defense.root_cause}",
                confidence=top_defense.confidence
            ))

        # Step 6: 位移分析
        if displacement and displacement.gap_description:
            steps.append(ReasoningStep(
                step_name="位移分析",
                input_summary=f"父母视角: {displacement.parent_sees}",
                conclusion=f"错位: {displacement.gap_description}",
                confidence=0.7
            ))

        # Step 7: 错误目的分析
        if error_purpose and error_purpose.purpose != ErrorPurpose.NONE:
            steps.append(ReasoningStep(
                step_name="错误目的分析",
                input_summary=f"行为信号: {error_purpose.evidence}",
                conclusion=f"错误目的: {error_purpose.purpose.value}，建议: {error_purpose.guidance}",
                confidence=error_purpose.confidence
            ))

        return steps


# ============================================================
# 模块 9: ResponseGenerator - 回复生成器
# ============================================================

class ResponseGenerator:
    """回复生成器 - 基于各模块结果生成适配的回复"""

    def generate_crisis_response(self, crisis: CrisisResult) -> str:
        """
        生成危机回复。

        包含关心表达 + 专业资源。
        """
        base = "我很担心你现在的状态。你愿意说的每一句话我都会认真听。"
        resources = (
            "\n\n如果你正处于紧急危险中，请立即拨打："
            "\n• 全国24小时心理援助热线：400-161-9995"
            "\n• 北京心理危机研究与干预中心：010-82951332"
            "\n• 生命热线：400-821-1215"
        )
        if crisis.level == CrisisLevel.IMMINENT:
            return f"我听到你说的这些，我非常担心你的安全。{base}{resources}"
        return f"{base}{resources}"

    def generate(
        self,
        crisis: CrisisResult,
        identity: UserIdentity,
        emotion: EmotionState,
        scenario: Optional[ScenarioMatch],
        defenses: List[DefenseSignal],
        displacement: Optional[DisplacementAnalysis],
        error_purpose: Optional[ErrorPurposeResult] = None
    ) -> str:
        """
        生成完整回复。

        策略:
            - 危机 → 危机回复
            - RED → 30秒简短共情
            - YELLOW → 2分钟共情+建议
            - GREEN → 2分钟
        """
        try:
            # 危机短路
            if crisis.level in (CrisisLevel.IMMINENT, CrisisLevel.DIRECT        ):
                return self.generate_crisis_response(crisis)

            parts: List[str] = []

            # 情绪共情开头
            if emotion.level == EmotionLevel.RED:
                emotion_word = "痛苦"
                if emotion.matched_groups.get("anger"):
                    emotion_word = "愤怒"
                elif emotion.matched_groups.get("high_distress"):
                    emotion_word = "崩溃"
                parts.append(f"我能感受到你现在非常{emotion_word}，这种感受是真实的。")
            elif emotion.level == EmotionLevel.YELLOW:
                parts.append("我听到你了，你愿意说出来已经很勇敢了。")
            else:
                parts.append("谢谢你愿意分享这些。")

            # 场景相关建议
            if scenario:
                if displacement:
                    parts.append(f"\n关于{scenario.name}：")
                    parts.append(f"你看到的是：{displacement.parent_sees}")
                    parts.append(f"但孩子可能感受到的是：{displacement.child_feels}")
                    parts.append(f"\n{displacement.gap_description}")
                else:
                    parts.append(f"\n关于{scenario.name}，我理解你的担忧。")

            # 防御信号的温和回应
            if defenses:
                top = max(defenses, key=lambda d: d.confidence)
                if top.defense_type == DefenseType.SHAME:
                    parts.append("\n孩子的表现不代表你作为父母的价值。")
                elif top.defense_type == DefenseType.ANXIETY:
                    parts.append("\n你的担心是可以理解的，但焦虑有时会让我们看不到孩子的感受。")
                elif top.defense_type == DefenseType.CONTROL:
                    parts.append("\n当我们感到无力时，控制会让我们觉得安全。但孩子需要的是引导，而不是控制。")
                elif top.defense_type == DefenseType.GUILT:
                    parts.append("\n自责说明你很在意，但过度内疚会阻碍你做出有效的改变。")

            # 错误目的建议
            if error_purpose and error_purpose.guidance:
                parts.append(f"\n关于孩子的行为：{error_purpose.guidance}")

            # 通用建议
            if scenario and not error_purpose:
                parts.append("\n\n建议：先倾听孩子的感受，不要急于给建议或解决方案。有时候，被理解比被帮助更重要。")

            # 追问引导
            if identity.role == UserRole.PARENT:
                parts.append("\n\n你愿意多说一些孩子的具体情况吗？比如最近发生了什么变化？")
            elif identity.role == UserRole.CHILD:
                parts.append("\n\n你愿意告诉我更多吗？你现在的感受是什么？")
            else:
                parts.append("\n\n你能告诉我更多细节吗？")

            return "".join(parts)
        except Exception:
            # 回复生成异常时返回安全的通用回复
            return "我理解你正在经历一些困难。请告诉我更多，我会尽力帮助你。"


# ============================================================
# 模块 10: ExitDetector - 退出信号检测器
# ============================================================

class ExitDetector:
    """退出信号检测器 - 识别用户想要结束对话的信号"""

    def detect(self, text: str, recent_messages: Optional[List[str]] = None) -> bool:
        """
        检测退出信号。

        类型:
            1. 直接退出: "够了"、"谢谢"等
            2. 间接退出: 连续2+条短AI回复（<8字符）表明对话即将结束
            3. 话题切换: 完全不同的主题
        """
        if not text:
            return False

        # 直接退出信号
        for signal in EXIT_SIGNALS:
            if signal in text:
                return True

        # 间接退出：连续短AI回复表明对话热度下降
        if recent_messages and len(recent_messages) >= 2:
            last_two = recent_messages[-2:]
            if all(len(m.strip()) < 8 for m in last_two):
                return True

        return False


# ============================================================
# 主引擎: ParentingReasoningEngine
# ============================================================

class ParentingReasoningEngine:
    """
    育儿心理学推理引擎 - 6层决策管道

    处理流程:
        1. CrisisDetector → 危机检测（短路）
        2. UserIdentifier → 身份识别
        3. EmotionAssessor → 情绪评估
        4. ScenarioMatcher → 场景匹配
        5. DefenseSignalDetector + DisplacementAnalyzer → 防御与位移分析
        6. ReasoningChainGenerator + ResponseGenerator → 推理链与回复
    """

    def __init__(self) -> None:
        self.crisis_detector = CrisisDetector()
        self.user_identifier = UserIdentifier()
        self.emotion_assessor = EmotionAssessor()
        self.scenario_matcher = ScenarioMatcher()
        self.defense_detector = DefenseSignalDetector()
        self.displacement_analyzer = DisplacementAnalyzer()
        self.error_purpose_detector = ErrorPurposeDetector()
        self.reasoning_generator = ReasoningChainGenerator()
        self.response_generator = ResponseGenerator()
        self.exit_detector = ExitDetector()

    def process(self, text: str, context: Optional[List[str]] = None) -> ReasoningResult:
        """
        处理用户输入，通过完整的6层决策管道。

        Args:
            text: 用户输入文本
            context: 可选的历史消息列表

        Returns:
            ReasoningResult 包含所有分析结果和回复
        """
        try:
            # Layer 1: 危机检测
            crisis = self.crisis_detector.detect(text)

            # 危机短路：直接返回危机回复
            if crisis.level in (CrisisLevel.IMMINENT, CrisisLevel.DIRECT):
                response = self.response_generator.generate_crisis_response(crisis)
                steps = self.reasoning_generator.generate(
                    crisis=crisis,
                    identity=UserIdentity(role=UserRole.UNKNOWN),
                    emotion=EmotionState(level=EmotionLevel.BLACK),
                    scenario=None,
                    defenses=[],
                    displacement=None
                )
                return ReasoningResult(
                    crisis=crisis,
                    identity=UserIdentity(role=UserRole.UNKNOWN),
                    emotion=EmotionState(level=EmotionLevel.BLACK, response_depth=ResponseDepth.CRISIS),
                    scenario=None,
                    defenses=[],
                    displacement=None,
                    error_purpose=None,
                    reasoning_steps=steps,
                    response=response,
                    follow_up_questions=["你现在安全吗？", "你身边有没有可以信任的人？"]
                )

            # Layer 2: 身份识别
            identity = self.user_identifier.identify(text)

            # Layer 3: 情绪评估（传入 context 增强评估）
            emotion = self.emotion_assessor.assess(text, crisis, context)

            # Layer 4: 场景匹配（传入 context 增强匹配）
            scenario = self.scenario_matcher.match(text, context)

            # Layer 5: 防御检测 + 位移分析 + 错误目的检测
            defenses = self.defense_detector.detect(text)
            displacement = self.displacement_analyzer.analyze(text, scenario, defenses, identity)
            error_purpose = self.error_purpose_detector.detect(text)

            # Layer 6: 推理链 + 回复生成
            reasoning_steps = self.reasoning_generator.generate(
                crisis=crisis,
                identity=identity,
                emotion=emotion,
                scenario=scenario,
                defenses=defenses,
                displacement=displacement,
                error_purpose=error_purpose
            )
            response = self.response_generator.generate(
                crisis=crisis,
                identity=identity,
                emotion=emotion,
                scenario=scenario,
                defenses=defenses,
                displacement=displacement,
                error_purpose=error_purpose
            )

            # 生成追问
            follow_ups = self._generate_follow_ups(identity, scenario, emotion)

            return ReasoningResult(
                crisis=crisis,
                identity=identity,
                emotion=emotion,
                scenario=scenario,
                defenses=defenses,
                displacement=displacement,
                error_purpose=error_purpose,
                reasoning_steps=reasoning_steps,
                response=response,
                follow_up_questions=follow_ups
            )
        except Exception as e:
            # 关键路径异常兜底：返回安全的默认结果
            return ReasoningResult(
                crisis=CrisisResult(level=CrisisLevel.NONE),
                identity=UserIdentity(role=UserRole.UNKNOWN),
                emotion=EmotionState(level=EmotionLevel.GREEN),
                response="抱歉，处理您的消息时遇到了问题。请您再描述一下情况，我会尽力帮助您。",
                follow_up_questions=["您能重新描述一下您的情况吗？"]
            )

    def process_conversation(self, messages: List[str]) -> List[ReasoningResult]:
        """
        处理一组对话消息。

        使用上下文信息增强理解。最后一条消息是当前输入。

        Args:
            messages: 消息列表，按时间顺序

        Returns:
            每条消息的 ReasoningResult 列表
        """
        if not messages:
            return []

        results: List[ReasoningResult] = []
        for i, msg in enumerate(messages):
            context = messages[:i] if i > 0 else None
            result = self.process(msg, context)
            results.append(result)

        return results

    def _generate_follow_ups(
        self,
        identity: UserIdentity,
        scenario: Optional[ScenarioMatch],
        emotion: EmotionState
    ) -> List[str]:
        """生成追问问题列表"""
        questions: List[str] = []

        if identity.role == UserRole.PARENT:
            if scenario:
                questions.append(f"关于{scenario.name}，这种情况持续多久了？")
                questions.append("你之前尝试过什么方法吗？")
            else:
                questions.append("你能具体描述一下发生了什么吗？")
            questions.append("你和孩子的关系平时怎么样？")
        elif identity.role == UserRole.CHILD:
            questions.append("你现在的感受是什么？")
            questions.append("你有没有信任的人可以倾诉？")
        else:
            questions.append("你能提供更多关于这个家庭的背景吗？")
            questions.append("孩子多大了？")

        return questions[:3]  # 最多3个追问


# ============================================================
# 便捷函数
# ============================================================

def create_engine() -> ParentingReasoningEngine:
    """创建推理引擎实例的工厂函数"""
    return ParentingReasoningEngine()


def quick_analyze(text: str) -> Dict:
    """
    快速分析函数 - 返回简化的分析结果字典。

    适用于快速测试或集成场景。
    """
    engine = create_engine()
    result = engine.process(text)
    return {
        "crisis_level": result.crisis.level.value,
        "user_role": result.identity.role.value,
        "emotion_level": result.emotion.level.value,
        "scenario": result.scenario.name if result.scenario else None,
        "defenses": [d.defense_type.value for d in result.defenses],
        "response": result.response,
        "follow_ups": result.follow_up_questions,
    }
