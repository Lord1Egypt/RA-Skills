#!/usr/bin/env python3
"""
食品营养数据库查询引擎
- 主数据源: TianAPI (在线)
- 备用数据: 内置常见食物库 (离线)
- 缓存机制: 查询结果自动缓存
"""

import json
import os
import hashlib
from pathlib import Path
from typing import Optional, Dict, List

# --- 内置常见食物数据库 (中国膳食常见食物, 每100g可食部) ---
# 数据来源: 《中国食物成分表标准版(第6版)》
BUILTIN_FOODS: Dict[str, dict] = {
    # ===== 谷类 =====
    "米饭": {"energy": 116, "protein": 2.6, "fat": 0.3, "carbs": 25.9, "fiber": 0.3, "category": "谷类"},
    "馒头": {"energy": 223, "protein": 7.0, "fat": 1.1, "carbs": 45.0, "fiber": 1.3, "category": "谷类"},
    "面条": {"energy": 284, "protein": 8.3, "fat": 0.7, "carbs": 61.0, "fiber": 1.5, "category": "谷类"},
    "小米粥": {"energy": 46, "protein": 1.4, "fat": 0.7, "carbs": 8.4, "fiber": 0.2, "category": "谷类"},
    "全麦面包": {"energy": 246, "protein": 9.7, "fat": 3.1, "carbs": 43.0, "fiber": 6.0, "category": "谷类"},
    "燕麦片": {"energy": 367, "protein": 13.5, "fat": 6.7, "carbs": 61.6, "fiber": 10.6, "category": "谷类"},
    "红薯": {"energy": 86, "protein": 1.6, "fat": 0.1, "carbs": 20.1, "fiber": 2.8, "category": "薯类"},
    "土豆": {"energy": 76, "protein": 2.0, "fat": 0.2, "carbs": 17.0, "fiber": 2.0, "category": "薯类"},
    "玉米": {"energy": 112, "protein": 4.0, "fat": 1.2, "carbs": 22.8, "fiber": 2.9, "category": "谷类"},

    # ===== 肉类 =====
    "鸡胸肉": {"energy": 133, "protein": 31.0, "fat": 1.2, "carbs": 0, "fiber": 0, "category": "禽肉"},
    "鸡腿肉": {"energy": 181, "protein": 16.0, "fat": 13.0, "carbs": 0, "fiber": 0, "category": "禽肉"},
    "鸡翅": {"energy": 194, "protein": 17.4, "fat": 13.5, "carbs": 0, "fiber": 0, "category": "禽肉"},
    "猪瘦肉": {"energy": 143, "protein": 20.3, "fat": 6.2, "carbs": 1.5, "fiber": 0, "category": "畜肉"},
    "猪五花肉": {"energy": 395, "protein": 9.3, "fat": 37.0, "carbs": 2.4, "fiber": 0, "category": "畜肉"},
    "猪排骨": {"energy": 264, "protein": 18.3, "fat": 20.4, "carbs": 1.7, "fiber": 0, "category": "畜肉"},
    "牛瘦肉": {"energy": 106, "protein": 20.2, "fat": 2.3, "carbs": 1.2, "fiber": 0, "category": "畜肉"},
    "牛腩": {"energy": 125, "protein": 19.9, "fat": 4.2, "carbs": 2.0, "fiber": 0, "category": "畜肉"},
    "羊瘦肉": {"energy": 118, "protein": 20.5, "fat": 3.9, "carbs": 0.2, "fiber": 0, "category": "畜肉"},
    "鸭肉": {"energy": 240, "protein": 15.5, "fat": 19.7, "carbs": 0.2, "fiber": 0, "category": "禽肉"},

    # ===== 水产 =====
    "鲈鱼": {"energy": 105, "protein": 18.6, "fat": 3.4, "carbs": 0, "fiber": 0, "category": "水产"},
    "三文鱼": {"energy": 139, "protein": 17.2, "fat": 7.8, "carbs": 0, "fiber": 0, "category": "水产"},
    "虾仁": {"energy": 99, "protein": 18.6, "fat": 1.7, "carbs": 2.7, "fiber": 0, "category": "水产"},
    "带鱼": {"energy": 127, "protein": 17.7, "fat": 4.9, "carbs": 3.1, "fiber": 0, "category": "水产"},

    # ===== 蛋奶 =====
    "鸡蛋": {"energy": 144, "protein": 13.3, "fat": 8.8, "carbs": 2.8, "fiber": 0, "category": "蛋类"},
    "水煮蛋": {"energy": 144, "protein": 13.3, "fat": 8.8, "carbs": 2.8, "fiber": 0, "category": "蛋类"},
    "煎蛋": {"energy": 196, "protein": 12.5, "fat": 15.0, "carbs": 1.5, "fiber": 0, "category": "蛋类"},
    "牛奶": {"energy": 54, "protein": 3.0, "fat": 3.2, "carbs": 4.8, "fiber": 0, "category": "奶类"},
    "全脂牛奶": {"energy": 61, "protein": 3.0, "fat": 3.5, "carbs": 4.8, "fiber": 0, "category": "奶类"},
    "脱脂牛奶": {"energy": 35, "protein": 3.0, "fat": 0.1, "carbs": 5.0, "fiber": 0, "category": "奶类"},
    "酸奶": {"energy": 72, "protein": 2.5, "fat": 2.7, "carbs": 9.3, "fiber": 0, "category": "奶类"},
    "豆浆": {"energy": 31, "protein": 3.0, "fat": 1.6, "carbs": 1.1, "fiber": 0.5, "category": "豆类"},
    "豆腐": {"energy": 81, "protein": 8.1, "fat": 3.7, "carbs": 4.2, "fiber": 0.4, "category": "豆类"},

    # ===== 蔬菜 =====
    "西兰花": {"energy": 34, "protein": 2.8, "fat": 0.4, "carbs": 6.6, "fiber": 2.6, "category": "蔬菜"},
    "菠菜": {"energy": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6, "fiber": 2.2, "category": "蔬菜"},
    "番茄": {"energy": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.5, "fiber": 1.2, "category": "蔬菜"},
    "黄瓜": {"energy": 15, "protein": 0.7, "fat": 0.1, "carbs": 2.9, "fiber": 0.5, "category": "蔬菜"},
    "胡萝卜": {"energy": 41, "protein": 0.9, "fat": 0.2, "carbs": 9.6, "fiber": 1.1, "category": "蔬菜"},
    "大白菜": {"energy": 13, "protein": 1.5, "fat": 0.2, "carbs": 2.2, "fiber": 0.8, "category": "蔬菜"},
    "生菜": {"energy": 15, "protein": 1.4, "fat": 0.3, "carbs": 2.0, "fiber": 1.3, "category": "蔬菜"},
    "茄子": {"energy": 25, "protein": 1.0, "fat": 0.2, "carbs": 5.9, "fiber": 1.4, "category": "蔬菜"},
    "芹菜": {"energy": 14, "protein": 0.7, "fat": 0.2, "carbs": 2.5, "fiber": 1.4, "category": "蔬菜"},
    "洋葱": {"energy": 40, "protein": 1.1, "fat": 0.1, "carbs": 9.3, "fiber": 1.7, "category": "蔬菜"},
    "青椒": {"energy": 20, "protein": 0.9, "fat": 0.2, "carbs": 4.6, "fiber": 1.2, "category": "蔬菜"},
    "蘑菇": {"energy": 22, "protein": 3.1, "fat": 0.3, "carbs": 3.3, "fiber": 1.0, "category": "菌藻"},

    # ===== 水果 =====
    "苹果": {"energy": 52, "protein": 0.3, "fat": 0.2, "carbs": 13.5, "fiber": 2.4, "category": "水果"},
    "香蕉": {"energy": 89, "protein": 1.1, "fat": 0.3, "carbs": 22.8, "fiber": 2.6, "category": "水果"},
    "橙子": {"energy": 47, "protein": 0.9, "fat": 0.1, "carbs": 11.8, "fiber": 2.4, "category": "水果"},
    "葡萄": {"energy": 67, "protein": 0.7, "fat": 0.2, "carbs": 17.1, "fiber": 1.0, "category": "水果"},
    "西瓜": {"energy": 30, "protein": 0.6, "fat": 0.1, "carbs": 7.5, "fiber": 0.3, "category": "水果"},
    "草莓": {"energy": 32, "protein": 0.7, "fat": 0.3, "carbs": 7.1, "fiber": 2.0, "category": "水果"},
    "猕猴桃": {"energy": 61, "protein": 1.1, "fat": 0.5, "carbs": 14.7, "fiber": 3.0, "category": "水果"},
    "蓝莓": {"energy": 57, "protein": 0.7, "fat": 0.3, "carbs": 14.5, "fiber": 2.4, "category": "水果"},
    "芒果": {"energy": 60, "protein": 0.8, "fat": 0.4, "carbs": 15.0, "fiber": 1.6, "category": "水果"},
    "梨": {"energy": 57, "protein": 0.4, "fat": 0.1, "carbs": 15.2, "fiber": 3.1, "category": "水果"},

    # ===== 坚果 =====
    "核桃": {"energy": 654, "protein": 15.2, "fat": 65.2, "carbs": 13.7, "fiber": 6.7, "category": "坚果"},
    "杏仁": {"energy": 579, "protein": 21.2, "fat": 49.9, "carbs": 21.6, "fiber": 12.5, "category": "坚果"},
    "花生": {"energy": 567, "protein": 25.8, "fat": 49.2, "carbs": 16.1, "fiber": 8.5, "category": "坚果"},

    # ===== 常见菜品(估算) =====
    "鱼香肉丝": {"energy": 165, "protein": 12.0, "fat": 10.0, "carbs": 6.0, "fiber": 1.0, "category": "菜品"},
    "宫保鸡丁": {"energy": 200, "protein": 18.0, "fat": 12.0, "carbs": 5.0, "fiber": 1.0, "category": "菜品"},
    "番茄炒蛋": {"energy": 110, "protein": 6.0, "fat": 7.0, "carbs": 5.0, "fiber": 0.5, "category": "菜品"},
    "红烧肉": {"energy": 350, "protein": 10.0, "fat": 32.0, "carbs": 5.0, "fiber": 0, "category": "菜品"},
    "麻婆豆腐": {"energy": 120, "protein": 8.0, "fat": 8.0, "carbs": 4.0, "fiber": 0.5, "category": "菜品"},
    "酸辣土豆丝": {"energy": 90, "protein": 1.5, "fat": 4.0, "carbs": 12.0, "fiber": 1.0, "category": "菜品"},
    "清炒西兰花": {"energy": 60, "protein": 3.0, "fat": 3.0, "carbs": 6.0, "fiber": 2.5, "category": "菜品"},
    "白切鸡": {"energy": 180, "protein": 22.0, "fat": 10.0, "carbs": 1.0, "fiber": 0, "category": "菜品"},

    # ===== 零食/饮料 =====
    "可乐": {"energy": 42, "protein": 0, "fat": 0, "carbs": 10.6, "fiber": 0, "category": "饮料"},
    "薯片": {"energy": 536, "protein": 7.0, "fat": 33.6, "carbs": 49.7, "fiber": 3.0, "category": "零食"},
    "巧克力": {"energy": 546, "protein": 7.7, "fat": 31.9, "carbs": 53.8, "fiber": 1.0, "category": "零食"},
    "方便面": {"energy": 473, "protein": 9.5, "fat": 21.1, "carbs": 60.9, "fiber": 1.0, "category": "速食"},
    "奶茶": {"energy": 52, "protein": 0.6, "fat": 1.2, "carbs": 10.0, "fiber": 0, "category": "饮料"},

    # ===== 油脂 =====
    "植物油": {"energy": 899, "protein": 0, "fat": 99.9, "carbs": 0, "fiber": 0, "category": "油脂"},
    "橄榄油": {"energy": 899, "protein": 0, "fat": 99.9, "carbs": 0, "fiber": 0, "category": "油脂"},
}

CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"


def _cache_path(keyword: str) -> Path:
    """生成缓存文件路径"""
    h = hashlib.md5(keyword.encode()).hexdigest()
    return CACHE_DIR / f"{h}.json"


def _load_cache(keyword: str) -> Optional[dict]:
    """读取缓存"""
    path = _cache_path(keyword)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def _save_cache(keyword: str, data: dict):
    """保存缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(_cache_path(keyword), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def search_food(keyword: str, use_api: bool = True, api_key: Optional[str] = None) -> Optional[dict]:
    """
    搜索食物营养成分
    优先级: 缓存 > 内置库 > TianAPI

    Args:
        keyword: 食物名称
        use_api: 是否尝试API
        api_key: TianAPI key

    Returns:
        {foodName, energy, protein, fat, carbs, fiber, category, serving(100g)}
    """
    keyword = keyword.strip()

    # 1. 查缓存
    cached = _load_cache(keyword)
    if cached:
        return cached

    # 2. 查内置库 (精确匹配 + 模糊匹配)
    if keyword in BUILTIN_FOODS:
        result = {"foodName": keyword, "serving": "100g", **BUILTIN_FOODS[keyword]}
        _save_cache(keyword, result)
        return result

    # 模糊匹配
    for name, data in BUILTIN_FOODS.items():
        if keyword in name or name in keyword:
            result = {"foodName": name, "serving": "100g", **data}
            _save_cache(keyword, result)
            return result

    # 3. 尝试 TianAPI (如果提供)
    if use_api and api_key:
        api_result = _tianapi_search(keyword, api_key)
        if api_result:
            _save_cache(keyword, api_result)
            return api_result

    return None


def _tianapi_search(keyword: str, api_key: str) -> Optional[dict]:
    """通过 TianAPI 查询"""
    try:
        import urllib.request
        import urllib.parse

        url = "https://apis.tianapi.com/nutrient/index"
        params = urllib.parse.urlencode({
            "key": api_key,
            "mode": 0,
            "word": keyword,
            "num": 1
        })
        req = urllib.request.Request(f"{url}?{params}")
        req.add_header("User-Agent", "FoodNutritionSkill/1.0")

        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data.get("code") == 200 and data.get("result", {}).get("list"):
                item = data["result"]["list"][0]
                return {
                    "foodName": item.get("foodName", keyword),
                    "energy": float(item.get("rl", 0)),
                    "protein": float(item.get("dbz", 0)),
                    "fat": float(item.get("zf", 0)),
                    "carbs": float(item.get("shhf", 0)),
                    "fiber": float(item.get("ssxw", 0)),
                    "serving": "100g",
                    "category": "API查询",
                    "calcium": float(item.get("gai", 0)),
                    "iron": float(item.get("tei", 0)),
                    "vitaminC": float(item.get("wsfc", 0)),
                    "vitaminA": float(item.get("wssa", 0)),
                }
    except Exception:
        pass
    return None


def list_categories() -> List[str]:
    """列出所有食物类别"""
    cats = set()
    for v in BUILTIN_FOODS.values():
        cats.add(v.get("category", "其他"))
    return sorted(cats)


def search_by_category(category: str) -> List[dict]:
    """按类别搜索"""
    results = []
    for name, data in BUILTIN_FOODS.items():
        if data.get("category") == category:
            results.append({"foodName": name, "serving": "100g", **data})
    return results


def get_dri(age: int = 30, gender: str = "male", goal: str = "maintain",
            height_cm: float = 170, weight_kg: float = 70,
            activity: str = "moderate") -> dict:
    """
    基于中国DRIs 2024 计算每日推荐摄入量

    Args:
        age: 年龄
        gender: male/female
        goal: lose(减脂)/gain(增肌)/maintain(维持)
        height_cm: 身高cm
        weight_kg: 体重kg
        activity: sedentary/light/moderate/active/very_active

    Returns:
        {energy, protein, fat, carbs, fiber, calcium, iron, vitaminC}
    """
    # BMR (Mifflin-St Jeor)
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # PAL
    pal = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55,
           "active": 1.725, "very_active": 1.9}.get(activity, 1.55)

    tdee = bmr * pal

    # 目标调整
    if goal == "lose":
        energy = tdee - 500  # 日均500kcal缺口
        protein = weight_kg * 2.0  # 减脂期高蛋白
        fat_pct = 0.25
    elif goal == "gain":
        energy = tdee + 300
        protein = weight_kg * 2.2
        fat_pct = 0.30
    else:
        energy = tdee
        protein = weight_kg * 1.2
        fat_pct = 0.28

    fat_g = (energy * fat_pct) / 9
    carbs_g = (energy - protein * 4 - fat_g * 9) / 4
    carbs_g = max(carbs_g, 100)

    return {
        "energy": round(energy),
        "protein": round(protein),
        "fat": round(fat_g),
        "carbs": round(carbs_g),
        "fiber": 25,
        "calcium": 800,
        "iron": 12 if gender == "male" else 20,
        "vitaminC": 100,
        "water": 2000,
    }


if __name__ == "__main__":
    # 测试
    r = search_food("鸡胸肉")
    print("鸡胸肉:", json.dumps(r, ensure_ascii=False))

    r2 = search_food("苹果")
    print("苹果:", json.dumps(r2, ensure_ascii=False))

    dri = get_dri(age=30, gender="male", goal="lose",
                  height_cm=175, weight_kg=80)
    print("DRI:", json.dumps(dri, ensure_ascii=False))

    print("缓存:", _load_cache("鸡胸肉"))
