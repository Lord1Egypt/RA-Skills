# Google Sheet Schema for Employee Reminder Ops

## Staff tab example
Suggested tab name:
- `Trang tính1`

### Required columns
- `Mã NV`
- `Họ và Tên`
- `Bộ Phận`
- `Loại hình nhân sự`
- `Vị trí`
- `Ngày sinh`

## Special event tab example
Suggested tab name:
- `NgayDacBiet`

### Required columns
- `STT`
- `Tên sự kiện`
- `Ngày diễn ra`
- `Loại sự kiện`
- `Bộ phận phụ trách`
- `Ghi chú`
- `Nhắc trước`
- `Kích hoạt`

## Date rules
- birthdays use `dd/MM/yyyy`
- birthday reminder logic compares day/month only
- special events use full event date
