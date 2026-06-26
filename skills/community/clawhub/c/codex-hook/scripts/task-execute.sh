#!/bin/bash
# task-execute.sh - 改进的任务执行脚本
# 特点：
# 1. 明确指定项目路径，避免项目混淆
# 2. 自动注入项目上下文
# 3. 执行后自动迁移代码 + 更新记忆

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REGISTRY="$SCRIPT_DIR/task-registry.sh"

# 配置
WORKTREE_DIR="${WORKTREE_DIR:-$HOME/codex-worktrees}"
MEMORY_DIR="${MEMORY_DIR:-$HOME/.openclaw/workspace/memory/projects}"

usage() {
    echo "用法: $0 execute <项目名> <任务描述> [目标目录]"
    echo ""
    echo "示例:"
    echo "  $0 execute lobster-plugin '添加用户签到功能'"
    echo "  $0 execute scutum-portal '修复登录bug' /path/to/project"
    exit 1
}

# 获取项目记忆
get_project_context() {
    local project_name="$1"
    local context_file="$MEMORY_DIR/$project_name/context.md"
    
    if [[ -f "$context_file" ]]; then
        echo "📚 项目上下文:"
        cat "$context_file"
        echo ""
    else
        echo "⚠️ 未找到项目记忆: $context_file"
    fi
}

# 清理 worktree（只保留目标项目）
prepare_worktree() {
    local task_id="$1"
    local project_path="$2"
    local worktree_path="$WORKTREE_DIR/$task_id"
    
    # 创建 worktree 目录
    mkdir -p "$worktree_path"
    
    # 复制项目文件（干净复制）
    if [[ -d "$project_path" ]]; then
        # 使用 rsync 或 cp 排除 .git
        rsync -av --exclude='.git' "$project_path/" "$worktree_path/" 2>/dev/null || \
            cp -r "$project_path/." "$worktree_path/"
        echo "✅ 项目文件已复制到 worktree: $worktree_path"
    else
        echo "❌ 项目目录不存在: $project_path"
        return 1
    fi
}

# 构建带上下文的 prompt
build_prompt() {
    local project_name="$1"
    local task_desc="$2"
    local project_path="$3"
    
    local context=$(get_project_context "$project_name")
    
    cat << EOF
## 任务：$task_desc

## 项目信息
- 项目名：$project_name
- 目标目录：$project_path

$context

## 重要提醒
1. 代码必须写到当前目录，不要写到其他项目目录
2. 完成后确认所有文件都在当前 worktree 内
3. 如果需要安装依赖，先尝试安装
EOF
}

# 执行任务
execute_task() {
    local project_name="$1"
    local task_desc="$2"
    local project_path="${3:-}"
    
    # 如果未指定路径，从项目名推断
    if [[ -z "$project_path" ]]; then
        project_path="$HOME/.openclaw/workspace/projects/$project_name"
    fi
    
    # 生成任务 ID
    local task_id="task-$(date +%Y%m%d)-$(openssl rand -hex 4 2>/dev/null || echo "$$")"
    
    echo "🚀 开始任务: $task_id"
    echo "   项目: $project_name"
    echo "   任务: $task_desc"
    echo "   路径: $project_path"
    
    # 构建带上下文的 prompt
    local prompt=$(build_prompt "$project_name" "$task_desc" "$project_path")
    
# 选择 worktree 策略
# - 有关联/依赖的任务 → 复用现有 worktree
# - 独立/可并行的任务 → 新建 worktree
choose_worktree_strategy() {
    local project_name="$1"
    local task_desc="$2"
    
    # 检查是否有关键词表明是关联任务
    local关联关键词="继续|接着|在上一个|基于|修改|完善|集成|对接"
    if echo "$task_desc" | grep -qE "$关联关键词"; then
        # 复用现有 worktree
        local existing
        existing=$(ls -td "$WORKTREE_DIR"/task-$(date +%Y%m%d)-${project_name}* 2>/dev/null | head -1)
        if [[ -n "$existing" ]]; then
            echo "$existing"
            return 0
        fi
    fi
    
    # 新建 worktree
    return 1
}
    
    # 对于 lobster 项目，复用同一个 worktree
    local worktree_path="$WORKTREE_DIR/$task_id"
    if [[ "$project_name" == *"lobster"* ]] && [[ -d "$WORKTREE_DIR/task-20260313-lobster-api" ]]; then
        worktree_path="$WORKTREE_DIR/task-20260313-lobster-api"
        echo "♻️ 复用现有 worktree: $worktree_path"
    fi
    
    # 使用 acpx 执行任务（正确的流程）
    # 关键：从 worktree 目录运行，确保 session 绑定
    cd "$worktree_path"
    acpx codex sessions ensure > /dev/null 2>&1
    acpx --approve-all codex prompt "$prompt" > "/tmp/codex-results/tasks/$task_id/output.log" 2>&1 &
    
    echo "✅ 任务已派发"
    echo "   工作目录: $worktree_path"
    echo "   日志: tail -f /tmp/codex-results/tasks/$task_id/output.log"
    echo ""
    echo "任务ID: $task_id"
}

# 主命令
case "${1:-}" in
    execute)
        shift
        if [[ $# -lt 2 ]]; then
            usage
        fi
        execute_task "$@"
        ;;
    context)
        shift
        get_project_context "$1"
        ;;
    *)
        usage
        ;;
esac
