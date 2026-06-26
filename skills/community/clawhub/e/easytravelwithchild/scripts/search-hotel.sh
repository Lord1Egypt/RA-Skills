#!/usr/bin/env bash
# ============================================================
# search-hotel.sh — 亲子酒店搜索脚本（基于 flyai CLI）
#
# 用法:
#   ./scripts/search-hotel.sh [选项]
#
# 选项:
#   -c, --city      <城市>        目的地城市（必填）例如：上海、北京
#   -k, --keywords  <关键词>      补充关键词，例如："亲子 儿童游乐场"
#   -i, --checkin   <YYYY-MM-DD>  入住日期
#   -o, --checkout  <YYYY-MM-DD>  退房日期
#   -s, --stars     <星级>        酒店星级，多个用逗号分隔，例如：4,5
#   -p, --max-price <价格>        最高价格（元/晚）
#   -b, --bed-type  <床型>        床型：king/twin/multi
#   -S, --sort      <排序>        排序方式：rate_desc/price_asc/price_desc
#   -h, --help                    显示帮助
#
# 示例:
#   ./scripts/search-hotel.sh -c 上海 -k "亲子 儿童乐园" -s 4,5
#   ./scripts/search-hotel.sh -c 北京 -i 2026-05-01 -o 2026-05-03 -p 1500
# ============================================================

set -uo pipefail

# ---------- 默认值 ----------
CITY=""
KEYWORDS="亲子 儿童游乐场"
CHECKIN=""
CHECKOUT=""
STARS=""
MAX_PRICE=""
BED_TYPE=""
SORT="rate_desc"

# ---------- 帮助信息 ----------
usage() {
  sed -n '3,20p' "$0"
  exit 0
}

# ---------- 参数解析 ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--city)       CITY="$2";      shift 2 ;;
    -k|--keywords)   KEYWORDS="$2";  shift 2 ;;
    -i|--checkin)    CHECKIN="$2";   shift 2 ;;
    -o|--checkout)   CHECKOUT="$2";  shift 2 ;;
    -s|--stars)      STARS="$2";     shift 2 ;;
    -p|--max-price)  MAX_PRICE="$2"; shift 2 ;;
    -b|--bed-type)   BED_TYPE="$2";  shift 2 ;;
    -S|--sort)       SORT="$2";      shift 2 ;;
    -h|--help)       usage ;;
    *) echo "未知参数: $1"; usage ;;
  esac
done

# ---------- 必填校验 ----------
if [[ -z "$CITY" ]]; then
  echo "❌ 错误：必须指定目的地城市，使用 -c 或 --city"
  echo "示例：$0 -c 上海"
  exit 1
fi

# ---------- 构建关键词查询 ----------
QUERY="${CITY}亲子酒店 ${KEYWORDS}"
[[ -n "$STARS"     ]] && QUERY+=" ${STARS}星"
[[ -n "$MAX_PRICE" ]] && QUERY+=" 价格${MAX_PRICE}元以内"
[[ -n "$CHECKIN"   ]] && QUERY+=" 入住${CHECKIN}"
[[ -n "$CHECKOUT"  ]] && QUERY+=" 退房${CHECKOUT}"
[[ -n "$BED_TYPE"  ]] && QUERY+=" ${BED_TYPE}床"

# ---------- 执行搜索 ----------
echo "🔍 正在搜索 [$CITY] 亲子酒店..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

RAW=$(flyai keyword-search --query "$QUERY" 2>/dev/null)

if [[ -z "$RAW" ]]; then
  echo "⚠️  未获取到数据，请检查城市名称或网络连接"
  exit 1
fi

# ---------- 格式化输出 ----------
TMPFILE=$(mktemp)
echo "$RAW" > "$TMPFILE"

python3 <<PYEOF
import json

with open("$TMPFILE") as f:
    obj = json.load(f)

data  = obj.get("data") or {}
items = data.get("hotelList") or data.get("itemList") or []

if not items:
    print("\u26a0\ufe0f  \u672a\u627e\u5230\u7b26\u5408\u6761\u4ef6\u7684\u9152\u5e97\uff0c\u8bf7\u5c1d\u8bd5\u8c03\u6574\u641c\u7d22\u6761\u4ef6")
else:
    print(f"\u2705 \u5171\u627e\u5230 {len(items)} \u5bb6\u4eb2\u5b50\u9152\u5e97\n")
    for i, item in enumerate(items, 1):
        info     = item.get("info") or item
        name     = info.get("hotelName") or info.get("title") or "\u672a\u77e5\u9152\u5e97"
        stars    = info.get("star") or info.get("hotelStar") or "-"
        price    = info.get("price") or info.get("minPrice") or "-"
        score    = info.get("scoreDesc") or info.get("score") or "-"
        tags     = info.get("tags") or []
        jump_url = info.get("detailUrl") or info.get("jumpUrl") or ""
        pic_url  = info.get("mainPic") or info.get("picUrl") or ""
        stars_str = "\u2b50" * int(stars) if str(stars).isdigit() else str(stars)
        price_str = f"\xa5{price}/\u665a" if str(price).replace(".","").isdigit() else "\u4ef7\u683c\u9762\u8bae"
        tags_str  = " | ".join(tags[:3]) if tags else ""
        print(f"{'\u2500'*50}")
        print(f"  {i}. {name}")
        print(f"     \u661f\u7ea7: {stars_str}  \u8bc4\u5206: {score}  \u4ef7\u683c: {price_str}")
        if tags_str:
            print(f"     \u6807\u7b7e: {tags_str}")
        if pic_url:
            print(f"     \u56fe\u7247: {pic_url}")
        if jump_url:
            print(f"     \u9884\u8ba2: {jump_url}")
    print(f"{'\u2500'*50}")
    print("\n\U0001f4a1 \u63d0\u793a\uff1a\u70b9\u51fb\u4e0a\u65b9\u9884\u8ba2\u94fe\u63a5\u8df3\u8f6c\u98de\u732a\u5b8c\u6210\u9884\u8ba2")
PYEOF

rm -f "$TMPFILE"
