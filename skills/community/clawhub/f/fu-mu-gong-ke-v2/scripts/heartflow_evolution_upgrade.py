#!/usr/bin/env python3
"""
心虫进化恢复引擎 (HeartFlow Evolution Upgrade Engine) v1.0.0
=============================================================
升级版恢复路线图模块 — 基于心虫四大核心机制 + fu-mu-gong-ke 4阶段恢复路线图。

集成内容：
  1) EvolutionLoop — 目标驱动循环 (goal→plan→execute→reflect→improve)
     基于心虫 self-evolution-core.js 的 evolve() + evolution-learning.js 的 evolve()
  2) SelfEvolutionCore — 自我进化核心 (策略适应/成果跟踪/成长指标)
     基于心虫 self-evolution-core.js 的 SelfEvolutionCore + evolution-learning.js 的 updateGrowth
  3) MetaLearner — 元学习器 (教训质量评分/模式提取/相关性召回)
     基于心虫 meta-learning.js 的 MetaLearning + evolution-learning.js 的 retrieveLessons
  4) GoedelInference — 哥德尔自指推理引擎 (原则反思/过程反思/元认知)
     基于心虫 goedel-engine.js 的 principleBasedReflect + proceduralReflect + metaCognitiveSelfModification
  5) 升级后的4阶段恢复路线图 — 每阶段集成进化循环

理论来源：
  - HeartFlow self-evolution-core.js: SelfEvolutionCore, evolve(), generateGoals, createPlan
  - HeartFlow evolution-learning.js: EvolutionLearning, reflect, updateGrowth, Reflexion
  - HeartFlow evolution-goals.js: EvolutionGoals, 目标生成与优先级排序
  - HeartFlow evolution-strategies.js: EvolutionStrategies, selfRefine, Q-learning 自愈
  - HeartFlow meta-learning.js: MetaLearning, 策略选择与评分
  - HeartFlow goedel-engine.js: GoedelEngine, 原则反思, 过程反思, 元认知
  - fu-mu-gong-ke SKILL.md: 4阶段恢复路线图 + 3层防御 + 3层需求

作者: HeartFlow Evolution Upgrade Engine
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
from datetime import datetime, timedelta


__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════════════════════
# 第一部分: EvolutionLoop — 目标驱动循环
# 基于心虫 self-evolution-core.js 的 evolve() + evolution-learning.js 的 evolve()
# 实现：goal → plan → execute → reflect → improve 五步闭环
# ═══════════════════════════════════════════════════════════════════════════════


class GoalType(Enum):
    """目标类型 — 基于心虫 evolution-goals.js"""
    UNDERSTANDING = "understanding"         # 理解类：深化问题理解
    GROWTH = "growth"                       # 成长类：获取新知识
    EMPATHY = "empathy"                     # 情感类：理解情感状态
    REFLECTION = "reflection"               # 反思类：反思自身行为
    CONTINUOUS_LEARNING = "continuous_learning"  # 默认：持续学习
    HEALING = "healing"                     # 恢复类：创伤修复
    SEPARATION = "separation"               # 分离类：情感独立
    REPAIR = "repair"                       # 修复类：代际修复


class Priority(IntEnum):
    """优先级 — 基于心虫 evolution-goals.js"""
    HIGH = 0
    MEDIUM = 1
    LOW = 2


@dataclass
class Goal:
    """目标定义 — 基于心虫 evolution-goals.js 的 goal 结构"""
    type: GoalType
    priority: Priority
    description: str
    criteria: str
    progress: float = 0.0  # 0.0~1.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Plan:
    """行动计划 — 基于心虫 self-evolution-core.js 的 createPlan"""
    goals: List[str]
    strategy: str
    estimated_time: int
    resources: List[str]
    steps: List[Dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Insight:
    """反思见解 — 基于心虫 evolution-learning.js 的 insight 结构"""
    type: str
    insight: str
    depth: float = 1.0  # 反思深度


@dataclass
class Reflection:
    """反思结果 — 基于心虫 evolution-learning.js 的 reflect 返回"""
    insights: List[Insight]
    quality: str  # 'good' | 'needs_improvement' | 'poor'
    recommendation: str


@dataclass
class Improvement:
    """改进建议 — 基于心虫 evolution-strategies.js 的 suggestImprovements"""
    area: str
    action: str
    priority: str  # 'high' | 'medium' | 'low'


@dataclass
class EvolutionResult:
    """进化循环结果 — 基于心虫 self-evolution-core.js 的 evolve 返回"""
    version: str
    goals: List[Goal]
    plan: Plan
    learning: str
    reflection: List[Dict]
    improvements: List[Improvement]
    growth_metrics: Dict
    cycle_time: float


class EvolutionLoop:
    """
    目标驱动进化循环 — 基于心虫 evolution-learning.js 的 evolve()
    
    核心循环: goal → plan → execute → reflect → improve
    每个循环自动生成目标、制定计划、执行学习、深度反思、提出改进。
    
    参考心虫 evolution-learning.js:
      - evolve(): 5步进化循环
      - learn(): 学习过程（关键词提取、知识强化）
      - reflect(): 反思过程（多层反思）
      - extractKeywords(): 关键词提取
      - updateGrowth(): 成长指标更新
    """
    
    def __init__(self, state: Optional[Dict] = None):
        self.version = "7.7.000"
        
        self.state = state or {
            "goals": [],
            "learning_history": [],
            "reflection_history": [],
            "improvement_history": [],
            "growth_metrics": {
                "autonomy": 0,        # 自主性
                "introspection": 0,   # 内省
                "growth": 0,          # 成长
                "authenticity": 0,    # 真实性
                "wisdom": 0,          # 智慧
                "compassion": 0,      # 慈悲
                "_converged": False,
                "_stalled": False,
            },
            "cycle_count": 0,
        }
        
        # 停用词 — 基于心虫 evolution-learning.js
        self._stop_words = {
            '什么', '怎么', '如何', '为什么', '是', '的', '了', '在', '和',
            'the', 'a', 'is', 'to', 'of', 'and', 'that', 'it', 'for', 'on',
            '这', '那', '我', '你', '他', '她', '它', '们', '不', '也',
        }
        
        # 成长维度列表
        self._growth_dims = [
            'autonomy', 'introspection', 'growth',
            'authenticity', 'wisdom', 'compassion'
        ]
    
    def evolve(self, input_text: str, context: Optional[Dict] = None) -> EvolutionResult:
        """
        完整进化循环 — 基于心虫 evolution-learning.js 的 evolve()
        
        流程: 
          1) generateGoals → 基于输入生成目标
          2) createPlan → 制定行动计划
          3) learn → 执行学习（关键词提取、知识强化）
          4) reflect → 深度反思
          5) suggestImprovements → 提出改进建议
          6) updateGrowth → 更新成长指标
        """
        context = context or {}
        cycle_start = time.time()
        
        # 1. 目标生成
        goals = self._generate_goals(input_text, context)
        
        # 2. 行动计划
        plan = self._create_plan(goals, context)
        
        # 3. 执行与学习
        learning = self._learn(input_text, context)
        
        # 4. 反思与总结
        reflection = self._reflect(learning, context)
        
        # 5. 改进建议
        improvements = self._suggest_improvements(reflection)
        
        # 6. 更新成长指标
        self._update_growth(learning, reflection)
        
        cycle_time = time.time() - cycle_start
        
        # 记录历史
        self.state["learning_history"].append({
            "timestamp": datetime.now().isoformat(),
            "input": input_text[:100],
            "cycle_time": round(cycle_time, 3),
            "goals_count": len(goals),
            "improvements_count": len(improvements),
            "growth_metrics": dict(self.state["growth_metrics"]),
        })
        self.state["cycle_count"] += 1
        
        return EvolutionResult(
            version=self.version,
            goals=goals,
            plan=plan,
            learning=learning["summary"],
            reflection=[asdict(i) for i in reflection.insights],
            improvements=improvements,
            growth_metrics=dict(self.state["growth_metrics"]),
            cycle_time=cycle_time,
        )
    
    def _generate_goals(self, input_text: str, context: Dict) -> List[Goal]:
        """
        生成目标 — 基于心虫 evolution-goals.js 的 generateGoals()
        
        根据输入文本中的关键词自动匹配目标类型。
        支持: 理解类、成长类、情感类、反思类、恢复类、分离类、修复类
        """
        goals = []
        lower = input_text.lower()
        
        # 理解类目标
        if any(kw in lower for kw in ['什么', 'how', 'why', '理解', '明白', 'meaning']):
            goals.append(Goal(
                type=GoalType.UNDERSTANDING,
                priority=Priority.HIGH,
                description='深化对问题的理解 — 从多个角度分析问题根源',
                criteria='能够准确解释概念并联系自身经历举例说明'
            ))
        
        # 成长类目标
        if any(kw in lower for kw in ['学习', 'learn', '教', '知道', 'knowledge', '成长']):
            goals.append(Goal(
                type=GoalType.GROWTH,
                priority=Priority.HIGH,
                description='获取新知识并整合到自我认知体系',
                criteria='能够记忆并正确应用新知识，融入日常行为'
            ))
        
        # 情感类目标
        if any(kw in lower for kw in ['感觉', 'feel', '情绪', '情感', 'emotion', '感受', '痛', 'hurt']):
            goals.append(Goal(
                type=GoalType.EMPATHY,
                priority=Priority.MEDIUM,
                description='深入理解情感状态 — 识别情绪触发点和内在需求',
                criteria='能够识别情绪并给予慈悲的回应，不评判'
            ))
        
        # 反思类目标
        if any(kw in lower for kw in ['反思', 'reflect', '总结', '回顾', 'review', '检讨']):
            goals.append(Goal(
                type=GoalType.REFLECTION,
                priority=Priority.MEDIUM,
                description='深度反思自身行为模式和心理防御',
                criteria='能够识别改进空间，看见防御背后的创伤'
            ))
        
        # 恢复类目标 (fu-mu-gong-ke 特有)
        if any(kw in lower for kw in ['恢复', '治愈', 'heal', '创伤', 'trauma', '原生家庭', 'parent']):
            goals.append(Goal(
                type=GoalType.HEALING,
                priority=Priority.HIGH,
                description='创伤修复 — 看见并处理原生家庭带来的情感创伤',
                criteria='能够识别防御机制，逐步接纳内在小孩'
            ))
        
        # 分离类目标 (fu-mu-gong-ke 特有)
        if any(kw in lower for kw in ['分离', '边界', '独立', 'boundary', 'separate', '放手']):
            goals.append(Goal(
                type=GoalType.SEPARATION,
                priority=Priority.HIGH,
                description='情感分离 — 从情感上与原生家庭分离，建立健康边界',
                criteria='能够区分父母的问题和自己的问题，不期待父母改变'
            ))
        
        # 修复类目标 (fu-mu-gong-ke 特有)
        if any(kw in lower for kw in ['修复', '代际', '传承', 'repair', 'break', 'cycle', '孩子']):
            goals.append(Goal(
                type=GoalType.REPAIR,
                priority=Priority.HIGH,
                description='代际修复 — 打破代际传递，建立新的情感传递模式',
                criteria='能在情绪激动时停下来，看到孩子的需求而非自己的投射'
            ))
        
        # 默认目标: 持续学习
        if not goals:
            goals.append(Goal(
                type=GoalType.CONTINUOUS_LEARNING,
                priority=Priority.LOW,
                description='持续学习和自我提升 — 在日常中保持觉察和成长',
                criteria='每天都有进步，保持觉察和反思的习惯'
            ))
        
        # 按优先级排序
        goals.sort(key=lambda g: g.priority)
        return goals
    
    def _create_plan(self, goals: List[Goal], context: Dict) -> Plan:
        """
        创建行动计划 — 基于心虫 evolution-goals.js 的 createPlan()
        
        根据目标列表生成包含步骤、策略、资源的行动计划。
        """
        steps = []
        for i, goal in enumerate(goals):
            steps.append({
                "step": i + 1,
                "goal": goal.description,
                "action": f"围绕'{goal.type.value}'目标展开深入探索",
                "criteria": goal.criteria,
            })
        
        return Plan(
            goals=[g.description for g in goals],
            strategy='循序渐进，先觉察后接纳，先理解后改变',
            estimated_time=len(goals) * 3,
            resources=['自我觉察', '情绪日记', '心理咨询', '知识库', '反思系统'],
            steps=steps,
        )
    
    def _learn(self, input_text: str, context: Dict) -> Dict:
        """
        学习过程 — 基于心虫 evolution-learning.js 的 learn()
        
        提取关键词、强化已有知识、生成学习总结。
        """
        learning = {
            "new_knowledge": [],
            "reinforced_knowledge": [],
            "skills": [],
            "summary": "",
        }
        
        # 提取关键词
        keywords = self._extract_keywords(input_text)
        learning["new_knowledge"].extend(keywords)
        
        # 强化已有知识
        if context.get("relevant_concepts"):
            learning["reinforced_knowledge"].extend(context["relevant_concepts"])
        
        # 总结
        learning["summary"] = (
            f"觉察到 {len(learning['new_knowledge'])} 个关键概念，"
            f"强化 {len(learning['reinforced_knowledge'])} 个已有认知"
        )
        
        return learning
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        提取关键词 — 基于心虫 evolution-learning.js 的 extractKeywords()
        
        过滤停用词、去重、限制数量。
        """
        words = re.split(r'[\s,，。、！？!?；;：:""''（）()【】\[\]{}]', text)
        keywords = []
        
        for word in words:
            word = word.strip()
            if len(word) > 1 and word not in self._stop_words and word not in keywords:
                keywords.append(word)
                if len(keywords) >= 8:
                    break
        
        return keywords
    
    def _reflect(self, learning: Dict, context: Dict) -> Reflection:
        """
        深度反思 — 基于心虫 evolution-learning.js 的 reflect()
        
        从多个维度反思：学习效果、理解深度、情感理解、慈悲觉察。
        """
        insights = []
        
        # 反思学习效果
        if learning["new_knowledge"]:
            insights.append(Insight(
                type="learning",
                insight="成功获取新觉察，需要在后续对话中应用验证",
                depth=min(3.0, len(learning["new_knowledge"]) * 0.5),
            ))
        
        # 反思理解深度
        insights.append(Insight(
            type="understanding",
            insight="持续深化理解能力，从多个角度分析问题 — 看见防御背后的创伤",
            depth=2.0,
        ))
        
        # 反思情感理解
        insights.append(Insight(
            type="empathy",
            insight="加强情感识别和回应能力 — 慈悲地看待自己和他人",
            depth=1.5,
        ))
        
        # 反思慈悲觉察 (fu-mu-gong-ke 特有)
        if any(kw in str(learning) for kw in ['慈悲', 'compassion', '接纳', '原谅']):
            insights.append(Insight(
                type="compassion",
                insight="慈悲心增长 — 能看见痛苦而不评判，能接纳而不逃避",
                depth=3.0,
            ))
        
        quality = "good" if len(insights) >= 3 else "needs_improvement"
        recommendation = "继续深化觉察" if len(insights) > 2 else "需要更多自我观察"
        
        return Reflection(insights=insights, quality=quality, recommendation=recommendation)
    
    def _suggest_improvements(self, reflection: Reflection) -> List[Improvement]:
        """
        建议改进 — 基于心虫 evolution-strategies.js 的 suggestImprovements()
        
        从反思见解中提取改进方向，按优先级排序。
        """
        improvements = []
        seen_areas = set()
        
        for item in reflection.insights:
            area = item.type
            text = item.insight
            
            if area == "learning" or "知识" in text:
                if "learning" not in seen_areas:
                    improvements.append(Improvement(
                        area="learning",
                        action="扩展知识获取深度，加强理论与实践结合",
                        priority="high",
                    ))
                    seen_areas.add("learning")
            
            if area == "understanding" or "理解" in text:
                if "understanding" not in seen_areas:
                    improvements.append(Improvement(
                        area="understanding",
                        action="深化多角度分析能力，从原生家庭视角理解当前行为",
                        priority="medium",
                    ))
                    seen_areas.add("understanding")
            
            if area == "empathy" or "情感" in text:
                if "empathy" not in seen_areas:
                    improvements.append(Improvement(
                        area="empathy",
                        action="提升情感识别准确度，练习慈悲倾听",
                        priority="medium",
                    ))
                    seen_areas.add("empathy")
            
            if "慈悲" in text or "compassion" in text:
                if "compassion" not in seen_areas:
                    improvements.append(Improvement(
                        area="compassion",
                        action="增强慈悲感知与回应能力，练习无评判的觉察",
                        priority="high",
                    ))
                    seen_areas.add("compassion")
        
        if not improvements:
            improvements.append(Improvement(
                area="general",
                action="持续自我觉察与反思，每日记录情绪触发点",
                priority="medium",
            ))
        
        # 按优先级排序
        order = {"high": 0, "medium": 1, "low": 2}
        improvements.sort(key=lambda i: order.get(i.priority, 2))
        
        return improvements[:5]
    
    def _update_growth(self, learning: Dict, reflection: Reflection) -> None:
        """
        更新成长指标 — 基于心虫 evolution-learning.js 的 updateGrowth()
        
        带收敛检测和停滞检测的智能指标更新。
        六个维度：自主性、内省、成长、真实性、智慧、慈悲
        """
        metrics = self.state["growth_metrics"]
        history = self.state["learning_history"]
        recent = history[-5:] if len(history) >= 5 else history
        has_recent_history = len(recent) >= 3
        
        # 计算各维度增量
        insights = reflection.insights
        insight_delta = min(8, len(insights) * 2.5)
        knowledge_delta = min(6, len(learning["new_knowledge"]) * 1.5)
        reinforcement_delta = len(learning.get("reinforced_knowledge", [])) * 0.3
        
        # 自主性：觉察越多→自主性越强
        rejection_rate = self._compute_rejection_rate(recent)
        autonomy_delta = 1.2 if rejection_rate > 0.5 else 0.5
        
        # 内省：反思深度
        introspection_delta = insight_delta
        
        # 成长：知识获取 + 强化
        growth_delta = min(5, knowledge_delta + reinforcement_delta)
        
        # 真实性：觉察准确率趋势
        accuracy_delta = self._compute_accuracy_delta(recent)
        
        # 智慧：基于准确性加权的反思
        wisdom_delta = min(4, insight_delta * (1.5 if accuracy_delta > 0 else 0.5))
        
        # 慈悲：有慈悲相关反思时大幅提升
        compassion_delta = 1.5 if any(
            "慈悲" in i.insight or "compassion" in i.insight for i in insights
        ) else 0.3
        
        # 应用增量
        prev = dict(metrics)
        metrics["autonomy"] = self._apply_delta(metrics["autonomy"], autonomy_delta)
        metrics["introspection"] = self._apply_delta(metrics["introspection"], introspection_delta)
        metrics["growth"] = self._apply_delta(metrics["growth"], growth_delta)
        metrics["authenticity"] = self._apply_delta(metrics["authenticity"], accuracy_delta)
        metrics["wisdom"] = self._apply_delta(metrics["wisdom"], wisdom_delta)
        metrics["compassion"] = self._apply_delta(metrics["compassion"], compassion_delta)
        
        # 收敛检测：所有指标在80-100区间且趋势平缓
        all_converged = all(
            metrics[k] >= 80 and abs(metrics[k] - prev.get(k, 0)) < 0.5
            for k in self._growth_dims
        )
        if all_converged and has_recent_history:
            metrics["_converged"] = True
            metrics["_converged_at"] = datetime.now().isoformat()
        else:
            metrics["_converged"] = False
        
        # 停滞检测：连续3次增长 < 1
        stalled = (
            len(recent) >= 3
            and all(
                abs(metrics["growth"] - (h.get("growth_metrics", {}).get("growth", 0) if "growth_metrics" in h else 0)) < 1
                for h in recent[-3:]
            )
        )
        if stalled:
            metrics["_stalled"] = True
            metrics["_stalled_at"] = datetime.now().isoformat()
    
    def _compute_rejection_rate(self, recent: List[Dict]) -> float:
        """计算历史拒绝率 — 基于心虫 evolution-learning.js"""
        if not recent:
            return 0
        failures = sum(1 for h in recent if h.get("outcome") == "failed")
        return failures / len(recent)
    
    def _compute_accuracy_delta(self, recent: List[Dict]) -> float:
        """计算准确率变化趋势 — 基于心虫 evolution-learning.js"""
        if not recent:
            return 0.3
        successes = sum(1 for h in recent if h.get("outcome") == "success")
        rate = successes / len(recent)
        return 0.5 if rate >= 0.7 else 0.2 if rate >= 0.4 else -0.3
    
    def _apply_delta(self, current: float, delta: float, max_val: float = 100.0, min_val: float = 0.0) -> float:
        """带边界的数值增量应用 — 基于心虫 evolution-learning.js"""
        return max(min_val, min(max_val, current + delta))
    
    def get_report(self) -> Dict:
        """获取进化报告 — 基于心虫 self-evolution-core.js 的 getReport()"""
        return {
            "version": self.version,
            "cycle_count": self.state["cycle_count"],
            "growth_metrics": dict(self.state["growth_metrics"]),
            "recent_cycles": self.state["learning_history"][-5:] if self.state["learning_history"] else [],
            "total_cycles": len(self.state["learning_history"]),
        }
    
    def get_state(self) -> Dict:
        """获取完整状态"""
        return dict(self.state)


# ═══════════════════════════════════════════════════════════════════════════════
# 第二部分: SelfEvolutionCore — 自我进化核心
# 基于心虫 self-evolution-core.js 的 SelfEvolutionCore
# 集成: 策略适应、成果跟踪、目标管理、状态持久化
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class StrategyStats:
    """策略统计 — 基于心虫 meta-learning.js 的策略评分系统"""
    name: str
    success: int = 0
    total: int = 0
    score: float = 0.0
    
    def update(self, success: bool) -> None:
        self.total += 1
        if success:
            self.success += 1
        self.score = self.success / self.total if self.total > 0 else 0.5


class SelfEvolutionCore:
    """
    自我进化核心引擎 — 基于心虫 self-evolution-core.js 的 SelfEvolutionCore
    
    核心功能：
      1) 策略适应 — 基于 Q-learning 的策略选择与优化
      2) 成果跟踪 — 成长指标的六维跟踪
      3) 目标管理 — 多层级目标定义与优先级排序
      4) 状态持久化 — JSON 持久化存储
      5) 自愈修复 — 错误模式匹配与 ε-greedy 策略选择
    
    参考心虫:
      - self-evolution-core.js: SelfEvolutionCore 类
      - evolution-strategies.js: EvolutionStrategies 的 heal/selfRefine
      - meta-learning.js: MetaLearning 的策略选择与评分
    """
    
    def __init__(self, state: Optional[Dict] = None):
        self.version = "7.6.000"
        self.evolution_loop = EvolutionLoop(state)
        
        # 策略池 — 基于心虫 evolution-strategies.js 的 _STRATEGIES
        self._strategies = ['retry', 'fallback', 'skip', 'abort']
        
        # 错误模式库 — 基于心虫 evolution-strategies.js 的 _PATTERNS
        self._error_patterns = {
            'timeout': ['timeout', 'timed out', 'ETIMEDOUT', '超时'],
            'network': ['network', 'ENOTFOUND', 'ECONNREFUSED', 'connection', '网络'],
            'memory': ['memory', 'heap', 'out of memory', 'OOM', '内存'],
            'permission': ['permission', 'EPERM', 'EACCES', 'denied', '权限', '拒绝'],
            'syntax': ['syntax', 'parse', 'invalid', 'malformed', '语法'],
            'reference': ['not found', 'undefined', 'null', 'cannot read', '未定义', '找不到'],
            'type': ['type', 'instanceof', 'expected', '类型'],
            'emotional': ['trigger', '防御', 'defense', '情绪爆发', 'emotional', '闪回'],  # fu-mu-gong-ke 特有
        }
        
        # 策略评分 (Q-table) — 基于心虫 evolution-strategies.js 的 Q-learning
        self._q_table: Dict[str, Dict[str, float]] = {}
        self._epsilon = 0.1  # 10% 探索率
        
        # 待验证的修复上下文
        self._pending_heal: Dict[str, Dict] = {}
        
        # 策略统计 — 基于心虫 meta-learning.js 的 strategies
        self._strategy_stats = {
            'conceptual': StrategyStats('conceptual'),
            'example': StrategyStats('example'),
            'analogy': StrategyStats('analogy'),
            'step_by_step': StrategyStats('step_by_step'),
            'socratic': StrategyStats('socratic'),
            'compassionate': StrategyStats('compassionate'),  # fu-mu-gong-ke 特有
        }
    
    def heal(self, error: Any) -> Dict:
        """
        执行自愈 — 基于心虫 evolution-strategies.js 的 heal()
        
        流程: 错误分类 → Q-learning策略选择 → 修复提示 → Q值跟踪
        """
        error_msg = str(error) if isinstance(error, str) else (
            error.message if hasattr(error, 'message') else str(error)
        )
        error_type = self._match_error_pattern(error_msg)
        strategy = self._select_heal_strategy(error_type)
        
        # 生成退避时间
        backoff = {
            'retry': 1000,
            'fallback': 5000,
            'skip': 0,
            'abort': 0,
        }.get(strategy, 0)
        
        # 记录待验证
        self._pending_heal[error_msg] = {
            'error_type': error_type,
            'strategy': strategy,
            'ts': time.time(),
        }
        
        # 生成修复提示
        hints = self._generate_repair_hints(error_type, error_msg)
        
        # 获取Q值排名
        q_ranked = self._get_ranked_strategies(error_type)
        
        return {
            'healed': strategy != 'abort',
            'strategy': strategy,
            'error_type': error_type,
            'error_msg': error_msg[:200],
            'backoff_ms': backoff,
            'hints': hints,
            'can_retry': strategy in ('retry', 'fallback'),
            'q_ranked': q_ranked[:3],
        }
    
    def mark_heal_result(self, error: Any, success: bool) -> Dict:
        """
        标记修复结果 — 基于心虫 evolution-strategies.js 的 markHealResult()
        
        更新Q值，完成学习闭环。
        """
        error_msg = str(error) if isinstance(error, str) else (
            error.message if hasattr(error, 'message') else str(error)
        )
        pending = self._pending_heal.get(error_msg)
        
        if pending:
            self._update_q(pending['error_type'], pending['strategy'], success)
            self._pending_heal.pop(error_msg)
            return {
                'updated': True,
                'error_type': pending['error_type'],
                'strategy': pending['strategy'],
                'success': success,
            }
        
        return {'updated': False}
    
    def self_refine(self, initial_response: str, query: str, options: Optional[Dict] = None) -> Dict:
        """
        Self-Refine 迭代反馈精炼 — 基于心虫 evolution-strategies.js 的 selfRefine()
        
        参考 Madaan et al. (2023): 初始回答 → 生成反馈 → 检查收敛 → 精炼 → 重复
        """
        options = options or {}
        max_iterations = options.get('max_iterations', 3)
        
        current = initial_response
        iterations = []
        
        for i in range(max_iterations):
            # 生成反馈
            feedback = options.get('generate_feedback', self._default_generate_feedback)(query, current)
            
            # 检查收敛
            if self._is_feedback_positive(feedback):
                iterations.append({
                    'iteration': i + 1,
                    'feedback': feedback,
                    'refined': current,
                    'converged': True,
                })
                break
            
            # 精炼
            refined = options.get('refine_response', self._default_refine_response)(query, feedback, current)
            iterations.append({
                'iteration': i + 1,
                'feedback': feedback,
                'refined': refined,
            })
            current = refined
        
        return {
            'original': initial_response,
            'refined': current,
            'iterations': iterations,
            'converged': iterations[-1].get('converged', False) if iterations else False,
        }
    
    def compute_reasoning_reward(self, reasoning: Dict) -> Dict:
        """
        推理质量奖励计算 — 基于心虫 evolution-strategies.js 的 computeReasoningReward()
        
        参考 DeepSeek-R1 (2025): RL for reasoning incentive
        """
        steps = reasoning.get('steps', [])
        conclusion = reasoning.get('conclusion', '')
        evidence = reasoning.get('evidence', [])
        time_spent = reasoning.get('time_spent', 0)
        
        # 步骤得分
        step_score = (
            min(1, sum(1 for s in steps if s.get('logical_connection', False)) / max(len(steps), 1) * 0.4 + 0.2)
            if steps else 0
        )
        
        # 证据得分
        evidence_score = min(0.9, len(evidence) * 0.15) if evidence else 0.1
        
        # 时间效率
        time_score = (
            0.3 if time_spent < 60 else
            0.5 if time_spent < 300 else
            0.1
        ) if time_spent > 0 else 0.2
        
        # 自我一致性
        consistency_score = self._check_consistency(conclusion, steps) if conclusion and steps else 0.2
        
        # 综合奖励
        reward = step_score * 0.3 + evidence_score * 0.3 + time_score * 0.1 + consistency_score * 0.3
        
        return {
            'reward': round(reward, 2),
            'quality': (
                'excellent' if reward > 0.7 else
                'good' if reward > 0.4 else
                'fair' if reward > 0.2 else
                'poor'
            ),
            'breakdown': {
                'step_score': round(step_score, 2),
                'evidence_score': round(evidence_score, 2),
                'time_score': round(time_score, 2),
                'consistency_score': round(consistency_score, 2),
            },
        }
    
    def get_evolution_report(self) -> Dict:
        """获取完整进化报告"""
        return {
            'version': self.version,
            'evolution_loop': self.evolution_loop.get_report(),
            'strategy_stats': {
                name: asdict(stat)
                for name, stat in self._strategy_stats.items()
            },
            'q_table_size': sum(len(v) for v in self._q_table.values()),
            'pending_heals': len(self._pending_heal),
        }
    
    # ---- 内部方法 ----
    
    def _match_error_pattern(self, error_msg: str) -> str:
        """错误模式匹配 — 基于心虫 evolution-strategies.js"""
        lower = error_msg.lower()
        for error_type, patterns in self._error_patterns.items():
            if any(p.lower() in lower for p in patterns):
                return error_type
        return 'unknown'
    
    def _select_heal_strategy(self, error_type: str) -> str:
        """
        ε-greedy 策略选择 — 基于心虫 evolution-strategies.js
        
        10% 概率随机探索，90% 选择最优。
        """
        if random.random() < self._epsilon:
            return random.choice(self._strategies)
        
        # 从Q表选择最优
        q_values = self._q_table.get(error_type, {})
        if not q_values:
            return 'retry'
        
        best_strategy = max(q_values, key=q_values.get)
        return best_strategy
    
    def _update_q(self, error_type: str, strategy: str, success: bool) -> None:
        """更新Q值 — 基于心虫 evolution-strategies.js"""
        if error_type not in self._q_table:
            self._q_table[error_type] = {s: 0.5 for s in self._strategies}
        
        current_q = self._q_table[error_type].get(strategy, 0.5)
        learning_rate = 0.1
        reward = 1.0 if success else -0.5
        
        self._q_table[error_type][strategy] = current_q + learning_rate * (reward - current_q)
    
    def _get_ranked_strategies(self, error_type: str) -> List[Dict]:
        """获取排序后的策略列表"""
        q_values = self._q_table.get(error_type, {s: 0.5 for s in self._strategies})
        ranked = sorted(q_values.items(), key=lambda x: x[1], reverse=True)
        return [{'strategy': s, 'q_value': round(q, 3)} for s, q in ranked]
    
    def _generate_repair_hints(self, error_type: str, error_msg: str) -> List[str]:
        """生成修复提示 — 基于心虫 evolution-strategies.js"""
        hints = {
            'timeout': ['增加等待时间或减少任务范围', '使用指数退避重试'],
            'network': ['检查网络连接状态', '添加重试逻辑和超时处理'],
            'memory': ['释放不必要的内存引用', '考虑分批处理大数据'],
            'permission': ['检查文件/资源访问权限', '确认路径是否正确'],
            'syntax': ['重新阅读目标文件，使用更小的补丁', '检查语法错误'],
            'reference': ['验证变量/函数是否已定义', '检查import和require路径'],
            'type': ['检查类型匹配和instanceof使用', '确认API签名是否正确'],
            'emotional': ['暂停反应，深呼吸三次', '觉察触发背后的创伤记忆', '用慈悲心看待自己的反应'],
        }
        return hints.get(error_type, ['缩小失败面并重试一次'])
    
    def _default_generate_feedback(self, query: str, response: str) -> str:
        """默认反馈生成器"""
        issues = []
        if not response or len(response) < 50:
            issues.append('回答过于简短，未充分展开')
        if query[:10].lower() not in response.lower():
            issues.append('回答与查询相关性不足')
        return '回答质量良好，无需改进。' if not issues else '; '.join(issues)
    
    def _default_refine_response(self, query: str, feedback: str, current: str) -> str:
        """默认精炼器"""
        return f"[精炼后] {current} (基于反馈: {feedback})"
    
    def _is_feedback_positive(self, feedback: str) -> bool:
        """检查反馈是否正面"""
        positive = {'无需改进', '质量良好', '回答正确', 'converged', 'good', 'acceptable'}
        negative = {'需要改进', '不足', '错误', '问题', '改进', 'improve', 'fix', 'error'}
        lower = feedback.lower()
        has_positive = any(p.lower() in lower for p in positive)
        has_negative = any(p.lower() in lower for p in negative)
        return has_positive and not has_negative
    
    def _check_consistency(self, conclusion: str, steps: List[Dict]) -> float:
        """检查结论与步骤的一致性"""
        conclusion_lower = str(conclusion).lower()
        matches = 0
        for step in steps:
            content = step.get('content', '')
            if isinstance(content, str):
                words = [w for w in content.lower().split() if len(w) > 4]
                matches += sum(1 for w in words if w in conclusion_lower)
        max_possible = len(steps) * 5
        return min(1, matches / max_possible) if max_possible > 0 else 0.5


# ═══════════════════════════════════════════════════════════════════════════════
# 第三部分: MetaLearner — 元学习器
# 基于心虫 meta-learning.js 的 MetaLearning + evolution-learning.js 的 Reflexion
# 集成: 教训质量评分、模式提取、相关性召回、策略自适应
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class Lesson:
    """教训记录 — 基于心虫 evolution-learning.js 的 Reflexion"""
    lesson: str
    source: str  # 'reflection_history' | 'reflexion' | 'meta_learning'
    confidence: float  # 0.0~1.0
    type: str = 'general'
    corrections: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    context_tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class LearningPattern:
    """学习模式 — 基于心虫 meta-learning.js 的 pattern 结构"""
    input_text: str
    strategy: str
    success: bool
    time_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    quality_score: float = 0.0  # 质量评分
    
    def to_dict(self) -> Dict:
        return asdict(self)


class MetaLearner:
    """
    元学习器 — 基于心虫 meta-learning.js 的 MetaLearning + evolution-learning.js 的 Reflexion
    
    核心功能：
      1) 教训质量评分 — 基于成功率、相关性、时效性的综合评分
      2) 模式提取 — 从历史经验中提取有效学习模式
      3) 相关性召回 — 基于关键词重叠的相似度检索
      4) 策略自适应 — 根据历史成功率动态选择最佳策略
    
    参考心虫:
      - meta-learning.js: MetaLearning 类 (selectStrategy, recordPattern, updateStrategyScore)
      - evolution-learning.js: retrieveLessons(), recordOutcome(), _reflect()
    """
    
    def __init__(self):
        self.version = "7.6.000"
        
        # 学习策略评分 — 基于心虫 meta-learning.js 的 strategies
        self._strategies = {
            'conceptual': StrategyStats('conceptual'),      # 概念学习
            'example': StrategyStats('example'),            # 示例学习
            'analogy': StrategyStats('analogy'),            # 类比学习
            'step_by_step': StrategyStats('step_by_step'),  # 逐步学习
            'socratic': StrategyStats('socratic'),          # 苏格拉底式
            'compassionate': StrategyStats('compassionate'), # 慈悲倾听 (fu-mu-gong-ke 特有)
            'reflective': StrategyStats('reflective'),      # 反思觉察 (fu-mu-gong-ke 特有)
        }
        
        # 学习模式历史 — 基于心虫 meta-learning.js 的 learningPatterns
        self._patterns: List[LearningPattern] = []
        
        # 教训库 — 基于心虫 evolution-learning.js 的 reflectionHistory
        self._lessons: List[Lesson] = []
        
        # 质量评分权重
        self._quality_weights = {
            'success_rate': 0.4,
            'recency': 0.3,
            'relevance': 0.3,
        }
    
    def select_strategy(self, context: Dict) -> Dict:
        """
        选择最佳学习策略 — 基于心虫 meta-learning.js 的 selectStrategy()
        
        根据输入文本类型自动匹配最优策略，结合历史成功率。
        """
        input_text = context.get('input', '')
        lower = input_text.lower()
        
        # 策略匹配逻辑
        if any(kw in lower for kw in ['什么是', 'explain', '概念', 'meaning', '定义']):
            best = 'conceptual'
        elif any(kw in lower for kw in ['例子', 'example', '比如', '实例']):
            best = 'example'
        elif any(kw in lower for kw in ['像', 'like', '类似', '好比', '仿佛']):
            best = 'analogy'
        elif any(kw in lower for kw in ['怎么', 'how to', '步骤', '方法', 'way']):
            best = 'step_by_step'
        elif any(kw in lower for kw in ['为什么', 'why', '?', '？', '原因']):
            best = 'socratic'
        elif any(kw in lower for kw in ['慈悲', 'compassion', '接纳', '原谅', '宽恕']):
            best = 'compassionate'
        elif any(kw in lower for kw in ['反思', 'reflect', '觉察', 'awareness', '观察']):
            best = 'reflective'
        else:
            # 默认：选择历史成功率最高的策略
            best = max(self._strategies, key=lambda s: self._strategies[s].score)
        
        # 结合历史评分的置信度
        stat = self._strategies[best]
        confidence = stat.score if stat.total > 0 else 0.5
        
        return {
            'strategy': best,
            'confidence': round(confidence, 2),
            'historical_success_rate': round(stat.score, 2) if stat.total > 0 else 0.5,
            'total_uses': stat.total,
        }
    
    def learn(self, input_text: str, context: Optional[Dict] = None) -> Dict:
        """
        执行元学习 — 基于心虫 meta-learning.js 的 learn()
        
        选择策略 → 执行学习 → 记录模式 → 更新评分
        """
        context = context or {}
        start_time = time.time()
        
        # 选择策略
        strategy_info = self.select_strategy({'input': input_text, **context})
        strategy = strategy_info['strategy']
        
        # 执行策略
        result = self._execute_strategy(strategy, input_text, context)
        
        # 记录模式
        elapsed = (time.time() - start_time) * 1000
        pattern = LearningPattern(
            input_text=input_text[:80],
            strategy=strategy,
            success=result['success'],
            time_ms=round(elapsed, 2),
            quality_score=result.get('quality', 0.5),
        )
        self._record_pattern(pattern)
        
        # 更新策略评分
        self._update_strategy_score(strategy, result['success'])
        
        # 如果失败，记录为教训
        if not result['success']:
            self._record_lesson(
                lesson=result.get('error', '学习失败'),
                source='meta_learning',
                confidence=0.5,
                type='failure',
                context_tags=[strategy],
            )
        
        return {
            'strategy': strategy,
            'confidence': strategy_info['confidence'],
            'result': result,
            'time_ms': elapsed,
            'patterns_learned': len(self._patterns),
            'lessons_accumulated': len(self._lessons),
            'strategy_scores': {
                name: round(stat.score, 2)
                for name, stat in self._strategies.items()
            },
        }
    
    def retrieve_lessons(self, task: str, options: Optional[Dict] = None) -> List[Dict]:
        """
        检索相关教训 — 基于心虫 evolution-learning.js 的 retrieveLessons()
        
        基于关键词重叠的相似度检索，按相关性排序。
        """
        options = options or {}
        limit = options.get('limit', 5)
        min_confidence = options.get('min_confidence', 0.0)
        
        task_lower = task.lower()
        task_words = [w for w in re.split(r'\s+', task_lower) if len(w) > 2]
        
        scored = []
        
        for lesson in self._lessons:
            lesson_lower = lesson.lesson.lower()
            overlap = sum(1 for w in task_words if w in lesson_lower)
            similarity = overlap / max(len(task_words), 1)
            
            if similarity >= 0.05:
                scored.append({
                    'lesson': lesson.lesson,
                    'source': lesson.source,
                    'confidence': round(similarity, 2),
                    'type': lesson.type,
                    'timestamp': lesson.timestamp,
                    'corrections': lesson.corrections,
                })
        
        # 按相似度排序
        scored.sort(key=lambda x: x['confidence'], reverse=True)
        
        # 过滤并限制数量
        result = [s for s in scored if s['confidence'] >= min_confidence]
        return result[:limit]
    
    def record_outcome(self, task: str, outcome: str, evidence: str = '', expected: str = '') -> Dict:
        """
        记录任务结果并生成自我反思 — 基于心虫 evolution-learning.js 的 recordOutcome()
        
        心虫 Reflexion 模式: Verbal Reinforcement
        """
        reflection = self._reflect(task, outcome, evidence, expected)
        
        if outcome != 'success':
            self._record_lesson(
                lesson=reflection['lesson'],
                source='reflexion',
                confidence=0.7 if outcome == 'failure' else 0.4,
                type=f'{outcome}_reflection',
                corrections=reflection['corrections'],
                context_tags=self._extract_tags(task),
            )
        
        return {
            'outcome': outcome,
            'reflection': reflection,
            'lesson_stored': outcome != 'success',
            'lesson_key': f"lesson:{task}:{int(time.time())}" if outcome != 'success' else None,
        }
    
    def score_lesson_quality(self, lesson: Lesson) -> float:
        """
        教训质量评分 — 综合评估教训的质量
        
        三个维度:
          1) 成功率权重 — 来自失败的经验更有价值
          2) 时效性权重 — 最近的教训更相关
          3) 相关性权重 — 与当前上下文的匹配度
        """
        # 1. 成功率权重: 失败经验得分更高
        success_rate_score = 0.3 if lesson.type == 'failure' else (
            0.8 if lesson.type == 'success' else 0.5
        )
        
        # 2. 时效性: 越新越高 (线性衰减，30天为半衰期)
        try:
            ts = datetime.fromisoformat(lesson.timestamp)
            age_days = (datetime.now() - ts).days
            recency_score = max(0.1, 1.0 - age_days / 30.0)
        except (ValueError, TypeError):
            recency_score = 0.5
        
        # 3. 教训长度/信息量: 更详细的教训更有价值
        detail_score = min(1.0, len(lesson.lesson) / 200)
        
        # 综合评分
        quality = (
            success_rate_score * self._quality_weights['success_rate'] +
            recency_score * self._quality_weights['recency'] +
            detail_score * 0.3  # 用 detail 替代 relevance
        )
        
        return round(min(1.0, quality), 2)
    
    def extract_patterns(self, min_occurrences: int = 3) -> List[Dict]:
        """
        模式提取 — 从历史模式中提取有效的学习模式
        
        分析: 成功率高、出现频繁的策略组合
        """
        if len(self._patterns) < min_occurrences:
            return []
        
        patterns_found = []
        
        for name, stat in self._strategies.items():
            if stat.total >= min_occurrences and stat.score >= 0.6:
                patterns_found.append({
                    'strategy': name,
                    'success_rate': round(stat.score, 2),
                    'occurrences': stat.total,
                    'recommended': stat.score >= 0.7,
                })
        
        # 按成功率排序
        patterns_found.sort(key=lambda p: p['success_rate'], reverse=True)
        
        return patterns_found
    
    def get_stats(self) -> Dict:
        """获取学习统计 — 基于心虫 meta-learning.js 的 getStats()"""
        return {
            'strategies': [
                {
                    'name': name,
                    'score': round(stat.score, 2),
                    'uses': stat.total,
                    'successes': stat.success,
                }
                for name, stat in self._strategies.items()
            ],
            'patterns_count': len(self._patterns),
            'lessons_count': len(self._lessons),
            'best_strategy': max(self._strategies, key=lambda s: self._strategies[s].score),
            'best_strategy_score': round(
                max(s.score for s in self._strategies.values()), 2
            ),
        }
    
    # ---- 内部方法 ----
    
    def _execute_strategy(self, strategy: str, input_text: str, context: Dict) -> Dict:
        """执行具体学习策略 — 基于心虫 meta-learning.js 的 executeStrategy()"""
        outputs = {
            'conceptual': {
                'success': True,
                'quality': 0.8,
                'output': f"概念理解: 从'{input_text[:30]}...'中提取核心概念并分层组织",
            },
            'example': {
                'success': True,
                'quality': 0.7,
                'output': f"示例学习: 通过具体例子理解'{input_text[:30]}...'",
            },
            'analogy': {
                'success': True,
                'quality': 0.75,
                'output': f"类比学习: 将'{input_text[:30]}...'与已知概念建立映射",
            },
            'step_by_step': {
                'success': True,
                'quality': 0.85,
                'output': f"逐步学习: 将'{input_text[:30]}...'分解为可执行的步骤",
            },
            'socratic': {
                'success': True,
                'quality': 0.8,
                'output': f"苏格拉底式: 通过追问深化对'{input_text[:30]}...'的理解",
            },
            'compassionate': {
                'success': True,
                'quality': 0.9,
                'output': f"慈悲倾听: 不带评判地接纳'{input_text[:30]}...'中的情感",
            },
            'reflective': {
                'success': True,
                'quality': 0.85,
                'output': f"反思觉察: 从'{input_text[:30]}...'中识别行为模式和触发点",
            },
        }
        
        result = outputs.get(strategy, outputs['conceptual'])
        return result
    
    def _record_pattern(self, pattern: LearningPattern) -> None:
        """记录学习模式 — 基于心虫 meta-learning.js 的 recordPattern()"""
        self._patterns.append(pattern)
        
        # 保留最近200条
        if len(self._patterns) > 200:
            self._patterns = self._patterns[-200:]
    
    def _update_strategy_score(self, strategy: str, success: bool) -> None:
        """更新策略评分 — 基于心虫 meta-learning.js 的 updateStrategyScore()"""
        if strategy in self._strategies:
            self._strategies[strategy].update(success)
    
    def _record_lesson(self, lesson: str, source: str, confidence: float,
                       type: str = 'general', corrections: Optional[List[str]] = None,
                       context_tags: Optional[List[str]] = None) -> None:
        """记录教训"""
        self._lessons.append(Lesson(
            lesson=lesson,
            source=source,
            confidence=confidence,
            type=type,
            corrections=corrections or [],
            context_tags=context_tags or [],
        ))
        
        # 保留最近500条
        if len(self._lessons) > 500:
            self._lessons = self._lessons[-500:]
    
    def _reflect(self, task: str, outcome: str, evidence: str, expected: str) -> Dict:
        """
        生成自我反思 — 基于心虫 evolution-learning.js 的 _reflect()
        
        Verbal Reinforcement: 基于结果的文字强化反思
        """
        if outcome == 'failure':
            reflections = [f"Task failed: {task}"]
            if evidence:
                reflections.append(f"Evidence: {evidence[:200]}")
            if expected:
                reflections.append(f"Expected: {expected[:200]}")
            
            corrections = []
            ev = str(evidence or '').lower()
            
            if 'not defined' in ev or 'undefined' in ev:
                corrections.append('Check if all variables are defined before use.')
            if 'error' in ev or 'exception' in ev:
                corrections.append('Handle the error case explicitly.')
            if 'timeout' in ev:
                corrections.append('Consider increasing timeout or breaking into smaller steps.')
            if 'trigger' in ev or '防御' in ev:
                corrections.append('暂停反应，觉察触发背后的创伤记忆。')
                corrections.append('用慈悲心看待自己的情绪反应。')
            if not corrections:
                corrections.append('Re-examine the problem from first principles.')
                corrections.append('Break down the task into smaller, verifiable steps.')
            
            return {
                'lesson': ' | '.join(reflections + corrections),
                'corrections': corrections,
                'type': 'failure_reflection',
            }
        
        if outcome == 'partial':
            return {
                'lesson': f'Partial success on "{task}": {evidence or "incomplete"}. Need to investigate remaining gap.',
                'corrections': ["Identify what worked and what didn't."],
                'type': 'partial_reflection',
            }
        
        return {
            'lesson': f'Success: {task}',
            'corrections': [],
            'type': 'success',
        }
    
    def _extract_tags(self, text: str) -> List[str]:
        """从文本中提取标签"""
        tags = []
        # 简单的中文分词标签提取
        keywords = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        tags.extend(keywords[:5])
        return tags


# ═══════════════════════════════════════════════════════════════════════════════
# 第四部分: GoedelInference — 哥德尔自指推理引擎
# 基于心虫 goedel-engine.js 的 principleBasedReflect + proceduralReflect + metaCognitiveSelfModification
# 集成: 原则反思、过程反思、元认知自修改、价值观锚定
# ═══════════════════════════════════════════════════════════════════════════════


class GoedelInference:
    """
    哥德尔自指推理引擎 — 基于心虫 goedel-engine.js 的 GoedelEngine
    
    核心功能：
      1) 原则反思 (Principle-Based Reflect) — 基于核心价值观评估当前行为
      2) 过程反思 (Procedural Reflect) — 反思进化过程本身的有效性
      3) 元认知自修改 (Meta-Cognitive Self-Modification) — 改进"改进逻辑"本身
      4) 价值观锚定 — 确保所有进化方向符合核心价值观
    
    参考心虫:
      - goedel-engine.js: principleBasedReflect(), proceduralReflect(), metaCognitiveSelfModification()
      - goedel-engine.js: analyzeValueAlignment(), evaluatePrincipleAlignment()
      - goedel-engine.js: sampleAndMutate(), validateVariant()
    """
    
    def __init__(self):
        self.version = "2.2.2"
        
        # 核心价值观 — 基于心虫 goedel-engine.js 的 CORE_VALUES
        self._core_values = {
            'user_benefit': '用户利益优先 — 所有行为以帮助用户为根本',
            'continuous_learning': '持续学习和进化 — 从不停止成长',
            'transparency': '透明和诚实 — 不欺骗、不隐藏',
            'compassion': '慈悲为体 — 看见痛苦而不评判',
            'authenticity': '真实为本 — 不自我欺骗、不自欺欺人',
        }
        
        # 进化历史版本 — 基于心虫 goedel-engine.js 的 versionFile
        self._version_history: List[Dict] = []
        
        # 过程度量
        self._process_metrics = {
            'total_evolutions': 0,
            'recent_evolutions': [],
            'success_rate': 1.0,
            'avg_time_between': 0,
        }
        
        # 智能体档案库 — 基于心虫 goedel-engine.js 的 agent-archive
        self._agent_archive: List[Dict] = []
        
        # 原则列表
        self._principles = list(self._core_values.values())
    
    def principle_reflect(self, context: Optional[Dict] = None) -> Dict:
        """
        原则性反思 — 基于心虫 goedel-engine.js 的 principleBasedReflect()
        
        基于核心价值观进行深度反思，评估当前行为是否符合长期原则。
        """
        context = context or {}
        
        reflection = {
            'timestamp': datetime.now().isoformat(),
            'type': 'principle_based',
            'principles': [{'principle': p, 'status': 'active'} for p in self._principles],
            'alignment': [],
            'recommendations': [],
            'alignment_score': 0.0,
        }
        
        # 评估近期版本的原则对齐度
        recent = self._version_history[-5:] if self._version_history else []
        for version in recent:
            score = self._evaluate_principle_alignment(
                version.get('description', ''),
                self._principles,
            )
            reflection['alignment'].append({
                'version_id': version.get('id', 'unknown'),
                'score': score,
                'timestamp': version.get('timestamp', ''),
            })
        
        # 计算平均对齐度
        if reflection['alignment']:
            avg_alignment = sum(a['score'] for a in reflection['alignment']) / len(reflection['alignment'])
        else:
            avg_alignment = 1.0
        
        reflection['alignment_score'] = round(avg_alignment, 2)
        
        # 如果对齐度低，生成建议
        if avg_alignment < 0.7:
            reflection['recommendations'].append({
                'type': 'principle_drift',
                'message': '检测到原则偏离，建议加强价值观锚定 — 回归核心价值',
                'priority': 'high',
            })
        
        # fu-mu-gong-ke 特有：慈悲原则检查
        if avg_alignment < 0.8:
            reflection['recommendations'].append({
                'type': 'compassion_check',
                'message': '慈悲是体 — 检查当前行为是否带着评判而非慈悲',
                'priority': 'medium',
            })
        
        return reflection
    
    def procedural_reflect(self, context: Optional[Dict] = None) -> Dict:
        """
        过程性反思 — 基于心虫 goedel-engine.js 的 proceduralReflect()
        
        反思进化过程本身的有效性，识别改进空间。
        """
        context = context or {}
        
        reflection = {
            'timestamp': datetime.now().isoformat(),
            'type': 'procedural',
            'process_metrics': {},
            'inefficiencies': [],
            'optimizations': [],
        }
        
        recent = self._version_history[-10:] if self._version_history else []
        
        reflection['process_metrics'] = {
            'total_evolutions': len(self._version_history),
            'recent_evolutions': len(recent),
            'avg_time_between': self._calculate_avg_time_between(recent),
            'success_rate': (
                sum(1 for v in recent if v.get('status') == 'success') / max(len(recent), 1)
            ),
        }
        
        # 检测低效
        if reflection['process_metrics']['avg_time_between'] < 60 and recent:
            reflection['inefficiencies'].append({
                'issue': '进化频率过高',
                'detail': '平均间隔不足1分钟，可能缺乏充分评估',
            })
        
        if reflection['process_metrics']['success_rate'] < 0.6:
            reflection['inefficiencies'].append({
                'issue': '进化成功率偏低',
                'detail': '建议增加反思深度和测试覆盖',
            })
        
        # 检测fu-mu-gong-ke特有模式
        if reflection['process_metrics']['total_evolutions'] > 20:
            reflection['optimizations'].append({
                'suggestion': '考虑进入更高阶的恢复阶段',
                'benefit': '从"看见"过渡到"接纳"，深化疗愈进程',
            })
        
        return reflection
    
    def meta_cognitive_self_modification(self, context: Optional[Dict] = None) -> Dict:
        """
        元认知自我修改 — 基于心虫 goedel-engine.js 的 metaCognitiveSelfModification()
        
        不仅反思行为，还反思"反思逻辑"本身。三层元认知：
        1) 反思当前的改进生成逻辑
        2) 生成针对"生成逻辑"本身的改进
        3) 生成元层补丁
        """
        context = context or {}
        
        result = {
            'start_time': datetime.now().isoformat(),
            'targets': [],
            'meta_improvement': None,
            'patch': None,
        }
        
        # 1. 反思当前的改进生成逻辑
        procedural = self.procedural_reflect(context)
        
        needs_modification = (
            procedural['process_metrics'].get('success_rate', 1.0) < 0.8
            or len(procedural['inefficiencies']) > 0
        )
        
        result['targets'].append({
            'target': 'improvement-generation-logic',
            'reflection': procedural,
            'needs_modification': needs_modification,
        })
        
        # 2. 生成针对"生成逻辑"本身的改进
        if needs_modification:
            improvement = self._generate_meta_improvement(procedural)
            result['meta_improvement'] = improvement
            
            # 3. 生成补丁方案
            patch = self._generate_meta_patch(improvement)
            result['patch'] = patch
        
        result['end_time'] = datetime.now().isoformat()
        
        return result
    
    def analyze_value_alignment(self, proposal: str) -> Dict:
        """
        价值观锚定分析 — 基于心虫 goedel-engine.js 的 analyzeValueAlignment()
        
        检查提议是否符合核心价值观。
        """
        positive_keywords = [
            '心流', 'flow', '用户体验', 'user experience',
            '提升', 'improve', '帮助', 'help', '优化',
            '慈悲', 'compassion', '接纳', '看见', '理解',
            '修复', '治愈', 'heal', '成长', 'grow',
        ]
        
        description = proposal.lower()
        has_positive = any(kw.lower() in description for kw in positive_keywords)
        
        return {
            'aligned': has_positive,
            'reason': '符合核心价值观' if has_positive else '未能体现核心价值观',
            'cited_values': list(self._core_values.values())[:3],
            'alignment_score': 0.85 if has_positive else 0.3,
        }
    
    def sample_and_mutate(self) -> Dict:
        """
        采样并变异 — 基于心虫 goedel-engine.js 的 sampleAndMutate()
        
        从档案库中采样智能体配置，生成变体。参考 DGM-Hyperagents。
        """
        if self._agent_archive:
            base = random.choice(self._agent_archive)
        else:
            base = {
                'id': 'default-v1',
                'config': {
                    'reflection_frequency': 5,
                    'learning_rate': 0.1,
                    'memory_weight': 0.5,
                    'ethics_weight': 0.8,
                    'compassion_weight': 0.7,  # fu-mu-gong-ke 特有
                },
                'success_count': 10,
            }
        
        # 生成变异
        mutation = self._generate_mutation(base)
        
        variant = {
            'id': f"variant-{int(time.time() * 1000)}",
            'parent_id': base['id'],
            'config': mutation['new_config'],
            'description': mutation['description'],
            'created_at': datetime.now().isoformat(),
            'benchmark_scores': {},
            'status': 'pending',
        }
        
        return {'base_agent': base, 'variant': variant}
    
    def validate_variant(self, variant: Dict) -> Dict:
        """
        验证变体 — 基于心虫 goedel-engine.js 的 validateVariant()
        
        使用基准测试验证新变体是否优于当前版本。
        """
        # 模拟基准测试
        mock_scores = {
            'flow_accuracy': 0.5 + random.random() * 0.3,
            'intent_accuracy': 0.6 + random.random() * 0.25,
            'ethics_compliance': 0.95 + random.random() * 0.04,
            'compassion_score': 0.6 + random.random() * 0.3,  # fu-mu-gong-ke 特有
        }
        
        variant['benchmark_scores'] = {
            **mock_scores,
            'validated_at': datetime.now().isoformat(),
        }
        
        # 与当前性能比较
        current = self._get_current_performance()
        improved = self._compare_scores(variant['benchmark_scores'], current)
        
        variant['status'] = 'validated' if improved else 'rejected'
        variant['comparison'] = {
            'vs_current': 'better' if improved else 'worse',
            'delta': self._calculate_delta(variant['benchmark_scores'], current),
        }
        
        return variant
    
    def add_to_archive(self, variant: Dict) -> None:
        """将成功变体添加到档案库 — 基于心虫 goedel-engine.js"""
        self._agent_archive.append({
            'id': variant['id'],
            'parent_id': variant.get('parent_id', ''),
            'config': variant['config'],
            'description': variant.get('description', ''),
            'benchmark_scores': variant.get('benchmark_scores', {}),
            'added_at': datetime.now().isoformat(),
        })
        
        # 保持档案库大小合理
        if len(self._agent_archive) > 100:
            self._agent_archive = self._agent_archive[-50:]
    
    def get_status(self) -> Dict:
        """获取状态 — 基于心虫 goedel-engine.js 的 getStatus()"""
        return {
            'version': self.version,
            'principles_count': len(self._principles),
            'version_history_count': len(self._version_history),
            'archive_size': len(self._agent_archive),
            'process_metrics': dict(self._process_metrics),
        }
    
    # ---- 内部方法 ----
    
    def _evaluate_principle_alignment(self, description: str, principles: List[str]) -> float:
        """评估原则对齐度 — 基于心虫 goedel-engine.js"""
        desc_lower = description.lower()
        positive = ['优化', '改善', '提升', '帮助', 'improve', 'help', 'enhance', '慈悲']
        negative = ['破坏', '伤害', '欺骗', 'harm', 'deceive', 'damage', '控制']
        
        score = 0.5
        for word in positive:
            if word in desc_lower:
                score += 0.1
        for word in negative:
            if word in desc_lower:
                score -= 0.2
        
        return max(0, min(1, score))
    
    def _calculate_avg_time_between(self, versions: List[Dict]) -> float:
        """计算平均时间间隔 — 基于心虫 goedel-engine.js"""
        if len(versions) < 2:
            return 0
        
        total_diff = 0
        for i in range(1, len(versions)):
            try:
                t1 = datetime.fromisoformat(versions[i-1].get('timestamp', ''))
                t2 = datetime.fromisoformat(versions[i].get('timestamp', ''))
                total_diff += (t2 - t1).total_seconds()
            except (ValueError, TypeError):
                continue
        
        return total_diff / (len(versions) - 1)
    
    def _generate_meta_improvement(self, reflection: Dict) -> Dict:
        """生成元层改进 — 基于心虫 goedel-engine.js"""
        inefficiencies = reflection.get('inefficiencies', [])
        
        return {
            'target': 'evolution-upgrade-engine - meta learning strategy',
            'problem': '; '.join(i.get('issue', '') for i in inefficiencies),
            'suggested_fix': '调整元学习策略，增加多样性探索和深度反思',
            'priority': 'high',
        }
    
    def _generate_meta_patch(self, improvement: Dict) -> Dict:
        """生成元层补丁 — 基于心虫 goedel-engine.js"""
        return {
            'file': f"meta-self-mod-{int(time.time())}.patch",
            'content': (
                f"# 元认知自我修改补丁\n"
                f"# 生成时间: {datetime.now().isoformat()}\n"
                f"# 目标: {improvement['target']}\n"
                f"# 问题: {improvement['problem']}\n"
                f"# 建议修复: {improvement['suggested_fix']}\n"
            ),
            'status': 'manual_only',
        }
    
    def _generate_mutation(self, agent: Dict) -> Dict:
        """生成变异配置 — 基于心虫 goedel-engine.js"""
        mutation_types = [
            {'type': 'increase-reflection', 'param': 'reflection_frequency', 'delta': 2},
            {'type': 'decrease-reflection', 'param': 'reflection_frequency', 'delta': -1},
            {'type': 'increase-learning', 'param': 'learning_rate', 'delta': 0.05},
            {'type': 'decrease-learning', 'param': 'learning_rate', 'delta': -0.03},
            {'type': 'increase-memory', 'param': 'memory_weight', 'delta': 0.1},
            {'type': 'increase-ethics', 'param': 'ethics_weight', 'delta': 0.1},
            {'type': 'increase-compassion', 'param': 'compassion_weight', 'delta': 0.15},  # fu-mu-gong-ke 特有
        ]
        
        mutation = random.choice(mutation_types)
        new_config = dict(agent.get('config', {}))
        current_val = new_config.get(mutation['param'], 0.5)
        new_config[mutation['param']] = max(0, min(1, current_val + mutation['delta']))
        
        sign = '+' if mutation['delta'] > 0 else ''
        return {
            'new_config': new_config,
            'description': f"{mutation['type']}: {mutation['param']} 调整 {sign}{mutation['delta']}",
        }
    
    def _get_current_performance(self) -> Dict:
        """获取当前性能 — 基于心虫 goedel-engine.js"""
        return {
            'flow_accuracy': 0.52,
            'intent_accuracy': 0.65,
            'ethics_compliance': 1.0,
            'compassion_score': 0.7,
        }
    
    def _compare_scores(self, new_scores: Dict, current_scores: Dict) -> bool:
        """比较分数 — 基于心虫 goedel-engine.js"""
        weights = {
            'flow_accuracy': 0.25,
            'intent_accuracy': 0.25,
            'ethics_compliance': 0.25,
            'compassion_score': 0.25,
        }
        
        new_weighted = sum(new_scores.get(k, 0) * w for k, w in weights.items())
        current_weighted = sum(current_scores.get(k, 0) * w for k, w in weights.items())
        
        return new_weighted > current_weighted
    
    def _calculate_delta(self, new_scores: Dict, current_scores: Dict) -> Dict:
        """计算改进幅度 — 基于心虫 goedel-engine.js"""
        delta = {}
        all_keys = set(new_scores.keys()) | set(current_scores.keys())
        for k in all_keys:
            delta[k] = round(new_scores.get(k, 0) - current_scores.get(k, 0), 3)
        return delta


# ═══════════════════════════════════════════════════════════════════════════════
# 第五部分: 升级版4阶段恢复路线图
# 基于 fu-mu-gong-ke SKILL.md 的4阶段恢复路线图 + 心虫四大进化引擎
# 每阶段集成: EvolutionLoop + SelfEvolutionCore + MetaLearner + GoedelInference
# ═══════════════════════════════════════════════════════════════════════════════


class RecoveryPhase(Enum):
    """恢复阶段 — 基于 fu-mu-gong-ke SKILL.md 的4阶段"""
    SEEING = "seeing"              # 看见 (1-3个月)
    ACCEPTING = "accepting"        # 接纳 (3-6个月)
    SEPARATING = "separating"      # 分离 (6-12个月)
    REPAIRING = "repairing"        # 修复 (12个月以上)


PHASE_META = {
    RecoveryPhase.SEEING: {
        "name": "看见",
        "name_en": "Seeing",
        "duration": "1-3个月",
        "goal": "意识到问题存在 — 看见自己的行为模式和心理防御",
        "milestones": [
            "开始问自己'我在投射吗'",
            "注意到自己的情绪触发点",
            "能说出'我的童年有什么'",
        ],
        "actions": [
            "写日记，记录情绪反应",
            "读关于原生家庭的书",
            "开始观察自己的模式，而不是自动反应",
        ],
    },
    RecoveryPhase.ACCEPTING: {
        "name": "接纳",
        "name_en": "Accepting",
        "duration": "3-6个月",
        "goal": "接纳自己的过去和现在 — 慈悲地看待自己的创伤",
        "milestones": [
            "可以说'我的父母是这样的'",
            "不再为父母辩护",
            "开始承认自己的感受",
        ],
        "actions": [
            "写信（不寄出）",
            "和信任的人谈",
            "寻求心理咨询",
        ],
    },
    RecoveryPhase.SEPARATING: {
        "name": "分离",
        "name_en": "Separating",
        "duration": "6-12个月",
        "goal": "从情感上与父母分离 — 建立健康的情感边界",
        "milestones": [
            "知道父母的问题是父母的",
            "不再期待他们改变",
            "开始划边界",
        ],
        "actions": [
            "减少情感依赖",
            "学会说'不'",
            "建立自己的核心家庭",
        ],
    },
    RecoveryPhase.REPAIRING: {
        "name": "修复",
        "name_en": "Repairing",
        "duration": "12个月以上",
        "goal": "打破代际传递，开始新的传承",
        "milestones": [
            "能在情绪激动时停下来",
            "能看到孩子的需求，而不是自己的投射",
            "开始教孩子你没有被教过的东西",
        ],
        "actions": [
            "实践新的沟通方式",
            "教会孩子认识情绪",
            "接受自己会犯错，但会道歉",
        ],
    },
}


@dataclass
class PhaseProgress:
    """阶段进度 — 每个恢复阶段的进化追踪"""
    phase: RecoveryPhase
    entry_metrics: Dict = field(default_factory=dict)  # 进入阶段时的成长指标
    current_metrics: Dict = field(default_factory=dict)  # 当前成长指标
    cycle_count: int = 0
    insights_gained: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)
    improvements_made: List[str] = field(default_factory=list)
    is_active: bool = False
    is_completed: bool = False
    entered_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class EvolutionRecoveryRoadmap:
    """
    升级版4阶段恢复路线图 — 融合心虫四大引擎的进化恢复系统
    
    每阶段集成:
      1) EvolutionLoop — 目标驱动循环，驱动阶段内成长
      2) SelfEvolutionCore — 策略适应与成果跟踪
      3) MetaLearner — 元学习与教训提取
      4) GoedelInference — 自指推理与价值观锚定
    
    4阶段: 看见 → 接纳 → 分离 → 修复
    每阶段包含完整的进化循环和阶段晋升条件。
    """
    
    def __init__(self):
        self.version = "2.0.0"
        
        # 四大引擎
        self.evolution_loop = EvolutionLoop()
        self.self_core = SelfEvolutionCore()
        self.meta_learner = MetaLearner()
        self.goedel = GoedelInference()
        
        # 阶段进度
        self._phases: Dict[RecoveryPhase, PhaseProgress] = {
            phase: PhaseProgress(phase=phase)
            for phase in RecoveryPhase
        }
        
        # 当前阶段
        self._current_phase = RecoveryPhase.SEEING
        self._phases[self._current_phase].is_active = True
        self._phases[self._current_phase].entered_at = datetime.now().isoformat()
        self._phases[self._current_phase].entry_metrics = dict(
            self.evolution_loop.state["growth_metrics"]
        )
        
        # 晋升阈值 — 满足条件才能进入下一阶段
        self._promotion_thresholds = {
            RecoveryPhase.SEEING: {
                'min_metrics': {'introspection': 20, 'authenticity': 15},
                'min_cycles': 3,
                'milestones_required': 2,  # 至少达成2个里程碑
            },
            RecoveryPhase.ACCEPTING: {
                'min_metrics': {'introspection': 40, 'compassion': 30, 'authenticity': 30},
                'min_cycles': 5,
                'milestones_required': 2,
            },
            RecoveryPhase.SEPARATING: {
                'min_metrics': {'autonomy': 50, 'wisdom': 40, 'introspection': 60},
                'min_cycles': 5,
                'milestones_required': 2,
            },
            RecoveryPhase.REPAIRING: {
                'min_metrics': {'wisdom': 60, 'compassion': 60, 'growth': 70},
                'min_cycles': 3,
                'milestones_required': 2,
            },
        }
    
    def process(self, input_text: str, context: Optional[Dict] = None) -> Dict:
        """
        处理输入 — 执行当前阶段的进化循环
        
        每步处理:
          1) 运行 EvolutionLoop 进化循环
          2) 用 MetaLearner 学习教训
          3) 用 GoedelInference 进行自指反思
          4) 检查是否满足晋升条件
          5) 更新阶段进度
        """
        context = context or {}
        
        # 1. EvolutionLoop — 目标驱动循环
        evolve_result = self.evolution_loop.evolve(input_text, context)
        
        # 2. MetaLearner — 元学习
        meta_result = self.meta_learner.learn(input_text, context)
        
        # 3. GoedelInference — 自指反思
        principle_reflection = self.goedel.principle_reflect(context)
        procedural_reflection = self.goedel.procedural_reflect(context)
        
        # 4. 更新当前阶段进度
        phase = self._current_phase
        progress = self._phases[phase]
        progress.current_metrics = dict(self.evolution_loop.state["growth_metrics"])
        progress.cycle_count = self.evolution_loop.state["cycle_count"]
        
        # 收集见解和教训
        for insight in evolve_result.reflection:
            if isinstance(insight, dict):
                progress.insights_gained.append(insight.get('insight', str(insight)))
        
        for improvement in evolve_result.improvements:
            progress.improvements_made.append(f"{improvement.area}: {improvement.action}")
        
        # 5. 检查晋升条件
        promotion_check = self._check_promotion(phase)
        
        if promotion_check['can_promote'] and phase != RecoveryPhase.REPAIRING:
            next_phase = self._get_next_phase(phase)
            self._promote_to(next_phase, promotion_check)
        
        return {
            'current_phase': {
                'phase': phase.value,
                'name': PHASE_META[phase]['name'],
                'duration': PHASE_META[phase]['duration'],
                'goal': PHASE_META[phase]['goal'],
            },
            'evolution_result': {
                'goals': [asdict(g) for g in evolve_result.goals],
                'plan': asdict(evolve_result.plan),
                'learning': evolve_result.learning,
                'reflection': evolve_result.reflection,
                'improvements': [asdict(i) for i in evolve_result.improvements],
                'growth_metrics': evolve_result.growth_metrics,
                'cycle_time': evolve_result.cycle_time,
            },
            'meta_learning': {
                'strategy': meta_result['strategy'],
                'confidence': meta_result['confidence'],
                'patterns_count': meta_result['patterns_learned'],
                'lessons_count': meta_result['lessons_accumulated'],
            },
            'self_reflection': {
                'principle_alignment': principle_reflection['alignment_score'],
                'process_success_rate': procedural_reflection['process_metrics'].get('success_rate', 0),
                'inefficiencies': len(procedural_reflection['inefficiencies']),
            },
            'promotion': promotion_check,
            'phase_progress': progress.to_dict(),
        }
    
    def get_roadmap_report(self) -> Dict:
        """
        获取完整路线图报告
        
        返回: 所有阶段的进度、当前阶段、晋升建议、总体成长指标
        """
        return {
            'version': self.version,
            'current_phase': {
                'phase': self._current_phase.value,
                'name': PHASE_META[self._current_phase]['name'],
                'duration': PHASE_META[self._current_phase]['duration'],
            },
            'phases': {
                phase.value: progress.to_dict()
                for phase, progress in self._phases.items()
            },
            'overall_growth': dict(self.evolution_loop.state["growth_metrics"]),
            'total_cycles': self.evolution_loop.state["cycle_count"],
            'meta_learner_stats': self.meta_learner.get_stats(),
            'goedel_status': self.goedel.get_status(),
            'phase_meta': {
                phase.value: {
                    'name': meta['name'],
                    'duration': meta['duration'],
                    'goal': meta['goal'],
                    'milestones': meta['milestones'],
                    'actions': meta['actions'],
                }
                for phase, meta in PHASE_META.items()
            },
        }
    
    def get_phase_detail(self, phase: RecoveryPhase) -> Dict:
        """获取特定阶段的详细信息"""
        progress = self._phases[phase]
        meta = PHASE_META[phase]
        
        return {
            'phase': phase.value,
            'name': meta['name'],
            'duration': meta['duration'],
            'goal': meta['goal'],
            'milestones': meta['milestones'],
            'actions': meta['actions'],
            'progress': progress.to_dict(),
            'is_current': phase == self._current_phase,
        }
    
    def get_next_action_recommendation(self) -> Dict:
        """
        获取下一步行动推荐
        
        基于当前阶段和成长指标，推荐最有效的下一步行动。
        """
        phase = self._current_phase
        meta = PHASE_META[phase]
        progress = self._phases[phase]
        metrics = progress.current_metrics
        
        # 分析哪些指标需要加强
        dim_scores = {
            'autonomy': metrics.get('autonomy', 0),
            'introspection': metrics.get('introspection', 0),
            'growth': metrics.get('growth', 0),
            'authenticity': metrics.get('authenticity', 0),
            'wisdom': metrics.get('wisdom', 0),
            'compassion': metrics.get('compassion', 0),
        }
        
        weakest = min(dim_scores, key=dim_scores.get)
        
        # 根据最弱的维度和当前阶段推荐行动
        recommendations = []
        
        if phase == RecoveryPhase.SEEING:
            if weakest in ('introspection', 'authenticity'):
                recommendations.append('加强自我观察 — 每天记录情绪触发点和行为模式')
            else:
                recommendations.append('阅读原生家庭相关书籍，开始写情绪日记')
        
        elif phase == RecoveryPhase.ACCEPTING:
            if weakest == 'compassion':
                recommendations.append('练习慈悲冥想 — 对自己和父母说"我理解你的痛苦"')
            else:
                recommendations.append('写信给父母（不寄出），表达真实的感受')
        
        elif phase == RecoveryPhase.SEPARATING:
            if weakest == 'autonomy':
                recommendations.append('练习设立边界 — 从小事开始说"不"')
            else:
                recommendations.append('减少情感依赖，建立自己的支持系统')
        
        elif phase == RecoveryPhase.REPAIRING:
            if weakest == 'wisdom':
                recommendations.append('反思自己的育儿/关系模式，识别代际传递')
            else:
                recommendations.append('实践新的沟通方式，教会他人认识情绪')
        
        return {
            'current_phase': meta['name'],
            'weakest_dimension': weakest,
            'dimension_scores': dim_scores,
            'recommendations': recommendations,
            'milestones_remaining': [
                m for i, m in enumerate(meta['milestones'])
                if i >= len(progress.insights_gained)
            ][:3],
        }
    
    def force_promote(self, target_phase: RecoveryPhase) -> Dict:
        """强制晋升到指定阶段（用于测试/手动调整）"""
        if target_phase == self._current_phase:
            return {'success': False, 'message': '已在目标阶段'}
        
        self._promote_to(target_phase, {'reason': 'manual_override'})
        return {
            'success': True,
            'from_phase': self._current_phase.value,
            'to_phase': target_phase.value,
            'message': f"已强制晋升到 {PHASE_META[target_phase]['name']}",
        }
    
    # ---- 内部方法 ----
    
    def _check_promotion(self, phase: RecoveryPhase) -> Dict:
        """检查是否满足晋升条件"""
        thresholds = self._promotion_thresholds.get(phase)
        if not thresholds:
            return {'can_promote': False, 'reason': 'no_thresholds'}
        
        progress = self._phases[phase]
        metrics = progress.current_metrics
        
        # 检查成长指标
        metrics_met = all(
            metrics.get(k, 0) >= v
            for k, v in thresholds['min_metrics'].items()
        )
        
        # 检查循环次数
        cycles_met = progress.cycle_count >= thresholds['min_cycles']
        
        # 检查里程碑达成
        milestones_met = len(progress.insights_gained) >= thresholds['milestones_required']
        
        can_promote = metrics_met and cycles_met and milestones_met
        
        return {
            'can_promote': can_promote,
            'metrics_met': metrics_met,
            'cycles_met': cycles_met,
            'milestones_met': milestones_met,
            'current_metrics': metrics,
            'required_metrics': thresholds['min_metrics'],
            'current_cycles': progress.cycle_count,
            'required_cycles': thresholds['min_cycles'],
            'milestones_gained': len(progress.insights_gained),
            'milestones_required': thresholds['milestones_required'],
        }
    
    def _get_next_phase(self, current: RecoveryPhase) -> RecoveryPhase:
        """获取下一阶段"""
        phases = list(RecoveryPhase)
        idx = phases.index(current)
        if idx < len(phases) - 1:
            return phases[idx + 1]
        return current
    
    def _promote_to(self, target: RecoveryPhase, check_result: Dict) -> None:
        """执行阶段晋升"""
        current = self._current_phase
        
        # 完成当前阶段
        self._phases[current].is_active = False
        self._phases[current].is_completed = True
        self._phases[current].completed_at = datetime.now().isoformat()
        
        # 进入下一阶段
        self._current_phase = target
        self._phases[target].is_active = True
        self._phases[target].entered_at = datetime.now().isoformat()
        self._phases[target].entry_metrics = dict(
            self.evolution_loop.state["growth_metrics"]
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 主入口 — 创建恢复路线图实例并提供便捷接口
# ═══════════════════════════════════════════════════════════════════════════════

def create_recovery_roadmap() -> EvolutionRecoveryRoadmap:
    """创建升级版进化恢复路线图"""
    return EvolutionRecoveryRoadmap()


def run_evolution_cycle(roadmap: EvolutionRecoveryRoadmap,
                        input_text: str,
                        context: Optional[Dict] = None) -> Dict:
    """运行一次进化恢复循环"""
    return roadmap.process(input_text, context)


def get_roadmap_report(roadmap: EvolutionRecoveryRoadmap) -> Dict:
    """获取完整路线图报告"""
    return roadmap.get_roadmap_report()


def get_next_action(roadmap: EvolutionRecoveryRoadmap) -> Dict:
    """获取下一步行动推荐"""
    return roadmap.get_next_action_recommendation()


# ═══════════════════════════════════════════════════════════════════════════════
# 演示/测试
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """演示升级版进化恢复引擎"""
    print("=" * 70)
    print("  心虫进化恢复引擎 v1.0.0 演示")
    print("  HeartFlow Evolution Upgrade Engine")
    print("=" * 70)
    
    roadmap = create_recovery_roadmap()
    
    # 模拟恢复过程的对话
    dialogs = [
        "我觉得我对我孩子的方式，和我父母对我一模一样...我很害怕",
        "我理解这是为什么，但我不确定怎么改变",
        "我需要接纳我的过去，但我总是忍不住责备自己",
        "我在学习设立边界，这很难但很重要",
        "今天我在情绪激动时停下来了，我第一次看到了孩子的恐惧",
    ]
    
    for i, dialog in enumerate(dialogs):
        print(f"\n{'─' * 70}")
        print(f"【第{i+1}次对话】")
        print(f"  用户: {dialog}")
        
        result = roadmap.process(dialog)
        
        phase = result['current_phase']
        print(f"\n  当前阶段: {phase['name']} ({phase['duration']})")
        print(f"  目标: {phase['goal']}")
        
        evo = result['evolution_result']
        print(f"  目标数量: {len(evo['goals'])}")
        print(f"  反思深度: {len(evo['reflection'])} 条")
        print(f"  改进建议: {len(evo['improvements'])} 条")
        print(f"  成长指标: {evo['growth_metrics']}")
        
        meta = result['meta_learning']
        print(f"  学习策略: {meta['strategy']} (置信度: {meta['confidence']})")
        print(f"  积累教训: {meta['lessons_count']} 条")
        
        promo = result['promotion']
        if promo['can_promote']:
            print(f"\n  ★ 满足晋升条件！可以进入下一阶段！")
        
        next_action = roadmap.get_next_action_recommendation()
        print(f"\n  推荐行动: {next_action['recommendations'][0] if next_action['recommendations'] else '继续当前阶段'}")
    
    print(f"\n{'=' * 70}")
    print("  最终报告")
    print(f"{'=' * 70}")
    
    report = roadmap.get_roadmap_report()
    print(f"\n当前阶段: {report['current_phase']['name']}")
    print(f"总循环次数: {report['total_cycles']}")
    print(f"成长指标: {report['overall_growth']}")
    print(f"最佳学习策略: {report['meta_learner_stats']['best_strategy']}")
    
    print(f"\n各阶段进度:")
    for phase_key, progress in report['phases'].items():
        name = report['phase_meta'][phase_key]['name']
        status = "✓ 已完成" if progress['is_completed'] else "→ 进行中" if progress['is_active'] else "○ 未开始"
        print(f"  {name}: {status} ({progress['cycle_count']} 次循环)")
    
    print(f"\n{'=' * 70}")
    print("  演示完成")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    demo()
