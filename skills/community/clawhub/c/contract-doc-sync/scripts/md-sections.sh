#!/usr/bin/env bash
#
# md-sections — 提取 Markdown 文件的章节结构（JSON）或章节内容
#
# 用法:
#   ./scripts/md-sections <file>                          JSON 章节树
#   ./scripts/md-sections <file> "技术设计"                输出指定章节内容
#   ./scripts/md-sections <file> "技术设计" "登录时序图"    精确定位子章节
#   ./scripts/md-sections <file> --line 163               输出第 163 行所在章节的内容
#   ./scripts/md-sections -h | --help                     显示帮助
#
set -euo pipefail

# ── 全局数组 ───────────────────────────────────────────────
H_COUNT=0
H_START=()
H_END=()
H_LEVEL=()
H_TITLE=()

# ── 帮助 ──────────────────────────────────────────────────
usage() {
    cat <<'EOF'
md-sections — 提取 Markdown 文件的章节结构或章节内容

用法:
  md-sections <file>                            JSON 章节树（含 start/end/children）
  md-sections <file> <title>                    输出指定章节的内容
  md-sections <file> <title> <subtitle>...      按层级路径精确定位子章节
  md-sections <file> --line <number>            输出第 N 行所在章节的内容
  md-sections -h | --help                       显示帮助

示例:
  md-sections docs/modules/auth.md
  md-sections docs/modules/auth.md "API 参考"
  md-sections docs/modules/auth.md "技术设计" "登录时序图"
  md-sections docs/modules/auth.md --line 170
EOF
    exit 0
}

# ── 参数解析 ──────────────────────────────────────────────
[[ "${1:-}" == "-h" || "${1:-}" == "--help" ]] && usage

if [[ $# -eq 0 ]]; then
    printf '{"error":"missing_file","message":"请指定 Markdown 文件路径"}\n'
    exit 1
fi
FILE="$1"
shift || true

if [[ ! -f "$FILE" ]]; then
    printf '{"error":"file_not_found","file":"%s"}\n' "$FILE"
    exit 1
fi

MODE="json"
SECTION_PATH=()
TARGET_LINE=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --line)
            shift
            TARGET_LINE="${1:?错误: --line 后需要指定行号}"
            MODE="line"
            shift
            ;;
        *)  MODE="section"; SECTION_PATH+=("$1"); shift ;;
    esac
done

# ══════════════════════════════════════════════════════════
#  核心: 提取真实标题，排除代码块/行内代码/HTML注释
# ══════════════════════════════════════════════════════════
extract_headers_raw() {
    local file="$1"
    local in_code_block=false
    local in_html_comment=false
    local line_num=0

    while IFS= read -r line || [[ -n "$line" ]]; do
        line_num=$((line_num + 1))

        # 围栏代码块边界（行首最多 3 空格 + 3+ 反引号/波浪号）
        if [[ "$line" =~ ^[[:space:]]{0,3}(\`\`\`+|~~~+) ]]; then
            in_code_block=$( [[ "$in_code_block" == "false" ]] && echo "true" || echo "false" )
            continue
        fi
        [[ "$in_code_block" == "true" ]] && continue

        # HTML 注释边界
        if [[ "$line" =~ '<\!--' ]] && ! [[ "$line" =~ '-->' ]]; then
            in_html_comment=true
            continue
        fi
        if [[ "$in_html_comment" == "true" ]]; then
            [[ "$line" =~ '-->' ]] && in_html_comment=false
            continue
        fi

        # 匹配标题行: 行首 1-6 个 # 后跟空格或行尾
        if [[ "$line" =~ ^(#){1,6}([[:space:]]|$) ]]; then
            # 检查行内代码干扰: # 前的反引号是否为奇数个
            local before_hash="${line%%#*}"
            local backtick_count
            backtick_count=$(echo "$before_hash" | tr -cd '`' | wc -c | tr -d ' ')
            [[ $((backtick_count % 2)) -ne 0 ]] && continue

            local level="${line%%[!#]*}"
            local level_len=${#level}
            local title
            title=$(echo "$line" | sed 's/^#\{1,6\}[[:space:]]*//' | sed 's/[[:space:]]*$//')
            printf "%d|%d|%s\n" "$line_num" "$level_len" "$title"
        fi
    done < "$file"
}

# ══════════════════════════════════════════════════════════
#  加载标题到全局数组，计算每个标题的结束行
# ══════════════════════════════════════════════════════════
load_tree() {
    local file="$1"

    H_COUNT=0
    H_START=()
    H_END=()
    H_LEVEL=()
    H_TITLE=()

    local total_lines
    total_lines=$(wc -l < "$file" | tr -d ' ')

    local headers
    headers=$(extract_headers_raw "$file")

    if [[ -z "$headers" ]]; then
        return 1
    fi

    # 加载标题到数组
    while IFS='|' read -r lnum lvl title; do
        H_START+=("$lnum")
        H_LEVEL+=("$lvl")
        H_TITLE+=("$title")
        H_COUNT=$((H_COUNT + 1))
    done <<< "$headers"

    # 计算结束行：每个标题的范围到同级或更高级标题的前一行
    for ((i = 0; i < H_COUNT; i++)); do
        local end_line=$total_lines
        local current_level=${H_LEVEL[$i]}
        for ((j = i + 1; j < H_COUNT; j++)); do
            if [[ ${H_LEVEL[$j]} -le $current_level ]]; then
                end_line=$(( H_START[$j] - 1 ))
                break
            fi
        done
        H_END+=("$end_line")
    done

    return 0
}

# ══════════════════════════════════════════════════════════
#  JSON 嵌套树（无限层级递归）
# ══════════════════════════════════════════════════════════
json_escape() {
    local str="$1"
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\t'/\\t}"
    str="${str//$'\r'/}"
    echo "$str"
}

json_children() {
    local parent_idx=$1
    local child_level=$2
    local parent_end=${H_END[$parent_idx]}
    local result=""
    local first=true

    local i=$((parent_idx + 1))
    while [[ $i -lt $H_COUNT ]]; do
        [[ ${H_START[$i]} -gt $parent_end ]] && break

        if [[ ${H_LEVEL[$i]} -eq $child_level ]]; then
            $first || result+=","
            first=false

            local title_e
            title_e=$(json_escape "${H_TITLE[$i]}")
            local span=$(( H_END[$i] - H_START[$i] + 1 ))

            local gc
            gc=$(json_children "$i" $((child_level + 1)))

            result+="{\"title\":\"${title_e}\",\"level\":${child_level},\"start\":${H_START[$i]},\"end\":${H_END[$i]},\"lines\":${span},\"children\":[${gc}]}"
        fi
        i=$((i + 1))
    done
    echo "$result"
}

build_json_tree() {
    local file="$1"
    local total_lines
    total_lines=$(wc -l < "$file" | tr -d ' ')

    if [[ $H_COUNT -eq 0 ]]; then
        printf '{"file":"%s","totalLines":%d,"tree":null}\n' "$file" "$total_lines"
        return
    fi

    local root_title
    root_title=$(json_escape "${H_TITLE[0]}")
    local root_span=$(( H_END[0] - H_START[0] + 1 ))
    local root_level=${H_LEVEL[0]}

    local children
    children=$(json_children 0 $((root_level + 1)))

    local root_json
    root_json="{\"title\":\"${root_title}\",\"level\":${root_level},\"start\":${H_START[0]},\"end\":${H_END[0]},\"lines\":${root_span},\"children\":[${children}]}"

    printf '{"file":"%s","totalLines":%d,"tree":%s}\n' "$file" "$total_lines" "$root_json"
}

# 输出指定行范围内的 JSON 子树（匹配失败时使用）
# 参数: start_line end_line missing_title
build_json_subtree() {
    local range_start=$1
    local range_end=$2
    local missing_title
    missing_title=$(json_escape "$3")

    # 找范围内的第一个标题作为子树根节点
    local root_idx=-1
    for ((i = 0; i < H_COUNT; i++)); do
        if [[ ${H_START[$i]} -ge $range_start && ${H_START[$i]} -le $range_end ]]; then
            root_idx=$i
            break
        fi
    done

    if [[ $root_idx -eq -1 ]]; then
        printf '{"error":"not_found","missing":"%s","children":[]}\n' "$missing_title"
        return
    fi

    local root_title
    root_title=$(json_escape "${H_TITLE[$root_idx]}")
    local root_span=$(( H_END[$root_idx] - H_START[$root_idx] + 1 ))
    local root_level=${H_LEVEL[$root_idx]}

    local children
    children=$(json_children "$root_idx" $((root_level + 1)))

    printf '{"error":"not_found","missing":"%s","children":[{"title":"%s","level":%d,"start":%d,"end":%d,"lines":%d,"children":[%s]}]}\n' \
        "$missing_title" "$root_title" "$root_level" "${H_START[$root_idx]}" "${H_END[$root_idx]}" "$root_span" "$children"
}

# ══════════════════════════════════════════════════════════
#  模式: 按层级路径提取（逐层匹配）
# ══════════════════════════════════════════════════════════
show_section() {
    local file="$1"
    shift

    if [[ $H_COUNT -eq 0 ]]; then
        printf '{"error":"no_headers","file":"%s"}\n' "$file"
        exit 1
    fi

    local current_start=${H_START[0]}
    local current_end=${H_END[0]}

    for ((depth = 0; depth < ${#SECTION_PATH[@]}; depth++)); do
        local target="${SECTION_PATH[$depth]}"
        local found=-1

        for ((i = 0; i < H_COUNT; i++)); do
            # 必须在当前范围内
            [[ ${H_START[$i]} -lt $current_start || ${H_START[$i]} -gt $current_end ]] && continue
            # 前缀匹配标题
            if [[ "${H_TITLE[$i]}" == "${target}"* ]]; then
                found=$i
                current_start=${H_START[$i]}
                current_end=${H_END[$i]}
                break
            fi
        done

        if [[ $found -eq -1 ]]; then
            # 输出当前范围下的 JSON 子树，方便调用方解析后重试
            build_json_subtree "$current_start" "$current_end" "$target"
            exit 1
        fi
    done

    sed -n "${current_start},${current_end}p" "$file"
}

# ══════════════════════════════════════════════════════════
#  模式: 按行号定位
# ══════════════════════════════════════════════════════════
show_by_line() {
    local file="$1"
    local target="$2"
    if [[ $H_COUNT -eq 0 ]]; then
        printf '{"error":"no_headers","file":"%s"}\n' "$file"
        exit 1
    fi
    local best_idx=-1 best_level=0
    for ((i = 0; i < H_COUNT; i++)); do
        if [[ $target -ge ${H_START[$i]} && $target -le ${H_END[$i]} ]]; then
            [[ ${H_LEVEL[$i]} -ge $best_level ]] && { best_idx=$i; best_level=${H_LEVEL[$i]}; }
        fi
    done
    if [[ $best_idx -eq -1 ]]; then
        printf '{"error":"line_not_found","line":%d,"totalLines":%d}\n' "$target" "$(wc -l < "$file" | tr -d ' ')"
        exit 1
    fi
    sed -n "${H_START[$best_idx]},${H_END[$best_idx]}p" "$file"
}

# ══════════════════════════════════════════════════════════
#  执行
# ══════════════════════════════════════════════════════════
load_tree "$FILE" || true

case "$MODE" in
    json)    build_json_tree "$FILE" ;;
    section) show_section "$FILE" "${SECTION_PATH[@]}" ;;
    line)    show_by_line "$FILE" "$TARGET_LINE" ;;
esac
