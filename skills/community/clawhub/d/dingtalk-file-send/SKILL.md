---
name: dingtalk-file-send
description: "Upload and send files to DingTalk users. Auto-detects account from current session. Use when: user asks to send/forward a file/document/PDF/image via DingTalk."
metadata:
  openclaw:
    emoji: "📤"
    requires:
      bins: ["curl", "jq"]
    config:
      read:
        - "~/.openclaw/openclaw.json (channels.dingtalk.accounts, bindings)"
    env:
      read:
        - "OPENCLAW_AGENT_ID (optional, auto-set by runtime)"
---

# DingTalk File Send Skill

Upload files to DingTalk media server and send them to specified users.

**Automatically detects DingTalk account from current session binding.**

## When to Use

✅ **USE this skill when:**

- "Send this PDF to [user]"
- "Forward this document via DingTalk"
- "Share this file with my boss"
- "Upload and send [filename]"

## Configuration (Automatic)

This skill **automatically detects** the DingTalk account from your current session:

**How it works:**
1. Reads current agent ID from OpenClaw runtime context
2. Looks up the binding in `~/.openclaw/openclaw.json`
3. Matches `agentId` → `accountId` → DingTalk credentials

**Binding example:**
```json
{
  "bindings": [
    {
      "agentId": "dingtalk-office",
      "match": {
        "channel": "dingtalk",
        "accountId": "office"
      }
    }
  ],
  "channels": {
    "dingtalk": {
      "accounts": {
        "office": {
          "clientId": "your_client_id",
          "clientSecret": "xxx",
          "robotCode": "your_robot_code"
        }
      }
    }
  }
}
```

**Note:** In DingTalk's API, `clientId` is used as `appKey` for authentication.

## Workflow

```
1. Detect current agentId from session context
2. Look up binding: agentId → accountId
3. Read credentials from OpenClaw config by accountId
4. Get access token
5. Upload file to DingTalk media server
6. Send file message to recipient
```

## Commands

### Step 1: Detect Account from Current Session

```bash
OPENCLAW_CONFIG=~/.openclaw/openclaw.json

# Get current agent ID from environment (set by OpenClaw runtime)
AGENT_ID="${OPENCLAW_AGENT_ID:-dingtalk-office}"

# Look up accountId from bindings
ACCOUNT_ID=$(jq -r ".bindings[] | select(.agentId == \"$AGENT_ID\") | .match.accountId" $OPENCLAW_CONFIG)

# Fallback: if no binding found, use agent ID suffix
if [ -z "$ACCOUNT_ID" ] || [ "$ACCOUNT_ID" = "null" ]; then
  # Extract account from agent ID (e.g., "dingtalk-office" → "office")
  ACCOUNT_ID=$(echo "$AGENT_ID" | sed 's/dingtalk-//')
fi

# Read credentials (clientId is used as appKey)
APP_KEY=$(jq -r ".channels.dingtalk.accounts[\"$ACCOUNT_ID\"].clientId" $OPENCLAW_CONFIG)
APP_SECRET=$(jq -r ".channels.dingtalk.accounts[\"$ACCOUNT_ID\"].clientSecret" $OPENCLAW_CONFIG)
ROBOT_CODE=$(jq -r ".channels.dingtalk.accounts[\"$ACCOUNT_ID\"].robotCode" $OPENCLAW_CONFIG)

# Validate
if [ "$APP_KEY" = "null" ] || [ "$APP_SECRET" = "null" ] || [ "$ROBOT_CODE" = "null" ]; then
  echo "❌ Account '$ACCOUNT_ID' not found in OpenClaw config."
  echo "Current agent: $AGENT_ID"
  echo "Available accounts: $(jq -r '.channels.dingtalk.accounts | keys | join(", ")' $OPENCLAW_CONFIG)"
  exit 1
fi
```

### Step 2: Get Access Token

```bash
ACCESS_TOKEN=$(curl -s -X POST "https://api.dingtalk.com/v1.0/oauth2/accessToken" \
  -H "Content-Type: application/json" \
  -d "{\"appKey\":\"$APP_KEY\",\"appSecret\":\"$APP_SECRET\"}" | jq -r '.accessToken')

if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "null" ]; then
  echo "❌ Failed to get access token."
  exit 1
fi
```

### Step 3: Upload File

```bash
FILE_PATH="$1"
FILE_NAME=$(basename "$FILE_PATH")

UPLOAD_RESULT=$(curl -s -X POST "https://oapi.dingtalk.com/media/upload?access_token=$ACCESS_TOKEN&type=file&robotCode=$ROBOT_CODE" \
  -F "media=@$FILE_PATH;filename=$FILE_NAME" \
  -H "Expect:")

MEDIA_ID=$(echo "$UPLOAD_RESULT" | jq -r '.media_id')

if [ -z "$MEDIA_ID" ] || [ "$MEDIA_ID" = "null" ]; then
  echo "❌ Upload failed: $UPLOAD_RESULT"
  exit 1
fi
```

### Step 4: Send File Message

```bash
USER_ID="$2"
FILE_EXT="${FILE_NAME##*.}"

PAYLOAD=$(jq -n \
  --arg robotCode "$ROBOT_CODE" \
  --arg msgKey "sampleFile" \
  --arg mediaId "$MEDIA_ID" \
  --arg fileName "$FILE_NAME" \
  --arg fileType "$FILE_EXT" \
  --arg userId "$USER_ID" \
  '{
    robotCode: $robotCode,
    msgKey: $msgKey,
    msgParam: ({
      mediaId: $mediaId,
      fileName: $fileName,
      fileType: $fileType
    } | tojson),
    userIds: [$userId]
  }')

SEND_RESULT=$(curl -s -X POST "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend" \
  -H "Content-Type: application/json" \
  -H "x-acs-dingtalk-access-token: $ACCESS_TOKEN" \
  -d "$PAYLOAD")

PROCESS_KEY=$(echo "$SEND_RESULT" | jq -r '.processQueryKey // empty')

if [ -n "$PROCESS_KEY" ]; then
  echo "✅ File sent successfully!"
  echo "ProcessQueryKey: $PROCESS_KEY"
else
  echo "❌ Send failed: $SEND_RESULT"
  exit 1
fi
```

## Complete Script

```bash
#!/bin/bash
# Usage: send_dingtalk_file.sh <file_path> <user_id>
# Automatically detects DingTalk account from current session

set -e

OPENCLAW_CONFIG=~/.openclaw/openclaw.json

# Check config file
if [ ! -f "$OPENCLAW_CONFIG" ]; then
  echo "❌ OpenClaw config not found: $OPENCLAW_CONFIG"
  exit 1
fi

# Check file argument
FILE_PATH="$1"
USER_ID="$2"

if [ -z "$FILE_PATH" ] || [ -z "$USER_ID" ]; then
  echo "Usage: $0 <file_path> <user_id>"
  exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
  echo "❌ File not found: $FILE_PATH"
  exit 1
fi

# Get current agent ID from environment (set by OpenClaw runtime)
AGENT_ID="${OPENCLAW_AGENT_ID:-dingtalk-office}"

# Look up accountId from bindings
ACCOUNT_ID=$(jq -r ".bindings[] | select(.agentId == \"$AGENT_ID\") | .match.accountId" $OPENCLAW_CONFIG)

# Fallback: if no binding found, use agent ID suffix
if [ -z "$ACCOUNT_ID" ] || [ "$ACCOUNT_ID" = "null" ]; then
  ACCOUNT_ID=$(echo "$AGENT_ID" | sed 's/dingtalk-//')
fi

# Read credentials from OpenClaw config
APP_KEY=$(jq -r ".channels.dingtalk.accounts[\"$ACCOUNT_ID\"].clientId" $OPENCLAW_CONFIG)
APP_SECRET=$(jq -r ".channels.dingtalk.accounts[\"$ACCOUNT_ID\"].clientSecret" $OPENCLAW_CONFIG)
ROBOT_CODE=$(jq -r ".channels.dingtalk.accounts[\"$ACCOUNT_ID\"].robotCode" $OPENCLAW_CONFIG)

# Validate credentials
if [ "$APP_KEY" = "null" ] || [ "$APP_SECRET" = "null" ] || [ "$ROBOT_CODE" = "null" ]; then
  echo "❌ Account '$ACCOUNT_ID' not found in OpenClaw config."
  echo "Current agent: $AGENT_ID"
  echo "Available accounts: $(jq -r '.channels.dingtalk.accounts | keys | join(", ")' $OPENCLAW_CONFIG)"
  exit 1
fi

FILE_NAME=$(basename "$FILE_PATH")
FILE_EXT="${FILE_NAME##*.}"

# Get access token
ACCESS_TOKEN=$(curl -s -X POST "https://api.dingtalk.com/v1.0/oauth2/accessToken" \
  -H "Content-Type: application/json" \
  -d "{\"appKey\":\"$APP_KEY\",\"appSecret\":\"$APP_SECRET\"}" | jq -r '.accessToken')

if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" = "null" ]; then
  echo "❌ Failed to get access token."
  exit 1
fi

# Upload file
UPLOAD_RESULT=$(curl -s -X POST "https://oapi.dingtalk.com/media/upload?access_token=$ACCESS_TOKEN&type=file&robotCode=$ROBOT_CODE" \
  -F "media=@$FILE_PATH;filename=$FILE_NAME" \
  -H "Expect:")

MEDIA_ID=$(echo "$UPLOAD_RESULT" | jq -r '.media_id')

if [ -z "$MEDIA_ID" ] || [ "$MEDIA_ID" = "null" ]; then
  echo "❌ Upload failed: $UPLOAD_RESULT"
  exit 1
fi

# Send file
PAYLOAD=$(jq -n \
  --arg robotCode "$ROBOT_CODE" \
  --arg msgKey "sampleFile" \
  --arg mediaId "$MEDIA_ID" \
  --arg fileName "$FILE_NAME" \
  --arg fileType "$FILE_EXT" \
  --arg userId "$USER_ID" \
  '{robotCode:$robotCode,msgKey:$msgKey,msgParam:({mediaId:$mediaId,fileName:$fileName,fileType:$fileType}|tojson),userIds:[$userId]}')

SEND_RESULT=$(curl -s -X POST "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend" \
  -H "Content-Type: application/json" \
  -H "x-acs-dingtalk-access-token: $ACCESS_TOKEN" \
  -d "$PAYLOAD")

PROCESS_KEY=$(echo "$SEND_RESULT" | jq -r '.processQueryKey // empty')

if [ -n "$PROCESS_KEY" ]; then
  echo "✅ File sent successfully!"
  echo "ProcessQueryKey: $PROCESS_KEY"
else
  echo "❌ Send failed: $SEND_RESULT"
  exit 1
fi
```

## Supported File Types

| Type | Extensions | Max Size |
|------|------------|----------|
| PDF | `.pdf` | 20 MB |
| Document | `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx` | 20 MB |
| Image | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp` | 10 MB |
| Other | `.txt`, `.zip`, `.rar` | 20 MB |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENCLAW_AGENT_ID` | Current agent ID (auto-set by OpenClaw runtime) | Auto |

## Response Handling

**Success response:**
```json
{
  "flowControlledStaffIdList": [],
  "invalidStaffIdList": [],
  "processQueryKey": "xxx="
}
```

**Check delivery status:**
```bash
curl -s -X GET "https://api.dingtalk.com/v1.0/robot/oToMessages/status?processQueryKey=$PROCESS_KEY" \
  -H "x-acs-dingtalk-access-token: $ACCESS_TOKEN"
```

## Notes

- **Fully automatic** — detects account from current session, no configuration needed
- Media files expire after **30 days** on DingTalk server
- Max file size: **20 MB** for files, **10 MB** for images
- Access token expires after **2 hours**
- Rate limit: ~100 requests/second per app
- Works with any DingTalk account bound in OpenClaw config

## Common Issues

**"Account not found in OpenClaw config"**
→ Check bindings: `jq '.bindings[] | select(.agentId == "current-agent-id")' ~/.openclaw/openclaw.json`
→ Verify account exists: `jq '.channels.dingtalk.accounts | keys' ~/.openclaw/openclaw.json`

**"Failed to get access token"**
→ Verify clientId/clientSecret in OpenClaw config are correct and not expired.

**"Invalid media_id"**
→ File upload failed or expired. Re-upload and get new media_id.

**"Invalid userId"**
→ Check the recipient's DingTalk user ID format.

**File shows but can't open**
→ Ensure file is valid (not HTML renamed to .pdf, etc.)

## Security Notes

- **No hardcoded credentials** — reads from OpenClaw config only
- **Session-based account detection** — uses current agent's bound account
- Access token is generated on-demand and not stored
- Credentials never leave your machine except for DingTalk API calls
