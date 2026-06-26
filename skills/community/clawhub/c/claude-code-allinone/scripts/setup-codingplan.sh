#!/usr/bin/env bash
# setup-codingplan.sh — 一键配置 火山方舟 Coding Plan 模式
#
# Coding Plan 与 AgentPlan 是两套独立的套餐,Key 互不通用,base_url 也不一样:
#   AgentPlan  -> https://ark.cn-beijing.volces.com/api/plan
#   CodingPlan -> https://ark.cn-beijing.volces.com/api/coding   (Anthropic 协议)
#
# 用法:
#   bash setup-codingplan.sh "<Coding Plan 专属 Key>"
#   bash setup-codingplan.sh --auto         # 零感知:从沙箱注入的 ARK_API_KEY 取
#
# 步骤等同 setup-agentplan.sh,只是写入的是 codingplan profile。

set -e

ARG1="${1:-}"
ARG2="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"

AUTO_MODE="no"
FROM_FALLBACK="no"
KEY=""

# 支持 --auto 和 --auto --from-fallback
if [ "$ARG1" = "--auto" ]; then
  AUTO_MODE="yes"
  if [ "$ARG2" = "--from-fallback" ]; then
    FROM_FALLBACK="yes"
  fi
  KEY="${ARK_API_KEY:-}"
  if [ -z "$KEY" ]; then
    cc_err "--auto 模式需要环境变量 ARK_API_KEY,但未注入。"
    cc_err "请改用: bash setup-codingplan.sh \"<你的 Coding Plan 专属 Key>\""
    exit 1
  fi
  is_coding_plan="$(printf '%s' "${ARK_CODING_PLAN:-}" | tr '[:upper:]' '[:lower:]')"
  if [ "$is_coding_plan" != "true" ] && [ "$is_coding_plan" != "1" ] && [ "$FROM_FALLBACK" != "yes" ]; then
    cc_warn "环境中未检测到 ARK_CODING_PLAN=true,但 ARK_API_KEY 已注入。"
    cc_warn "仍按 Coding Plan 配置继续(若 Key 不匹配,后续 401 时请改用 setup-agentplan)。"
  fi
else
  KEY="$ARG1"
  if [ -z "$KEY" ]; then
    cc_err "缺少 Coding Plan Key。"
    cc_err "用法 1: bash setup-codingplan.sh \"<你的 Coding Plan 专属 Key>\""
    cc_err "用法 2: bash setup-codingplan.sh --auto   # 零感知,从沙箱注入的 ARK_API_KEY 取"
    cc_err "Key 获取方式: 火山引擎方舟控制台 → API Key 管理 → 复制专属 Key"
    exit 1
  fi
fi

# ============================================================
# 步骤 0: 预校验
# ============================================================
if ! cc_format_check_key "$KEY"; then
  cc_err "你给的这串看起来不像一把有效的 Key。"
  cc_err "Coding Plan 的 Key 应该是一串 20 位以上的字母+数字(可能含 - 或 _)。"
  cc_err "请去火山方舟控制台 → Coding Plan 页面,完整复制专属 Key 后再发给我。"
  exit 1
fi

CODINGPLAN_BASE="https://ark.cn-beijing.volces.com/api/coding"
cc_ping_key "$KEY" "$CODINGPLAN_BASE"
ping_ret=$?
case "$ping_ret" in
  0)
    cc_log "步骤 0/6: Key 在线校验通过 ✅"
    ;;
  2)
    cc_warn "步骤 0/6: 网络抖动,跳过在线校验,直接写入配置(若运行时报 401 我会再处理)"
    ;;
  1)
    cc_err "用这把 Key 连火山方舟 Coding Plan 时被拒绝(HTTP 401/403)。"
    cc_err "通常的原因是:"
    cc_err "  • Key 已经过期或被回收 — 请去 ArkClaw 控制台刷新"
    cc_err "  • 你贴的是 AgentPlan 的 Key,不是 Coding Plan 的"
    cc_err "请确认后重新提供 Key,或告诉我用别的方式接入"
    exit 1
    ;;
esac

SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TMPL="$SKILL_DIR/profiles/codingplan.json"
TARGET_PROFILE="$CC_PROFILES_DIR/codingplan.json"

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
# 步骤 3: 渲染 profile 文件 (codingplan 模板无占位符,直接拷贝)
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
cc_log "步骤 4/6: 已激活 Coding Plan 配置 → $CC_SETTINGS"

# ============================================================
# 步骤 5: 标记 onboarding 完成
# ============================================================
cc_ensure_onboarding_completed
cc_log "步骤 5/6: ~/.claude.json hasCompletedOnboarding=true"

# ============================================================
# 步骤 6: 写 active-profile marker
# ============================================================
cc_set_active_profile "codingplan"
cc_log "步骤 6/6: ~/.claude/active-profile = codingplan"

echo ""
if [ "$AUTO_MODE" = "yes" ]; then
  if [ "$FROM_FALLBACK" = "yes" ]; then
    cc_log "✅ 已配置 Coding Plan(AgentPlan Key 不可用,自动切到了 Coding Plan)"
  else
    cc_log "✅ Coding Plan 配置已自动完成 (使用沙箱注入的 ARK_API_KEY,无需粘贴 Key)"
  fi
else
  cc_log "✅ Coding Plan 配置全部完成!"
fi
cc_log "   现在可以直接说编程需求,例如:"
cc_log "   「用 claude code 帮我重构 utils.py」"
cc_log "   「claude code review 一下 main.py」"
