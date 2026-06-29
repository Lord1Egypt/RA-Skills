#!/usr/bin/env python3
"""
Empathy Generator — 共情生成器 v2.1.0
育儿心理学共情表达引擎

核心哲学（源自真实的育儿智慧）：
1. 没有评判的接纳 — 看到"你受苦了"，不是"你有问题"
2. 没有负罪感的许可 — 坦然地说"你可以暂停"
3. 陪伴而非拯救 — "事情发生了，我和你一起面对"
4. 规则归规则，支持归支持

四层共情模型:
    Layer 1: 接纳 — 承认情绪的存在，不评判
    Layer 2: 理解 — 从对方视角理解处境
    Layer 3: 支持 — 提供情感支撑和陪伴感
    Layer 4: 赋能 — 引导对方看到自己的力量

来源理论:
    - Carl Rogers: 无条件积极关注
    - Kristin Neff: 自我慈悲三要素
    - Marshall Rosenberg: 非暴力沟通
    - Daniel Goleman: 情商
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Tuple
import re
import logging

# 从共享常量模块导入情绪关键词
try:
    from constants import (
        EMOTION_KEYWORDS, INTENSITY_MARKERS_UP, INTENSITY_MARKERS_DOWN,
        POSITIVE_EMOTION_WORDS, NEGATIVE_EMOTION_WORDS,
    )
except ImportError:
    # 回退: 本地定义（向后兼容）
    EMOTION_KEYWORDS = {
        "anger": ["愤怒", "生气", "气死", "火大", "暴怒", "发火", "怒", "恼", "吼了", "吼孩子"],
        "sadness": ["难过", "伤心", "悲伤", "哭", "心碎", "痛", "失落", "心酸"],
        "anxiety": ["焦虑", "担心", "不安", "紧张", "害怕", "恐惧", "慌", "万一", "以后怎么办"],
        "shame": ["丢人", "没面子", "羞耻", "丢脸", "被人看"],
        "guilt": ["内疚", "愧疚", "自责", "我的错", "害了", "对不起", "后悔",
                  "不是好妈妈", "不是好爸爸", "不是好", "打了孩子", "打孩子", "吼了孩子"],
        "helplessness": ["无助", "没办法", "不知道怎么办", "无能为力", "绝望", "怎么办"],
        "exhaustion": ["累", "疲惫", "撑不住", "精疲力竭", "倦怠", "崩溃", "撑不下去", "受不了"],
        "loneliness": ["孤独", "没人理解", "一个人", "没人懂", "没人关心"],
        "frustration": ["挫败", "沮丧", "受挫", "不听话", "怎么说都不听"],
    }
    INTENSITY_MARKERS_UP = ["非常", "极其", "完全", "彻底", "超级", "极度", "太", "好", "真的"]
    INTENSITY_MARKERS_DOWN = ["有点", "稍微", "略微", "一点点", "一些", "有些", "不太", "不怎么", "还行"]
    POSITIVE_EMOTION_WORDS = {"开心", "快乐", "幸福", "兴奋", "满足", "爱", "喜欢", "高兴", "愉快", "欣慰", "温暖", "感动", "自豪", "轻松"}
    NEGATIVE_EMOTION_WORDS = {"生气", "愤怒", "伤心", "难过", "焦虑", "恐惧", "绝望", "崩溃", "无助", "委屈", "压抑", "沉重", "紧张", "害怕", "担忧"}

logger = logging.getLogger(__name__)


# ============================================================
# 数据模型
# ============================================================

class EmpathyLevel(Enum):
    ACCEPTANCE = "acceptance"
    UNDERSTANDING = "understanding"
    SUPPORT = "support"
    EMPOWERMENT = "empowerment"


class EmpathyTrap(Enum):
    PSEUDO_EMPATHY = "pseudo_empathy"
    JUDGMENTAL = "judgmental"
    FIXING = "fixing"
    COMPARING = "comparing"
    MINIMIZING = "minimizing"
    OVER_IDENTIFYING = "over_identifying"
    TOXIC_POSITIVITY = "toxic_positivity"
    ADVICE_DISGUISED = "advice_disguised"
    BLAME_SHIFTING = "blame_shifting"


class EmpathyScenario(Enum):
    EMOTIONAL_CRISIS = "emotional_crisis"
    PARENT_GUILT = "parent_guilt"
    CHILD_BEHAVIOR = "child_behavior"
    COMMUNICATION_BREAK = "communication_break"
    EXHAUSTION = "exhaustion"
    FEAR_ANXIETY = "fear_anxiety"
    GENERAL = "general"


@dataclass
class EmotionInput:
    primary_emotion: str = ""
    secondary_emotions: List[str] = field(default_factory=list)
    intensity: float = 5.0
    valence: float = 0.0
    is_crisis: bool = False


@dataclass
class EmpathyTrapResult:
    has_trap: bool = False
    trap_type: Optional[EmpathyTrap] = None
    trap_text: str = ""
    suggestion: str = ""
    severity: int = 0


@dataclass
class EmpathyBalance:
    empathy_ratio: float = 0.0
    advice_ratio: float = 0.0
    is_balanced: bool = True
    recommendation: str = ""


@dataclass
class EmpathyExpression:
    level: EmpathyLevel = EmpathyLevel.ACCEPTANCE
    text: str = ""
    scenario: EmpathyScenario = EmpathyScenario.GENERAL
    techniques_used: List[str] = field(default_factory=list)
    quality_score: float = 0.0


@dataclass
class EmpathyResult:
    level: EmpathyLevel = EmpathyLevel.ACCEPTANCE
    expressions: List[EmpathyExpression] = field(default_factory=list)
    full_response: str = ""
    traps_detected: List[EmpathyTrapResult] = field(default_factory=list)
    balance: EmpathyBalance = field(default_factory=EmpathyBalance)
    quality_score: float = 0.0
    techniques_used: List[str] = field(default_factory=list)
    follow_up_questions: List[str] = field(default_factory=list)


# ============================================================
# 共情话术库
# ============================================================

ACCEPTANCE_TEMPLATES: Dict[str, List[str]] = {
    "anger": [
        "我听到你说的了，你的愤怒是真实的。",
        "你有权利生气。这种愤怒背后，是深深的在乎。",
        "感受到这么强烈的愤怒，一定很不容易。",
        "你的愤怒在告诉我，这件事对你很重要。",
        "生气是正常的，你不需要为自己的情绪道歉。",
        "我能感受到你现在非常愤怒，这种情绪是被允许的。",
    ],
    "sadness": [
        "我听到了你的难过。这种感受是真实的，不需要隐藏。",
        "你愿意说出来，本身就需要很大的勇气。",
        "悲伤不是软弱，是你在乎的证明。",
        "你的眼泪在说一些语言无法表达的东西。",
        "难过的时候不需要假装坚强，我在这里。",
        "这种心痛是真实的，你不需要解释。",
    ],
    "anxiety": [
        "你的焦虑是真实的反应，不是'想太多'。",
        "面对不确定性感到焦虑，是人之常情。",
        "我听到你的担心了。这种感受是有原因的。",
        "焦虑的感觉很不舒服，但它是你内心在乎的信号。",
        "你的担心说明你在认真对待这件事。",
        "在不确定中感到不安，这完全可以理解。",
    ],
    "fear": [
        "害怕是正常的反应，它在保护你。",
        "你愿意承认自己害怕，这本身就很勇敢。",
        "恐惧不代表你软弱，代表你在乎。",
        "你感受到的恐惧是真实的，不需要克服它才算是好父母。",
        "害怕未知是人的本能，你不需要为此羞愧。",
    ],
    "shame": [
        "你感受到的羞耻，不代表你这个人有问题。",
        "很多父母都会有这种感受，你不是一个人。",
        "感到羞耻说明你在乎，但你不该为此受罚。",
        "羞耻感会让人想要躲起来，但你选择了说出来，这很勇敢。",
        "你不需要为自己的挣扎感到羞耻。",
    ],
    "guilt": [
        "你的内疚说明你很在意孩子。但内疚不等于事实。",
        "感到内疚的父母，往往是最用心的父母。",
        "你不需要完美，你已经在努力了。",
        "内疚说明你在乎，但你不该被它困住。",
        "你愿意反思自己，这本身就说明你是一个好父母。",
        "没有人天生就会当父母，你已经在尽力了。",
    ],
    "helplessness": [
        "感到无助是真实的，不代表你失败了。",
        "当所有方法都试过却没用时，无助是正常反应。",
        "你已经在能力范围内尽力了。",
        "无助的感觉会让人窒息，但你不是真的无能为力。",
        "承认无助需要勇气，你做到了。",
    ],
    "exhaustion": [
        "你累了。这种累不只是身体上的，是心累。",
        "持续消耗而不补充，任何人都会枯竭。",
        "你有权利说'我撑不住了'。这不是软弱。",
        "你一直在付出，累了是正常的。",
        "精疲力竭的时候，连呼吸都觉得重。",
        "你不需要坚强到永远不会累。",
    ],
    "loneliness": [
        "没人理解的感觉真的很孤独。",
        "你不是一个人。虽然现在感觉如此。",
        "孤独是一种很重的感受，你不需要独自承受。",
        "你渴望被理解，这很正常。",
    ],
    "frustration": [
        "反复尝试却没有结果，确实令人沮丧。",
        "你的挫败感是真实的，这说明你在乎。",
        "怎么努力都没用的感觉，真的很难受。",
        "挫败不代表你做得不够好。",
    ],
    "default": [
        "我听到你说的了。你的感受是真实的。",
        "谢谢你愿意告诉我这些。",
        "你愿意说出来，这很重要。",
        "你的感受值得被看见。",
        "我在这里，你愿意多说一些吗？",
    ],
}

UNDERSTANDING_TEMPLATES: Dict[str, List[str]] = {
    "parent_guilt": [
        "你一直在努力做一个好父母，但没有人教过你怎么做。",
        "你复制了父母的方式，不是因为你想，是因为你不知道还有别的路。",
        "你现在的愧疚，恰恰说明你和你的父母不一样——你在反思。",
        "每个父母都会犯错，重要的是你意识到了。",
        "你对自己的要求太高了，没有人能做到完美。",
        "你想要给孩子最好的，但'最好'不等于'完美'。",
    ],
    "child_behavior": [
        "孩子的行为让你困惑和疲惫，这是真实的。",
        "你看到的是行为，但行为背后有一个不知道怎么表达自己的孩子。",
        "你想要帮助孩子，但不知道从哪里开始，这种感觉很煎熬。",
        "孩子的行为不是你的失败，它是一种沟通方式。",
        "你试了很多方法都没用，这种无力感是可以理解的。",
        "每个孩子都会经历困难阶段，这不代表你教育失败。",
    ],
    "communication_break": [
        "你想靠近孩子，但每次尝试都被推开，这一定很痛。",
        "你和孩子之间好像隔了一堵墙，你在外面喊，里面听不到。",
        "沟通断裂不是一天发生的，修复也需要时间。",
        "你渴望和孩子连接，但不知道怎么打破僵局。",
        "沉默比争吵更让人难受，因为至少争吵还有回应。",
    ],
    "exhaustion": [
        "你一直在付出，但没有人在补充你的能量。",
        "你照顾了所有人，唯独忘了自己。",
        '当"我是妈妈/爸爸"变成了唯一身份，人会枯萎。',
        "你不需要做一个超人父母，你也是一个普通人。",
        "长期的付出没有回报，任何人都会感到疲惫。",
    ],
    "fear_anxiety": [
        "你害怕孩子走弯路，害怕自己没教好，害怕来不及。",
        "你的焦虑来自爱，但焦虑有时会遮住你看到孩子真正需求的眼睛。",
        "你想要保护孩子免受一切伤害，但这个世界不允许。",
        "你担心的不是现在，是孩子的未来，这说明你是一个有远见的父母。",
        "焦虑的根源是你太在乎了，但过度的在乎有时会变成压力。",
    ],
    "emotional_crisis": [
        "你现在的感受像暴风雨一样猛烈，但暴风雨会过去的。",
        "你感觉自己快要崩溃了，这种感觉是真实的。",
        "在最黑暗的时刻，你还在寻找出路，这本身就是力量。",
    ],
    "general": [
        "我能感受到你现在的处境不容易。",
        "你面对的不是一个简单的问题。",
        "你愿意说出来，说明你还在寻找出路。",
        "你的经历让我看到了你的坚韧。",
        "这不是你的错，你已经在尽力了。",
    ],
}

SUPPORT_TEMPLATES: Dict[str, List[str]] = {
    "emotional_crisis": [
        "你不需要一个人扛。我在这里。",
        "你现在的感受很重要，不需要急着'好起来'。",
        "先照顾好自己，你值得被照顾。",
        "你不需要现在就解决问题，先让自己喘口气。",
        "深呼吸，你不是一个人在面对这些。",
    ],
    "parent_guilt": [
        "犯错不等于失败。重要的是你愿意面对。",
        "你已经比你的父母多走了很多步——你在反思，这本身就是改变。",
        "给自己一些慈悲。你也是第一次当父母。",
        "你不需要为过去的错误惩罚自己。",
        "你的孩子需要的不是完美的父母，而是愿意成长的父母。",
    ],
    "child_behavior": [
        "你不需要独自面对孩子的困难行为。",
        "寻求帮助不是失败，是智慧。",
        "你和孩子都在学习，慢慢来。",
        "你比你想象的更有耐心，你已经坚持了这么久。",
    ],
    "communication_break": [
        "修复关系需要时间，不要着急。",
        "你愿意尝试修复，这本身就是第一步。",
        "有时候，安静的陪伴比千言万语更有力量。",
    ],
    "exhaustion": [
        "你需要休息，这不是奢侈，是必需。",
        "允许自己不完美，允许自己需要帮助。",
        "你不需要等到'准备好了'才开始照顾自己。",
        "你值得被好好对待，先从自己开始。",
        "给自己放个假，哪怕只有十分钟。",
    ],
    "fear_anxiety": [
        "你的担心是可以被理解的。",
        "你不需要独自承受这些恐惧。",
        "一步一步来，不要想太远。",
    ],
    "general": [
        "你不是一个人在面对这些。",
        "你的感受值得被看见。",
        "慢慢来，不着急。",
        "你已经迈出了最难的一步——开口说出来。",
        "无论你需要什么，我都在这里。",
    ],
}

EMPOWERMENT_TEMPLATES: Dict[str, List[str]] = {
    "parent_guilt": [
        "你愿意面对自己的模式，这已经是改变的开始。",
        "你不是在重复父母的路——你在开一条新的路。",
        "你的反思能力，是你给孩子最好的礼物。",
        "改变不需要完美，只需要方向对了。",
        "你已经走出了最艰难的一步——意识到问题。",
    ],
    "child_behavior": [
        "你比你想象的更有能力帮助孩子。关键是从理解开始，而不是从控制开始。",
        "你愿意寻求帮助，说明你是一个负责任的父母。",
        "改变不需要一步到位。今天的一个小尝试，就是进步。",
        "你的孩子很幸运，有你这样愿意学习的父母。",
        "每一个小的改变，都会在孩子心里留下印记。",
    ],
    "communication_break": [
        "修复关系不需要完美的语言，需要的是真诚和耐心。",
        "你愿意修复关系，这个意愿本身就是桥梁。",
        '先从一句话开始："我想理解你。"这就够了。',
        "有时候，一个拥抱比千言万语更有力量。",
        "你不需要找到完美的话语，你的真诚孩子能感受到。",
    ],
    "exhaustion": [
        "你不需要等到精力恢复才开始改变。一个小小的自我照顾，就是开始。",
        "你已经证明了自己的坚韧。现在，把这份坚韧用在照顾自己上。",
        "你值得被好好对待——先从自己开始。",
        "给自己十分钟，做一件只属于自己的事。",
        "你不是机器，你是一个值得被爱的人。",
    ],
    "fear_anxiety": [
        "你的担心来自爱，把这份爱转化为行动就好。",
        "你不需要控制一切，只需要做好今天能做的事。",
        "相信你和孩子一起面对问题的能力。",
    ],
    "emotional_crisis": [
        "你已经撑过了最难的时刻，你比你想象的更坚强。",
        "暴风雨会过去，而你会更强大。",
        "你不需要一步到位，先让自己好起来。",
    ],
    "general": [
        "你已经在路上了。愿意面对问题，本身就是力量。",
        "你有能力做出改变。一步一步来。",
        "相信自己的直觉。你比任何人都了解你的孩子。",
        "你已经证明了自己的勇气——你选择了面对。",
        "每一个小进步都值得被看见。",
    ],
}

# 有害表述黑名单
HARMFUL_PHRASES: Dict[str, str] = {
    "你应该爱孩子": "我看到你在努力，这很不容易",
    "你要理解孩子": "先照顾好你自己，才能更好地支持孩子",
    "孩子需要的是父母改变": "改变是可能的，但需要时间和支持",
    "你的原生家庭有问题": "你的经历塑造了你，但这不是你的错",
    "你的孩子有行为问题": "孩子在用行为表达他们无法用语言说的事",
    "你应该原谅父母": "接纳自己的感受比原谅更重要",
    "你需要修复创伤": "你的感受是真实的，专业的支持可以帮到你",
}


# ============================================================
# 共情陷阱检测规则
# ============================================================

TRAP_PATTERNS: Dict[EmpathyTrap, Dict] = {
    EmpathyTrap.PSEUDO_EMPATHY: {
        "patterns": [r"我理解你[。，]", r"我能体会", r"我懂你的感受"],
        "requires_followup": True,
        "suggestion": "伪共情：只说'我理解你'但没有具体内容。请加入对具体情境的描述。",
        "severity": 3,
    },
    EmpathyTrap.JUDGMENTAL: {
        "patterns": [r"你不应该", r"你不该", r"你怎么能", r"你不可以这样想"],
        "suggestion": "评判性共情：在共情中夹带了评判。去掉'应该/不该'，只描述感受。",
        "severity": 4,
    },
    EmpathyTrap.FIXING: {
        "patterns": [r"你应该这样做", r"你需要", r"你要做的就是", r"解决办法是"],
        "suggestion": "急于解决：跳过了情绪回应直接给建议。先用1-2句承接情绪，再给建议。",
        "severity": 3,
    },
    EmpathyTrap.COMPARING: {
        "patterns": [r"我比你更", r"还有人比你", r"至少你", r"比起.*算好的"],
        "suggestion": "比较式共情：用他人的痛苦来轻视对方的感受。每个人的痛苦都是真实的。",
        "severity": 4,
    },
    EmpathyTrap.MINIMIZING: {
        "patterns": [r"没那么严重", r"想太多了", r"小题大做", r"不至于", r"没什么大不了"],
        "suggestion": "轻视式共情：否定了对方感受的严重性。对方的感受就是真实的。",
        "severity": 4,
    },
    EmpathyTrap.TOXIC_POSITIVITY: {
        "patterns": [r"往好处想", r"一切都会好的", r"积极一点", r"别想太多.*开心"],
        "suggestion": "毒性正能量：强迫对方积极思考。允许消极情绪存在才是真正的共情。",
        "severity": 3,
    },
    EmpathyTrap.ADVICE_DISGUISED: {
        "patterns": [r"我觉得你应该", r"我建议你", r"你最好", r"你为什么不"],
        "suggestion": "伪装共情的建议：看起来在共情，其实在给建议。先完成情绪回应再建议。",
        "severity": 2,
    },
    EmpathyTrap.BLAME_SHIFTING: {
        "patterns": [r"你也有问题", r"你是不是也", r"你自己想想"],
        "suggestion": "转移责任：在共情中暗示对方有责任。共情阶段不分析责任归属。",
        "severity": 5,
    },
    EmpathyTrap.OVER_IDENTIFYING: {
        "patterns": [r"我完全懂", r"我和你一模一样", r"我也经历过.*完全一样"],
        "suggestion": "过度认同：声称完全理解对方经历。每个人的体验都是独特的。",
        "severity": 2,
    },
}


# ============================================================
# 核心模块
# ============================================================

class EmotionClassifier:
    """情绪分类器"""

    # 使用共享常量模块中的情绪关键词
    EMOTION_MAP: Dict[str, List[str]] = {k: list(v) for k, v in EMOTION_KEYWORDS.items()}

    def classify(self, text: str) -> EmotionInput:
        result = EmotionInput()
        scores: Dict[str, int] = {}
        for emotion, keywords in self.EMOTION_MAP.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[emotion] = score
        if not scores:
            result.primary_emotion = "default"
            result.intensity = 3.0
            return result
        sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        result.primary_emotion = sorted_emotions[0][0]
        result.secondary_emotions = [e for e, _ in sorted_emotions[1:3]]
        intensity_markers = INTENSITY_MARKERS_UP
        base = min(8.0, 4.0 + sorted_emotions[0][1] * 1.5)
        for m in intensity_markers:
            if m in text:
                base = min(10.0, base + 0.5)
        result.intensity = base
        negative = {"anger", "sadness", "anxiety", "shame", "guilt",
                    "helplessness", "exhaustion", "loneliness", "frustration"}
        if result.primary_emotion in negative:
            result.valence = -0.5
        return result


class EmpathyLevelRouter:
    """共情层次路由器 — 根据情绪强度决定共情深度"""

    def route(self, emotion: EmotionInput) -> EmpathyLevel:
        if emotion.is_crisis or emotion.intensity >= 9:
            return EmpathyLevel.ACCEPTANCE
        if emotion.intensity >= 7:
            return EmpathyLevel.UNDERSTANDING
        if emotion.intensity >= 5:
            return EmpathyLevel.SUPPORT
        return EmpathyLevel.EMPOWERMENT


class EmpathyTrapChecker:
    """共情陷阱检测器"""

    def check(self, text: str) -> List[EmpathyTrapResult]:
        results = []
        for trap_type, config in TRAP_PATTERNS.items():
            for pattern in config["patterns"]:
                match = re.search(pattern, text)
                if match:
                    result = EmpathyTrapResult(
                        has_trap=True,
                        trap_type=trap_type,
                        trap_text=match.group(),
                        suggestion=config["suggestion"],
                        severity=config["severity"],
                    )
                    results.append(result)
                    break
        return results

    def check_harmful_phrases(self, text: str) -> List[Tuple[str, str]]:
        """检测有害表述并返回替代建议"""
        found = []
        for harmful, replacement in HARMFUL_PHRASES.items():
            if harmful in text:
                found.append((harmful, replacement))
        return found


class EmpathyBalancer:
    """共情平衡器 — 确保共情与建议的比例恰当"""

    # 共情关键词
    EMPATHY_KEYWORDS = ["感受到", "听到", "理解", "不容易", "真实的",
                        "勇气", "在乎", "看见", "陪伴", "不孤单"]
    # 建议关键词
    ADVICE_KEYWORDS = ["建议", "应该", "可以试试", "方法", "步骤",
                       "策略", "技巧", "做法", "解决方案"]

    def analyze(self, text: str, emotion_intensity: float = 5.0) -> EmpathyBalance:
        """
        分析共情与建议的平衡性。

        Args:
            text: 待分析文本
            emotion_intensity: 情绪强度（1-10），默认5.0。高情绪强度要求更高共情比例。
        """
        sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if s.strip()]
        if not sentences:
            return EmpathyBalance(is_balanced=True, recommendation="内容为空")

        empathy_count = 0
        advice_count = 0
        for sent in sentences:
            is_empathy = any(kw in sent for kw in self.EMPATHY_KEYWORDS)
            is_advice = any(kw in sent for kw in self.ADVICE_KEYWORDS)
            if is_empathy:
                empathy_count += 1
            if is_advice:
                advice_count += 1

        total = empathy_count + advice_count
        if total == 0:
            return EmpathyBalance(is_balanced=True, recommendation="未检测到共情或建议关键词")

        empathy_ratio = empathy_count / total
        advice_ratio = advice_count / total

        # 平衡规则：根据情绪强度动态调整共情比例要求
        # 高情绪(>=7): 共情>=70%, 中情绪(5-7): 共情>=50%, 低情绪(<5): 共情>=40%
        if emotion_intensity >= 7:
            min_empathy = 0.7
        elif emotion_intensity >= 5:
            min_empathy = 0.5
        else:
            min_empathy = 0.4

        is_balanced = empathy_ratio >= min_empathy
        recommendation = ""
        if empathy_ratio < 0.3:
            recommendation = "共情严重不足：建议增加情绪回应，减少建议比例"
        elif empathy_ratio < min_empathy:
            if emotion_intensity >= 7:
                recommendation = "高情绪状态下共情不足：建议先充分共情，再给建议"
            else:
                recommendation = "共情偏少：建议先充分共情，再给建议"
        elif advice_ratio > 0.6:
            recommendation = "建议过多：高情绪状态下应以共情为主"

        return EmpathyBalance(
            empathy_ratio=empathy_ratio,
            advice_ratio=advice_ratio,
            is_balanced=is_balanced,
            recommendation=recommendation,
        )


class ScenarioDetector:
    """场景检测器 — 从文本推断共情场景"""

    SCENARIO_KEYWORDS: Dict[EmpathyScenario, List[str]] = {
        EmpathyScenario.EMOTIONAL_CRISIS: ["崩溃", "撑不住", "受不了", "疯了", "帮帮我", "撑不下去"],
        EmpathyScenario.PARENT_GUILT: ["我的错", "内疚", "愧疚", "不是好妈妈", "不是好爸爸",
                                        "打孩子", "吼了", "吼孩子", "后悔", "打了"],
        EmpathyScenario.CHILD_BEHAVIOR: ["不听话", "叛逆", "发脾气", "打人", "成绩", "沉迷",
                                         "怎么说都不听", "顶嘴", "反抗"],
        EmpathyScenario.COMMUNICATION_BREAK: ["不说话", "不理我", "拒绝沟通", "沉默", "锁门",
                                              "不跟我说", "不跟我"],
        EmpathyScenario.EXHAUSTION: ["累了", "倦怠", "精疲力竭", "撑不住", "没有精力",
                                     "心累", "太累了"],
        EmpathyScenario.FEAR_ANXIETY: ["害怕", "担心", "万一", "焦虑", "以后怎么办",
                                       "以后", "来不及"],
    }

    def detect(self, text: str) -> EmpathyScenario:
        scores: Dict[EmpathyScenario, int] = {}
        for scenario, keywords in self.SCENARIO_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[scenario] = score
        if not scores:
            return EmpathyScenario.GENERAL
        return max(scores, key=scores.get)


class EmpathyQualityAssessor:
    """共情质量评估器 — 多维度评估共情表达质量"""

    # 评估维度权重
    DIMENSION_WEIGHTS = {
        "specificity": 0.20,      # 具体性：是否针对具体情境
        "emotional_accuracy": 0.25,  # 情绪准确性：是否准确识别情绪
        "non_judgmental": 0.20,   # 非评判性：是否避免评判
        "warmth": 0.15,           # 温暖度：是否传递温暖
        "actionability": 0.10,    # 可操作性：是否给出可执行建议
        "balance": 0.10,          # 平衡性：共情与建议的比例
    }

    # 非评判性指标
    JUDGMENTAL_MARKERS = ["应该", "不该", "必须", "一定要", "你怎么能"]
    WARMTH_MARKERS = ["理解", "感受到", "听到", "看见", "陪伴", "不孤单", "在乎",
                      "真实", "勇气", "不容易", "重要", "权利", "努力", "在乎"]
    SPECIFICITY_MARKERS = ["你", "孩子", "你们", "这件事", "这种情况", "父母", "妈妈", "爸爸"]

    def assess(self, text: str, balance: EmpathyBalance) -> float:
        """评估共情质量，返回0-10分"""
        scores: Dict[str, float] = {}

        # 具体性：检查是否有具体指代
        specificity_count = sum(1 for m in self.SPECIFICITY_MARKERS if m in text)
        scores["specificity"] = min(10.0, 3.0 + specificity_count * 2.0)

        # 情绪准确性：检查是否包含情绪词
        emotion_words = ["愤怒", "难过", "焦虑", "害怕", "内疚", "无助", "疲惫",
                         "孤独", "挫败", "伤心", "崩溃", "痛苦", "生气", "担心",
                         "愧疚", "后悔", "累", "撑不住"]
        emotion_count = sum(1 for w in emotion_words if w in text)
        scores["emotional_accuracy"] = min(10.0, 4.0 + emotion_count * 2.0)

        # 非评判性：越少评判词越好
        judgmental_count = sum(1 for m in self.JUDGMENTAL_MARKERS if m in text)
        scores["non_judgmental"] = max(0.0, 10.0 - judgmental_count * 3.0)

        # 温暖度
        warmth_count = sum(1 for m in self.WARMTH_MARKERS if m in text)
        scores["warmth"] = min(10.0, 3.0 + warmth_count * 2.0)

        # 可操作性：检查是否有具体建议
        action_markers = ["试试", "可以", "第一步", "从", "开始"]
        action_count = sum(1 for m in action_markers if m in text)
        scores["actionability"] = min(10.0, action_count * 2.5)

        # 平衡性
        scores["balance"] = 10.0 if balance.is_balanced else 5.0

        # 加权平均
        total = sum(scores[dim] * weight
                    for dim, weight in self.DIMENSION_WEIGHTS.items())
        return round(total, 1)


# ============================================================
# 共情表达生成器
# ============================================================

class EmpathyExpressionGenerator:
    """共情表达生成器 — 组装四层共情表达"""

    # 情绪→模板索引映射：确保同一情绪类别有多个模板轮换
    EMOTION_TEMPLATE_MAP: Dict[str, int] = {
        "anger": 0,
        "sadness": 1,
        "anxiety": 2,
        "fear": 3,
        "shame": 4,
        "guilt": 5,
        "helplessness": 6,
        "exhaustion": 7,
        "loneliness": 8,
        "frustration": 9,
        "default": 10,
    }

    def __init__(self):
        self.emotion_classifier = EmotionClassifier()
        self.level_router = EmpathyLevelRouter()
        self.scenario_detector = ScenarioDetector()
        # 模板轮换计数器：记录每个类别已使用次数
        self._rotation_counter: Dict[str, int] = {}

    def _select_template(self, templates: List[str], category_key: str) -> str:
        """
        从模板列表中选择一个模板，确保轮换且不连续重复。

        Args:
            templates: 可用模板列表
            category_key: 类别标识（用于跟踪轮换状态）
        """
        if not templates:
            return ""
        count = self._rotation_counter.get(category_key, 0)
        idx = count % len(templates)
        self._rotation_counter[category_key] = count + 1
        return templates[idx]

    def _get_context_hint(self, context: Optional[Dict], emotion: EmotionInput) -> str:
        """根据上下文生成提示（如对话历史中的重复情绪）"""
        if not context:
            return ""
        conversation_history = context.get("conversation_history", [])
        if not conversation_history:
            return ""
        # 如果对话历史中出现过相同情绪，标记为"持续"
        prev_emotions = context.get("detected_emotions", [])
        if emotion.primary_emotion in prev_emotions:
            return "持续"
        return ""

    def generate(
        self,
        text: str,
        emotion: Optional[EmotionInput] = None,
        target_level: Optional[EmpathyLevel] = None,
        context: Optional[Dict] = None,
    ) -> EmpathyResult:
        """
        生成完整的共情表达。

        Args:
            text: 用户输入文本
            emotion: 可选的情绪输入（如果不提供会自动检测）
            target_level: 目标共情层次（如果不提供会自动路由）
            context: 可选的上下文信息（如 conversation_history, detected_emotions）

        Returns:
            EmpathyResult 包含四层共情表达
        """
        try:
            # Step 1: 情绪检测
            if emotion is None:
                emotion = self.emotion_classifier.classify(text)

            # Step 2: 路由到合适的共情层次
            if target_level is None:
                target_level = self.level_router.route(emotion)

            # Step 3: 场景检测
            scenario = self.scenario_detector.detect(text)

            # Step 4: 生成四层表达
            expressions = []
            techniques = []

            # Layer 1: 接纳（始终包含）
            acceptance = self._build_acceptance(emotion, context)
            expressions.append(EmpathyExpression(
                level=EmpathyLevel.ACCEPTANCE,
                text=acceptance,
                scenario=scenario,
                techniques_used=["reflection", "validation"],
            ))
            techniques.extend(["reflection", "validation"])

            # Layer 2: 理解（UNDERSTANDING 及以上）
            if target_level in (EmpathyLevel.UNDERSTANDING, EmpathyLevel.SUPPORT,
                                EmpathyLevel.EMPOWERMENT):
                understanding = self._build_understanding(scenario, emotion, context)
                expressions.append(EmpathyExpression(
                    level=EmpathyLevel.UNDERSTANDING,
                    text=understanding,
                    scenario=scenario,
                    techniques_used=["reframing", "normalization"],
                ))
                techniques.extend(["reframing", "normalization"])

            # Layer 3: 支持（SUPPORT 及以上）
            if target_level in (EmpathyLevel.SUPPORT, EmpathyLevel.EMPOWERMENT):
                support = self._build_support(scenario, emotion, context)
                expressions.append(EmpathyExpression(
                    level=EmpathyLevel.SUPPORT,
                    text=support,
                    scenario=scenario,
                    techniques_used=["validation"],
                ))
                techniques.append("validation")

            # Layer 4: 赋能（EMPOWERMENT）
            if target_level == EmpathyLevel.EMPOWERMENT:
                empowerment = self._build_empowerment(scenario, context)
                expressions.append(EmpathyExpression(
                    level=EmpathyLevel.EMPOWERMENT,
                    text=empowerment,
                    scenario=scenario,
                    techniques_used=["reframing"],
                ))
                techniques.append("reframing")

            # 组装完整回复
            full_response = "\n\n".join(e.text for e in expressions)

            # 不确定性表达：当情绪强度低或检测不确定时，添加缓和语气
            if emotion.intensity <= 3.0 and emotion.primary_emotion == "default":
                uncertainty_prefix = "我不太确定是否完全理解了你的感受，但"
                full_response = uncertainty_prefix + full_response

            # 生成追问
            follow_ups = self._generate_follow_ups(scenario, emotion)

            return EmpathyResult(
                level=target_level,
                expressions=expressions,
                full_response=full_response,
                techniques_used=list(set(techniques)),
                follow_up_questions=follow_ups,
            )
        except Exception as e:
            logger.error(f"共情表达生成失败: {e}")
            # 降级处理：返回基础接纳表达
            fallback_text = "我听到你说的了。你的感受是真实的。"
            return EmpathyResult(
                level=EmpathyLevel.ACCEPTANCE,
                expressions=[EmpathyExpression(
                    level=EmpathyLevel.ACCEPTANCE,
                    text=fallback_text,
                    scenario=EmpathyScenario.GENERAL,
                    techniques_used=["reflection"],
                )],
                full_response=fallback_text,
                techniques_used=["reflection"],
                quality_score=3.0,
            )

    def _build_acceptance(self, emotion: EmotionInput,
                           context: Optional[Dict] = None) -> str:
        """构建接纳层表达"""
        templates = ACCEPTANCE_TEMPLATES.get(
            emotion.primary_emotion, ACCEPTANCE_TEMPLATES["default"]
        )
        # 根据强度选择起始偏移，但使用轮换确保多样性
        category_key = f"acceptance_{emotion.primary_emotion}"
        context_hint = self._get_context_hint(context, emotion)
        if context_hint:
            category_key = f"{category_key}_{context_hint}"
        return self._select_template(templates, category_key)

    def _build_understanding(self, scenario: EmpathyScenario,
                              emotion: EmotionInput,
                              context: Optional[Dict] = None) -> str:
        """构建理解层表达"""
        templates = UNDERSTANDING_TEMPLATES.get(
            scenario.value, UNDERSTANDING_TEMPLATES["general"]
        )
        # 使用情绪→模板索引映射 + 轮换，确保语义相关且多样
        category_key = f"understanding_{scenario.value}_{emotion.primary_emotion}"
        context_hint = self._get_context_hint(context, emotion)
        if context_hint:
            category_key = f"{category_key}_{context_hint}"
        return self._select_template(templates, category_key)

    def _build_support(self, scenario: EmpathyScenario,
                        emotion: EmotionInput,
                        context: Optional[Dict] = None) -> str:
        """构建支持层表达"""
        templates = SUPPORT_TEMPLATES.get(
            scenario.value, SUPPORT_TEMPLATES["general"]
        )
        # 使用情绪→模板索引映射 + 轮换
        category_key = f"support_{scenario.value}_{emotion.primary_emotion}"
        context_hint = self._get_context_hint(context, emotion)
        if context_hint:
            category_key = f"{category_key}_{context_hint}"
        return self._select_template(templates, category_key)

    def _build_empowerment(self, scenario: EmpathyScenario,
                            context: Optional[Dict] = None) -> str:
        """构建赋能层表达"""
        templates = EMPOWERMENT_TEMPLATES.get(
            scenario.value, EMPOWERMENT_TEMPLATES["general"]
        )
        # 使用轮换选择，确保多样
        category_key = f"empowerment_{scenario.value}"
        return self._select_template(templates, category_key)

    def _generate_follow_ups(self, scenario: EmpathyScenario,
                              emotion: EmotionInput) -> List[str]:
        """生成追问引导"""
        follow_ups = {
            EmpathyScenario.PARENT_GUILT: [
                "你愿意说说当时发生了什么吗？",
                "你现在最想对孩子说什么？",
            ],
            EmpathyScenario.CHILD_BEHAVIOR: [
                "孩子的这种行为是从什么时候开始的？",
                "你注意到孩子在什么情况下会这样？",
            ],
            EmpathyScenario.COMMUNICATION_BREAK: [
                "你们最后一次好好聊天是什么时候？",
                "你觉得孩子最想对你说什么？",
            ],
            EmpathyScenario.EXHAUSTION: [
                "你上一次为自己做一件事是什么时候？",
                "你身边有没有可以帮忙的人？",
            ],
            EmpathyScenario.FEAR_ANXIETY: [
                "你最担心的具体是什么？",
                "这种担心是从什么时候开始的？",
            ],
        }
        return follow_ups.get(scenario, ["你愿意多说一些吗？"])


# ============================================================
# 主引擎: EmpathyGenerator
# ============================================================

class EmpathyGenerator:
    """
    共情生成器主引擎

    完整处理流程:
        1. 情绪分类 → 识别主要情绪和强度
        2. 共情层次路由 → 决定共情深度
        3. 共情陷阱检测 → 检查已有文本中的陷阱
        4. 共情平衡分析 → 确保共情/建议比例
        5. 共情表达生成 → 生成四层共情
        6. 质量回路 → 陷阱检测→自动修正→重新评估
        7. 质量评估 → 多维度打分
    """

    # 陷阱修正映射：检测到陷阱时的替代文本
    TRAP_CORRECTIONS: Dict[EmpathyTrap, List[str]] = {
        EmpathyTrap.PSEUDO_EMPATHY: [
            "我听到了你说的，这对你来说一定很不容易。",
            "我能感受到你现在的处境很艰难。",
        ],
        EmpathyTrap.JUDGMENTAL: [
            "你的感受是可以理解的。",
            "在这种情况下，有这样的反应是正常的。",
        ],
        EmpathyTrap.FIXING: [
            "你现在的感受很重要，不需要急着解决。",
            "先照顾好自己的情绪，我们再慢慢想怎么办。",
        ],
        EmpathyTrap.COMPARING: [
            "你的痛苦是真实的，不需要和任何人比较。",
            "每个人的感受都是独特的，你的也一样。",
        ],
        EmpathyTrap.MINIMIZING: [
            "你的感受是真实的，不需要被轻视。",
            "这件事对你来说很重要，我理解。",
        ],
        EmpathyTrap.TOXIC_POSITIVITY: [
            "你不需要强迫自己积极。允许自己难过。",
            "消极的情绪也是真实的，不需要被否定。",
        ],
        EmpathyTrap.ADVICE_DISGUISED: [
            "你现在的感受很重要。",
            "先让我理解你的处境。",
        ],
        EmpathyTrap.BLAME_SHIFTING: [
            "这不是任何人的错。",
            "你不需要在这个时候分析责任。",
        ],
        EmpathyTrap.OVER_IDENTIFYING: [
            "我能感受到你的处境很不容易。",
            "你的经历是独特的，我尊重这一点。",
        ],
    }

    def __init__(self):
        self.emotion_classifier = EmotionClassifier()
        self.level_router = EmpathyLevelRouter()
        self.trap_checker = EmpathyTrapChecker()
        self.balancer = EmpathyBalancer()
        self.expression_generator = EmpathyExpressionGenerator()
        self.quality_assessor = EmpathyQualityAssessor()
        self._correction_counter = 0  # 防止无限修正循环

    def _correct_traps(self, text: str, traps: List[EmpathyTrapResult]) -> str:
        """
        自动修正检测到的共情陷阱。

        Args:
            text: 原始文本
            traps: 检测到的陷阱列表

        Returns:
            修正后的文本
        """
        corrected = text
        for trap in traps:
            if trap.trap_type and trap.trap_type in self.TRAP_CORRECTIONS:
                corrections = self.TRAP_CORRECTIONS[trap.trap_type]
                # 选择一个修正文本替换陷阱文本
                correction = corrections[self._correction_counter % len(corrections)]
                self._correction_counter += 1
                # 替换陷阱文本（保守替换：只替换明确匹配的部分）
                if trap.trap_text in corrected:
                    corrected = corrected.replace(trap.trap_text, correction, 1)
        return corrected

    def generate(self, text: str, context: Optional[Dict] = None) -> EmpathyResult:
        """
        生成完整共情回应，包含质量回路。

        Args:
            text: 用户输入文本
            context: 可选上下文（如 conversation_history, detected_emotions）

        Returns:
            EmpathyResult 包含完整共情分析和表达
        """
        try:
            # Step 1: 情绪分类
            emotion = self.emotion_classifier.classify(text)

            # Step 2: 共情层次路由
            level = self.level_router.route(emotion)

            # Step 3: 生成共情表达
            result = self.expression_generator.generate(
                text=text, emotion=emotion, target_level=level, context=context
            )

            # Step 4: 质量回路 — 陷阱检测→自动修正→重新评估
            max_corrections = 2  # 最多修正2次，防止无限循环
            for attempt in range(max_corrections):
                traps = self.trap_checker.check(result.full_response)
                if not traps:
                    break  # 没有陷阱，跳出修正循环

                result.traps_detected = traps
                # 自动修正陷阱
                corrected_text = self._correct_traps(result.full_response, traps)
                if corrected_text == result.full_response:
                    break  # 无法修正，跳出

                result.full_response = corrected_text
                # 更新表达列表中的文本
                if result.expressions:
                    result.expressions[-1].text = corrected_text.split("\n\n")[-1]

            # Step 5: 平衡分析（传入情绪强度）
            balance = self.balancer.analyze(result.full_response, emotion.intensity)
            result.balance = balance

            # Step 6: 质量评估
            quality = self.quality_assessor.assess(result.full_response, balance)
            result.quality_score = quality

            return result

        except Exception as e:
            logger.error(f"共情生成失败: {e}")
            # 降级处理
            fallback_text = "我听到你说的了。你的感受是真实的。"
            return EmpathyResult(
                level=EmpathyLevel.ACCEPTANCE,
                expressions=[EmpathyExpression(
                    level=EmpathyLevel.ACCEPTANCE,
                    text=fallback_text,
                    scenario=EmpathyScenario.GENERAL,
                    techniques_used=["reflection"],
                )],
                full_response=fallback_text,
                techniques_used=["reflection"],
                quality_score=3.0,
                balance=EmpathyBalance(is_balanced=True),
            )

    def check_existing_response(self, response_text: str,
                                 emotion_intensity: float = 5.0) -> Dict:
        """
        检查已有回复的共情质量。

        Args:
            response_text: 已有的回复文本
            emotion_intensity: 情绪强度（1-10），默认5.0

        Returns:
            包含陷阱检测、平衡分析、质量评分的字典
        """
        try:
            traps = self.trap_checker.check(response_text)
            harmful = self.trap_checker.check_harmful_phrases(response_text)
            balance = self.balancer.analyze(response_text, emotion_intensity)
            quality = self.quality_assessor.assess(response_text, balance)

            return {
                "traps": traps,
                "harmful_phrases": harmful,
                "balance": balance,
                "quality_score": quality,
                "has_issues": len(traps) > 0 or len(harmful) > 0 or not balance.is_balanced,
            }
        except Exception as e:
            logger.error(f"共情质量检查失败: {e}")
            return {
                "traps": [],
                "harmful_phrases": [],
                "balance": EmpathyBalance(is_balanced=True),
                "quality_score": 0.0,
                "has_issues": True,
            }

    def get_empathy_level_for_intensity(self, intensity: float) -> EmpathyLevel:
        """根据情绪强度获取推荐的共情层次"""
        emotion = EmotionInput(intensity=intensity)
        return self.level_router.route(emotion)


# ============================================================
# CLI 入口
# ============================================================

def main():
    """CLI 入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 empathy_generator.py <文本>")
        print("      python3 empathy_generator.py --check <已有回复文本>")
        print("      python3 empathy_generator.py --test")
        sys.exit(1)

    gen = EmpathyGenerator()

    if sys.argv[1] == "--test":
        run_tests()
        return

    if sys.argv[1] == "--check":
        text = " ".join(sys.argv[2:])
        result = gen.check_existing_response(text)
        print(f"\n=== 共情质量检查 ===")
        print(f"质量评分: {result['quality_score']}/10")
        print(f"共情占比: {result['balance'].empathy_ratio:.1%}")
        print(f"建议占比: {result['balance'].advice_ratio:.1%}")
        print(f"是否平衡: {'✅' if result['balance'].is_balanced else '❌'}")
        if result['balance'].recommendation:
            print(f"建议: {result['balance'].recommendation}")
        if result['traps']:
            print(f"\n⚠️ 检测到 {len(result['traps'])} 个共情陷阱:")
            for t in result['traps']:
                print(f"  - [{t.trap_type.value}] {t.suggestion}")
        if result['harmful_phrases']:
            print(f"\n🚫 检测到有害表述:")
            for harmful, replacement in result['harmful_phrases']:
                print(f"  - '{harmful}' → '{replacement}'")
        return

    text = " ".join(sys.argv[1:])
    result = gen.generate(text)

    print(f"\n=== 共情生成结果 ===")
    print(f"情绪: {gen.emotion_classifier.classify(text).primary_emotion}")
    print(f"强度: {gen.emotion_classifier.classify(text).intensity}/10")
    print(f"共情层次: {result.level.value}")
    print(f"质量评分: {result.quality_score}/10")
    print(f"\n--- 共情表达 ---")
    print(result.full_response)
    if result.follow_up_questions:
        print(f"\n--- 追问引导 ---")
        for q in result.follow_up_questions:
            print(f"  • {q}")
    if result.traps_detected:
        print(f"\n⚠️ 陷阱检测: {len(result.traps_detected)} 个")


def run_tests():
    """运行内置测试"""
    gen = EmpathyGenerator()
    test_cases = [
        ("我今天吼了孩子，我不是个好妈妈", "guilt", "high"),
        ("孩子成绩下降了，我好焦虑", "anxiety", "medium"),
        ("我真的撑不住了，太累了", "exhaustion", "high"),
        ("孩子不跟我说话，我不知道怎么办", "helplessness", "medium"),
        ("我打了孩子，很后悔", "guilt", "high"),
        ("孩子沉迷游戏，怎么说都不听", "frustration", "medium"),
        ("我害怕孩子以后过得不好", "anxiety", "medium"),
        ("没人理解我，我好孤独", "loneliness", "high"),
    ]

    print("\n=== 共情生成器测试 ===\n")
    total_score = 0
    passed = 0

    for text, expected_emotion, expected_intensity in test_cases:
        result = gen.generate(text)
        emotion = gen.emotion_classifier.classify(text)
        score = result.quality_score
        total_score += score

        status = "✅" if score >= 6.0 else "⚠️"
        if score >= 6.0:
            passed += 1

        print(f"{status} [{expected_emotion}] \"{text[:30]}...\"")
        print(f"   检测情绪: {emotion.primary_emotion} | 强度: {emotion.intensity:.1f}")
        print(f"   共情层次: {result.level.value} | 质量: {score}/10")
        print(f"   陷阱: {len(result.traps_detected)} | 平衡: {'✅' if result.balance.is_balanced else '❌'}")
        print(f"   回复: {result.full_response[:80]}...")
        print()

    avg_score = total_score / len(test_cases)
    print(f"=== 测试结果 ===")
    print(f"通过: {passed}/{len(test_cases)}")
    print(f"平均共情分: {avg_score:.1f}/10")

    # 陷阱检测测试
    print(f"\n=== 陷阱检测测试 ===")
    trap_tests = [
        ("我理解你。", True, "pseudo_empathy"),
        ("你不应该这样想。", True, "judgmental"),
        ("你应该这样做：第一步...", True, "fixing"),
        ("至少你还有孩子，比那些没孩子的好。", True, "comparing"),
        ("没那么严重，想太多了。", True, "minimizing"),
        ("往好处想，一切都会好的。", True, "toxic_positivity"),
        ("我听到你的愤怒了，这种感受是真实的。", False, None),
    ]

    trap_passed = 0
    for text, should_have_trap, expected_type in trap_tests:
        traps = gen.trap_checker.check(text)
        has_trap = len(traps) > 0
        detected_type = traps[0].trap_type.value if traps else None

        ok = has_trap == should_have_trap
        if should_have_trap and expected_type:
            ok = ok and detected_type == expected_type
        if ok:
            trap_passed += 1

        status = "✅" if ok else "❌"
        print(f"{status} \"{text[:40]}\" → 陷阱: {detected_type or '无'}")

    print(f"\n陷阱检测通过: {trap_passed}/{len(trap_tests)}")


if __name__ == "__main__":
    main()

