---
name: full-mail
description: 完整邮件功能 - 支持发送 (SMTP) 和接收 (IMAP) 邮件
metadata: {"openclaw":{"emoji":"📧","requires":{"anyBins":["python3"]}}}
---

# Full Mail - 完整邮件功能

支持发送邮件 (SMTP) 和接收邮件 (IMAP) 的完整邮件技能。

## 配置

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "full-mail": {
        "enabled": true,
        "env": {
          "EMAIL_SMTP_SERVER": "smtp.163.com",
          "EMAIL_SMTP_PORT": "465",
          "EMAIL_IMAP_SERVER": "imap.163.com",
          "EMAIL_IMAP_PORT": "993",
          "EMAIL_USER": "your-email@163.com",
          "EMAIL_PASSWORD": "授权码或应用密码"
        }
      }
    }
  }
}
```

## 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| EMAIL_SMTP_SERVER | SMTP 服务器地址 | smtp.163.com |
| EMAIL_SMTP_PORT | SMTP 端口 (SSL:465, TLS:587) | 465 |
| EMAIL_IMAP_SERVER | IMAP 服务器地址 | imap.163.com |
| EMAIL_IMAP_PORT | IMAP 端口 (SSL:993) | 993 |
| EMAIL_USER | 邮箱账号 | your-email@163.com |
| EMAIL_PASSWORD | 授权码/应用密码 | ABC123DEF456 |

## 常用邮箱服务器配置

| 邮箱 | SMTP 服务器 | SMTP 端口 | IMAP 服务器 | IMAP 端口 |
|------|------------|----------|------------|----------|
| 163 邮箱 | smtp.163.com | 465 | imap.163.com | 993 |
| 126 邮箱 | smtp.126.com | 465 | imap.126.com | 993 |
| QQ 邮箱 | smtp.qq.com | 465 | imap.qq.com | 993 |
| Gmail | smtp.gmail.com | 587 | imap.gmail.com | 993 |
| Outlook | smtp.office365.com | 587 | outlook.office365.com | 993 |
| 新浪邮箱 | smtp.sina.com | 465 | imap.sina.com | 993 |

## 使用方法

### 发送邮件

```bash
# 纯文本邮件
python3 ~/.openclaw/workspace/skills/full-mail/send_email.py "收件人" "主题" "正文"

# 带附件
python3 ~/.openclaw/workspace/skills/full-mail/send_email.py "收件人" "主题" "正文" "/path/to/file.pdf"

# 多个收件人 (逗号分隔)
python3 ~/.openclaw/workspace/skills/full-mail/send_email.py "a@x.com,b@y.com" "主题" "正文"
```

### 接收邮件

```bash
# 查看收件箱最新 10 封邮件
python3 ~/.openclaw/workspace/skills/full-mail/read_email.py list 10

# 查看指定邮件 (按序号)
python3 ~/.openclaw/workspace/skills/full-mail/read_email.py read 1

# 搜索邮件
python3 ~/.openclaw/workspace/skills/full-mail/read_email.py search "关键词"

# 下载附件
python3 ~/.openclaw/workspace/skills/full-mail/read_email.py attachments 1

# 标记已读
python3 ~/.openclaw/workspace/skills/full-mail/read_email.py markread 1

# 删除邮件
python3 ~/.openclaw/workspace/skills/full-mail/read_email.py delete 1
```

## 授权码获取

### 163/QQ 邮箱
1. 登录邮箱网页版
2. 设置 → 账户/POP3/SMTP/IMAP
3. 开启 SMTP/IMAP 服务
4. 生成授权码 (需短信验证)

### Gmail
1. 开启两步验证
2. 访问 https://myaccount.google.com/apppasswords
3. 生成应用密码

## 故障排查

- 认证失败：检查 EMAIL_PASSWORD 是否为授权码 (非登录密码)
- 连接失败：检查服务器地址和端口
- 收件箱为空：检查 IMAP 配置是否正确
