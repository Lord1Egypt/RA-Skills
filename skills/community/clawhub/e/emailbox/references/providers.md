# 邮箱服务商配置 Email Provider Configuration

## 12+ 服务商 IMAP/SMTP 配置

| 服务商 | IMAP 服务器 | SMTP 服务器 | SMTP 端口 | SSL | 环境变量 |
|--------|-------------|-------------|----------|-----|----------|
| QQ 邮箱 | imap.qq.com | smtp.qq.com | 465 | SSL | EMAIL_QQ / EMAIL_QQ_AUTH |
| 163 邮箱 | imap.163.com | smtp.163.com | 465 | SSL | EMAIL_163 / EMAIL_163_AUTH |
| 126 邮箱 | imap.126.com | smtp.126.com | 465 | SSL | EMAIL_126 / EMAIL_126_AUTH |
| 新浪邮箱 | imap.sina.com | smtp.sina.com | 465 | SSL | EMAIL_SINA / EMAIL_SINA_AUTH |
| Outlook | outlook.office365.com | smtp.office365.com | 587 | STARTTLS | EMAIL_OUTLOOK / EMAIL_OUTLOOK_AUTH |
| Gmail | imap.gmail.com | smtp.gmail.com | 587 | STARTTLS | EMAIL_GMAIL / EMAIL_GMAIL_AUTH |
| Yahoo | imap.mail.yahoo.com | smtp.mail.yahoo.com | 587 | STARTTLS | EMAIL_YAHOO / EMAIL_YAHOO_AUTH |
| iCloud | imap.mail.me.com | smtp.mail.me.com | 587 | STARTTLS | EMAIL_ICLOUD / EMAIL_ICLOUD_AUTH |
| 腾讯企业邮箱 | imap.exmail.qq.com | smtp.exmail.qq.com | 465 | SSL | EMAIL_EXMAIL / EMAIL_EXMAIL_AUTH |
| 阿里企业邮箱 | imap.mxhichina.com | smtp.mxhichina.com | 465 | SSL | EMAIL_ALIMAIL / EMAIL_ALIMAIL_AUTH |
| 华为邮箱 | imap.mail.hicloud.com | smtp.mail.hicloud.com | 465 | SSL | EMAIL_HUAWEI / EMAIL_HUAWEI_AUTH |
| 139 邮箱 | imap.mail.139.com | smtp.mail.139.com | 465 | SSL | EMAIL_139 / EMAIL_139_AUTH |

---

## 环境变量配置

### 单账号模式（推荐新手）

最简配置，只需 2 个环境变量：

```bash
export EMAIL_ADDRESS="your@email.com"
export EMAIL_AUTH="your_authorization_code"
```

### 多账号模式（支持多个邮箱）

每个邮箱单独配置：

```bash
# QQ 邮箱
export EMAIL_QQ="your@qq.com"
export EMAIL_QQ_AUTH="qq_authorization_code"

# 163 邮箱
export EMAIL_163="your@163.com"
export EMAIL_163_AUTH="163_client_password"

# Outlook
export EMAIL_OUTLOOK="your@outlook.com"
export EMAIL_OUTLOOK_AUTH="outlook_app_password"

# Gmail
export EMAIL_GMAIL="your@gmail.com"
export EMAIL_GMAIL_AUTH="gmail_app_password"
```

### 优先级规则

1. 命令行指定 `--from-addr` 和 `--provider` 最高优先
2. 对应服务商的环境变量（如 `EMAIL_QQ` / `EMAIL_QQ_AUTH`）
3. 通用环境变量 `EMAIL_ADDRESS` / `EMAIL_AUTH`

---

## Authorization Code Setup / 授权码获取教程

### QQ Mail / QQ 邮箱

1. Log in to QQ Mail (mail.qq.com) → Settings (设置) → Account (账号)
2. Find "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service"
3. Enable IMAP/SMTP service
4. Click "Generate Authorization Code" (生成授权码)
5. Follow prompts to send SMS verification from your phone
6. Receive 16-character authorization code (no spaces)

```bash
export EMAIL_QQ="your@qq.com"
export EMAIL_QQ_AUTH="abcdefghijklmnop"
```

**Note:** QQ Mail authorization code is 16 letters, NOT your QQ password.

### 163 Mail / 163 邮箱

1. Log in to 163 Mail (mail.163.com) → Settings (设置) → POP3/SMTP/IMAP
2. Enable "IMAP/SMTP Service"
3. Click "Client Authorization Password" (客户端授权密码)
4. Verify via SMS, then set the authorization password

```bash
export EMAIL_163="your@163.com"
export EMAIL_163_AUTH="your_client_password"
```

**Note:** 163 Mail requires authorization password, NOT your login password.

### 126 Mail / 126 邮箱

1. Log in to 126 Mail (mail.126.com) → Settings → POP3/SMTP/IMAP
2. Enable IMAP service
3. Set client authorization password

```bash
export EMAIL_126="your@126.com"
export EMAIL_126_AUTH="your_client_password"
```

### Sina Mail / 新浪邮箱

1. Log in to Sina Mail (mail.sina.com) → Settings → Client Settings
2. Enable IMAP/SMTP service
3. 部分账号需要通过手机验证

```bash
export EMAIL_SINA="your@sina.com"
export EMAIL_SINA_AUTH="your_password"
```

### Outlook / Hotmail

1. Visit https://account.microsoft.com/security
2. Advanced security options → App passwords
3. Generate a new app password

```bash
export EMAIL_OUTLOOK="your@outlook.com"
export EMAIL_OUTLOOK_AUTH="your_app_password"
```

**Note:** If two-step verification is enabled, you MUST use an app password, not your login password. Microsoft is deprecating basic auth — OAuth2 Modern Auth may be required in the future.

### Gmail

1. Enable two-step verification: https://myaccount.google.com/security
2. Create an app password: https://myaccount.google.com/apppasswords
3. Select "Mail" and device, generate the 16-character password
4. **Google removed "Less Secure Apps" access in 2022** — only App Passwords work now

```bash
export EMAIL_GMAIL="your@gmail.com"
export EMAIL_GMAIL_AUTH="abcd efgh ijkl mnop"
```

**Note:** Gmail app passwords may contain spaces; no need to remove them. Requires VPN in mainland China.

### Yahoo Mail

1. Log in to Yahoo → Account Security → Generate app password
2. Yahoo no longer supports "Less Secure Apps" — app password is required

```bash
export EMAIL_YAHOO="your@yahoo.com"
export EMAIL_YAHOO_AUTH="your_app_password"
```

**Note:** Requires VPN in mainland China.

### iCloud Mail

1. Apple ID → Account Settings → App-Specific Passwords
2. Generate a password

```bash
export EMAIL_ICLOUD="your@icloud.com"
export EMAIL_ICLOUD_AUTH="your_app_specific_password"
```

**Note:** Requires VPN in mainland China.

### Tencent Exmail / 腾讯企业邮箱

1. Log in to enterprise mail (exmail.qq.com) → Settings → Client Settings
2. Confirm IMAP service is enabled
3. Use enterprise email password or authorization code

```bash
export EMAIL_EXMAIL="your@company.com"
export EMAIL_EXMAIL_AUTH="your_password"
```

### Ali Mail / 阿里企业邮箱

1. Log in to Ali Mail (mail.mxhichina.com) → Settings → POP/IMAP Settings
2. Enable IMAP service

```bash
export EMAIL_ALIMAIL="your@company.com"
export EMAIL_ALIMAIL_AUTH="your_password"
```

### Huawei Mail / 华为邮箱

1. Log in to Huawei Mail (mail.hicloud.com) → Settings → Account Security
2. Generate app password

```bash
export EMAIL_HUAWEI="your@hicloud.com"
export EMAIL_HUAWEI_AUTH="your_app_password"
```

### 139 Mail / 139 邮箱 (China Mobile)

1. Log in to 139 Mail (mail.139.com) → Settings → Account
2. Enable IMAP service

```bash
export EMAIL_139="your@139.com"
export EMAIL_139_AUTH="your_password"
```

---

## Common Issues / 常见问题

### SMTP Authentication Failed / SMTP 认证失败

- Check that you're using the authorization code, NOT your login password
- Make sure IMAP/SMTP service is enabled in your email settings
- QQ/163: You must explicitly enable IMAP service in email settings

### Connection Timeout / 连接超时

- Gmail/Yahoo/iCloud: Requires VPN in mainland China (国内需翻墙)
- Check if firewall blocks ports 465/587/993
- Try SSL (port 465) or STARTTLS (port 587) alternatively

### 163 Requires Phone Verification / 163 邮箱提示需要手机验证

- New IMAP enablement on 163 may require SMS verification
- Wait 5-10 minutes after verification before trying again

### Sending Rate Limits / 发送频率限制

| Service | Daily Limit / 每日上限 |
|---------|----------------------|
| QQ Mail | 500 emails/day, 1 email/minute |
| 163/126 Mail | 200 emails/day |
| Gmail | 500 emails/day |
| Outlook | 300 emails/day |
| Yahoo | 500 emails/day |

### Attachment Size Limits / 附件大小限制

| Service | Attachment Limit / 附件上限 |
|---------|---------------------------|
| QQ Mail | 50MB |
| 163/126 Mail | 50MB |
| Gmail | 25MB |
| Outlook | 20MB |
| Yahoo | 25MB |
| iCloud | 20MB |