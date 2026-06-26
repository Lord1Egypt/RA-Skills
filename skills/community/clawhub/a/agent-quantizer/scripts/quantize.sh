#!/usr/bin/env bash
# Agent Quantizer - 主入口
# 跨 OpenClaw 实例的 API 调用优化工具

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CACHE_DIR="$SKILL_DIR/cache"
CONFIG_FILE="$SKILL_DIR/config.json"

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
NC=$'\033[0m'

mkdir -p "$CACHE_DIR"

# ═══════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════

load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo '{}' > "$CONFIG_FILE"
    fi
}

get_config() {
    jq -r "$1 // $2" "$CONFIG_FILE" 2>/dev/null || echo "$2"
}

count_tokens() {
    # 粗略 token 估算：中文 ~1.5 token/字，英文 ~1.3 token/词
    local text="$1"
    python3 -c "
import re
text = '''$text'''
cn = len(re.findall(r'[\u4e00-\u9fff]', text))
en = len(re.findall(r'[a-zA-Z]+', text))
print(int(cn * 1.5 + en * 1.3))
" 2>/dev/null || echo "0"
}

check_deps() {
    local missing=()
    command -v jq &>/dev/null || missing+=("jq")
    command -v openclaw &>/dev/null || missing+=("openclaw")
    command -v python3 &>/dev/null || missing+=("python3")

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}缺少依赖: ${missing[*]}${NC}" >&2
        echo "安装: apt-get install jq python3" >&2
        return 1
    fi
}

# ═══════════════════════════════════════
# stats - Token 消耗统计
# ═══════════════════════════════════════

cmd_stats() {
    check_deps || return 1
    load_config

    local sessions_json
    sessions_json=$(openclaw sessions --json 2>/dev/null)

    if [[ -z "$sessions_json" ]] || [[ "$sessions_json" == "null" ]]; then
        echo -e "${RED}无法获取 session 数据${NC}" >&2
        return 1
    fi

    local count
    count=$(echo "$sessions_json" | jq -r '.count // 0')
    local threshold
    threshold=$(get_config '.compress.threshold' '80')

    echo -e "${BOLD}📊 Token 消耗统计${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "${CYAN}%-4s %-42s %-8s %10s %8s${NC}\n" "#" "SESSION" "TYPE" "TOKENS" "USAGE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    local i=1 total_tokens=0
    echo "$sessions_json" | jq -r '.sessions | sort_by(.totalTokens) | reverse | .[] | [.key, .kind, .totalTokens, .contextTokens] | @tsv' | \
    while IFS=$'\t' read -r key kind tokens context; do
        if [[ "$context" -le 0 ]]; then context=100000; fi
        local usage=$((tokens * 100 / context))
        total_tokens=$((total_tokens + tokens))

        local color="$GREEN"
        local tag=""
        if [[ $usage -ge $threshold ]]; then
            color="$YELLOW"
            tag=" ⚠️"
        fi
        if [[ $usage -ge 90 ]]; then
            color="$RED"
            tag=" 🔥"
        fi

        printf "${color}%-4s %-42s %-8s %10s %7s%%${NC}%s\n" "$i" "$key" "$kind" "$tokens" "$usage" "$tag"
        ((i++))
    done

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # 缓存统计
    if [[ -f "$CACHE_DIR/stats.json" ]]; then
        local hits misses
        hits=$(jq '.hits // 0' "$CACHE_DIR/stats.json")
        misses=$(jq '.misses // 0' "$CACHE_DIR/stats.json")
        local total=$((hits + misses))
        local rate=0
        if [[ $total -gt 0 ]]; then
            rate=$((hits * 100 / total))
        fi
        echo -e "  ${CYAN}缓存命中率: ${rate}% (${hits}/${total})${NC}"
    fi
}

# ═══════════════════════════════════════
# scan - 扫描高消耗 session
# ═══════════════════════════════════════

cmd_scan() {
    check_deps || return 1
    load_config

    local threshold
    threshold=$(get_config '.compress.threshold' '80')

    local sessions_json
    sessions_json=$(openclaw sessions --json 2>/dev/null)

    if [[ -z "$sessions_json" ]] || [[ "$sessions_json" == "null" ]]; then
        echo -e "${RED}无法获取 session 数据${NC}" >&2
        return 1
    fi

    echo -e "${BOLD}🔍 扫描阈值: ${threshold}%${NC}"
    echo ""

    local found=0
    echo "$sessions_json" | jq -r '.sessions | sort_by(.totalTokens) | reverse | .[] | [.key, .totalTokens, .contextTokens, .sessionId] | @tsv' | \
    while IFS=$'\t' read -r key tokens context sid; do
        if [[ "$context" -le 0 ]]; then context=100000; fi
        local usage=$((tokens * 100 / context))

        if [[ $usage -ge $threshold ]]; then
            found=1
            echo -e "${YELLOW}⚠️  ${key}${NC}"
            echo -e "   Token: ${tokens}/${context} (${usage}%)"
            echo -e "   建议: quantize compress ${key}"
            echo ""
        fi
    done

    if [[ $found -eq 0 ]]; then
        echo -e "${GREEN}✓ 所有 session 都在安全范围内${NC}"
    fi
}

# ═══════════════════════════════════════
# compress - 上下文压缩
# ═══════════════════════════════════════

cmd_compress() {
    check_deps || return 1
    load_config

    local session_key=""
    local mode="window"  # window | ai

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --ai) mode="ai"; shift ;;
            --window) mode="window"; shift ;;
            *) session_key="$1"; shift ;;
        esac
    done

    if [[ -z "$session_key" ]]; then
        echo -e "${RED}用法: quantize compress <session_key> [--ai|--window]${NC}" >&2
        return 1
    fi

    local sessions_json
    sessions_json=$(openclaw sessions --json 2>/dev/null)

    local session_data
    session_data=$(echo "$sessions_json" | jq -r --arg k "$session_key" '.sessions[] | select(.key == $k)')

    if [[ -z "$session_data" ]] || [[ "$session_data" == "null" ]]; then
        echo -e "${RED}Session 未找到: $session_key${NC}" >&2
        return 1
    fi

    local sid
    sid=$(echo "$session_data" | jq -r '.sessionId')
    local agent_id
    agent_id=$(echo "$session_key" | cut -d':' -f2)
    local state_dir="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
    local jsonl_file="$state_dir/agents/$agent_id/sessions/$sid.jsonl"

    echo -e "${YELLOW}🧠 压缩 session: $session_key${NC}"
    echo -e "   模式: $mode"
    echo -e "   Session ID: $sid"

    # 备份
    local timestamp
    timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_dir="$CACHE_DIR/backups"
    mkdir -p "$backup_dir"

    if [[ -f "$jsonl_file" ]]; then
        cp "$jsonl_file" "$backup_dir/${timestamp}_${sid}.jsonl"
        echo -e "${GREEN}   已备份: ${timestamp}_${sid}.jsonl${NC}"
    fi

    if [[ "$mode" == "ai" ]]; then
        # AI 摘要模式
        local summary_prompt='总结以下对话的关键信息，格式：1)已完成 2)关键决策 3)当前状态 4)待办事项。控制在 300 字内。不要使用工具。'

        local summary
        summary=$(openclaw agent --session-id "$sid" -m "$summary_prompt" --json 2>/dev/null | \
            jq -r '.result.payloads[0].text // .message.content[0].text // empty' 2>/dev/null)

        if [[ -n "$summary" ]]; then
            # 保存摘要
            echo "$summary" > "$backup_dir/${timestamp}_summary.md"
            echo -e "${GREEN}   摘要已生成${NC}"

            # 重置 session 并注入摘要
            if [[ -f "$jsonl_file" ]]; then
                rm "$jsonl_file"
                sleep 1
            fi

            local inject_msg="[上下文已压缩 - $(date '+%Y-%m-%d %H:%M')]\n\n$summary\n\n请确认已接收压缩上下文。"
            openclaw agent --to "$agent_id" -m "$inject_msg" --json 2>/dev/null

            echo -e "${GREEN}✅ 压缩完成 (AI 摘要模式)${NC}"
        else
            echo -e "${RED}   摘要生成失败${NC}" >&2
            return 1
        fi
    else
        # 滑动窗口模式 - 纯本地处理
        local max_window
        max_window=$(get_config '.compress.max_window' '6')
        local max_msgs=$((max_window * 2))  # user + assistant 对

        if [[ ! -f "$jsonl_file" ]]; then
            echo -e "${RED}   Session 文件不存在${NC}" >&2
            return 1
        fi

        local total_lines
        total_lines=$(wc -l < "$jsonl_file")

        if [[ $total_lines -le $((max_msgs + 1)) ]]; then
            echo -e "${GREEN}   上下文未超限，无需压缩${NC}"
            return 0
        fi

        # 生成旧消息摘要（grep 提取关键信息）
        local summary_file="$backup_dir/${timestamp}_window_summary.md"
        {
            echo "# 滑动窗口压缩摘要"
            echo "生成时间: $(date -Iseconds)"
            echo "保留最近 $max_window 轮对话"
            echo ""
            echo "## 关键信息"

            # 提取旧消息中的关键内容
            head -n -$max_msgs "$jsonl_file" | tail -n +2 | \
                jq -r '.message.content[]?.text // empty' 2>/dev/null | \
                grep -iE "决定|选择|使用|创建|修改|完成|错误|TODO|NOTE" | \
                head -20
        } > "$summary_file"

        # 构建新的 session 文件：保留 metadata + 摘要 + 最近消息
        local new_file="${jsonl_file}.new"

        # 保留第一行 (metadata)
        head -1 "$jsonl_file" > "$new_file"

        # 注入摘要作为 system 消息
        local summary_text
        summary_text=$(cat "$summary_file")
        jq -n --arg t "$summary_text" \
            '{"message":{"role":"system","content":[{"type":"text","text":"[之前对话摘要]\n" + $t}]}}' >> "$new_file"

        # 追加最近的消息
        tail -n "$max_msgs" "$jsonl_file" >> "$new_file"

        # 替换原文件
        mv "$new_file" "$jsonl_file"

        local before=$((total_lines - 1))
        local after=$(wc -l < "$jsonl_file")
        after=$((after - 1))
        echo -e "${GREEN}✅ 压缩完成 (滑动窗口)${NC}"
        echo -e "   消息数: $before → $after"
    fi
}

# ═══════════════════════════════════════
# trim - Prompt 精简
# ═══════════════════════════════════════

cmd_trim() {
    local file="$1"

    if [[ -z "$file" ]] || [[ ! -f "$file" ]]; then
        echo -e "${RED}用法: quantize trim <file.md>${NC}" >&2
        return 1
    fi

    echo -e "${YELLOW}✂️  精简文件: $file${NC}"

    local before_tokens
    before_tokens=$(count_tokens "$(cat "$file")")

    # 精简规则
    python3 - "$file" << 'PYEOF'
import sys, re

with open(sys.argv[1], 'r') as f:
    text = f.read()

original_len = len(text)

# 1. 删除空行超过 2 行的
text = re.sub(r'\n{3,}', '\n\n', text)

# 2. 删除礼貌性用语
politeness = [
    r'请.{0,5}(注意|确保|确认|记住)',
    r'(非常|十分|特别)?(感谢|谢谢).*?\n',
    r'如有.{0,3}(问题|疑问).{0,10}(请|欢迎).{0,10}\n',
    r'(希望|祝).{0,20}(顺利|愉快).*?\n',
]
for p in politeness:
    text = re.sub(p, '', text)

# 3. 压缩重复指令
text = re.sub(r'(请.{0,10})(\n\1)+', r'\1\n', text)

# 4. 删除 markdown 注释
text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

# 5. 合并连续的 bullet point 描述行
text = re.sub(r'(- .+)\n  (.+)', r'\1 \2', text)

# 6. 清理尾部空白
text = text.strip() + '\n'

saved = original_len - len(text)
with open(sys.argv[1], 'w') as f:
    f.write(text)

print(f"  原始: {original_len} 字符")
print(f"  精简: {len(text)} 字符")
print(f"  节省: {saved} 字符 ({saved*100//original_len}%)")
PYEOF

    local after_tokens
    after_tokens=$(count_tokens "$(cat "$file")")
    echo -e "${GREEN}  Token: ~${before_tokens} → ~${after_tokens}${NC}"
}

# ═══════════════════════════════════════
# cache 子命令代理
# ═══════════════════════════════════════

cmd_cache() {
    shift
    bash "$SCRIPT_DIR/cache.sh" "$@"
}

# ═══════════════════════════════════════
# 主入口
# ═══════════════════════════════════════

usage() {
    echo -e "${BOLD}Agent Quantizer - API 调用优化器${NC}"
    echo ""
    echo "用法: quantize <命令> [参数]"
    echo ""
    echo "命令:"
    echo -e "  ${CYAN}stats${NC}              查看所有 session token 消耗"
    echo -e "  ${CYAN}scan${NC}               扫描高消耗 session"
    echo -e "  ${CYAN}compress${NC} <key>     压缩 session 上下文"
    echo -e "  ${CYAN}  --ai${NC}              用 AI 生成摘要 (消耗少量 token)"
    echo -e "  ${CYAN}  --window${NC}          滑动窗口模式 (零消耗)"
    echo -e "  ${CYAN}trim${NC} <file>        精简 prompt 文件"
    echo -e "  ${CYAN}cache${NC} <subcmd>     缓存管理 (get/set/stats/clean/flush)"
    echo ""
    echo "示例:"
    echo "  quantize stats"
    echo "  quantize scan"
    echo "  quantize compress agent:main:main --window"
    echo "  quantize cache stats"
    echo "  quantize trim SOUL.md"
}

case "${1:-help}" in
    stats)    cmd_stats ;;
    scan)     cmd_scan ;;
    compress) shift; cmd_compress "$@" ;;
    trim)     shift; cmd_trim "${1:-}" ;;
    cache)    cmd_cache "$@" ;;
    help|--help|-h) usage ;;
    *)
        echo -e "${RED}未知命令: $1${NC}" >&2
        usage
        exit 1
        ;;
esac
