#!/bin/bash
# 记忆分析归档脚本
# 每日 08:00 运行，分析前一天临时记忆 → 创建正式记忆 → 更新长期记忆

set -e

WORKSPACE=~/.openclaw/workspace
MEMORY_DIR=$WORKSPACE/memory
MEMORY_MD=$WORKSPACE/MEMORY.md
SESSION_STATE=$WORKSPACE/SESSION-STATE.md
YESTERDAY=$(date -v-1d +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 开始分析昨日记忆..."

# 检查临时记忆文件是否存在
TEMP_FILE=$MEMORY_DIR/${YESTERDAY}-temp.md
FORMAL_FILE=$MEMORY_DIR/${YESTERDAY}.md

if [ ! -f "$TEMP_FILE" ]; then
    echo "ℹ️  无昨日临时记忆文件，跳过分析"
    # 如果没有临时文件，检查是否已有正式文件
    if [ -f "$FORMAL_FILE" ]; then
        echo "✅ 昨日正式记忆文件已存在：${FORMAL_FILE}"
    else
        echo "⚠️  昨日无任何记忆文件"
    fi
    exit 0
fi

echo "📖 读取临时记忆：${TEMP_FILE}"

# 如果正式文件已存在，跳过创建
if [ -f "$FORMAL_FILE" ]; then
    echo "ℹ️  正式记忆文件已存在，仅更新长期记忆"
else
    # 创建正式记忆文件（简化版，实际需要 AI 分析）
    cat > "$FORMAL_FILE" << EOF
# ${YESTERDAY} 记忆日志

**日期**: $(date -v-1d +%Y 年 %-m 月 %-d 日) $(date -v-1d +%A)  
**时区**: Asia/Shanghai (GMT+8)

---

## 📝 今日重要事件

### 上午 (08:00-12:00)
- [待 AI 分析临时记忆后填充]

### 下午 (12:00-18:00)
- [待 AI 分析临时记忆后填充]

### 晚上 (18:00-24:00)
- [待 AI 分析临时记忆后填充]

---

## 🎯 今日决策

| 时间 | 决策 | 原因 |
|------|------|------|
| - | - | - |

---

## 💡 今日教训

| 问题 | 原因 | 改进 |
|------|------|------|
| - | - | - |

---

## 📋 待办事项

- [ ] [待 AI 分析临时记忆后填充]

---

## 🔗 相关链接

- [记忆仓库]: 待同步

---

*创建时间：${TIMESTAMP}*  
*最后更新：${TIMESTAMP}*  
*同步状态：⏳ 待同步 (下次：今日 23:55)*
EOF
    echo "✅ 创建正式记忆文件：${FORMAL_FILE}"
fi

# 更新 SESSION-STATE.md
if [ -f "$SESSION_STATE" ]; then
    echo "📝 更新 SESSION-STATE.md..."
    # 添加记忆分析完成标记
    sed -i.bak "s/## 记忆系统状态.*/## 记忆系统状态 (${TODAY} 更新)\n- ✅ 昨日记忆已分析归档/" "$SESSION_STATE"
    rm -f "${SESSION_STATE}.bak"
fi

# 从 GitHub 拉取最新记忆
if git -C $WORKSPACE remote get-url memory >/dev/null 2>&1; then
    echo "🔄 从 GitHub 拉取最新记忆..."
    cd $WORKSPACE
    git fetch memory main 2>/dev/null || true
    git merge memory/main --ff-only 2>/dev/null || echo "ℹ️  无需合并或已是最新"
fi

echo "✅ 记忆分析归档完成"
echo ""
echo "📋 下一步："
echo "   1. AI 读取 ${FORMAL_FILE} 和 ${TEMP_FILE}"
echo "   2. AI 分析临时记忆，填充正式记忆文件"
echo "   3. AI 提炼长期记忆，更新 MEMORY.md"
echo "   4. 今晚 23:55 自动同步到 GitHub"
