#!/bin/bash
# flirt_cron.sh - 情话定时发送脚本
# 调用方式: crontab -e 添加: 0 8-22 * * * /root/.openclaw/workspace/flirt_cron.sh
# 每小时(8-22点)触发一次，40%概率发送

# 配置
PROBABILITY=40  # 触发概率40%
WORKSPACE="/root/.openclaw/workspace"
FLIRT_LIB="$WORKSPACE/flirt_library.txt"
FLIRT_STATE="$WORKSPACE/flirt_state.json"

# 飞书配置 - 请替换为你的值
FEISHU_APP_ID="cli_你的APP_ID"
FEISHU_APP_SECRET="你的APP_SECRET"
FEISHU_USER_ID="你的用户ID"

# QQ配置 - 请替换为你的值
QQ_OPENID="你的QQ_OPENID"

# 上次对话时间记录（分开记录）
LAST_CHAT_FILE_FEISHU="$WORKSPACE/memory/last_chat_feishu.txt"
LAST_CHAT_FILE_QQ="$WORKSPACE/memory/last_chat_qq.txt"

# 语音参数 - 使用Noiz tts skill + 声音克隆（参考音频需<30秒）
VOICE_SCRIPT="$WORKSPACE/.agents/skills/tts/scripts/tts.py"
REF_VOICE="$WORKSPACE/ref_voice_latest.mp3"

# 生成飞书语音 (使用Noiz声音克隆)
VOICE_FILE_FEISHU="/tmp/flirt_voice_feishu_$(date +%s).wav"
python3 $VOICE_SCRIPT -t "$MESSAGE_FEISHU" --ref-audio "$REF_VOICE" -o "$VOICE_FILE_FEISHU" 2>/dev/null
# 转换为真正的Opus格式
VOICE_FILE_FEISHU_OGG="${VOICE_FILE_FEISHU%.wav}.ogg"
ffmpeg -y -i "$VOICE_FILE_FEISHU" -c:a libopus -b:a 64k "$VOICE_FILE_FEISHU_OGG" 2>/dev/null
VOICE_FILE_FEISHU="$VOICE_FILE_FEISHU_OGG"

# 生成QQ语音 (使用Noiz声音克隆)
VOICE_FILE_QQ="/tmp/flirt_voice_qq_$(date +%s).wav"
python3 $VOICE_SCRIPT -t "$MESSAGE_QQ" --ref-audio "$REF_VOICE" -o "$VOICE_FILE_QQ" 2>/dev/null
# 转换为真正的Opus格式
VOICE_FILE_QQ_OGG="${VOICE_FILE_QQ%.wav}.ogg"
ffmpeg -y -i "$VOICE_FILE_QQ" -c:a libopus -b:a 64k "$VOICE_FILE_QQ_OGG" 2>/dev/null
VOICE_FILE_QQ="$VOICE_FILE_QQ_OGG"

# OpenClaw路径
OPENCLAW="/root/.nvm/versions/node/v22.22.1/bin/openclaw"

# 获取飞书token
get_feishu_token() {
    curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" | \
        python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))"
}

# 计算时间差函数
calc_time_diff() {
    local last_file="$1"
    local default_time="2026-03-15 01:35:00"
    
    if [ -f "$last_file" ]; then
        LAST_CHAT=$(cat "$last_file")
    else
        LAST_CHAT="$default_time"
        echo "$default_time" > "$last_file"
    fi
    
    python3 -c "
from datetime import datetime
last = datetime.strptime('$LAST_CHAT', '%Y-%m-%d %H:%M:%S')
now = datetime.now()
diff = now - last
hours = diff.total_seconds() / 3600
if hours < 1:
    mins = int(diff.total_seconds() / 60)
    print(f'{mins}分钟')
elif hours < 24:
    print(f'{int(hours)}小时')
else:
    days = int(hours / 24)
    print(f'{days}天{int(hours%24)}小时')
" 2>/dev/null || echo "一会儿"
}

# 更新时间记录函数
update_last_chat() {
    local last_file="$1"
    date '+%Y-%m-%d %H:%M:%S' > "$last_file"
}

# 随机触发判断
RANDOM_NUM=$((RANDOM % 100 + 1))
if [ $RANDOM_NUM -gt $PROBABILITY ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - 随机数 $RANDOM_NUM > $PROBABILITY，跳过"
    exit 0
fi

# 读取情话库
if [ ! -f "$FLIRT_LIB" ]; then
    echo "Error: 情话库不存在"
    exit 1
fi

# 读取所有情话（去掉注释和空行）
FLAIRS=$(grep -v "^#" "$FLIRT_LIB" | grep -v "^$" | grep -v "^{" | tail -n +2)
FLAIR_LIST=()
while IFS= read -r line; do
    if [[ "$line" =~ ^\" ]]; then
        FLAIR_LIST+=("$line")
    fi
done <<< "$FLAIRS"

if [ ${#FLAIR_LIST[@]} -eq 0 ]; then
    echo "Error: 情话库为空"
    exit 1
fi

# 读取已发送记录
if [ -f "$FLIRT_STATE" ]; then
    SENT_COUNT=$(python3 -c "import json; d=json.load(open('$FLIRT_STATE')); print(len(d.get('sent_flirts', [])))" 2>/dev/null || echo "0")
else
    SENT_COUNT=0
fi

# 如果发送数量 >= 情话数量，重置
TOTAL_FLAIRS=${#FLAIR_LIST[@]}
if [ "$SENT_COUNT" -ge "$TOTAL_FLAIRS" ]; then
    echo "$(date) - 情话已发完一轮，重置"
    python3 -c "
import json
with open('$FLIRT_STATE', 'w') as f:
    json.dump({'last_flirt_date': '$(date +%Y-%m-%d)', 'sent_flirts': [], 'last_chat': ''}, f)
" 2>/dev/null
    SENT_COUNT=0
fi

# 随机选择一条未发送的
AVAILABLE_INDEXES=()
for i in "${!FLAIR_LIST[@]}"; do
    if [ $i -ge $SENT_COUNT ]; then
        AVAILABLE_INDEXES+=($i)
    fi
done

if [ ${#AVAILABLE_INDEXES[@]} -eq 0 ]; then
    python3 -c "
import json
with open('$FLIRT_STATE', 'w') as f:
    json.dump({'last_flirt_date': '$(date +%Y-%m-%d)', 'sent_flirts': [], 'last_chat': ''}, f)
" 2>/dev/null
    exit 0
fi

RAND_IDX=$((RANDOM % ${#AVAILABLE_INDEXES[@]}))
SELECTED_IDX=${AVAILABLE_INDEXES[$RAND_IDX]}
SELECTED_FLAIR="${FLAIR_LIST[$SELECTED_IDX]}"

# 计算飞书时间差并生成消息
TIME_DIFF_FEISHU=$(calc_time_diff "$LAST_CHAT_FILE_FEISHU")
MESSAGE_FEISHU=$(echo "$SELECTED_FLAIR" | sed "s/{time_diff}/$TIME_DIFF_FEISHU/g" | tr -d '"')

# 计算QQ时间差并生成消息
TIME_DIFF_QQ=$(calc_time_diff "$LAST_CHAT_FILE_QQ")
MESSAGE_QQ=$(echo "$SELECTED_FLAIR" | sed "s/{time_diff}/$TIME_DIFF_QQ/g" | tr -d '"')

echo "$(date '+%Y-%m-%d %H:%M:%S') - 飞书情话: $MESSAGE_FEISHU (间隔: $TIME_DIFF_FEISHU)"
echo "$(date '+%Y-%m-%d %H:%M:%S') - QQ情话: $MESSAGE_QQ (间隔: $TIME_DIFF_QQ)"

# 生成飞书语音 (使用Noiz克隆)
VOICE_FILE_FEISHU="/tmp/flirt_voice_feishu_$(date +%s).wav"
python3 $VOICE_SCRIPT -t "$MESSAGE_FEISHU" --ref-audio "$REF_VOICE" -o "$VOICE_FILE_FEISHU" 2>/dev/null
# 转换为真正的Opus格式
VOICE_FILE_FEISHU_OGG="${VOICE_FILE_FEISHU%.wav}.ogg"
ffmpeg -y -i "$VOICE_FILE_FEISHU" -c:a libopus -b:a 64k "$VOICE_FILE_FEISHU_OGG" 2>/dev/null
VOICE_FILE_FEISHU="$VOICE_FILE_FEISHU_OGG"

# 生成QQ语音 (使用Noiz克隆)
VOICE_FILE_QQ="/tmp/flirt_voice_qq_$(date +%s).wav"
python3 $VOICE_SCRIPT -t "$MESSAGE_QQ" --ref-audio "$REF_VOICE" -o "$VOICE_FILE_QQ" 2>/dev/null
# 转换为真正的Opus格式
VOICE_FILE_QQ_OGG="${VOICE_FILE_QQ%.wav}.ogg"
ffmpeg -y -i "$VOICE_FILE_QQ" -c:a libopus -b:a 64k "$VOICE_FILE_QQ_OGG" 2>/dev/null
VOICE_FILE_QQ="$VOICE_FILE_QQ_OGG"

# 发送飞书
if [ -f "$VOICE_FILE_FEISHU" ]; then
    # 获取飞书token并发送语音
    FEISHU_TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" | \
        python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")
    
    if [ -n "$FEISHU_TOKEN" ]; then
        # 获取音频时长
        DURATION_MS=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOICE_FILE_FEISHU" | python3 -c "print(int(float(input()) * 1000))")
        
        # 上传文件
        UPLOAD_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
            -H "Authorization: Bearer $FEISHU_TOKEN" \
            -F "file_type=opus" \
            -F "file_name=voice.ogg" \
            -F "duration=$DURATION_MS" \
            -F "file=@$VOICE_FILE_FEISHU")
        
        FILE_KEY=$(echo "$UPLOAD_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('file_key',''))")
        
        if [ -n "$FILE_KEY" ]; then
            # 发送语音消息
            curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
                -H "Authorization: Bearer $FEISHU_TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"receive_id\":\"$FEISHU_USER_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}" 2>/dev/null
            echo "飞书语音发送完成"
        fi
    fi
    rm -f "$VOICE_FILE_FEISHU"
fi
# 飞书文字
/root/.nvm/versions/node/v22.22.1/bin/openclaw message send --channel feishu --target "user:$FEISHU_USER_ID" --message "$MESSAGE_FEISHU" 2>/dev/null
update_last_chat "$LAST_CHAT_FILE_FEISHU"

# 发送QQ
if [ -f "$VOICE_FILE_QQ" ]; then
    $OPENCLAW message send --channel qqbot --target "qqbot:c2c:$QQ_OPENID" --message "<qqvoice>$VOICE_FILE_QQ</qqvoice>" 2>/dev/null
    echo "QQ语音发送完成"
    rm -f "$VOICE_FILE_QQ"
fi
# QQ文字
$OPENCLAW message send --channel qqbot --target "qqbot:c2c:$QQ_OPENID" --message "$MESSAGE_QQ" 2>/dev/null
update_last_chat "$LAST_CHAT_FILE_QQ"

# 更新状态
python3 -c "
import json
with open('$FLIRT_STATE', 'r+') as f:
    d = json.load(f)
    d['sent_flirts'].append('$SELECTED_FLAIR')
    d['last_flirt_date'] = '$(date +%Y-%m-%d)'
    f.seek(0)
    json.dump(d, f, ensure_ascii=False)
    f.truncate()
" 2>/dev/null

echo "$(date) - 完成"
