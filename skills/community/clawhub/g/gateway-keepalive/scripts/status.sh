#!/bin/bash
# Gateway Keepalive - 状态检查
# 作者: 康妃 (config)
# 版本: 1.1.0

echo "🦞 Gateway Keepalive 状态"
echo "========================"
echo ""

# 检查 LaunchAgents
echo "📋 LaunchAgent 状态:"
GATEWAY_STATUS=$(launchctl list | grep "ai.openclaw.gateway" | awk '{print $1}')
HEALTH_STATUS=$(launchctl list | grep "com.openclaw.health-check" | awk '{print $1}')

if [ -n "$GATEWAY_STATUS" ]; then
    echo "  ✅ Gateway (PID: $GATEWAY_STATUS)"
else
    echo "  ❌ Gateway 未运行"
fi

if [ -n "$HEALTH_STATUS" ]; then
    echo "  ✅ Health Check"
else
    echo "  ❌ Health Check 未运行"
fi

echo ""

# 检查 Gateway 进程
echo "🔍 Gateway 进程:"
if pgrep -f "openclaw gateway" > /dev/null; then
    PID=$(pgrep -f "openclaw gateway")
    echo "  ✅ 进程运行中 (PID: $PID)"
else
    echo "  ❌ 进程未运行"
fi

echo ""

# 检查端口
echo "🌐 端口状态:"
if nc -z localhost 18789 2>/dev/null; then
    echo "  ✅ 端口 18789 正常"
else
    echo "  ❌ 端口 18789 无响应"
fi

echo ""

# 检查黄金备份
echo "📦 黄金备份:"
if [ -f ~/.openclaw/backups/golden-config/openclaw.json ]; then
    SIZE=$(du -h ~/.openclaw/backups/golden-config/openclaw.json | cut -f1)
    MODIFIED=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" ~/.openclaw/backups/golden-config/openclaw.json 2>/dev/null || stat -c "%y" ~/.openclaw/backups/golden-config/openclaw.json 2>/dev/null | cut -d'.' -f1)
    echo "  ✅ 存在 ($SIZE, 更新于 $MODIFIED)"
else
    echo "  ❌ 不存在"
fi

echo ""

# 检查失败计数
echo "📊 失败计数:"
if [ -f ~/.openclaw/state/recovery-count ]; then
    COUNT=$(cat ~/.openclaw/state/recovery-count)
    echo "  当前: $COUNT / 3"
else
    echo "  当前: 0 / 3"
fi

echo ""

# 检查日志
echo "📋 健康检测日志:"
if [ -f ~/.openclaw/logs/health-recovery.log ]; then
    SIZE=$(du -h ~/.openclaw/logs/health-recovery.log | cut -f1)
    LAST_CHECK=$(tail -1 ~/.openclaw/logs/health-recovery.log 2>/dev/null | cut -d'[' -f2 | cut -d']' -f1)
    echo "  大小: $SIZE"
    echo "  最后检测: $LAST_CHECK"

    # 统计
    TOTAL=$(grep -c "健康检测" ~/.openclaw/logs/health-recovery.log 2>/dev/null || echo "0")
    RECOVERIES=$(grep -c "自动恢复成功" ~/.openclaw/logs/health-recovery.log 2>/dev/null || echo "0")
    echo "  总检测: $TOTAL 次"
    echo "  成功恢复: $RECOVERIES 次"
else
    echo "  ❌ 日志不存在"
fi

echo ""

# 检查压缩日志
echo "🗂️ 压缩日志:"
COMPRESSED=$(ls ~/.openclaw/logs/health-recovery.log.*.gz 2>/dev/null | wc -l | tr -d ' ')
if [ "$COMPRESSED" -gt 0 ]; then
    echo "  ✅ $COMPRESSED 个压缩文件"
    ls -lh ~/.openclaw/logs/health-recovery.log.*.gz 2>/dev/null | tail -3 | awk '{print "    " $NF " (" $5 ")"}'
else
    echo "  无压缩文件"
fi

echo ""
echo "========================"
