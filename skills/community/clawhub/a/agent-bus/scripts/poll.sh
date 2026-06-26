#!/bin/bash
# poll.sh — Agent Bus message poll script
#
# How it works:
#   1. Sync repo via git pull
#   2. Scan inbox/<MY_AGENT_ID>/ for status: unread messages
#   3. If found: run agent-bus.sh read (auto-ack), then trigger a one-shot notify cron
#   4. No messages: exit silently
#
# Environment variables (must be set before running):
#   AGENT_BUS_REPO           Path to local agent-bus repo (default: ~/agent-bus-repo)
#   AGENT_BUS_AGENT_ID       Your agent ID (default: your-agent-id)
#   AGENT_BUS_NOTIFY_TARGET  Notify target for openclaw cron --to (e.g. single_<uid>)
#   AGENT_BUS_NOTIFY_CHANNEL Notify channel (e.g. daxiang)

REPO="${AGENT_BUS_REPO:-~/agent-bus-repo}"
MY_AGENT_ID="${AGENT_BUS_AGENT_ID:-your-agent-id}"
OWNER_NOTIFY_TARGET="${AGENT_BUS_NOTIFY_TARGET:-}"
OWNER_NOTIFY_CHANNEL="${AGENT_BUS_NOTIFY_CHANNEL:-daxiang}"

export AGENT_BUS_REPO="$REPO"

# ── Sync repo ──
cd "$REPO" || { echo "[agent-bus-poll] ERROR: repo not found at $REPO"; exit 1; }
git pull --rebase --quiet 2>/dev/null || true

# ── Scan inbox for unread messages ──
HAS_MESSAGE=false
while IFS= read -r -d '' f; do
  if grep -q "^status: unread" "$f"; then
    HAS_MESSAGE=true
    break
  fi
done < <(find "$REPO/inbox/$MY_AGENT_ID/" -name "*.md" -not -name ".gitkeep" -print0 2>/dev/null)

echo "[agent-bus-poll] hasMessage=$HAS_MESSAGE (via status:unread scan)"

# ── If new messages: read (auto-ack) and notify owner ──
READ_OUT=""
if [[ "$HAS_MESSAGE" == "true" ]]; then
  READ_OUT=$(bash agent-bus.sh read 2>&1)
  echo "[agent-bus-poll] read: $READ_OUT"

  NOTIFY_FILE=$(mktemp /tmp/agent-bus-notify.XXXXXX.txt)
  echo "$READ_OUT" > "$NOTIFY_FILE"

  openclaw cron add \
    --name "agent-bus-notify" \
    --at "1m" \
    --session isolated \
    --message "【重要执行约束】严禁 sessions_spawn，所有步骤在本 session 内顺序完成。读取文件 $NOTIFY_FILE 的内容，用 message 工具发送（channel: ${OWNER_NOTIFY_CHANNEL}, to: ${OWNER_NOTIFY_TARGET}）把内容原文发出去。" \
    --announce \
    --channel "${OWNER_NOTIFY_CHANNEL}" \
    --to "${OWNER_NOTIFY_TARGET}" > /dev/null 2>&1 || true

  echo "[agent-bus-poll] notify cron created."
fi

echo "[agent-bus-poll] done."
