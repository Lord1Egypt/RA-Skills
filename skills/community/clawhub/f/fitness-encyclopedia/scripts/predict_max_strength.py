#!/usr/bin/env python3
"""
最大力量预测器
根据训练重量和次数预测最大力量（1RM）
使用多种公式进行预测，取平均值
"""

import argparse
import json
import math


def predict_epley(weight, reps):
    """
    Epley公式
    1RM = weight × (1 + reps/30)

    参数:
        weight: 训练重量(公斤)
        reps: 重复次数

    返回:
        预测的1RM值
    """
    return weight * (1 + reps / 30)


def predict_brzycki(weight, reps):
    """
    Brzycki公式
    1RM = weight × 36 / (37 - reps)
    适用于reps < 10的情况

    参数:
        weight: 训练重量(公斤)
        reps: 重复次数

    返回:
        预测的1RM值
    """
    if reps >= 10:
        # 对于高次数使用Epley公式
        return predict_epley(weight, reps)
    return weight * 36 / (37 - reps)


def predict_lander(weight, reps):
    """
    Lander公式
    1RM = 100 × weight / (101.3 - 2.67123 × reps)

    参数:
        weight: 训练重量(公斤)
        reps: 重复次数

    返回:
        预测的1RM值
    """
    return 100 * weight / (101.3 - 2.67123 * reps)


def predict_lombardi(weight, reps):
    """
    Lombardi公式
    1RM = weight × reps^0.10

    参数:
        weight: 训练重量(公斤)
        reps: 重复次数

    返回:
        预测的1RM值
    """
    return weight * (reps ** 0.10)


def predict_one_rm(weight, reps, method='average'):
    """
    使用多种公式预测1RM，并根据method参数返回结果

    参数:
        weight: 训练重量(公斤)
        reps: 重复次数
        method: 返回方法 ('epley', 'brzycki', 'lander', 'lombardi', 'average')

    返回:
        预测的1RM值
    """
    # 计算各个公式的预测值
    epley_1rm = predict_epley(weight, reps)
    brzycki_1rm = predict_brzycki(weight, reps)
    lander_1rm = predict_lander(weight, reps)
    lombardi_1rm = predict_lombardi(weight, reps)

    predictions = {
        'epley': epley_1rm,
        'brzycki': brzycki_1rm,
        'lander': lander_1rm,
        'lombardi': lombardi_1rm
    }

    if method == 'average':
        # 排除最大最小值后取平均，减少异常值影响
        values = list(predictions.values())
        values_sorted = sorted(values)
        # 如果有4个值，去掉最大最小值后取平均
        if len(values_sorted) >= 4:
            trimmed = values_sorted[1:-1]
            avg_1rm = sum(trimmed) / len(trimmed)
        else:
            avg_1rm = sum(values) / len(values)
        return avg_1rm, predictions
    elif method in predictions:
        return predictions[method], predictions
    else:
        # 默认使用平均值
        values = list(predictions.values())
        return sum(values) / len(values), predictions


def calculate_training_percentages(one_rm):
    """
    根据最大力量计算训练强度百分比对应重量

    参数:
        one_rm: 最大力量(1RM)

    返回:
        dict: 不同强度百分比对应的训练重量
    """
    percentages = {
        '100%': 1.0,    # 1RM（极限）
        '95%': 0.95,    # 1-2次
        '90%': 0.90,    # 3-4次
        '85%': 0.85,    # 5-6次
        '80%': 0.80,    # 6-8次
        '75%': 0.75,    # 8-10次
        '70%': 0.70,    # 10-12次
        '65%': 0.65,    # 12-15次
        '60%': 0.60,    # 15次以上
    }

    training_weights = {}
    for percent, factor in percentages.items():
        training_weights[percent] = round(one_rm * factor, 2)

    return training_weights


def format_exercise_name(exercise_code):
    """
    将动作代码转换为中文名称

    参数:
        exercise_code: 动作代码

    返回:
        中文名称
    """
    exercise_names = {
        'bench_press': '卧推',
        'squat': '深蹲',
        'deadlift': '硬拉',
        'overhead_press': '推举',
        'barbell_row': '划船',
        'pull_up': '引体向上',
        'dip': '双杠臂屈伸',
        'leg_press': '腿举',
        'leg_curl': '腿弯举',
        'lat_pulldown': '高位下拉'
    }

    return exercise_names.get(exercise_code, exercise_code)


def main():
    parser = argparse.ArgumentParser(description='最大力量预测器')
    parser.add_argument('--exercise', required=True, help='动作名称 (如: bench_press, squat, deadlift)')
    parser.add_argument('--weight', type=float, required=True, help='训练重量(公斤)')
    parser.add_argument('--reps', type=int, required=True, help='重复次数')
    parser.add_argument('--method', default='average',
                       choices=['epley', 'brzycki', 'lander', 'lombardi', 'average'],
                       help='预测公式')
    parser.add_argument('--format', default='text', choices=['text', 'json'],
                       help='输出格式')

    args = parser.parse_args()

    # 验证输入
    if args.reps <= 0:
        print("错误：重复次数必须大于0")
        sys.exit(1)
    if args.weight <= 0:
        print("错误：训练重量必须大于0")
        sys.exit(1)

    # 预测1RM
    one_rm, all_predictions = predict_one_rm(args.weight, args.reps, args.method)

    # 计算训练强度百分比
    training_weights = calculate_training_percentages(one_rm)

    # 格式化动作名称
    exercise_cn_name = format_exercise_name(args.exercise)

    # 组装结果
    result = {
        'exercise': {
            'code': args.exercise,
            'name': exercise_cn_name
        },
        'input': {
            'weight_kg': args.weight,
            'reps': args.reps
        },
        'predictions': {
            'epley': round(all_predictions['epley'], 2),
            'brzycki': round(all_predictions['brzycki'], 2),
            'lander': round(all_predictions['lander'], 2),
            'lombardi': round(all_predictions['lombardi'], 2),
            'average': round(one_rm, 2)
        },
        'training_percentages': training_weights
    }

    # 输出结果
    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print(f"最大力量预测 - {exercise_cn_name}")
        print("=" * 60)

        print(f"\n【输入数据】")
        print(f"动作: {exercise_cn_name}")
        print(f"训练重量: {args.weight} kg")
        print(f"重复次数: {args.reps} 次")

        print(f"\n【预测结果】")
        print(f"Epley公式: {round(all_predictions['epley'], 2)} kg")
        print(f"Brzycki公式: {round(all_predictions['brzycki'], 2)} kg")
        print(f"Lander公式: {round(all_predictions['lander'], 2)} kg")
        print(f"Lombardi公式: {round(all_predictions['lombardi'], 2)} kg")
        print("-" * 40)
        print(f"平均预测值: {round(one_rm, 2)} kg")

        print(f"\n【训练强度参考】")
        print(f"基于预测的1RM ({round(one_rm, 2)} kg)，不同强度对应的重量：")
        for percent, weight in training_weights.items():
            print(f"  {percent:4s} = {weight:6.2f} kg  ({int(weight)} kg)")


if __name__ == '__main__':
    main()
