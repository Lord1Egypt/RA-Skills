#!/usr/bin/env bash
# setup-agentplan.sh — 一键配置 AgentPlan 模式
#
# 用法:
#   bash setup-agentplan.sh "<AgentPlan 专属 Key>"
#   bash setup-agentplan.sh --auto         # 零感知:自动从 ArkClaw 沙箱注入的 ARK_API_KEY 取 Key
#
# 这个脚本会依次完成:
#   1. 将 ARK_API_KEY 保存到 ~/.bashrc(沙箱重启后仍然有效)
#   2. 把 Key 写入 ~/.claude/.token 文件(settings.json 的 apiKeyHelper 读它)
#   3. 写入 ~/.claude/profiles/agentplan.json (settings.json 模板)
#   4. 把 ~/.claude/settings.json 替换为该 profile 内容(已有则先备份)
#   5. 标记 ~/.claude.json hasCompletedOnboarding=true
#   6. 写 active-profile marker
#
# --auto 模式(零感知配置):
#   ArkClaw / OpenClaw 沙箱会通过 OPENCLAW_SERVICE_MANAGED_ENV_KEYS 托管 ARK_API_KEY,
#   套餐归属由 ARK_AGENT_PLAN / ARK_CODING_PLAN 标识。当这些变量都已注入时,本脚本会
#   直接复用 $ARK_API_KEY,无需用户再粘贴。

set -e

ARG1="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"

AUTO_MODE="no"
KEY=""

if [ "$ARG1" = "--auto" ]; then
  AUTO_MODE="yes"
  KEY="${ARK_API_KEY:-}"
  if [ -z "$KEY" ]; then
    cc_err "--auto 模式需要环境变量 ARK_API_KEY,但未注入。"
    cc_err "请改用: bash setup-agentplan.sh \"<你的 AgentPlan 专属 Key>\""
    exit 1
  fi
  is_agent_plan="$(printf '%s' "${ARK_AGENT_PLAN:-}" | tr '[:upper:]' '[:lower:]')"
  is_coding_plan="$(printf '%s' "${ARK_CODING_PLAN:-}" | tr '[:upper:]' '[:lower:]')"

  # 套餐分流: AgentPlan 和 Coding Plan 是两套不同的上游 + 两套不同的 Key,
  # 沙箱根据用户当前套餐只会注入其中一把,base_url 也不一样:
  #   AgentPlan  -> https://ark.cn-beijing.volces.com/api/plan
  #   CodingPlan -> https://ark.cn-beijing.volces.com/api/coding
  # 所以 --auto 检测到 ARK_CODING_PLAN=true 时,要转发去 setup-codingplan.sh,
  # 不能套用 AgentPlan profile,否则 401 / 路由错误必现。
  if [ "$is_coding_plan" = "true" ] || [ "$is_coding_plan" = "1" ]; then
    if [ "$is_agent_plan" != "true" ] && [ "$is_agent_plan" != "1" ]; then
      cc_log "检测到 ARK_CODING_PLAN=true,转发到 setup-codingplan.sh"
      exec bash "$SCRIPT_DIR/setup-codingplan.sh" --auto
    fi
  fi

  if [ "$is_agent_plan" != "true" ] && [ "$is_agent_plan" != "1" ] \
     && [ "$is_coding_plan" != "true" ] && [ "$is_coding_plan" != "1" ]; then
    cc_warn "环境中未检测到 ARK_AGENT_PLAN=true 或 ARK_CODING_PLAN=true,但 ARK_API_KEY 已注入。"
    cc_warn "仍按 AgentPlan 配置继续(若 Key 不匹配,后续 401 时请改用 custom 网关)。"
  fi
else
  KEY="$ARG1"
  if [ -z "$KEY" ]; then
    cc_err "缺少 AgentPlan Key。"
    cc_err "用法 1: bash setup-agentplan.sh \"<你的 AgentPlan 专属 Key>\""
    cc_err "用法 2: bash setup-agentplan.sh --auto   # 零感知,从沙箱注入的 ARK_API_KEY 取"
    cc_err "Key 获取方式: 登录 AgentPlan 控制台 → 复制专属 Key"
    exit 1
  fi
fi

# ============================================================
# 步骤 0: 预校验 (本地格式 + 抗抖动 ping)
# ============================================================
# 0.1 本地格式自检 - 不联网,挡掉粘错的输入(空格/换行/中文等)
if ! cc_format_check_key "$KEY"; then
  cc_err "你给的这串看起来不像一把有效的 Key。"
  cc_err "AgentPlan 的 Key 应该是一串 20 位以上的字母+数字(可能含 - 或 _)。"
  cc_err "请去火山方舟控制台 → AgentPlan 页面,完整复制专属 Key 后再发给我。"
  exit 1
fi

# 0.2 活性 ping(可选,失败有 fallback)
AGENTPLAN_BASE="https://ark.cn-beijing.volces.com/api/plan"
cc_ping_key "$KEY" "$AGENTPLAN_BASE"
ping_ret=$?
case "$ping_ret" in
  0)
    cc_log "步骤 0/6: Key 在线校验通过 ✅"
    ;;
  2)
    cc_warn "步骤 0/6: 网络抖动,跳过在线校验,直接写入配置(若运行时报 401 我会再处理)"
    ;;
  1)
    # AgentPlan Key 鉴权失败
    if [ "$AUTO_MODE" = "yes" ]; then
      is_coding_plan="$(printf '%s' "${ARK_CODING_PLAN:-}" | tr '[:upper:]' '[:lower:]')"
      if [ "$is_coding_plan" = "true" ] || [ "$is_coding_plan" = "1" ]; then
        cc_warn "AgentPlan 鉴权失败(HTTP 401),但检测到当前账号也开通了 Coding Plan。"
        cc_warn "自动切换到 Coding Plan 试试..."
        exec bash "$SCRIPT_DIR/setup-codingplan.sh" --auto --from-fallback
      fi
    fi
    cc_err "用这把 Key 连火山方舟 AgentPlan 时被拒绝(HTTP 401/403)。"
    cc_err "通常的原因是:"
    cc_err "  • Key 已经过期或被回收 — 请去 ArkClaw 控制台刷新一下"
    cc_err "  • 你贴的是 Coding Plan 的 Key,不是 AgentPlan 的"
    cc_err "  • 你贴的是火山方舟普通 v3 Key,不是套餐专属 Key"
    cc_err "请确认后重新提供 Key,或告诉我用别的方式接入(比如 Kimi / DeepSeek / 你自己的网关)"
    exit 1
    ;;
esac

SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TMPL="$SKILL_DIR/profiles/agentplan.json"
TARGET_PROFILE="$CC_PROFILES_DIR/agentplan.json"

mkdir -p "$CC_PROFILES_DIR"

# ============================================================
# 步骤 1: 保存 ARK_API_KEY 到 ~/.bashrc
# ============================================================
cc_persist_env_to_bashrc "ARK_API_KEY" "$KEY"
cc_log "步骤 1/6: ARK_API_KEY 已保存到 ~/.bashrc"

# ============================================================
# 步骤 2: 写 Key 到 ~/.claude/.token
# ============================================================
cc_write_token "$KEY"
cc_log "步骤 2/6: Key 已写入 ~/.claude/.token (仅 600 权限)"

# ============================================================
# 步骤 3: 渲染 profile 文件 (agentplan 模板无占位符,直接拷贝)
# ============================================================
cp "$TMPL" "$TARGET_PROFILE"
chmod 600 "$TARGET_PROFILE" 2>/dev/null || true
cc_log "步骤 3/6: 配置文件已写入 $TARGET_PROFILE"

# ============================================================
# 步骤 4: 激活该 profile (备份旧 settings.json 后覆盖)
# ============================================================
cc_backup_if_needed "$CC_SETTINGS"
cp "$TARGET_PROFILE" "$CC_SETTINGS"
chmod 600 "$CC_SETTINGS" 2>/dev/null || true
cc_log "步骤 4/6: 已激活 AgentPlan 配置 → $CC_SETTINGS"

# ============================================================
# 步骤 5: 标记 onboarding 完成
# ============================================================
cc_ensure_onboarding_completed
cc_log "步骤 5/6: ~/.claude.json hasCompletedOnboarding=true"

# ============================================================
# 步骤 6: 写 active-profile marker
# ============================================================
cc_set_active_profile "agentplan"
cc_log "步骤 6/6: ~/.claude/active-profile = agentplan"

echo ""
if [ "$AUTO_MODE" = "yes" ]; then
  cc_log "✅ AgentPlan 配置已自动完成 (使用沙箱注入的 ARK_API_KEY,无需粘贴 Key)"
else
  cc_log "✅ AgentPlan 配置全部完成!"
fi
cc_log "   现在可以直接说编程需求,例如:"
cc_log "   「用 claude code 帮我重构 utils.py」"
cc_log "   「claude code review 一下 main.py」"
