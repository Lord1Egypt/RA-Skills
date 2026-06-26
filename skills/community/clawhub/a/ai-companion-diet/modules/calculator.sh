#!/bin/bash

# 热量计算模块

# 计算BMR (基础代谢率)
# 参数: 性别 年龄 身高(cm) 体重(kg)
calculate_bmr() {
    local gender="$1"
    local age="$2"
    local height="$3"
    local weight="$4"
    
    if [[ "$gender" == "male" ]]; then
        # 男性: BMR = 88.362 + (13.397 × 体重kg) + (4.799 × 身高cm) - (5.677 × 年龄)
        echo "scale=2; 88.362 + (13.397 * $weight) + (4.799 * $height) - (5.677 * $age)" | bc
    else
        # 女性: BMR = 447.593 + (9.247 × 体重kg) + (3.098 × 身高cm) - (4.330 × 年龄)
        echo "scale=2; 447.593 + (9.247 * $weight) + (3.098 * $height) - (4.330 * $age)" | bc
    fi
}

# 计算TDEE (每日总能量消耗)
# 参数: BMR 活动系数
calculate_tdee() {
    local bmr="$1"
    local activity_level="$2"
    
    local activity_factor
    case "$activity_level" in
        sedentary)    activity_factor="1.2" ;;  # 久坐
        light)        activity_factor="1.375" ;; # 轻度活动
        moderate)     activity_factor="1.55" ;;  # 中度活动
        heavy)        activity_factor="1.725" ;; # 重度活动
        *)            activity_factor="1.375" ;; # 默认轻度活动
    esac
    
    echo "scale=2; $bmr * $activity_factor" | bc
}

# 计算目标热量差对应的步数
# 参数: 热量差(kcal)
calculate_target_steps() {
    local calorie_deficit="$1"
    # 每走1000步约消耗30-40千卡，取平均值35
    echo "scale=0; ($calorie_deficit * 1000) / 35" | bc
}

# 估算食物热量
# 参数: 食物名称 [重量(g)]
estimate_food_calories() {
    local food_name="$1"
    local weight="${2:-100}"  # 默认100g
    
    # 常见食物热量表（每100g）
    declare -A food_calories=(
        ["米饭"]=116 ["面条"]=284 ["馒头"]=221 ["面包"]=312
        ["鸡蛋"]=144 ["牛奶"]=54 ["豆浆"]=16 ["酸奶"]=72
        ["苹果"]=52 ["香蕉"]=91 ["橙子"]=47 ["西瓜"]=25
        ["鸡肉"]=167 ["牛肉"]=125 ["猪肉"]=143 ["鱼肉"]=113
        ["青菜"]=20 ["白菜"]=17 ["菠菜"]=24 ["西兰花"]=34
        ["西红柿"]=18 ["黄瓜"]=15 ["土豆"]=77 ["红薯"]=86
        ["豆腐"]=70 ["豆浆"]=16 ["豆皮"]=245 ["豆干"]=140
        ["油"]=900 ["盐"]=0 ["糖"]=400 ["酱油"]=63
    )
    
    local calories_per_100g="${food_calories[$food_name]}"
    
    if [[ -z "$calories_per_100g" ]]; then
        # 如果不在列表中，使用AI估算或提示用户
        echo "100"  # 默认值，实际应调用AI分析
    else
        echo "scale=2; $calories_per_100g * $weight / 100" | bc
    fi
}

# 计算BMI
# 参数: 体重(kg) 身高(cm)
calculate_bmi() {
    local weight="$1"
    local height_cm="$2"
    local height_m=$(echo "scale=4; $height_cm / 100" | bc)
    echo "scale=2; $weight / ($height_m * $height_m)" | bc
}

# 获取BMI分类
get_bmi_category() {
    local bmi="$1"
    
    if (( $(echo "$bmi < 18.5" | bc -l) )); then
        echo "偏瘦"
    elif (( $(echo "$bmi < 24" | bc -l) )); then
        echo "正常"
    elif (( $(echo "$bmi < 28" | bc -l) )); then
        echo "超重"
    else
        echo "肥胖"
    fi
}
