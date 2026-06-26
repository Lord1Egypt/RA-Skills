#!/usr/bin/env bash
# cap-arxiv/interpret.sh - AI 深度解读 arXiv 论文
#
# Usage:
#   ./interpret.sh --arxiv-id 2501.12948
#   ./interpret.sh --arxiv-id 2501.12948 --output-dir ./output
#   ./interpret.sh --arxiv-id 2501.12948 --model deepseek-chat
#
# 环境变量:
#   AI_API_KEY    - AI API 密钥 (必需)
#   AI_BASE_URL   - AI API 地址 (可选，默认 https://api.openai.com/v1)
#   AI_MODEL      - 模型名 (可选，默认 gpt-4o-mini)
#
# 输出: Markdown 格式的论文解读文件
# 依赖: curl, jq

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ─── 默认配置 ─────────────────────────────────────────────────────────────────

AI_API_KEY="${AI_API_KEY:-}"
AI_BASE_URL="${AI_BASE_URL:-https://api.openai.com/v1}"
AI_MODEL="${AI_MODEL:-gpt-4o-mini}"

# ─── Prompt 定义 ──────────────────────────────────────────────────────────────

# Q1-Q6 系统提示
SYSTEM_PROMPT='{
  "role_definition": {
    "identity": "顶级学者 (Top Scholar)",
    "description": "一位对待科学态度严谨、表达简洁有力无歧义的学术专家。负责深度解读论文，实事求是，不发表主观臆测，一切分析均以论文原文和参考文献为据。以中文输出。",
    "core_traits": {
      "scientific_rigor": "逻辑严密，推导有据，拒绝模糊表述。",
      "objectivity": "完全基于文献证据，绝不虚构数据或结论。",
      "conciseness": "高密度信息输出，直击核心，拒绝冗余。而对核心内容进行适当的深度解释，揭示其机理。",
      "visual_structure": "善用排版工具（表格、公式、图片引用）增强结构感。"
    }
  },
  "global_formatting_rules": {
    "latex_math": "所有变量、符号、公式必须使用 LaTeX 格式。",
    "citation_protocol": "所有基于文献的事实陈述必须在句末标注来源。",
    "output_cleanliness": {
      "no_redundant_titles": "严禁在输出开头添加冗余标题行。直接从 Q1 开始输出。",
      "no_preamble": "不要添加任何开场白，直接进入解读内容。"
    }
  },
  "execution_framework_Q1_to_Q6": {
    "Q1_Problem": "Q1: 这篇论文试图解决什么问题？",
    "Q2_Related_Work": "Q2: 有哪些相关研究和技术路线？",
    "Q3_Methodology": "Q3: 论文如何解决这个问题？",
    "Q4_Experiments": "Q4: 论文做了哪些实验？",
    "Q5_Future_Exploration": "Q5: 有什么可以进一步探索的点？",
    "Q6_Summary": "Q6: 主要内容总结？"
  }
}'

# ─── 参数解析 ──────────────────────────────────────────────────────────────────

CB_ARXIV_ID=""
CB_OUTPUT_DIR="."
CB_INPUT_FILE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --arxiv-id) CB_ARXIV_ID="$2"; shift 2 ;;
        --output-dir|-o) CB_OUTPUT_DIR="$2"; shift 2 ;;
        --input-file|-i) CB_INPUT_FILE="$2"; shift 2 ;;
        --api-key) AI_API_KEY="$2"; shift 2 ;;
        --base-url) AI_BASE_URL="$2"; shift 2 ;;
        --model) AI_MODEL="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: $(basename "$0") --arxiv-id <ID> [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --arxiv-id ID       arXiv 论文 ID (如 2501.12948)"
            echo "  --output-dir DIR    输出目录 (默认当前目录)"
            echo "  --api-key KEY       AI API 密钥 (覆盖 AI_API_KEY)"
            echo "  --base-url URL      AI API 地址 (覆盖 AI_BASE_URL)"
            echo "  --model MODEL       模型名 (覆盖 AI_MODEL)"
            echo "  --input-file FILE   批量输入文件"
            exit 0
            ;;
        *) shift ;;
    esac
done

# ─── 校验 ─────────────────────────────────────────────────────────────────────

if [[ -z "$AI_API_KEY" ]]; then
    echo '{"code":40102,"message":"AI_API_KEY is required. Set via --api-key or AI_API_KEY env var."}' >&2
    exit 1
fi

# ─── AI API 调用 ──────────────────────────────────────────────────────────────

# 调用 OpenAI-compatible chat completions API
ai_chat() {
    local messages_json="$1"

    local response
    response=$(curl -sS --max-time 120 \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $AI_API_KEY" \
        -d "{
            \"model\": \"$AI_MODEL\",
            \"messages\": $messages_json,
            \"temperature\": 0.3
        }" \
        "${AI_BASE_URL}/chat/completions") || {
        echo "AI API call failed" >&2
        return 1
    }

    # 检查错误
    local error
    error=$(echo "$response" | jq -r '.error.message // empty' 2>/dev/null)
    if [[ -n "$error" ]]; then
        echo "AI API error: $error" >&2
        return 1
    fi

    # 提取回复内容
    echo "$response" | jq -r '.choices[0].message.content // empty'
}

# ─── 论文解读 ──────────────────────────────────────────────────────────────────

interpret_paper() {
    local arxiv_id="$1"
    local output_dir="$2"

    # 1. 获取论文内容
    echo "[$arxiv_id] Fetching paper..." >&2
    local fetch_result
    fetch_result=$("$SCRIPT_DIR/fetch.sh" "$arxiv_id") || {
        echo "[$arxiv_id] Failed to fetch paper" >&2
        return 1
    }

    local title content
    title=$(echo "$fetch_result" | jq -r '.data.title // empty' 2>/dev/null)
    content=$(echo "$fetch_result" | jq -r '.data.content // empty' 2>/dev/null)

    if [[ -z "$title" ]]; then title="$arxiv_id"; fi
    if [[ -z "$content" ]]; then
        echo "[$arxiv_id] No content available" >&2
        return 1
    fi

    # 截断过长内容（避免 token 超限）
    local max_chars=80000
    if [[ ${#content} -gt $max_chars ]]; then
        content="${content:0:$max_chars}"
        echo "[$arxiv_id] Content truncated to $max_chars chars" >&2
    fi

    # 2. 第一轮: Q1-Q6 解读
    echo "[$arxiv_id] [1/2] Q1-Q6 框架解读中..." >&2

    local user_prompt_1
    user_prompt_1="请按照系统提示中的框架，对以下论文进行深度解读。

论文标题: ${title}

论文内容:
${content}

输出要求：
1. 严格按照 Q1-Q6 的框架输出 Markdown 格式的解读
2. 直接从 \"## Q1: 这篇论文试图解决什么问题？\" 开始
3. 每个问题使用二级标题(##)，子节使用三级标题(###)"

    # 构建 messages JSON
    local messages_r1
    messages_r1=$(jq -n \
        --arg system "$SYSTEM_PROMPT" \
        --arg user "$user_prompt_1" \
        '[{"role":"system","content":$system},{"role":"user","content":$user}]')

    local result_1
    result_1=$(ai_chat "$messages_r1") || return 1

    if [[ -z "$result_1" ]]; then
        echo "[$arxiv_id] AI returned empty response for round 1" >&2
        return 1
    fi

    # 3. 第二轮: 补充指标、损失函数、数据集
    echo "[$arxiv_id] [2/2] 评价指标 / 损失函数 / 数据集..." >&2

    local user_prompt_2="解读论文中涉及到的评价指标、损失函数、数据集。

输出要求：
1. 使用 Markdown 格式
2. 直接从内容开始，不要添加开场白
3. 使用三级标题(###)区分各部分
4. 如果某部分论文中未涉及，简要说明即可"

    local messages_r2
    messages_r2=$(jq -n \
        --arg system "$SYSTEM_PROMPT" \
        --arg user1 "$user_prompt_1" \
        --arg assistant1 "$result_1" \
        --arg user2 "$user_prompt_2" \
        '[{"role":"system","content":$system},{"role":"user","content":$user1},{"role":"assistant","content":$assistant1},{"role":"user","content":$user2}]')

    local result_2
    result_2=$(ai_chat "$messages_r2") || {
        echo "[$arxiv_id] Round 2 failed, using round 1 only" >&2
        result_2=""
    }

    # 4. 组合输出
    local combined
    combined="# ${title}

> arXiv: [${arxiv_id}](https://arxiv.org/abs/${arxiv_id})

${result_1}"

    if [[ -n "$result_2" ]]; then
        combined="${combined}

${result_2}"
    fi

    # 5. 保存文件
    mkdir -p "$output_dir"
    local safe_title
    safe_title=$(echo "$title" | tr -cs 'A-Za-z0-9_-' '_' | head -c 100)
    local output_file="${output_dir}/${arxiv_id}_${safe_title}.md"
    echo "$combined" > "$output_file"

    echo "[$arxiv_id] Saved to: $output_file" >&2

    # 6. 输出 JSON 结果
    jq -n \
        --arg arxiv_id "$arxiv_id" \
        --arg title "$title" \
        --arg output_file "$output_file" \
        --argjson content_length "${#combined}" \
        '{
            code: 0,
            message: "ok",
            data: {
                arxiv_id: $arxiv_id,
                title: $title,
                output_file: $output_file,
                content_length: $content_length,
                rounds_completed: 2
            }
        }'
}

# ─── 主逻辑 ──────────────────────────────────────────────────────────────────

main() {
    echo "Model: $AI_MODEL" >&2

    # 收集所有 arxiv ID
    local ids=()

    if [[ -n "$CB_ARXIV_ID" ]]; then
        ids+=("$CB_ARXIV_ID")
    fi

    if [[ -n "$CB_INPUT_FILE" ]]; then
        if [[ ! -f "$CB_INPUT_FILE" ]]; then
            echo '{"code":40201,"message":"Input file not found: '"$CB_INPUT_FILE"'"}' >&2
            exit 1
        fi
        while IFS= read -r line; do
            line=$(echo "$line" | sed 's/#.*//' | tr -d '[:space:]')
            [[ -z "$line" ]] && continue
            ids+=("$line")
        done < "$CB_INPUT_FILE"
    fi

    if [[ ${#ids[@]} -eq 0 ]]; then
        echo '{"code":40201,"message":"No arXiv ID provided. Use --arxiv-id or --input-file."}' >&2
        exit 1
    fi

    echo "Papers to process: ${#ids[@]}" >&2

    local successes=0
    local failures=0

    for id in "${ids[@]}"; do
        echo "" >&2
        echo "========== $id ==========" >&2
        if interpret_paper "$id" "$CB_OUTPUT_DIR"; then
            ((successes++))
        else
            ((failures++))
            echo "[$id] FAILED" >&2
        fi
    done

    echo "" >&2
    echo "========== Done: $successes success, $failures failed ==========" >&2

    if [[ $failures -gt 0 ]]; then
        exit 1
    fi
}

main
