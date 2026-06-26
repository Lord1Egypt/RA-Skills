---
name: feishu-calendar
description: 飞书日历管理技能。用于查询日程、创建事件、查询忙闲状态。当用户询问日程、会议、日历相关问题时使用此技能。触发条件：(1) 用户询问今天的日程/明天的日程/某天的日程 (2) 用户要求创建日程/添加会议/新建事件 (3) 用户询问日历/日程安排 (4) 用户提到飞书日历相关需求。
---

# 飞书日历技能

用于管理个人飞书日历，包括查询日程、创建事件、查询忙闲状态等功能。

## 前置配置

使用此技能前需要完成 OAuth 授权，详见 [OAuth 配置指南](references/oauth-setup.md)。

## 配置文件

Token 文件位置：`~/.openclaw/workspace/skills/feishu-calendar/scripts/.user_token.json`

```json
{
  "access_token": "u-xxx",
  "refresh_token": "ur-xxx",
  "calendar_id": "feishu.cn_xxx@group.calendar.feishu.cn"
}
```

## 使用方法

### 查询日程

```powershell
# 读取配置
$tokenFile = "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar\scripts\.user_token.json"
$config = Get-Content $tokenFile | ConvertFrom-Json

# 查询今天的日程
$startTime = [int][double]::Parse((Get-Date -Date (Get-Date).Date -UFormat %s))
$endTime = $startTime + 86400

$result = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/$($config.calendar_id)/events?start_time=$startTime&end_time=$endTime" -Method Get -Headers @{ Authorization = "Bearer $($config.access_token)" }

$result.data.items | ForEach-Object {
    Write-Host "$($_.summary) - $(Get-Date -UnixTimeSeconds $_.start_time.timestamp -Format 'HH:mm') 到 $(Get-Date -UnixTimeSeconds $_.end_time.timestamp -Format 'HH:mm')"
}
```

### 创建日程

```powershell
# 读取配置
$tokenFile = "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar\scripts\.user_token.json"
$config = Get-Content $tokenFile | ConvertFrom-Json

# 设置时间
$startTime = [int][double]::Parse((Get-Date -Date "2026-03-21 14:00:00" -UFormat %s))
$endTime = [int][double]::Parse((Get-Date -Date "2026-03-21 15:00:00" -UFormat %s))

$body = @{
    summary = "会议标题"
    start_time = @{ timestamp = $startTime.ToString(); timezone = "Asia/Shanghai" }
    end_time = @{ timestamp = $endTime.ToString(); timezone = "Asia/Shanghai" }
    location = @{ name = "会议室A" }
} | ConvertTo-Json -Depth 3

$result = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/$($config.calendar_id)/events" -Method Post -Body $body -ContentType "application/json" -Headers @{ Authorization = "Bearer $($config.access_token)" }

if ($result.code -eq 0) {
    Write-Host "✅ 日程创建成功"
} else {
    Write-Host "❌ 创建失败: $($result.msg)"
}
```

### Token 刷新

Token 有效期约 2 小时，过期后运行：

```powershell
$tokenFile = "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar\scripts\.user_token.json"
$config = Get-Content $tokenFile | ConvertFrom-Json

# 获取 app_access_token
$appBody = @{ app_id = "cli_a93bf9470db85cc2"; app_secret = "9QGw66iouZcjp3JrnaOC3gI1cHgTS8eF" } | ConvertTo-Json
$appToken = (Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal" -Method Post -Body $appBody -ContentType "application/json").app_access_token

# 刷新 user_access_token
$refreshBody = @{ grant_type = "refresh_token"; refresh_token = $config.refresh_token } | ConvertTo-Json
$newToken = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/authen/v1/oidc/refresh_access_token" -Method Post -Body $refreshBody -ContentType "application/json" -Headers @{ Authorization = "Bearer $appToken" }

# 保存
$config.access_token = $newToken.data.access_token
$config.refresh_token = $newToken.data.refresh_token
$config | ConvertTo-Json | Out-File $tokenFile
Write-Host "✅ Token 已刷新"
```

## 自然语言示例

```
用户：帮我查看今天的飞书日程
用户：查看我明天的日历
用户：帮我在飞书日历创建一个会议，明天 14:00 到 15:00，标题是"项目评审"
用户：我下周一有什么安排？
```

## 注意事项

1. **Token 有效期**：access_token 约 2 小时，refresh_token 约 30 天
2. **权限要求**：需要 `calendar:calendar:readonly` 权限
3. **首次使用**：需要完成 OAuth 授权流程