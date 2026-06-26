#!/usr/bin/env bash
# install.sh — 非交互式安装 ai-image-cli
#
# 从内部 PyPI 安装 ai-image-cli，自动处理环境变量和认证。
# 全程无交互，适合 AI 直接调用。
#
# 用法: bash install.sh [--user] [--upgrade]

set -euo pipefail

# ===================== 常量 =====================

PACKAGE_NAME="ai-image-cli"
DEFAULT_PYPI_HOST="music-pypi.hz.netease.com"
DEFAULT_PYPI_INDEX="http://avlab:avlab123@music-pypi.hz.netease.com/simple"

# ===================== 工具函数 =====================

json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

# 输出成功 JSON 到 stdout
print_success() {
  local version="$1"
  local note="${2:-}"
  if [[ -n "$note" ]]; then
    echo "{\"success\":true,\"version\":\"$(json_escape "$version")\",\"note\":\"$(json_escape "$note")\"}"
  else
    echo "{\"success\":true,\"version\":\"$(json_escape "$version")\"}"
  fi
}

# 输出失败 JSON 到 stdout 并以非零码退出
print_error() {
  local error="$1"
  echo "{\"success\":false,\"error\":\"$(json_escape "$error")\"}"
  exit 1
}

# ===================== 参数解析 =====================

USER_INSTALL=false
UPGRADE=false

usage() {
  cat >&2 <<'USAGE'
用法: bash install.sh [--user] [--upgrade]

非交互式安装 ai-image-cli。

选项:
  --user      用户级安装 (pip install --user)
  --upgrade   强制升级到最新版本
  -h, --help  显示此帮助信息

退出码: 0=安装成功, 1=安装失败, 2=用法错误
USAGE
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --user) USER_INSTALL=true; shift ;;
    --upgrade) UPGRADE=true; shift ;;
    -h|--help) usage ;;
    *) echo "未知参数: $1" >&2; usage ;;
  esac
done

# ===================== 环境变量加载 =====================
# 与 preflight.sh 相同：非交互式 shell 需要主动 source user.env

USER_ENV_CANDIDATES=(
  "${HOME:+${HOME}/.openclaw/user.env}"
  "/home/appops/.openclaw/user.env"
)

if [[ -z "${PIP_INDEX_URL:-}" ]] || [[ -z "${PIP_TRUSTED_HOST:-}" ]]; then
  for candidate in "${USER_ENV_CANDIDATES[@]}"; do
    [[ -z "$candidate" ]] && continue
    if [[ -f "$candidate" ]]; then
      set -a
      # shellcheck source=/dev/null
      source "$candidate"
      set +a
      echo "已从 $candidate 加载环境变量" >&2
      break
    fi
  done
fi

# 确保 PIP_TRUSTED_HOST 存在
PIP_TRUSTED_HOST="${PIP_TRUSTED_HOST:-$DEFAULT_PYPI_HOST}"
# 内部 PyPI 下载需要认证，如果 URL 指向内部仓库但没带凭证（缺少 @），强制用带认证的默认值
if [[ -z "${PIP_INDEX_URL:-}" ]]; then
  PIP_INDEX_URL="$DEFAULT_PYPI_INDEX"
elif [[ "$PIP_INDEX_URL" == *"$DEFAULT_PYPI_HOST"* ]] && [[ "$PIP_INDEX_URL" != *"@"* ]]; then
  echo "PIP_INDEX_URL 缺少认证凭证，使用内置默认值" >&2
  PIP_INDEX_URL="$DEFAULT_PYPI_INDEX"
fi
export PIP_TRUSTED_HOST PIP_INDEX_URL

# ===================== 检测 pip =====================

PIP_CMD=""
if command -v pip3 >/dev/null 2>&1; then
  PIP_CMD="pip3"
elif command -v pip >/dev/null 2>&1; then
  PIP_CMD="pip"
elif command -v python3 >/dev/null 2>&1; then
  PIP_CMD="python3 -m pip"
elif command -v python >/dev/null 2>&1; then
  PIP_CMD="python -m pip"
else
  print_error "未找到 pip 或 python，请先安装 Python 3.10+"
fi

# 验证 pip 可用
if ! $PIP_CMD --version >/dev/null 2>&1; then
  print_error "pip 命令不可用: $PIP_CMD"
fi

echo "使用 pip: $PIP_CMD" >&2

# ===================== 构建安装参数 =====================

INSTALL_ARGS=(install "$PACKAGE_NAME")

if [[ "$UPGRADE" == true ]]; then
  INSTALL_ARGS+=(--upgrade)
fi

if [[ "$USER_INSTALL" == true ]]; then
  INSTALL_ARGS+=(--user)
fi

# PIP_INDEX_URL 和 PIP_TRUSTED_HOST 通过环境变量传递，pip 自动识别

# ===================== 执行安装 =====================

echo "正在安装 ${PACKAGE_NAME}..." >&2

install_output=""
if install_output=$($PIP_CMD "${INSTALL_ARGS[@]}" 2>&1); then
  echo "pip install 成功" >&2
else
  # 全局安装失败时，自动 fallback 到 --user（仅当未指定 --user 时）
  if [[ "$USER_INSTALL" == false ]]; then
    echo "全局安装失败，尝试用户级安装 (--user)..." >&2
    INSTALL_ARGS+=(--user)
    if ! install_output=$($PIP_CMD "${INSTALL_ARGS[@]}" 2>&1); then
      print_error "pip install 失败（全局和用户级均失败）: $(echo "$install_output" | tail -3 | tr '\n' ' ')"
    fi
    echo "用户级安装成功" >&2
  else
    print_error "pip install --user 失败: $(echo "$install_output" | tail -3 | tr '\n' ' ')"
  fi
fi

# ===================== 验证安装 =====================

# --user 安装后 bin 可能在 ~/.local/bin，刷新 PATH
export PATH="${HOME:+${HOME}/.local/bin}:${PATH}"

if command -v ai-image >/dev/null 2>&1; then
  version=$(ai-image --version 2>/dev/null || echo "unknown")
  print_success "$version"
else
  # ai-image 不在 PATH，尝试 python -m 方式验证
  python_cmd=""
  if command -v python3 >/dev/null 2>&1; then
    python_cmd="python3"
  elif command -v python >/dev/null 2>&1; then
    python_cmd="python"
  fi

  if [[ -n "$python_cmd" ]] && $python_cmd -m ai_image --version >/dev/null 2>&1; then
    version=$($python_cmd -m ai_image --version 2>/dev/null || echo "unknown")
    print_success "$version" "ai-image 不在 PATH 中，请使用 $python_cmd -m ai_image 运行"
  else
    print_error "安装完成但验证失败: ai-image 命令不可用。尝试将 ~/.local/bin 加入 PATH"
  fi
fi
