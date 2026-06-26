---
name: feishu-calendar-oauth
description: 飞书日历管理技能。支持查询日程、创建/更新/删除事件、设置重复规则。触发条件：(1) 询问今天/明天/某天的日程 (2) 创建日程/添加会议/新建事件 (3) 更新或删除日程 (4) 设置重复提醒（生日、周会等）(5) 查看日历/日程安排。
---

# 飞书日历技能

管理个人飞书日历，支持完整的日程管理功能。

## 快速检测

```powershell
$tokenFile = "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar-oauth\scripts\.user_token.json"
if (Test-Path $tokenFile) {
    $config = Get-Content $tokenFile | ConvertFrom-Json
    Write-Host "✅ 已配置，日历 ID: $($config.calendar_id)"
} else {
    Write-Host "❌ 未配置，请参考 [OAuth 配置指南](references/oauth-setup.md)"
}
```

## 功能

| 功能 | 状态 | 触发示例 |
|------|------|---------|
| 查询日程 | ✅ | "今天有什么日程" / "查看本周日程" |
| 创建日程 | ✅ | "帮我创建一个会议，明天14点" |
| 更新日程 | ✅ | "把明天的会议改到下午3点" |
| 删除日程 | ✅ | "删除明天的那个会议" |
| 重复事件 | ✅ | "添加生日提醒，每年5月1日" |
| 多级提醒 | ✅ | "创建会议，提前1天和1小时提醒" |

## 自然语言示例

```
用户：帮我查看今天的飞书日程
用户：明天下午2点到4点有个项目会议
用户：每周一上午10点添加一个周会
用户：帮我添加一个生日提醒，每年5月1日
用户：删除明天的会议
```

## API 使用

查询和操作日程的详细方法见 **[API 使用指南](references/api-guide.md)**。

## Token 管理

Token 有效期约 2 小时，过期后自动刷新或手动执行：

```powershell
# 刷新 Token
$config = Get-Content "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar-oauth\scripts\.user_token.json" | ConvertFrom-Json
$body1 = @{ app_id = $config.app_id; app_secret = $config.app_secret } | ConvertTo-Json
$appToken = (Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal" -Method Post -Body $body1 -ContentType "application/json").app_access_token
$body2 = @{ grant_type = "refresh_token"; refresh_token = $config.refresh_token } | ConvertTo-Json
$newToken = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/authen/v1/oidc/refresh_access_token" -Method Post -Body $body2 -ContentType "application/json" -Headers @{ Authorization = "Bearer $appToken" }
$config.access_token = $newToken.data.access_token
$config.refresh_token = $newToken.data.refresh_token
$config | ConvertTo-Json | Out-File "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar-oauth\scripts\.user_token.json"
Write-Host "✅ Token 已刷新"
```

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 授权码无效 | 授权码只能使用一次，重新获取 |
| 重定向 URL 错误 | 检查飞书开放平台"安全设置" |
| 权限不足 | 确认已开通 `calendar:calendar` |

## 参考文档

- **[OAuth 配置指南](references/oauth-setup.md)** — 首次配置必读
- **[API 使用指南](references/api-guide.md)** — 详细 API 调用方法