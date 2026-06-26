#!/usr/bin/env python3
"""
父母的功课 - 行动规划器 (Action Planner) v1.1.0

核心能力：
1. 行动粒度模型：大目标 → 小步骤 → 微行动
2. 行动难度评估：基于用户能力匹配
3. 行动阶梯生成：从易到难的行动序列
4. 行动反馈机制：行动后评估效果

理论基础：SMART目标、行为激活、BJ Fogg微习惯、GROW教练模型

用法:
    python3 scripts/action_planner.py --plan "改善亲子沟通"
    python3 scripts/action_planner.py --assess "每天和孩子聊15分钟"
    python3 scripts/action_planner.py --ladder "孩子不听话"
    python3 scripts/action_planner.py --demo
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum

import os
if not os.environ.get("ALLOW_FILE_PERSISTENCE"):
    print("❌ 文件持久化功能已禁用。如需启用，请设置 ALLOW_FILE_PERSISTENCE=1")
    exit(0)

# ============================================================
# 数据模型
# ============================================================

class ActionDifficulty(Enum):
    TRIVIAL = 1
    EASY = 2
    MODERATE = 3
    HARD = 4
    CHALLENGING = 5

class FeedbackRating(Enum):
    DIDNT_TRY = 0
    FAILED = 1
    PARTIAL = 2
    SUCCESS = 3
    EXCEEDED = 4


@dataclass
class UserCapability:
    energy_level: int = 5
    stress_level: int = 5
    available_minutes: int = 30
    support_system: int = 5
    previous_attempts: int = 0
    success_history: list = field(default_factory=list)


# ============================================================
# 行动模板库
# ============================================================

ACTION_TEMPLATES = {
    "亲子沟通": {
        "goal": "建立有效、温暖的亲子沟通",
        "steps": [
            {
                "text": "每天找一个自然时机，问孩子一个开放式问题",
                "granularity": "micro", "difficulty": 2, "type": "沟通", "minutes": 5,
                "smart": {"specific": "每天问1个开放式问题", "measurable": "记录是否完成", "achievable": "只需5分钟", "relevant": "建立沟通习惯", "timebound": "今天开始"},
                "indicators": ["孩子愿意回答", "对话持续超过1分钟"],
                "obstacles": ["不知道问什么", "孩子不想回答"],
                "coping": ["准备3个问题备用", "不强迫，换个时间再试"]
            },
            {
                "text": "倾听时放下手机，看着孩子的眼睛，不打断",
                "granularity": "step", "difficulty": 3, "type": "行为", "minutes": 10,
                "smart": {"specific": "每次孩子说话时全神贯注", "measurable": "是否放下手机", "achievable": "从5分钟开始", "relevant": "让孩子感到被重视", "timebound": "每天至少一次"},
                "indicators": ["孩子说话时间变长", "孩子主动分享更多"],
                "obstacles": ["习惯性看手机", "忍不住想给建议"],
                "coping": ["手机放另一个房间", "默数3秒再回应"]
            },
            {
                "text": "用'我注意到...'句式代替'你怎么又...'句式",
                "granularity": "step", "difficulty": 3, "type": "沟通", "minutes": 0,
                "smart": {"specific": "转换语言模式", "measurable": "记录使用次数", "achievable": "每天至少1次", "relevant": "减少防御反应", "timebound": "持续2周"},
                "indicators": ["孩子防御反应减少", "对话更顺畅"],
                "obstacles": ["旧习惯太强", "情绪上来时忘了"],
                "coping": ["在冰箱贴提示语", "情绪激动时先暂停"]
            }
        ]
    },
    "情绪管理": {
        "goal": "学会在情绪激动时自我调节",
        "steps": [
            {
                "text": "情绪升起时，先深呼吸3次再回应",
                "granularity": "nano", "difficulty": 1, "type": "情绪", "minutes": 1,
                "smart": {"specific": "深呼吸3次", "measurable": "是否执行", "achievable": "随时可做", "relevant": "打断自动反应", "timebound": "每次情绪升起时"},
                "indicators": ["回应前有停顿", "冲动行为减少"],
                "obstacles": ["情绪太快来不及", "忘记使用"],
                "coping": ["在手机设提醒", "贴便利贴在常见触发点"]
            },
            {
                "text": "每天记录一次情绪日记",
                "granularity": "step", "difficulty": 2, "type": "反思", "minutes": 10,
                "smart": {"specific": "写情绪日记", "measurable": "是否完成", "achievable": "10分钟", "relevant": "提高情绪觉察", "timebound": "每天睡前"},
                "indicators": ["能识别情绪模式", "提前预判触发点"],
                "obstacles": ["太累不想写", "不知道写什么"],
                "coping": ["用模板简化", "只写关键词也行"]
            },
            {
                "text": "每周回顾情绪日记，找出高频触发点",
                "granularity": "step", "difficulty": 3, "type": "反思", "minutes": 20,
                "smart": {"specific": "分析情绪模式", "measurable": "找出3个触发点", "achievable": "每周一次", "relevant": "从被动到主动预防", "timebound": "每周日"},
                "indicators": ["能预测情绪触发", "有应对方案"],
                "obstacles": ["分析太复杂", "找不到规律"],
                "coping": ["从最明显的1个开始", "请伴侣帮忙观察"]
            }
        ]
    },
    "孩子不听话": {
        "goal": "理解行为背后的需求，建立合作",
        "steps": [
            {
                "text": "孩子不听话时，先问自己：他此刻需要什么？",
                "granularity": "nano", "difficulty": 2, "type": "反思", "minutes": 1,
                "smart": {"specific": "暂停并思考孩子需求", "measurable": "是否执行", "achievable": "1分钟内", "relevant": "从反应到理解", "timebound": "每次冲突时"},
                "indicators": ["能识别孩子需求", "回应更有针对性"],
                "obstacles": ["情绪太激动", "只想让孩子听话"],
                "coping": ["先处理自己情绪", "记住：行为是沟通"]
            },
            {
                "text": "给孩子2个可接受的选择，而不是命令",
                "granularity": "step", "difficulty": 2, "type": "沟通", "minutes": 2,
                "smart": {"specific": "提供2个选择", "measurable": "是否提供选择", "achievable": "准备常见场景选择", "relevant": "给予自主权", "timebound": "每天至少1次"},
                "indicators": ["孩子更愿意配合", "权力斗争减少"],
                "obstacles": ["想不出选择", "孩子都不选"],
                "coping": ["提前准备选择库", "都不选就帮他选"]
            },
            {
                "text": "设定清晰规则和后果，温和而坚定地执行",
                "granularity": "step", "difficulty": 4, "type": "边界", "minutes": 15,
                "smart": {"specific": "制定3条核心规则", "measurable": "规则是否清晰", "achievable": "从1条开始", "relevant": "提供安全感", "timebound": "本周内"},
                "indicators": ["孩子知道界限", "测试行为减少"],
                "obstacles": ["不忍心执行", "伴侣不一致"],
                "coping": ["后果要合理", "和伴侣统一标准"]
            }
        ]
    },
    "孩子沉迷手机": {
        "goal": "建立健康的屏幕时间习惯",
        "steps": [
            {
                "text": "和孩子一起制定屏幕时间规则",
                "granularity": "step", "difficulty": 3, "type": "沟通", "minutes": 20,
                "smart": {"specific": "共同商定屏幕时间", "measurable": "达成协议", "achievable": "一次对话", "relevant": "参与感提高遵守", "timebound": "本周内"},
                "indicators": ["孩子参与讨论", "规则得到认可"],
                "obstacles": ["孩子不愿谈", "谈不拢"],
                "coping": ["先听孩子想法", "各让一步"]
            },
            {
                "text": "创建无屏幕时间区域（餐桌、卧室）",
                "granularity": "step", "difficulty": 2, "type": "环境", "minutes": 5,
                "smart": {"specific": "设定2个无屏幕区域", "measurable": "是否执行", "achievable": "从1个开始", "relevant": "减少诱惑", "timebound": "今天开始"},
                "indicators": ["规则被遵守", "替代活动增加"],
                "obstacles": ["自己也做不到", "孩子抗议"],
                "coping": ["以身作则", "提供替代活动"]
            },
            {
                "text": "找到孩子喜欢的线下替代活动",
                "granularity": "step", "difficulty": 3, "type": "环境", "minutes": 30,
                "smart": {"specific": "每天1个线下活动", "measurable": "活动是否执行", "achievable": "从简单开始", "relevant": "用有趣的事替代", "timebound": "持续2周"},
                "indicators": ["孩子主动参与", "屏幕时间减少"],
                "obstacles": ["孩子说无聊", "没好主意"],
                "coping": ["让孩子选活动", "准备活动清单"]
            }
        ]
    },
    "孩子成绩下降": {
        "goal": "理解原因并提供有效支持",
        "steps": [
            {
                "text": "和孩子聊学习困难（不是质问）",
                "granularity": "micro", "difficulty": 2, "type": "沟通", "minutes": 15,
                "smart": {"specific": "了解学习困难", "measurable": "是否完成对话", "achievable": "选轻松时机", "relevant": "找到真正原因", "timebound": "本周内"},
                "indicators": ["孩子愿意说", "找到具体问题"],
                "obstacles": ["孩子不愿说", "自己太焦虑"],
                "coping": ["先表达关心", "分享自己经历"]
            },
            {
                "text": "一起制定简单可行的学习计划",
                "granularity": "step", "difficulty": 3, "type": "技能", "minutes": 30,
                "smart": {"specific": "制定学习计划", "measurable": "计划是否完成", "achievable": "从1科开始", "relevant": "提供结构", "timebound": "本周内"},
                "indicators": ["计划可执行", "孩子有参与感"],
                "obstacles": ["计划太复杂", "执行不下去"],
                "coping": ["留出弹性", "每周调整"]
            },
            {
                "text": "关注努力和进步，而不只是分数",
                "granularity": "step", "difficulty": 3, "type": "行为", "minutes": 0,
                "smart": {"specific": "每天表扬1个努力", "measurable": "是否执行", "achievable": "每天1次", "relevant": "建立成长心态", "timebound": "持续3周"},
                "indicators": ["学习动力提升", "焦虑减少"],
                "obstacles": ["忍不住关注分数", "不知道怎么表扬"],
                "coping": ["用'我看到你...'句式", "表扬过程"]
            }
        ]
    }
}


# ============================================================
# 核心引擎
# ============================================================

class ActionPlanner:
    """行动规划器核心引擎"""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path.home() / ".hermes" / "still_growing"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_file = self.data_dir / "action_feedback.json"
        self.ladder_file = self.data_dir / "action_ladders.json"

    # --------------------------------------------------------
    # 1. 行动粒度模型：大目标 → 小步骤 → 微行动
    # --------------------------------------------------------
    def decompose_goal(self, goal_text: str, scenario: str = None) -> Dict:
        """将大目标分解为可执行的微行动"""
        matched = self._match_scenario(goal_text, scenario)
        if matched:
            template = ACTION_TEMPLATES[matched]
            return {
                "goal": template["goal"],
                "scenario": matched,
                "granularity_chain": self._build_chain(template),
                "first_action": template["steps"][0],
                "total_actions": len(template["steps"])
            }
        return self._generic_decompose(goal_text)

    def _match_scenario(self, text: str, scenario: str = None) -> Optional[str]:
        search = f"{text} {scenario or ''}"
        keywords = {
            "亲子沟通": ["沟通", "说话", "聊天", "交流", "倾听"],
            "情绪管理": ["情绪", "发脾气", "控制", "暴躁", "生气", "焦虑"],
            "孩子不听话": ["不听话", "叛逆", "顶嘴", "对抗", "不配合", "反抗"],
            "孩子沉迷手机": ["手机", "游戏", "屏幕", "沉迷", "上网"],
            "孩子成绩下降": ["成绩", "学习", "考试", "分数", "作业", "厌学"]
        }
        for name, kws in keywords.items():
            if any(k in search for k in kws):
                return name
        return None

    def _build_chain(self, template: Dict) -> List[Dict]:
        chain = [{"level": "goal", "text": template["goal"]}]
        for s in template["steps"]:
            chain.append({"level": s["granularity"], "text": s["text"], "difficulty": s["difficulty"]})
        return chain

    def _generic_decompose(self, goal_text: str) -> Dict:
        return {
            "goal": goal_text,
            "scenario": "通用",
            "granularity_chain": [
                {"level": "goal", "text": goal_text},
                {"level": "step", "text": f"将'{goal_text}'分解为3个具体行动"},
                {"level": "micro", "text": "为每个行动找到今天就能做的最小步骤"},
                {"level": "nano", "text": "现在就做第一个纳米行动"}
            ],
            "first_action": {"text": "现在深呼吸，思考这个目标对你和孩子意味着什么", "difficulty": 1, "minutes": 1},
            "total_actions": 3
        }

    # --------------------------------------------------------
    # 2. 行动难度评估
    # --------------------------------------------------------
    def assess_difficulty(self, action_text: str, capability: UserCapability = None) -> Dict:
        """评估行动难度并匹配用户能力"""
        if capability is None:
            capability = UserCapability()
        base = self._base_difficulty(action_text)
        adjusted = self._adjust_for_capability(base, capability)
        return {
            "action": action_text,
            "base_difficulty": base,
            "adjusted_difficulty": adjusted,
            "difficulty_label": ActionDifficulty(adjusted).name,
            "recommendation": self._difficulty_recommendation(adjusted, capability),
            "capability_summary": {
                "energy": capability.energy_level,
                "stress": capability.stress_level,
                "time": capability.available_minutes,
                "support": capability.support_system
            }
        }

    def _base_difficulty(self, text: str) -> int:
        easy = ["深呼吸", "问", "想", "记", "写", "观察", "暂停"]
        moderate = ["倾听", "放下", "每天", "一起", "制定", "记录"]
        hard = ["执行", "坚持", "改变", "设定规则", "控制", "每周"]
        if any(k in text for k in easy): return 2
        if any(k in text for k in moderate): return 3
        if any(k in text for k in hard): return 4
        return 3

    def _adjust_for_capability(self, base: int, cap: UserCapability) -> int:
        adjustment = 0
        if cap.energy_level <= 3: adjustment += 1
        if cap.stress_level >= 7: adjustment += 1
        if cap.available_minutes < 15: adjustment += 1
        if cap.support_system >= 7: adjustment -= 1
        if cap.previous_attempts > 3: adjustment -= 1
        return max(1, min(5, base + adjustment))

    def _difficulty_recommendation(self, diff: int, cap: UserCapability) -> str:
        if diff <= 2:
            return "这个行动难度很低，适合现在就开始。"
        elif diff == 3:
            if cap.energy_level <= 3:
                return "中等难度，但你精力较低。建议先休息，精力好时再尝试。"
            return "中等难度，建议做好准备后执行。"
        elif diff == 4:
            return "较高难度。建议先完成2-3个简单行动建立信心后再尝试。"
        else:
            return "高难度。建议分解为更小的步骤，或寻求支持后再尝试。"

    # --------------------------------------------------------
    # 3. 行动阶梯生成
    # --------------------------------------------------------
    def generate_ladder(self, scenario: str, capability: UserCapability = None) -> Dict:
        """生成从易到难的行动阶梯"""
        if capability is None:
            capability = UserCapability()

        template = ACTION_TEMPLATES.get(scenario)
        if not template:
            return {"error": f"未找到场景: {scenario}", "available": list(ACTION_TEMPLATES.keys())}

        sorted_steps = sorted(template["steps"], key=lambda s: s["difficulty"])
        ladder_steps = []
        total_days = 0
        for i, step in enumerate(sorted_steps, 1):
            diff = self._adjust_for_capability(step["difficulty"], capability)
            days = max(1, diff * 2)
            total_days += days
            ladder_steps.append({
                "step": i,
                "text": step["text"],
                "difficulty": diff,
                "granularity": step["granularity"],
                "estimated_days": days,
                "is_gateway": i == 1,
                "smart": step.get("smart", {}),
                "indicators": step.get("indicators", []),
                "obstacles": step.get("obstacles", []),
                "coping": step.get("coping", [])
            })

        return {
            "goal": template["goal"],
            "scenario": scenario,
            "steps": ladder_steps,
            "total_steps": len(ladder_steps),
            "total_estimated_days": total_days,
            "first_step": ladder_steps[0] if ladder_steps else None,
            "adaptation_note": self._adaptation_note(capability)
        }

    def _adaptation_note(self, cap: UserCapability) -> str:
        notes = []
        if cap.energy_level <= 3:
            notes.append("精力较低：建议先从纳米行动开始")
        if cap.stress_level >= 7:
            notes.append("压力较大：每步之间多留缓冲时间")
        if cap.available_minutes < 15:
            notes.append("时间有限：优先选择5分钟以内的行动")
        if cap.previous_attempts > 3:
            notes.append("有经验：可以跳过最基础的步骤")
        return "; ".join(notes) if notes else "按标准节奏推进即可"

    # --------------------------------------------------------
    # 4. 行动反馈机制
    # --------------------------------------------------------
    def record_feedback(self, action_id: str, rating: int, what_worked: str,
                        what_didnt: str, child_response: str, lessons: str,
                        adjustment: str) -> Dict:
        """记录行动反馈"""
        feedback = {
            "action_id": action_id,
            "rating": rating,
            "rating_label": FeedbackRating(rating).name,
            "what_worked": what_worked,
            "what_didnt": what_didnt,
            "child_response": child_response,
            "lessons_learned": lessons,
            "next_adjustment": adjustment,
            "timestamp": datetime.now().isoformat()
        }
        feedbacks = self._load_feedbacks()
        feedbacks.append(feedback)
        self._save_feedbacks(feedbacks)
        return feedback

    def get_feedback_summary(self, last_n: int = 10) -> Dict:
        """获取反馈摘要"""
        feedbacks = self._load_feedbacks()
        if not feedbacks:
            return {"total": 0, "message": "暂无反馈记录"}
        recent = feedbacks[-last_n:]
        ratings = [f["rating"] for f in recent]
        avg = sum(ratings) / len(ratings) if ratings else 0
        success_count = sum(1 for r in ratings if r >= 3)
        return {
            "total": len(feedbacks),
            "recent_count": len(recent),
            "average_rating": round(avg, 1),
            "success_rate": round(success_count / len(recent) * 100, 1) if recent else 0,
            "trend": self._calculate_trend(ratings),
            "common_lessons": self._extract_lessons(recent),
            "recommendations": self._generate_recommendations(avg, ratings)
        }

    def _calculate_trend(self, ratings: List[int]) -> str:
        if len(ratings) < 3:
            return "数据不足"
        first_half = sum(ratings[:len(ratings)//2]) / (len(ratings)//2)
        second_half = sum(ratings[len(ratings)//2:]) / (len(ratings) - len(ratings)//2)
        if second_half > first_half + 0.5:
            return "上升趋势"
        elif second_half < first_half - 0.5:
            return "下降趋势"
        return "稳定"

    def _extract_lessons(self, feedbacks: List[Dict]) -> List[str]:
        lessons = []
        for f in feedbacks:
            if f.get("lessons_learned"):
                lessons.append(f["lessons_learned"])
        return lessons[:5]

    def _generate_recommendations(self, avg: float, ratings: List[int]) -> List[str]:
        recs = []
        if avg < 1.5:
            recs.append("行动可能太难了，建议降低难度")
            recs.append("检查是否有未解决的障碍")
        elif avg < 2.5:
            recs.append("有些进展，继续尝试并微调方法")
            recs.append("关注什么有效的，多做那些")
        else:
            recs.append("做得很好！可以尝试更有挑战的行动")
        if len(ratings) >= 3 and all(r < 2 for r in ratings[-3:]):
            recs.append("连续失败：建议重新评估目标或寻求支持")
        return recs

    def _load_feedbacks(self) -> List[Dict]:
        if self.feedback_file.exists():
            try:
                return json.loads(self.feedback_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_feedbacks(self, feedbacks: List[Dict]):
        self.feedback_file.write_text(json.dumps(feedbacks, ensure_ascii=False, indent=2), encoding="utf-8")

    # --------------------------------------------------------
    # 5. 综合规划
    # --------------------------------------------------------
    def create_full_plan(self, goal_text: str, scenario: str = None,
                         capability: UserCapability = None) -> Dict:
        """创建完整的行动计划"""
        if capability is None:
            capability = UserCapability()

        decomposed = self.decompose_goal(goal_text, scenario)
        matched_scenario = decomposed.get("scenario", "通用")

        if matched_scenario != "通用":
            ladder = self.generate_ladder(matched_scenario, capability)
        else:
            ladder = {"steps": [], "total_steps": 0, "message": "通用目标，请参考分解结果"}

        first = decomposed.get("first_action", {})
        first_assess = self.assess_difficulty(first.get("text", ""), capability)

        return {
            "goal": decomposed["goal"],
            "scenario": matched_scenario,
            "decomposition": decomposed["granularity_chain"],
            "ladder": ladder,
            "first_action": {
                "text": first.get("text", ""),
                "assessment": first_assess
            },
            "quick_start": self._quick_start(decomposed, first_assess),
            "created_at": datetime.now().isoformat()
        }

    def _quick_start(self, decomposed: Dict, assessment: Dict) -> str:
        first = decomposed.get("first_action", {})
        diff = assessment.get("adjusted_difficulty", 3)
        if diff <= 2:
            return f"现在就开始：{first.get('text', '')}（只需{first.get('minutes', 1)}分钟）"
        else:
            return f"准备好了再开始：{first.get('text', '')}。如果觉得太难，先做3次深呼吸。"


# ============================================================
# CLI 入口
# ============================================================

def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))

def main():
    args = sys.argv[1:]
    planner = ActionPlanner()

    if not args or "--help" in args:
        print(__doc__)
        return

    if "--demo" in args:
        print("=" * 50)
        print("行动规划器演示")
        print("=" * 50)
        cap = UserCapability(energy_level=4, stress_level=6, available_minutes=20)
        scenarios = list(ACTION_TEMPLATES.keys())
        for sc in scenarios[:3]:
            print(f"\n--- 场景: {sc} ---")
            plan = planner.create_full_plan(sc, capability=cap)
            print(f"目标: {plan['goal']}")
            print(f"阶梯步数: {plan['ladder'].get('total_steps', 0)}")
            print(f"预估天数: {plan['ladder'].get('total_estimated_days', 'N/A')}")
            print(f"快速开始: {plan['quick_start']}")
        return

    if "--plan" in args:
        idx = args.index("--plan")
        goal = args[idx + 1] if idx + 1 < len(args) else "改善亲子关系"
        plan = planner.create_full_plan(goal)
        print_json(plan)
        return

    if "--assess" in args:
        idx = args.index("--assess")
        action = args[idx + 1] if idx + 1 < len(args) else "每天和孩子聊15分钟"
        result = planner.assess_difficulty(action)
        print_json(result)
        return

    if "--ladder" in args:
        idx = args.index("--ladder")
        scenario = args[idx + 1] if idx + 1 < len(args) else "孩子不听话"
        result = planner.generate_ladder(scenario)
        print_json(result)
        return

    if "--feedback" in args:
        idx = args.index("--feedback")
        action_id = args[idx + 1] if idx + 1 < len(args) else "test"
        fb = planner.record_feedback(action_id, 3, "孩子有回应", "时间不够", "微笑", "要坚持", "明天继续")
        print_json(fb)
        return

    if "--summary" in args:
        summary = planner.get_feedback_summary()
        print_json(summary)
        return

    print("用法: python3 action_planner.py --plan|--assess|--ladder|--feedback|--demo [参数]")
    print("示例: python3 action_planner.py --plan '改善亲子沟通'")


if __name__ == "__main__":
    main()
