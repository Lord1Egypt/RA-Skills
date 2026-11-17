# Register the Chrome keepalive task: run every 10 minutes + at logon.
$ErrorActionPreference = 'Stop'
$name = 'MyLikeFavChromeKeepalive'
$ps = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
$action = New-ScheduledTaskAction -Execute $ps -Argument '-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File D:\Tools\mylike-fav-import\keepalive.ps1'
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest
$t1 = New-ScheduledTaskTrigger -AtLogOn
$t2 = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $name -Action $action -Trigger @($t1, $t2) -Principal $principal -Settings $settings -Force | Out-Null
$t = Get-ScheduledTask -TaskName $name
$i = Get-ScheduledTaskInfo -TaskName $name
"task=" + $t.TaskName + " state=" + $t.State
"triggers=" + (($t.Triggers | ForEach-Object { $_.CimClass.CimClassName + ":" + $_.StartBoundary }) -join ' | ')
"last=" + $i.LastRunTime + " result=" + $i.LastTaskResult + " next=" + $i.NextRunTime
