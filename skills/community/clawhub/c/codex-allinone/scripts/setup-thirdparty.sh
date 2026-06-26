#!/usr/bin/env bash
# setup-thirdparty.sh — 配置第三方 OpenAI 兼容模型服务（v7: all-via-relay 架构）
#
# 用法:
#   bash setup-thirdparty.sh kimi     "<Key>" [model]
#   bash setup-thirdparty.sh deepseek "<Key>" [model]
#   bash setup-thirdparty.sh arkv3    "<Key>" [model]
#   bash setup-thirdparty.sh custom   "<Key>" "<model>" "<base_url>"
#
# v7 架构说明:
#   Codex CLI 0.130+ 默认发 OpenAI Responses 协议,而多数第三方服务只支持 Chat。
#   因此除 arkv3(原生 Responses)外,其他 provider 都通过 codex-relay 协议中转。
#
#   provider  端口   说明
#   --------  -----  ----------------------------------------------------
#   kimi      4447   Moonshot 仅支持 Chat,必须 relay
#   deepseek  4448   DeepSeek 仅支持 Chat,必须 relay
#   arkv3     —      火山方舟 v3 原生支持 Responses,直连
#   custom    4449   自动探测:支持 Responses 直连;否则 relay
#
# 功能:
#   1. 将对应的 API Key 保存到 ~/.bashrc
#   2. 写入对应的 profile 配置文件
#   3. 将 codex 的配置指向该文件(如有旧配置会先备份)
#   4. 按需启动 codex-relay
#   5. 自动恢复命令已由 setup-agentplan / 通用 .bashrc 块负责

set -e

PROVIDER="${1:-}"
KEY="${2:-}"
CUSTOM_MODEL="${3:-}"
CUSTOM_BASE_URL="${4:-}"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$SKILL_DIR/scripts"
CODEX_DIR="$HOME/.codex"
PROFILES_DIR="$CODEX_DIR/profiles"

# 加载共享工具函数
. "$SCRIPT_DIR/relay-helper.sh"

log() { printf '\033[1;36m[%s]\033[0m %s\n' "$PROVIDER" "$*"; }
err() { printf '\033[1;31m[%s]\033[0m %s\n' "${PROVIDER:-setup}" "$*" >&2; }

if [ -z "$PROVIDER" ] || [ -z "$KEY" ]; then
  err "用法: bash setup-thirdparty.sh <provider> \"<Key>\" [model] [base_url]"
  err "可选 provider: kimi | deepseek | arkv3 | custom"
  exit 1
fi

case "$PROVIDER" in
  kimi|deepseek|arkv3|custom) ;;
  *)
    err "不支持的 provider: $PROVIDER"
    err "支持的选项: kimi | deepseek | arkv3 | custom"
    exit 1
    ;;
esac

# custom 必须额外提供 model 和 base_url
if [ "$PROVIDER" = "custom" ]; then
  if [ -z "$CUSTOM_MODEL" ] || [ -z "$CUSTOM_BASE_URL" ]; then
    err "自定义模式必须提供 3 个参数: <Key> <model> <base_url>"
    err "用法: bash setup-thirdparty.sh custom \"<Key>\" \"<model>\" \"<base_url>\""
    err "示例: bash setup-thirdparty.sh custom \"sk-xxx\" \"qwen-max\" \"https://dashscope.aliyuncs.com/compatible-mode/v1\""
    exit 1
  fi
fi

mkdir -p "$PROFILES_DIR"

ENV_KEY_NAME="$(profile_env_key_name "$PROVIDER")"
TMPL="$SKILL_DIR/profiles/${PROVIDER}.toml"
PROFILE_FILE="$PROFILES_DIR/${PROVIDER}.toml"

if [ ! -f "$TMPL" ]; then
  err "找不到配置模板: $TMPL"
  exit 1
fi

# ============================================================
# 步骤 1: 保存 API Key 到 ~/.bashrc
# ============================================================
sed -i "/^export $ENV_KEY_NAME=/d" "$HOME/.bashrc" 2>/dev/null || true
echo "export $ENV_KEY_NAME=\"$KEY\"" >> "$HOME/.bashrc"
export "$ENV_KEY_NAME=$KEY"
log "步骤 1/4: $ENV_KEY_NAME 已保存到 ~/.bashrc"

# ============================================================
# 步骤 2: 决定走 relay 还是直连,然后写 profile
# ============================================================
USE_RELAY="no"
RELAY_PORT=""
RELAY_UPSTREAM=""
EFFECTIVE_BASE_URL=""

case "$PROVIDER" in
  kimi)
    USE_RELAY="yes"
    RELAY_PORT="4447"
    RELAY_UPSTREAM="https://api.moonshot.cn/v1"
    EFFECTIVE_BASE_URL="http://127.0.0.1:${RELAY_PORT}/v1"
    ;;
  deepseek)
    USE_RELAY="yes"
    RELAY_PORT="4448"
    RELAY_UPSTREAM="https://api.deepseek.com/v1"
    EFFECTIVE_BASE_URL="http://127.0.0.1:${RELAY_PORT}/v1"
    ;;
  arkv3)
    USE_RELAY="no"
    EFFECTIVE_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
    ;;
  custom)
    # 自动探测上游是否原生支持 Responses API
    log "正在探测 $CUSTOM_BASE_URL 是否原生支持 Responses API..."
    if probe_responses_support "$CUSTOM_BASE_URL" "$KEY"; then
      log "  → 上游原生支持 Responses,直连无需 relay"
      USE_RELAY="no"
      EFFECTIVE_BASE_URL="$CUSTOM_BASE_URL"
    else
      log "  → 上游仅支持 Chat,将通过本地 relay (端口 4449) 翻译"
      USE_RELAY="yes"
      RELAY_PORT="4449"
      RELAY_UPSTREAM="$CUSTOM_BASE_URL"
      EFFECTIVE_BASE_URL="http://127.0.0.1:${RELAY_PORT}/v1"
      # 持久化上游 URL,供 .bashrc 自动恢复使用
      echo "$CUSTOM_BASE_URL" > "$CODEX_DIR/custom-upstream"
    fi
    ;;
esac

# 渲染 profile
if [ "$PROVIDER" = "custom" ]; then
  sed -e "s|__MODEL__|$CUSTOM_MODEL|g" \
      -e "s|__BASE_URL__|$EFFECTIVE_BASE_URL|g" \
      "$TMPL" > "$PROFILE_FILE"
else
  cp "$TMPL" "$PROFILE_FILE"
  if [ -n "$CUSTOM_MODEL" ]; then
    sed -i "s|^model = \".*\"|model = \"$CUSTOM_MODEL\"|" "$PROFILE_FILE"
  fi
fi
log "步骤 2/4: 配置文件已写入 $PROFILE_FILE"

# ============================================================
# 步骤 3: 激活该 profile (如有旧配置会先备份)
# ============================================================
if [ -f "$CODEX_DIR/config.toml" ] && [ ! -L "$CODEX_DIR/config.toml" ]; then
  BACKUP="$CODEX_DIR/config.toml.bak.$(date +%Y%m%d_%H%M%S)"
  cp "$CODEX_DIR/config.toml" "$BACKUP"
  log "  → 已备份你原有的 config.toml 到 $BACKUP"
fi
ln -sf "$PROFILE_FILE" "$CODEX_DIR/config.toml"
echo "$PROVIDER" > "$CODEX_DIR/active-profile"
log "步骤 3/4: 已激活 $PROVIDER 配置"

# ============================================================
# 步骤 4: 按需启动 codex-relay
# ============================================================
if [ "$USE_RELAY" = "yes" ]; then
  log "步骤 4/4: 启动 codex-relay (端口 $RELAY_PORT → $RELAY_UPSTREAM)..."
  ensure_codex_relay_installed || exit 3

  if relay_running "$RELAY_PORT"; then
    stop_relay_on_port "$RELAY_PORT"
  fi

  start_relay "$PROVIDER" "$RELAY_PORT" "$RELAY_UPSTREAM" || exit 3
  log "  → codex-relay 启动成功 (端口 $RELAY_PORT)"
else
  log "步骤 4/4: $PROVIDER 直连模式,无需 relay"
fi

# ============================================================
# 写入通用自动恢复命令(沙箱重启后自动重启对应端口的 relay)
# ============================================================
RELAY_AUTOSTART_MARKER='# [codex-allinone] auto-recover relay'
if ! grep -qF "$RELAY_AUTOSTART_MARKER" "$HOME/.bashrc" 2>/dev/null; then
  cat >> "$HOME/.bashrc" <<'EOF'

# [codex-allinone] auto-recover relay
if [ -f "$HOME/.codex/active-profile" ] && command -v codex-relay >/dev/null 2>&1; then
  __codex_profile="$(cat "$HOME/.codex/active-profile" 2>/dev/null | tr -d '[:space:]')"
  case "$__codex_profile" in
    agentplan) __codex_port=4446; __codex_upstream="https://ark.cn-beijing.volces.com/api/plan/v3"; __codex_env_key="ARK_API_KEY" ;;
    codingplan) __codex_port=4450; __codex_upstream="https://ark.cn-beijing.volces.com/api/coding/v3"; __codex_env_key="ARK_API_KEY" ;;
    kimi)      __codex_port=4447; __codex_upstream="https://api.moonshot.cn/v1"; __codex_env_key="MOONSHOT_API_KEY" ;;
    deepseek)  __codex_port=4448; __codex_upstream="https://api.deepseek.com/v1"; __codex_env_key="DEEPSEEK_API_KEY" ;;
    custom)    __codex_port=4449; __codex_upstream="$(cat "$HOME/.codex/custom-upstream" 2>/dev/null || echo)"; __codex_env_key="CUSTOM_API_KEY" ;;
    *)         __codex_port="" ;;
  esac
  if [ -n "$__codex_port" ] && [ -n "$__codex_upstream" ] && [ -n "$__codex_env_key" ]; then
    if ! (echo > /dev/tcp/127.0.0.1/$__codex_port) >/dev/null 2>&1; then
      __codex_key_value="$(eval echo \"\$$__codex_env_key\")"
      if [ -n "$__codex_key_value" ]; then
        CODEX_RELAY_API_KEY="$__codex_key_value" nohup codex-relay --port $__codex_port --upstream "$__codex_upstream" \
          > "$HOME/.codex-relay-${__codex_profile}.log" 2>&1 &
      fi
      unset __codex_key_value
    fi
  fi
  unset __codex_profile __codex_port __codex_upstream __codex_env_key
fi
EOF
  log "  → 已写入自动恢复命令到 ~/.bashrc"
fi

echo ""
log "✅ $PROVIDER 配置完成!"
log "   现在可以直接说编程需求,例如:"
log "   「用 codex 帮我写一个 Python 脚本」"
log ""
log "💡 需要切换到其他模型服务? 执行: bash switch-profile.sh"
