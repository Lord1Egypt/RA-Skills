# Employee Reminder Ops Troubleshooting

## Không đọc được Google Sheet
- kiểm tra `gog` đã auth chưa
- kiểm tra đúng account Google chưa
- kiểm tra `PLAN_A_SHEET_ID` đúng chưa
- kiểm tra tab staff/event đúng tên chưa

## Reminder không ra dữ liệu
- kiểm tra format `Ngày sinh`
- kiểm tra tab event có dữ liệu active không
- kiểm tra logic remind days

## Scheduler không chạy
- macOS: kiểm tra `launchd`
- Linux: kiểm tra `systemd` hoặc `cron`
- Windows: kiểm tra Task Scheduler

## Gửi chat/group sai đích
- kiểm tra chat ID / destination config local
- test manual send trước khi bật lịch tự động
