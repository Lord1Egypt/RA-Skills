#!/bin/bash
# =============================================================================
# CodeBuddy CLI 工具安装/更新脚本
# 智能检测包管理器并安装 CLI 工具
#
# 用法: ./install_cli.sh <tool_name> [--version <version>] [--force]
#       ./install_cli.sh <tool_name> [--manager brew|npm|pip3|cargo|go]
#
# 参数:
#   tool_name    - CLI 工具名称
#   --version    - 指定版本（可选）
#   --force      - 强制重新安装
#   --manager    - 指定包管理器（可选，不指定则自动检测）
#
# 输出: JSON 格式的安装结果
# =============================================================================

set -eo pipefail

# ---------- 参数解析 ----------
TOOL_NAME="${1:-}"
SPECIFIC_VERSION=""
FORCE=false
MANAGER=""

shift 1 2>/dev/null || true
while [ $# -gt 0 ]; do
  case "$1" in
    --version) SPECIFIC_VERSION="${2:-}"; shift 2 ;;
    --force) FORCE=true; shift ;;
    --manager) MANAGER="${2:-}"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$TOOL_NAME" ]; then
  echo '{"success":false,"error":"Usage: install_cli.sh <tool_name> [--version <ver>] [--force] [--manager brew|npm|pip3|cargo|go]"}'
  exit 1
fi

# ---------- JSON 输出 ----------
output_result() {
  local success="$1"
  local message="$2"
  local manager="${3:-}"
  local version="${4:-}"
  cat <<EOF
{
  "success": $success,
  "message": "$(echo "$message" | perl -CS -pe 's/"/\\"/g' 2>/dev/null || echo "$message")",
  "tool": "$TOOL_NAME",
  "manager": "$(echo "$manager" | perl -CS -pe 's/"/\\"/g' 2>/dev/null || echo "$manager")",
  "version": "$(echo "$version" | perl -CS -pe 's/"/\\"/g' 2>/dev/null || echo "$version")"
}
EOF
  exit $([ "$success" = "true" ] && echo 0 || echo 1)
}

# ---------- 包管理器检测 ----------
detect_managers() {
  local managers=()
  command -v brew &>/dev/null && managers+=("brew")
  command -v npm &>/dev/null && managers+=("npm")
  command -v pip3 &>/dev/null && managers+=("pip3")
  command -v cargo &>/dev/null && managers+=("cargo")
  command -v go &>/dev/null && managers+=("go")
  echo "${managers[@]}"
}

# ---------- 智能检测: 查找哪个包管理器能安装此工具 ----------
find_installer() {
  local tool="$1"
  local suggestions=""

  # brew
  if command -v brew &>/dev/null; then
    if brew search "$tool" 2>/dev/null | grep -qi "^${tool}$" 2>/dev/null; then
      echo "brew"
      return 0
    fi
  fi

  # npm （检查 npm 包是否存在）
  if command -v npm &>/dev/null; then
    if npm view "$tool" version &>/dev/null 2>&1; then
      echo "npm"
      return 0
    fi
  fi

  # pip3
  if command -v pip3 &>/dev/null; then
    if pip3 search "$tool" 2>/dev/null | grep -qi "^${tool} " 2>/dev/null; then
      echo "pip3"
      return 0
    fi
  fi

  # 如果没有找到特定包管理器，返回最佳猜测
  # 基于常见工具的默认选择
  case "$tool" in
    node|nodejs|npx|yarn|pnpm) echo "brew" ;;
    python|python3|pip|virtualenv) echo "brew" ;;
    go|golang) echo "brew" ;;
    rust|rustc) echo "brew" ;;
    ffmpeg|imagemagick|wget|curl|git) echo "brew" ;;
    typescript|ts-node|eslint|prettier|webpack) echo "npm" ;;
    black|flake8|mypy|pytest|jupyter) echo "pip3" ;;
    *) echo "brew" ;;  # 默认使用 brew
  esac
  return 0
}

# ---------- 通过 brew 安装 ----------
install_with_brew() {
  local version_flag=""
  [ -n "$SPECIFIC_VERSION" ] && version_flag="@$SPECIFIC_VERSION"

  echo "  → 使用 Homebrew 安装 $TOOL_NAME$version_flag ..."

  if $FORCE; then
    brew reinstall "$TOOL_NAME" 2>&1 || brew install "$TOOL_NAME" 2>&1
  else
    if brew list "$TOOL_NAME" &>/dev/null 2>&1; then
      echo "  → $TOOL_NAME 已安装，尝试升级..."
      brew upgrade "$TOOL_NAME" 2>&1 || true
    else
      brew install "$TOOL_NAME" 2>&1
    fi
  fi

  local exit_code=$?
  if [ $exit_code -eq 0 ]; then
    local ver
    ver=$("$TOOL_NAME" --version 2>/dev/null | head -1 || echo "unknown")
    output_result true "通过 Homebrew 安装成功" "brew" "$ver"
  else
    output_result false "Homebrew 安装失败 (exit: $exit_code)" "brew"
  fi
}

# ---------- 通过 npm 安装 ----------
install_with_npm() {
  local version_flag=""
  [ -n "$SPECIFIC_VERSION" ] && version_flag="@$SPECIFIC_VERSION"

  echo "  → 使用 npm 全局安装 $TOOL_NAME$version_flag ..."

  if $FORCE; then
    npm install -g "${TOOL_NAME}${version_flag}" --force 2>&1
  else
    npm install -g "${TOOL_NAME}${version_flag}" 2>&1
  fi

  local exit_code=$?
  if [ $exit_code -eq 0 ]; then
    local ver
    ver=$("$TOOL_NAME" --version 2>/dev/null | head -1 || echo "unknown")
    output_result true "通过 npm 全局安装成功" "npm" "$ver"
  else
    output_result false "npm 安装失败 (exit: $exit_code)" "npm"
  fi
}

# ---------- 通过 pip3 安装 ----------
install_with_pip3() {
  local version_flag=""
  [ -n "$SPECIFIC_VERSION" ] && version_flag=="==$SPECIFIC_VERSION"

  echo "  → 使用 pip3 安装 $TOOL_NAME$version_flag ..."

  if $FORCE; then
    pip3 install --force-reinstall "${TOOL_NAME}${version_flag}" 2>&1
  else
    pip3 install "${TOOL_NAME}${version_flag}" 2>&1
  fi

  local exit_code=$?
  if [ $exit_code -eq 0 ]; then
    local ver
    ver=$(pip3 show "$TOOL_NAME" 2>/dev/null | grep "^Version:" | awk '{print $2}' || echo "unknown")
    output_result true "通过 pip3 安装成功" "pip3" "$ver"
  else
    output_result false "pip3 安装失败 (exit: $exit_code)" "pip3"
  fi
}

# ---------- 通过 cargo 安装 ----------
install_with_cargo() {
  echo "  → 使用 cargo 安装 $TOOL_NAME ..."

  if $FORCE; then
    cargo install "$TOOL_NAME" --force 2>&1
  else
    cargo install "$TOOL_NAME" 2>&1
  fi

  local exit_code=$?
  if [ $exit_code -eq 0 ]; then
    local ver
    ver=$("$TOOL_NAME" --version 2>/dev/null | head -1 || echo "unknown")
    output_result true "通过 cargo 安装成功" "cargo" "$ver"
  else
    output_result false "cargo 安装失败 (exit: $exit_code)" "cargo"
  fi
}

# ---------- 通过 go install 安装 ----------
install_with_go() {
  echo "  → 使用 go install 安装 $TOOL_NAME ..."

  local ver_before
  if command -v "$TOOL_NAME" &>/dev/null; then
    ver_before=$("$TOOL_NAME" --version 2>/dev/null | head -1 || echo "")
  fi

  if go install "${TOOL_NAME}@latest" 2>&1; then
    local ver
    ver=$("$TOOL_NAME" --version 2>/dev/null | head -1 || echo "$ver_before")
    output_result true "通过 go install 安装成功" "go" "$ver"
  else
    output_result false "go install 失败" "go"
  fi
}

# =============================================================================
# 主逻辑
# =============================================================================

echo "═══════════════════════════════════════════"
echo "  CLI 工具安装: $TOOL_NAME"
echo "═══════════════════════════════════════════"

# 检查是否已安装
if command -v "$TOOL_NAME" &>/dev/null 2>&1; then
  current_ver=$("$TOOL_NAME" --version 2>/dev/null | head -1 || echo "已安装")
  echo "  当前状态: 已安装 ($current_ver)"

  if [ "$FORCE" = false ] && [ -z "$SPECIFIC_VERSION" ]; then
    echo "  使用 --force 强制重新安装，或 --version 指定版本"
    output_result true "CLI '$TOOL_NAME' 已安装" "auto" "$current_ver"
  fi
fi

# 确定包管理器
if [ -n "$MANAGER" ]; then
  echo "  使用指定包管理器: $MANAGER"
else
  MANAGER=$(find_installer "$TOOL_NAME")
  echo "  自动检测包管理器: $MANAGER"
fi

echo "  可用包管理器: $(detect_managers)"
echo "───────────────────────────────────────────"

# 按管理器执行安装
case "$MANAGER" in
  brew)  install_with_brew ;;
  npm)   install_with_npm ;;
  pip3)  install_with_pip3 ;;
  cargo) install_with_cargo ;;
  go)    install_with_go ;;
  *)
    # 尝试所有管理器
    echo "  尝试所有可用包管理器..."
    for mgr in $(detect_managers); do
      echo "  → 尝试 $mgr ..."
      case "$mgr" in
        brew)  install_with_brew;  exit $? ;;
        npm)   install_with_npm;   exit $? ;;
        pip3)  install_with_pip3;  exit $? ;;
        cargo) install_with_cargo; exit $? ;;
        go)    install_with_go;    exit $? ;;
      esac
    done
    output_result false "所有包管理器均安装失败" "auto"
    ;;
esac
