# Windows 任务计划程序模板

可直接复制修改。用 PowerShell 创建（比 schtasks 参数更清晰、支持"仅登录时运行"）。

## 创建每日任务

```powershell
$py = 'C:\path\to\python.exe'
$script = 'D:\path\to\business_flow.py'
$taskName = 'MyDailyGuiTask'
$action = New-ScheduledTaskAction -Execute $py -Argument ('"' + $script + '"')
$trigger = New-ScheduledTaskTrigger -Daily -At '09:00'
$principal = New-ScheduledTaskPrincipal -UserId 'MACHINE\Username' -LogonType Interactive -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 10)
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) { Unregister-ScheduledTask -TaskName $taskName -Confirm:$false }
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description '每日 GUI 自动化' | Out-Null
Get-ScheduledTask -TaskName $taskName | Select-Object TaskName, State
```

要点：
- `-LogonType Interactive` = "仅在用户登录时运行"，**这是能截屏的关键**。
- `-RunLevel Highest` = 最高权限，减少权限拒绝。
- `-StartWhenAvailable` = 错过触发时间（如休眠）后登录时补跑。
- `UserId` 用 `机器名\用户名`，本机可用 `$env:COMPUTERNAME + '\' + $env:USERNAME` 拼。
- `python.exe` 要用**装了依赖的那个解释器**的绝对路径，用 `python -c "import sys;print(sys.executable)"` 查。

## 手动触发并验证（上线前必做）

```powershell
$before = (Get-Content 'D:\path\to\checkin-log.md' | Measure-Object -Line).Lines
Start-ScheduledTask -TaskName 'MyDailyGuiTask'
Start-Sleep -Seconds 30
$i = Get-ScheduledTaskInfo -TaskName 'MyDailyGuiTask'
"LastRunTime=$($i.LastRunTime) LastResult=$($i.LastTaskResult)"
$after = (Get-Content 'D:\path\to\checkin-log.md' | Measure-Object -Line).Lines
"log lines: $before -> $after"
```

判定：
- `LastResult=0` 且日志行数增加、生成了新截图 → 会话可用，闭环成立。
- `LastResult=267009` (0x41301) = 仍在运行，多等一会再查。
- 日志没增加 → 脚本在计划任务会话里仍失败，回看 `session-isolation.md`。

## 常见 LastTaskResult

| 值 | 含义 |
|---|---|
| 0 | 成功 |
| 267009 (0x41301) | 任务正在运行 |
| 267011 (0x41301 变体) | 已启动、等待运行 |
| 1 | 常规错误，查脚本日志 |

## 查询 / 停止 / 删除

```powershell
Get-ScheduledTask -TaskName 'MyDailyGuiTask' | Select TaskName,State
(Get-ScheduledTask -TaskName 'MyDailyGuiTask').Triggers
Stop-ScheduledTask -TaskName 'MyDailyGuiTask'
Unregister-ScheduledTask -TaskName 'MyDailyGuiTask' -Confirm:$false
```

## 与 WorkBuddy automation 配合

操作任务（计划任务 9:00）+ 汇报任务（WorkBuddy automation 9:20）。汇报任务只读日志和截图：
- UTF-8 读 `checkin-log.md` 最后几行，找当天日期记录。
- 列 `logs/` 下当天截图，必要时用读图确认状态。
- 读不到就如实标注"未能读取"，禁止虚构成功。
- 全程不碰 GUI，避免和正在操作或被中断的任务抢窗口。
