$ErrorActionPreference = 'Stop'
$vbs = 'D:\Tools\mylike-fav-import\keepalive_hidden.vbs'
$arg = '//B //Nologo "' + $vbs + '"'
$a = New-ScheduledTaskAction -Execute 'C:\Windows\System32\wscript.exe' -Argument $arg
Set-ScheduledTask -TaskName 'MyLikeFavChromeKeepalive' -Action $a | Out-Null
$t = Get-ScheduledTask -TaskName 'MyLikeFavChromeKeepalive'
$i = Get-ScheduledTaskInfo -TaskName 'MyLikeFavChromeKeepalive'
'EXEC=' + $t.Actions[0].Execute
'ARGS=' + $t.Actions[0].Arguments
'STATE=' + $t.State
'TRIGGERS=' + (($t.Triggers | ForEach-Object { $_.CimClass.CimClassName + ':' + $_.Repetition.Interval }) -join ' | ')
'PRINCIPAL=' + $t.Principal.UserId + '/' + $t.Principal.LogonType + '/' + $t.Principal.RunLevel
'LAST=' + $i.LastRunTime + ' result=' + $i.LastTaskResult + ' next=' + $i.NextRunTime
