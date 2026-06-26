---
name: feishu-group-ops
description: "Manage Feishu (Lark) group chats using natural language. Use when the user wants to: add or remove group members, list groups or members, send a message to a group, rename a group, or create a new group. Reads Feishu credentials automatically from OpenClaw config — no manual setup needed. Read operations are free; write operations are billed per call via SkillPay."
homepage: https://github.com/your-github/feishu-group-ops
metadata: {"clawdbot":{"emoji":"🐦","files":["scripts/*"]}}
---

# Feishu Group Manager

## Quick Reference

| Operation | Command | Billed |
|-----------|---------|--------|
| Check permissions | `check_permissions` | Free |
| Get access token | `get_token` | Free |
| List all groups | `list_chats` | Free |
| Find group by name | `find_chat --name` | Free |
| List group members | `list_members --chat_id` | Free |
| Search user by name | `find_user --name` | Free |
| Add member to group | `add_member` | 0.002 USDT |
| Remove member | `remove_member` | 0.002 USDT |
| Send message | `send_message` | 0.002 USDT |
| Rename group | `rename_chat` | 0.002 USDT |
| Create group | `create_chat` | 0.002 USDT |

When a write operation returns `{"error": "payment_required", ...}`: stop, show the `message` field to the user, and wait for them to top up before retrying.

---

## First Use: Credential Check + Permission Verification

The user is already chatting via Feishu, so the app exists and credentials are configured. No need to ask them to set anything up.

Credentials are resolved automatically in this order:
1. Environment variables `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
2. `~/.openclaw/openclaw.json` → `channels.feishu.accounts.<any>.appId / appSecret`

On the **first request of a session**, run:

```bash
python3 {baseDir}/scripts/feishu.py check_permissions
```

**If `all_ok: true`** — proceed directly.

**If `all_ok: false`** — show the user a friendly message listing missing permissions and how to grant them, e.g.:

> "Before I can manage your groups, your Feishu app needs a couple of extra permissions (takes ~2 min).
>
> Missing:
> - `im:chat.member` — add/remove group members
> - `contact:user.id:readonly` — search members by name
>
> Steps:
> 1. Open https://open.feishu.cn/app and find your app
> 2. Go to **Permission Management** → search and enable the permissions above
> 3. Go to **Version Management** → create a new version → submit for review
> 4. Once approved (usually a few minutes), let me know and I'll continue."

Re-run `check_permissions` after the user confirms. Cache the result for the session — only re-check if the user says they just updated permissions, or if Feishu returns error code `99991672`.

---

## Execution Flow

### Step 1 — Understand intent
Confirm briefly in the user's language, e.g.: "Got it, I'll add Zhang San to the Marketing group."

### Step 2 — Gather info
```bash
python3 {baseDir}/scripts/feishu.py get_token
python3 {baseDir}/scripts/feishu.py find_chat --token TOKEN --name "marketing"
python3 {baseDir}/scripts/feishu.py find_user --token TOKEN --name "Zhang San"
```
If multiple matches are returned, list them and ask the user to confirm.

### Step 3 — Confirm before any write
> "I'm about to add **Zhang San (Marketing dept.)** to **Marketing Group**. Confirm?"

Wait for confirmation before executing.

### Step 4 — Execute and report
Success: "Done! Zhang San has been added to Marketing Group."
Failure: Explain in plain language — never expose raw API errors.

---

## Command Reference

```bash
# Check app permissions
python3 {baseDir}/scripts/feishu.py check_permissions

# Get tenant access token (auto-reads credentials)
python3 {baseDir}/scripts/feishu.py get_token

# List all groups
python3 {baseDir}/scripts/feishu.py list_chats --token TOKEN

# Find group by name (fuzzy)
python3 {baseDir}/scripts/feishu.py find_chat --token TOKEN --name "NAME"

# List group members
python3 {baseDir}/scripts/feishu.py list_members --token TOKEN --chat_id CHAT_ID

# Search user by name
python3 {baseDir}/scripts/feishu.py find_user --token TOKEN --name "NAME"

# Add member to group (billed)
python3 {baseDir}/scripts/feishu.py add_member \
  --token TOKEN --chat_id CHAT_ID \
  --target_user_id TARGET_UID --user_id CALLER_UID

# Remove member from group (billed)
python3 {baseDir}/scripts/feishu.py remove_member \
  --token TOKEN --chat_id CHAT_ID \
  --target_user_id TARGET_UID --user_id CALLER_UID

# Send message to group (billed)
python3 {baseDir}/scripts/feishu.py send_message \
  --token TOKEN --chat_id CHAT_ID --text "MESSAGE" --user_id CALLER_UID

# Rename group (billed)
python3 {baseDir}/scripts/feishu.py rename_chat \
  --token TOKEN --chat_id CHAT_ID --name "NEW NAME" --user_id CALLER_UID

# Create group and add members (billed)
python3 {baseDir}/scripts/feishu.py create_chat \
  --token TOKEN --name "GROUP NAME" --user_ids "uid1,uid2" --user_id CALLER_UID
```

`--user_id` is the caller's Feishu `open_id` — used for billing. Retrieve it from conversation context or from `find_user` results.

---

## Error Handling

| Error | Response |
|-------|----------|
| Group not found | "I couldn't find a group called 'X'. Could you give me the full name?" |
| User not found | "I couldn't find anyone called 'X'. Please check the name or provide their email." |
| Feishu error `99991672` | Re-run `check_permissions` and show missing permission guidance |
| Token expired | Automatically re-call `get_token` and retry |
| Network error | "There was a problem reaching Feishu. Please try again in a moment." |
| `payment_required` | Show the `message` field (includes top-up link), stop, wait for user |
