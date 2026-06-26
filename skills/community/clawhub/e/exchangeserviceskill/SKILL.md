---
name: exchangeservice
description: Cross-platform (Linux/macOS/Windows) skill for Exchange Server 2016 CU21 EWS operations on OpenClaw Node.js runtime.
metadata: {"openclaw":{"emoji":"✉️","requires":{"env":["EXCHANGE_URL","EXCHANGE_USERNAME","EXCHANGE_AUTH_MODE","EXCHANGE_PASSWORD","EXCHANGE_SKILL_MASTER_KEY"],"bins":["node","npm"]},"primaryEnv":"EXCHANGE_PASSWORD"}}
---

# Exchange On-Prem Skill

## Overview
This skill provides EWS (SOAP) operations for on‑prem Exchange 2016 CU21: mail, folders, and calendar/meetings.

## Requirements
- Node.js 20+ (22+ recommended)
- Exchange EWS endpoint: `/EWS/Exchange.asmx`

## Quick Start
1) Install deps:
```
npm install
```
2) Create encrypted config:
```
npm run setup-config -- \
  --exchange-url https://mail.example.com/EWS/Exchange.asmx \
  --username user \
  --auth-mode ntlm \
  --password "<password>" \
  --master-key "<masterKey>"
```
3) Verify:
```
npm run verify-login
```

## Safety Policy
- Read-first by default
- Any write operation requires explicit confirmation
- Write commands require `--confirm true` (or `EXCHANGE_WRITE_CONFIRM=true`)
- `--dry-run` is supported for write commands to preview SOAP body
- `--insecure true` (if used) only relaxes TLS validation per request and does not change global Node TLS settings

## Config Model
File: `config/exchange.config.json`
Required fields: `exchange_url`, `username`, `auth_mode`, `secret_store`
Optional: `domain`

## Capability Groups & Status
Status:
- `READY`: implemented and verified
- `RESTRICTED`: write/risky actions require explicit confirmation
- `LIMITED`: implemented but blocked by environment limitations

### A) Mailbox & Items
- `FindItem` (mail list/read window): `READY`
- `SearchMail` (keyword in subject/body/recipients): `READY`
- `GetItem`: `READY`
- `GetUnreadCount`: `READY`
- `CreateItem` (mail create): `READY` `RESTRICTED`
- `UpdateItem`: `READY` `RESTRICTED`
- `MoveItem / CopyItem / DeleteItem`: `READY` `RESTRICTED`
- `SendItem`: `READY` `RESTRICTED`
- `ReplyItem / ReplyAll`: `READY` `RESTRICTED`
- `MarkAllItemsAsRead`: `READY` `RESTRICTED`
- `ArchiveItem`: `LIMITED` `RESTRICTED`

### B) Folders
- `GetFolder`: `READY`
- `FindFolder`: `READY`
- `CreateFolder`: `READY` `RESTRICTED`
- `UpdateFolder`: `READY` `RESTRICTED`
- `DeleteFolder`: `READY` `RESTRICTED`

### C) Calendar & Meetings
- Calendar window read (`FindItem + CalendarView`): `READY`
- Create meeting (`CreateItem` CalendarItem): `READY` `RESTRICTED`

### D) Structure & Config
- `exchange.config.json` create/update: `READY`
- Scripts organized by module folders: `READY`
- SKILL.md commands and status updated: `READY`

## Defaults That Matter
- `get-mail` / `search-mail` default scope is `all` (msgfolderroot).
- `get-mail` / `search-mail` default includes subfolders of the scope.
- `get-mail` / `search-mail` default time window is last 3650 days. Use `--days-back` to narrow.
- `get-calendar` default time window is next 7 days. Use `--start-time` / `--end-time` to override.

## Command List

Read commands:
- `npm run verify-login`
- `npm run get-mail -- --unread-only --limit 10`
- `npm run get-mail -- --scope all --limit 10` (all folders under msgfolderroot)
- `npm run get-mail -- --scope all --days-back 3650 --limit 10`
- `npm run search-mail -- --query "keyword" --limit 10`
- `npm run search-mail -- --scope all --query "keyword" --limit 10`
- `npm run get-item -- --item-id <EWS_ITEM_ID>`
- `npm run get-unread-count -- --scope all` (all folders under msgfolderroot)
- `npm run get-folder -- --distinguished-id inbox`
- `npm run find-folder -- --parent-distinguished-id msgfolderroot --traversal Shallow --limit 50`
- `npm run get-calendar -- --limit 20`
- `npm run get-calendar -- --start-time 2026-03-01T00:00:00+08:00 --end-time 2026-05-01T00:00:00+08:00 --limit 200`

Write commands (require confirm):
- `npm run create-mail -- --confirm true --to a@b.com --subject "s" --body "b"`
- `npm run reply-item -- --confirm true --item-id <id> --body "thanks"` (supports `--reply-all true`)
- `npm run update-item -- --confirm true --item-id <id> --subject "new"` (auto-fetches ChangeKey if omitted)
- `npm run mark-all-read -- --confirm true --distinguished-id inbox`
- `npm run create-folder -- --confirm true --display-name "My Folder" --parent-distinguished-id inbox`
- `npm run update-folder -- --confirm true --folder-id <id> --change-key <ck> --display-name "New Name"`
- `npm run delete-folder -- --confirm true --folder-id <id> --delete-type MoveToDeletedItems`
- `npm run move-item -- --confirm true --item-id <id> --target-distinguished-id inbox`
- `npm run copy-item -- --confirm true --item-id <id> --target-distinguished-id drafts`
- `npm run delete-item -- --confirm true --item-id <id> --delete-type MoveToDeletedItems`
- `npm run send-item -- --confirm true --item-id <draftId>`
- `npm run send-item -- --confirm true --item-id <draftId> --change-key <ck>` (recommended; send will auto-fetch ChangeKey if omitted)
- `npm run archive-item -- --confirm true --item-id <id>`
- `npm run create-meeting -- --confirm true --subject "Weekly Sync" --start "2026-03-18T09:00:00+08:00" --end "2026-03-18T09:30:00+08:00" --required a@b.com --location "Room A" --body "Agenda" --send-invitations SendToAllAndSaveCopy`

Send receipt verification:
- `create-mail`, `reply-item`, `send-item` support `--verify-sent true|false`, `--verify-window-minutes <n>`, `--verify-max-entries <n>`, `--verify-strict true|false`

## References
- https://learn.microsoft.com/en-us/exchange/client-developer/web-service-reference/ews-operations-in-exchange
