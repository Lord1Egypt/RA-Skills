#!/bin/bash
# 对话复盘脚本 — 每次对话结束后调用
# 用法: bash review.sh "日志文件路径" "输出目录"

log_path="$1"
output_dir="${2:-memory}"

mkdir -p "$output_dir"

echo "📋 开始复盘..."
echo ""

# 检查是否有新信息需要归档
echo "检查项:"
echo "  [ ] 有没有新决策/方向变化？"
echo "  [ ] 有没有新项目/术语？"
echo "  [ ] 有没有收到反馈/批评？"
echo "  [ ] 有没有用户偏好/习惯？"
echo "  [ ] 有没有值得跨领域推导的信息？"
echo ""

# 生成今日日志占位
date_str=$(date +%Y-%m-%d)
log_file="$output_dir/$date_str.md"

if [ ! -f "$log_file" ]; then
    cat > "$log_file" << LOG
# $date_str 日志

> 由 Agent Memory Keeper 自动创建

## 今日事项

_请在此记录今日的重要决策、进度、教训_

## 知识沉淀

_新学到的知识点、值得记下来的东西_

## 待办

- [ ]
LOG
    echo "✅ 已创建今日日志: $log_file"
else
    echo "📄 今日日志已存在: $log_file"
fi

echo ""
echo "✅ 复盘完成"
