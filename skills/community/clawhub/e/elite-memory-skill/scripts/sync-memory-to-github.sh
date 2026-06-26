#!/bin/bash
# 记忆系统自动化脚本
# 每日 23:55 同步记忆到 GitHub 仓库
# 添加到 crontab: 55 23 * * * ~/.openclaw/workspace/scripts/sync-memory-to-github.sh

set -e

WORKSPACE=~/.openclaw/workspace
MEMORY_DIR=$WORKSPACE/memory
MEMORY_MD=$WORKSPACE/MEMORY.md
LOG_DIR=$WORKSPACE/logs
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE=$LOG_DIR/memory-sync.log

# 确保日志目录存在
mkdir -p $LOG_DIR

# 日志函数
log() {
    echo "[$TIMESTAMP] $1" | tee -a $LOG_FILE
}

# 飞书通知函数
send_feishu_notification() {
    local status=$1
    local message=$2
    local feishu_user_id="${FEISHU_USER_ID:-}"
    
    if [ -z "$feishu_user_id" ]; then
        log "⚠️ 未配置 FEISHU_USER_ID，跳过飞书通知"
        return 0
    fi
    
    log "📤 发送飞书通知..."
    
    # 使用 openclaw message 命令发送
    if [ "$status" == "success" ]; then
        emoji="✅"
        title="记忆同步成功"
    else
        emoji="❌"
        title="记忆同步失败"
    fi
    
    # 构建通知内容
    notification="$emoji **$title**

📅 日期：$TIMESTAMP
📊 状态：$status

$message

---
*自动推送通知*"

    # 尝试使用 openclaw 命令发送
    if command -v openclaw >/dev/null 2>&1; then
        export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
        openclaw message send --channel feishu --target "user:$feishu_user_id" --message "$notification" 2>/dev/null || log "⚠️ 飞书消息发送失败"
    else
        log "⚠️ openclaw 命令不可用，跳过飞书通知"
    fi
}

log "开始同步记忆到 GitHub..."

# 检查是否已配置 memory remote
if ! git -C $WORKSPACE remote get-url memory >/dev/null 2>&1; then
    error_msg="❌ 未配置 memory remote。请先运行：gh repo create ai-memory --private"
    log "$error_msg"
    send_feishu_notification "failure" "$error_msg"
    exit 1
fi

# 更新 MEMORY.md 的同步时间
if [ -f "$MEMORY_MD" ]; then
    sed -i.bak "s/\*同步状态：.*/\*同步状态：✅ 已同步 (上次：$TIMESTAMP)/" "$MEMORY_MD"
    sed -i.bak "s/\*下次同步：.*/\*下次同步：明日 23:55/" "$MEMORY_MD"
    rm -f "${MEMORY_MD}.bak"
fi

# 更新今日记忆文件的同步状态
TODAY_FILE=$MEMORY_DIR/${TODAY}.md
if [ -f "$TODAY_FILE" ]; then
    sed -i.bak "s/\*同步状态：.*/\*同步状态：✅ 已同步 (上次：$TIMESTAMP)/" "$TODAY_FILE"
    sed -i.bak "s/\*下次同步：.*/\*下次同步：明日 23:55/" "$TODAY_FILE"
    rm -f "${TODAY_FILE}.bak"
fi

# Git 操作
cd $WORKSPACE

git add -A
git commit -m "🧠 记忆同步 $(date '+%Y-%m-%d %H:%M')" --allow-empty 2>/dev/null || echo "无变更"

# 推送并捕获结果
push_result=0
git push memory main 2>&1 || {
    log "⚠️ 推送失败，尝试先拉取..."
    git pull --rebase memory main 2>/dev/null || push_result=1
    if [ $push_result -eq 0 ]; then
        git push memory main 2>/dev/null || push_result=1
    fi
}

if [ $push_result -eq 0 ]; then
    log "✅ 记忆同步完成"
    
    # 统计变更
    changed_files=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null | wc -l | tr -d ' ')
    
    success_msg="**本次同步内容:**
- 临时记忆文件 (${TODAY}-temp.md)
- 正式记忆文件 (${TODAY}.md)
- 长期记忆 (MEMORY.md)
- SESSION-STATE.md

**同步详情:**
- 提交：$(git rev-parse --short HEAD 2>/dev/null || echo "N/A")
- 文件变更：${changed_files} 个
- GitHub: renguanjie/ai-memory"
    
    send_feishu_notification "success" "$success_msg"
else
    error_msg="⚠️ GitHub 推送失败，可能是网络问题。已本地提交，下次同步时重试。"
    log "$error_msg"
    send_feishu_notification "failure" "$error_msg"
fi
