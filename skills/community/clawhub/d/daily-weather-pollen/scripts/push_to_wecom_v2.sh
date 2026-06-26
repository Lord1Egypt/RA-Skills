#!/bin/bash
# 北京天气花粉每日推送 - 企业微信群机器人 Webhook 版 v2
# 使用方式: ./push_to_wecom_v2.sh [城市]
# 支持配置化城市，增强错误处理和日志记录

set -o pipefail

# ============ 环境配置 ============
export PATH="/root/.nvm/versions/node/v22.22.1/bin:/root/.local/share/pnpm:/root/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="/root"

# ============ 配置加载 ============
CONFIG_FILE="$HOME/.openclaw/config/wecom.env"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: 配置文件不存在 $CONFIG_FILE"
    exit 1
fi

# 城市配置（支持参数覆盖）
CITY="${1:-北京}"
POLLEN_CITY="${POLLEN_CITY:-$CITY}"

# 日志配置
LOG_FILE="/tmp/pollen-push.log"
ERROR_LOG_FILE="/tmp/pollen-push-error.log"

# ============ 函数定义 ============

log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    if [ "$level" = "ERROR" ]; then
        echo "[$timestamp] [$level] $message" >> "$ERROR_LOG_FILE"
    fi
}

send_wecom_message() {
    local content="$1"
    local msgtype="${2:-markdown}"
    
    local response
    response=$(curl -s -w "\n%{http_code}" -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"msgtype\": \"$msgtype\",
            \"$msgtype\": {
                \"content\": $(echo -e "$content" | jq -Rs .)
            }
        }")
    
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" != "200" ]; then
        log "ERROR" "HTTP请求失败: $http_code"
        return 1
    fi
    
    local errcode=$(echo "$body" | jq -r '.errcode')
    if [ "$errcode" != "0" ]; then
        log "ERROR" "企业微信返回错误: $body"
        return 1
    fi
    
    log "INFO" "消息发送成功"
    return 0
}

retry_request() {
    local cmd="$1"
    local max_retries="${2:-3}"
    local retry=0
    local result=""
    
    while [ $retry -lt $max_retries ]; do
        result=$(eval "$cmd" 2>/dev/null)
        if [ $? -eq 0 ] && [ -n "$result" ]; then
            echo "$result"
            return 0
        fi
        retry=$((retry + 1))
        log "WARN" "请求失败，重试 $retry/$max_retries"
        if [ $retry -lt $max_retries ]; then
            sleep 2
        fi
    done
    return 1
}

get_pollen_data() {
    local pollen_data=""
    local success=1
    
    for i in 1 2 3; do
        log "INFO" "尝试获取花粉数据 ($i/3)"
        
        # 打开页面
        if ! agent-browser open "https://richerculture.cn/hf/" >/dev/null 2>&1; then
            log "WARN" "无法打开页面"
            continue
        fi
        
        sleep 3
        
        # 获取页面内容
        local page_content
        page_content=$(agent-browser snapshot -c 2>/dev/null)
        local content_length=${#page_content}
        
        log "INFO" "页面内容长度: $content_length"
        
        # 关闭浏览器
        agent-browser close >/dev/null 2>&1
        
        # 解析数据
        pollen_data=$(echo "$page_content" | grep -E 'cell "(202[0-9]-[0-9]{2}-[0-9]{2}|[0-9]+|很高|高|中|低|很低)"' | head -3)
        
        if [ -n "$pollen_data" ]; then
            success=0
            log "INFO" "成功获取花粉数据"
            break
        fi
        
        log "WARN" "数据解析失败，原始数据长度: $content_length"
        
        if [ $i -lt 3 ]; then
            sleep 2
        fi
    done
    
    if [ $success -eq 0 ]; then
        echo "$pollen_data"
        return 0
    else
        return 1
    fi
}

parse_pollen_data() {
    local data="$1"
    
    TODAY=$(echo "$data" | head -1 | grep -oP '\d{4}-\d{2}-\d{2}' || date +"%Y-%m-%d")
    CONCENTRATION=$(echo "$data" | sed -n '2p' | grep -oP '(?<=cell ")[0-9]+(?=")' || echo "")
    LEVEL=$(echo "$data" | sed -n '3p' | grep -oP '(?<=cell ")[很高低中]+(?=")' || echo "")
    
    if [ -z "$CONCENTRATION" ] || [ -z "$LEVEL" ]; then
        log "ERROR" "数据解析失败: TODAY=$TODAY, CONCENTRATION=$CONCENTRATION, LEVEL=$LEVEL"
        return 1
    fi
    
    log "INFO" "数据解析成功: $TODAY | $CONCENTRATION 粒/千平方毫米 | $LEVEL"
    return 0
}

get_risk_level() {
    local concentration="$1"
    
    if [ "$concentration" -gt 520 ]; then
        RISK="5级（很高）"
        RISK_ACTION="强烈建议：避免户外活动"
    elif [ "$concentration" -gt 290 ]; then
        RISK="4级（高）"
        RISK_ACTION="建议：减少户外活动"
    elif [ "$concentration" -gt 150 ]; then
        RISK="3级（中）"
        RISK_ACTION="注意：敏感人群减少外出"
    elif [ "$concentration" -gt 70 ]; then
        RISK="2级（低）"
        RISK_ACTION="可正常户外活动"
    else
        RISK="1级（很低）"
        RISK_ACTION="适宜户外活动"
    fi
}

# ============ 主流程 ============

DATE=$(date +"%-m月%-d日 %H:%M")
log "INFO" "========== 开始执行推送任务 =========="
log "INFO" "城市: $POLLEN_CITY"

# 验证配置
if [ -z "$WECOM_WEBHOOK_KEY" ]; then
    log "ERROR" "WECOM_WEBHOOK_KEY 未配置"
    exit 1
fi

WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$WECOM_WEBHOOK_KEY"

# 获取天气数据
log "INFO" "获取天气数据..."
WEATHER=$(retry_request 'curl -s "wttr.in/Beijing?format=3"')
if [ $? -ne 0 ]; then
    WEATHER="天气数据暂不可用"
    log "WARN" "天气数据获取失败"
fi

# 获取花粉数据
log "INFO" "获取花粉数据..."
POLLEN_DATA=$(get_pollen_data)
if [ $? -ne 0 ]; then
    log "ERROR" "花粉数据获取失败"
    
    # 发送错误通知
    ERROR_MSG="## ⚠️ 花粉数据获取失败

**发布时间：** $DATE

---

### ❌ 无法获取花粉浓度数据

花粉浓度数据暂时无法获取（已重试3次），请稍后重试或手动查询：
• 访问 [花粉通](https://richerculture.cn/hf/)
• 微信搜索"花粉健康宝"小程序

---
🐉 小龙提醒"

    send_wecom_message "$ERROR_MSG"
    log "INFO" "已发送错误通知"
    exit 1
fi

# 解析花粉数据
log "INFO" "解析花粉数据..."
if ! parse_pollen_data "$POLLEN_DATA"; then
    log "ERROR" "数据解析失败"
    exit 1
fi

# 计算风险等级
EXCEED=$((CONCENTRATION / 70))
get_risk_level "$CONCENTRATION"

# 构建消息
MESSAGE="## 📍 $POLLEN_CITY | 花粉过敏指数权威发布

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

# 发送消息
log "INFO" "发送推送消息..."
if send_wecom_message "$MESSAGE"; then
    log "INFO" "推送完成: $DATE | $CONCENTRATION 粒 | $LEVEL"
    echo "{\"errcode\":0,\"errmsg\":\"ok\"}"
    echo "推送完成: $DATE"
else
    log "ERROR" "推送失败"
    exit 1
fi

log "INFO" "========== 推送任务结束 =========="
