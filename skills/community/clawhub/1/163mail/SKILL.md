# 163 Mail Skill

163 邮箱收发邮件技能。使用 IMAP 接收邮件，SMTP 发送邮件。

## 配置

### 1. 创建配置文件

复制 `config.template.json` 到 `config.json`：

```bash
cp /root/.openclaw/workspace/skills/163mail/config.template.json /root/.openclaw/workspace/skills/163mail/config.json
```

### 2. 填写配置

编辑 `config.json`：

```json
{
  "email": "your-email@163.com",
  "imapPassword": "your-imap-authorization-code",
  "smtpPassword": "your-smtp-authorization-code"
}
```

### 3. 获取 163 邮箱授权码

1. 登录 163 邮箱网页版：https://mail.163.com
2. 进入 **设置** → **POP3/SMTP/IMAP**
3. 开启 **IMAP/SMTP 服务**
4. 点击 **生成授权码**
5. 复制授权码到配置文件

> ⚠️ 注意：授权码不是登录密码，是专门用于第三方客户端的密码

## 命令

### 查看收件箱

```
/163mail inbox
/163mail list
```

查看最新 10 封邮件。

### 查看特定文件夹

```
/163mail folder 已发送
/163mail folder 草稿箱
```

可用文件夹：INBOX, 草稿箱，已发送，已删除，垃圾邮件，病毒文件夹，广告邮件

### 读取邮件

```
/163mail read <邮件 ID>
```

### 搜索邮件

```
/163mail search from someone@163.com
/163mail search subject 会议
/163mail search 关键词
```

### 发送邮件

```
/163mail send to@example.com 邮件主题 邮件正文
```

### 回复邮件

```
/163mail reply <邮件 ID> 回复内容
```

### 转发邮件

```
/163mail forward <邮件 ID> to@example.com 转发说明
```

### 删除邮件

```
/163mail delete <邮件 ID>
```

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `163MAIL_EMAIL` | 163 邮箱地址 |
| `163MAIL_IMAP_PASS` | IMAP 授权码 |
| `163MAIL_SMTP_PASS` | SMTP 授权码（可选，默认同 IMAP） |

## 文件结构

```
163mail/
├── SKILL.md              # 技能说明
├── _meta.json            # 技能元数据
├── index.js              # 主入口
├── config.template.json  # 配置模板
├── config.json           # 实际配置（需创建）
├── scripts/              # 辅助脚本
└── references/           # 参考资料
```

## 注意事项

1. **授权码安全**：不要将授权码提交到版本控制
2. **频率限制**：避免频繁调用，163 邮箱有速率限制
3. **安全登录**：首次使用可能需要在网页端确认信任设备
4. **附件支持**：当前版本不支持附件，仅纯文本邮件

## 故障排除

### "Unsafe Login" 错误

163 邮箱安全策略阻止登录：
1. 登录网页版邮箱确认信任设备
2. 检查 IMAP/SMTP 服务是否开启
3. 等待 10-15 分钟后重试

### 授权码错误

1. 确认使用的是授权码而非登录密码
2. 重新生成授权码并更新配置
3. 确认 IMAP/SMTP 服务已开启
