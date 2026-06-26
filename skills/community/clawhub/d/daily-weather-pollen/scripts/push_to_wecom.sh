#!/bin/bash
# 北京天气花粉每日推送 - 企业微信群机器人 Webhook 版
# 使用方式: ./push_to_wecom.sh

# 设置 cron 环境变量
export PATH="/root/.nvm/versions/node/v22.22.1/bin:/root/.local/share/pnpm:/root/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="/root"

# 加载配置文件
CONFIG_FILE="$HOME/.openclaw/config/wecom.env"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    echo "错误: 配置文件不存在 $CONFIG_FILE"
    exit 1
fi

# 验证配置
if [ -z "$WECOM_WEBHOOK_KEY" ]; then
    echo "错误: WECOM_WEBHOOK_KEY 未配置"
    exit 1
fi

WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$WECOM_WEBHOOK_KEY"
DATE=$(date +"%-m月%-d日 %H:%M")

# 重试函数：最多重试3次
retry_request() {
    local cmd="$1"
    local max_retries=3
    local retry=0
    local result=""
    
    while [ $retry -lt $max_retries ]; do
        result=$(eval "$cmd" 2>/dev/null)
        if [ $? -eq 0 ] && [ -n "$result" ]; then
            echo "$result"
            return 0
        fi
        retry=$((retry + 1))
        if [ $retry -lt $max_retries ]; then
            sleep 2
        fi
    done
    return 1
}

# 获取天气数据（带重试）
WEATHER=$(retry_request 'curl -s "wttr.in/Beijing?format=3"')
if [ $? -ne 0 ]; then
    WEATHER="天气数据暂不可用"
fi

# 获取花粉数据（带重试）
POLLEN_SUCCESS=1
POLLEN_DATA=""
for i in 1 2 3; do
    # 打开页面并等待加载
    agent-browser open "https://richerculture.cn/hf/" 2>/dev/null
    sleep 3  # 等待页面完全加载
    
    # 获取页面内容
    PAGE_CONTENT=$(agent-browser snapshot -c 2>/dev/null)
    
    # 解析花粉数据：提取日期、浓度、等级
    POLLEN_DATA=$(echo "$PAGE_CONTENT" | grep -E 'cell "(202[0-9]-[0-9]{2}-[0-9]{2}|[0-9]+|很高|高|中|低|很低)"' | head -3)
    
    agent-browser close 2>/dev/null
    
    if [ -n "$POLLEN_DATA" ]; then
        POLLEN_SUCCESS=0
        break
    fi
    
    if [ $i -lt 3 ]; then
        sleep 2
    fi
done

# 检查花粉数据获取是否成功（天气失败只显示友好提示，不影响推送）
if [ $POLLEN_SUCCESS -ne 0 ]; then
    # 构建错误消息
    ERROR_MSG="## ⚠️ 花粉数据获取失败

**发布时间：** $DATE

---

### ❌ 无法获取花粉浓度数据

花粉浓度数据暂时无法获取（已重试3次），请稍后重试或手动查询：
• 访问 richerculture.cn/hf
• 微信搜索"花粉健康宝"小程序

---
🐉 小龙提醒"

    # 发送错误消息
    curl -s -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"msgtype\": \"markdown\",
            \"markdown\": {
                \"content\": $(echo -e "$ERROR_MSG" | jq -Rs .)
            }
        }"
    
    echo ""
    echo "花粉数据获取失败，已发送错误通知: $DATE"
    exit 1
fi

# 解析花粉浓度
# 从前3行中提取：日期、浓度、等级
TODAY=$(echo "$POLLEN_DATA" | head -1 | grep -oP '\d{4}-\d{2}-\d{2}' || date +"%Y-%m-%d")
CONCENTRATION=$(echo "$POLLEN_DATA" | sed -n '2p' | grep -oP '(?<=cell ")[0-9]+(?=")' || echo "")
LEVEL=$(echo "$POLLEN_DATA" | sed -n '3p' | grep -oP '(?<=cell ")[很高低中]+(?=")' || echo "")

# 验证数据有效性
if [ -z "$CONCENTRATION" ] || [ -z "$LEVEL" ]; then
    echo "解析花粉数据失败，原始数据："
    echo "$POLLEN_DATA"
    exit 1
fi

# 计算超标倍数
EXCEED=$((CONCENTRATION / 70))

# 风险等级
if [ "$CONCENTRATION" -gt 520 ]; then
    RISK="5级（很高）"
    RISK_ACTION="强烈建议：避免户外活动"
elif [ "$CONCENTRATION" -gt 290 ]; then
    RISK="4级（高）"
    RISK_ACTION="建议：减少户外活动"
elif [ "$CONCENTRATION" -gt 150 ]; then
    RISK="3级（中）"
    RISK_ACTION="注意：敏感人群减少外出"
elif [ "$CONCENTRATION" -gt 70 ]; then
    RISK="2级（低）"
    RISK_ACTION="可正常户外活动"
else
    RISK="1级（很低）"
    RISK_ACTION="适宜户外活动"
fi

# 构建消息
MESSAGE="## 📍 北京 | 花粉过敏指数权威发布

**权威来源：** 中国天气网 × 首都医科大学附属北京同仁医院
**发布时间：** $DATE

---

### 🚨 今日过敏风险等级：$RISK
> **$RISK_ACTION**

• **浓度：** $CONCENTRATION 粒/千平方毫米（安全值70，<font color=\"warning\">超标${EXCEED}倍</font>）
• **主要来源：** 柏树、榆树、杨树

### 📊 天气提示
$WEATHER

### 🛡️ 防护建议
✅ 关闭门窗，开启空气净化器
✅ 外出佩戴N95口罩
✅ 外出后立即洗脸、漱口、换衣
❌ 禁止开窗通风、晾晒衣物

---
🐉 <font color=\"info\">小龙每日提醒</font> | 数据来源：花粉健康宝小程序"

# 发送到企业微信
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"msgtype\": \"markdown\",
    \"markdown\": {
      \"content\": $(echo "$MESSAGE" | jq -Rs .)
    }
  }"

echo ""
echo "推送完成: $DATE"
