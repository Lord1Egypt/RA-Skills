#!/usr/bin/env python3
"""
健身营养计算器
基于用户信息计算基础代谢、热量需求、营养配比
"""

import argparse
import json
import sys


def calculate_bmr(gender, height_cm, weight_kg, age):
    """
    使用Mifflin-St Jeor方程计算基础代谢率(BMR)

    参数:
        gender: 性别 ('male' 或 'female')
        height_cm: 身高(厘米)
        weight_kg: 体重(公斤)
        age: 年龄

    返回:
        BMR值(大卡)
    """
    if gender == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:  # female
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    return round(bmr)


def calculate_tdee(bmr, activity_level):
    """
    计算日常总消耗(TDEE)
    基于模型：基础代谢约占每日总耗能的70%，因此 TDEE = BMR / 0.7

    参数:
        bmr: 基础代谢率
        activity_level: 活动量 ('sedentary', 'light', 'moderate', 'active', 'very_active')

    返回:
        TDEE值(大卡)
    """
    # 基础模型：TDEE = BMR / 0.7
    base_tdee = bmr / 0.7

    # 根据活动量进行微调
    activity_multiplier = {
        'sedentary': 1.0,
        'light': 1.1,
        'moderate': 1.2,
        'active': 1.3,
        'very_active': 1.4
    }

    multiplier = activity_multiplier.get(activity_level, 1.0)
    tdee = base_tdee * multiplier

    return round(tdee)


def calculate_target_calories(tdee, goal):
    """
    计算目标热量

    参数:
        tdee: 日常总消耗
        goal: 目标 ('cut' 减脂, 'maintain' 保持, 'bulk' 增肌)

    返回:
        目标热量(大卡)
    """
    # 系数说明（基于运动营养学标准）：
    # 减脂：0.75（25%热量缺口，约500-750大卡，科学且可持续）
    # 保持：1.0（维持热量平衡）
    # 增肌：0.90（10%热量盈余，约300-500大卡，避免过多脂肪堆积）

    goal_coefficients = {
        'cut': 0.75,
        'maintain': 1.0,
        'bulk': 0.90
    }

    coefficient = goal_coefficients.get(goal, 1.0)
    target = tdee * coefficient

    return round(target)


def calculate_macros(target_calories, weight_kg, goal, gender, is_training_day=True):
    """
    计算三大营养素配比

    参数:
        target_calories: 目标热量
        weight_kg: 体重(公斤)
        goal: 目标 ('cut' 减脂, 'maintain' 保持, 'bulk' 增肌)
        gender: 性别 ('male' 或 'female')
        is_training_day: 是否为训练日

    返回:
        dict: 包含蛋白质、碳水、脂肪的克数
    """
    # 脂肪固定值（克）
    fat_g = 60 if gender == 'male' else 50
    fat_cal = fat_g * 9  # 脂肪每克9大卡

    # 剩余热量分配给蛋白质和碳水
    remaining_cal = target_calories - fat_cal

    # 蛋白质需求（克/公斤体重）
    if goal == 'cut':
        # 减脂期蛋白质需求更高
        if is_training_day:
            protein_per_kg = 2.0
        else:
            protein_per_kg = 1.8
    elif goal == 'bulk':
        # 增肌期
        if is_training_day:
            protein_per_kg = 1.8
        else:
            protein_per_kg = 1.6
    else:  # maintain
        # 保持期
        if is_training_day:
            protein_per_kg = 1.6
        else:
            protein_per_kg = 1.4

    protein_g = round(protein_per_kg * weight_kg)
    protein_cal = protein_g * 4  # 蛋白质每克4大卡

    # 碳水获取剩余热量
    carb_cal = remaining_cal - protein_cal
    carb_g = round(carb_cal / 4)  # 碳水每克4大卡

    return {
        'protein': protein_g,
        'carbs': carb_g,
        'fat': fat_g
    }


def generate_meal_plan(macros_training, macros_rest, goal, training_time='evening'):
    """
    生成一日饮食安排示例

    参数:
        macros_training: 训练日营养配比
        macros_rest: 休息日营养配比
        goal: 目标
        training_time: 训练时段 ('morning', 'noon', 'evening')

    返回:
        dict: 一日饮食安排
    """
    # 食物等价交换示例（每份营养量）
    protein_sources = {
        '鸡胸肉': {'protein': 30, 'cal': 140},
        '瘦牛肉': {'protein': 25, 'cal': 150},
        '鸡蛋': {'protein': 6, 'cal': 70},
        '鱼肉': {'protein': 22, 'cal': 120},
        '豆腐': {'protein': 15, 'cal': 90}
    }

    carb_sources = {
        '米饭': {'carbs': 30, 'cal': 130},  # 100g熟米饭
        '面条': {'carbs': 25, 'cal': 120},
        '燕麦': {'carbs': 40, 'cal': 150},
        '馒头': {'carbs': 50, 'cal': 220},
        '红薯': {'carbs': 20, 'cal': 86}
    }

    fat_sources = {
        '蛋黄': {'fat': 5, 'cal': 55},
        '牛奶': {'fat': 3, 'cal': 15},  # 每100ml
        '坚果': {'fat': 15, 'cal': 170},
        '植物油': {'fat': 14, 'cal': 120}
    }

    # 根据训练时段生成饮食框架
    if training_time == 'morning':
        # 早上练：练前餐→训练→练后餐→午饭→晚饭
        meal_structure = {
            '练前餐': '燕麦+鸡蛋',
            '训练': '抗阻训练',
            '练后餐': '蛋白粉/蛋白餐+碳水',
            '午饭': '正餐',
            '晚饭': '正餐'
        }
    elif training_time == 'noon':
        # 中午练：早饭→练前餐→训练→练后餐→晚饭
        meal_structure = {
            '早饭': '碳水+蛋白',
            '练前餐': '少量碳水',
            '训练': '抗阻训练',
            '练后餐': '蛋白餐+碳水',
            '晚饭': '正餐'
        }
    else:  # evening
        # 晚上练：早饭→午饭→练前餐→训练→练后餐
        meal_structure = {
            '早饭': '碳水+蛋白',
            '午饭': '正餐',
            '练前餐': '碳水',
            '训练': '抗阻训练',
            '练后餐': '蛋白餐'
        }

    return {
        'meal_structure': meal_structure,
        'training_day_macros': macros_training,
        'rest_day_macros': macros_rest,
        'food_examples': {
            'protein': protein_sources,
            'carbs': carb_sources,
            'fats': fat_sources
        }
    }


def main():
    parser = argparse.ArgumentParser(description='健身营养计算器')
    parser.add_argument('--gender', required=True, choices=['male', 'female'], help='性别')
    parser.add_argument('--height', type=float, required=True, help='身高(厘米)')
    parser.add_argument('--weight', type=float, required=True, help='体重(公斤)')
    parser.add_argument('--age', type=int, required=True, help='年龄')
    parser.add_argument('--activity', required=True,
                       choices=['sedentary', 'light', 'moderate', 'active', 'very_active'],
                       help='活动量')
    parser.add_argument('--goal', required=True, choices=['cut', 'maintain', 'bulk'],
                       help='目标: cut(减脂), maintain(保持), bulk(增肌)')
    parser.add_argument('--training-time', default='evening',
                       choices=['morning', 'noon', 'evening'],
                       help='训练时段')
    parser.add_argument('--format', default='text', choices=['text', 'json'],
                       help='输出格式')

    args = parser.parse_args()

    # 计算BMR
    bmr = calculate_bmr(args.gender, args.height, args.weight, args.age)

    # 计算TDEE
    tdee = calculate_tdee(bmr, args.activity)

    # 计算目标热量
    target_calories = calculate_target_calories(tdee, args.goal)

    # 计算训练日和休息日的营养配比
    macros_training = calculate_macros(target_calories, args.weight, args.goal,
                                      args.gender, is_training_day=True)
    macros_rest = calculate_macros(target_calories, args.weight, args.goal,
                                   args.gender, is_training_day=False)

    # 生成饮食计划
    meal_plan = generate_meal_plan(macros_training, macros_rest, args.goal, args.training_time)

    # 组装结果
    result = {
        'user_info': {
            'gender': args.gender,
            'height_cm': args.height,
            'weight_kg': args.weight,
            'age': args.age,
            'activity_level': args.activity,
            'goal': args.goal
        },
        'calculations': {
            'bmr': bmr,
            'tdee': tdee,
            'target_calories': target_calories,
            'calorie_deficit_surplus': target_calories - tdee
        },
        'macros': {
            'training_day': macros_training,
            'rest_day': macros_rest
        },
        'meal_plan': meal_plan
    }

    # 输出结果
    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("营养计算结果")
        print("=" * 60)
        print(f"\n【基本信息】")
        print(f"性别: {'男' if args.gender == 'male' else '女'}")
        print(f"身高: {args.height} cm")
        print(f"体重: {args.weight} kg")
        print(f"年龄: {args.age} 岁")
        print(f"活动量: {args.activity}")
        print(f"目标: {'减脂' if args.goal == 'cut' else ('增肌' if args.goal == 'bulk' else '保持')}")

        print(f"\n【热量计算】")
        print(f"基础代谢率(BMR): {bmr} 大卡/天")
        print(f"日常总消耗(TDEE): {tdee} 大卡/天")
        print(f"目标热量: {target_calories} 大卡/天")
        if args.goal == 'cut':
            print(f"热量缺口: {tdee - target_calories} 大卡/天")
        elif args.goal == 'bulk':
            print(f"热量盈余: {target_calories - tdee} 大卡/天")

        print(f"\n【营养配比】")
        print(f"训练日:")
        print(f"  蛋白质: {macros_training['protein']}g ({macros_training['protein'] * 4}大卡)")
        print(f"  碳水化合物: {macros_training['carbs']}g ({macros_training['carbs'] * 4}大卡)")
        print(f"  脂肪: {macros_training['fat']}g ({macros_training['fat'] * 9}大卡)")

        print(f"\n休息日:")
        print(f"  蛋白质: {macros_rest['protein']}g ({macros_rest['protein'] * 4}大卡)")
        print(f"  碳水化合物: {macros_rest['carbs']}g ({macros_rest['carbs'] * 4}大卡)")
        print(f"  脂肪: {macros_rest['fat']}g ({macros_rest['fat'] * 9}大卡)")

        print(f"\n【一日饮食安排示例（{args.training_time}练）】")
        for meal, desc in meal_plan['meal_structure'].items():
            print(f"  {meal}: {desc}")


if __name__ == '__main__':
    main()
