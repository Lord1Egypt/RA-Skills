# Email Sender / 郵件發送工具 - 使用說明

**Email sending and template management tool for OpenClaw agents.**
**郵件發送和模板管理工具。**

Supports SMTP sending, email templates, and attachments (Traditional Chinese version).
支持 SMTP 發送、郵件模板、附件管理（繁體中文版）。

---

## Table of Contents / 目錄

- [Quick Start / 快速開始](#quick-start--快速開始)
- [SMTP Configuration / SMTP 配置](#smtp-configuration--smtp-配置)
- [Sending Emails / 發送郵件](#sending-emails--發送郵件)
- [Template System / 模板系統](#template-system--模板系統)
- [Command Reference / 命令參考](#command-reference--命令參考)
- [Troubleshooting / 故障排除](#troubleshooting--故障排除)

---

## Quick Start / 快速開始

### Installation / 安裝

**Via ClawHub (Recommended) / 通過 ClawHub 安裝（推薦）：**

```bash
clawhub install email-sender-tw
```

OpenClaw automatically loads the skill in the next session.
OpenClaw 會在下一個會話自動載入此技能。

### First-Time Setup / 首次設置

```bash
# Find scripts directory / 查找 scripts 目錄
cd ~/.openclaw/workspace/skills/email-sender-tw/scripts

# Or use workspace config / 或使用工作區配置
cd $(openclaw config get workdir 2>/dev/null)/skills/email-sender-tw/scripts

# Configure SMTP / 配置 SMTP
python3 config.py setup
```

Follow prompts to enter:
按照提示輸入：
- Configuration name / 配置名稱（例如：gmail）
- SMTP server / SMTP 服務器（例如：smtp.gmail.com）
- Port / 端口（587 for TLS）
- Email account / 郵件帳號
- Password / 密碼（stored in macOS Keychain / 存儲在 macOS Keychain）

### Test Email / 測試郵件

```bash
python3 template_manager.py send reminder recipient@example.com name="Your Name" message="Test" date="2026-03-08" sender="Sender"
```

---

## SMTP Configuration / SMTP 配置

### Gmail Setup / Gmail 設置

Gmail requires an **App Password**:
Gmail 需要「應用專屬密碼」：

1. Visit / 前往：https://myaccount.google.com/apppasswords
2. Create app password / 創建應用專屬密碼
3. Use it for SMTP authentication / 使用它進行 SMTP 認證

### Test Configuration / 測試配置

```bash
python3 config.py test <config-name>
```

### List All Configs / 列出所有配置

```bash
python3 config.py list
```

---

## Sending Emails / 發送郵件

### Simple Email / 簡單郵件

```python
from send_email import send_email

send_email(
    to="recipient@example.com",
    subject="Subject / 主題",
    body="Email body / 郵件內容"
)
```

### HTML Email / HTML 郵件

```python
send_email(
    to="recipient@example.com",
    subject="HTML Email",
    body="<h1>Hello / 你好</h1><p>This is HTML.</p>",
    html=True
)
```

### With Attachments / 帶附件

```python
send_email(
    to="recipient@example.com",
    subject="Report / 報告",
    body="Please see attachment / 請查看附件",
    attachments=["/path/to/report.pdf"]
)
```

### Batch Send / 批量發送

```python
from send_email import send_batch

recipients = ["a@example.com", "b@example.com"]
send_batch(
    recipients,
    subject="Weekly Report / 週報",
    body="Content / 內容"
)
```

---

## Template System / 模板系統

### Using Templates / 使用模板

```bash
# Preview template / 預覽模板
python3 template_manager.py preview reminder

# Send with template / 使用模板發送
python3 template_manager.py send reminder recipient@example.com name="Name" message="Message" date="2026-03-08" sender="Sender"
```

### Python API / Python 接口

```python
from template_manager import send_templated_email

send_templated_email(
    template_name="reminder",
    to="recipient@example.com",
    variables={
        "name": "Your Name",
        "date": "2026-03-08",
        "message": "Test message"
    }
)
```

### Create Custom Template / 創建自定義模板

```bash
python3 template_manager.py create
```

Template format example / 模板格式範例：

```html
<!-- SUBJECT: Appointment / 預約通知 -->

<p>Hi {{name}},</p>

<p>Your appointment is confirmed / 您的預約已確認： </p>
<ul>
  <li>Date: {{date}}</li>
  <li>Location: {{location}}</li>
</ul>
```

---

## Command Reference / 命令參考

### config.py / 配置管理

```bash
python3 config.py setup          # Configure SMTP / 配置 SMTP
python3 config.py test [name]    # Test config / 測試配置
python3 config.py list           # List all configs / 列出所有配置
python3 config.py remove <name>  # Delete config / 刪除配置
```

### template_manager.py / 模板管理

```bash
python3 template_manager.py list                # List templates / 列出模板
python3 template_manager.py create              # Create template / 創建模板
python3 template_manager.py preview <name>      # Preview template / 預覽模板
python3 template_manager.py delete <name>       # Delete template / 刪除模板
python3 template_manager.py send <name> <to>    # Send with template / 使用模板發送
```

---

## Troubleshooting / 故障排除

### Gmail Auth Failed / Gmail 認證失敗
**Error:** "Username and Password not accepted"
**Solution / 解決方案：** Enable app password / 啟用「應用專屬密碼」

### SMTP Connection Failed / SMTP 連線失敗
**Error:** "Connection refused" or "Timeout"
**Solution / 解決方案：** Check firewall and port / 檢查防火牆和端口

### Attachment Failed / 附件失敗
**Error:** "File not found" or "Too large"
**Solution / 解決方案：** Verify path and size / 確認路徑和大小（< 25MB）

### Keychain Error / Keychain 錯誤
**Error:** "Unable to get password from Keychain"
**Solution / 解決方案：** Remove and reconfigure / 刪除並重新配置

---

## Best Practices / 最佳实践

### Security / 安全性
- Use app passwords for Gmail / Gmail 使用應用專屬密碼
- Never store passwords in plain text / 不要明文存儲密碼
- Keychain handles credentials safely / Keychain 安全管理憑證

### Path Handling / 路徑處理
The skill uses dynamic paths, compatible with all users:
Skill 使用動態路徑，兼容所有用戶：

```python
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "smtp_config.json")
```

---

**Version / 版本：** 1.2.0
**Updated / 更新日期：** 2026-03-08
**Language / 語言：** 繁體中文 (Traditional Chinese)
