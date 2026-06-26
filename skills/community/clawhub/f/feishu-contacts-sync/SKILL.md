---
name: feishu-contacts
description: Sync Feishu (Lark) contacts into USER.md so the agent can identify DM senders by name. Use when setting up Feishu identity recognition, updating contacts after HR changes, or configuring multi-user agent access. Feishu DMs only include open_id (no sender name), so this skill embeds an open_id→name lookup table directly in USER.md for zero-tool-call identification.
---

# Feishu Contacts Sync

## Problem

Feishu (Lark) DM messages only include the sender's `open_id` — no name. Group messages include `Sender metadata` with the name, but DMs don't. Without a lookup table, the agent will either:
- Assume all DMs are from the person in USER.md (wrong)
- Fail to identify the sender entirely

## Solution

Embed the full contacts table directly in USER.md. Since workspace files are injected into the system prompt at gateway startup, the agent can match `open_id` from inbound metadata against the table — zero tool calls needed.

## Important: open_id is per-app

Feishu `open_id` is scoped to each app. The same person has different open_ids across different Feishu apps. Each OpenClaw instance using a different Feishu app **must pull contacts with its own app credentials**.

## Setup

### 1. Ensure Feishu app has contacts permission

The app needs `contact:user.employee_id:readonly` or `contact:user.base:readonly` scope to list users via the contacts API.

### 2. Run the sync script

```bash
python3 scripts/sync_feishu_contacts.py <openclaw_config_path> <feishu_account_name> <user_md_path>
```

Example:
```bash
python3 scripts/sync_feishu_contacts.py ~/.openclaw/openclaw.json my_app ~/workspace/USER.md
```

Arguments:
- `openclaw_config_path`: Path to your openclaw.json (contains Feishu app credentials)
- `feishu_account_name`: The account name under `channels.feishu.accounts` in your config
- `user_md_path`: Path to your USER.md file

### 3. USER.md format

The script expects USER.md to contain a contacts section with this format:

```markdown
## 飞书通讯录 (App Name)
飞书 DM 不携带发送者姓名。用 inbound metadata 的 chat_id（格式 `user:ou_xxx`）匹配下表识别发送者。
| 姓名 | open_id |
|------|---------|
| Alice | ou_abc123 |
| Bob | ou_def456 |
```

On first run, if no contacts section exists, add the section header and description line manually, then run the script to populate the table.

### 4. Add sender identification to AGENTS.md

Add this to your startup sequence:

```
识别消息发送者（必须执行）：飞书 DM 不携带发送者姓名，只有 open_id（inbound metadata 的 chat_id 格式 `user:ou_xxx`）。提取 open_id，在 USER.md 的飞书通讯录表格中匹配找到姓名。不要假设 DM 对方就是主人——任何人都可能给你发私聊。群聊消息自带 Sender metadata 可直接使用。
```

### 5. Set up periodic sync (optional)

Add a system crontab to keep contacts fresh (e.g., weekly Monday 7am):

```bash
0 7 * * 1 python3 /path/to/scripts/sync_feishu_contacts.py ~/.openclaw/openclaw.json my_app ~/workspace/USER.md
```

**Note**: After sync updates USER.md, restart the gateway for changes to take effect (workspace files are cached at gateway startup).

## Multi-user principle

USER.md should clearly state:
- Who the "primary human" (主人) is
- That the agent serves multiple users and must not assume DM sender identity
- A communication preference to address people by their actual name

## Privacy

- The contacts table contains only names and open_ids (no emails, phone numbers, or other PII)
- open_id is an opaque identifier meaningful only within your Feishu app
- The sync script reads app credentials from openclaw.json but never outputs them
