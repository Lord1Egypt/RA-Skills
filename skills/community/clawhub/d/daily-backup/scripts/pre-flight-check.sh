#!/bin/bash
# Daily Backup Pre-flight Check
# 只做检查，不做提交；输出变更状态供 agent 判断是否需要提交
# exit 0 = 是 git 仓库，exit 1 = 不是 git 仓库

AGENT_WORKSPACE="${AGENT_WORKSPACE:-/home/axelhu/.openclaw/workspace-main}"
LOG_DIR="$AGENT_WORKSPACE/data/exec-logs/daily-backup"
TODAY=$(date +%Y-%m-%d)

mkdir -p "$LOG_DIR"
cd "$AGENT_WORKSPACE" || exit 1

# 检查是否是 git 仓库
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "NOT_GIT_REPO"
    exit 1
fi

# 获取变更状态
# --porcelain: 简洁格式
# A = 新增, M = 修改, D = 删除, ? = 未跟踪
CHANGES=$(git status --porcelain 2>/dev/null)

if [ -z "$CHANGES" ]; then
    echo "NO_CHANGES"
    exit 0
fi

# 有变更：输出摘要
NEW_FILES=$(echo "$CHANGES" | grep "^A" | wc -l)
MODIFIED_FILES=$(echo "$CHANGES" | grep "^.M" | wc -l)
DELETED_FILES=$(echo "$CHANGES" | grep "^.D" | wc -l)
UNTRACKED_FILES=$(echo "$CHANGES" | grep "^?" | wc -l)

echo "HAS_CHANGES"
echo "NEW:$NEW_FILES"
echo "MODIFIED:$MODIFIED_FILES"
echo "DELETED:$DELETED_FILES"
echo "UNTRACKED:$UNTRACKED_FILES"

# 输出变更文件列表（最多 30 个）
echo "---FILES---"
echo "$CHANGES" | head -30
exit 0