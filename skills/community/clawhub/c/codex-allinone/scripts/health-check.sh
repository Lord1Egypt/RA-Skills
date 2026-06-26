#!/usr/bin/env bash
# health-check.sh — 对用户已有的 codex 配置做兼容性检查
#
# 什么时候会调用?
#   当检测到用户手动写过 ~/.codex/config.toml(不是本 skill 生成的)时,
#   doctor.sh 会自动调用本脚本,检查现有配置能否正常运行 Codex CLI。
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

CONFIG_TOML="$HOME/.codex/config.toml"

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
if [ ! -f "$CONFIG_TOML" ]; then
  echo "{\"is_healthy\":false,\"checks\":[],\"issues\":[\"~/.codex/config.toml 文件不存在\"]}"
  exit 0
fi

# --- 从配置文件中提取关键字段 ---
MODEL_PROVIDER="$(grep -E '^model_provider' "$CONFIG_TOML" 2>/dev/null | head -1 | sed -E 's/.*=\s*"([^"]*)".*/\1/')"
MODEL="$(grep -E '^model\s*=' "$CONFIG_TOML" 2>/dev/null | head -1 | sed -E 's/.*=\s*"([^"]*)".*/\1/')"

# 提取对应 provider 配置段中的 base_url / wire_api / env_key
BASE_URL=""
WIRE_API=""
ENV_KEY=""
if [ -n "$MODEL_PROVIDER" ]; then
  PROVIDER_BLOCK="$(awk -v p="[model_providers.$MODEL_PROVIDER]" '
    $0 == p { in_block = 1; next }
    /^\[/ && in_block { exit }
    in_block { print }
  ' "$CONFIG_TOML")"
  BASE_URL="$(echo "$PROVIDER_BLOCK" | grep -E '^base_url' | head -1 | sed -E 's/.*=\s*"([^"]*)".*/\1/')"
  WIRE_API="$(echo "$PROVIDER_BLOCK" | grep -E '^wire_api' | head -1 | sed -E 's/.*=\s*"([^"]*)".*/\1/')"
  ENV_KEY="$(echo "$PROVIDER_BLOCK" | grep -E '^env_key' | head -1 | sed -E 's/.*=\s*"([^"]*)".*/\1/')"
fi

# ============================================================
# 检查 1: model_provider 字段是否已设置
# ============================================================
if [ -n "$MODEL_PROVIDER" ]; then
  add_check "model_provider_set" true "model_provider=$MODEL_PROVIDER"
else
  add_check "model_provider_set" false "配置文件中缺少 model_provider 字段,Codex 不知道该连接哪个服务"
fi

# ============================================================
# 检查 2: 对应的 provider 配置段中是否有 base_url
# ============================================================
if [ -n "$MODEL_PROVIDER" ]; then
  if [ -n "$BASE_URL" ]; then
    add_check "base_url_defined" true "base_url=$BASE_URL"
  else
    add_check "base_url_defined" false "[model_providers.$MODEL_PROVIDER] 段中缺少 base_url,Codex 不知道请求发往哪里"
  fi
fi

# ============================================================
# 检查 3: wire_api 协议是否有效
# ============================================================
# Codex 0.130+ 默认发 "responses";"chat" 仍可解析但已被官方标记 deprecated
# 老版本的 "chat_completions" 已彻底废弃
if [ -n "$WIRE_API" ]; then
  case "$WIRE_API" in
    responses)
      add_check "wire_api_valid" true "wire_api=$WIRE_API"
      ;;
    chat)
      add_check "wire_api_valid" true "wire_api=chat (已 deprecated,建议改为 responses + relay)"
      ;;
    *)
      add_check "wire_api_valid" false "wire_api=\"$WIRE_API\" 已不被支持,Codex 0.130+ 只接受 \"responses\" 或 \"chat\""
      ;;
  esac
fi

# ============================================================
# 检查 4: API Key 环境变量是否已设置
# ============================================================
if [ -n "$ENV_KEY" ]; then
  KEY_LINE="$(grep "^export $ENV_KEY=" "$HOME/.bashrc" 2>/dev/null | tail -1 || true)"
  if [ -n "$KEY_LINE" ]; then
    KEY_VAL="$(echo "$KEY_LINE" | sed -E "s/^export $ENV_KEY=\"?([^\"]*)\"?.*/\1/")"
    if [ -n "$KEY_VAL" ] && [ "$KEY_VAL" != "" ]; then
      add_check "env_key_set" true "$ENV_KEY 已设置(长度 ${#KEY_VAL} 字符)"
    else
      add_check "env_key_set" false "$ENV_KEY 存在但值为空,Codex 连接时会被拒绝(401)"
    fi
  else
    # 也检查当前 shell 环境
    CUR_VAL="$(eval "echo \${$ENV_KEY:-}")"
    if [ -n "$CUR_VAL" ]; then
      add_check "env_key_set" true "$ENV_KEY 在当前环境中已设置"
    else
      add_check "env_key_set" false "$ENV_KEY 未设置(~/.bashrc 和当前环境中都没找到),Codex 连接时会被拒绝(401)"
    fi
  fi
fi

# ============================================================
# 检查 5: 如果配置指向本地 relay (任意端口 4446-4449),检查 relay 是否在运行
# ============================================================
RELAY_PORT_DETECTED="$(echo "$BASE_URL" | grep -oE '127\.0\.0\.1:[0-9]+' | head -1 | cut -d: -f2)"
if [ -n "$RELAY_PORT_DETECTED" ]; then
  if (echo > /dev/tcp/127.0.0.1/$RELAY_PORT_DETECTED) >/dev/null 2>&1; then
    add_check "relay_running" true "codex-relay 服务正常运行(端口 $RELAY_PORT_DETECTED)"
  else
    add_check "relay_running" false "配置指向本地 127.0.0.1:$RELAY_PORT_DETECTED 但该服务未运行,Codex 会报 connection refused"
  fi
fi

# ============================================================
# 检查 6: 是否硬编码了采样参数(会导致火山方舟部分模型返回 400 错误)
# ============================================================
if grep -qE '^(temperature|top_p)\s*=' "$CONFIG_TOML"; then
  add_check "no_sampling_override" false "配置中硬编码了 temperature 或 top_p,部分模型不支持自定义采样参数,会返回 400 错误"
else
  add_check "no_sampling_override" true "未硬编码采样参数"
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
