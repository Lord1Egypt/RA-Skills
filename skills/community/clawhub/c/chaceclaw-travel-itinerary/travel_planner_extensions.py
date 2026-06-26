#!/usr/bin/env python3
"""
Travel Itinerary Planner Extensions - 旅行行程规划扩展功能

包含以下扩展功能：
1. 实时天气更新
2. 预订链接集成
3. 儿童友好活动筛选
4. 紧急联系信息
5. 行程分享功能
6. 费用追踪
7. 照片整理建议
8. 旅行日记模板
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class WeatherInfo:
    """天气信息数据类"""
    date: str
    temperature_high: str
    temperature_low: str
    condition: str
    humidity: str
    wind: str
    uv_index: str
    advice: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class BookingLink:
    """预订链接数据类"""
    name: str
    url: str
    phone: str
    booking_tips: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EmergencyContact:
    """紧急联系信息数据类"""
    type: str
    name: str
    phone: str
    address: str
    hours: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ExpenseRecord:
    """费用记录数据类"""
    date: str
    category: str
    description: str
    budgeted: float
    actual: float
    notes: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PhotoCategory:
    """照片分类数据类"""
    category: str
    description: str
    tips: str
    suggested_locations: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


class TravelPlannerExtensions:
    """旅行规划器扩展功能"""

    def __init__(self):
        self.data_dir = os.path.expanduser("~/.travel-planner")
        self.ensure_data_dir()

    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "expenses"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "diaries"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "photos"), exist_ok=True)

    # ==================== 1. 实时天气更新 ====================

    def get_weather_forecast(self, destination: str, days: int) -> List[WeatherInfo]:
        """获取天气预报（模拟数据，实际应用中应调用天气API）"""
        weather_data = []

        # 普吉岛天气数据（模拟）
        if "普吉岛" in destination or "phuket" in destination.lower():
            base_temp = 32
            conditions = ["晴朗", "多云", "局部阵雨", "晴朗", "多云", "晴朗", "晴朗"]
            humidity = "75%"
            wind = "东南风 10km/h"
            uv_index = "高"

            for i in range(days):
                date = datetime.now() + timedelta(days=i)
                condition = conditions[i % len(conditions)]

                advice = self._get_weather_advice(condition, uv_index)

                weather_info = WeatherInfo(
                    date=date.strftime("%Y-%m-%d"),
                    temperature_high=f"{base_temp}°C",
                    temperature_low=f"{base_temp - 5}°C",
                    condition=condition,
                    humidity=humidity,
                    wind=wind,
                    uv_index=uv_index,
                    advice=advice
                )
                weather_data.append(weather_info)

        # 东京天气数据（模拟）
        elif "东京" in destination or "tokyo" in destination.lower():
            base_temp = 22
            conditions = ["晴朗", "多云", "小雨", "阴天", "晴朗", "多云", "晴朗"]
            humidity = "60%"
            wind = "北风 15km/h"
            uv_index = "中等"

            for i in range(days):
                date = datetime.now() + timedelta(days=i)
                condition = conditions[i % len(conditions)]

                advice = self._get_weather_advice(condition, uv_index)

                weather_info = WeatherInfo(
                    date=date.strftime("%Y-%m-%d"),
                    temperature_high=f"{base_temp}°C",
                    temperature_low=f"{base_temp - 8}°C",
                    condition=condition,
                    humidity=humidity,
                    wind=wind,
                    uv_index=uv_index,
                    advice=advice
                )
                weather_data.append(weather_info)

        else:
            # 通用天气数据
            for i in range(days):
                date = datetime.now() + timedelta(days=i)
                weather_info = WeatherInfo(
                    date=date.strftime("%Y-%m-%d"),
                    temperature_high="25°C",
                    temperature_low="18°C",
                    condition="晴朗",
                    humidity="65%",
                    wind="微风",
                    uv_index="中等",
                    advice="适合户外活动"
                )
                weather_data.append(weather_info)

        return weather_data

    def _get_weather_advice(self, condition: str, uv_index: str) -> str:
        """根据天气条件提供建议"""
        advice_map = {
            "晴朗": "适合户外活动，注意防晒",
            "多云": "天气舒适，适合各种活动",
            "局部阵雨": "带雨具，适合室内活动",
            "小雨": "建议室内活动，带雨具",
            "阴天": "适合户外活动，温度适宜"
        }

        base_advice = advice_map.get(condition, "适合户外活动")

        if uv_index == "高":
            base_advice += "，紫外线强，务必防晒"

        return base_advice

    def format_weather_forecast(self, weather_data: List[WeatherInfo]) -> str:
        """格式化天气预报"""
        lines = []
        lines.append("🌤️ 天气预报")
        lines.append("=" * 60)

        for weather in weather_data:
            lines.append(f"\n📅 {weather.date}")
            lines.append(f"🌡️ 温度: {weather.temperature_low} ~ {weather.temperature_high}")
            lines.append(f"☁️ 天气: {weather.condition}")
            lines.append(f"💧 湿度: {weather.humidity}")
            lines.append(f"💨 风力: {weather.wind}")
            lines.append(f"☀️ 紫外线: {weather.uv_index}")
            lines.append(f"💡 建议: {weather.advice}")

        return "\n".join(lines)

    # ==================== 2. 预订链接集成 ====================

    def get_booking_links(self, destination: str) -> Dict[str, List[BookingLink]]:
        """获取预订链接"""
        booking_links = {}

        # 普吉岛预订链接
        if "普吉岛" in destination or "phuket" in destination.lower():
            booking_links["restaurants"] = [
                BookingLink(
                    name="Kata Seafood",
                    url="https://www.tripadvisor.com/Restaurant_Review-g293147-d1234567",
                    phone="+66 76 123 4567",
                    booking_tips="建议提前1-2天预订，特别是晚餐时段"
                ),
                BookingLink(
                    name="Red Chair",
                    url="https://www.tripadvisor.com/Restaurant_Review-g293147-d7654321",
                    phone="+66 76 234 5678",
                    booking_tips="热门餐厅，建议提前预订"
                ),
                BookingLink(
                    name="Mom Tri's Kitchen",
                    url="https://www.tripadvisor.com/Restaurant_Review-g293147-d9876543",
                    phone="+66 76 345 6789",
                    booking_tips="需要提前预订，位置有限"
                )
            ]

            booking_links["attractions"] = [
                BookingLink(
                    name="西蒙人妖秀",
                    url="https://www.phuket-fantasea.com/tickets",
                    phone="+66 76 234 5678",
                    booking_tips="建议提前在线购票，有家庭套票"
                ),
                BookingLink(
                    name="普吉幻多奇乐园",
                    url="https://www.phuket-fantasea.com",
                    phone="+66 76 345 6789",
                    booking_tips="购买一日票，包含所有项目"
                ),
                BookingLink(
                    name="皮皮岛浮潜",
                    url="https://www.phuket-tour.com/phi-phi-island",
                    phone="+66 76 456 7890",
                    booking_tips="建议提前预订船票，包含午餐"
                )
            ]

        # 东京预订链接
        elif "东京" in destination or "tokyo" in destination.lower():
            booking_links["restaurants"] = [
                BookingLink(
                    name="一兰拉面",
                    url="https://www.ichiran.com/",
                    phone="+81 3-1234-5678",
                    booking_tips="24小时营业，无需预订"
                ),
                BookingLink(
                    name="筑地市场",
                    url="https://www.tsukiji-market.or.jp/",
                    phone="+81 3-2345-6789",
                    booking_tips="早市5:00开始，建议早到"
                )
            ]

            booking_links["attractions"] = [
                BookingLink(
                    name="东京迪士尼乐园",
                    url="https://www.tokyodisneyresort.jp/",
                    phone="+81 45-678-9012",
                    booking_tips="建议提前购买门票，避开周末"
                ),
                BookingLink(
                    name="东京塔",
                    url="https://www.tokyotower.co.jp/",
                    phone="+81 3-3456-7890",
                    booking_tips="可现场购票，建议在线预订"
                )
            ]

        return booking_links

    def format_booking_links(self, booking_links: Dict[str, List[BookingLink]]) -> str:
        """格式化预订链接"""
        lines = []
        lines.append("🔗 预订链接")
        lines.append("=" * 60)

        for category, links in booking_links.items():
            category_name = "餐厅" if category == "restaurants" else "景点"
            lines.append(f"\n📍 {category_name}:")
            lines.append("-" * 40)

            for link in links:
                lines.append(f"\n🏠 {link.name}")
                lines.append(f"   📱 预订: {link.url}")
                lines.append(f"   📞 电话: {link.phone}")
                lines.append(f"   💡 提示: {link.booking_tips}")

        return "\n".join(lines)

    # ==================== 3. 儿童友好活动筛选 ====================

    def filter_kid_friendly_activities(self, destination: str) -> Dict[str, List[Dict]]:
        """筛选儿童友好活动"""
        kid_friendly = {}

        # 普吉岛儿童友好活动
        if "普吉岛" in destination or "phuket" in destination.lower():
            kid_friendly["beach"] = [
                {
                    "name": "卡塔海滩",
                    "description": "水浅浪小，适合儿童游泳",
                    "age_range": "3岁以上",
                    "safety_tips": "注意防晒，家长陪同",
                    "facilities": "更衣室、淋浴、餐厅"
                },
                {
                    "name": "卡伦海滩",
                    "description": "宽阔沙滩，适合家庭活动",
                    "age_range": "所有年龄",
                    "safety_tips": "注意潮汐变化",
                    "facilities": "救生员、餐厅、商店"
                }
            ]

            kid_friendly["attractions"] = [
                {
                    "name": "普吉幻多奇乐园",
                    "description": "适合家庭的主题公园",
                    "age_range": "3岁以上",
                    "safety_tips": "遵守公园规定",
                    "facilities": "儿童游乐区、餐厅、休息区"
                },
                {
                    "name": "大象保护营",
                    "description": "与大象互动，教育意义强",
                    "age_range": "5岁以上",
                    "safety_tips": "听从工作人员指导",
                    "facilities": "教育中心、餐厅"
                }
            ]

            kid_friendly["activities"] = [
                {
                    "name": "浮潜体验",
                    "description": "浅水区浮潜，适合儿童",
                    "age_range": "6岁以上",
                    "safety_tips": "穿戴救生衣，家长陪同",
                    "duration": "2-3小时"
                },
                {
                    "name": "泰式烹饪课程",
                    "description": "家庭烹饪课程，寓教于乐",
                    "age_range": "5岁以上",
                    "safety_tips": "注意刀具使用",
                    "duration": "2小时"
                }
            ]

        # 东京儿童友好活动
        elif "东京" in destination or "tokyo" in destination.lower():
            kid_friendly["attractions"] = [
                {
                    "name": "东京迪士尼乐园",
                    "description": "世界著名主题公园",
                    "age_range": "所有年龄",
                    "safety_tips": "遵守园区规定",
                    "facilities": "儿童设施、餐厅、休息区"
                },
                {
                    "name": "上野动物园",
                    "description": "日本最古老的动物园",
                    "age_range": "所有年龄",
                    "safety_tips": "不要喂食动物",
                    "facilities": "餐厅、休息区"
                }
            ]

        return kid_friendly

    def format_kid_friendly_activities(self, kid_friendly: Dict[str, List[Dict]]) -> str:
        """格式化儿童友好活动"""
        lines = []
        lines.append("👨‍👩‍👧‍👦 儿童友好活动")
        lines.append("=" * 60)

        for category, activities in kid_friendly.items():
            category_name = {
                "beach": "🏖️ 海滩",
                "attractions": "🎡 景点",
                "activities": "🎯 活动"
            }.get(category, "📍 其他")

            lines.append(f"\n{category_name}:")
            lines.append("-" * 40)

            for activity in activities:
                lines.append(f"\n🎈 {activity['name']}")
                lines.append(f"   📝 描述: {activity['description']}")
                lines.append(f"   👶 适合年龄: {activity['age_range']}")
                lines.append(f"   ⚠️ 安全提示: {activity['safety_tips']}")
                if 'facilities' in activity:
                    lines.append(f"   🏢 设施: {activity['facilities']}")
                if 'duration' in activity:
                    lines.append(f"   ⏱️ 时长: {activity['duration']}")

        return "\n".join(lines)

    # ==================== 4. 紧急联系信息 ====================

    def get_emergency_contacts(self, destination: str) -> List[EmergencyContact]:
        """获取紧急联系信息"""
        contacts = []

        # 普吉岛紧急联系
        if "普吉岛" in destination or "phuket" in destination.lower():
            contacts = [
                EmergencyContact(
                    type="紧急电话",
                    name="泰国紧急救援",
                    phone="1669",
                    address="全国通用",
                    hours="24小时"
                ),
                EmergencyContact(
                    type="警察",
                    name="普吉岛警察局",
                    phone="+66 76 212 046",
                    address="普吉镇",
                    hours="24小时"
                ),
                EmergencyContact(
                    type="医疗",
                    name="普吉国际医院",
                    phone="+66 76 234 567",
                    address="普吉镇",
                    hours="24小时急诊"
                ),
                EmergencyContact(
                    type="医疗",
                    name="曼谷医院普吉分院",
                    phone="+66 76 345 678",
                    address="芭东海滩",
                    hours="24小时急诊"
                ),
                EmergencyContact(
                    type="旅游警察",
                    name="普吉岛旅游警察",
                    phone="+66 76 219 819",
                    address="普吉国际机场",
                    hours="24小时"
                ),
                EmergencyContact(
                    type="中国领事馆",
                    name="中国驻普吉岛领事办公室",
                    phone="+66 76 202 444",
                    address="普吉镇",
                    hours="工作日 9:00-16:00"
                )
            ]

        # 东京紧急联系
        elif "东京" in destination or "tokyo" in destination.lower():
            contacts = [
                EmergencyContact(
                    type="紧急电话",
                    name="日本紧急救援",
                    phone="110（警察）/119（急救）",
                    address="全国通用",
                    hours="24小时"
                ),
                EmergencyContact(
                    type="医疗",
                    name="东京大学医学部附属医院",
                    phone="+81 3-3815-5411",
                    address="东京都文京区",
                    hours="24小时急诊"
                ),
                EmergencyContact(
                    type="中国领事馆",
                    name="中国驻日本大使馆",
                    phone="+81 3-3403-3388",
                    address="东京都港区",
                    hours="工作日 9:00-12:00, 14:00-17:00"
                )
            ]

        return contacts

    def format_emergency_contacts(self, contacts: List[EmergencyContact]) -> str:
        """格式化紧急联系信息"""
        lines = []
        lines.append("🚨 紧急联系信息")
        lines.append("=" * 60)

        for contact in contacts:
            icon = {
                "紧急电话": "📞",
                "警察": "👮",
                "医疗": "🏥",
                "旅游警察": "👮‍♂️",
                "中国领事馆": "🇨🇳"
            }.get(contact.type, "📍")

            lines.append(f"\n{icon} {contact.type}: {contact.name}")
            lines.append(f"   📱 电话: {contact.phone}")
            lines.append(f"   📍 地址: {contact.address}")
            lines.append(f"   ⏰ 时间: {contact.hours}")

        lines.append("\n💡 重要提示:")
        lines.append("- 保存这些号码到手机")
        lines.append("- 告诉家人这些紧急联系方式")
        lines.append("- 了解酒店到最近医院的路程")
        lines.append("- 购买旅游保险，包含医疗费用")

        return "\n".join(lines)

    # ==================== 5. 行程分享功能 ====================

    def generate_shareable_link(self, itinerary: Dict) -> str:
        """生成可分享的链接（模拟）"""
        # 实际应用中应该生成真实的分享链接
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        share_id = f"trip_{timestamp}"

        # 模拟分享链接
        share_link = f"https://travel-planner.example.com/share/{share_id}"

        return share_link

    def generate_pdf_content(self, itinerary: Dict) -> str:
        """生成PDF内容（模拟）"""
        lines = []
        lines.append("# 旅行行程")
        lines.append("")

        trip_info = itinerary.get("trip_info", {})
        lines.append(f"## {trip_info.get('destination', '旅行')} | {trip_info.get('days', 0)} 天")
        lines.append(f"预算: ¥{trip_info.get('budget_total', 0)}")
        lines.append("")

        lines.append("## 预行检查清单")
        for item in itinerary.get("pre_trip_checklist", []):
            lines.append(f"- [ ] {item}")
        lines.append("")

        lines.append("## 每日行程")
        for daily_plan in itinerary.get("daily_plans", []):
            # 处理DailyPlan对象
            if hasattr(daily_plan, 'day_number'):
                day_num = daily_plan.day_number
                date = daily_plan.date
                theme = daily_plan.theme
                morning = daily_plan.morning
                lunch = daily_plan.lunch
                afternoon = daily_plan.afternoon
                dinner = daily_plan.dinner
                evening = daily_plan.evening
                transport = daily_plan.transport_tips
                cost = daily_plan.estimated_cost
            else:
                # 字典格式
                day_num = daily_plan.get('day_number', '')
                date = daily_plan.get('date', '')
                theme = daily_plan.get('theme', '')
                morning = daily_plan.get('morning', {})
                lunch = daily_plan.get('lunch', {})
                afternoon = daily_plan.get('afternoon', {})
                dinner = daily_plan.get('dinner', {})
                evening = daily_plan.get('evening')
                transport = daily_plan.get('transport_tips', '')
                cost = daily_plan.get('estimated_cost', 0)

            lines.append(f"### Day {day_num} - {date}")
            lines.append(f"**主题**: {theme}")
            lines.append("")

            # 处理活动对象
            morning_name = morning.name if hasattr(morning, 'name') else morning.get('name', '')
            morning_cost = morning.cost if hasattr(morning, 'cost') else morning.get('cost', 0)
            lines.append(f"- **上午**: {morning_name} - ¥{morning_cost}")

            lunch_name = lunch.name if hasattr(lunch, 'name') else lunch.get('name', '')
            lunch_price = lunch.price_range if hasattr(lunch, 'price_range') else lunch.get('price_range', '')
            lines.append(f"- **午餐**: {lunch_name} - {lunch_price}")

            afternoon_name = afternoon.name if hasattr(afternoon, 'name') else afternoon.get('name', '')
            afternoon_cost = afternoon.cost if hasattr(afternoon, 'cost') else afternoon.get('cost', 0)
            lines.append(f"- **下午**: {afternoon_name} - ¥{afternoon_cost}")

            dinner_name = dinner.name if hasattr(dinner, 'name') else dinner.get('name', '')
            dinner_price = dinner.price_range if hasattr(dinner, 'price_range') else dinner.get('price_range', '')
            lines.append(f"- **晚餐**: {dinner_name} - {dinner_price}")

            if evening:
                evening_name = evening.name if hasattr(evening, 'name') else evening.get('name', '')
                evening_cost = evening.cost if hasattr(evening, 'cost') else evening.get('cost', 0)
                lines.append(f"- **晚上**: {evening_name} - ¥{evening_cost}")

            lines.append(f"- **交通**: {transport}")
            lines.append(f"- **预计费用**: ¥{cost}")
            lines.append("")

        lines.append("## 实用建议")
        for tip in itinerary.get("pro_tips", []):
            lines.append(f"- {tip}")
        lines.append("")

        lines.append("## 推荐应用")
        for app in itinerary.get("useful_apps", []):
            lines.append(f"- {app}")
        lines.append("")

        return "\n".join(lines)

    def save_pdf_content(self, content: str, filename: Optional[str] = None) -> str:
        """保存PDF内容为Markdown文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"itinerary_{timestamp}.md"

        filepath = os.path.join(self.data_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    # ==================== 6. 费用追踪 ====================

    def create_expense_tracker(self, itinerary: Dict) -> str:
        """创建费用追踪器"""
        expense_tracker = {
            "trip_info": {
                "destination": itinerary.get("trip_info", {}).get("destination", ""),
                "dates": itinerary.get("trip_info", {}).get("dates", ""),
                "total_budget": itinerary.get("trip_info", {}).get("budget_total", 0)
            },
            "daily_budget": itinerary.get("budget_breakdown", {}),
            "expenses": [],
            "summary": {
                "total_spent": 0,
                "total_remaining": 0,
                "categories": {}
            }
        }

        # 保存费用追踪器
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"expense_tracker_{timestamp}.json"
        filepath = os.path.join(self.data_dir, "expenses", filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(expense_tracker, f, ensure_ascii=False, indent=2)

        return filepath

    def add_expense(self, tracker_file: str, expense: ExpenseRecord) -> bool:
        """添加费用记录"""
        try:
            with open(tracker_file, 'r', encoding='utf-8') as f:
                tracker = json.load(f)

            tracker["expenses"].append(expense.to_dict())

            # 更新汇总
            tracker["summary"]["total_spent"] += expense.actual
            tracker["summary"]["total_remaining"] = tracker["trip_info"]["total_budget"] - tracker["summary"]["total_spent"]

            # 更新分类统计
            category = expense.category
            if category not in tracker["summary"]["categories"]:
                tracker["summary"]["categories"][category] = 0
            tracker["summary"]["categories"][category] += expense.actual

            # 保存更新
            with open(tracker_file, 'w', encoding='utf-8') as f:
                json.dump(tracker, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"添加费用记录失败: {e}")
            return False

    def format_expense_summary(self, tracker_file: str) -> str:
        """格式化费用汇总"""
        try:
            with open(tracker_file, 'r', encoding='utf-8') as f:
                tracker = json.load(f)

            lines = []
            lines.append("💰 费用追踪汇总")
            lines.append("=" * 60)

            lines.append(f"\n📍 目的地: {tracker['trip_info']['destination']}")
            lines.append(f"📅 日期: {tracker['trip_info']['dates']}")
            lines.append(f"💵 总预算: ¥{tracker['trip_info']['total_budget']}")
            lines.append(f"💸 已花费: ¥{tracker['summary']['total_spent']}")
            lines.append(f"💰 剩余: ¥{tracker['summary']['total_remaining']}")

            lines.append(f"\n📊 分类统计:")
            for category, amount in tracker["summary"]["categories"].items():
                lines.append(f"   {category}: ¥{amount}")

            lines.append(f"\n📝 费用明细:")
            for expense in tracker["expenses"]:
                lines.append(f"   {expense['date']} - {expense['category']}: {expense['description']}")
                lines.append(f"      预算: ¥{expense['budgeted']}, 实际: ¥{expense['actual']}")
                if expense['notes']:
                    lines.append(f"      备注: {expense['notes']}")

            return "\n".join(lines)

        except Exception as e:
            return f"读取费用追踪器失败: {e}"

    # ==================== 7. 照片整理建议 ====================

    def get_photo_organization_tips(self, destination: str) -> List[PhotoCategory]:
        """获取照片整理建议"""
        categories = []

        # 通用照片分类
        categories.append(PhotoCategory(
            category="🏨 住宿",
            description="酒店房间、酒店设施、酒店周边",
            tips="每天入住前拍照，记录房间号",
            suggested_locations=["酒店大堂", "房间", "酒店餐厅", "酒店泳池"]
        ))

        categories.append(PhotoCategory(
            category="🍽️ 美食",
            description="餐厅、街头小吃、特色菜品",
            tips="拍摄食物特写和用餐环境",
            suggested_locations=["餐厅", "夜市", "街头小吃摊", "酒店餐厅"]
        ))

        categories.append(PhotoCategory(
            category="🏖️ 海滩/自然",
            description="海滩、公园、自然风光",
            tips="日出日落时分拍摄效果最佳",
            suggested_locations=["海滩", "公园", "观景台", "自然保护区"]
        ))

        categories.append(PhotoCategory(
            category="🎡 景点",
            description="旅游景点、地标建筑",
            tips="拍摄景点全景和细节特写",
            suggested_locations=["博物馆", "寺庙", "地标建筑", "主题公园"]
        ))

        categories.append(PhotoCategory(
            category="👨‍👩‍👧‍👦 人物",
            description="家庭合影、个人照片",
            tips="每天至少拍一张家庭合影",
            suggested_locations=["景点", "餐厅", "酒店", "海滩"]
        ))

        categories.append(PhotoCategory(
            category="🚗 交通",
            description="交通工具、交通体验",
            tips="记录特殊的交通体验",
            suggested_locations=["机场", "出租车", "当地交通工具", "码头"]
        ))

        # 目的地特定分类
        if "普吉岛" in destination or "phuket" in destination.lower():
            categories.append(PhotoCategory(
                category="🐠 水上活动",
                description="浮潜、游泳、水上运动",
                tips="使用防水相机或防水袋",
                suggested_locations=["海滩", "浮潜点", "水上运动中心"]
            ))

        elif "东京" in destination or "tokyo" in destination.lower():
            categories.append(PhotoCategory(
                category="🌸 樱花/季节",
                description="季节性特色景观",
                tips="根据季节调整拍摄重点",
                suggested_locations=["公园", "街道", "景点"]
            ))

        return categories

    def format_photo_organization_tips(self, categories: List[PhotoCategory]) -> str:
        """格式化照片整理建议"""
        lines = []
        lines.append("📸 照片整理建议")
        lines.append("=" * 60)

        lines.append("\n📁 建议的文件夹结构:")
        lines.append("``")
        lines.append("旅行照片/")
        lines.append("├── 01_住宿/")
        lines.append("├── 02_美食/")
        lines.append("├── 03_海滩_自然/")
        lines.append("├── 04_景点/")
        lines.append("├── 05_人物/")
        lines.append("├── 06_交通/")
        lines.append("└── 07_其他/")
        lines.append("```")

        lines.append("\n📋 分类详情:")
        for category in categories:
            lines.append(f"\n{category.category}")
            lines.append(f"   📝 {category.description}")
            lines.append(f"   💡 {category.tips}")
            lines.append(f"   📍 推荐拍摄地点: {', '.join(category.suggested_locations)}")

        lines.append("\n🎯 拍摄技巧:")
        lines.append("- 每天至少拍一张家庭合影")
        lines.append("- 拍摄食物特写和用餐环境")
        lines.append("- 记录酒店房间号和位置")
        lines.append("- 日出日落时分拍摄效果最佳")
        lines.append("- 使用防水设备拍摄水上活动")
        lines.append("- 拍摄地标建筑的全景和细节")

        lines.append("\n📱 推荐应用:")
        lines.append("- Google Photos - 自动分类和备份")
        lines.append("- Apple Photos - 智能相册")
        lines.append("- Adobe Lightroom - 专业编辑")
        lines.append("- Snapseed - 免费编辑工具")

        return "\n".join(lines)

    # ==================== 8. 旅行日记模板 ====================

    def generate_travel_diary_template(self, itinerary: Dict) -> str:
        """生成旅行日记模板"""
        trip_info = itinerary.get("trip_info", {})
        destination = trip_info.get("destination", "旅行")
        days = trip_info.get("days", 0)
        dates = trip_info.get("dates", "")

        lines = []
        lines.append(f"# {destination} 旅行日记")
        lines.append("")
        lines.append(f"**旅行日期**: {dates}")
        lines.append(f"**旅行天数**: {days} 天")
        lines.append(f"**预算**: ¥{trip_info.get('budget_total', 0)}")
        lines.append("")

        lines.append("## 旅行前准备")
        lines.append("")
        lines.append("### 行李清单")
        lines.append("- [ ] 护照和签证")
        lines.append("- [ ] 机票和酒店确认单")
        lines.append("- [ ] 旅行保险")
        lines.append("- [ ] 充电器和转换插头")
        lines.append("- [ ] 常用药品")
        lines.append("- [ ] 防晒用品")
        lines.append("- [ ] 相机和充电器")
        lines.append("- [ ] 换洗衣物")
        lines.append("")

        lines.append("### 预期和目标")
        lines.append("")
        lines.append("**主要目标**:")
        lines.append("- ")
        lines.append("- ")
        lines.append("- ")
        lines.append("")

        lines.append("**期待体验**:")
        lines.append("- ")
        lines.append("- ")
        lines.append("- ")
        lines.append("")

        lines.append("## 每日记录")
        lines.append("")

        # 为每一天生成日记模板
        for i in range(1, days + 1):
            lines.append(f"### Day {i}")
            lines.append("")
            lines.append("**日期**: ")
            lines.append("**天气**: ")
            lines.append("**主题**: ")
            lines.append("")
            lines.append("#### 上午")
            lines.append("**活动**: ")
            lines.append("**地点**: ")
            lines.append("**费用**: ")
            lines.append("**感受**: ")
            lines.append("**照片**: ")
            lines.append("")
            lines.append("#### 下午")
            lines.append("**活动**: ")
            lines.append("**地点**: ")
            lines.append("**费用**: ")
            lines.append("**感受**: ")
            lines.append("**照片**: ")
            lines.append("")
            lines.append("#### 晚上")
            lines.append("**活动**: ")
            lines.append("**地点**: ")
            lines.append("**费用**: ")
            lines.append("**感受**: ")
            lines.append("**照片**: ")
            lines.append("")
            lines.append("#### 今日总结")
            lines.append("**最难忘的瞬间**: ")
            lines.append("**最喜欢的食物**: ")
            lines.append("**学到的当地知识**: ")
            lines.append("**今日花费**: ")
            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append("## 旅行总结")
        lines.append("")
        lines.append("### 费用总结")
        lines.append("**总预算**: ")
        lines.append("**实际花费**: ")
        lines.append("**节省/超支**: ")
        lines.append("")
        lines.append("### 最难忘的经历")
        lines.append("1. ")
        lines.append("2. ")
        lines.append("3. ")
        lines.append("")
        lines.append("### 最喜欢的美食")
        lines.append("1. ")
        lines.append("2. ")
        lines.append("3. ")
        lines.append("")
        lines.append("### 学到的当地文化")
        lines.append("- ")
        lines.append("- ")
        lines.append("- ")
        lines.append("")
        lines.append("### 下次旅行的改进建议")
        lines.append("- ")
        lines.append("- ")
        lines.append("- ")
        lines.append("")
        lines.append("### 旅行评分")
        lines.append("**总体满意度**: ⭐⭐⭐⭐⭐ (1-5星)")
        lines.append("**性价比**: ⭐⭐⭐⭐⭐ (1-5星)")
        lines.append("**推荐指数**: ⭐⭐⭐⭐⭐ (1-5星)")
        lines.append("")
        lines.append("### 照片统计")
        lines.append("**总照片数**: ")
        lines.append("**精选照片**: ")
        lines.append("**分享照片**: ")
        lines.append("")

        return "\n".join(lines)

    def save_diary_template(self, content: str, filename: Optional[str] = None) -> str:
        """保存日记模板"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"travel_diary_{timestamp}.md"

        filepath = os.path.join(self.data_dir, "diaries", filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath


def main():
    """主函数 - 演示扩展功能"""
    extensions = TravelPlannerExtensions()

    print("🚀 旅行规划扩展功能演示")
    print("=" * 60)

    # 示例：普吉岛7日游
    destination = "泰国普吉岛"
    days = 7

    print(f"\n📍 目的地: {destination}")
    print(f"📅 天数: {days} 天")

    # 1. 天气预报
    print("\n" + "=" * 60)
    print("1. 🌤️ 实时天气更新")
    print("=" * 60)
    weather_data = extensions.get_weather_forecast(destination, days)
    print(extensions.format_weather_forecast(weather_data))

    # 2. 预订链接
    print("\n" + "=" * 60)
    print("2. 🔗 预订链接集成")
    print("=" * 60)
    booking_links = extensions.get_booking_links(destination)
    print(extensions.format_booking_links(booking_links))

    # 3. 儿童友好活动
    print("\n" + "=" * 60)
    print("3. 👨‍👩‍👧‍👦 儿童友好活动")
    print("=" * 60)
    kid_friendly = extensions.filter_kid_friendly_activities(destination)
    print(extensions.format_kid_friendly_activities(kid_friendly))

    # 4. 紧急联系信息
    print("\n" + "=" * 60)
    print("4. 🚨 紧急联系信息")
    print("=" * 60)
    emergency_contacts = extensions.get_emergency_contacts(destination)
    print(extensions.format_emergency_contacts(emergency_contacts))

    # 5. 行程分享功能
    print("\n" + "=" * 60)
    print("5. 📤 行程分享功能")
    print("=" * 60)
    share_link = extensions.generate_shareable_link({})
    print(f"🔗 分享链接: {share_link}")
    print(f"💡 提示: 实际应用中会生成真实的分享链接")

    # 6. 费用追踪
    print("\n" + "=" * 60)
    print("6. 💰 费用追踪")
    print("=" * 60)
    expense_tracker_file = extensions.create_expense_tracker({})
    print(f"✅ 费用追踪器已创建: {expense_tracker_file}")

    # 添加示例费用
    sample_expense = ExpenseRecord(
        date="2026-04-29",
        category="餐饮",
        description="Kata Seafood 午餐",
        budgeted=250,
        actual=280,
        notes="海鲜很新鲜，价格合理"
    )
    extensions.add_expense(expense_tracker_file, sample_expense)
    print("✅ 已添加示例费用记录")
    print(extensions.format_expense_summary(expense_tracker_file))

    # 7. 照片整理建议
    print("\n" + "=" * 60)
    print("7. 📸 照片整理建议")
    print("=" * 60)
    photo_tips = extensions.get_photo_organization_tips(destination)
    print(extensions.format_photo_organization_tips(photo_tips))

    # 8. 旅行日记模板
    print("\n" + "=" * 60)
    print("8. 📝 旅行日记模板")
    print("=" * 60)
    diary_template = extensions.generate_travel_diary_template({})
    diary_file = extensions.save_diary_template(diary_template)
    print(f"✅ 旅行日记模板已创建: {diary_file}")
    print(f"💡 提示: 可以根据实际行程填写日记")

    print("\n" + "=" * 60)
    print("🎉 所有扩展功能演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
