---
name: employee-reminder-ops
description: Google Sheets-driven employee reminder and special-event reporting workflow for internal operations. Use when setting up or migrating birthday reminders, daily management reports, Telegram/Discord reminder routing, Google Sheets staff/event schemas, or scheduled reporting jobs that read Sheets and send summaries into team chats.
---

# Employee Reminder Ops

Use this skill when working on the internal reminder workflow currently called Plan A.

## What this skill covers

- Read employee and special-event data from Google Sheets
- Generate daily reminder reports
- Route reminder reports into Telegram or Discord groups/channels
- Configure scheduler/runtime for daily 7:00 AM reports
- Migrate the workflow to another machine

## Core workflow

1. Load staff and event data from Google Sheets
2. Normalize dates and detect upcoming birthdays/events
3. Render one report message per day
4. Send the report to the mapped chat/group/channel
5. Avoid duplicate sends for the same day

## Current data model

### Google Sheet
- Spreadsheet ID is deployment config, not hardcoded in the skill
- Staff tab example: `Trang tính1`
- Event tab example: `NgayDacBiet`

### Staff columns
- `Mã NV`
- `Họ và Tên`
- `Bộ Phận`
- `Loại hình nhân sự`
- `Vị trí`
- `Ngày sinh`

### Event columns
- `STT`
- `Tên sự kiện`
- `Ngày diễn ra`
- `Loại sự kiện`
- `Bộ phận phụ trách`
- `Ghi chú`
- `Nhắc trước`
- `Kích hoạt`

## Deployment guidance

Read `references/deployment.md` when setting up on a new machine.

## Runtime/config boundary

Keep these outside the skill package:
- Google OAuth tokens
- Telegram/Discord bot tokens
- group/channel IDs
- `.env*`
- `.state/*`
- logs

Bundle only:
- workflow scripts
- schema notes
- templates/examples
- scheduler examples
- `assets/windows/` example env file and PowerShell helper for Windows bring-up

## Included references

- `references/architecture.md` - Plan A architecture and routing notes
- `references/deployment.md` - install/migrate checklist
- `references/google-sheet-schema.md` - canonical Sheet structure for staff/events
- `references/clawhub.md` - publish/install/update commands via ClawHub
- `references/troubleshooting.md` - common runtime/scheduler/data issues
- `references/windows.md` - Windows-specific deployment notes
- `references/macos.md` - macOS-specific deployment notes
