---
name: email-operations
description: |
  邮件操作技能，通过 SMTP/IMAP 协议读取和发送邮件。当用户想要查看邮件、搜索邮件内容、
  获取收件箱列表、拉取特定邮件详情、发送邮件、或需要与邮箱服务交互时，使用此技能。
  无论用户是否明确提到 "IMAP" 或 "SMTP"，只要涉及邮件收发操作，均可触发此技能。
  适用场景：查看收件箱、搜索邮件、按条件过滤、获取邮件正文和附件信息、发送邮件、群发邮件等。
version: 2.0.0
---

# Email Operations Skill

通过 SMTP/IMAP 协议读取和管理邮件的技能，支持邮件收发全流程操作。

## 凭证配置

**重要**：凭证存储在技能目录下的 `.env` 文件中，而非系统环境变量。

使用此技能前，请先配置 `skills/email-operations/.env` 文件：

```env
# 邮箱基础配置
EMAIL_ADDRESS=your@email.com
EMAIL_IMAP_PASSWORD=your_imap_password
EMAIL_SMTP_PASSWORD=your_smtp_password

# IMAP 服务器配置（可选，有默认值）
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_IMAP_PORT=993

# SMTP 服务器配置（可选，有默认值）
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_SSL=false
```

### 常用邮件服务配置

**Gmail:**
```env
EMAIL_ADDRESS=your@gmail.com
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
```
注意：需要开启"应用专用密码"

**QQ/foxmail:**
```env
EMAIL_ADDRESS=your@qq.com
EMAIL_IMAP_HOST=imap.qq.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_HOST=smtp.qq.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_SSL=false
```

**163/188:**
```env
EMAIL_ADDRESS=your@163.com
EMAIL_IMAP_HOST=imap.163.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_HOST=smtp.163.com
EMAIL_SMTP_PORT=465
EMAIL_SMTP_SSL=true
```

**Outlook:**
```env
EMAIL_ADDRESS=your@outlook.com
EMAIL_IMAP_HOST=outlook.office365.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_HOST=smtp.office365.com
EMAIL_SMTP_PORT=587
```

## 核心功能

### 读取邮件

| 功能 | 方法 | 说明 |
|------|------|------|
| 获取收件箱 | `get_inbox()` | 返回邮件列表摘要 |
| 获取详情 | `get_email()` | 返回完整邮件内容 |
| 搜索邮件 | `search_emails()` | 按关键词/发件人/日期搜索 |
| 保存附件 | `save_attachment()` | 下载附件到本地 |
| 文件夹列表 | `get_folders()` | 获取邮箱文件夹 |

### 发送邮件

| 功能 | 方法 | 说明 |
|------|------|------|
| 发送文本邮件 | `send_email()` | 发送纯文本邮件 |
| 发送HTML邮件 | `send_html_email()` | 发送 HTML 格式邮件 |
| 发送带附件 | `send_email_with_attachments()` | 添加附件发送 |

## 使用示例

### 读取邮件

```python
from scripts.email_client import EmailClient

client = EmailClient()

# 获取收件箱邮件列表
emails = client.get_inbox(count=10)
for email in emails:
    print(f"主题: {email['subject']}")
    print(f"发件人: {email['from']}")
    print(f"时间: {email['date']}")
    print("---")

# 按 UID 获取邮件详情
email = client.get_email(uid=123)
print(f"正文: {email['body']['plain']}")
print(f"附件: {email['attachments']}")

# 搜索邮件
results = client.search_emails(
    keyword="发票",
    from_addr="zhangsan@company.com",
    date_from="2024-01-01",
    date_to="2024-12-31"
)
```

### 发送邮件

```python
# 发送文本邮件
client.send_email(
    to="recipient@example.com",
    subject="邮件主题",
    body="这是邮件正文内容"
)

# 发送 HTML 邮件
client.send_html_email(
    to="recipient@example.com",
    subject="HTML 邮件",
    html_body="<h1>标题</h1><p>正文内容</p>"
)

# 发送带附件的邮件
client.send_email_with_attachments(
    to="recipient@example.com",
    subject="带附件的邮件",
    body="请查收附件",
    attachments=[
        "./files/document.pdf",
        "./files/image.png"
    ]
)

# 群发邮件
recipients = ["user1@example.com", "user2@example.com", "user3@example.com"]
for recipient in recipients:
    client.send_email(
        to=recipient,
        subject="群发邮件",
        body="这是一封群发邮件"
    )
```

## EmailClient 方法列表

### 读取操作

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_inbox()` | 获取收件箱邮件列表 | `count=10`, `offset=0`, `folder="INBOX"` |
| `get_email()` | 获取单封邮件详情 | `uid`, `folder="INBOX"` |
| `search_emails()` | 搜索邮件 | `keyword`, `from_addr`, `to_addr`, `date_from`, `date_to`, `folder` |
| `save_attachment()` | 保存附件 | `email_uid`, `attachment_index`, `save_path` |
| `get_folders()` | 获取文件夹列表 | 无 |

### 发送操作

| 方法 | 说明 | 参数 |
|------|------|------|
| `send_email()` | 发送文本邮件 | `to`, `subject`, `body`, `cc=None`, `bcc=None` |
| `send_html_email()` | 发送HTML邮件 | `to`, `subject`, `html_body`, `cc=None`, `bcc=None` |
| `send_email_with_attachments()` | 发送带附件邮件 | `to`, `subject`, `body`, `attachments`, `cc`, `bcc` |

## 数据结构

### 邮件摘要 (get_inbox 返回)

```python
{
    "uid": 12345,
    "subject": "邮件主题",
    "from": "sender@example.com",
    "from_name": "发件人姓名",
    "to": "recipient@example.com",
    "date": "2024-01-15 10:30:00",
    "size": 1024,
    "flags": ["已读", "星标"],
    "is_read": True
}
```

### 邮件详情 (get_email 返回)

```python
{
    "uid": 12345,
    "subject": "邮件主题",
    "from": {"name": "发件人", "email": "sender@example.com"},
    "to": [{"name": "收件人", "email": "recipient@example.com"}],
    "date": "2024-01-15 10:30:00",
    "body": {
        "plain": "纯文本内容",
        "html": "<html>...</html>"
    },
    "attachments": [
        {"index": 0, "name": "file.pdf", "size": 102400, "type": "application/pdf"}
    ],
    "headers": {"Message-ID": "...", "References": "..."}
}
```

## 命令行使用

```bash
# 列出收件箱邮件
python -m scripts.email_client --action list --count 10

# 查看邮件详情
python -m scripts.email_client --action show --uid 12345

# 搜索邮件
python -m scripts.email_client --action search --keyword "发票"

# 查看文件夹
python -m scripts.email_client --action folders

# 发送测试邮件
python -m scripts.email_client --action send \
    --to "recipient@example.com" \
    --subject "测试邮件" \
    --body "这是测试邮件的内容"

# 从 UTF-8 文件读取正文后发送，适合 Windows 下发送中文邮件
python -m scripts.email_client --action send \
    --to "recipient@example.com" \
    --subject "天气简报" \
    --body-file "./mail_body.txt"

# 发送 HTML 文件内容
python -m scripts.email_client --action send \
    --to "recipient@example.com" \
    --subject "HTML 邮件" \
    --html-body-file "./mail_body.html"
```

## 常见问题

### Q: 认证失败怎么办？
A: 请确保：
1. 邮箱地址正确
2. 使用的是"应用专用密码"而非登录密码（Gmail/QQ等）
3. IMAP 和 SMTP 服务已在邮箱设置中开启

### Q: 如何处理中文乱码？
A: 脚本已内置编码检测和转换，会自动处理 GBK、UTF-8 等编码。

### Q: 附件大小有限制吗？
A: 一般邮箱对附件大小有限制（Gmail 通常 25MB），请确保附件在此范围内。

## 输出格式示例

```
========================================
📧 收件箱 - 最新邮件
========================================

[1] 主题: 会议通知
    发件人: zhangsan@company.com
    时间: 2024-01-15 10:30:00
    状态: 已读

[2] 主题: 发票报销
    发件人: finance@company.com
    时间: 2024-01-15 09:15:00
    状态: 未读 ⭐

========================================
共 2 封邮件
========================================
```
