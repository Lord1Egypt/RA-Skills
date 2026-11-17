$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$chromeExe = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$douyinUrl = 'https://www.douyin.com/'
$taskName = 'MyLikeFavChrome'
$log = 'D:\Tools\mylike-fav-import\keepalive.log'
$hideLog = 'D:\Tools\mylike-fav-import\hide_chrome.log'
function W($m) { ("{0}`t{1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m) | Add-Content -Path $log -Encoding UTF8 }
function WH($m) { ("{0}`t{1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m) | Add-Content -Path $hideLog -Encoding UTF8 }

# Window hiding is inlined here. Previously hide_chrome_window.ps1 was spawned as a child
# powershell, which allocated its own console window and flashed on every run.
Add-Type -TypeDefinition @"
using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public class WinApiKH {
  public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lp);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  public static List<IntPtr> All() {
    var list = new List<IntPtr>();
    EnumWindows((h, l) => { list.Add(h); return true; }, IntPtr.Zero);
    return list;
  }
  public static string Cls(IntPtr h) { var sb = new StringBuilder(256); GetClassName(h, sb, 256); return sb.ToString(); }
  public static string Txt(IntPtr h) { var sb = new StringBuilder(512); GetWindowText(h, sb, 512); return sb.ToString(); }
}
"@

function HideChrome {
  try {
    $pids = @(Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
      Where-Object { $_.CommandLine -like '*mylike-fav-import\chrome-profile*' } |
      ForEach-Object { [uint32]$_.ProcessId })
    if ($pids.Count -eq 0) { WH "no mylike chrome process"; return }
    $visible = 0
    $hidden = 0
    foreach ($h in [WinApiKH]::All()) {
      if ([WinApiKH]::Cls($h) -ne 'Chrome_WidgetWin_1') { continue }
      $wpid = [uint32]0
      [WinApiKH]::GetWindowThreadProcessId($h, [ref]$wpid) | Out-Null
      if ($pids -notcontains $wpid) { continue }
      if (-not [WinApiKH]::IsWindowVisible($h)) { continue }
      $visible++
      $title = [WinApiKH]::Txt($h)
      [WinApiKH]::ShowWindow($h, 0) | Out-Null
      Start-Sleep -Milliseconds 200
      if (-not [WinApiKH]::IsWindowVisible($h)) { $hidden++ } else { WH ("hide failed pid=" + $wpid + " hwnd=" + $h) }
      WH ("hidden title='" + $title + "' pid=" + $wpid + " hwnd=" + $h)
    }
    WH ("done visible_before=" + $visible + " hidden=" + $hidden + " profile_pids=" + ($pids -join ','))
  } catch { WH ("hide failed: " + $_.Exception.Message) }
}

function CdpUp {
  try { $v = Invoke-RestMethod -Uri 'http://127.0.0.1:9333/json/version' -TimeoutSec 5; return $v.Browser } catch { return $null }
}

$browser = CdpUp
if ($browser) {
  $hasPage = $false
  try {
    $tabs = Invoke-RestMethod -Uri 'http://127.0.0.1:9333/json/list' -TimeoutSec 5
    foreach ($t in $tabs) { if ($t.type -eq 'page' -and $t.url -like '*douyin.com*') { $hasPage = $true } }
  } catch { }
  if ($hasPage) { HideChrome; exit 0 }
  W "cdp up ($browser) but no douyin page; opening one"
  try { Invoke-RestMethod -Uri ("http://127.0.0.1:9333/json/new?" + [uri]::EscapeDataString($douyinUrl)) -Method Put -TimeoutSec 8 | Out-Null } catch { W ("new-tab failed: " + $_.Exception.Message) }
  Start-Sleep -Seconds 6
  HideChrome
  exit 0
}

W "cdp down; starting scheduled task $taskName"
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if (-not $existing) {
  $chromeArgs = '--remote-debugging-port=9333 --remote-debugging-address=127.0.0.1 --user-data-dir=D:\Tools\mylike-fav-import\chrome-profile --no-first-run --no-default-browser-check --window-size=1200,860 ' + $douyinUrl
  $action = New-ScheduledTaskAction -Execute $chromeExe -Argument $chromeArgs
  $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest
  $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit ([TimeSpan]::Zero)
  Register-ScheduledTask -TaskName $taskName -Action $action -Principal $principal -Settings $settings -Force | Out-Null
  W "registered task $taskName"
}
Start-ScheduledTask -TaskName $taskName
for ($i = 0; $i -lt 12; $i++) {
  Start-Sleep -Seconds 5
  $b = CdpUp
  if ($b) { W ("cdp back up: " + $b); HideChrome; exit 0 }
}
W "cdp still down after 60s"
exit 1
