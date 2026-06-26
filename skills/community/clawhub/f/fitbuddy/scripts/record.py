#!/usr/bin/env python3
"""fitbuddy - 记录饮食/体重/运动/饮水 (v2)"""

import argparse
import json
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(SKILL_DIR, "fitbuddy-data")
RECORDS_DIR = os.path.join(DATA_DIR, "records")
FOOD_DB_PATH = os.path.join(DATA_DIR, "food-db.json")
PROFILE_PATH = os.path.join(DATA_DIR, "profile.json")
PATTERNS_PATH = os.path.join(DATA_DIR, "user-patterns.json")


def _stamp(item):
    """给记录条目添加时间戳"""
    item["_added_at"] = datetime.now().isoformat()
    return item

def load_day(date_str):
    path = os.path.join(RECORDS_DIR, f"{date_str}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "date": date_str,
        "weight_kg": None,
        "meals": {"breakfast": [], "lunch": [], "dinner": [], "snack": []},
        "water_ml": 0,
        "water_target_ml": 2000,
        "exercises": [],
        "daily_summary": {
            "total_calories_in": 0,
            "total_calories_out": 0,
            "total_protein_g": 0,
            "total_carbs_g": 0,
            "total_fat_g": 0,
            "total_water_ml": 0,
        },
    }


def save_day(record):
    os.makedirs(RECORDS_DIR, exist_ok=True)
    path = os.path.join(RECORDS_DIR, f"{record['date']}.json")
    recalc_summary(record)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return record


def recalc_summary(record):
    total_in = 0
    total_p = 0
    total_c = 0
    total_f = 0
    for meal_items in record["meals"].values():
        for item in meal_items:
            cal = item.get("calories", item["protein_g"] * 4 + item["carbs_g"] * 4 + item["fat_g"] * 9)
            total_in += cal
            total_p += item.get("protein_g", 0)
            total_c += item.get("carbs_g", 0)
            total_f += item.get("fat_g", 0)

    total_out = sum(ex.get("calories_burned", 0) for ex in record["exercises"])

    s = record["daily_summary"]
    s["total_calories_in"] = round(total_in)
    s["total_calories_out"] = round(total_out)
    s["total_protein_g"] = round(total_p)
    s["total_carbs_g"] = round(total_c)
    s["total_fat_g"] = round(total_f)
    s["total_water_ml"] = record["water_ml"]


def load_food_db():
    if os.path.exists(FOOD_DB_PATH):
        with open(FOOD_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"foods": {}, "portion_aliases": {}}


def load_foods():
    db = load_food_db()
    return db.get("foods", {})


def load_portion_aliases():
    db = load_food_db()
    return db.get("portion_aliases", {})


def save_food_db(foods):
    db = load_food_db()
    db["foods"] = foods
    with open(FOOD_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def lookup_food(food_name):
    """模糊匹配食物数据库"""
    foods = load_foods()
    if food_name in foods:
        return food_name, foods[food_name]
    # 模糊匹配：包含关系
    best = None
    for name, info in foods.items():
        if food_name in name or name in food_name:
            if best is None or len(name) < len(best[0]):
                best = (name, info)
    return best if best else (None, None)


def parse_portion(portion_str):
    """解析模糊份量表达式，返回克数"""
    portion_aliases = load_portion_aliases()
    portion_str = portion_str.strip()

    # 直接匹配
    if portion_str in portion_aliases:
        return portion_aliases[portion_str]

    # 去掉数字部分匹配
    import re
    match = re.match(r'^(\d+)(.*)$', portion_str)
    if match:
        num = int(match.group(1))
        unit = match.group(2).strip()
        if unit in portion_aliases:
            return num * portion_aliases[unit]
        # 默认单位为克
        if not unit:
            return num

    return None


def calc_food(food_name, grams=None, portion_str=None):
    """根据食物名和克数计算营养素。grams=None 时使用 serving_g 或 portion_str"""
    matched_name, info = lookup_food(food_name)
    if not info:
        return None

    # 处理菜品类型（分解成食材）
    if info.get("type") == "dish":
        ingredients = info.get("ingredients", [])
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_calories = 0
        ingredient_details = []

        # 如果菜品有指定serving_g且未指定grams，按serving_g计算比例
        dish_serving = info.get("serving_g", sum(ing["grams"] for ing in ingredients))
        if grams is None:
            grams = dish_serving

        ratio = grams / dish_serving if dish_serving > 0 else 1

        for ing in ingredients:
            ing_name = ing["name"]
            ing_grams = ing["grams"] * ratio
            ing_result = calc_food(ing_name, ing_grams)
            if ing_result:
                total_protein += ing_result["protein_g"]
                total_carbs += ing_result["carbs_g"]
                total_fat += ing_result["fat_g"]
                total_calories += ing_result["calories"]
                ingredient_details.append({
                    "name": ing_name,
                    "grams": round(ing_grams, 1),
                    "protein_g": ing_result["protein_g"],
                    "carbs_g": ing_result["carbs_g"],
                    "fat_g": ing_result["fat_g"],
                    "calories": ing_result["calories"]
                })

        result = {
            "food": f"{matched_name}{grams}g",
            "protein_g": round(total_protein, 1),
            "carbs_g": round(total_carbs, 1),
            "fat_g": round(total_fat, 1),
            "calories": round(total_calories),
            "type": "dish",
            "ingredients": ingredient_details
        }
        return result

    # 处理普通食物
    if grams is None:
        # 尝试用portion_str解析
        if portion_str:
            grams = parse_portion(portion_str)
        if grams is None:
            grams = info.get("serving_g")
    if grams is None:
        return None

    ratio = grams / 100.0
    return {
        "food": f"{matched_name}{grams}g",
        "protein_g": round(info["protein_g"] * ratio, 1),
        "carbs_g": round(info["carbs_g"] * ratio, 1),
        "fat_g": round(info["fat_g"] * ratio, 1),
        "calories": round((info["protein_g"] * 4 + info["carbs_g"] * 4 + info["fat_g"] * 9) * ratio),
    }


def load_patterns():
    """加载用户饮食模式数据"""
    if os.path.exists(PATTERNS_PATH):
        with open(PATTERNS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "food_frequency": {},
        "meal_combinations": {
            "breakfast": {},
            "lunch": {},
            "dinner": {},
            "snack": {}
        },
        "last_updated": None
    }


def save_patterns(patterns):
    """保存用户饮食模式数据"""
    patterns["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PATTERNS_PATH, "w", encoding="utf-8") as f:
        json.dump(patterns, f, ensure_ascii=False, indent=2)


def update_food_pattern(food_name):
    """更新食物频率统计"""
    import re
    patterns = load_patterns()
    food_name = re.sub(r'\d+\.?\d*g$', '', food_name).rstrip()  # 去除克数后缀
    patterns["food_frequency"][food_name] = patterns["food_frequency"].get(food_name, 0) + 1
    save_patterns(patterns)


def update_meal_pattern(meal_key, food_items):
    """更新餐次组合统计"""
    import re
    patterns = load_patterns()
    # 简化组合名：取前2个食物名
    food_names = []
    for item in food_items:
        name = re.sub(r'\d+\.?\d*g$', '', item["food"]).rstrip()
        food_names.append(name)
    if len(food_names) > 2:
        combo_name = "+".join(food_names[:2]) + "..."
    else:
        combo_name = "+".join(food_names)
    if not combo_name:
        return
    patterns["meal_combinations"][meal_key][combo_name] = patterns["meal_combinations"][meal_key].get(combo_name, 0) + 1
    save_patterns(patterns)


def auto_meal(date_str):
    """根据时间和已有记录自动判断餐次"""
    now = datetime.now()
    hour = now.hour
    rec = load_day(date_str)

    if hour < 10:
        return "breakfast"
    elif hour < 14:
        return "lunch"
    elif hour < 16:
        if rec["meals"]["lunch"]:
            return "snack"
        return "lunch"
    elif hour < 21:
        return "dinner"
    else:
        if rec["meals"]["dinner"]:
            return "snack"
        return "dinner"


# ── 命令 ──────────────────────────────────────────────

def cmd_weight(args):
    rec = load_day(args.date)
    rec["weight_kg"] = args.kg
    rec = save_day(rec)
    # Update profile
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            profile = json.load(f)
        profile["weight_kg"] = args.kg
        profile["updated_at"] = datetime.now().isoformat()
        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
    print(json.dumps(rec, ensure_ascii=False))


def cmd_meal(args):
    from datetime import timedelta

    # 处理 --like-yesterday
    if getattr(args, 'like_yesterday', False):
        yesterday = (datetime.strptime(args.date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_rec = load_day(yesterday)
        rec = load_day(args.date)

        meal_key = args.meal or auto_meal(args.date)
        if meal_key not in rec["meals"]:
            meal_key = "snack"

        # 追加昨日餐次（不覆盖已有记录）
        if args.meal:
            if yesterday_rec["meals"][meal_key]:
                for item in yesterday_rec["meals"][meal_key]:
                    rec["meals"][meal_key].append(item.copy())
                    update_food_pattern(item["food"])
                update_meal_pattern(meal_key, rec["meals"][meal_key])
        else:
            for mk in rec["meals"]:
                if yesterday_rec["meals"][mk]:
                    for item in yesterday_rec["meals"][mk]:
                        rec["meals"][mk].append(item.copy())
                        update_food_pattern(item["food"])
                    update_meal_pattern(mk, rec["meals"][mk])

        rec = save_day(rec)
        print(json.dumps({"action": "copied_from_yesterday", "from": yesterday, "record": rec}, ensure_ascii=False))
        return

    # 处理 --usual
    if getattr(args, 'usual', False):
        patterns = load_patterns()
        rec = load_day(args.date)

        meal_key = args.meal or auto_meal(args.date)
        if meal_key not in rec["meals"]:
            meal_key = "snack"

        # 获取最常吃的餐次组合
        meal_patterns = patterns.get("meal_combinations", {}).get(meal_key, {})
        if not meal_patterns:
            print(json.dumps({"error": "暂无饮食记录，无法推荐常用组合"}, ensure_ascii=False))
            return

        # 找出最频繁的组合
        best_combo = max(meal_patterns.items(), key=lambda x: x[1])
        combo_name = best_combo[0]

        # 从历史记录中找到这个组合的具体食物
        from datetime import timedelta
        for i in range(1, 31):  # 查找最近30天
            d = (datetime.strptime(args.date, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d")
            path = os.path.join(RECORDS_DIR, f"{d}.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    day_rec = json.load(f)
                if day_rec["meals"][meal_key]:
                    import re
                    food_names = []
                    for item in day_rec["meals"][meal_key]:
                        name = re.sub(r'\d+\.?\d*g$', '', item["food"]).rstrip()
                        food_names.append(name)
                    if len(food_names) > 2:
                        current_combo = "+".join(food_names[:2]) + "..."
                    else:
                        current_combo = "+".join(food_names)
                    if current_combo == combo_name:
                        rec["meals"][meal_key] = day_rec["meals"][meal_key].copy()
                        for item in rec["meals"][meal_key]:
                            update_food_pattern(item["food"])
                        rec = save_day(rec)
                        print(json.dumps({"action": "added_usual_combo", "combo": combo_name, "count": best_combo[1], "record": rec}, ensure_ascii=False))
                        return

        print(json.dumps({"error": "无法找到常用组合的详细记录"}, ensure_ascii=False))
        return

    rec = load_day(args.date)

    # 自动判断餐次
    meal_key = args.meal or auto_meal(args.date)
    if meal_key not in rec["meals"]:
        meal_key = "snack"

    # 批量模式：--foods '[{"name":"鸡胸肉","grams":200},{"name":"米饭","grams":150}]'
    if args.foods:
        food_list = json.loads(args.foods)
        added = []
        errors = []
        for f in food_list:
            item = calc_food(f["name"], f.get("grams"))
            if item:
                _stamp(item)
                rec["meals"][meal_key].append(item)
                added.append(item)
                update_food_pattern(item["food"])
            else:
                errors.append(f["name"])
        if added:
            update_meal_pattern(meal_key, added)
            rec = save_day(rec)
        if errors:
            print(json.dumps({"added": len(added), "errors": errors, "record": rec}, ensure_ascii=False))
        else:
            print(json.dumps(rec, ensure_ascii=False))
        return

    if args.food_name:
        item = calc_food(args.food_name, args.grams)
        if not item:
            if args.grams is None:
                print(f"错误: '{args.food_name}' 没有默认份量，请指定 --grams")
            else:
                print(f"错误: 未找到食物 '{args.food_name}'，请先添加到数据库")
            sys.exit(1)
        _stamp(item)
        rec["meals"][meal_key].append(item)
        update_food_pattern(item["food"])
        update_meal_pattern(meal_key, [item])
        rec = save_day(rec)
        print(json.dumps(rec, ensure_ascii=False))
        return

    # 手动输入
    cal = args.protein * 4 + args.carbs * 4 + args.fat * 9
    item = {
        "food": args.food or "",
        "protein_g": args.protein,
        "carbs_g": args.carbs,
        "fat_g": args.fat,
        "calories": round(cal),
    }
    _stamp(item)
    rec["meals"][meal_key].append(item)
    if args.food:
        update_food_pattern(item["food"])
        update_meal_pattern(meal_key, [item])
    rec = save_day(rec)
    print(json.dumps(rec, ensure_ascii=False))


def cmd_water(args):
    rec = load_day(args.date)
    rec["water_ml"] = rec.get("water_ml", 0) + args.ml
    rec = save_day(rec)
    print(json.dumps(rec, ensure_ascii=False))


def cmd_exercise(args):
    rec = load_day(args.date)
    if args.type == "cardio":
        rates = {"running": 10, "walking": 5, "cycling": 7, "swimming": 9, "jump_rope": 12, "hiit": 13}
        rate = 8
        for key, val in rates.items():
            if key in args.name.lower():
                rate = val
                break
        duration = args.duration or 30
        cal = rate * duration
    else:
        total_sets = args.sets or 3
        cal = total_sets * 2.5 * 7

    exercise = {
        "type": args.type or "strength",
        "name": args.name,
        "sets": args.sets,
        "reps": args.reps,
        "weight_kg": args.weight,
        "muscle_group": args.group or "other",
        "duration_min": args.duration,
        "calories_burned": round(cal),
    }
    _stamp(exercise)
    rec["exercises"].append(exercise)
    rec = save_day(rec)
    print(json.dumps(rec, ensure_ascii=False))


def cmd_analyze(args):
    """分析体重趋势"""
    from datetime import timedelta
    today = datetime.strptime(args.date, "%Y-%m-%d").date()
    
    weights = []
    for i in range(min(args.days, 30) - 1, -1, -1):
        d = today - timedelta(days=i)
        path = os.path.join(RECORDS_DIR, f"{d}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                rec = json.load(f)
            if rec.get("weight_kg"):
                weights.append({"date": str(d), "weight_kg": rec["weight_kg"]})
    
    if len(weights) < 2:
        print(json.dumps({"error": "数据不足，至少需要2天体重记录"}, ensure_ascii=False))
        return
    
    first = weights[0]
    last = weights[-1]
    change = round(last["weight_kg"] - first["weight_kg"], 1)
    
    # 计算周均变化
    days_span = (datetime.strptime(last["date"], "%Y-%m-%d") - datetime.strptime(first["date"], "%Y-%m-%d")).days
    weekly_change = round(change / max(days_span, 1) * 7, 2) if days_span > 0 else 0
    
    # 判断趋势
    if len(weights) >= 5:
        recent_3 = [w["weight_kg"] for w in weights[-3:]]
        older = [w["weight_kg"] for w in weights[:-3]]
        recent_avg = sum(recent_3) / len(recent_3)
        older_avg = sum(older) / len(older) if older else recent_avg
        if abs(recent_avg - older_avg) < 0.3:
            trend = "plateau"
            trend_text = "平台期"
        elif recent_avg < older_avg:
            trend = "decreasing"
            trend_text = "下降中"
        else:
            trend = "increasing"
            trend_text = "上升中"
    else:
        trend = "insufficient"
        trend_text = "数据不足"
    
    result = {
        "period": f"{first['date']} ~ {last['date']}",
        "data_points": len(weights),
        "weight_start": first["weight_kg"],
        "weight_end": last["weight_kg"],
        "change_kg": change,
        "weekly_change_kg": weekly_change,
        "trend": trend,
        "trend_text": trend_text,
        "weights": weights
    }
    print(json.dumps(result, ensure_ascii=False))


def cmd_undo(args):
    """撤销最近一条记录（按时间戳倒序）"""
    rec = load_day(args.date)

    # 收集所有条目，找到最新的
    candidates = []
    for meal_key in rec["meals"]:
        for i, item in enumerate(rec["meals"][meal_key]):
            ts = item.get("_added_at", "")
            candidates.append((ts, "meal", meal_key, i))
    for i, item in enumerate(rec["exercises"]):
        ts = item.get("_added_at", "")
        candidates.append((ts, "exercise", None, i))

    if not candidates:
        print("没有可撤销的记录")
        return

    # 按 _added_at 排序，取最新的
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, typ, meal_key, idx = candidates[0]

    if typ == "meal":
        removed = rec["meals"][meal_key].pop(idx)
        _clean_item(removed)
        rec = save_day(rec)
        print(json.dumps({"action": "undo", "removed": removed, "from": meal_key, "record": rec}, ensure_ascii=False))
    elif typ == "exercise":
        removed = rec["exercises"].pop(idx)
        _clean_item(removed)
        rec = save_day(rec)
        print(json.dumps({"action": "undo", "removed": removed, "record": rec}, ensure_ascii=False))


def _clean_item(item):
    """移除内部字段，不输出给用户"""
    item.pop("_added_at", None)


def cmd_today(args):
    """今日总览"""
    rec = load_day(args.date)
    print(json.dumps(rec, ensure_ascii=False))


def cmd_food_db(args):
    if args.action == "list":
        foods = load_foods()
        for name, info in foods.items():
            if info.get("type") == "dish":
                ing_list = ", ".join([f"{ing['name']}({ing['grams']}g)" for ing in info.get("ingredients", [])])
                print(f"[菜品] {name}: {ing_list}")
            elif "protein_g" not in info:
                continue
            else:
                serving = f" (默认{info['serving_g']}g)" if "serving_g" in info else ""
                print(f"{name}: 蛋白{info['protein_g']}g 碳水{info['carbs_g']}g 脂肪{info['fat_g']}g (每100g){serving}")
    elif args.action == "add":
        foods = load_foods()
        entry = {
            "protein_g": args.protein,
            "carbs_g": args.carbs,
            "fat_g": args.fat,
            "source": "用户添加"
        }
        if args.serving_g:
            entry["serving_g"] = args.serving_g
        foods[args.name] = entry
        save_food_db(foods)
        print(f"已添加: {args.name}")
    elif args.action == "add-dish":
        foods = load_foods()
        if not args.ingredients:
            print("错误: 菜品需要指定 --ingredients 参数")
            return
        try:
            ingredients = json.loads(args.ingredients)
        except:
            print("错误: --ingredients 必须是JSON数组格式: [{\"name\":\"鸡蛋\",\"grams\":150}]")
            return
        entry = {
            "type": "dish",
            "ingredients": ingredients,
            "source": "用户添加"
        }
        if args.serving_g:
            entry["serving_g"] = args.serving_g
        foods[args.name] = entry
        save_food_db(foods)
        print(f"已添加菜品: {args.name}")
    elif args.action == "search":
        matched_name, info = lookup_food(args.name)
        if info:
            if info.get("type") == "dish":
                ing_list = ", ".join([f"{ing['name']}({ing['grams']}g)" for ing in info.get("ingredients", [])])
                print(f"[菜品] {matched_name}: {ing_list}")
            else:
                serving = f" (默认{info['serving_g']}g)" if "serving_g" in info else ""
                print(f"{matched_name}: 蛋白{info['protein_g']}g 碳水{info['carbs_g']}g 脂肪{info['fat_g']}g (每100g){serving}")
        else:
            print(f"未找到: {args.name}")
    elif args.action == "calc":
        result = calc_food(args.name, args.grams, args.portion)
        if result:
            print(json.dumps(result, ensure_ascii=False))
        elif args.grams is None and not args.portion:
            print(f"未找到默认份量: {args.name}，请指定 --grams 或 --portion")
        else:
            print(f"未找到: {args.name}")


def cmd_patterns(args):
    """显示用户饮食习惯TOP10"""
    patterns = load_patterns()

    print("=== TOP10 最常吃的食物 ===")
    food_freq = patterns.get("food_frequency", {})
    sorted_foods = sorted(food_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (food, count) in enumerate(sorted_foods, 1):
        print(f"{i}. {food}: {count}次")

    print("\n=== 各餐次常用组合 ===")
    meal_combos = patterns.get("meal_combinations", {})
    for meal_key in ["breakfast", "lunch", "dinner", "snack"]:
        combos = meal_combos.get(meal_key, {})
        if combos:
            meal_name = {"breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐", "snack": "加餐"}[meal_key]
            print(f"\n{meal_name}:")
            sorted_combos = sorted(combos.items(), key=lambda x: x[1], reverse=True)[:5]
            for combo, count in sorted_combos:
                print(f"  - {combo}: {count}次")


def cmd_progress(args):
    """显示进度条可视化"""
    import sys
    rec = load_day(args.date)
    profile = {}
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            profile = json.load(f)

    # 从 calc.py 获取当天实际目标（低碳/高碳）
    import subprocess
    try:
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "calc.py"), "daily",
             "--profile", PROFILE_PATH, "--date", args.date],
            capture_output=True, text=True, encoding="utf-8")
        daily_target = json.loads(result.stdout.strip())
        target_cal = daily_target["daily_calorie_target"]
        target_prot = daily_target["macros"]["protein_g"]
        target_carbs = daily_target["macros"]["carbs_g"]
        target_fat = daily_target["macros"]["fat_g"]
    except Exception:
        target_cal = profile.get("daily_calorie_target", 2000)
        target_prot = profile.get("macros", {}).get("protein_g", 150)
        target_carbs = profile.get("macros", {}).get("carbs_g", 200)
        target_fat = profile.get("macros", {}).get("fat_g", 70)

    actual_cal = rec["daily_summary"]["total_calories_in"]
    actual_prot = rec["daily_summary"]["total_protein_g"]
    actual_carbs = rec["daily_summary"]["total_carbs_g"]
    actual_fat = rec["daily_summary"]["total_fat_g"]

    def draw_bar(current, target, label, width=30):
        ratio = min(current / target, 1.0) if target > 0 else 0
        filled = int(ratio * width)
        # 使用ASCII字符兼容Windows控制台
        bar = "=" * filled + "-" * (width - filled)
        percent = int(ratio * 100)
        return f"{label:12} [{bar}] {current}/{target} ({percent}%)"

    try:
        print(f"\n=== {args.date} 进度 ===\n")
        print(draw_bar(actual_cal, target_cal, "热量"))
        print(draw_bar(actual_prot, target_prot, "蛋白质"))
        print(draw_bar(actual_carbs, target_carbs, "碳水"))
        print(draw_bar(actual_fat, target_fat, "脂肪"))
        print(f"\n饮水: {rec['water_ml']}/{rec['water_target_ml']}ml")
        if rec.get("weight_kg"):
            print(f"体重: {rec['weight_kg']}kg")
    except UnicodeEncodeError:
        # Windows控制台编码问题备用方案
        output = [
            f"\n=== {args.date} 进度 ===\n",
            draw_bar(actual_cal, target_cal, "Calories"),
            draw_bar(actual_prot, target_prot, "Protein"),
            draw_bar(actual_carbs, target_carbs, "Carbs"),
            draw_bar(actual_fat, target_fat, "Fat"),
            f"\nWater: {rec['water_ml']}/{rec['water_target_ml']}ml"
        ]
        if rec.get("weight_kg"):
            output.append(f"Weight: {rec['weight_kg']}kg")
        sys.stdout.write("\n".join(output) + "\n")


def cmd_weekly(args):
    """生成周报JSON"""
    from datetime import datetime, timedelta

    target_date = datetime.strptime(args.date, "%Y-%m-%d")
    # 找到该周的周一
    monday = target_date
    while monday.weekday() != 0:
        monday -= timedelta(days=1)

    weekly_data = {
        "week_start": monday.strftime("%Y-%m-%d"),
        "week_end": (monday + timedelta(days=6)).strftime("%Y-%m-%d"),
        "days": []
    }

    total_cal_in = 0
    total_cal_out = 0
    total_prot = 0
    total_carbs = 0
    total_fat = 0
    total_water = 0
    weight_records = []

    for i in range(7):
        d = monday + timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        path = os.path.join(RECORDS_DIR, f"{date_str}.json")

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                rec = json.load(f)

            day_data = {
                "date": date_str,
                "calories_in": rec["daily_summary"]["total_calories_in"],
                "calories_out": rec["daily_summary"]["total_calories_out"],
                "protein_g": rec["daily_summary"]["total_protein_g"],
                "carbs_g": rec["daily_summary"]["total_carbs_g"],
                "fat_g": rec["daily_summary"]["total_fat_g"],
                "water_ml": rec["daily_summary"]["total_water_ml"],
                "meals_count": sum(len(rec["meals"][k]) for k in rec["meals"]),
                "exercises_count": len(rec["exercises"])
            }

            if rec.get("weight_kg"):
                day_data["weight_kg"] = rec["weight_kg"]
                weight_records.append({"date": date_str, "weight_kg": rec["weight_kg"]})

            weekly_data["days"].append(day_data)

            total_cal_in += day_data["calories_in"]
            total_cal_out += day_data["calories_out"]
            total_prot += day_data["protein_g"]
            total_carbs += day_data["carbs_g"]
            total_fat += day_data["fat_g"]
            total_water += day_data["water_ml"]

    # 计算平均值
    days_with_data = len(weekly_data["days"])
    if days_with_data > 0:
        weekly_data["summary"] = {
            "avg_calories_in": round(total_cal_in / days_with_data),
            "avg_calories_out": round(total_cal_out / days_with_data),
            "avg_protein_g": round(total_prot / days_with_data),
            "avg_carbs_g": round(total_carbs / days_with_data),
            "avg_fat_g": round(total_fat / days_with_data),
            "avg_water_ml": round(total_water / days_with_data),
            "total_days_recorded": days_with_data
        }

        # 体重变化
        if len(weight_records) >= 2:
            first_weight = weight_records[0]["weight_kg"]
            last_weight = weight_records[-1]["weight_kg"]
            weekly_data["summary"]["weight_change_kg"] = round(last_weight - first_weight, 1)
            weekly_data["summary"]["weight_first"] = first_weight
            weekly_data["summary"]["weight_last"] = last_weight

    print(json.dumps(weekly_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fitbuddy record v2")
    sub = parser.add_subparsers(dest="command")

    # weight
    p_w = sub.add_parser("weight")
    p_w.add_argument("--date", required=True)
    p_w.add_argument("--kg", type=float, required=True)

    # meal
    p_m = sub.add_parser("meal")
    p_m.add_argument("--date", required=True)
    p_m.add_argument("--meal", default=None, choices=["breakfast", "lunch", "dinner", "snack"],
                     help="餐次，不填则自动判断")
    p_m.add_argument("--food", default="")
    p_m.add_argument("--protein", type=float, default=0)
    p_m.add_argument("--carbs", type=float, default=0)
    p_m.add_argument("--fat", type=float, default=0)
    p_m.add_argument("--food-name", default=None, help="食物数据库名称")
    p_m.add_argument("--grams", type=float, default=None, help="克数，不填用默认份量")
    p_m.add_argument("--foods", default=None, help="批量模式：JSON数组 [{\"name\":\"鸡胸肉\",\"grams\":200}, ...]")
    p_m.add_argument("--like-yesterday", action="store_true", help="复制昨天的餐食")
    p_m.add_argument("--usual", action="store_true", help="使用常吃的组合")

    # food-db
    p_fd = sub.add_parser("food-db")
    p_fd.add_argument("action", choices=["list", "add", "add-dish", "search", "calc"])
    p_fd.add_argument("--name", default="")
    p_fd.add_argument("--protein", type=float, default=0)
    p_fd.add_argument("--carbs", type=float, default=0)
    p_fd.add_argument("--fat", type=float, default=0)
    p_fd.add_argument("--grams", type=float, default=None)
    p_fd.add_argument("--portion", default=None, help="模糊份量，如\"一碗\"、\"一个鸡蛋\"")
    p_fd.add_argument("--serving-g", type=float, default=None, help="默认份量(g)")
    p_fd.add_argument("--ingredients", default=None, help="菜品食材JSON数组")

    # water
    p_wa = sub.add_parser("water")
    p_wa.add_argument("--date", required=True)
    p_wa.add_argument("--ml", type=int, required=True)

    # exercise
    p_e = sub.add_parser("exercise")
    p_e.add_argument("--date", required=True)
    p_e.add_argument("--name", required=True)
    p_e.add_argument("--sets", type=int, default=None)
    p_e.add_argument("--reps", type=int, default=None)
    p_e.add_argument("--weight", type=float, default=None)
    p_e.add_argument("--group", default=None)
    p_e.add_argument("--type", default="strength", choices=["strength", "cardio"])
    p_e.add_argument("--duration", type=int, default=None)

    # undo
    p_u = sub.add_parser("undo")
    p_u.add_argument("--date", required=True)

    # today (总览)
    p_t = sub.add_parser("today")
    p_t.add_argument("--date", required=True)

    # analyze (趋势分析)
    p_a = sub.add_parser("analyze")
    p_a.add_argument("--date", required=True)
    p_a.add_argument("--days", type=int, default=14)

    # patterns (饮食模式)
    p_pat = sub.add_parser("patterns")

    # progress (进度可视化)
    p_prog = sub.add_parser("progress")
    p_prog.add_argument("--date", default=None, help="日期 YYYY-MM-DD，默认今天")
    p_prog.set_defaults(date=lambda: datetime.now().strftime("%Y-%m-%d"))

    # weekly (周报)
    p_week = sub.add_parser("weekly")
    p_week.add_argument("--date", default=None, help="日期 YYYY-MM-DD，默认今天")
    p_week.set_defaults(date=lambda: datetime.now().strftime("%Y-%m-%d"))

    args = parser.parse_args()

    # 处理默认日期参数
    if args.command == "progress" or args.command == "weekly":
        if not args.date or callable(args.date):
            args.date = datetime.now().strftime("%Y-%m-%d")

    if args.command == "weight":
        cmd_weight(args)
    elif args.command == "meal":
        cmd_meal(args)
    elif args.command == "water":
        cmd_water(args)
    elif args.command == "exercise":
        cmd_exercise(args)
    elif args.command == "undo":
        cmd_undo(args)
    elif args.command == "today":
        cmd_today(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "food-db":
        cmd_food_db(args)
    elif args.command == "patterns":
        cmd_patterns(args)
    elif args.command == "progress":
        cmd_progress(args)
    elif args.command == "weekly":
        cmd_weekly(args)
    else:
        parser.print_help()
