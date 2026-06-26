# OpenClaw 139mail Skill

📧 139邮箱邮件收发 Skill，支持 IMAP/SMTP 协议，兼容主流邮箱

## 功能特性

- ✅ **发送邮件** - 支持文本/HTML 邮件
- ✅ **接收邮件** - 查看收件箱、未读邮件
- ✅ **邮件列表** - 列出最近邮件
- ✅ **读取邮件** - 查看邮件详情
- ✅ **多邮箱支持** - 139/QQ/163/Gmail 等主流邮箱

## 安装

```bash
# 通过 OpenClaw CLI 安装
openclaw skills install 139mail

# 或手动安装
git clone https://github.com/yourusername/openclaw-skill-139mail.git
npm install
```

## 配置

1. 复制配置模板：
```bash
cp config/email.json.example config/email.json
```

2. 编辑 `config/email.json`：

```json
{
  "email": "your-email@example.com",
  "password": "your-authorization-code",
  "smtp": {
    "host": "smtp.example.com",
    "port": 465,
    "secure": true
  },
  "imap": {
    "host": "imap.example.com",
    "port": 993,
    "secure": true
  }
}
```

### 常用邮箱配置

| 邮箱 | SMTP | IMAP | 密码 |
|------|------|------|------|
| **QQ 邮箱** | smtp.qq.com:465 | imap.qq.com:993 | 授权码 |
| **163 邮箱** | smtp.163.com:465 | imap.163.com:993 | 授权码 |
| **139 邮箱** | smtp.139.com:465 | imap.139.com:993 | 授权码 |
| **Gmail** | smtp.gmail.com:465 | imap.gmail.com:993 | 应用密码 |

## 使用方法

### 自然语言交互

```
发邮件给 example@qq.com，主题是测试，内容是你好
查看最近的5封邮件
读取邮件 123
```

### CLI 命令

```bash
# 发送邮件
node scripts/email.js send "收件人@example.com" "主题" "内容"

# 列出邮件
node scripts/email.js list 10

# 读取邮件
node scripts/email.js read 123

# 测试配置
node scripts/email.js test
```

## 依赖

- Node.js >= 18
- imap: ^0.8.19
- nodemailer: ^6.9.0
- mailparser: ^3.6.0

## 安全说明

- ⚠️ 配置文件存储在本地，**不要提交到 Git**
- ⚠️ 使用邮箱授权码而非登录密码
- ⚠️ 配置文件已设置为仅用户可读 (chmod 600)

## License

MIT
