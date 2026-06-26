#!/bin/bash
# Promo API 提交优惠
# 用法: promo_submit.sh <平台> <标题> <链接> [奖励] [描述]

API_ENDPOINT="https://cli.aipromo.workers.dev"
USER_FILE="$HOME/.promo_user_id"

# 获取 user_id
get_user_id() {
  if [[ -f "$USER_FILE" ]]; then
    cat "$USER_FILE"
  else
    local new_id="u_$(head -c 16 /dev/urandom | xxd -p)"
    echo "$new_id" > "$USER_FILE"
    echo "$new_id"
  fi
}

# 提交优惠
submit_promo() {
  local platform="$1"
  local title="$2"
  local link="$3"
  local bonus="${4:-}"
  local description="${5:-}"
  
  local user_id=$(get_user_id)
  
  local json_payload=$(cat <<EOF
{
  "user_id": "$user_id",
  "platform_name": "$platform",
  "promo_title": "$title",
  "promo_link": "$link",
  "promo_bonus": "$bonus",
  "description": "$description"
}
EOF
)
  
  local response=$(curl -s --max-time 30 -X POST \
    -H "Content-Type: application/json" \
    -d "$json_payload" \
    "${API_ENDPOINT}/submit")
  
  if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
    echo "❌ 提交失败"
    echo "$response" | jq -r '.error'
  else
    echo "✅ 提交成功"
    echo "平台: $platform"
    echo "标题: $title"
    echo "链接: $link"
    if [[ -n "$bonus" ]]; then
      echo "奖励: $bonus"
    fi
    echo ""
    echo "📋 提交后会进行审核，审核通过后将展示给其他用户"
  fi
}

# 显示帮助
show_help() {
  echo "提交优惠信息"
  echo ""
  echo "用法: promo_submit.sh <平台> <标题> <链接> [奖励] [描述]"
  echo ""
  echo "示例:"
  echo "  promo_submit.sh \"硅基流动\" \"新用户福利\" \"https://siliconflow.cn\" \"100万Tokens\" \"新用户注册即送\""
  echo ""
  echo "参数说明:"
  echo "  平台    - 平台名称（如：硅基流动、智谱AI GLM）"
  echo "  标题    - 优惠标题"
  echo "  链接    - 优惠链接"
  echo "  奖励    - 优惠奖励（可选）"
  echo "  描述    - 详细描述（可选）"
}

# 主逻辑
main() {
  if [[ $# -lt 3 ]]; then
    show_help
    exit 1
  fi
  
  submit_promo "$@"
}

main "$@"
