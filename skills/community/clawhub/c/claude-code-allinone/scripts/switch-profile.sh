#!/usr/bin/env bash
# switch-profile.sh — 在不同模型服务之间快速切换
#
# 用法:
#   bash switch-profile.sh           # 列出已配置的模型,供用户选择
#   bash switch-profile.sh <名称>    # 直接切换到指定模型配置
#
# 原理:
#   ~/.claude/settings.json 是当前激活配置的实际内容(由 setup / switch 脚本写入),
#   切换 = 用对应 profile 文件的内容覆盖 settings.json,并同步 .token 文件 + active-profile marker。
#
# 注意:
#   .token 文件保存的是当前 profile 的 Key。切换 profile 时需要同步切换 Key。
#   - agentplan → 取 ARK_API_KEY (从 .bashrc 或当前环境)
#   - custom    → 取 CUSTOM_ANTHROPIC_KEY

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/helpers.sh"

TARGET="${1:-}"

list_profiles() {
  if [ ! -d "$CC_PROFILES_DIR" ]; then
    echo "❌ 还没有配置任何模型服务。请先完成初始配置。"
    exit 1
  fi
  CURRENT=""
  [ -f "$CC_ACTIVE_FILE" ] && CURRENT="$(cat "$CC_ACTIVE_FILE" | tr -d '[:space:]')"

  echo "已配置的模型服务:"
  for f in "$CC_PROFILES_DIR"/*.json; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .json)"
    if [ "$name" = "$CURRENT" ]; then
      echo "  ★ $name (当前使用)"
    else
      echo "    $name"
    fi
  done
}

if [ -z "$TARGET" ]; then
  list_profiles
  echo ""
  echo "切换方式: bash switch-profile.sh <名称>"
  echo "例如:     bash switch-profile.sh agentplan"
  exit 0
fi

PROFILE_FILE="$CC_PROFILES_DIR/${TARGET}.json"
if [ ! -f "$PROFILE_FILE" ]; then
  echo "❌ 配置 '$TARGET' 不存在或还没设置。" >&2
  echo "" >&2
  list_profiles
  exit 1
fi

# 备份当前 settings.json (如果不是软链)
cc_backup_if_needed "$CC_SETTINGS"

# 用 profile 文件覆盖 settings.json
cp "$PROFILE_FILE" "$CC_SETTINGS"
chmod 600 "$CC_SETTINGS" 2>/dev/null || true

# 同步 .token 文件: 取目标 profile 对应的 Key
SOURCE_KEY=""
case "$TARGET" in
  agentplan)
    SOURCE_KEY="${ARK_API_KEY:-}"
    if [ -z "$SOURCE_KEY" ]; then
      SOURCE_KEY="$(grep -E '^export ARK_API_KEY=' "$HOME/.bashrc" 2>/dev/null | tail -1 | sed -E 's/^export ARK_API_KEY=\"?([^\"]*)\"?.*/\1/')"
    fi
    ;;
  codingplan)
    SOURCE_KEY="${ARK_API_KEY:-}"
    if [ -z "$SOURCE_KEY" ]; then
      SOURCE_KEY="$(grep -E '^export ARK_API_KEY=' "$HOME/.bashrc" 2>/dev/null | tail -1 | sed -E 's/^export ARK_API_KEY=\"?([^\"]*)\"?.*/\1/')"
    fi
    ;;
  custom)
    SOURCE_KEY="${CUSTOM_ANTHROPIC_KEY:-}"
    if [ -z "$SOURCE_KEY" ]; then
      SOURCE_KEY="$(grep -E '^export CUSTOM_ANTHROPIC_KEY=' "$HOME/.bashrc" 2>/dev/null | tail -1 | sed -E 's/^export CUSTOM_ANTHROPIC_KEY=\"?([^\"]*)\"?.*/\1/')"
    fi
    ;;
esac

if [ -n "$SOURCE_KEY" ]; then
  cc_write_token "$SOURCE_KEY"
  echo "✅ 已同步 ~/.claude/.token (来源: $TARGET 对应的环境变量)"
else
  echo "⚠️  警告: 没找到 $TARGET 对应的 Key,~/.claude/.token 未更新"
  echo "    请重跑对应的 setup 脚本传入正确的 Key"
fi

# 写 active-profile marker
cc_set_active_profile "$TARGET"

# 确保 onboarding 标记
cc_ensure_onboarding_completed

echo "✅ 已切换到: $TARGET"
echo "   settings.json: $CC_SETTINGS"
echo "   active-profile: $CC_ACTIVE_FILE"
