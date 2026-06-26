#!/bin/bash
# 克隆龙虾 - 从备份仓库恢复 OpenClaw/CatPaw 配置
# 用法: bash restore.sh [--workspace] [--config] [--skills] [--all]

set -e

BACKUP_REPO_URL="${CLONE_LOBSTER_REPO_URL:-}"
BACKUP_DIR="/tmp/clone-lobster-backup"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"

RESTORE_WORKSPACE=false
RESTORE_CONFIG=false
RESTORE_SKILLS=false

# 解析参数
if [ $# -eq 0 ] || [ "$1" = "--all" ]; then
    RESTORE_WORKSPACE=true
    RESTORE_CONFIG=true
    RESTORE_SKILLS=true
else
    for arg in "$@"; do
        case $arg in
            --workspace) RESTORE_WORKSPACE=true ;;
            --config) RESTORE_CONFIG=true ;;
            --skills) RESTORE_SKILLS=true ;;
        esac
    done
fi

if [ -z "$BACKUP_REPO_URL" ]; then
    echo "❌ 错误: 未配置备份仓库地址"
    exit 1
fi

# 克隆最新备份
echo "📦 获取最新备份..."
rm -rf "$BACKUP_DIR"
git clone "$BACKUP_REPO_URL" "$BACKUP_DIR" 2>&1
cd "$BACKUP_DIR"

if $RESTORE_WORKSPACE; then
    echo "📝 恢复工作区..."
    mkdir -p "$WORKSPACE_DIR"
    cp -r workspace/* "$WORKSPACE_DIR/" 2>/dev/null || true
    [ -d workspace/.openclaw ] && cp -r workspace/.openclaw "$WORKSPACE_DIR/" 2>/dev/null || true
    echo "   ✅ 工作区已恢复"
fi

if $RESTORE_CONFIG; then
    echo "⚙️  恢复配置..."
    mkdir -p "$OPENCLAW_DIR"
    cp config/*.json "$OPENCLAW_DIR/" 2>/dev/null || true
    echo "   ✅ 配置已恢复"
fi

if $RESTORE_SKILLS; then
    echo "🧩 恢复 Skills..."
    mkdir -p "$OPENCLAW_DIR/skills"
    cp -r skills/* "$OPENCLAW_DIR/skills/" 2>/dev/null || true
    echo "   ✅ Skills 已恢复"
fi

echo ""
echo "🦞 恢复完成！可能需要重启 OpenClaw 使配置生效。"
