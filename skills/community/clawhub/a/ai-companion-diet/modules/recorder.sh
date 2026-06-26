#!/bin/bash

# 数据记录模块

source "$SKILL_DIR/modules/calculator.sh"

# 初始化用户数据
init_user_data() {
    local user_data_file="$DATA_DIR/user_data.json"
    
    if [[ -f "$user_data_file" ]]; then
        echo "用户数据已存在，是否覆盖？(y/n)"
        read -r confirm
        if [[ "$confirm" != "y" ]]; then
            echo "已取消初始化"
            return
        fi
    fi
    
    echo "=== 用户基础数据初始化 ==="
    read -p "请输入性别 (male/female): " gender
    read -p "请输入年龄: " age
    read -p "请输入身高 (cm): " height
    read -p "请输入初始体重 (kg): " initial_weight
    read -p "请输入目标体重 (kg): " target_weight
    read -p "请输入日常活动水平 (sedentary/light/moderate/heavy): " activity_level
    
    local bmr=$(calculate_bmr "$gender" "$age" "$height" "$initial_weight")
    local tdee=$(calculate_tdee "$bmr" "$activity_level")
    local target_calorie_deficit=500  # 目标每天500大卡热量差
    local target_steps=$(calculate_target_steps "$target_calorie_deficit")
    
    cat > "$user_data_file" << EOF
{
    "gender": "$gender",
    "age": $age,
    "height": $height,
    "initial_weight": $initial_weight,
    "target_weight": $target_weight,
    "activity_level": "$activity_level",
    "bmr": $bmr,
    "tdee": $tdee,
    "target_calorie_deficit": $target_calorie_deficit,
    "target_steps": $target_steps,
    "created_at": "$(date +%Y-%m-%d)"
}
EOF
    
    echo "用户数据初始化完成！"
    echo "基础代谢率 (BMR): $bmr kcal"
    echo "每日总能量消耗 (TDEE): $tdee kcal"
    echo "每日目标步数: $target_steps 步"
}

# 开始今日计划
start_daily_plan() {
    local today=$(date +%Y%m%d)
    local daily_file="$DATA_DIR/daily_records/${today}.json"
    
    if [[ ! -f "$DATA_DIR/user_data.json" ]]; then
        echo "请先初始化用户数据: init-user-data"
        return 1
    fi
    
    if [[ -f "$daily_file" ]]; then
        echo "今日计划已存在，查看今日总结请使用: daily-summary"
        return
    fi
    
    local user_data=$(cat "$DATA_DIR/user_data.json")
    local target_steps=$(echo "$user_data" | grep -o '"target_steps": [0-9]*' | grep -o '[0-9]*')
    local target_calorie_deficit=$(echo "$user_data" | grep -o '"target_calorie_deficit": [0-9]*' | grep -o '[0-9]*')
    
    cat > "$daily_file" << EOF
{
    "date": "$today",
    "meals": {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snack": []
    },
    "steps": 0,
    "weight": null,
    "target_steps": $target_steps,
    "target_calorie_deficit": $target_calorie_deficit,
    "total_calories": 0
}
EOF
    
    echo "=== 今日减肥计划已开始 ==="
    echo "日期: $(date +%Y年%m月%d日)"
    echo "目标步数: $target_steps 步"
    echo "目标热量差: ${target_calorie_deficit} kcal"
    echo ""
    echo "记得按时记录饮食和运动情况哦！💪"
}

# 记录饮食
# 参数: 餐别 食物描述 [重量]
record_meal() {
    local meal_type="$1"
    local food_desc="$2"
    local weight="${3:-100}"
    
    local today=$(date +%Y%m%d)
    local daily_file="$DATA_DIR/daily_records/${today}.json"
    
    if [[ ! -f "$daily_file" ]]; then
        echo "请先开始今日计划: start-daily-plan"
        return 1
    fi
    
    local estimated_calories=$(estimate_food_calories "$food_desc" "$weight")
    
    # 更新每日记录
    local daily_data=$(cat "$daily_file")
    
    # 创建新的餐食记录
    local meal_record="{\"name\": \"$food_desc\", \"weight\": $weight, \"calories\": $estimated_calories, \"time\": \"$(date +%H:%M)\"}"
    
    # 使用Python更新JSON（简化处理）
    python3 << EOF
import json
import sys

with open("$daily_file", 'r', encoding='utf-8') as f:
    data = json.load(f)

meal_record = json.loads('$meal_record')
data['meals']['$meal_type'].append(meal_record)
data['total_calories'] = sum(
    meal['calories'] 
    for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']
    for meal in data['meals'][meal_type]
)

with open("$daily_file", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
EOF
    
    local meal_name=""
    case "$meal_type" in
        breakfast) meal_name="早餐" ;;
        lunch) meal_name="午餐" ;;
        dinner) meal_name="晚餐" ;;
        snack) meal_name="加餐" ;;
    esac
    
    echo "✅ 已记录$meal_name: $food_desc"
    echo "   估算热量: ${estimated_calories} kcal"
    
    # 鼓励语
    if (( $(echo "$estimated_calories < 400" | bc -l) )); then
        echo "   很棒！选择了健康的食物！🌟"
    fi
}

# 记录步数
record_steps() {
    local steps="$1"
    
    local today=$(date +%Y%m%d)
    local daily_file="$DATA_DIR/daily_records/${today}.json"
    
    if [[ ! -f "$daily_file" ]]; then
        echo "请先开始今日计划: start-daily-plan"
        return 1
    fi
    
    python3 << EOF
import json

with open("$daily_file", 'r', encoding='utf-8') as f:
    data = json.load(f)

data['steps'] = $steps

with open("$daily_file", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
EOF
    
    echo "✅ 已记录今日步数: $steps 步"
    
    # 检查是否达标
    local target_steps=$(grep -o '"target_steps": [0-9]*' "$daily_file" | grep -o '[0-9]*')
    if (( steps >= target_steps )); then
        echo "🎉 太棒了！今日步数已达标！继续保持！"
    elif (( steps >= target_steps * 8 / 10 )); then
        echo "💪 已经完成80%了！再加把劲就达标了！"
    else
        echo "🏃 目前完成了$((steps * 100 / target_steps))%，动起来吧！"
    fi
}

# 记录体重
record_weight() {
    local weight="$1"
    
    local today=$(date +%Y%m%d)
    local daily_file="$DATA_DIR/daily_records/${today}.json"
    local weight_history="$DATA_DIR/weight_history.json"
    
    if [[ ! -f "$daily_file" ]]; then
        echo "请先开始今日计划: start-daily-plan"
        return 1
    fi
    
    # 更新今日记录
    python3 << EOF
import json

with open("$daily_file", 'r', encoding='utf-8') as f:
    data = json.load(f)

data['weight'] = $weight

with open("$daily_file", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
EOF
    
    # 更新体重历史
    if [[ ! -f "$weight_history" ]]; then
        echo "[]" > "$weight_history"
    fi
    
    python3 << EOF
import json

with open("$weight_history", 'r', encoding='utf-8') as f:
    history = json.load(f)

# 移除同一天的旧记录
history = [h for h in history if h['date'] != '$today']
history.append({'date': '$today', 'weight': $weight})

with open("$weight_history", 'w', encoding='utf-8') as f:
    json.dump(history, f, ensure_ascii=False, indent=2)
EOF
    
    echo "✅ 已记录今日体重: ${weight} kg"
    
    # 计算BMI
    local user_data=$(cat "$DATA_DIR/user_data.json")
    local height=$(echo "$user_data" | grep -o '"height": [0-9]*' | grep -o '[0-9]*')
    local bmi=$(calculate_bmi "$weight" "$height")
    local bmi_category=$(get_bmi_category "$bmi")
    
    echo "   当前BMI: ${bmi} (${bmi_category})"
}
