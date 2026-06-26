#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业用车服务技能 - 核心API
"""

import json
import random
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class CarServiceError(Exception):
    """用车服务异常"""
    pass


class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"           # 待接单
    ACCEPTED = "accepted"         # 已接单
    ARRIVING = "arriving"         # 司机前往中
    ARRIVED = "arrived"           # 司机已到达
    IN_PROGRESS = "in_progress"   # 行程进行中
    COMPLETED = "completed"       # 已完成
    CANCELLED = "cancelled"       # 已取消


class CarType(Enum):
    """车型"""
    ECONOMY = "economy"           # 经济型
    COMFORT = "comfort"           # 舒适型
    BUSINESS = "business"         # 商务型
    LUXURY = "luxury"             # 豪华型


# 车型配置
CAR_TYPE_CONFIG = {
    "ECONOMY": {
        "name": "经济型",
        "seats": 4,
        "luggage": 2,
        "base_fare": 14,
        "mileage_rate": 2.3,
        "time_rate": 0.5,
        "examples": ["大众朗逸", "丰田卡罗拉", "日产轩逸"]
    },
    "COMFORT": {
        "name": "舒适型",
        "seats": 4,
        "luggage": 3,
        "base_fare": 18,
        "mileage_rate": 3.0,
        "time_rate": 0.65,
        "examples": ["大众帕萨特", "丰田凯美瑞", "本田雅阁"]
    },
    "BUSINESS": {
        "name": "商务型",
        "seats": 7,
        "luggage": 6,
        "base_fare": 25,
        "mileage_rate": 4.2,
        "time_rate": 0.9,
        "examples": ["别克GL8", "本田奥德赛", "奔驰V级"]
    },
    "LUXURY": {
        "name": "豪华型",
        "seats": 4,
        "luggage": 3,
        "base_fare": 40,
        "mileage_rate": 6.5,
        "time_rate": 1.5,
        "examples": ["奥迪A6L", "宝马5系", "奔驰E级"]
    }
}

# 司机数据库（模拟）
DRIVERS_DB = [
    {
        "driver_id": "DRV001",
        "name": "张师傅",
        "phone": "138****8888",
        "rating": 4.9,
        "trips": 5234,
        "vehicle": {
            "plate_number": "京A·12345",
            "brand": "大众",
            "model": "帕萨特",
            "color": "黑色",
            "type": "COMFORT"
        }
    },
    {
        "driver_id": "DRV002",
        "name": "李师傅",
        "phone": "139****6666",
        "rating": 4.8,
        "trips": 3892,
        "vehicle": {
            "plate_number": "京A·67890",
            "brand": "别克",
            "model": "GL8",
            "color": "银色",
            "type": "BUSINESS"
        }
    },
    {
        "driver_id": "DRV003",
        "name": "王师傅",
        "phone": "137****5555",
        "rating": 4.9,
        "trips": 6123,
        "vehicle": {
            "plate_number": "京A·11111",
            "brand": "奥迪",
            "model": "A6L",
            "color": "黑色",
            "type": "LUXURY"
        }
    },
    {
        "driver_id": "DRV004",
        "name": "刘师傅",
        "phone": "136****4444",
        "rating": 4.7,
        "trips": 2156,
        "vehicle": {
            "plate_number": "京A·22222",
            "brand": "大众",
            "model": "朗逸",
            "color": "白色",
            "type": "ECONOMY"
        }
    }
]

# 机场信息
AIRPORTS_DB = {
    "北京首都国际机场": {
        "code": "PEK",
        "terminals": ["T1", "T2", "T3"],
        "address": "北京市顺义区机场西路"
    },
    "北京大兴国际机场": {
        "code": "PKX",
        "terminals": ["T1"],
        "address": "北京市大兴区机场大道"
    },
    "上海浦东国际机场": {
        "code": "PVG",
        "terminals": ["T1", "T2"],
        "address": "上海市浦东新区机场镇"
    },
    "上海虹桥国际机场": {
        "code": "SHA",
        "terminals": ["T1", "T2"],
        "address": "上海市长宁区虹桥路2550号"
    }
}


@dataclass
class Location:
    """位置信息"""
    address: str
    latitude: float = 0.0
    longitude: float = 0.0


@dataclass
class Driver:
    """司机信息"""
    driver_id: str
    name: str
    phone: str
    rating: float
    trips: int
    vehicle: Dict


@dataclass
class PriceEstimate:
    """价格预估"""
    min_price: float
    max_price: float
    base_fare: float
    mileage_fare: float
    time_fare: float
    currency: str = "CNY"


@dataclass
class RideOrder:
    """用车订单"""
    order_id: str
    order_status: str
    ride_type: str
    pickup: Location
    dropoff: Location
    car_type: str
    car_type_name: str
    estimated_price: PriceEstimate
    estimated_duration: int
    estimated_distance: float
    driver: Optional[Driver] = None
    create_time: str = ""
    scheduled_time: Optional[str] = None
    passenger_count: int = 1
    luggage_count: int = 0
    remarks: str = ""

    def to_dict(self) -> Dict:
        result = {
            "order_id": self.order_id,
            "order_status": self.order_status,
            "ride_type": self.ride_type,
            "pickup": {
                "location": self.pickup.address,
                "latitude": self.pickup.latitude,
                "longitude": self.pickup.longitude
            },
            "dropoff": {
                "location": self.dropoff.address,
                "latitude": self.dropoff.latitude,
                "longitude": self.dropoff.longitude
            },
            "car_type": self.car_type,
            "car_type_name": self.car_type_name,
            "estimated_price": {
                "min": self.estimated_price.min_price,
                "max": self.estimated_price.max_price,
                "currency": self.estimated_price.currency
            },
            "estimated_duration": self.estimated_duration,
            "estimated_distance": self.estimated_distance,
            "passenger_count": self.passenger_count,
            "luggage_count": self.luggage_count,
            "create_time": self.create_time
        }
        
        if self.driver:
            result["driver"] = {
                "driver_id": self.driver.driver_id,
                "name": self.driver.name,
                "phone": self.driver.phone,
                "rating": self.driver.rating,
                "vehicle": self.driver.vehicle
            }
        
        if self.scheduled_time:
            result["scheduled_time"] = self.scheduled_time
            
        return result


class CarServiceApi:
    """用车服务API"""
    
    def __init__(self):
        self.car_config = CAR_TYPE_CONFIG
        self.drivers = DRIVERS_DB
        self.airports = AIRPORTS_DB
        self.orders = {}  # 订单缓存
    
    def estimate_price(
        self,
        pickup_location: str,
        dropoff_location: str,
        car_type: str = None
    ) -> Dict:
        """
        费用预估
        """
        # 模拟计算距离和时间
        distance = self._calculate_distance(pickup_location, dropoff_location)
        duration = self._estimate_duration(distance)
        
        # 计算各车型价格
        price_estimates = {}
        for car_type_key, config in self.car_config.items():
            base_fare = config["base_fare"]
            mileage_fare = distance * config["mileage_rate"]
            time_fare = duration * config["time_rate"]
            
            # 添加浮动范围
            min_price = base_fare + mileage_fare + time_fare
            max_price = min_price * 1.2
            
            price_estimates[car_type_key] = {
                "min": round(min_price),
                "max": round(max_price),
                "base_fare": base_fare,
                "mileage_fare": round(mileage_fare, 1),
                "time_fare": round(time_fare, 1)
            }
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "pickup": pickup_location,
                "dropoff": dropoff_location,
                "distance": distance,
                "duration": duration,
                "price_estimate": price_estimates
            }
        }
    
    def _calculate_distance(self, pickup: str, dropoff: str) -> float:
        """计算距离（模拟）"""
        # 实际应该调用地图API
        # 这里使用随机值模拟
        return round(random.uniform(5, 50), 1)
    
    def _estimate_duration(self, distance: float) -> int:
        """预估时间（分钟）"""
        # 假设平均速度30km/h
        return int(distance * 2)
    
    def request_ride(
        self,
        pickup_location: str,
        dropoff_location: str,
        car_type: str = "COMFORT",
        passenger_count: int = 1,
        luggage_count: int = 0,
        remarks: str = ""
    ) -> Dict:
        """
        即时叫车
        """
        # 获取车型配置
        car_config = self.car_config.get(car_type.upper())
        if not car_config:
            return {
                "code": 400,
                "msg": f"不支持的车型: {car_type}",
                "data": None
            }
        
        # 计算距离和时间
        distance = self._calculate_distance(pickup_location, dropoff_location)
        duration = self._estimate_duration(distance)
        
        # 计算价格
        base_fare = car_config["base_fare"]
        mileage_fare = distance * car_config["mileage_rate"]
        time_fare = duration * car_config["time_rate"]
        min_price = base_fare + mileage_fare + time_fare
        max_price = min_price * 1.2
        
        # 分配司机
        driver = self._assign_driver(car_type)
        
        # 创建订单
        order_id = f"CAR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order = RideOrder(
            order_id=order_id,
            order_status="accepted",
            ride_type="immediate",
            pickup=Location(address=pickup_location),
            dropoff=Location(address=dropoff_location),
            car_type=car_type.upper(),
            car_type_name=car_config["name"],
            estimated_price=PriceEstimate(
                min_price=round(min_price),
                max_price=round(max_price),
                base_fare=base_fare,
                mileage_fare=mileage_fare,
                time_fare=time_fare
            ),
            estimated_duration=duration,
            estimated_distance=distance,
            driver=driver,
            create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            passenger_count=passenger_count,
            luggage_count=luggage_count,
            remarks=remarks
        )
        
        # 保存订单
        self.orders[order_id] = order
        
        return {
            "code": 0,
            "msg": "success",
            "data": order.to_dict()
        }
    
    def _assign_driver(self, car_type: str) -> Driver:
        """分配司机"""
        # 筛选符合车型的司机
        eligible_drivers = [d for d in self.drivers if d["vehicle"]["type"] == car_type.upper()]
        
        if not eligible_drivers:
            # 如果没有完全匹配的，随机选一个
            driver_data = random.choice(self.drivers)
        else:
            driver_data = random.choice(eligible_drivers)
        
        return Driver(
            driver_id=driver_data["driver_id"],
            name=driver_data["name"],
            phone=driver_data["phone"],
            rating=driver_data["rating"],
            trips=driver_data["trips"],
            vehicle=driver_data["vehicle"]
        )
    
    def schedule_ride(
        self,
        pickup_location: str,
        dropoff_location: str,
        scheduled_time: str,
        car_type: str = "COMFORT",
        passenger_count: int = 1,
        luggage_count: int = 0
    ) -> Dict:
        """
        预约用车
        """
        # 验证预约时间
        try:
            schedule_dt = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M")
            if schedule_dt < datetime.now():
                return {
                    "code": 400,
                    "msg": "预约时间不能早于当前时间",
                    "data": None
                }
        except ValueError:
            return {
                "code": 400,
                "msg": "预约时间格式错误，应为yyyy-MM-dd HH:mm",
                "data": None
            }
        
        # 获取车型配置
        car_config = self.car_config.get(car_type.upper())
        if not car_config:
            return {
                "code": 400,
                "msg": f"不支持的车型: {car_type}",
                "data": None
            }
        
        # 计算距离和时间
        distance = self._calculate_distance(pickup_location, dropoff_location)
        duration = self._estimate_duration(distance)
        
        # 计算价格
        base_fare = car_config["base_fare"]
        mileage_fare = distance * car_config["mileage_rate"]
        time_fare = duration * car_config["time_rate"]
        min_price = base_fare + mileage_fare + time_fare
        max_price = min_price * 1.2
        
        # 创建订单（预约订单暂不分配司机）
        order_id = f"CAR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order = RideOrder(
            order_id=order_id,
            order_status="pending",
            ride_type="scheduled",
            pickup=Location(address=pickup_location),
            dropoff=Location(address=dropoff_location),
            car_type=car_type.upper(),
            car_type_name=car_config["name"],
            estimated_price=PriceEstimate(
                min_price=round(min_price),
                max_price=round(max_price),
                base_fare=base_fare,
                mileage_fare=mileage_fare,
                time_fare=time_fare
            ),
            estimated_duration=duration,
            estimated_distance=distance,
            driver=None,
            create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            scheduled_time=scheduled_time,
            passenger_count=passenger_count,
            luggage_count=luggage_count
        )
        
        # 保存订单
        self.orders[order_id] = order
        
        return {
            "code": 0,
            "msg": "success",
            "data": order.to_dict()
        }
    
    def book_airport_transfer(
        self,
        service_type: str,
        airport: str,
        location: str,
        flight_number: str = None,
        flight_date: str = None,
        car_type: str = "COMFORT",
        passenger_count: int = 1,
        luggage_count: int = 0
    ) -> Dict:
        """
        接送机预订
        """
        # 验证机场
        if airport not in self.airports:
            return {
                "code": 400,
                "msg": f"不支持的机场: {airport}",
                "data": None
            }
        
        # 验证服务类型
        if service_type not in ["pickup", "dropoff"]:
            return {
                "code": 400,
                "msg": "服务类型必须是pickup（接机）或dropoff（送机）",
                "data": None
            }
        
        # 接机必须提供航班号
        if service_type == "pickup" and not flight_number:
            return {
                "code": 400,
                "msg": "接机服务必须提供航班号",
                "data": None
            }
        
        # 获取车型配置
        car_config = self.car_config.get(car_type.upper())
        
        # 接送机一口价（模拟）
        distance = self._calculate_distance(airport, location)
        if car_type.upper() == "ECONOMY":
            fixed_price = 150
        elif car_type.upper() == "COMFORT":
            fixed_price = 220
        elif car_type.upper() == "BUSINESS":
            fixed_price = 350
        else:
            fixed_price = 550
        
        # 创建订单
        order_id = f"CAR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        service_name = "接机" if service_type == "pickup" else "送机"
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "order_id": order_id,
                "order_status": "pending",
                "service_type": service_type,
                "service_name": service_name,
                "airport": airport,
                "flight_number": flight_number,
                "flight_date": flight_date,
                "location": location,
                "car_type": car_type.upper(),
                "car_type_name": car_config["name"] if car_config else car_type,
                "fixed_price": fixed_price,
                "currency": "CNY",
                "distance": distance,
                "includes": ["高速费", "停车费", "免费等待2小时"],
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    
    def get_order_detail(self, order_id: str) -> Dict:
        """
        获取订单详情
        """
        order = self.orders.get(order_id)
        if not order:
            return {
                "code": 404,
                "msg": f"订单不存在: {order_id}",
                "data": None
            }
        
        return {
            "code": 0,
            "msg": "success",
            "data": order.to_dict()
        }
    
    def cancel_order(self, order_id: str, reason: str = "") -> Dict:
        """
        取消订单
        """
        order = self.orders.get(order_id)
        if not order:
            return {
                "code": 404,
                "msg": f"订单不存在: {order_id}",
                "data": None
            }
        
        if order.order_status in ["completed", "cancelled"]:
            return {
                "code": 400,
                "msg": f"订单状态不允许取消: {order.order_status}",
                "data": None
            }
        
        order.order_status = "cancelled"
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "order_id": order_id,
                "status": "cancelled",
                "cancel_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reason": reason
            }
        }
    
    def format_order(self, result: Dict) -> str:
        """格式化订单信息"""
        data = result.get("data", {})
        
        if not data:
            return "订单信息获取失败"
        
        lines = []
        
        # 判断是接送机还是普通用车
        if "service_type" in data:
            # 接送机
            service_name = data.get("service_name", "")
            lines.append(f"✈️ {service_name}预约成功")
        else:
            # 普通用车
            ride_type = data.get("ride_type", "")
            if ride_type == "immediate":
                lines.append("🚗 即时叫车成功")
            else:
                lines.append("📅 预约用车成功")
        
        lines.append("")
        lines.append("=" * 40)
        lines.append("")
        
        # 行程信息
        lines.append("📍 行程信息")
        lines.append("━" * 40)
        
        if "pickup" in data:
            pickup = data["pickup"]
            dropoff = data["dropoff"]
            lines.append(f"🛫 上车地点：{pickup.get('location', '')}")
            lines.append(f"🛬 下车地点：{dropoff.get('location', '')}")
        elif "airport" in data:
            service_type = data.get("service_type", "")
            airport = data.get("airport", "")
            location = data.get("location", "")
            if service_type == "pickup":
                lines.append(f"🛬 接机机场：{airport}")
                lines.append(f"🏨 送达地址：{location}")
                flight = data.get("flight_number", "")
                if flight:
                    lines.append(f"✈️ 航班号：{flight}")
            else:
                lines.append(f"🏨 上车地址：{location}")
                lines.append(f"🛫 送达机场：{airport}")
        
        if "estimated_distance" in data:
            lines.append(f"📏 预估里程：{data['estimated_distance']}公里")
        if "estimated_duration" in data:
            lines.append(f"⏱️ 预估时间：{data['estimated_duration']}分钟")
        
        lines.append("")
        
        # 费用信息
        lines.append("💰 费用信息")
        lines.append("━" * 40)
        
        if "estimated_price" in data:
            price = data["estimated_price"]
            lines.append(f"预估费用：¥{price.get('min', 0)}-{price.get('max', 0)}")
        elif "fixed_price" in data:
            lines.append(f"一口价：¥{data['fixed_price']}")
            if "includes" in data:
                lines.append(f"包含：{'、'.join(data['includes'])}")
        
        lines.append("")
        
        # 司机信息
        if "driver" in data and data["driver"]:
            driver = data["driver"]
            lines.append("👤 司机信息")
            lines.append("━" * 40)
            
            vehicle = driver.get("vehicle", {})
            lines.append(f"🚗 车辆信息")
            lines.append(f"   车牌：{vehicle.get('plate_number', '')}")
            lines.append(f"   车型：{vehicle.get('brand', '')} {vehicle.get('model', '')}（{vehicle.get('color', '')}）")
            
            lines.append(f"\n👨‍✈️ 司机信息")
            lines.append(f"   姓名：{driver.get('name', '')}")
            lines.append(f"   评分：⭐ {driver.get('rating', 0)}")
            lines.append(f"   电话：{driver.get('phone', '')}")
            lines.append("")
        
        # 订单信息
        lines.append("📋 订单信息")
        lines.append("━" * 40)
        lines.append(f"订单号：{data.get('order_id', '')}")
        lines.append(f"状态：{self._format_status(data.get('order_status', ''))}")
        lines.append(f"创建时间：{data.get('create_time', '')}")
        
        if data.get('scheduled_time'):
            lines.append(f"预约时间：{data['scheduled_time']}")
        
        lines.append("")
        lines.append("=" * 40)
        
        return "\n".join(lines)
    
    def _format_status(self, status: str) -> str:
        """格式化状态"""
        status_map = {
            "pending": "🟡 待接单",
            "accepted": "🟢 已接单",
            "arriving": "🔵 司机前往中",
            "arrived": "🟣 司机已到达",
            "in_progress": "🟠 行程进行中",
            "completed": "✅ 已完成",
            "cancelled": "❌ 已取消"
        }
        return status_map.get(status, status)


# 测试
if __name__ == "__main__":
    api = CarServiceApi()
    
    # 测试费用预估
    print("=" * 60)
    print("测试费用预估")
    print("=" * 60)
    result = api.estimate_price(
        pickup_location="北京市朝阳区建国路88号",
        dropoff_location="北京首都国际机场T3航站楼"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 测试即时叫车
    print("\n" + "=" * 60)
    print("测试即时叫车")
    print("=" * 60)
    result = api.request_ride(
        pickup_location="北京市朝阳区建国路88号",
        dropoff_location="北京首都国际机场T3航站楼",
        car_type="COMFORT"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 格式化展示
    print("\n" + "=" * 60)
    print("格式化订单：")
    print("=" * 60)
    print(api.format_order(result))
