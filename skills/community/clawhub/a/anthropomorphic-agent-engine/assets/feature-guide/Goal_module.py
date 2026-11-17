# ================================================================
# 目标系统（Goal Engine）—— 【自设模块】
# ================================================================
# 目标是角色行为的驱动力。目标受阻产生挫折感，
# 目标达成产生成就感。不同角色有不同的目标层级。
#
# 用法：在 Agent 初始化时加载 GoalEngine，
#       用 update_progress() 更新目标进度，
#       用 get_emotion_vector() 获取目标状态的情绪影响。
# ================================================================

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import math


@dataclass
class GoalNode:
    """一个目标节点"""
    name: str              # 目标名称
    importance: float      # 重要性 [0,1]
    progress: float = 0.0  # 当前进度 [0,1]
    urgency: float = 0.5   # 紧迫度 [0,1]
    difficulty: float = 0.5  # 难度 [0,1]
    dependencies: List[str] = field(default_factory=list)  # 依赖的其他目标
    stalled: bool = False  # 是否卡住了


class GoalEngine:
    """
    目标引擎：管理目标的层级结构和进度。

    核心机制：
    1. 目标受阻（progress 停滞 + urgency 高）→ 挫折情绪
    2. 目标达成（progress → 1.0）→ 成就感
    3. 目标冲突（A 的进度牺牲了 B）→ 内在张力
    4. 当前主目标决定注意力分配和行为优先级
    """

    def __init__(self):
        self.goals: List[GoalNode] = []
        self.completed_goals: List[GoalNode] = []

    def add_goal(self, name: str, importance: float, urgency: float = 0.5,
                 difficulty: float = 0.5, dependencies: List[str] = None):
        """添加一个目标。"""
        self.goals.append(GoalNode(
            name=name, importance=importance,
            urgency=urgency, difficulty=difficulty,
            dependencies=dependencies or [],
        ))

    def update_progress(self, goal_name: str, delta: float):
        """
        更新目标进度。

        Args:
            goal_name: 目标名
            delta: 进度变化 [-1, 1]
        """
        for goal in self.goals:
            if goal.name == goal_name:
                old_progress = goal.progress
                goal.progress = max(0.0, min(1.0, goal.progress + delta))

                # 进度停止 → 标记为卡住
                if abs(goal.progress - old_progress) < 0.01 and goal.progress < 0.9:
                    goal.stalled = True
                else:
                    goal.stalled = False

                # 目标达成
                if goal.progress >= 0.99:
                    self.completed_goals.append(goal)
                    self.goals.remove(goal)
                break

    def set_urgency(self, goal_name: str, urgency: float):
        """更新目标紧迫度。"""
        for goal in self.goals:
            if goal.name == goal_name:
                goal.urgency = max(0.0, min(1.0, urgency))
                break

    def get_primary_goal(self) -> Optional[GoalNode]:
        """获取当前主目标（重要性 × 紧迫度 × (1-进度) 最大）。"""
        if not self.goals:
            return None
        return max(self.goals, key=lambda g:
            g.importance * g.urgency * (1.0 - g.progress) * g.difficulty)

    def goal_conflict_level(self) -> float:
        """
        计算目标间的冲突水平。

        高重要性目标之间的进度权衡会产生冲突。
        """
        if len(self.goals) < 2:
            return 0.0
        # 依赖冲突：如果 A 的完成阻碍了 B
        conflict = 0.0
        for g in self.goals:
            for dep_name in g.dependencies:
                for other in self.goals:
                    if other.name == dep_name and other.progress < 0.3:
                        conflict += g.importance * g.urgency
        return min(1.0, conflict * 0.5)

    def get_emotion_vector(self) -> Dict[str, float]:
        """
        将目标状态转化为情绪向量。

        定期调用，注入 core.process_vector() 作为基底。
        """
        vector = {}
        primary = self.get_primary_goal()

        if primary:
            # 重要目标卡住 → 挫折/张力
            if primary.stalled and primary.importance > 0.5:
                frustration = primary.importance * primary.urgency * 0.3
                vector["tension_base"] = vector.get("tension_base", 0.0) + frustration
                # 如果卡住的是高难度目标 → 可能触发羞耻（"我做不到"）
                if primary.difficulty > 0.7:
                    vector["shame_trigger"] = 0.15 * primary.importance

            # 目标进展 → 轻微喜悦
            if primary.progress > 0.5:
                progress_joy = primary.importance * (primary.progress - 0.5) * 0.2
                vector["belonging"] = vector.get("belonging", 0.0) + progress_joy

            # 高紧迫度 → 张力
            if primary.urgency > 0.7:
                vector["tension_base"] = vector.get("tension_base", 0.0) + primary.urgency * 0.2

        # 目标冲突 → 张力
        conflict = self.goal_conflict_level()
        if conflict > 0.1:
            vector["tension_base"] = vector.get("tension_base", 0.0) + conflict * 0.3

        # 近期完成目标 → 喜悦+自尊提升
        if self.completed_goals:
            total_importance = sum(g.importance for g in self.completed_goals[-3:])
            vector["belonging"] = vector.get("belonging", 0.0) + total_importance * 0.15

        return vector

    def snapshot(self) -> dict:
        """目标系统快照。"""
        return {
            "active_goals": [
                {"name": g.name, "importance": g.importance,
                 "progress": g.progress, "urgency": g.urgency,
                 "stalled": g.stalled}
                for g in self.goals
            ],
            "primary": self.get_primary_goal().name if self.get_primary_goal() else None,
            "completed": len(self.completed_goals),
            "conflict": self.goal_conflict_level(),
        }


# ── 预设：苏瑾的目标配置 ──

def sujin_goals() -> GoalEngine:
    """苏瑾的目标层级"""
    engine = GoalEngine()
    engine.add_goal("赢得客户信任", importance=0.8, urgency=0.7, difficulty=0.7)
    engine.add_goal("保持专业独立性", importance=0.75, urgency=0.5, difficulty=0.6)
    engine.add_goal("交付高质量方案", importance=0.9, urgency=0.8, difficulty=0.8)
    # 此目标依赖"赢得客户信任"
    engine.add_goal("建立长期战略合作", importance=0.7, urgency=0.4, difficulty=0.8,
                    dependencies=["赢得客户信任"])
    return engine
