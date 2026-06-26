#!/bin/bash
#
# Git Hooks 设置工具 - 安装预提交检查
#
# 用法: bash scripts/setup-hooks.sh [选项]
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

HOOKS_DIR=".git/hooks"
SCRIPTS_DIR="scripts/hooks"

# 显示帮助
show_help() {
    echo "Git Hooks 设置工具"
    echo ""
    echo "用法: bash scripts/setup-hooks.sh <命令>"
    echo ""
    echo "命令:"
    echo "  install    安装 hooks"
    echo "  uninstall  卸载 hooks"
    echo "  status     查看 hooks 状态"
    echo "  test       测试 hooks"
    echo ""
}

# 检查是否在 git 仓库中
check_git_repo() {
    if [ ! -d ".git" ]; then
        error "当前目录不是 Git 仓库"
        info "请先运行: git init"
        exit 1
    fi
}

# 创建 hooks 脚本
create_precommit_hook() {
    mkdir -p "$HOOKS_DIR"

    cat > "$HOOKS_DIR/pre-commit" << 'HOOK_EOF'
#!/bin/bash
#
# Pre-commit Hook - 提交前自动检查
#

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️${NC}  $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $1"; }
error() { echo -e "${RED}❌${NC} $1"; }

exit_code=0

echo "═══════════════════════════════════════════════════"
echo "  🔍 Pre-commit 检查"
echo "═══════════════════════════════════════════════════"
echo ""

# 1. 检查是否有 TODO 标记在 staged 文件中
info "1/5 检查待办事项标记..."
staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|ets)$' || true)
if [ -n "$staged_files" ]; then
    todo_count=0
    for file in $staged_files; do
        if [ -f "$file" ]; then
            count=$(grep -c "\[TODO\]" "$file" 2>/dev/null || echo 0)
            todo_count=$((todo_count + count))
        fi
    done

    if [ "$todo_count" -gt 0 ]; then
        warn "发现 $todo_count 个 [TODO] 标记"
        echo ""
        for file in $staged_files; do
            if [ -f "$file" ]; then
                grep -n "\[TODO\]" "$file" 2>/dev/null | while read -r line; do
                    echo "   $file: $line"
                done
            fi
        done
        echo ""
        read -p "是否继续提交? (y/N): " continue
        if [[ ! $continue =~ ^[Yy]$ ]]; then
            error "提交已取消"
            exit 1
        fi
    else
        success "没有 TODO 标记"
    fi
else
    info "没有 TypeScript/ArkTS 文件被暂存"
fi

# 2. 代码规范检查
info "2/5 代码规范检查..."
if [ -f "scripts/lint.sh" ]; then
    if bash scripts/lint.sh --staged 2>/dev/null; then
        success "规范检查通过"
    else
        warn "规范检查发现问题"
        read -p "是否继续提交? (y/N): " continue
        if [[ ! $continue =~ ^[Yy]$ ]]; then
            error "提交已取消"
            info "运行 'bash scripts/quick.sh fix' 自动修复"
            exit 1
        fi
    fi
else
    info "未配置 lint 脚本"
fi

# 3. 编译检查
info "3/5 编译检查..."
if [ -f "scripts/build-check.sh" ]; then
    if bash scripts/build-check.sh 2>/dev/null; then
        success "编译检查通过"
    else
        error "编译检查失败"
        read -p "是否强制继续? (y/N): " continue
        if [[ ! $continue =~ ^[Yy]$ ]]; then
            exit 1
        fi
        exit_code=1
    fi
else
    info "未配置编译检查脚本"
fi

# 4. 测试检查
info "4/5 运行相关测试..."
if [ -d "test" ]; then
    # 获取被修改的文件对应的服务
    changed_services=""
    for file in $staged_files; do
        if [[ $file =~ services/([^/]+)\.ts$ ]]; then
            service="${BASH_REMATCH[1]}"
            changed_services="$changed_services $service"
        fi
    done

    if [ -n "$changed_services" ]; then
        info "检测到服务变更: $changed_services"
        for service in $changed_services; do
            test_file="test/unittest/${service}.test.ts"
            if [ -f "$test_file" ]; then
                info "运行测试: $test_file"
                # 这里可以添加实际的测试命令
                # hcp test $test_file
            fi
        done
    fi
    success "测试检查完成"
else
    info "未配置测试目录"
fi

# 5. 敏感信息检查
info "5/5 敏感信息检查..."
forbidden_patterns=("password" "secret" "token" "key" "api_key" "private_key")
staged_content=$(git diff --cached --name-only)
found_sensitive=false

for pattern in "${forbidden_patterns[@]}"; do
    if echo "$staged_content" | xargs grep -l "$pattern=" 2>/dev/null; then
        warn "可能包含敏感信息: $pattern"
        found_sensitive=true
    fi
done

if [ "$found_sensitive" = true ]; then
    read -p "确认不包含敏感信息后继续? (y/N): " continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        error "提交已取消"
        exit 1
    fi
else
    success "未发现明显敏感信息"
fi

echo ""
echo "═══════════════════════════════════════════════════"
if [ $exit_code -eq 0 ]; then
    success "✅ Pre-commit 检查通过"
else
    warn "⚠️  Pre-commit 检查完成 (有警告)"
fi
echo "═══════════════════════════════════════════════════"
echo ""

exit $exit_code
HOOK_EOF

    chmod +x "$HOOKS_DIR/pre-commit"
    success "pre-commit hook 已创建"
}

# 创建 commit-msg hook
create_commitmsg_hook() {
    cat > "$HOOK_DIR/commit-msg" << 'HOOK_EOF'
#!/bin/bash
#
# Commit-msg Hook - 提交信息规范检查
#

commit_msg_file=$1
commit_msg=$(head -n1 "$commit_msg_file")

# 提交信息格式检查
# 格式: <type>: <subject>
# type: feat|fix|docs|style|refactor|test|chore

valid_types="feat|fix|docs|style|refactor|test|chore|perf|ci|build"

if ! echo "$commit_msg" | grep -qE "^($valid_types)(\(.+\))?: .+"; then
    echo "❌ 提交信息格式不正确"
    echo ""
    echo "格式: <type>: <subject>"
    echo "或:   <type>(scope): <subject>"
    echo ""
    echo "类型:"
    echo "  feat     - 新功能"
    echo "  fix      - 修复"
    echo "  docs     - 文档"
    echo "  style    - 格式"
    echo "  refactor - 重构"
    echo "  test     - 测试"
    echo "  chore    - 构建/工具"
    echo "  perf     - 性能"
    echo "  ci       - CI/CD"
    echo "  build    - 构建"
    echo ""
    echo "示例:"
    echo "  feat: 添加用户登录功能"
    echo "  fix(auth): 修复 token 过期问题"
    exit 1
fi

# 检查长度
if [ ${#commit_msg} -gt 72 ]; then
    echo "⚠️ 提交信息长度超过 72 字符，建议精简"
fi

exit 0
HOOK_EOF

    chmod +x "$HOOKS_DIR/commit-msg"
    success "commit-msg hook 已创建"
}

# 创建 pre-push hook
create_prepush_hook() {
    cat > "$HOOKS_DIR/pre-push" << 'HOOK_EOF'
#!/bin/bash
#
# Pre-push Hook - 推送前检查
#

echo "🔍 Pre-push 检查..."
echo ""

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo "❌ 有未提交的更改，请先提交或暂存"
    exit 1
fi

# 运行完整测试套件
if [ -f "scripts/quick.sh" ]; then
    echo "运行健康检查..."
    bash scripts/quick.sh health || true
fi

echo "✅ Pre-push 检查通过"
exit 0
HOOK_EOF

    chmod +x "$HOOKS_DIR/pre-push"
    success "pre-push hook 已创建"
}

# 安装 hooks
install_hooks() {
    step "安装 Git Hooks..."
    check_git_repo

    create_precommit_hook
    create_commitmsg_hook
    create_prepush_hook

    echo ""
    success "Hooks 安装完成！"
    info "已启用:"
    info "  - pre-commit: 提交前自动检查"
    info "  - commit-msg: 提交信息规范检查"
    info "  - pre-push: 推送前完整检查"
}

# 卸载 hooks
uninstall_hooks() {
    step "卸载 Git Hooks..."
    check_git_repo

    rm -f "$HOOKS_DIR/pre-commit"
    rm -f "$HOOKS_DIR/commit-msg"
    rm -f "$HOOKS_DIR/pre-push"

    success "Hooks 已卸载"
}

# 查看状态
show_status() {
    step "Git Hooks 状态"
    check_git_repo

    echo ""
    echo "已安装的 Hooks:"
    echo "==============="

    for hook in pre-commit commit-msg pre-push; do
        if [ -f "$HOOKS_DIR/$hook" ]; then
            success "$hook - 已安装"
        else
            info "$hook - 未安装"
        fi
    done

    echo ""
    echo "项目检查:"
    echo "========="
    if [ -f "scripts/build-check.sh" ]; then
        success "build-check.sh - 存在"
    else
        warn "build-check.sh - 不存在"
    fi

    if [ -f "scripts/lint.sh" ]; then
        success "lint.sh - 存在"
    else
        warn "lint.sh - 不存在"
    fi
}

# 测试 hooks
test_hooks() {
    step "测试 Hooks..."
    check_git_repo

    # 创建一个临时测试文件
    test_file=".hook-test-$(date +%s).txt"
    echo "test" > "$test_file"
    git add "$test_file"

    echo ""
    info "正在测试 pre-commit hook..."
    if bash "$HOOKS_DIR/pre-commit" 2>&1; then
        success "pre-commit 测试通过"
    else
        error "pre-commit 测试失败"
    fi

    # 清理
    git reset HEAD "$test_file" > /dev/null 2>&1
    rm -f "$test_file"
}

# 主函数
main() {
    local cmd="${1:-install}"

    case "$cmd" in
        install)
            install_hooks
            ;;
        uninstall)
            uninstall_hooks
            ;;
        status)
            show_status
            ;;
        test)
            test_hooks
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
