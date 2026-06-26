#!/usr/bin/env bash
# install_cron.sh — 安装赏金自动化 Cron Jobs 到 OpenClaw
# 用法: bash scripts/install_cron.sh [qq_chat_id]
# 如果不传参数，使用默认 openid

set -euo pipefail

QQ_TARGET="${1:-qqbot:c2c:77B8CFE33C9E63BA4AF783B6F9FAF286}"
CRON_FILE="${HOME}/.openclaw/cron/jobs.json"

echo "安装赏金自动化 Cron Jobs..."
echo "推送目标: ${QQ_TARGET}"

# 确保目录存在
mkdir -p "$(dirname "$CRON_FILE")"

cat > "$CRON_FILE" << CRONEOF
[
  {
    "name": "BountyHunter-Push",
    "enabled": true,
    "schedule": {
      "kind": "every",
      "intervalMs": 600000
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run bounty hunter scanner.\npython3 /home/node/clawd/bounty-hunter/bounty_hunter.py\nExtract QQ_MSG: lines and push to user.\nIf NO_NEW, reply NO_REPLY."
    },
    "delivery": {
      "mode": "announce",
      "channel": "qqbot",
      "to": "${QQ_TARGET}"
    }
  },
  {
    "name": "GitHub-Bounty-Auto",
    "enabled": true,
    "schedule": {
      "kind": "every",
      "intervalMs": 7200000
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "GitHub bounty auto pipeline.\n\nStep 1: python3 /home/node/clawd/bounty-github/bounty_scanner.py\nIf NO_BOUNTY, reply NO_REPLY.\nStep 2: Read target/current.json for selected task info.\nStep 3: Get issue body, implement.\nStep 4: git add commit push, create PR via API.\nPR title starts: [ baobao ].\nAdd payment comment.\nOne task per run. Notify user with PR link."
    },
    "delivery": {
      "mode": "announce",
      "channel": "qqbot",
      "to": "${QQ_TARGET}"
    }
  }
]
CRONEOF

echo "✅ Cron Jobs 已写入: ${CRON_FILE}"
echo "请重启 OpenClaw Gateway 以使配置生效: openclaw gateway restart"
