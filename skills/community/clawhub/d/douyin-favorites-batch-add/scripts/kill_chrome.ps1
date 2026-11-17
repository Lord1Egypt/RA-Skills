$p = Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object { $_.CommandLine -like '*mylike-fav-import*' }
"procs=" + ($p | Measure-Object).Count
foreach ($x in $p) { Stop-Process -Id $x.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 4
try { Invoke-RestMethod 'http://127.0.0.1:9333/json/version' -TimeoutSec 3 | Out-Null; 'cdp=still-up' } catch { 'cdp=down' }
