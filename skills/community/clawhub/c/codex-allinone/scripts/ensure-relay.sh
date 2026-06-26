#!/usr/bin/env bash
# ensure-relay.sh — 根据当前 active-profile 启动对应端口的 codex-relay (v7)
#
# 设计目的:
#   沙箱重启后所有进程会被清理,本脚本在每次使用 codex 前自动恢复对应的 relay。
#   通过读取 ~/.codex/active-profile 决定该启哪个端口,对用户完全透明。
#
# 行为:
#   - active-profile = arkv3 或不存在 → 直连模式,什么都不做
#   - active-profile = agentplan/kimi/deepseek → 启对应固定端口
#   - active-profile = custom → 读 ~/.codex/custom-upstream 决定端口和上游
#                                (如果该文件不存在,说明 custom 是直连模式,无需 relay)
#   - relay 已在运行 → 立即退出
#   - 否则后台启动并最多等 5 秒确认就绪

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/relay-helper.sh"

ACTIVE_FILE="$HOME/.codex/active-profile"
if [ ! -f "$ACTIVE_FILE" ]; then
  exit 0   # 还没配置,无事可做
fi

ACTIVE="$(cat "$ACTIVE_FILE" | tr -d '[:space:]')"
if [ -z "$ACTIVE" ]; then
  exit 0
fi

# 确定端口和上游
RELAY_PORT=""
RELAY_UPSTREAM=""
case "$ACTIVE" in
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
    # custom 上游存盘了才说明是 relay 模式;否则是原生 Responses 直连
    if [ -f "$HOME/.codex/custom-upstream" ]; then
      RELAY_PORT=4449
      RELAY_UPSTREAM="$(cat "$HOME/.codex/custom-upstream" | tr -d '[:space:]')"
    else
      exit 0   # custom 直连模式
    fi
    ;;
  arkv3)
    exit 0   # 火山方舟 v3 原生支持 Responses,直连
    ;;
  *)
    echo "⚠️  未识别的 profile: $ACTIVE,跳过 relay 启动" >&2
    exit 0
    ;;
esac

if [ -z "$RELAY_PORT" ] || [ -z "$RELAY_UPSTREAM" ]; then
  exit 0
fi

# 已在跑就退出 — 但要做一次"鉴权闭环"探测,
# 防止 v3.1 之前残留的 relay 进程没拿到 Key 导致 401。
if relay_running "$RELAY_PORT"; then
  __probe_code=$(curl -sS -o /dev/null -w "%{http_code}" \
    --max-time 4 \
    -X POST "http://127.0.0.1:${RELAY_PORT}/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d '{"model":"probe","messages":[{"role":"user","content":"ping"}],"max_tokens":1}' 2>/dev/null || echo "000")
  case "$__probe_code" in
    401|403)
      # relay 启动时没拿到 Key,杀掉旧进程重启
      echo "⚠️  检测到 relay 鉴权失败(可能 Key 未注入),正在重启..." >&2
      stop_relay_on_port "$RELAY_PORT"
      ;;
    *)
      exit 0
      ;;
  esac
fi

# 没装就装
ensure_codex_relay_installed || exit 2

# 启动并等待就绪
if start_relay "$ACTIVE" "$RELAY_PORT" "$RELAY_UPSTREAM"; then
  echo "✅ codex-relay 已自动恢复 (profile=$ACTIVE, 端口=$RELAY_PORT)"
  exit 0
fi

echo "❌ codex-relay 启动失败。请查看日志: cat ~/.codex-relay-${ACTIVE}.log" >&2
exit 4
