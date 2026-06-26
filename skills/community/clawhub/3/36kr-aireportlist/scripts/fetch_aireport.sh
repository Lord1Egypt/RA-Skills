#!/usr/bin/env bash
# fetch_aireport.sh — 36kr 自助报道栏目文章 Shell 查询工具
#
# 依赖: curl, python3 (内置 json 模块)
#
# 用法:
#   bash fetch_aireport.sh                   # 查询今日自助报道
#   bash fetch_aireport.sh 2026-03-10        # 查询指定日期
#   bash fetch_aireport.sh --top 5           # 只显示前 5 篇
#   bash fetch_aireport.sh --json            # 输出原始 JSON
#   bash fetch_aireport.sh --titles          # 只输出标题列表
#   bash fetch_aireport.sh --recent 7        # 最近 7 天标题汇总
#
# Demo 直接运行:
#   chmod +x fetch_aireport.sh && ./fetch_aireport.sh

set -euo pipefail

BASE_URL="https://openclaw.36krcdn.com/media/aireport"
FILE_NAME="ai_report_articles.json"
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

# 日期偏移计算（兼容 macOS 与 Linux）
date_offset() {
    local base_date="$1"
    local offset="$2"
    if command -v gdate &>/dev/null; then
        gdate -d "${base_date} -${offset} days" +%Y-%m-%d 2>/dev/null
    else
        # macOS date
        date -v"-${offset}d" -jf "%Y-%m-%d" "${base_date}" +%Y-%m-%d 2>/dev/null \
            || date -d "${base_date} -${offset} days" +%Y-%m-%d
    fi
}

# 查询自助报道 JSON（带自动回退）
fetch_aireport() {
    local date="${1:-$(date +%Y-%m-%d)}"
    local fallback="${2:-true}"
    local max_attempts=1
    [ "$fallback" = "true" ] && max_attempts=$((MAX_FALLBACK + 1))

    for (( i=0; i<max_attempts; i++ )); do
        local query_date
        query_date=$(date_offset "$date" "$i")

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

# 格式化打印自助报道文章表格
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

print(f"\n{'─'*70}")
print(f"  36kr 自助报道  {date_str}")
print(f"{'─'*70}")

for item in articles:
    rank   = item.get("rank", "?")
    title  = item.get("title", "")
    author = item.get("author", "")
    pub    = item.get("publishTime", "")
    url    = item.get("url", "")
    print(f"  #{rank:<3} {title}")
    print(f"       作者: {author}  |  发布: {pub}")
    print(f"       {url}")
    print()

print(f"数据生成于: {gen_time}  共 {len(articles)} 篇")
print(f"{'─'*70}")
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

# 查询最近 N 天标题汇总（去重）
fetch_recent_titles() {
    local days="${1:-7}"
    local today
    today=$(date +%Y-%m-%d)

    python3 - "$BASE_URL" "$FILE_NAME" "$days" "$today" <<'PYEOF'
import sys, json, datetime, urllib.request, urllib.error

base_url  = sys.argv[1]
file_name = sys.argv[2]
days      = int(sys.argv[3])
today_str = sys.argv[4]
today     = datetime.date.fromisoformat(today_str)

seen = set()
results = []

for i in range(days):
    d = (today - datetime.timedelta(days=i)).isoformat()
    url = f"{base_url}/{d}/{file_name}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status == 200:
                for item in json.loads(resp.read().decode("utf-8")).get("data", []):
                    if item.get("url") not in seen:
                        seen.add(item["url"])
                        results.append(item)
    except urllib.error.HTTPError:
        pass
    except Exception:
        pass

results.sort(key=lambda x: x.get("publishTime", ""), reverse=True)
print(f"\n最近 {days} 天自助报道汇总（共 {len(results)} 篇，已去重）")
print("─" * 68)
for item in results:
    print(f"  [{item.get('publishTime','')}] #{item.get('rank','-')} {item.get('title','')}")
    print(f"       作者: {item.get('author','')}  链接: {item.get('url','')}")
    print()
PYEOF
}

# ─────── 主逻辑 ───────

main() {
    local date=""
    local top=999
    local output_mode="table"  # table | json | titles | recent
    local recent_days=7

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --top)     top="$2"; shift 2 ;;
            --json)    output_mode="json"; shift ;;
            --titles)  output_mode="titles"; shift ;;
            --recent)  output_mode="recent"; recent_days="${2:-7}"; shift 2 ;;
            --help|-h)
                echo "用法: $0 [日期 YYYY-MM-DD] [--top N] [--json] [--titles] [--recent N]"
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

    # 近期汇总模式
    if [ "$output_mode" = "recent" ]; then
        fetch_recent_titles "$recent_days"
        return
    fi

    [ -z "$date" ] && date=$(date +%Y-%m-%d)

    local json
    if ! json=$(fetch_aireport "$date" "true"); then
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

# Demo 1: 今日自助报道（表格模式）
# main

# Demo 2: 查看 2026-03-17 的自助报道
# main 2026-03-17

# Demo 3: 只看前 3 篇标题
# fetch_aireport | python3 -c "
# import sys, json
# for i in json.load(sys.stdin)['data'][:3]:
#     print(f\"TOP{i['rank']}: {i['title']}\")
# "

# Demo 4: 批量查询最近 7 天的第 1 篇标题
# for i in $(seq 0 6); do
#   d=$(date_offset "$(date +%Y-%m-%d)" "$i")
#   json=$(curl -sf "${BASE_URL}/${d}/${FILE_NAME}" 2>/dev/null)
#   if [ -n "$json" ]; then
#     title=$(echo "$json" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(d[0]['title'] if d else '无')")
#     echo "$d  #1: $title"
#   else
#     echo "$d  [无数据]"
#   fi
# done

# Demo 5: 近 3 天去重汇总
# main --recent 3
