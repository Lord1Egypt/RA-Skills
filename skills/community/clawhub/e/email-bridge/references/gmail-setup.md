# Gmail 配置指南

> ⚠️ **注意**：Gmail API 配置流程较复杂，需要 Google Cloud 项目和 OAuth 授权。
> 如果你只需要基本的收发邮件功能，建议使用 QQ 邮箱或网易邮箱（授权码配置更简单）。

## 前置条件

- 一个 Google 账号（Gmail 邮箱）
- 能访问 Google Cloud Console（可能需要科学上网）

---

## Step 1：创建 Google Cloud 项目

1. 打开 [Google Cloud Console](https://console.cloud.google.com/)
2. 登录你的 Google 账号
3. 页面顶部点击项目选择器，点击 **"NEW PROJECT"**
4. 项目名称随便填（如 `email-bridge`），点击 **"CREATE"**
5. 创建完成后选中该项目

---

## Step 2：启用 Gmail API

1. 打开 [Gmail API 页面](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
2. 确保顶部显示的是刚创建的项目
3. 点击 **"ENABLE"**

---

## Step 3：配置 OAuth 同意屏幕

1. 打开 [OAuth 同意屏幕配置](https://console.cloud.google.com/apis/credentials/consent)
2. 用户类型选择 **"External"**，点击 **"CREATE"**

### 填写配置

| 字段 | 填写内容 |
|------|----------|
| App name | `Email Bridge` 或任意名称 |
| User support email | 选择你的邮箱 |
| Developer contact | 填你的邮箱 |
| 其他字段 | 可留空 |

点击 **"SAVE AND CONTINUE"**。

### Scopes（权限范围）

1. 点击 **"ADD OR REMOVE SCOPES"**
2. 搜索 `gmail.modify`，勾选 `https://www.googleapis.com/auth/gmail.modify`
3. 点击 **"UPDATE"**，然后 **"SAVE AND CONTINUE"**

> 💡 `gmail.modify` 包含读取和修改权限，以后发邮件也能用。

### Test Users（测试用户）

1. 点击 **"ADD USERS"**
2. 填写你的 Gmail 地址
3. 点击 **"ADD"**，然后 **"SAVE AND CONTINUE"**

最后检查无误，点击 **"BACK TO DASHBOARD"**。

---

## Step 4：创建 OAuth 客户端凭证

1. 打开 [Credentials 页面](https://console.cloud.google.com/apis/credentials)
2. 点击 **"CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Application type 选择 **"Desktop app"**
4. Name 随便填（如 `Email Bridge CLI`）
5. 点击 **"CREATE"**
6. 在弹出窗口点击 **"DOWNLOAD JSON"** 下载凭证文件

---

## Step 5：安装凭证文件

```bash
# 创建目录
mkdir -p ~/.email-bridge/gmail

# 将下载的凭证文件移动过去，重命名为 credentials.json
mv ~/Downloads/client_secret_xxx.json ~/.email-bridge/gmail/credentials.json
```

---

## Step 6：添加账户并授权

```bash
# 添加 Gmail 账户
email-bridge accounts add your@gmail.com --provider gmail --name "Personal Gmail"

# 首次同步，会打开浏览器要求授权
email-bridge sync
```

授权完成后，token 会自动保存在 `~/.email-bridge/gmail/token_*.json`，后续同步无需再次授权。

---

## 配置选项

```bash
# 自定义同步范围：最近 3 天，最多 50 封
email-bridge accounts add user@gmail.com -p gmail \
  --config '{"sync_days": 3, "sync_max_messages": 50}'
```

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `sync_days` | 同步最近 N 天的邮件 | 7 |
| `sync_max_messages` | 每次同步最大邮件数 | 100 |
| `credentials_path` | 自定义凭证文件路径 | `~/.email-bridge/gmail/credentials.json` |
| `token_path` | 自定义 token 存储路径 | 自动生成 |

---

## 发送邮件

Gmail SMTP 发送需要**应用专用密码**（与 OAuth token 不同）：

1. 开启 Google 账户的两步验证
2. 访问 [应用专用密码](https://myaccount.google.com/apppasswords)
3. 生成一个新密码，选择"邮件"和"其他设备"
4. 更新账户配置：
   ```bash
   email-bridge accounts update <account_id> --config '{"password": "YOUR_APP_PASSWORD"}'
   ```