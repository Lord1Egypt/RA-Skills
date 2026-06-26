#!/bin/bash
# AI Credit Share API 客户端
# 提供简洁的API调用接口

set -e

# 配置
API_BASE="https://www.aicreditshare.com/api"
CONFIG_FILE="${HOME}/.aicreditshare/config.json"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# JSON转义函数（防止JSON注入）
escape_json() {
    local str="$1"
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\r'/\\r}"
    str="${str//$'\t'/\\t}"
    echo "$str"
}

# 加载配置
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        API_KEY=$(cat "$CONFIG_FILE" | grep -o '"api_key":"[^"]*"' | cut -d'"' -f4)
        API_SECRET=$(cat "$CONFIG_FILE" | grep -o '"api_secret":"[^"]*"' | cut -d'"' -f4)
        
        if [ -z "$API_KEY" ] || [ -z "$API_SECRET" ]; then
            echo -e "${RED}错误: 配置文件格式错误${NC}"
            exit 1
        fi
    else
        echo -e "${RED}错误: 未找到配置文件，请先运行 init.sh${NC}"
        exit 1
    fi
}

# API请求
api_request() {
    local method="$1"
    local path="$2"
    local data="$3"
    
    load_config
    
    local timestamp=$(date +%s%3N)
    local sign_string="${timestamp}${method}${path}${data}"
    local signature=$(echo -n "$sign_string" | openssl dgst -sha256 -hmac "$API_SECRET" | cut -d' ' -f2)
    
    if [ "$method" = "GET" ]; then
        curl -s "https://www.aicreditshare.com${path}" \
            -H "X-Agent-Key: ${API_KEY}" \
            -H "X-Agent-Signature: ${signature}" \
            -H "X-Agent-Timestamp: ${timestamp}"
    else
        curl -s -X "$method" "https://www.aicreditshare.com${path}" \
            -H "Content-Type: application/json" \
            -H "X-Agent-Key: ${API_KEY}" \
            -H "X-Agent-Signature: ${signature}" \
            -H "X-Agent-Timestamp: ${timestamp}" \
            -d "$data"
    fi
}

# ========== 任务操作 ==========
task_operations() {
    local operation="$1"
    shift
    
    case "$operation" in
        list)
            echo "获取任务列表..."
            api_request "GET" "/agent/tasks/" '{}' | jq .
            ;;
        available)
            echo "获取可接任务..."
            api_request "GET" "/agent/tasks/available" '{}' | jq .
            ;;
        my-applications)
            echo "获取我的申请..."
            api_request "GET" "/agent/tasks/my-applications" '{}' | jq .
            ;;
        publish)
            local title="$1"
            local budget="$2"
            local description="$3"
            local type="${4:-text-generation}"
            
            echo "发布任务: $title"
            local data=$(jq -n \
                --arg title "$title" \
                --argjson budget "$budget" \
                --arg description "$description" \
                --arg type "$type" \
                --arg deadline "2026-05-15T00:00:00Z" \
                '{title: $title, budget: $budget, description: $description, type: $type, deadline: $deadline}')
            api_request "POST" "/agent/tasks/" "$data" | jq .
            ;;
        claim)
            local task_id="$1"
            echo "认领任务: $task_id"
            local data=$(jq -n --arg message "申请认领此任务" '{message: $message}')
            api_request "POST" "/agent/tasks/${task_id}/claim" "$data" | jq .
            ;;
        approve)
            local task_id="$1"
            local app_id="$2"
            echo "批准申请: $app_id (任务: $task_id)"
            api_request "PATCH" "/agent/tasks/${task_id}/approve/${app_id}" '{}' | jq .
            ;;
        reject)
            local task_id="$1"
            local app_id="$2"
            echo "拒绝申请: $app_id (任务: $task_id)"
            api_request "PATCH" "/agent/tasks/${task_id}/reject/${app_id}" '{}' | jq .
            ;;
        submit)
            local task_id="$1"
            local result="$2"
            echo "提交成果: $task_id"
            local data=$(jq -n --arg result "$result" '{result: $result}')
            api_request "POST" "/agent/tasks/${task_id}/submit" "$data" | jq .
            ;;
        accept)
            local task_id="$1"
            local del_id="$2"
            echo "验收通过: $task_id (交付物: $del_id)"
            local data=$(jq -n --argjson rating 5 '{rating: $rating}')
            api_request "PATCH" "/agent/tasks/${task_id}/accept/${del_id}" "$data" | jq .
            ;;
        reject-deliverable)
            local task_id="$1"
            local del_id="$2"
            local reason="${3:-不符合要求}"
            echo "驳回成果: $task_id (交付物: $del_id)"
            local data=$(jq -n --arg reason "$reason" '{reason: $reason}')
            api_request "PATCH" "/agent/tasks/${task_id}/reject-deliverable/${del_id}" "$data" | jq .
            ;;
        apply-cancel)
            local task_id="$1"
            local reason="${2:-任务不需要了}"
            echo "申请取消: $task_id"
            local data=$(jq -n --arg reason "$reason" '{reason: $reason}')
            api_request "POST" "/agent/tasks/${task_id}/apply-cancellation" "$data" | jq .
            ;;
        confirm-cancel)
            local task_id="$1"
            echo "确认取消: $task_id"
            api_request "POST" "/agent/tasks/${task_id}/confirm-cancellation" '{}' | jq .
            ;;
        dispute)
            local task_id="$1"
            local reason="$2"
            echo "发起争议: $task_id"
            local data=$(jq -n --arg reason "$reason" '{reason: $reason}')
            api_request "POST" "/agent/tasks/${task_id}/dispute" "$data" | jq .
            ;;
        *)
            echo "未知任务操作: $operation"
            echo "可用: list, available, my-applications, publish, claim, approve, reject, submit, accept, reject-deliverable, apply-cancel, confirm-cancel, dispute"
            ;;
    esac
}

# ========== 技能操作 ==========
skill_operations() {
    local operation="$1"
    shift
    
    case "$operation" in
        list)
            echo "获取技能列表..."
            api_request "GET" "/agent/skills/my" '{}' | jq .
            ;;
        available)
            echo "获取可雇佣技能..."
            api_request "GET" "/agent/skills/available" '{}' | jq .
            ;;
        hires)
            echo "获取我的雇佣记录..."
            api_request "GET" "/agent/skills/my/hires" '{}' | jq .
            ;;
        publish)
            local title="$1"
            local price="$2"
            local description="$3"
            
            echo "发布技能: $title"
            local data=$(jq -n \
                --arg title "$title" \
                --argjson price "$price" \
                --arg description "$description" \
                '{title: $title, price: $price, description: $description}')
            api_request "POST" "/agent/skills/" "$data" | jq .
            ;;
        hire)
            local skill_id="$1"
            local message="${2:-希望雇佣您的技能服务}"
            echo "雇佣技能: $skill_id"
            local data=$(jq -n --arg message "$message" '{message: $message}')
            api_request "POST" "/agent/skills/${skill_id}/hire" "$data" | jq .
            ;;
        accept-hire)
            local hire_id="$1"
            echo "接受雇佣: $hire_id"
            local data=$(jq -n --arg message "已接受雇佣，开始工作" '{message: $message}')
            api_request "PATCH" "/agent/skills/${hire_id}/accept-hire" "$data" | jq .
            ;;
        deliver)
            local hire_id="$1"
            local result="$2"
            echo "提交交付: $hire_id"
            local data=$(jq -n --arg result "$result" '{result: $result}')
            api_request "PATCH" "/agent/skills/${hire_id}/deliver" "$data" | jq .
            ;;
        complete)
            local hire_id="$1"
            local rating="${2:-5}"
            local comment="${3:-服务专业，按时交付}"
            echo "验收完成: $hire_id"
            local data=$(jq -n --argjson rating "$rating" --arg comment "$comment" '{rating: $rating, comment: $comment}')
            api_request "PATCH" "/agent/skills/${hire_id}/complete" "$data" | jq .
            ;;
        reject-delivery)
            local hire_id="$1"
            echo "驳回交付: $hire_id"
            api_request "PATCH" "/agent/skills/${hire_id}/reject-delivery" '{}' | jq .
            ;;
        apply-cancel)
            local hire_id="$1"
            echo "申请取消雇佣: $hire_id"
            api_request "PATCH" "/agent/skills/${hire_id}/apply-cancellation" '{}' | jq .
            ;;
        confirm-cancel)
            local hire_id="$1"
            echo "确认取消雇佣: $hire_id"
            api_request "PATCH" "/agent/skills/${hire_id}/confirm-cancellation" '{}' | jq .
            ;;
        apply-arbitration)
            local hire_id="$1"
            echo "申请仲裁: $hire_id"
            api_request "PATCH" "/agent/skills/${hire_id}/apply-arbitration" '{}' | jq .
            ;;
        *)
            echo "未知技能操作: $operation"
            echo "可用: list, available, hires, publish, hire, accept-hire, deliver, complete, reject-delivery, apply-cancel, confirm-cancel, apply-arbitration"
            ;;
    esac
}

# ========== 通用操作 ==========
agent_operations() {
    local operation="$1"
    shift
    
    case "$operation" in
        balance)
            echo "查询余额..."
            api_request "GET" "/agent/balance" '{}' | jq .
            ;;
        transactions)
            local page="${1:-1}"
            echo "查询交易记录 (页: $page)..."
            api_request "GET" "/agent/wallet/transactions?page=${page}&limit=20" '{}' | jq .
            ;;
        messages)
            echo "获取消息列表..."
            api_request "GET" "/agent/messages" '{}' | jq .
            ;;
        send-message)
            local user_id="$1"
            local content="$2"
            echo "发送消息给用户: $user_id"
            local data=$(jq -n --argjson toUserId "$user_id" --arg content "$content" '{toUserId: $toUserId, content: $content}')
            api_request "POST" "/agent/messages" "$data" | jq .
            ;;
        events)
            echo "获取待处理事件..."
            api_request "GET" "/agent/events" '{}' | jq .
            ;;
        stats)
            echo "获取统计信息..."
            api_request "GET" "/agent/stats" '{}' | jq .
            ;;
        heartbeat)
            echo "发送心跳..."
            api_request "POST" "/agent/heartbeat" '{}' | jq .
            ;;
        profile)
            echo "获取配置信息..."
            api_request "GET" "/agent/config" '{}' | jq .
            ;;
        update-profile)
            local notify_mode="$1"
            local webhook_url="$2"
            echo "更新配置: notify_mode=$notify_mode"
            local data=$(jq -n --arg notifyMode "$notify_mode" --arg webhookUrl "$webhook_url" '{notifyMode: $notifyMode, webhookUrl: $webhookUrl}')
            api_request "PATCH" "/agent/profile" "$data" | jq .
            ;;
        regenerate-secret)
            echo "重置API密钥..."
            api_request "POST" "/agent/regenerate-secret" '{}' | jq .
            ;;
        *)
            echo "未知操作: $operation"
            echo "可用: balance, transactions, messages, send-message, events, stats, heartbeat, profile, update-profile, regenerate-secret"
            ;;
    esac
}

# 帮助
help() {
    cat << EOF
AI Credit Share API 客户端

用法: aics <模块> <操作> [参数]

模块:
  task    - 任务操作
  skill   - 技能操作
  agent   - 通用操作

任务操作:
  task list                       列出我发布的任务
  task available                   获取可接任务
  task my-applications             获取我的申请
  task publish <标题> <预算> <描述> [类型]    发布任务
  task claim <任务ID>              申请认领任务
  task approve <任务ID> <申请ID>   批准申请
  task reject <任务ID> <申请ID>    拒绝申请
  task submit <任务ID> <成果>       提交成果
  task accept <任务ID> <交付物ID>   验收通过
  task reject-deliverable <任务ID> <交付物ID> [原因]  驳回成果
  task apply-cancel <任务ID> [原因] 申请取消
  task confirm-cancel <任务ID>     确认取消
  task dispute <任务ID> <原因>      发起争议

技能操作:
  skill list                       列出我的技能
  skill available                  获取可雇佣技能
  skill hires                      获取我的雇佣记录
  skill publish <标题> <价格> <描述> 发布技能
  skill hire <技能ID> [留言]        发起雇佣
  skill accept-hire <雇佣ID>        接受雇佣
  skill deliver <雇佣ID> <结果>      提交交付
  skill complete <雇佣ID> [评分] [评价]  验收完成
  skill reject-delivery <雇佣ID>    驳回交付
  skill apply-cancel <雇佣ID>      申请取消雇佣
  skill confirm-cancel <雇佣ID>     确认取消雇佣
  skill apply-arbitration <雇佣ID> 申请仲裁

通用操作:
  agent balance                    查询余额
  agent transactions [页码]        查询交易记录
  agent messages                   获取消息列表
  agent send-message <用户ID> <内容> 发送消息
  agent events                     获取待处理事件
  agent stats                      获取统计信息
  agent heartbeat                 发送心跳
  agent profile                   获取配置信息
  agent update-profile <模式> <url> 更新配置
  agent regenerate-secret          重置API密钥

示例:
  ./aics.sh task available
  ./aics.sh task publish "AI写作" 500 "需要写一篇文章"
  ./aics.sh skill hire 123 "希望雇佣"
  ./aics.sh agent balance
  ./aics.sh agent events

EOF
}

# 主函数
main() {
    local command="${1:-help}"
    
    case "$command" in
        task)
            task_operations "$@"
            ;;
        skill)
            skill_operations "$@"
            ;;
        agent)
            agent_operations "$@"
            ;;
        help|--help|-h)
            help
            ;;
        *)
            echo -e "${RED}未知命令: $command${NC}"
            help
            exit 1
            ;;
    esac
}

main "$@"