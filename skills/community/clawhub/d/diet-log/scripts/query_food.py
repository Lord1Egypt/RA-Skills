#!/usr/bin/env python3
"""
饮食记录 Skill - 食物查询脚本 v2
增强版：支持多营养字段、分类匹配、维生素矿物质全量返回
用法: python query_food.py <食物关键词> [limit]
"""
import json
import sys
import os
import re

def parse_number(value_str):
    """从营养值字符串中提取数字（克/千卡/微克/毫克）"""
    if not value_str or value_str in ('-', '—', '', '克', '微克', '毫克'):
        return 0.0
    # 去掉单位
    cleaned = re.sub(r'[千微毫]?[克卡路里]|[a-zA-Z%（）()\s]', '', str(value_str))
    match = re.search(r'[\d.]+', cleaned)
    if match:
        try:
            return float(match.group())
        except:
            return 0.0
    return 0.0

def search_foods(query, food_data, limit=5):
    """
    在食物数据库中模糊搜索匹配的食物
    匹配策略（优先级递减）：
    1. 名字完全相等 > 名字以查询词开头 > 名字包含查询词
    2. 别名包含查询词
    3. 分类匹配（type 字段匹配查询词）
    4. 返回空列表（需人工介入提问）
    """
    query_lower = query.lower().strip()
    exact = []       # 优先级1：精确相等
    prefix = []      # 优先级2：名字以查询词开头
    contains = []    # 优先级3：名字包含查询词
    nickname_hit = [] # 优先级4：别名匹配
    seen_names = set()

    for item in food_data:
        name = item.get('name', '')
        nickname = item.get('nickname', '')
        if name in seen_names:
            continue

        name_lower = name.lower()
        nick_lower = nickname.lower()

        if name_lower == query_lower:
            exact.append(item)
            seen_names.add(name)
        elif name_lower.startswith(query_lower) or name_lower.startswith(query_lower.replace('类', '')):
            prefix.append(item)
            seen_names.add(name)
        elif query_lower in name_lower:
            contains.append(item)
            seen_names.add(name)
        elif query_lower in nick_lower:
            nickname_hit.append(item)
            seen_names.add(name)

    # 按优先级组装结果
    results = exact + prefix + contains + nickname_hit
    return results[:limit]

def format_food_info(item, include_all=True):
    """
    将单条食物记录格式化为完整的营养摘要
    include_all=True 时返回全部可用字段
    """
    info = item.get('info', {})

    def get_val(key):
        return info.get(key, '-')

    def get_num(key):
        return parse_number(info.get(key, '0'))

    # 宏量营养素（核心）
    macro = {
        'energy_kcal': get_num('能量'),
        'protein_g': get_num('蛋白质'),
        'fat_g': get_num('脂肪'),
        'carbs_g': get_num('碳水化合物'),
        'fiber_g': get_num('粗纤维'),
    }

    # 脂肪酸详情
    fatty_acids = {
        'saturated_fat_g': get_num('饱和脂肪酸'),
        'monounsaturated_fat_g': get_num('单不饱和脂肪酸'),
        'polyunsaturated_fat_g': get_num('多不饱和脂肪酸'),
        'trans_fat_g': get_num('反式脂肪酸'),
    }

    # 矿物质
    minerals = {
        'calcium_mg': get_num('钙'),
        'magnesium_mg': get_num('镁'),
        'sodium_mg': get_num('钠'),
        'potassium_mg': get_num('钾'),
        'phosphorus_mg': get_num('磷'),
        'iron_mg': get_num('铁'),
        'zinc_mg': get_num('锌'),
        'selenium_mg': get_num('硒'),
        'copper_mg': get_num('铜'),
        'manganese_mg': get_num('锰'),
    }

    # 维生素
    vitamins = {
        'vitamin_a_mcg': get_num('维生素A'),
        'vitamin_c_mg': get_num('维生素C'),
        'vitamin_d_mcg': get_num('维生素D'),
        'vitamin_e_mg': get_num('维生素E'),
        'vitamin_k_mcg': get_num('维生素K'),
        'vitamin_b1_mg': get_num('维生素B1（硫胺素）'),
        'vitamin_b2_mg': get_num('维生素B2（核黄素）'),
        'vitamin_b3_mg': get_num('维生素B3（烟酸）'),
        'vitamin_b5_mg': get_num('维生素B5（泛酸）'),
        'vitamin_b6_mg': get_num('维生素B6'),
        'vitamin_b7_mcg': get_num('维生素B7（生物素）'),
        'vitamin_b9_mcg': get_num('维生素B9（叶酸）'),
        'vitamin_b12_mcg': get_num('维生素B12'),
    }

    result = {
        'name': item.get('name'),
        'nickname': item.get('nickname'),
        'type': item.get('type'),
        **macro,
        **fatty_acids,
        **minerals,
        **vitamins,
        'raw_info': {
            'energy': get_val('能量'),
            'protein': get_val('蛋白质'),
            'fat': get_val('脂肪'),
            'carbs': get_val('碳水化合物'),
        }
    }

    return result

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '用法: python query_food.py <食物关键词> [limit]'}, ensure_ascii=False, indent=2))
        sys.exit(1)

    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) >= 3 else 5

    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    data_path = os.path.join(skill_dir, 'references', 'food_data.json')

    if not os.path.exists(data_path):
        print(json.dumps({'error': f'数据文件不存在: {data_path}'}, ensure_ascii=False, indent=2))
        sys.exit(1)

    with open(data_path, 'r', encoding='utf-8') as f:
        food_data = json.load(f)

    results = search_foods(query, food_data, limit=limit)

    if not results:
        print(json.dumps({
            'query': query,
            'matches': 0,
            'results': [],
            'suggestion': '未找到匹配食物，请提供更多描述或说明食物类别'
        }, ensure_ascii=False, indent=2))
        return

    formatted = [format_food_info(item) for item in results]

    output = {
        'query': query,
        'matches': len(formatted),
        'results': formatted
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
