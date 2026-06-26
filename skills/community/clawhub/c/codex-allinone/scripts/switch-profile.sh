#!/usr/bin/env bash
# switch-profile.sh — 在不同模型服务之间快速切换 (v7)
#
# 用法:
#   bash switch-profile.sh           # 列出已配置的模型,供用户选择
#   bash switch-profile.sh <名称>    # 直接切换到指定模型配置
#
# 原理:
#   ~/.codex/config.toml 是一个快捷方式(软链接),指向 ~/.codex/profiles/ 中的某个配置文件。
#   "切换"就是把这个快捷方式重新指向另一个配置文件,并按需启动对应端口的 relay。

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/relay-helper.sh"

CODEX_DIR="$HOME/.codex"
PROFILES_DIR="$CODEX_DIR/profiles"
ACTIVE_FILE="$CODEX_DIR/active-profile"

TARGET="${1:-}"

list_profiles() {
  if [ ! -d "$PROFILES_DIR" ]; then
    echo "❌ 还没有配置任何模型服务。请先完成初始配置。"
    exit 1
  fi
  CURRENT=""
  [ -f "$ACTIVE_FILE" ] && CURRENT="$(cat "$ACTIVE_FILE" | tr -d '[:space:]')"

  echo "已配置的模型服务:"
  for f in "$PROFILES_DIR"/*.toml; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .toml)"
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
  echo "例如:     bash switch-profile.sh kimi"
  exit 0
fi

PROFILE_FILE="$PROFILES_DIR/${TARGET}.toml"
if [ ! -f "$PROFILE_FILE" ]; then
  echo "❌ 配置 '$TARGET' 不存在或还没设置。" >&2
  echo "" >&2
  list_profiles
  exit 1
fi

ln -sf "$PROFILE_FILE" "$CODEX_DIR/config.toml"
echo "$TARGET" > "$ACTIVE_FILE"
echo "✅ 已切换到: $TARGET"

# 按需启动对应端口的 relay (arkv3 直连不需要;custom 直连模式也不需要)
RELAY_PORT=""
RELAY_UPSTREAM=""
case "$TARGET" in
  agentplan)
    RELAY_PORT=4446
    RELAY_UPSTREAM="https://ark.cn-beijing.volces.com/api/plan/v3"
    ;;
  codingplan)
    RELAY_PORT=4450
    RELAY_UPSTREAM="https://ark.cn-beijing.volces.com/api/coding/v3"
    ;;
  kimi)
    RELAY_PORT=4447
    RELAY_UPSTREAM="https://api.moonshot.cn/v1"
    ;;
  deepseek)
    RELAY_PORT=4448
    RELAY_UPSTREAM="https://api.deepseek.com/v1"
    ;;
  custom)
    if [ -f "$HOME/.codex/custom-upstream" ]; then
      RELAY_PORT=4449
      RELAY_UPSTREAM="$(cat "$HOME/.codex/custom-upstream" | tr -d '[:space:]')"
    fi
    ;;
  arkv3)
    : # 直连
    ;;
esac

if [ -n "$RELAY_PORT" ] && [ -n "$RELAY_UPSTREAM" ]; then
  if ! relay_running "$RELAY_PORT"; then
    echo ""
    echo "⚠️  $TARGET 需要 codex-relay 服务(端口 $RELAY_PORT),正在启动..."
    if ensure_codex_relay_installed && start_relay "$TARGET" "$RELAY_PORT" "$RELAY_UPSTREAM"; then
      echo "✅ codex-relay 已就绪"
    else
      echo "❌ codex-relay 启动失败,请查看 ~/.codex-relay-${TARGET}.log"
      exit 2
    fi
  fi
fi
