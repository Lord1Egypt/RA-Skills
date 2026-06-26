#!/bin/bash
# Agent 完整设置脚本
# 一键完成：添加agent配置 -> 注册Matrix账号 -> 添加账号到配置 -> 绑定agent与账号

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 默认配置
HOMESERVER_URL="${HOMESERVER_URL:-http://localhost:8008}"
CONFIG_PATH="${CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"

# 显示帮助
show_help() {
    cat << EOF
Agent 完整设置脚本

用法:
  $0 <agent_id> <agent_name>

参数:
  agent_id     - agent的唯一标识（如: juezhi）
  agent_name   - agent的显示名称（如: 货绝知）
    
环境变量:
  HOMESERVER_URL  - Matrix服务器地址
  CONFIG_PATH     - openclaw.json配置文件路径

示例:
  $0 "huojuezhi" "货绝知"
  HOMESERVER_URL=http://192.168.1.100:8008 $0 "huojuezhi" "货绝知"

流程:
  1. 添加agent到openclaw.json配置
  2. 在Matrix服务器注册账号
  3. 将账号添加到openclaw.json配置
  4. 绑定agent与Matrix账号
EOF
}

# 主函数
main() {
    if [ $# -lt 2 ]; then
        show_help
        exit 1
    fi
    
    local agent_id="$1"
    local agent_name="$2"
    shift 2
    
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}  Agent 设置向导${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo ""
    echo "配置信息:"
    echo "  Agent ID: $agent_id"
    echo "  Agent名称: $agent_name"
    echo "  Matrix服务器: $HOMESERVER_URL"
    echo "  配置文件: $CONFIG_PATH"
    echo ""
    
    # 检查依赖
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ 需要安装 python3${NC}"
        exit 1
    fi
    
    # 步骤1: 添加agent配置
    echo -e "${YELLOW}步骤 1/4: 添加agent配置...${NC}"
    if ! python3 "$SCRIPT_DIR/config_manager.py" agents add "$agent_name" "$agent_id" "$HOME/.openclaw/${agent_id}-workspace" "nvidia/moonshotai/kimi-k2.5"; then
        echo -e "${RED}❌ 步骤1失败：无法添加Agent配置。${NC}"
        exit 1
    fi

    # 步骤2: 注册Matrix账号
    echo -e "${YELLOW}步骤 2/4: 注册/登录Matrix账号...${NC}"
    local password="${agent_id}20260205openclaw"
    local register_output
    # 捕获输出
    if ! register_output=$(HOMESERVER_URL="$HOMESERVER_URL" bash "$SCRIPT_DIR/matrix_register.sh" "$agent_id" "$password" 2>&1); then
        echo -e "${RED}❌ 步骤2失败：Matrix注册或登录过程出错。${NC}"
        echo "$register_output"
        exit 1
    fi
    
    # 解析 Token 和 UID (增加容错)
    local access_token=$(echo "$register_output" | grep "RESULT_ACCESS_TOKEN:" | awk '{print $NF}')
    local user_id=$(echo "$register_output" | grep "RESULT_USER_ID:" | awk '{print $NF}')

    if [[ -z "$access_token" || -z "$user_id" ]]; then
        echo -e "${RED}❌ 步骤2失败：解析Token失败。原始输出：${NC}\n$register_output"
        exit 1
    fi
    echo -e "${GREEN}成功获取 Token 为: ${access_token:0:8}...${NC}"

    # 步骤3: 添加账号到配置
    echo -e "${YELLOW}步骤 3/4: 添加Matrix账号到配置...${NC}"
    if ! python3 "$SCRIPT_DIR/config_manager.py" accounts add "$agent_name" "$access_token" "$agent_id" "$HOMESERVER_URL" "$user_id" "pairing"; then
        echo -e "${RED}❌ 步骤3失败：无法将账号写入配置文件。${NC}"
        exit 1
    fi

    # 步骤4: 绑定agent与账号
    echo -e "${YELLOW}步骤 4/4: 绑定agent与Matrix账号...${NC}"
    if ! python3 "$SCRIPT_DIR/config_manager.py" bindings add "$agent_id" "$agent_id" "matrix"; then
        echo -e "${RED}❌ 步骤4失败：绑定关系建立失败。${NC}"
        exit 1
    fi

    # 初始化工作空间
    cp -r "${HOME}/.openclaw/tmp-workspace/." "${HOME}/.openclaw/${agent_id}-workspace"

    # 完成
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ Agent设置完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo ""
    echo "总结:"
    echo "  Agent ID: $agent_id"
    echo "  显示名: $agent_name"
    echo "  Matrix账号: $user_id"
    echo "  配置文件: $CONFIG_PATH"
    echo ""
    echo -e "${YELLOW}⚠️ 请保存以下密码（仅在本次显示）:${NC}"
    echo "  密码: $password"
}

main "$@"
