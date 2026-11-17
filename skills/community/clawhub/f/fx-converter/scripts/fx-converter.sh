#!/usr/bin/env bash
# fx-converter: 实时汇率换算（数据源: Frankfurter / ECB 欧洲央行参考汇率）
# 用法:
#   fx-converter USD CNY          # 1 USD = ? CNY
#   fx-converter USD CNY 100      # 100 USD = ? CNY
#   fx-converter USD              # 列出 USD 兑主要货币
#   fx-converter --list           # 列出支持的货币
set -euo pipefail

API="https://api.frankfurter.app/latest"

# 货币代码 -> 中文名
declare -A CURRENCIES=(
  [USD]=美元 [CNY]=人民币 [EUR]=欧元 [JPY]=日元 [GBP]=英镑 [HKD]=港币
  [TWD]=新台币 [KRW]=韩元 [SGD]=新加坡元 [AUD]=澳元 [CAD]=加元 [CHF]=瑞郎
  [NZD]=新西兰元 [THB]=泰铢 [MYR]=马币 [INR]=卢比 [RUB]=卢布 [BRL]=雷亚尔
  [MXN]=墨西哥比索 [ZAR]=兰特 [SEK]=瑞典克朗 [NOK]=挪威克朗 [DKK]=丹麦克朗
)
cname() { echo "${CURRENCIES[${1^^}]:-${1^^}}"; }

LIST=0
FROM=""
TO=""
AMOUNT=1
for arg in "$@"; do
  case "$arg" in
    --list|-l) LIST=1 ;;
    --help|-h) sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)
      if [[ "$arg" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then AMOUNT="$arg"
      elif [ -z "$FROM" ]; then FROM="${arg^^}"
      elif [ -z "$TO" ]; then TO="${arg^^}"
      else echo "多余参数: $arg" >&2; exit 1; fi ;;
  esac
done

if [ "$LIST" = 1 ]; then
  echo "支持的主要货币："
  for k in USD CNY EUR JPY GBP HKD TWD KRW SGD AUD CAD CHF NZD THB MYR INR RUB BRL; do
    printf "  %s  %s\n" "$k" "${CURRENCIES[$k]}"
  done
  exit 0
fi

[ -z "$FROM" ] && { echo "用法: fx-converter USD CNY [金额]" >&2; exit 1; }

# 只有 FROM：列出主要兑换
if [ -z "$TO" ]; then
  echo "💱 1 $FROM（$(cname "$FROM")）兑换主要货币："
  DATA=$(curl -fsSL --max-time 15 "$API?from=$FROM&to=CNY,USD,EUR,JPY,GBP,HKD,KRW,SGD,AUD,CAD,CHF") || { echo "获取汇率失败，请检查网络" >&2; exit 1; }
  echo "$DATA" | FROM="$FROM" python3 -c '
import json,sys,os
from_ = os.environ["FROM"]
d=json.load(sys.stdin)
rates=d.get("rates",{})
order=["CNY","USD","EUR","JPY","GBP","HKD","KRW","SGD","AUD","CAD","CHF"]
names={"CNY":"人民币","USD":"美元","EUR":"欧元","JPY":"日元","GBP":"英镑","HKD":"港币","KRW":"韩元","SGD":"新加坡元","AUD":"澳元","CAD":"加元","CHF":"瑞郎"}
for c in order:
    if c in rates and c != from_:
        print(f"  {c} {names[c]}: {rates[c]:.4f}")
date_str = d.get("date", "-")
print(f"（数据日期: {date_str}，ECB参考汇率）")
'
  exit 0
fi

# 转换
DATA=$(curl -fsSL --max-time 15 "$API?from=$FROM&to=$TO") || { echo "获取汇率失败，请检查网络（注意：部分小众货币组合不可用）" >&2; exit 1; }
echo "$DATA" | FROM="$FROM" TO="$TO" AMOUNT="$AMOUNT" FNAME="$(cname "$FROM")" TNAME="$(cname "$TO")" python3 -c '
import json,sys,os
from_, to, amt, fname, tname = os.environ["FROM"], os.environ["TO"], float(os.environ["AMOUNT"]), os.environ["FNAME"], os.environ["TNAME"]
d=json.load(sys.stdin)
rate=d["rates"].get(to)
if rate is None:
    print(f"暂不支持 {from_} -> {to} 直接换算，试试用 USD 中转")
    sys.exit(1)
date_str = d.get("date", "-")
print(f"💱 {amt:,.2f} {from_}（{fname}） = {amt*rate:,.2f} {to}（{tname}）")
print(f"  汇率: 1 {from_} = {rate:.4f} {to}  （数据日期 {date_str}，ECB参考汇率）")
'
