# Employee Reminder Ops on Windows

## Hỗ trợ hiện tại
- Plan A reminder workflow: supported
- Google Sheets reading: supported if `gog` works on the target environment

## Scheduler
Khuyên dùng:
- Windows Task Scheduler

## Runtime
- Node.js
- gog CLI

## Cấu hình
- tạo env local cho sheet ID, tabs, remind days, Google account
- dùng file mẫu trong `assets/windows/.env.plan-a.example`
- test manual preview trước khi tạo task tự động

## Wrapper gợi ý
- `assets/windows/start-plan-a-preview.ps1`
