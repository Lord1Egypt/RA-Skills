$ErrorActionPreference = 'SilentlyContinue'
$procs = Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object { $_.CommandLine -like '*mylike-fav-import*' }
"our chrome procs: " + ($procs | Measure-Object).Count
foreach ($p in $procs) { "pid=" + $p.ProcessId + " session=" + $p.SessionId }
$exp = Get-Process explorer | Select-Object -First 1
"explorer session=" + $exp.SessionId

Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public class W {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
}
"@
$ids = @($procs | ForEach-Object { $_.ProcessId })
$found = @()
$cb = [W+EnumProc]{
  param($h, $l)
  $pid2 = 0
  [void][W]::GetWindowThreadProcessId($h, [ref]$pid2)
  if ($ids -contains [int]$pid2) {
    $sb = New-Object System.Text.StringBuilder 512
    [void][W]::GetWindowText($h, $sb, 512)
    $script:found += [pscustomobject]@{ hwnd = $h; pid = $pid2; title = $sb.ToString(); visible = [W]::IsWindowVisible($h) }
  }
  return $true
}
[void][W]::EnumWindows($cb, [IntPtr]::Zero)
"windows:"
$found | Format-Table -AutoSize | Out-String
foreach ($w in $found) {
  if ($w.title -ne '') {
    [void][W]::ShowWindow($w.hwnd, 9)
    [void][W]::ShowWindow($w.hwnd, 3)
    [void][W]::SetForegroundWindow($w.hwnd)
    "activated hwnd=" + $w.hwnd + " title=" + $w.title
  }
}
