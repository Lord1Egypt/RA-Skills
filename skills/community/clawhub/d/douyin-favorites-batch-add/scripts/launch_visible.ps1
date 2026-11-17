$ErrorActionPreference = 'Stop'
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$chromeArgs = '--remote-debugging-port=9333 --remote-debugging-address=127.0.0.1 --user-data-dir=D:\Tools\mylike-fav-import\chrome-profile --no-first-run --no-default-browser-check --window-size=1200,860 https://www.douyin.com/'

# 1) kill any chrome we started in session 0
Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
  Where-Object { $_.CommandLine -like '*mylike-fav-import*' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 3

# 2) register an interactive task so Chrome starts in the logged-on desktop session
$action = New-ScheduledTaskAction -Execute $chrome -Argument $chromeArgs
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit ([TimeSpan]::Zero)
Register-ScheduledTask -TaskName 'MyLikeFavChrome' -Action $action -Principal $principal -Settings $settings -Force | Out-Null
Start-ScheduledTask -TaskName 'MyLikeFavChrome'
Start-Sleep -Seconds 8

# 3) report
$p = Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object { $_.CommandLine -like '*mylike-fav-import*' }
"procs=" + ($p | Measure-Object).Count
foreach ($x in $p) { "pid=" + $x.ProcessId + " session=" + $x.SessionId }
try { $v = Invoke-RestMethod -Uri 'http://127.0.0.1:9333/json/version' -TimeoutSec 5; "cdp=" + $v.Browser } catch { "cdp=down" }
