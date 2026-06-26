---
name: slack-integration
description: Slack messaging — send messages, manage channels, upload files, add reactions, and automate team notifications via CLI and API.
metadata: {"openclaw":{"requires":{"env":["SLACK_TOKEN"]}}}
---

# Slack Integration

Send messages, manage channels, upload files, and automate notifications in Slack workspaces using the Web API. Works with bot tokens or user tokens.

## Setup

```bash
# 1. Create a Slack App: https://api.slack.com/apps → Create New App
# 2. Add scopes under OAuth & Permissions:
#    Bot Token Scopes: chat:write, channels:read, channels:history,
#                      files:write, reactions:write, users:read
# 3. Install to workspace → copy Bot User OAuth Token

export SLACK_TOKEN="xoxb-..."   # Bot token (starts with xoxb-)
```

For user-level actions (DMs to yourself, custom status), use a User OAuth Token (`xoxp-...`) instead.

## Sending Messages

```bash
# Simple text message
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C0123ABCDEF", "text": "Deploy complete ✓"}'

# With rich formatting (Block Kit)
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0123ABCDEF",
    "blocks": [
      {"type": "header", "text": {"type": "plain_text", "text": "Deploy Report"}},
      {"type": "section", "text": {"type": "mrkdwn", "text": "*Status:* ✅ Success\n*Version:* v2.1.0\n*Duration:* 45s"}}
    ]
  }'

# Reply in thread
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C0123ABCDEF", "thread_ts": "1234567890.123456", "text": "Fix deployed"}'

# Schedule a message (Unix timestamp)
curl -s -X POST https://slack.com/api/chat.scheduleMessage \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C0123ABCDEF", "text": "Standup time!", "post_at": 1700000000}'

# Update a message
curl -s -X POST https://slack.com/api/chat.update \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C0123ABCDEF", "ts": "1234567890.123456", "text": "Updated text"}'
```

## Channels

```bash
# List channels (paginated — follow next_cursor)
curl -s "https://slack.com/api/conversations.list?types=public_channel,private_channel&limit=200" \
  -H "Authorization: Bearer $SLACK_TOKEN" | jq '.channels[] | {id, name, num_members}'

# Get channel info
curl -s "https://slack.com/api/conversations.info?channel=C0123ABCDEF" \
  -H "Authorization: Bearer $SLACK_TOKEN"

# Channel history (recent messages)
curl -s "https://slack.com/api/conversations.history?channel=C0123ABCDEF&limit=10" \
  -H "Authorization: Bearer $SLACK_TOKEN" | jq '.messages[] | {ts, text, user}'

# Find channel by name
curl -s "https://slack.com/api/conversations.list?types=public_channel&limit=999" \
  -H "Authorization: Bearer $SLACK_TOKEN" | jq '.channels[] | select(.name=="general") | .id'

# Create a channel
curl -s -X POST https://slack.com/api/conversations.create \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "incident-2026-04", "is_private": false}'

# Set channel topic
curl -s -X POST https://slack.com/api/conversations.setTopic \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C0123ABCDEF", "topic": "Production incident — DB latency spike"}'
```

## Files

```bash
# Upload a file (v2 API)
curl -s -X POST https://slack.com/api/files.getUploadURLExternal \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filename": "report.csv", "length": 1024}' \
  | jq '{upload_url, file_id}'
# Then POST the file content to upload_url, then call files.completeUploadExternal

# Share a remote file link
curl -s -X POST https://slack.com/api/files.remote.add \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"external_id": "report-1", "external_url": "https://example.com/report.pdf", "title": "Monthly Report"}'
```

## Reactions & Users

```bash
# Add reaction to a message
curl -s -X POST https://slack.com/api/reactions.add \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C0123ABCDEF", "timestamp": "1234567890.123456", "name": "white_check_mark"}'

# List users
curl -s "https://slack.com/api/users.list?limit=200" \
  -H "Authorization: Bearer $SLACK_TOKEN" | jq '.members[] | {id, name, real_name}'

# User info by ID
curl -s "https://slack.com/api/users.info?user=U0123ABCDEF" \
  -H "Authorization: Bearer $SLACK_TOKEN" | jq '.user | {name, real_name, tz}'

# Look up user by email
curl -s "https://slack.com/api/users.lookupByEmail?email=dev@company.com" \
  -H "Authorization: Bearer $SLACK_TOKEN" | jq '.user.id'
```

## Common Workflows

**CI/CD notification:** After a deploy, post a formatted message to #deployments with version, commit, and status. On failure, create a thread with the error log.

**Incident channel:** Create a private channel named `incident-YYYY-MM-DD-<slug>`, set the topic, invite responders, post the initial report with severity and affected services.

**Standup reminder:** Schedule a daily message at 9:30 AM to #team with a prompt template. Collect threaded replies.

**Error alert:** When Sentry fires a webhook, post the error title, count, and link to the relevant channel. Add a 🔴 reaction for critical, 🟡 for warning.

## Notes

- Bot tokens (`xoxb-`) can only post to channels the bot has been invited to
- Rate limits: ~1 msg/sec per channel (Tier 2); respect `Retry-After` headers
- Channel IDs (not names) are required for most API calls — look them up first
- For rich messages, use [Block Kit Builder](https://app.slack.com/block-kit-builder) to design layouts
- `mrkdwn` (Slack's markdown) uses `*bold*`, `_italic_`, `~strike~`, `` `code` ``, `>quote`
- DMs: use `conversations.open` with user IDs to get the DM channel ID, then post normally
