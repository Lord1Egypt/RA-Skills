#!/bin/bash
# Gateway Delayed Restart - 延迟重启网关（带通知）
# 用法：./restart.sh [延迟分钟数]

DELAY_MINUTES=${1:-2}
DELAY_SECONDS=$((DELAY_MINUTES * 60))
RESTART_TIME=$(date -d "+${DELAY_MINUTES} minutes" '+%H:%M:%S')
START_TIME=$(date +%s)

echo "⏰ 将在 ${DELAY_MINUTES} 分钟后重启 Gateway"
echo "📅 重启时间：${RESTART_TIME}"
echo ""

# 倒计时
for remaining in $(seq $DELAY_SECONDS -1 1); do
    mins=$((remaining / 60))
    secs=$((remaining % 60))
    printf "\r⏳ 剩余：%d分%02d秒" $mins $secs
    sleep 1
done

echo ""
echo "🔄 正在重启 Gateway..."
openclaw gateway restart

RESULT=$?
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
COMPLETE_TIME=$(date '+%H:%M:%S')

# 获取 PID
GATEWAY_PID=$(pgrep -f "openclaw-gateway" | tail -1)

echo ""
echo "=================================================="
echo "📊 重启报告"
echo "=================================================="
if [ $RESULT -eq 0 ]; then
    echo "✅ Gateway 重启成功！"
    STATUS="成功"
else
    echo "❌ Gateway 重启失败！"
    STATUS="失败"
fi
echo "📅 完成时间：${COMPLETE_TIME}"
echo "⏱️ 总耗时：${DURATION}秒"
echo "🔧 进程 PID: ${GATEWAY_PID:-未知}"
echo "=================================================="

# 发送通知
if [ $RESULT -eq 0 ]; then
    MESSAGE="🎉 Gateway 重启${STATUS}！时间：${COMPLETE_TIME}，耗时：${DURATION}秒"
    openclaw message send \
        --channel feishu \
        --target ou_6650e2645a6e8f4c7363cbbfd6bbcf33 \
        --message "$MESSAGE" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "📱 通知已发送"
    fi
fi

exit $RESULT
