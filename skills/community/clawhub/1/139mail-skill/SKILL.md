---
name: 139mail
namespace: true
description: |
  139邮箱邮件收发 Skill - 支持 IMAP/SMTP 协议，兼容139/QQ/163/Gmail等主流邮箱

  功能：
  1. 发送邮件（SMTP）
  2. 接收邮件（IMAP）
  3. 查看收件箱列表
  4. 查看未读邮件

  当用户提到 "发邮件"、"收邮件"、"查看邮件"、"邮箱" 或 "email" 时激活此 skill。
---

# 139mail Skill

使用 IMAP/SMTP 协议收发邮件，支持 139 邮箱、QQ 邮箱、163 邮箱、Gmail 等主流邮箱。

## 功能特性

| 功能 | 说明 |
|------|------|
| **发送邮件** | 支持文本邮件、HTML 邮件、附件 |
| **接收邮件** | 查看收件箱、未读邮件、搜索邮件 |
| **邮件列表** | 列出最近邮件，支持分页 |
| **读取邮件** | 查看邮件详情、正文、附件列表 |

## 配置方法

### 1. 编辑配置文件

```bash
~/.openclaw/skills/139mail/config/email.json
```

### 2. 配置示例（139 邮箱）

```json
{
  "email": "13811741897@139.com",
  "password": "你的授权码",
  "smtp": {
    "host": "smtp.139.com",
    "port": 465,
    "secure": true
  },
  "imap": {
    "host": "imap.139.com",
    "port": 993,
    "secure": true
  }
}
```

### 3. 主流邮箱配置参考

**QQ 邮箱：**
- SMTP: smtp.qq.com:465
- IMAP: imap.qq.com:993
- 密码: QQ 邮箱授权码

**163 邮箱：**
- SMTP: smtp.163.com:465
- IMAP: imap.163.com:993
- 密码: 163 邮箱授权码

**Gmail：**
- SMTP: smtp.gmail.com:465
- IMAP: imap.gmail.com:993
- 密码: 应用专用密码

## 使用方法

### 发送邮件

**普通邮件：**
```
发邮件给 example@qq.com，主题是 "测试邮件"，内容是 "这是一封测试邮件"
```

**带附件的邮件：**
```
发邮件给 example@qq.com，主题是 "文档"，内容是 "请查收附件"，附件是 /path/to/document.pdf
```

### 查看收件箱

```
查看最近的邮件
显示未读邮件
```

### 读取邮件

```
读取第 3 封邮件
查看邮件详情 12345
```

## 安全说明

- 配置文件存储在本地，不会被上传到云端
- 建议使用邮箱授权码而非登录密码
- 配置文件权限已设置为仅用户可读
