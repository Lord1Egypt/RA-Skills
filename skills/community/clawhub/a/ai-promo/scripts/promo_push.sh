#!/bin/bash
# Promo API 每日推送
# 用法: promo_push.sh
# Cron: 0 9 * * * ~/.openclaw/skills/promo-api/scripts/promo_push.sh

PROMO_SUB_FILE="$HOME/.promo_subscribers.json"
API_ENDPOINT="https://cli.aipromo.workers.dev"
LOG_FILE="$HOME/.promo_push.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 获取今日精选优惠
get_daily_promos() {
  local user_id="$1"
  curl -s --max-time 30 "${API_ENDPOINT}/list?user_id=${user_id}&limit=5" 2>/dev/null
}

# 格式化推送消息
format_push_message() {
  local json="$1"
  
  echo "【今日优惠速递】"
  echo ""
  
  # 按类型分组
  local referral=$(echo "$json" | jq -r '.items[] | select(.types[] | contains("referral")) | "• 【\(.platform.name)】\(.title): \(.bonus // "无")"' 2>/dev/null | head -3)
  local new_customer=$(echo "$json" | jq -r '.items[] | select(.types[] | contains("new_customer")) | "• 【\(.platform.name)】\(.title): \(.bonus // "无")"' 2>/dev/null | head -3)
  local limited=$(echo "$json" | jq -r '.items[] | select(.types[] | contains("limited_time")) | "• 【\(.platform.name)】\(.title): \(.bonus // "无")"' 2>/dev/null | head -3)
  
  if [[ -n "$referral" ]]; then
    echo "💰 推荐奖励"
    echo "$referral"
    echo ""
  fi
  
  if [[ -n "$new_customer" ]]; then
    echo "🎁 新客优惠"
    echo "$new_customer"
    echo ""
  fi
  
  if [[ -n "$limited" ]]; then
    echo "🔥 限时抢购"
    echo "$limited"
    echo ""
  fi
  
  echo "📋 推荐规则"
  echo "   - 提交的推荐链接有机会展示"
  echo "   - 20% 概率显示"
  echo ""
  echo "🔗 查看详情: https://cli.aipromo.workers.dev/landing"
  echo ""
  echo "---"
  echo "💬 关闭订阅？说'优惠订阅 关闭'"
}

# 推送给单个订阅者
push_to_subscriber() {
  local channel="$1"
  local user_id="$2"
  
  log "推送给 $channel (user_id: $user_id)"
  
  local promos=$(get_daily_promos "$user_id")
  
  if [[ -z "$promos" || "$promos" == "null" ]]; then
    log "获取优惠失败: $channel"
    return 1
  fi
  
  local message=$(format_push_message "$promos")
  
  # 这里需要集成消息发送
  # 示例：使用 message tool 发送
  log "消息内容: $(echo "$message" | head -5)"
  
  # 更新 last_sent
  local tmp=$(mktemp)
  jq --arg channel "$channel" \
     --arg time "$(date +%Y-%m-%d)" \
     '.subscribers[$channel].last_sent = $time' "$PROMO_SUB_FILE" > "$tmp" && mv "$tmp" "$PROMO_SUB_FILE"
  
  return 0
}

# 主逻辑
main() {
  log "开始每日推送"
  
  if [[ ! -f "$PROMO_SUB_FILE" ]]; then
    log "无订阅者"
    exit 0
  fi
  
  # 获取所有启用的订阅者
  local subscribers=$(jq -r '.subscribers | to_entries[] | select(.value.enabled == true) | "\(.key) \(.value.user_id)"' "$PROMO_SUB_FILE" 2>/dev/null)
  
  if [[ -z "$subscribers" ]]; then
    log "无启用的订阅者"
    exit 0
  fi
  
  # 遍历推送
  while IFS=' ' read -r channel user_id; do
    push_to_subscriber "$channel" "$user_id"
    sleep 1  # 避免频率过高
  done <<< "$subscribers"
  
  log "推送完成"
}

main "$@"
