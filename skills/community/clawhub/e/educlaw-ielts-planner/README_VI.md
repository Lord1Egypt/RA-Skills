# 📚 EduClaw — Trợ Lý Học IELTS Cá Nhân

> Một skill cho [OpenClaw](https://openclaw.dev) biến AI agent thành trợ lý học IELTS chuyên dụng — tự động lên kế hoạch, đồng bộ Google Calendar, tìm tài liệu và theo dõi tiến độ.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[🇬🇧 Read in English](README.md)**

---

## Tổng Quan

EduClaw là skill quản lý học IELTS toàn diện cho OpenClaw. Tự động hóa toàn bộ quy trình — từ tạo lộ trình cá nhân hóa đến lên lịch trên Google Calendar với mô tả bài học chi tiết, độc nhất cho từng buổi.

### Tính Năng Chính

- **Song ngữ Anh-Việt** — Tự phát hiện ngôn ngữ, phản hồi nhất quán
- **Quy trình 4 bước** — Hỏi lịch → Nghiên cứu & Lập kế hoạch → Calendar → Tài liệu
- **Tích hợp Google Calendar** — Tạo sự kiện chi tiết qua `gcalcli` với mô tả độc nhất mỗi buổi
- **Lên lịch thông minh** — Tôn trọng khung giờ người dùng, xử lý xung đột tương tác
- **Múi giờ động** — Phát hiện múi giờ hệ thống lúc chạy (không bao giờ hardcode)
- **Cron tự động** — Chuẩn bị bài hằng ngày, báo cáo tuần, cập nhật tài liệu qua Discord
- **SQLite Database** — Cơ sở dữ liệu tiến độ local với 4 bảng (sessions, vocabulary, materials, weekly_summaries) — hỗ trợ query phức tạp, ACID-compliant
- **Thông báo Discord** — Cảnh báo xung đột lịch, nhắc nhở học tập, báo cáo tiến độ
- **Lộ trình 4 tháng** — Band 6.0 → 7.5+ chia 4 giai đoạn

---

## Yêu Cầu

| Phụ thuộc | Mục đích |
|----------|----------|
| [OpenClaw](https://openclaw.dev) | Nền tảng agent (khuyên v2026.3+) |
| [gcalcli](https://github.com/insanum/gcalcli) | CLI Google Calendar (cần xác thực) |
| Tài khoản Google Calendar | Lên lịch buổi học |
| Discord bot (tùy chọn) | Nhận thông báo và cron |

### Tùy Chọn

- Web search trong OpenClaw — tìm tài liệu tự động

> **📖 Lần đầu cài đặt?** Xem **[Hướng dẫn cài đặt đầy đủ (VI)](SETUP_VI.md)** | **[Complete Setup Guide (EN)](SETUP.md)** — hướng dẫn từng bước tất cả tool, API key, tạo bot, và nhiều hơn.

---

## Cài Đặt

### Từ OpenClaw Skills Registry

```bash
openclaw skill install educlaw-ielts-planner
```

### Cài Đặt Thủ Công

1. Clone repo:
   ```bash
   git clone https://github.com/moclaw/educlaw-ielts-planner.git
   ```

2. Copy vào thư mục skills:
   ```bash
   cp -r educlaw-ielts-planner ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/
   ```

3. Kiểm tra:
   ```bash
   openclaw skill list
   ```

### Thiết Lập Trước Khi Dùng

1. **Cài đặt & xác thực gcalcli:**
   ```bash
   pip install gcalcli
   gcalcli list   # Làm theo OAuth flow để xác thực
   ```

2. **Bật web search** trong `openclaw.json`:
   ```json
   {
     "agents": {
       "defaults": {
         "webSearch": true
       }
     }
   }
   ```

---

## Cách Sử Dụng

### Discord

```
@Jaclyn Lên kế hoạch học IELTS 7.5 trong 4 tháng
```

Hoặc dùng slash command:
```
/educlaw_ielts_planner
```

### Terminal (TUI)

```bash
openclaw tui
# Gõ: "Lên kế hoạch học IELTS 7.5"
```

### CLI

```bash
openclaw agent --message "Lên kế hoạch học IELTS 7.5 trong 4 tháng"
openclaw agent --message "Tạo lịch IELTS tuần này"
openclaw agent --message "Xem tiến độ IELTS"
```

---

## Quy Trình Hoạt Động

### Bước 0: Hỏi Khung Giờ Học
Agent hỏi giờ học ưu tiên, ngày available, thời gian bận. **Không bao giờ tự chọn giờ.**

### Bước 1: Nghiên Cứu & Lập Kế Hoạch
- Xem lại lịch sử học từ các buổi trước
- Tìm tài liệu mới, cụ thể (sách, YouTube, website)
- Xây lịch 2 tuần cuốn chiếu với từ vựng, bài tập, mục tiêu
- Trình bày kế hoạch và **chờ phê duyệt**

### Bước 2: Tạo Sự Kiện Google Calendar
- Kiểm tra slot trống trong khung giờ đã chọn
- Xử lý xung đột tương tác (không tự giải quyết)
- Tạo sự kiện với **mô tả 100% độc nhất** — mỗi buổi có từ vựng, tài liệu, bài tập riêng
- Đặt nhắc nhở 15 phút trước mỗi buổi

### Bước 3: Tài Liệu
- Tạo/cập nhật `IELTS_STUDY_PLAN.md` với lộ trình, từ vựng, tài nguyên
- Khởi tạo SQLite database (`workspace/tracker/educlaw.db`) với 4 bảng

---

## Lộ Trình 4 Tháng (Band 6.0 → 7.5+)

| Giai Đoạn | Tuần | Mục Tiêu |
|-----------|------|----------|
| **Phase 1: Nền tảng** | 1–4 | Nắm format đề, xây dựng từ vựng & ngữ pháp |
| **Phase 2: Xây dựng kỹ năng** | 5–8 | Nâng cao kỹ thuật, hướng tới band 6.5 |
| **Phase 3: Nâng cao** | 9–12 | Ổn định band 7.0, điều kiện thi thực |
| **Phase 4: Mô phỏng thi** | 13–16 | Ổn định 7.0–7.5, sẵn sàng thi |

---

## Cron Jobs (Hỗ Trợ Học Tự Động)

| Job | Lịch | Mục đích |
|-----|------|----------|
| `ielts-calendar-watcher` | Mỗi 2 giờ | Phát hiện xung đột lịch với buổi học |
| `ielts-daily-prep` | 23:00 CN–T6 | Chuẩn bị bài cho ngày mai (từ vựng, tài liệu, ôn tập) |
| `ielts-meeting-conflict-check` | 08:00 T2–T7 | Kiểm tra xung đột sáng nay |
| `ielts-weekly-report` | Chủ nhật 10:00 | Tổng kết tiến độ tuần |
| `ielts-weekly-material-update` | Thứ 7, 14:00 | Tài liệu mới cho tuần tới |

---

## Theo Dõi Tiến Độ (SQLite Database)

EduClaw dùng SQLite database tại `workspace/tracker/educlaw.db` làm nguồn dữ liệu chính:

| Bảng | Theo dõi |
|-------|----------|
| **sessions** | Ngày, giai đoạn, kỹ năng, chủ đề, event_id, trạng thái, điểm |
| **vocabulary** | Từ, IPA, nghĩa, collocations, ví dụ, số lần ôn, trạng thái |
| **materials** | Tên, loại, URL, kỹ năng, giai đoạn, đánh giá |
| **weekly_summaries** | Buổi học hoàn thành, từ vựng, điểm mock test |

> **Tại sao dùng SQLite?** Hỗ trợ query phức tạp (aggregation, join, filter), ACID-compliant, dùng `sqlite3` CLI hoặc Python built-in. Không cần API bên ngoài. Cron jobs query trực tiếp từ DB.

---

## Quy Tắc An Toàn

| Quy tắc | Chi tiết |
|---------|----------|
| ❌ Không xóa event không có trong DB | Chỉ xóa event có event_id trong SQLite database, sau khi user xác nhận |
| ❌ Không tự chọn giờ | Luôn hỏi trước (Bước 0) |
| ❌ Không tự giải quyết xung đột | Hiện lựa chọn, chờ phản hồi |
| ❌ Không hardcode múi giờ | Phát hiện từ hệ thống lúc chạy |
| ❌ Không tạo >14 sự kiện cùng lúc | Chia theo 2 tuần |
| ❌ Không dùng link chưa xác minh | Mọi URL trong event phải được fetch & kiểm tra nội dung trước khi đưa vào |
| ✅ Luôn phát hiện ngôn ngữ | Phản hồi nhất quán |
| ✅ Luôn hỏi lịch trước | Trước khi xếp lịch |
| ✅ Luôn chờ phê duyệt | Trước khi tạo sự kiện |
| ✅ Mô tả luôn độc nhất | Không trùng từ vựng/tài liệu giữa các buổi |

---

## Cấu Trúc Thư Mục

```
educlaw-ielts-planner/
├── README.md           # Tài liệu tiếng Anh
├── README_VI.md        # Tài liệu tiếng Việt (file này)
├── SETUP.md            # Hướng dẫn cài đặt đầy đủ (EN)
├── SETUP_VI.md         # Hướng dẫn cài đặt đầy đủ (VI)
├── SKILL.md            # Prompt skill OpenClaw (logic chính)
├── WORKFLOW.md          # Hướng dẫn thực thi từng bước
├── schema.sql          # Schema SQLite database
├── _meta.json          # Metadata skill
├── LICENSE             # Giấy phép MIT
├── CHANGELOG.md        # Lịch sử phiên bản
└── examples/
    └── sample-events.md # Ví dụ sự kiện calendar
```

---

## Đóng Góp

1. Fork repo
2. Tạo branch (`git checkout -b feature/tinh-nang-moi`)
3. Commit (`git commit -m 'Thêm tính năng mới'`)
4. Push (`git push origin feature/tinh-nang-moi`)
5. Tạo Pull Request

---

## Giấy Phép

Dự án này được cấp phép theo MIT License — xem file [LICENSE](LICENSE).

---

## Tác Giả

**moclaw** — [GitHub](https://github.com/moclaw)

Xây dựng với [OpenClaw](https://openclaw.dev) 🦞
