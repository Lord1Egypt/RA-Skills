#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍳 Recipe Finder - 菜谱助手（优化版）
功能：食材推荐、菜谱详情、营养分析、购物清单、难度筛选
"""

import json
import random
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent
FAVORITES_FILE = DATA_DIR / "favorites.json"
SHOPPING_LIST_FILE = DATA_DIR / "shopping_list.json"

# ========== 扩展菜谱数据库 ==========

RECIPES = {
    "家常菜": [
        {
            "name": "番茄炒蛋",
            "difficulty": 1,
            "time": 10,
            "ingredients": ["番茄 2 个", "鸡蛋 3 个", "葱花", "盐", "糖"],
            "steps": [
                "番茄切块，鸡蛋打散加少许盐",
                "热锅凉油，倒入蛋液炒至凝固盛出",
                "锅中留底油，炒番茄出汁",
                "加入鸡蛋翻炒均匀",
                "加盐、少许糖调味",
                "撒葱花出锅"
            ],
            "tips": "鸡蛋加少许水更嫩滑，番茄要炒出汁",
            "calories": 200,
            "protein": 12,
            "tags": ["快手", "下饭", "素食"]
        },
        {
            "name": "宫保鸡丁",
            "difficulty": 3,
            "time": 20,
            "ingredients": ["鸡胸肉 300g", "花生米", "干辣椒", "葱姜蒜", "花椒"],
            "steps": [
                "鸡肉切丁，加料酒、淀粉腌制 10 分钟",
                "花生米炸香备用",
                "炒香干辣椒和花椒",
                "下鸡丁翻炒至变色",
                "加宫保酱汁（生抽、醋、糖、淀粉）",
                "出锅前加花生米"
            ],
            "tips": "鸡肉用淀粉腌制更嫩，火候要大",
            "calories": 350,
            "protein": 25,
            "tags": ["川菜", "下饭", "微辣"]
        },
        {
            "name": "红烧肉",
            "difficulty": 4,
            "time": 60,
            "ingredients": ["五花肉 500g", "冰糖", "料酒", "生抽", "老抽", "八角", "桂皮"],
            "steps": [
                "五花肉切块，冷水下锅焯水",
                "炒糖色：冰糖小火炒至焦糖色",
                "下肉块翻炒上色",
                "加料酒、生抽、老抽",
                "加开水没过肉，加八角桂皮",
                "小火炖 40 分钟，大火收汁"
            ],
            "tips": "炒糖色不要炒糊，要用小火",
            "calories": 500,
            "protein": 20,
            "tags": ["硬菜", "下饭", "经典"]
        },
        {
            "name": "鱼香肉丝",
            "difficulty": 3,
            "time": 25,
            "ingredients": ["猪里脊", "木耳", "胡萝卜", "青椒", "豆瓣酱"],
            "steps": [
                "肉切丝，加淀粉腌制",
                "蔬菜切丝",
                "调鱼香汁（醋、糖、生抽、淀粉）",
                "炒肉丝盛出",
                "炒香豆瓣酱，下蔬菜",
                "加肉丝和鱼香汁翻炒"
            ],
            "tips": "鱼香汁比例：醋 3 勺、糖 2 勺、生抽 1 勺",
            "calories": 320,
            "protein": 22,
            "tags": ["川菜", "下饭", "微辣"]
        }
    ],
    "汤类": [
        {
            "name": "番茄蛋花汤",
            "difficulty": 1,
            "time": 10,
            "ingredients": ["番茄 2 个", "鸡蛋 2 个", "葱花", "盐"],
            "steps": [
                "番茄切块",
                "水烧开下番茄煮 2 分钟",
                "淋入蛋液，用筷子搅散",
                "加盐、香油调味",
                "撒葱花"
            ],
            "tips": "蛋液要慢慢淋，用筷子搅散成蛋花",
            "calories": 100,
            "protein": 8,
            "tags": ["快手", "清淡", "素食"]
        },
        {
            "name": "玉米排骨汤",
            "difficulty": 2,
            "time": 90,
            "ingredients": ["排骨 500g", "玉米 2 根", "胡萝卜", "姜片"],
            "steps": [
                "排骨焯水去腥",
                "玉米切段，胡萝卜切块",
                "排骨加水、姜片，大火烧开",
                "转小火炖 40 分钟",
                "加玉米胡萝卜",
                "再炖 30 分钟，加盐调味"
            ],
            "tips": "排骨要冷水下锅焯水",
            "calories": 280,
            "protein": 28,
            "tags": ["营养", "清淡", "滋补"]
        }
    ],
    "素食": [
        {
            "name": "麻婆豆腐",
            "difficulty": 2,
            "time": 15,
            "ingredients": ["嫩豆腐", "豆瓣酱", "花椒粉", "葱姜蒜", "淀粉"],
            "steps": [
                "豆腐切块，开水焯一下",
                "炒香豆瓣酱",
                "下豆腐轻轻翻炒",
                "加水煮 3 分钟",
                "勾芡收汁",
                "撒花椒粉和葱花"
            ],
            "tips": "豆腐焯水去腥，翻炒要轻",
            "calories": 250,
            "protein": 15,
            "tags": ["川菜", "下饭", "素食", "微辣"]
        },
        {
            "name": "地三鲜",
            "difficulty": 2,
            "time": 20,
            "ingredients": ["土豆", "茄子", "青椒", "葱姜蒜"],
            "steps": [
                "土豆茄子切块，青椒切块",
                "土豆炸至金黄",
                "茄子炸软",
                "炒香葱姜蒜",
                "下三鲜翻炒",
                "加生抽、盐、糖调味"
            ],
            "tips": "茄子先炸不吸油",
            "calories": 300,
            "protein": 5,
            "tags": ["东北菜", "下饭", "素食"]
        }
    ],
    "快手菜": [
        {
            "name": "蒜蓉西兰花",
            "difficulty": 1,
            "time": 8,
            "ingredients": ["西兰花", "大蒜", "盐"],
            "steps": [
                "西兰花切小朵，焯水 1 分钟",
                "大蒜切末",
                "热锅凉油，炒香蒜末",
                "下西兰花翻炒",
                "加盐调味"
            ],
            "tips": "西兰花焯水时间不要太长",
            "calories": 80,
            "protein": 4,
            "tags": ["快手", "清淡", "素食", "减脂"]
        }
    ]
}

# ========== 食材匹配（扩展版） ==========

INGREDIENT_MAP = {
    "番茄": ["番茄炒蛋", "番茄蛋花汤"],
    "西红柿": ["番茄炒蛋", "番茄蛋花汤"],
    "鸡蛋": ["番茄炒蛋", "番茄蛋花汤"],
    "土豆": ["土豆烧牛肉", "地三鲜"],
    "马铃薯": ["土豆烧牛肉", "地三鲜"],
    "牛肉": ["土豆烧牛肉"],
    "豆腐": ["麻婆豆腐"],
    "鸡肉": ["宫保鸡丁"],
    "鸡胸肉": ["宫保鸡丁"],
    "猪肉": ["红烧肉", "鱼香肉丝"],
    "五花肉": ["红烧肉"],
    "排骨": ["玉米排骨汤"],
    "西兰花": ["蒜蓉西兰花"],
    "茄子": ["地三鲜"],
    "青椒": ["鱼香肉丝", "地三鲜"],
    "玉米": ["玉米排骨汤"]
}

# ========== 营养建议 ==========

NUTRITION_TIPS = {
    "减脂": "选择低热量、高蛋白的菜谱，如蒜蓉西兰花、番茄蛋花汤",
    "增肌": "选择高蛋白菜谱，如宫保鸡丁、玉米排骨汤",
    "清淡": "选择清淡菜谱，如番茄蛋花汤、蒜蓉西兰花",
    "下饭": "选择口味浓郁的菜谱，如红烧肉、麻婆豆腐",
    "快手": "选择 15 分钟以内的菜谱，如番茄炒蛋、蒜蓉西兰花"
}


def load_json(filepath):
    """加载 JSON 文件"""
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"favorites": [], "shopping_list": []}


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def recommend_by_ingredients(ingredients):
    """根据食材推荐菜谱"""
    results = []
    for ing in ingredients:
        # 支持模糊匹配
        for key, recipes in INGREDIENT_MAP.items():
            if key in ing or ing in key:
                results.extend(recipes)
    
    # 去重
    return list(set(results))


def recommend_by_difficulty(difficulty):
    """根据难度推荐"""
    results = []
    for category, recipes in RECIPES.items():
        for recipe in recipes:
            if recipe["difficulty"] == difficulty:
                results.append(recipe)
    return results


def recommend_by_time(max_time):
    """根据时间推荐"""
    results = []
    for category, recipes in RECIPES.items():
        for recipe in recipes:
            if recipe["time"] <= max_time:
                results.append(recipe)
    return results


def recommend_by_tag(tag):
    """根据标签推荐"""
    results = []
    for category, recipes in RECIPES.items():
        for recipe in recipes:
            if tag in recipe.get("tags", []):
                results.append(recipe)
    return results


def get_recipe_detail(name):
    """获取菜谱详情"""
    for category, recipes in RECIPES.items():
        for recipe in recipes:
            if recipe["name"] == name:
                return recipe
    return None


def add_to_favorites(recipe_name):
    """添加到收藏"""
    data = load_json(FAVORITES_FILE)
    
    # 检查是否已存在
    for fav in data["favorites"]:
        if fav["name"] == recipe_name:
            return False, "已收藏过"
    
    recipe = get_recipe_detail(recipe_name)
    if recipe:
        data["favorites"].append({
            "name": recipe_name,
            "added_date": datetime.now().isoformat(),
            "cook_count": 0
        })
        save_json(FAVORITES_FILE, data)
        return True, "收藏成功"
    
    return False, "菜谱不存在"


def add_to_shopping_list(ingredients):
    """添加到购物清单"""
    data = load_json(SHOPPING_LIST_FILE)
    
    for ing in ingredients:
        if ing not in data["shopping_list"]:
            data["shopping_list"].append(ing)
    
    save_json(SHOPPING_LIST_FILE, data)
    return data["shopping_list"]


def get_shopping_list():
    """获取购物清单"""
    data = load_json(SHOPPING_LIST_FILE)
    return data.get("shopping_list", [])


def clear_shopping_list():
    """清空购物清单"""
    data = {"shopping_list": []}
    save_json(SHOPPING_LIST_FILE, data)
    return True


def get_nutrition_info(recipe):
    """获取营养信息"""
    info = f"""
📊 **营养信息**（每份）：
- 热量：{recipe.get('calories', 0)} 卡
- 蛋白质：{recipe.get('protein', 0)}g
"""
    return info


def format_recipe(recipe):
    """格式化菜谱"""
    difficulty = "⭐" * recipe["difficulty"]
    
    response = f"🍳 **{recipe['name']}**\n\n"
    response += f"难度：{difficulty}\n"
    response += f"时间：{recipe['time']}分钟\n"
    response += f"热量：{recipe['calories']}卡\n"
    
    if recipe.get("tags"):
        response += f"标签：{'、'.join(recipe['tags'])}\n"
    
    response += "\n" + get_nutrition_info(recipe)
    
    response += "📝 **食材**：\n"
    response += "、".join(recipe["ingredients"]) + "\n\n"
    
    response += "👨‍🍳 **步骤**：\n"
    for i, step in enumerate(recipe["steps"], 1):
        response += f"{i}. {step}\n"
    
    response += f"\n💡 **技巧**：{recipe['tips']}\n"
    
    return response


def format_recipe_simple(recipe):
    """简单格式化菜谱（用于列表）"""
    difficulty = "⭐" * recipe["difficulty"]
    return f"{recipe['name']} ({recipe['time']}分钟 | 难度：{difficulty} | {recipe['calories']}卡)"


def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # ========== 推荐菜谱 ==========
    
    # 今日推荐
    if "推荐" in query_lower or "吃什么" in query_lower:
        # 随机推荐 5 个
        all_recipes = []
        for category, recipes in RECIPES.items():
            all_recipes.extend(recipes)
        
        selected = random.sample(all_recipes, min(5, len(all_recipes)))
        
        response = "🍳 **今日推荐菜谱**：\n\n"
        for i, recipe in enumerate(selected, 1):
            response += f"{i}. {format_recipe_simple(recipe)}\n"
        
        return response
    
    # 根据食材推荐
    if "我有" in query_lower or "食材" in query_lower:
        ingredients = []
        for ing in INGREDIENT_MAP.keys():
            if ing in query_lower:
                ingredients.append(ing)
        
        if ingredients:
            results = recommend_by_ingredients(ingredients)
            response = f"🥔 用{','.join(ingredients)}可以做：\n\n"
            for name in results[:5]:
                recipe = get_recipe_detail(name)
                if recipe:
                    response += f"- {format_recipe_simple(recipe)}\n"
            return response
        
        return "😅 没找到匹配的食材，试试其他食材？"
    
    # 根据难度推荐
    if "简单" in query_lower or "容易" in query_lower:
        recipes = recommend_by_difficulty(1)
        response = "🍳 **简单菜谱**（⭐难度）：\n\n"
        for recipe in recipes:
            response += f"- {format_recipe_simple(recipe)}\n"
        return response
    
    if "难" in query_lower and ("一点" in query_lower or "一些" in query_lower):
        recipes = recommend_by_difficulty(3)
        response = "🍳 **有挑战性菜谱**（⭐⭐⭐难度）：\n\n"
        for recipe in recipes:
            response += f"- {format_recipe_simple(recipe)}\n"
        return response
    
    # 根据时间推荐
    if "分钟" in query_lower or "快" in query_lower:
        import re
        match = re.search(r'(\d+) 分钟', query)
        if match:
            max_time = int(match.group(1))
        else:
            max_time = 15
        
        recipes = recommend_by_time(max_time)
        response = f"🍳 **{max_time}分钟内菜谱**：\n\n"
        for recipe in recipes:
            response += f"- {format_recipe_simple(recipe)}\n"
        return response
    
    # 根据标签推荐
    for tag in ["减脂", "增肌", "清淡", "下饭", "快手"]:
        if tag in query_lower:
            recipes = recommend_by_tag(tag)
            response = f"🍳 **{tag}菜谱**：\n\n"
            for recipe in recipes:
                response += f"- {format_recipe_simple(recipe)}\n"
            response += f"\n💡 {NUTRITION_TIPS[tag]}"
            return response
    
    # ========== 菜谱详情 ==========
    
    # 查询具体菜谱
    for category, recipes in RECIPES.items():
        for recipe in recipes:
            if recipe["name"] in query_lower or query_lower in recipe["name"]:
                return format_recipe(recipe)
    
    # 怎么做 XXX
    if "怎么做" in query_lower or "做法" in query_lower:
        import re
        match = re.search(r'怎么做 (.+)', query)
        if match:
            recipe_name = match.group(1).strip()
            recipe = get_recipe_detail(recipe_name)
            if recipe:
                return format_recipe(recipe)
            return f"😅 没找到{recipe_name}的做法"
    
    # ========== 收藏功能 ==========
    
    if "收藏" in query_lower:
        import re
        match = re.search(r'收藏 (.+)', query)
        if match:
            recipe_name = match.group(1).strip()
            success, msg = add_to_favorites(recipe_name)
            return f"{'✅' if success else '⚠️'} {msg}"
    
    if "我的收藏" in query_lower or "收藏列表" in query_lower:
        data = load_json(FAVORITES_FILE)
        if data["favorites"]:
            response = "❤️ **我的收藏**：\n\n"
            for fav in data["favorites"]:
                response += f"- {fav['name']} (收藏于：{fav['added_date'][:10]})\n"
            return response
        return "❤️ 暂无收藏"
    
    # ========== 购物清单 ==========
    
    if "购物清单" in query_lower:
        if "添加" in query_lower:
            import re
            match = re.search(r'添加 (.+)', query)
            if match:
                ingredients = match.group(1).split("、")
                result = add_to_shopping_list(ingredients)
                return f"✅ 已添加到购物清单，共{len(result)}项"
        
        shopping_list = get_shopping_list()
        if shopping_list:
            response = "🛒 **购物清单**：\n\n"
            for item in shopping_list:
                response += f"- {item}\n"
            return response
        return "🛒 购物清单为空"
    
    if "清空清单" in query_lower:
        clear_shopping_list()
        return "✅ 购物清单已清空"
    
    # ========== 默认回复 ==========
    
    return """🍳 菜谱助手（优化版）

**功能**：

🥘 菜谱推荐
1. 今日推荐 - "今天吃什么"
2. 食材推荐 - "我有番茄和鸡蛋"
3. 难度推荐 - "简单的菜谱"
4. 时间推荐 - "15 分钟内的菜"
5. 标签推荐 - "减脂菜谱"

📖 菜谱详情
6. 做法查询 - "怎么做红烧肉"
7. 菜谱详情 - "番茄炒蛋的做法"

❤️ 收藏功能
8. 收藏菜谱 - "收藏番茄炒蛋"
9. 我的收藏 - "查看收藏"

🛒 购物清单
10. 添加食材 - "添加购物清单：番茄、鸡蛋"
11. 查看清单 - "购物清单"
12. 清空清单 - "清空购物清单"

**菜系**：家常菜、汤类、素食、快手菜
**难度**：⭐ (简单) - ⭐⭐⭐⭐⭐ (困难)
**标签**：减脂、增肌、清淡、下饭、快手

告诉我你想吃什么？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("🍳 菜谱助手 - 测试")
    print("=" * 60)
    
    print("\n测试 1: 今日推荐")
    print(main("今天吃什么"))
    
    print("\n" + "=" * 60)
    print("测试 2: 食材推荐")
    print(main("我有番茄和鸡蛋"))
    
    print("\n" + "=" * 60)
    print("测试 3: 菜谱详情")
    print(main("番茄炒蛋怎么做"))
