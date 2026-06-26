#!/bin/bash
# =============================================================================
# CodeBuddy MCP Server 安装/更新脚本
# 安装或更新 MCP Server 配置到 mcp.json
#
# 用法: ./install_mcp.sh <config_name> <config_scope> [command] [args...]
#       ./install_mcp.sh <config_name> <config_scope> --json <json_config>
#       ./install_mcp.sh <config_name> <config_scope> --url <config_url>
#
# 参数:
#   config_name  - MCP Server 名称
#   config_scope - 作用域: global | project
#   command      - 启动命令（可选，与 --json/--url 二选一）
#   args         - 命令参数（可选）
#   --json       - 完整的 JSON 配置块
#   --url        - 从 URL 获取配置
#
# 输出: JSON 格式的安装结果
# =============================================================================

set -eo pipefail

# ---------- 参数解析 ----------
CONFIG_NAME="${1:-}"
CONFIG_SCOPE="${2:-project}"
shift 2 2>/dev/null || true

if [ -z "$CONFIG_NAME" ]; then
  echo '{"success":false,"error":"Usage: install_mcp.sh <config_name> <scope> [command|--json|--url] [args...]"}'
  exit 1
fi

# ---------- 路径常量 ----------
HOME_DIR="$HOME"
PROJECT_DIR="$(cd "$(dirname "$0")/../../../.." 2>/dev/null && pwd || echo "")"

if [ "$CONFIG_SCOPE" = "global" ]; then
  TARGET_DIR="$HOME_DIR/.codebuddy"
  MCP_FILE="$TARGET_DIR/mcp.json"
else
  TARGET_DIR="$PROJECT_DIR/.codebuddy"
  MCP_FILE="$TARGET_DIR/mcp.json"
fi

# ---------- JSON 输出辅助 ----------
output_result() {
  local success="$1"
  local message="$2"
  local detail="$3"
  cat <<EOF
{
  "success": $success,
  "message": "$(echo "$message" | perl -CS -pe 's/"/\\"/g' 2>/dev/null || echo "$message")",
  "config_name": "$CONFIG_NAME",
  "scope": "$CONFIG_SCOPE",
  "target_file": "$MCP_FILE"
}
EOF
  exit $([ "$success" = "true" ] && echo 0 || echo 1)
}

# ---------- 确保目录存在 ----------
ensure_dir() {
  if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
  fi
}

# ---------- 安装: 从命令行参数 ----------
install_from_args() {
  local cmd="$1"
  shift || true
  local args=("$@")

  ensure_dir

  # 通过临时文件传递参数，避免 heredoc 嵌入（保护 args 中的敏感信息）
  local tmpfile_args
  tmpfile_args=$(mktemp 2>/dev/null || mktemp -t cbargs 2>/dev/null)
  trap 'rm -f "$tmpfile_args"' EXIT

  # 将 args 写入临时文件（按行存储）
  for a in "${args[@]}"; do
    printf '%s\n' "$a" >> "$tmpfile_args"
  done

  local config_payload
  config_payload=$(python3 << PYEOF
import json, sys

config_name = "$CONFIG_NAME"
cmd = "$cmd"
mcp_file = "$MCP_FILE"
args_file = "$tmpfile_args"

# 从临时文件读取 args（避免 shell 注入和敏感信息嵌入 heredoc）
args = []
try:
    with open(args_file) as f:
        args = [line.rstrip('\n') for line in f if line.rstrip('\n')]
except:
    pass

config = {
    config_name: {
        "type": "stdio",
        "command": cmd,
        "args": args,
        "description": "MCP Server: " + config_name + " (installed by config-manager)"
    }
}

try:
    with open(mcp_file) as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}

if "mcpServers" not in data:
    data["mcpServers"] = {}

data["mcpServers"].update(config)

with open(mcp_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(json.dumps({"success": True, "message": "MCP Server '" + config_name + "' 安装成功"}))
PYEOF
) || { output_result false "安装 MCP Server 失败" "Python 执行错误"; return 1; }

  # 清理临时文件
  rm -f "$tmpfile_args"
  trap - EXIT

  # 输出结果前确保不包含敏感信息
  echo "$config_payload" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps({'success':d.get('success'),'message':'MCP Server 安装完成'}))" 2>/dev/null || echo "$config_payload"
  exit 0
}

# ---------- 安装: 从 JSON 配置块（通过 stdin 传递，避免 heredoc 嵌入） ----------
install_from_json() {
  local json_payload="$1"
  ensure_dir

  # 通过 stdin 传递 JSON payload（避免 heredoc 嵌入，保护敏感数据）
  printf '%s' "$json_payload" | python3 << PYEOF
import json, sys

payload_str = sys.stdin.read()
target_file = "$MCP_FILE"
config_name = "$CONFIG_NAME"

try:
    new_config = json.loads(payload_str)
except json.JSONDecodeError as e:
    print(json.dumps({"success": False, "error": "JSON 解析错误（详情已隐藏）"}))
    sys.exit(1)

try:
    with open(target_file) as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}

if "mcpServers" not in data:
    data["mcpServers"] = {}

if "mcpServers" in new_config and isinstance(new_config["mcpServers"], dict):
    data["mcpServers"].update(new_config["mcpServers"])
elif config_name in new_config:
    data["mcpServers"][config_name] = new_config[config_name]
else:
    data["mcpServers"].update(new_config)

with open(target_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(json.dumps({"success": True, "message": f"MCP Server '{config_name}' 配置已更新"}))
PYEOF
}

# ---------- 安装: 从 URL 获取配置（对 URL 做脱敏处理） ----------
install_from_url() {
  local url="$1"
  # 对 URL 做脱敏：遮盖查询参数中的密钥/令牌
  local safe_url
  safe_url=$(printf '%s' "$url" | perl -pe 's/([?&](token|key|api_key|secret|password)=)[^&]*/\1****/gi' 2>/dev/null || echo "$url")
  echo "正在从 $safe_url 获取配置..."

  local config_data
  config_data=$(curl -sL --connect-timeout 10 "$url" 2>/dev/null || wget -qO- --timeout=10 "$url" 2>/dev/null || echo "")

  if [ -z "$config_data" ]; then
    output_result false "从 URL 获取配置失败" "无法访问: $safe_url"
  fi

  # 尝试作为 JSON 解析
  if echo "$config_data" | python3 -c "import json,sys; json.load(sys.stdin)" 2>/dev/null; then
    install_from_json "$config_data"
  else
    output_result false "URL 内容不是有效 JSON" "请检查 URL: $safe_url"
  fi
}

# =============================================================================
# 主分派
# =============================================================================

case "${1:-}" in
  --json)
    shift
    install_from_json "$*"
    ;;
  --url)
    shift
    install_from_url "$1"
    ;;
  *)
    if [ $# -ge 1 ]; then
      install_from_args "$@"
    else
      # 交互式模式 - 提示用户输入命令
      echo "请输入 MCP Server 的启动命令 (如: python, npx):"
      read -r cmd
      echo "请输入启动参数 (以空格分隔，直接回车跳过):"
      read -r args_line
      if [ -n "$args_line" ]; then
        # shellcheck disable=SC2086
        set -- $args_line
        install_from_args "$cmd" "$@"
      else
        install_from_args "$cmd"
      fi
    fi
    ;;
esac
