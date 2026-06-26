#!/bin/bash
# submit-fangyan-sync.sh - 提交方言云端同步任务到 MQ队列
# 用法: ./submit-fangyan-sync.sh [receive_id] [receive_id_type] [submitter_open_id] [姓名]
#
# receive_id: 接收消息的目标ID（用户open_id 或 群chat_id）
# receive_id_type: open_id（私聊）或 chat_id（群聊）
#
# 示例：
#   私聊触发：./submit-fangyan-sync.sh ou_xxx open_id
#   群聊触发：./submit-fangyan-sync.sh oc_xxx chat_id
#   默认发给徐哥：./submit-fangyan-sync.sh

cd /root/.openclaw/workspace-zhiduoxia/skills/fangyan-map

# 默认发给徐哥
RECEIVE_ID="${1:-ou_6e6e2e480c296ed9871e916bd6693677}"
RECEIVE_TYPE="${2:-open_id}"
SUBMITTER="${3:-ou_6e6e2e480c296ed9871e916bd6693677}"
SUBMITTER_NAME="${4:-徐俊晖}"

python3 /root/.openclaw/skills/task-queue-manager/scripts/submit.py fangyan_sync \
 --params '{}' \
 --agent 智多虾 \
 --app-id cli_a938e384743bdcd3 \
 --submitter "$SUBMITTER" \
 --submitter-name "$SUBMITTER_NAME" \
 --receive-id "$RECEIVE_ID" \
 --receive-id-type "$RECEIVE_TYPE"