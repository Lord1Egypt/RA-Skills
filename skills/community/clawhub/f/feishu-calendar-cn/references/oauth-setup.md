# 飞书日历 OAuth 配置指南

## 一、核心概念

飞书日历 API 有两种身份：

| 身份 | Token | 访问的日历 |
|------|-------|-----------|
| 应用身份 | tenant_access_token | 机器人自己的日历 |
| 用户身份 | user_access_token | 用户个人的日历 |

**个人日程管理需要使用用户身份（user_access_token）。**

## 二、飞书开放平台配置

### 2.1 开通日历权限

1. 进入 [飞书开放平台](https://open.feishu.cn/app)
2. 点击 **"权限管理"**
3. 开通以下权限：
   - `calendar:calendar:readonly` - 获取日历、日程及忙闲信息
   - `calendar:calendar` - 更新日历及日程信息

### 2.2 配置重定向 URL

1. 点击 **"安全设置"**
2. 添加重定向 URL：`http://127.0.0.1:18080/callback`
3. 保存

## 三、OAuth 授权流程

### 3.1 获取授权码

打开授权链接：

```
https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=cli_a93bf9470db85cc2&redirect_uri=http%3A%2F%2F127.0.0.1%3A18080%2Fcallback&scope=calendar%3Acalendar%3Areadonly&state=calendar_auth
```

同意授权后，从跳转 URL 中获取 `code` 参数。

### 3.2 换取 Token

```powershell
# 配置
$appId = "cli_a93bf9470db85cc2"
$appSecret = "9QGw66iouZcjp3JrnaOC3gI1cHgTS8eF"
$code = "你的授权码"

# 获取 app_access_token
$body1 = @{ app_id = $appId; app_secret = $appSecret } | ConvertTo-Json
$appToken = (Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal" -Method Post -Body $body1 -ContentType "application/json").app_access_token

# 换取 user_access_token
$body2 = @{ grant_type = "authorization_code"; code = $code } | ConvertTo-Json
$userToken = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/authen/v1/oidc/access_token" -Method Post -Body $body2 -ContentType "application/json" -Headers @{ Authorization = "Bearer $appToken" }

# 获取日历 ID
$calendar = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary" -Method Post -Headers @{ Authorization = "Bearer $($userToken.data.access_token)" }

# 保存配置
$config = @{
    access_token = $userToken.data.access_token
    refresh_token = $userToken.data.refresh_token
    calendar_id = $calendar.data.calendars[0].calendar.calendar_id
}
$tokenFile = "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar\scripts\.user_token.json"
$config | ConvertTo-Json | Out-File $tokenFile
Write-Host "✅ 配置完成"
```

## 四、常见错误

| 错误码 | 问题 | 解决方案 |
|--------|------|---------|
| 20029 | 重定向 URL 有误 | 检查安全设置中的配置 |
| 20043 | scope 有误 | 使用 `calendar:calendar:readonly` |
| 99991679 | 权限不足 | 使用 user_access_token |

## 五、API 参考

| 功能 | 端点 |
|------|------|
| 获取主日历 | POST `/calendar/v4/calendars/primary` |
| 查询事件 | GET `/calendar/v4/calendars/:id/events` |
| 创建事件 | POST `/calendar/v4/calendars/:id/events` |