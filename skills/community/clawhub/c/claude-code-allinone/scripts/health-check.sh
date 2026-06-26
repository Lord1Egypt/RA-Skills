#!/usr/bin/env bash
# health-check.sh — 对用户已有的 claude code 配置做兼容性检查
#
# 什么时候会调用?
#   当检测到用户手动写过 ~/.claude/settings.json (不是本 skill 生成的) 时,
#   doctor.sh 会自动调用本脚本,检查现有配置能否正常运行 Claude Code CLI。
#
# 输出: JSON 格式
#   {
#     "is_healthy": true/false,
#     "checks": [...],     // 每项检查的详细结果
#     "issues": [...]      // 不通过的项目(人话描述,可直接展示给用户)
#   }
#
# 本脚本不修改任何文件,只读检测。

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"

issues=()
checks=()

add_check() {
  local name="$1" ok="$2" detail="$3"
  checks+=("{\"name\":\"$name\",\"ok\":$ok,\"detail\":\"$detail\"}")
  if [ "$ok" = "false" ]; then
    issues+=("\"$detail\"")
  fi
}

# 文件不存在就直接返回
if [ ! -f "$CC_SETTINGS" ]; then
  echo "{\"is_healthy\":false,\"checks\":[],\"issues\":[\"~/.claude/settings.json 文件不存在\"]}"
  exit 0
fi

# --- 提取关键字段 (env 块下的几个常用变量) ---
BASE_URL="$(cc_read_env_value ANTHROPIC_BASE_URL)"
MODEL="$(cc_read_env_value ANTHROPIC_MODEL)"
USED_API_KEY_VAR=""
if grep -q 'ANTHROPIC_API_KEY' "$CC_SETTINGS"; then
  USED_API_KEY_VAR="ANTHROPIC_API_KEY"
elif grep -q 'ANTHROPIC_AUTH_TOKEN' "$CC_SETTINGS"; then
  USED_API_KEY_VAR="ANTHROPIC_AUTH_TOKEN"
fi

# ============================================================
# 检查 1: settings.json 是否合法 JSON
# ============================================================
if command -v jq >/dev/null 2>&1; then
  if jq -e . "$CC_SETTINGS" >/dev/null 2>&1; then
    add_check "settings_valid_json" true "settings.json 是合法 JSON"
  else
    add_check "settings_valid_json" false "~/.claude/settings.json 不是合法 JSON,Claude Code 启动会直接 abort"
  fi
else
  add_check "settings_valid_json" true "未安装 jq,跳过 JSON 合法性检查"
fi

# ============================================================
# 检查 2: ANTHROPIC_BASE_URL 是否设置
# ============================================================
if [ -n "$BASE_URL" ]; then
  add_check "base_url_set" true "base_url=$BASE_URL"
else
  add_check "base_url_set" false "settings.json 的 env 块缺少 ANTHROPIC_BASE_URL,Claude Code 不知道请求发往哪里"
fi

# ============================================================
# 检查 3: 用了 ANTHROPIC_AUTH_TOKEN 而不是 ANTHROPIC_API_KEY
# ============================================================
# ANTHROPIC_API_KEY 会被 CLI 强制走 anthropic.com 鉴权链路,境内 IDC 必然失败
case "$USED_API_KEY_VAR" in
  ANTHROPIC_AUTH_TOKEN|"")
    # 没在 env 块里写 Key 是 OK 的(可能用 apiKeyHelper)
    add_check "no_anthropic_api_key" true "未使用 ANTHROPIC_API_KEY (推荐)"
    ;;
  ANTHROPIC_API_KEY)
    add_check "no_anthropic_api_key" false "settings.json 使用了 ANTHROPIC_API_KEY,会被 CLI 强制走 anthropic.com 鉴权,境内 IDC 必然失败。请改用 ANTHROPIC_AUTH_TOKEN 或 apiKeyHelper"
    ;;
esac

# ============================================================
# 检查 4: 是否有 Key 来源 (env.ANTHROPIC_AUTH_TOKEN / apiKeyHelper / .token 文件)
# ============================================================
HAS_KEY_SOURCE=false
if grep -q 'ANTHROPIC_AUTH_TOKEN' "$CC_SETTINGS"; then HAS_KEY_SOURCE=true; fi
if grep -q 'apiKeyHelper' "$CC_SETTINGS"; then HAS_KEY_SOURCE=true; fi
if [ -s "$CC_TOKEN_FILE" ]; then HAS_KEY_SOURCE=true; fi

if [ "$HAS_KEY_SOURCE" = true ]; then
  add_check "key_source_available" true "找到至少一种 Key 来源 (env / apiKeyHelper / .token)"
else
  add_check "key_source_available" false "settings.json 没配 ANTHROPIC_AUTH_TOKEN / apiKeyHelper,~/.claude/.token 也不存在,Claude Code 连接时会被拒(401)"
fi

# ============================================================
# 检查 5: ~/.claude.json 标记 onboarding 完成
# ============================================================
if [ -f "$CC_USER_JSON" ] && grep -q '"hasCompletedOnboarding"\s*:\s*true' "$CC_USER_JSON"; then
  add_check "onboarding_complete" true "~/.claude.json hasCompletedOnboarding=true"
else
  add_check "onboarding_complete" false "~/.claude.json 缺少 hasCompletedOnboarding=true,Claude Code 在非交互模式下会直接 abort"
fi

# ============================================================
# 检查 6: ANTHROPIC_MODEL 是否设置
# ============================================================
if [ -n "$MODEL" ]; then
  add_check "model_set" true "model=$MODEL"
else
  add_check "model_set" false "settings.json 的 env 块缺少 ANTHROPIC_MODEL,部分自定义网关会找不到模型"
fi

# --- 输出 JSON ---
is_healthy=true
[ ${#issues[@]} -gt 0 ] && is_healthy=false

checks_json="$(IFS=,; echo "${checks[*]}")"
issues_json="$(IFS=,; echo "${issues[*]}")"

cat <<EOF
{
  "is_healthy": $is_healthy,
  "checks": [$checks_json],
  "issues": [$issues_json]
}
EOF
