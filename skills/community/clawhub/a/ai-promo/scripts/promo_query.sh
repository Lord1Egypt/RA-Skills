#!/bin/bash
# Promo API 查询优惠
# 用法: promo_query.sh [all|referral|new_customer|limited_time|permanent_free] [user_id]

API_ENDPOINT="https://cli.aipromo.workers.dev"
USER_FILE="$HOME/.promo_user_id"

# 平台链接映射
declare -A PLATFORM_URLS=(
  ["plat_aliyun"]="https://www.aliyun.com/product/bailian"
  ["plat_siliconflow"]="https://cloud.siliconflow.cn/i/MhfNgy2S"
  ["plat_zhipu"]="https://www.bigmodel.cn/glm-coding?ic=40FM6F50MO"
  ["plat_minimax"]="https://platform.minimaxi.com"
  ["plat_moonshot"]="https://platform.moonshot.cn"
  ["plat_volcengine"]="https://www.volcengine.com"
  ["plat_tencent"]="https://cloud.tencent.com/product/hunyuan"
  ["plat_baidu"]="https://cloud.baidu.com/product/wenxinworkbench"
  ["plat_jdcloud"]="https://www.jdcloud.com/cn/pages/codingplan"
)

# 平台名称映射
declare -A PLATFORM_NAMES=(
  ["plat_aliyun"]="阿里云百炼"
  ["plat_siliconflow"]="硅基流动"
  ["plat_zhipu"]="智谱AI GLM"
  ["plat_minimax"]="MiniMax"
  ["plat_moonshot"]="月之暗面 Kimi"
  ["plat_volcengine"]="火山引擎豆包"
  ["plat_tencent"]="腾讯云混元"
  ["plat_baidu"]="百度千帆"
  ["plat_jdcloud"]="京东云 Coding Plan"
)

# 获取或创建 user_id
get_user_id() {
  if [[ -f "$USER_FILE" ]]; then
    cat "$USER_FILE"
  else
    local new_id="u_$(head -c 16 /dev/urandom | xxd -p)"
    echo "$new_id" > "$USER_FILE"
    echo "$new_id"
  fi
}

# 查询优惠
query_promos() {
  local category="$1"
  local user_id="$2"
  
  local url="${API_ENDPOINT}/list?user_id=${user_id}"
  
  if [[ -n "$category" && "$category" != "all" ]]; then
    url="${url}&categories=${category}"
  fi
  
  local json=$(curl -s --max-time 30 "$url" 2>/dev/null)
  
  # 如果 API 无法访问，使用本地缓存
  if [[ -z "$json" || "$json" == "null" || ! "$json" =~ '"items"' ]]; then
    local cache_file="$(dirname "$0")/../cache.json"
    if [[ -f "$cache_file" ]]; then
      json=$(cat "$cache_file")
      # 过滤分类
      if [[ -n "$category" && "$category" != "all" ]]; then
        json=$(echo "$json" | jq --arg cat "$category" '.items = [.items[] | select(.types[] | contains($cat))]')
      fi
    fi
  fi
  
  echo "$json"
}

# 格式化输出单个优惠
format_promo() {
  local id="$1"
  local platform_id="$2"
  local title="$3"
  local bonus="$4"
  local types="$5"
  local link="$6"
  local threshold="$7"
  
  local platform_name="${PLATFORM_NAMES[$platform_id]:-$platform_id}"
  local platform_url="${PLATFORM_URLS[$platform_id]:-}"
  
  # 使用优惠链接或平台链接
  local final_link="${link:-$platform_url}"
  
  echo "【${platform_name}】${title}"
  echo "   奖励: ${bonus:-无}"
  
  # 门槛信息
  if [[ -n "$threshold" && "$threshold" != "null" ]]; then
    local requirement=$(echo "$threshold" | jq -r '.requirement // empty' 2>/dev/null)
    if [[ -n "$requirement" ]]; then
      echo "   ⚠️ ${requirement}"
    fi
  fi
  
  # 链接
  if [[ -n "$final_link" ]]; then
    echo "   链接: ${final_link}"
  fi
  echo ""
}

# 主逻辑
main() {
  local category="${1:-all}"
  local user_id="${2:-$(get_user_id)}"
  
  local json=$(query_promos "$category" "$user_id")
  
  echo "📋 优惠列表（用户: $user_id）"
  echo ""
  
  case "$category" in
    referral)
      echo "💰 推荐奖励"
      ;;
    new_customer)
      echo "🎁 新客优惠"
      ;;
    limited_time)
      echo "🔥 限时抢购"
      ;;
    permanent_free)
      echo "🆓 永久免费"
      ;;
    *)
      echo "📦 全部优惠"
      ;;
  esac
  
  echo ""
  
  # 解析并输出
  local items=$(echo "$json" | jq -r '.items[] | @base64' 2>/dev/null)
  
  if [[ -z "$items" ]]; then
    echo "暂无数据（API 可能无法访问）"
  else
    echo "$json" | jq -r '.items[] | 
      "PLATFORM:\(.platform.id)|TITLE:\(.title)|BONUS:\(.bonus)|TYPES:\(.types | join(","))|LINK:\(.link)|THRESHOLD:\(.threshold)"' 2>/dev/null | \
    while IFS='|' read -r platform title bonus types link threshold; do
      platform_id="${platform#PLATFORM:}"
      title="${title#TITLE:}"
      bonus="${bonus#BONUS:}"
      link="${link#LINK:}"
      threshold="${threshold#THRESHOLD:}"
      
      if [[ "$link" == "null" ]]; then
        link=""
      fi
      
      format_promo "" "$platform_id" "$title" "$bonus" "" "$link" "$threshold"
    done
  fi
  
  echo "📋 推荐规则"
  echo "   - 提交的推荐链接有机会展示给其他用户"
  echo "   - 20% 概率显示您的推荐链接"
  echo "   - 同类优惠仅保留最早提交者"
  echo ""
  echo "🔗 查看详情: https://cli.aipromo.workers.dev/landing"
  echo ""
  echo "---"
  echo "💬 订阅每日优惠？说'优惠订阅 开启'"
  echo "🔄 更换用户ID？说'更换优惠用户ID'"
}

main "$@"
