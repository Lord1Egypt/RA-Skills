#!/bin/bash
# =============================================================================
# CodeBuddy 配置状态检测脚本
# 用于检测 MCP/Skill/Plugin/Model/CLI 等配置是否已安装及当前状态
#
# 用法: ./check_status.sh <config_type> <config_name> [config_scope]
#
# 参数:
#   config_type  - 配置类型: mcp | skill | plugin | model | cli | other
#   config_name  - 配置项名称
#   config_scope - 作用域: global | project (默认: project)
#
# 输出: JSON 格式的状态报告
# =============================================================================

set -eo pipefail

# ---------- 参数解析 ----------
CONFIG_TYPE="${1:-}"
CONFIG_NAME="${2:-}"
CONFIG_SCOPE="${3:-project}"

if [ -z "$CONFIG_TYPE" ] || [ -z "$CONFIG_NAME" ]; then
  echo '{"error":true,"message":"Usage: check_status.sh <config_type> <config_name> [config_scope]"}'
  exit 1
fi

# ---------- 路径常量 ----------
HOME_DIR="$HOME"
PROJECT_DIR="$(cd "$(dirname "$0")/../../../.." 2>/dev/null && pwd || echo "")"

GLOBAL_MCP_FILE="$HOME_DIR/.codebuddy/mcp.json"
GLOBAL_SETTINGS_FILE="$HOME_DIR/.codebuddy/settings.json"
GLOBAL_SKILLS_DIR="$HOME_DIR/.codebuddy/skills-marketplace/skills"
GLOBAL_PLUGINS_DIR="$HOME_DIR/.codebuddy/plugins/marketplaces"

PROJECT_MCP_FILE="$PROJECT_DIR/.codebuddy/mcp.json"
PROJECT_SKILLS_DIR="$PROJECT_DIR/.codebuddy/skills"
PROJECT_CODEBUDDY_DIR="$PROJECT_DIR/.codebuddy"

# ---------- JSON 输出辅助函数 ----------
output_status() {
  local exists="$1"
  local status="$2"
  local version="$3"
  local needs_update="$4"
  local expected_version="$5"
  local details="$6"
  # JSON 转义（perl 兼容中文）
  details=$(printf '%s' "$details" | perl -CS -pe 's/"/\\"/g; s/\n/\\n/g' 2>/dev/null || echo "$details")
  cat <<EOF
{
  "exists": $exists,
  "status": "$status",
  "version": $( [ -z "$version" ] && echo 'null' || echo "\"$version\"" ),
  "needs_update": $needs_update,
  "expected_version": $( [ -z "$expected_version" ] && echo 'null' || echo "\"$expected_version\"" ),
  "details": "$details"
}
EOF
  exit 0
}

output_error() {
  local message="$1"
  local escaped_msg
  escaped_msg=$(printf '%s' "$message" | perl -CS -pe 's/"/\\"/g' 2>/dev/null || echo "$message")
  cat <<EOF
{
  "error": true,
  "message": "$escaped_msg"
}
EOF
  exit 1
}

# ---------- 版本比较函数 ----------
# 比较两个语义化版本号，若 current < expected 则返回 0 (需要更新)
version_lt() {
  [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$1" ] && [ "$1" != "$2" ]
}

# ---------- 检测 MCP Server ----------
check_mcp() {
  local mcp_file
  if [ "$CONFIG_SCOPE" = "global" ]; then
    mcp_file="$GLOBAL_MCP_FILE"
  else
    mcp_file="$PROJECT_MCP_FILE"
  fi

  # 检查文件是否存在
  if [ ! -f "$mcp_file" ]; then
    output_status false "not_found" "" false "" "MCP 配置文件不存在: $mcp_file"
  fi

  # 读取配置并检查指定 MCP Server
  if command -v python3 &>/dev/null; then
    local result
    result=$(python3 << PYEOF
import json, sys

mcp_file = "$mcp_file"
config_name = "$CONFIG_NAME"

try:
    with open(mcp_file) as f:
        data = json.load(f)
    servers = data.get('mcpServers', {})
    if config_name in servers:
        cfg = servers[config_name]
        ver = cfg.get('version', '')
        sys.stdout.write("EXISTS|enabled|" + ver)
    else:
        sys.stdout.write("NOT_FOUND|not_found|")
except Exception as e:
    sys.stdout.write("ERROR|error|" + str(e))
PYEOF
) 2>/dev/null || output_error "读取 MCP 配置文件失败: $mcp_file"

    local found=""; local status=""; local ver=""
    IFS='|' read -r found status ver <<< "${result:-|}" || true
    found="${found:-}"; status="${status:-}"; ver="${ver:-}"
    if [ "$found" = "EXISTS" ]; then
      output_status true "$status" "$ver" false "" "MCP Server '$CONFIG_NAME' 已配置，版本: ${ver:-未知}"
    elif [ "$found" = "NOT_FOUND" ]; then
      output_status false "not_found" "" false "" "MCP Server '$CONFIG_NAME' 未在 $mcp_file 中配置"
    else
      output_status false "error" "" false "" "读取 MCP 配置出错: $ver"
    fi
  else
    # 无 Python3 时用 grep 简易检测
    if grep -q "\"$CONFIG_NAME\"" "$mcp_file" 2>/dev/null; then
      local ver
      ver=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$mcp_file" 2>/dev/null | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"\(.*\)"/\1/')
      output_status true "enabled" "$ver" false "" "MCP Server '$CONFIG_NAME' 已配置（grep 检测）"
    else
      output_status false "not_found" "" false "" "MCP Server '$CONFIG_NAME' 未找到"
    fi
  fi
}

# ---------- 检测 Skill ----------
check_skill() {
  local skill_dir
  if [ "$CONFIG_SCOPE" = "global" ]; then
    skill_dir="$GLOBAL_SKILLS_DIR/$CONFIG_NAME"
  else
    skill_dir="$PROJECT_SKILLS_DIR/$CONFIG_NAME"
  fi

  if [ -d "$skill_dir" ]; then
    if [ -f "$skill_dir/SKILL.md" ]; then
      # 从 YAML frontmatter 读取版本
      local version=""
      if command -v python3 &>/dev/null; then
        version=$(python3 << PYEOF
import re, sys
skill_file = "$skill_dir/SKILL.md"
try:
    with open(skill_file) as f:
        content = f.read()
    match = re.search(r'^version:\s*([\d.]+)', content, re.MULTILINE)
    sys.stdout.write(match.group(1) if match else '')
except Exception:
    sys.stdout.write('')
PYEOF
) 2>/dev/null || version=""
      else
        version=$(grep -m1 '^version:' "$skill_dir/SKILL.md" 2>/dev/null | sed 's/^version:[[:space:]]*//')
      fi
      output_status true "enabled" "$version" false "" "Skill '$CONFIG_NAME' 已安装于 $skill_dir，版本: ${version:-未知}"
    else
      output_status true "disabled" "" false "" "Skill 目录 $skill_dir 存在但缺少 SKILL.md"
    fi
  else
    output_status false "not_found" "" false "" "Skill '$CONFIG_NAME' 未安装"
  fi
}

# ---------- 检测 Plugin ----------
check_plugin() {
  local settings_file="$GLOBAL_SETTINGS_FILE"

  if [ ! -f "$settings_file" ]; then
    output_status false "not_found" "" false "" "全局 settings.json 不存在"
  fi

  if command -v python3 &>/dev/null; then
    local result
    result=$(python3 << PYEOF
import json, sys

settings_file = "$settings_file"
config_name = "$CONFIG_NAME"

try:
    with open(settings_file) as f:
        data = json.load(f)
    plugins = data.get('enabledPlugins', {})
    found_key = None
    found_val = None
    for key, val in plugins.items():
        if key == config_name or key.startswith(config_name + '@'):
            found_key = key
            found_val = val
            break
    if found_key is not None:
        status = "enabled" if found_val else "disabled"
        sys.stdout.write("EXISTS|" + status + "|" + found_key)
    else:
        sys.stdout.write("NOT_FOUND|not_found|")
except Exception as e:
    sys.stdout.write("ERROR|error|" + str(e))
PYEOF
) 2>/dev/null || output_error "读取 settings.json 失败"

    local found=""; local status=""; local detail=""
    IFS='|' read -r found status detail <<< "${result:-|}" || true
    found="${found:-}"; status="${status:-}"; detail="${detail:-}"
    if [ "$found" = "EXISTS" ]; then
      output_status true "$status" "" false "" "Plugin '$CONFIG_NAME' 已启用（配置项: $detail）"
    elif [ "$found" = "NOT_FOUND" ]; then
      output_status false "not_found" "" false "" "Plugin '$CONFIG_NAME' 未在 settings.json 中配置"
    else
      output_status false "error" "" false "" "读取 Plugin 配置出错: $detail"
    fi
  else
    if grep -q "\"$CONFIG_NAME" "$settings_file" 2>/dev/null; then
      output_status true "enabled" "" false "" "Plugin '$CONFIG_NAME' 已启用（grep 检测）"
    else
      output_status false "not_found" "" false "" "Plugin '$CONFIG_NAME' 未配置"
    fi
  fi
}

# ---------- 检测 Model ----------
check_model() {
  # Model 配置主要通过 IDE UI，这里检测 settings.json 中的模型相关配置
  local settings_file="$GLOBAL_SETTINGS_FILE"
  local model_found=false
  local details=""

  if [ -f "$settings_file" ]; then
    if grep -qi "$CONFIG_NAME" "$settings_file" 2>/dev/null; then
      model_found=true
      details="settings.json 中包含 '$CONFIG_NAME' 相关配置"
    fi
  fi

  # 额外检测常见的模型环境变量
  if [ -n "${OPENAI_API_KEY:-}" ] || [ -n "${OPENAI_BASE_URL:-}" ] || [ -n "${DEEPSEEK_API_KEY:-}" ]; then
    if $model_found; then
      details="$details; 环境变量中检测到 API Key 配置"
    else
      model_found=true
      details="环境变量中检测到 API Key 配置"
    fi
  fi

  if $model_found; then
    output_status true "enabled" "" false "" "Model '$CONFIG_NAME': $details"
  else
    output_status false "not_found" "" false "" "Model '$CONFIG_NAME' 未检测到配置"
  fi
}

# ---------- 检测 CLI 工具 ----------
check_cli() {
  local bin_path
  bin_path=$(command -v "$CONFIG_NAME" 2>/dev/null || which "$CONFIG_NAME" 2>/dev/null || echo "")

  if [ -n "$bin_path" ]; then
    local version=""
    # 尝试获取版本号
    version=$("$CONFIG_NAME" --version 2>/dev/null || "$CONFIG_NAME" -v 2>/dev/null || "$CONFIG_NAME" version 2>/dev/null || echo "")
    # 清理输出去除非版本号部分，取第一行
    version=$(echo "$version" | head -1 | grep -oE '([0-9]+\.){1,3}[0-9]+' | head -1 || echo "")
    output_status true "enabled" "$version" false "" "CLI '$CONFIG_NAME' 已安装于 $bin_path${version:+"，版本: $version"}"
  else
    output_status false "not_found" "" false "" "CLI '$CONFIG_NAME' 未在 PATH 中找到"
  fi
}

# ---------- 检测 Other 类型 ----------
check_other() {
  # 对于未列明类型，尝试所有可能的检测方式，只要有匹配即返回
  local all_results=""

  # 尝试 skill
  local skill_dir_global="$GLOBAL_SKILLS_DIR/$CONFIG_NAME"
  local skill_dir_project="$PROJECT_SKILLS_DIR/$CONFIG_NAME"
  if [ -d "$skill_dir_global" ] || [ -d "$skill_dir_project" ]; then
    output_status true "enabled" "" false "" "'$CONFIG_NAME' 作为 Skill 已安装"
    return
  fi

  # 尝试 CLI
  if command -v "$CONFIG_NAME" &>/dev/null; then
    output_status true "enabled" "" false "" "'$CONFIG_NAME' 作为 CLI 工具已安装"
    return
  fi

  # 尝试 MCP
  for mcp_file in "$GLOBAL_MCP_FILE" "$PROJECT_MCP_FILE"; do
    if [ -f "$mcp_file" ] && grep -q "\"$CONFIG_NAME\"" "$mcp_file" 2>/dev/null; then
      output_status true "enabled" "" false "" "'$CONFIG_NAME' 作为 MCP Server 已配置"
      return
    fi
  done

  # 尝试 Plugin
  if [ -f "$GLOBAL_SETTINGS_FILE" ] && grep -q "\"$CONFIG_NAME" "$GLOBAL_SETTINGS_FILE" 2>/dev/null; then
    output_status true "enabled" "" false "" "'$CONFIG_NAME' 作为 Plugin 已配置"
    return
  fi

  output_status false "not_found" "" false "" "'$CONFIG_NAME' 在任何配置类型中均未找到"
}

# =============================================================================
# 主分派逻辑
# =============================================================================

case "$CONFIG_TYPE" in
  mcp)
    check_mcp
    ;;
  skill)
    check_skill
    ;;
  plugin)
    check_plugin
    ;;
  model)
    check_model
    ;;
  cli)
    check_cli
    ;;
  other)
    check_other
    ;;
  *)
    output_error "不支持的配置类型: $CONFIG_TYPE（支持: mcp, skill, plugin, model, cli, other）"
    ;;
esac
