"""
AI营养师 — 核心推荐引擎
提供：用户画像管理 / 方案生成 / 体质辨识 / 食物推荐 / 营养素分析
"""

import sys
import os
import json
import random
from pathlib import Path

# Add parent scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nutrition_db import (
    FOOD_DB, NUTRIENT_DB, TCM_CONSTITUTIONS, DISEASE_NUTRITION,
    SPORTS_NUTRITION, SPECIAL_POPULATIONS, MEAL_TEMPLATES, FOOD_PAIRING,
    calculate_bmr, calculate_tdee, calculate_target_calories, calculate_macros,
    identify_constitution, search_food, get_top_foods, format_nutrition
)


class NutritionEngine:
    """营养推荐引擎"""

    def __init__(self, user_data_dir=None):
        if user_data_dir is None:
            user_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "user_data")
        self.user_data_dir = user_data_dir
        os.makedirs(user_data_dir, exist_ok=True)
        self.profile_path = os.path.join(user_data_dir, "profile.json")

    # ---------- 用户画像管理 ----------

    def load_profile(self):
        """加载用户画像"""
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_profile(self, profile):
        """保存用户画像"""
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
        return self.profile_path

    def build_profile(self, answers):
        """
        从交互答案构建完整用户画像
        answers: dict with age, gender, height, weight, goal, diet_type, allergies, activity_level, budget, cook_time
        """
        required = ["age", "gender", "height", "weight", "goal"]
        missing = [k for k in required if k not in answers]
        if missing:
            return {"error": f"缺少必要信息: {', '.join(missing)}"}

        defaults = {
            "diet_type": "杂食",
            "allergies": [],
            "activity_level": "轻度活动",
            "budget": "普通",
            "cook_time": "30分钟",
            "health_conditions": [],
        }

        profile = {**defaults, **answers}

        # 计算关键指标
        bmr = calculate_bmr(
            profile["weight"], profile["height"], profile["age"],
            "male" if profile["gender"] in ("男", "male", "男性") else "female"
        )
        tdee = calculate_tdee(bmr, profile["activity_level"])
        target_cal = calculate_target_calories(tdee, profile["goal"])
        macros = calculate_macros(target_cal, profile["goal"], profile["weight"])

        profile["bmr"] = round(bmr)
        profile["tdee"] = round(tdee)
        profile["target_calories"] = round(target_cal)
        profile["macros"] = macros
        profile["bmi"] = round(profile["weight"] / ((profile["height"]/100) ** 2), 1)

        return profile

    # ---------- 饮食方案生成 ----------

    def generate_meal_plan(self, profile, days=7):
        """
        生成个性化饮食方案
        返回完整的周计划，包含每日三餐+加餐的食谱
        """
        goal = profile.get("goal", "健康饮食")

        # 选择对应的食谱模板
        if goal in ("减脂", "减肥", "减重"):
            template_key = "减脂"
        elif goal in ("增肌", "增重"):
            template_key = "增肌"
        else:
            template_key = "维持"

        templates = MEAL_TEMPLATES.get(template_key, MEAL_TEMPLATES["维持"])

        # 根据饮食偏好过滤
        diet_type = profile.get("diet_type", "杂食")
        allergies = profile.get("allergies", [])

        plan = {
            "profile_summary": {
                "目标": goal,
                "每日热量": f"{profile['target_calories']}kcal",
                "蛋白质": f"{profile['macros']['protein_g']}g",
                "脂肪": f"{profile['macros']['fat_g']}g",
                "碳水化合物": f"{profile['macros']['carb_g']}g",
                "BMR": f"{profile['bmr']}kcal",
                "TDEE": f"{profile['tdee']}kcal",
                "BMI": profile.get("bmi", "N/A"),
            },
            "week_plan": [],
            "shopping_list": {},
            "prep_tips": self._get_prep_tips(goal)
        }

        used_meals = {"breakfast": [], "lunch": [], "dinner": [], "snacks": []}
        shopping = {}

        for day in range(1, days + 1):
            day_plan = {
                "day": day,
                "day_name": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][day-1],
                "meals": {}
            }

            for meal_type in ["breakfast", "lunch", "dinner"]:
                available = [m for m in templates[meal_type] if m["name"] not in used_meals[meal_type]]
                if not available:
                    available = templates[meal_type]
                    used_meals[meal_type] = []

                chosen = random.choice(available)
                used_meals[meal_type].append(chosen["name"])

                # Adjust for diet type
                items = self._adjust_for_diet(chosen["items"], diet_type, allergies)

                # Set calorie target per meal
                if meal_type == "breakfast":
                    target_pct = 0.25
                elif meal_type == "lunch":
                    target_pct = 0.35
                else:
                    target_pct = 0.25

                day_plan["meals"][meal_type] = {
                    "name": chosen["name"],
                    "items": items,
                    "estimated_kcal": chosen["kcal"],
                    "protein_g": chosen["protein"],
                    "prep_time_min": chosen["prep"],
                    "target_pct": f"{int(target_pct*100)}%"
                }

                # Add to shopping list
                for item in items:
                    food_name = item.split("(")[0].strip()
                    cat = self._get_food_category(food_name)
                    if cat not in shopping:
                        shopping[cat] = []
                    shopping[cat].append(food_name)

            # Add 2 snacks
            if "snacks" in templates:
                snack_choices = random.sample(templates["snacks"], min(2, len(templates["snacks"])))
                day_plan["meals"]["snacks"] = [
                    {"name": s["name"], "items": self._adjust_for_diet(s["items"], diet_type, allergies),
                     "estimated_kcal": s["kcal"], "protein_g": s["protein"]}
                    for s in snack_choices
                ]
                for s in snack_choices:
                    for item in s["items"]:
                        food_name = item.split("(")[0].strip()
                        cat = self._get_food_category(food_name)
                        if cat not in shopping:
                            shopping[cat] = []
                        shopping[cat].append(food_name)

            plan["week_plan"].append(day_plan)

        # Deduplicate and count shopping list
        plan["shopping_list"] = {k: list(set(v)) for k, v in shopping.items()}

        return plan

    def _adjust_for_diet(self, items, diet_type, allergies):
        """根据饮食偏好调整食材"""
        adjusted = []
        meat_items = {"鸡胸肉", "鸡腿肉", "猪瘦肉", "猪排骨", "牛肉(瘦)", "牛腩", "羊肉(瘦)", "鸭肉"}
        seafood_items = {"三文鱼", "虾仁", "带鱼", "鳕鱼", "鲈鱼", "鲫鱼", "蛤蜊"}
        dairy_items = {"牛奶", "酸奶", "芝士", "奶酪"}

        for item in items:
            # Extract base food name
            base_name = item.split("g")[0].split("ml")[0].split("个")[0].split("片")[0].split("勺")[0].split("碗")[0].split("杯")[0].strip()
            # Remove quantity prefix
            for prefix in meat_items | seafood_items | dairy_items:
                if prefix in item:
                    base_name = prefix
                    break

            if diet_type == "素食":
                if base_name in meat_items or base_name in seafood_items:
                    continue  # skip
                if base_name in dairy_items:
                    continue
                if "鸡蛋" in item:
                    continue
            elif diet_type == "蛋奶素":
                if base_name in meat_items or base_name in seafood_items:
                    continue
            elif diet_type == "鱼素":
                if base_name in meat_items:
                    continue

            if base_name in allergies:
                continue

            adjusted.append(item)

        return adjusted

    def _get_food_category(self, food_name):
        """将食物名称映射到购物清单分类"""
        mapping = {
            "鸡胸肉": "肉类", "鸡腿肉": "肉类", "猪瘦肉": "肉类", "牛肉": "肉类", "羊肉": "肉类", "鸭肉": "肉类",
            "三文鱼": "海鲜", "虾仁": "海鲜", "带鱼": "海鲜", "鳕鱼": "海鲜", "鲈鱼": "海鲜",
            "鸡蛋": "蛋奶", "牛奶": "蛋奶", "酸奶": "蛋奶", "芝士": "蛋奶", "蛋白粉": "补剂",
            "西兰花": "蔬菜", "菠菜": "蔬菜", "番茄": "蔬菜", "黄瓜": "蔬菜", "生菜": "蔬菜",
            "胡萝卜": "蔬菜", "芦笋": "蔬菜", "秋葵": "蔬菜", "青椒": "蔬菜", "青菜": "蔬菜", "冬瓜": "蔬菜",
            "菌菇": "蔬菜", "混合生菜": "蔬菜", "木耳": "蔬菜",
            "燕麦": "主食", "全麦面包": "主食", "全麦吐司": "主食", "米饭": "主食", "糙米饭": "主食",
            "杂粮饭": "主食", "小米粥": "主食", "红薯": "主食", "藜麦": "主食", "馒头": "主食",
            "香蕉": "水果", "蓝莓": "水果", "苹果": "水果", "牛油果": "水果", "小番茄": "水果",
            "核桃": "坚果", "花生酱": "坚果", "坚果": "坚果",
            "橄榄油": "调味", "油醋汁": "调味", "柠檬汁": "调味",
        }
        return mapping.get(food_name, "其他")

    def _get_prep_tips(self, goal):
        """备餐建议"""
        base_tips = [
            "周末花1-2小时完成下周备餐(batch cooking)，工作日只需加热",
            "主食类(米饭/杂粮/红薯)可一次做3天量，分装冷藏",
            "蛋白质(鸡胸/牛肉/鱼)可提前腌制分装冷冻，解冻即用",
            "蔬菜建议当天洗切，叶菜不超过2天",
            "准备一套好用的饭盒，按餐分装"
        ]

        if goal in ("减脂", "减肥"):
            base_tips.extend([
                "厨房备好喷雾油(少油烹饪神器)",
                "蒸和煮为主，少煎炒",
                "糖替换为代糖(赤藓糖醇/甜菊糖)",
            ])
        elif goal in ("增肌", "增重"):
            base_tips.extend([
                "准备便携摇摇杯和蛋白粉分装盒",
                "坚果能量棒自制(更健康)",
                "睡前准备好明天的加餐",
            ])

        return base_tips

    # ---------- 体质辨识 ----------

    def identify_tcm_constitution(self, answers):
        """
        answers: 体质自评答案
        返回体质判定结果和对应的食疗方案
        """
        result = identify_constitution(answers)

        primary = result["primary"]
        constitution_data = TCM_CONSTITUTIONS.get(primary, TCM_CONSTITUTIONS["平和质"])

        return {
            "identification": result,
            "constitution": {
                "name": primary,
                "key_features": constitution_data["key_features"],
                "tendency_diseases": constitution_data["tendency_diseases"],
                "food_principle": constitution_data["food_principle"],
                "recommend": constitution_data["recommend"],
                "avoid": constitution_data["avoid"],
                "lifestyle": constitution_data["lifestyle"],
            }
        }

    # ---------- 慢病营养 ----------

    def disease_nutrition_guide(self, disease_name):
        """获取慢病营养指导"""
        disease_map = {
            "糖尿病": "糖尿病", "血糖": "糖尿病", "diabetes": "糖尿病",
            "高血压": "高血压", "血压": "高血压", "hypertension": "高血压",
            "痛风": "痛风/高尿酸", "尿酸": "痛风/高尿酸", "gout": "痛风/高尿酸",
            "高血脂": "高血脂", "血脂": "高血脂", "cholesterol": "高血脂",
        }

        key = disease_map.get(disease_name, disease_name)
        if key not in DISEASE_NUTRITION:
            known = list(DISEASE_NUTRITION.keys())
            return {"error": f"暂不支持该慢病。当前支持: {', '.join(known)}"}

        return DISEASE_NUTRITION[key]

    # ---------- 运动营养 ----------

    def sports_nutrition_guide(self, goal):
        """获取运动营养指导"""
        goal_map = {
            "增肌": "增肌", "muscle": "增肌", "build muscle": "增肌",
            "减脂": "减脂", "fat loss": "减脂", "cut": "减脂",
            "耐力": "耐力", "endurance": "耐力", "马拉松": "耐力", "跑步": "耐力",
        }

        key = goal_map.get(goal, goal)
        if key not in SPORTS_NUTRITION:
            known = list(SPORTS_NUTRITION.keys())
            return {"error": f"暂不支持该运动目标。当前支持: {', '.join(known)}"}

        return SPORTS_NUTRITION[key]

    # ---------- 特殊人群 ----------

    def special_population_guide(self, population):
        """特殊人群营养指导"""
        pop_map = {
            "孕期": "孕期", "怀孕": "孕期", "孕妇": "孕期", "pregnancy": "孕期",
            "哺乳期": "哺乳期", "哺乳": "哺乳期", "lactation": "哺乳期",
            "儿童": "儿童", "小孩": "儿童", "孩子": "儿童", "children": "儿童", "kids": "儿童",
            "老年": "老年", "老人": "老年", "长辈": "老年", "elderly": "老年",
        }

        key = pop_map.get(population, population)
        if key not in SPECIAL_POPULATIONS:
            known = list(SPECIAL_POPULATIONS.keys())
            return {"error": f"暂不支持该人群。当前支持: {', '.join(known)}"}

        return SPECIAL_POPULATIONS[key]

    # ---------- 营养素查询 ----------

    def nutrient_info(self, nutrient_name):
        """营养素详细信息"""
        # Fuzzy match
        for key in NUTRIENT_DB:
            if nutrient_name.lower() in key.lower() or key in nutrient_name:
                info = NUTRIENT_DB[key].copy()
                # Add top foods
                info["name"] = key
                info["top_foods"] = get_top_foods(key, 8)
                return info
        return {"error": f"未找到营养素'{nutrient_name}'", "available": list(NUTRIENT_DB.keys())}

    # ---------- 食物查询 ----------

    def food_info(self, keyword):
        """食物营养信息"""
        results = search_food(keyword)
        if not results:
            return {"error": f"未找到食物'{keyword}'"}
        return [{"name": name, **data} for name, data in results]

    # ---------- 食物搭配 ----------

    def food_pairing_info(self):
        """食物搭配知识"""
        return FOOD_PAIRING


def main():
    """命令行测试"""
    engine = NutritionEngine()

    # Test profile
    profile = engine.build_profile({
        "age": 30, "gender": "男", "height": 175, "weight": 78,
        "goal": "减脂", "diet_type": "杂食", "activity_level": "中度活动"
    })
    print(json.dumps(profile, ensure_ascii=False, indent=2))

    # Test meal plan
    plan = engine.generate_meal_plan(profile, days=3)
    print(f"\nGenerated {len(plan['week_plan'])} days of meals")
    print(f"Shopping categories: {list(plan['shopping_list'].keys())}")

    # Test TCM
    tcm = engine.identify_tcm_constitution({
        "energy": "容易疲劳", "cold": "怕冷", "thirst": "不渴",
        "body": "偏胖", "stool": "稀溏"
    })
    print(f"\nTCM: {tcm['constitution']['name']}")

    # Test nutrient
    iron = engine.nutrient_info("铁")
    print(f"\nIron top foods: {iron['top_foods'][:3]}")

    print("\n✅ 引擎测试通过")


if __name__ == "__main__":
    main()
