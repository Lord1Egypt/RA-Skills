# 各邮箱配置详细指南

## Gmail

### 1. 获取 OAuth 凭据

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 导航到 **API和服务** → **库**
4. 搜索并启用 **Gmail API**
5. 导航到 **凭据** → **创建凭据** → **OAuth 客户端 ID**
6. 选择 **桌面应用** 作为应用类型
7. 下载 JSON 文件，重命名为 `credentials.json`

### 2. 所需权限

创建 OAuth 凭据时需要添加以下 scope：
```
https://mail.google.com/
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.labels
```

### 3. 首次授权

首次运行脚本时：
1. 会自动打开浏览器
2. 使用 Gmail 账号登录
3. 点击"允许"授权
4. 凭据会自动缓存（token.json）

### 4. 常见问题

- **token.json 失效**: 删除文件重新授权
- **安全警告**: 在 Google Cloud Console 添加测试用户

---

## 163 邮箱

### 1. 开启 IMAP

1. 登录 163 邮箱
2. 设置 → POP3/IMAP/SMTP → 开启 IMAP
3. 获取 **客户端授权密码**（不是登录密码）

### 2. 服务器配置

```
IMAP 服务器: imap.163.com
IMAP 端口: 993
加密: SSL
```

### 3. 使用

```bash
python3 imap_client.py \
  --server imap.163.com \
  --email yourname@163.com \
  --password xxxxxxxx
```

---

## QQ 邮箱

### 1. 开启 IMAP

1. 登录 QQ 邮箱
2. 设置 → POP3/IMAP/SMTP → 开启 IMAP 服务
3. 获取 **授权码**（不是 QQ 密码）

### 2. 服务器配置

```
IMAP 服务器: imap.qq.com
IMAP 端口: 993
加密: SSL
```

### 3. 使用

```bash
python3 imap_client.py \
  --server imap.qq.com \
  --email yourname@qq.com \
  --password xxxxxxxx
```

---

## Outlook / Hotmail

### 1. 开启 IMAP

1. 登录 Outlook 邮箱
2. 设置 → 查看所有 Outlook 设置 → 邮件 → POP 和 IMAP
3. 开启 IMAP

### 2. 服务器配置

```
IMAP 服务器: outlook.office365.com
IMAP 端口: 993
加密: SSL
```

### 3. 使用

```bash
python3 imap_client.py \
  --server outlook.office365.com \
  --email yourname@outlook.com \
  --password xxxxxxxx
```

---

## App Password 说明

| 邮箱 | 获取方式 |
|------|---------|
| 163 | 设置 → POP3/IMAP/SMTP → 客户端授权密码 |
| QQ | 设置 → POP3/IMAP/SMTP → 开启IMAP → 获取授权码 |
| Outlook | Microsoft 账户 → 安全 → 双重验证 → 应用密码 |
| Hotmail | 同 Outlook |

---

## 安全建议

1. **始终使用 App Password**：不要使用邮箱登录密码
2. **保管好凭据文件**：credentials.json 和 token.json 不要提交到代码仓库
3. **定期检查**：授权的应用列表，及时撤销不用的授权
4. **限制权限**：只申请必要的权限范围
