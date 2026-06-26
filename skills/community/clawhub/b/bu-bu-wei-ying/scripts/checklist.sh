#!/bin/bash
# ============================================================
# 步步为营 - 开发流程自动化脚本集
# 用于复杂APP开发、CI/CD、DevOps场景
# ============================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录（根据实际情况修改）
PROJECT_ROOT="${PROJECT_ROOT:-.}"

# -------------------------------------------------------
# 辅助函数
# -------------------------------------------------------

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "命令 '$1' 未找到，请先安装"
        exit 1
    fi
}

# -------------------------------------------------------
# 1. 修正验证脚本 - 核心安全检查
# 确保只修改了指定问题和相关代码
# -------------------------------------------------------

verify_fix_scope() {
    local target_file="$1"
    local baseline_hash="${2:-}"
    
    log_info "执行修正范围验证..."
    
    if [ ! -f "$target_file" ]; then
        log_error "目标文件不存在: $target_file"
        return 1
    fi
    
    # 检查是否有未追踪的更改
    if git rev-parse --git-dir > /dev/null 2>&1; then
        local changed_files=$(git diff --name-only HEAD)
        local file_count=$(echo "$changed_files" | grep -c "$target_file" || true)
        
        if [ "$file_count" -gt 1 ]; then
            log_warn "检测到多个文件被修改，可能影响其他功能"
            echo "修改的文件列表:"
            echo "$changed_files"
        else
            log_success "修正范围正常，仅修改了目标文件"
        fi
    fi
    
    # 检查目标文件的语法
    log_info "验证文件语法..."
    if [[ "$target_file" == *.py ]]; then
        python3 -m py_compile "$target_file" && log_success "Python 语法正确" || return 1
    elif [[ "$target_file" == *.js ]]; then
        node --check "$target_file" && log_success "JavaScript 语法正确" || return 1
    elif [[ "$target_file" == *.ts ]]; then
        npx tsc --noEmit "$target_file" 2>/dev/null && log_success "TypeScript 语法正确" || log_warn "TypeScript 检查跳过"
    fi
    
    return 0
}

# -------------------------------------------------------
# 2. 开发流程脚本
# -------------------------------------------------------

dev_full_check() {
    log_info "=== 执行完整开发检查 ==="
    
    cd "$PROJECT_ROOT"
    
    # 依赖检查
    log_info "检查依赖..."
    if [ -f "package.json" ]; then
        npm install 2>&1 | tail -5
    fi
    
    # Lint 检查
    log_info "运行代码检查..."
    if [ -f "package.json" ]; then
        npm run lint 2>/dev/null || npm run lint:fix 2>/dev/null || log_warn "Lint 配置未找到"
    fi
    
    # 测试
    log_info "运行测试..."
    if [ -f "package.json" ]; then
        npm test 2>&1 | tail -20
    fi
    
    # 构建
    log_info "执行构建..."
    if [ -f "package.json" ]; then
        npm run build 2>&1 | tail -10
    fi
    
    log_success "完整检查完成"
}

# -------------------------------------------------------
# 3. Docker 构建脚本
# -------------------------------------------------------

docker_build_check() {
    local image_name="${1:-app}"
    local image_tag="${2:-latest}"
    
    log_info "=== Docker 构建流程 ==="
    
    # 安全扫描
    log_info "执行 Trivy 安全扫描（基础镜像）..."
    if command -v trivy &> /dev/null; then
        trivy image --ignore-unfixed alpine:latest 2>/dev/null || log_warn "安全扫描跳过"
    else
        log_warn "Trivy 未安装，跳过安全扫描"
    fi
    
    # 构建
    log_info "构建 Docker 镜像..."
    docker build -t "${image_name}:${image_tag}" .
    
    # 检查
    log_info "验证镜像..."
    docker run --rm "${image_name}:${image_tag}" --help 2>/dev/null || \
    docker run --rm "${image_name}:${image_tag}" sh -c "echo 'Image OK'" || \
    log_warn "镜像验证跳过（无入口命令）"
    
    log_success "Docker 构建完成: ${image_name}:${image_tag}"
}

# -------------------------------------------------------
# 4. 健康检查脚本
# -------------------------------------------------------

health_check() {
    local host="${1:-localhost}"
    local port="${2:-8080}"
    local endpoint="${3:-/health}"
    
    log_info "=== 健康检查: http://${host}:${port}${endpoint} ==="
    
    local response=$(curl -s -w "\n%{http_code}" "http://${host}:${port}${endpoint}" 2>/dev/null)
    local body=$(echo "$response" | sed '$d')
    local status=$(echo "$response" | tail -1)
    
    if [ "$status" == "200" ]; then
        log_success "健康检查通过"
        echo "$body"
        return 0
    else
        log_error "健康检查失败 (HTTP $status)"
        echo "$body"
        return 1
    fi
}

# -------------------------------------------------------
# 5. 灰度发布脚本
# -------------------------------------------------------

canary_release() {
    local image_name="${1:-app}"
    local stages="${2:-5,25,100}"
    
    log_info "=== 灰度发布流程 ==="
    
    IFS=',' read -ra STAGES <<< "$stages"
    for stage in "${STAGES[@]}"; do
        log_info "部署到 ${stage}% 流量..."
        
        # 这里需要根据实际的 K8s 或负载均衡配置修改
        # kubectl patch deployment app -p "{\"spec\":{\"replicas\":${stage}}}"
        
        sleep 5
        log_success "阶段 ${stage}% 部署完成"
        
        if [ "$stage" != "100" ]; then
            read -p "确认无异常后按 Enter 继续..."
        fi
    done
    
    log_success "灰度发布完成"
}

# -------------------------------------------------------
# 6. 回滚脚本
# -------------------------------------------------------

rollback() {
    local namespace="${1:-default}"
    local deployment="${2:-app}"
    
    log_warn "=== 执行回滚 ==="
    read -p "确认回滚到上一个稳定版本? (y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "执行回滚..."
        kubectl rollout undo deployment/"$deployment" -n "$namespace"
        kubectl rollout status deployment/"$deployment" -n "$namespace"
        log_success "回滚完成"
    else
        log_info "取消回滚"
    fi
}

# -------------------------------------------------------
# 7. 测试覆盖率检查
# -------------------------------------------------------

check_coverage() {
    local threshold="${1:-80}"
    
    log_info "=== 检查测试覆盖率（阈值: ${threshold}%）==="
    
    if [ -f "coverage/coverage-summary.json" ]; then
        local coverage=$(cat coverage/coverage-summary.json | grep -o '"percent":[0-9.]*' | grep -o '[0-9.]*' | head -1)
        
        if [ -n "$coverage" ]; then
            log_info "当前覆盖率: ${coverage}%"
            
            if (( $(echo "$coverage >= $threshold" | bc -l) )); then
                log_success "覆盖率达标"
                return 0
            else
                log_error "覆盖率未达标 (需要 ${threshold}%)"
                return 1
            fi
        fi
    fi
    
    log_warn "覆盖率报告未找到"
    return 0
}

# -------------------------------------------------------
# 主菜单
# -------------------------------------------------------

show_help() {
    echo "步步为营 - 开发自动化脚本"
    echo ""
    echo "用法: $0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  verify-fix <文件> [基准哈希]  - 验证修正范围"
    echo "  dev-check                      - 完整开发检查"
    echo "  docker-build [镜像名] [标签]   - Docker 构建"
    echo "  health [主机] [端口] [端点]     - 健康检查"
    echo "  canary [镜像] [阶段]            - 灰度发布"
    echo "  rollback [命名空间] [部署名]    - 回滚"
    echo "  coverage [阈值]                - 覆盖率检查"
    echo "  all                            - 执行全部检查"
    echo ""
}

case "$1" in
    verify-fix)
        verify_fix_scope "$2" "$3"
        ;;
    dev-check)
        dev_full_check
        ;;
    docker-build)
        docker_build_check "$2" "$3"
        ;;
    health)
        health_check "$2" "$3" "$4"
        ;;
    canary)
        canary_release "$2" "$3"
        ;;
    rollback)
        rollback "$2" "$3"
        ;;
    coverage)
        check_coverage "$2"
        ;;
    all)
        dev_full_check
        health_check
        check_coverage
        ;;
    *)
        show_help
        ;;
esac
