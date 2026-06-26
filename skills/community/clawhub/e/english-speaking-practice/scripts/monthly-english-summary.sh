#!/bin/bash
# 每月最后一天 22:00 发送月度总结 - AI 版本

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"
DEFAULT_DATA_DIR="$SCRIPT_DIR/practice-data"

# 读取配置
if [ -f "$CONFIG_FILE" ]; then
    DATA_DIR=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('data',{}).get('baseDir','$DEFAULT_DATA_DIR'))")
    API_URL=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('api',{}).get('url',''))")
    API_KEY=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('api',{}).get('apiKey',''))")
    MODEL=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('api',{}).get('model','glm-5'))")
    TARGET_USER_ID=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('push',{}).get('targetUserId',''))")
    PUSH_CHANNEL=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('push',{}).get('channel','feishu'))")
else
    DATA_DIR="$DEFAULT_DATA_DIR"
    API_URL=""
    API_KEY=""
    MODEL="glm-5"
    TARGET_USER_ID="ou_your_user_id"
fi

# 相对路径转绝对路径
if [[ "$DATA_DIR" != /* ]]; then
    DATA_DIR="$SCRIPT_DIR/$DATA_DIR"
fi

# 检查今天是否是本月最后一天
today=$(date +%Y-%m-%d)
last_day=$(date -d "$(date +%Y-%m-01) +1 month -1 day" +%Y-%m-%d)

if [ "$today" = "$last_day" ]; then
    # 读取本月数据
    DATA_FILE=$DATA_DIR/$(date +%Y-%m).json
    
    if [ -f "$DATA_FILE" ]; then
        # 读取统计数据
        voc=$(python3 -c "import json;d=json.load(open('$DATA_FILE'));print(d.get('vocabulary',{}).get('totalCount',0))")
        err=$(python3 -c "import json;d=json.load(open('$DATA_FILE'));e=d.get('errors',{});print(e.get('grammar',[]).__len__()+e.get('pronunciation',[]).__len__()+e.get('wordChoice',[]).__len__())")
        good=$(python3 -c "import json;d=json.load(open('$DATA_FILE'));print(d.get('goodExpressions',{}).get('totalCount',0))")
        
        # 构建数据摘要给 AI
        SUMMARY_PROMPT="生成本月英语学习总结，包含：
- 练习天数统计
- 词汇数：$voc
- 错误数：$err  
- 好表达数：$good
- 本月心得和建议

用友好的语气，100字以内。"
        
        # 调用 AI 生成总结
        SUMMARY=$(curl -s "$API_URL" \
          -H "Authorization: Bearer $API_KEY" \
          -H "Content-Type: application/json" \
          -d "{\"model\": \"$MODEL\", \"messages\": [{\"role\": \"user\", \"content\": \"$SUMMARY_PROMPT\"}], \"max_tokens\": 300}" \
          | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('choices',[{}])[0].get('message',{}).get('content',''))")
        
        MESSAGE="📊 **本月英语学习总结** 🗓️

📚 词汇: $voc 个
❌ 错误: $err 次
✨ 好表达: $good 个

$SUMMARY"
        
        # 发送消息
        openclaw agent --channel $PUSH_CHANNEL --to $TARGET_USER_ID --message "$MESSAGE" --deliver
        
        echo "月度总结已发送"
    else
        echo "数据文件不存在"
    fi
else
    echo "今天不是本月最后一天，不发送"
fi
