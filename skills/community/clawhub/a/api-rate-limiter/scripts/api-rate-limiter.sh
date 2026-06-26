#!/bin/bash
# api-rate-limiter.sh - 全局API请求频率限制器

set -e

# 配置文件路径
CONFIG_DIR="$HOME/.openclaw/workspace/config"
CONFIG_FILE="$CONFIG_DIR/api_rate_limiter_config.json"
DEFAULT_CONFIG_FILE="/root/.openclaw/workspace/skills/api-rate-limiter/default_config.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 创建默认配置
create_default_config() {
    mkdir -p "$CONFIG_DIR"
    
    cat > "$DEFAULT_CONFIG_FILE" << 'EOF'
{
  "base_delay_ms": 800,
  "max_requests_per_minute": 1,
  "max_requests_per_hour": 40,
  "concurrency_limit": 1,
  "retry_count": 2,
  "cache_enabled": true,
  "cache_ttl_seconds": 600,
  "request_types": {
    "light": {
      "delay_ms": 300,
      "timeout_seconds": 30
    },
    "medium": {
      "delay_ms": 600,
      "timeout_seconds": 45
    },
    "heavy": {
      "delay_ms": 1000,
      "timeout_seconds": 90
    },
    "custom": {
      "delay_ms": 500,
      "timeout_seconds": 60
    }
  },
  "circuit_breaker": {
    "failure_threshold": 1,
    "reset_timeout_seconds": 150,
    "cooldown_after_trigger": 90
  },
  "enabled": true
}
EOF
}

# 初始化配置
init_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        print_info "创建默认配置文件: $CONFIG_FILE"
        cp "$DEFAULT_CONFIG_FILE" "$CONFIG_FILE"
    fi
}

# 检查依赖
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        print_error "jq is required but not installed. Please install jq first."
        exit 1
    fi
}

# 应用请求延迟
apply_delay() {
    local request_type="${1:-custom}"
    local delay_ms
    
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "配置文件不存在: $CONFIG_FILE"
        return 1
    fi
    
    # 从配置中获取延迟值
    delay_ms=$(jq -r ".request_types[\"$request_type\"].delay_ms // .base_delay_ms" "$CONFIG_FILE")
    
    if [ "$delay_ms" = "null" ] || [ -z "$delay_ms" ]; then
        delay_ms=500  # 默认延迟
    fi
    
    print_info "应用 $delay_ms ms 延迟 for $request_type 请求"
    
    # 转换为秒并休眠
    local delay_sec=$(echo "$delay_ms / 1000" | bc -l 2>/dev/null || echo "0.5")
    sleep "$delay_sec"
    
    print_success "延迟完成"
}

# 检查限流状态
check_status() {
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "配置文件不存在: $CONFIG_FILE"
        return 1
    fi
    
    print_info "API限流器状态:"
    local enabled=$(jq -r ".enabled" "$CONFIG_FILE")
    echo "  启用状态: $enabled"
    
    local base_delay=$(jq -r ".base_delay_ms" "$CONFIG_FILE")
    echo "  基础延迟: ${base_delay}ms"
    
    local rpm=$(jq -r ".max_requests_per_minute" "$CONFIG_FILE")
    echo "  每分钟最大请求数: $rpm"
    
    local rph=$(jq -r ".max_requests_per_hour" "$CONFIG_FILE")
    echo "  每小时最大请求数: $rph"
    
    local concurrency=$(jq -r ".concurrency_limit" "$CONFIG_FILE")
    echo "  并发限制: $concurrency"
}

# 显示当前配置
show_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "配置文件不存在: $CONFIG_FILE"
        return 1
    fi
    
    print_info "当前配置:"
    jq '.' "$CONFIG_FILE" | sed 's/^/  /'
}

# 更新配置
update_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "配置文件不存在: $CONFIG_FILE"
        return 1
    fi
    
    local key=""
    local value=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --key)
                key="$2"
                shift 2
                ;;
            --value)
                value="$2"
                shift 2
                ;;
            *)
                print_error "未知参数: $1"
                return 1
                ;;
        esac
    done
    
    if [ -z "$key" ] || [ -z "$value" ]; then
        print_error "必须指定 --key 和 --value 参数"
        return 1
    fi
    
    print_info "更新配置: $key = $value"
    
    # 尝试解析值，如果是数字则不加引号，否则加引号
    if [[ $value =~ ^[0-9]+$ ]] || [[ $value =~ ^[0-9]+\.[0-9]+$ ]]; then
        # 数字值，不需要引号
        jq --argjson val "$value" ".[$key] = \$val" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    elif [ "$value" = "true" ] || [ "$value" = "false" ]; then
        # 布尔值，不需要引号
        jq --argjson val "$value" ".[$key] = \$val" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    else
        # 字符串值，需要引号
        jq --arg val "$value" ".[$key] = \$val" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    fi
    
    print_success "配置已更新"
}

# 重置为默认配置
reset_config() {
    print_info "重置配置为默认值"
    cp "$DEFAULT_CONFIG_FILE" "$CONFIG_FILE"
    print_success "配置已重置"
}

# 显示帮助信息
show_help() {
    echo "全局API请求频率限制器"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  apply-delay [request-type]      应用请求延迟 (light|medium|heavy|custom)"
    echo "  check-status                    检查限流状态"
    echo "  show-config                     显示当前配置"
    echo "  update-config --key KEY --value VALUE"
    echo "                                  更新配置项"
    echo "  reset-config                    重置为默认配置"
    echo "  -h, --help                     显示此帮助信息"
    echo ""
    echo "请求类型:"
    echo "  light: 轻量请求 (默认延迟 300ms)"
    echo "  medium: 中量请求 (默认延迟 600ms)"
    echo "  heavy: 重量请求 (默认延迟 1000ms)"
    echo "  custom: 自定义请求 (默认延迟 500ms)"
    echo ""
}

# 主函数
main() {
    check_dependencies
    create_default_config
    init_config
    
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case $1 in
        "apply-delay")
            shift
            apply_delay "$@"
            ;;
        "check-status")
            check_status
            ;;
        "show-config")
            show_config
            ;;
        "update-config")
            shift
            update_config "$@"
            ;;
        "reset-config")
            reset_config
            ;;
        "-h"|"--help")
            show_help
            ;;
        *)
            print_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"