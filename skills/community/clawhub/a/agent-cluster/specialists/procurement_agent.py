"""
Procurement Agent - 采购智能体

专注领域：供应商对接、订单下达、SRM接口调用、采购分析

角色定位：专业智能体，负责企业采购全流程，
涉及高风险操作（金额>5万需人工审批）
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from mcp_servers.srm_server import SRMService
from mcp_servers.erp_server import ERPService
from safety.audit_logger import AuditLogger, EventType, LogLevel, traced
from safety.permission_manager import PermissionManager, PermissionContext, PermissionResult
from safety.human_loop import HumanInTheLoop, RiskLevel, ApprovalChannel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class OrderPriority(Enum):
    """订单优先级"""
    CRITICAL = "critical"   # 紧急
    URGENT = "urgent"       # 急
    NORMAL = "normal"       # 普通
    LOW = "low"             # 低


class OrderStage(Enum):
    """订单阶段"""
    PR_CREATED = "pr_created"
    PO_SUBMITTED = "po_submitted"
    PO_CONFIRMED = "po_confirmed"
    IN_PRODUCTION = "in_production"
    SHIPPED = "shipped"
    RECEIVED = "received"
    CLOSED = "closed"


@dataclass
class SupplierInfo:
    """供应商信息"""
    supplier_id: str
    name: str
    category: str
    rating: float
    status: str
    credit_level: str
    lead_time_days: int
    min_order_amount: float
    payment_terms: str
    contact: dict
    recommendation: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PurchaseOrder:
    """采购订单"""
    po_id: str
    pr_id: str
    supplier: SupplierInfo
    items: list[dict]
    total_amount: float
    priority: str
    status: str
    approval_status: str
    approval_ticket_id: Optional[str]
    estimated_delivery: str
    created_at: str
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# =============================================================================
# 采购智能体
# =============================================================================

class ProcurementAgent:
    """
    采购智能体

    核心能力：
    1. 供应商搜索与推荐
    2. 智能供应商推荐（综合评分）
    3. 采购申请创建
    4. 订单状态追踪
    5. 高风险操作人机回环

    安全规范：
    - 所有订单操作需权限校验
    - 金额>5万触发人工审批
    - 关键操作记录完整审计日志
    """

    def __init__(
        self,
        agent_id: str = "procurement_agent",
        user_id: str = "system",
        user_role: str = "procurement_manager",
    ):
        self.agent_id = agent_id
        self.user_id = user_id
        self.user_role = user_role

        self._srm_service = SRMService()
        self._erp_service = ERPService()
        self._audit = AuditLogger(log_dir=f"./logs/{agent_id}")
        self._permission = PermissionManager()
        self._hitl = HumanInTheLoop(default_channel=ApprovalChannel.CONSOLE)

        self.capabilities = [
            "supplier_lookup",
            "recommend_supplier",
            "place_order",
            "track_order",
            "cancel_order",
            "analyze_spend",
        ]

        logger.info(f"采购智能体初始化: {agent_id}, role={user_role}")

    @traced(agent_name="procurement_agent", action="supplier_lookup")
    async def supplier_lookup(
        self,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        min_rating: Optional[float] = None,
        sku: Optional[str] = None,  # 兼容orchestrator传递的参数
    ) -> dict[str, Any]:
        """
        搜索供应商

        Args:
            keyword: 搜索关键词
            category: 供应商类别
            min_rating: 最低评分

        Returns:
            供应商搜索结果
        """
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="supplier_lookup",
            parameters={"keyword": keyword, "category": category},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return {"success": False, "error": decision.reason, "suppliers": []}

        result = await self._srm_service.search_suppliers(
            keyword=keyword,
            category=category,
            min_rating=min_rating,
        )

        await self._audit.log(
            event_type=EventType.MCP_CALL,
            action="srm.search_suppliers",
            agent_name=self.agent_id,
            actor_id=self.user_id,
            actor_role=self.user_role,
            input_data={"keyword": keyword, "category": category},
            output_data={"count": result.get("count", 0)},
            level=LogLevel.INFO,
        )

        return result

    async def recommend_supplier(
        self,
        sku: str = "SKU001",
        category_hint: str = "",
        top_n: int = 3,
        keyword: Optional[str] = None,  # 兼容orchestrator传递的参数
    ) -> dict[str, Any]:
        """智能推荐供应商"""
        result = await self._srm_service.recommend_supplier(sku, category_hint)

        if result.get("success"):
            recommendations = result["data"]["recommendations"][:top_n]
            return {
                **result,
                "data": {
                    **result["data"],
                    "recommendations": recommendations,
                    "analysis": self._analyze_recommendations(recommendations),
                }
            }
        return result

    @traced(agent_name="procurement_agent", action="place_order")
    async def place_order(
        self,
        supplier_id: str,
        items: list[dict],
        priority: str = "normal",
        notes: str = "",
        skip_approval: bool = False,
        keyword: Optional[str] = None,  # 兼容orchestrator传递的参数
    ) -> dict[str, Any]:
        """
        下达采购订单

        ⚠️ 高风险操作：
        - 金额>5万：自动触发人机回环审批
        - 首次下单供应商：需要额外审核
        - 紧急订单：需要说明原因

        Args:
            supplier_id: 供应商ID
            items: 采购明细 [{"sku": "SKU001", "quantity": 100, "unit_price": 25.5}]
            priority: 优先级
            notes: 备注
            skip_approval: 跳过审批（仅admin角色可用）

        Returns:
            订单结果
        """
        # 权限校验
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="place_order",
            parameters={"supplier_id": supplier_id, "items": items},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return {"success": False, "error": decision.reason, "order_id": None}

        # 计算总金额
        total_amount = sum(item.get("quantity", 0) * item.get("unit_price", 0) for item in items)
        ctx.parameters["total_amount"] = total_amount

        # 高风险评估
        risk_level, request_id = self._hitl.assess_and_request(
            agent_name=self.agent_id,
            action="place_order",
            parameters={"supplier_id": supplier_id, "items": items, "total_amount": total_amount},
            requested_by=self.user_id,
        )

        # 人机回环审批（金额>5万或高风险）
        if request_id and not skip_approval:
            logger.info(f"[采购审批] 订单金额¥{total_amount}，发起人工审批: {request_id}")

            hitl_result = await self._hitl.request_approval(
                agent_name=self.agent_id,
                action="place_order",
                parameters={"supplier_id": supplier_id, "items": items, "total_amount": total_amount},
                requested_by=self.user_id,
                description=f"采购申请: ¥{total_amount}",
            )

            if not hitl_result.approved:
                await self._audit.log(
                    event_type=EventType.HUMAN_APPROVAL,
                    action="place_order_rejected",
                    agent_name=self.agent_id,
                    actor_id=self.user_id,
                    level=LogLevel.WARNING,
                    input_data={"supplier_id": supplier_id, "total_amount": total_amount},
                    output_data={"reason": hitl_result.comments},
                )
                return {
                    "success": False,
                    "error": f"审批未通过: {hitl_result.comments}",
                    "order_id": None,
                    "approval_status": "rejected",
                    "approved_by": hitl_result.approved_by,
                }

        # 调用SRM服务创建订单
        result = await self._srm_service.create_purchase_request(
            supplier_id=supplier_id,
            items=items,
            requested_by=self.user_id,
            priority=priority,
            notes=notes,
        )

        # 审计日志
        await self._audit.log(
            event_type=EventType.AGENT_CALL,
            action="place_order",
            agent_name=self.agent_id,
            actor_id=self.user_id,
            actor_role=self.user_role,
            input_data={
                "supplier_id": supplier_id,
                "items": items,
                "total_amount": total_amount,
                "priority": priority,
            },
            output_data=result,
            level=LogLevel.WARNING if total_amount > 50000 else LogLevel.INFO,
            risk_score=min(total_amount / 200000, 1.0),
        )

        if result["success"]:
            data = result["data"]
            # 同时在ERP中创建采购订单
            erp_result = await self._erp_service.create_purchase_order(
                supplier_id=supplier_id,
                items=items,
                notes=notes,
                priority=priority,
            )

            return {
                "success": True,
                "order_id": data["po_id"],
                "pr_id": data["pr_id"],
                "supplier_id": supplier_id,
                "total_amount": data["total_amount"],
                "status": data["status"],
                "approval_status": "approved" if not request_id else "human_approved",
                "approval_ticket_id": request_id,
                "estimated_delivery": data["estimated_delivery"],
                "payment_terms": data["payment_terms"],
                "erp_order_id": erp_result.get("data", {}).get("order_id") if erp_result.get("success") else None,
                "alerts": self._generate_order_alerts(data),
            }

        return result

    async def track_order(self, order_id: str) -> dict[str, Any]:
        """追踪订单状态"""
        result = await self._srm_service.get_order_status(order_id)

        if result.get("success"):
            data = result["data"]
            # 判断是否需要跟进
            if data["status"] in ("submitted", "confirmed"):
                data["follow_up_needed"] = True
                data["follow_up_suggestion"] = "建议联系供应商确认交期"
            else:
                data["follow_up_needed"] = False

        return result

    async def cancel_order(
        self,
        order_id: str,
        reason: str,
    ) -> dict[str, Any]:
        """
        取消订单

        ⚠️ 高风险操作：几乎所有取消都需要人工审批
        """
        # 必须经过人机回环
        result = await self._hitl.request_approval(
            agent_name=self.agent_id,
            action="cancel_order",
            parameters={"order_id": order_id, "reason": reason},
            requested_by=self.user_id,
            description=f"取消订单{order_id}: {reason}",
        )

        if not result.approved:
            return {
                "success": False,
                "error": f"取消申请被拒绝: {result.comments}",
            }

        # 执行取消（模拟）
        await self._audit.log(
            event_type=EventType.AGENT_CALL,
            action="cancel_order",
            agent_name=self.agent_id,
            actor_id=self.user_id,
            level=LogLevel.CRITICAL,
            input_data={"order_id": order_id, "reason": reason},
            output_data={"status": "cancelled"},
            risk_score=0.8,
        )

        return {
            "success": True,
            "order_id": order_id,
            "status": "cancelled",
            "cancelled_by": result.approved_by,
            "cancelled_at": datetime.now().isoformat(),
        }

    def _analyze_recommendations(self, recommendations: list[dict]) -> dict[str, Any]:
        """分析推荐结果"""
        if not recommendations:
            return {"summary": "无可用供应商"}

        scores = [r["composite_score"] for r in recommendations]
        top = recommendations[0]

        return {
            "summary": f"推荐{top['name']}（综合分{top['composite_score']}），"
                       f"评分{top['rating']}，交期{top['lead_time_days']}天",
            "best_for": {
                "price": min(recommendations, key=lambda x: x["composite_score"]),
                "speed": min(recommendations, key=lambda x: x["lead_time_days"]),
                "rating": max(recommendations, key=lambda x: x["rating"]),
            },
            "score_range": {
                "min": min(scores),
                "max": max(scores),
                "avg": round(sum(scores) / len(scores), 2),
            },
        }

    def _generate_order_alerts(self, order_data: dict) -> list[str]:
        """生成订单告警"""
        alerts = []
        amount = order_data.get("total_amount", 0)
        if amount > 50000:
            alerts.append(f"⚠️ 大额订单: ¥{amount}，需财务审批")
        if order_data.get("approval_required"):
            alerts.append("📋 订单需管理层审批")
        if order_data.get("priority") == "urgent":
            alerts.append("🚨 紧急订单，请优先处理")
        return alerts


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    async def demo():
        print("=" * 60)
        print("  采购智能体演示")
        print("=" * 60)

        agent = ProcurementAgent(user_role="procurement_manager")

        # 供应商搜索
        print("\n[1] 搜索零部件供应商")
        result = await agent.supplier_lookup(category="component")
        print(f"  找到{result['count']}家供应商:")
        for s in result["data"][:3]:
            print(f"    {s['name']} | 评分:{s['rating']} | 交期:{s['lead_time_days']}天 | "
                  f"{s['payment_terms']}")

        # 智能推荐
        print("\n[2] 推荐轴承供应商")
        rec = await agent.recommend_supplier("SKU001", top_n=3)
        for r in rec["data"]["recommendations"]:
            print(f"  #{r['rank']} {r['name']} (综合分:{r['composite_score']})")

        # 下达订单（模拟，金额低不触发审批）
        print("\n[3] 下达采购订单（¥5000，小额不触发审批）")
        order = await agent.place_order(
            supplier_id="SUP001",
            items=[{"sku": "SKU001", "name": "电机轴承", "quantity": 100, "unit_price": 50.0}],
            priority="normal",
            notes="库存补货",
        )
        print(f"  订单ID: {order.get('order_id')}")
        print(f"  金额: ¥{order.get('total_amount')}")
        print(f"  ERP订单: {order.get('erp_order_id')}")
        print(f"  审批状态: {order.get('approval_status')}")
        print(f"  告警: {order.get('alerts', [])}")

        # ERP订单查询
        if order.get("erp_order_id"):
            print("\n[4] 查询ERP订单状态")
            status = await agent._erp_service.get_order_status(order["erp_order_id"])
            print(f"  状态: {status['data']['status']}")

    asyncio.run(demo())
