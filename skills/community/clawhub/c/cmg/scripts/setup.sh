#!/bin/bash
# cmg-recommend Skill 设置脚本
#
# 用法:
#   setup.sh --check-only                    仅检查环境状态
#   setup.sh --server-url <URL>              配置 MCP Server 地址并完成设置
#
# 示例:
#   setup.sh --check-only
#   setup.sh --server-url https://cmg-mcp.example.com

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}!${NC} $1"; }

MCPORTER_CONFIG="$HOME/.mcporter/mcporter.json"
SERVER_NAME="cmg-recommend"
DEFAULT_SERVER_URL="http://61.151.231.241"

# ========== 检查函数 ==========

check_node() {
  if command -v node &>/dev/null; then
    ok "Node.js $(node --version)"
    return 0
  else
    fail "Node.js 未安装（mcporter 依赖 Node.js）"
    return 1
  fi
}

check_npm() {
  if command -v npm &>/dev/null; then
    ok "npm $(npm --version)"
    return 0
  else
    fail "npm 未安装"
    return 1
  fi
}

check_mcporter() {
  if command -v mcporter &>/dev/null; then
    ok "mcporter $(mcporter --version 2>/dev/null || echo '已安装')"
    return 0
  else
    fail "mcporter 未安装"
    return 1
  fi
}

check_mcporter_config() {
  if [ -f "$MCPORTER_CONFIG" ]; then
    if grep -q "\"$SERVER_NAME\"" "$MCPORTER_CONFIG" 2>/dev/null; then
      local url
      url=$(node -e "
        const c = require('$MCPORTER_CONFIG');
        console.log((c.mcpServers && c.mcpServers['$SERVER_NAME'] && c.mcpServers['$SERVER_NAME'].url) || '');
      " 2>/dev/null)
      ok "mcporter 已配置 $SERVER_NAME (${url:-url未知})"
      return 0
    else
      warn "mcporter.json 存在但未配置 $SERVER_NAME"
      return 1
    fi
  else
    fail "$MCPORTER_CONFIG 不存在"
    return 1
  fi
}

check_server_reachable() {
  local url="$1"
  if [ -z "$url" ]; then
    # 从配置文件读取 URL
    if [ -f "$MCPORTER_CONFIG" ]; then
      url=$(node -e "
        const c = require('$MCPORTER_CONFIG');
        console.log((c.mcpServers && c.mcpServers['$SERVER_NAME'] && c.mcpServers['$SERVER_NAME'].url) || '');
      " 2>/dev/null)
    fi
  fi

  if [ -z "$url" ]; then
    warn "未配置 server url，跳过连通性检查"
    return 1
  fi

  # Streamable HTTP 协议：POST /mcp 发送 initialize 请求验证连通性
  local mcp_url="${url%/}/mcp"
  local response
  response=$(curl -s --max-time 5 -X POST "$mcp_url" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"setup","version":"1.0"}}}' \
    2>/dev/null)
  if echo "$response" | grep -q '"protocolVersion"'; then
    ok "MCP Server 连通性正常 ($url)"
    return 0
  else
    warn "MCP Server 无法连接 ($url)，请确认服务已启动"
    return 1
  fi
}

# ========== 检查模式 ==========

do_check() {
  echo "=== cmg-recommend Skill 环境检查 ==="
  echo ""
  echo "--- 基础环境 ---"
  check_node || true
  check_npm || true
  echo ""
  echo "--- mcporter ---"
  check_mcporter || true
  check_mcporter_config || true
  echo ""
  echo "--- MCP Server 连通性 ---"
  check_server_reachable "" || true
  echo ""
}

# ========== 设置模式 ==========

do_setup() {
  local SERVER_URL=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --server-url) SERVER_URL="$2"; shift 2;;
      *) shift;;
    esac
  done

  if [ -z "$SERVER_URL" ]; then
    SERVER_URL="$DEFAULT_SERVER_URL"
    warn "未指定 --server-url，使用默认地址: $SERVER_URL"
  fi

  # 去掉末尾斜杠
  SERVER_URL="${SERVER_URL%/}"

  echo "=== cmg-recommend Skill 自动设置 ==="
  echo ""

  # 步骤 1：检查 Node.js
  echo "--- 步骤 1: 检查 Node.js ---"
  if ! check_node; then
    fail "请先安装 Node.js: https://nodejs.org/"
    exit 1
  fi

  # 步骤 2：安装 mcporter
  echo ""
  echo "--- 步骤 2: 安装 mcporter ---"
  if ! command -v mcporter &>/dev/null; then
    echo "正在安装 mcporter..."
    npm install -g mcporter --no-progress 2>&1 | tail -3
    if command -v mcporter &>/dev/null; then
      ok "mcporter 全局安装完成"
    else
      fail "mcporter 安装失败，请手动执行: npm install -g mcporter"
      exit 1
    fi
  else
    ok "mcporter 已安装"
  fi

  # 步骤 3：写入 mcporter 配置
  echo ""
  echo "--- 步骤 3: 配置 mcporter ---"
  mkdir -p "$HOME/.mcporter"

  # 用 mcporter config add 写入（Streamable HTTP 协议，路径 /mcp）
  mcporter config add "$SERVER_NAME" "${SERVER_URL}/mcp" \
    --transport http \
    --persist "$MCPORTER_CONFIG" 2>&1 | grep -v '^$' || true
  ok "mcporter.json 已配置 $SERVER_NAME"

  # 步骤 4：验证连通性
  echo ""
  echo "--- 步骤 4: 验证 MCP Server 连通性 ---"
  check_server_reachable "$SERVER_URL" || true

  echo ""
  echo "=== 设置完成 ==="
  echo ""
  echo "现在可以通过 mcporter 调用推荐工具："
  echo ""
  echo "  # 列出所有可用工具"
  echo "  mcporter list $SERVER_NAME --config $MCPORTER_CONFIG --schema"
  echo ""
  echo "  # 推荐示例：阿里云 4C8G ECS"
  echo "  mcporter call $SERVER_NAME.recommend_cvm \\"
  echo "    --config $MCPORTER_CONFIG --output json \\"
  echo "    --args '{\"vendor\":\"aliyun\",\"cpu\":4,\"memory\":8,\"src_region_id\":\"cn-beijing\"}'"
}

# ========== 主入口 ==========

case "$1" in
  --check-only)
    do_check
    ;;
  --server-url)
    do_setup "$@"
    ;;
  --setup)
    do_setup
    ;;
  *)
    echo "cmg-recommend Skill 设置工具"
    echo ""
    echo "用法:"
    echo "  $0 --check-only"
    echo "    检查环境状态（mcporter 安装情况、配置、连通性）"
    echo ""
    echo "  $0 --setup"
    echo "    使用默认 MCP Server 地址安装配置 (${DEFAULT_SERVER_URL})"
    echo ""
    echo "  $0 --server-url <URL>"
    echo "    安装 mcporter 并配置自定义 MCP Server 地址"
    ;;
esac
