#!/usr/bin/env bash
# cap-arxiv/fetch.sh - 从 arXiv 获取论文标题和内容
#
# Usage:
#   ./fetch.sh <arxiv_id_or_url>
#   ./fetch.sh 2501.12948
#   ./fetch.sh https://arxiv.org/abs/2501.12948
#
# 输出: JSON { arxiv_id, title, content, content_length }
# 依赖: curl, sed, grep

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ─── 工具函数 ────────────────────────────────────────────────────────────────

# 从 URL 或纯 ID 提取 arXiv ID
extract_arxiv_id() {
    local input="$1"
    local id=""

    # 匹配 arxiv.org URL
    id=$(echo "$input" | grep -oE 'arxiv\.org/(abs|pdf|html)/([0-9]+\.[0-9]+)' | grep -oE '[0-9]+\.[0-9]+' || true)
    if [[ -n "$id" ]]; then echo "$id"; return 0; fi

    # 匹配纯 ID（可带 vN 后缀）
    id=$(echo "$input" | grep -oE '^[0-9]+\.[0-9]+(v[0-9]+)?$' | grep -oE '^[0-9]+\.[0-9]+' || true)
    if [[ -n "$id" ]]; then echo "$id"; return 0; fi

    return 1
}

# 从 abs 页面获取标题
fetch_title() {
    local arxiv_id="$1"
    local abs_url="https://arxiv.org/abs/${arxiv_id}"

    local html
    html=$(curl -sS -L --max-time 30 \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
        "$abs_url") || return 1

    # 提取 <meta name="citation_title"> 内容
    local title
    title=$(echo "$html" | grep -o '<meta name="citation_title"[^>]*content="[^"]*"' \
        | sed 's/.*content="\([^"]*\)".*/\1/' | head -1)

    if [[ -z "$title" ]]; then
        # 备用：从 <title> 提取
        title=$(echo "$html" | grep -o '<title>[^<]*</title>' | sed 's/<[^>]*>//g' | head -1)
    fi

    echo "$title"
}

# 从 HTML 版本获取论文内容（简化文本提取）
fetch_html_content() {
    local arxiv_id="$1"
    local html_url="https://arxiv.org/html/${arxiv_id}"

    local response http_code body
    response=$(curl -sS -L --max-time 60 -w "\n%{http_code}" \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
        "$html_url") || return 1

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [[ "$http_code" == "404" ]]; then
        # HTML 版本不可用，降级为 abs 页面摘要
        fetch_abs_content "$arxiv_id"
        return $?
    fi

    if [[ ! "$http_code" =~ ^2[0-9][0-9]$ ]]; then
        echo "HTTP error: $http_code" >&2
        return 1
    fi

    # 提取正文文本（去除 HTML 标签、脚本、样式）
    echo "$body" \
        | sed 's/<script[^>]*>.*<\/script>//g' \
        | sed 's/<style[^>]*>.*<\/style>//g' \
        | sed 's/<nav[^>]*>.*<\/nav>//g' \
        | sed 's/<footer[^>]*>.*<\/footer>//g' \
        | sed 's/<[^>]*>//g' \
        | sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&quot;/"/g' \
        | sed '/^[[:space:]]*$/d' \
        | tr -s ' ' \
        | head -3000
}

# 从 abs 页面获取摘要（降级）
fetch_abs_content() {
    local arxiv_id="$1"
    local abs_url="https://arxiv.org/abs/${arxiv_id}"

    local html
    html=$(curl -sS -L --max-time 30 \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
        "$abs_url") || return 1

    # 提取 abstract 块的文本
    local abstract
    abstract=$(echo "$html" \
        | sed -n '/<blockquote class="abstract/,/<\/blockquote>/p' \
        | sed 's/<[^>]*>//g' \
        | sed 's/^Abstract:[[:space:]]*//' \
        | tr -s ' ' \
        | sed '/^[[:space:]]*$/d')

    if [[ -n "$abstract" ]]; then
        echo "## Abstract"
        echo ""
        echo "$abstract"
    else
        echo "[No content available for ${arxiv_id}]"
    fi
}

# ─── 主逻辑 ──────────────────────────────────────────────────────────────────

main() {
    local input="${1:-}"

    if [[ -z "$input" || "$input" == "--help" || "$input" == "-h" ]]; then
        echo "Usage: $(basename "$0") <arxiv_id_or_url>" >&2
        echo "" >&2
        echo "Examples:" >&2
        echo "  $(basename "$0") 2501.12948" >&2
        echo "  $(basename "$0") https://arxiv.org/abs/2501.12948" >&2
        exit 1
    fi

    # 提取 arXiv ID
    local arxiv_id
    arxiv_id=$(extract_arxiv_id "$input") || {
        echo "{\"code\":40201,\"message\":\"Cannot extract arXiv ID from: $input\"}" >&2
        exit 1
    }

    echo "arXiv ID: $arxiv_id" >&2

    # 获取标题
    echo "Fetching title..." >&2
    local title
    title=$(fetch_title "$arxiv_id") || title="$arxiv_id"
    echo "Title: $title" >&2

    # 获取内容
    echo "Fetching content..." >&2
    local content
    content=$(fetch_html_content "$arxiv_id") || {
        echo "{\"code\":50001,\"message\":\"Failed to fetch content for $arxiv_id\"}" >&2
        exit 1
    }

    local content_length=${#content}
    echo "Content length: $content_length chars" >&2

    # 输出 JSON（使用 jq 如果可用，否则手动拼）
    if command -v jq &>/dev/null; then
        jq -n \
            --arg arxiv_id "$arxiv_id" \
            --arg title "$title" \
            --arg content "$content" \
            --argjson content_length "$content_length" \
            '{
                code: 0,
                message: "ok",
                data: {
                    arxiv_id: $arxiv_id,
                    title: $title,
                    content: $content,
                    content_length: $content_length
                }
            }'
    else
        # 无 jq 降级：纯文本输出
        echo "---"
        echo "arxiv_id: $arxiv_id"
        echo "title: $title"
        echo "content_length: $content_length"
        echo "---"
        echo "$content"
    fi
}

main "$@"
