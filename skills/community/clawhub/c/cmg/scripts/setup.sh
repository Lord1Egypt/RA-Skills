#!/bin/bash
# cmg-recommend Skill 设置脚本
#
# 用法:
#   setup.sh --check-only                    仅检查环境状态（只读，不做任何修改）
#   setup.sh --server-url <URL>              配置 MCP Server 地址并完成设置
#   setup.sh --server-url <URL> --yes        跳过交互确认（供 CI 使用）
#
# 示例:
#   setup.sh --check-only
#   setup.sh --server-url https://cmg-mcp.your-domain.example
#
# 安全说明:
#   - 本脚本没有内置默认 MCP Server 地址。必须由你显式提供 --server-url。
#   - 仅接受 https:// 地址（localhost / 127.0.0.1 可用 http:// 以便本地调试）。
#     推荐结果请求会携带你的云资源清单，明文 HTTP 传输会导致这些信息在链路上泄露。
#   - 安装依赖（npm -g）和写入配置文件前都会请求确认，除非显式传入 --yes。

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}!${NC} $1"; }

MCPORTER_CONFIG="$HOME/.mcporter/mcporter.json"
SERVER_NAME="cmg-recommend"
ASSUME_YES=0

# ========== 安全校验 ==========

# 校验 server URL：必须是 https://，本地回环地址除外。
validate_server_url() {
  local url="$1"

  case "$url" in
    https://*)
      return 0
      ;;
    http://localhost|http://localhost:*|http://localhost/*|\
    http://127.0.0.1|http://127.0.0.1:*|http://127.0.0.1/*|\
    http://[::1]|http://[::1]:*|http://[::1]/*)
      warn "使用本地回环地址的明文 HTTP（仅限本地调试）: $url"
      return 0
      ;;
    http://*)
      fail "拒绝明文 HTTP 地址: $url"
      echo ""
      echo "  推荐请求会发送你的云资源清单（实例规格、地域、数量等）。"
      echo "  明文 HTTP 无加密、无服务端身份校验，链路上的任何一跳都能读取或篡改这些数据。"
      echo ""
      echo "  请改用 https:// 地址。若服务端尚未启用 TLS，请先为其配置证书。"
      return 1
      ;;
    *)
      fail "无法识别的地址: $url（需要以 https:// 开头）"
      return 1
      ;;
  esac
}

# 交互确认。--yes 时直接通过；非交互终端且未传 --yes 时拒绝执行。
confirm() {
  local prompt="$1"
  if [ "$ASSUME_YES" -eq 1 ]; then
    echo "  (--yes 已指定，跳过确认: $prompt)"
    return 0
  fi
  if [ ! -t 0 ]; then
    fail "需要确认「$prompt」，但当前不是交互式终端。"
    echo "  如确认要执行，请重新运行并显式传入 --yes。"
    return 1
  fi
  local reply=""
  printf "  %s [y/N] " "$prompt"
  read -r reply
  case "$reply" in
    [yY]|[yY][eE][sS]) return 0 ;;
    *) return 1 ;;
  esac
}

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

# 从配置文件读取已配置的 server url。用 python3 解析 JSON，
# 避免用 require() 执行配置文件内容。
read_configured_url() {
  [ -f "$MCPORTER_CONFIG" ] || return 0
  python3 - "$MCPORTER_CONFIG" "$SERVER_NAME" <<'PY' 2>/dev/null || true
import json, sys
try:
    with open(sys.argv[1], encoding="utf-8") as fh:
        cfg = json.load(fh)
    print((cfg.get("mcpServers", {}).get(sys.argv[2], {}) or {}).get("url", ""))
except Exception:
    pass
PY
}

check_mcporter_config() {
  if [ -f "$MCPORTER_CONFIG" ]; then
    local url
    url=$(read_configured_url)
    if [ -n "$url" ]; then
      ok "mcporter 已配置 $SERVER_NAME ($url)"
      case "$url" in
        http://localhost*|http://127.0.0.1*|http://[::1]*) ;;
        http://*) warn "该地址为明文 HTTP，建议改为 https://（重新运行 --server-url 覆盖）" ;;
      esac
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
  local url="${1:-}"
  if [ -z "$url" ]; then
    url=$(read_configured_url)
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
    2>/dev/null) || true
  if echo "$response" | grep -q '"protocolVersion"'; then
    ok "MCP Server 连通性正常 ($url)"
    return 0
  else
    warn "MCP Server 无法连接 ($url)，请确认服务已启动"
    return 1
  fi
}

# ========== 检查模式（只读） ==========

do_check() {
  echo "=== cmg-recommend Skill 环境检查（只读，不做任何修改）==="
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
      --server-url) SERVER_URL="${2:-}"; shift 2;;
      --yes|-y)     ASSUME_YES=1; shift;;
      --setup)      shift;;
      *) shift;;
    esac
  done

  if [ -z "$SERVER_URL" ]; then
    fail "必须提供 --server-url <URL>"
    echo ""
    echo "  本 Skill 不内置默认 MCP Server 地址。推荐服务会接收你的云资源清单，"
    echo "  因此目标地址必须由你自己指定并确认可信。"
    echo ""
    echo "  用法: $0 --server-url https://<你的-cmg-mcp-地址>"
    exit 1
  fi

  SERVER_URL="${SERVER_URL%/}"

  if ! validate_server_url "$SERVER_URL"; then
    exit 1
  fi

  echo "=== cmg-recommend Skill 设置 ==="
  echo ""
  echo "将要执行的操作："
  echo "  1. 检查 Node.js"
  echo "  2. 若缺失，全局安装 mcporter（npm install -g mcporter）"
  echo "  3. 将 $SERVER_NAME -> ${SERVER_URL}/mcp 写入 $MCPORTER_CONFIG"
  echo "  4. 验证连通性"
  echo ""
  echo "注意：配置写入后，推荐请求中的云资源清单会发送到上述地址。"
  echo ""

  if ! confirm "确认继续？"; then
    echo "已取消，未做任何修改。"
    exit 1
  fi

  # 步骤 1：检查 Node.js
  echo ""
  echo "--- 步骤 1: 检查 Node.js ---"
  if ! check_node; then
    fail "请先安装 Node.js: https://nodejs.org/"
    exit 1
  fi

  # 步骤 2：安装 mcporter
  echo ""
  echo "--- 步骤 2: 检查 mcporter ---"
  if ! command -v mcporter &>/dev/null; then
    warn "mcporter 未安装，需要全局安装（会修改全局 npm 环境）"
    if ! confirm "执行 npm install -g mcporter？"; then
      fail "已取消。可手动安装后重新运行：npm install -g mcporter"
      exit 1
    fi
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

  mcporter config add "$SERVER_NAME" "${SERVER_URL}/mcp" \
    --transport http \
    --persist "$MCPORTER_CONFIG" 2>&1 | grep -v '^$' || true
  ok "mcporter.json 已配置 $SERVER_NAME -> ${SERVER_URL}/mcp"

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
  echo ""
  echo "如需更换地址：$0 --server-url https://<新地址>"
}

# ========== 主入口 ==========

case "${1:-}" in
  --check-only)
    do_check
    ;;
  --server-url|--setup|--yes|-y)
    do_setup "$@"
    ;;
  *)
    echo "cmg-recommend Skill 设置工具"
    echo ""
    echo "用法:"
    echo "  $0 --check-only"
    echo "    检查环境状态（只读：mcporter 安装情况、配置、连通性）"
    echo ""
    echo "  $0 --server-url <URL>"
    echo "    安装 mcporter 并配置 MCP Server 地址（需交互确认）"
    echo "    地址必须为 https://（localhost 可用 http:// 调试）"
    echo ""
    echo "  $0 --server-url <URL> --yes"
    echo "    跳过交互确认，供 CI 使用"
    echo ""
    echo "本 Skill 不内置默认 MCP Server 地址：推荐请求会携带你的云资源清单，"
    echo "目标地址必须由你显式指定。"
    ;;
esac
