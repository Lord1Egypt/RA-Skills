#!/bin/bash
# Promo API 订阅管理
# 用法: promo_subscribe.sh [enable|disable|status] <channel> <user_id>

PROMO_SUB_FILE="$HOME/.promo_subscribers.json"
API_ENDPOINT="https://cli.aipromo.workers.dev"

# 初始化订阅文件
init_sub_file() {
  if [[ ! -f "$PROMO_SUB_FILE" ]]; then
    echo '{"subscribers":{}}' > "$PROMO_SUB_FILE"
  fi
}

# 开启订阅
enable_subscribe() {
  local channel="$1"
  local user_id="$2"
  
  init_sub_file
  
  local tmp=$(mktemp)
  jq --arg channel "$channel" \
     --arg user_id "$user_id" \
     --arg time "$(date +%Y-%m-%d)" \
     '.subscribers[$channel] = {
       "user_id": $user_id,
       "channel": $channel,
       "enabled": true,
       "created": $time,
       "last_sent": null
     }' "$PROMO_SUB_FILE" > "$tmp" && mv "$tmp" "$PROMO_SUB_FILE"
  
  echo "✅ 已开启每日优惠推送"
  echo "   推送时间：每天 9:00"
  echo "   关闭订阅：说'优惠订阅 关闭'"
}

# 关闭订阅
disable_subscribe() {
  local channel="$1"
  
  init_sub_file
  
  local tmp=$(mktemp)
  jq --arg channel "$channel" \
     '.subscribers[$channel].enabled = false' "$PROMO_SUB_FILE" > "$tmp" 2>/dev/null && mv "$tmp" "$PROMO_SUB_FILE"
  
  echo "❌ 已关闭每日优惠推送"
  echo "   重新开启：说'优惠订阅 开启'"
}

# 查看状态
get_status() {
  local channel="$1"
  
  init_sub_file
  
  local status=$(jq -r --arg channel "$channel" '.subscribers[$channel] // empty' "$PROMO_SUB_FILE")
  
  if [[ -z "$status" || "$status" == "null" ]]; then
    echo "📭 未订阅每日优惠推送"
    echo "   开启订阅：说'优惠订阅 开启'"
  else
    local enabled=$(jq -r --arg channel "$channel" '.subscribers[$channel].enabled' "$PROMO_SUB_FILE")
    local created=$(jq -r --arg channel "$channel" '.subscribers[$channel].created' "$PROMO_SUB_FILE")
    
    if [[ "$enabled" == "true" ]]; then
      echo "✅ 已订阅每日优惠推送"
      echo "   订阅时间：$created"
      echo "   关闭订阅：说'优惠订阅 关闭'"
    else
      echo "❌ 已关闭每日优惠推送"
      echo "   重新开启：说'优惠订阅 开启'"
    fi
  fi
}

case "$1" in
  enable|on|开启)
    enable_subscribe "$2" "$3"
    ;;
  disable|off|关闭)
    disable_subscribe "$2"
    ;;
  status|"")
    get_status "$2"
    ;;
  *)
    echo "用法: $0 [enable|disable|status] <channel> [user_id]"
    ;;
esac
