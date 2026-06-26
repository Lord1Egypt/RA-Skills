# Employee Reminder Ops Deployment

## Mục tiêu

Cài skill này trên máy mới theo hướng:
1. install skill
2. nạp config Google/chat đích
3. test chạy tay
4. bật scheduler 7:00 sáng

Skill đóng gói:
- logic reminder
- schema/docs
- scheduler examples

Skill không đóng gói:
- Google auth token
- Telegram/Discord bot tokens
- chat IDs thực tế
- `.env*`
- `.state/*`
- logs

## Runtime requirements
- Node.js
- gog CLI + Google auth

## Install ClawHub CLI

```bash
npm i -g clawhub
```

## Install skill from ClawHub

```bash
clawhub install employee-reminder-ops
```

## Local config needed
Tạo env cục bộ sau khi install, ví dụ:

```bash
PLAN_A_SHEET_ID='YOUR_SHEET_ID'
PLAN_A_STAFF_TAB='Trang tính1'
PLAN_A_EVENTS_TAB='NgayDacBiet'
PLAN_A_REMIND_DAYS='3'
GOG_ACCOUNT='your-google-account@gmail.com'
```

Nếu dùng Telegram/Discord sender riêng, thêm chat destination và token tương ứng ở local runtime layer.

## Google auth
Ví dụ flow:

```bash
gog auth credentials /path/to/client_secret.json
gog auth add your-google-account@gmail.com --services sheets,drive
```

Thêm Gmail nếu cần workflow mail về sau.

## Test checklist
1. Xác nhận đọc được sheet metadata
2. Xác nhận đọc được tab nhân sự
3. Xác nhận đọc được tab sự kiện
4. Chạy manual report preview
5. Chạy manual send vào chat test
6. Bật scheduler 7:00 sáng

## Scheduler note
- macOS: `launchd`
- Linux: `systemd` hoặc `cron`

## Publish

```bash
clawhub publish ./skills/employee-reminder-ops --slug employee-reminder-ops --name "Employee Reminder Ops" --version 1.0.0 --changelog "Initial release: Google Sheets reminder workflow, Telegram/Discord routing, scheduler notes"
```
