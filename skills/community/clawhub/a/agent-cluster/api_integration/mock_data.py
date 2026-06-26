"""
Mock Data Generator - 模拟数据生成器

为开发/演示模式提供真实的模拟数据
支持多种场景配置，便于测试和演示
"""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Optional

from api_adapter import APIResponse, ERPType


# =============================================================================
# 模拟库存数据
# =============================================================================

MOCK_INVENTORY = {
    "SKU001": {
        "sku": "SKU001", "name": "工业级传感器-A1", "quantity": 450,
        "unit": "件", "warehouse": "华东仓", "safety_stock": 200,
        "max_stock": 1000, "status": "normal",
        "location": "A-01-03", "last_updated": datetime.now().isoformat(),
    },
    "SKU002": {
        "sku": "SKU002", "name": "精密轴承-B2", "quantity": 80,
        "unit": "件", "warehouse": "华东仓", "safety_stock": 150,
        "max_stock": 800, "status": "low",
        "location": "B-02-05", "last_updated": datetime.now().isoformat(),
    },
    "SKU003": {
        "sku": "SKU003", "name": "液压泵-C3", "quantity": 1200,
        "unit": "件", "warehouse": "华南仓", "safety_stock": 300,
        "max_stock": 2000, "status": "normal",
        "location": "C-03-01", "last_updated": datetime.now().isoformat(),
    },
    "SKU004": {
        "sku": "SKU004", "name": "控制器-D4", "quantity": 0,
        "unit": "件", "warehouse": "华北仓", "safety_stock": 50,
        "max_stock": 300, "status": "critical",
        "location": "D-01-02", "last_updated": datetime.now().isoformat(),
    },
    "SKU005": {
        "sku": "SKU005", "name": "电机-E5", "quantity": 3200,
        "unit": "件", "warehouse": "华东仓", "safety_stock": 500,
        "max_stock": 5000, "status": "overstocked",
        "location": "E-04-08", "last_updated": datetime.now().isoformat(),
    },
}


# =============================================================================
# 模拟供应商数据
# =============================================================================

MOCK_SUPPLIERS = {
    "SUP001": {
        "supplier_id": "SUP001", "name": "华通传感科技有限公司",
        "contact": "张经理", "phone": "021-12345678",
        "rating": 4.8, "delivery_days": 5, "min_order": 100,
        "products": ["SKU001"], "region": "华东",
    },
    "SUP002": {
        "supplier_id": "SUP002", "name": "精工轴承制造厂",
        "contact": "李总", "phone": "0755-87654321",
        "rating": 4.5, "delivery_days": 7, "min_order": 200,
        "products": ["SKU002"], "region": "华南",
    },
    "SUP003": {
        "supplier_id": "SUP003", "name": "瑞控液压设备有限公司",
        "contact": "王工", "phone": "010-23456789",
        "rating": 4.9, "delivery_days": 10, "min_order": 50,
        "products": ["SKU003", "SKU004"], "region": "华北",
    },
}


# =============================================================================
# 模拟采购订单数据
# =============================================================================

MOCK_ORDERS = [
    {
        "order_id": "PO20260401001", "supplier_id": "SUP001",
        "supplier_name": "华通传感科技有限公司",
        "items": [{"sku": "SKU001", "quantity": 500, "unit_price": 120.0}],
        "total_amount": 60000.0, "status": "delivered",
        "created_at": (datetime.now() - timedelta(days=15)).isoformat(),
        "expected_delivery": (datetime.now() - timedelta(days=10)).isoformat(),
    },
    {
        "order_id": "PO20260412001", "supplier_id": "SUP002",
        "supplier_name": "精工轴承制造厂",
        "items": [{"sku": "SKU002", "quantity": 300, "unit_price": 45.0}],
        "total_amount": 13500.0, "status": "shipped",
        "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
        "expected_delivery": (datetime.now() + timedelta(days=5)).isoformat(),
    },
    {
        "order_id": "PO20260413001", "supplier_id": "SUP003",
        "supplier_name": "瑞控液压设备有限公司",
        "items": [{"sku": "SKU004", "quantity": 100, "unit_price": 280.0}],
        "total_amount": 28000.0, "status": "pending",
        "created_at": datetime.now().isoformat(),
        "expected_delivery": (datetime.now() + timedelta(days=10)).isoformat(),
    },
]


# =============================================================================
# 模拟物流数据
# =============================================================================

MOCK_SHIPMENTS = {
    "EXP20260412001": {
        "tracking_no": "EXP20260412001",
        "carrier": "顺丰速运", "status": "in_transit",
        "origin": "深圳市", "destination": "上海市",
        "estimated_delivery": (datetime.now() + timedelta(days=2)).isoformat(),
        "current_location": "杭州中转站",
        "events": [
            {"time": (datetime.now() - timedelta(days=1)).isoformat(), "location": "深圳发出", "status": "已发货"},
            {"time": (datetime.now() - timedelta(hours=12)).isoformat(), "location": "杭州中转", "status": "运输中"},
        ],
    },
    "EXP20260411001": {
        "tracking_no": "EXP20260411001",
        "carrier": "中通快递", "status": "delivered",
        "origin": "广州市", "destination": "北京市",
        "actual_delivery": (datetime.now() - timedelta(days=1)).isoformat(),
        "current_location": "北京市（已签收）",
        "events": [
            {"time": (datetime.now() - timedelta(days=3)).isoformat(), "location": "广州发出", "status": "已发货"},
            {"time": (datetime.now() - timedelta(days=2)).isoformat(), "location": "武汉中转", "status": "运输中"},
            {"time": (datetime.now() - timedelta(days=1)).isoformat(), "location": "北京签收", "status": "已签收"},
        ],
    },
}


# =============================================================================
# 模拟财务数据
# =============================================================================

MOCK_FINANCE = {
    "budget_summary": {
        "total_budget": 5000000.0, "allocated": 3250000.0,
        "used": 2180000.0, "remaining": 2820000.0,
        "month": datetime.now().strftime("%Y-%m"),
    },
    "recent_payments": [
        {"payment_id": "PAY20260401001", "order_id": "PO20260401001",
         "amount": 60000.0, "status": "paid", "paid_at": (datetime.now() - timedelta(days=14)).isoformat()},
        {"payment_id": "PAY20260410001", "order_id": "PO20260410001",
         "amount": 28000.0, "status": "paid", "paid_at": (datetime.now() - timedelta(days=4)).isoformat()},
        {"payment_id": "PAY20260412001", "order_id": "PO20260412001",
         "amount": 13500.0, "status": "pending", "pending_since": (datetime.now() - timedelta(days=2)).isoformat()},
    ],
}


# =============================================================================
# 演示数据标识常量
# =============================================================================

DEMO_PREFIX = "[⚠️ 演示数据]"
DEMO_DATA_SOURCE = "模拟数据（开发/演示模式），不可用于真实业务决策"
DEMO_DISCLAIMER = "⚠️ 演示数据仅供参考，请勿用于实际业务决策"


# =============================================================================
# 模拟数据生成器
# =============================================================================

class MockDataGenerator:
    """
    模拟数据生成器

    在开发/演示模式下返回真实感的模拟数据
    支持随机波动，让演示更自然
    响应数据均附带演示数据标识，不可用于真实决策
    """

    def __init__(self, variance: float = 0.1, demo_prefix: str = DEMO_PREFIX,
                 demo_disclaimer: str = DEMO_DISCLAIMER):
        """
        Args:
            variance: 数据随机波动幅度（0-1），0表示固定数据
            demo_prefix: 演示数据前缀标记
            demo_disclaimer: 演示数据免责声明
        """
        self.variance = variance
        self.demo_prefix = demo_prefix
        self.demo_disclaimer = demo_disclaimer

    def _fluctuate(self, base: float) -> float:
        """在基础值上加随机波动"""
        if self.variance == 0:
            return base
        return base * (1 + random.uniform(-self.variance, self.variance))

    def _demo_meta(self, data: Any) -> dict:
        """为数据附加演示数据标识元信息"""
        if isinstance(data, dict):
            return {
                "_demo": True,
                "_demo_prefix": self.demo_prefix,
                "_demo_source": DEMO_DATA_SOURCE,
                "_demo_disclaimer": self.demo_disclaimer,
                **data,
            }
        return {
            "_demo": True,
            "_demo_prefix": self.demo_prefix,
            "_demo_source": DEMO_DATA_SOURCE,
            "_demo_disclaimer": self.demo_disclaimer,
            "data": data,
        }

    def query_inventory(
        self,
        sku: Optional[str] = None,
        warehouse: Optional[str] = None,
    ) -> APIResponse:
        """模拟库存查询"""
        import time
        start = time.time()
        if sku:
            data = MOCK_INVENTORY.get(sku)
            if data is None:
                return APIResponse(
                    success=False,
                    error=f"SKU [{sku}] 不存在",
                    source="mock",
                    latency_ms=(time.time() - start) * 1000,
                )
            result = self._demo_meta({**data, "quantity": int(self._fluctuate(data["quantity"]))})
        else:
            result = self._demo_meta([
                {**item, "quantity": int(self._fluctuate(item["quantity"]))}
                for item in MOCK_INVENTORY.values()
                if not warehouse or item["warehouse"] == warehouse
            ])
        return APIResponse(
            success=True,
            data=result,
            source="mock",
            latency_ms=(time.time() - start) * 1000,
        )

    def query_orders(
        self,
        order_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> APIResponse:
        """模拟订单查询"""
        import time
        start = time.time()
        if order_id:
            data = next((o for o in MOCK_ORDERS if o["order_id"] == order_id), None)
            if data is None:
                return APIResponse(success=False, error=f"订单 [{order_id}] 不存在", source="mock")
            result = self._demo_meta(data)
        else:
            result = self._demo_meta(MOCK_ORDERS if not status else [o for o in MOCK_ORDERS if o["status"] == status])
        return APIResponse(
            success=True,
            data=result,
            source="mock",
            latency_ms=(time.time() - start) * 1000,
        )

    def create_order(self, order_data: dict) -> APIResponse:
        """模拟创建订单"""
        import time
        start = time.time()
        new_order = self._demo_meta({
            "order_id": f"PO{datetime.now().strftime('%Y%m%d')}{random.randint(100, 999)}",
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            **order_data,
        })
        MOCK_ORDERS.append(new_order)
        return APIResponse(
            success=True,
            data=new_order,
            source="mock",
            status_code=201,
            latency_ms=(time.time() - start) * 1000,
        )

    def query_suppliers(self, supplier_id: Optional[str] = None) -> APIResponse:
        """模拟供应商查询"""
        import time
        start = time.time()
        if supplier_id:
            data = MOCK_SUPPLIERS.get(supplier_id)
            if data is None:
                return APIResponse(success=False, error=f"供应商 [{supplier_id}] 不存在", source="mock")
            result = self._demo_meta(data)
        else:
            result = self._demo_meta(list(MOCK_SUPPLIERS.values()))
        return APIResponse(
            success=True,
            data=result,
            source="mock",
            latency_ms=(time.time() - start) * 1000,
        )

    def query_shipments(self, tracking_no: Optional[str] = None) -> APIResponse:
        """模拟物流查询"""
        import time
        start = time.time()
        if tracking_no:
            data = MOCK_SHIPMENTS.get(tracking_no)
            if data is None:
                return APIResponse(success=False, error=f"运单 [{tracking_no}] 不存在", source="mock")
            result = self._demo_meta(data)
        else:
            result = self._demo_meta(list(MOCK_SHIPMENTS.values()))
        return APIResponse(
            success=True,
            data=result,
            source="mock",
            latency_ms=(time.time() - start) * 1000,
        )

    def query_finance(
        self,
        budget_summary: bool = True,
        recent_payments: bool = False,
    ) -> APIResponse:
        """模拟财务查询"""
        import time
        start = time.time()
        result = self._demo_meta({
            k: v for k, v in {
                "budget_summary": MOCK_FINANCE.get("budget_summary") if budget_summary else None,
                "recent_payments": MOCK_FINANCE.get("recent_payments") if recent_payments else None,
            }.items() if v is not None
        })
        return APIResponse(
            success=True,
            data=result,
            source="mock",
            latency_ms=(time.time() - start) * 1000,
        )

    def health_check(self) -> dict:
        """模拟健康检查"""
        return {
            "_demo": True,
            "_demo_prefix": self.demo_prefix,
            "_demo_source": DEMO_DATA_SOURCE,
            "_demo_disclaimer": self.demo_disclaimer,
            "erp_type": "mock",
            "status": "healthy",
            "latency_ms": random.uniform(5, 20),
            "message": f"{self.demo_prefix} 模拟数据模式运行正常",
            "last_success": datetime.now().isoformat(),
            "failure_count": 0,
        }
