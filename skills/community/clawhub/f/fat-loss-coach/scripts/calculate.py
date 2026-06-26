#!/usr/bin/env python3
"""
Fat Loss Coach - 热量和营养计算工具
"""

import sys
import json

def calculate_bmr(gender, weight, height, age):
    """
    计算基础代谢率 (Mifflin-St Jeor 公式)
    
    Args:
        gender: 'male' 或 'female'
        weight: 体重 (kg)
        height: 身高 (cm)
        age: 年龄
    
    Returns:
        BMR (kcal/day)
    """
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return round(bmr, 1)

def calculate_tdee(bmr, activity_level):
    """
    计算每日总消耗
    
    Args:
        bmr: 基础代谢率
        activity_level: 活动系数 (1.2/1.375/1.55/1.725/1.9)
    
    Returns:
        TDEE (kcal/day)
    """
    return round(bmr * activity_level, 1)

def calculate_macros(target_calories, weight):
    """
    计算宏量营养素分配
    
    Args:
        target_calories: 目标热量
        weight: 体重 (kg)
    
    Returns:
        dict: {protein_g, fat_g, carb_g, protein_kcal, fat_kcal, carb_kcal}
    """
    # 蛋白质: 2g/kg
    protein_g = round(weight * 2, 1)
    protein_kcal = protein_g * 4
    
    # 脂肪: 0.8g/kg
    fat_g = round(weight * 0.8, 1)
    fat_kcal = fat_g * 9
    
    # 碳水: 剩余热量
    carb_kcal = target_calories - protein_kcal - fat_kcal
    carb_g = round(carb_kcal / 4, 1)
    
    return {
        'protein_g': protein_g,
        'protein_kcal': protein_kcal,
        'fat_g': fat_g,
        'fat_kcal': fat_kcal,
        'carb_g': carb_g,
        'carb_kcal': carb_kcal
    }

def calculate_target(tdee, deficit=400):
    """
    计算减脂目标热量
    
    Args:
        tdee: 每日总消耗
        deficit: 热量缺口 (默认400 kcal)
    
    Returns:
        目标热量
    """
    return round(tdee - deficit, 1)

def main():
    """
    主函数 - 从命令行参数或JSON输入计算
    """
    if len(sys.argv) > 1:
        # 命令行参数模式
        try:
            data = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Error: Invalid JSON input")
            sys.exit(1)
    else:
        print("Usage: calculate.py '{json_input}'")
        print("Example: calculate.py '{\"gender\":\"male\",\"weight\":80,\"height\":175,\"age\":30,\"activity\":1.375}'")
        sys.exit(0)
    
    # 解析输入
    gender = data.get('gender', 'male')
    weight = float(data.get('weight', 70))
    height = float(data.get('height', 170))
    age = int(data.get('age', 30))
    activity = float(data.get('activity', 1.375))
    deficit = float(data.get('deficit', 400))
    
    # 计算
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    target = calculate_target(tdee, deficit)
    macros = calculate_macros(target, weight)
    
    # 输出结果
    result = {
        'bmr': bmr,
        'tdee': tdee,
        'target_calories': target,
        'macros': macros
    }
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()