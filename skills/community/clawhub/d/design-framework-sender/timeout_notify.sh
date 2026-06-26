#!/usr/bin/env bash
# 10分钟超时检查
# 退出码：0=未超时，1=已超时已处理

PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

SK="$(dirname "$0")"
GRP=$(python3 "$SK/config.py" group_chat_id)
OC=$(python3 "$SK/config.py" openclaw_bin)

now=$(date +%s)
triggered=$(cat /tmp/design-framework-timestamp 2>/dev/null || echo "$now")
elapsed=$(( now - triggered ))

if [ "$elapsed" -ge 600 ]; then
    rm -f /tmp/design-framework-waiting \
          /tmp/design-framework-timestamp \
          /tmp/design-framework-sender-username \
          /tmp/design-framework-ref-image \
          /tmp/design_framework.txt \
          /tmp/preview_message.txt \
          /tmp/image_prompt.txt \
          /tmp/design-framework-context-summary.txt \
          /tmp/design-framework-trigger-user \
          /tmp/design-framework-trigger-time \
          /tmp/design-framework-waiting-requirement \
          /tmp/design-framework-wait-start
    rmdir /tmp/design-framework-lock 2>/dev/null
    "$OC" message send --channel telegram --target "$GRP" --message "任务已超时自动取消，如需继续请重新发起"
    exit 1
fi

exit 0
