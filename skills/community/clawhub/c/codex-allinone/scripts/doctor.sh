#!/usr/bin/env bash
# doctor.sh — 输出当前环境状态(JSON 格式),供 skill 决策使用 (v7)
#
# 每次 skill 被触发时都会先运行本脚本,根据输出的 JSON 判断:
#   - 是否需要安装 Codex CLI
#   - 当前配置属于谁(本 skill / 用户手动 / 无配置)
#   - 当前 profile 对应的 relay 是否在跑(端口随 profile 变化)
#   - 关键 Key 是否已设置
#
# 本脚本不修改任何文件,只读检测。

set -e

CODEX_DIR="$HOME/.codex"
PROFILES_DIR="$CODEX_DIR/profiles"
ACTIVE_FILE="$CODEX_DIR/active-profile"
CONFIG_TOML="$CODEX_DIR/config.toml"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# --- 检测 Codex CLI 是否安装 ---
codex_installed=false
codex_version=""
codex_outdated=false
MIN_VERSION="0.130.0"

if command -v codex >/dev/null 2>&1; then
  codex_installed=true
  codex_version="$(codex --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "")"
  if [ -n "$codex_version" ]; then
    if [ "$(printf '%s\n%s\n' "$MIN_VERSION" "$codex_version" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
      codex_outdated=true
    fi
  fi
fi

# --- 判断配置归属 ---
config_state="clean"
active_profile="null"
user_config_summary="null"

if [ -f "$ACTIVE_FILE" ]; then
  config_state="managed-by-skill"
  active_profile="\"$(cat "$ACTIVE_FILE" | tr -d '[:space:]')\""
elif [ -f "$CONFIG_TOML" ]; then
  USER_PROVIDER="$(grep -E '^model_provider' "$CONFIG_TOML" 2>/dev/null | head -1 | sed -E 's/.*=\s*"([^"]*)".*/\1/')"
  USER_MODEL="$(grep -E '^model\s*=' "$CONFIG_TOML" 2>/dev/null | head -1 | sed -E 's/.*=\s*"([^"]*)".*/\1/')"
  if [ -n "$USER_PROVIDER" ] || [ -n "$USER_MODEL" ]; then
    config_state="user-managed"
    user_config_summary="{\"model_provider\":\"$USER_PROVIDER\",\"model\":\"$USER_MODEL\"}"
  fi
fi

config_toml_exists=false
[ -f "$CONFIG_TOML" ] && config_toml_exists=true

# --- 决定当前 profile 应该用的 relay 端口 ---
# v7: 端口随 profile 变化
ACTIVE="$(echo "$active_profile" | tr -d '"')"
expected_relay_port=""
expected_relay_upstream=""
case "$ACTIVE" in
  agentplan) expected_relay_port=4446 ;;
  codingplan) expected_relay_port=4450 ;;
  kimi)      expected_relay_port=4447 ;;
  deepseek)  expected_relay_port=4448 ;;
  custom)
    # custom 看是否存了上游 URL,存了就要 relay
    if [ -f "$CODEX_DIR/custom-upstream" ]; then
      expected_relay_port=4449
    fi
    ;;
  arkv3|null|"") : ;;   # 直连,不需要 relay
esac

relay_running=false
if [ -n "$expected_relay_port" ]; then
  if (echo > /dev/tcp/127.0.0.1/$expected_relay_port) >/dev/null 2>&1; then
    relay_running=true
  fi
fi

# --- relay 鉴权闭环检查 (v3.2) ---
# 端口在 ≠ 上游真的能通,常见 bug:relay 启动时没拿到 Key,导致所有请求 401。
# 用一个轻量 probe 调用 relay 的 /v1/chat/completions:
#   200/400/422 = 关键字段问题或正常 → relay 自身有 Key,健康
#   401/403     = relay 缺 Key 或 Key 失效 → 不健康
#   其它       = 无法判断,保守视为健康
relay_auth_healthy="null"
if [ "$relay_running" = true ] && [ -n "$expected_relay_port" ]; then
  __probe_code=$(curl -sS -o /dev/null -w "%{http_code}" \
    --max-time 4 \
    -X POST "http://127.0.0.1:${expected_relay_port}/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d '{"model":"probe","messages":[{"role":"user","content":"ping"}],"max_tokens":1}' 2>/dev/null || echo "000")
  case "$__probe_code" in
    401|403) relay_auth_healthy=false ;;
    2*|400|404|405|422) relay_auth_healthy=true ;;
    *) relay_auth_healthy="null" ;;
  esac
fi

# --- 检测各 provider 的 Key 是否设置 ---
ark_api_key_set=false
moonshot_api_key_set=false
deepseek_api_key_set=false
ark_v3_api_key_set=false
custom_api_key_set=false

[ -n "${ARK_API_KEY:-}" ] && ark_api_key_set=true
[ -n "${MOONSHOT_API_KEY:-}" ] && moonshot_api_key_set=true
[ -n "${DEEPSEEK_API_KEY:-}" ] && deepseek_api_key_set=true
[ -n "${ARK_V3_API_KEY:-}" ] && ark_v3_api_key_set=true
[ -n "${CUSTOM_API_KEY:-}" ] && custom_api_key_set=true

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

# 兼容:有些 Key 写在 .bashrc 里但当前 shell 没 source
if [ "$config_state" = "managed-by-skill" ]; then
  case "$ACTIVE" in
    agentplan) [ "$ark_api_key_set" = false ] && grep -q '^export ARK_API_KEY=' "$HOME/.bashrc" 2>/dev/null && ark_api_key_set=true ;;
    codingplan) [ "$ark_api_key_set" = false ] && grep -q '^export ARK_API_KEY=' "$HOME/.bashrc" 2>/dev/null && ark_api_key_set=true ;;
    kimi)      [ "$moonshot_api_key_set" = false ] && grep -q '^export MOONSHOT_API_KEY=' "$HOME/.bashrc" 2>/dev/null && moonshot_api_key_set=true ;;
    deepseek)  [ "$deepseek_api_key_set" = false ] && grep -q '^export DEEPSEEK_API_KEY=' "$HOME/.bashrc" 2>/dev/null && deepseek_api_key_set=true ;;
    arkv3)     [ "$ark_v3_api_key_set" = false ] && grep -q '^export ARK_V3_API_KEY=' "$HOME/.bashrc" 2>/dev/null && ark_v3_api_key_set=true ;;
    custom)    [ "$custom_api_key_set" = false ] && grep -q '^export CUSTOM_API_KEY=' "$HOME/.bashrc" 2>/dev/null && custom_api_key_set=true ;;
  esac
fi

# --- 用户手动配置时,运行兼容性检查 ---
user_health="null"
if [ "$config_state" = "user-managed" ] && [ -x "$SKILL_DIR/scripts/health-check.sh" ]; then
  user_health="$(bash "$SKILL_DIR/scripts/health-check.sh" 2>/dev/null || echo 'null')"
fi

# --- 生成问题列表 ---
issues=()
if [ "$codex_installed" = false ]; then
  issues+=("\"Codex CLI 未安装\"")
elif [ "$codex_outdated" = true ]; then
  issues+=("\"Codex CLI 版本过旧($codex_version),需要 ≥ $MIN_VERSION\"")
fi

case "$ACTIVE" in
  agentplan)
    [ "$relay_running" = false ] && issues+=("\"AgentPlan 模式已激活,但 codex-relay 未运行(端口 4446)\"")
    [ "$ark_api_key_set" = false ] && issues+=("\"AgentPlan 模式已激活,但 ARK_API_KEY 未设置\"")
    ;;
  codingplan)
    [ "$relay_running" = false ] && issues+=("\"Coding Plan 模式已激活,但 codex-relay 未运行(端口 4450)\"")
    [ "$ark_api_key_set" = false ] && issues+=("\"Coding Plan 模式已激活,但 ARK_API_KEY 未设置\"")
    ;;
  kimi)
    [ "$relay_running" = false ] && issues+=("\"Kimi 模式已激活,但 codex-relay 未运行(端口 4447)\"")
    [ "$moonshot_api_key_set" = false ] && issues+=("\"Kimi 模式已激活,但 MOONSHOT_API_KEY 未设置\"")
    ;;
  deepseek)
    [ "$relay_running" = false ] && issues+=("\"DeepSeek 模式已激活,但 codex-relay 未运行(端口 4448)\"")
    [ "$deepseek_api_key_set" = false ] && issues+=("\"DeepSeek 模式已激活,但 DEEPSEEK_API_KEY 未设置\"")
    ;;
  arkv3)
    [ "$ark_v3_api_key_set" = false ] && issues+=("\"火山方舟 v3 模式已激活,但 ARK_V3_API_KEY 未设置\"")
    ;;
  custom)
    [ "$custom_api_key_set" = false ] && issues+=("\"自定义模式已激活,但 CUSTOM_API_KEY 未设置\"")
    if [ -n "$expected_relay_port" ] && [ "$relay_running" = false ]; then
      issues+=("\"自定义模式需要 codex-relay(端口 $expected_relay_port),但当前未运行\"")
    fi
    ;;
esac

if [ "$config_state" = "clean" ] && [ "$codex_installed" = true ]; then
  issues+=("\"Codex CLI 已安装但尚未配置模型服务,请选择 AgentPlan 或第三方 Key\"")
fi

# relay 鉴权闭环异常 — 端口活着但调用 401 = relay 启动时没拿到 Key
if [ "$relay_auth_healthy" = false ]; then
  issues+=("\"本地协议中转服务已启动但鉴权失败(可能启动时未注入 Key),需要重启 relay\"")
fi

# --- 输出 JSON ---
expected_relay_port_json="null"
[ -n "$expected_relay_port" ] && expected_relay_port_json="$expected_relay_port"

issues_json="$(IFS=,; echo "${issues[*]}")"
cat <<EOF
{
  "codex_installed": $codex_installed,
  "codex_version": "$codex_version",
  "codex_outdated": $codex_outdated,
  "config_state": "$config_state",
  "active_profile": $active_profile,
  "user_config_summary": $user_config_summary,
  "user_health": $user_health,
  "config_toml_exists": $config_toml_exists,
  "expected_relay_port": $expected_relay_port_json,
  "relay_running": $relay_running,
  "relay_auth_healthy": $relay_auth_healthy,
  "ark_api_key_set": $ark_api_key_set,
  "moonshot_api_key_set": $moonshot_api_key_set,
  "deepseek_api_key_set": $deepseek_api_key_set,
  "ark_v3_api_key_set": $ark_v3_api_key_set,
  "custom_api_key_set": $custom_api_key_set,
  "ark_managed_env": $ark_managed_env,
  "ark_agent_plan": $ark_agent_plan,
  "ark_coding_plan": $ark_coding_plan,
  "ark_api_key_managed": $ark_api_key_managed,
  "ark_model_id": "$ark_model_id",
  "issues": [$issues_json]
}
EOF
