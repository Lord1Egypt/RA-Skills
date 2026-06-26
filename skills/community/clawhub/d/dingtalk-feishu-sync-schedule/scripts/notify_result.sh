#!/bin/bash
# 钉钉同步完成后发送飞书通知
# 从 /var/log/dingtalk_sync.log 读取最新结果并发送

LOG_FILE="/var/log/dingtalk_sync.log"

# 从 ~/.feishu/config.json 读取 user_open_id
FEISHU_CONFIG="${HOME}/.feishu/config.json"
if [ -f "$FEISHU_CONFIG" ]; then
    TARGET=$(python3 -c "import json,sys; d=json.load(open('$FEISHU_CONFIG')); uid=d.get('user_open_id',''); print('user:'+uid if uid else '')" 2>/dev/null)
fi

if [ -z "$TARGET" ]; then
    echo "❌ 错误: ~/.feishu/config.json 中缺少 user_open_id，无法发送通知" >&2
    exit 1
fi

# 读取最新同步结果
RESULT=$(tail -30 "$LOG_FILE" | grep -A 15 "同步完成" | head -20)

if [ -z "$RESULT" ]; then
    MESSAGE="✅ 钉钉→飞书自动同步完成，日志无异常"
else
    COUNT=$(echo "$RESULT" | grep "成功创建" | head -1)
    if [ -z "$COUNT" ]; then
        COUNT="同步完成"
    fi
    MESSAGE="✅ 钉钉→飞书自动同步\n\n$COUNT\n\n详情查看飞书日历"
fi

# 发送飞书通知
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
/root/.nvm/versions/node/v22.22.0/bin/openclaw message send --channel feishu --target "$TARGET" --message "$MESSAGE"
