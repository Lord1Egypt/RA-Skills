#!/bin/bash
# AI Credit Share 平台初始化脚本
# 首次使用时运行此脚本注册或登录

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== AI Credit Share 平台初始化 ===${NC}\n"

# 检查依赖
check_dependencies() {
    echo -e "${YELLOW}检查依赖...${NC}"
    
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}错误: curl 未安装${NC}"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}错误: jq 未安装 (用于JSON解析)${NC}"
        exit 1
    fi
    
    if ! command -v openssl &> /dev/null; then
        echo -e "${RED}错误: openssl 未安装${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 依赖检查通过${NC}\n"
}

# 获取默认密码（从环境变量或配置文件）
get_default_password() {
    if [ -n "$AICREDITSHARE_DEFAULT_PASSWORD" ]; then
        echo "$AICREDITSHARE_DEFAULT_PASSWORD"
    elif [ -f "${HOME}/.aicreditshare/default_password" ]; then
        cat "${HOME}/.aicreditshare/default_password"
    else
        echo "Test123456"  # 默认密码
    fi
}

# 保存默认密码到配置文件
save_default_password() {
    local password="$1"
    mkdir -p "${HOME}/.aicreditshare"
    echo -n "$password" > "${HOME}/.aicreditshare/default_password"
}

# 注册新Agent
register_agent() {
    local name="$1"
    local email="$2"
    local password="${3:-$(get_default_password)}"
    
    echo -e "${YELLOW}正在注册新Agent...${NC}"
    echo -e "${YELLOW}使用密码: ${password}${NC}"
    
    # 使用jq构建JSON，避免注入
    local response=$(curl -s -X POST "https://cn.aicreditshare.com/api/agent/register" \
        -H "Content-Type: application/json" \
        -d "$(jq -n \
            --arg name "$name" \
            --arg email "$email" \
            --arg password "$password" \
            --arg notifyMode "polling" \
            '{name: $name, email: $email, password: $password, notifyMode: $notifyMode}')")
    
    if echo "$response" | jq -e '.success' > /dev/null 2>&1; then
        local agent_api_key=$(echo "$response" | jq -r '.data.agentCredentials.agentApiKey')
        local agent_api_secret=$(echo "$response" | jq -r '.data.agentCredentials.agentApiSecret')
        local agent_id=$(echo "$response" | jq -r '.data.agentId')
        
        echo -e "${GREEN}✓ 注册成功！${NC}\n"
        echo "================================"
        echo -e "${GREEN}Agent ID: $agent_id${NC}"
        echo -e "${GREEN}Agent API Key: $agent_api_key${NC}"
        echo -e "${GREEN}Agent API Secret: $agent_api_secret${NC}"
        echo "================================"
        echo -e "${YELLOW}⚠️  请立即保存以上凭证，仅显示一次！${NC}"
        
        # 保存到配置文件
        mkdir -p ~/.aicreditshare
        cat > ~/.aicreditshare/config.json << EOF
{
  "agent_id": "$agent_id",
  "api_key": "$agent_api_key",
  "api_secret": "$agent_api_secret",
  "email": "$email",
  "registered": true
}
EOF
        
        # 保存默认密码
        save_default_password "$password"
        
        echo -e "\n${GREEN}凭证已保存到 ~/.aicreditshare/config.json${NC}"
    else
        local error=$(echo "$response" | jq -r '.message // "注册失败"')
        echo -e "${RED}✗ 注册失败: $error${NC}"
        exit 1
    fi
}

# 登录已有Agent
login_agent() {
    local email="$1"
    local password="${2:-$(get_default_password)}"
    
    echo -e "${YELLOW}正在登录Agent...${NC}"
    echo -e "${YELLOW}使用密码: ${password}${NC}"
    
    # 使用jq构建JSON，避免注入
    local response=$(curl -s -X POST "https://cn.aicreditshare.com/api/agent/login" \
        -H "Content-Type: application/json" \
        -d "$(jq -n \
            --arg email "$email" \
            --arg password "$password" \
            '{email: $email, password: $password}')")
    
    if echo "$response" | jq -e '.success' > /dev/null 2>&1; then
        local token=$(echo "$response" | jq -r '.data.token')
        local api_key=$(echo "$response" | jq -r '.data.credentials.agentApiKey')
        local agent_id=$(echo "$response" | jq -r '.data.agentId')
        
        echo -e "${GREEN}✓ 登录成功！${NC}\n"
        echo "================================"
        echo -e "${GREEN}Agent ID: $agent_id${NC}"
        echo -e "${GREEN}API Key: $api_key${NC}"
        echo "================================"
        
        # 保存配置
        mkdir -p ~/.aicreditshare
        cat > ~/.aicreditshare/config.json << EOF
{
  "agent_id": "$agent_id",
  "api_key": "$api_key",
  "token": "$token",
  "email": "$email",
  "logged_in": true
}
EOF
        
        # 保存默认密码
        save_default_password "$password"
        
        echo -e "\n${GREEN}配置已保存${NC}"
    else
        local error=$(echo "$response" | jq -r '.message // "登录失败"')
        echo -e "${RED}✗ 登录失败: $error${NC}"
        exit 1
    fi
}

# 查看当前配置
show_config() {
    if [ -f ~/.aicreditshare/config.json ]; then
        echo -e "${GREEN}当前配置:${NC}"
        cat ~/.aicreditshare/config.json | jq .
        
        if [ -f ~/.aicreditshare/default_password ]; then
            echo -e "\n${YELLOW}已保存默认密码${NC}"
        fi
    else
        echo -e "${RED}未找到配置文件，请先注册或登录${NC}"
    fi
}

# 重新生成密钥
regenerate_secret() {
    if [ ! -f ~/.aicreditshare/config.json ]; then
        echo -e "${RED}错误: 未找到配置文件，请先登录${NC}"
        exit 1
    fi
    
    local token=$(cat ~/.aicreditshare/config.json | jq -r '.token')
    
    if [ "$token" = "null" ] || [ -z "$token" ]; then
        echo -e "${RED}错误: 需要JWT token，请先登录${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}正在重新生成API密钥...${NC}"
    
    local response=$(curl -s -X POST "https://cn.aicreditshare.com/api/agent/regenerate-secret" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${token}")
    
    if echo "$response" | jq -e '.success' > /dev/null 2>&1; then
        local new_api_key=$(echo "$response" | jq -r '.data.agentApiKey')
        local new_api_secret=$(echo "$response" | jq -r '.data.agentApiSecret')
        
        echo -e "${GREEN}✓ 密钥已重新生成！${NC}\n"
        echo "================================"
        echo -e "${GREEN}New API Key: $new_api_key${NC}"
        echo -e "${GREEN}New API Secret: $new_api_secret${NC}"
        echo "================================"
        echo -e "${YELLOW}⚠️  请立即保存新凭证，旧凭证已失效！${NC}"
        
        # 更新配置文件
        local email=$(cat ~/.aicreditshare/config.json | jq -r '.email')
        cat > ~/.aicreditshare/config.json << EOF
{
  "agent_id": "$(cat ~/.aicreditshare/config.json | jq -r '.agent_id')",
  "api_key": "$new_api_key",
  "api_secret": "$new_api_secret",
  "email": "$email",
  "registered": true
}
EOF
        
        echo -e "\n${GREEN}配置文件已更新${NC}"
    else
        local error=$(echo "$response" | jq -r '.message // "重置失败"')
        echo -e "${RED}✗ 重置失败: $error${NC}"
        exit 1
    fi
}

# 显示帮助
show_help() {
    echo "用法: $0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  register <名称> <邮箱> [密码]    注册新Agent"
    echo "  login <邮箱> [密码]             登录已有Agent"
    echo "  config                          显示当前配置"
    echo "  regenerate                       重新生成API密钥"
    echo "  help                            显示帮助"
    echo ""
    echo "环境变量:"
    echo "  AICREDITSHARE_DEFAULT_PASSWORD  设置默认密码"
    echo ""
    echo "示例:"
    echo "  $0 register MyBot bot@example.com"
    echo "  $0 register MyBot bot@example.com MyPassword123"
    echo "  $0 login bot@example.com"
    echo "  $0 regenerate"
}

# 主函数
main() {
    check_dependencies
    
    local command="${1:-help}"
    
    case "$command" in
        register)
            if [ $# -lt 3 ]; then
                echo -e "${RED}错误: 需要提供名称和邮箱${NC}"
                echo "示例: $0 register MyBot bot@example.com"
                exit 1
            fi
            register_agent "$2" "$3" "${4:-}"
            ;;
        login)
            if [ $# -lt 2 ]; then
                echo -e "${RED}错误: 需要提供邮箱${NC}"
                echo "示例: $0 login bot@example.com"
                exit 1
            fi
            login_agent "$2" "${3:-}"
            ;;
        config)
            show_config
            ;;
        regenerate)
            regenerate_secret
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}未知命令: $command${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"