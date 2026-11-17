$ErrorActionPreference = 'SilentlyContinue'
Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public class WF {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
}
"@
$log = "D:\Tools\mylike-fav-import\front.log"
"--- run " + (Get-Date -Format o) | Out-File -FilePath $log -Encoding utf8
$ids = @(Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
  Where-Object { $_.CommandLine -like '*mylike-fav-import*' } |
  ForEach-Object { [int]$_.ProcessId })
"target pids: " + ($ids -join ',')
$found = New-Object System.Collections.ArrayList
$cb = [WF+EnumProc]{
  param($h, $l)
  $winPid = 0
  [void][WF]::GetWindowThreadProcessId($h, [ref]$winPid)
  if ($ids -contains [int]$winPid) {
    $sb = New-Object System.Text.StringBuilder 512
    [void][WF]::GetWindowText($h, $sb, 512)
    [void]$found.Add([pscustomobject]@{ hwnd = $h; pid = $winPid; title = $sb.ToString(); visible = [WF]::IsWindowVisible($h) })
  }
  return $true
}
[void][WF]::EnumWindows($cb, [IntPtr]::Zero)
foreach ($w in $found) { ("cand hwnd=" + $w.hwnd + " visible=" + $w.visible + " title=" + $w.title) | Out-File -FilePath $log -Append -Encoding utf8 } 
foreach ($w in $found) { "cand hwnd=" + $w.hwnd + " visible=" + $w.visible + " title=" + $w.title }
foreach ($w in $found) {
  if ($w.title -like '*Google Chrome*') {
    if ([WF]::IsIconic($w.hwnd)) { [void][WF]::ShowWindow($w.hwnd, 9) }
    [void][WF]::ShowWindow($w.hwnd, 5)
    $fg = [WF]::GetForegroundWindow()
    $fgPid = 0
    $fgThread = [WF]::GetWindowThreadProcessId($fg, [ref]$fgPid)
    $cur = [WF]::GetCurrentThreadId()
    [void][WF]::AttachThreadInput($fgThread, $cur, $true)
    $ok = [WF]::SetForegroundWindow($w.hwnd)
    [void][WF]::AttachThreadInput($fgThread, $cur, $false)
    ("activated=" + $ok + " hwnd=" + $w.hwnd + " title=" + $w.title) | Out-File -FilePath $log -Append -Encoding utf8
    break
  }
}
