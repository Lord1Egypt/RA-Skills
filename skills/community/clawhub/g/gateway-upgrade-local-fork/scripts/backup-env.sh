#!/bin/bash
# backup-env.sh - 一键备份 OpenClaw 升级前状态
# 用法: bash backup-env.sh
#
# 备份核心: service unit (含 user 自定义 env) + per agent dbs
# 大版本升级建议也备份 binary 目录

set -e

BACKUP_TS=$(date +%Y%m%d-%H%M%S)
echo "=== OpenClaw upgrade backup ==="
echo "Timestamp: $BACKUP_TS"
echo ""

# 1. 备份 service unit (必做)
SERVICE=~/.config/systemd/user/openclaw-gateway.service
SERVICE_BAK="${SERVICE}.bak.${BACKUP_TS}"
cp "$SERVICE" "$SERVICE_BAK"
echo "✓ service unit: $SERVICE_BAK"
echo ""

# 2. 备份 per agent qmd dbs (必做)
DB_COUNT=0
for db in $(find ~/.openclaw/agents/*/qmd/xdg-cache/qmd/ -name "index.sqlite" 2>/dev/null); do
    cp "$db" "$db.bak.${BACKUP_TS}"
    DB_COUNT=$((DB_COUNT + 1))
done
echo "✓ per agent dbs: $DB_COUNT 个 (备份到 .bak.${BACKUP_TS})"
echo ""

# 3. (可选) 备份 binary 目录 - 大版本升级建议
# cp -r $HOME/openclaw-local{,.bak.${BACKUP_TS}}

# 4. (可选) 备份 plugin configs - 大版本升级建议
# cp -r $HOME/openclaw-local/extensions{,.bak.${BACKUP_TS}}

# 5. npm global 列表 (推荐)
NPM_LIST=/tmp/npm-global-pre-upgrade-${BACKUP_TS}.txt
npm list -g --depth=0 > "$NPM_LIST" 2>&1
echo "✓ npm global list: $NPM_LIST"
echo ""

# 6. qmd doctor baseline (推荐)
QMD_DOC=/tmp/qmd-doctor-pre-upgrade-${BACKUP_TS}.txt
qmd doctor > "$QMD_DOC" 2>&1
echo "✓ qmd doctor baseline: $QMD_DOC"
echo ""

# 7. 当前 binary 版本
BIN_VER=$(node -e "console.log(require('\$HOME/openclaw-local/package.json').version)" 2>/dev/null)
echo "当前 binary version: $BIN_VER"
echo "BACKUP_TS: $BACKUP_TS"
echo ""
echo "=== 备份完成 ==="
echo "如果升级后需要回滚, 用这个 BACKUP_TS:"
echo "  $BACKUP_TS"
