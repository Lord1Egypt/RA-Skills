# 🛠️ Hướng Dẫn Cài Đặt EduClaw — Từ A đến Z

> Hướng dẫn từng bước cài đặt **EduClaw IELTS Study Planner** từ đầu, bao gồm OpenClaw, Google Calendar, Google AI (Gemini), Discord bot, Telegram bot, web search, và SQLite.

**[🇬🇧 Read in English](SETUP.md)**

---

## Mục Lục

1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Cài đặt OpenClaw](#2-cài-đặt-openclaw)
3. [Cấu hình Google Cloud (API Keys)](#3-cấu-hình-google-cloud)
4. [Cấu hình OpenClaw với API Key](#4-cấu-hình-openclaw-với-api-key)
5. [Cài đặt & Xác thực gcalcli (Google Calendar)](#5-cài-đặt--xác-thực-gcalcli)
6. [Bật Web Search](#6-bật-web-search)
7. [Tạo & Kết nối Discord Bot](#7-tạo--kết-nối-discord-bot)
8. [Tạo & Kết nối Telegram Bot (Tùy chọn)](#8-tạo--kết-nối-telegram-bot-tùy-chọn)
9. [Cài đặt SQLite](#9-cài-đặt-sqlite)
10. [Cài đặt EduClaw Skill](#10-cài-đặt-educlaw-skill)
11. [Khởi động OpenClaw Gateway](#11-khởi-động-openclaw-gateway)
12. [Danh sách kiểm tra](#12-danh-sách-kiểm-tra)
13. [Xử lý sự cố](#13-xử-lý-sự-cố)

---

## 1. Yêu Cầu Hệ Thống

| Yêu cầu | Phiên bản tối thiểu |
|----------|---------------------|
| **OS** | Linux (Ubuntu/Debian khuyên dùng), macOS, hoặc WSL2 |
| **Node.js** | v20+ (`node --version`) |
| **Python** | 3.10+ (`python3 --version`) |
| **pip** | Mới nhất (`pip3 --version`) |
| **Git** | Bất kỳ phiên bản gần đây |
| **Tài khoản Google** | Cho Calendar + AI API |

---

## 2. Cài Đặt OpenClaw

### Cách A: Cài một dòng (khuyên dùng)

```bash
curl -fsSL https://get.openclaw.dev | bash
```

### Cách B: Cài qua npm

```bash
npm install -g openclaw
```

### Kiểm tra

```bash
openclaw --version
# Kết quả: OpenClaw 2026.x.x
```

### Khởi tạo OpenClaw

```bash
openclaw config
```

Wizard sẽ:
- Tạo thư mục `~/.openclaw/`
- Hỏi nhà cung cấp model và API key
- Thiết lập cấu hình cơ bản

Chạy lại wizard bất cứ lúc nào:
```bash
openclaw config          # Wizard đầy đủ
openclaw doctor          # Kiểm tra sự cố
```

---

## 3. Cấu Hình Google Cloud

EduClaw cần hai API key từ Google:
1. **Gemini API Key** — cho AI model (Gemini 2.5/3.x)
2. **Google Calendar OAuth** — cho gcalcli đọc/ghi sự kiện lịch

### 3.1. Lấy Gemini API Key (cho AI model)

1. Truy cập [Google AI Studio](https://aistudio.google.com/apikey)
2. Nhấn **"Create API Key"**
3. Chọn hoặc tạo Google Cloud project
4. Copy API key (bắt đầu bằng `AIzaSy...`)
5. **Quan trọng:** Kiểm tra [billing/quota](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas) — free tier có giới hạn. Tăng spending cap nếu cần.

> **Lưu key này** — bạn sẽ cần ở Bước 4.

### 3.2. Bật Google Calendar API

1. Vào [Google Cloud Console → APIs & Services](https://console.cloud.google.com/apis/library)
2. Tìm **"Google Calendar API"**
3. Nhấn **Enable**
4. Vào [Credentials](https://console.cloud.google.com/apis/credentials)
5. Nhấn **"+ CREATE CREDENTIALS" → "OAuth client ID"**
6. Nếu được hỏi, cấu hình **OAuth consent screen** trước:
   - User Type: **External** (hoặc Internal nếu dùng Google Workspace)
   - App name: ví dụ `EduClaw Calendar`
   - User support email: email của bạn
   - Scopes: thêm `https://www.googleapis.com/auth/calendar`
   - Test users: thêm email bạn
   - Lưu
7. Quay lại Credentials → **"+ CREATE CREDENTIALS" → "OAuth client ID"**:
   - Application type: **Desktop app**
   - Name: ví dụ `gcalcli`
   - Nhấn **Create**
8. Tải file **JSON** (client secret) — sẽ dùng cho gcalcli

> **Giữ file JSON này** — dùng ở Bước 5.

### 3.3. Lấy Web Search API Key (tùy chọn nhưng khuyên dùng)

EduClaw dùng web search để tìm tài liệu học. Hai cách:

#### Cách A: Dùng Gemini search grounding (dễ nhất)
Nếu Gemini API key có hỗ trợ search grounding, dùng cùng key. Bỏ qua đến Bước 6.

#### Cách B: Google Custom Search API
1. Vào [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/all)
2. Tạo search engine mới → tìm toàn bộ web
3. Copy **Search Engine ID (cx)**
4. Vào [Custom Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com) → **Enable**
5. Tạo API key (hoặc dùng key hiện có)

---

## 4. Cấu hình OpenClaw với API Key

### Cách A: Qua setup wizard

```bash
openclaw config
# Chọn "google" làm provider
# Dán Gemini API key khi được hỏi
```

### Cách B: Cấu hình thủ công

Sửa `~/.openclaw/agents/main/agent/auth-profiles.json`:
```json
{
  "version": 1,
  "profiles": {
    "google:default": {
      "type": "api_key",
      "provider": "google",
      "key": "GEMINI_API_KEY_CỦA_BẠN"
    }
  }
}
```

### Cấu hình model

Sửa `~/.openclaw/openclaw.json` → `agents.defaults.model`:
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3-flash-preview",
        "fallbacks": [
          "google/gemini-2.5-flash",
          "google/gemini-2.5-pro"
        ]
      }
    }
  }
}
```

### Kiểm tra model hoạt động

```bash
openclaw agent --message "Xin chào, trả lời OK"
# Phải nhận được phản hồi từ model
```

---

## 5. Cài Đặt & Xác Thực gcalcli

gcalcli là công cụ dòng lệnh cho Google Calendar.

### Cài đặt

```bash
pip3 install gcalcli
```

> Nếu gặp lỗi `externally-managed-environment` trên Ubuntu 24+:
> ```bash
> pip3 install --break-system-packages gcalcli
> # HOẶC dùng pipx:
> pipx install gcalcli
> ```

### Xác thực OAuth

#### Cách A: Dùng file client secret JSON từ Bước 3.2

```bash
gcalcli --client-id /đường/dẫn/client_secret.json list
```

Trình duyệt sẽ mở ra để xác thực. Đăng nhập Google và cho phép.

#### Cách B: Chạy lần đầu (mặc định)

```bash
gcalcli list
```

Lần đầu chạy, gcalcli sẽ:
1. Mở cửa sổ trình duyệt
2. Yêu cầu đăng nhập Google
3. Xin quyền truy cập lịch
4. Lưu credentials tại (~/.gcalcli_oauth)

### Kiểm tra

```bash
gcalcli --nocolor list
# Kết quả ví dụ:
#  owner  moclaw128@gmail.com
#  reader Holidays in Viet Nam
```

```bash
gcalcli --nocolor agenda
# Hiện các sự kiện sắp tới (hoặc trống nếu chưa có)
```

---

## 6. Bật Web Search

Web search giúp EduClaw tự động tìm tài liệu IELTS.

### Dùng Gemini search grounding (khuyên dùng)

Sửa `~/.openclaw/openclaw.json`:
```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "gemini",
        "gemini": {
          "apiKey": "API_KEY_WEB_SEARCH_CỦA_BẠN"
        }
      }
    }
  }
}
```

> Có thể dùng cùng Gemini API key nếu hỗ trợ search grounding, hoặc key riêng.

### Kiểm tra

```bash
openclaw agent --message "Tìm trên web 'IELTS Listening tips 2026' và cho tôi 3 link"
# Phải trả về URL thực từ web search
```

---

## 7. Tạo & Kết Nối Discord Bot

### 7.1. Tạo Discord Application

1. Vào [Discord Developer Portal](https://discord.com/developers/applications)
2. Nhấn **"New Application"**
3. Đặt tên (ví dụ: `Jaclyn`, `EduClaw Bot`)
4. Vào tab **"Bot"** bên trái
5. Nhấn **"Reset Token"** → **Copy bot token**
6. Trong **Privileged Gateway Intents**, bật:
   - ✅ **Message Content Intent**
   - ✅ **Server Members Intent** (tùy chọn)
   - ✅ **Presence Intent** (tùy chọn)

### 7.2. Tạo Link Mời Bot

1. Vào **"OAuth2" → "URL Generator"**
2. Chọn scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Chọn bot permissions:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Embed Links
   - ✅ Use Slash Commands
   - ✅ Send Messages in Threads
   - ✅ Manage Messages (tùy chọn)
4. Copy URL đã tạo
5. Mở URL → chọn server Discord → **Authorize**

### 7.3. Kết nối với OpenClaw

```bash
openclaw channels add \
  --channel discord \
  --token "TOKEN_DISCORD_BOT_CỦA_BẠN" \
  --name "Jaclyn"
```

Hoặc sửa trực tiếp `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "discord": {
      "name": "Jaclyn",
      "enabled": true,
      "token": "TOKEN_DISCORD_BOT_CỦA_BẠN",
      "groupPolicy": "open",
      "streaming": "partial"
    }
  }
}
```

### 7.4. Khởi động lại & kiểm tra

```bash
systemctl --user restart openclaw-gateway
openclaw channels status
# Phải hiện Discord: connected
```

### 7.5. Deploy slash commands

```bash
openclaw directory self --channel discord
```

Deploy các lệnh slash lên Discord (ví dụ: `/educlaw_ielts_planner`, `/help`...)

### 7.6. Test

- Mở Discord
- DM bot hoặc mention trong server: `@Jaclyn xin chào`
- Phải nhận được phản hồi

### 7.7. Sửa lỗi "not authorized" trong server

Nếu slash commands chạy được trong DM nhưng hiện "not authorized" trong server:

1. Vào **Server Settings → Integrations**
2. Tìm bot → nhấn **"Manage"**
3. Bật commands cho channels/roles muốn dùng
4. Đảm bảo bot có quyền gửi tin nhắn và dùng slash commands trong channel đó

---

## 8. Tạo & Kết Nối Telegram Bot (Tùy Chọn)

### 8.1. Tạo Telegram Bot

1. Mở Telegram, tìm **@BotFather**
2. Gửi `/newbot`
3. Chọn tên (ví dụ: `EduClaw Bot`)
4. Chọn username (phải kết thúc bằng `bot`, ví dụ: `educlaw_ielts_bot`)
5. **Copy bot token** mà BotFather cung cấp (dạng: `1234567890:ABCdefGHI...`)

### 8.2. Cấu hình bot (tùy chọn)

Gửi các lệnh sau cho @BotFather:
```
/setdescription    → "Trợ lý học IELTS cá nhân"
/setabouttext      → "EduClaw giúp bạn lên kế hoạch và theo dõi việc học IELTS với Google Calendar"
/setcommands       → plan - Lên kế hoạch IELTS
                     progress - Xem tiến độ
                     schedule - Lên lịch 2 tuần tới
```

### 8.3. Kết nối với OpenClaw

```bash
openclaw channels add \
  --channel telegram \
  --token "TOKEN_TELEGRAM_BOT_CỦA_BẠN" \
  --name "EduClaw"
```

Hoặc sửa `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "telegram": {
      "name": "EduClaw",
      "enabled": true,
      "token": "TOKEN_TELEGRAM_BOT_CỦA_BẠN"
    }
  }
}
```

### 8.4. Khởi động lại & kiểm tra

```bash
systemctl --user restart openclaw-gateway
openclaw channels status
# Phải hiện Telegram: connected
```

### 8.5. Test

- Mở Telegram
- Tìm bot theo username
- Gửi: `Lên kế hoạch IELTS 7.5`
- Phải nhận được phản hồi

---

## 9. Cài Đặt SQLite

EduClaw dùng SQLite để theo dõi tiến độ.

### Ubuntu/Debian

```bash
sudo apt install -y sqlite3
```

### macOS

```bash
# sqlite3 đã cài sẵn trên macOS
sqlite3 --version
```

### Kiểm tra

```bash
sqlite3 --version
# Kết quả: 3.x.x ...

# Kiểm tra module Python sqlite3
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

---

## 10. Cài Đặt EduClaw Skill

### Từ OpenClaw registry (khi có)

```bash
openclaw skill install educlaw-ielts-planner
```

### Cài đặt thủ công

```bash
git clone https://github.com/moclaw/educlaw-ielts-planner.git
cp -r educlaw-ielts-planner/* ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/
```

### Khởi tạo SQLite database

```bash
mkdir -p ~/.openclaw/workspace/tracker
sqlite3 ~/.openclaw/workspace/tracker/educlaw.db \
  < ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/schema.sql
```

### Kiểm tra skill đã load

```bash
openclaw skill list
# Phải hiện: educlaw-ielts-planner  1.0.0  ✓ loaded
```

---

## 11. Khởi Động OpenClaw Gateway

### Cách A: Dịch vụ systemd (khuyên dùng cho always-on)

```bash
openclaw gateway install-service
systemctl --user enable openclaw-gateway
systemctl --user start openclaw-gateway
```

Kiểm tra:
```bash
systemctl --user status openclaw-gateway
# Phải hiện: active (running)
```

### Cách B: Chạy foreground

```bash
openclaw gateway
```

### Cách C: Chạy nền

```bash
nohup openclaw gateway &
```

---

## 12. Danh Sách Kiểm Tra

| # | Kiểm tra | Kết quả mong đợi |
|---|----------|-------------------|
| 1 | `openclaw --version` | `OpenClaw 2026.x.x` |
| 2 | `openclaw agent --message "Xin chào"` | AI phản hồi |
| 3 | `gcalcli --nocolor list` | Hiện danh sách lịch |
| 4 | Web search test | Trả về URL thực |
| 5 | `openclaw channels status` | Discord/Telegram: connected |
| 6 | `sqlite3 ~/.openclaw/workspace/tracker/educlaw.db ".tables"` | 4 bảng + 5 views |
| 7 | `openclaw skill list` | `educlaw-ielts-planner ✓` |
| 8 | `systemctl --user status openclaw-gateway` | `active (running)` |
| 9 | Test EduClaw | Agent hỏi khung giờ học |

---

## 13. Xử Lý Sự Cố

### Model trả về 429 / RESOURCE_EXHAUSTED

Gemini API key đã hết quota/spending cap.

**Cách sửa:** Vào [Google Cloud Console → Billing](https://console.cloud.google.com/billing) → tăng spending cap cho Generative Language API.

### gcalcli: "Unable to authenticate"

Token OAuth hết hạn hoặc file credentials bị mất.

**Cách sửa:**
```bash
rm -f ~/.gcalcli_oauth
gcalcli list   # Xác thực lại
```

### Discord bot không phản hồi

1. Kiểm tra gateway: `systemctl --user status openclaw-gateway`
2. Kiểm tra channel: `openclaw channels status`
3. Xem log: `openclaw channels logs --channel discord | tail -20`
4. Kiểm tra bot token trong `openclaw.json`
5. Đảm bảo **Message Content Intent** đã bật ở Discord Developer Portal

### "not authorized" cho slash commands trong server

Vào **Server Settings → Integrations → Bot → Manage** → bật commands cho channel.

### SQLite: "unable to open database"

```bash
mkdir -p ~/.openclaw/workspace/tracker
sqlite3 ~/.openclaw/workspace/tracker/educlaw.db \
  < ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/schema.sql
```

### Web search không hoạt động

1. Kiểm tra config: `openclaw config get tools.web.search`
2. Kiểm tra API key trong `openclaw.json` → `tools.web.search.gemini.apiKey`
3. Đảm bảo API đã enable ở Google Cloud Console

### Lỗi pip: "externally-managed-environment"

Ubuntu 24+ chặn cài pip global.

**Cách sửa:**
```bash
pip3 install --break-system-packages gcalcli
# HOẶC
pipx install gcalcli
```

### Cron jobs không gửi tin Discord

1. Xem danh sách: `openclaw cron list`
2. Test job: `openclaw cron run ielts-daily-prep`
3. Xem log: `openclaw channels logs --channel discord | tail -30`
4. Kiểm tra gateway đang chạy và Discord đã kết nối

---

## Cài Đặt Nhanh (Tóm Tắt)

```bash
# 1. Cài OpenClaw
curl -fsSL https://get.openclaw.dev | bash

# 2. Chạy setup wizard (cấu hình API key + model)
openclaw config

# 3. Cài gcalcli + xác thực
pip3 install gcalcli
gcalcli list

# 4. Kết nối Discord bot
openclaw channels add --channel discord --token "BOT_TOKEN" --name "Jaclyn"

# 5. Cài EduClaw skill
git clone https://github.com/moclaw/educlaw-ielts-planner.git
cp -r educlaw-ielts-planner/* ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/

# 6. Khởi tạo database + khởi động
mkdir -p ~/.openclaw/workspace/tracker
sqlite3 ~/.openclaw/workspace/tracker/educlaw.db \
  < ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/schema.sql
systemctl --user restart openclaw-gateway

# 7. Test!
openclaw agent --message "Lên kế hoạch học IELTS 7.5"
```
