$ErrorActionPreference = 'Stop'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -ExecutionPolicy Bypass -File D:\Tools\mylike-fav-import\front.ps1'
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest
Register-ScheduledTask -TaskName 'MyLikeFavFront' -Action $action -Principal $principal -Force | Out-Null
Start-ScheduledTask -TaskName 'MyLikeFavFront'
Start-Sleep -Seconds 4
$out = (Get-ScheduledTaskInfo -TaskName 'MyLikeFavFront').LastTaskResult
"task_result=$out"
