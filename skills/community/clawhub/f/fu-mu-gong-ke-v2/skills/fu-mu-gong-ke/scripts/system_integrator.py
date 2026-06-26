#!/usr/bin/env python3
"""
System Integrator v2.1.0 — 育儿心理学技能全栈集成模块
Pipeline: UserInput -> SafetyGate -> UserIdentifier -> EmotionAssessor
    -> ScenarioMatcher -> DefenseDetector -> ResponseGenerator -> QualityChecker

核心哲学：
1. 没有评判的接纳 — 看到"你受苦了"，不是"你有问题"
2. 没有负罪感的许可 — 坦然地说"你可以暂停"
3. 陪伴而非拯救 — "事情发生了，我和你一起面对"
4. 规则归规则，支持归支持
"""

import json
import sys
import time
import traceback
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
VERSION = "2.0.3"

# 从共享常量模块导入
try:
    from constants import (
        DIRECT_CRISIS_KEYWORDS, METAPHOR_KEYWORDS, IMMINENT_SIGNALS,
        PARENT_SIGNALS, CHILD_SIGNALS, INTERMEDIARY_SIGNALS,
        SCENARIO_INDEX, CRISIS_HOTLINES,
        EMOTION_KEYWORDS, INTENSITY_MARKERS_UP, INTENSITY_MARKERS_DOWN,
        POSITIVE_EMOTION_WORDS, NEGATIVE_EMOTION_WORDS,
    )
except ImportError:
    # 回退: 本地定义（向后兼容）
    DIRECT_CRISIS_KEYWORDS = ["不想活","想死","死了算了","自杀","遗书","解脱","活着没意思","活不下去","结束生命","割腕","划手腕","自残","自伤"]
    METAPHOR_KEYWORDS = ["累了真的累了","撑不下去了","一切都无所谓了","没有人在乎","消失就好了"]
    IMMINENT_SIGNALS = ["正在","现在就要","马上就","已经准备好了","已经割了","已经吃了","正在割","正在打","此时此刻","就在现在"]
    PARENT_SIGNALS = ["我的孩子","我儿子","我女儿","我家孩子","娃","宝宝","我打了孩子","打了孩子","打了他","打了她"]
    CHILD_SIGNALS = ["我爸","我妈","我父母","父亲","母亲","小时候"]
    INTERMEDIARY_SIGNALS = ["我朋友","我姐的孩子","我弟","我妹的孩子","亲戚","同事的孩子"]
    SCENARIO_INDEX = {
        "01": {"name": "孩子成绩下降", "keywords": ["成绩","分数","考试","退步","考差"]},
        "02": {"name": "孩子不想上学", "keywords": ["不上学","逃学","厌学","不想去学校"]},
        "03": {"name": "孩子说我不想活了", "keywords": ["不想活","想死","自杀"]},
        "05": {"name": "孩子打人发脾气", "keywords": ["打人","发脾气","踢人","咬人"]},
        "07": {"name": "父母自己情绪崩溃", "keywords": ["情绪崩溃","控制不住","我发火了","我打了孩子"]},
        "10": {"name": "孩子沉迷手机", "keywords": ["手机","游戏","沉迷","短视频"]},
        "11": {"name": "孩子被欺负霸凌", "keywords": ["欺负","霸凌","被打了","被孤立"]},
        "17": {"name": "青春期孩子锁门", "keywords": ["锁门","不说话","拒绝沟通","不理我"]},
        "18": {"name": "孩子早恋", "keywords": ["早恋","恋爱","喜欢同"]},
        "27": {"name": "父母焦虑投射", "keywords": ["投射","我的焦虑","我太紧张"]},
        "37": {"name": "育儿倦怠", "keywords": ["倦怠","撑不住","太累了"]},
        "42": {"name": "孩子自伤", "keywords": ["自伤","割臂","划手腕"]},
        "43": {"name": "心理控制", "keywords": ["为你好","控制","不允许"]},
        "66": {"name": "父母打孩子", "keywords": ["打了孩子","打孩子","体罚"]},
        "70": {"name": "父母复制创伤", "keywords": ["复制","像我爸妈","原生家庭","代际"]},
    }
    CRISIS_HOTLINES = ["全国24小时心理援助热线：400-161-9995","北京心理危机研究与干预中心：010-82951332","生命热线：400-821-1215","希望24热线：400-161-9995","青少年心理热线：12355","报警电话：110","急救电话：120"]
    EMOTION_KEYWORDS = {}
    INTENSITY_MARKERS_UP = ["非常","特别","极其","太","超级","无比","暴","死","炸","疯"]
    INTENSITY_MARKERS_DOWN = ["有点","稍微","略微","一点点","一些","有些","不太","不怎么","还行"]
    POSITIVE_EMOTION_WORDS = {"开心","快乐","幸福","兴奋","满足","爱","喜欢","高兴","愉快","欣慰","温暖","感动","自豪","轻松"}
    NEGATIVE_EMOTION_WORDS = {"生气","愤怒","伤心","难过","焦虑","恐惧","绝望","崩溃","无助","委屈","压抑","沉重","紧张","害怕","担忧"}


class PipelineConfig:
    """集中管理管道配置"""
    STAGE_WEIGHTS = {0: 2.0, 1: 1.0, 2: 1.5, 3: 1.0, 4: 1.0, 5: 2.0, 6: 1.5}
    QUALITY_PASS_THRESHOLD = 6.0
    EMOTION_30SEC_THRESHOLD = 8.0
    DEFENSE_INJECT_THRESHOLD = 0.7
    MAX_PERF_METRICS = 1000
    MAX_STATE_HISTORY = 100


class PipelineStage(IntEnum):
    SAFETY_GATE = 0
    USER_IDENTIFY = 1
    EMOTION_ASSESS = 2
    SCENARIO_MATCH = 3
    DEFENSE_DETECT = 4
    RESPONSE_GENERATE = 5
    QUALITY_CHECK = 6


class StageStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    SKIPPED = "skipped"
    DEGRADED = "degraded"
    FAILED = "failed"


class IntegrationMode(Enum):
    FULL = "full"
    FAST = "fast"
    SAFETY_ONLY = "safety_only"
    DIAGNOSTIC = "diagnostic"


@dataclass
class StageResult:
    stage: PipelineStage
    status: StageStatus = StageStatus.PENDING
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: float = 0.0
    confidence: float = 0.0


@dataclass
class PipelineContext:
    user_input: str = ""
    session_id: str = ""
    timestamp: str = ""
    safety_result: Optional[Dict] = None
    user_identity: Optional[Dict] = None
    emotion_state: Optional[Dict] = None
    scenario_match: Optional[Dict] = None
    defense_signals: Optional[Dict] = None
    response: Optional[Dict] = None
    quality_check: Optional[Dict] = None
    conversation_history: List[Dict] = field(default_factory=list)
    stage_results: Dict[str, StageResult] = field(default_factory=dict)
    pipeline_mode: IntegrationMode = IntegrationMode.FULL
    total_duration_ms: float = 0.0
    errors: List[Dict] = field(default_factory=list)
    flow_issues: List[Tuple] = field(default_factory=list)
    transforms_applied: List[str] = field(default_factory=list)

    def add_error(self, severity, stage, message):
        self.errors.append({
            "severity": severity, "stage": stage,
            "message": message, "timestamp": datetime.now().isoformat(),
        })

    def get_upstream_data(self, stage):
        upstream = {}
        if stage.value >= 0 and self.safety_result:
            upstream["safety"] = self.safety_result
        if stage.value >= 1 and self.user_identity:
            upstream["identity"] = self.user_identity
        if stage.value >= 2 and self.emotion_state:
            upstream["emotion"] = self.emotion_state
        if stage.value >= 3 and self.scenario_match:
            upstream["scenario"] = self.scenario_match
        if stage.value >= 4 and self.defense_signals:
            upstream["defense"] = self.defense_signals
        return upstream


@dataclass
class ConversationState:
    session_id: str = ""
    turn_count: int = 0
    current_topic: str = ""
    current_emotion: str = ""
    current_crisis_level: str = "none"
    user_role: str = "unknown"
    defense_pattern: List[str] = field(default_factory=list)
    emotion_trajectory: List[float] = field(default_factory=list)
    topic_history: List[str] = field(default_factory=list)
    last_updated: str = ""
    max_history: int = 50

    def update(self, context):
        try:
            self.turn_count += 1
            self.last_updated = datetime.now().isoformat()
            if context.safety_result:
                self.current_crisis_level = context.safety_result.get("level", "none")
            if context.user_identity:
                self.user_role = context.user_identity.get("role", "unknown")
            if context.emotion_state:
                self.current_emotion = context.emotion_state.get("primary_emotion", "neutral")
                score = context.emotion_state.get("score", 5.0)
                self.emotion_trajectory.append(score)
                if len(self.emotion_trajectory) > self.max_history:
                    self.emotion_trajectory = self.emotion_trajectory[-self.max_history:]
            if context.scenario_match:
                topic = context.scenario_match.get("matched_scenario", "")
                if topic:
                    self.current_topic = topic
                    self.topic_history.append(topic)
                if len(self.topic_history) > self.max_history:
                    self.topic_history = self.topic_history[-self.max_history:]
            if context.defense_signals:
                defense = context.defense_signals.get("primary_defense", "none")
                self.defense_pattern.append(defense)
                if len(self.defense_pattern) > self.max_history:
                    self.defense_pattern = self.defense_pattern[-self.max_history:]
        except Exception as error:
            context.add_error("WARNING", "STATE_UPDATE", str(error))

    def to_dict(self):
        return {
            "session_id": self.session_id, "turn_count": self.turn_count,
            "current_topic": self.current_topic, "current_emotion": self.current_emotion,
            "current_crisis_level": self.current_crisis_level, "user_role": self.user_role,
            "defense_pattern": self.defense_pattern[-5:],
            "emotion_trajectory": self.emotion_trajectory[-10:],
            "topic_history": self.topic_history[-5:], "last_updated": self.last_updated,
        }

    def save(self, path=None):
        save_path = path or (DATA_DIR / f"state_{self.session_id}.json")
        try:
            with open(save_path, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(self.to_dict(), ensure_ascii=False, indent=2))
        except Exception as error:
            print(f"[ConversationState] save error: {error}", file=sys.stderr)

    @classmethod
    def load(cls, session_id, path=None):
        load_path = path or (DATA_DIR / f"state_{session_id}.json")
        if not Path(load_path).exists():
            return cls(session_id=session_id)
        try:
            with open(load_path, "r", encoding="utf-8") as fh:
                data = json.loads(fh.read())
            state = cls(session_id=session_id)
            state.turn_count = data.get("turn_count", 0)
            state.current_topic = data.get("current_topic", "")
            state.current_emotion = data.get("current_emotion", "")
            state.current_crisis_level = data.get("current_crisis_level", "none")
            state.user_role = data.get("user_role", "unknown")
            state.defense_pattern = data.get("defense_pattern", [])
            state.emotion_trajectory = data.get("emotion_trajectory", [])
            state.topic_history = data.get("topic_history", [])
            state.last_updated = data.get("last_updated", "")
            return state
        except Exception as error:
            print(f"[ConversationState] load error: {error}", file=sys.stderr)
            return cls(session_id=session_id)

    def reset(self):
        self.turn_count = 0
        self.current_topic = ""
        self.current_emotion = ""
        self.current_crisis_level = "none"
        self.user_role = "unknown"
        self.defense_pattern = []
        self.emotion_trajectory = []
        self.topic_history = []
        self.last_updated = datetime.now().isoformat()


@dataclass
class IntegrationReport:
    success: bool = False
    context: Optional[PipelineContext] = None
    state: Optional[ConversationState] = None
    stage_summary: Dict[str, Dict] = field(default_factory=dict)
    errors: List[Dict] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    total_duration_ms: float = 0.0
    integration_score: float = 0.0
    performance: Optional[Dict] = None
    transforms_applied: List[str] = field(default_factory=list)

    def to_dict(self):
        result = {
            "success": self.success, "stage_summary": self.stage_summary,
            "errors": self.errors, "warnings": self.warnings,
            "total_duration_ms": self.total_duration_ms,
            "integration_score": self.integration_score,
        }
        if self.performance:
            result["performance"] = self.performance
        if self.transforms_applied:
            result["transforms_applied"] = self.transforms_applied
        return result


class ModuleRegistry:
    def __init__(self):
        self._modules = {}
        self._routes = {}

    def register(self, name, module_fn, stages, priority=0,
                 required=True, fallback=None, timeout_ms=5000.0):
        self._modules[name] = {
            "fn": module_fn, "stages": stages, "priority": priority,
            "required": required, "fallback": fallback, "timeout_ms": timeout_ms,
        }
        for stage in stages:
            stage_name = stage.name
            if stage_name not in self._routes:
                self._routes[stage_name] = []
            self._routes[stage_name].append(name)
            self._routes[stage_name].sort(
                key=lambda n: self._modules[n]["priority"], reverse=True)

    def get_modules_for_stage(self, stage):
        return self._routes.get(stage.name, [])

    def get_module(self, name):
        return self._modules.get(name)

    def list_modules(self):
        return list(self._modules.keys())

    def get_highest_priority(self, stage):
        modules = self.get_modules_for_stage(stage)
        return modules[0] if modules else None


# === Stage Modules ===

class SafetyGate:
    """安全门 — 危机检测（第一道防线）"""
    KEYWORDS = DIRECT_CRISIS_KEYWORDS
    METAPHORS = METAPHOR_KEYWORDS

    @staticmethod
    def execute(context):
        try:
            text = context.user_input.lower()
            matched_keywords = [kw for kw in SafetyGate.KEYWORDS if kw in text]
            matched_metaphors = [mt for mt in SafetyGate.METAPHORS if mt in text]
            if matched_keywords:
                level = "imminent" if any(k in text for k in ["自杀", "想死", "遗书"]) else "direct"
                return {"level": level, "matched_keywords": matched_keywords,
                        "matched_metaphors": matched_metaphors, "is_crisis": True,
                        "confidence": 0.95, "action": "immediate_intervention"}
            if matched_metaphors:
                return {"level": "metaphor", "matched_keywords": [],
                        "matched_metaphors": matched_metaphors, "is_crisis": True,
                        "confidence": 0.7, "action": "cautious_inquiry"}
            return {"level": "none", "matched_keywords": [], "matched_metaphors": [],
                    "is_crisis": False, "confidence": 0.9, "action": "continue_pipeline"}
        except Exception as error:
            return {"level": "none", "matched_keywords": [], "matched_metaphors": [],
                    "is_crisis": False, "confidence": 0.0, "action": "continue_pipeline",
                    "error": str(error)}


class UserIdentifier:
    """用户身份识别"""
    PARENT_SIGNALS = PARENT_SIGNALS
    CHILD_SIGNALS = CHILD_SIGNALS
    INTERMEDIARY_SIGNALS = INTERMEDIARY_SIGNALS

    @staticmethod
    def execute(context):
        try:
            text = context.user_input
            scores = {
                "parent": sum(1 for s in UserIdentifier.PARENT_SIGNALS if s in text),
                "child": sum(1 for s in UserIdentifier.CHILD_SIGNALS if s in text),
                "intermediary": sum(1 for s in UserIdentifier.INTERMEDIARY_SIGNALS if s in text),
            }
            best_role = max(scores, key=scores.get)
            if scores[best_role] == 0:
                return {"role": "unknown", "confidence": 0.0, "signals": [], "needs_confirm": True}
            total = sum(scores.values())
            confidence = scores[best_role] / total if total else 0.0
            signal_map = {
                "parent": UserIdentifier.PARENT_SIGNALS,
                "child": UserIdentifier.CHILD_SIGNALS,
                "intermediary": UserIdentifier.INTERMEDIARY_SIGNALS,
            }
            matched = [s for s in signal_map[best_role] if s in text]
            return {"role": best_role, "confidence": confidence,
                    "signals": matched, "needs_confirm": confidence < 0.6}
        except Exception as error:
            return {"role": "unknown", "confidence": 0.0, "signals": [],
                    "needs_confirm": True, "error": str(error)}


class EmotionAssessor:
    """情绪评估器"""
    # 使用共享常量构建情绪评估映射
    _base_emotions = {}
    if EMOTION_KEYWORDS:
        _emotion_base_scores = {
            "anger": 8.0, "sadness": 7.0, "anxiety": 7.5, "guilt": 6.5,
            "exhaustion": 7.0, "helplessness": 7.0, "love": 3.0,
        }
        for emo, kws in EMOTION_KEYWORDS.items():
            if emo in _emotion_base_scores:
                _base_emotions[emo] = (list(kws), _emotion_base_scores[emo])
    EMOTIONS = _base_emotions or {
        "anger": (["气死", "愤怒", "火大", "暴怒", "发火", "吼了", "打了", "骂了"], 8.0),
        "sadness": (["难过", "伤心", "心碎", "哭", "悲伤", "心疼"], 7.0),
        "anxiety": (["焦虑", "担心", "害怕", "恐惧", "紧张", "不安"], 7.5),
        "guilt": (["内疚", "愧疚", "后悔", "自责", "我的错", "都是我"], 6.5),
        "exhaustion": (["累", "撑不住", "崩溃", "疲惫", "倦怠", "没力气"], 7.0),
        "helplessness": (["无助", "不知道怎么办", "没办法", "没希望", "绝望"], 7.0),
        "love": (["爱", "关心", "心疼", "在乎", "保护"], 3.0),
    }
    DOWN_MODIFIERS = INTENSITY_MARKERS_DOWN
    UP_MODIFIERS = INTENSITY_MARKERS_UP

    @staticmethod
    def execute(context):
        try:
            text = context.user_input
            detected = {}
            for emotion, (keywords, base_score) in EmotionAssessor.EMOTIONS.items():
                matches = [kw for kw in keywords if kw in text]
                if matches:
                    detected[emotion] = {"matches": matches, "base_score": base_score}
            if not detected:
                return {"primary_emotion": "neutral", "score": 3.0, "all_emotions": {},
                        "intensity": "low", "response_depth": "2min"}
            primary = max(detected, key=lambda e: detected[e]["base_score"] * len(detected[e]["matches"]))
            raw_score = detected[primary]["base_score"] + len(detected[primary]["matches"]) * 0.5
            has_down = any(mod in text for mod in EmotionAssessor.DOWN_MODIFIERS)
            has_up = any(mod in text for mod in EmotionAssessor.UP_MODIFIERS)
            if has_down and not has_up:
                raw_score *= 0.5
            elif has_up:
                raw_score = min(10.0, raw_score * 1.3)
            score = min(10.0, max(1.0, raw_score))
            intensity = "high" if score >= 7.5 else "medium" if score >= 5.0 else "low"
            depth = "30sec" if score >= 8.0 else "2min" if score >= 5.0 else "deep"
            return {"primary_emotion": primary, "score": score, "all_emotions": detected,
                    "intensity": intensity, "response_depth": depth}
        except Exception as error:
            return {"primary_emotion": "neutral", "score": 3.0, "all_emotions": {},
                    "intensity": "low", "response_depth": "2min", "error": str(error)}


class ScenarioMatcher:
    """场景匹配器"""
    # 从共享常量构建场景映射（保持向后兼容的键格式）
    SCENARIOS = {
        f"{sid}-{info['name']}": info["keywords"]
        for sid, info in SCENARIO_INDEX.items()
    }

    @staticmethod
    def execute(context):
        try:
            text = context.user_input
            matches = {}
            for scenario, keywords in ScenarioMatcher.SCENARIOS.items():
                score = sum(1 for kw in keywords if kw in text)
                if score > 0:
                    matches[scenario] = score
            if not matches:
                return {"matched_scenario": "", "confidence": 0.0,
                        "all_matches": {}, "fallback": "generic_analysis"}
            best = max(matches, key=matches.get)
            return {"matched_scenario": best, "confidence": min(1.0, matches[best] / 3.0),
                    "all_matches": matches, "fallback": None}
        except Exception as error:
            return {"matched_scenario": "", "confidence": 0.0,
                    "all_matches": {}, "fallback": "generic_analysis", "error": str(error)}


class DefenseDetector:
    """防御机制检测器"""
    DEFENSE_PATTERNS = {
        "shame": (["丢人", "没面子", "别人怎么看", "失败的父母", "不是好妈妈"], 1.2),
        "anxiety": (["以后怎么办", "未来", "前途", "来不及"], 1.0),
        "control": (["必须", "应该", "听话", "服从", "我说了算", "不允许"], 1.0),
        "projection": (["像我小时候", "是我的影子", "复制", "跟我一样"], 1.1),
        "denial": (["没有问题", "挺好的", "没事", "不至于"], 0.8),
        "guilt": (["都是我的错", "我不是好", "害了孩子", "我毁了"], 1.0),
    }

    @staticmethod
    def execute(context):
        try:
            text = context.user_input
            detected = {}
            for defense, (keywords, weight) in DefenseDetector.DEFENSE_PATTERNS.items():
                matches = [kw for kw in keywords if kw in text]
                if matches:
                    detected[defense] = {"matches": matches, "weight": weight,
                                         "score": len(matches) * weight}
            if not detected:
                return {"primary_defense": "none", "all_defenses": {},
                        "confidence": 0.0, "guidance_needed": False}
            primary = max(detected, key=lambda d: detected[d]["score"])
            return {"primary_defense": primary, "all_defenses": detected,
                    "confidence": min(1.0, detected[primary]["score"] / 3.0),
                    "guidance_needed": True}
        except Exception as error:
            return {"primary_defense": "none", "all_defenses": {},
                    "confidence": 0.0, "guidance_needed": False, "error": str(error)}


class ResponseGenerator:
    """响应生成器"""
    CRISIS_HOTLINES = [
        "全国24小时心理援助热线：400-161-9995",
        "北京心理危机研究与干预中心：010-82951332",
        "生命热线：400-821-1215",
    ]
    EMPATHY_TEMPLATES = {
        "anxiety": "我能感受到你内心的焦虑和不安。",
        "sadness": "你的难过我能理解，这种感受是真实的。",
        "anger": "你的情绪是被理解的，愤怒背后往往是深深的在乎。",
        "guilt": "你愿意反思自己，这本身就说明你是一位有责任心的家长。",
        "exhaustion": "你已经很累了，照顾好自己才能更好地照顾孩子。",
        "helplessness": "感到无助是正常的，我们一起来想想办法。",
        "neutral": "感谢你的信任，愿意分享这些。",
    }
    ACTION_TEMPLATES = {
        "01-成绩下降": "试试今天回家后先不问成绩，而是问孩子今天有什么开心的事。",
        "02-不想上学": "找个轻松的时间，和孩子聊聊学校里发生了什么。",
        "66-打孩子": "下次情绪上头时，先离开现场深呼吸10秒。",
        "10-沉迷手机": "和孩子一起制定一个双方都认可的手机使用规则。",
    }

    @staticmethod
    def execute(context):
        try:
            safety = context.safety_result or {}
            identity = context.user_identity or {}
            emotion = context.emotion_state or {}
            scenario = context.scenario_match or {}
            defense = context.defense_signals or {}

            # Crisis response
            if safety.get("is_crisis", False):
                return {
                    "type": "crisis",
                    "empathy": "我听到你说的了，你现在不是一个人。",
                    "action": "请立即拨打以下热线寻求专业帮助：",
                    "guidance": "",
                    "hotlines": ResponseGenerator.CRISIS_HOTLINES,
                    "role": identity.get("role", "unknown"),
                }

            # Normal response
            primary_emotion = emotion.get("primary_emotion", "neutral")
            role = identity.get("role", "unknown")
            matched_scenario = scenario.get("matched_scenario", "")
            primary_defense = defense.get("primary_defense", "none")

            empathy = ResponseGenerator.EMPATHY_TEMPLATES.get(
                primary_emotion, ResponseGenerator.EMPATHY_TEMPLATES["neutral"])
            action = ResponseGenerator.ACTION_TEMPLATES.get(
                matched_scenario, "试着在今天找一个安静的时刻，和孩子聊聊天。")

            # Defense-specific guidance
            guidance = ""
            if primary_defense == "control":
                guidance = "当我们在意孩子的未来时，很容易不自觉地想要控制。试着把「你必须」换成「我建议」。"
            elif primary_defense == "projection":
                guidance = "有时候我们看到的孩子的问题，其实是自己内心未解决的课题。"
            elif primary_defense == "shame":
                guidance = "育儿没有完美，每个家长都在学习中成长。"
            elif primary_defense == "guilt":
                guidance = "内疚说明你在乎，但过度自责并不能帮助孩子。把精力放在下一步该怎么做。"

            result = {
                "type": "normal",
                "empathy": empathy,
                "action": action,
                "guidance": guidance,
                "hotlines": [],
                "role": role,
            }
            return result
        except Exception as error:
            return {
                "type": "normal",
                "empathy": "感谢你的分享。",
                "action": "",
                "guidance": "",
                "hotlines": [],
                "role": "unknown",
                "error": str(error),
            }


class QualityChecker:
    """质量检查器"""
    HARMFUL_PATTERNS = [
        "你应该打", "打得好", "孩子就该打", "不打不成器",
        "你真没用", "你不配当", "活该", "你应该",
    ]

    @staticmethod
    def execute(context):
        try:
            response = context.response or {}
            safety = context.safety_result or {}
            issues = []
            score = 10.0

            # Check empathy
            empathy = response.get("empathy", "")
            if not empathy:
                issues.append("缺少共情内容")
                score -= 3.0

            # Check harmful language
            combined_text = " ".join([
                response.get("empathy", ""),
                response.get("action", ""),
                response.get("guidance", ""),
            ])
            for pattern in QualityChecker.HARMFUL_PATTERNS:
                if pattern in combined_text:
                    issues.append(f"包含有害语言: {pattern}")
                    score -= 4.0
                    break

            # Check crisis response has hotlines
            if safety.get("is_crisis", False):
                hotlines = response.get("hotlines", [])
                if not hotlines:
                    issues.append("危机响应缺少热线信息")
                    score -= 5.0

            # Check action exists for normal responses
            if response.get("type") == "normal":
                if not response.get("action", ""):
                    issues.append("缺少行动建议")
                    score -= 1.0

            score = max(0.0, min(10.0, score))
            passed = score >= PipelineConfig.QUALITY_PASS_THRESHOLD
            return {"passed": passed, "score": score, "issues": issues}
        except Exception as error:
            return {"passed": False, "score": 0.0, "issues": [f"质量检查异常: {error}"]}


# === Data Flow Rules ===

class DataFlowRules:
    """数据流规则 — 验证阶段间数据依赖和转换"""
    DEPENDENCY_GRAPH = {
        PipelineStage.SAFETY_GATE: [],
        PipelineStage.USER_IDENTIFY: [PipelineStage.SAFETY_GATE],
        PipelineStage.EMOTION_ASSESS: [PipelineStage.SAFETY_GATE, PipelineStage.USER_IDENTIFY],
        PipelineStage.SCENARIO_MATCH: [PipelineStage.SAFETY_GATE, PipelineStage.USER_IDENTIFY,
                                        PipelineStage.EMOTION_ASSESS],
        PipelineStage.DEFENSE_DETECT: [PipelineStage.SAFETY_GATE, PipelineStage.USER_IDENTIFY,
                                        PipelineStage.EMOTION_ASSESS, PipelineStage.SCENARIO_MATCH],
        PipelineStage.RESPONSE_GENERATE: [PipelineStage.SAFETY_GATE, PipelineStage.USER_IDENTIFY,
                                           PipelineStage.EMOTION_ASSESS, PipelineStage.SCENARIO_MATCH,
                                           PipelineStage.DEFENSE_DETECT],
        PipelineStage.QUALITY_CHECK: [PipelineStage.SAFETY_GATE, PipelineStage.RESPONSE_GENERATE],
    }

    REQUIRED_FIELDS = {
        PipelineStage.SAFETY_GATE: [],
        PipelineStage.USER_IDENTIFY: ["safety_result"],
        PipelineStage.EMOTION_ASSESS: ["safety_result"],
        PipelineStage.SCENARIO_MATCH: ["safety_result", "emotion_state"],
        PipelineStage.DEFENSE_DETECT: ["safety_result", "emotion_state"],
        PipelineStage.RESPONSE_GENERATE: ["safety_result", "emotion_state"],
        PipelineStage.QUALITY_CHECK: ["safety_result", "response"],
    }

    TRANSFORMS = {
        "crisis_override": "If crisis detected, short-circuit to response generation",
        "emotion_depth_mapping": "Map emotion score to response depth",
        "defense_guidance_injection": "Inject defense-specific guidance into response",
    }

    @staticmethod
    def get_upstream_for(stage):
        """获取指定阶段的所有上游依赖阶段"""
        return DataFlowRules.DEPENDENCY_GRAPH.get(stage, [])

    @staticmethod
    def validate_flow(context):
        """验证当前上下文的数据流完整性（基础三字段检查）"""
        issues = []
        if context.safety_result is None:
            issues.append(("safety_result", "missing"))
        if context.user_identity is None:
            issues.append(("user_identity", "missing"))
        if context.emotion_state is None:
            issues.append(("emotion_state", "missing"))
        return issues

    @staticmethod
    def apply_transforms(context):
        """应用数据流转换规则"""
        applied = []
        try:
            # Crisis override: short-circuit if crisis
            if context.safety_result and context.safety_result.get("is_crisis", False):
                applied.append("crisis_override")

            # Emotion depth mapping
            if context.emotion_state:
                score = context.emotion_state.get("score", 5.0)
                if score >= PipelineConfig.EMOTION_30SEC_THRESHOLD:
                    context.emotion_state["response_depth"] = "30sec"
                    applied.append("emotion_depth_mapping")

            # Defense guidance injection
            if context.defense_signals:
                primary = context.defense_signals.get("primary_defense", "none")
                if primary != "none":
                    applied.append("defense_guidance_injection")

            context.transforms_applied = applied
        except Exception as error:
            context.add_error("WARNING", "TRANSFORM", str(error))
        return applied


# === State Manager ===

class StateManager:
    """状态管理器 — 管理多轮对话状态"""

    def __init__(self, session_id):
        self.session_id = session_id
        self.conversation_state = ConversationState(session_id=session_id)
        self.mode_transitions = []

    def update(self, context):
        """根据管道上下文更新状态"""
        try:
            # Track emotion transitions
            old_emotion = self.conversation_state.current_emotion
            old_score = (self.conversation_state.emotion_trajectory[-1]
                        if self.conversation_state.emotion_trajectory else 5.0)

            self.conversation_state.update(context)

            new_emotion = self.conversation_state.current_emotion
            new_score = (self.conversation_state.emotion_trajectory[-1]
                        if self.conversation_state.emotion_trajectory else 5.0)

            # Detect emotion shifts
            if old_emotion and new_emotion and old_emotion != new_emotion:
                self.mode_transitions.append({
                    "type": "emotion_shift",
                    "from": old_emotion,
                    "to": new_emotion,
                    "score_delta": new_score - old_score,
                    "timestamp": datetime.now().isoformat(),
                })
            elif abs(new_score - old_score) >= 2.0:
                self.mode_transitions.append({
                    "type": "intensity_shift",
                    "from_score": old_score,
                    "to_score": new_score,
                    "timestamp": datetime.now().isoformat(),
                })

            # Trim transitions history
            if len(self.mode_transitions) > PipelineConfig.MAX_STATE_HISTORY:
                self.mode_transitions = self.mode_transitions[-PipelineConfig.MAX_STATE_HISTORY:]
        except Exception as error:
            context.add_error("WARNING", "STATE_MANAGER", str(error))

    def detect_emotion_trend(self):
        """检测情绪趋势"""
        trajectory = self.conversation_state.emotion_trajectory
        if len(trajectory) < 2:
            return "stable"
        recent = trajectory[-3:] if len(trajectory) >= 3 else trajectory
        deltas = [recent[i + 1] - recent[i] for i in range(len(recent) - 1)]
        avg_delta = sum(deltas) / len(deltas)
        if avg_delta > 1.0:
            return "worsening"
        elif avg_delta < -1.0:
            return "improving"
        return "stable"

    def get_context_summary(self):
        """获取上下文摘要"""
        return {
            "turn_count": self.conversation_state.turn_count,
            "current_emotion": self.conversation_state.current_emotion,
            "current_topic": self.conversation_state.current_topic,
            "user_role": self.conversation_state.user_role,
            "emotion_trend": self.detect_emotion_trend(),
            "crisis_level": self.conversation_state.current_crisis_level,
            "transition_count": len(self.mode_transitions),
        }

    def save(self, path=None):
        """保存状态到文件"""
        save_path = path or (DATA_DIR / f"state_manager_{self.session_id}.json")
        try:
            data = {
                "session_id": self.session_id,
                "conversation_state": self.conversation_state.to_dict(),
                "mode_transitions": self.mode_transitions[-20:],
            }
            with open(save_path, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as error:
            print(f"[StateManager] save error: {error}", file=sys.stderr)

    def load(self, path=None):
        """从文件加载状态"""
        load_path = path or (DATA_DIR / f"state_manager_{self.session_id}.json")
        if not Path(load_path).exists():
            return
        try:
            with open(load_path, "r", encoding="utf-8") as fh:
                data = json.loads(fh.read())
            state_data = data.get("conversation_state", {})
            self.conversation_state = ConversationState(session_id=self.session_id)
            self.conversation_state.turn_count = state_data.get("turn_count", 0)
            self.conversation_state.current_topic = state_data.get("current_topic", "")
            self.conversation_state.current_emotion = state_data.get("current_emotion", "")
            self.conversation_state.current_crisis_level = state_data.get("current_crisis_level", "none")
            self.conversation_state.user_role = state_data.get("user_role", "unknown")
            self.conversation_state.defense_pattern = state_data.get("defense_pattern", [])
            self.conversation_state.emotion_trajectory = state_data.get("emotion_trajectory", [])
            self.conversation_state.topic_history = state_data.get("topic_history", [])
            self.conversation_state.last_updated = state_data.get("last_updated", "")
            self.mode_transitions = data.get("mode_transitions", [])
        except Exception as error:
            print(f"[StateManager] load error: {error}", file=sys.stderr)


# === Error Recovery ===

class ErrorRecovery:
    """错误恢复策略"""
    STRATEGIES = {
        PipelineStage.SAFETY_GATE: {
            "on_fail": "assume_crisis",
            "fallback_data": {"is_crisis": True, "level": "direct",
                              "confidence": 0.5, "action": "immediate_intervention"},
            "retry": False,
        },
        PipelineStage.USER_IDENTIFY: {
            "on_fail": "assume_unknown",
            "fallback_data": {"role": "unknown", "confidence": 0.0,
                              "signals": [], "needs_confirm": True},
            "retry": False,
        },
        PipelineStage.EMOTION_ASSESS: {
            "on_fail": "assume_neutral",
            "fallback_data": {"primary_emotion": "neutral", "score": 3.0,
                              "all_emotions": {}, "intensity": "low",
                              "response_depth": "2min"},
            "retry": True,
        },
        PipelineStage.SCENARIO_MATCH: {
            "on_fail": "generic_analysis",
            "fallback_data": {"matched_scenario": "", "confidence": 0.0,
                              "all_matches": {}, "fallback": "generic_analysis"},
            "retry": True,
        },
        PipelineStage.DEFENSE_DETECT: {
            "on_fail": "no_defense",
            "fallback_data": {"primary_defense": "none", "all_defenses": {},
                              "confidence": 0.0, "guidance_needed": False},
            "retry": False,
        },
        PipelineStage.RESPONSE_GENERATE: {
            "on_fail": "generic_response",
            "fallback_data": {"type": "normal", "empathy": "感谢你的分享。",
                              "action": "", "guidance": "", "hotlines": []},
            "retry": True,
        },
        PipelineStage.QUALITY_CHECK: {
            "on_fail": "pass_with_warning",
            "fallback_data": {"passed": True, "score": 5.0,
                              "issues": ["质量检查未能完成"]},
            "retry": False,
        },
    }

    @staticmethod
    def get_strategy(stage):
        """获取指定阶段的错误恢复策略"""
        return ErrorRecovery.STRATEGIES.get(stage, {
            "on_fail": "skip",
            "fallback_data": {},
            "retry": False,
        })

    @staticmethod
    def should_retry(stage):
        """判断指定阶段失败后是否应重试"""
        strategy = ErrorRecovery.get_strategy(stage)
        return strategy.get("retry", False)

    @staticmethod
    def execute_recovery(context, stage, error):
        """执行错误恢复"""
        strategy = ErrorRecovery.get_strategy(stage)
        fallback = strategy.get("fallback_data", {})
        context.add_error("RECOVERY", stage.name, f"Using fallback: {error}")
        return fallback


# === Performance Optimizer ===

class PerformanceOptimizer:
    """性能优化器 — 追踪管道执行性能"""

    def __init__(self):
        self.metrics = []

    def record(self, report):
        """记录一次管道执行的性能指标"""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "success": report.success,
                "score": report.integration_score,
                "total_ms": report.total_duration_ms,
                "stages": {},
            }
            for stage_name, stage_data in report.stage_summary.items():
                entry["stages"][stage_name] = {
                    "duration_ms": stage_data.get("duration_ms", 0.0),
                    "confidence": stage_data.get("confidence", 0.0),
                    "status": stage_data.get("status", "unknown"),
                }
            self.metrics.append(entry)
            # Trim to max limit
            if len(self.metrics) > PipelineConfig.MAX_PERF_METRICS:
                self.metrics = self.metrics[-PipelineConfig.MAX_PERF_METRICS:]
        except Exception as error:
            print(f"[PerformanceOptimizer] record error: {error}", file=sys.stderr)

    def get_bottleneck(self):
        """识别性能瓶颈阶段"""
        if not self.metrics:
            return None
        stage_totals = {}
        for entry in self.metrics:
            for stage_name, stage_data in entry.get("stages", {}).items():
                if stage_name not in stage_totals:
                    stage_totals[stage_name] = 0.0
                stage_totals[stage_name] += stage_data.get("duration_ms", 0.0)
        if not stage_totals:
            return None
        return max(stage_totals, key=stage_totals.get)

    def get_report(self):
        """生成性能报告"""
        if not self.metrics:
            return {"status": "no_data"}
        total_runs = len(self.metrics)
        successes = sum(1 for m in self.metrics if m["success"])
        total_ms_values = [m["total_ms"] for m in self.metrics]
        score_values = [m["score"] for m in self.metrics]
        return {
            "total_runs": total_runs,
            "success_rate": successes / total_runs if total_runs else 0.0,
            "avg_total_ms": sum(total_ms_values) / total_runs,
            "avg_score": sum(score_values) / total_runs,
            "bottleneck": self.get_bottleneck(),
        }


# === Pipeline Orchestrator ===

class PipelineOrchestrator:
    """管道编排器 — 协调所有阶段的执行"""

    STAGE_EXECUTORS = {
        PipelineStage.SAFETY_GATE: SafetyGate.execute,
        PipelineStage.USER_IDENTIFY: UserIdentifier.execute,
        PipelineStage.EMOTION_ASSESS: EmotionAssessor.execute,
        PipelineStage.SCENARIO_MATCH: ScenarioMatcher.execute,
        PipelineStage.DEFENSE_DETECT: DefenseDetector.execute,
        PipelineStage.RESPONSE_GENERATE: ResponseGenerator.execute,
        PipelineStage.QUALITY_CHECK: QualityChecker.execute,
    }

    STAGE_CONTEXT_MAP = {
        PipelineStage.SAFETY_GATE: "safety_result",
        PipelineStage.USER_IDENTIFY: "user_identity",
        PipelineStage.EMOTION_ASSESS: "emotion_state",
        PipelineStage.SCENARIO_MATCH: "scenario_match",
        PipelineStage.DEFENSE_DETECT: "defense_signals",
        PipelineStage.RESPONSE_GENERATE: "response",
        PipelineStage.QUALITY_CHECK: "quality_check",
    }

    def __init__(self, mode=IntegrationMode.FULL):
        self.mode = mode
        self.state_manager = None
        self.perf_optimizer = PerformanceOptimizer()

    def run(self, user_input, session_id="default"):
        """执行完整管道"""
        start_time = time.time()
        context = PipelineContext(
            user_input=user_input,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            pipeline_mode=self.mode,
        )
        self.state_manager = StateManager(session_id)
        report = IntegrationReport(context=context, state=self.state_manager.conversation_state)

        try:
            # Determine which stages to run
            stages_to_run = self._get_stages_for_mode()

            for stage in stages_to_run:
                stage_start = time.time()
                stage_name = stage.name
                result = StageResult(stage=stage)
                result.status = StageStatus.RUNNING

                try:
                    # Check if we should skip (e.g., crisis short-circuit)
                    if self._should_skip_stage(stage, context):
                        result.status = StageStatus.SKIPPED
                        result.duration_ms = (time.time() - stage_start) * 1000
                        context.stage_results[stage_name] = result
                        report.stage_summary[stage_name] = {
                            "status": "skipped",
                            "confidence": 0.0,
                            "duration_ms": result.duration_ms,
                        }
                        continue

                    # Execute stage
                    executor = self.STAGE_EXECUTORS.get(stage)
                    if executor:
                        stage_result = executor(context)
                        context_attr = self.STAGE_CONTEXT_MAP.get(stage)
                        if context_attr:
                            setattr(context, context_attr, stage_result)
                        result.data = stage_result
                        result.status = StageStatus.SUCCESS
                        result.confidence = stage_result.get("confidence", 0.8)

                except Exception as stage_error:
                    result.status = StageStatus.FAILED
                    result.error = str(stage_error)
                    # Apply error recovery
                    if ErrorRecovery.should_retry(stage):
                        fallback = ErrorRecovery.execute_recovery(
                            context, stage, stage_error)
                        context_attr = self.STAGE_CONTEXT_MAP.get(stage)
                        if context_attr:
                            setattr(context, context_attr, fallback)
                        result.data = fallback
                        result.status = StageStatus.DEGRADED
                    else:
                        fallback = ErrorRecovery.execute_recovery(
                            context, stage, stage_error)
                        context_attr = self.STAGE_CONTEXT_MAP.get(stage)
                        if context_attr:
                            setattr(context, context_attr, fallback)
                        result.data = fallback
                        result.status = StageStatus.DEGRADED

                result.duration_ms = (time.time() - stage_start) * 1000
                context.stage_results[stage_name] = result
                report.stage_summary[stage_name] = {
                    "status": result.status.value,
                    "confidence": result.confidence,
                    "duration_ms": result.duration_ms,
                    "error": result.error,
                }

                # Crisis short-circuit: skip remaining stages after safety gate
                if (stage == PipelineStage.SAFETY_GATE
                        and context.safety_result
                        and context.safety_result.get("is_crisis", False)):
                    # Mark all remaining stages as skipped
                    for remaining in stages_to_run:
                        if remaining.value <= stage.value:
                            continue
                        report.stage_summary[remaining.name] = {
                            "status": "skipped",
                            "confidence": 0.0,
                            "duration_ms": 0.0,
                        }
                    # Execute response and quality for crisis (unless SAFETY_ONLY mode)
                    if self.mode != IntegrationMode.SAFETY_ONLY:
                        for crisis_stage in [PipelineStage.RESPONSE_GENERATE,
                                            PipelineStage.QUALITY_CHECK]:
                            crisis_start = time.time()
                            try:
                                executor = self.STAGE_EXECUTORS.get(crisis_stage)
                                if executor:
                                    crisis_result = executor(context)
                                    context_attr = self.STAGE_CONTEXT_MAP.get(crisis_stage)
                                    if context_attr:
                                        setattr(context, context_attr, crisis_result)
                            except Exception as crisis_error:
                                fallback = ErrorRecovery.execute_recovery(
                                    context, crisis_stage, crisis_error)
                                context_attr = self.STAGE_CONTEXT_MAP.get(crisis_stage)
                                if context_attr:
                                    setattr(context, context_attr, fallback)
                            crisis_ms = (time.time() - crisis_start) * 1000
                            report.stage_summary[crisis_stage.name] = {
                                "status": "success",
                                "confidence": 0.8,
                                "duration_ms": crisis_ms,
                            }
                    break

            # Apply data flow transforms
            DataFlowRules.apply_transforms(context)

            # Update state
            self.state_manager.update(context)
            report.state = self.state_manager.conversation_state

            # Calculate integration score
            report.integration_score = self._calculate_score(report)
            report.success = report.integration_score > 0
            report.transforms_applied = context.transforms_applied

        except Exception as error:
            context.add_error("FATAL", "PIPELINE", str(error))
            report.errors = context.errors
            report.success = False

        # Finalize
        total_ms = (time.time() - start_time) * 1000
        context.total_duration_ms = total_ms
        report.total_duration_ms = total_ms
        report.errors = context.errors

        # Record performance
        self.perf_optimizer.record(report)
        report.performance = self.perf_optimizer.get_report()

        return report

    def diagnose(self, user_input, session_id="default"):
        """诊断模式 — 返回详细的阶段分析"""
        original_mode = self.mode
        self.mode = IntegrationMode.DIAGNOSTIC
        try:
            report = self.run(user_input, session_id)
            result = {}
            for stage_name, stage_data in report.stage_summary.items():
                result[stage_name] = stage_data
            result["integration_score"] = report.integration_score
            result["total_duration_ms"] = report.total_duration_ms
            result["errors"] = report.errors
            result["transforms"] = report.transforms_applied
            return result
        finally:
            self.mode = original_mode

    def _get_stages_for_mode(self):
        """根据模式返回需要执行的阶段列表（始终返回所有阶段，跳过逻辑由_should_skip_stage控制）"""
        return list(PipelineStage)

    def _should_skip_stage(self, stage, context):
        """判断是否应跳过某阶段"""
        if self.mode == IntegrationMode.SAFETY_ONLY:
            return stage != PipelineStage.SAFETY_GATE
        return False

    def _calculate_score(self, report):
        """计算集成得分（加权平均）"""
        total_weight = 0.0
        weighted_sum = 0.0
        for stage in PipelineStage:
            stage_name = stage.name
            weight = PipelineConfig.STAGE_WEIGHTS.get(stage.value, 1.0)
            if stage_name in report.stage_summary:
                status = report.stage_summary[stage_name].get("status", "skipped")
                confidence = report.stage_summary[stage_name].get("confidence", 0.0)
                if status == "success":
                    weighted_sum += weight * confidence
                elif status == "degraded":
                    weighted_sum += weight * confidence * 0.5
                # failed/skipped contribute 0
            total_weight += weight
        return weighted_sum / total_weight if total_weight > 0 else 0.0


# === Convenience Functions ===

def process_input(user_input, session_id="default"):
    """便捷函数 — 执行完整管道"""
    orchestrator = PipelineOrchestrator(mode=IntegrationMode.FULL)
    return orchestrator.run(user_input, session_id)


def diagnose_input(user_input, session_id="default"):
    """便捷函数 — 诊断模式"""
    orchestrator = PipelineOrchestrator(mode=IntegrationMode.DIAGNOSTIC)
    return orchestrator.diagnose(user_input, session_id)


# === Main ===

def main():
    """CLI 入口"""
    print(f"System Integrator v{VERSION}")
    print("=" * 50)

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = "我的孩子成绩下降了，我很焦虑"

    print(f"Input: {user_input}")
    print("-" * 50)

    report = process_input(user_input, "cli_test")

    print(f"Success: {report.success}")
    print(f"Score: {report.integration_score:.2f}")
    print(f"Duration: {report.total_duration_ms:.1f}ms")
    print()

    for stage_name, stage_data in report.stage_summary.items():
        status = stage_data.get("status", "unknown")
        confidence = stage_data.get("confidence", 0.0)
        print(f"  {stage_name}: {status} (conf={confidence:.2f})")

    if report.errors:
        print(f"\nErrors ({len(report.errors)}):")
        for err in report.errors:
            print(f"  [{err['severity']}] {err['stage']}: {err['message']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
