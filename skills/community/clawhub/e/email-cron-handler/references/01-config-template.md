# Email Cron Handler 配置模板

## 替换以下占位符为你的实际值

| 占位符 | 你的值 |
|-------|-------|
| {EMAIL} | your_email@qq.com |
| {PASSWORD} | your_auth_code |
| {IMAP_HOST} | imap.qq.com |
| {IMAP_PORT} | 993 |
| {SMTP_HOST} | smtp.qq.com |
| {SMTP_PORT} | 465 |
| {WHITELIST_SENDER} | your_phone@qq.com |

## 完整指令模板（直接复制使用）

```
请用Python imaplib和smtplib检查邮箱 {EMAIL} 的最近50封邮件（包括已读和未读）。
IMAP登录: user={EMAIL}, password={PASSWORD}, host={IMAP_HOST}, port={IMAP_PORT}
SMTP登录: user={EMAIL}, password={PASSWORD}, host={SMTP_HOST}, port={SMTP_PORT}

⚠️ 核心任务：读取 {WHITELIST_SENDER} 发来的邮件，邮件内容是你需要执行的指令！

处理步骤：
1. 读取~/.openclaw/workspace/memory/processed_emails.json，获取已处理邮件UID列表
2. 获取最近50封邮件
3. 筛选出发件人 {WHITELIST_SENDER} 的未处理邮件
4. 对每封未处理邮件：
   a. 解析邮件内容，这就是你需要执行的指令
   b. 尝试执行该指令（查询天气/搜索信息/执行操作等）
   c. 将执行结果（或失败信息）作为邮件正文，用SMTP回复给发件人
      - 执行成功：正文写实际执行结果
      - 执行失败：详细说明失败原因
   d. 将该邮件UID添加到已处理列表
5. 保存更新后的已处理列表到~/.openclaw/workspace/memory/processed_emails.json

【重要】无论成功还是失败，都必须回复邮件！

执行完成后汇报处理结果。禁止使用浏览器工具。
```

## Cron 任务创建命令

### 白天模式（每分钟）
```bash
# 7:00-23:00，每分钟执行
cron add --name "邮件指令-白天" \
  --schedule "expr" "* 7-23 * * *" \
  --tz "Asia/Shanghai" \
  --session-target "isolated" \
  --payload '{"kind":"agentTurn","message":"请用Python imaplib和smtplib检查邮箱 {EMAIL} 的最近50封邮件（包括已读和未读）。IMAP登录: user={EMAIL}, password={PASSWORD}, host={IMAP_HOST}, port={IMAP_PORT}。SMTP登录: user={EMAIL}, password={PASSWORD}, host={SMTP_HOST}, port={SMTP_PORT}。处理步骤：1. 读取~/.openclaw/workspace/memory/processed_emails.json；2. 获取最近50封邮件；3. 筛选出发件人 {WHITELIST_SENDER} 的未处理邮件；4. 执行指令并回复结果；5. 更新已处理列表。","model":"minimax-portal/MiniMax-M2.5","timeoutSeconds":300}'
```

### 夜间模式（每30分钟）
```bash
# 0:00-7:00，每30分钟执行
cron add --name "邮件指令-夜间" \
  --schedule "expr" "*/30 0-7 * * *" \
  --tz "Asia/Shanghai" \
  --session-target "isolated" \
  --payload '{"kind":"agentTurn","message":"...同上方指令...","model":"minimax-portal/MiniMax-M2.5","timeoutSeconds":300}'
```
