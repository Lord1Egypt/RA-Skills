#!/usr/bin/env bash
# cn-holidays: 中国节假日查询（数据源: Nager.Date 公共节假日 API）
# 用法:
#   cn-holidays            # 今年所有法定节假日
#   cn-holidays 2026       # 指定年份
#   cn-holidays 2026-10    # 指定月份
#   cn-holidays 2026-10-01 # 指定日期
set -euo pipefail

API="https://date.nager.at/api/v3/PublicHolidays"

YEAR=$(date +%Y)
QUERY=""
for arg in "$@"; do
  case "$arg" in
    --help|-h) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) QUERY="$arg" ;;
  esac
done

# 解析查询
if [ -z "$QUERY" ]; then
  YEAR=$(date +%Y)
  MODE="year"
elif [[ "$QUERY" =~ ^[0-9]{4}$ ]]; then
  YEAR="$QUERY"; MODE="year"
elif [[ "$QUERY" =~ ^[0-9]{4}-[0-9]{2}$ ]]; then
  YEAR="${QUERY%%-*}"; MONTH="${QUERY##*-}"; MODE="month"
elif [[ "$QUERY" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  YEAR="${QUERY%%-*}"; MODE="day"
else
  echo "格式不对，试试: cn-holidays 2026 / cn-holidays 2026-10 / cn-holidays 2026-10-01" >&2
  exit 1
fi

# 节假日名称中英对照
declare -A HOLIDAYS=(
  [New Year's Day]=元旦 [Chinese New Year (Spring Festival)]=春节 [Qing Ming Festival]=清明节
  [Labour Day]=劳动节 [Dragon Boat Festival]=端午节 [Mid-Autumn Festival]=中秋节
  [National Day]=国庆节 [Lantern Festival]=元宵节 [Double Seventh Festival]=七夕
  [Hungry Ghost Festival]=中元节 [Chinese Valentine's Day]=七夕 [Ching Ming Festival]=清明节
  [Spring Festival]=春节 [Tomb-Sweeping Day]=清明节 [Labor Day]=劳动节
  [National Day Golden Week]=国庆黄金周
)
hname() {
  local en="$1"
  echo "${HOLIDAYS[$en]:-$en}"
}

case "$MODE" in
  year)
    DATA=$(curl -fsSL --max-time 20 "$API/$YEAR/CN") || { echo "获取失败，请检查网络" >&2; exit 1; }
    echo "$DATA" | python3 -c "
import json,sys
data=json.load(sys.stdin)
print(f'📅 $YEAR 年中国法定节假日（共 {len(data)} 天）：')
print()
for h in data:
    d=h['date']; name=h['localName']
    print(f'  {d}  {name}')
" ;;
  month)
    DATA=$(curl -fsSL --max-time 20 "$API/$YEAR/CN") || { echo "获取失败，请检查网络" >&2; exit 1; }
    echo "$DATA" | python3 -c "
import json,sys
data=json.load(sys.stdin)
month='$MONTH'
items=[h for h in data if h['date'][5:7]==month]
print(f'📅 $YEAR 年 $MONTH 月节假日（共 {len(items)} 天）：')
for h in items:
    print(f'  {h[\"date\"]}  {h[\"localName\"]}')
" ;;
  day)
    DATA=$(curl -fsSL --max-time 20 "$API/$YEAR/CN") || { echo "获取失败，请检查网络" >&2; exit 1; }
    echo "$DATA" | python3 -c "
import json,sys
data=json.load(sys.stdin)
q='$QUERY'
found=[h for h in data if h['date']==q]
if found:
    for h in found:
        print(f'🎉 $QUERY 是法定节假日：{h[\"localName\"]}')
else:
    print(f'📅 $QUERY 不是法定节假日')
" ;;
esac
