---
name: email-assistant
description: Multi-email management assistant supporting Gmail, 163, QQ, Outlook, and Hotmail. Features: (1) Fetch inbox and summarize emails (2) Keyword-based important email detection (3) Auto-extract calendar events from emails. Use when: users need unified email management across multiple accounts, want to avoid missing important emails, or need to extract schedules from email content.
---

# Email Assistant - 多邮箱管理助手

## 功能概览

- **多邮箱支持**: Gmail、163、QQ、Outlook、Hotmail
- **邮件读取**: 获取收件箱、显示摘要、搜索邮件
- **智能分析**: 关键词识别重要邮件
- **日程提取**: 自动从邮件中提取日程信息

## 支持的邮箱

| 邮箱 | 协议 | 服务器配置 |
|------|------|-----------|
| Gmail | OAuth2 + IMAP | imap.gmail.com:993 |
| 163 | IMAP | imap.163.com:993 |
| QQ | IMAP | imap.qq.com:993 |
| Outlook | IMAP | outlook.office365.com:993 |
| Hotmail | IMAP | outlook.office365.com:993 |

## 使用方法

### 1. Gmail 配置

首次使用需要配置 OAuth：

```bash
# 1. 在 Google Cloud Console 创建项目
# 2. 启用 Gmail API
# 3. 创建 OAuth 2.0 客户端凭据
# 4. 下载凭据文件为 credentials.json
# 5. 首次运行会自动打开浏览器授权
```

运行脚本：
```bash
cd scripts
python3 gmail_client.py --credentials ../credentials.json
```

### 2. IMAP 邮箱 (163/QQ/Outlook/Hotmail)

直接运行：
```bash
python3 imap_client.py --server <服务器> --email <邮箱> --password <密码或App密码>
```

### 3. 查看邮件

```bash
# 查看收件箱
python3 mail_parser.py --inbox

# 搜索特定邮件
python3 mail_parser.py --search "关键词"

# 分析重要邮件
python3 mail_parser.py --analyze
```

### 4. 提取日程

```bash
# 从邮件中提取日程并生成 ICS 文件
python3 scheduler.py --extract --output events.ics
```

## 脚本说明

### scripts/gmail_client.py
Gmail OAuth 认证客户端。首次运行会打开浏览器进行授权，之后凭据会缓存。

### scripts/imap_client.py
通用 IMAP 客户端，适用于 163、QQ、Outlook、Hotmail。使用 App Password 认证。

### scripts/mail_parser.py
邮件解析器。解析纯文本/HTML 邮件，提取关键信息，分析重要性。

### scripts/scheduler.py
日程提取器。从邮件中识别 iCal 附件或纯文本日程，生成标准 ICS 日历文件。

## 重要邮件识别

自动识别以下关键词：
- urgent, 紧急, 重要, 即时
- deadline, 截止, 期限
- meeting, 会议, 面试
- invoice, 发票, 付款, 账单
- contract, 合同, 协议

## 日程提取

支持格式：
- iCal 附件 (.ics)
- 纯文本日程（日期+时间+内容）

## 注意事项

1. **Gmail**: 必须使用 OAuth2，密码登录已被禁用
2. **163/QQ**: 需开启 IMAP 并使用 App Password
3. **Outlook/Hotmail**: 使用常规密码或 App Password
4. 建议使用 App Password 而非登录密码，提高安全性
