#!/bin/bash
#
# 实时协作支持工具 - 多开发者协作管理
#
# 用法: bash scripts/sync.sh <命令> [选项]
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️${NC}  $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
step() { echo -e "${CYAN}▶ $1${NC}"; }

SYNC_STATE_FILE=".sync-state"

# 显示帮助
show_help() {
    echo "实时协作支持工具 (v2.0)"
    echo ""
    echo "用法: bash scripts/sync.sh <命令>"
    echo ""
    echo "命令:"
    echo "  status              查看同步状态"
    echo "  check               检查冲突风险"
    echo "  suggest             获取合并建议"
    echo "  lock <file>         锁定文件（防止冲突）"
    echo "  unlock <file>       解锁文件"
    echo "  share <file>        标记文件为共享编辑"
    echo "  report              生成协作报告"
    echo ""
    echo "选项:"
    echo "  --branch=<name>     指定分支"
    echo "  --remote=<name>     指定远程 (默认: origin)"
    echo ""
}

# 检查 git 仓库
check_git() {
    if [ ! -d ".git" ]; then
        error "当前目录不是 Git 仓库"
        exit 1
    fi
}

# 获取当前状态
cmd_status() {
    step "检查协作状态..."
    check_git

    local branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    local remote=$(git remote get-url origin 2>/dev/null || echo "none")

    echo ""
    echo "📊 仓库状态"
    echo "==========="
    echo "当前分支: $branch"
    echo "远程仓库: $remote"
    echo ""

    # 检查未提交的更改
    local uncommitted=$(git status --short | wc -l)
    if [ "$uncommitted" -gt 0 ]; then
        warn "未提交更改: $uncommitted 个文件"
        git status --short | head -10
    else
        success "工作区干净"
    fi

    echo ""

    # 检查与远程的差异
    git fetch --quiet 2>/dev/null || true

    local ahead=$(git rev-list --count HEAD..@{upstream} 2>/dev/null || echo 0)
    local behind=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo 0)

    if [ "$ahead" -gt 0 ]; then
        warn "落后远程 $ahead 个提交"
        info "建议运行: git pull"
    elif [ "$behind" -gt 0 ]; then
        info "领先远程 $behind 个提交"
        info "建议运行: git push"
    else
        success "与远程同步"
    fi

    echo ""

    # 显示最近提交
    echo "📜 最近提交:"
    git log --oneline -5 2>/dev/null || echo "无提交历史"
}

# 检查冲突风险
cmd_check() {
    step "检查冲突风险..."
    check_git

    # 获取当前修改的文件
    local modified_files=$(git diff --name-only 2>/dev/null || true)

    if [ -z "$modified_files" ]; then
        info "没有本地修改"
        return 0
    fi

    echo ""
    echo "🔍 冲突风险分析"
    echo "==============="
    echo ""

    # 检查远程是否有相同文件的修改
    local conflicts_risk=()

    for file in $modified_files; do
        # 检查远程是否有更新
        if git log --oneline HEAD..@{upstream} -- "$file" 2>/dev/null | grep -q .; then
            conflicts_risk+=("$file")
        fi
    done

    if [ ${#conflicts_risk[@]} -eq 0 ]; then
        success "✅ 低冲突风险"
        info "远程没有修改您正在编辑的文件"
    else
        warn "⚠️  检测到潜在冲突风险"
        echo ""
        echo "以下文件远程有更新:"
        for file in "${conflicts_risk[@]}"; do
            echo "  - $file"
        done
        echo ""
        echo "建议操作:"
        echo "  1. 先提交当前更改: git commit -am '保存进度'"
        echo "  2. 拉取远程更新: git pull --rebase"
        echo "  3. 解决可能的冲突"
    fi
}

# 合并建议
cmd_suggest() {
    step "分析合并策略..."
    check_git

    local branch=$(git branch --show-current)
    local has_changes=$(git status --porcelain | wc -l)

    echo ""
    echo "💡 合并建议"
    echo "==========="
    echo ""

    if [ "$has_changes" -gt 0 ]; then
        echo "1. 保存当前工作"
        echo "   git add ."
        echo "   git commit -m 'WIP: 保存工作进度'"
        echo ""
    fi

    echo "2. 获取远程更新"
    echo "   git fetch origin"
    echo ""

    echo "3. 查看差异"
    echo "   git log HEAD..origin/$branch --oneline"
    echo ""

    echo "4. 选择合并策略:"
    echo ""

    # 检查是否有合并冲突历史
    local conflict_count=$(git log --merge 2>/dev/null | wc -l || echo 0)

    if [ "$conflict_count" -gt 0 ]; then
        echo "   A) 使用 rebase (推荐用于特性分支)"
        echo "      git pull --rebase origin $branch"
        echo ""
        echo "   B) 使用 merge (保留完整历史)"
        echo "      git pull origin $branch"
        echo ""
        echo "   C) 使用 cherry-pick (精确控制)"
        echo "      git cherry-pick <commit-hash>"
    else
        echo "   推荐: git pull --rebase origin $branch"
    fi

    echo ""
    echo "5. 冲突解决后"
    echo "   git rebase --continue"
    echo "   git push origin $branch"
}

# 文件锁定
cmd_lock() {
    local file="$1"
    if [ -z "$file" ]; then
        error "请指定要锁定的文件"
        exit 1
    fi

    if [ ! -f "$file" ]; then
        error "文件不存在: $file"
        exit 1
    fi

    step "锁定文件: $file"

    # 创建锁定标记
    local lock_file=".sync-locks/$(echo "$file" | tr '/' '_').lock"
    mkdir -p ".sync-locks"

    if [ -f "$lock_file" ]; then
        local locker=$(cat "$lock_file")
        if [ "$locker" != "$(whoami)" ]; then
            error "文件已被 $locker 锁定"
            exit 1
        fi
        warn "文件已被您锁定"
        return 0
    fi

    echo "$(whoami)@$(hostname) $(date)" > "$lock_file"
    success "文件已锁定"
    info "编辑完成后请运行: bash scripts/sync.sh unlock $file"
}

# 文件解锁
cmd_unlock() {
    local file="$1"
    if [ -z "$file" ]; then
        error "请指定要解锁的文件"
        exit 1
    fi

    local lock_file=".sync-locks/$(echo "$file" | tr '/' '_').lock"

    if [ ! -f "$lock_file" ]; then
        warn "文件未被锁定"
        return 0
    fi

    rm -f "$lock_file"
    success "文件已解锁: $file"
}

# 标记共享编辑
cmd_share() {
    local file="$1"
    if [ -z "$file" ]; then
        error "请指定要共享的文件"
        exit 1
    fi

    step "标记共享编辑: $file"

    # 添加到 .gitattributes 标记为可合并
    if [ -f ".gitattributes" ]; then
        if ! grep -q "$file merge=union" ".gitattributes"; then
            echo "$file merge=union" >> ".gitattributes"
        fi
    else
        echo "$file merge=union" > ".gitattributes"
    fi

    success "已标记为共享编辑模式"
    info "合并时将尝试自动合并内容"
}

# 生成协作报告
cmd_report() {
    step "生成协作报告..."
    check_git

    local report_file="docs/reports/collaboration-$(date +%Y%m%d).md"
    mkdir -p "docs/reports"

    cat > "$report_file" << EOF
# 🤝 协作报告

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 📊 仓库统计

### 提交统计
\`\`\`
$(git shortlog -sn --no-merges 2>/dev/null | head -10 || echo "无数据")
\`\`\`

### 最近活动
\`\`\`
$(git log --oneline --graph -10 2>/dev/null || echo "无提交历史")
\`\`\`

### 分支列表
\`\`\`
$(git branch -a 2>/dev/null || echo "无分支")
\`\`\`

## 📁 文件变更统计

| 文件 | 变更次数 |
|------|---------|
$(git log --pretty=format: --name-only 2>/dev/null | sort | uniq -c | sort -rg | head -10 | awk '{print "| " $2 " | " $1 " |"}' || echo "| 无数据 | - |")

## ⚠️ 潜在问题

$(if [ -d ".sync-locks" ]; then
    echo "### 当前锁定的文件"
    echo ""
    for lock in .sync-locks/*.lock 2>/dev/null; do
        if [ -f "$lock" ]; then
            local file=$(basename "$lock" .lock | tr '_' '/')
            local info=$(cat "$lock")
            echo "- $file (锁定者: $info)"
        fi
    done
else
    echo "无锁定文件"
fi)

---

*报告由 sync.sh 自动生成*
EOF

    success "协作报告已生成: $report_file"
}

# 主函数
main() {
    local cmd="${1:-status}"
    shift || true

    case "$cmd" in
        status)
            cmd_status
            ;;
        check)
            cmd_check
            ;;
        suggest)
            cmd_suggest
            ;;
        lock)
            cmd_lock "$1"
            ;;
        unlock)
            cmd_unlock "$1"
            ;;
        share)
            cmd_share "$1"
            ;;
        report)
            cmd_report
            ;;
        --help|-h)
            show_help
            ;;
        *)
            error "未知命令: $cmd"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
