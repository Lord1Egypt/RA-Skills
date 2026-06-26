# 每日早晨自动读取记忆脚本

# 每日 08:00 读取昨日记忆和长期记忆
# 添加到 crontab: 0 8 * * * ~/.openclaw/workspace/scripts/morning-memory-read.sh

#!/bin/bash
set -e

WORKSPACE=~/.openclaw/workspace
MEMORY_DIR=$WORKSPACE/memory
MEMORY_MD=$WORKSPACE/MEMORY.md
YESTERDAY=$(date -v-1d +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 晨间记忆读取..."

# 创建今日记忆文件
TODAY_FILE=$MEMORY_DIR/${TODAY}.md
if [ ! -f "$TODAY_FILE" ]; then
    cat > "$TODAY_FILE" << EOF
# ${TODAY} 记忆日志

**日期**: $(date -v-1d +%Y 年 %-m 月 %-d 日) $(date -v-1d +%A)  
**时区**: Asia/Shanghai (GMT+8)

---

## 📝 今日重要事件

### 上午 (08:00-12:00)
- [待记录]

### 下午 (12:00-18:00)
- [待记录]

### 晚上 (18:00-24:00)
- [待记录]

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

- [ ] [待添加]

---

## 🔗 相关链接

- [记忆仓库]: 待同步

---

*创建时间：${TIMESTAMP}*  
*最后更新：${TIMESTAMP}*  
*同步状态：⏳ 待同步 (下次：今日 23:55)*
EOF
    echo "✅ 创建今日记忆文件：${TODAY_FILE}"
fi

# 读取昨日记忆（如果有）
YESTERDAY_FILE=$MEMORY_DIR/${YESTERDAY}.md
if [ -f "$YESTERDAY_FILE" ]; then
    echo "📖 昨日记忆存在：${YESTERDAY_FILE}"
    # 可以在这里添加逻辑将昨日记忆摘要添加到今日文件
else
    echo "ℹ️  无昨日记忆文件"
fi

# 检查长期记忆
if [ -f "$MEMORY_MD" ]; then
    echo "📖 长期记忆存在：${MEMORY_MD}"
else
    echo "⚠️  长期记忆文件不存在"
fi

# 从 GitHub 拉取最新记忆（如果已配置）
if git -C $WORKSPACE remote get-url memory >/dev/null 2>&1; then
    echo "🔄 从 GitHub 拉取最新记忆..."
    cd $WORKSPACE
    git fetch memory main 2>/dev/null || true
    git merge memory/main --ff-only 2>/dev/null || echo "ℹ️  无需合并或已是最新"
fi

echo "✅ 晨间记忆读取完成"
