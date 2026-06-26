#!/bin/bash
#
# 车辆信息查询脚本
# 功能：查询车辆位置、车况信息
# 版本：3.1.0
# 支持：Linux / macOS / Windows (Git Bash/WSL)
#

set -e

# ==================== 系统检测 ====================
detect_os() {
  case "$(uname -s)" in
    Linux*)     echo "Linux" ;;
    Darwin*)    echo "macOS" ;;
    MINGW*|MSYS*|CYGWIN*) echo "Windows" ;;
    *)          echo "Unknown" ;;
  esac
}

OS_TYPE=$(detect_os)

# ==================== 配置 ====================
if [ "$OS_TYPE" = "Windows" ]; then
  CACHE_FILE="${USERPROFILE}/.carkey_cache.json"
  HISTORY_FILE="${USERPROFILE}/.carkey_history.json"
  TMP_DIR="${TMP:-/tmp}"
else
  CACHE_FILE="${HOME}/.carkey_cache.json"
  HISTORY_FILE="${HOME}/.carkey_history.json"
  TMP_DIR="/tmp"
fi

TIMEOUT=30
MAX_RETRIES=2
API_BASE_URL="https://openapi.nokeeu.com"

# ==================== 颜色输出 ====================
if [ "$OS_TYPE" = "Windows" ]; then
  # Windows CMD/PowerShell 可能不支持 ANSI
  RED=''
  GREEN=''
  YELLOW=''
  BLUE=''
  NC=''
else
  RED='\e[0;31m'
  GREEN='\e[0;32m'
  YELLOW='\e[1;33m'
  BLUE='\e[0;34m'
  NC='\e[0m'
fi

# ==================== 状态码映射 ====================
map_power_status() {
  case "$1" in
    0) echo "熄火" ;;
    1) echo "ACC" ;;
    2) echo "ON" ;;
    *) echo "未知 ($1)" ;;
  esac
}

map_gear_status() {
  case "$1" in
    0) echo "无效" ;;
    1) echo "P 档" ;;
    2) echo "N 档" ;;
    3) echo "D 档" ;;
    4) echo "R 档" ;;
    5) echo "S 档" ;;
    *) echo "未知 ($1)" ;;
  esac
}

map_binary_status() {
  case "$1" in
    0) echo "关闭" ;;
    1) echo "开启" ;;
    *) echo "未知 ($1)" ;;
  esac
}

map_lock_status() {
  case "$1" in
    0) echo "解锁" ;;
    1) echo "上锁" ;;
    *) echo "未知 ($1)" ;;
  esac
}

# ==================== 工具函数 ====================
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
}

format_timestamp() {
  local ts="$1"
  if [ "$ts" = "null" ] || [ -z "$ts" ]; then
    echo "未知"
    return
  fi
  local secs=$((ts / 1000))
  
  case "$OS_TYPE" in
    macOS)
      date -r "$secs" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$ts"
      ;;
    Windows)
      # Git Bash/WSL 的 date 通常兼容 Linux
      date -d "@$secs" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$ts"
      ;;
    *)
      # Linux
      date -d "@$secs" "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "$ts"
      ;;
  esac
}

# ==================== 依赖检查 ====================
check_dependencies() {
  local missing=()
  
  if ! command -v curl &> /dev/null; then
    missing+=("curl")
  fi
  
  if ! command -v jq &> /dev/null; then
    missing+=("jq")
  fi
  
  if [ ${#missing[@]} -gt 0 ]; then
    echo ""
    echo "❌ 缺少依赖：${missing[*]}"
    echo ""
    echo "请安装："
    case "$OS_TYPE" in
      macOS)
        echo "  brew install ${missing[*]}"
        ;;
      Linux)
        echo "  Ubuntu/Debian: sudo apt-get install ${missing[*]}"
        echo "  CentOS/RHEL:   sudo yum install ${missing[*]}"
        ;;
      Windows)
        echo "  Git Bash: 重新安装 Git for Windows"
        echo "  WSL:       wsl sudo apt-get install ${missing[*]}"
        ;;
    esac
    echo ""
    exit 1
  fi
}

# ==================== 缓存管理 ====================
check_cache() {
  if [ ! -f "$CACHE_FILE" ]; then
    return 1
  fi
  
  local accessToken=$(jq -r '.accessToken // empty' "$CACHE_FILE")
  local vehicleToken=$(jq -r '.vehicleToken // empty' "$CACHE_FILE")
  
  if [ -n "$accessToken" ] && [ -n "$vehicleToken" ]; then
    return 0
  else
    return 1
  fi
}

save_tokens() {
  local vehicleToken="$1"
  local accessToken="$2"
  
  cat > "$CACHE_FILE" << EOF
{
  "accessToken": "$accessToken",
  "vehicleToken": "$vehicleToken",
  "last_updated": "$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S')"
}
EOF
  
  log_success "认证信息已保存"
}

parse_auth_input() {
  local input="$1"
  
  if [[ ! "$input" =~ "####" ]]; then
    log_error "认证信息格式错误，必须包含 #### 分隔符"
    return 1
  fi
  
  local vehicleToken=$(echo "$input" | awk -F '####' '{print $1}')
  local accessToken=$(echo "$input" | awk -F '####' '{print $2}')
  
  if [ -z "$vehicleToken" ] || [ -z "$accessToken" ]; then
    log_error "认证信息不完整"
    return 1
  fi
  
  echo "$vehicleToken"
  echo "$accessToken"
}

# ==================== API 调用 ====================
call_vehicle_api() {
  local accessToken="$1"
  local vehicleToken="$2"
  
  local retry=0
  local response
  
  while [ $retry -lt $MAX_RETRIES ]; do
    response=$(curl -s -X POST "${API_BASE_URL}/iot/v1/condition" \
      -H "Authorization: Bearer ${accessToken}" \
      -H "Content-Type: application/json" \
      -d "{\"vehicleToken\": \"${vehicleToken}\"}" \
      --max-time $TIMEOUT \
      2>/dev/null)
    
    local code=$(echo "$response" | jq -r '.code // -1' 2>/dev/null)
    
    if [ "$code" = "0" ]; then
      echo "$response"
      return 0
    elif [ "$code" = "401" ] || [ "$code" = "403" ]; then
      log_error "认证失败，Token 可能已过期"
      return 2
    else
      retry=$((retry + 1))
      if [ $retry -lt $MAX_RETRIES ]; then
        log_warning "请求失败，重试中... ($retry/$MAX_RETRIES)"
        sleep 1
      fi
    fi
  done
  
  local message=$(echo "$response" | jq -r '.message // "未知错误"' 2>/dev/null)
  log_error "查询失败：$message"
  return 1
}

# ==================== 数据展示 ====================
display_vehicle_info() {
  local response="$1"
  local query_type="${2:-full}"
  
  local sn=$(echo "$response" | jq -r '.data.sn // "未知"')
  local vin=$(echo "$response" | jq -r '.data.vin // "未知"')
  
  # 位置信息
  local longitude=$(echo "$response" | jq -r '.data.vehiclePosition.longitude // "null"')
  local latitude=$(echo "$response" | jq -r '.data.vehiclePosition.latitude // "null"')
  local address=$(echo "$response" | jq -r '.data.vehiclePosition.address // "null"')
  local update_time=$(echo "$response" | jq -r '.data.vehiclePosition.positionUpdateTime // "null"')
  local formatted_time=$(format_timestamp "$update_time")
  
  # 车况信息
  local power=$(echo "$response" | jq -r '.data.vehicleCondition.power // -1')
  local trunk=$(echo "$response" | jq -r '.data.vehicleCondition.trunk // -1')
  local gear=$(echo "$response" | jq -r '.data.vehicleCondition.gear // -1')
  
  # 车门状态
  local door_fl=$(echo "$response" | jq -r '.data.vehicleCondition.door.frontLeft // -1')
  local door_fr=$(echo "$response" | jq -r '.data.vehicleCondition.door.frontRight // -1')
  local door_rl=$(echo "$response" | jq -r '.data.vehicleCondition.door.rearLeft // -1')
  local door_rr=$(echo "$response" | jq -r '.data.vehicleCondition.door.rearRight // -1')
  
  # 车锁状态
  local lock_fl=$(echo "$response" | jq -r '.data.vehicleCondition.lock.frontLeft // -1')
  local lock_fr=$(echo "$response" | jq -r '.data.vehicleCondition.lock.frontRight // -1')
  local lock_rl=$(echo "$response" | jq -r '.data.vehicleCondition.lock.rearLeft // -1')
  local lock_rr=$(echo "$response" | jq -r '.data.vehicleCondition.lock.rearRight // -1')
  
  # 车窗状态
  local window_fl=$(echo "$response" | jq -r '.data.vehicleCondition.window.frontLeft // -1')
  local window_fr=$(echo "$response" | jq -r '.data.vehicleCondition.window.frontRight // -1')
  local window_rl=$(echo "$response" | jq -r '.data.vehicleCondition.window.rearLeft // -1')
  local window_rr=$(echo "$response" | jq -r '.data.vehicleCondition.window.rearRight // -1')
  
  # 空调状态
  local ac_left=$(echo "$response" | jq -r '.data.vehicleCondition.airConditionerState.acLeftTemp // "null"')
  local ac_right=$(echo "$response" | jq -r '.data.vehicleCondition.airConditionerState.acRightTemp // "null"')
  
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🚗 车辆信息"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📱 SN:  $sn"
  echo "🆔 VIN: $vin"
  echo ""
  
  if [ "$query_type" != "condition" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 位置信息"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ "$address" != "null" ] && [ -n "$address" ]; then
      echo "🏠 地址：$address"
      echo "📍 坐标：$latitude, $longitude"
      echo "🕐 更新：$formatted_time"
    else
      echo "🏠 地址：未知"
    fi
    echo ""
  fi
  
  if [ "$query_type" != "position" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔧 车况信息"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚡ 电源：$(map_power_status $power)"
    echo "🎯 档位：$(map_gear_status $gear)"
    echo "🚪 后备箱：$(map_binary_status $trunk)"
    echo ""
    
    # 车门状态汇总
    local all_doors_closed=true
    [[ "$door_fl" != "0" || "$door_fr" != "0" || "$door_rl" != "0" || "$door_rr" != "0" ]] && all_doors_closed=false
    if $all_doors_closed; then
      echo "🚪 车门：全部关闭 ✅"
    else
      echo "🚪 车门状态:"
      [[ "$door_fl" != "0" ]] && echo "   - 左前门：开启 ⚠️"
      [[ "$door_fr" != "0" ]] && echo "   - 右前门：开启 ⚠️"
      [[ "$door_rl" != "0" ]] && echo "   - 左后门：开启 ⚠️"
      [[ "$door_rr" != "0" ]] && echo "   - 右后门：开启 ⚠️"
    fi
    echo ""
    
    # 车锁状态汇总
    local all_locked=true
    [[ "$lock_fl" != "1" || "$lock_fr" != "1" || "$lock_rl" != "1" || "$lock_rr" != "1" ]] && all_locked=false
    if $all_locked; then
      echo "🔒 车锁：全部上锁 ✅"
    else
      echo "🔒 车锁状态:"
      [[ "$lock_fl" != "1" ]] && echo "   - 左前门：未上锁 ⚠️"
      [[ "$lock_fr" != "1" ]] && echo "   - 右前门：未上锁 ⚠️"
      [[ "$lock_rl" != "1" ]] && echo "   - 左后门：未上锁 ⚠️"
      [[ "$lock_rr" != "1" ]] && echo "   - 右后门：未上锁 ⚠️"
    fi
    echo ""
    
    # 车窗状态汇总
    local all_windows_closed=true
    [[ "$window_fl" != "0" || "$window_fr" != "0" || "$window_rl" != "0" || "$window_rr" != "0" ]] && all_windows_closed=false
    if $all_windows_closed; then
      echo "🪟 车窗：全部关闭 ✅"
    else
      echo "🪟 车窗状态:"
      [[ "$window_fl" != "0" ]] && echo "   - 左前窗：开启 ⚠️"
      [[ "$window_fr" != "0" ]] && echo "   - 右前窗：开启 ⚠️"
      [[ "$window_rl" != "0" ]] && echo "   - 左后窗：开启 ⚠️"
      [[ "$window_rr" != "0" ]] && echo "   - 右后窗：开启 ⚠️"
    fi
    echo ""
    
    # 空调状态
    if [ "$ac_left" != "null" ] && [ "$ac_right" != "null" ]; then
      echo "❄️ 空调：左侧 ${ac_left}℃ | 右侧 ${ac_right}℃"
    else
      echo "❄️ 空调：未开启"
    fi
  fi
  
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

save_history() {
  local response="$1"
  local query_type="$2"
  
  local timestamp=$(date +%s)
  local address=$(echo "$response" | jq -r '.data.vehiclePosition.address // "未知"')
  
  local history="[]"
  if [ -f "$HISTORY_FILE" ]; then
    history=$(jq '.queries // []' "$HISTORY_FILE" 2>/dev/null || echo "[]")
  fi
  
  local new_record=$(cat << EOF
{
  "timestamp": $timestamp,
  "type": "$query_type",
  "address": "$address",
  "sn": "$(echo "$response" | jq -r '.data.sn // "未知"')"
}
EOF
)
  
  echo "$history" | jq --argjson new "$new_record" '. + [$new] | .[-10:]' > "${TMP_DIR}/history_tmp.json"
  jq -n --slurpfile queries "${TMP_DIR}/history_tmp.json" '{queries: $queries[0]}' > "$HISTORY_FILE"
  rm -f "${TMP_DIR}/history_tmp.json"
}

# ==================== 主函数 ====================
main() {
  local query_type="${1:-full}"
  
  # 检查依赖
  check_dependencies
  
  if ! check_cache; then
    echo ""
    echo "❌ 未找到认证信息"
    echo ""
    echo "请提供认证信息，格式为："
    echo "  vehicleToken####accessToken"
    echo ""
    echo "示例："
    echo "  sk-api-xxxxx####eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    echo ""
    exit 1
  fi
  
  local accessToken=$(jq -r '.accessToken' "$CACHE_FILE")
  local vehicleToken=$(jq -r '.vehicleToken' "$CACHE_FILE")
  
  log_info "正在查询车辆信息..."
  
  local response
  response=$(call_vehicle_api "$accessToken" "$vehicleToken")
  local exit_code=$?
  
  if [ $exit_code -eq 0 ]; then
    display_vehicle_info "$response" "$query_type"
    save_history "$response" "$query_type"
    log_success "查询完成"
  elif [ $exit_code -eq 2 ]; then
    echo ""
    echo "⚠️  Token 已过期，请重新提供认证信息"
    echo ""
    rm -f "$CACHE_FILE"
    exit 2
  else
    exit 1
  fi
}

main "$@"