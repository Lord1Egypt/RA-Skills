"""
Human-in-the-Loop (HITL) 人机回环确认模块

高风险操作的强制人工审批机制：
- 风险等级评估
- 审批工作流
- 异步确认（支持WebSocket/邮件/飞书等渠道）
- 超时处理策略
- 决策追踪
"""

from __future__ import annotations

import asyncio
import uuid
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"           # 低风险，自动放行
    MEDIUM = "medium"     # 中风险，记录日志
    HIGH = "high"         # 高风险，需要审批
    CRITICAL = "critical"  # 极高风险，严谨审批


class ApprovalStatus(Enum):
    """审批状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class ApprovalChannel(Enum):
    """审批渠道"""
    WEBHOOK = "webhook"       # Webhook回调
    EMAIL = "email"           # 邮件确认
    FEISHU = "feishu"         # 飞书审批
    CONSOLE = "console"       # 控制台（开发测试）
    SMS = "sms"               # 短信确认


@dataclass
class ApprovalRequest:
    """审批请求"""
    request_id: str
    agent_name: str
    action: str
    description: str
    parameters: dict
    risk_level: RiskLevel
    requested_by: str
    requested_at: str = field(default_factory=lambda: datetime.now().isoformat())
    timeout_seconds: int = 300
    channel: ApprovalChannel = ApprovalChannel.CONSOLE
    status: ApprovalStatus = ApprovalStatus.PENDING
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    comments: str = ""
    audit_ref: str = ""


@dataclass
class HITLResult:
    """人机回环结果"""
    approved: bool
    request_id: str
    approved_by: Optional[str] = None
    comments: str = ""
    duration_seconds: float = 0.0
    channel: str = ""


# =============================================================================
# 审批渠道处理器
# =============================================================================

class ApprovalChannelHandler:
    """审批渠道抽象基类"""

    async def send_approval(self, req: ApprovalRequest) -> bool:
        """发送审批请求"""
        raise NotImplementedError

    async def get_approval(self, request_id: str) -> Optional[HITLResult]:
        """获取审批结果（轮询模式）"""
        raise NotImplementedError


class WebhookHandler(ApprovalChannelHandler):
    """Webhook审批处理器"""

    def __init__(self, webhook_url: str, secret: str = ""):
        self.webhook_url = webhook_url
        self.secret = secret

    async def send_approval(self, req: ApprovalRequest) -> bool:
        """通过Webhook发送审批请求"""
        import json
        logger.info(f"[Webhook] 发送审批请求: {req.request_id}")
        # 实际项目中使用httpx/aiohttp发送HTTP POST请求
        payload = {
            "request_id": req.request_id,
            "agent_name": req.agent_name,
            "action": req.action,
            "description": req.description,
            "risk_level": req.risk_level.value,
            "parameters": req.parameters,
            "callback_url": f"https://internal.company.com/hitl/callback/{req.request_id}",
        }
        logger.info(f"[Webhook] Payload: {json.dumps(payload, ensure_ascii=False)[:200]}")
        return True

    async def get_approval(self, request_id: str) -> Optional[HITLResult]:
        """从回调存储中获取审批结果"""
        return None


class ConsoleHandler(ApprovalChannelHandler):
    """控制台审批处理器（开发测试用）"""

    async def send_approval(self, req: ApprovalRequest) -> bool:
        """在控制台打印审批请求"""
        print("\n" + "=" * 70)
        print(f"  ⏳ 人工审批请求 - [{req.risk_level.value.upper()}]")
        print("=" * 70)
        print(f"  请求ID:    {req.request_id}")
        print(f"  智能体:    {req.agent_name}")
        print(f"  操作:      {req.action}")
        print(f"  描述:      {req.description}")
        print(f"  申请人:    {req.requested_by}")
        print(f"  超时:      {req.timeout_seconds}秒")
        print("-" * 70)
        print("  参数:")
        for k, v in (req.parameters or {}).items():
            print(f"    {k}: {v}")
        print("=" * 70)
        return True

    async def get_approval(self, request_id: str) -> Optional[HITLResult]:
        """
        从控制台获取审批输入

        开发模式下支持：
        - 直接输入 approve/reject
        - 超时自动拒绝
        """
        print(f"\n[审批输入] 请输入审批决定 ({request_id[:8]}): ", end="", flush=True)
        try:
            # 异步读取（开发模式使用简单input）
            loop = asyncio.get_event_loop()
            choice = await asyncio.wait_for(
                loop.run_in_executor(None, input),
                timeout=300,
            )
            choice = choice.strip().lower()

            if choice in ("y", "yes", "approve", "a", "通过", "同意"):
                return HITLResult(
                    approved=True,
                    request_id=request_id,
                    approved_by="console_user",
                    comments="控制台审批通过",
                    duration_seconds=5.0,
                    channel="console",
                )
            elif choice in ("n", "no", "reject", "r", "拒绝", "不同意"):
                return HITLResult(
                    approved=False,
                    request_id=request_id,
                    approved_by="console_user",
                    comments="控制台审批拒绝",
                    duration_seconds=5.0,
                    channel="console",
                )
            else:
                print("  无效输入，默认拒绝")
                return HITLResult(
                    approved=False,
                    request_id=request_id,
                    approved_by="console_user",
                    comments="无效输入",
                    channel="console",
                )
        except asyncio.TimeoutError:
            return HITLResult(
                approved=False,
                request_id=request_id,
                approved_by="system",
                comments="审批超时自动拒绝",
                duration_seconds=300,
                channel="console",
            )


class EmailHandler(ApprovalChannelHandler):
    """邮件审批处理器"""

    def __init__(self, smtp_config: dict):
        self.smtp_config = smtp_config

    async def send_approval(self, req: ApprovalRequest) -> bool:
        """发送审批邮件"""
        logger.info(f"[Email] 发送审批邮件: {req.request_id}")
        # 实际项目中调用email_request工具
        logger.info(f"[Email] 收件人: 审批管理员, 主题: [{req.risk_level.value}] {req.description}")
        return True

    async def get_approval(self, request_id: str) -> Optional[HITLResult]:
        """轮询邮件系统获取审批回复"""
        # 实际项目中定期检查邮件回复
        return None


# =============================================================================
# 风险评估器
# =============================================================================

class RiskAssessor:
    """
    风险等级自动评估器

    评估维度：
    1. 操作金额（财务操作）
    2. 操作类型（不可逆操作权重更高）
    3. 数据敏感性
    4. 历史行为异常
    5. 时段因素（夜间操作加风险）
    """

    RISK_WEIGHTS = {
        "amount": 0.35,
        "operation_type": 0.30,
        "data_sensitivity": 0.20,
        "time_factor": 0.10,
        "history": 0.05,
    }

    AMOUNT_RISK_THRESHOLDS = [
        (100000, 0.8),   # 10万以上 -> 高风险
        (50000, 0.6),    # 5万以上 -> 中高风险
        (10000, 0.4),    # 1万以上 -> 中风险
        (0, 0.1),        # 其他 -> 低风险
    ]

    IRREVERSIBLE_ACTIONS = {
        "cancel_order": 0.7,
        "delete": 0.8,
        "revoke": 0.7,
        "terminate": 0.9,
        "adjust_budget": 0.6,
    }

    SENSITIVE_DATA_TYPES = {
        "financial_data": 0.5,
        "supplier_data": 0.3,
        "personal_data": 0.6,
        "pricing_data": 0.4,
    }

    def assess(
        self,
        agent_name: str,
        action: str,
        parameters: dict,
        actor_role: str,
    ) -> tuple[RiskLevel, float, str]:
        """
        评估风险等级

        Returns:
            (风险等级, 风险分数, 评估理由)
        """
        score = 0.0
        reasons = []

        # 1. 金额风险
        amount = parameters.get("total_amount") or parameters.get("amount") or 0
        for threshold, risk_score in self.AMOUNT_RISK_THRESHOLDS:
            if amount >= threshold:
                if risk_score > 0:
                    score += risk_score * self.RISK_WEIGHTS["amount"]
                    reasons.append(f"金额风险: ¥{amount} (权重{self.RISK_WEIGHTS['amount']})")
                break

        # 2. 操作类型风险
        for irreversible, risk_score in self.IRREVERSIBLE_ACTIONS.items():
            if irreversible in action.lower():
                score += risk_score * self.RISK_WEIGHTS["operation_type"]
                reasons.append(f"不可逆操作: {action} (权重{self.RISK_WEIGHTS['operation_type']})")
                break

        # 3. 数据敏感性
        sensitive_keys = ["password", "token", "secret", "credit_card"]
        if any(k in str(parameters) for k in sensitive_keys):
            score += self.SENSITIVE_DATA_TYPES["personal_data"] * self.RISK_WEIGHTS["data_sensitivity"]
            reasons.append(f"敏感数据访问 (权重{self.RISK_WEIGHTS['data_sensitivity']})")

        # 4. 时间因素（夜间操作）
        hour = datetime.now().hour
        if hour < 7 or hour > 21:
            score += 0.15 * self.RISK_WEIGHTS["time_factor"]
            reasons.append(f"非工作时间操作({hour}点)")

        # 5. 角色风险加成
        if actor_role in ["viewer", "warehouse_operator"]:
            if "finance" in agent_name or "procurement" in agent_name:
                score += 0.2
                reasons.append("角色权限异常访问")

        # 归一化
        score = min(score, 1.0)

        # 风险等级判定
        if score >= 0.7:
            level = RiskLevel.CRITICAL
        elif score >= 0.5:
            level = RiskLevel.HIGH
        elif score >= 0.3:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        reason = "; ".join(reasons) if reasons else "标准流程"

        return level, score, reason


# =============================================================================
# 人机回环核心类
# =============================================================================

class HumanInTheLoop:
    """
    人机回环审批控制器

    核心功能：
    - 风险自动评估
    - 审批流程编排
    - 多渠道支持
    - 超时处理
    - 审批历史追踪
    """

    def __init__(
        self,
        default_channel: ApprovalChannel = ApprovalChannel.CONSOLE,
        default_timeout: int = 300,
    ):
        self._pending_requests: dict[str, ApprovalRequest] = {}
        self._request_history: list[ApprovalRequest] = []
        self._handlers: dict[ApprovalChannel, ApprovalChannelHandler] = {
            ApprovalChannel.CONSOLE: ConsoleHandler(),
            ApprovalChannel.WEBHOOK: WebhookHandler("https://internal.company.com/hitl/webhook"),
            ApprovalChannel.EMAIL: EmailHandler({}),
        }
        self._default_channel = default_channel
        self._default_timeout = default_timeout
        self._risk_assessor = RiskAssessor()

        logger.info(f"HITL初始化完成，默认渠道={default_channel.value}，超时={default_timeout}秒")

    def set_handler(self, channel: ApprovalChannel, handler: ApprovalChannelHandler) -> None:
        """注册审批渠道处理器"""
        self._handlers[channel] = handler

    def assess_and_request(
        self,
        agent_name: str,
        action: str,
        parameters: dict,
        requested_by: str = "system",
        force_approval: bool = False,
    ) -> tuple[RiskLevel, Optional[str]]:
        """
        风险评估并自动决定是否需要人工审批

        Returns:
            (风险等级, 如果需要审批则返回request_id，否则None)
        """
        level, score, reason = self._risk_assessor.assess(
            agent_name, action, parameters, requested_by
        )

        logger.info(
            f"[风险评估] {agent_name}.{action}: "
            f"level={level.value} score={score:.2f} reason={reason}"
        )

        # 决定是否需要审批
        needs_approval = force_approval or level in (RiskLevel.HIGH, RiskLevel.CRITICAL)

        if needs_approval:
            request_id = self._create_approval_request(
                agent_name=agent_name,
                action=action,
                parameters=parameters,
                risk_level=level,
                requested_by=requested_by,
                description=f"风险评估触发审批: {reason}",
            )
            return level, request_id

        return level, None

    def _create_approval_request(
        self,
        agent_name: str,
        action: str,
        parameters: dict,
        risk_level: RiskLevel,
        requested_by: str,
        description: str,
    ) -> str:
        """创建审批请求"""
        request_id = f"HITL-{datetime.now().strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:6].upper()}"

        req = ApprovalRequest(
            request_id=request_id,
            agent_name=agent_name,
            action=action,
            description=description,
            parameters=parameters,
            risk_level=risk_level,
            requested_by=requested_by,
            timeout_seconds=self._default_timeout,
            channel=self._default_channel,
            audit_ref=request_id,
        )

        self._pending_requests[request_id] = req
        return request_id

    async def request_approval(
        self,
        agent_name: str,
        action: str,
        parameters: dict,
        requested_by: str = "system",
        description: str = "",
        channel: Optional[ApprovalChannel] = None,
        timeout_seconds: Optional[int] = None,
    ) -> HITLResult:
        """
        发起人工审批请求

        执行流程：
        1. 风险评估
        2. 如需审批，发送到对应渠道
        3. 等待审批结果
        4. 返回最终决策
        """
        # 风险评估
        level, request_id = self.assess_and_request(
            agent_name, action, parameters, requested_by
        )

        if request_id is None:
            # 低风险，自动批准
            return HITLResult(
                approved=True,
                request_id="auto",
                approved_by="system",
                comments=f"风险等级{level.value}，自动批准",
                channel="auto",
            )

        # 发送审批请求
        req = self._pending_requests[request_id]
        if description:
            req.description = description
        if timeout_seconds:
            req.timeout_seconds = timeout_seconds
        if channel:
            req.channel = channel

        handler = self._handlers.get(req.channel, self._handlers[self._default_channel])
        await handler.send_approval(req)

        # 等待审批结果
        start_time = datetime.now()
        result = await self._wait_for_approval(request_id, req.timeout_seconds)

        # 更新请求状态
        req.status = ApprovalStatus.APPROVED if result.approved else ApprovalStatus.REJECTED
        if result.approved:
            req.approved_by = result.approved_by
            req.approved_at = datetime.now().isoformat()
        req.comments = result.comments

        # 归档到历史
        self._request_history.append(req)
        del self._pending_requests[request_id]

        # 记录决策
        logger.info(
            f"[审批决策] {request_id}: "
            f"{'✅ APPROVED' if result.approved else '❌ REJECTED'} "
            f"by {result.approved_by}, {result.comments}"
        )

        return result

    async def _wait_for_approval(
        self,
        request_id: str,
        timeout_seconds: int,
    ) -> HITLResult:
        """等待审批结果（轮询模式）"""
        handler = self._handlers[self._default_channel]

        # 轮询直到有结果或超时
        for attempt in range(timeout_seconds // 5):
            await asyncio.sleep(5)

            result = await handler.get_approval(request_id)
            if result:
                return result

            # 进度日志
            elapsed = (attempt + 1) * 5
            if elapsed % 30 == 0:
                logger.info(f"[审批等待] {request_id} 等待中，已过{elapsed}秒...")

        # 超时处理
        return HITLResult(
            approved=False,
            request_id=request_id,
            approved_by="system",
            comments="审批超时未响应",
            duration_seconds=float(timeout_seconds),
            channel="timeout",
        )

    def get_pending_requests(self, agent_name: Optional[str] = None) -> list[dict]:
        """获取待审批请求列表"""
        results = []
        for req in self._pending_requests.values():
            if agent_name is None or req.agent_name == agent_name:
                results.append({
                    "request_id": req.request_id,
                    "agent_name": req.agent_name,
                    "action": req.action,
                    "risk_level": req.risk_level.value,
                    "description": req.description,
                    "requested_by": req.requested_by,
                    "waiting_seconds": (
                        datetime.now() - datetime.fromisoformat(req.requested_at)
                    ).total_seconds(),
                    "status": req.status.value,
                })
        return results

    def get_history(self, limit: int = 50) -> list[dict]:
        """获取审批历史"""
        return [
            {
                "request_id": r.request_id,
                "agent_name": r.agent_name,
                "action": r.action,
                "risk_level": r.risk_level.value,
                "status": r.status.value,
                "approved_by": r.approved_by,
                "requested_at": r.requested_at,
                "comments": r.comments,
            }
            for r in self._request_history[-limit:]
        ]


# =============================================================================
# 装饰器：自动人机回环
# =============================================================================

def requires_approval(
    channel: ApprovalChannel = ApprovalChannel.CONSOLE,
    timeout: int = 300,
):
    """
    方法级人机回环装饰器

    Usage:
        @requires_approval(channel=ApprovalChannel.FEISHU, timeout=600)
        async def place_order(supplier_id: str, amount: float):
            # 此处代码仅在审批通过后执行
            ...
    """
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            hitl = HumanInTheLoop(default_channel=channel, default_timeout=timeout)

            # 从参数推断agent和action
            agent_name = kwargs.get("_agent", "unknown_agent")
            action = func.__name__

            # 获取金额参数
            amount = kwargs.get("amount") or kwargs.get("total_amount") or 0

            result = await hitl.request_approval(
                agent_name=agent_name,
                action=action,
                parameters={**kwargs, "amount": amount},
                requested_by=kwargs.get("user_id", "system"),
            )

            if not result.approved:
                raise PermissionError(f"审批未通过: {result.comments}")

            # 审批通过，执行原方法
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  人机回环系统测试")
    print("=" * 60)

    async def test():
        hitl = HumanInTheLoop(
            default_channel=ApprovalChannel.CONSOLE,
            default_timeout=60,
        )

        # 测试1: 低风险（自动批准）
        print("\n[测试1] 低风险操作评估")
        level, req_id = hitl.assess_and_request(
            agent_name="inventory_agent",
            action="query_stock",
            parameters={"sku": "SKU001"},
            requested_by="viewer",
        )
        print(f"  结果: {level.value}, {'需审批' if req_id else '自动批准'}")

        # 测试2: 高金额（需审批）
        print("\n[测试2] 高金额采购审批")
        result = await hitl.request_approval(
            agent_name="procurement_agent",
            action="place_order",
            parameters={
                "supplier_id": "SUP001",
                "total_amount": 80000,
                "items": [{"sku": "SKU001", "quantity": 500}],
            },
            requested_by="buyer001",
            description="紧急采购电机轴承500套",
        )
        print(f"  审批结果: {'✅ 通过' if result.approved else '❌ 拒绝'}")
        print(f"  审批人: {result.approved_by}")
        print(f"  备注: {result.comments}")

        # 测试3: 审批历史
        print("\n[审批历史]")
        history = hitl.get_history()
        for h in history:
            print(f"  {h['request_id']}: {h['action']} -> {h['status']} by {h['approved_by']}")

    asyncio.run(test())
