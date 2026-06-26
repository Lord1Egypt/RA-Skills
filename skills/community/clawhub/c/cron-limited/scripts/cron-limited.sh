#!/bin/bash
# cron-limited - 创建有限次数重复的定时任务
# 支持农历生日等场景及每年自动重复

set -e

COMMAND=""
EVERY=""
REPEAT=""
MESSAGE=""
CHANNEL="openclaw-weixin"
TO=""
LUNAR_MONTH=""
LUNAR_DAY=""
TIME="08:00"
DAYS_BEFORE=0
REPEAT_YEARLY=false

# 配置文件目录
CONFIG_DIR="$HOME/.openclaw/cron-limited"
CONFIG_FILE="$CONFIG_DIR/birthdays.json"
DAILY_JOB_MSG="CRON-LIMITED-DAILY-CHECK"

# 初始化配置目录
init_config() {
  mkdir -p "$CONFIG_DIR"
  if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "[]" > "$CONFIG_FILE"
  fi
}

# 获取当前时间戳（毫秒）
now_ms() {
  echo $(($(date +%s) * 1000))
}

# 解析时间间隔为秒
parse_duration() {
  local dur="$1"
  local seconds=0
  
  if [[ "$dur" =~ ^([0-9]+)s$ ]]; then
    seconds="${BASH_REMATCH[1]}"
  elif [[ "$dur" =~ ^([0-9]+)m$ ]]; then
    seconds=$(( ${BASH_REMATCH[1]} * 60 ))
  elif [[ "$dur" =~ ^([0-9]+)h$ ]]; then
    seconds=$(( ${BASH_REMATCH[1]} * 3600 ))
  else
    echo "错误: 无法解析时间间隔: $dur"
    exit 1
  fi
  
  echo $seconds
}

# 获取下一个农历日期对应的阳历日期
get_next_lunar_date() {
  local month=$1
  local day=$2
  local year=${3:-""}
  
  /tmp/lunar-venv/bin/python3 -c "
from lunarcalendar import Lunar, Converter
import datetime

today = datetime.date.today()
if '$year':
    year = int('$year')
else:
    year = today.year

lunar = Lunar(year, $month, $day)
solar = Converter.Lunar2Solar(lunar)
print(f'{solar.year}-{solar.month:02d}-{solar.day:02d}')
"
}

# 计算提前N天后的日期
calculate_reminder_date() {
  local solar_date="$1"
  local days_before=$2
  
  /tmp/lunar-venv/bin/python3 -c "
import datetime
date = datetime.date.fromisoformat('$solar_date')
reminder = date - datetime.timedelta(days=$days_before)
print(reminder.isoformat())
"
}

# 保存生日配置
save_birthday_config() {
  local lunar_month="$1"
  local lunar_day="$2"
  local message="$3"
  local time="$4"
  local days_before="$5"
  local channel="$6"
  local to="$7"
  
  init_config
  
  /tmp/lunar-venv/bin/python3 << PYEOF
import json
with open('$CONFIG_FILE', 'r') as f:
    data = json.load(f)

# 检查是否已存在相同配置
for entry in data:
    if entry['lunar_month'] == $lunar_month and entry['lunar_day'] == $lunar_day:
        # 更新现有条目
        entry['message'] = '''$message'''.strip()
        entry['time'] = '$time'
        entry['days_before'] = $days_before
        entry['channel'] = '$channel'
        entry['to'] = '$to'
        with open('$CONFIG_FILE', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('updated')
        exit(0)

# 添加新配置
new_entry = {
    'id': 'lunar_${lunar_month}_${lunar_day}',
    'lunar_month': $lunar_month,
    'lunar_day': $lunar_day,
    'message': '''$message'''.strip(),
    'time': '$time',
    'days_before': $days_before,
    'channel': '$channel',
    'to': '$to'
}
data.append(new_entry)

with open('$CONFIG_FILE', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('added')
PYEOF
}

# 创建每日检查任务（如果不存在）
ensure_daily_checker() {
  local job_name="cron-limited-每日生日检查"
  
  # 检查是否已存在
  if openclaw cron list --json 2>/dev/null | grep -q "\"$job_name\""; then
    return 0
  fi
  
  # 创建每日检查任务
  # 注意：这个任务的消息是一个特殊标记，实际检查逻辑由agent执行
  openclaw cron add \
    --name "$job_name" \
    --cron "0 7 * * *" \
    --message "$DAILY_JOB_MSG" \
    --no-deliver \
    --session isolated \
    --timeout-seconds 60 \
    --json 2>/dev/null
  
  echo "已创建每日检查任务"
}

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    add)
      COMMAND="add"
      shift
      ;;
    add-lunar)
      COMMAND="add-lunar"
      shift
      ;;
    --every)
      EVERY="$2"
      shift 2
      ;;
    --repeat)
      REPEAT="$2"
      shift 2
      ;;
    --message)
      MESSAGE="$2"
      shift 2
      ;;
    --channel)
      CHANNEL="$2"
      shift 2
      ;;
    --to)
      TO="$2"
      shift 2
      ;;
    --lunar)
      LUNAR="$2"
      LUNAR_MONTH="${LUNAR%%-*}"
      LUNAR_DAY="${LUNAR#*-}"
      shift 2
      ;;
    --time)
      TIME="$2"
      shift 2
      ;;
    --days-before)
      DAYS_BEFORE="$2"
      shift 2
      ;;
    --yearly)
      REPEAT_YEARLY=true
      shift
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

# 农历生日提醒
if [[ "$COMMAND" == "add-lunar" ]]; then
  if [[ -z "$LUNAR_MONTH" ]] || [[ -z "$LUNAR_DAY" ]] || [[ -z "$MESSAGE" ]]; then
    echo "错误: 需要 --lunar <月份-日期> 和 --message"
    exit 1
  fi
  
  # 计算生日阳历日期
  birthday_solar=$(get_next_lunar_date "$LUNAR_MONTH" "$LUNAR_DAY")
  echo "农历 ${LUNAR_MONTH}月${LUNAR_DAY}日 -> 阳历生日: $birthday_solar"
  
  # 计算提醒日期
  reminder_solar=$(calculate_reminder_date "$birthday_solar" "$DAYS_BEFORE")
  if [[ "$DAYS_BEFORE" -gt 0 ]]; then
    echo "提前 $DAYS_BEFORE 天 -> 提醒日期: $reminder_solar"
  else
    echo "提醒日期: $reminder_solar"
  fi
  
  if [[ "$REPEAT_YEARLY" == "true" ]]; then
    # 保存配置
    save_birthday_config "$LUNAR_MONTH" "$LUNAR_DAY" "$MESSAGE" "$TIME" "$DAYS_BEFORE" "$CHANNEL" "$TO"
    
    # 确保每日检查任务存在
    ensure_daily_checker
    
    echo ""
    echo "✅ 已创建每年重复的农历提醒！"
    echo ""
    echo "配置信息："
    echo "  农历日期: ${LUNAR_MONTH}月${LUNAR_DAY}日"
    echo "  生日阳历: $birthday_solar"
    echo "  提醒时间: $TIME"
    echo "  提前天数: $DAYS_BEFORE"
    echo ""
    echo "📋 提醒日程："
    echo "  ${reminder_solar} $TIME - 发送第一条提醒"
    echo "  之后每年自动重复，无需重新创建"
  else
    # 单次提醒 - 创建一次性任务
    if [[ "$DAYS_BEFORE" -gt 0 ]]; then
      display_message="📅 提醒：农历${LUNAR_MONTH}月${LUNAR_DAY}日是 ${birthday_solar}，还有 ${DAYS_BEFORE} 天！
${MESSAGE}"
    else
      display_message="🎂 今天是农历${LUNAR_MONTH}月${LUNAR_DAY}日！
${MESSAGE}"
    fi
    
    openclaw cron add \
      --name "农历${LUNAR_MONTH}月${LUNAR_DAY}日提醒" \
      --at "${reminder_solar}T${TIME}:00" \
      --message "$display_message" \
      --announce \
      --channel "$CHANNEL" \
      --to "$TO" \
      --delete-after-run \
      --json 2>&1 | jq -r '.id' > /dev/null
    
    echo ""
    echo "✅ 单次提醒创建成功！"
    echo "执行时间: ${reminder_solar} $TIME (上海时区)"
  fi
  
  exit 0
fi

# 有限次数重复任务
if [[ "$COMMAND" != "add" ]]; then
  echo "仅支持 add 和 add-lunar 命令"
  exit 1
fi

if [[ -z "$EVERY" ]] || [[ -z "$REPEAT" ]] || [[ -z "$MESSAGE" ]]; then
  echo "错误: --every, --repeat, --message 都是必需参数"
  exit 1
fi

every_seconds=$(parse_duration "$EVERY")
repeat_count=$REPEAT
total_ms=$(( (repeat_count - 1) * every_seconds * 1000 ))
delete_after_ms=$(( total_ms + 60 * 1000 ))

now_ts=$(now_ms)
delete_at_ms=$(( now_ts + delete_after_ms ))
delete_at_iso=$(date -d "@$(( delete_at_ms / 1000 ))" -Iseconds 2>/dev/null || date -r "$(( delete_at_ms / 1000 ))" "+%Y-%m-%dT%H:%M:%S%z")

echo "创建主任务..."
main_job=$(openclaw cron add \
  --name "cron-limited-主任务-$(date +%s)" \
  --every "$EVERY" \
  --message "$MESSAGE" \
  --announce \
  --channel "$CHANNEL" \
  --to "$TO" \
  --json 2>&1)

main_id=$(echo "$main_job" | jq -r '.id // empty')

if [[ -z "$main_id" ]]; then
  echo "错误: 创建主任务失败"
  echo "$main_job"
  exit 1
fi

echo "主任务创建成功: $main_id"

echo "创建自动删除任务..."

delete_job=$(openclaw cron add \
  --name "cron-limited-删除任务-$main_id" \
  --at "$delete_at_iso" \
  --message "openclaw cron rm $main_id" \
  --announce \
  --channel "$CHANNEL" \
  --to "$TO" \
  --delete-after-run \
  --json 2>&1)

delete_id=$(echo "$delete_job" | jq -r '.id // empty')

echo ""
echo "✅ cron-limited 任务创建完成！"
echo ""
echo "主任务ID:   $main_id"
echo "删除任务ID: $delete_id"
echo "执行次数:   $REPEAT 次"
echo "执行间隔:   $EVERY"
echo "删除时间:   $(date -d "@$(( delete_at_ms / 1000 ))" "+%Y-%m-%d %H:%M:%S %Z")"
