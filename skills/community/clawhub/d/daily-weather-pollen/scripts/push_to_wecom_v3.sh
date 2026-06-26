#!/bin/bash
# 北京天气花粉每日推送 - 企业微信群机器人 Webhook 版 v3
# 修复: 解决 agent-browser 浏览器实例锁定问题
# 使用方式: ./push_to_wecom_v3.sh [城市]

set -o pipefail

# ============ 环境配置 ============
export PATH="/root/.nvm/versions/node/v22.22.1/bin:/root/.local/share/pnpm:/root/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export HOME="/root"

# agent-browser 会话隔离
export AGENT_BROWSER_SESSION="pollen-push-$(date +%Y%m%d)"

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
    # 注意：cron 任务必须独立运行，不能复用旧实例
    local chrome_count=$(ps aux | grep -E 'agent-browser|chrome.*agent-browser' | grep -v grep | wc -l)
    if [ "$chrome_count" -gt 0 ]; then
        log "INFO" "发现 $chrome_count 个旧浏览器进程，强制清理..."
        pkill -9 -f 'agent-browser' 2>/dev/null || true
        sleep 1
        pkill -9 -f 'chrome.*agent-browser' 2>/dev/null || true
        sleep 2
    fi
}

get_pollen_data() {
    local pollen_data=""
    local success=1
    
    # 先清理可能存在的旧会话
    cleanup_browser
    
    for i in 1 2 3; do
        log "INFO" "尝试获取花粉数据 ($i/3)"
        
        # 使用独立 session 打开页面，设置超时
        local open_output
        open_output=$(timeout 30 agent-browser open "https://richerculture.cn/hf/" 2>&1)
        local open_exit=$?
        
        log "DEBUG" "browser open 退出码: $open_exit, 输出: ${open_output:0:100}"
        
        if [ $open_exit -ne 0 ]; then
            log "WARN" "打开页面失败 (exit=$open_exit)"
            # 强制清理后重试
            pkill -f 'chrome.*pollen-push' 2>/dev/null || true
            sleep 2
            continue
        fi
        
        # 等待页面加载
        sleep 3
        
        # 获取页面内容（完整 snapshot）
        local page_content
        page_content=$(timeout 15 agent-browser snapshot -c 2>/dev/null)
        local content_length=${#page_content}
        
        log "INFO" "页面内容长度: $content_length"
        
        # 关闭浏览器
        timeout 5 agent-browser close 2>/dev/null || true
        
        # 直接返回完整页面内容，让解析函数处理
        if [ $content_length -gt 100 ]; then
            echo "$page_content"
            log "INFO" "成功获取页面内容"
            return 0
        fi
        
        log "WARN" "页面内容过短"
        
        if [ $i -lt 3 ]; then
            sleep 3
        fi
    done
    
    return 1
}

parse_pollen_data() {
    local page_content="$1"
    
    # 从北京近7天花粉报告表格提取第一行数据
    # 格式:
    #   - cell "2026-03-31" [ref=e5]
    #   - cell "800" [ref=e6]
    #   - cell "很高" [ref=e7]
    
    # 提取日期（第一个日期格式的 cell）
    TODAY=$(echo "$page_content" | grep -oP 'cell "\d{4}-\d{2}-\d{2}"' | head -1 | grep -oP '\d{4}-\d{2}-\d{2}')
    if [ -z "$TODAY" ]; then
        TODAY=$(date +"%Y-%m-%d")
    fi
    
    # 提取浓度：在日期行之后的数字 cell
    # 北京表格格式是：日期、浓度、等级 三列连续
    # 找到日期那一行附近的 cell 数字
    local date_line_num=$(echo "$page_content" | grep -n "cell \"$TODAY\"" | head -1 | cut -d: -f1)
    if [ -n "$date_line_num" ]; then
        # 从日期行开始往后找浓度
        CONCENTRATION=$(echo "$page_content" | tail -n +$((date_line_num + 1)) | grep -oP 'cell "[0-9>]+"' | head -1 | grep -oP '[0-9]+')
        LEVEL=$(echo "$page_content" | tail -n +$((date_line_num + 2)) | grep -oP 'cell "(很高|高|中|低|很低)"' | head -1 | grep -oP '(很高|高|中|低|很低)')
    fi
    
    # 如果上面方法失败，用备用方法：找所有 cell 数字（排除日期）
    if [ -z "$CONCENTRATION" ]; then
        # 排除日期格式，找第一个纯数字 cell
        CONCENTRATION=$(echo "$page_content" | grep -oP 'cell "[0-9>]+"' | grep -v '\d{4}-\d{2}' | head -1 | grep -oP '[0-9]+')
    fi
    
    if [ -z "$LEVEL" ]; then
        LEVEL=$(echo "$page_content" | grep -oP 'cell "(很高|高|中|低|很低)"' | head -1 | grep -oP '(很高|高|中|低|很低)')
    fi
    
    if [ -z "$CONCENTRATION" ] || [ -z "$LEVEL" ]; then
        log "ERROR" "数据解析失败: TODAY=$TODAY, CONCENTRATION=$CONCENTRATION, LEVEL=$LEVEL"
        log "DEBUG" "页面片段: $(echo "$page_content" | grep -A2 -B2 'cell "2026' | head -10)"
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
log "INFO" "========== 开始执行推送任务 v3 =========="
log "INFO" "城市: $POLLEN_CITY"
log "INFO" "会话: $AGENT_BROWSER_SESSION"

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
