"""
Inventory Agent - 库存智能体

专注领域：库存查询、安全水位计算、ERP接口调用、补货建议

角色定位：专业智能体（Specialist），不直接面向用户，
只接收指挥智能体的任务分派，返回结构化结果
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from mcp_servers.erp_server import ERPService, StockStatus
from mcp_servers.wms_server import WMSService
from safety.audit_logger import AuditLogger, EventType, LogLevel, traced
from safety.permission_manager import PermissionManager, PermissionContext, PermissionResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class InventoryAlert(Enum):
    """库存告警类型"""
    STOCKOUT = "stockout"               # 缺货
    LOW_STOCK = "low_stock"             # 低库存
    OVERSTOCK = "overstock"            # 库存过剩
    EXPIRY_WARNING = "expiry_warning"  # 临期警告
    QUALITY_HOLD = "quality_hold"       # 质量待检


@dataclass
class StockQueryResult:
    """库存查询结果"""
    success: bool
    sku: str
    name: str
    quantity: int
    unit: str
    warehouse: str
    safety_stock: int
    status: str
    stock_ratio: float
    alerts: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SafetyStockResult:
    """安全库存计算结果"""
    success: bool
    sku: str
    current_stock: int
    calculated_safety_stock: int
    reorder_point: int
    recommended_reorder_qty: int
    status: str
    formula: str
    gap: int = 0  # 当前库存与安全库存的差距

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReplenishmentSuggestion:
    """补货建议"""
    sku: str
    name: str
    current_stock: int
    safety_stock: int
    suggested_qty: int
    urgency: str  # critical/high/medium/low
    reason: str
    target_warehouse: str
    estimated_cost: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


# =============================================================================
# 库存智能体
# =============================================================================

class InventoryAgent:
    """
    库存智能体

    核心能力：
    1. 库存查询：支持SKU/仓库/状态多维查询
    2. 安全水位计算：基于统计学方法计算最优安全库存
    3. 补货建议：综合分析后给出补货建议
    4. 告警生成：自动识别库存异常并告警
    5. ERP/WMS集成：通过MCP协议调用后端系统

    调用规范：
    - 接收：指挥智能体分派的任务（Task对象）
    - 输出：结构化的SpecialistResult
    """

    def __init__(
        self,
        agent_id: str = "inventory_agent",
        user_id: str = "system",
        user_role: str = "warehouse_operator",
    ):
        self.agent_id = agent_id
        self.user_id = user_id
        self.user_role = user_role

        # 初始化MCP服务
        self._erp_service = ERPService()
        self._wms_service = WMSService()

        # 初始化安全模块
        self._audit = AuditLogger(log_dir=f"./logs/{agent_id}")
        self._permission = PermissionManager()

        # 能力清单
        self.capabilities = [
            "query_stock",
            "calculate_safety_stock",
            "trigger_replenishment",
            "check_alerts",
            "get_warehouse_info",
        ]

        logger.info(f"库存智能体初始化: {agent_id}, role={user_role}")

    # -------------------------------------------------------------------------
    # 核心能力
    # -------------------------------------------------------------------------

    @traced(agent_name="inventory_agent", action="query_stock")
    async def query_stock(
        self,
        sku: Optional[str] = None,
        warehouse: Optional[str] = None,
        check_alerts: bool = True,
    ) -> StockQueryResult:
        """
        查询库存

        Args:
            sku: SKU编码，None表示查询全部
            warehouse: 仓库名称过滤
            check_alerts: 是否检查告警

        Returns:
            库存查询结果
        """
        # 权限校验
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="query_stock",
            parameters={"sku": sku, "warehouse": warehouse},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return StockQueryResult(
                success=False,
                sku=sku or "all",
                name="",
                quantity=0,
                unit="",
                warehouse=warehouse or "all",
                safety_stock=0,
                status="permission_denied",
                stock_ratio=0.0,
                alerts=[decision.reason],
            )

        # 调用ERP服务
        result = await self._erp_service.query_stock(sku=sku, warehouse=warehouse)

        if not result["success"]:
            return StockQueryResult(
                success=False,
                sku=sku or "all",
                name="",
                quantity=0,
                unit="",
                warehouse=warehouse or "all",
                safety_stock=0,
                status="error",
                stock_ratio=0.0,
                alerts=[result.get("error", "未知错误")],
            )

        # 审计日志
        await self._audit.log(
            event_type=EventType.MCP_CALL,
            action="erp.query_stock",
            agent_name=self.agent_id,
            actor_id=self.user_id,
            actor_role=self.user_role,
            input_data={"sku": sku, "warehouse": warehouse},
            output_data=result,
            level=LogLevel.INFO,
            metadata={"result_count": result.get("count", 0)},
        )

        # 取第一条（单SKU查询）
        data = result.get("data", [])
        if sku and data:
            item = data[0]
            alerts = []
            recommendations = []

            if check_alerts:
                alerts, recommendations = self._generate_alerts(item)

            return StockQueryResult(
                success=True,
                sku=item["sku"],
                name=item["name"],
                quantity=item["quantity"],
                unit=item["unit"],
                warehouse=item["warehouse"],
                safety_stock=item["safety_stock"],
                status=item["status"],
                stock_ratio=item.get("stock_ratio", 0.0),
                alerts=alerts,
                recommendations=recommendations,
                metadata={"last_updated": item.get("last_updated")},
            )

        # 全量查询结果
        return StockQueryResult(
            success=True,
            sku="ALL",
            name=f"共{result['count']}个SKU",
            quantity=sum(i["quantity"] for i in data),
            unit="件",
            warehouse=warehouse or "全部",
            safety_stock=sum(i["safety_stock"] for i in data),
            status="summary",
            stock_ratio=0.0,
            alerts=[],
            recommendations=[],
            metadata=result.get("summary", {}),
        )

    @traced(agent_name="inventory_agent", action="calculate_safety_stock")
    async def calculate_safety_stock(
        self,
        sku: str,
        lead_time_days: int = 7,
        service_level: float = 0.95,
    ) -> SafetyStockResult:
        """
        计算安全库存水位

        使用统计学安全库存公式：
        Safety Stock = Z × σ × √(LT)

        Args:
            sku: SKU编码
            lead_time_days: 采购提前期（天）
            service_level: 目标服务水平（默认95%）

        Returns:
            安全库存计算结果
        """
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="calculate_safety_stock",
            parameters={"sku": sku, "lead_time_days": lead_time_days},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return SafetyStockResult(
                success=False,
                sku=sku,
                current_stock=0,
                calculated_safety_stock=0,
                reorder_point=0,
                recommended_reorder_qty=0,
                status="permission_denied",
                formula="",
            )

        result = await self._erp_service.calculate_safety_stock(
            sku=sku,
            lead_time_days=lead_time_days,
            service_level=service_level,
        )

        if not result["success"]:
            return SafetyStockResult(
                success=False,
                sku=sku,
                current_stock=0,
                calculated_safety_stock=0,
                reorder_point=0,
                recommended_reorder_qty=0,
                status="error",
                formula="",
            )

        data = result["data"]
        return SafetyStockResult(
            success=True,
            sku=data["sku"],
            current_stock=data["current_stock"],
            calculated_safety_stock=data["calculated_safety_stock"],
            reorder_point=data["reorder_point"],
            recommended_reorder_qty=data["recommended_reorder_qty"],
            status=data["status"],
            formula=data["formula"],
            gap=data["calculated_safety_stock"] - data["current_stock"],
        )

    @traced(agent_name="inventory_agent", action="trigger_replenishment")
    async def trigger_replenishment(
        self,
        sku: str,
        suggested_qty: Optional[int] = None,
        urgency: str = "normal",
    ) -> dict[str, Any]:
        """
        触发补货流程

        当库存低于安全水位时，触发自动补货建议，
        供指挥智能体判断是否下达采购订单

        Args:
            sku: SKU编码
            suggested_qty: 建议补货数量（未提供则自动计算）
            urgency: 紧急程度 normal/urgent/critical

        Returns:
            补货建议
        """
        # 先查询当前库存
        stock = await self.query_stock(sku=sku, check_alerts=False)
        if not stock.success:
            return {"success": False, "error": f"查询失败: {sku}"}

        # 计算安全库存
        safety_result = await self.calculate_safety_stock(sku=sku)

        if not suggested_qty:
            suggested_qty = safety_result.recommended_reorder_qty

        # 紧急程度判断
        if stock.quantity == 0:
            urgency = "critical"
        elif stock.quantity <= stock.safety_stock * 0.5:
            urgency = "high"

        suggestion = ReplenishmentSuggestion(
            sku=sku,
            name=stock.name,
            current_stock=stock.quantity,
            safety_stock=safety_result.calculated_safety_stock,
            suggested_qty=max(suggested_qty, 1),
            urgency=urgency,
            reason=self._build_replenishment_reason(stock, safety_result),
            target_warehouse=stock.warehouse,
            estimated_cost=suggested_qty * 25.5,  # 模拟单价
        )

        await self._audit.log(
            event_type=EventType.AGENT_CALL,
            action="trigger_replenishment",
            agent_name=self.agent_id,
            actor_id=self.user_id,
            level=LogLevel.WARNING if urgency in ("high", "critical") else LogLevel.INFO,
            input_data={"sku": sku, "suggested_qty": suggested_qty, "urgency": urgency},
            output_data=suggestion.to_dict(),
            risk_score=0.3 if urgency == "high" else 0.1,
        )

        return {
            "success": True,
            "replenishment": suggestion.to_dict(),
            "requires_approval": urgency in ("high", "critical"),
        }

    async def check_alerts(self) -> list[dict[str, Any]]:
        """检查全量库存告警"""
        result = await self._erp_service.query_stock()

        all_alerts = []
        for item in result.get("data", []):
            alerts, _ = self._generate_alerts(item)
            if alerts:
                all_alerts.append({
                    "sku": item["sku"],
                    "name": item["name"],
                    "warehouse": item["warehouse"],
                    "status": item["status"],
                    "quantity": item["quantity"],
                    "safety_stock": item["safety_stock"],
                    "alerts": alerts,
                })

        # 按紧急程度排序
        priority = {"critical": 0, "low": 1, "normal": 2, "overstocked": 3}
        all_alerts.sort(key=lambda x: priority.get(x["status"], 99))

        return all_alerts

    async def get_warehouse_info(self, warehouse_id: str) -> dict[str, Any]:
        """获取仓库信息"""
        return await self._wms_service.get_warehouse_summary(warehouse_id=warehouse_id)

    # -------------------------------------------------------------------------
    # 辅助方法
    # -------------------------------------------------------------------------

    def _generate_alerts(
        self,
        item: dict,
    ) -> tuple[list[str], list[str]]:
        """生成库存告警和建议"""
        alerts = []
        recommendations = []

        status = item["status"]
        qty = item["quantity"]
        safety = item["safety_stock"]

        if qty == 0:
            alerts.append(f"⚠️ 紧急缺货: {item['name']}")
            recommendations.append(f"立即触发紧急补货流程，目标数量: {safety * 2}")
        elif status == "low":
            ratio = qty / safety if safety else 0
            alerts.append(f"⚡ 低库存预警: 当前{safety - qty}件低于安全水位")
            recommendations.append(f"建议补货至{safety * 2}件（当前{safety * 2 - qty}件）")
        elif status == "overstocked":
            alerts.append(f"📦 库存过剩: {item['name']}超过最大库存")
            recommendations.append("建议暂停进货，考虑促销或调拨")
        elif status == "critical":
            alerts.append(f"🚨 库存严重不足: {item['name']}")
            recommendations.append("需紧急采购，请联系采购部门")

        return alerts, recommendations

    def _build_replenishment_reason(
        self,
        stock: StockQueryResult,
        safety: SafetyStockResult,
    ) -> str:
        """生成补货原因"""
        gap = safety.calculated_safety_stock - stock.quantity
        if gap <= 0:
            return f"库存过剩{gap}件，无需补货"
        return (
            f"当前库存({stock.quantity})低于安全水位({safety.calculated_safety_stock})，"
            f"缺{gap}件，建议补货{safety.recommended_reorder_qty}件"
        )


# =============================================================================
# 便捷调用接口
# =============================================================================

async def quick_stock_check(sku: str, role: str = "warehouse_operator") -> dict:
    """快速库存检查（单行调用）"""
    agent = InventoryAgent(user_role=role)
    result = await agent.query_stock(sku=sku)
    return result.to_dict()


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    async def demo():
        print("=" * 60)
        print("  库存智能体演示")
        print("=" * 60)

        agent = InventoryAgent(user_role="warehouse_operator")

        # 演示1: 单SKU库存查询
        print("\n[1] 查询SKU001库存")
        result = await agent.query_stock(sku="SKU001")
        print(f"  名称: {result.name}")
        print(f"  库存: {result.quantity}{result.unit}")
        print(f"  状态: {result.status}")
        print(f"  告警: {result.alerts}")
        print(f"  建议: {result.recommendations}")

        # 演示2: 安全库存计算
        print("\n[2] 计算安全库存")
        safety = await agent.calculate_safety_stock(sku="SKU003")
        print(f"  SKU003 安全水位: {safety.calculated_safety_stock}")
        print(f"  建议补货点: {safety.reorder_point}")
        print(f"  推荐补货量: {safety.recommended_reorder_qty}")
        print(f"  公式: {safety.formula}")

        # 演示3: 触发补货
        print("\n[3] 触发补货流程")
        rep = await agent.trigger_replenishment(sku="SKU003")
        print(f"  建议补货量: {rep['replenishment']['suggested_qty']}件")
        print(f"  紧急程度: {rep['replenishment']['urgency']}")
        print(f"  需要审批: {rep['requires_approval']}")

        # 演示4: 全量告警检查
        print("\n[4] 库存告警检查")
        alerts = await agent.check_alerts()
        print(f"  告警数量: {len(alerts)}")
        for a in alerts[:3]:
            print(f"  [{a['status']}] {a['name']}: {a['alerts']}")

        # 演示5: 权限不足场景
        print("\n[5] 权限不足场景（viewer角色）")
        viewer_agent = InventoryAgent(user_role="viewer")
        result = await viewer_agent.query_stock(sku="SKU001")
        print(f"  结果: {result.status}")
        print(f"  告警: {result.alerts}")

    asyncio.run(demo())
