#!/usr/bin/env python3
"""
Travel Itinerary Planner - 智能旅行行程规划系统

核心功能：
1. 信息收集和验证
2. 智能行程规划
3. 预算计算和分配
4. 实用建议生成
5. 行程格式化输出
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import re


@dataclass
class TravelInfo:
    """旅行信息数据类"""
    destination: str
    dates: str
    days: int
    budget_total: float
    budget_daily: float
    travelers: str
    interests: List[str]
    style: str
    must_see: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Activity:
    """活动数据类"""
    name: str
    duration: str
    cost: float
    tips: str
    time_of_day: str  # morning, afternoon, evening

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Restaurant:
    """餐厅数据类"""
    name: str
    cuisine: str
    price_range: str
    must_try: str
    location: str
    price_range_numeric: float = 0  # 添加数值属性

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DailyPlan:
    """每日行程数据类"""
    day_number: int
    date: str
    theme: str
    morning: Activity
    lunch: Restaurant
    afternoon: Activity
    dinner: Restaurant
    evening: Optional[Activity]
    transport_tips: str
    estimated_cost: float

    def to_dict(self) -> Dict:
        return asdict(self)


class TravelItineraryPlanner:
    """旅行行程规划器"""

    def __init__(self):
        self.data_dir = os.path.expanduser("~/.travel-planner")
        self.ensure_data_dir()

        # 旅行风格预算分配模型
        self.style_multipliers = {
            "backpacker": {
                "accommodation": 0.25,
                "food": 0.35,
                "transport": 0.20,
                "activities": 0.15,
                "misc": 0.05
            },
            "mid-range": {
                "accommodation": 0.35,
                "food": 0.30,
                "transport": 0.15,
                "activities": 0.15,
                "misc": 0.05
            },
            "luxury": {
                "accommodation": 0.50,
                "food": 0.25,
                "transport": 0.10,
                "activities": 0.10,
                "misc": 0.05
            }
        }

        # 兴趣推荐映射
        self.interest_recommendations = {
            "美食": {
                "activities": ["美食市场", "烹饪课程", "当地特色餐厅"],
                "restaurants": ["街头小吃", "米其林推荐", "当地特色"]
            },
            "历史": {
                "activities": ["博物馆", "历史遗迹", "文化遗址"],
                "restaurants": ["传统餐厅", "历史建筑内的餐厅"]
            },
            "自然": {
                "activities": ["公园", "海滩", "徒步路线"],
                "restaurants": ["露营餐厅", "景观餐厅"]
            },
            "夜生活": {
                "activities": ["酒吧", "夜市", "演出"],
                "restaurants": ["深夜餐厅", "24小时餐厅"]
            },
            "购物": {
                "activities": ["购物区", "市场", "精品店"],
                "restaurants": ["购物中心餐厅", "市场美食"]
            },
            "冒险": {
                "activities": ["极限运动", "户外活动"],
                "restaurants": ["能量补充站", "当地特色"]
            }
        }

    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "destinations"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "templates"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "budgets"), exist_ok=True)

    def collect_travel_info(self, user_input: str) -> TravelInfo:
        """从用户输入中收集旅行信息"""
        # 解析用户输入
        info = self.parse_user_input(user_input)

        # 验证信息完整性
        self.validate_travel_info(info)

        return info

    def parse_user_input(self, user_input: str) -> TravelInfo:
        """解析用户输入"""
        # 简单解析逻辑（实际应用中可以使用更复杂的NLP）
        destination = self.extract_destination(user_input)
        days = self.extract_days(user_input)
        budget = self.extract_budget(user_input)
        travelers = self.extract_travelers(user_input)
        interests = self.extract_interests(user_input)
        style = self.extract_style(user_input)

        # 计算每日预算
        budget_daily = budget / days if days > 0 else 0

        # 生成日期范围（简化版）
        start_date = datetime.now() + timedelta(days=7)  # 默认7天后出发
        end_date = start_date + timedelta(days=days)
        dates = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"

        return TravelInfo(
            destination=destination,
            dates=dates,
            days=days,
            budget_total=budget,
            budget_daily=budget_daily,
            travelers=travelers,
            interests=interests,
            style=style,
            must_see=[]
        )

    def extract_destination(self, text: str) -> str:
        """提取目的地"""
        # 简化版：查找"去"、"到"、"travel to"等关键词后的地点
        patterns = [
            r'去(.+?)的旅行',
            r'去(.+?)\d+天',
            r'to (.+?) for',
            r'去(.+?)，'
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        return "未知目的地"

    def extract_days(self, text: str) -> int:
        """提取天数"""
        patterns = [
            r'(\d+)天',
            r'(\d+) days',
            r'(\d+) day'
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))

        return 5  # 默认5天

    def extract_budget(self, text: str) -> float:
        """提取预算"""
        patterns = [
            r'预算(\d+)元',
            r'预算(\d+)',
            r'budget.*?(\d+)',
            r'(\d+)元'
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))

        return 10000  # 默认10000元

    def extract_travelers(self, text: str) -> str:
        """提取旅行者类型"""
        if "情侣" in text or "couple" in text.lower():
            return "couple"
        elif "家庭" in text or "family" in text.lower():
            return "family"
        elif "团队" in text or "group" in text.lower():
            return "group"
        else:
            return "solo"

    def extract_interests(self, text: str) -> List[str]:
        """提取兴趣"""
        interests = []
        interest_keywords = {
            "美食": ["美食", "food", "吃", "餐厅"],
            "历史": ["历史", "history", "文化", "culture"],
            "自然": ["自然", "nature", "海滩", "beach", "公园"],
            "夜生活": ["夜生活", "nightlife", "酒吧", "bar"],
            "购物": ["购物", "shopping", "买"],
            "冒险": ["冒险", "adventure", "运动"]
        }

        for interest, keywords in interest_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    interests.append(interest)
                    break

        return interests if interests else ["美食", "历史"]  # 默认兴趣

    def extract_style(self, text: str) -> str:
        """提取旅行风格"""
        if "背包客" in text or "backpacker" in text.lower():
            return "backpacker"
        elif "奢华" in text or "luxury" in text.lower():
            return "luxury"
        else:
            return "mid-range"  # 默认中档

    def validate_travel_info(self, info: TravelInfo):
        """验证旅行信息完整性"""
        if not info.destination or info.destination == "未知目的地":
            raise ValueError("请提供目的地信息")

        if info.days <= 0:
            raise ValueError("旅行天数必须大于0")

        if info.budget_total <= 0:
            raise ValueError("预算必须大于0")

        if info.style not in self.style_multipliers:
            raise ValueError(f"不支持的旅行风格: {info.style}")

    def calculate_budget_breakdown(self, info: TravelInfo) -> Dict:
        """计算预算分配"""
        breakdown = self.style_multipliers[info.style]

        return {
            "daily": info.budget_daily,
            "accommodation": info.budget_daily * breakdown["accommodation"],
            "food": info.budget_daily * breakdown["food"],
            "transport": info.budget_daily * breakdown["transport"],
            "activities": info.budget_daily * breakdown["activities"],
            "misc": info.budget_daily * breakdown["misc"]
        }

    def generate_daily_themes(self, days: int, interests: List[str]) -> List[str]:
        """生成每日主题"""
        themes = []

        # 基于兴趣生成主题
        interest_themes = {
            "美食": ["美食探索", "当地特色", "烹饪体验", "夜市美食"],
            "历史": ["历史文化", "古迹探访", "博物馆之旅", "文化体验"],
            "自然": ["自然风光", "海滩休闲", "公园漫步", "户外探险"],
            "夜生活": ["夜生活体验", "酒吧巡游", "夜市探索", "文化演出"],
            "购物": ["购物天堂", "市场探索", "精品店巡礼", "纪念品购物"],
            "冒险": ["户外冒险", "极限运动", "自然探索", "水上运动"]
        }

        # 第一天和最后一天固定主题
        if days >= 1:
            themes.append("抵达与安顿")
        if days >= 2:
            themes.append("海滩休闲")

        # 中间天数根据兴趣循环
        for i in range(2, days - 1):
            if interests:
                interest = interests[i % len(interests)]
                theme_options = interest_themes.get(interest, ["城市探索"])
                themes.append(theme_options[i % len(theme_options)])
            else:
                themes.append("城市探索")

        # 最后一天主题
        if days >= 3:
            themes.append("告别与纪念品购物")

        return themes

    def create_itinerary(self, info: TravelInfo) -> Dict:
        """创建完整行程"""
        # 计算预算分配
        budget_breakdown = self.calculate_budget_breakdown(info)

        # 生成每日主题
        daily_themes = self.generate_daily_themes(info.days, info.interests)

        # 生成每日行程
        daily_plans = []
        for day in range(1, info.days + 1):
            theme = daily_themes[day - 1] if day <= len(daily_themes) else "城市探索"
            daily_plan = self.create_daily_plan(day, info, theme, budget_breakdown)
            daily_plans.append(daily_plan)

        # 生成预行检查清单
        pre_trip_checklist = self.generate_pre_trip_checklist(info)

        # 生成实用建议
        pro_tips = self.generate_pro_tips(info)

        # 生成推荐应用
        useful_apps = self.generate_useful_apps(info)

        return {
            "trip_info": {
                "destination": info.destination,
                "dates": info.dates,
                "days": info.days,
                "budget_total": info.budget_total,
                "budget_daily": info.budget_daily,
                "travelers": info.travelers
            },
            "pre_trip_checklist": pre_trip_checklist,
            "daily_plans": daily_plans,
            "pro_tips": pro_tips,
            "useful_apps": useful_apps,
            "budget_breakdown": budget_breakdown
        }

    def create_daily_plan(self, day_number: int, info: TravelInfo, theme: str, budget_breakdown: Dict) -> DailyPlan:
        """创建每日行程"""
        # 生成日期
        start_date = datetime.strptime(info.dates.split(" to ")[0], "%Y-%m-%d")
        current_date = start_date + timedelta(days=day_number - 1)
        date_str = current_date.strftime("%Y-%m-%d")

        # 生成活动（简化版，实际应用中应该调用web_search等技能）
        morning_activity = self.generate_activity("morning", theme, info)
        lunch_restaurant = self.generate_restaurant("lunch", info)
        afternoon_activity = self.generate_activity("afternoon", theme, info)
        dinner_restaurant = self.generate_restaurant("dinner", info)
        evening_activity = self.generate_activity("evening", theme, info) if day_number < info.days else None

        # 计算每日成本
        daily_cost = (
            morning_activity.cost +
            lunch_restaurant.price_range_numeric +
            afternoon_activity.cost +
            dinner_restaurant.price_range_numeric +
            (evening_activity.cost if evening_activity else 0)
        )

        # 交通建议
        transport_tips = self.generate_transport_tips(info)

        return DailyPlan(
            day_number=day_number,
            date=date_str,
            theme=theme,
            morning=morning_activity,
            lunch=lunch_restaurant,
            afternoon=afternoon_activity,
            dinner=dinner_restaurant,
            evening=evening_activity,
            transport_tips=transport_tips,
            estimated_cost=daily_cost
        )

    def generate_activity(self, time_of_day: str, theme: str, info: TravelInfo) -> Activity:
        """生成活动"""
        # 普吉岛特色活动
        phuket_activities = {
            "morning": {
                "抵达与安顿": Activity("普吉岛机场接机", "1.5小时", 300, "建议提前预订酒店接送", "morning"),
                "海滩休闲": Activity("海滩日出", "1.5小时", 0, "全家一起看日出", "morning"),
                "烹饪体验": Activity("泰式烹饪课程", "3小时", 500, "学习制作冬阴功汤和泰式炒河粉", "morning"),
                "户外探险": Activity("普吉老镇漫步", "2小时", 0, "感受中葡式建筑", "morning"),
                "美食探索": Activity("查龙寺参观", "1.5小时", 0, "普吉岛最重要的佛教寺庙", "morning"),
                "海滩休闲": Activity("海滩晨练", "1.5小时", 0, "在芭东海滩看日出", "morning"),
                "城市探索": Activity("大佛参观", "2.5小时", 200, "普吉岛地标性建筑", "morning")
            },
            "afternoon": {
                "抵达与安顿": Activity("酒店入住和休息", "2小时", 0, "安顿下来，熟悉酒店设施", "afternoon"),
                "海滩休闲": Activity("浮潜体验", "3小时", 600, "皮皮岛或珊瑚岛浮潜", "afternoon"),
                "烹饪体验": Activity("当地香料市场", "2小时", 150, "了解泰式料理的香料", "afternoon"),
                "户外探险": Activity("大佛参观", "2.5小时", 200, "普吉岛地标性建筑", "afternoon"),
                "美食探索": Activity("泰式按摩体验", "1.5小时", 300, "家庭友好的按摩店", "afternoon"),
                "海滩休闲": Activity("海滩休闲", "4小时", 0, "在卡塔海滩或卡伦海滩游泳", "afternoon"),
                "城市探索": Activity("普吉幻多奇乐园", "4小时", 800, "适合家庭的主题公园", "afternoon")
            },
            "evening": {
                "抵达与安顿": Activity("芭东海滩漫步", "2小时", 0, "感受海滩夜生活", "evening"),
                "海滩休闲": Activity("海滩烧烤晚餐", "2.5小时", 400, "在海滩边享受烧烤", "evening"),
                "烹饪体验": Activity("夜市美食探索", "2小时", 200, "尝试各种街头小吃", "evening"),
                "户外探险": Activity("西蒙人妖秀", "2小时", 500, "世界著名的人妖表演", "evening"),
                "美食探索": Activity("邦拉路夜生活", "2小时", 300, "体验普吉岛夜生活", "evening"),
                "海滩休闲": Activity("日落观赏", "1.5小时", 0, "在神仙半岛看日落", "evening"),
                "城市探索": Activity("夜市购物", "2小时", 300, "购买纪念品和当地特产", "evening")
            }
        }

        # 通用活动模板
        general_activities = {
            "morning": {
                "抵达与城市初探": Activity("机场抵达与交通", "2小时", 100, "建议提前预订机场交通", "morning"),
                "深度文化体验": Activity("博物馆参观", "3小时", 150, "建议提前在线购票", "morning"),
                "烹饪体验": Activity("当地早餐体验", "1.5小时", 50, "尝试当地特色早餐", "morning"),
                "自然风光": Activity("公园晨练", "2小时", 0, "免费活动，享受清晨阳光", "morning"),
                "夜生活体验": Activity("城市观光", "2小时", 100, "乘坐观光巴士", "morning"),
                "购物天堂": Activity("早市探索", "2小时", 50, "体验当地早市文化", "morning"),
                "户外冒险": Activity("户外徒步", "3小时", 80, "穿着舒适的鞋子", "morning"),
                "城市探索": Activity("地标建筑参观", "2小时", 120, "建议购买联票", "morning")
            },
            "afternoon": {
                "抵达与城市初探": Activity("市中心漫步", "3小时", 0, "免费活动，熟悉环境", "afternoon"),
                "深度文化体验": Activity("历史遗迹探访", "3小时", 200, "建议请导游讲解", "afternoon"),
                "烹饪体验": Activity("烹饪课程", "3小时", 300, "提前预订课程", "afternoon"),
                "自然风光": Activity("海滩休闲", "4小时", 0, "免费活动，注意防晒", "afternoon"),
                "夜生活体验": Activity("文化演出", "2.5小时", 250, "提前预订门票", "afternoon"),
                "购物天堂": Activity("购物中心购物", "3小时", 500, "注意退税政策", "afternoon"),
                "户外冒险": Activity("水上运动", "3小时", 400, "注意安全", "afternoon"),
                "城市探索": Activity("特色街区探索", "3小时", 100, "步行游览最佳", "afternoon")
            },
            "evening": {
                "抵达与城市初探": Activity("夜景欣赏", "2小时", 0, "免费活动，拍照留念", "evening"),
                "深度文化体验": Activity("夜游古迹", "2小时", 150, "注意开放时间", "evening"),
                "烹饪体验": Activity("夜市美食", "2小时", 100, "尝试各种街头小吃", "evening"),
                "自然风光": Activity("日落观赏", "1.5小时", 0, "免费活动，最佳拍照时间", "evening"),
                "夜生活体验": Activity("酒吧体验", "3小时", 200, "注意安全", "evening"),
                "购物天堂": Activity("夜市购物", "2小时", 150, "可以讨价还价", "evening"),
                "户外冒险": Activity("篝火晚会", "2小时", 100, "注意防火", "evening"),
                "城市探索": Activity("城市夜景", "2小时", 0, "免费活动", "evening")
            }
        }

        # 检查是否是普吉岛
        if "普吉岛" in info.destination or "phuket" in info.destination.lower():
            activities = phuket_activities
        else:
            activities = general_activities

        return activities.get(time_of_day, {}).get(
            theme,
            Activity("自由活动", "2小时", 100, "根据个人喜好安排", time_of_day)
        )

    def generate_restaurant(self, meal_type: str, info: TravelInfo) -> Restaurant:
        """生成餐厅推荐"""
        # 普吉岛特色餐厅
        phuket_restaurants = {
            "lunch": {
                "backpacker": Restaurant("当地小馆", "泰式街头小吃", "฿50-80", "泰式炒河粉", "芭东夜市"),
                "mid-range": Restaurant("Kata Seafood", "海鲜", "฿200-300", "新鲜海产", "卡塔海滩"),
                "luxury": Restaurant("Mom Tri's Kitchen", "精致泰式料理", "฿800-1200", "主厨推荐", "卡马拉海滩")
            },
            "dinner": {
                "backpacker": Restaurant("夜市摊位", "街头小吃", "฿30-60", "必吃小吃", "芭东夜市"),
                "mid-range": Restaurant("Red Chair", "泰式海鲜", "฿400-600", "特色菜", "芭东海滩"),
                "luxury": Restaurant("The Deck", "法式泰式融合", "฿2000-3000", "主厨套餐", "普吉老镇")
            }
        }

        # 通用餐厅模板
        general_restaurants = {
            "lunch": {
                "backpacker": Restaurant("当地小馆", "当地菜", "¥50-80", "招牌菜", "市中心"),
                "mid-range": Restaurant("特色餐厅", "融合菜", "¥100-150", "推荐菜", "商业区"),
                "luxury": Restaurant("高级餐厅", "精致料理", "¥300-500", "主厨推荐", "五星级酒店")
            },
            "dinner": {
                "backpacker": Restaurant("夜市摊位", "街头小吃", "¥30-60", "必吃小吃", "夜市"),
                "mid-range": Restaurant("景观餐厅", "当地菜", "¥150-250", "特色菜", "观景台"),
                "luxury": Restaurant("米其林餐厅", "法式料理", "¥800-1200", "主厨套餐", "高级商圈")
            }
        }

        # 检查是否是普吉岛
        if "普吉岛" in info.destination or "phuket" in info.destination.lower():
            restaurants = phuket_restaurants
        else:
            restaurants = general_restaurants

        restaurant = restaurants.get(meal_type, {}).get(
            info.style,
            Restaurant("当地餐厅", "当地菜", "¥80-120", "特色菜", "市中心")
        )

        # 添加价格数值属性
        price_range_map = {
            "฿50-80": 65, "฿200-300": 250, "฿800-1200": 1000,
            "฿30-60": 45, "฿400-600": 500, "฿2000-3000": 2500,
            "¥50-80": 65, "¥100-150": 125, "¥300-500": 400,
            "¥30-60": 45, "¥150-250": 200, "¥800-1200": 1000,
            "¥80-120": 100
        }
        restaurant.price_range_numeric = price_range_map.get(restaurant.price_range, 100)

        return restaurant

    def generate_transport_tips(self, info: TravelInfo) -> str:
        """生成交通建议"""
        tips = []

        # 普吉岛特色交通建议
        if "普吉岛" in info.destination or "phuket" in info.destination.lower():
            if info.style == "backpacker":
                tips.append("推荐租摩托车（฿300/天）")
                tips.append("使用Songthaew（双条车）")
                tips.append("海滩之间可步行")
            elif info.style == "mid-range":
                tips.append("建议包车或使用Grab")
                tips.append("下载Grab和本地交通App")
                tips.append("酒店可安排机场接送")
            else:  # luxury
                tips.append("建议包车或使用专车服务")
                tips.append("酒店提供豪华车辆")
                tips.append("可安排私人游艇")
        else:
            # 通用交通建议
            if info.style == "backpacker":
                tips.append("推荐购买公共交通日票")
                tips.append("步行是探索城市的最佳方式")
            elif info.style == "mid-range":
                tips.append("地铁和出租车结合使用")
                tips.append("下载当地交通App")
            else:  # luxury
                tips.append("建议包车或使用专车服务")
                tips.append("酒店可提供交通安排")

        return "；".join(tips)

    def generate_pre_trip_checklist(self, info: TravelInfo) -> List[str]:
        """生成预行检查清单"""
        checklist = [
            f"签证要求: {self.check_visa_requirement(info.destination)}",
            f"货币: {self.get_currency_info(info.destination)}",
            f"天气: {self.get_weather_info(info.destination)}",
            "SIM卡/网络: 推荐购买当地eSIM",
            "保险: 建议购买旅行保险",
            "紧急联系: 记录当地紧急电话"
        ]

        return checklist

    def check_visa_requirement(self, destination: str) -> str:
        """检查签证要求（简化版）"""
        visa_free = ["日本", "韩国", "新加坡", "泰国", "马来西亚"]
        if any(country in destination for country in visa_free):
            return "中国公民免签"
        else:
            return "需要提前申请签证"

    def get_currency_info(self, destination: str) -> str:
        """获取货币信息（简化版）"""
        currency_map = {
            "日本": "日元 (JPY) | 1 CNY ≈ 20 JPY",
            "韩国": "韩元 (KRW) | 1 CNY ≈ 190 KRW",
            "泰国": "泰铢 (THB) | 1 CNY ≈ 5 THB",
            "新加坡": "新加坡元 (SGD) | 1 CNY ≈ 0.19 SGD",
            "欧洲": "欧元 (EUR) | 1 CNY ≈ 0.13 EUR",
            "英国": "英镑 (GBP) | 1 CNY ≈ 0.11 GBP",
            "美国": "美元 (USD) | 1 CNY ≈ 0.14 USD"
        }

        for key, value in currency_map.items():
            if key in destination:
                return value

        return "当地货币（建议提前兑换）"

    def get_weather_info(self, destination: str) -> str:
        """获取天气信息（简化版）"""
        weather_map = {
            "日本": "四季分明，根据季节准备衣物",
            "泰国": "热带气候，全年炎热，注意防晒",
            "欧洲": "温带气候，建议携带雨具",
            "新加坡": "热带雨林气候，全年高温多雨"
        }

        for key, value in weather_map.items():
            if key in destination:
                return value

        return "建议出发前查看天气预报"

    def generate_pro_tips(self, info: TravelInfo) -> List[str]:
        """生成实用建议"""
        tips = [
            "避开旅游旺季，节省费用",
            "使用Google Maps离线地图",
            "学习几句当地基本用语",
            "保持警惕，注意个人财物安全",
            "尊重当地文化和习俗",
            "尝试当地特色美食",
            "购买旅游保险",
            "保持重要文件备份"
        ]

        return tips

    def generate_useful_apps(self, info: TravelInfo) -> List[str]:
        """生成推荐应用"""
        apps = [
            "Google Maps - 导航和地图",
            "Google Translate - 翻译工具",
            "XE Currency - 货币转换",
            "TripAdvisor - 餐厅和景点评价"
        ]

        # 根据目的地添加特定应用
        if "日本" in info.destination:
            apps.extend(["Hyperdia - 日本交通查询", "Japan Travel - 官方旅游App"])
        elif "欧洲" in info.destination:
            apps.extend(["Rail Planner - 欧洲铁路", "Citymapper - 城市交通"])

        return apps

    def format_itinerary(self, itinerary: Dict) -> str:
        """格式化行程输出"""
        lines = []

        # 标题
        trip_info = itinerary["trip_info"]
        lines.append(f"✈️ Trip to {trip_info['destination']} | {trip_info['days']} Days")
        lines.append(f"Budget: ¥{trip_info['budget_total']:.0f} total | ¥{trip_info['budget_daily']:.0f}/day")
        lines.append("")

        # 预行检查清单
        lines.append("📋 Pre-Trip Checklist:")
        for item in itinerary["pre_trip_checklist"]:
            lines.append(f"- [ ] {item}")
        lines.append("")

        # 每日行程
        for daily_plan in itinerary["daily_plans"]:
            lines.append(f"🗓️ Day {daily_plan.day_number} — {daily_plan.date} | {daily_plan.theme}")
            lines.append(f"- Morning: {daily_plan.morning.name} — {daily_plan.morning.duration}, ¥{daily_plan.morning.cost}, {daily_plan.morning.tips}")
            lines.append(f"- Lunch: {daily_plan.lunch.name} - {daily_plan.lunch.cuisine}, {daily_plan.lunch.price_range}, {daily_plan.lunch.must_try}")
            lines.append(f"- Afternoon: {daily_plan.afternoon.name} — {daily_plan.afternoon.duration}, ¥{daily_plan.afternoon.cost}, {daily_plan.afternoon.tips}")
            lines.append(f"- Dinner: {daily_plan.dinner.name} - {daily_plan.dinner.cuisine}, {daily_plan.dinner.price_range}, {daily_plan.dinner.must_try}")

            if daily_plan.evening:
                lines.append(f"- Evening: {daily_plan.evening.name} — {daily_plan.evening.duration}, ¥{daily_plan.evening.cost}, {daily_plan.evening.tips}")

            lines.append(f"- 🚗 Getting around: {daily_plan.transport_tips}")
            lines.append(f"- 💰 Estimated day cost: ¥{daily_plan.estimated_cost:.0f}")
            lines.append("")

        # 实用建议
        lines.append("💡 Pro Tips:")
        for tip in itinerary["pro_tips"]:
            lines.append(f"- {tip}")
        lines.append("")

        # 推荐应用
        lines.append("📱 Useful Apps:")
        for app in itinerary["useful_apps"]:
            lines.append(f"- {app}")
        lines.append("")

        # 预算分配
        budget = itinerary["budget_breakdown"]
        lines.append("💰 Budget Breakdown:")
        lines.append(f"- Daily budget: ¥{budget['daily']:.0f}")
        lines.append(f"- Accommodation: ¥{budget['accommodation']:.0f} ({budget['accommodation']/budget['daily']*100:.0f}%)")
        lines.append(f"- Food: ¥{budget['food']:.0f} ({budget['food']/budget['daily']*100:.0f}%)")
        lines.append(f"- Transport: ¥{budget['transport']:.0f} ({budget['transport']/budget['daily']*100:.0f}%)")
        lines.append(f"- Activities: ¥{budget['activities']:.0f} ({budget['activities']/budget['daily']*100:.0f}%)")
        lines.append(f"- Misc: ¥{budget['misc']:.0f} ({budget['misc']/budget['daily']*100:.0f}%)")

        return "\n".join(lines)

    def save_itinerary(self, itinerary: Dict, filename: Optional[str] = None) -> str:
        """保存行程到文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"itinerary_{timestamp}.json"

        filepath = os.path.join(self.data_dir, filename)

        # 转换数据类为字典以便JSON序列化
        serializable_itinerary = self._make_serializable(itinerary)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_itinerary, f, ensure_ascii=False, indent=2)

        return filepath

    def _make_serializable(self, obj) -> Dict:
        """将对象转换为可序列化的字典"""
        if isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return obj

    def load_itinerary(self, filepath: str) -> Dict:
        """从文件加载行程"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)


def main():
    """主函数 - 演示使用"""
    planner = TravelItineraryPlanner()

    # 示例用户输入
    user_input = "帮我规划去日本东京的旅行，5天，预算20000元，情侣旅行，喜欢美食和历史文化"

    # 收集旅行信息
    print("🔍 收集旅行信息...")
    travel_info = planner.collect_travel_info(user_input)
    print(f"✅ 目的地: {travel_info.destination}")
    print(f"✅ 天数: {travel_info.days}")
    print(f"✅ 预算: ¥{travel_info.budget_total}")
    print(f"✅ 旅行者: {travel_info.travelers}")
    print(f"✅ 兴趣: {', '.join(travel_info.interests)}")
    print(f"✅ 风格: {travel_info.style}")
    print()

    # 创建行程
    print("📝 创建行程...")
    itinerary = planner.create_itinerary(travel_info)
    print("✅ 行程创建完成")
    print()

    # 格式化输出
    print("📋 行程详情:")
    print("=" * 80)
    formatted_itinerary = planner.format_itinerary(itinerary)
    print(formatted_itinerary)
    print("=" * 80)

    # 保存行程
    print("💾 保存行程...")
    filepath = planner.save_itinerary(itinerary)
    print(f"✅ 行程已保存到: {filepath}")


if __name__ == "__main__":
    main()
