# Manual Patching Guide

If the automatic patch script fails, follow these steps to apply the patch manually.

## Target File

The monitor file location depends on your OpenClaw installation:

- **openclaw-lark extension (v2026.3+):** `~/.openclaw/extensions/openclaw-lark/src/channel/monitor.js`
- **Built-in feishu extension (older):** `/usr/lib/node_modules/openclaw/extensions/feishu/src/monitor.ts`

## What the Patch Does

1. Adds a **debounce map** (30s per fileToken) to prevent event storms
2. Adds a **`_handleDriveEditEvent`** function that:
   - Checks for bot self-edits (anti-loop)
   - Applies debounce (30s per file)
   - Reads `~/.openclaw/openclaw.json` for hooks token and gateway port
   - POSTs to `http://127.0.0.1:{port}/hooks/agent` with `deliver: false, name: "DocCollab"`
3. Registers event handlers:
   - `drive.file.edit_v1` -> `_handleDriveEditEvent`
   - `drive.file.bitable_record_changed_v1` -> `_handleDriveEditEvent`
   - `drive.file.read_v1` -> empty handler (suppress warnings)

## Easiest Approach

Copy the reference file directly:

[35m[plugins][39m [36mfeishu_chat: Registered feishu_chat, feishu_chat_members[39m
[35m[plugins][39m [36mfeishu_im: Registered feishu_im_user_message, feishu_im_user_fetch_resource, feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages[39m
[35m[plugins][39m [36mfeishu_search: Registered feishu_search_doc_wiki[39m
[35m[plugins][39m [36mfeishu_drive: Registered feishu_drive_file, feishu_doc_comments, feishu_doc_media[39m
[35m[plugins][39m [36mfeishu_wiki: Registered feishu_wiki_space, feishu_wiki_space_node[39m
[35m[plugins][39m [36mfeishu_sheets: Registered feishu_sheet tool[39m
[35m[plugins][39m [36mfeishu_im_bot_image: Registered feishu_im_bot_image tool[39m
[35m[plugins][39m [36mfeishu_im: Registered feishu_im_bot_image[39m
[35m[plugins][39m [36mRegistered all OAPI tools (calendar, task, bitable, search, drive, wiki, sheets, im)[39m
[35m[plugins][39m [36mfeishu_doc: Registered feishu_fetch_doc, feishu_create_doc, feishu_update_doc[39m
[35m[plugins][39m [36mfeishu_oauth: Registered feishu_oauth tool[39m
[35m[plugins][39m [36mfeishu_oauth_batch_auth: Registered feishu_oauth_batch_auth tool[39m
Gateway service disabled.
Start with: openclaw gateway install
Start with: openclaw gateway
Start with: systemctl --user start openclaw-gateway.service

## Key Details

- The `/hooks/agent` POST body must include `deliver: false` to prevent the isolated session
  from trying to deliver results via IM (doc collab writes back to the document directly)
- The `name: "DocCollab"` field helps identify hook sessions in logs
- For .js files (openclaw-lark), no jiti cache clearing is needed
- For .ts files (older installs), clear jiti cache after patching:
  `rm -f /tmp/jiti/src-monitor.*.cjs`

## Required Feishu App Permissions

**User OAuth Scopes** (user must authorize via card):
- `space:document:retrieve` - read documents
- `base:table:read` - read bitable table structure
- `base:record:read` - read bitable records
- `base:record:update` - update bitable records
- `base:field:read` - read bitable field definitions

**App-level Permissions** (enable in Feishu Open Platform console):
- `docx:document:readonly` - read docx content
- `drive:drive:readonly` - read drive file info

## Verification

After restarting, edit a Feishu doc and check logs for:

