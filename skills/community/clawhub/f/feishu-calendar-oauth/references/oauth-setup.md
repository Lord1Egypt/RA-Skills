# OAuth 配置指南

首次使用飞书日历技能，需完成 OAuth 授权配置。

---

## 前置条件

- 拥有飞书账号
- 可访问飞书开放平台

---

## 步骤一：创建飞书应用

### 1.1 访问开放平台

打开 [https://open.feishu.cn/app](https://open.feishu.cn/app)

### 1.2 创建应用

1. 点击 **"创建企业自建应用"**
2. 填写应用名称（如：`日历助手`）
3. 点击 **"创建"**

### 1.3 获取凭证

进入 **"凭证与基础信息"** 页面，记录：
- **App ID**（格式：`cli_xxxxxxxxxxxx`）
- **App Secret**

---

## 步骤二：开通日历权限

### 2.1 进入权限管理

点击左侧 **"权限管理"**

### 2.2 开通权限

搜索 `calendar`，开通以下权限：

| 权限标识 | 权限名称 | 用途 |
|---------|---------|------|
| `calendar:calendar:readonly` | 获取日历、日程及忙闲信息 | 查询日程 |
| `calendar:calendar` | 更新日历及日程信息 | 创建/更新/删除 |

### 2.3 发布应用

点击 **"版本管理与发布" → "创建版本"**，发布应用。

---

## 步骤三：配置重定向 URL

### 3.1 进入安全设置

点击左侧 **"安全设置"**

### 3.2 添加 URL

在 **"重定向 URL"** 部分：
1. 点击 **"添加重定向 URL"**
2. 输入：`http://127.0.0.1:18080/callback`
3. 点击 **"保存"**

---

## 步骤四：获取授权码

### 4.1 构建授权链接

将下方链接中的 `YOUR_APP_ID` 替换为你的 App ID：

```
https://accounts.feishu.cn/open-apis/authen/v1/authorize?app_id=YOUR_APP_ID&redirect_uri=http%3A%2F%2F127.0.0.1%3A18080%2Fcallback&scope=calendar%3Acalendar&state=calendar_auth
```

### 4.2 授权

1. 打开链接
2. 点击 **"同意授权"**
3. 页面跳转到本地地址

### 4.3 获取 Code

从跳转 URL 中复制 `code=` 后面的值：

```
http://127.0.0.1:18080/callback?code=xxxxxx&state=calendar_auth
                                      ↑↑↑↑↑↑
                                      授权码
```

---

## 步骤五：完成配置

在 PowerShell 中运行以下脚本（替换三个值）：

```powershell
# ========= 请替换以下三个值 =========
$appId = "YOUR_APP_ID"           # 你的 App ID
$appSecret = "YOUR_APP_SECRET"   # 你的 App Secret
$code = "YOUR_CODE"              # 刚才获取的授权码
# ====================================

Write-Host "开始配置..." -ForegroundColor Cyan

# 获取 app_access_token
$body1 = @{ app_id = $appId; app_secret = $appSecret } | ConvertTo-Json
$resp1 = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal" -Method Post -Body $body1 -ContentType "application/json"
$appToken = $resp1.app_access_token
Write-Host "✅ 步骤 1/4: 获取 app_access_token 成功"

# 换取 user_access_token
$body2 = @{ grant_type = "authorization_code"; code = $code } | ConvertTo-Json
$resp2 = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/authen/v1/oidc/access_token" -Method Post -Body $body2 -ContentType "application/json" -Headers @{ Authorization = "Bearer $appToken" }
if ($resp2.code -ne 0) {
    Write-Host "❌ 失败: $($resp2.msg)" -ForegroundColor Red
    Write-Host "提示: 授权码只能使用一次，请重新获取"
    exit 1
}
Write-Host "✅ 步骤 2/4: 获取 user_access_token 成功"

# 获取日历 ID
$resp3 = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary" -Method Post -Headers @{ Authorization = "Bearer $($resp2.data.access_token)" }
$calendarId = $resp3.data.calendars[0].calendar.calendar_id
Write-Host "✅ 步骤 3/4: 获取日历 ID 成功"

# 保存配置
$config = @{
    access_token = $resp2.data.access_token
    refresh_token = $resp2.data.refresh_token
    calendar_id = $calendarId
    app_id = $appId
    app_secret = $appSecret
}
$tokenFile = "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar-oauth\scripts\.user_token.json"
New-Item -ItemType Directory -Force -Path (Split-Path $tokenFile) | Out-Null
$config | ConvertTo-Json | Out-File $tokenFile -Encoding UTF8

Write-Host "✅ 步骤 4/4: 保存配置成功"
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🎉 配置完成！" -ForegroundColor Green
Write-Host "日历 ID: $calendarId" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
```

---

## 步骤六：验证配置

```powershell
$config = Get-Content "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar-oauth\scripts\.user_token.json" | ConvertFrom-Json
Write-Host "日历 ID: $($config.calendar_id)"
```

输出日历 ID 即表示配置成功。

---

## 常见问题

### 授权码过期

授权码只能使用一次，失败后重新执行步骤四获取新授权码。

### Token 有效期

- `access_token`：约 2 小时
- `refresh_token`：约 30 天

过期后参考 SKILL.md 中的 Token 刷新方法。