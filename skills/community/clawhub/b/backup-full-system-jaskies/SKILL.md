---
name: backup-system
description: Thực hiện sao lưu toàn bộ hệ thống OpenClaw (bao gồm database, cấu hình và bộ nhớ) rồi tải lên đám mây. Yêu cầu cài đặt rclone hoặc công cụ upload tương ứng.
---

# Backup System: Sao lưu hệ thống toàn diện

Skill này giúp em bảo vệ an toàn toàn bộ dữ liệu của chúng mình bằng cách nén và tải lên đám mây (Google Drive/OneDrive) một cách tự động.

## Yêu cầu hệ thống

Để skill này hoạt động, máy của anh cần có:

1.  **Bash Shell**: Môi trường thực thi script chuẩn trên Linux.
2.  **tar & zip**: Để đóng gói và nén dữ liệu.
3.  **rclone** (Khuyến nghị): Công cụ mạnh mẽ để đồng bộ dữ liệu lên đám mây.

### Lệnh cài đặt nhanh (cho Linux/Ubuntu)

Anh chạy lệnh này để cài đặt các công cụ cần thiết nhé:

```bash
# Cài đặt công cụ nén và rclone
sudo apt update && sudo apt install -y tar zip rclone
```

### Cấu hình Đám mây (Rclone)

Trước khi chạy lần đầu, anh cần cấu hình nơi lưu trữ:

```bash
rclone config
# Làm theo hướng dẫn để thêm Google Drive hoặc tài khoản lưu trữ của anh.
# Đảm bảo đặt tên remote trùng với cấu hình trong file script backup.
```

## Quy trình thực hiện

1.  **Quét dữ liệu:** Script tự động liệt kê các thư mục quan trọng cần sao lưu (workspace, configs, memory).
2.  **Nén & Đóng gói:** Sử dụng `tar` để tạo bản lưu trữ gọn nhẹ.
3.  **Tải lên:** Sử dụng lệnh thực thi bên trong script để đẩy file lên đám mây.

## Lệnh thực thi sao lưu

```bash
bash skills/public/backup-system/scripts/backup_full_system.sh
```

## Lưu ý
- **Thời gian:** Quá trình sao lưu có thể mất từ 1-5 phút tùy thuộc vào dung lượng bộ nhớ của em.
- **Bảo mật:** Script đã được thiết kế để không làm lộ các mã khóa bí mật trong quá trình nén nếu được cấu hình đúng.
- **Định kỳ:** Anh có thể kết hợp với công cụ `cron` để đặt lịch sao lưu tự động hàng tuần.
