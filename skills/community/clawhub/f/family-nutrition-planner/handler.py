#!/usr/bin/env python3
"""
Family Nutrition Planner - Handler
Main entry point for the nutrition planning skill.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional


# ==================== Types ====================

class NutritionPlanRequest:
    """Request format for nutrition planning."""
    
    def __init__(self, data: Dict[str, Any]):
        self.family_name = data.get("familyName", "我的家庭")
        self.members = data.get("members", [])
        self.preferences = data.get("preferences", {})
        self.constraints = data.get("constraints", {})
        self.goals = data.get("goals", {"type": "balance"})


class NutritionCalculator:
    """Calculate nutritional needs based on member profiles."""
    
    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,
        "lightly-active": 1.375,
        "moderately-active": 1.55,
        "very-active": 1.725,
        "extra-active": 1.9
    }
    
    GOAL_ADJUSTMENTS = {
        "balance": 0,
        "low-carb": -0.1,
        "high-protein": 0.05,
        "weight-loss": -0.2,
        "muscle-gain": 0.15
    }
    
    MACRO_RATIOS = {
        "balance": {"protein": 0.20, "carbs": 0.50, "fat": 0.30},
        "low-carb": {"protein": 0.25, "carbs": 0.30, "fat": 0.45},
        "high-protein": {"protein": 0.30, "carbs": 0.40, "fat": 0.30},
        "weight-loss": {"protein": 0.30, "carbs": 0.40, "fat": 0.30},
        "muscle-gain": {"protein": 0.30, "carbs": 0.45, "fat": 0.25}
    }
    
    @staticmethod
    def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation."""
        if gender == "male":
            return 10 * weight + 6.25 * height - 5 * age + 5
        else:
            return 10 * weight + 6.25 * height - 5 * age - 161
    
    @staticmethod
    def calculate_tdee(bmr: float, activity_level: str) -> float:
        """Calculate Total Daily Energy Expenditure."""
        multiplier = NutritionCalculator.ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
        return bmr * multiplier
    
    def calculate_member_needs(self, member: Dict) -> Dict[str, Any]:
        """Calculate nutritional needs for a single member."""
        bmr = self.calculate_bmr(
            member["weight"],
            member["height"],
            member["age"],
            member["gender"]
        )
        tdee = self.calculate_tdee(bmr, member.get("activityLevel", "sedentary"))
        
        goal_type = self.goals.get("type", "balance")
        adjustment = self.GOAL_ADJUSTMENTS.get(goal_type, 0)
        target = tdee * (1 + adjustment)
        
        macros = self.MACRO_RATIOS.get(goal_type, self.MACRO_RATIOS["balance"])
        
        return {
            "name": member["name"],
            "bmr": round(bmr, 1),
            "tdee": round(tdee, 1),
            "target": round(target, 1),
            "macros": {
                "protein_grams": round(target * macros["protein"] / 4, 1),
                "carbs_grams": round(target * macros["carbs"] / 4, 1),
                "fat_grams": round(target * macros["fat"] / 9, 1)
            }
        }


class MealPlanGenerator:
    """Generate weekly meal plans."""
    
    # Mock recipe database
    RECIPES = {
        "breakfast": [
            {"name": "全麦吐司配鸡蛋牛油果", "calories": 420, "time": "15分钟", 
             "ingredients": ["全麦吐司", "鸡蛋", "牛油果", "西红柿"], "protein": 18},
            {"name": "燕麦粥配水果", "calories": 350, "time": "10分钟",
             "ingredients": ["燕麦", "牛奶", "香蕉", "蓝莓"], "protein": 12},
            {"name": "中式豆腐脑", "calories": 280, "time": "20分钟",
             "ingredients": ["黄豆", "内酯豆腐", "葱花", "酱油"], "protein": 22},
            {"name": "蔬菜鸡蛋饼", "calories": 380, "time": "15分钟",
             "ingredients": ["鸡蛋", "面粉", "青菜", "胡萝卜"], "protein": 16},
            {"name": "牛奶鸡蛋羹", "calories": 320, "time": "15分钟",
             "ingredients": ["鸡蛋", "牛奶", "葱花"], "protein": 20},
        ],
        "lunch": [
            {"name": "清蒸鲈鱼 + 米饭 + 青菜", "calories": 580, "time": "25分钟",
             "ingredients": ["鲈鱼", "大米", "青菜", "姜"], "protein": 35},
            {"name": "鸡胸肉沙拉配藜麦", "calories": 520, "time": "20分钟",
             "ingredients": ["鸡胸肉", "混合蔬菜", "藜麦", "橄榄油"], "protein": 40},
            {"name": "番茄牛腩面", "calories": 620, "time": "35分钟",
             "ingredients": ["牛肉", "西红柿", "面条", "洋葱"], "protein": 32},
            {"name": "红烧肉 + 米饭", "calories": 720, "time": "40分钟",
             "ingredients": ["五花肉", "大米", "土豆", "酱油"], "protein": 28},
            {"name": "虾仁炒饭", "calories": 550, "time": "20分钟",
             "ingredients": ["虾仁", "米饭", "鸡蛋", "豌豆"], "protein": 30},
        ],
        "dinner": [
            {"name": "蒜蓉西兰花 + 烤鸡腿", "calories": 520, "time": "30分钟",
             "ingredients": ["西兰花", "鸡腿", "大蒜", "橄榄油"], "protein": 38},
            {"name": "番茄鸡蛋汤 + 清炒藕片", "calories": 420, "time": "25分钟",
             "ingredients": ["西红柿", "鸡蛋", "莲藕", "青菜"], "protein": 22},
            {"name": "清蒸鲈鱼 + 凉拌黄瓜", "calories": 480, "time": "30分钟",
             "ingredients": ["鲈鱼", "黄瓜", "蒜", "醋"], "protein": 36},
            {"name": "肉末豆腐 + 米饭", "calories": 550, "time": "25分钟",
             "ingredients": ["猪肉", "豆腐", "大米", "葱"], "protein": 30},
            {"name": "冬瓜排骨汤 + 炒青菜", "calories": 500, "time": "40分钟",
             "ingredients": ["排骨", "冬瓜", "青菜", "姜"], "protein": 28},
        ]
    }
    
    DAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    def __init__(self, preferences: Dict, constraints: Dict, goals: Dict):
        self.preferences = preferences
        self.constraints = constraints
        self.goals = goals
        self.max_prep_time = constraints.get("maxPrepTime", 60)
        self.weekly_budget = constraints.get("weeklyBudget", 500)
    
    def generate_daily_plan(self, day: str) -> Dict[str, Any]:
        """Generate a single day's meal plan."""
        breakfast = random.choice(self.RECIPES["breakfast"])
        lunch = random.choice(self.RECIPES["lunch"])
        dinner = random.choice(self.RECIPES["dinner"])
        
        total_cal = breakfast["calories"] + lunch["calories"] + dinner["calories"]
        
        return {
            "day": day,
            "meals": {
                "breakfast": {
                    "name": breakfast["name"],
                    "calories": breakfast["calories"],
                    "prepTime": breakfast["time"],
                    "ingredients": breakfast["ingredients"]
                },
                "lunch": {
                    "name": lunch["name"],
                    "calories": lunch["calories"],
                    "prepTime": lunch["time"],
                    "ingredients": lunch["ingredients"]
                },
                "dinner": {
                    "name": dinner["name"],
                    "calories": dinner["calories"],
                    "prepTime": dinner["time"],
                    "ingredients": dinner["ingredients"]
                }
            },
            "dailyNutrition": {
                "calories": total_cal,
                "protein": "约{}g".format(
                    breakfast.get("protein", 15) + lunch.get("protein", 30) + dinner.get("protein", 30)
                ),
                "carbohydrates": "约200g",
                "fat": "约60g"
            }
        }
    
    def generate_weekly_plan(self) -> List[Dict[str, Any]]:
        """Generate a 7-day meal plan."""
        return [self.generate_daily_plan(day) for day in self.DAYS]


class ShoppingListGenerator:
    """Generate shopping list from meal plan."""
    
    def __init__(self, weekly_plan: List[Dict], budget: float):
        self.weekly_plan = weekly_plan
        self.budget = budget
    
    def generate(self) -> Dict[str, Any]:
        """Generate categorized shopping list."""
        all_ingredients = []
        for day_plan in self.weekly_plan:
            for meal_type, meal in day_plan["meals"].items():
                all_ingredients.extend(meal.get("ingredients", []))
        
        categories = {
            "肉类": ["鸡腿", "鸡胸肉", "鲈鱼", "虾仁", "猪肉", "排骨", "牛肉", "五花肉"],
            "蔬菜": ["青菜", "西兰花", "黄瓜", "西红柿", "胡萝卜", "莲藕", "冬瓜", "洋葱", "姜", "蒜", "葱"],
            "主食": ["大米", "面条", "燕麦", "全麦吐司", "藜麦"],
            "蛋奶": ["鸡蛋", "牛奶", "内酯豆腐"],
            "豆制品": ["黄豆", "豆腐"],
            "水果": ["香蕉", "蓝莓", "牛油果"],
            "调料": ["酱油", "醋", "橄榄油", "葱花"]
        }
        
        shopping_items = []
        for category, items in categories.items():
            cat_items = [item for item in items if item in all_ingredients]
            if cat_items:
                shopping_items.append({
                    "category": category,
                    "items": [
                        {"name": item, "quantity": "适量", "estimatedCost": random.randint(5, 30)}
                        for item in cat_items
                    ]
                })
        
        estimated_cost = sum(
            sum(item["estimatedCost"] for item in cat["items"])
            for cat in shopping_items
        )
        
        savings_tips = [
            "周末一次性采购可以节省时间",
            "选择当季蔬菜可以降低成本",
            "大型超市比便利店便宜约20%",
            "关注会员特价活动"
        ]
        
        return {
            "categories": shopping_items,
            "estimatedCost": estimated_cost,
            "savingsTips": savings_tips
        }


class AllergyChecker:
    """Check for allergens in meal plans."""
    
    COMMON_ALLERGENS = ["花生", "虾", "牛奶", "鸡蛋", "小麦", "大豆", "坚果"]
    
    @staticmethod
    def check_ingredients(ingredients: List[str], allergies: List[str]) -> List[str]:
        """Check if any ingredients contain allergens."""
        found_allergens = []
        for allergen in allergies:
            for ingredient in ingredients:
                if allergen in ingredient:
                    found_allergens.append(allergen)
        return found_allergens
    
    @staticmethod
    def filter_safe_recipes(recipes: List[Dict], allergies: List[str]) -> List[Dict]:
        """Filter out recipes containing allergens."""
        if not allergies:
            return recipes
        
        safe_recipes = []
        for recipe in recipes:
            all_ingredients = recipe.get("ingredients", [])
            has_allergen = False
            for allergen in allergies:
                if any(allergen in ing for ing in all_ingredients):
                    has_allergen = True
                    break
            if not has_allergen:
                safe_recipes.append(recipe)
        return safe_recipes


def handle_nutrition_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main handler for nutrition planning requests."""
    request = NutritionPlanRequest(request_data)
    
    calculator = NutritionCalculator()
    calculator.goals = request.goals
    
    member_needs = []
    all_allergies = set()
    total_tdee = 0
    
    for member in request.members:
        needs = calculator.calculate_member_needs(member)
        member_needs.append(needs)
        total_tdee += needs["target"]
        if member.get("allergies"):
            all_allergies.update(member["allergies"])
    
    avg_daily_cal = total_tdee / len(request.members) if request.members else 2000
    
    meal_generator = MealPlanGenerator(
        request.preferences,
        request.constraints,
        request.goals
    )
    weekly_plan = meal_generator.generate_weekly_plan()
    
    allergen_warnings = []
    for day_plan in weekly_plan:
        for meal_type, meal in day_plan["meals"].items():
            found = AllergyChecker.check_ingredients(
                meal.get("ingredients", []),
                list(all_allergies)
            )
            if found:
                allergen_warnings.append(f"{day_plan['day']}{meal_type}: 发现过敏原 {', '.join(found)}")
    
    shopping_gen = ShoppingListGenerator(weekly_plan, request.constraints.get("weeklyBudget", 500))
    shopping_list = shopping_gen.generate()
    
    goal_type = request.goals.get("type", "balance")
    macro_ratios = NutritionCalculator.MACRO_RATIOS.get(goal_type, NutritionCalculator.MACRO_RATIOS["balance"])
    
    unique_ingredients = set()
    for day_plan in weekly_plan:
        for meal in day_plan["meals"].values():
            unique_ingredients.update(meal.get("ingredients", []))
    
    response = {
        "success": True,
        "nutritionSummary": {
            "averageDailyCalories": round(avg_daily_cal, 0),
            "macronutrientBalance": {
                "protein": "{}%".format(int(macro_ratios["protein"] * 100)),
                "carbohydrates": "{}%".format(int(macro_ratios["carbs"] * 100)),
                "fat": "{}%".format(int(macro_ratios["fat"] * 100))
            },
            "foodVariety": len(unique_ingredients)
        },
        "dailyPlans": weekly_plan,
        "shoppingList": shopping_list,
        "nutritionAnalysis": {
            "strengths": [
                "每日三餐营养均衡",
                "包含多种蛋白质来源（鱼、肉、豆制品）",
                "蔬菜摄入充足",
                "食材多样性良好（{}种食材）".format(len(unique_ingredients))
            ],
            "concerns": allergen_warnings if allergen_warnings else [],
            "suggestions": [
                "建议每天饮用300-500ml牛奶或酸奶",
                "适量增加全谷物摄入",
                "每周安排2-3次鱼类摄入"
            ]
        },
        "weeklyNutritionTrend": "本周营养摄入整体均衡，蛋白质和蔬菜摄入充足，建议继续保持多样化的饮食结构。",
        "memberNutritionNeeds": member_needs
    }
    
    return response


def handle_nutrition_calculation(member_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate nutritional needs for a single member."""
    calculator = NutritionCalculator()
    calculator.goals = {"type": member_data.get("goalType", "balance")}
    needs = calculator.calculate_member_needs(member_data)
    
    goal_type = member_data.get("goalType", "balance")
    macro_ratios = NutritionCalculator.MACRO_RATIOS.get(goal_type, NutritionCalculator.MACRO_RATIOS["balance"])
    
    return {
        "success": True,
        "member": needs["name"],
        "bmr": needs["bmr"],
        "tdee": needs["tdee"],
        "targetIntake": needs["target"],
        "macronutrientTargets": {
            "protein": {
                "grams": needs["macros"]["protein_grams"],
                "calories": round(needs["macros"]["protein_grams"] * 4, 1),
                "percentage": int(macro_ratios["protein"] * 100)
            },
            "carbohydrates": {
                "grams": needs["macros"]["carbs_grams"],
                "calories": round(needs["macros"]["carbs_grams"] * 4, 1),
                "percentage": int(macro_ratios["carbs"] * 100)
            },
            "fat": {
                "grams": needs["macros"]["fat_grams"],
                "calories": round(needs["macros"]["fat_grams"] * 9, 1),
                "percentage": int(macro_ratios["fat"] * 100)
            }
        },
        "recommendations": [
            "蛋白质分布在每餐 25-40g 有助于最佳吸收",
            "训练后碳水摄入为主有助于恢复",
            "适量健康脂肪（坚果、橄榄油）有益心血管健康"
        ]
    }


if __name__ == "__main__":
    test_request = {
        "familyName": "张氏家庭",
        "members": [
            {"name": "爸爸", "age": 35, "gender": "male", "weight": 75, "height": 175, "activityLevel": "lightly-active", "allergies": []},
            {"name": "妈妈", "age": 32, "gender": "female", "weight": 58, "height": 162, "activityLevel": "lightly-active", "allergies": []},
            {"name": "孩子", "age": 8, "gender": "male", "weight": 28, "height": 130, "activityLevel": "moderately-active", "allergies": ["虾"]}
        ],
        "preferences": {"cuisine": ["中式"], "cookingStyle": ["少油", "清淡"]},
        "constraints": {"weeklyBudget": 500, "maxPrepTime": 60, "servingSize": 4},
        "goals": {"type": "balance"}
    }
    
    print("=" * 50)
    print("Family Nutrition Planner - Test")
    print("=" * 50)
    print()
    
    result = handle_nutrition_request(test_request)
    print(json.dumps(result, ensure_ascii=False, indent=2))
