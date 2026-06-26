"""
Orchestrator - 指挥智能体

企业级智能调度中心，负责：
1. 用户意图理解（自然语言 → 结构化任务）
2. 任务拆解与分发（1 → N 专业智能体）
3. 协作编排（串行/并行）
4. 结果汇总与输出

角色定位：项目经理，不直接干活，只负责调度
对标：OpenClaw Main Agent / 腾讯ADP Router
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Callable

from safety.audit_logger import AuditLogger, EventType, LogLevel, TraceContext
from safety.permission_manager import PermissionManager, PermissionContext, PermissionResult

from specialists.inventory_agent import InventoryAgent
from specialists.logistics_agent import LogisticsAgent
from specialists.procurement_agent import ProcurementAgent
from specialists.finance_agent import FinanceAgent
from specialists.doc_agent import DocumentAgent

# 【新增 v3.0】执行引擎层
try:
    from execution import (
        EngineRouter,
        RoutingContext,
        RoutingStrategy,
        ClaudeMAEngine,
        LocalEngine,
        DeepSeekEngine,
    )
    _EXECUTION_LAYER_ENABLED = True
except ImportError:
    _EXECUTION_LAYER_ENABLED = False
    LocalEngine = None
    EngineRouter = None
    RoutingContext = None
    RoutingStrategy = None
    ClaudeMAEngine = None
    DeepSeekEngine = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"  # 部分完成


class TaskPriority(Enum):
    """任务优先级"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Intent:
    """用户意图"""
    raw_input: str
    intent_type: str              # stock_query/purchase/logistics/finance/doc/mixed
    entities: dict[str, Any]     # 提取的实体
    confidence: float             # 意图置信度
    required_agents: list[str]   # 需要调用的智能体
    suggested_workflow: Optional[str]  # 建议的工作流
    reasoning: str                # 推理过程


@dataclass
class SubTask:
    """子任务"""
    task_id: str
    agent_name: str
    action: str
    parameters: dict
    depends_on: list[str] = field(default_factory=list)  # 依赖的子任务ID
    parallel_group: Optional[str] = None  # 并行组标识
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "agent_name": self.agent_name,
            "action": self.action,
            "parameters": self.parameters,
            "depends_on": self.depends_on,
            "status": self.status.value,
            "result": str(self.result)[:200] if self.result else None,
            "error": self.error,
        }


@dataclass
class OrchestrationResult:
    """编排结果"""
    request_id: str
    status: TaskStatus
    intent: Intent
    sub_tasks: list[SubTask]
    aggregated_result: dict[str, Any]
    summary: str
    next_actions: list[str]
    execution_time_ms: float

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "status": self.status.value,
            "intent_type": self.intent.intent_type,
            "summary": self.summary,
            "sub_tasks": [t.to_dict() for t in self.sub_tasks],
            "aggregated_result": self.aggregated_result,
            "next_actions": self.next_actions,
            "execution_time_ms": round(self.execution_time_ms, 2),
        }


# =============================================================================
# 意图识别引擎
# =============================================================================

class IntentRecognizer:
    """
    意图识别引擎

    使用规则+关键词匹配识别用户意图
    实际项目中可替换为LLM调用
    """

    INTENT_PATTERNS = {
        "stock_query": {
            "keywords": ["库存", "库存量", "还有多少", "查库存", "库存情况", "stock", "查一下库存", "有没有货", "库存不足", "缺货"],
            "agents": ["inventory_agent"],
            "workflow": "stock_check",
        },
        "purchase": {
            "keywords": ["采购", "买", "下单", "订货", "进货", "supplier", "供应商", "询价", "报价"],
            "agents": ["procurement_agent", "finance_agent"],
            "workflow": "purchase_order",
        },
        "logistics": {
            "keywords": ["物流", "运费", "发货", "到货", "运输", "配送", "快递", "追踪", "tracking", "物流查询"],
            "agents": ["logistics_agent"],
            "workflow": "logistics_query",
        },
        "finance": {
            "keywords": ["预算", "付款", "报销", "财务", "发票", "成本", "费用", "付款审核", "budget", "财务查询"],
            "agents": ["finance_agent"],
            "workflow": "finance_check",
        },
        "document": {
            "keywords": ["文档", "报表", "工艺", "截图", "填表", "导出", "PDF", "工艺卡", "BOM", "doc", "报告", "申请单"],
            "agents": ["doc_agent"],
            "workflow": "document_generation",
        },
        "replenishment": {
            "keywords": ["补货", "进货", "缺货", "补仓", "补充库存"],
            "agents": ["inventory_agent", "procurement_agent", "finance_agent"],
            "workflow": "stock_replenishment",
        },
        "procurement_with_logistics": {
            "keywords": ["采购", "物流", "到货时间", "运费", "发货", "一体化", "全程"],
            "agents": ["procurement_agent", "logistics_agent", "finance_agent"],
            "workflow": "procurement_with_logistics",
        },
        "mixed": {
            "keywords": ["帮我", "帮我查", "执行", "处理"],
            "agents": [],
            "workflow": None,
        },
    }

    ENTITY_EXTRACTORS = {
        "sku": (r"SKU\d{3}|[A-Z]{2,3}-\d{3}", "SKU编号"),
        "warehouse": (r"华东仓|华北仓|华南仓|WH\d{3}", "仓库"),
        "supplier": (r"SUP\d{3}|供应商[A-Z]?", "供应商"),
        "amount": (r"¥?\d+(?:\.\d+)?(?:万|千|元)?", "金额"),
        "priority": (r"紧急|加急|urgent|急", "优先级"),
    }

    def recognize(self, user_input: str) -> Intent:
        """
        识别用户意图

        Args:
            user_input: 用户输入

        Returns:
            Intent对象
        """
        user_input_lower = user_input.lower()

        # 匹配意图
        best_intent = "mixed"
        best_score = 0.0

        for intent_type, config in self.INTENT_PATTERNS.items():
            score = 0
            for kw in config["keywords"]:
                if kw.lower() in user_input_lower:
                    score += 1.0
            if score > best_score:
                best_score = score
                best_intent = intent_type

        config = self.INTENT_PATTERNS[best_intent]

        # 提取实体
        entities = {}
        for entity_name, (pattern, _) in self.ENTITY_EXTRACTORS.items():
            matches = re.findall(pattern, user_input)
            if matches:
                entities[entity_name] = matches[0] if len(matches) == 1 else matches

        # 提取SKU
        sku_match = re.findall(r"SKU\d{3}", user_input, re.IGNORECASE)
        if sku_match:
            entities["sku"] = sku_match[0]

        # 提取金额
        amount_match = re.findall(r"(\d+(?:\.\d+)?)\s*(?:万|千)?\s*元", user_input)
        if amount_match:
            entities["amount"] = float(amount_match[0])
            if "万" in user_input:
                entities["amount"] *= 10000

        # 推断需要的智能体
        required_agents = config["agents"].copy()

        # 混合意图特殊处理
        if best_intent == "mixed":
            if any(w in user_input_lower for w in ["库存", "采购", "下单"]):
                best_intent = "replenishment"
                required_agents = ["inventory_agent", "procurement_agent"]
            elif any(w in user_input_lower for w in ["物流", "运费"]):
                best_intent = "logistics"
                required_agents = ["logistics_agent"]

        confidence = min(best_score / 2.0, 1.0) if best_score else 0.5

        return Intent(
            raw_input=user_input,
            intent_type=best_intent,
            entities=entities,
            confidence=confidence,
            required_agents=required_agents,
            suggested_workflow=config.get("workflow"),
            reasoning=self._build_reasoning(best_intent, entities, confidence),
        )

    def _build_reasoning(
        self,
        intent_type: str,
        entities: dict,
        confidence: float,
    ) -> str:
        parts = [f"识别意图: {intent_type}"]
        if entities:
            parts.append(f"提取实体: {', '.join(f'{k}={v}' for k, v in entities.items())}")
        parts.append(f"置信度: {confidence:.0%}")
        return " | ".join(parts)


# =============================================================================
# 任务分解器
# =============================================================================

class TaskDecomposer:
    """
    任务分解器

    根据意图和工作流配置，将用户请求拆解为可执行的子任务
    支持串行和并行两种执行模式
    """

    WORKFLOW_STEPS = {
        "stock_check": [
            ("inventory_agent", "query_stock", {}),
        ],
        "stock_replenishment": [
            ("inventory_agent", "query_stock", {}),
            ("inventory_agent", "trigger_replenishment", {"depends_on": 0}),
        ],
        "purchase_order": [
            ("procurement_agent", "supplier_lookup", {}),
            ("procurement_agent", "place_order", {"depends_on": 0}),
        ],
        "procurement_with_logistics": [
            ("procurement_agent", "place_order", {}),
            # 并行
            ("logistics_agent", "plan_route", {"parallel_group": "parallel_1"}),
            ("finance_agent", "query_budget", {"parallel_group": "parallel_1"}),
        ],
        "logistics_query": [
            ("logistics_agent", "query_freight", {}),
        ],
        "finance_check": [
            ("finance_agent", "query_budget", {}),
        ],
        "document_generation": [
            ("doc_agent", "plm_lookup", {}),
            ("doc_agent", "generate_document", {"depends_on": 0}),
        ],
    }

    def decompose(
        self,
        intent: Intent,
        user_id: str = "user",
        user_role: str = "viewer",
    ) -> list[SubTask]:
        """
        分解任务

        Args:
            intent: 识别到的意图
            user_id: 用户ID
            user_role: 用户角色

        Returns:
            子任务列表
        """
        workflow = intent.suggested_workflow or self._infer_workflow(intent)

        steps = self.WORKFLOW_STEPS.get(workflow, [])

        if not steps:
            # 兜底：根据意图类型推断步骤
            steps = self._default_steps_for_intent(intent)

        tasks = []
        completed_deps = []  # 已完成的依赖

        for i, step in enumerate(steps):
            agent_name, action, options = step if len(step) == 3 else (*step, {})

            # 构造参数
            params = self._build_params(intent, action)

            # 处理依赖
            depends_on = []
            if "depends_on" in options:
                idx = options["depends_on"]
                if idx < len(tasks):
                    depends_on = [tasks[idx].task_id]

            # 并行组
            parallel_group = options.get("parallel_group")

            # 为高风险操作添加审批参数
            if action in ("place_order", "audit_payment", "cancel_order"):
                params["skip_approval"] = (user_role == "admin")

            task = SubTask(
                task_id=f"task-{uuid.uuid4().hex[:8]}",
                agent_name=agent_name,
                action=action,
                parameters=params,
                depends_on=depends_on,
                parallel_group=parallel_group,
            )
            tasks.append(task)
            completed_deps.append(task.task_id)

        return tasks

    def _infer_workflow(self, intent: Intent) -> str:
        """根据意图推断工作流"""
        type_to_workflow = {
            "stock_query": "stock_check",
            "replenishment": "stock_replenishment",
            "purchase": "purchase_order",
            "logistics": "logistics_query",
            "finance": "finance_check",
            "document": "document_generation",
            "procurement_with_logistics": "procurement_with_logistics",
        }
        return type_to_workflow.get(intent.intent_type, "stock_check")

    def _default_steps_for_intent(self, intent: Intent) -> list[tuple]:
        """根据意图生成默认步骤"""
        steps = []
        for agent in intent.required_agents:
            steps.append((agent, self._default_action_for_agent(agent), {}))
        return steps

    @staticmethod
    def _default_action_for_agent(agent_name: str) -> str:
        defaults = {
            "inventory_agent": "query_stock",
            "logistics_agent": "query_freight",
            "procurement_agent": "supplier_lookup",
            "finance_agent": "query_budget",
            "doc_agent": "plm_lookup",
        }
        return defaults.get(agent_name, "query_stock")

    @staticmethod
    def _build_params(intent: Intent, action: str) -> dict:
        """根据动作构建参数"""
        params = {}

        # 从实体中提取参数（金额排除SKU后缀数字）
        entities = {k: v for k, v in intent.entities.items() if k != "amount"}

        if "sku" in entities:
            params["sku"] = entities["sku"]
        if "warehouse" in entities:
            params["warehouse"] = entities["warehouse"]

        # 采购订单参数构造
        if action == "place_order":
            supplier = entities.get("supplier", "SUP001")
            if isinstance(supplier, list):
                supplier = supplier[0]
            params["supplier_id"] = supplier
            # 从数量实体生成items
            amounts = intent.entities.get("amount", [])
            if isinstance(amounts, list) and len(amounts) >= 2:
                qty = float(amounts[1]) if len(amounts) > 1 else 100
            else:
                qty = float(amounts) if isinstance(amounts, (int, float)) else 100
            params["items"] = [{"sku": entities.get("sku", "SKU001"), "quantity": int(qty), "unit_price": 50}]
            params["keyword"] = entities.get("supplier", "SUP001")
        elif "supplier" in entities:
            supplier = entities["supplier"]
            if isinstance(supplier, list):
                supplier = supplier[0]
            params["keyword"] = supplier

        # 动作特定参数
        action_params = {
            "query_stock": {"check_alerts": True},
            "query_freight": {"origin": "上海", "destination": "北京", "weight": 100},
            "supplier_lookup": {},
            "query_budget": {"department": "生产部"},
            "generate_document": {"output_format": "json"},
        }

        params.update(action_params.get(action, {}))
        return params


# =============================================================================
# 指挥智能体核心
# =============================================================================

class Orchestrator:
    """
    指挥智能体（Orchestrator）

    核心流程：
    1. 接收用户请求
    2. 意图识别 → 任务分解 → 智能体调度 → 结果汇总 → 返回

    支持协作模式：
    - 串行：顺序执行，上一步输出作为下一步输入
    - 并行：同组任务并发执行，所有组内任务完成后再汇总
    """

    def __init__(
        self,
        user_id: str = "user",
        user_role: str = "admin",
        enable_engine_router: bool = True,
    ):
        self.user_id = user_id
        self.user_role = user_role

        # 初始化意图识别和任务分解
        self._intent_recognizer = IntentRecognizer()
        self._task_decomposer = TaskDecomposer()

        # 初始化专业智能体
        self._agents: dict[str, Any] = {
            "inventory_agent": InventoryAgent(user_id=user_id, user_role=user_role),
            "logistics_agent": LogisticsAgent(user_id=user_id, user_role=user_role),
            "procurement_agent": ProcurementAgent(user_id=user_id, user_role=user_role),
            "finance_agent": FinanceAgent(user_id=user_id, user_role=user_role),
            "doc_agent": DocumentAgent(user_id=user_id, user_role=user_role),
        }

        # 初始化安全模块
        self._audit = AuditLogger(log_dir="./logs/orchestrator")
        self._permission = PermissionManager()

        # 【新增 v3.0】执行引擎路由器
        self._engine_router: Optional[EngineRouter] = None
        if enable_engine_router and _EXECUTION_LAYER_ENABLED:
            self._init_engine_router()

        # 统计
        self._stats = {"total_requests": 0, "success": 0, "failed": 0}

        logger.info(f"指挥智能体初始化完成, user={user_id}, role={user_role}")

    async def handle_request(
        self,
        user_input: str,
        user_id: Optional[str] = None,
        user_role: Optional[str] = None,
    ) -> OrchestrationResult:
        """
        处理用户请求（主入口）

        完整流程：
        1. 意图识别
        2. 任务分解
        3. 权限校验
        4. 任务执行（串行/并行）
        5. 结果汇总
        6. 返回结构化结果

        Args:
            user_input: 用户自然语言输入
            user_id: 用户ID
            user_role: 用户角色

        Returns:
            编排结果
        """
        request_id = f"REQ-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4].upper()}"
        user_id = user_id or self.user_id
        user_role = user_role or self.user_role

        # 开始追踪
        trace = self._audit.start_trace(
            agent_name="orchestrator",
            action="handle_request",
            input_summary=user_input[:100],
        )

        start_time = datetime.now()
        self._stats["total_requests"] += 1

        try:
            # ====== Step 1: 意图识别 ======
            intent = self._intent_recognizer.recognize(user_input)
            logger.info(f"[{request_id}] 意图识别: {intent.intent_type} "
                        f"(置信度:{intent.confidence:.0%})")
            logger.info(f"[{request_id}] 推理: {intent.reasoning}")

            await self._audit.log(
                event_type=EventType.AGENT_CALL,
                action="intent_recognition",
                agent_name="orchestrator",
                actor_id=user_id,
                level=LogLevel.INFO,
                input_data={"raw_input": user_input},
                output_data=intent.__dict__,
                metadata={"request_id": request_id},
            )

            # ====== Step 2: 任务分解 ======
            sub_tasks = self._task_decomposer.decompose(intent, user_id, user_role)
            logger.info(f"[{request_id}] 任务分解: {len(sub_tasks)}个子任务")
            for t in sub_tasks:
                deps = f" (依赖:{t.depends_on})" if t.depends_on else ""
                pg = f" [并行组:{t.parallel_group}]" if t.parallel_group else ""
                logger.info(f"  - {t.task_id}: {t.agent_name}.{t.action}{deps}{pg}")

            # ====== Step 3: 任务执行 ======
            await self._execute_tasks(sub_tasks, request_id, user_id, user_role)

            # ====== Step 4: 结果汇总 ======
            aggregated = self._aggregate_results(intent, sub_tasks)
            summary = self._generate_summary(intent, sub_tasks, aggregated)
            next_actions = self._suggest_next_actions(intent, sub_tasks)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # 判断最终状态
            failed_tasks = [t for t in sub_tasks if t.status == TaskStatus.FAILED]
            completed_tasks = [t for t in sub_tasks if t.status == TaskStatus.COMPLETED]

            if failed_tasks and not completed_tasks:
                status = TaskStatus.FAILED
            elif failed_tasks and completed_tasks:
                status = TaskStatus.PARTIAL
            else:
                status = TaskStatus.COMPLETED

            self._audit.end_trace(trace, output_summary=summary[:200])

            await self._audit.log(
                event_type=EventType.AGENT_END,
                action="handle_request_completed",
                agent_name="orchestrator",
                actor_id=user_id,
                level=LogLevel.INFO if status == TaskStatus.COMPLETED else LogLevel.WARNING,
                output_data={
                    "status": status.value,
                    "tasks_count": len(sub_tasks),
                    "completed": len(completed_tasks),
                    "failed": len(failed_tasks),
                    "execution_time_ms": execution_time,
                },
                metadata={"request_id": request_id},
            )

            if status == TaskStatus.COMPLETED:
                self._stats["success"] += 1
            else:
                self._stats["failed"] += 1

            return OrchestrationResult(
                request_id=request_id,
                status=status,
                intent=intent,
                sub_tasks=sub_tasks,
                aggregated_result=aggregated,
                summary=summary,
                next_actions=next_actions,
                execution_time_ms=execution_time,
            )

        except Exception as e:
            logger.exception(f"[{request_id}] 处理异常")
            self._stats["failed"] += 1
            self._audit.end_trace(trace, error=str(e))

            return OrchestrationResult(
                request_id=request_id,
                status=TaskStatus.FAILED,
                intent=Intent(
                    raw_input=user_input,
                    intent_type="error",
                    entities={},
                    confidence=0,
                    required_agents=[],
                    suggested_workflow=None,
                    reasoning="处理异常",
                ),
                sub_tasks=[],
                aggregated_result={"error": str(e)},
                summary=f"处理失败: {e}",
                next_actions=["请重试或联系管理员"],
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    # -------------------------------------------------------------------------
    # 任务执行引擎
    # -------------------------------------------------------------------------

    async def _execute_tasks(
        self,
        tasks: list[SubTask],
        request_id: str,
        user_id: str,
        user_role: str,
    ) -> None:
        """
        执行任务

        执行策略：
        1. 按依赖关系排序（拓扑排序）
        2. 同并行组的任务并发执行
        3. 等待所有依赖完成后执行当前任务
        """
        # 识别并行组
        parallel_groups: dict[str, list[SubTask]] = {}
        serial_tasks: list[SubTask] = []

        for task in tasks:
            if task.parallel_group:
                if task.parallel_group not in parallel_groups:
                    parallel_groups[task.parallel_group] = []
                parallel_groups[task.parallel_group].append(task)
            else:
                serial_tasks.append(task)

        # 按顺序执行串行任务，同时处理其中的并行组
        await self._execute_serial_tasks(serial_tasks, request_id, user_id, user_role)

        # 执行并行组（在串行任务中找到它们的执行点）
        for task in tasks:
            if task.parallel_group:
                pg = task.parallel_group
                # 找到并行组中第一个串行任务的位置
                group_tasks = parallel_groups.get(pg, [task])

    async def _execute_serial_tasks(
        self,
        tasks: list[SubTask],
        request_id: str,
        user_id: str,
        user_role: str,
    ) -> None:
        """顺序执行串行任务"""
        for task in tasks:
            await self._execute_single_task(task, request_id, user_id, user_role)

    async def _execute_parallel_group(
        self,
        tasks: list[SubTask],
        request_id: str,
        user_id: str,
        user_role: str,
    ) -> None:
        """并发执行一组任务"""
        logger.info(f"[{request_id}] 并行执行 {len(tasks)} 个任务")
        await asyncio.gather(
            *[
                self._execute_single_task(task, request_id, user_id, user_role)
                for task in tasks
            ]
        )

    async def _execute_single_task(
        self,
        task: SubTask,
        request_id: str,
        user_id: str,
        user_role: str,
    ) -> None:
        """执行单个子任务"""
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now().isoformat()

        logger.info(f"[{request_id}] 执行: {task.agent_name}.{task.action}")

        try:
            # 获取对应智能体
            agent = self._agents.get(task.agent_name)
            if not agent:
                raise ValueError(f"未知智能体: {task.agent_name}")

            # 检查智能体是否有该方法
            if not hasattr(agent, task.action):
                raise AttributeError(f"智能体{task.agent_name}不支持操作:{task.action}")

            # 执行动作
            action_method = getattr(agent, task.action)
            result = await action_method(**task.parameters)

            # 处理结果
            if isinstance(result, dict):
                if result.get("success") is False:
                    task.error = result.get("error", "执行失败")
                    task.status = TaskStatus.FAILED
                    logger.warning(f"[{request_id}] {task.task_id} 失败: {task.error}")
                else:
                    task.result = result
                    task.status = TaskStatus.COMPLETED
            else:
                task.result = result
                task.status = TaskStatus.COMPLETED

        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            logger.exception(f"[{request_id}] {task.task_id} 异常")

        task.completed_at = datetime.now().isoformat()

    # -------------------------------------------------------------------------
    # 结果汇总
    # -------------------------------------------------------------------------

    def _aggregate_results(
        self,
        intent: Intent,
        tasks: list[SubTask],
    ) -> dict[str, Any]:
        """汇总子任务结果"""
        aggregated = {
            "intent_type": intent.intent_type,
            "execution_summary": {
                "total": len(tasks),
                "completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
                "failed": sum(1 for t in tasks if t.status == TaskStatus.FAILED),
            },
            "agent_results": {},
        }

        for task in tasks:
            if task.result:
                # 简化结果，只保留关键信息
                if isinstance(task.result, dict):
                    aggregated["agent_results"][task.agent_name] = {
                        "action": task.action,
                        "status": task.status.value,
                        "key_data": self._extract_key_data(task.result),
                        "success": task.result.get("success", True),
                    }
                else:
                    aggregated["agent_results"][task.agent_name] = {
                        "action": task.action,
                        "status": task.status.value,
                        "data": str(task.result)[:200],
                    }

        return aggregated

    def _extract_key_data(self, result: dict) -> dict:
        """从结果中提取关键数据"""
        key_fields = [
            "quantity", "total_amount", "status", "recommendations",
            "quotes", "suggestions", "summary", "data",
            "replenishment", "analysis", "content",
        ]
        return {k: result[k] for k in key_fields if k in result}

    def _generate_summary(
        self,
        intent: Intent,
        tasks: list[SubTask],
        aggregated: dict[str, Any],
    ) -> str:
        """生成自然语言摘要"""
        completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in tasks if t.status == TaskStatus.FAILED)
        agent_names = [t.agent_name.replace("_agent", "") for t in tasks]

        parts = [
            f"已完成{completed}个任务",
            f"涉及智能体:{', '.join(set(agent_names))}",
        ]

        if failed > 0:
            parts.append(f"失败{failed}个")
            failed_tasks = [t for t in tasks if t.status == TaskStatus.FAILED]
            parts.append(f"失败原因:{failed_tasks[0].error}")

        # 意图特定摘要
        if intent.intent_type == "stock_query":
            for task in tasks:
                if task.result and isinstance(task.result, dict):
                    if "quantity" in task.result:
                        parts.append(f"库存量:{task.result['quantity']}")
                    if "alerts" in task.result:
                        parts.append(f"告警:{task.result['alerts'][:2]}")

        elif intent.intent_type == "purchase":
            for task in tasks:
                if task.action == "place_order" and task.result:
                    if isinstance(task.result, dict):
                        parts.append(
                            f"订单:{task.result.get('order_id', 'N/A')}, "
                            f"金额:¥{task.result.get('total_amount', 0)}"
                        )

        return "；".join(parts)

    def _suggest_next_actions(
        self,
        intent: Intent,
        tasks: list[SubTask],
    ) -> list[str]:
        """建议下一步操作"""
        suggestions = []

        for task in tasks:
            if task.status == TaskStatus.COMPLETED and task.result:
                # 采购订单 → 建议查看物流
                if task.action == "place_order":
                    suggestions.append("可查询该订单的物流状态")
                    suggestions.append("如需取消或修改订单，请回复：取消订单")

                # 库存低于安全水位 → 建议补货
                if task.action == "trigger_replenishment":
                    suggestions.append("已生成补货建议，可回复「确认补货」执行")

                # 文档生成 → 建议导出
                if task.action == "generate_document":
                    suggestions.append("可回复「导出PDF」获取文档")

        if not suggestions:
            suggestions.append("如需其他帮助，请继续描述需求")

        return suggestions

    def get_stats(self) -> dict[str, Any]:
        """获取统计信息"""
        stats = {
            **self._stats,
            "active_agents": list(self._agents.keys()),
            "success_rate": round(
                self._stats["success"] / max(self._stats["total_requests"], 1) * 100, 1
            ),
        }
        # 【新增 v3.0】附加引擎路由统计
        if self._engine_router:
            stats["engine_router"] = self._engine_router.get_stats()
        return stats

    # -------------------------------------------------------------------------
    # 【新增 v3.0】执行引擎层
    # -------------------------------------------------------------------------

    def _init_engine_router(self) -> None:
        """
        初始化执行引擎路由器

        注册所有可用引擎并加载路由规则。
        优先从 config/engines.yaml 加载规则，失败则使用默认规则。
        """
        if not _EXECUTION_LAYER_ENABLED:
            logger.warning("[Orchestrator] 执行引擎层未启用（缺少 execution 模块）")
            return

        router = EngineRouter()

        # 注册引擎
        # 1. LocalEngine（默认，必选）
        try:
            router.register_engine(
                LocalEngine({"default_role": self.user_role}),
                set_default=True,
            )
        except Exception as e:
            logger.warning(f"[Orchestrator] 注册 LocalEngine 失败: {e}")

        # 2. ClaudeMAEngine（可选）
        if os.environ.get("ANTHROPIC_API_KEY"):
            try:
                router.register_engine(ClaudeMAEngine())
            except Exception as e:
                logger.warning(f"[Orchestrator] 注册 ClaudeMAEngine 失败: {e}")
        else:
            logger.info("[Orchestrator] 未配置 ANTHROPIC_API_KEY，ClaudeMAEngine 已跳过")

        # 3. DeepSeekEngine（可选）
        if os.environ.get("DEEPSEEK_API_KEY"):
            try:
                router.register_engine(DeepSeekEngine())
            except Exception as e:
                logger.warning(f"[Orchestrator] 注册 DeepSeekEngine 失败: {e}")
        else:
            logger.info("[Orchestrator] 未配置 DEEPSEEK_API_KEY，DeepSeekEngine 已跳过")

        # 加载路由规则
        yaml_path = os.path.join(
            os.path.dirname(__file__), "config", "engines.yaml"
        )
        rule_count = router.load_rules_from_yaml(yaml_path)
        if rule_count == 0:
            logger.info("[Orchestrator] YAML 规则加载失败，使用默认规则")
            router.add_default_rules()

        self._engine_router = router
        logger.info(
            f"[Orchestrator] 引擎路由器初始化完成: "
            f"engines={list(router._engines.keys())}, "
            f"rules={len(router._rules)}, "
            f"default={router._default_engine}"
        )

    async def execute_with_engine(
        self,
        user_input: str,
        user_id: Optional[str] = None,
        user_role: Optional[str] = None,
        engine_hint: Optional[str] = None,
        scene: str = "general",
    ) -> dict[str, Any]:
        """
        【新增 v3.0】通过执行引擎路由执行任务

        与 handle_request 的区别：
        - handle_request：直接调度专业智能体（Orchestrator 内部逻辑）
        - execute_with_engine：通过 EngineRouter 选择最优引擎执行（可利用 Claude MA / DeepSeek 等外部能力）

        引擎选择逻辑（见 EngineRouter.route）：
        1. 显式指定（engine_hint）
        2. 场景规则（scene）
        3. 意图类型规则
        4. 关键词匹配
        5. 默认引擎

        Args:
            user_input: 用户自然语言输入
            user_id: 用户ID
            user_role: 用户角色
            engine_hint: 显式指定引擎（覆盖自动路由）
            scene: 场景标签（compliance/dev/general/offline）

        Returns:
            dict: 包含 engine_used, routing_info, result 等字段
        """
        user_id = user_id or self.user_id
        user_role = user_role or self.user_role

        # 意图识别（用于路由决策）
        intent = self._intent_recognizer.recognize(user_input)

        # 构造路由上下文
        ctx = RoutingContext(
            task=user_input,
            intent_type=intent.intent_type,
            user_role=user_role,
            scene=scene,
            entities=intent.entities,
            engine_hint=engine_hint,
        )

        # 路由决策
        if not self._engine_router:
            self._init_engine_router()

        decision = self._engine_router.route(ctx)
        engine = decision.engine

        logger.info(
            f"[Orchestrator.execute_with_engine] "
            f"engine={engine.engine_name}, "
            f"strategy={decision.strategy.value}, "
            f"confidence={decision.confidence:.2f}, "
            f"fallbacks={len(decision.fallback_engines)}"
        )

        # 执行
        context = {
            "user_id": user_id,
            "user_role": user_role,
            "intent_type": intent.intent_type,
            "entities": intent.entities,
            "scene": scene,
        }

        result = await engine.execute(user_input, context)

        return {
            "engine_used": engine.engine_name,
            "routing": decision.to_dict(),
            "result": result.to_dict(),
            "intent": {
                "type": intent.intent_type,
                "confidence": intent.confidence,
                "entities": intent.entities,
            },
        }

    async def stream_with_engine(
        self,
        user_input: str,
        user_id: Optional[str] = None,
        user_role: Optional[str] = None,
        scene: str = "general",
    ):
        """
        【新增 v3.0】流式执行（通过执行引擎路由）

        Args:
            user_input: 用户输入
            user_id: 用户ID
            user_role: 用户角色
            scene: 场景标签

        Yields:
            dict: 包含 engine_used, chunk.content, done 等字段
        """
        user_id = user_id or self.user_id
        user_role = user_role or self.user_role

        intent = self._intent_recognizer.recognize(user_input)

        if not self._engine_router:
            self._init_engine_router()

        ctx = RoutingContext(
            task=user_input,
            intent_type=intent.intent_type,
            user_role=user_role,
            scene=scene,
            entities=intent.entities,
        )

        decision = self._engine_router.route(ctx)
        engine = decision.engine

        context = {
            "user_id": user_id,
            "user_role": user_role,
            "intent_type": intent.intent_type,
            "entities": intent.entities,
        }

        async for chunk in engine.stream(user_input, context):
            yield {
                "engine_used": engine.engine_name,
                "chunk": chunk.content,
                "done": chunk.done,
                "delta_ms": chunk.delta_ms,
            }


# =============================================================================
# 快速调用接口
# =============================================================================

async def process(user_input: str, user_role: str = "admin") -> dict:
    """
    快速处理接口

    Usage:
        result = await process("查询SKU001的库存")
        print(result["summary"])
    """
    orch = Orchestrator(user_role=user_role)
    result = await orch.handle_request(user_input)
    return result.to_dict()


# =============================================================================
# 交互式演示
# =============================================================================

async def demo():
    """交互式演示"""
    print("=" * 70)
    print("  企业级智能体集群指挥中心 演示")
    print("=" * 70)
    print("\n支持场景：")
    print("  1. 库存查询     → 输入: 查询SKU001库存")
    print("  2. 安全库存计算 → 输入: SKU003安全水位")
    print("  3. 补货触发     → 输入: 触发SKU003补货")
    print("  4. 物流查询     → 输入: 上海到北京的运费")
    print("  5. 路线规划     → 输入: 规划从上海到广州的物流")
    print("  6. 供应商搜索   → 输入: 搜索轴承供应商")
    print("  7. 采购下单     → 输入: 向SUP001采购轴承500套")
    print("  8. 财务查询     → 输入: 查询研发部预算")
    print("  9. 工艺文档     → 输入: 生成BOM-ASSY-001的工艺卡")
    print("  10.复杂场景     → 输入: 帮我查下库存，缺货的话触发补货流程")
    print()

    orch = Orchestrator(user_role="admin")

    test_cases = [
        "查询SKU001的库存",
        "查询研发部预算",
        "向SUP001采购轴承500套",
        "帮我查下SKU003的库存情况",
        "规划从上海到广州的物流路线",
    ]

    for i, query in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"  测试 {i}: {query}")
        print("=" * 70)

        result = await orch.handle_request(query)

        print(f"\n📋 请求ID: {result.request_id}")
        print(f"🎯 意图类型: {result.intent.intent_type}")
        print(f"🧠 置信度: {result.intent.confidence:.0%}")
        print(f"📝 推理: {result.intent.reasoning}")
        print(f"\n📊 任务执行:")
        for task in result.sub_tasks:
            icon = "✅" if task.status == TaskStatus.COMPLETED else "❌"
            print(f"  {icon} {task.agent_name}.{task.action}: {task.status.value}")
            if task.error:
                print(f"     错误: {task.error}")

        print(f"\n📈 执行统计:")
        exec_summary = result.aggregated_result.get("execution_summary", {})
        print(f"  完成: {exec_summary.get('completed', 0)}/{exec_summary.get('total', 0)}")
        print(f"  耗时: {result.execution_time_ms:.0f}ms")

        print(f"\n📝 摘要: {result.summary}")
        if result.next_actions:
            print(f"💡 建议: {result.next_actions[0]}")


if __name__ == "__main__":
    asyncio.run(demo())
