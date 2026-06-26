---
name: email-manager
description: 查询和发送邮件，支持 POP3 协议收件、SMTP 协议发件
version: 0.1.0
author: hopeWing
---

# Email Manager

一个用于查询和发送邮件的 OpenClaw 技能，支持 POP3 协议接收邮件和 SMTP 协议发送邮件。

## 配置说明

在技能目录下创建 `config.yaml` 配置文件：

```yaml
email:
  host_pop3: pop.example.com      # POP3 服务器地址
  host_smtp: smtp.example.com      # SMTP 服务器地址
  port_pop3: 995                   # POP3 端口 (SSL 通常为 995)
  port_smtp: 465                   # SMTP 端口 (SSL 通常为 465 或 587)
  username: your_email@example.com # 邮箱账号
  password: your_app_token         # 授权码或密码
  use_ssl: true                    # 是否使用 SSL
```

## 使用方法

### 查询收件箱
- 获取未读邮件列表
- 读取指定邮件内容
- 查询邮件数量

### 发送邮件
- 发送文本邮件
- 指定收件人、主题、正文
- 支持抄送 (CC) 和密送 (BCC)

## 安全提示

- 建议使用邮箱服务商提供的「授权码」而非登录密码
- 配置文件包含敏感信息，请妥善保管
- 生产环境建议使用加密方式存储密码
