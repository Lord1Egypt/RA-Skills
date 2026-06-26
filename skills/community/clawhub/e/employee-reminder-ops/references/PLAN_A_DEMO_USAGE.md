# PLAN_A_DEMO_USAGE.md

## Script

- File: `plan-a-demo.js`

## Mục đích

Script này:
- đọc dữ liệu từ Google Sheet qua `gog`
- dựng báo cáo Plan A
- có thể gửi thẳng vào Discord channel bằng bot token
- có mode production với state file chống gửi trùng cùng ngày

## Yêu cầu

- `gog` đã auth với tài khoản có quyền đọc sheet
- bot Discord đã ở trong server và có quyền gửi message vào channel đích
- có `DISCORD_BOT_TOKEN`

## Biến môi trường hỗ trợ

- `PLAN_A_SHEET_ID`
- `PLAN_A_STAFF_TAB`
- `PLAN_A_EVENTS_TAB`
- `PLAN_A_REMIND_DAYS`
- `PLAN_A_RUN_DATE`
- `DISCORD_CHANNEL_ID`
- `DISCORD_BOT_TOKEN`
- `GOG_ACCOUNT`
- `PLAN_A_STATE_DIR`
- `PLAN_A_STATE_FILE`
- `PLAN_A_ALLOW_RESEND_SAME_DAY=true`
- `PLAN_A_INCLUDE_INVALID_DETAILS=true`

## Mặc định hiện tại

- Sheet ID: `17JU1m6rBOhlD7vqSTrMOSPcEQehO04HnYg7oMeDXnn8`
- Staff tab: `Trang tính1`
- Events tab: `NgayDacBiet`
- Remind days: `3`
- Discord channel: `1483444824895000697`
- Gog account: `vinhtamforwork@gmail.com`
- State file: `.state/plan-a-state.json`

## File env cục bộ

Có thể dùng file `.env.plan-a` ở workspace root để lưu cấu hình chạy thật cục bộ.
Lưu ý: đây là file local, không nên commit vào git public.

## Cách chạy

### 1. Xem preview báo cáo

```bash
node plan-a-demo.js preview
```

### 2. Xem JSON chi tiết

```bash
node plan-a-demo.js json
```

### 3. Gửi demo vào Discord thật

```bash
DISCORD_BOT_TOKEN='YOUR_BOT_TOKEN' node plan-a-demo.js send
```

### 4. Gửi theo mode production (chống gửi trùng cùng ngày)

```bash
DISCORD_BOT_TOKEN='YOUR_BOT_TOKEN' node plan-a-demo.js prod-send
```

## Giả lập ngày chạy

Ví dụ giả lập ngày `17/03/2026`:

```bash
PLAN_A_RUN_DATE=2026-03-17 node plan-a-demo.js preview
```

hoặc

```bash
PLAN_A_RUN_DATE=17/03/2026 node plan-a-demo.js preview
```

## Ví dụ production sau này

Khi chuyển từ test sang dữ liệu thật:

```bash
PLAN_A_STAFF_TAB='Trang tính1' \
PLAN_A_EVENTS_TAB='NgayDacBiet' \
DISCORD_BOT_TOKEN='YOUR_BOT_TOKEN' \
node plan-a-demo.js prod-send
```

## Logic production hiện tại

- Sinh nhật được tính theo ngày/tháng, bỏ qua năm sinh
- Rule global đang là nhắc trước 3 ngày
- Event dùng `Nhắc trước` riêng của từng dòng
- Dòng lỗi/thiếu dữ liệu bị bỏ qua khỏi báo cáo chính và được thống kê ở mục `Dữ liệu cần rà soát`
- Có state file để chống gửi trùng cùng ngày
- Nếu lỗi gửi hoặc lỗi đọc sheet, script ghi `lastError` vào state file
- Case 29/02 ở năm không nhuận hiện bị đánh dấu là dữ liệu cần rà soát

## Lưu ý bảo mật

- Không hardcode Discord bot token vào file
- Chỉ truyền token bằng biến môi trường khi chạy
- Nếu token từng bị lộ trong chat/log, nên rotate token sau khi test xong
