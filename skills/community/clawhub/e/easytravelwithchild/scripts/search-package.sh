#!/usr/bin/env bash
# ============================================================
# search-package.sh — 亲子度假套餐搜索脚本（基于 flyai CLI）
#
# 用法:
#   ./scripts/search-package.sh [选项]
#
# 选项:
#   -q, --query     <关键词>  搜索关键词（必填），支持自然语言描述
#   -h, --help                显示帮助
#
# 示例:
#   ./scripts/search-package.sh -q "上海亲子酒店套餐 含儿童门票"
#   ./scripts/search-package.sh -q "北京度假套餐 2大1小 周末"
#   ./scripts/search-package.sh -q "上海迪士尼亲子套票 春季"
#   ./scripts/search-package.sh -q "杭州亲子民宿 含早餐 含儿童活动"
# ============================================================

set -uo pipefail

QUERY=""

usage() {
  sed -n '3,17p' "$0"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -q|--query) QUERY="$2"; shift 2 ;;
    -h|--help)  usage ;;
    *) echo "未知参数: $1"; usage ;;
  esac
done

if [[ -z "$QUERY" ]]; then
  echo "❌ 错误：必须指定搜索关键词，使用 -q 或 --query"
  echo "示例：$0 -q \"上海亲子酒店套餐 含儿童门票\""
  exit 1
fi

echo "🎯 正在搜索度假套餐：[$QUERY]"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

RAW=$(flyai keyword-search --query "$QUERY" 2>/dev/null)

if [[ -z "$RAW" ]]; then
  echo "⚠️  未获取到数据，请检查关键词或网络连接"
  exit 1
fi

TMPFILE=$(mktemp)
echo "$RAW" > "$TMPFILE"

python3 <<PYEOF
import json

with open("$TMPFILE") as f:
    obj = json.load(f)

data     = obj.get("data") or {}
items    = data.get("itemList") or []

if not items:
    print("\u26a0\ufe0f  \u672a\u627e\u5230\u76f8\u5173\u5957\u9910\uff0c\u8bf7\u5c1d\u8bd5\u8c03\u6574\u5173\u952e\u8bcd")
else:
    hotels, packages, others = [], [], []
    for item in items:
        info  = item.get("info") or item
        title = info.get("title") or ""
        star  = info.get("star")
        if star:
            hotels.append(info)
        elif any(k in title for k in ["\u5957", "\u7968", "\u5929", "\u665a", "\u542b"]):
            packages.append(info)
        else:
            others.append(info)

    def print_section(label, infos):
        if not infos:
            return
        print(f"\n{'\u2550'*50}")
        print(f"  {label}\uff08{len(infos)} \u6761\uff09")
        print(f"{'\u2550'*50}")
        for i, info in enumerate(infos, 1):
            name     = info.get("title") or "\u672a\u77e5"
            star     = info.get("star") or ""
            price    = info.get("price") or ""
            score    = info.get("scoreDesc") or ""
            jump_url = info.get("jumpUrl") or info.get("detailUrl") or ""
            pic_url  = info.get("picUrl") or info.get("mainPic") or ""
            stars_str = "\u2b50" * int(star) if str(star).isdigit() else ""
            price_str = f"  \xa5{price}" if str(price).replace(".","").isdigit() else ""
            score_str = f"  \u8bc4\u5206:{score}" if score else ""
            print(f"  {i}. {name}")
            if stars_str or price_str or score_str:
                print(f"     {stars_str}{price_str}{score_str}")
            if pic_url:
                print(f"     \u56fe\u7247: {pic_url}")
            if jump_url:
                print(f"     \u9884\u8ba2: {jump_url}")

    print_section("\U0001f3e8 \u9152\u5e97",     hotels)
    print_section("\U0001f381 \u5ea6\u5047\u5957\u9910", packages)
    print_section("\U0001f4e6 \u5176\u4ed6\u4ea7\u54c1", others)

    total = len(hotels) + len(packages) + len(others)
    print(f"\n{'\u2500'*50}")
    print(f"\u2705 \u5171\u8fd4\u56de {total} \u6761\u7ed3\u679c\uff08\u9152\u5e97 {len(hotels)} | \u5957\u9910 {len(packages)} | \u5176\u4ed6 {len(others)}\uff09")
    print("\U0001f4a1 \u63d0\u793a\uff1a\u70b9\u51fb\u4e0a\u65b9\u9884\u8ba2\u94fe\u63a5\u8df3\u8f6c\u98de\u732a\u5b8c\u6210\u9884\u8ba2")
PYEOF

rm -f "$TMPFILE"
