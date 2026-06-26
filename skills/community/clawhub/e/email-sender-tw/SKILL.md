---
name: email-sender-tw
description: Email sending and template management tool for OpenClaw agents. Supports SMTP sending, email templates, and attachments.
tags: productivity, mail, email, smtp, zh-tw
---

# Email Sender / 郵件發送工具

Email sending and template management tool for OpenClaw agents. Supports SMTP sending, email templates, and attachments (Traditional Chinese version).

郵件發送和模板管理工具。支持 SMTP 發送、郵件模板、附件管理（繁體中文版）。

---

## Quick Reference / 快速參考

| Situation / 情況 | Action / 操作 |
|-----------------|--------------|
| Send simple email / 發送簡單郵件 | `python3 ../scripts/send_email.py` (from scripts dir) |
| Use template / 使用模板郵件 | `python3 script manager.py send <template> <recipient>` |
| Configure SMTP / 配置 SMTP | `python3 config.py setup` |
| List templates / 列出模板 | `python3 template_manager.py list` |
| Test configuration / 測試配置 | `python3 config.py test` |
| View help / 查看幫助 | `python3 <script>.py --help` |

---

## Quick Start / 快速開始

### Installation / 安裝

**Via ClawHub (Recommended) / 通過 ClawHub 安裝（推薦）：**

```bash
clawhub install email-sender-tw
```

OpenClaw will automatically load the skill in the next session.
OpenClaw 會在下一個會話自動載入此技能。

### First-Time Configuration / 首次配置

After installation, configure SMTP:
安裝後，配置 SMTP：

```bash
# Find and navigate to scripts directory / 查找並進入 scripts 目錄
cd ~/.openclaw/workspace/skills/email-sender-tw/scripts

# Or use workspace path / 或使用工作區路徑
cd $(openclaw config get workdir 2>/dev/null)/skills/email-sender-tw/scripts

# Configure SMTP / 配置 SMTP
python3 config.py setup
```

### Send Test Email / 發送測試郵件

```bash
python3 template_manager.py send reminder recipient@example.com name="Your Name" message="Test message" date="2026-03-08" sender="Sender"
```

---

## Features / 功能

**Send Emails / 發送郵件：**
- Plain text and HTML emails / 純文字和 HTML 郵件
- Attachments support / 支持附件
- CC, BCC support / 支持抄送和密送
- Batch sending / 批量發送

**Template Management / 模板管理：**
- Save common email templates / 保存常用郵件模板
- Variable substitution (e.g., `{{name}}`, `{{date}}`) / 變量替換
- Pre-built templates: reminder, report, welcome / 預設模板：提醒、報告、歡迎信

**Configuration Management / 配置管理：**
- SMTP server configuration / SMTP 服務器配置
- Secure storage (macOS Keychain) / 安全存儲（macOS Keychain）
- Multiple SMTP profiles / 支持多個 SMTP 配置

---

## SMTP Configuration / SMTP 配置

### Common SMTP Providers / 常用 SMTP 服務商

| Provider / 服務商 | SMTP Server | Port | Encryption / 加密 | Notes / 備註 |
|-----------------|-----------|------|------------------|-------------|
| Gmail | smtp.gmail.com | 587 | TLS | Requires app password / 需要應用專屬密碼 |
| Outlook | smtp.office365.com | 587 | TLS | |
| iCloud | smtp.mail.me.com | 587 | TLS | |

### Gmail Setup / Gmail 設置

Gmail requires an **App Password**:
Gmail 需要「應用專屬密碼」：

1. Go to: https://myaccount.google.com/apppasswords
2. Create an app password / 創建應用專屬密碼
3. Use it for SMTP login / 使用它進行 SMTP 登入

### Test Configuration / 測試配置

```bash
python3 config.py test <config-name>
```

### List All Configurations / 列出所有配置

```bash
python3 config.py list
```

---

## Usage Examples / 使用範例

### Send Simple Email / 發送簡單郵件

```python
from send_email import send_email

send_email(
    to="recipient@example.com",
    subject="Test Email / 測試郵件",
    body="This is a test email. / 這是測試郵件。"
)
```

### Use Template / 使用模板

```python
from template_manager import send_templated_email

send_templated_email(
    template_name="reminder",
    to="recipient@example.com",
    variables={
        "name": "Your Name / 你的名字",
        "date": "2026-03-07",
        "message": "Test message / 測試訊息"
    }
)
```

---

## Scripts / 腳本說明

### scripts/send_email.py
Main email sending script / 主要郵件發送腳本：
- `send_email()` - Send single email / 發送單封郵件
- `send_batch()` - Batch sending / 批量發送

### scripts/template_manager.py
Template management script / 模板管理腳本：
- `send_templated_email()` - Send with template / 使用模板發送
- `list_templates()` - List all templates / 列出所有模板
- `create_template()` - Create new template / 創建新模板

### scripts/config.py
Configuration management script / 配置管理腳本：
- `setup` - Configure SMTP / 配置 SMTP
- `test` - Test configuration / 測試配置
- `list` - List all configs / 列出所有配置
- `remove` - Delete config / 刪除配置

---

## Path Handling / 路徑處理

This skill uses dynamic paths, suitable for any user:
這個 skill 使用動態路徑，適用於任何用戶：

```python
import os

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "smtp_config.json")
```

This ensures the skill works correctly regardless of where it's installed or which user's machine it's on.
這確保無論 skill 安裝在哪裡，或在哪個用戶的電腦上，都能正常工作。

---

## Security / 安全性

✅ **Passwords not exposed in config files / 密碼不暴露在配置文件中**
✅ **Secure storage via macOS Keychain / 使用 macOS Keychain 安全存儲**
✅ **No sensitive info in logs / 不在日誌中記錄敏感信息**
⚠️ **Never share files with Keychain keys / 不要共享包含 Keychain 金鑰的文件**
⚠️ **Rotate email passwords regularly / 定期更換郵件帳號密碼**

---

## Troubleshooting / 故障排除

### Gmail Login Failed / Gmail 登入失敗
Solution / 解決方案：Enable app password / 啟用「應用專屬密碼」
https://myaccount.google.com/apppasswords

### SMTP Connection Failed / SMTP 連線失敗
Check firewall and SMTP port settings / 檢查防火牆和 SMTP 端口

### Attachment Failed / 附件發送失敗
Verify file path and size limit (usually 25MB) / 確認檔案路徑和大小限制（通常 25MB）

### Can't Find Skill Directory / 找不到 Skill 目錄
```bash
# Find skill location / 查找 skill 位置
find ~/.openclaw /opt/homebrew/lib/node_modules/openclaw -name "email-sender-tw" -type d

# Or use workspace / 或使用工作區
echo $(openclaw config get workdir)/skills/email-sender-tw/scripts
```

---

**Version / 版本：** 1.2.0
**Language / 語言：** 繁體中文 (Traditional Chinese)
**Platform / 平台：** macOS (Keychain required)
**Compatible with / 兼容：** OpenClaw 2026.3.2+
