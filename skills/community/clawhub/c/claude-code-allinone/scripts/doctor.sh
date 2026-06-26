#!/usr/bin/env bash
# doctor.sh — 输出当前环境状态(JSON 格式),供 skill 决策使用
#
# 每次 skill 被触发时都会先运行本脚本,根据输出的 JSON 判断:
#   - 是否需要安装 Claude Code CLI
#   - 当前配置属于谁(本 skill / 用户手动 / 无配置)
#   - onboarding 是否标记完成
#   - 关键 Key 是否已设置
#
# 本脚本不修改任何文件,只读检测。

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- 检测 Claude Code CLI 是否安装 ---
claude_installed=false
claude_version=""
claude_outdated=false

if command -v claude >/dev/null 2>&1; then
  claude_installed=true
  claude_version="$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "")"
  if [ -n "$claude_version" ]; then
    if ! cc_version_ge "$claude_version" "$CC_MIN_VERSION"; then
      claude_outdated=true
    fi
  fi
fi

# --- 判断配置归属 ---
config_state="clean"
active_profile="null"
user_settings_summary="null"

if [ -f "$CC_ACTIVE_FILE" ]; then
  config_state="managed-by-skill"
  ap="$(tr -d '[:space:]' < "$CC_ACTIVE_FILE")"
  active_profile="\"$ap\""
elif [ -f "$CC_SETTINGS" ]; then
  USER_BASE_URL="$(cc_read_env_value ANTHROPIC_BASE_URL)"
  USER_MODEL="$(cc_read_env_value ANTHROPIC_MODEL)"
  if [ -n "$USER_BASE_URL" ] || [ -n "$USER_MODEL" ]; then
    config_state="user-managed"
    user_settings_summary="{\"base_url\":\"$USER_BASE_URL\",\"model\":\"$USER_MODEL\"}"
  fi
fi

settings_exists=false
[ -f "$CC_SETTINGS" ] && settings_exists=true

# --- onboarding 状态 ---
onboarding_complete=false
if [ -f "$CC_USER_JSON" ]; then
  if grep -q '"hasCompletedOnboarding"\s*:\s*true' "$CC_USER_JSON"; then
    onboarding_complete=true
  fi
fi

# --- token 文件 ---
token_set=false
[ -s "$CC_TOKEN_FILE" ] && token_set=true

# --- 各 provider 的 Key 是否设置 ---
ark_api_key_set=false
custom_api_key_set=false

[ -n "${ARK_API_KEY:-}" ] && ark_api_key_set=true
[ -n "${CUSTOM_ANTHROPIC_KEY:-}" ] && custom_api_key_set=true

# --- ArkClaw / OpenClaw 沙箱托管的环境变量探测 ---
# 沙箱通常会注入: ARK_API_KEY / ARK_MODEL_ID / ARK_AGENT_PLAN / ARK_CODING_PLAN
# 列在 OPENCLAW_SERVICE_MANAGED_ENV_KEYS 中的变量是被托管的
ark_managed_env=false
ark_agent_plan=false
ark_coding_plan=false
ark_api_key_managed=false
ark_model_id="${ARK_MODEL_ID:-}"

if [ -n "${OPENCLAW_SERVICE_MANAGED_ENV_KEYS:-}" ]; then
  ark_managed_env=true
  case ",${OPENCLAW_SERVICE_MANAGED_ENV_KEYS}," in
    *,ARK_API_KEY,*) ark_api_key_managed=true ;;
  esac
fi
case "$(printf '%s' "${ARK_AGENT_PLAN:-}" | tr '[:upper:]' '[:lower:]')" in
  true|1|yes) ark_agent_plan=true ;;
esac
case "$(printf '%s' "${ARK_CODING_PLAN:-}" | tr '[:upper:]' '[:lower:]')" in
  true|1|yes) ark_coding_plan=true ;;
esac

# 兼容: Key 写在 .bashrc 里但当前 shell 没 source
if [ "$config_state" = "managed-by-skill" ]; then
  ACTIVE="$(echo "$active_profile" | tr -d '"')"
  case "$ACTIVE" in
    agentplan) [ "$ark_api_key_set" = false ] && grep -q '^export ARK_API_KEY=' "$HOME/.bashrc" 2>/dev/null && ark_api_key_set=true ;;
    codingplan) [ "$ark_api_key_set" = false ] && grep -q '^export ARK_API_KEY=' "$HOME/.bashrc" 2>/dev/null && ark_api_key_set=true ;;
    custom)    [ "$custom_api_key_set" = false ] && grep -q '^export CUSTOM_ANTHROPIC_KEY=' "$HOME/.bashrc" 2>/dev/null && custom_api_key_set=true ;;
  esac
fi

# --- 用户手动配置时,运行兼容性检查 ---
user_health="null"
if [ "$config_state" = "user-managed" ] && [ -x "$SKILL_DIR/scripts/health-check.sh" ]; then
  user_health="$(bash "$SKILL_DIR/scripts/health-check.sh" 2>/dev/null || echo 'null')"
fi

# --- 生成问题列表 ---
issues=()
if [ "$claude_installed" = false ]; then
  issues+=("\"Claude Code CLI 未安装\"")
elif [ "$claude_outdated" = true ]; then
  issues+=("\"Claude Code CLI 版本过旧($claude_version),需要 ≥ $CC_MIN_VERSION\"")
fi

ACTIVE="$(echo "$active_profile" | tr -d '"')"
case "$ACTIVE" in
  agentplan)
    [ "$ark_api_key_set" = false ] && issues+=("\"AgentPlan 模式已激活,但 ARK_API_KEY 未设置\"")
    [ "$token_set" = false ] && issues+=("\"AgentPlan 模式已激活,但 ~/.claude/.token 未生成\"")
    ;;
  codingplan)
    [ "$ark_api_key_set" = false ] && issues+=("\"Coding Plan 模式已激活,但 ARK_API_KEY 未设置\"")
    [ "$token_set" = false ] && issues+=("\"Coding Plan 模式已激活,但 ~/.claude/.token 未生成\"")
    ;;
  custom)
    [ "$custom_api_key_set" = false ] && issues+=("\"自定义模式已激活,但 CUSTOM_ANTHROPIC_KEY 未设置\"")
    [ "$token_set" = false ] && issues+=("\"自定义模式已激活,但 ~/.claude/.token 未生成\"")
    ;;
esac

if [ "$config_state" = "managed-by-skill" ] && [ "$onboarding_complete" = false ]; then
  issues+=("\"~/.claude.json 缺少 hasCompletedOnboarding=true,运行 ensure-onboarding.sh 可修复\"")
fi

if [ "$config_state" = "clean" ] && [ "$claude_installed" = true ]; then
  issues+=("\"Claude Code CLI 已安装但尚未配置模型服务,请选择 AgentPlan 或自定义网关\"")
fi

# --- 输出 JSON ---
issues_json="$(IFS=,; echo "${issues[*]}")"
cat <<EOF
{
  "claude_installed": $claude_installed,
  "claude_version": "$claude_version",
  "claude_outdated": $claude_outdated,
  "config_state": "$config_state",
  "active_profile": $active_profile,
  "user_settings_summary": $user_settings_summary,
  "user_health": $user_health,
  "settings_exists": $settings_exists,
  "onboarding_complete": $onboarding_complete,
  "token_set": $token_set,
  "ark_api_key_set": $ark_api_key_set,
  "custom_api_key_set": $custom_api_key_set,
  "ark_managed_env": $ark_managed_env,
  "ark_agent_plan": $ark_agent_plan,
  "ark_coding_plan": $ark_coding_plan,
  "ark_api_key_managed": $ark_api_key_managed,
  "ark_model_id": "$ark_model_id",
  "issues": [$issues_json]
}
EOF
