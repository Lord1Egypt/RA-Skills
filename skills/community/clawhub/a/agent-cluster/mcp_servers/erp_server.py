"""
ERP (Enterprise Resource Planning) MCP Server
ERP系统MCP协议封装

提供库存查询、安全水位计算、订单管理等ERP核心接口
基于Model Context Protocol实现标准化调用
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from enum import Enum
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class StockStatus(Enum):
    """库存状态枚举"""
    NORMAL = "normal"              # 正常
    LOW = "low"                    # 低库存
    CRITICAL = "critical"          # 紧急缺货
    OVERSTOCKED = "overstocked"   # 库存过剩


class OrderStatus(Enum):
    """订单状态枚举"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PRODUCTION = "in_production"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class StockItem:
    """库存项"""
    sku: str
    name: str
    quantity: int
    unit: str = "件"
    warehouse: str = "主仓"
    location: str = ""
    safety_stock: int = 0
    max_stock: int = 0
    status: StockStatus = StockStatus.NORMAL
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())

    def check_status(self) -> StockStatus:
        """检查库存状态"""
        if self.quantity <= 0:
            self.status = StockStatus.CRITICAL
        elif self.quantity <= self.safety_stock:
            self.status = StockStatus.LOW
        elif self.quantity > self.max_stock:
            self.status = StockStatus.OVERSTOCKED
        else:
            self.status = StockStatus.NORMAL
        return self.status


@dataclass
class PurchaseOrder:
    """采购订单"""
    order_id: str
    supplier_id: str
    supplier_name: str
    items: list[dict]
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    expected_delivery: str = ""
    notes: str = ""


@dataclass
class MCPTool:
    """MCP工具定义"""
    name: str
    description: str
    input_schema: dict
    output_schema: dict


@dataclass
class MCPRequest:
    """MCP请求"""
    jsonrpc: str = "2.0"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    method: str = ""
    params: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)


@dataclass
class MCPResponse:
    """MCP响应"""
    jsonrpc: str = "2.0"
    id: str = ""
    result: Optional[dict] = None
    error: Optional[dict] = None

    def to_dict(self) -> dict:
        if self.error:
            return {
                "jsonrpc": self.jsonrpc,
                "id": self.id,
                "error": self.error
            }
        return {
            "jsonrpc": self.jsonrpc,
            "id": self.id,
            "result": self.result
        }


# =============================================================================
# ERP服务模拟层（实际项目中替换为真实ERP API调用）
# =============================================================================

class ERPService:
    """
    ERP服务封装层

    模拟企业ERP系统接口，包含：
    - 库存查询与管理
    - 采购订单管理
    - 供应商管理
    """

    def __init__(self):
        # 模拟数据库
        self._stock_db: dict[str, StockItem] = self._init_stock_db()
        self._orders_db: dict[str, PurchaseOrder] = {}
        self._suppliers_db = self._init_suppliers()

    # -------------------------------------------------------------------------
    # 初始化数据
    # -------------------------------------------------------------------------

    def _init_stock_db(self) -> dict[str, StockItem]:
        """初始化模拟库存数据"""
        return {
            "SKU001": StockItem(
                sku="SKU001", name="电机轴承 6205-2Z",
                quantity=1200, unit="套", warehouse="华东仓",
                safety_stock=500, max_stock=3000,
            ),
            "SKU002": StockItem(
                sku="SKU002", name="不锈钢板 304 2mm",
                quantity=350, unit="张", warehouse="华北仓",
                safety_stock=400, max_stock=2000,
            ),
            "SKU003": StockItem(
                sku="SKU003", name="液压油 HLP-46",
                quantity=80, unit="桶", warehouse="华东仓",
                safety_stock=100, max_stock=500,
            ),
            "SKU004": StockItem(
                sku="SKU004", name="PLC控制器 S7-1200",
                quantity=25, unit="台", warehouse="华东仓",
                safety_stock=20, max_stock=100,
            ),
            "SKU005": StockItem(
                sku="SKU005", name="工业皮带 10M-1200",
                quantity=0, unit="条", warehouse="华南仓",
                safety_stock=50, max_stock=500,
            ),
        }

    def _init_suppliers(self) -> dict[str, dict]:
        """初始化供应商数据"""
        return {
            "SUP001": {"id": "SUP001", "name": "华东轴承有限公司", "rating": 4.8, "lead_time_days": 3},
            "SUP002": {"id": "SUP002", "name": "宝钢材料供应链", "rating": 4.6, "lead_time_days": 5},
            "SUP003": {"id": "SUP003", "name": "壳牌工业油品", "rating": 4.9, "lead_time_days": 2},
            "SUP004": {"id": "SUP004", "name": "西门子工业自动化", "rating": 4.7, "lead_time_days": 7},
        }

    # -------------------------------------------------------------------------
    # 核心业务方法
    # -------------------------------------------------------------------------

    async def query_stock(
        self,
        sku: Optional[str] = None,
        warehouse: Optional[str] = None,
        status_filter: Optional[StockStatus] = None
    ) -> dict[str, Any]:
        """
        查询库存

        Args:
            sku: SKU编码，None表示查询所有
            warehouse: 仓库名称，None表示查询所有
            status_filter: 库存状态过滤

        Returns:
            库存查询结果
        """
        logger.info(f"查询库存: sku={sku}, warehouse={warehouse}")

        await asyncio.sleep(0.1)  # 模拟API延迟

        results = []
        for item in self._stock_db.values():
            if sku and item.sku != sku:
                continue
            if warehouse and item.warehouse != warehouse:
                continue
            if status_filter and item.check_status() != status_filter:
                continue

            results.append({
                "sku": item.sku,
                "name": item.name,
                "quantity": item.quantity,
                "unit": item.unit,
                "warehouse": item.warehouse,
                "location": item.location,
                "safety_stock": item.safety_stock,
                "max_stock": item.max_stock,
                "status": item.check_status().value,
                "stock_ratio": round(item.quantity / item.safety_stock, 2) if item.safety_stock else None,
                "last_updated": item.last_updated,
            })

        return {
            "success": True,
            "count": len(results),
            "data": results,
            "summary": {
                "total_skus": len(results),
                "low_stock_count": sum(1 for r in results if r["status"] == "low"),
                "critical_count": sum(1 for r in results if r["status"] == "critical"),
                "normal_count": sum(1 for r in results if r["status"] == "normal"),
            }
        }

    async def calculate_safety_stock(
        self,
        sku: str,
        lead_time_days: int = 7,
        daily_consumption: Optional[float] = None,
        service_level: float = 0.95
    ) -> dict[str, Any]:
        """
        计算安全库存

        使用统计学方法计算安全库存：
        Safety Stock = Z × σ × √(LT)
        Z: 服务水平对应Z值（1.65 for 95%）
        σ: 需求标准差
        LT: 采购提前期

        Args:
            sku: SKU编码
            lead_time_days: 采购提前期（天）
            daily_consumption: 日均消耗量（未提供则用历史推算）
            service_level: 服务水平（默认95%）

        Returns:
            安全库存计算结果
        """
        logger.info(f"计算安全库存: sku={sku}, lead_time={lead_time_days}, service_level={service_level}")

        await asyncio.sleep(0.05)

        item = self._stock_db.get(sku)
        if not item:
            return {"success": False, "error": f"SKU不存在: {sku}"}

        # Z值表
        z_values = {0.90: 1.28, 0.95: 1.65, 0.97: 1.88, 0.99: 2.33}
        z = z_values.get(service_level, 1.65)

        # 模拟日均消耗和标准差
        if daily_consumption is None:
            daily_consumption = item.quantity / 30 if item.quantity > 0 else 10.0

        # 需求标准差（模拟）
        sigma = daily_consumption * 0.3

        # 安全库存 = Z × σ × √(LT)
        safety_stock_calc = z * sigma * (lead_time_days ** 0.5)

        # 最高库存 = 安全库存 + 日均消耗 × 补货周期
        reorder_point = daily_consumption * lead_time_days + safety_stock_calc

        recommendation = "normal"
        if item.quantity <= safety_stock_calc:
            recommendation = "critical"
        elif item.quantity <= safety_stock_calc * 1.5:
            recommendation = "low"

        return {
            "success": True,
            "data": {
                "sku": sku,
                "name": item.name,
                "current_stock": item.quantity,
                "calculated_safety_stock": round(safety_stock_calc),
                "reorder_point": round(reorder_point),
                "current_safety_stock": item.safety_stock,
                "recommended_reorder_qty": round(max(0, item.max_stock - item.quantity + safety_stock_calc)),
                "service_level": service_level,
                "lead_time_days": lead_time_days,
                "daily_consumption": round(daily_consumption, 2),
                "z_value": z,
                "status": recommendation,
                "formula": f"SS = {z} × {round(sigma, 2)} × √{lead_time_days} = {round(safety_stock_calc)}",
            }
        }

    async def create_purchase_order(
        self,
        supplier_id: str,
        items: list[dict],
        notes: str = "",
        priority: str = "normal"
    ) -> dict[str, Any]:
        """
        创建采购订单

        Args:
            supplier_id: 供应商ID
            items: 采购明细 [{"sku": "SKU001", "quantity": 100, "unit_price": 25.5}]
            notes: 备注
            priority: 优先级 normal/urgent

        Returns:
            采购订单结果
        """
        logger.info(f"创建采购订单: supplier={supplier_id}, items={len(items)}, priority={priority}")

        await asyncio.sleep(0.15)

        supplier = self._suppliers_db.get(supplier_id)
        if not supplier:
            return {"success": False, "error": f"供应商不存在: {supplier_id}"}

        order_id = f"PO{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        total_amount = sum(item.get("quantity", 0) * item.get("unit_price", 0) for item in items)

        order = PurchaseOrder(
            order_id=order_id,
            supplier_id=supplier_id,
            supplier_name=supplier["name"],
            items=items,
            total_amount=total_amount,
            notes=notes,
            expected_delivery=(
                datetime.now().replace(hour=0, minute=0, second=0).isoformat()
            ),
        )
        self._orders_db[order_id] = order

        return {
            "success": True,
            "data": {
                "order_id": order.order_id,
                "supplier_id": supplier_id,
                "supplier_name": supplier["name"],
                "items": items,
                "total_amount": round(total_amount, 2),
                "status": order.status.value,
                "created_at": order.created_at,
                "expected_delivery": supplier["lead_time_days"],
                "priority": priority,
                "notes": notes,
            }
        }

    async def get_order_status(self, order_id: str) -> dict[str, Any]:
        """查询订单状态"""
        await asyncio.sleep(0.05)
        order = self._orders_db.get(order_id)
        if not order:
            return {"success": False, "error": f"订单不存在: {order_id}"}

        return {
            "success": True,
            "data": {
                "order_id": order.order_id,
                "supplier_name": order.supplier_name,
                "status": order.status.value,
                "total_amount": order.total_amount,
                "created_at": order.created_at,
                "items_count": len(order.items),
            }
        }


# =============================================================================
# MCP协议处理器
# =============================================================================

class ERPProtocolHandler:
    """
    ERP MCP协议处理器

    实现标准MCP协议接口：
    - tools/list: 列出可用工具
    - tools/call: 调用工具
    - resources/*: 资源管理
    """

    def __init__(self, service: ERPService):
        self.service = service
        self._tool_registry = self._build_tool_registry()

    def _build_tool_registry(self) -> dict[str, dict]:
        """构建工具注册表"""
        return {
            "erp.query_stock": {
                "handler": self.service.query_stock,
                "description": "查询ERP系统库存数据",
                "parameters": {
                    "sku": {"type": "string", "description": "SKU编码", "required": False},
                    "warehouse": {"type": "string", "description": "仓库名称", "required": False},
                    "status_filter": {"type": "string", "description": "库存状态过滤", "required": False},
                }
            },
            "erp.calculate_safety_stock": {
                "handler": self.service.calculate_safety_stock,
                "description": "计算安全库存水位",
                "parameters": {
                    "sku": {"type": "string", "description": "SKU编码", "required": True},
                    "lead_time_days": {"type": "integer", "description": "采购提前期(天)", "required": False},
                    "daily_consumption": {"type": "number", "description": "日均消耗量", "required": False},
                    "service_level": {"type": "number", "description": "服务水平", "required": False},
                }
            },
            "erp.create_purchase_order": {
                "handler": self.service.create_purchase_order,
                "description": "创建采购订单",
                "parameters": {
                    "supplier_id": {"type": "string", "description": "供应商ID", "required": True},
                    "items": {"type": "array", "description": "采购明细", "required": True},
                    "notes": {"type": "string", "description": "备注", "required": False},
                    "priority": {"type": "string", "description": "优先级", "required": False},
                }
            },
            "erp.get_order_status": {
                "handler": self.service.get_order_status,
                "description": "查询采购订单状态",
                "parameters": {
                    "order_id": {"type": "string", "description": "订单ID", "required": True},
                }
            },
        }

    async def list_tools(self) -> list[MCPTool]:
        """列出所有可用工具"""
        tools = []
        for name, meta in self._tool_registry.items():
            tools.append(MCPTool(
                name=name,
                description=meta["description"],
                input_schema={"type": "object", "properties": meta["parameters"]},
                output_schema={"type": "object"}
            ))
        return tools

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """调用指定工具"""
        if tool_name not in self._tool_registry:
            return {"error": f"未知工具: {tool_name}"}

        handler = self._tool_registry[tool_name]["handler"]

        # 参数验证
        required = []
        for param_name, param_info in self._tool_registry[tool_name]["parameters"].items():
            if param_info.get("required") and param_name not in arguments:
                required.append(param_name)

        if required:
            return {"error": f"缺少必需参数: {required}"}

        try:
            result = await handler(**arguments)
            return result
        except Exception as e:
            # [FIX 2026-04-14] 不使用 logger.exception() 避免敏感信息写入日志
            logger.warning(f"工具调用失败: {tool_name}")
            return {"error": "Internal error"}

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """处理MCP协议请求"""
        response = MCPResponse(id=request.id)

        try:
            if request.method == "tools/list":
                tools = await self.list_tools()
                response.result = {
                    "tools": [
                        {"name": t.name, "description": t.description, "inputSchema": t.input_schema}
                        for t in tools
                    ]
                }
            elif request.method == "tools/call":
                tool_name = request.params.get("name", "")
                arguments = request.params.get("arguments", {})
                result = await self.call_tool(tool_name, arguments)
                response.result = result
            else:
                response.error = {"code": -32601, "message": f"未知方法: {request.method}"}
        except Exception as e:
            logger.exception("MCP请求处理异常")
            response.error = {"code": -32603, "message": f"内部错误: {str(e)}"}

        return response


# =============================================================================
# FastAPI MCP Server（生产部署用）
# =============================================================================

def create_erp_app() -> Any:
    """创建FastAPI ERP MCP Server"""
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        import uvicorn

        app = FastAPI(title="ERP MCP Server", version="1.0.0")
        service = ERPService()
        handler = ERPProtocolHandler(service)

        class ToolCallRequest(BaseModel):
            name: str
            arguments: dict = {}

        @app.get("/health")
        async def health():
            return {"status": "healthy", "service": "erp-mcp-server"}

        @app.get("/tools")
        async def list_tools():
            tools = await handler.list_tools()
            return {"tools": [asdict(t) for t in tools]}

        @app.post("/call")
        async def call_tool(req: ToolCallRequest):
            result = await handler.call_tool(req.name, req.arguments)
            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])
            return result

        @app.get("/stock")
        async def query_stock(sku: str = None, warehouse: str = None):
            return await service.query_stock(sku=sku, warehouse=warehouse)

        @app.get("/stock/{sku}/safety")
        async def safety_stock(sku: str, lead_time_days: int = 7):
            return await service.calculate_safety_stock(sku, lead_time_days)

        @app.post("/orders")
        async def create_order(supplier_id: str, items: list, notes: str = "", priority: str = "normal"):
            return await service.create_purchase_order(supplier_id, items, notes, priority)

        return app
    except ImportError:
        logger.warning("FastAPI/uvicorn未安装，返回None（开发模式）")
        return None


# =============================================================================
# 入口点
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  ERP MCP Server 启动")
    print("  基于Model Context Protocol的企业资源规划接口")
    print("=" * 60)

    app = create_erp_app()
    if app:
        import uvicorn
        # [FIX 2026-04-14] 开发环境使用 127.0.0.1，生产环境通过反向代理暴露
        # ⚠️ 禁止在公网直接绑定 0.0.0.0，必须配置 TLS + API Key 认证
        _host = os.getenv("MCP_HOST", "127.0.0.1")
        _port = int(os.getenv("MCP_PORT", "8081"))
        uvicorn.run(app, host=_host, port=_port, log_level="info")
    else:
        # 开发模式：直接测试
        async def dev_test():
            service = ERPService()
            handler = ERPProtocolHandler(service)

            print("\n[1] 列出所有工具...")
            tools = await handler.list_tools()
            for t in tools:
                print(f"  - {t.name}: {t.description}")

            print("\n[2] 查询库存...")
            result = await service.query_stock()
            print(f"  结果: {result['summary']}")

            print("\n[3] 计算安全库存...")
            result = await service.calculate_safety_stock("SKU003")
            print(f"  安全库存: {result['data']['calculated_safety_stock']}")
            print(f"  建议补货量: {result['data']['recommended_reorder_qty']}")

            print("\n[4] 检查低库存项...")
            result = await service.query_stock(status_filter=StockStatus.LOW)
            print(f"  低库存SKU: {[r['sku'] for r in result['data']]}")

        asyncio.run(dev_test())
