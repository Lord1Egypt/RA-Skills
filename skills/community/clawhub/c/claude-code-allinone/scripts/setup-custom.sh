#!/usr/bin/env bash
# setup-custom.sh — 一键配置自定义 Anthropic 兼容网关
#
# 用法: bash setup-custom.sh "<base_url>" "<Key>" "<model>"
#
# 适用场景:
#   - 公司自建的 Anthropic Messages 协议网关
#   - 第三方厂商提供的 Anthropic 兼容端点
#   - 火山方舟之外的其他 Anthropic 协议服务
#
# 这个脚本会依次完成:
#   1. 探测 base_url + Key 是否能跑通(可选,失败仅警告不退出)
#   2. 将 CUSTOM_ANTHROPIC_KEY 保存到 ~/.bashrc
#   3. 把 Key 写入 ~/.claude/.token
#   4. 渲染 ~/.claude/profiles/custom.json (替换 __BASE_URL__ / __MODEL__)
#   5. 把 ~/.claude/settings.json 替换为该 profile (已有则先备份)
#   6. 标记 ~/.claude.json hasCompletedOnboarding=true
#   7. 写 active-profile marker

set -e

BASE_URL="${1:-}"
KEY="${2:-}"
MODEL="${3:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"

if [ -z "$BASE_URL" ] || [ -z "$KEY" ] || [ -z "$MODEL" ]; then
  cc_err "用法: bash setup-custom.sh \"<base_url>\" \"<Key>\" \"<model>\""
  cc_err "示例: bash setup-custom.sh \"https://internal-gw.example.com\" \"sk-xxx\" \"claude-3-5-sonnet\""
  exit 1
fi

# 去掉 base_url 末尾的斜杠 (claude code 会自动拼)
BASE_URL="${BASE_URL%/}"

SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TMPL="$SKILL_DIR/profiles/custom.json"
TARGET_PROFILE="$CC_PROFILES_DIR/custom.json"

mkdir -p "$CC_PROFILES_DIR"

# ============================================================
# 步骤 1: 轻量探测 base_url(失败仅警告,不退出 — 用户网络可能临时抖动)
# ============================================================
cc_log "步骤 1/7: 探测 $BASE_URL ..."
if command -v curl >/dev/null 2>&1; then
  PROBE_CODE="$(curl -sS -m 8 -o /dev/null -w '%{http_code}' \
                  -H "x-api-key: $KEY" \
                  -H "anthropic-version: 2023-06-01" \
                  -X POST "$BASE_URL/v1/messages" \
                  -H "Content-Type: application/json" \
                  -d '{"model":"'"$MODEL"'","max_tokens":1,"messages":[{"role":"user","content":"ping"}]}' 2>/dev/null || echo "000")"
  case "$PROBE_CODE" in
    2*|400|422)
      cc_log "  → 端点可达 (HTTP $PROBE_CODE)"
      ;;
    401|403)
      cc_warn "  → 端点可达但鉴权失败 (HTTP $PROBE_CODE),请确认 Key 正确"
      ;;
    404)
      cc_warn "  → /v1/messages 返回 404,base_url 可能不正确;继续配置但实际调用会失败"
      ;;
    000)
      cc_warn "  → 网络不可达或超时,继续配置(用户可能后续会修)"
      ;;
    *)
      cc_warn "  → 探测返回 HTTP $PROBE_CODE,继续配置"
      ;;
  esac
else
  cc_warn "  → 没装 curl,跳过探测"
fi

# ============================================================
# 步骤 2: 保存 CUSTOM_ANTHROPIC_KEY 到 ~/.bashrc
# ============================================================
cc_persist_env_to_bashrc "CUSTOM_ANTHROPIC_KEY" "$KEY"
cc_log "步骤 2/7: CUSTOM_ANTHROPIC_KEY 已保存到 ~/.bashrc"

# ============================================================
# 步骤 3: 写 Key 到 ~/.claude/.token
# ============================================================
cc_write_token "$KEY"
cc_log "步骤 3/7: Key 已写入 ~/.claude/.token (仅 600 权限)"

# ============================================================
# 步骤 4: 渲染 profile 文件
# ============================================================
cc_render_profile "$TMPL" "$TARGET_PROFILE" \
  "__BASE_URL__=$BASE_URL" \
  "__MODEL__=$MODEL"
cc_log "步骤 4/7: 配置文件已写入 $TARGET_PROFILE"
cc_log "  → base_url: $BASE_URL"
cc_log "  → model:    $MODEL"

# ============================================================
# 步骤 5: 激活该 profile (备份旧 settings.json 后覆盖)
# ============================================================
cc_backup_if_needed "$CC_SETTINGS"
cp "$TARGET_PROFILE" "$CC_SETTINGS"
chmod 600 "$CC_SETTINGS" 2>/dev/null || true
cc_log "步骤 5/7: 已激活 custom 配置 → $CC_SETTINGS"

# ============================================================
# 步骤 6: 标记 onboarding 完成
# ============================================================
cc_ensure_onboarding_completed
cc_log "步骤 6/7: ~/.claude.json hasCompletedOnboarding=true"

# ============================================================
# 步骤 7: 写 active-profile marker
# ============================================================
cc_set_active_profile "custom"
cc_log "步骤 7/7: ~/.claude/active-profile = custom"

echo ""
cc_log "✅ 自定义网关配置完成!"
cc_log "   现在可以直接说编程需求,例如:"
cc_log "   「用 claude code 帮我写一个 Python 脚本」"
cc_log ""
cc_log "💡 需要切换到其他模型服务? 执行: bash switch-profile.sh"
