---
name: email163-sender
description: 163邮箱发送工具。使用授权密码(授权码)进行SMTP认证发送邮件。支持文本邮件、HTML邮件、带附件邮件、抄送/密送。当用户需要发送邮件时使用此技能。

license: MIT
---

# Email Sender (163)

通过授权密码发送邮件的技能。

## 环境配置

```bash
# 163邮箱地址
export EMAIL_163_USER="your_email@163.com"

# 授权密码（在163邮箱设置中开启）
export EMAIL_163_AUTH_CODE="your_auth_code"
```

**获取授权密码：**
1. 登录163邮箱 → 设置 → POP3/SMTP设置
2. 开启 POP3/SMTP服务
3. 新增授权密码并保存

## 快速开始

### 发送简单邮件
```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "测试邮件" \
  --body "这是一封测试邮件"
```

### 发送带附件邮件
```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "报告" \
  --body "请查收附件" \
  -a report.pdf
```

### 发送HTML邮件
```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "周报" \
  --html \
  --body "<h1>周报</h1><p>本周工作进展...</p>"
```

### 查看发送历史
```bash
python3 scripts/send_email.py --list
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--to`, `-t` | 收件人邮箱（多个用逗号分隔） |
| `--subject`, `-s` | 邮件主题 |
| `--body`, `-b` | 邮件正文 |
| `--html` | HTML格式邮件 |
| `-a`, `--attachment` | 附件路径（可多次指定） |
| `--cc` | 抄送 |
| `--bcc` | 密送 |
| `--from`, `-f` | 发件人邮箱 |
| `--auth-code` | 授权密码 |
| `--list`, `-l` | 列出已发送邮件 |
| `--status` | 查看邮件状态 |
| `--clear-history` | 清空发送历史 |

## 常见问题

**Q: 认证失败？**
A: 检查授权密码是否正确，确认已在163邮箱中开启POP3/SMTP服务。

**Q: 附件发送失败？**
A: 确认文件路径正确，文件大小建议<20MB。
