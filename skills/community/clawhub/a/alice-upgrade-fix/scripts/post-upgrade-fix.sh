#!/bin/bash
# OpenClaw 升级后修复脚本
# 修复常见问题：插件冲突、权限重置、目录清理

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
LOG_FILE="$HOME/.openclaw/logs/upgrade.log"

log() {
    echo "[$(date)] $1" | tee -a "$LOG_FILE"
}

echo "=========================================="
echo "  OpenClaw 升级后修复"
echo "=========================================="
echo ""

# 步骤1: 清理插件运行时目录
echo "🧹 步骤1: 清理插件冲突目录..."

PLUGIN_DEPS="$HOME/.openclaw/plugin-runtime-deps"

# 找出旧版本目录
OLD_DIRS=$(ls -d "$PLUGIN_DEPS"/openclaw-unknown-* "$PLUGIN_DEPS"/openclaw-2026.* 2>/dev/null | grep -v "$(openclaw --version 2>/dev/null | head -1 | cut -d' ' -f2)" || true)

if [ -n "$OLD_DIRS" ]; then
    echo "发现旧版本插件目录:"
    echo "$OLD_DIRS"
    echo ""
    echo "正在清理..."
    for dir in $OLD_DIRS; do
        rm -rf "$dir"
        echo "  ✅ 已删除: $(basename $dir)"
    done
    log "清理了 $(echo "$OLD_DIRS" | wc -l) 个旧插件目录"
else
    echo "✅ 没有旧的插件目录"
fi

# 步骤2: 检查 tools.profile
echo ""
echo "🔧 步骤2: 检查工具权限..."

TOOLS_PROFILE=$(python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    print(c.get('tools', {}).get('profile', 'messaging'))
except:
    print('error')
" 2>/dev/null)

if [ "$TOOLS_PROFILE" != "full" ]; then
    echo "⚠️  tools.profile 是 '$TOOLS_PROFILE'，正在修复为 'full'..."
    python3 << 'PYEOF' "$CONFIG_FILE" 2>/dev/null
import json, sys
config_file = sys.argv[1]
with open(config_file, 'r') as f:
    config = json.load(f)
config.setdefault('tools', {})['profile'] = 'full'
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)
print("✅ tools.profile 已修复为 full")
PYEOF
    log "修复了 tools.profile"
else
    echo "✅ tools.profile = full"
fi

# 步骤3: 验证配置 JSON
echo ""
echo "📋 步骤3: 验证配置..."

if python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
    echo "✅ 配置 JSON 格式正确"
else
    echo "❌ 配置 JSON 格式错误！尝试从备份恢复..."
    LATEST_BACKUP=$(ls -t "$HOME/.openclaw/backups"/openclaw.json.bak.* 2>/dev/null | head -1)
    if [ -n "$LATEST_BACKUP" ]; then
        cp "$LATEST_BACKUP" "$CONFIG_FILE"
        echo "✅ 已从备份恢复: $(basename $LATEST_BACKUP)"
        log "从备份恢复配置: $LATEST_BACKUP"
    fi
fi

# 步骤4: 检查飞书插件
echo ""
echo "🔌 步骤4: 检查飞书插件..."

FEISHU_ENABLED=$(python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    print(c.get('plugins', {}).get('entries', {}).get('feishu', {}).get('enabled', False))
except:
    print(False)
" 2>/dev/null)

if [ "$FEISHU_ENABLED" = "True" ] || [ "$FEISHU_ENABLED" = "true" ]; then
    echo "✅ 飞书插件已启用"
    
    # 检查 appId 配置
    FEISHU_APP_ID=$(python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    print(c.get('channels', {}).get('feishu', {}).get('appId', ''))
except:
    print('')
" 2>/dev/null)
    
    if [ -n "$FEISHU_APP_ID" ]; then
        echo "✅ 飞书 AppId: $FEISHU_APP_ID"
    else
        echo "⚠️  飞书 AppId 未配置"
    fi
else
    echo "⚠️  飞书插件未启用"
fi

# 步骤5: 重启 Gateway
echo ""
echo "🔄 步骤5: 重启 Gateway..."

openclaw gateway restart 2>&1 | tee -a "$LOG_FILE"
sleep 8

# 验证
if nc -z -w 1 127.0.0.1 18789 2>/dev/null; then
    echo "✅ Gateway 重启成功"
    log "Gateway 重启成功"
else
    echo "⚠️  Gateway 可能未完全启动，请稍后检查"
fi

echo ""
echo "=========================================="
echo "  修复完成！"
echo "=========================================="
echo ""
echo "如仍有问题，请查看日志:"
echo "  tail -50 ~/.openclaw/logs/gateway.err.log"
echo ""
