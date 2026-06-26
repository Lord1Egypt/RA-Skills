#!/bin/bash
# GitHub Backup Script
# 用法: ./backup.sh [github-username] [repo-name] [token]

GITHUB_USER="${1}"
REPO_NAME="${2}"
TOKEN="${3}"
BACKUP_MESSAGE="${4:-Backup: $(date +%Y-%m-%d)}"

WORKSPACE_DIR="/root/.openclaw/workspace"
BACKUP_DIR="$WORKSPACE_DIR"

if [ -z "$GITHUB_USER" ] || [ -z "$REPO_NAME" ] || [ -z "$TOKEN" ]; then
    echo "用法: $0 <github-用户名> <仓库名> <token> [提交信息]"
    exit 1
fi

cd "$BACKUP_DIR"

# 配置 git (如果还没有)
git config user.email "backup@openclaw.local" 2>/dev/null || true
git config user.name "OpenClaw Backup" 2>/dev/null || true

# 设置 remote (如果还没有)
CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
EXPECTED_REMOTE="https://x-access-token:${TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

if [ "$CURRENT_REMOTE" != "$EXPECTED_REMOTE" ]; then
    git remote set-url origin "$EXPECTED_REMOTE" 2>/dev/null || \
    git remote add origin "$EXPECTED_REMOTE"
fi

# 添加需要备份的文件
git add AGENTS.md SOUL.md USER.md IDENTITY.md TOOLS.md HEARTBEAT.md README.md SYNC.md .gitignore skills/ memory/ 2>/dev/null

# 检查是否有更改
if git diff --staged --quiet; then
    echo "没有需要备份的更改"
    exit 0
fi

# 提交
git commit -m "$BACKUP_MESSAGE"

# 推送
if git push origin main 2>&1; then
    echo "备份成功！"
    exit 0
else
    # 如果是首次推送，可能需要设置 main 分支
    git push -u origin main
    exit 0
fi