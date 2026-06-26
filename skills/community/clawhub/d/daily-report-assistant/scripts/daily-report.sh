#!/usr/bin/env bash
# ============================================================
# 教研日报助手 — 每日日报处理模块
# 功能：解析对话输入 → 写入腾讯文档
# ============================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKDIR="${WORKDIR:-/root/.openclaw/workspace}"
MEMORY_DIR="${WORKDIR}/memory"
TDOC_MCP_URL="https://docs.qq.com/openapi/mcp"

# ── 配置文件位置 ──────────────────────────────────────────
CONFIG_FILE="${MEMORY_DIR}/user-config.md"
RECORD_CACHE_DIR="${MEMORY_DIR}/daily-records"

# ── 颜色输出 ──────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error(){ echo -e "${RED}[ERR]${NC} $1"; }
bold()  { echo -e "${CYAN}$1${NC}"; }

# ── 初始化目录 ───────────────────────────────────────────
init() {
    mkdir -p "$RECORD_CACHE_DIR"
}

# ── 读取配置 ──────────────────────────────────────────────
load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo "ERROR:not_configured"
        echo "请先运行：我要配置教研日报助手"
        return 1
    fi
    USER_NAME=$(grep "姓名：" "$CONFIG_FILE" | head -1 | sed 's/.*：//')
    RECORD_ID=$(grep "record_id：" "$CONFIG_FILE" | head -1 | sed 's/.*：//')
    # ── 可配置变量（可通过环境变量 TDOC_FILE_ID / TDOC_DAILY_SHEET_ID 覆盖） ──
    FILE_ID="${TDOC_FILE_ID:-DQ1hFandNaE1jZkto}"
    SHEET_ID="${TDOC_DAILY_SHEET_ID:-tMmx23}"
    PERSON_SHEET_ID="${TDOC_PERSON_SHEET_ID:-tFPVpZ}"
    PROJECT_SHEET_ID="${TDOC_PROJECT_SHEET_ID:-ss_w6lavv}"
    if [[ -z "$USER_NAME" ]]; then
        echo "ERROR:config_incomplete"
        return 1
    fi
    echo "OK:$USER_NAME:$RECORD_ID"
    return 0
}

# ── 写入单条日报 ─────────────────────────────────────────
write_daily_record() {
    local date_ts="$1"       # 毫秒时间戳
    local project_id="$2"    # 项目 record_id
    local hours="$3"         # 工时
    local content="$4"       # 工作内容
    local work_type="$5"     # 开发/非研发

    local result
    result=$(npx -y mcporter call "tencent-docs" "smartsheet.add_records" \
        --args "{
            \"file_id\": \"$FILE_ID\",
            \"records\": [{
                \"fields\": {
                    \"日期\": \"$date_ts\",
                    \"姓名\": {\"items\": [\"$RECORD_ID\"]},
                    \"项目名称\": {\"items\": [\"$project_id\"]},
                    \"工时\": $hours,
                    \"工作内容\": \"$content\",
                    \"类型\": \"$work_type\"
                }
            }],
            \"sheet_id\": \"$SHEET_ID\"
        }" 2>&1)

    if echo "$result" | grep -q '"error":""'; then
        echo "WRITE_OK"
        return 0
    else
        echo "WRITE_FAILED:$result"
        return 1
    fi
}

# ── 写入请假记录 ─────────────────────────────────────────
write_leave_record() {
    local date_ts="$1"
    local hours="$2"
    local note="${3:-}"

    # 请假记录写入同一表，但项目留空，类型为"非研发"
    local result
    result=$(npx -y mcporter call "tencent-docs" "smartsheet.add_records" \
        --args "{
            \"file_id\": \"$FILE_ID\",
            \"records\": [{
                \"fields\": {
                    \"日期\": \"$date_ts\",
                    \"姓名\": {\"items\": [\"$RECORD_ID\"]},
                    \"工时\": $hours,
                    \"工作内容\": \"请假：$note\",
                    \"类型\": \"非研发\"
                }
            }],
            \"sheet_id\": \"$SHEET_ID\"
        }" 2>&1)

    if echo "$result" | grep -q '"error":""'; then
        echo "WRITE_OK"
        return 0
    else
        echo "WRITE_FAILED:$result"
        return 1
    fi
}

# ── 写入加班记录 ─────────────────────────────────────────
write_overtime_record() {
    local date_ts="$1"
    local hours="$2"
    local note="${3:-}"

    local result
    result=$(npx -y mcporter call "tencent-docs" "smartsheet.add_records" \
        --args "{
            \"file_id\": \"$FILE_ID\",
            \"records\": [{
                \"fields\": {
                    \"日期\": \"$date_ts\",
                    \"姓名\": {\"items\": [\"$RECORD_ID\"]},
                    \"工时\": $hours,
                    \"工作内容\": \"加班：$note\",
                    \"类型\": \"非研发\"
                }
            }],
            \"sheet_id\": \"$SHEET_ID\"
        }" 2>&1)

    if echo "$result" | grep -q '"error":""'; then
        echo "WRITE_OK"
        return 0
    else
        echo "WRITE_FAILED:$result"
        return 1
    fi
}

# ── 读取某人员某月所有记录 ────────────────────────────────
read_monthly_records() {
    local user_record_id="$1"
    local year="$2"
    local month="$3"

    # 计算月份起始和结束时间戳
    local start_ts end_ts
    start_ts=$(date -d "${year}-${month}-01" +%s000 2>/dev/null || echo "0")
    local last_day=$(date -d "${year}-${month}-01 +1month -1day" +%Y-%m-%d 2>/dev/null || echo "${year}-${month}-28")
    end_ts=$(date -d "$last_day 23:59:59" +%s000 2>/dev/null || echo "0")

    npx -y mcporter call "tencent-docs" "smartsheet.list_records" \
        --args "{
            \"file_id\": \"$FILE_ID\",
            \"sheet_id\": \"$SHEET_ID\",
            \"limit\": 500
        }" 2>/dev/null | python3 -c "
import sys, json, datetime

try:
    data = json.load(sys.stdin)
    records = data.get('records', [])
    results = []
    for rec in records:
        fields = rec.get('field_values', [])
        rec_info = {}
        for f in fields:
            fname = f.get('field', '')
            if '日期' in fname:
                try:
                    ts = int(f.get('string_value', 0))
                    rec_info['date'] = datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d')
                except:
                    rec_info['date'] = ''
            elif '工时' in fname:
                rec_info['hours'] = f.get('number_value', 0)
            elif '工作内容' in fname:
                texts = f.get('text_value', {}).get('items', [])
                rec_info['content'] = ''.join(t.get('text', '') for t in texts)
            elif '类型' in fname:
                rec_info['type'] = f.get('option_value', {}).get('items', [{}])[0].get('text', '')
        if rec_info:
            rec_info['id'] = rec.get('record_id', '')
            results.append(rec_info)
    # 过滤当月
    month_prefix = f'${year}-{month.zfill(2)}'
    filtered = [r for r in results if r.get('date', '').startswith(month_prefix)]
    for r in filtered:
        print(json.dumps(r, ensure_ascii=False))
except Exception as e:
    print(f'ERROR:{e}', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null
}

# ── 生成月报摘要 ──────────────────────────────────────────
generate_monthly_summary() {
    local user_record_id="$1"
    local year="$2"
    local month="$3"

    local records
    records=$(read_monthly_records "$user_record_id" "$year" "$month")

    if [[ -z "$records" ]]; then
        echo "NO_RECORDS"
        return 1
    fi

    local total_hours=0
    local leave_hours=0
    local overtime_hours=0
    local projects=()

    while IFS= read -r line; do
        local hours content
        hours=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('hours',0))" 2>/dev/null)
        content=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('content',''))" 2>/dev/null)

        if [[ -z "$hours" ]]; then continue; fi

        total_hours=$((total_hours + hours))

        if echo "$content" | grep -q "请假"; then
            leave_hours=$((leave_hours + hours))
        elif echo "$content" | grep -q "加班"; then
            overtime_hours=$((overtime_hours + hours))
        fi
    done <<< "$records"

    echo "SUMMARY:"
    echo "总工时=$total_hours"
    echo "请假=$leave_hours"
    echo "加班=$overtime_hours"
    return 0
}

# ── 主帮助 ────────────────────────────────────────────────
show_help() {
    cat <<'EOF'
每日日报处理模块

用法：
  bash daily-report.sh config          检查配置状态
  bash daily-report.sh write <日期> <项目ID> <工时> <内容> <类型>
  bash daily-report.sh leave <日期> <工时> <说明>
  bash daily-report.sh overtime <日期> <工时> <说明>
  bash daily-report.sh read <年> <月>  读取月度记录
  bash daily-report.sh summary <年> <月> 生成月报摘要

示例：
  # 记录今日工作
  bash daily-report.sh write "2026-04-30" "rL5tMS" 4 "AI课程研发" "开发"

  # 记录请假
  bash daily-report.sh leave "2026-04-30" 4 "事假"

  # 生成月报
  bash daily-report.sh summary 2026 4
EOF
}

# ── 主入口 ───────────────────────────────────────────────
main() {
    init
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        config)
            load_config
            ;;
        write)
            local date_str="$1" project_id="$2" hours="$3" content="$4" work_type="$5"
            if [[ -z "$date_str" ]]; then
                error "缺少日期参数"
                exit 1
            fi
            # 转换为时间戳
            local date_ts
            date_ts=$(date -d "$date_str" +%s000 2>/dev/null || echo "0")
            write_daily_record "$date_ts" "$project_id" "$hours" "$content" "$work_type"
            ;;
        leave)
            local date_str="$1" hours="$2" note="$3"
            local date_ts
            date_ts=$(date -d "$date_str" +%s000 2>/dev/null || echo "0")
            write_leave_record "$date_ts" "$hours" "$note"
            ;;
        overtime)
            local date_str="$1" hours="$2" note="$3"
            local date_ts
            date_ts=$(date -d "$date_str" +%s000 2>/dev/null || echo "0")
            write_overtime_record "$date_ts" "$hours" "$note"
            ;;
        read)
            local year="$1" month="$2"
            load_config | grep -q "^OK" || exit 1
            local record_id=$(load_config | cut -d: -f3)
            read_monthly_records "$record_id" "$year" "$month"
            ;;
        summary)
            local year="$1" month="$2"
            load_config | grep -q "^OK" || exit 1
            local record_id=$(load_config | cut -d: -f3)
            generate_monthly_summary "$record_id" "$year" "$month"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "未知命令：$cmd"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
