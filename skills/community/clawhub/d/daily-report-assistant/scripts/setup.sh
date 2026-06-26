#!/usr/bin/env bash
# ============================================================
# 教研日报助手 — 初始配置脚本
# 功能：引导用户完成腾讯文档授权 + 姓名确认
# 调用方式：bash scripts/setup.sh <子命令>
# ============================================================
set -euo pipefail

TDOC_API_BASE="${TDOC_API_BASE:-https://docs.qq.com}"
TDOC_AUTH_URL="${TDOC_AUTH_URL:-https://docs.qq.com/scenario/open-claw.html?nlc=1}"
TDOC_MCP_URL="https://docs.qq.com/openapi/mcp"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKDIR="${WORKDIR:-/root/.openclaw/workspace}"
MEMORY_DIR="${WORKDIR}/memory"

# ── 颜色输出 ──────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error(){ echo -e "${RED}[ERR]${NC} $1"; }

# ── 检查 mcporter ─────────────────────────────────────────
check_mcporter() {
    if ! command -v npx &>/dev/null; then
        echo "ERROR:node_not_found"
        return 1
    fi
    if ! npx -y mcporter list tencent-docs &>/dev/null 2>&1; then
        echo "ERROR:mcporter_not_configured"
        return 1
    fi
    echo "OK"
    return 0
}

# ── 检查授权状态 ──────────────────────────────────────────
# ── 可配置变量 ──────────────────────────────────────────
FILE_ID="${TDOC_FILE_ID:-DQ1hFandNaE1jZkto}"

check_auth() {
    result=$(npx -y mcporter call "tencent-docs" "smartsheet.list_tables" \
        --args "{\"file_id\": \"$FILE_ID\"}" 2>&1)
    if echo "$result" | grep -q '"error":""'; then
        echo "AUTH_OK"
        return 0
    fi
    if echo "$result" | grep -q "400006\|token"; then
        echo "AUTH_REQUIRED"
        return 1
    fi
    echo "AUTH_UNKNOWN"
    return 1
}

# ── 设置 Token ────────────────────────────────────────────
set_token() {
    local token="$1"
    npx -y mcporter config add tencent-docs "$TDOC_MCP_URL" \
        --header "Authorization=$token" \
        --transport http \
        --scope home 2>&1
    echo "TOKEN_SET"
}

# ── 验证 Token ────────────────────────────────────────────
verify_token() {
    result=$(npx -y mcporter call "tencent-docs" "smartsheet.list_tables" \
        --args "{\"file_id\": \"$FILE_ID\"}" 2>&1)
    if echo "$result" | grep -q '"error":""'; then
        echo "TOKEN_VALID"
        return 0
    fi
    echo "TOKEN_INVALID"
    return 1
}

# ── 获取人员列表 ──────────────────────────────────────────
list_persons() {
    npx -y mcporter call "tencent-docs" "smartsheet.list_records" \
        --args "{\"file_id\": \"$FILE_ID\", \"limit\": 50, \"sheet_id\": \"${TDOC_PERSON_SHEET_ID:-tFPVpZ}\"}" \
        2>/dev/null | grep -o '"text":"[^"]*"' | grep -v "^\"text\":\"$" | \
        sed 's/"text":"//;s/"$//' | head -50
}

# ── 匹配人员 ─────────────────────────────────────────────
match_person() {
    local name="$1"
    list_persons | grep -F "$name" | head -1
}

# ── 保存用户配置 ─────────────────────────────────────────
save_user_config() {
    local name="$1"
    local record_id="$2"
    mkdir -p "$MEMORY_DIR"
    cat > "$MEMORY_DIR/user-config.md" <<EOF
# 用户配置 — 教研日报助手
> 更新时间：$(date '+%Y-%m-%d %H:%M:%S')

## 基本信息
- 姓名：$name
- record_id：$record_id
- 授权状态：已授权
- 配置时间：$(date '+%Y-%m-%d %H:%M:%S')

## 腾讯文档配置
- 日报表 file_id：DQ1hFandNaE1jZkto
- 每日进展 sheet_id：tMmx23
- 教研人员 sheet_id：tFPVpZ
- 项目信息 sheet_id：ss_w6lavv

## 最近更新
EOF
    info "配置已保存到 $MEMORY_DIR/user-config.md"
}

# ── 主帮助 ────────────────────────────────────────────────
show_help() {
    cat <<'EOF'
教研日报助手配置脚本

用法：
  bash setup.sh check          检查当前状态
  bash setup.sh auth <token>  设置授权 Token
  bash setup.sh verify         验证 Token 是否有效
  bash setup.sh persons        列出可用人员
  bash setup.sh set-name <姓名> 设置用户姓名
  bash setup.sh show           显示当前配置

首次使用请按顺序执行：
  1. bash setup.sh auth <your_token>
  2. bash setup.sh verify
  3. bash setup.sh set-name <你的姓名>
EOF
}

# ── 主入口 ───────────────────────────────────────────────
main() {
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        check)
            if check_mcporter | grep -q "ERROR"; then
                echo "STATUS:mcporter_missing"
                exit 1
            fi
            if check_auth | grep -q "AUTH_OK"; then
                echo "STATUS:ready"
            else
                echo "STATUS:auth_required"
                echo "AUTH_URL:$TDOC_AUTH_URL"
            fi
            ;;
        auth)
            local token="${1:-}"
            if [[ -z "$token" ]]; then
                error "请提供 Token：bash setup.sh auth <your_token>"
                exit 1
            fi
            set_token "$token"
            ;;
        verify)
            verify_token
            ;;
        persons)
            list_persons
            ;;
        set-name)
            local name="${1:-}"
            if [[ -z "$name" ]]; then
                error "请提供姓名：bash setup.sh set-name <你的姓名>"
                exit 1
            fi
            local matched=$(match_person "$name")
            if [[ -n "$matched" ]]; then
                save_user_config "$name" "$matched"
                echo "NAME_SET:$name"
            else
                warn "未找到匹配人员，请尝试更完整的姓名"
                echo "MATCH_FAILED"
                exit 1
            fi
            ;;
        show)
            if [[ -f "$MEMORY_DIR/user-config.md" ]]; then
                cat "$MEMORY_DIR/user-config.md"
            else
                echo "尚未配置，请先运行配置流程"
            fi
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
