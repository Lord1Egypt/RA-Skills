#!/bin/bash
# fitness-planner 初始化脚本
# 创建必要的数据目录和文件

BASE_DIR="$HOME/.openclaw/workspace/fitness-planner"

# 创建目录结构
mkdir -p "$BASE_DIR"
mkdir -p "$BASE_DIR/plans"
mkdir -p "$BASE_DIR/records"

# 初始化默认配置
if [ ! -f "$BASE_DIR/config.json" ]; then
    cat > "$BASE_DIR/config.json" << 'EOF'
{
  "user": {
    "gender": null,
    "age": null,
    "goal": null,
    "location": null,
    "weekly_days": null,
    "session_duration": null,
    "experience": null,
    "limitations": []
  },
  "notification": {
    "channel": "wecom",
    "advance_minutes": 30,
    "morning_summary": true,
    "weekly_summary_day": "sunday",
    "weekly_summary_time": "20:00"
  },
  "created_at": null,
  "updated_at": null
}
EOF
    echo "已创建默认配置文件"
fi

# 初始化统计数据
if [ ! -f "$BASE_DIR/stats.json" ]; then
    cat > "$BASE_DIR/stats.json" << 'EOF'
{
  "total_workouts": 0,
  "total_minutes": 0,
  "current_streak": 0,
  "longest_streak": 0,
  "this_month": {
    "workouts": 0,
    "minutes": 0,
    "feeling_distribution": {
      "great": 0,
      "okay": 0,
      "tired": 0
    }
  },
  "last_workout": null
}
EOF
    echo "已创建统计文件"
fi

echo "健身规划助手初始化完成！"
echo "数据目录：$BASE_DIR"
