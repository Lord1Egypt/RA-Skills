#!/bin/bash
# =============================================================================
# CodeBuddy Plugin 安装/启用脚本
# 安装或启用 CodeBuddy 插件
#
# 用法: ./install_plugin.sh <config_name> [config_scope] [--marketplace <marketplace>]
#       ./install_plugin.sh <config_name> [config_scope] [--disable]
#
# 参数:
#   config_name   - 插件名称（如 pptx, pdf 等）
#   config_scope  - 作用域 (仅 global，扩展支持)
#   --marketplace - 插件市场标识 (默认: codebuddy-plugins-official)
#   --disable     - 禁用插件而非启用
#
# 输出: JSON 格式的安装结果
# =============================================================================

set -eo pipefail

# ---------- 参数解析 ----------
CONFIG_NAME="${1:-}"
CONFIG_SCOPE="${2:-global}"
ACTION="enable"
MARKETPLACE="codebuddy-plugins-official"

# 解析剩余参数
shift 2 2>/dev/null || true
while [ $# -gt 0 ]; do
  case "$1" in
    --disable) ACTION="disable"; shift ;;
    --marketplace) MARKETPLACE="${2:-}"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$CONFIG_NAME" ]; then
  echo '{"success":false,"error":"Usage: install_plugin.sh <config_name> [scope] [--disable] [--marketplace <name>]"}'
  exit 1
fi

# ---------- 路径常量 ----------
SETTINGS_FILE="$HOME/.codebuddy/settings.json"
PLUGIN_KEY="${CONFIG_NAME}@${MARKETPLACE}"

# ---------- JSON 输出 ----------
output_result() {
  local success="$1"
  local message="$2"
  cat <<EOF
{
  "success": $success,
  "message": "$(echo "$message" | perl -CS -pe 's/"/\\"/g' 2>/dev/null || echo "$message")",
  "plugin": "$CONFIG_NAME",
  "key": "$PLUGIN_KEY",
  "action": "$ACTION",
  "target_file": "$SETTINGS_FILE"
}
EOF
  exit $([ "$success" = "true" ] && echo 0 || echo 1)
}

# ---------- 确保 settings.json 存在 ----------
ensure_settings() {
  if [ ! -f "$SETTINGS_FILE" ]; then
    # 创建空配置文件
    mkdir -p "$(dirname "$SETTINGS_FILE")"
    cat > "$SETTINGS_FILE" <<EOF
{
  "enabledPlugins": {}
}
EOF
  fi
}

# =============================================================================
# 主逻辑
# =============================================================================

ensure_settings

python3 << PYEOF
import json, sys, os

settings_file = "$SETTINGS_FILE"
plugin_key = "$PLUGIN_KEY"
action = "$ACTION"
config_name = "$CONFIG_NAME"

try:
    with open(settings_file) as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}

if "enabledPlugins" not in data:
    data["enabledPlugins"] = {}

plugins = data["enabledPlugins"]

if action == "enable":
    # 检查是否已存在（支持精确匹配和 @ 后缀匹配）
    already_enabled = False
    for key, val in plugins.items():
        if key == plugin_key or key == config_name:
            if val is True:
                already_enabled = True
            break

    if already_enabled:
        result = {"success": True, "message": f"Plugin '{config_name}' 已启用，无需操作"}
        sys.stdout.write(json.dumps(result))
        sys.exit(0)

    # 启用插件
    plugins[plugin_key] = True
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    result = {"success": True, "message": f"Plugin '{config_name}' 已启用（配置: {plugin_key}）"}
    sys.stdout.write(json.dumps(result))

elif action == "disable":
    # 禁用插件
    removed = False
    for key in list(plugins.keys()):
        if key == plugin_key or key == config_name or key.startswith(config_name + "@"):
            del plugins[key]
            removed = True

    if removed:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        result = {"success": True, "message": f"Plugin '{config_name}' 已禁用"}
    else:
        result = {"success": True, "message": f"Plugin '{config_name}' 未找到，无需禁用"}

    sys.stdout.write(json.dumps(result))

sys.exit(0)
PYEOF
