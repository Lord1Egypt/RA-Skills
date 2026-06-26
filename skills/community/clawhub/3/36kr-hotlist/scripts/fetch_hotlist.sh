#!/usr/bin/env bash
# fetch_hotlist.sh — 36kr 24小时热榜 Shell 查询工具
#
# 依赖: curl, python3 (内置 json 模块)
#
# 用法:
#   bash fetch_hotlist.sh                   # 查询今日热榜
#   bash fetch_hotlist.sh 2026-03-10        # 查询指定日期
#   bash fetch_hotlist.sh --top 5           # 只显示前 5 名
#   bash fetch_hotlist.sh --json            # 输出原始 JSON
#   bash fetch_hotlist.sh --titles          # 只输出标题列表
#
# Demo 直接运行:
#   chmod +x fetch_hotlist.sh && ./fetch_hotlist.sh

set -euo pipefail

BASE_URL="https://openclaw.36krcdn.com/media/hotlist"
FILE_NAME="24h_hot_list.json"
MAX_FALLBACK=3

# ─────── 工具函数 ───────

log_warn()  { echo "[WARN]  $*" >&2; }
log_error() { echo "[ERROR] $*" >&2; }
log_info()  { echo "[INFO]  $*" >&2; }

# 构造 URL
build_url() {
    local date="$1"
    echo "${BASE_URL}/${date}/${FILE_NAME}"
}

# 查询热榜 JSON（带自动回退）
fetch_hotlist() {
    local date="${1:-$(date +%Y-%m-%d)}"
    local fallback="${2:-true}"
    local max_attempts=1
    [ "$fallback" = "true" ] && max_attempts=$((MAX_FALLBACK + 1))

    for (( i=0; i<max_attempts; i++ )); do
        local query_date
        if command -v gdate &>/dev/null; then
            query_date=$(gdate -d "${date} -${i} days" +%Y-%m-%d 2>/dev/null || date -v"-${i}d" -jf "%Y-%m-%d" "$date" +%Y-%m-%d)
        else
            # macOS date
            query_date=$(date -v"-${i}d" -jf "%Y-%m-%d" "$date" +%Y-%m-%d 2>/dev/null || date -d "${date} -${i} days" +%Y-%m-%d)
        fi

        local url
        url=$(build_url "$query_date")

        local http_code
        local tmp_body
        tmp_body=$(mktemp)
        http_code=$(curl -s -o "$tmp_body" -w "%{http_code}" --max-time 10 "$url" 2>/dev/null)
        local body
        body=$(cat "$tmp_body")
        rm -f "$tmp_body"

        if [ "$http_code" = "200" ]; then
            [ "$i" -gt 0 ] && log_info "当日无数据，已回退至 $query_date"
            echo "$body"
            return 0
        elif [ "$http_code" = "404" ]; then
            [ "$fallback" = "true" ] && log_warn "$query_date 无数据，尝试前一天..."
        else
            log_error "HTTP $http_code: $url"
            return 1
        fi
    done

    log_error "连续 ${max_attempts} 天均无数据，放弃查询"
    return 1
}

# 格式化打印热榜
print_table() {
    local json="$1"
    local top="${2:-999}"

    python3 - "$json" "$top" <<'PYEOF'
import sys, json

raw = sys.argv[1]
top = int(sys.argv[2])

data = json.loads(raw)
articles = data.get("data", [])[:top]

date_str = data.get("date", "?")
gen_ts   = data.get("time", 0)

import datetime
gen_time = datetime.datetime.fromtimestamp(gen_ts / 1000).strftime("%Y-%m-%d %H:%M:%S") if gen_ts else "?"

print(f"\n{'─'*68}")
print(f"  36kr 24小时热榜  {date_str}")
print(f"{'─'*68}")

for item in articles:
    rank  = item.get("rank", "?")
    title = item.get("title", "")
    author = item.get("author", "")
    pub   = item.get("publishTime", "")
    url   = item.get("url", "")
    print(f"  #{rank:<3} {title}")
    print(f"       作者: {author}  |  发布: {pub}")
    print(f"       {url}")
    print()

print(f"数据生成于: {gen_time}  共 {len(articles)} 篇")
print(f"{'─'*68}")
PYEOF
}

# 只输出标题列表
print_titles() {
    local json="$1"
    local top="${2:-999}"
    echo "$json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data['data'][:${top}]:
    print(f\"#{item['rank']:>2}  {item['title']}\")
"
}

# ─────── 主逻辑 ───────

main() {
    local date=""
    local top=999
    local output_mode="table"  # table | json | titles

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --top)    top="$2"; shift 2 ;;
            --json)   output_mode="json"; shift ;;
            --titles) output_mode="titles"; shift ;;
            --help|-h)
                echo "用法: $0 [日期 YYYY-MM-DD] [--top N] [--json] [--titles]"
                exit 0
                ;;
            *)
                if [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
                    date="$1"
                else
                    log_error "未知参数: $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done

    [ -z "$date" ] && date=$(date +%Y-%m-%d)

    local json
    if ! json=$(fetch_hotlist "$date" "true"); then
        exit 1
    fi

    case "$output_mode" in
        json)   echo "$json" | python3 -m json.tool ;;
        titles) print_titles "$json" "$top" ;;
        *)      print_table "$json" "$top" ;;
    esac
}

main "$@"


# ═══════════════════════════════════════════
# Demo 区 —— 取消注释直接运行体验各功能
# ═══════════════════════════════════════════

# Demo 1: 今日热榜（表格模式）
# main

# Demo 2: 查看 2026-03-17 的热榜
# main 2026-03-17

# Demo 3: 只看前 3 名标题
# fetch_hotlist | python3 -c "
# import sys, json
# for i in json.load(sys.stdin)['data'][:3]:
#     print(f\"TOP{i['rank']}: {i['title']}\")
# "

# Demo 4: 批量查询最近 7 天的第 1 名
# for i in $(seq 0 6); do
#   if command -v gdate &>/dev/null; then
#     d=$(gdate -d "today -${i} days" +%Y-%m-%d)
#   else
#     d=$(date -v"-${i}d" +%Y-%m-%d)
#   fi
#   json=$(curl -sf "${BASE_URL}/${d}/${FILE_NAME}" 2>/dev/null)
#   if [ -n "$json" ]; then
#     title=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(d[0]['title'] if d else '无')")
#     echo "$d  TOP1: $title"
#   else
#     echo "$d  [无数据]"
#   fi
# done
