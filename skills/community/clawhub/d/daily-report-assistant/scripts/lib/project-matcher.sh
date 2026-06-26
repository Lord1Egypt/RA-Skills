#!/usr/bin/env bash
# ============================================================
# 教研日报助手 — 项目匹配工具
# 功能：输入工作描述 → 输出标准项目名称和ID
# ============================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKDIR="${WORKDIR:-/root/.openclaw/workspace}"
MEMORY_DIR="${WORKDIR}/memory"
TDOC_MCP_URL="https://docs.qq.com/openapi/mcp"

PROJECT_CACHE="${MEMORY_DIR}/projects-cache.json"
FILE_ID="${TDOC_FILE_ID:-DQ1hFandNaE1jZkto}"
PROJECT_SHEET_ID="${TDOC_PROJECT_SHEET_ID:-ss_w6lavv}"

# ── 项目匹配规则 ─────────────────────────────────────────
# 格式：关键词|项目ID|标准项目名|类型
declare -a PROJECT_RULES=(
    "AI微信小程序|rL5tMS|AI微信小程序|开发"
    "AI小龙虾|rL5tMS|AI小龙虾-4次课|开发"
    "图形化|r2kxf2|图形化编程一级V3.0|开发"
    "图形化二级|rrlnpL|图形化编程二级V3.0|开发"
    "Python|python|Rython编程一级V3.0|开发"
    "Python二级|rH5ldJ|Python编程二级V3.0|开发"
    "机器狗|rvNizC|灵芯派机器狗V1.0|开发"
    "灵芯派|rvNizC|灵芯派机器狗V1.0|开发"
    "单片机|r2kxf2|单片机三级-英文|开发"
    "3D打印|rM4mNH|2026-3D打印课程|开发"
    "红色文化图形化|rWVKrl|红色文化-图形化集训课|非研发"
    "红色文化Python|riLvSJ|红色文化-Python集训课|非研发"
    "AI人形|r5fXFX|人工智能三级V1.0-AI人形|开发"
    "AI交互|rxRas7|AI交互编程一级V3.0|开发"
    "威奇|r2kxf2|威奇硬件编程V3.0|开发"
    "一校|rH5ldJ|一校系统|非研发"
    "亚运村|rtgogk|亚运村校区支持|非研发"
    "儿童中心|rvwm6U|中国儿童中心课题|开发"
    "教研内部|r1Jb6i|教研内部工作|非研发"
    "会议|rlX2mm|会议|非研发"
    "渠道|rb0GGc|集团渠道支持|非研发"
    "乐博加盟|rYGdQ6|乐博加盟支持|非研发"
    "乐博直营|rmHs1L|乐博直营教学支持|非研发"
    "在线|rcbCUd|在线支持|开发"
    "AI赋能|rL5tMS|AI业务赋能|非研发"
    "知识库|rL5tMS|AI业务赋能|非研发"
    "暑期|rL5tMS|AI业务赋能|非研发"
    "人工智能平台|rHyzfP|人工智能教育平台|开发"
    "清华|rHyzfP|人工智能教育平台|开发"
    "教研|r1Jb6i|教研内部工作|非研发"
)

# ── 加载项目缓存 ──────────────────────────────────────────
load_project_cache() {
    if [[ -f "$PROJECT_CACHE" ]]; then
        cat "$PROJECT_CACHE"
        return 0
    fi
    # 缓存不存在，从网络加载
    refresh_project_cache
}

# ── 刷新项目缓存 ──────────────────────────────────────────
refresh_project_cache() {
    mkdir -p "$(dirname "$PROJECT_CACHE")"
    npx -y mcporter call "tencent-docs" "smartsheet.list_records" \
        --args "{
            \"file_id\": \"$FILE_ID\",
            \"sheet_id\": \"$PROJECT_SHEET_ID\",
            \"limit\": 100
        }" 2>/dev/null | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    records = data.get('records', [])
    projects = []
    for rec in records:
        fields = rec.get('field_values', [])
        name = ''
        pid = rec.get('record_id', '')
        for f in fields:
            if f.get('field') == '项目':
                texts = f.get('text_value', {}).get('items', [])
                name = ''.join(t.get('text', '') for t in texts)
                break
        if name:
            projects.append({'id': pid, 'name': name})
    print(json.dumps(projects, ensure_ascii=False))
except:
    print('[]')
" > "$PROJECT_CACHE"
    echo "Cache refreshed"
}

# ── 模糊匹配项目 ──────────────────────────────────────────
match_project() {
    local input="$1"
    input_lower=$(echo "$input" | tr '[:upper:]' '[:lower:]')

    for rule in "${PROJECT_RULES[@]}"; do
        IFS='|' read -r keyword project_id project_name work_type <<< "$rule"
        keyword_lower=$(echo "$keyword" | tr '[:upper:]' '[:lower:]')
        if echo "$input_lower" | grep -q "$keyword_lower"; then
            echo "MATCHED:$project_id:$project_name:$work_type"
            return 0
        fi
    done

    echo "MATCH_FAILED:未知项目，请描述具体工作内容"
    return 1
}

# ── 显示项目列表 ──────────────────────────────────────────
list_projects() {
    if [[ ! -f "$PROJECT_CACHE" ]]; then
        refresh_project_cache
    fi
    cat "$PROJECT_CACHE" | python3 -c "
import sys, json
projects = json.load(sys.stdin)
for p in projects:
    print(f\"{p['name']} (ID: {p['id']})\")
" 2>/dev/null || echo "无法读取项目列表"
}

# ── 主入口 ───────────────────────────────────────────────
main() {
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        match)
            local input="$*"
            if [[ -z "$input" ]]; then
                echo "请提供工作描述"
                exit 1
            fi
            match_project "$input"
            ;;
        list)
            list_projects
            ;;
        refresh)
            refresh_project_cache
            ;;
        help|--help|-h)
            cat <<'EOF'
项目匹配工具

用法：
  bash project-matcher.sh match <工作描述>   匹配项目
  bash project-matcher.sh list                列出所有项目
  bash project-matcher.sh refresh            刷新项目缓存

示例：
  bash project-matcher.sh match "AI课程研发"
  bash project-matcher.sh match "机器狗课程"
EOF
            ;;
        *)
            echo "未知命令：$cmd"
            main help
            ;;
    esac
}

main "$@"
