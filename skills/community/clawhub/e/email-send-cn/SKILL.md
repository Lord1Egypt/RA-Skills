---
name: email-send
description: 基于 Nodemailer 的邮件发送技能。使用 nodemailer + SMTP 向任意邮箱发送邮件。支持 163、QQ、Gmail 等主流 SMTP 服务。当用户请求发送邮件时触发。
metadata:
  {
    "openclaw": {
      "emoji": "📧",
      "user-invocable": true,
      "requires": {
        "env": ["SMTP_HOST", "SMTP_USER", "SMTP_PASS"],
        "bins": ["node"]
      },
      "primaryEnv": "SMTP_PASS"
    }
  }
---

# Email Send Skill

使用 nodemailer 通过 SMTP 发送邮件。

## 安装依赖

使用前请先安装依赖：

```bash
npm install
```

这将安装包括 nodemailer 在内的所有必要依赖。

## 安全注意事项

- **请勿在命令行中直接使用真实的 SMTP 凭据**，特别是在生产环境中
- **避免将 SMTP 密码提交到版本控制系统**
- **使用环境变量或安全的配置管理系统**来存储敏感信息
- **定期更新 SMTP 授权码**以增强安全性

## 环境配置

SMTP 凭据通过环境变量配置：

| 变量 | 说明 | 示例 |
|------|------|------|
| SMTP_HOST | SMTP 服务器地址 | smtp.example.com |
| SMTP_PORT | 端口 (25/465/587) | 465 |
| SMTP_SECURE | 是否 SSL (true/false) | true |
| SMTP_USER | 用户名/邮箱 | your-email@example.com |
| SMTP_PASS | 授权码/密码 | your-smtp-password |
| SMTP_FROM | 发件人显示名 | Your Name <your-email@example.com> |

## 使用方式

### 直接调用脚本

```bash
SMTP_HOST=smtp.163.com \
SMTP_PORT=465 \
SMTP_SECURE=true \
SMTP_USER=your-email@example.com \
SMTP_PASS=your-smtp-password \
SMTP_FROM="Your Name <your-email@example.com>" \
node {baseDir}/scripts/send.js \
  --to "recipient@example.com" \
  --subject "Email Subject" \
  --body "Email Body"
```

### AI 调用方式

当用户请求发送邮件时，使用 exec 工具执行上述命令。

## 脚本参数

| 参数 | 必填 | 说明 |
|------|------|------|
| --to | 是 | 收件人邮箱 |
| --cc | 否 | 抄送 (逗号分隔多个) |
| --subject | 是 | 邮件主题 |
| --body | 是 | 邮件正文 |
| --html | 否 | body 是否为 HTML (设为 "true") |

## 常用 SMTP 配置

- **163 邮箱**: smtp.163.com, 端口 465 (SSL) 或 587 (TLS)
- **QQ 邮箱**: smtp.qq.com, 端口 465 (SSL) 或 587 (TLS)
- **Gmail**: smtp.gmail.com, 端口 587 (TLS)

授权码需要在邮箱设置中获取。
