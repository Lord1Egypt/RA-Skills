#!/bin/bash

#######################################
# 阿里云 OSS 技能 - 自动安装配置脚本
# 参考：qiniu-kodo 技能
#######################################

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认值
CHECK_ONLY=false
INSTALL_SDK=false
ACCESS_KEY_ID=""
ACCESS_KEY_SECRET=""
REGION=""
BUCKET=""
DOMAIN=""

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$BASE_DIR/config"
CONFIG_FILE="$CONFIG_DIR/oss-config.json"

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --check-only)
                CHECK_ONLY=true
                shift
                ;;
            --install-sdk)
                INSTALL_SDK=true
                shift
                ;;
            --access-key-id)
                ACCESS_KEY_ID="$2"
                shift 2
                ;;
            --access-key-secret)
                ACCESS_KEY_SECRET="$2"
                shift 2
                ;;
            --region)
                REGION="$2"
                shift 2
                ;;
            --bucket)
                BUCKET="$2"
                shift 2
                ;;
            --domain)
                DOMAIN="$2"
                shift 2
                ;;
            *)
                log_error "未知参数: $1"
                exit 1
                ;;
        esac
    done
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查 Node.js 环境
check_nodejs() {
    log_info "检查 Node.js 环境..."
    
    if command_exists node; then
        NODE_VERSION=$(node --version 2>&1)
        log_info "✅ Node.js 已安装: $NODE_VERSION"
        return 0
    else
        log_error "❌ Node.js 未安装"
        return 1
    fi
}

# 检查 npm
check_npm() {
    log_info "检查 npm..."
    
    if command_exists npm; then
        NPM_VERSION=$(npm --version 2>&1)
        log_info "✅ npm 已安装: $NPM_VERSION"
        return 0
    else
        log_error "❌ npm 未安装"
        return 1
    fi
}

# 检查 ali-oss Node.js SDK
check_sdk() {
    log_info "检查 ali-oss Node.js SDK..."
    
    # 检查技能目录下的 node_modules
    if [ -d "$BASE_DIR/node_modules/ali-oss" ]; then
        SDK_VERSION=$(node -p "require('$BASE_DIR/node_modules/ali-oss/package.json').version" 2>/dev/null || echo "unknown")
        log_info "✅ ali-oss Node.js SDK 已安装: $SDK_VERSION"
        return 0
    else
        log_warn "⚠️  ali-oss Node.js SDK 未安装"
        return 1
    fi
}

# 检查 ossutil 命令行工具
check_ossutil() {
    log_info "检查 ossutil..."
    
    if command_exists ossutil; then
        log_info "✅ ossutil 已安装"
        return 0
    else
        log_warn "⚠️  ossutil 未安装"
        return 1
    fi
}

# 检查配置文件
check_config() {
    log_info "检查配置文件..."
    
    if [ -f "$CONFIG_FILE" ]; then
        log_info "✅ 配置文件已存在: $CONFIG_FILE"
        
        # 验证配置（使用 node 检查 JSON）
        if node -e "require('$CONFIG_FILE')" 2>/dev/null; then
            log_info "✅ 配置文件格式正确"
            return 0
        else
            log_error "❌ 配置文件格式错误"
            return 1
        fi
    else
        log_warn "⚠️  配置文件不存在"
        return 1
    fi
}

# 检查凭证是否已配置
check_credentials() {
    log_info "检查凭证配置..."
    
    if [ -f "$CONFIG_FILE" ]; then
        ACCESS_KEY_ID_CHECK=$(node -p "require('$CONFIG_FILE').accessKeyId || ''" 2>/dev/null)
        
        if [ -n "$ACCESS_KEY_ID_CHECK" ] && [ "$ACCESS_KEY_ID_CHECK" != "你的AccessKey ID" ]; then
            log_info "✅ 凭证已配置"
            return 0
        else
            log_warn "⚠️  凭证未配置或使用示例值"
            return 1
        fi
    else
        log_warn "⚠️  配置文件不存在"
        return 1
    fi
}

# 安装 ali-oss Node.js SDK
install_sdk() {
    log_info "安装 ali-oss Node.js SDK..."
    
    cd "$BASE_DIR"
    
    # 初始化 package.json（如果不存在）
    if [ ! -f "package.json" ]; then
        npm init -y > /dev/null 2>&1
    fi
    
    # 安装 ali-oss SDK
    if npm install ali-oss --save 2>/dev/null; then
        log_info "✅ ali-oss Node.js SDK 安装成功"
        return 0
    else
        log_error "❌ ali-oss Node.js SDK 安装失败"
        return 1
    fi
}

# 创建配置文件
create_config() {
    log_info "创建配置文件..."
    
    mkdir -p "$CONFIG_DIR"
    
    cat > "$CONFIG_FILE" <<EOF
{
  "accessKeyId": "$ACCESS_KEY_ID",
  "accessKeySecret": "$ACCESS_KEY_SECRET",
  "bucket": "$BUCKET",
  "region": "$REGION",
  "domain": "$DOMAIN",
  "options": {
    "secure": true,
    "timeout": 60000,
    "upload_threshold": 1048576,
    "chunk_size": 1048576,
    "retry_times": 3
  }
}
EOF
    
    # 设置权限
    chmod 600 "$CONFIG_FILE"
    
    log_info "✅ 配置文件已创建: $CONFIG_FILE"
}

# 配置 shell 环境
configure_shell() {
    log_info "配置 shell 环境..."
    
    local SHELL_RC=""
    
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
    
    # 添加环境变量
    if ! grep -q "ALIYUN_ACCESS_KEY_ID" "$SHELL_RC" 2>/dev/null; then
        cat >> "$SHELL_RC" <<EOF

# 阿里云 OSS 配置
export ALIYUN_ACCESS_KEY_ID="$ACCESS_KEY_ID"
export ALIYUN_ACCESS_KEY_SECRET="$ACCESS_KEY_SECRET"
export ALIYUN_BUCKET="$BUCKET"
export ALIYUN_REGION="$REGION"
EOF
        log_info "✅ Shell 环境已配置: $SHELL_RC"
    else
        log_info "✅ Shell 环境已存在配置"
    fi
}

# 验证连接
verify_connection() {
    log_info "验证阿里云 OSS 连接..."
    
    if node "$SCRIPT_DIR/oss_node.mjs" test-connection 2>/dev/null; then
        log_info "✅ 阿里云 OSS 连接验证成功"
        return 0
    else
        log_error "❌ 阿里云 OSS 连接验证失败"
        return 1
    fi
}

# 环境检查
check_environment() {
    log_info "=========================================="
    log_info "  阿里云 OSS 环境检查"
    log_info "=========================================="
    echo ""
    
    local ALL_OK=true
    
    check_nodejs || ALL_OK=false
    check_npm || ALL_OK=false
    check_sdk || ALL_OK=false
    check_ossutil || true  # 可选
    check_config || true
    check_credentials || true
    
    echo ""
    log_info "=========================================="
    
    if $ALL_OK; then
        log_info "✅ 环境检查通过"
        return 0
    else
        log_warn "⚠️  环境检查未完全通过"
        return 1
    fi
}

# 完整安装
full_setup() {
    log_info "=========================================="
    log_info "  阿里云 OSS 自动安装"
    log_info "=========================================="
    echo ""
    
    # 检查必需项
    if ! check_nodejs; then
        log_error "Node.js 是必需的"
        exit 1
    fi
    
    if ! check_npm; then
        log_error "npm 是必需的"
        exit 1
    fi
    
    # 安装 SDK
    if ! check_sdk; then
        install_sdk
    fi
    
    # 创建配置
    if [ -n "$ACCESS_KEY_ID" ] && [ -n "$ACCESS_KEY_SECRET" ]; then
        create_config
        configure_shell
        verify_connection
    fi
    
    echo ""
    log_info "=========================================="
    log_info "✅ 安装完成！"
    log_info "=========================================="
}

# 主函数
main() {
    parse_args "$@"
    
    if $CHECK_ONLY; then
        check_environment
    elif $INSTALL_SDK; then
        install_sdk
    elif [ -n "$ACCESS_KEY_ID" ]; then
        full_setup
    else
        check_environment
        echo ""
        log_info "使用方法："
        log_info "  检查环境: $0 --check-only"
        log_info "  完整安装: $0 --access-key-id <ID> --access-key-secret <SECRET> --region <REGION> --bucket <BUCKET>"
        log_info "  安装 SDK: $0 --install-sdk"
    fi
}

main "$@"
