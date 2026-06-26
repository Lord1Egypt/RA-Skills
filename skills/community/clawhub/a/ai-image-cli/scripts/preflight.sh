#!/usr/bin/env bash
# preflight.sh — ai-image-cli 环境预检
#
# 检测 ai-image-cli 安装状态、认证配置和连通性。
# 输出 JSON 到 stdout，AI 根据结果决定下一步操作。
#
# 用法: bash preflight.sh [--install-hint]

set -euo pipefail

# ===================== 参数解析 =====================

INSTALL_HINT=false

usage() {
  cat >&2 <<'USAGE'
用法: bash preflight.sh [--install-hint]

检测 ai-image-cli 环境就绪状态。

选项:
  --install-hint  在 issues 中附加安装命令提示
  -h, --help      显示此帮助信息

输出 (stdout): JSON 格式检测结果
退出码: 0=检测完成(不论是否就绪), 1=脚本自身错误, 2=用法错误
USAGE
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --install-hint) INSTALL_HINT=true; shift ;;
    -h|--help) usage ;;
    *) echo "未知参数: $1" >&2; usage ;;
  esac
done

# ===================== 工具函数 =====================

# JSON 字符串转义（处理反斜杠、双引号、换行、制表符）
json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

# ===================== 环境变量加载 =====================
#
# 核心逻辑：非交互式 shell（AI exec 命令、cron 等）不会加载 .bashrc，
# 因此 LANGBASE_TOKEN、ARK_API_KEY 等变量可能不存在。
# 需要主动尝试 source user.env（与 install.sh 的 setup_shell_env 一致）。

ENV_SOURCE="null"

# 候选 user. 路径（按优先级排列）
USER_ENV_CANDIDATES=(
  "${HOME:+${HOME}/.openclaw/user.env}"
  "/home/appops/.openclaw/user.env"
)

if [[ -n "${LANGBASE_TOKEN:-}" ]] || [[ -n "${ARK_API_KEY:-}" ]]; then
  # 环境变量已存在（交互式 shell 或 systemd EnvironmentFile 注入）
  ENV_SOURCE="inherited"
else
  # 遍历候选路径，找到第一个存在的 user.env 并 source
  for candidate in "${USER_ENV_CANDIDATES[@]}"; do
    # 跳过空字符串（HOME 未设置时 candidate 为空）
    [[ -z "$candidate" ]] && continue
    if [[ -f "$candidate" ]]; then
      set -a
      # shellcheck source=/dev/null
      source "$candidate"
      set +a
      ENV_SOURCE="user.env"
      break
    fi
  done
fi

# ===================== 检测项 =====================

CLI_INSTALLED=false
CLI_VERSION="null"
AUTH_CONFIGURED=false
AUTH_METHOD="null"
CONNECTIVITY=false
ISSUES=()

# --- 1. CLI 安装检测 ---
if command -v ai-image >/dev/null 2>&1; then
  CLI_INSTALLED=true
  # 获取版本号
  version_output=$(ai-image --version 2>/dev/null || true)
  if [[ -n "$version_output" ]]; then
    CLI_VERSION="$version_output"
  fi
else
  # 尝试 python -m 方式（pip --user 安装后可能不在 PATH 中）
  export PATH="${HOME:+${HOME}/.local/bin}:${PATH}"
  if command -v ai-image >/dev/null 2>&1; then
    CLI_INSTALLED=true
    version_output=$(ai-image --version 2>/dev/null || true)
    if [[ -n "$version_output" ]]; then
      CLI_VERSION="$version_output"
    fi
    ISSUES+=("ai-image 在 ~/.local/bin 中，建议将其加入 PATH")
  else
    ISSUES+=("ai-image 未安装")
    if [[ "$INSTALL_HINT" == true ]]; then
      script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
      ISSUES+=("安装命令: bash ${script_dir}/install.sh")
    fi
  fi
fi

# --- 2. 认证检测 ---
if [[ -n "${LANGBASE_TOKEN:-}" ]]; then
  AUTH_CONFIGURED=true
  AUTH_METHOD="langbase"
elif [[ -n "${ARK_API_KEY:-}" ]]; then
  AUTH_CONFIGURED=true
  AUTH_METHOD="direct"
else
  ISSUES+=("未配置认证: 需要 LANGBASE_TOKEN 或 ARK_API_KEY")
  if [[ "$ENV_SOURCE" == "null" ]]; then
    ISSUES+=("未找到 ~/.openclaw/user.env 文件")
  fi
fi

# --- 3. 连通性测试（仅在 CLI 已安装时执行） ---
if [[ "$CLI_INSTALLED" == true ]]; then
  # capabilities 子命令无需认证，验证 CLI 可正常运行
  caps_output=$(ai-image capabilities 2>/dev/null || true)
  if [[ -n "$caps_output" ]] && echo "$caps_output" | grep -q '"tools"' 2>/dev/null; then
    CONNECTIVITY=true
  else
    ISSUES+=("ai-image capabilities 命令执行异常")
  fi
fi

# --- 4. 综合判定 ---
READY=false
if [[ "$CLI_INSTALLED" == true ]] && [[ "$AUTH_CONFIGURED" == true ]] && [[ "$CONNECTIVITY" == true ]]; then
  READY=true
fi

# ===================== 输出 JSON =====================
# 手工构建 JSON，不依赖 jq（目标环境可能未安装 jq）

# 构建 issues 数组
issues_json="["
first=true
for issue in "${ISSUES[@]+"${ISSUES[@]}"}"; do
  if [[ "$first" == true ]]; then
    first=false
  else
    issues_json+=","
  fi
  issues_json+="\"$(json_escape "$issue")\""
done
issues_json+="]"

# 处理可能为 null 的字符串字段
if [[ "$CLI_VERSION" == "null" ]]; then
  version_json="null"
else
  version_json="\"$(json_escape "$CLI_VERSION")\""
fi

if [[ "$AUTH_METHOD" == "null" ]]; then
  auth_method_json="null"
else
  auth_method_json="\"$AUTH_METHOD\""
fi

if [[ "$ENV_SOURCE" == "null" ]]; then
  env_source_json="null"
else
  env_source_json="\"$ENV_SOURCE\""
fi

cat <<ENDJSON
{
  "ready": $READY,
  "cli_installed": $CLI_INSTALLED,
  "cli_version": $version_json,
  "auth_configured": $AUTH_CONFIGURED,
  "auth_method": $auth_method_json,
  "connectivity": $CONNECTIVITY,
  "issues": $issues_json,
  "env_source": $env_source_json
}
ENDJSON
