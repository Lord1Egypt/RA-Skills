#!/usr/bin/env bash
# fetch_ainotes.sh — 36kr AI 测评笔记 Shell 查询工具
#
# 依赖: curl, python3 (内置 json 模块)
#
# 用法:
#   bash fetch_ainotes.sh                   # 查询今日测评笔记
#   bash fetch_ainotes.sh 2026-03-18        # 查询指定日期
#   bash fetch_ainotes.sh --top 5           # 只显示前 5 篇
#   bash fetch_ainotes.sh --json            # 输出原始 JSON
#   bash fetch_ainotes.sh --titles          # 只输出标题列表
#
# Demo 直接运行:
#   chmod +x fetch_ainotes.sh && ./fetch_ainotes.sh

set -euo pipefail

BASE_URL="https://openclaw.36krcdn.com/media/ainotes"
FILE_NAME="ai_notes.json"
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

# 查询测评笔记 JSON（带自动回退）
fetch_ainotes() {
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

# 格式化打印测评笔记
print_table() {
    local json="$1"
    local top="${2:-999}"

    python3 - "$json" "$top" <<'PYEOF'
import sys, json, datetime

raw = sys.argv[1]
top = int(sys.argv[2])

notes = json.loads(raw)
if not isinstance(notes, list):
    notes = []
notes = notes[:top]

def fmt_time(ts_ms):
    if not ts_ms:
        return "?"
    try:
        return datetime.datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts_ms)

print(f"\n{'─'*70}")
print(f"  36kr AI 测评笔记  共 {len(notes)} 篇")
print(f"{'─'*70}")

for idx, item in enumerate(notes, 1):
    title   = item.get("title", "")
    author  = item.get("authorName", "")
    url     = item.get("noteUrl", "")
    circles  = "、".join(c.get("circleName", "") for c in (item.get("circleNames") or [])) or "—"
    products = "、".join(p.get("productName", "") for p in (item.get("productNames") or [])) or "—"
    pub_time = fmt_time(item.get("publishTime"))
    print(f"  #{idx:<3} {title}")
    print(f"       作者: {author}  |  发布: {pub_time}")
    print(f"       圈子: {circles}")
    print(f"       产品: {products}")
    print(f"       {url}")
    print()

print(f"{'─'*70}")
PYEOF
}

# 只输出标题列表
print_titles() {
    local json="$1"
    local top="${2:-999}"
    python3 - "$json" "$top" <<'PYEOF'
import sys, json

raw = sys.argv[1]
top = int(sys.argv[2])

notes = json.loads(raw)
if not isinstance(notes, list):
    notes = []
for i, item in enumerate(notes[:top], 1):
    print(f"#{i:>2}  {item.get('title', '')}  —  {item.get('authorName', '')}")
PYEOF
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
    if ! json=$(fetch_ainotes "$date" "true"); then
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

# Demo 1: 今日测评笔记（表格模式）
# main

# Demo 2: 查看 2026-03-18 的测评笔记
# main 2026-03-18

# Demo 3: 只看前 5 篇标题
# fetch_ainotes | python3 -c "
# import sys, json
# for i, n in enumerate(json.load(sys.stdin)[:5], 1):
#     print(f'#{i} {n[\"title\"]} — {n[\"authorName\"]}')
# "

# Demo 4: 输出原始 JSON
# main --json
