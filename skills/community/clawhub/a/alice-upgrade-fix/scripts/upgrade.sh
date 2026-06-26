#!/bin/bash
# OpenClaw 一键升级脚本
# 功能：备份 + 升级 + 验证

set -e

BACKUP_DIR="$HOME/.openclaw/backups"
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
LOG_FILE="$HOME/.openclaw/logs/upgrade.log"

mkdir -p "$BACKUP_DIR"
mkdir -p "$HOME/.openclaw/logs"

log() {
    echo "[$(date)] $1" | tee -a "$LOG_FILE"
}

echo "=========================================="
echo "  OpenClaw 一键升级"
echo "=========================================="
echo ""

# 获取当前版本
CURRENT_VERSION=$(openclaw --version 2>/dev/null | head -1 || echo "unknown")
log "当前版本: $CURRENT_VERSION"

# 步骤1: 备份配置
echo ""
echo "📦 步骤1: 备份配置..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 备份主配置
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$BACKUP_DIR/openclaw.json.bak.$TIMESTAMP"
    log "✅ 配置已备份: openclaw.json.bak.$TIMESTAMP"
fi

# 备份 auth
AUTH_FILE="$HOME/.openclaw/agents/main/agent/auth-profiles.json"
if [ -f "$AUTH_FILE" ]; then
    cp "$AUTH_FILE" "$BACKUP_DIR/auth-profiles.json.bak.$TIMESTAMP"
    log "✅ Auth 已备份"
fi

# 备份工作区关键文件
WORKSPACE="$HOME/.openclaw/workspace"
for file in MEMORY.md SOUL.md USER.md TOOLS.md AGENTS.md; do
    if [ -f "$WORKSPACE/$file" ]; then
        cp "$WORKSPACE/$file" "$BACKUP_DIR/$file.bak.$TIMESTAMP"
    fi
done
log "✅ 工作区文件已备份"

# 步骤2: 执行升级
echo ""
echo "⬆️  步骤2: 执行升级..."
log "开始升级..."

# 使用 gateway update 工具
echo "正在下载并安装最新版本，预计需要 3-5 分钟..."
npm i -g openclaw@latest --no-fund --no-audit --loglevel=error 2>&1 | tee -a "$LOG_FILE"

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ npm 安装失败"
    log "npm 安装失败"
    exit 1
fi

NEW_VERSION=$(openclaw --version 2>/dev/null | head -1 || echo "unknown")
log "新版本: $NEW_VERSION"

# 重启 Gateway
echo ""
echo "🔄 重启 Gateway..."
openclaw gateway restart 2>&1 | tee -a "$LOG_FILE"

# 等待启动
echo "等待 Gateway 启动..."
sleep 10

# 步骤3: 验证
echo ""
echo "✅ 步骤3: 验证升级..."

# 检查版本
echo "当前版本: $NEW_VERSION"

# 检查进程
if pgrep -f "openclaw.*gateway" > /dev/null; then
    echo "✅ Gateway 进程运行中"
    log "✅ Gateway 运行正常"
else
    echo "⚠️  Gateway 进程未找到，尝试重新启动..."
    openclaw gateway start
    sleep 5
fi

# 检查端口
if nc -z -w 1 127.0.0.1 18789 2>/dev/null; then
    echo "✅ 端口 18789 监听正常"
else
    echo "⚠️  端口 18789 未监听"
fi

echo ""
echo "=========================================="
echo "  升级完成！"
echo "=========================================="
echo ""
echo "📊 版本: $CURRENT_VERSION → $NEW_VERSION"
echo "📦 备份位置: $BACKUP_DIR"
echo "📝 日志: $LOG_FILE"
echo ""
echo "⚠️  升级后请检查:"
echo "   1. 运行 post-upgrade-fix.sh 修复可能的问题"
echo "   2. 检查工具权限: check-permissions.sh"
echo ""
