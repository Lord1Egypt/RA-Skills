#!/usr/bin/env bash
# setup-agentplan.sh — 一键配置 AgentPlan 模式
#
# 用法:
#   bash setup-agentplan.sh "<AgentPlan 专属 Key>"
#   bash setup-agentplan.sh --auto         # 零感知:自动从 ArkClaw 沙箱注入的 ARK_API_KEY 取 Key
#
# 这个脚本会依次完成:
#   1. 将 ARK_API_KEY 保存到 ~/.bashrc(重启后仍然有效)
#   2. 写入 agentplan.toml 配置文件
#   3. 将 codex 的配置指向该文件(如果已有配置会先备份)
#   4. 安装并启动 codex-relay 协议转换服务(端口 4446)
#   5. 写入开机自动恢复命令
#
# --auto 模式(零感知配置):
#   ArkClaw / OpenClaw 沙箱会通过 OPENCLAW_SERVICE_MANAGED_ENV_KEYS 托管 ARK_API_KEY,
#   套餐归属由 ARK_AGENT_PLAN / ARK_CODING_PLAN 标识。当这些变量都已注入时,本脚本会
#   直接复用 $ARK_API_KEY,无需用户再粘贴。
#
# 为什么需要 codex-relay?
#   AgentPlan 服务端只支持 OpenAI Chat Completions API,而 Codex CLI 0.130+ 默认发
#   Responses 协议。codex-relay 在本机 4446 端口接 Responses 请求,翻译成 Chat
#   后转发给火山方舟。

set -e

ARG1="${1:-}"
AUTO_MODE="no"
KEY=""

if [ "$ARG1" = "--auto" ]; then
  AUTO_MODE="yes"
  # 从环境变量取 Key(沙箱托管的 ARK_API_KEY)
  KEY="${ARK_API_KEY:-}"
  if [ -z "$KEY" ]; then
    echo "❌ --auto 模式需要环境变量 ARK_API_KEY,但未注入。" >&2
    echo "   请改用: bash setup-agentplan.sh \"<你的 AgentPlan 专属 Key>\"" >&2
    exit 1
  fi
  is_agent_plan="$(printf '%s' "${ARK_AGENT_PLAN:-}" | tr '[:upper:]' '[:lower:]')"
  is_coding_plan="$(printf '%s' "${ARK_CODING_PLAN:-}" | tr '[:upper:]' '[:lower:]')"

  # 套餐分流: AgentPlan 与 Coding Plan 是两套独立套餐,Key 互不通用,base_url 也不一样:
  #   AgentPlan  -> https://ark.cn-beijing.volces.com/api/plan/v3   (relay 4446)
  #   CodingPlan -> https://ark.cn-beijing.volces.com/api/coding/v3 (relay 4450)
  # 所以 --auto 检测到 ARK_CODING_PLAN=true 时要转发到 setup-codingplan.sh,不能套用 AgentPlan profile
  if [ "$is_coding_plan" = "true" ] || [ "$is_coding_plan" = "1" ]; then
    if [ "$is_agent_plan" != "true" ] && [ "$is_agent_plan" != "1" ]; then
      echo "[AgentPlan] 检测到 ARK_CODING_PLAN=true,转发到 setup-codingplan.sh" >&2
      SCRIPT_DIR_FWD="$(cd "$(dirname "$0")" && pwd)"
      exec bash "$SCRIPT_DIR_FWD/setup-codingplan.sh" --auto
    fi
  fi

  if [ "$is_agent_plan" != "true" ] && [ "$is_agent_plan" != "1" ] \
     && [ "$is_coding_plan" != "true" ] && [ "$is_coding_plan" != "1" ]; then
    echo "⚠️  环境中未检测到 ARK_AGENT_PLAN=true 或 ARK_CODING_PLAN=true,但 ARK_API_KEY 已注入。" >&2
    echo "   仍按 AgentPlan 配置继续(若 Key 不匹配,后续 401 时请改用第三方分支)。" >&2
  fi
else
  KEY="$ARG1"
  if [ -z "$KEY" ]; then
    echo "❌ 缺少 AgentPlan Key。" >&2
    echo "   用法 1: bash setup-agentplan.sh \"<你的 AgentPlan 专属 Key>\"" >&2
    echo "   用法 2: bash setup-agentplan.sh --auto   # 零感知,从沙箱注入的 ARK_API_KEY 取" >&2
    echo "   Key 获取方式: 登录 AgentPlan 控制台 → 复制专属 Key" >&2
    exit 1
  fi
fi

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$SKILL_DIR/scripts"
CODEX_DIR="$HOME/.codex"
PROFILES_DIR="$CODEX_DIR/profiles"

# 加载共享工具函数
. "$SCRIPT_DIR/relay-helper.sh"

log() { printf '\033[1;36m[AgentPlan]\033[0m %s\n' "$*"; }

# ============================================================
# 步骤 0: 预校验 (本地格式 + 抗抖动 ping)
# ============================================================
if ! codex_format_check_key "$KEY"; then
  echo "❌ 你给的这串看起来不像一把有效的 Key。" >&2
  echo "   AgentPlan 的 Key 应该是一串 20 位以上的字母+数字(可能含 - 或 _)。" >&2
  echo "   请去火山方舟控制台 → AgentPlan 页面,完整复制专属 Key 后再发给我。" >&2
  exit 1
fi

# 直接 ping 上游 /models endpoint,不消耗推理 token
codex_ping_key "$KEY" "https://ark.cn-beijing.volces.com/api/plan/v3"
ping_ret=$?
case "$ping_ret" in
  0)
    log "步骤 0/5: Key 在线校验通过 ✅"
    ;;
  2)
    log "步骤 0/5: 网络抖动,跳过在线校验,直接写入配置(若运行时报 401 我会再处理)"
    ;;
  1)
    if [ "$AUTO_MODE" = "yes" ]; then
      is_coding_plan="$(printf '%s' "${ARK_CODING_PLAN:-}" | tr '[:upper:]' '[:lower:]')"
      if [ "$is_coding_plan" = "true" ] || [ "$is_coding_plan" = "1" ]; then
        echo "⚠️  AgentPlan 鉴权失败(HTTP 401),但当前账号也开通了 Coding Plan,自动切换中..." >&2
        SCRIPT_DIR_FWD="$(cd "$(dirname "$0")" && pwd)"
        exec bash "$SCRIPT_DIR_FWD/setup-codingplan.sh" --auto --from-fallback
      fi
    fi
    echo "❌ 用这把 Key 连火山方舟 AgentPlan 时被拒绝(HTTP 401/403)。" >&2
    echo "   通常的原因是:" >&2
    echo "   • Key 已过期或被回收 — 请去 ArkClaw 控制台刷新一下" >&2
    echo "   • 你贴的是 Coding Plan 的 Key,不是 AgentPlan 的" >&2
    echo "   • 你贴的是火山方舟普通 v3 Key,不是套餐专属 Key" >&2
    echo "   请确认后重新提供 Key,或告诉我用别的方式接入(Kimi/DeepSeek/自定义网关)" >&2
    exit 1
    ;;
esac

mkdir -p "$PROFILES_DIR"

# ============================================================
# 步骤 1: 保存 ARK_API_KEY 到 ~/.bashrc
# ============================================================
sed -i '/^export ARK_API_KEY=/d' "$HOME/.bashrc" 2>/dev/null || true
echo "export ARK_API_KEY=\"$KEY\"" >> "$HOME/.bashrc"
export ARK_API_KEY="$KEY"
log "步骤 1/5: ARK_API_KEY 已保存到 ~/.bashrc"

# ============================================================
# 步骤 2: 写入 profile 配置文件
# ============================================================
cp "$SKILL_DIR/profiles/agentplan.toml" "$PROFILES_DIR/agentplan.toml"
log "步骤 2/5: 配置文件已写入 $PROFILES_DIR/agentplan.toml"

# ============================================================
# 步骤 3: 激活该 profile(如果有旧的自定义配置会先备份)
# ============================================================
if [ -f "$CODEX_DIR/config.toml" ] && [ ! -L "$CODEX_DIR/config.toml" ]; then
  BACKUP="$CODEX_DIR/config.toml.bak.$(date +%Y%m%d_%H%M%S)"
  cp "$CODEX_DIR/config.toml" "$BACKUP"
  log "  → 已备份你原有的 config.toml 到 $BACKUP"
fi
ln -sf "$PROFILES_DIR/agentplan.toml" "$CODEX_DIR/config.toml"
echo "agentplan" > "$CODEX_DIR/active-profile"
log "步骤 3/5: 已激活 AgentPlan 配置"

# ============================================================
# 步骤 4: 安装并启动 codex-relay(端口 4446)
# ============================================================
log "步骤 4/5: 准备 codex-relay 协议转换服务..."
ensure_codex_relay_installed || exit 3

# 端口已被占用就先停掉旧进程
if relay_running 4446; then
  stop_relay_on_port 4446
fi

start_relay "agentplan" 4446 "https://ark.cn-beijing.volces.com/api/plan/v3" || exit 3
log "  → codex-relay 启动成功 (端口 4446)"

# ============================================================
# 步骤 5: 写入自动恢复命令(沙箱重启后自动生效)
# ============================================================
# 通用恢复脚本:根据 active-profile 启动对应端口的 relay,适用于所有需要 relay 的 profile
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
  log "步骤 5/5: 已写入自动恢复命令到 ~/.bashrc"
fi

echo ""
if [ "$AUTO_MODE" = "yes" ]; then
  log "✅ AgentPlan 配置已自动完成 (使用沙箱注入的 ARK_API_KEY,无需粘贴 Key)"
else
  log "✅ AgentPlan 配置全部完成!"
fi
log "   现在可以直接说编程需求,例如:"
log "   「用 codex 帮我重构 utils.py」"
