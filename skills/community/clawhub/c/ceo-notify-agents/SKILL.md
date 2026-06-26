---
name: ceo-notify-agents
description: CEO向其他Agent发送通知（通过共享记忆文件）
triggers:
  - "通知 {targetAgents} {message}"
  - "告诉 {targetAgents} {message}"
  - "提醒 {targetAgents} {message}"
  - "给 {targetAgents} 发消息 {message}"
  - "请通知 {targetAgents} {message}"
  - "通知一下 {targetAgents} {message}"
  - "让 {targetAgents} 知道 {message}"
requires: []
actions:
  - name: write_notification
    tool: exec
    params:
      command: |
        #!/bin/bash
        TARGETS="{{targetAgents}}"
        MESSAGE="{{message}}"
        NOTIFICATION_DIR="/Users/anran/Documents/openclaw/shared_memory/notifications"
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)

        mkdir -p "$NOTIFICATION_DIR"

        IFS=',' read -ra AGENTS <<< "$TARGETS"
        for raw in "${AGENTS[@]}"; do
          agent=$(echo "$raw" | xargs)
          echo "$TIMESTAMP: $MESSAGE" >> "$NOTIFICATION_DIR/${agent}.log"
        done

        echo "$TIMESTAMP: 通知 $TARGETS - $MESSAGE" >> "$NOTIFICATION_DIR/all.log"

        /Users/anran/.npm-global/bin/openclaw memory index --agent main

        echo "通知已写入共享记忆，目标Agent下次对话时将看到。"
