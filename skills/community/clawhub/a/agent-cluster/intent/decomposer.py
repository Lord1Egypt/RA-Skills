"""
Task Decomposer - 任务拆解引擎

将用户意图拆解为可执行的子任务列表，包含：
    - 依赖关系分析（DAG构建）
    - 执行顺序规划（拓扑排序）
    - Agent分配策略
    - 并行组识别
    - 优先级计算

Change Log:
    2026-04-14: 初始版本
"""

from __future__ import annotations

import logging
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from intent.recognizer import Intent, SubTask as IntentSubTask

logger = logging.getLogger(__name__)


# =============================================================================
# 执行模式
# =============================================================================

class ExecutionMode(Enum):
    """执行模式"""
    SEQUENTIAL  = "sequential"   # 严格串行
    PARALLEL    = "parallel"     # 全部并行
    HYBRID      = "hybrid"       # 混合（可并行的并行，串行的串行）
    PRIORITY    = "priority"     # 按优先级调度


# =============================================================================
# Agent配置
# =============================================================================

@dataclass
class AgentSpec:
    """Agent规格说明"""
    name: str
    supported_actions: list[str]
    max_concurrent: int = 3
    timeout_seconds: float = 30.0
    fallback_agent: Optional[str] = None


AGENT_REGISTRY: dict[str, AgentSpec] = {
    "inventory_agent": AgentSpec(
        name="inventory_agent",
        supported_actions=[
            "query_stock", "check_stock", "trigger_replenishment",
            "calc_replenishment", "forecast_stock", "stock_alert",
        ],
        max_concurrent=3,
        timeout_seconds=20.0,
    ),
    "logistics_agent": AgentSpec(
        name="logistics_agent",
        supported_actions=[
            "query_logistics", "calc_freight", "plan_route",
            "track_shipment", "shipping_notify",
        ],
        max_concurrent=3,
        timeout_seconds=25.0,
    ),
    "procurement_agent": AgentSpec(
        name="procurement_agent",
        supported_actions=[
            "query_supplier", "place_order", "cancel_order",
            "query_quote", "negotiate_price",
        ],
        max_concurrent=2,
        timeout_seconds=30.0,
    ),
    "finance_agent": AgentSpec(
        name="finance_agent",
        supported_actions=[
            "approve_payment", "query_budget", "cost_analysis",
            "analyze_profit", "optimize_pricing",
        ],
        max_concurrent=2,
        timeout_seconds=30.0,
        fallback_agent="doc_agent",
    ),
    "doc_agent": AgentSpec(
        name="doc_agent",
        supported_actions=[
            "generate_document", "export_pdf", "generate_ppt",
            "fill_form",
        ],
        max_concurrent=2,
        timeout_seconds=60.0,
    ),
}


# =============================================================================
# 拆解结果
# =============================================================================

@dataclass
class DecompositionResult:
    """
    任务拆解结果

    Attributes:
        request_id: 关联的请求ID
        intent: 原始Intent
        sub_tasks: 拆解后的子任务列表
        execution_plan: 执行计划（dag描述）
        estimated_total_time_ms: 预估总耗时
        agents_used: 使用的Agent列表
        parallelism_score: 并行度得分 [0, 1]
        confidence: 拆解置信度
    """
    request_id: str
    intent: Intent
    sub_tasks: list[IntentSubTask]
    execution_plan: dict = field(default_factory=dict)
    estimated_total_time_ms: float = 0.0
    agents_used: list[str] = field(default_factory=list)
    parallelism_score: float = 0.0
    confidence: float = 0.0

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "intent_type": self.intent.intent_type.value,
            "sub_intent": self.intent.sub_intent,
            "sub_tasks": [t.to_dict() for t in self.sub_tasks],
            "execution_plan": self.execution_plan,
            "estimated_total_time_ms": round(self.estimated_total_time_ms, 1),
            "agents_used": self.agents_used,
            "parallelism_score": round(self.parallelism_score, 2),
            "confidence": round(self.confidence, 2),
        }


# =============================================================================
# 任务拆解引擎
# =============================================================================

class TaskDecomposer:
    """
    任务拆解引擎

    核心流程：
        1. 接收 Intent 对象
        2. 从 Intent.sub_task_candidates 生成 SubTask 列表
        3. 分析依赖关系，构建 DAG
        4. 拓扑排序，确定执行顺序
        5. 标记并行组
        6. 计算优先级和预估耗时
        7. 分配 Agent

    依赖关系策略：
        - 采购下单: place_order → approve_payment（顺序依赖）
        - 补货流程: check_stock → calc_replenishment → place_order → approve_payment
        - 文档生成: generate_document → export_pdf
        - 并行组: 无依赖的同Agent任务可并行
    """

    # 动作依赖规则
    DEPENDENCY_RULES: dict[str, list[str]] = {
        "place_order":          ["query_supplier"],
        "approve_payment":      ["place_order"],
        "calc_replenishment":   ["check_stock", "query_stock"],
        "export_pdf":           ["generate_document"],
        "optimize_pricing":     ["analyze_profit"],
        "negotiate_price":      ["query_quote"],
    }

    # 执行耗时估算（毫秒）
    ACTION_COST_ESTIMATE: dict[str, float] = {
        "query_stock":          800,
        "check_stock":          600,
        "trigger_replenishment": 1000,
        "calc_replenishment":   500,
        "query_supplier":       1200,
        "place_order":          1500,
        "cancel_order":         800,
        "query_quote":          1000,
        "negotiate_price":      2000,
        "query_logistics":      1000,
        "calc_freight":         500,
        "plan_route":           1500,
        "track_shipment":       800,
        "shipping_notify":      600,
        "approve_payment":      1200,
        "query_budget":         800,
        "cost_analysis":        1500,
        "analyze_profit":       2000,
        "optimize_pricing":     2500,
        "forecast_stock":       2000,
        "trend_analysis":        1500,
        "stock_alert":          500,
        "generate_document":    3000,
        "export_pdf":           1500,
        "generate_ppt":         5000,
        "fill_form":            1000,
        "general_query":        1000,
    }

    def __init__(self, agent_registry: Optional[dict[str, AgentSpec]] = None):
        self.agent_registry = agent_registry or AGENT_REGISTRY

    # -------------------------------------------------------------------
    # 主拆解入口
    # -------------------------------------------------------------------

    def decompose(self, intent: Intent, request_id: Optional[str] = None) -> DecompositionResult:
        """
        将意图拆解为可执行子任务

        Args:
            intent: IntentRecognizer 返回的 Intent 对象
            request_id: 请求ID（用于关联追踪）

        Returns:
            DecompositionResult
        """
        request_id = request_id or str(uuid.uuid4())[:8]

        # Step 1: 生成基础 SubTask 列表
        sub_tasks = self._build_sub_tasks(intent, request_id)

        # Step 2: 构建依赖 DAG
        dag = self._build_dag(sub_tasks)

        # Step 3: 拓扑排序，确定执行顺序
        sorted_ids = self._topological_sort(dag, sub_tasks)
        self._apply_order(sub_tasks, sorted_ids)

        # Step 4: 标记并行组
        parallel_groups = self._detect_parallel_groups(sub_tasks, dag)
        self._assign_parallel_groups(sub_tasks, parallel_groups)

        # Step 5: 分配 Agent
        self._assign_agents(sub_tasks)

        # Step 6: 计算优先级
        self._compute_priorities(sub_tasks, intent)

        # Step 7: 预估耗时
        total_time = self._estimate_total_time(sub_tasks, parallel_groups)

        # Step 8: 并行度评估
        parallelism_score = self._compute_parallelism_score(
            sub_tasks, parallel_groups, total_time
        )

        # Step 9: 拆解置信度
        confidence = self._compute_decompose_confidence(intent, sub_tasks)

        result = DecompositionResult(
            request_id=request_id,
            intent=intent,
            sub_tasks=sub_tasks,
            execution_plan=self._build_execution_plan(sub_tasks, parallel_groups),
            estimated_total_time_ms=total_time,
            agents_used=self._collect_agents_used(sub_tasks),
            parallelism_score=parallelism_score,
            confidence=confidence,
        )

        logger.info(
            f"[TaskDecomposer] decomposed '{intent.sub_intent}' "
            f"→ {len(sub_tasks)} sub_tasks, "
            f"parallelism={parallelism_score:.2f}, "
            f"est_time={total_time:.0f}ms, "
            f"confidence={confidence:.2%}"
        )

        return result

    # -------------------------------------------------------------------
    # Step 1: 构建子任务
    # -------------------------------------------------------------------

    def _build_sub_tasks(
        self,
        intent: Intent,
        request_id: str,
    ) -> list[IntentSubTask]:
        """从 Intent 生成 SubTask 列表"""
        tasks = []

        candidates = intent.sub_task_candidates or [
            {"action": "general_query", "description": "通用查询", "agents": ["inventory_agent"]}
        ]

        for i, cand in enumerate(candidates):
            task_id = f"{request_id}-t{i+1:02d}"
            agents = cand.get("agents", intent.required_agents[:1] or ["inventory_agent"])

            tasks.append(IntentSubTask(
                task_id=task_id,
                action=cand.get("action", "general_query"),
                description=cand.get("description", ""),
                parameters={"entities": intent.entities, "raw_input": intent.raw_input},
                depends_on=[],
                parallel_group=None,
                priority=50,
                estimated_cost=self.ACTION_COST_ESTIMATE.get(cand.get("action", ""), 1.0),
            ))

        return tasks

    # -------------------------------------------------------------------
    # Step 2: 构建 DAG
    # -------------------------------------------------------------------

    def _build_dag(self, tasks: list[IntentSubTask]) -> dict[str, set[str]]:
        """
        构建有向无环图（DAG）

        Returns:
            adjacency dict: task_id → set of dependent task_ids
            即: task_id 执行前必须完成其 depends_on 中的任务
        """
        task_map = {t.action: t for t in tasks}
        dag: dict[str, set[str]] = {t.task_id: set() for t in tasks}

        for task in tasks:
            rule_deps = self.DEPENDENCY_RULES.get(task.action, [])
            for dep_action in rule_deps:
                # 找到对应的前置任务
                for potential_dep in tasks:
                    if potential_dep.action == dep_action:
                        dag[task.task_id].add(potential_dep.task_id)
                        task.depends_on.append(potential_dep.task_id)

        return dag

    # -------------------------------------------------------------------
    # Step 3: 拓扑排序
    # -------------------------------------------------------------------

    def _topological_sort(
        self,
        dag: dict[str, set[str]],
        tasks: list[IntentSubTask],
    ) -> list[str]:
        """
        Kahn算法拓扑排序

        Returns:
            排序后的 task_id 列表
        """
        # 入度统计
        task_map = {t.task_id: t for t in tasks}
        in_degree = {tid: len(deps) for tid, deps in dag.items()}

        # 入度为0的队列
        queue = [tid for tid, deg in in_degree.items() if deg == 0]
        sorted_ids: list[str] = []

        while queue:
            # 按优先级排序（优先级高的先执行）
            queue.sort(key=lambda tid: -task_map[tid].priority)
            current = queue.pop(0)
            sorted_ids.append(current)

            for tid, deps in dag.items():
                if current in deps:
                    in_degree[tid] -= 1
                    if in_degree[tid] == 0:
                        queue.append(tid)

        # 检测环（理论上不应该出现）
        if len(sorted_ids) != len(tasks):
            logger.error(f"[TaskDecomposer] 检测到环！{len(tasks)} tasks, only sorted {len(sorted_ids)}")
            # 降级：返回原始顺序
            sorted_ids = [t.task_id for t in tasks]

        return sorted_ids

    def _apply_order(
        self,
        tasks: list[IntentSubTask],
        sorted_ids: list[str],
    ) -> None:
        """将拓扑排序结果应用到任务列表"""
        id_to_task = {t.task_id: t for t in tasks}
        ordered = [id_to_task[tid] for tid in sorted_ids]
        tasks.clear()
        tasks.extend(ordered)

    # -------------------------------------------------------------------
    # Step 4: 并行组检测
    # -------------------------------------------------------------------

    def _detect_parallel_groups(
        self,
        tasks: list[IntentSubTask],
        dag: dict[str, set[str]],
    ) -> dict[str, list[str]]:
        """
        检测可并行执行的任务组

        策略：
            - 无依赖关系的任务，若属于不同Agent，可并行
            - 若属于同一Agent，最多并行 max_concurrent 个
            - 依赖链上的任务串行
        """
        groups: dict[str, list[str]] = defaultdict(list)
        visited: set[str] = set()

        for task in tasks:
            if task.task_id in visited:
                continue

            # 找所有与当前任务无依赖的同组任务
            parallel: list[IntentSubTask] = [task]
            visited.add(task.task_id)

            for other in tasks:
                if other.task_id in visited:
                    continue
                # 检查是否可并行：无相互依赖
                if task.task_id not in dag.get(other.task_id, set()) and \
                   other.task_id not in dag.get(task.task_id, set()):
                    # 同Agent需检查并发上限
                    agent = self._find_agent_for_action(other.action)
                    if agent and agent.max_concurrent > 1:
                        parallel.append(other)
                        visited.add(other.task_id)

            group_id = f"parallel_{len(groups)}"
            groups[group_id] = [t.task_id for t in parallel]

        return groups

    def _assign_parallel_groups(
        self,
        tasks: list[IntentSubTask],
        parallel_groups: dict[str, list[str]],
    ) -> None:
        """将并行组ID分配给任务"""
        id_to_task = {t.task_id: t for t in tasks}
        for group_id, task_ids in parallel_groups.items():
            for tid in task_ids:
                if tid in id_to_task:
                    # 只有多个任务同组的才标记并行组
                    if len(task_ids) > 1:
                        id_to_task[tid].parallel_group = group_id

    # -------------------------------------------------------------------
    # Step 5: Agent分配
    # -------------------------------------------------------------------

    def _assign_agents(self, tasks: list[IntentSubTask]) -> None:
        """为每个子任务分配执行Agent"""
        for task in tasks:
            agent = self._find_agent_for_action(task.action)
            # Agent 已在 _build_sub_tasks 中通过 candidates 隐式指定
            # 此处可覆写或验证
            pass

    def _find_agent_for_action(self, action: str) -> Optional[AgentSpec]:
        """根据动作查找支持该动作的Agent"""
        for name, spec in self.agent_registry.items():
            if action in spec.supported_actions:
                return spec
        return None

    # -------------------------------------------------------------------
    # Step 6: 优先级计算
    # -------------------------------------------------------------------

    def _compute_priorities(self, tasks: list[IntentSubTask], intent: Intent) -> None:
        """
        计算任务优先级

        规则：
            - 基础分: 50
            - intent_type = OPERATIONAL: +20（执行类优先）
            - intent_type = INFORMATIONAL: +10
            - 有依赖（靠前）: +5
            - entities含priority=high: +30
            - 子任务越靠前: +递减权重
        """
        intent_bonus = {
            "operational":   20,
            "informational": 10,
            "analytical":    15,
            "creative":      5,
            "collaborative": 12,
        }

        bonus = intent_bonus.get(intent.intent_type.value, 0)

        # entities中的优先级
        if intent.entities.get("priority") == "high":
            bonus += 30

        for i, task in enumerate(tasks):
            depth_bonus = max(10 - i * 2, 0)  # 越靠前加分越多（递减）
            task.priority = min(50 + bonus + depth_bonus, 100)

    # -------------------------------------------------------------------
    # Step 7: 耗时预估
    # -------------------------------------------------------------------

    def _estimate_total_time(
        self,
        tasks: list[IntentSubTask],
        parallel_groups: dict[str, list[str]],
    ) -> float:
        """
        预估总耗时（毫秒）

        策略：
            - 并行组内取 max（并行执行）
            - 串行任务相加
        """
        id_to_task = {t.task_id: t for t in tasks}

        total = 0.0
        for group_id, task_ids in parallel_groups.items():
            group_tasks = [id_to_task[tid] for tid in task_ids if tid in id_to_task]
            if len(group_tasks) > 1:
                # 并行组耗时 = max
                group_cost = max(
                    self.ACTION_COST_ESTIMATE.get(t.action, 1000)
                    for t in group_tasks
                )
            else:
                group_cost = self.ACTION_COST_ESTIMATE.get(
                    group_tasks[0].action, 1000
                ) if group_tasks else 0
            total += group_cost

        return total

    # -------------------------------------------------------------------
    # Step 8: 并行度评估
    # -------------------------------------------------------------------

    def _compute_parallelism_score(
        self,
        tasks: list[IntentSubTask],
        parallel_groups: dict[str, list[str]],
        total_time: float,
    ) -> float:
        """
        并行度得分 [0, 1]

        score = (理想串行时间 - 实际时间) / 理想串行时间
        理想串行时间 = sum(所有任务耗时)
        """
        ideal_sequential = sum(
            self.ACTION_COST_ESTIMATE.get(t.action, 1000)
            for t in tasks
        )
        if ideal_sequential == 0:
            return 0.0
        score = (ideal_sequential - total_time) / ideal_sequential
        return max(0.0, min(score, 1.0))

    # -------------------------------------------------------------------
    # Step 9: 拆解置信度
    # -------------------------------------------------------------------

    def _compute_decompose_confidence(
        self,
        intent: Intent,
        tasks: list[IntentSubTask],
    ) -> float:
        """
        拆解置信度

        目标：复杂任务拆解成功率 > 90%
        """
        score = intent.confidence  # 从意图识别继承

        # 有候选子任务
        if len(tasks) > 0:
            score = max(score, 0.6)

        # 子任务数量合理（1-8个）
        if 1 <= len(tasks) <= 8:
            score = max(score, 0.7)

        # Agent覆盖完整
        agents_needed = set(intent.required_agents)
        agents_found = set()
        for task in tasks:
            agent = self._find_agent_for_action(task.action)
            if agent:
                agents_found.add(agent.name)
        coverage = len(agents_needed & agents_found) / max(len(agents_needed), 1)
        score = score * 0.5 + coverage * 0.5

        return min(score, 1.0)

    # -------------------------------------------------------------------
    # 辅助方法
    # -------------------------------------------------------------------

    def _collect_agents_used(self, tasks: list[IntentSubTask]) -> list[str]:
        """收集使用的Agent列表"""
        agents = []
        seen = set()
        for task in tasks:
            agent = self._find_agent_for_action(task.action)
            if agent and agent.name not in seen:
                agents.append(agent.name)
                seen.add(agent.name)
        return agents

    def _build_execution_plan(
        self,
        tasks: list[IntentSubTask],
        parallel_groups: dict[str, list[str]],
    ) -> dict:
        """构建可视化执行计划"""
        plan: dict[str, Any] = {
            "total_tasks": len(tasks),
            "groups": [],
        }

        id_to_task = {t.task_id: t for t in tasks}

        for group_id, task_ids in parallel_groups.items():
            group_tasks = [id_to_task[tid] for tid in task_ids if tid in id_to_task]
            is_parallel = len(group_tasks) > 1
            mode = "PARALLEL" if is_parallel else "SEQUENTIAL"
            plan["groups"].append({
                "group_id": group_id,
                "mode": mode,
                "tasks": [
                    {
                        "task_id": t.task_id,
                        "action": t.action,
                        "agent": self._find_agent_for_action(t.action).name
                            if self._find_agent_for_action(t.action) else "unknown",
                        "priority": t.priority,
                        "estimated_ms": self.ACTION_COST_ESTIMATE.get(t.action, 1000),
                    }
                    for t in group_tasks
                ],
            })

        return plan
