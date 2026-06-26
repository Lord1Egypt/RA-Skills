# API 使用指南

飞书日历 API 详细调用方法。

---

## 目录

1. [查询日程](#一查询日程)
2. [创建日程](#二创建日程)
3. [重复事件](#三重复事件)
4. [设置提醒](#四设置提醒)
5. [更新日程](#五更新日程)
6. [删除日程](#六删除日程)
7. [查询忙闲](#七查询忙闲)
8. [错误处理](#八错误处理)

---

## 一、查询日程

### 1.1 查询今日日程

```powershell
$config = Get-Content "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar-oauth\scripts\.user_token.json" | ConvertFrom-Json

$startTime = [int][double]::Parse((Get-Date -Date (Get-Date).Date -UFormat %s))
$endTime = $startTime + 86400

$result = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/$($config.calendar_id)/events?start_time=$startTime&end_time=$endTime" -Method Get -Headers @{ Authorization = "Bearer $($config.access_token)" }

Write-Host "📅 今日日程" -ForegroundColor Cyan
foreach ($item in $result.data.items) {
    $startTs = [long]$item.start_time.timestamp
    $endTs = [long]$item.end_time.timestamp
    $start = [DateTimeOffset]::FromUnixTimeSeconds($startTs).LocalDateTime.ToString("HH:mm")
    $end = [DateTimeOffset]::FromUnixTimeSeconds($endTs).LocalDateTime.ToString("HH:mm")
    Write-Host "$start - $end  $($item.summary)"
}
```

### 1.2 查询指定日期

```powershell
$dateStr = "2026-03-21"
$date = Get-Date -Date $dateStr
$startTime = [int][double]::Parse((Get-Date -Date $date.Date -UFormat %s))
$endTime = $startTime + 86400
# 后续同上
```

### 1.3 查询一周日程

```powershell
$startTime = [int][double]::Parse((Get-Date -Date (Get-Date).Date -UFormat %s))
$endTime = $startTime + (86400 * 7)
# 后续同上
```

---

## 二、创建日程

### 2.1 创建定时事件

```powershell
$config = Get-Content "$env:USERPROFILE\.openclaw\workspace\skills\feishu-calendar-oauth\scripts\.user_token.json" | ConvertFrom-Json

$startTime = [int][double]::Parse((Get-Date -Date "2026-03-21 14:00:00" -UFormat %s))
$endTime = [int][double]::Parse((Get-Date -Date "2026-03-21 15:00:00" -UFormat %s))

$body = @{
    summary = "项目会议"
    description = "讨论 Q2 目标"
    start_time = @{ timestamp = $startTime.ToString(); timezone = "Asia/Shanghai" }
    end_time = @{ timestamp = $endTime.ToString(); timezone = "Asia/Shanghai" }
    location = @{ name = "会议室A" }
} | ConvertTo-Json -Depth 3

$result = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/$($config.calendar_id)/events" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $($config.access_token)" }

if ($result.code -eq 0) {
    Write-Host "✅ 创建成功，事件 ID: $($result.data.event.event_id)"
} else {
    Write-Host "❌ 创建失败: $($result.msg)"
}
```

### 2.2 创建全天事件

```powershell
$body = @{
    summary = "团队建设日"
    start_time = @{ date = "2026-03-25"; timezone = "Asia/Shanghai" }
    end_time = @{ date = "2026-03-25"; timezone = "Asia/Shanghai" }
    is_all_day = $true
} | ConvertTo-Json -Depth 3
# 发送请求同上
```

---

## 三、重复事件

### 3.1 每年重复（生日提醒）

```powershell
$body = @{
    summary = "🎂 生日"
    start_time = @{ date = "2026-05-01"; timezone = "Asia/Shanghai" }
    end_time = @{ date = "2026-05-01"; timezone = "Asia/Shanghai" }
    is_all_day = $true
    recurrence = "FREQ=YEARLY;INTERVAL=1"
    reminders = @(@{ minutes = 1440 })
} | ConvertTo-Json -Depth 3
```

### 3.2 每周重复（周会）

```powershell
$body = @{
    summary = "每周例会"
    start_time = @{ timestamp = $startTime.ToString(); timezone = "Asia/Shanghai" }
    end_time = @{ timestamp = $endTime.ToString(); timezone = "Asia/Shanghai" }
    recurrence = "FREQ=WEEKLY;INTERVAL=1"
} | ConvertTo-Json -Depth 3
```

### 3.3 重复规则

| 规则 | 说明 | 场景 |
|------|------|------|
| `FREQ=DAILY;INTERVAL=1` | 每天 | 每日站会 |
| `FREQ=WEEKLY;INTERVAL=1` | 每周 | 周例会 |
| `FREQ=MONTHLY;INTERVAL=1` | 每月 | 月度总结 |
| `FREQ=YEARLY;INTERVAL=1` | 每年 | 生日、纪念日 |

---

## 四、设置提醒

### 4.1 单级提醒

```powershell
$body = @{
    summary = "重要会议"
    start_time = @{ timestamp = $startTime.ToString(); timezone = "Asia/Shanghai" }
    end_time = @{ timestamp = $endTime.ToString(); timezone = "Asia/Shanghai" }
    reminders = @(@{ minutes = 30 })
} | ConvertTo-Json -Depth 3
```

### 4.2 多级提醒

```powershell
$body = @{
    summary = "重要会议"
    start_time = @{ timestamp = $startTime.ToString(); timezone = "Asia/Shanghai" }
    end_time = @{ timestamp = $endTime.ToString(); timezone = "Asia/Shanghai" }
    reminders = @(
        @{ minutes = 5 },
        @{ minutes = 60 },
        @{ minutes = 1440 }
    )
} | ConvertTo-Json -Depth 3
```

---

## 五、更新日程

```powershell
$eventId = "事件ID"

$body = @{
    summary = "新标题"
    description = "新描述"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/$($config.calendar_id)/events/$eventId" -Method Patch -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $($config.access_token)" }

if ($result.code -eq 0) { Write-Host "✅ 更新成功" }
```

---

## 六、删除日程

```powershell
$eventId = "事件ID"

$result = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/$($config.calendar_id)/events/$eventId" -Method Delete -Headers @{ Authorization = "Bearer $($config.access_token)" }

if ($result.code -eq 0) { Write-Host "✅ 删除成功" }
```

---

## 七、查询忙闲

```powershell
$body = @{
    time_min = "2026-03-21T00:00:00+08:00"
    time_max = "2026-03-21T23:59:59+08:00"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/freebusy/list" -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -Headers @{ Authorization = "Bearer $($config.access_token)" }
```

---

## 八、错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 99991661 | Token 缺失 | 检查 Authorization Header |
| 99991679 | 权限不足 | 确认已开通日历权限 |
| 99991663 | 时间格式错误 | 使用正确的 timestamp 格式 |

### 错误处理示例

```powershell
$result = Invoke-RestMethod -Uri "..." -Method Post ...

if ($result.code -eq 0) {
    Write-Host "✅ 成功"
} else {
    switch ($result.code) {
        99991661 { Write-Host "❌ Token 缺失" }
        99991679 { Write-Host "❌ 权限不足" }
        default { Write-Host "❌ 错误: $($result.msg)" }
    }
}
```