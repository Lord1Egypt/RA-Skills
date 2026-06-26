#!/bin/bash
# 服务器环境安装脚本
# 用法：在服务器上执行 ./install-env.sh

set -e

echo "========================================"
echo "  服务器环境安装脚本"
echo "========================================"
echo ""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检测系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
fi

log_info "检测到操作系统：$OS"

# 安装 Node.js (v20)
install_nodejs() {
    log_info "正在安装 Node.js v20..."
    
    case $OS in
        centos|rhel|almalinux|rocky)
            curl -fsSL https://rpm.nodesource.com/setup_20.x | bash -
            yum install -y nodejs
            ;;
        ubuntu|debian)
            curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
            apt-get install -y nodejs
            ;;
        *)
            log_error "不支持的操作系统：$OS"
            return 1
            ;;
    esac
    
    log_info "Node.js 安装完成：$(node -v)"
    log_info "npm 版本：$(npm -v)"
}

# 安装 Maven
install_maven() {
    log_info "正在安装 Maven..."
    
    case $OS in
        centos|rhel|almalinux|rocky)
            yum install -y maven
            ;;
        ubuntu|debian)
            apt-get install -y maven
            ;;
        *)
            log_error "不支持的操作系统：$OS"
            return 1
            ;;
    esac
    
    log_info "Maven 安装完成：$(mvn -v | head -1)"
}

# 安装 PM2
install_pm2() {
    log_info "正在安装 PM2..."
    npm install -g pm2
    log_info "PM2 安装完成：$(pm2 -v)"
}

# 创建部署目录
setup_dirs() {
    log_info "正在创建部署目录..."
    
    DEPLOY_PATH="/www/wwwroot/points"
    BACKUP_PATH="/www/backup/points"
    
    mkdir -p $DEPLOY_PATH
    mkdir -p $BACKUP_PATH
    chown -R www:www $DEPLOY_PATH
    chown -R www:www $BACKUP_PATH
    
    log_info "部署目录：$DEPLOY_PATH"
    log_info "备份目录：$BACKUP_PATH"
}

# 主菜单
echo ""
echo "请选择要安装的组件："
echo "  1) 全部安装（推荐）"
echo "  2) 仅 Node.js"
echo "  3) 仅 Maven"
echo "  4) 仅 PM2"
echo "  5) 仅创建目录"
echo "  0) 退出"
echo ""
read -p "请输入选项 [0-5]: " choice

case $choice in
    1)
        install_nodejs
        install_maven
        install_pm2
        setup_dirs
        ;;
    2)
        install_nodejs
        ;;
    3)
        install_maven
        ;;
    4)
        install_pm2
        ;;
    5)
        setup_dirs
        ;;
    0)
        echo "退出安装"
        exit 0
        ;;
    *)
        log_error "无效选项"
        exit 1
        ;;
esac

echo ""
echo "========================================"
log_info "✅ 环境安装完成！"
echo "========================================"
echo ""
echo "📋 环境摘要："
echo "  - Node.js: $(node -v 2>/dev/null || echo '未安装')"
echo "  - npm: $(npm -v 2>/dev/null || echo '未安装')"
echo "  - Maven: $(mvn -v 2>/dev/null | head -1 || echo '未安装')"
echo "  - PM2: $(pm2 -v 2>/dev/null || echo '未安装')"
echo ""
echo "下一步：回到 OpenClaw 运行测试部署"
echo "========================================"
