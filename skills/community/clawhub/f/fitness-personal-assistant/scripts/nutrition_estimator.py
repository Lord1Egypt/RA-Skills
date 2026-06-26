#!/usr/bin/env python3
"""
Nutrition Estimator - 营养估算引擎
支持：
1. OpenFoodFacts API（全球食品数据库）
2. 中文食物规则库（本地）
3. 交互式询问用户（当无法识别时）
"""

import json
import requests
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# ================= OpenFoodFacts API =================
OFF_API_BASE = "https://world.openfoodfacts.org/cgi/search.pl"

def query_openfoodfacts(product_name: str, language: str = "zh") -> Optional[Dict]:
    """
    查询 OpenFoodFacts API 获取营养数据
    
    Args:
        product_name: 产品名称（英文或中文）
        language: 返回语言偏好
    
    Returns:
        营养数据字典或 None
    """
    try:
        params = {
            "search_terms": product_name,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 1,
        }
        
        response = requests.get(OFF_API_BASE, params=params, timeout=5)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        products = data.get("products", [])
        
        if not products:
            return None
        
        product = products[0]
        
        # 提取营养数据（每 100g）
        nutrition = product.get("nutriments", {})
        
        return {
            "calories": nutrition.get("energy-kcal_100g") or nutrition.get("energy-kcal") or 0,
            "protein": nutrition.get("proteins_100g") or nutrition.get("proteins") or 0,
            "carbs": nutrition.get("carbohydrates_100g") or nutrition.get("carbohydrates") or 0,
            "fat": nutrition.get("fat_100g") or nutrition.get("fat") or 0,
            "fiber": nutrition.get("fiber_100g") or nutrition.get("fiber") or 0,
            "sodium": nutrition.get("sodium_100g") or nutrition.get("sodium") or 0,
            "source": "OpenFoodFacts",
            "product_name": product.get("product_name", product_name),
        }
    
    except Exception as e:
        print(f"⚠️ OpenFoodFacts 查询失败：{e}")
        return None

# ================= 中文食物规则库 =================
CHINESE_FOOD_RULES = {
    # 肉类（每 100g）
    "鸡胸肉": {"calories": 110, "protein": 23, "carbs": 0, "fat": 1.5},
    "鸡胸": {"calories": 110, "protein": 23, "carbs": 0, "fat": 1.5},
    "鸡腿": {"calories": 180, "protein": 18, "carbs": 0, "fat": 11},
    "鸡翅": {"calories": 200, "protein": 18, "carbs": 0, "fat": 14},
    "鸡肉": {"calories": 150, "protein": 20, "carbs": 0, "fat": 8},
    "鸡": {"calories": 150, "protein": 20, "carbs": 0, "fat": 8},
    
    "牛肉": {"calories": 200, "protein": 22, "carbs": 0, "fat": 12},
    "牛排": {"calories": 250, "protein": 22, "carbs": 0, "fat": 18},
    "牛腩": {"calories": 280, "protein": 18, "carbs": 0, "fat": 22},
    "牛": {"calories": 180, "protein": 20, "carbs": 0, "fat": 10},
    
    "猪肉": {"calories": 250, "protein": 20, "carbs": 0, "fat": 18},
    "猪": {"calories": 220, "protein": 18, "carbs": 0, "fat": 15},
    "五花肉": {"calories": 350, "protein": 15, "carbs": 0, "fat": 30},
    "瘦肉": {"calories": 180, "protein": 22, "carbs": 0, "fat": 8},
    
    "羊肉": {"calories": 220, "protein": 20, "carbs": 0, "fat": 15},
    "羊": {"calories": 200, "protein": 19, "carbs": 0, "fat": 13},
    
    "鱼肉": {"calories": 120, "protein": 20, "carbs": 0, "fat": 3},
    "鱼": {"calories": 120, "protein": 20, "carbs": 0, "fat": 3},
    "三文鱼": {"calories": 200, "protein": 20, "carbs": 0, "fat": 13},
    "鳕鱼": {"calories": 90, "protein": 18, "carbs": 0, "fat": 1},
    
    "虾": {"calories": 100, "protein": 20, "carbs": 0, "fat": 1},
    "虾仁": {"calories": 100, "protein": 20, "carbs": 0, "fat": 1},
    "蟹": {"calories": 90, "protein": 18, "carbs": 0, "fat": 1},
    "贝": {"calories": 80, "protein": 15, "carbs": 3, "fat": 1},
    
    # 蛋奶（每 100g/ml）
    "鸡蛋": {"calories": 155, "protein": 13, "carbs": 1, "fat": 11},
    "蛋": {"calories": 155, "protein": 13, "carbs": 1, "fat": 11},
    "蛋黄": {"calories": 320, "protein": 16, "carbs": 4, "fat": 27},
    "蛋白": {"calories": 50, "protein": 11, "carbs": 1, "fat": 0},
    
    "牛奶": {"calories": 50, "protein": 3.5, "carbs": 5, "fat": 1.5},
    "奶": {"calories": 60, "protein": 3, "carbs": 5, "fat": 2},
    "酸奶": {"calories": 70, "protein": 3, "carbs": 10, "fat": 2},
    "奶酪": {"calories": 350, "protein": 25, "carbs": 3, "fat": 28},
    "芝士": {"calories": 350, "protein": 25, "carbs": 3, "fat": 28},
    
    "豆浆": {"calories": 30, "protein": 3, "carbs": 2, "fat": 1.5},
    "豆腐": {"calories": 80, "protein": 8, "carbs": 2, "fat": 4},
    
    # 主食（每 100g）
    "米饭": {"calories": 130, "protein": 2.5, "carbs": 28, "fat": 0.5},
    "饭": {"calories": 130, "protein": 2.5, "carbs": 28, "fat": 0.5},
    "白米饭": {"calories": 130, "protein": 2.5, "carbs": 28, "fat": 0.5},
    "糙米饭": {"calories": 110, "protein": 2.5, "carbs": 23, "fat": 1},
    
    "面条": {"calories": 110, "protein": 3, "carbs": 25, "fat": 0.5},
    "面": {"calories": 120, "protein": 3, "carbs": 26, "fat": 1},
    "拉面": {"calories": 130, "protein": 4, "carbs": 28, "fat": 1},
    "意面": {"calories": 140, "protein": 5, "carbs": 28, "fat": 1},
    "意大利面": {"calories": 140, "protein": 5, "carbs": 28, "fat": 1},
    
    "面包": {"calories": 270, "protein": 8, "carbs": 50, "fat": 4},
    "吐司": {"calories": 280, "protein": 8, "carbs": 52, "fat": 5},
    "全麦面包": {"calories": 250, "protein": 9, "carbs": 45, "fat": 3},
    "馒头": {"calories": 220, "protein": 7, "carbs": 47, "fat": 1},
    "包子": {"calories": 200, "protein": 7, "carbs": 35, "fat": 5},
    "饺子": {"calories": 200, "protein": 8, "carbs": 25, "fat": 8},
    "馄饨": {"calories": 180, "protein": 7, "carbs": 22, "fat": 7},
    
    "粥": {"calories": 50, "protein": 1.5, "carbs": 10, "fat": 0.5},
    "小米粥": {"calories": 45, "protein": 1.5, "carbs": 9, "fat": 0.5},
    "燕麦": {"calories": 380, "protein": 13, "carbs": 67, "fat": 7},
    "麦片": {"calories": 350, "protein": 12, "carbs": 65, "fat": 6},
    
    "玉米": {"calories": 110, "protein": 4, "carbs": 23, "fat": 1.5},
    "红薯": {"calories": 90, "protein": 2, "carbs": 21, "fat": 0.5},
    "土豆": {"calories": 80, "protein": 2, "carbs": 17, "fat": 0.2},
    "山药": {"calories": 60, "protein": 2, "carbs": 14, "fat": 0.2},
    
    # 蔬菜（每 100g）
    "蔬菜": {"calories": 30, "protein": 2, "carbs": 5, "fat": 0.5},
    "菜": {"calories": 35, "protein": 2, "carbs": 6, "fat": 0.5},
    "西兰花": {"calories": 35, "protein": 3, "carbs": 7, "fat": 0.5},
    "菠菜": {"calories": 25, "protein": 3, "carbs": 4, "fat": 0.5},
    "生菜": {"calories": 15, "protein": 1.5, "carbs": 3, "fat": 0.2},
    "白菜": {"calories": 20, "protein": 1.5, "carbs": 4, "fat": 0.2},
    "青菜": {"calories": 25, "protein": 2, "carbs": 4, "fat": 0.5},
    
    "番茄": {"calories": 20, "protein": 1, "carbs": 4, "fat": 0.2},
    "西红柿": {"calories": 20, "protein": 1, "carbs": 4, "fat": 0.2},
    "黄瓜": {"calories": 15, "protein": 1, "carbs": 3, "fat": 0.2},
    "胡萝卜": {"calories": 40, "protein": 1, "carbs": 10, "fat": 0.2},
    "茄子": {"calories": 25, "protein": 1, "carbs": 6, "fat": 0.2},
    "辣椒": {"calories": 30, "protein": 1.5, "carbs": 6, "fat": 0.5},
    "蘑菇": {"calories": 25, "protein": 3, "carbs": 4, "fat": 0.5},
    "金针菇": {"calories": 30, "protein": 3, "carbs": 6, "fat": 0.5},
    "香菇": {"calories": 35, "protein": 3, "carbs": 7, "fat": 0.5},
    
    "洋葱": {"calories": 40, "protein": 1, "carbs": 9, "fat": 0.2},
    "大蒜": {"calories": 150, "protein": 6, "carbs": 33, "fat": 0.5},
    "姜": {"calories": 80, "protein": 2, "carbs": 18, "fat": 0.8},
    
    # 水果（每 100g）
    "水果": {"calories": 60, "protein": 1, "carbs": 15, "fat": 0.5},
    "苹果": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
    "香蕉": {"calories": 90, "protein": 1, "carbs": 23, "fat": 0.3},
    "橙子": {"calories": 47, "protein": 1, "carbs": 12, "fat": 0.1},
    "橘子": {"calories": 45, "protein": 0.8, "carbs": 11, "fat": 0.2},
    "梨": {"calories": 50, "protein": 0.5, "carbs": 13, "fat": 0.2},
    "葡萄": {"calories": 70, "protein": 0.7, "carbs": 18, "fat": 0.5},
    "西瓜": {"calories": 30, "protein": 0.6, "carbs": 8, "fat": 0.2},
    "草莓": {"calories": 35, "protein": 0.7, "carbs": 8, "fat": 0.3},
    "蓝莓": {"calories": 60, "protein": 0.7, "carbs": 14, "fat": 0.3},
    "芒果": {"calories": 60, "protein": 0.8, "carbs": 15, "fat": 0.4},
    "菠萝": {"calories": 50, "protein": 0.5, "carbs": 13, "fat": 0.2},
    "猕猴桃": {"calories": 60, "protein": 1, "carbs": 14, "fat": 0.5},
    "柠檬": {"calories": 30, "protein": 1, "carbs": 9, "fat": 0.3},
    "桃子": {"calories": 40, "protein": 0.9, "carbs": 10, "fat": 0.2},
    "李子": {"calories": 45, "protein": 0.7, "carbs": 11, "fat": 0.3},
    
    # 快餐/加工食品（每 100g）
    "方便面": {"calories": 450, "protein": 10, "carbs": 55, "fat": 22},
    "汉堡": {"calories": 280, "protein": 13, "carbs": 30, "fat": 12},
    "披萨": {"calories": 270, "protein": 11, "carbs": 33, "fat": 10},
    "炸鸡": {"calories": 300, "protein": 18, "carbs": 10, "fat": 22},
    "薯条": {"calories": 320, "protein": 4, "carbs": 40, "fat": 16},
    "可乐": {"calories": 42, "protein": 0, "carbs": 11, "fat": 0},
    "雪碧": {"calories": 40, "protein": 0, "carbs": 10, "fat": 0},
    "果汁": {"calories": 50, "protein": 0.5, "carbs": 12, "fat": 0.2},
    
    # 零食（每 100g）
    "饼干": {"calories": 450, "protein": 7, "carbs": 65, "fat": 18},
    "巧克力": {"calories": 550, "protein": 8, "carbs": 60, "fat": 30},
    "蛋糕": {"calories": 350, "protein": 6, "carbs": 50, "fat": 15},
    "冰淇淋": {"calories": 200, "protein": 4, "carbs": 25, "fat": 10},
    "坚果": {"calories": 600, "protein": 20, "carbs": 20, "fat": 50},
    "花生": {"calories": 570, "protein": 26, "carbs": 16, "fat": 49},
    "瓜子": {"calories": 600, "protein": 23, "carbs": 20, "fat": 50},
    
    # 调料/油脂（每 100g）
    "油": {"calories": 900, "protein": 0, "carbs": 0, "fat": 100},
    "酱油": {"calories": 60, "protein": 8, "carbs": 6, "fat": 0},
    "醋": {"calories": 20, "protein": 0, "carbs": 1, "fat": 0},
    "糖": {"calories": 390, "protein": 0, "carbs": 100, "fat": 0},
    "盐": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0},
    "沙拉酱": {"calories": 450, "protein": 1, "carbs": 10, "fat": 45},
    "花生酱": {"calories": 590, "protein": 25, "carbs": 20, "fat": 50},
}

# ================= 单位换算 =================
UNIT_TO_GRAMS = {
    "g": 1,
    "ml": 1,  # 液体近似 1g/ml
    "l": 1000,
    "kg": 1000,
    "个": 50,  # 平均估算（鸡蛋约 50-60g）
    "只": 50,
    "碗": 150,
    "杯": 250,
    "瓶": 250,
    "包": 100,
    "袋": 100,
    "片": 30,
    "块": 50,
    "勺": 15,
    "汤匙": 15,
    "茶匙": 5,
}

# 中文数字转换
CHINESE_TO_NUM = {
    "一": 1, "二": 2, "两": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
    "百": 100, "千": 1000,
}

class NutritionEstimator:
    """营养估算引擎"""
    
    def __init__(self, use_off_api: bool = True, interactive: bool = False):
        """
        Args:
            use_off_api: 是否使用 OpenFoodFacts API
            interactive: 是否在无法识别时询问用户
        """
        self.use_off_api = use_off_api
        self.interactive = interactive
        self.cache = {}  # 缓存查询结果
    
    def parse_food_quantity(self, text: str) -> List[Dict]:
        """
        解析食物文本，提取食物名称和重量
        
        支持格式：
        - "250ml 牛奶"
        - "200 克鸡胸肉"
        - "两个鸡蛋"
        - "一碗米饭"
        """
        foods = []
        
        # 先按"和"、"、"分割成多个食物
        parts = re.split(r'[和，,]', text)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # 清理单位
            part = part.replace("克", "g").replace("毫升", "ml").replace("升", "l")
            
            found = self._parse_single_food(part)
            if found:
                foods.extend(found)
            else:
                # 如果完全无法解析，返回整个部分作为未知食物
                foods.append({
                    "name": part.strip(),
                    "grams": 100,  # 默认 100g
                    "source": "unknown"
                })
        
        return foods
    
    def _parse_single_food(self, part: str) -> Optional[List[Dict]]:
        """解析单个食物部分"""
        foods = []
        
        # 匹配模式
        patterns = [
            # 数字 + 单位 + 食物名
            (r'(\d+(?:\.\d+)?)\s*(g|ml|l|kg)\s*([\u4e00-\u9fa5a-zA-Z]+)', 3),
            # 中文数字 + 个/碗/杯 + 食物名
            (r'([一二三四五六七八九十]+) 个 ([\u4e00-\u9fa5a-zA-Z]+)', 2),
            (r'([一二三四五六七八九十]+) 碗 ([\u4e00-\u9fa5a-zA-Z]+)', 2),
            (r'([一二三四五六七八九十]+) 杯 ([\u4e00-\u9fa5a-zA-Z]+)', 2),
            (r'([一二三四五六七八九十]+) 瓶 ([\u4e00-\u9fa5a-zA-Z]+)', 2),
            (r'([一二三四五六七八九十]+) 包 ([\u4e00-\u9fa5a-zA-Z]+)', 2),
            # 食物名 + 数字 + 单位
            (r'([\u4e00-\u9fa5a-zA-Z]+)\s*(\d+(?:\.\d+)?)\s*(g|ml)', 3),
        ]
        
        for pattern, group_count in patterns:
            matches = re.findall(pattern, part)
            for match in matches:
                if group_count == 3:
                    qty_str, unit, food_name = match
                    qty = self._parse_quantity(qty_str)
                    grams = qty * UNIT_TO_GRAMS.get(unit, 1)
                elif group_count == 2:
                    qty_str, food_name = match
                    qty = CHINESE_TO_NUM.get(qty_str, 1)
                    unit = self._detect_unit_from_pattern(pattern)
                    grams = qty * UNIT_TO_GRAMS.get(unit, 100)
                else:
                    continue
                
                foods.append({
                    "name": food_name.strip(),
                    "grams": grams,
                    "source": "parsed"
                })
                return foods  # 匹配成功就返回
        
        return None
    
    def _parse_quantity(self, qty_str: str) -> float:
        """解析数量（支持中文数字）"""
        if qty_str in CHINESE_TO_NUM:
            return float(CHINESE_TO_NUM[qty_str])
        try:
            return float(qty_str)
        except:
            return 1.0
    
    def _detect_unit_from_pattern(self, pattern: str) -> str:
        """从匹配模式推断单位"""
        if "个" in pattern:
            return "个"
        elif "碗" in pattern:
            return "碗"
        elif "杯" in pattern:
            return "杯"
        elif "瓶" in pattern:
            return "瓶"
        elif "包" in pattern:
            return "包"
        return "个"
    
    def estimate_nutrition(self, food_name: str, grams: float, use_off: bool = True) -> Dict:
        """
        估算食物营养
        
        策略：
        1. 先查本地缓存
        2. 查询 OpenFoodFacts API（如果启用）
        3. 查询中文食物规则库
        4. 询问用户（如果交互式启用）
        5. 使用默认值
        """
        cache_key = f"{food_name}_{grams}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 策略 1: OpenFoodFacts API
        if use_off and self.use_off_api:
            off_result = query_openfoodfacts(food_name)
            if off_result:
                # 按比例计算
                ratio = grams / 100
                result = {
                    "calories": off_result["calories"] * ratio,
                    "protein": off_result["protein"] * ratio,
                    "carbs": off_result["carbs"] * ratio,
                    "fat": off_result["fat"] * ratio,
                    "source": f"OpenFoodFacts: {off_result['product_name']}",
                }
                self.cache[cache_key] = result
                return result
        
        # 策略 2: 中文食物规则库（优先匹配更长的关键词）
        food_name_lower = food_name.lower()
        sorted_keywords = sorted(CHINESE_FOOD_RULES.keys(), key=len, reverse=True)
        
        for keyword in sorted_keywords:
            if keyword in food_name_lower:
                nutrition = CHINESE_FOOD_RULES[keyword]
                ratio = grams / 100
                result = {
                    "calories": nutrition["calories"] * ratio,
                    "protein": nutrition["protein"] * ratio,
                    "carbs": nutrition["carbs"] * ratio,
                    "fat": nutrition["fat"] * ratio,
                    "source": f"中文规则库：{keyword}",
                }
                self.cache[cache_key] = result
                return result
        
        # 策略 3: 交互式询问
        if self.interactive:
            user_input = self._ask_user(food_name, grams)
            if user_input:
                self.cache[cache_key] = user_input
                return user_input
        
        # 策略 4: 默认值
        ratio = grams / 100
        result = {
            "calories": 150 * ratio,
            "protein": 10 * ratio,
            "carbs": 20 * ratio,
            "fat": 5 * ratio,
            "source": "默认估算",
            "warning": f"未知食物：{food_name}"
        }
        self.cache[cache_key] = result
        return result
    
    def _ask_user(self, food_name: str, grams: float) -> Optional[Dict]:
        """询问用户营养信息"""
        print(f"\n❓ 未识别食物：{food_name} ({grams}g)")
        print("请选择:")
        print("  1. 手动输入营养数据")
        print("  2. 使用默认估算（150kcal/100g）")
        print("  3. 跳过此食物")
        
        choice = input("请输入选项 (1/2/3): ").strip()
        
        if choice == "1":
            try:
                calories = float(input("  热量 (kcal/100g): "))
                protein = float(input("  蛋白质 (g/100g): "))
                carbs = float(input("  碳水 (g/100g): "))
                fat = float(input("  脂肪 (g/100g): "))
                
                ratio = grams / 100
                return {
                    "calories": calories * ratio,
                    "protein": protein * ratio,
                    "carbs": carbs * ratio,
                    "fat": fat * ratio,
                    "source": "用户输入",
                }
            except:
                print("⚠️ 输入无效，使用默认估算")
        
        elif choice == "2":
            pass  # 使用默认
        
        elif choice == "3":
            return None
        
        # 默认估算
        ratio = grams / 100
        return {
            "calories": 150 * ratio,
            "protein": 10 * ratio,
            "carbs": 20 * ratio,
            "fat": 5 * ratio,
            "source": "默认估算",
        }
    
    def calculate_meal_nutrition(self, foods: List[Dict]) -> Dict:
        """计算整餐营养总和"""
        total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        sources = []
        
        for food in foods:
            nutrition = self.estimate_nutrition(
                food["name"],
                food["grams"],
                use_off=self.use_off_api
            )
            
            for key in total:
                total[key] += nutrition[key]
            
            if "source" in nutrition:
                sources.append(nutrition["source"])
        
        total["sources"] = sources
        return total


# ================= 测试 =================
if __name__ == "__main__":
    estimator = NutritionEstimator(use_off_api=True, interactive=False)
    
    # 测试解析
    test_cases = [
        "250ml 牛奶",
        "200 克鸡胸肉",
        "两个鸡蛋",
        "一碗米饭",
        "早餐：250ml 牛奶和方便面",
        "300g 牛肉和 200 克米饭",
    ]
    
    for text in test_cases:
        print(f"\n{'='*50}")
        print(f"输入：{text}")
        print("-" * 50)
        
        foods = estimator.parse_food_quantity(text)
        print(f"解析结果：{len(foods)} 种食物")
        for food in foods:
            print(f"  - {food['name']}: {food['grams']:.0f}g")
        
        nutrition = estimator.calculate_meal_nutrition(foods)
        print(f"营养总计:")
        print(f"  热量：{nutrition['calories']:.0f} kcal")
        print(f"  蛋白质：{nutrition['protein']:.1f}g")
        print(f"  碳水：{nutrition['carbs']:.1f}g")
        print(f"  脂肪：{nutrition['fat']:.1f}g")
        print(f"  数据来源：{', '.join(nutrition.get('sources', []))}")
