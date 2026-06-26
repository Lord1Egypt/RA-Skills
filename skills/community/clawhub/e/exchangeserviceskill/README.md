# ExchangeService (Exchange On-Prem EWS Skill)

A Node.js skill for OpenClaw that provides EWS (SOAP) operations against on‑prem Exchange Server 2016 CU21. It supports mail, folders, and calendar/meeting workflows with explicit write confirmations.

## Highlights
- Mail list/search/read and unread count
- Mail create/update/move/copy/delete/send/reply
- Mark-all-read for a folder
- Folder CRUD
- Calendar read (CalendarView) and meeting creation
- Encrypted config via `exchange.config.json`

## Requirements
- Node.js 20+ (22+ recommended)
- Exchange EWS endpoint: `/EWS/Exchange.asmx`

## Install
```bash
npm install
```

## Configure
Generate an encrypted config (recommended):
```bash
npm run setup-config -- \
  --exchange-url https://mail.example.com/EWS/Exchange.asmx \
  --username user \
  --auth-mode ntlm \
  --password "<password>" \
  --master-key "<masterKey>"
```

Config file location:
- `config/exchange.config.json`
- Sample: `config/exchange.config.sample.json`

## Safety Policy
- Read‑first by default
- Any write operation requires explicit confirmation
- Write commands require `--confirm true` (or `EXCHANGE_WRITE_CONFIRM=true`)
- `--dry-run` is supported for write commands to preview SOAP body

## Defaults That Matter
- `get-mail` / `search-mail` default scope is `all` (msgfolderroot)
- Default includes subfolders of the scope
- Default time window is last 3650 days (use `--days-back` to narrow)

## Usage

Read commands:
```bash
npm run verify-login
npm run get-mail -- --unread-only --limit 10
npm run get-mail -- --scope all --limit 10
npm run search-mail -- --query "keyword" --limit 10
npm run get-item -- --item-id <EWS_ITEM_ID>
npm run get-unread-count -- --scope all
npm run get-folder -- --distinguished-id inbox
npm run find-folder -- --parent-distinguished-id msgfolderroot --traversal Shallow --limit 50
npm run get-calendar -- --limit 20
```

Write commands (require confirm):
```bash
npm run create-mail -- --confirm true --to a@b.com --subject "s" --body "b"
npm run reply-item -- --confirm true --item-id <id> --body "thanks"
npm run update-item -- --confirm true --item-id <id> --subject "new"
npm run mark-all-read -- --confirm true --distinguished-id inbox
npm run create-folder -- --confirm true --display-name "My Folder" --parent-distinguished-id inbox
npm run update-folder -- --confirm true --folder-id <id> --change-key <ck> --display-name "New Name"
npm run delete-folder -- --confirm true --folder-id <id> --delete-type MoveToDeletedItems
npm run move-item -- --confirm true --item-id <id> --target-distinguished-id inbox
npm run copy-item -- --confirm true --item-id <id> --target-distinguished-id drafts
npm run delete-item -- --confirm true --item-id <id> --delete-type MoveToDeletedItems
npm run send-item -- --confirm true --item-id <draftId>
npm run send-item -- --confirm true --item-id <draftId> --change-key <ck>
npm run archive-item -- --confirm true --item-id <id>
npm run create-meeting -- --confirm true --subject "Weekly Sync" --start "2026-03-18T09:00:00+08:00" --end "2026-03-18T09:30:00+08:00" --required a@b.com --location "Room A" --body "Agenda" --send-invitations SendToAllAndSaveCopy
```

## OpenClaw Packaging
If you package for OpenClaw, do not include:
- `node_modules/`
- `config/exchange.config.json`
- `.git/`
- `references/`

Use `config/exchange.config.sample.json` for demo/config guidance.

## References
- https://learn.microsoft.com/en-us/exchange/client-developer/web-service-reference/ews-operations-in-exchange

---

# 中文简介

ExchangeService 是一个用于 OpenClaw 的 Node.js 技能，基于 EWS (SOAP) 对本地部署的 Exchange Server 2016 CU21 提供邮件、文件夹与日历/会议能力。所有写操作都需要显式确认，配置文件使用加密方式保存密码。

## 功能概览
- 邮件列表/搜索/详情/未读统计
- 邮件创建/更新/移动/复制/删除/发送/回复
- 文件夹创建/更新/删除/查找
- 日历读取与创建会议

## 配置
推荐使用 `npm run setup-config` 生成 `config/exchange.config.json`（加密存储）。
示例配置请参考 `config/exchange.config.sample.json`。

## 默认行为
- `get-mail` / `search-mail` 默认范围为全文件夹（msgfolderroot）
- 默认包含子文件夹
- 默认时间范围为最近 3650 天（可用 `--days-back` 缩小范围）
