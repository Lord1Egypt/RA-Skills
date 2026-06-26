"""
SRM (Supplier Relationship Management) MCP Server
供应商关系管理系统MCP协议封装

提供供应商信息查询、采购下单、合同管理等功能
"""

from __future__ import annotations

import asyncio
import uuid
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class SupplierCategory(Enum):
    """供应商类别"""
    RAW_MATERIAL = "raw_material"     # 原材料
    COMPONENT = "component"           # 零部件
    SERVICE = "service"               # 服务
    EQUIPMENT = "equipment"           # 设备


class SupplierStatus(Enum):
    """供应商状态"""
    ACTIVE = "active"
    PENDING = "pending"
    SUSPENDED = "suspended"
    BLACKLISTED = "blacklisted"


class OrderStatus(Enum):
    """采购单状态"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    CONFIRMED = "confirmed"
    IN_PRODUCTION = "in_production"
    SHIPPED = "shipped"
    RECEIVED = "received"
    CANCELLED = "cancelled"


@dataclass
class Supplier:
    """供应商"""
    supplier_id: str
    name: str
    category: SupplierCategory
    contact_person: str
    phone: str
    email: str
    address: str
    rating: float = 0.0
    status: SupplierStatus = SupplierStatus.ACTIVE
    credit_level: str = "A"
    lead_time_days: int = 7
    min_order_amount: float = 1000.0
    payment_terms: str = "月结30天"
    contracts: list = field(default_factory=list)


@dataclass
class PurchaseRequest:
    """采购申请"""
    pr_id: str
    supplier_id: str
    items: list[dict]
    total_amount: float
    requested_by: str
    priority: str = "normal"
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Contract:
    """采购合同"""
    contract_id: str
    supplier_id: str
    contract_no: str
    content: str
    amount: float
    start_date: str
    end_date: str
    status: str = "active"


# =============================================================================
# SRM服务层
# =============================================================================

class SRMService:
    """
    供应商关系管理服务

    核心功能：
    - 供应商档案管理
    - 供应商搜索与推荐
    - 采购申请与订单下达
    - 合同管理
    """

    def __init__(self):
        self._suppliers = self._init_suppliers()
        self._orders: dict[str, dict] = {}
        self._contracts: dict[str, Contract] = {}

    def _init_suppliers(self) -> dict[str, Supplier]:
        """初始化供应商数据"""
        return {
            "SUP001": Supplier(
                supplier_id="SUP001",
                name="华东轴承有限公司",
                category=SupplierCategory.COMPONENT,
                contact_person="李经理",
                phone="021-88880001",
                email="contact@huadong-bearing.com",
                address="上海市嘉定区工业园区",
                rating=4.8,
                status=SupplierStatus.ACTIVE,
                credit_level="A",
                lead_time_days=3,
                min_order_amount=5000,
                payment_terms="月结30天",
            ),
            "SUP002": Supplier(
                supplier_id="SUP002",
                name="宝钢材料供应链",
                category=SupplierCategory.RAW_MATERIAL,
                contact_person="王经理",
                phone="021-88880002",
                email="order@baosteel-supply.com",
                address="上海市宝山区钢铁园区",
                rating=4.6,
                status=SupplierStatus.ACTIVE,
                credit_level="A",
                lead_time_days=5,
                min_order_amount=10000,
                payment_terms="月结45天",
            ),
            "SUP003": Supplier(
                supplier_id="SUP003",
                name="壳牌工业油品有限公司",
                category=SupplierCategory.RAW_MATERIAL,
                contact_person="张经理",
                phone="020-88880003",
                email="sales@shell-industrial.cn",
                address="广州市黄埔区化工园",
                rating=4.9,
                status=SupplierStatus.ACTIVE,
                credit_level="AA",
                lead_time_days=2,
                min_order_amount=3000,
                payment_terms="预付30%+月结70%",
            ),
            "SUP004": Supplier(
                supplier_id="SUP004",
                name="西门子工业自动化",
                category=SupplierCategory.EQUIPMENT,
                contact_person="赵经理",
                phone="010-88880004",
                email="industry@siemens.cn",
                address="北京市朝阳区望京科技园",
                rating=4.7,
                status=SupplierStatus.ACTIVE,
                credit_level="A",
                lead_time_days=7,
                min_order_amount=20000,
                payment_terms="月结60天",
            ),
            "SUP005": Supplier(
                supplier_id="SUP005",
                name="南方传动设备厂",
                category=SupplierCategory.COMPONENT,
                contact_person="陈经理",
                phone="0755-88880005",
                email="sales@nanfang-drive.com",
                address="深圳市龙华区工业园",
                rating=4.3,
                status=SupplierStatus.PENDING,
                credit_level="B",
                lead_time_days=5,
                min_order_amount=8000,
                payment_terms="月结30天",
            ),
        }

    # -------------------------------------------------------------------------
    # 核心业务方法
    # -------------------------------------------------------------------------

    async def search_suppliers(
        self,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        min_rating: Optional[float] = None,
        status_filter: Optional[str] = None
    ) -> dict[str, Any]:
        """
        搜索供应商

        Args:
            keyword: 搜索关键词（名称、类别）
            category: 供应商类别过滤
            min_rating: 最低评分
            status_filter: 状态过滤

        Returns:
            供应商列表
        """
        logger.info(f"搜索供应商: keyword={keyword}, category={category}")

        await asyncio.sleep(0.08)

        results = []
        for sup in self._suppliers.values():
            if status_filter and sup.status.value != status_filter:
                continue
            if category and sup.category.value != category:
                continue
            if min_rating and sup.rating < min_rating:
                continue
            if keyword:
                kw = keyword.lower()
                if kw not in sup.name.lower() and kw not in sup.category.value:
                    continue

            results.append({
                "supplier_id": sup.supplier_id,
                "name": sup.name,
                "category": sup.category.value,
                "rating": sup.rating,
                "status": sup.status.value,
                "credit_level": sup.credit_level,
                "lead_time_days": sup.lead_time_days,
                "min_order_amount": sup.min_order_amount,
                "payment_terms": sup.payment_terms,
                "contact_person": sup.contact_person,
                "phone": sup.phone,
            })

        # 按评分排序
        results.sort(key=lambda x: x["rating"], reverse=True)

        return {
            "success": True,
            "count": len(results),
            "data": results,
            "summary": {
                "total": len(results),
                "active": sum(1 for r in results if r["status"] == "active"),
                "avg_rating": round(sum(r["rating"] for r in results) / len(results), 2) if results else 0,
            }
        }

    async def get_supplier_detail(self, supplier_id: str) -> dict[str, Any]:
        """获取供应商详情"""
        await asyncio.sleep(0.05)
        sup = self._suppliers.get(supplier_id)
        if not sup:
            return {"success": False, "error": f"供应商不存在: {supplier_id}"}

        return {
            "success": True,
            "data": {
                "supplier_id": sup.supplier_id,
                "name": sup.name,
                "category": sup.category.value,
                "status": sup.status.value,
                "rating": sup.rating,
                "credit_level": sup.credit_level,
                "lead_time_days": sup.lead_time_days,
                "min_order_amount": sup.min_order_amount,
                "payment_terms": sup.payment_terms,
                "contact": {
                    "person": sup.contact_person,
                    "phone": sup.phone,
                    "email": sup.email,
                    "address": sup.address,
                },
                "recommendation": self._generate_recommendation(sup),
            }
        }

    def _generate_recommendation(self, sup: Supplier) -> str:
        """生成供应商评价"""
        pros = []
        cons = []
        if sup.rating >= 4.7:
            pros.append("优质供应商，评分高")
        if sup.credit_level in ["AA", "A"]:
            pros.append("信用等级良好")
        if sup.lead_time_days <= 3:
            pros.append("交货周期短")
        if sup.min_order_amount > 10000:
            cons.append(f"最小起订量较高({sup.min_order_amount}元)")
        if sup.status == SupplierStatus.PENDING:
            cons.append("资质待审核")

        return "; ".join(pros + [f"⚠️{c}" for c in cons]) if pros or cons else "常规供应商"

    async def create_purchase_request(
        self,
        supplier_id: str,
        items: list[dict],
        requested_by: str = "system",
        priority: str = "normal",
        notes: str = ""
    ) -> dict[str, Any]:
        """
        创建采购申请

        Args:
            supplier_id: 供应商ID
            items: 采购明细 [{"sku": "SKU001", "name": "电机轴承", "quantity": 500, "unit_price": 25.5}]
            requested_by: 申请人
            priority: 优先级 normal/urgent
            notes: 备注

        Returns:
            采购申请结果
        """
        logger.info(f"创建采购申请: supplier={supplier_id}, items={len(items)}, priority={priority}")

        await asyncio.sleep(0.12)

        sup = self._suppliers.get(supplier_id)
        if not sup:
            return {"success": False, "error": f"供应商不存在: {supplier_id}"}

        if sup.status != SupplierStatus.ACTIVE:
            return {"success": False, "error": f"供应商状态异常: {sup.status.value}"}

        total_amount = sum(item.get("quantity", 0) * item.get("unit_price", 0) for item in items)

        if total_amount < sup.min_order_amount:
            return {
                "success": False,
                "error": f"订单金额({total_amount})未达最小起订量({sup.min_order_amount})"
            }

        pr_id = f"PR{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        pr = PurchaseRequest(
            pr_id=pr_id,
            supplier_id=supplier_id,
            items=items,
            total_amount=total_amount,
            requested_by=requested_by,
            priority=priority,
        )

        order_id = f"PO{uuid.uuid4().hex[:8].upper()}"
        self._orders[order_id] = {
            "po_id": order_id,
            "pr_id": pr_id,
            "supplier_id": supplier_id,
            "supplier_name": sup.name,
            "items": items,
            "total_amount": round(total_amount, 2),
            "status": OrderStatus.SUBMITTED.value,
            "created_at": pr.created_at,
            "priority": priority,
            "notes": notes,
        }

        return {
            "success": True,
            "data": {
                "pr_id": pr_id,
                "po_id": order_id,
                "supplier_id": supplier_id,
                "supplier_name": sup.name,
                "items": items,
                "total_amount": round(total_amount, 2),
                "status": "submitted",
                "estimated_delivery": f"{sup.lead_time_days}个工作日",
                "payment_terms": sup.payment_terms,
                "approval_required": total_amount > 50000,
                "priority": priority,
            }
        }

    async def get_order_status(self, order_id: str) -> dict[str, Any]:
        """查询订单状态"""
        await asyncio.sleep(0.05)
        order = self._orders.get(order_id)
        if not order:
            return {"success": False, "error": f"订单不存在: {order_id}"}

        return {
            "success": True,
            "data": {
                **order,
                "timeline": [
                    {"status": "submitted", "time": order["created_at"], "actor": "system"},
                    {"status": "confirmed", "time": order["created_at"], "actor": order["supplier_name"]},
                ]
            }
        }

    async def recommend_supplier(self, sku: str, category_hint: str = "") -> dict[str, Any]:
        """智能推荐供应商"""
        await asyncio.sleep(0.1)

        # 查找与SKU类别匹配的供应商
        candidates = [
            s for s in self._suppliers.values()
            if s.status == SupplierStatus.ACTIVE
        ]

        if not candidates:
            return {"success": False, "error": "无可用供应商"}

        # 综合评分
        scored = []
        for s in candidates:
            score = s.rating * 0.4 + (5 - s.lead_time_days) * 0.3
            if s.credit_level == "AA":
                score += 0.5
            elif s.credit_level == "A":
                score += 0.3
            scored.append((s, round(score, 3)))

        scored.sort(key=lambda x: x[1], reverse=True)
        top3 = scored[:3]

        return {
            "success": True,
            "data": {
                "sku": sku,
                "recommendations": [
                    {
                        "rank": i + 1,
                        "supplier_id": s.supplier_id,
                        "name": s.name,
                        "composite_score": score,
                        "rating": s.rating,
                        "lead_time_days": s.lead_time_days,
                        "payment_terms": s.payment_terms,
                        "min_order_amount": s.min_order_amount,
                    }
                    for i, (s, score) in enumerate(top3)
                ]
            }
        }


# =============================================================================
# MCP协议处理器
# =============================================================================

class SRMProtocolHandler:
    """SRM MCP协议处理器"""

    def __init__(self, service: SRMService):
        self.service = service
        self._tools = {
            "srm.search_suppliers": service.search_suppliers,
            "srm.supplier_detail": service.get_supplier_detail,
            "srm.create_purchase_request": service.create_purchase_request,
            "srm.get_order_status": service.get_order_status,
            "srm.recommend_supplier": service.recommend_supplier,
        }

    async def list_tools(self) -> list[dict]:
        return [
            {"name": name, "description": func.__doc__.strip().split("\n")[0] if func.__doc__ else ""}
            for name, func in self._tools.items()
        ]

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        if tool_name not in self._tools:
            return {"error": f"未知工具: {tool_name}"}
        kwargs = {k: v for k, v in arguments.items() if k != "name"}
        return await self._tools[tool_name](**kwargs)


if __name__ == "__main__":
    async def test():
        service = SRMService()
        handler = SRMProtocolHandler(service)

        print("\n[搜索轴承类供应商]")
        r = await service.search_suppliers(category="component")
        for s in r["data"]:
            print(f"  {s['name']} | 评分:{s['rating']} | 交期:{s['lead_time_days']}天")

        print("\n[推荐SKU003的供应商]")
        r = await service.recommend_supplier("SKU003")
        for rec in r["data"]["recommendations"]:
            print(f"  #{rec['rank']} {rec['name']} (综合分:{rec['composite_score']})")

        print("\n[创建采购申请]")
        r = await service.create_purchase_request(
            supplier_id="SUP001",
            items=[{"sku": "SKU001", "name": "电机轴承", "quantity": 500, "unit_price": 25.5}],
            priority="normal"
        )
        print(f"  订单ID: {r['data']['po_id']}, 金额: {r['data']['total_amount']}, 审批: {r['data']['approval_required']}")

    asyncio.run(test())
