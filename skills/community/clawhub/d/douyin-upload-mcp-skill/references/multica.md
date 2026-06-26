# Multica And Multi-Client Bridge

Use this reference when tasks enter through Multica, WeChat, QQ, or another client instead of Feishu.

## Role

Multica and other clients are task intake and status channels. Default customer action prompts still go to Feishu.

Do not default to Multica for QR delivery. Its image UI is not clear enough for customer login. QR images, SMS prompts, security-verification screenshots, authorization prompts, and final critical success/failure notifications default to Feishu.

If task came from Multica and QR is needed, leave only:

`二维码已发送到飞书，请在电脑端飞书查看并用手机抖音 App 扫码。`

## Registered Multica Skill

Bridge skill:

- name: `douyin-creator-ops-bridge`
- id: `7df48990-fecd-41d9-b2d8-aafebace2edf`
- points to the installed skill path, usually `$HOME/.openclaw/workspace/skills/douyin-upload-mcp-skill` for ClawHub installs or `$HOME/.openclaw/skills/douyin-upload-mcp-skill` for older/manual installs

Example issue:

```bash
multica issue create \
  --title "发布抖音任务" \
  --description '<字段化发布任务或任务说明>' \
  --assignee "OpenClaw 连接" \
  --attachment /path/to/file.png
```

## Attachments

Issue attachments are visible in `attachments[]`:

```bash
multica issue get <issue-id> --output json
multica attachment download <attachment-id> -o /tmp/douyin-attachments
```

The channel was tested with QR PNG upload and agent-side reading, but customer visual display was not good enough for QR login.

## Sandboxed Agents

Multica and some agents may mount `$HOME/.openclaw/workspace` as read-only. Redirect temporary writes:

```bash
mkdir -p "$PWD/.douyin-state" "$PWD/.douyin-output"
DOUYIN_MONITOR_STATE_DIR="$PWD/.douyin-state" \
OUTPUT_DIR="$PWD/.douyin-output" \
node scripts/douyin-login-monitor.js check
```

`douyin-login-monitor.js` now skips log-write failures so a read-only log path does not hide real login results.

If multica daemon starts Codex without `ICE_API_KEY`, import the current shell env and restart daemon:

```bash
systemctl --user import-environment ICE_API_KEY
systemctl --user restart multica-daemon.service
```

Do not write secrets into unit files.
