#!/bin/bash
# OpenClaw 权限检查脚本

CONFIG_FILE="$HOME/.openclaw/openclaw.json"

echo "=========================================="
echo "  OpenClaw 权限检查"
echo "=========================================="
echo ""

ERRORS=0

# 1. 检查 tools.profile
echo "📋 检查 tools.profile..."
TOOLS_PROFILE=$(python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    print(c.get('tools', {}).get('profile', 'NOT_SET'))
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null)

if [ "$TOOLS_PROFILE" = "full" ]; then
    echo "  ✅ tools.profile = full"
else
    echo "  ❌ tools.profile = $TOOLS_PROFILE (应该是 full)"
    ERRORS=$((ERRORS + 1))
fi

# 2. 检查 exec 权限
echo ""
echo "📋 检查 exec 权限..."
HAS_EXEC=$(python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    tools = c.get('agents', {}).get('list', [{}])[0].get('tools', {}).get('alsoAllow', [])
    print('yes' if 'exec' in tools else 'no')
except:
    print('no')
" 2>/dev/null)

if [ "$HAS_EXEC" = "yes" ]; then
    echo "  ✅ exec 权限已配置"
else
    echo "  ⚠️  exec 未在 alsoAllow 中"
fi

# 3. 检查 gateway 权限
echo ""
echo "📋 检查 gateway 权限..."
HAS_GATEWAY=$(python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    tools = c.get('agents', {}).get('list', [{}])[0].get('tools', {}).get('alsoAllow', [])
    print('yes' if 'gateway' in tools else 'no')
except:
    print('no')
" 2>/dev/null)

if [ "$HAS_GATEWAY" = "yes" ]; then
    echo "  ✅ gateway 权限已配置"
else
    echo "  ⚠️  gateway 未在 alsoAllow 中"
fi

# 4. 检查飞书配置
echo ""
echo "📋 检查飞书配置..."
FEISHU_APP_ID=$(python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    print(c.get('channels', {}).get('feishu', {}).get('appId', 'NOT_SET'))
except:
    print('NOT_SET')
" 2>/dev/null)

FEISHU_ENABLED=$(python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    print(c.get('channels', {}).get('feishu', {}).get('enabled', False))
except:
    print(False)
" 2>/dev/null)

if [ "$FEISHU_ENABLED" = "True" ] || [ "$FEISHU_ENABLED" = "true" ]; then
    echo "  ✅ 飞书已启用"
    if [ "$FEISHU_APP_ID" != "NOT_SET" ]; then
        echo "  ✅ AppId: $FEISHU_APP_ID"
    else
        echo "  ❌ AppId 未设置"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  ⚠️  飞书未启用"
fi

# 5. 检查 Gateway 进程
echo ""
echo "📋 检查 Gateway 状态..."
if pgrep -f "openclaw.*gateway" > /dev/null; then
    PID=$(pgrep -f "openclaw.*gateway")
    echo "  ✅ Gateway 运行中 (PID: $PID)"
    
    if nc -z -w 1 127.0.0.1 18789 2>/dev/null; then
        echo "  ✅ 端口 18789 监听正常"
    else
        echo "  ⚠️  端口 18789 未监听"
    fi
else
    echo "  ❌ Gateway 未运行"
    ERRORS=$((ERRORS + 1))
fi

# 总结
echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo "  ✅ 所有检查通过！"
else
    echo "  ⚠️  发现 $ERRORS 个问题"
    echo ""
    echo "  运行以下命令修复:"
    echo "  bash ~/.openclaw/workspace/skills/openclaw-upgrade/scripts/post-upgrade-fix.sh"
fi
echo "=========================================="
echo ""
