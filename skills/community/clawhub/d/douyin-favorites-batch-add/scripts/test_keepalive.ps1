$ErrorActionPreference = 'Continue'
$hideLog = 'D:\Tools\mylike-fav-import\hide_chrome.log'
$keepLog = 'D:\Tools\mylike-fav-import\keepalive.log'
$before = @{
  hide = (Get-Content $hideLog -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
  keep = (Get-Content $keepLog -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
}
Add-Type -TypeDefinition @"
using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public class WinScan {
  public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lp);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  public static List<string> Visible() {
    var outl = new List<string>();
    EnumWindows((h, l) => {
      if (!IsWindowVisible(h)) return true;
      var c = new StringBuilder(256); GetClassName(h, c, 256);
      var t = new StringBuilder(256); GetWindowText(h, t, 256);
      uint pid = 0; GetWindowThreadProcessId(h, out pid);
      outl.Add(pid + "|" + c.ToString() + "|" + t.ToString());
      return true;
    }, IntPtr.Zero);
    return outl;
  }
}
"@

Start-ScheduledTask -TaskName 'MyLikeFavChromeKeepalive'
$seen = New-Object System.Collections.Generic.HashSet[string]
$consoleWins = New-Object System.Collections.Generic.HashSet[string]
for ($i = 0; $i -lt 40; $i++) {
  Start-Sleep -Milliseconds 250
  foreach ($w in [WinScan]::Visible()) {
    $parts = $w.Split('|')
    $cls = $parts[1]
    if ($cls -match 'Console|CASCADIA|PseudoConsole|WSCRIPT|Shell_TrayWnd') {
      if ($cls -match 'Console|CASCADIA|PseudoConsole') { [void]$consoleWins.Add($w) }
    }
    if ($parts[2] -match 'keepalive|powershell|wscript') { [void]$seen.Add($w) }
  }
  $st = (Get-ScheduledTask -TaskName 'MyLikeFavChromeKeepalive').State
  if ($st -eq 'Ready' -and $i -gt 4) { break }
}
Start-Sleep -Seconds 2
$after = @{
  hide = (Get-Content $hideLog -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
  keep = (Get-Content $keepLog -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
}
$info = Get-ScheduledTaskInfo -TaskName 'MyLikeFavChromeKeepalive'
'RESULT_LAST=' + $info.LastTaskResult + ' LAST_RUN=' + $info.LastRunTime
'CONSOLE_WINDOWS_SEEN=' + $consoleWins.Count
$consoleWins | ForEach-Object { '  CONSOLE: ' + $_ }
'NAMED_WINDOWS_SEEN=' + $seen.Count
$seen | ForEach-Object { '  WIN: ' + $_ }
'HIDELOG_LINES ' + $before.hide + ' -> ' + $after.hide
'KEEPLOG_LINES ' + $before.keep + ' -> ' + $after.keep
if ($after.hide -gt $before.hide) { '--- new hide_chrome.log ---'; Get-Content $hideLog -Tail ($after.hide - $before.hide) }
if ($after.keep -gt $before.keep) { '--- new keepalive.log ---'; Get-Content $keepLog -Tail ($after.keep - $before.keep) }
Get-Process powershell, wscript, conhost -ErrorAction SilentlyContinue |
  Select-Object Id, ProcessName, MainWindowHandle, MainWindowTitle |
  ForEach-Object { 'PROC ' + $_.Id + ' ' + $_.ProcessName + ' hwnd=' + $_.MainWindowHandle + ' title=' + $_.MainWindowTitle }
