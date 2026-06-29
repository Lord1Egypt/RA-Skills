#!/usr/bin/env python3
"""食材替换建议引擎 — 缺失食材的替代方案"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recipe_db import load_recipes, get_recipe_detail

# 食材替换知识库
SUBSTITUTION_DB = {
    # 调味料
    "豆瓣酱": [
        {"substitute": "甜面酱+辣椒油", "ratio": "甜面酱2:辣椒油1", "score": 5, "note": "味道最接近，颜色也相似"},
        {"substitute": "黄豆酱+辣椒粉", "ratio": "黄豆酱2:辣椒粉1", "score": 4, "note": "咸鲜底味一致，辣度可调"},
        {"substitute": "老干妈", "ratio": "1:1", "score": 3, "note": "懒人救星，口味偏重"},
    ],
    "生抽": [
        {"substitute": "普通酱油", "ratio": "1:0.8", "score": 5, "note": "颜色稍深，咸度略高，减量使用"},
        {"substitute": "蒸鱼豉油", "ratio": "1:1", "score": 4, "note": "鲜味更足，咸度适中"},
        {"substitute": "味极鲜", "ratio": "1:1", "score": 3, "note": "鲜味突出，适合凉拌"},
    ],
    "老抽": [
        {"substitute": "生抽+红糖", "ratio": "生抽1:红糖0.5", "score": 4, "note": "用糖炒色替代老抽上色"},
        {"substitute": "炒糖色", "ratio": "冰糖30g代替1勺老抽", "score": 4, "note": "传统红烧上色法，需要练习"},
    ],
    "料酒": [
        {"substitute": "啤酒", "ratio": "1:1.5", "score": 4, "note": "去腥效果相似，略带麦香"},
        {"substitute": "白酒+水", "ratio": "白酒1:水3", "score": 3, "note": "高度白酒去腥更强，注意用量"},
        {"substitute": "姜汁+水", "ratio": "1:1", "score": 2, "note": "去腥但缺少酒香"},
    ],
    "蚝油": [
        {"substitute": "生抽+糖", "ratio": "生抽1:糖0.3", "score": 3, "note": "鲜甜味接近，但缺少蚝香"},
        {"substitute": "鱼露", "ratio": "1:0.5", "score": 3, "note": "鲜味充足但味道不同"},
    ],
    "醋": [
        {"substitute": "柠檬汁", "ratio": "1:1", "score": 4, "note": "酸度接近，更多果香"},
        {"substitute": "白醋", "ratio": "1:0.8", "score": 5, "note": "陈醋可用白醋替代，风味稍逊"},
    ],
    "冰糖": [
        {"substitute": "白砂糖", "ratio": "1:0.8", "score": 5, "note": "甜度更高，炒糖色效果接近"},
        {"substitute": "红糖", "ratio": "1:1", "score": 3, "note": "颜色深，适合红烧类"},
        {"substitute": "蜂蜜", "ratio": "1:0.5", "score": 2, "note": "不适合高温烹饪"},
    ],
    "味精": [
        {"substitute": "鸡精", "ratio": "1:1", "score": 5, "note": "鲜味来源不同但效果接近"},
        {"substitute": "蚝油", "ratio": "1勺替代1小勺味精", "score": 3, "note": "鲜味足但会改变风味"},
    ],
    "花椒": [
        {"substitute": "麻椒", "ratio": "1:0.5", "score": 4, "note": "麻味更重，香味略逊"},
        {"substitute": "黑胡椒", "ratio": "1:0.5", "score": 2, "note": "完全不同风味，仅提供辛辣感"},
    ],
    "八角": [
        {"substitute": "五香粉", "ratio": "1小勺替代2颗八角", "score": 4, "note": "复合香料，用量要控制"},
        {"substitute": "桂皮+丁香", "ratio": "桂皮1块+丁香2粒", "score": 3, "note": "搭配使用最接近"},
    ],

    # 食材
    "五花肉": [
        {"substitute": "前腿肉", "ratio": "1:1", "score": 4, "note": "肥瘦比例接近，口感略柴"},
        {"substitute": "梅花肉", "ratio": "1:1", "score": 3, "note": "更嫩但肥肉少，红烧风味打折扣"},
    ],
    "鸡胸肉": [
        {"substitute": "鸡腿肉", "ratio": "1:1", "score": 5, "note": "更嫩滑多汁，口感更好"},
        {"substitute": "火鸡肉", "ratio": "1:1", "score": 3, "note": "口感接近但较柴"},
    ],
    "淀粉": [
        {"substitute": "面粉", "ratio": "1:1.5", "score": 3, "note": "勾芡效果差些，口感不同"},
        {"substitute": "藕粉", "ratio": "1:1", "score": 4, "note": "勾芡透明度好"},
    ],
    "鸡蛋": [
        {"substitute": "鸭蛋", "ratio": "1:1", "score": 4, "note": "口感更Q，略有腥味"},
        {"substitute": "嫩豆腐", "ratio": "100g替代1个蛋", "score": 2, "note": "仅限炒蛋类替代"},
    ],
    "豆腐": [
        {"substitute": "豆干", "ratio": "1:0.7", "score": 4, "note": "口感更韧，适合炒菜"},
        {"substitute": "千张", "ratio": "1:0.8", "score": 3, "note": "切丝可替代豆腐丝"},
    ],
    "西红柿": [
        {"substitute": "番茄罐头", "ratio": "1:1", "score": 4, "note": "酸甜味固定，适合炖煮"},
        {"substitute": "番茄酱+糖", "ratio": "番茄酱2勺+糖1小勺", "score": 3, "note": "可模拟西红柿味但缺口感"},
    ],
    "青椒": [
        {"substitute": "尖椒", "ratio": "1:0.7", "score": 4, "note": "辣度更高，注意用量"},
        {"substitute": "彩椒", "ratio": "1:1", "score": 4, "note": "不辣但颜色更丰富"},
    ],
    "葱": [
        {"substitute": "洋葱", "ratio": "1:0.5", "score": 4, "note": "爆香效果一样，味道更浓"},
        {"substitute": "蒜苗", "ratio": "1:1", "score": 3, "note": "不同方向的风味"},
    ],
    "姜": [
        {"substitute": "姜粉", "ratio": "1小勺替代1块姜", "score": 3, "note": "方便但去腥效果弱"},
        {"substitute": "料酒+葱", "ratio": "料酒2勺+葱1段", "score": 3, "note": "组合去腥替代"},
    ],
    "蒜": [
        {"substitute": "蒜粉", "ratio": "1小勺替代3瓣蒜", "score": 3, "note": "方便但爆香味不足"},
        {"substitute": "洋葱", "ratio": "半个洋葱替代5瓣蒜", "score": 2, "note": "只能提供辛香味"},
    ],
    "花生": [
        {"substitute": "腰果", "ratio": "1:1", "score": 5, "note": "口感更脆，档次更高"},
        {"substitute": "杏仁", "ratio": "1:1", "score": 4, "note": "脆度接近，风味不同"},
        {"substitute": "瓜子仁", "ratio": "1:1", "score": 3, "note": "最经济的替代"},
    ],
    "芝麻油": [
        {"substitute": "花椒油", "ratio": "1:0.5", "score": 3, "note": "风味完全不同但增香效果好"},
        {"substitute": "普通食用油", "ratio": "1:1", "score": 1, "note": "只为润滑，无香味"},
    ],
    "虾皮": [
        {"substitute": "虾米", "ratio": "1:0.5", "score": 4, "note": "鲜味更浓"},
        {"substitute": "鱼露", "ratio": "1小勺替代1把虾皮", "score": 3, "note": "液体替代固体"},
    ],
    "火腿": [
        {"substitute": "培根", "ratio": "1:1", "score": 4, "note": "烟熏风味不同但效果接近"},
        {"substitute": "腊肉", "ratio": "1:0.8", "score": 4, "note": "更咸，注意减盐"},
    ],
    "猪油": [
        {"substitute": "黄油", "ratio": "1:1", "score": 3, "note": "奶香味不同，炒青菜别有风味"},
        {"substitute": "植物油+五花肉", "ratio": "油为主+几片五花肉爆香", "score": 4, "note": "用五花肉煸出油增香"},
    ],
    "高汤": [
        {"substitute": "浓汤宝+水", "ratio": "1块+500ml水", "score": 4, "note": "最便捷的替代"},
        {"substitute": "鸡精+水", "ratio": "1小勺+500ml水", "score": 3, "note": "鲜味有但缺少层次"},
    ],
    "郫县豆瓣酱": [
        {"substitute": "豆瓣酱+辣椒面", "ratio": "豆瓣酱1:辣椒面0.3", "score": 4, "note": "缺少发酵香但辣味接近"},
        {"substitute": "黄豆酱+干辣椒", "ratio": "黄豆酱1:干辣椒3个", "score": 3, "note": "风味差异较大"},
    ],
    "豆豉": [
        {"substitute": "老干妈豆豉", "ratio": "1:1.5", "score": 4, "note": "含油的豆豉，注意整体用油量"},
        {"substitute": "酱油+五香粉", "ratio": "酱油1勺+五香粉少许", "score": 2, "note": "只能模拟咸香味"},
    ],
    "豆腐乳": [
        {"substitute": "豆瓣酱+糖", "ratio": "豆瓣酱1:糖0.3", "score": 3, "note": "缺少发酵风味"},
        {"substitute": "味噌", "ratio": "1:0.8", "score": 3, "note": "日式替代，风味接近"},
    ],
    "椰浆": [
        {"substitute": "牛奶+椰蓉", "ratio": "牛奶200ml+椰蓉30g", "score": 3, "note": "加热搅拌可模拟椰香"},
        {"substitute": "淡奶油", "ratio": "1:0.7", "score": 2, "note": "奶香替代椰香，完全不同"},
    ],
    "菜籽油": [
        {"substitute": "花生油", "ratio": "1:1", "score": 5, "note": "耐高温，炒菜首选替代"},
        {"substitute": "大豆油", "ratio": "1:1", "score": 4, "note": "经济实惠，味道中性"},
    ],
    "糯米": [
        {"substitute": "大米+淀粉", "ratio": "大米200g+淀粉1勺", "score": 3, "note": "黏度不够可加淀粉"},
        {"substitute": "粳米", "ratio": "1:1", "score": 2, "note": "完全无黏性"},
    ],
    "鲜奶油": [
        {"substitute": "牛奶+黄油", "ratio": "牛奶150ml+黄油30g", "score": 3, "note": "加热混合使用"},
        {"substitute": "炼乳+牛奶", "ratio": "炼乳50g+牛奶100ml", "score": 3, "note": "偏甜"},
    ],
    "咖喱粉": [
        {"substitute": "咖喱块", "ratio": "咖喱块50g替代2勺咖喱粉", "score": 5, "note": "味道更浓郁"},
        {"substitute": "姜黄粉+孜然+辣椒粉", "ratio": "1:0.5:0.3", "score": 3, "note": "自己调配咖喱风味"},
    ],
    "甜面酱": [
        {"substitute": "黄豆酱+糖", "ratio": "黄豆酱1:糖0.5", "score": 4, "note": "甜咸味接近"},
        {"substitute": "海鲜酱", "ratio": "1:1", "score": 3, "note": "更甜，有海鲜味"},
    ],
    "柱候酱": [
        {"substitute": "海鲜酱+豆瓣酱", "ratio": "海鲜酱1:豆瓣酱0.3", "score": 3, "note": "粤式炖肉替代方案"},
        {"substitute": "蚝油+生抽", "ratio": "蚝油1:生抽0.5", "score": 3, "note": "鲜味接近"},
    ],
    "虾油": [
        {"substitute": "鱼露+油", "ratio": "鱼露1:油3", "score": 3, "note": "鲜味来源不同"},
        {"substitute": "蚝油稀释", "ratio": "蚝油1:水2", "score": 2, "note": "风味差异大"},
    ],
}

# 通用替代规则
GENERAL_RULES = [
    "同类食材互换：叶菜换叶菜、根茎换根茎、菌菇换菌菇",
    "颜色相近替代：红色（西红柿/红椒/胡萝卜），绿色（青椒/豆角/西兰花）",
    "口感匹配：脆的换脆的（黄瓜换西芹），软的换软的（茄子换西葫芦）",
    "烹饪方式决定替代自由度：炖菜 > 炒菜 > 凉拌菜 — 炖菜替代空间最大",
    "先看调料再看食材：调料缺失影响大于主食材缺失",
]


def find_substitution(ingredient: str) -> dict:
    """查找食材替代方案"""
    ingredient = ingredient.strip()

    # 精确匹配
    if ingredient in SUBSTITUTION_DB:
        return {
            "ingredient": ingredient,
            "found": True,
            "alternatives": SUBSTITUTION_DB[ingredient],
        }

    # 模糊匹配
    for key in SUBSTITUTION_DB:
        if ingredient in key or key in ingredient:
            return {
                "ingredient": ingredient,
                "found": True,
                "matched_key": key,
                "alternatives": SUBSTITUTION_DB[key],
            }

    return {
        "ingredient": ingredient,
        "found": False,
        "message": f"暂无 {ingredient} 的替代数据，请尝试联网搜索或根据通用规则自行判断",
        "general_rules": GENERAL_RULES[:3],
    }


def check_recipe_substitutions(recipe_name: str, missing_ingredients: list[str]) -> dict:
    """检查菜谱中缺失食材的替代方案"""
    recipes = load_recipes()
    recipe = get_recipe_detail(recipes, recipe_name)

    if not recipe:
        return {"error": f"未找到菜谱: {recipe_name}"}

    substitutions = []
    for missing in missing_ingredients:
        sub = find_substitution(missing)
        substitutions.append(sub)

    return {
        "recipe": recipe_name,
        "missing_ingredients": missing_ingredients,
        "substitutions": substitutions,
        "general_rules": GENERAL_RULES,
    }


def main():
    parser = argparse.ArgumentParser(description="食材替换建议引擎")
    parser.add_argument("--missing", type=str, required=True, help="缺失的食材")
    parser.add_argument("--recipe", type=str, help="关联的菜名（可选）")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    missing = [m.strip() for m in args.missing.split(",") if m.strip()]

    if args.recipe:
        result = check_recipe_substitutions(args.recipe, missing)
    else:
        result = {"substitutions": [find_substitution(m) for m in missing]}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for sub in result.get("substitutions", []):
            ing = sub["ingredient"]
            if not sub["found"]:
                print(f"\n❓ {ing}: {sub.get('message', '未找到替代')}")
                continue

            alts = sub["alternatives"]
            print(f"\n🔄 **{ing}** 替代方案：\n")
            for i, alt in enumerate(alts):
                medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "📌"
                stars = "⭐" * alt["score"]
                print(f"  {medal} {alt['substitute']} — 替代比例: {alt['ratio']}")
                print(f"     评分: {stars} | {alt['note']}")
            print()

        if result.get("general_rules"):
            print("💡 通用替代原则:")
            for rule in result["general_rules"]:
                print(f"  • {rule}")


if __name__ == "__main__":
    main()
