#!/bin/bash
set -e

# ============================================================================
# DolphinDB Docker 自动化部署脚本
# 功能：自动检测架构、计算内存、下载镜像、持久化数据目录
# ============================================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ============================================================================
# 1. 检测本机芯片架构
# ============================================================================
detect_architecture() {
    local ARCH=$(uname -m)
    
    case "$ARCH" in
        arm64|aarch64)
            echo "arm64"
            ;;
        x86_64|amd64)
            echo "amd64"
            ;;
        *)
            log_error "不支持的架构：$ARCH"
            exit 1
            ;;
    esac
}

# 根据架构获取镜像名称
get_image_name() {
    local ARCH="$1"
    
    if [ "$ARCH" == "arm64" ]; then
        echo "dolphindb/dolphindb-arm64"
    else
        echo "dolphindb/dolphindb"
    fi
}

# ============================================================================
# 2. 读取本机内存并计算（50% 原则）
# ============================================================================
calculate_memory() {
    local MEM_BYTES MEM_GB MEM_LIMIT
    
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        MEM_BYTES=$(sysctl -n hw.memsize)
    # Linux
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        MEM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
        MEM_BYTES=$((MEM_KB * 1024))
    else
        log_warn "未知操作系统，使用默认内存 8GB"
        echo "8"
        return
    fi
    
    # 转换为 GB
    MEM_GB=$((MEM_BYTES / 1024 / 1024 / 1024))
    
    # 50% 原则
    MEM_LIMIT=$((MEM_GB / 2))
    
    # 最小值限制（不低于 2GB）
    if [ $MEM_LIMIT -lt 2 ]; then
        MEM_LIMIT=2
    fi
    
    # 最大值限制（不高于 32GB）
    if [ $MEM_LIMIT -gt 32 ]; then
        MEM_LIMIT=32
    fi
    
    echo "$MEM_LIMIT"
}

# ============================================================================
# 3. 准备数据目录（从镜像初始化）
# ============================================================================
prepare_data_dir() {
    local DATA_DIR="$1"
    local IMAGE="$2"
    local VERSION="$3"
    
    log_info "准备数据目录：$DATA_DIR"
    
    # 检查目录是否为空
    if [ -z "$(ls -A $DATA_DIR 2>/dev/null)" ]; then
        log_info "数据目录为空，从镜像初始化..."
        
        # 创建临时容器复制文件
        local TEMP_CONTAINER="dolphindb_init_$$"
        
        docker create --name "$TEMP_CONTAINER" "${IMAGE}:${VERSION}" > /dev/null 2>&1
        
        # 复制 server 目录内容
        docker cp "${TEMP_CONTAINER}:/data/ddb/server/." "$DATA_DIR"
        
        # 删除临时容器
        docker rm "$TEMP_CONTAINER" > /dev/null 2>&1
        
        log_success "数据目录初始化完成"
    else
        log_warn "数据目录非空，跳过初始化"
    fi
    
    # 设置权限
    chmod -R 755 "$DATA_DIR"
    
    log_success "数据目录准备完成"
}

# ============================================================================
# 4. 拉取 Docker 镜像
# ============================================================================
pull_image() {
    local IMAGE="$1"
    local VERSION="$2"
    local FULL_IMAGE="${IMAGE}:${VERSION}"
    
    log_info "拉取 Docker 镜像：$FULL_IMAGE"
    
    # 检查是否已存在
    if docker image inspect "$FULL_IMAGE" > /dev/null 2>&1; then
        log_warn "镜像已存在，跳过拉取"
    else
        docker pull "$FULL_IMAGE"
    fi
    
    log_success "镜像准备完成"
}

# ============================================================================
# 5. 停止并删除旧容器
# ============================================================================
cleanup_container() {
    local CONTAINER_NAME="$1"
    
    log_info "清理旧容器：$CONTAINER_NAME"
    
    # 停止容器
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    
    # 删除容器
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    
    log_success "容器清理完成"
}

# ============================================================================
# 6. 启动 DolphinDB 容器
# ============================================================================
start_container() {
    local CONTAINER_NAME="$1"
    local HOSTNAME="$2"
    local PLATFORM="$3"
    local MEMORY="$4"
    local DATA_DIR="$5"
    local IMAGE="$6"
    local VERSION="$7"
    
    log_info "启动 DolphinDB 容器..."
    log_info "  容器名：$CONTAINER_NAME"
    log_info "  主机名：$HOSTNAME"
    log_info "  架构：$PLATFORM"
    log_info "  内存：${MEMORY}GB"
    log_info "  数据目录：$DATA_DIR"
    log_info "  镜像：${IMAGE}:${VERSION}"
    
    docker run -itd \
        --name "$CONTAINER_NAME" \
        --hostname "$HOSTNAME" \
        --platform "linux/$PLATFORM" \
        -m "${MEMORY}g" \
        -p 8848:8848 \
        -p 8849:8849 \
        -v /etc:/dolphindb/etc \
        -v "$DATA_DIR:/data/ddb/server" \
        "${IMAGE}:${VERSION}"
    
    log_success "容器启动成功"
}

# ============================================================================
# 7. 验证部署
# ============================================================================
verify_deployment() {
    local CONTAINER_NAME="$1"
    
    log_info "验证部署..."
    
    # 等待容器启动
    sleep 5
    
    # 检查容器状态
    if docker ps --filter "name=$CONTAINER_NAME" --format "{{.Status}}" | grep -q "Up"; then
        log_success "容器运行正常"
    else
        log_error "容器启动失败，查看日志："
        docker logs "$CONTAINER_NAME"
        exit 1
    fi
    
    # 检查端口
    sleep 2
    if curl -s http://localhost:8848 > /dev/null 2>&1; then
        log_success "Web UI 可访问 (http://localhost:8848)"
    else
        log_warn "Web UI 暂时无法访问，可能正在启动中"
    fi
}

# ============================================================================
# 主函数
# ============================================================================
main() {
    echo ""
    echo "============================================"
    echo "  DolphinDB Docker 自动化部署"
    echo "============================================"
    echo ""
    
    # 参数解析
    local VERSION="${1:-v2.00.7}"
    local MEMORY="${2:-}"
    local DATA_DIR="${3:-/Users/mac/Documents/dolphindb_docker_server}"
    local CONTAINER_NAME="${4:-dolphindb}"
    local HOSTNAME="${5:-cnserver10}"
    
    # 1. 检测架构
    log_info "检测本机芯片架构..."
    local ARCH=$(detect_architecture)
    
    if [ "$ARCH" == "arm64" ]; then
        log_success "检测到 ARM64 架构 (Apple Silicon)"
    else
        log_success "检测到 x86_64 架构"
    fi
    
    local IMAGE=$(get_image_name "$ARCH")
    
    # 2. 计算内存（如果未指定）
    if [ -z "$MEMORY" ]; then
        MEMORY=$(calculate_memory)
        log_success "本机内存自动计算：${MEMORY}GB (50%)"
    else
        log_success "使用指定内存：${MEMORY}GB"
    fi
    
    # 3. 拉取镜像（先拉取才能初始化数据目录）
    pull_image "$IMAGE" "$VERSION"
    
    # 4. 准备数据目录（从镜像初始化）
    prepare_data_dir "$DATA_DIR" "$IMAGE" "$VERSION"
    
    # 5. 清理旧容器
    cleanup_container "$CONTAINER_NAME"
    
    # 6. 启动容器
    start_container "$CONTAINER_NAME" "$HOSTNAME" "$ARCH" "$MEMORY" "$DATA_DIR" "$IMAGE" "$VERSION"
    
    # 7. 验证部署
    verify_deployment "$CONTAINER_NAME"
    
    echo ""
    echo "============================================"
    echo "  部署完成！"
    echo "============================================"
    echo ""
    echo "📊 部署信息:"
    echo "   架构：$ARCH"
    echo "   内存：${MEMORY}GB"
    echo "   数据目录：$DATA_DIR"
    echo "   镜像：${IMAGE}:${VERSION}"
    echo ""
    echo "🌐 访问方式:"
    echo "   Web UI: http://localhost:8848"
    echo "   Python: localhost:8848"
    echo ""
    echo "📝 常用命令:"
    echo "   docker ps --filter name=$CONTAINER_NAME"
    echo "   docker logs $CONTAINER_NAME"
    echo "   docker stop $CONTAINER_NAME"
    echo "   docker rm $CONTAINER_NAME"
    echo ""
}

# 执行主函数
main "$@"
