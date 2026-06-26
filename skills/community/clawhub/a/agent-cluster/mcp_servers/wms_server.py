"""
WMS (Warehouse Management System) MCP Server
仓库管理系统MCP协议封装

提供仓库数据查询、库位管理、盘点管理等WMS核心接口
"""

from __future__ import annotations

import asyncio
import uuid
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class LocationType(Enum):
    """库位类型"""
    STORAGE = "storage"           # 存储区
    PICKING = "picking"           # 拣货区
    STAGING = "staging"           # 待发区
    RECEIVING = "receiving"       # 收货区
    DEFECTIVE = "defective"       # 残次区


class InventoryStatus(Enum):
    """库存状态"""
    AVAILABLE = "available"       # 可用
    RESERVED = "reserved"         # 已预留
    QUARANTINE = "quarantine"    # 隔离/待检
    DAMAGED = "damaged"          # 损坏


@dataclass
class WarehouseLocation:
    """库位"""
    location_id: str
    zone: str                     # 库区
    aisle: str                    # 巷道
    rack: str                     # 货架
    level: str                    # 层
    position: str                 # 位
    warehouse_id: str = ""        # 所属仓库
    location_type: LocationType = LocationType.STORAGE
    capacity: int = 100           # 容量
    current_fill: int = 0        # 当前填充率


@dataclass
class InventoryRecord:
    """库存记录"""
    record_id: str
    sku: str
    batch_no: str
    quantity: int
    location_id: str
    warehouse_id: str
    status: InventoryStatus = InventoryStatus.AVAILABLE
    received_at: str = field(default_factory=lambda: datetime.now().isoformat())
    expiry_date: str = ""
    lot_no: str = ""


@dataclass
class MovementRecord:
    """移库记录"""
    movement_id: str
    sku: str
    from_location: str
    to_location: str
    quantity: int
    operator: str
    reason: str
    moved_at: str = field(default_factory=lambda: datetime.now().isoformat())


# =============================================================================
# WMS服务层
# =============================================================================

class WMSService:
    """
    仓库管理系统服务

    核心功能：
    - 仓库与库位管理
    - 库存查询与状态管理
    - 移库操作
    - 批次追溯
    """

    def __init__(self):
        self._warehouses = self._init_warehouses()
        self._locations = self._init_locations()
        self._inventory = self._init_inventory()
        self._movements: list[MovementRecord] = []

    def _init_warehouses(self) -> dict[str, dict]:
        return {
            "WH001": {"id": "WH001", "name": "华东配送中心", "region": "华东", "capacity": 50000},
            "WH002": {"id": "WH002", "name": "华北配送中心", "region": "华北", "capacity": 30000},
            "WH003": {"id": "WH003", "name": "华南配送中心", "region": "华南", "capacity": 40000},
        }

    def _init_locations(self) -> dict[str, WarehouseLocation]:
        locations = {}
        for wh_id, wh in self._warehouses.items():
            for zone in ["A", "B", "C"]:
                for aisle in range(1, 5):
                    for rack in range(1, 6):
                        for level in range(1, 4):
                            loc_id = f"{wh_id}-{zone}{aisle:02d}-{rack:02d}-{level:02d}"
                            locations[loc_id] = WarehouseLocation(
                                location_id=loc_id,
                                zone=zone,
                                aisle=str(aisle),
                                rack=str(rack),
                                level=str(level),
                                position="01",
                                warehouse_id=wh_id,
                                capacity=100,
                                current_fill=0,
                            )
        return locations

    def _init_inventory(self) -> dict[str, InventoryRecord]:
        """初始化模拟库存"""
        records = {}
        items = [
            ("SKU001", "WH001", 500, "LOT20240101"),
            ("SKU001", "WH002", 300, "LOT20240102"),
            ("SKU002", "WH001", 200, "LOT20240103"),
            ("SKU003", "WH001", 80, "LOT20240104"),
            ("SKU004", "WH001", 25, "LOT20240105"),
            ("SKU005", "WH003", 0, "LOT20240106"),
        ]
        for i, (sku, wh, qty, lot) in enumerate(items):
            loc_id = f"{wh}-A01-{(i % 5) + 1:02d}-{(i % 3) + 1:02d}"
            rec_id = f"INV{uuid.uuid4().hex[:8].upper()}"
            records[rec_id] = InventoryRecord(
                record_id=rec_id,
                sku=sku,
                batch_no=lot,
                quantity=qty,
                location_id=loc_id,
                warehouse_id=wh,
                status=InventoryStatus.QUARANTINE if qty == 0 else InventoryStatus.AVAILABLE,
                lot_no=lot,
            )
        return records

    # -------------------------------------------------------------------------
    # 核心业务方法
    # -------------------------------------------------------------------------

    async def get_warehouse_summary(self, warehouse_id: Optional[str] = None) -> dict[str, Any]:
        """获取仓库概览"""
        await asyncio.sleep(0.05)
        warehouses = {k: v for k, v in self._warehouses.items() if warehouse_id is None or k == warehouse_id}

        result = {}
        for wh_id, wh in warehouses.items():
            # 统计该仓库库位数
            locs = [l for l in self._locations.values() if l.warehouse_id == wh_id]
            # 统计库存
            inv_count = sum(r.quantity for r in self._inventory.values() if r.warehouse_id == wh_id)
            sku_count = len({r.sku for r in self._inventory.values() if r.warehouse_id == wh_id})

            result[wh_id] = {
                **wh,
                "total_locations": len(locs),
                "total_inventory": inv_count,
                "sku_count": sku_count,
                "utilization_rate": round(inv_count / wh["capacity"] * 100, 2),
            }

        return {"success": True, "data": result}

    async def find_available_location(
        self,
        warehouse_id: str,
        zone: Optional[str] = None,
        required_capacity: int = 10
    ) -> dict[str, Any]:
        """查找可用库位"""
        await asyncio.sleep(0.05)

        candidates = [
            loc for loc in self._locations.values()
            if loc.warehouse_id == warehouse_id
            and (zone is None or loc.zone == zone)
            and (loc.capacity - loc.current_fill) >= required_capacity
            and loc.location_type == LocationType.STORAGE
        ]

        if not candidates:
            return {"success": False, "error": "无可用库位", "warehouse_id": warehouse_id}

        best = candidates[0]
        return {
            "success": True,
            "data": {
                "location_id": best.location_id,
                "zone": best.zone,
                "aisle": best.aisle,
                "rack": best.rack,
                "level": best.level,
                "available_capacity": best.capacity - best.current_fill,
                "suggestion": f"建议存放至{best.zone}区{best.aisle}巷道{best.rack}货架第{best.level}层",
            }
        }

    async def transfer_stock(
        self,
        sku: str,
        from_warehouse: str,
        to_warehouse: str,
        quantity: int,
        reason: str = "调拨"
    ) -> dict[str, Any]:
        """库存调拨"""
        await asyncio.sleep(0.1)

        # 查找源库存
        source_rec = None
        for rec in self._inventory.values():
            if rec.sku == sku and rec.warehouse_id == from_warehouse and rec.quantity >= quantity:
                source_rec = rec
                break

        if not source_rec:
            return {"success": False, "error": f"{from_warehouse}仓库中{sku}库存不足"}

        # 查找目标库位
        loc_result = await self.find_available_location(to_warehouse)
        if not loc_result["success"]:
            return loc_result

        to_location = loc_result["data"]["location_id"]

        # 执行调拨
        source_rec.quantity -= quantity
        movement_id = f"MOV{uuid.uuid4().hex[:8].upper()}"
        self._movements.append(MovementRecord(
            movement_id=movement_id,
            sku=sku,
            from_location=source_rec.location_id,
            to_location=to_location,
            quantity=quantity,
            operator="system",
            reason=reason,
        ))

        # 在目标仓库创建新记录
        new_id = f"INV{uuid.uuid4().hex[:8].upper()}"
        self._inventory[new_id] = InventoryRecord(
            record_id=new_id,
            sku=sku,
            batch_no=source_rec.batch_no,
            quantity=quantity,
            location_id=to_location,
            warehouse_id=to_warehouse,
            status=InventoryStatus.AVAILABLE,
            lot_no=source_rec.lot_no,
        )

        return {
            "success": True,
            "data": {
                "movement_id": movement_id,
                "sku": sku,
                "from_warehouse": from_warehouse,
                "to_warehouse": to_warehouse,
                "to_location": to_location,
                "quantity": quantity,
                "reason": reason,
                "moved_at": self._movements[-1].moved_at,
            }
        }

    async def get_inventory_by_sku(self, sku: str) -> dict[str, Any]:
        """按SKU查询所有仓库库存分布"""
        await asyncio.sleep(0.05)

        records = [r for r in self._inventory.values() if r.sku == sku and r.quantity > 0]
        total = sum(r.quantity for r in records)

        distribution = {}
        for r in records:
            wh = r.warehouse_id
            if wh not in distribution:
                distribution[wh] = {"warehouse": self._warehouses[wh]["name"], "total": 0, "locations": []}
            distribution[wh]["total"] += r.quantity
            distribution[wh]["locations"].append({
                "location": r.location_id,
                "quantity": r.quantity,
                "batch": r.batch_no,
                "status": r.status.value,
            })

        return {
            "success": True,
            "data": {
                "sku": sku,
                "total_quantity": total,
                "warehouse_distribution": distribution,
                "record_count": len(records),
            }
        }


# =============================================================================
# MCP协议处理器
# =============================================================================

class WMSProtocolHandler:
    """WMS MCP协议处理器"""

    def __init__(self, service: WMSService):
        self.service = service
        self._tools = {
            "wms.warehouse_summary": service.get_warehouse_summary,
            "wms.find_location": service.find_available_location,
            "wms.transfer_stock": service.transfer_stock,
            "wms.inventory_by_sku": service.get_inventory_by_sku,
        }

    async def list_tools(self) -> list[dict]:
        return [
            {"name": name, "description": func.__doc__.strip().split("\n")[0] if func.__doc__ else ""}
            for name, func in self._tools.items()
        ]

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        if tool_name not in self._tools:
            return {"error": f"未知工具: {tool_name}"}
        return await self._tools[tool_name](**{k: v for k, v in arguments.items() if k != "name"})


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    async def test():
        service = WMSService()
        handler = WMSProtocolHandler(service)

        print("\n[仓库概览]")
        r = await service.get_warehouse_summary()
        for wh_id, info in r["data"].items():
            print(f"  {info['name']}: 在库{int(info['total_inventory'])}件, 利用率{info['utilization_rate']}%")

        print("\n[SKU001库存分布]")
        r = await service.get_inventory_by_sku("SKU001")
        print(f"  总计: {r['data']['total_quantity']}件")
        for wh, dist in r["data"]["warehouse_distribution"].items():
            print(f"  {dist['warehouse']}: {dist['total']}件")

        print("\n[查找华东仓可用库位]")
        r = await service.find_available_location("WH001")
        print(f"  {r['data']['suggestion']}")

    asyncio.run(test())
