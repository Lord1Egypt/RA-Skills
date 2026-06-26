#!/bin/bash

# 夜间反思脚本 - 每天 23:45 执行
# 功能：CRUD 验证 + 知识提炼 + 更新 INDEX.md 健康度
#
# 用法：./nightly-reflection.sh [--skip-reflection]

set -e

SKIP_REFLECTION="${1:-}"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${BLUE}=== $1 ===${NC}"
}

echo "========================================"
echo "  夜间反思开始 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 1. 确保 reflections 目录存在
mkdir -p "$MEMORY_DIR/reflections"
mkdir -p "$MEMORY_DIR/lessons"
mkdir -p "$MEMORY_DIR/decisions"
mkdir -p "$MEMORY_DIR/people"

# 2. 读取今日日志，分析内容
TODAY_LOG="$MEMORY_DIR/$TODAY.md"
log_section "检查今日日志"

if [ -f "$TODAY_LOG" ]; then
    log_info "找到今日日志：$TODAY_LOG"
    
    # 统计今日完成事项
    COMPLETED_COUNT=$(grep -c "✅\|完成\|done" "$TODAY_LOG" 2>/dev/null || echo "0")
    TODO_COUNT=$(grep -c "\- \[ \]" "$TODAY_LOG" 2>/dev/null || echo "0")
    
    echo "  - 完成事项：$COMPLETED_COUNT 个"
    echo "  - 待办事项：$TODO_COUNT 个"
    
    # 检查日志大小
    LOG_SIZE=$(wc -c < "$TODAY_LOG")
    echo "  - 日志大小：$LOG_SIZE bytes"
else
    log_warn "今日日志不存在：$TODAY_LOG"
    log_info "建议创建今日日志文件"
fi

# 3. 验证核心文件
log_section "验证核心文件"

# MEMORY.md
if [ -f "$WORKSPACE/MEMORY.md" ]; then
    MEMORY_SIZE=$(wc -c < "$WORKSPACE/MEMORY.md")
    MEMORY_LINES=$(wc -l < "$WORKSPACE/MEMORY.md")
    log_info "MEMORY.md: $MEMORY_LINES 行, $MEMORY_SIZE bytes"
else
    log_warn "MEMORY.md 不存在，建议创建"
fi

# INDEX.md
if [ -f "$MEMORY_DIR/INDEX.md" ]; then
    log_info "INDEX.md 存在"
else
    log_warn "INDEX.md 不存在，建议创建"
fi

# 4. 统计各目录
log_section "目录统计"

count_files() {
    local dir="$1"
    local name="$2"
    if [ -d "$dir" ]; then
        count=$(find "$dir" -name "*.md" -type f 2>/dev/null | wc -l)
        echo "  - $name: $count 个文件"
    else
        echo "  - $name: 目录不存在"
    fi
}

count_files "$MEMORY_DIR/lessons" "Lessons"
count_files "$MEMORY_DIR/decisions" "Decisions"
count_files "$MEMORY_DIR/people" "People"
count_files "$MEMORY_DIR/reflections" "Reflections"

# 5. 创建反思记录
if [ "$SKIP_REFLECTION" != "--skip-reflection" ]; then
    log_section "创建反思记录"
    
    REFLECTION_FILE="$MEMORY_DIR/reflections/$TODAY.md"
    
    # 检查是否已存在
    if [ -f "$REFLECTION_FILE" ]; then
        log_info "反思记录已存在：$REFLECTION_FILE"
    else
        cat > "$REFLECTION_FILE" << EOF
---
title: "$TODAY 反思"
date: $TODAY
category: reflections
type: daily-reflection
tags: [reflection, daily]
---

# $TODAY 反思

## ✅ 今日完成
- 自动生成的反思记录
- 详细内容由 Agent 补充

## 🤔 遇到的问题
- 

## 💡 学到的东西
- 

## 📝 需要跟进
- 

## 🎯 明天重点
- 

---
*自动生成时间：$(date '+%Y-%m-%d %H:%M:%S')*
EOF
        log_info "反思记录已创建：$REFLECTION_FILE"
    fi
fi

# 6. 更新 INDEX.md（如果存在）
log_section "更新 INDEX.md"

INDEX_FILE="$MEMORY_DIR/INDEX.md"
if [ -f "$INDEX_FILE" ]; then
    # 获取统计数据
    LESSONS_COUNT=$(find "$MEMORY_DIR/lessons" -name "*.md" -type f 2>/dev/null | wc -l)
    DECISIONS_COUNT=$(find "$MEMORY_DIR/decisions" -name "*.md" -type f 2>/dev/null | wc -l)
    PEOPLE_COUNT=$(find "$MEMORY_DIR/people" -name "*.md" -type f 2>/dev/null | wc -l)
    REFLECTIONS_COUNT=$(find "$MEMORY_DIR/reflections" -name "*.md" -type f 2>/dev/null | wc -l)
    
    # 检查是否需要更新
    if grep -q "健康度" "$INDEX_FILE" 2>/dev/null; then
        log_info "INDEX.md 已包含健康度统计"
    else
        log_info "添加健康度统计到 INDEX.md"
        echo "" >> "$INDEX_FILE"
        echo "## 📊 健康度统计" >> "$INDEX_FILE"
        echo "" >> "$INDEX_FILE"
        echo "| 类型 | 数量 | 最后更新 |" >> "$INDEX_FILE"
        echo "|------|------|----------|" >> "$INDEX_FILE"
        echo "| Lessons | $LESSONS_COUNT | $TODAY |" >> "$INDEX_FILE"
        echo "| Decisions | $DECISIONS_COUNT | $TODAY |" >> "$INDEX_FILE"
        echo "| People | $PEOPLE_COUNT | $TODAY |" >> "$INDEX_FILE"
        echo "| Reflections | $REFLECTIONS_COUNT | $TODAY |" >> "$INDEX_FILE"
    fi
fi

# 7. 检查冷数据
log_section "检查冷数据"

OLD_LOGS=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -mtime +30 2>/dev/null | wc -l)
if [ "$OLD_LOGS" -gt 0 ]; then
    log_warn "发现 $OLD_LOGS 个超过 30 天的日志文件（待归档）"
    log_info "建议运行 memory-gc.sh 进行归档"
else
    log_info "没有需要归档的冷数据"
fi

echo ""
echo "========================================"
echo "  夜间反思完成"
echo "========================================"