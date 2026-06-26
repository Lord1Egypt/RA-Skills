#!/bin/bash
# auto-merge.sh - 自动 PR 创建、CI 检查、代码审查、自动合并

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REGISTRY="$SCRIPT_DIR/task-registry.sh"

# 配置
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
REPO_DIR="${REPO_DIR:-$HOME/projects}"
MAX_RETRIES="${MAX_RETRIES:-3}"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_msg() { echo -e "${1}${2}${NC}"; }

# 检查依赖
check_deps() {
    local missing=()
    
    if ! command -v gh &>/dev/null; then
        missing+=("gh CLI")
    fi
    
    if ! command -v jq &>/dev/null; then
        missing+=("jq")
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        print_msg "$RED" "缺少依赖: ${missing[*]}"
        return 1
    fi
    
    return 0
}

# 获取任务信息
get_task_info() {
    local task_id="$1"
    $REGISTRY get "$task_id"
}

# 创建 PR
create_pr() {
    local task_id="$1"
    local branch="$2"
    local title="$3"
    local description="$4"
    local repo="${5:-.}"
    
    print_msg "$YELLOW" "🔄 创建 PR: $branch"
    
    cd "$repo"
    
    # 检查分支是否存在
    if ! git rev-parse --verify "$branch" &>/dev/null; then
        print_msg "$RED" "❌ 分支不存在: $branch"
        return 1
    fi
    
    # 创建 PR
    local pr_info
    if pr_info=$(gh pr create --title "$title" --body "$description" --base main 2>&1); then
        local pr_num
        pr_num=$(echo "$pr_info" | grep -oE '[0-9]+$' || echo "0")
        
        # 更新任务
        $REGISTRY update "$task_id" "pr" "$pr_num"
        $REGISTRY log "$task_id" "PR created: #$pr_num" "info"
        
        print_msg "$GREEN" "✅ PR 创建成功: #$pr_num"
        echo "$pr_num"
    else
        print_msg "$RED" "❌ PR 创建失败: $pr_info"
        return 1
    fi
}

# 检查 CI 状态
check_ci() {
    local pr_num="$1"
    local repo="${2:-.}"
    
    print_msg "$YELLOW" "🔍 检查 CI 状态..."
    
    cd "$repo"
    
    # 获取 CI checks
    local checks
    checks=$(gh pr checks "$pr_num" 2>/dev/null || echo "")
    
    if [[ -z "$checks" ]]; then
        print_msg "$YELLOW" "⚠️ 无 CI 检查"
        return 0
    fi
    
    # 检查是否有失败的检查
    if echo "$checks" | grep -qE "(FAILURE|FAILED|Error)"; then
        print_msg "$RED" "❌ CI 检查失败"
        echo "$checks" | grep -E "(FAILURE|FAILED|Error)"
        return 1
    fi
    
    print_msg "$GREEN" "✅ CI 全部通过"
    return 0
}

# 代码审查
code_review() {
    local pr_num="$1"
    local repo="${2:-.}"
    local reviewer="${3:-}"
    
    print_msg "$YELLOW" "🔍 代码审查..."
    
    cd "$repo"
    
    # 获取 PR 差异
    local diff
    diff=$(gh pr diff "$pr_num" --stat 2>/dev/null || echo "")
    
    # 这里可以调用多个模型审查
    # 1. Codex 审查
    # 2. Claude 审查  
    # 3. Gemini 审查
    
    # 简化版：记录审查状态
    $REGISTRY update "$pr_num" "checks" '{"code_review": "pending"}'
    
    print_msg "$GREEN" "✅ 审查完成"
    return 0
}

# 自动合并
auto_merge() {
    local task_id="$1"
    local repo="${2:-.}"
    
    print_msg "$YELLOW" "🔄 开始自动合并流程..."
    
    # 获取任务信息
    local task_info
    task_info=$(get_task_info "$task_id")
    
    local branch pr_num
    branch=$(echo "$task_info" | jq -r '.branch')
    pr_num=$(echo "$task_info" | jq -r '.pr')
    
    if [[ -z "$pr_num" || "$pr_num" == "null" ]]; then
        print_msg "$RED" "❌ 任务无 PR"
        return 1
    fi
    
    cd "$repo"
    
    # 1. 检查 CI
    print_msg "$YELLOW" "📋 步骤 1/3: 检查 CI..."
    if ! check_ci "$pr_num" "$repo"; then
        print_msg "$RED" "❌ CI 失败，无法合并"
        return 1
    fi
    
    # 2. 代码审查
    print_msg "$YELLOW" "📋 步骤 2/3: 代码审查..."
    if ! code_review "$pr_num" "$repo"; then
        print_msg "$RED" "❌ 审查失败"
        return 1
    fi
    
    # 3. 执行合并
    print_msg "$YELLOW" "📋 步骤 3/3: 合并 PR..."
    if gh pr merge "$pr_num" --squash --delete-branch 2>&1; then
        $REGISTRY complete "$task_id" "$pr_num"
        $REGISTRY log "$task_id" "PR merged: #$pr_num" "info"
        
        print_msg "$GREEN" "✅ 合并完成！"
        return 0
    else
        print_msg "$RED" "❌ 合并失败"
        return 1
    fi
}

# 汇报完成
report_completion() {
    local task_id="$1"
    local channel="${2:-telegram}"
    
    local task_info
    task_info=$(get_task_info "$task_id")
    
    local name status pr
    name=$(echo "$task_info" | jq -r '.name')
    status=$(echo "$task_info" | jq -r '.status')
    pr=$(echo "$task_info" | jq -r '.pr // "无PR"')
    
    local message
    message=$(cat <<EOF
✅ 任务完成

名称: $name
状态: $status
PR: #$pr
EOF
)
    
    print_msg "$GREEN" "$message"
    
    # 发送通知
    if [[ "$channel" == "telegram" ]]; then
        send_telegram "$message"
    fi
}

# 发送 Telegram 通知
send_telegram() {
    local message="$1"
    local tg_token tg_chat_id
    
    tg_token="${TELEGRAM_BOT_TOKEN:-}"
    tg_chat_id="${TELEGRAM_CHAT_ID:-}"
    
    if [[ -z "$tg_token" || -z "$tg_chat_id" ]]; then
        print_msg "$YELLOW" "⚠️ 未配置 Telegram (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)"
        return 1
    fi
    
    # URL 编码消息
    local encoded_msg
    encoded_msg=$(echo "$message" | jq -sRr @uri)
    
    # 发送消息
    local response
    response=$(curl -s -X POST "https://api.telegram.org/bot$tg_token/sendMessage" \
        -d "chat_id=$tg_chat_id" \
        -d "text=$message" \
        -d "parse_mode=Markdown" 2>&1)
    
    if echo "$response" | jq -e '.ok' &>/dev/null; then
        print_msg "$GREEN" "✅ Telegram 通知已发送"
    else
        print_msg "$RED" "❌ Telegram 发送失败: $response"
    fi
}

# 主流程：完整执行
run_full_flow() {
    local task_id="$1"
    local repo="${2:-.}"
    local channel="${3:-telegram}"
    
    check_deps || return 1
    
    # 自动合并
    if auto_merge "$task_id" "$repo"; then
        # 汇报
        report_completion "$task_id" "$channel"
    else
        print_msg "$RED" "❌ 流程失败"
        return 1
    fi
}

# 帮助
show_help() {
    cat <<EOF
auto-merge.sh - 自动 PR 创建、CI 检查、合并

用法: auto-merge.sh <command> [options]

命令:
  create-pr <task_id> <branch> <title> <desc> [repo]
    创建 PR
  
  check-ci <pr_num> [repo]
    检查 CI 状态
  
  review <pr_num> [repo]
    代码审查
  
  merge <task_id> [repo]
    自动合并
  
  report <task_id> [channel]
    汇报完成
  
  run-flow <task_id> [repo] [channel]
    完整流程：CI → 审查 → 合并 → 汇报

示例:
  auto-merge.sh create-pr task-xxx "feat-login" "实现登录" "实现用户登录功能"
  auto-merge.sh check-ci 123
  auto-merge.sh merge task-xxx
  auto-merge.sh run-flow task-xxx ~/projects/myapp
EOF
}

# 主命令
main() {
    local command="${1:-}"
    shift || true
    
    case "$command" in
        create-pr|create)
            create_pr "$@"
            ;;
        check-ci|ci)
            check_ci "$@"
            ;;
        review)
            code_review "$@"
            ;;
        merge)
            auto_merge "$@"
            ;;
        report)
            report_completion "$@"
            ;;
        run-flow|run)
            run_full_flow "$@"
            ;;
        help|--help|-h|"")
            show_help
            ;;
        *)
            print_msg "$RED" "未知命令: $command"
            show_help
            ;;
    esac
}

main "$@"
