# generic-mail-client

通用邮箱客户端 Skill。支持任何基于 IMAP/POP3 + SMTP 且使用用户名+密码登录的邮箱：
- 阿里云企业邮箱
- QQ 邮箱 / 163 / Gmail / Outlook / Exchange（开启 IMAP/POP3/SMTP 后）

## 能力

- 多账号支持，通过 accountId 选择邮箱
- 发信（SMTP）：
  - 文本 / HTML / Markdown 正文
  - 多个收件人（To/Cc/Bcc）
  - 附件（base64 传输）
- 收信（IMAP/POP3）：
  - 列出最近邮件（指定文件夹、时间、是否未读、关键字）
  - 查看邮件详情（标题、正文、附件信息）
  - 获取附件内容（可选）
  - 标记已读/未读、移动邮件（IMAP Only）

## 安全说明

- 所有邮箱凭据（host/port/username/password）只保存在宿主配置中，对 LLM 不可见。
- 日志中不记录完整邮件正文和附件内容，只记录接口调用结果、邮件 ID、时间等元数据。
- 强烈建议使用“机器人专用邮箱账号”或应用专用密码，不要用个人登录密码。
- 对发送频率和列表数量有默认上限，以防止误用为垃圾邮件工具。

## 配置

见 `config.example.yaml`，宿主侧复制为实际 `config.yaml` 后注入 skill。
