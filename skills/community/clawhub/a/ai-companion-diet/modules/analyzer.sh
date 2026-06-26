#!/bin/bash

# 数据分析模块

source "$SKILL_DIR/modules/calculator.sh"

# 显示今日总结
show_daily_summary() {
    local today=$(date +%Y%m%d)
    local daily_file="$DATA_DIR/daily_records/${today}.json"
    
    if [[ ! -f "$daily_file" ]]; then
        echo "今日还没有记录，请先开始: start-daily-plan"
        return 1
    fi
    
    python3 << EOF
import json

with open("$daily_file", 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 50)
print("📊 今日减肥总结 - $(date +%Y年%m月%d日)")
print("=" * 50)
print()

# 步数统计
steps = data['steps']
target_steps = data['target_steps']
steps_progress = min(100, int(steps / target_steps * 100))
print(f"🚶 今日步数: {steps} / {target_steps} 步")
print(f"   进度: [{'█' * (steps_progress // 10)}{'░' * (10 - steps_progress // 10)}] {steps_progress}%")
print()

# 热量统计
total_calories = data['total_calories']
target_deficit = data['target_calorie_deficit']
print(f"🍽️  今日摄入总热量: {total_calories} kcal")
print(f"   目标热量差: {target_deficit} kcal")
print()

# 详细餐食记录
meal_names = {'breakfast': '🌅 早餐', 'lunch': '☀️ 午餐', 'dinner': '🌙 晚餐', 'snack': '🍪 加餐'}
for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
    meals = data['meals'][meal_type]
    if meals:
        meal_calories = sum(m['calories'] for m in meals)
        print(f"{meal_names[meal_type]} ({meal_calories} kcal):")
        for meal in meals:
            print(f"   - {meal['name']}: {meal['calories']} kcal ({meal['time']})")
        print()

# 体重
if data['weight']:
    print(f"⚖️  今日体重: {data['weight']} kg")
    print()

# 鼓励语
if steps >= target_steps and total_calories < 2000:
    print("🎉 完美的一天！继续保持，你离目标越来越近了！")
elif steps >= target_steps:
    print("👍 运动达标了！注意控制一下饮食哦～")
elif total_calories < 2000:
    print("💪 饮食控制得不错！再多走几步就更好了！")
else:
    print("🎯 明天继续加油！相信自己一定可以！")

print("=" * 50)
EOF
}

# 显示体重趋势
show_weight_trend() {
    local weight_history="$DATA_DIR/weight_history.json"
    
    if [[ ! -f "$weight_history" ]]; then
        echo "还没有体重记录数据"
        return 1
    fi
    
    python3 << EOF
import json

with open("$weight_history", 'r', encoding='utf-8') as f:
    history = json.load(f)

if len(history) < 2:
    print("需要至少2条记录才能显示趋势")
else:
    history.sort(key=lambda x: x['date'])
    
    print("=" * 50)
    print("📈 体重变化趋势")
    print("=" * 50)
    print()
    
    first = history[0]
    last = history[-1]
    total_change = last['weight'] - first['weight']
    
    print(f"起始体重: {first['weight']} kg ({first['date']})")
    print(f"最新体重: {last['weight']} kg ({last['date']})")
    print(f"总体重变化: {'+' if total_change > 0 else ''}{total_change:.2f} kg")
    print()
    
    print("最近7天记录:")
    for record in history[-7:]:
        change = ""
        idx = history.index(record)
        if idx > 0:
            prev = history[idx - 1]
            diff = record['weight'] - prev['weight']
            change = f" ({'+' if diff > 0 else ''}{diff:.2f} kg)"
        print(f"  {record['date']}: {record['weight']} kg{change}")
    
    print()
    if total_change < 0:
        print("🎉 恭喜减重成功！继续保持！")
    elif total_change == 0:
        print("⚖️  体重保持稳定")
    else:
        print("💪 加油，还有进步空间！")
    print("=" * 50)
EOF
}

# 周度分析
show_weekly_analysis() {
    echo "📅 周度分析功能（开发中）"
    echo "将包含："
    echo "- 本周平均步数统计"
    echo "- 本周平均热量摄入"
    echo "- 本周减重/增重情况"
    echo "- 下周目标建议"
}

# 平台期分析
analyze_plateau() {
    local weight_history="$DATA_DIR/weight_history.json"
    
    if [[ ! -f "$weight_history" ]]; then
        echo "还没有足够的体重数据进行分析"
        return 1
    fi
    
    python3 << EOF
import json

with open("$weight_history", 'r', encoding='utf-8') as f:
    history = json.load(f)

if len(history) < 14:
    print("需要至少14天的数据才能分析平台期")
else:
    history.sort(key=lambda x: x['date'])
    recent = history[-14:]
    weights = [h['weight'] for h in recent]
    weight_range = max(weights) - min(weights)
    
    print("=" * 50)
    print("🔍 平台期分析")
    print("=" * 50)
    print()
    print(f"最近14天体重波动范围: {weight_range:.2f} kg")
    print()
    
    if weight_range < 0.5:
        print("⚠️  检测到可能处于平台期")
        print()
        print("平台期建议:")
        print("1. 增加运动强度或改变运动方式")
        print("2. 调整饮食结构，增加蛋白质摄入")
        print("3. 保证充足睡眠（7-8小时）")
        print("4. 增加饮水量（每天2-3升）")
        print("5. 保持耐心，平台期是正常现象")
        print("6. 可以尝试轻断食（如8+16模式）")
    else:
        print("✅ 体重在正常波动范围内，未检测到平台期")
        print("继续保持良好的饮食和运动习惯！")
    print("=" * 50)
EOF
}

# 预测减重趋势
predict_weight_loss() {
    local weight_history="$DATA_DIR/weight_history.json"
    
    if [[ ! -f "$weight_history" ]]; then
        echo "还没有足够的体重数据进行预测"
        return 1
    fi
    
    python3 << EOF
import json
import numpy as np

with open("$weight_history", 'r', encoding='utf-8') as f:
    history = json.load(f)

if len(history) < 7:
    print("需要至少7天的数据才能进行预测")
else:
    history.sort(key=lambda x: x['date'])
    weights = [h['weight'] for h in history]
    
    # 简单线性回归预测
    x = np.arange(len(weights))
    slope, intercept = np.polyfit(x, weights, 1)
    
    # 计算平均每周减重
    weekly_loss = abs(slope * 7)
    
    # 读取目标体重
    with open("$DATA_DIR/user_data.json", 'r', encoding='utf-8') as f:
        user_data = json.load(f)
    
    target_weight = user_data['target_weight']
    current_weight = weights[-1]
    
    print("=" * 50)
    print("🔮 减重趋势预测")
    print("=" * 50)
    print()
    print(f"当前体重: {current_weight} kg")
    print(f"目标体重: {target_weight} kg")
    print(f"还需减重: {current_weight - target_weight:.2f} kg")
    print()
    
    if slope < 0:
        print(f"📉 平均每周减重: {weekly_loss:.2f} kg")
        if weekly_loss > 0:
            weeks_needed = (current_weight - target_weight) / weekly_loss
            print(f"⏱️  预计还需要: {weeks_needed:.1f} 周达到目标")
            print()
            print("💡 建议:")
            if weekly_loss > 1:
                print("- 减重速度偏快，建议适当放缓，注意身体健康")
            elif weekly_loss < 0.25:
                print("- 减重速度较慢，可以适当增加运动量或调整饮食")
            else:
                print("- 减重速度在健康范围内，继续保持！")
    else:
        print("📈 体重呈上升趋势，建议调整饮食和运动计划")
    
    print("=" * 50)
EOF
}
