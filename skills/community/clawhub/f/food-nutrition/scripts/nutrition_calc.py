#!/usr/bin/env python3
"""
营养素计算引擎
- 单餐/单日营养素汇总
- 多日趋势分析
- 目标偏差计算
- 饮食评分
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional
from .food_db import search_food, get_dri

DATA_DIR = Path(__file__).parent.parent / "user_data"
DIARY_DIR = DATA_DIR / "diary"
PROFILE_PATH = DATA_DIR / "profile.json"


class NutritionCalc:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        DIARY_DIR.mkdir(parents=True, exist_ok=True)

    def load_profile(self) -> Optional[dict]:
        """加载用户档案"""
        if PROFILE_PATH.exists():
            with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_profile(self, profile: dict):
        """保存用户档案"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)

    def get_dri_for_user(self) -> dict:
        """获取用户每日推荐摄入"""
        profile = self.load_profile()
        if profile:
            return get_dri(**profile.get("body", {}), goal=profile.get("goal", "maintain"))
        # 默认值: 轻体力成年男性
        return get_dri(age=30, gender="male", goal="maintain",
                       height_cm=170, weight_kg=70, activity="moderate")

    def parse_food_items(self, text: str) -> list:
        """
        自然语言解析食物列表
        支持格式: "吃了鸡胸肉200g、米饭一碗、西兰花一份"
        返回: [{foodName, amount_g, foodData}]
        """
        import re

        items = []
        # 分句: 按顿号、逗号、和、与分割
        parts = re.split(r'[，,、和与及]', text)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # 去除前缀: 吃了/我吃/早餐/午餐/晚餐等
            part = re.sub(r'^(吃了?|我吃了?|早餐|午餐|晚餐|中午|早上|晚上|上午|下午)', '', part).strip()

            # 提取份量: 200g, 一碗, 一份, 一个, 半碗等
            amount_g = 100  # 默认100g
            food_name = part

            # 匹配具体克数
            m = re.match(r'(.+?)(\d+)\s*[g克]$', part)
            if m:
                food_name = m.group(1).strip()
                amount_g = int(m.group(2))
            else:
                # 匹配中文份量
                portion_map = {
                    '一碗': 250, '半碗': 125, '一小碗': 150, '一大碗': 400,
                    '一份': 200, '一个': 80, '两个': 160, '三个': 240,
                    '半个': 40, '一杯': 250, '半杯': 125,
                    '一盘': 300, '一小盘': 150,
                    '一根': 100, '两根': 200,
                    '一片': 30, '两片': 60,
                    '一块': 80, '两块': 160,
                }
                for kw, grams in portion_map.items():
                    if kw in part:
                        food_name = part.replace(kw, '').strip()
                        amount_g = grams
                        break

            # 清理食物名
            food_name = re.sub(r'^\d+\s*[g克]?', '', food_name).strip()
            if not food_name:
                continue

            # 查询食物数据
            food_data = search_food(food_name, api_key=self.api_key)
            if food_data:
                items.append({
                    "foodName": food_data["foodName"],
                    "amount_g": amount_g,
                    "foodData": food_data,
                })
            else:
                # 未知食物, 记录但无数据
                items.append({
                    "foodName": food_name,
                    "amount_g": amount_g,
                    "foodData": None,
                })

        return items

    def calc_meal(self, items: list) -> dict:
        """计算一餐/几餐的营养总计"""
        total = {"energy": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0}
        unknown_foods = []

        for item in items:
            fd = item.get("foodData")
            if fd:
                ratio = item["amount_g"] / 100.0
                for key in total:
                    total[key] += fd.get(key, 0) * ratio
            else:
                unknown_foods.append(item["foodName"])

        for key in total:
            total[key] = round(total[key], 1)

        total["unknownFoods"] = unknown_foods
        total["itemCount"] = len(items)
        return total

    def calc_daily(self, dt: Optional[date] = None) -> dict:
        """计算某天总摄入(从日记读取)"""
        if dt is None:
            dt = date.today()

        day_file = DIARY_DIR / f"{dt.isoformat()}.json"
        total = {"energy": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0, "meals": []}

        if day_file.exists():
            with open(day_file, "r", encoding="utf-8") as f:
                entries = json.load(f)
                for entry in entries:
                    if "nutrition" in entry:
                        for key in ["energy", "protein", "fat", "carbs", "fiber"]:
                            total[key] += entry["nutrition"].get(key, 0)
                    total["meals"].append(entry)

        for key in ["energy", "protein", "fat", "carbs", "fiber"]:
            total[key] = round(total[key], 1)

        return total

    def save_meal(self, meal_name: str, nutrition: dict, items: list,
                  dt: Optional[date] = None, note: str = ""):
        """保存一餐记录"""
        if dt is None:
            dt = date.today()

        day_file = DIARY_DIR / f"{dt.isoformat()}.json"

        # 读取已有记录
        if day_file.exists():
            with open(day_file, "r", encoding="utf-8") as f:
                entries = json.load(f)
        else:
            entries = []

        entries.append({
            "meal": meal_name,
            "time": datetime.now().strftime("%H:%M"),
            "nutrition": nutrition,
            "items": items,
            "note": note,
        })

        with open(day_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

    def calc_trend(self, days: int = 7) -> dict:
        """计算多日趋势"""
        trend = {"dates": [], "energy": [], "protein": [], "fat": [], "carbs": [], "fiber": []}

        for i in range(days - 1, -1, -1):
            dt = date.today() - timedelta(days=i)
            daily = self.calc_daily(dt)
            trend["dates"].append(dt.strftime("%m/%d"))
            trend["energy"].append(daily["energy"])
            trend["protein"].append(daily["protein"])
            trend["fat"].append(daily["fat"])
            trend["carbs"].append(daily["carbs"])
            trend["fiber"].append(daily["fiber"])

        return trend

    def rate_diet(self, daily: dict, dri: dict) -> dict:
        """饮食评分 (满分100)"""
        score = 100
        feedback = []

        # 热量评估 (±20%内为正常)
        energy_ratio = daily["energy"] / dri["energy"] if dri["energy"] else 0
        if energy_ratio < 0.7:
            score -= 20
            feedback.append({"type": "warn", "msg": f"热量摄入偏低 ({daily['energy']}/{dri['energy']} kcal)", "diff": "偏低"})
        elif energy_ratio > 1.3:
            score -= 20
            feedback.append({"type": "warn", "msg": f"热量摄入偏高 ({daily['energy']}/{dri['energy']} kcal)", "diff": "偏高"})
        elif 0.9 <= energy_ratio <= 1.1:
            feedback.append({"type": "good", "msg": f"热量摄入合理 ({daily['energy']}/{dri['energy']} kcal)", "diff": "合理"})
        else:
            score -= 5
            feedback.append({"type": "info", "msg": f"热量摄入略{'低' if energy_ratio < 1 else '高'} ({daily['energy']}/{dri['energy']} kcal)", "diff": "略偏"})

        # 蛋白质
        prot_ratio = daily["protein"] / dri["protein"] if dri["protein"] else 0
        if prot_ratio < 0.7:
            score -= 10
            feedback.append({"type": "warn", "msg": f"蛋白质摄入不足 ({daily['protein']:.0f}/{dri['protein']}g)", "diff": "不足"})
        elif prot_ratio > 2.0:
            score -= 5
            feedback.append({"type": "info", "msg": f"蛋白质摄入偏高 ({daily['protein']:.0f}/{dri['protein']}g)", "diff": "偏高"})
        else:
            feedback.append({"type": "good", "msg": f"蛋白质摄入合理 ({daily['protein']:.0f}/{dri['protein']}g)", "diff": "合理"})

        # 脂肪
        fat_ratio = daily["fat"] / dri["fat"] if dri["fat"] else 0
        if fat_ratio > 1.5:
            score -= 10
            feedback.append({"type": "warn", "msg": f"脂肪摄入超标 ({daily['fat']:.0f}/{dri['fat']}g)", "diff": "超标"})
        elif fat_ratio < 0.5:
            score -= 5
            feedback.append({"type": "info", "msg": f"脂肪摄入偏低 ({daily['fat']:.0f}/{dri['fat']}g)", "diff": "偏低"})
        else:
            feedback.append({"type": "good", "msg": f"脂肪摄入合理 ({daily['fat']:.0f}/{dri['fat']}g)", "diff": "合理"})

        # 纤维
        fiber_ratio = daily["fiber"] / dri["fiber"] if dri["fiber"] else 0
        if fiber_ratio < 0.5:
            score -= 10
            feedback.append({"type": "warn", "msg": f"膳食纤维严重不足 ({daily['fiber']:.0f}/{dri['fiber']}g)", "diff": "严重不足"})
        elif fiber_ratio < 0.8:
            score -= 5
            feedback.append({"type": "info", "msg": f"膳食纤维偏低 ({daily['fiber']:.0f}/{dri['fiber']}g)", "diff": "偏低"})
        else:
            feedback.append({"type": "good", "msg": f"膳食纤维达标 ({daily['fiber']:.0f}/{dri['fiber']}g)", "diff": "达标"})

        return {
            "score": max(score, 0),
            "grade": "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D",
            "feedback": feedback,
        }
