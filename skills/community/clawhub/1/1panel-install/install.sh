#!/bin/bash

################################################################################
# 1Panel 一键安装脚本
# 用途：检查是否已安装 1Panel，未安装则自动安装，已安装则显示信息
# 版本：1.0.0
# 日期：2025-03-13
################################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
INSTALL_DIR="/opt"
TAR_DIR="/root/.openclaw/workspace/1panel-v2.1.4-linux-amd64"
TAR_FILE="/root/.openclaw/workspace/1panel-v2.1.4-linux-amd64.tar.gz"
ONEDRIVE_URL="https://resource.fit2cloud.com/1panel/package/v2/stable/v2.1.4/release/1panel-v2.1.4-linux-amd64.tar.gz"
VERSION="v2.1.4"

################################################################################
# 函数定义
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "此脚本需要 root 权限运行，请使用 sudo"
        exit 1
    fi
}

check_1panel_installed() {
    if command -v 1pctl &> /dev/null; then
        return 0  # 已安装
    else
        return 1  # 未安装
    fi
}

show_1panel_info() {
    log_info "1Panel 已安装，获取面板信息..."
    echo ""
    if command -v 1pctl &> /dev/null; then
        1pctl user-info
        return 0
    else
        log_error "1pctl 命令未找到，安装可能不完整"
        return 1
    fi
}

download_install_package() {
    local retry_count=3
    local retry_delay=2
    
    if [[ -d "$TAR_DIR" ]]; then
        log_info "安装包已存在，跳过下载"
        return 0
    fi
    
    log_info "正在下载 1Panel $VERSION 安装包..."
    
    for i in $(seq 1 $retry_count); do
        if curl -fSL --retry 3 --retry-delay $retry_delay "$ONEDRIVE_URL" -o "$TAR_FILE"; then
            log_success "下载完成"
            break
        else
            if [[ $i -lt $retry_count ]]; then
                log_warning "下载失败，第 $i 次重试..."
                sleep $retry_delay
            else
                log_error "下载失败，请检查网络连接"
                return 1
            fi
        fi
    done
    
    # 解压
    log_info "正在解压安装包..."
    if tar -xzf "$TAR_FILE" -C /root/.openclaw/workspace/; then
        log_success "解压完成"
        return 0
    else
        log_error "解压失败，安装包可能损坏"
        return 1
    fi
}

run_install_script() {
    log_info "开始安装 1Panel..."
    log_info "安装路径: $INSTALL_DIR (默认)"
    log_info "是否安装 Docker: 否"
    log_info "语言: 中文"
    echo ""
    
    cd "$TAR_DIR"
    
    # 使用 heredoc 自动输入安装选项
    # 选项顺序：
    # 2 - 选择中文
    # (回车) - 使用默认路径 /opt
    # n - 不安装 Docker
    if echo -e "2\n\nn" | ./install.sh; then
        log_success "安装脚本执行完成"
        return 0
    else
        log_error "安装脚本执行失败"
        return 1
    fi
}

wait_for_service() {
    local max_wait=30
    local waited=0
    local interval=2
    
    log_info "等待 1Panel 服务启动..."
    
    while [[ $waited -lt $max_wait ]]; do
        if systemctl is-active --quiet 1panel-core 2>/dev/null; then
            log_success "1Panel 服务已启动"
            sleep 2  # 再等两秒确保完全就绪
            return 0
        fi
        sleep $interval
        waited=$((waited + interval))
    done
    
    log_warning "服务启动超时，但可能已启动，继续检查..."
    return 0
}

################################################################################
# 主程序
################################################################################

main() {
    echo ""
    echo "=========================================="
    echo "   1Panel 一键安装工具"
    echo "=========================================="
    echo ""
    
    # 检查 root 权限
    check_root
    
    # 检查是否已安装
    if check_1panel_installed; then
        log_info "检测到 1Panel 已安装"
        show_1panel_info
        exit 0
    fi
    
    # 未安装，开始安装流程
    log_info "未检测到 1Panel，开始安装..."
    echo ""
    
    # 下载安装包
    if ! download_install_package; then
        exit 1
    fi
    
    # 运行安装脚本
    if ! run_install_script; then
        log_error "安装失败，请检查日志"
        exit 1
    fi
    
    # 等待服务启动
    wait_for_service
    
    # 显示安装信息
    echo ""
    log_success "1Panel 安装完成！"
    echo ""
    show_1panel_info
    
    echo ""
    log_warning "安全提醒："
    log_warning "1. 请立即修改面板密码：1pctl update password"
    log_warning "2. 如果使用云服务器，请在安全组中打开对应端口"
    log_warning "3. 建议定期更新系统和 1Panel"
    echo ""
    
    log_info "访问提示："
    log_info "如果地址无法访问，或者服务器没有公网 IP，"
    log_info "推荐使用 Cloudflare Tunnel 功能配置域名访问，实现安全的内网穿透。"
    echo ""
}

main "$@"
