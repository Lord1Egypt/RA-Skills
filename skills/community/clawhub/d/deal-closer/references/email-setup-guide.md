# 邮件服务配置指南

本指南帮助你配置 Gmail 和 Outlook 邮箱集成，以启用邮件扫描和信号提取功能。

---

## Gmail 配置（OAuth2）

### 步骤 1：创建 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择已有项目
3. 启用 **Gmail API**：导航到「API 和服务」>「库」，搜索 Gmail API 并启用

### 步骤 2：配置 OAuth 同意屏幕

1. 导航到「API 和服务」>「OAuth 同意屏幕」
2. 选择「外部」用户类型
3. 填写应用信息（名称、支持邮箱等）
4. 添加范围：`https://www.googleapis.com/auth/gmail.readonly`
5. 添加测试用户（你的邮箱地址）

### 步骤 3：创建 OAuth 凭据

1. 导航到「API 和服务」>「凭据」
2. 点击「创建凭据」>「OAuth 客户端 ID」
3. 应用类型选择「桌面应用」
4. 下载 JSON 凭据文件，保存到安全位置

### 步骤 4：设置环境变量

```bash
export DC_GMAIL_CREDENTIALS="/path/to/gmail_credentials.json"
```

### 步骤 5：验证连接

首次使用时，系统会引导你完成 OAuth 授权流程，在浏览器中确认授权即可。

---

## Outlook 配置

### 步骤 1：注册 Azure AD 应用

1. 访问 [Azure Portal](https://portal.azure.com/)
2. 导航到「Azure Active Directory」>「应用注册」
3. 点击「新注册」
4. 填写应用名称，选择「任何组织目录中的帐户」
5. 重定向 URI 设置为 `http://localhost:8080/callback`

### 步骤 2：配置 API 权限

1. 在应用注册页面，点击「API 权限」
2. 添加权限：Microsoft Graph > 委托的权限
3. 选择 `Mail.Read` 权限
4. 点击「授予管理员同意」

### 步骤 3：创建客户端密钥

1. 点击「证书和密钥」>「新客户端密钥」
2. 设置描述和过期时间
3. 记录生成的密钥值（仅显示一次）

### 步骤 4：设置环境变量

```bash
export DC_OUTLOOK_CLIENT_ID="你的应用（客户端）ID"
export DC_OUTLOOK_SECRET="你的客户端密钥"
```

### 步骤 5：验证连接

首次使用时会引导完成 OAuth2 授权流程。

---

## 安全注意事项

- 凭据文件请妥善保管，不要提交到代码仓库
- 建议将环境变量写入 `.env` 文件并加入 `.gitignore`
- 定期轮换客户端密钥
- 仅授予最小必要权限（只读邮件权限）
- OAuth token 过期后需重新授权

---

## 常见问题

### Q: OAuth 授权失败怎么办？
检查重定向 URI 是否正确配置，确保测试用户已添加（Gmail）或管理员已同意权限（Outlook）。

### Q: 只能读取最近多少邮件？
默认扫描最近 50 封，可通过 `max_results` 参数调整（最大 500）。

### Q: 支持其他邮箱吗？
目前仅支持 Gmail 和 Outlook。其他邮箱请通过 CSV 导入方式手动添加邮件记录。
