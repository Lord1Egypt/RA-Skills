#!/bin/bash
# FC Online官网监控脚本
# 版本：v1.0.0

set -e

# 配置
CONFIG_FILE="/tmp/fco-monitor-config.json"
LOG_FILE="/tmp/fco-monitor-$(date +%Y-%m-%d).log"
LAST_CHECK_FILE="/tmp/fco-monitor-last-check.json"
FCO_URL="https://fco.qq.com/main.shtml"

# 默认配置
DEFAULT_CONFIG='{
  "monitor": {
    "start_hour": 8,
    "end_hour": 23,
    "interval_minutes": 60
  },
  "notification": {
    "enabled": true,
    "only_new": true,
    "format": "detailed"
  },
  "keywords": {
    "high_priority": ["26TOTY", "绝版", "TY礼包", "限时折扣", "TOTYN"],
    "normal_priority": ["赛季", "活动", "更新", "公告", "礼包", "球员"]
  }
}'

# 日志函数
log() {
  local level="$1"
  local message="$2"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
  if [ "$level" = "ERROR" ] || [ "$level" = "WARN" ]; then
    echo "[$level] $message" >&2
  fi
}

# 初始化配置
init_config() {
  if [ ! -f "$CONFIG_FILE" ]; then
    echo "$DEFAULT_CONFIG" > "$CONFIG_FILE"
    log "INFO" "初始化默认配置"
  fi
}

# 读取配置
read_config() {
  if [ -f "$CONFIG_FILE" ]; then
    cat "$CONFIG_FILE"
  else
    echo "$DEFAULT_CONFIG"
  fi
}

# 获取官网内容
fetch_fco_content() {
  log "INFO" "开始获取FC Online官网内容"
  
  # 尝试多种方式获取内容
  local content=""
  local max_retries=3
  local retry_count=0
  
  while [ $retry_count -lt $max_retries ]; do
    log "INFO" "尝试获取官网内容 (第 $((retry_count+1)) 次)"
    
    # 方法1：使用curl直接获取
    content=$(curl -s -L "$FCO_URL" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" --connect-timeout 10 --max-time 30 2>/dev/null || true)
    
    if [ -n "$content" ] && [ ${#content} -gt 1000 ]; then
      log "INFO" "成功获取官网内容，长度: ${#content} 字符"
      break
    fi
    
    retry_count=$((retry_count+1))
    if [ $retry_count -lt $max_retries ]; then
      log "WARN" "获取内容失败，5秒后重试..."
      sleep 5
    fi
  done
  
  if [ -z "$content" ] || [ ${#content} -le 1000 ]; then
    log "ERROR" "无法获取官网内容"
    return 1
  fi
  
  echo "$content"
  return 0
}

# 提取新闻信息
extract_news() {
  local content="$1"
  local news_list=""
  
  # 尝试多种解析方式
  # 方式1：提取新闻标题和日期
  news_list=$(echo "$content" | grep -o 'news-title[^>]*>[^<]*' | sed 's/news-title[^>]*>//g' | head -20)
  
  if [ -z "$news_list" ]; then
    # 方式2：提取包含日期的新闻项
    news_list=$(echo "$content" | grep -o 'date[^>]*>[^<]*' | sed 's/date[^>]*>//g' | head -20)
  fi
  
  if [ -z "$news_list" ]; then
    # 方式3：提取所有可能的中文新闻标题
    news_list=$(echo "$content" | grep -o '>[^<>]*[0-9][0-9]/[0-9][0-9]<' | sed 's/>//g; s/</ /g' | head -20)
  fi
  
  echo "$news_list"
}

# 分析活动
analyze_activities() {
  local news_list="$1"
  local config_json="$2"
  
  # 提取关键词
  local high_priority_keywords=$(echo "$config_json" | jq -r '.keywords.high_priority[]' 2>/dev/null || echo "26TOTY 绝版 TY礼包")
  local normal_priority_keywords=$(echo "$config_json" | jq -r '.keywords.normal_priority[]' 2>/dev/null || echo "赛季 活动 更新")
  
  local activities=""
  local found_new=false
  
  # 检查上次检查结果
  local last_news=""
  if [ -f "$LAST_CHECK_FILE" ]; then
    last_news=$(jq -r '.news' "$LAST_CHECK_FILE" 2>/dev/null || echo "")
  fi
  
  # 分析每条新闻
  while IFS= read -r line; do
    if [ -z "$line" ]; then
      continue
    fi
    
    # 检查是否是新的
    if [ -n "$last_news" ] && echo "$last_news" | grep -q "$line"; then
      continue  # 上次已经检查过
    fi
    
    found_new=true
    
    # 检查关键词优先级
    local priority="normal"
    for keyword in $high_priority_keywords; do
      if echo "$line" | grep -q "$keyword"; then
        priority="high"
        break
      fi
    done
    
    # 提取日期
    local date=$(echo "$line" | grep -o '[0-9][0-9]/[0-9][0-9]' | head -1 || echo "")
    
    # 构建活动信息
    local activity="{\"title\":\"$line\",\"date\":\"$date\",\"priority\":\"$priority\"}"
    
    if [ -z "$activities" ]; then
      activities="$activity"
    else
      activities="$activities,$activity"
    fi
    
  done <<< "$news_list"
  
  # 保存本次检查结果
  echo "{\"timestamp\":\"$(date +%s)\",\"news\":\"$news_list\"}" > "$LAST_CHECK_FILE"
  
  if [ "$found_new" = true ]; then
    echo "[$activities]"
  else
    echo "[]"
  fi
}

# 生成通知消息
generate_notification() {
  local activities_json="$1"
  local config_json="$2"
  
  local notification=""
  local high_priority_count=0
  local normal_priority_count=0
  
  # 解析活动JSON
  local activities=$(echo "$activities_json" | jq -r '.[] | @base64' 2>/dev/null || echo "")
  
  if [ -z "$activities" ]; then
    echo "无新活动"
    return 0
  fi
  
  # 构建通知
  notification="🎯 【FC Online新活动通知】\n\n"
  
  for activity_base64 in $activities; do
    local activity=$(echo "$activity_base64" | base64 --decode)
    local title=$(echo "$activity" | jq -r '.title' 2>/dev/null || echo "")
    local date=$(echo "$activity" | jq -r '.date' 2>/dev/null || echo "")
    local priority=$(echo "$activity" | jq -r '.priority' 2>/dev/null || echo "normal")
    
    if [ "$priority" = "high" ]; then
      notification="${notification}🔥 **高优先级活动**\n"
      high_priority_count=$((high_priority_count+1))
    else
      notification="${notification}📢 常规活动\n"
      normal_priority_count=$((normal_priority_count+1))
    fi
    
    notification="${notification}📅 发布时间：$date\n"
    notification="${notification}📝 活动内容：$title\n\n"
  done
  
  notification="${notification}---\n"
  notification="${notification}📊 统计：高优先级活动 $high_priority_count 个，常规活动 $normal_priority_count 个\n"
  notification="${notification}🔗 官网地址：$FCO_URL\n"
  notification="${notification}⏰ 检查时间：$(date '+%Y-%m-%d %H:%M:%S')"
  
  echo "$notification"
}

# 主检查函数
check_now() {
  log "INFO" "开始执行FC Online官网检查"
  
  # 初始化
  init_config
  local config_json=$(read_config)
  
  # 获取内容
  local content=$(fetch_fco_content)
  if [ $? -ne 0 ]; then
    echo "❌ 无法访问FC Online官网"
    return 1
  fi
  
  # 提取新闻
  local news_list=$(extract_news "$content")
  if [ -z "$news_list" ]; then
    log "WARN" "未提取到新闻信息"
    echo "ℹ️ 未发现明显的活动信息"
    return 0
  fi
  
  log "INFO" "提取到新闻信息：$news_list"
  
  # 分析活动
  local activities_json=$(analyze_activities "$news_list" "$config_json")
  
  # 生成通知
  local notification=$(generate_notification "$activities_json" "$config_json")
  
  echo "$notification"
  return 0
}

# 设置定时任务
setup_monitor() {
  local start_hour=${1:-8}
  local end_hour=${2:-23}
  local interval_minutes=${3:-60}
  
  log "INFO" "设置监控任务：$start_hour:00-$end_hour:00，间隔${interval_minutes}分钟"
  
  # 更新配置
  local config_json=$(read_config)
  config_json=$(echo "$config_json" | jq ".monitor.start_hour = $start_hour | .monitor.end_hour = $end_hour | .monitor.interval_minutes = $interval_minutes")
  echo "$config_json" > "$CONFIG_FILE"
  
  echo "✅ 监控任务已设置"
  echo "   开始时间：$start_hour:00"
  echo "   结束时间：$end_hour:00"
  echo "   检查间隔：${interval_minutes}分钟"
  
  # 这里应该设置实际的cron任务
  # 实际实现会调用OpenClaw的cron工具
}

# 显示状态
show_status() {
  if [ -f "$CONFIG_FILE" ]; then
    local config_json=$(cat "$CONFIG_FILE")
    local start_hour=$(echo "$config_json" | jq -r '.monitor.start_hour')
    local end_hour=$(echo "$config_json" | jq -r '.monitor.end_hour')
    local interval=$(echo "$config_json" | jq -r '.monitor.interval_minutes')
    
    echo "📊 FC Online监控状态"
    echo "   运行时间：$start_hour:00 - $end_hour:00"
    echo "   检查间隔：${interval}分钟"
    echo "   最后日志：$LOG_FILE"
    
    if [ -f "$LAST_CHECK_FILE" ]; then
      local last_timestamp=$(jq -r '.timestamp' "$LAST_CHECK_FILE" 2>/dev/null || echo "0")
      if [ "$last_timestamp" != "0" ]; then
        local last_time=$(date -d "@$last_timestamp" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "未知")
        echo "   最后检查：$last_time"
      fi
    fi
  else
    echo "ℹ️ 监控未配置"
  fi
}

# 主函数
main() {
  local command="${1:-check-now}"
  
  case "$command" in
    "check-now")
      check_now
      ;;
    "setup")
      setup_monitor "$2" "$3" "$4"
      ;;
    "status")
      show_status
      ;;
    "help"|"--help"|"-h")
      echo "FC Online官网监控工具"
      echo "用法：$0 [命令]"
      echo ""
      echo "命令："
      echo "  check-now         立即检查官网活动"
      echo "  setup [开始小时] [结束小时] [间隔分钟]  设置定时监控"
      echo "  status            显示监控状态"
      echo "  help              显示帮助信息"
      ;;
    *)
      echo "未知命令: $command"
      echo "使用 '$0 help' 查看帮助"
      exit 1
      ;;
  esac
}

# 执行主函数
main "$@"