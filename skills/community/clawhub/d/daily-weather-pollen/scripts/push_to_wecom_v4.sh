#!/bin/bash
# 北京天气花粉每日推送 - 企业微信群机器人 Webhook 版 v4
# 改进: 结果导向，完整重试机制，确保成功
# 使用方式: ./push_to_wecom_v4.sh [城市]

set -o pipefail

# ============ 环境配置 ============
export PATH="/root/.nvm/versions/node/v22.22.1/bin:/root/.local/share/pnpm:/root/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="/root"

# agent-browser 会话隔离
export AGENT_BROWSER_SESSION="pollen-push-$(date +%Y%m%d%H%M%S)"

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

# 全局变量
TODAY=""
CONCENTRATION=""
LEVEL=""
RISK=""
RISK_ACTION=""

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

# 清理旧的浏览器进程（彻底清理，防止僵尸进程阻塞）
cleanup_browser() {
    log "INFO" "清理浏览器会话..."
    
    # 尝试正常关闭
    timeout 5 agent-browser close 2>/dev/null || true
    
    # 统计僵尸进程
    local zombie_count=$(ps aux | grep 'chrome.*<defunct>' | grep -v grep | wc -l)
    if [ "$zombie_count" -gt 0 ]; then
        log "WARN" "发现 $zombie_count 个僵尸 chrome 进程，将彻底清理"
    fi
    
    # 彻底清理所有 agent-browser 相关进程
    local chrome_count=$(ps aux | grep -E 'agent-browser|chrome.*agent-browser' | grep -v grep | wc -l)
    if [ "$chrome_count" -gt 0 ]; then
        log "INFO" "发现 $chrome_count 个旧浏览器进程，强制清理..."
        pkill -9 -f 'agent-browser' 2>/dev/null || true
        sleep 1
        pkill -9 -f 'chrome' 2>/dev/null || true
        sleep 2
    fi
}

# 单次获取花粉数据（不带重试）
fetch_pollen_once() {
    local page_content=""
    
    # 清理旧会话
    cleanup_browser
    
    # 使用独立 session 打开页面
    local open_output
    open_output=$(timeout 45 agent-browser open "https://richerculture.cn/hf/" 2>&1)
    local open_exit=$?
    
    if [ $open_exit -ne 0 ]; then
        log "WARN" "打开页面失败 (exit=$open_exit)"
        return 1
    fi
    
    # 等待页面加载
    sleep 4
    
    # 获取页面内容
    page_content=$(timeout 20 agent-browser snapshot -c 2>/dev/null)
    local content_length=${#page_content}
    
    # 关闭浏览器
    timeout 5 agent-browser close 2>/dev/null || true
    
    if [ $content_length -lt 100 ]; then
        log "WARN" "页面内容过短: $content_length"
        return 1
    fi
    
    echo "$page_content"
    return 0
}

# 解析花粉数据
parse_pollen_data() {
    local page_content="$1"
    
    # 重置全局变量
    TODAY=""
    CONCENTRATION=""
    LEVEL=""
    
    # 提取日期（第一个日期格式的 cell）
    TODAY=$(echo "$page_content" | grep -oP 'cell "\d{4}-\d{2}-\d{2}"' | head -1 | grep -oP '\d{4}-\d{2}-\d{2}')
    if [ -z "$TODAY" ]; then
        TODAY=$(date +"%Y-%m-%d")
    fi
    
    # 提取浓度：在日期行之后的数字 cell
    local date_line_num=$(echo "$page_content" | grep -n "cell \"$TODAY\"" | head -1 | cut -d: -f1)
    if [ -n "$date_line_num" ]; then
        CONCENTRATION=$(echo "$page_content" | tail -n +$((date_line_num + 1)) | grep -oP 'cell "[0-9>]+"' | head -1 | grep -oP '[0-9]+')
        LEVEL=$(echo "$page_content" | tail -n +$((date_line_num + 2)) | grep -oP 'cell "(很高|高|中|低|很低)"' | head -1 | grep -oP '(很高|高|中|低|很低)')
    fi
    
    # 备用方法
    if [ -z "$CONCENTRATION" ]; then
        CONCENTRATION=$(echo "$page_content" | grep -oP 'cell "[0-9>]+"' | grep -v '\d{4}-\d{2}' | head -1 | grep -oP '[0-9]+')
    fi
    
    if [ -z "$LEVEL" ]; then
        LEVEL=$(echo "$page_content" | grep -oP 'cell "(很高|高|中|低|很低)"' | head -1 | grep -oP '(很高|高|中|低|很低)')
    fi
    
    # 验证结果有效性
    if [ -z "$CONCENTRATION" ] || [ -z "$LEVEL" ]; then
        log "ERROR" "数据解析失败: TODAY=$TODAY, CONCENTRATION=$CONCENTRATION, LEVEL=$LEVEL"
        return 1
    fi
    
    # 验证浓度是有效数字
    if ! [[ "$CONCENTRATION" =~ ^[0-9]+$ ]]; then
        log "ERROR" "浓度不是有效数字: $CONCENTRATION"
        return 1
    fi
    
    log "INFO" "数据解析成功: $TODAY | $CONCENTRATION 粒/千平方毫米 | $LEVEL"
    return 0
}

# 获取风险等级
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

# 完整的花粉数据获取流程（带重试）
get_pollen_data_with_retry() {
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        log "INFO" "=== 第 $attempt/$max_attempts 次尝试获取花粉数据 ==="
        
        # 获取页面内容
        local page_content
        page_content=$(fetch_pollen_once)
        
        if [ $? -ne 0 ] || [ -z "$page_content" ]; then
            log "WARN" "第 $attempt 次获取页面失败"
            if [ $attempt -lt $max_attempts ]; then
                log "INFO" "等待 10 秒后重试..."
                sleep 10
            fi
            attempt=$((attempt + 1))
            continue
        fi
        
        log "INFO" "页面获取成功，内容长度: ${#page_content}"
        
        # 解析数据
        if parse_pollen_data "$page_content"; then
            log "INFO" "=== 花粉数据获取成功 ==="
            return 0
        else
            log "WARN" "第 $attempt 次解析失败"
            if [ $attempt -lt $max_attempts ]; then
                log "INFO" "等待 10 秒后重试..."
                sleep 10
            fi
        fi
        
        attempt=$((attempt + 1))
    done
    
    log "ERROR" "=== 所有重试均失败 ==="
    return 1
}

# ============ 主流程 ============

DATE=$(date +"%-m月%-d日 %H:%M")
log "INFO" "========== 开始执行推送任务 v4 =========="
log "INFO" "城市: $POLLEN_CITY"
log "INFO" "会话: $AGENT_BROWSER_SESSION"

# 验证配置
if [ -z "$WECOM_WEBHOOK_KEY" ]; then
    log "ERROR" "WECOM_WEBHOOK_KEY 未配置"
    exit 1
fi

WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=$WECOM_WEBHOOK_KEY"

# 获取天气数据（带重试和多备用源）
get_weather_data() {
    local max_attempts=2
    local attempt=1
    local weather=""
    
    # 方案1: wttr.in format=3
    while [ $attempt -le $max_attempts ]; do
        log "INFO" "获取天气数据 - wttr.in (尝试 $attempt/$max_attempts)..."
        weather=$(curl -s --connect-timeout 8 --max-time 12 "wttr.in/Beijing?format=3" 2>/dev/null)
        
        if [ -n "$weather" ] && [[ ! "$weather" =~ "render failed" ]] && [[ ! "$weather" =~ "error" ]] && [[ ! "$weather" =~ "null" ]]; then
            log "INFO" "天气数据获取成功: $weather"
            echo "$weather"
            return 0
        fi
        log "WARN" "wttr.in 返回无效: $weather"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    # 方案2: Open-Meteo (免费，无需API Key)
    log "INFO" "尝试备用天气源: Open-Meteo..."
    local lat="39.9042"
    local lon="116.4074"
    local weather_json
    weather_json=$(curl -s --connect-timeout 8 --max-time 12 \
        "https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lon&current=temperature_2m,relative_humidity_2m,weather_code&timezone=Asia/Shanghai" 2>/dev/null)
    
    if [ -n "$weather_json" ] && [[ ! "$weather_json" =~ "error" ]]; then
        local temp=$(echo "$weather_json" | jq -r '.current.temperature_2m // empty')
        local humidity=$(echo "$weather_json" | jq -r '.current.relative_humidity_2m // empty')
        local weather_code=$(echo "$weather_json" | jq -r '.current.weather_code // empty')
        
        # 天气代码转文字
        local weather_desc="未知"
        case "$weather_code" in
            0) weather_desc="晴" ;;
            1|2|3) weather_desc="多云" ;;
            45|48) weather_desc="雾" ;;
            51|53|55|56|57) weather_desc="毛毛雨" ;;
            61|63|65) weather_desc="雨" ;;
            71|73|75) weather_desc="雪" ;;
            80|81|82) weather_desc="阵雨" ;;
            95|96|99) weather_desc="雷雨" ;;
        esac
        
        if [ -n "$temp" ]; then
            weather="$weather_desc ${temp}°C 湿度${humidity}%"
            log "INFO" "Open-Meteo 天气数据获取成功: $weather"
            echo "$weather"
            return 0
        fi
    fi
    log "WARN" "Open-Meteo 获取失败"
    
    # 方案3: 简化格式
    log "INFO" "尝试简化天气格式..."
    weather=$(curl -s --connect-timeout 8 --max-time 12 "wttr.in/Beijing?format=%t+%h" 2>/dev/null)
    if [ -n "$weather" ] && [[ ! "$weather" =~ "render failed" ]] && [[ "$weather" =~ [0-9] ]]; then
        log "INFO" "简化天气格式成功: $weather"
        echo "北京 $weather"
        return 0
    fi
    
    log "WARN" "所有天气源均失败"
    echo "天气数据暂不可用"
    return 1
}

log "INFO" "获取天气数据..."
WEATHER=$(get_weather_data)

# 获取花粉数据（带重试）
log "INFO" "获取花粉数据..."
if ! get_pollen_data_with_retry; then
    log "ERROR" "花粉数据获取失败（已重试3次）"
    
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

# 再次验证数据有效性
if [ -z "$CONCENTRATION" ] || [ -z "$LEVEL" ]; then
    log "ERROR" "数据验证失败：浓度或等级为空"
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

# 发送前校验消息内容
log "INFO" "=== 发送前消息内容校验 ==="
log "INFO" "天气数据: $WEATHER"
log "INFO" "花粉浓度: $CONCENTRATION 粒/千平方毫米"
log "INFO" "风险等级: $LEVEL -> $RISK"

# 检查消息中是否包含错误标记
if [[ "$MESSAGE" =~ "render failed" ]] || [[ "$MESSAGE" =~ "error" ]]; then
    log "ERROR" "消息内容包含错误标记，拒绝发送"
    log "ERROR" "问题消息: $MESSAGE"
    exit 1
fi

# 检查天气数据是否有效
if [[ "$WEATHER" =~ "暂不可用" ]]; then
    log "WARN" "天气数据不可用，但继续发送花粉数据"
fi

# 检查关键数据是否存在
if [ -z "$CONCENTRATION" ] || [ -z "$LEVEL" ] || [ -z "$RISK" ]; then
    log "ERROR" "关键数据缺失，拒绝发送"
    exit 1
fi

log "INFO" "消息内容校验通过，准备发送"

# 发送消息
log "INFO" "发送推送消息..."
if send_wecom_message "$MESSAGE"; then
    log "INFO" "推送完成: $DATE | $CONCENTRATION 粒 | $LEVEL"
    echo "{\"errcode\":0,\"errmsg\":\"ok\"}"
    echo "推送完成: $DATE | $CONCENTRATION 粒 | $LEVEL"
else
    log "ERROR" "推送失败"
    exit 1
fi

log "INFO" "========== 推送任务结束 =========="
