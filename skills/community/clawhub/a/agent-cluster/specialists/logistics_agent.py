"""
Logistics Agent - 物流智能体

专注领域：运费查询、路线规划、物流跟踪、物流API调用

角色定位：专业智能体，接收指挥智能体任务分派，
返回物流相关的结构化分析结果
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional

from safety.audit_logger import AuditLogger, EventType, LogLevel, traced
from safety.permission_manager import PermissionManager, PermissionContext, PermissionResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class TransportMode(Enum):
    """运输方式"""
    TRUCK = "truck"           # 公路运输
    RAIL = "rail"           # 铁路运输
    SEA = "sea"             # 海运
    AIR = "air"             # 空运
    MULTIMODAL = "multimodal"  # 多式联运


class ShipmentStatus(Enum):
    """物流状态"""
    PENDING = "pending"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    EXCEPTION = "exception"


@dataclass
class FreightQuote:
    """运费报价"""
    origin: str
    destination: str
    weight: float
    volume: float
    transport_mode: str
    unit_price: float
    total_price: float
    estimated_days: int
    carrier: str
    carrier_rating: float
    insurance_available: bool
    insurance_fee: float = 0.0
    remarks: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RoutePlan:
    """路线规划"""
    origin: str
    destination: str
    distance_km: float
    estimated_hours: float
    transport_mode: str
    waypoints: list[dict]
    cost_breakdown: dict[str, float]
    total_cost: float
    carbon_footprint_kg: float
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Shipment:
    """物流追踪"""
    tracking_no: str
    status: str
    origin: str
    destination: str
    current_location: str
    estimated_delivery: str
    events: list[dict]
    carrier: str
    carrier_contact: str

    def to_dict(self) -> dict:
        return asdict(self)


# =============================================================================
# 物流服务（模拟外部API）
# =============================================================================

class LogisticsAPIService:
    """物流API封装（模拟外部三方API）"""

    CARRIERS = {
        "SF": {"name": "顺丰速运", "rating": 4.9, "coverage": "全国", "avg_days": 1.5},
        "YTO": {"name": "圆通速递", "rating": 4.5, "coverage": "全国", "avg_days": 3.0},
        "ZTO": {"name": "中通速递", "rating": 4.4, "coverage": "全国", "avg_days": 3.5},
        "JD": {"name": "京东物流", "rating": 4.8, "coverage": "全国", "avg_days": 1.8},
        "DB": {"name": "德邦快递", "rating": 4.6, "coverage": "全国", "avg_days": 2.5},
    }

    PRICE_RATES = {
        "truck": 0.8,      # 元/吨/公里
        "rail": 0.5,
        "sea": 0.3,
        "air": 8.0,
    }

    async def get_freight_quote(
        self,
        origin: str,
        destination: str,
        weight: float,
        volume: float = 0.0,
        transport_mode: str = "truck",
    ) -> dict[str, Any]:
        """获取运费报价"""
        await asyncio.sleep(0.08)

        # 模拟距离计算
        distance = self._calc_distance(origin, destination)
        rate = self.PRICE_RATES.get(transport_mode, 0.8)

        # 计费重量（体积重与实际重取大）
        volume_weight = volume * 167  # 长cm×宽cm×高cm/6000 ≈ ×0.167
        billable_weight = max(weight, volume_weight)

        base_cost = billable_weight * distance * rate / 1000  # 转换为元

        quotes = []
        for carrier_code, carrier_info in self.CARRIERS.items():
            # 不同承运商价格浮动
            multiplier = 1.0 + (carrier_info["rating"] - 4.4) * 0.3
            insurance_fee = base_cost * 0.002  # 保费=货值×0.2%

            quotes.append({
                "carrier_code": carrier_code,
                "carrier_name": carrier_info["name"],
                "carrier_rating": carrier_info["rating"],
                "unit_price": round(base_cost * multiplier / billable_weight, 2),
                "total_price": round(base_cost * multiplier, 2),
                "estimated_days": carrier_info["avg_days"],
                "insurance_available": True,
                "insurance_fee": round(insurance_fee, 2),
                "tracking_available": True,
            })

        # 按价格排序
        quotes.sort(key=lambda x: x["total_price"])

        return {
            "success": True,
            "origin": origin,
            "destination": destination,
            "weight": weight,
            "volume": volume,
            "distance_km": distance,
            "billable_weight": round(billable_weight, 2),
            "transport_mode": transport_mode,
            "quotes": quotes,
            "best_value": quotes[0] if quotes else None,
        }

    async def plan_route(
        self,
        origin: str,
        destination: str,
        cargo_type: str = "general",
        urgent: bool = False,
    ) -> dict[str, Any]:
        """规划物流路线"""
        await asyncio.sleep(0.1)

        distance = self._calc_distance(origin, destination)

        # 选择最优运输方式
        if urgent:
            transport_mode = "air"
            estimated_hours = distance / 800  # 800km/h
            carbon = distance * 0.18  # kg CO2/km
        else:
            if distance > 1000:
                transport_mode = "rail"
                estimated_hours = distance / 60  # 60km/h
                carbon = distance * 0.06
            else:
                transport_mode = "truck"
                estimated_hours = distance / 50  # 50km/h（含停靠）
                carbon = distance * 0.12

        waypoints = self._generate_waypoints(origin, destination, transport_mode)

        cost = distance * self.PRICE_RATES.get(transport_mode, 0.8) / 1000

        return {
            "success": True,
            "origin": origin,
            "destination": destination,
            "distance_km": round(distance, 1),
            "estimated_hours": round(estimated_hours, 1),
            "estimated_days": round(estimated_hours / 24, 1),
            "transport_mode": transport_mode,
            "waypoints": waypoints,
            "cost_breakdown": {
                "base_freight": round(cost, 2),
                "fuel_surcharge": round(cost * 0.15, 2),
                "handling_fee": round(max(cost * 0.05, 20), 2),
                "insurance": round(cost * 0.02, 2),
            },
            "total_cost": round(cost * 1.22, 2),  # 含附加费
            "carbon_footprint_kg": round(carbon, 1),
            "recommendations": [
                f"推荐{self.CARRIERS['SF']['name']}" if urgent else f"推荐{self.CARRIERS['DB']['name']}大件运输",
                "建议购买货运险，覆盖货值3‰",
                f"碳排放: {round(carbon, 1)}kg CO2，可通过植树中和",
            ] if not urgent else [f"建议使用{self.CARRIERS['SF']['name']}空运"],
        }

    async def track_shipment(self, tracking_no: str) -> dict[str, Any]:
        """追踪物流"""
        await asyncio.sleep(0.05)

        # 模拟物流轨迹
        events = [
            {
                "time": (datetime.now() - timedelta(days=2)).isoformat(),
                "location": "上海浦东分拨中心",
                "status": "已揽收",
                "description": "快件已收件，正在分拣",
            },
            {
                "time": (datetime.now() - timedelta(days=1)).isoformat(),
                "location": "上海转运中心",
                "status": "运输中",
                "description": "快件已离开上海，正在发往目的地",
            },
            {
                "time": (datetime.now() - timedelta(hours=12)).isoformat(),
                "location": "北京大兴分拨中心",
                "status": "到达目的城市",
                "description": "快件已到达北京分拨中心",
            },
            {
                "time": (datetime.now() - timedelta(hours=2)).isoformat(),
                "location": "北京朝阳区营业部",
                "status": "派送中",
                "description": "快递员正在派送，预计今日送达",
            },
        ]

        return {
            "success": True,
            "tracking_no": tracking_no,
            "status": "in_transit",
            "current_location": "北京朝阳区",
            "estimated_delivery": datetime.now().isoformat(),
            "events": events,
            "carrier": "顺丰速运",
            "carrier_phone": "95338",
        }

    @staticmethod
    def _calc_distance(origin: str, destination: str) -> float:
        """模拟距离计算"""
        # 简单哈希模拟城市间距离
        o_hash = sum(ord(c) for c in origin)
        d_hash = sum(ord(c) for c in destination)
        return abs(o_hash - d_hash) * 5 + 100

    @staticmethod
    def _generate_waypoints(
        origin: str,
        destination: str,
        mode: str
    ) -> list[dict]:
        """生成途经点"""
        waypoints = [
            {"name": f"{origin}物流中心", "arrival": "出发", "departure": "02:00"},
            {"name": "高速公路服务区", "arrival": "中途停靠", "departure": "30分钟后"},
            {"name": "目的地城市分拨中心", "arrival": "到达", "departure": "卸货中"},
        ]
        return waypoints


# =============================================================================
# 物流智能体
# =============================================================================

class LogisticsAgent:
    """
    物流智能体

    核心能力：
    1. 运费查询：多承运商比较
    2. 路线规划：最优运输方式推荐
    3. 物流追踪：实时状态更新
    4. 成本优化建议
    """

    def __init__(
        self,
        agent_id: str = "logistics_agent",
        user_id: str = "system",
        user_role: str = "logistics_operator",
    ):
        self.agent_id = agent_id
        self.user_id = user_id
        self.user_role = user_role

        self._api = LogisticsAPIService()
        self._audit = AuditLogger(log_dir=f"./logs/{agent_id}")
        self._permission = PermissionManager()

        self.capabilities = [
            "query_freight",
            "plan_route",
            "track_shipment",
            "compare_carriers",
        ]

        logger.info(f"物流智能体初始化: {agent_id}")

    @traced(agent_name="logistics_agent", action="query_freight")
    async def query_freight(
        self,
        origin: str,
        destination: str,
        weight: float,
        volume: float = 0.0,
        transport_mode: str = "truck",
        compare_carriers: bool = True,
    ) -> dict[str, Any]:
        """
        查询运费

        Args:
            origin: 出发地
            destination: 目的地
            weight: 货物重量(kg)
            volume: 体积(m³)
            transport_mode: 运输方式
            compare_carriers: 是否比较承运商

        Returns:
            运费报价结果
        """
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="query_freight",
            parameters={"origin": origin, "destination": destination, "weight": weight},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return {"success": False, "error": decision.reason}

        result = await self._api.get_freight_quote(
            origin=origin,
            destination=destination,
            weight=weight,
            volume=volume,
            transport_mode=transport_mode,
        )

        if not result["success"]:
            return result

        # 生成分析建议
        best = result["best_value"]
        summary = {
            "total_quotes": len(result["quotes"]),
            "best_price": best["total_price"] if best else None,
            "cheapest_carrier": result["quotes"][0]["carrier_name"] if result["quotes"] else None,
            "fastest_carrier": min(result["quotes"], key=lambda x: x["estimated_days"])["carrier_name"]
                if result["quotes"] else None,
            "avg_price": round(sum(q["total_price"] for q in result["quotes"]) / len(result["quotes"]), 2)
                if result["quotes"] else None,
            "price_range": {
                "min": result["quotes"][0]["total_price"] if result["quotes"] else 0,
                "max": result["quotes"][-1]["total_price"] if result["quotes"] else 0,
            },
        }

        return {
            **result,
            "analysis": summary,
            "recommendation": self._generate_recommendation(result, summary),
        }

    @traced(agent_name="logistics_agent", action="plan_route")
    async def plan_route(
        self,
        origin: str,
        destination: str,
        cargo_type: str = "general",
        urgent: bool = False,
        max_budget: Optional[float] = None,
    ) -> RoutePlan:
        """规划物流路线"""
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="plan_route",
            parameters={"origin": origin, "destination": destination, "urgent": urgent},
        )
        decision = self._permission.check_permission(ctx)
        if decision.result == PermissionResult.DENIED:
            return RoutePlan(
                origin=origin,
                destination=destination,
                distance_km=0,
                estimated_hours=0,
                transport_mode="error",
                waypoints=[],
                cost_breakdown={},
                total_cost=0,
                carbon_footprint_kg=0,
                recommendations=[decision.reason],
            )

        result = await self._api.plan_route(
            origin=origin,
            destination=destination,
            cargo_type=cargo_type,
            urgent=urgent,
        )

        return RoutePlan(
            origin=result["origin"],
            destination=result["destination"],
            distance_km=result["distance_km"],
            estimated_hours=result["estimated_hours"],
            transport_mode=result["transport_mode"],
            waypoints=result["waypoints"],
            cost_breakdown=result["cost_breakdown"],
            total_cost=result["total_cost"],
            carbon_footprint_kg=result["carbon_footprint_kg"],
            recommendations=result["recommendations"],
        )

    @traced(agent_name="logistics_agent", action="track_shipment")
    async def track_shipment(self, tracking_no: str) -> Shipment:
        """追踪物流"""
        ctx = PermissionContext(
            user_id=self.user_id,
            user_role=self.user_role,
            agent_id=self.agent_id,
            action="track_shipment",
            parameters={"tracking_no": tracking_no},
        )
        decision = self._permission.check_permission(ctx)

        result = await self._api.track_shipment(tracking_no)
        return Shipment(
            tracking_no=result["tracking_no"],
            status=result["status"],
            origin=result["origin"] or "",
            destination=result["destination"] or "",
            current_location=result["current_location"],
            estimated_delivery=result["estimated_delivery"],
            events=result["events"],
            carrier=result["carrier"],
            carrier_contact=result["carrier_phone"],
        )

    def _generate_recommendation(
        self,
        result: dict,
        summary: dict
    ) -> dict[str, Any]:
        """生成物流建议"""
        best = result["best_value"]
        if not best:
            return {"action": "无法提供建议", "reason": "无可用承运商"}

        return {
            "recommended_carrier": best["carrier_name"],
            "reason": f"综合评分{best['carrier_rating']}，价格¥{best['total_price']}，"
                      f"预计{best['estimated_days']}天送达",
            "alternative": summary.get("cheapest_carrier"),
            "cost_saving_tip": (
                f"选择{result['quotes'][0]['carrier_name']}可节省¥"
                f"{result['quotes'][-1]['total_price'] - result['quotes'][0]['total_price']}"
                if len(result["quotes"]) > 1 else "当前已是最优价格"
            ),
        }

    async def compare_logistics_options(
        self,
        origin: str,
        destination: str,
        weight: float,
    ) -> dict[str, Any]:
        """综合比较多种运输方案"""
        results = {}

        for mode in ["truck", "rail", "air"]:
            result = await self.query_freight(
                origin=origin,
                destination=destination,
                weight=weight,
                transport_mode=mode,
            )
            if result.get("best_value"):
                results[mode] = {
                    "carrier": result["best_value"]["carrier_name"],
                    "price": result["best_value"]["total_price"],
                    "days": result["best_value"]["estimated_days"],
                    "price_per_kg": round(result["best_value"]["unit_price"], 2),
                }

        return {
            "success": True,
            "origin": origin,
            "destination": destination,
            "weight": weight,
            "options": results,
            "best_value": min(results.items(), key=lambda x: x[1]["price"]) if results else None,
        }


# =============================================================================
# 入口
# =============================================================================

if __name__ == "__main__":
    async def demo():
        print("=" * 60)
        print("  物流智能体演示")
        print("=" * 60)

        agent = LogisticsAgent(user_role="logistics_operator")

        # 运费查询
        print("\n[1] 查询上海→北京运费")
        result = await agent.query_freight(
            origin="上海",
            destination="北京",
            weight=500,
            volume=2.0,
        )
        print(f"  距离: {result['distance_km']}km")
        print(f"  报价数量: {result['analysis']['total_quotes']}")
        print(f"  最优价格: ¥{result['analysis']['best_price']} ({result['analysis']['cheapest_carrier']})")
        print(f"  推荐: {result['recommendation']['recommended_carrier']}")

        # 路线规划
        print("\n[2] 规划物流路线")
        route = await agent.plan_route(
            origin="上海",
            destination="广州",
            urgent=False,
        )
        print(f"  距离: {route.distance_km}km")
        print(f"  预计: {route.estimated_hours}小时")
        print(f"  方式: {route.transport_mode}")
        print(f"  总费用: ¥{route.total_cost}")
        print(f"  碳排放: {route.carbon_footprint_kg}kg CO2")
        print(f"  建议: {route.recommendations[0]}")

        # 物流追踪
        print("\n[3] 物流追踪")
        shipment = await agent.track_shipment("SF1234567890")
        print(f"  状态: {shipment.status}")
        print(f"  当前位置: {shipment.current_location}")
        print(f"  最新事件: {shipment.events[-1]['status']} @ {shipment.events[-1]['location']}")

    asyncio.run(demo())
