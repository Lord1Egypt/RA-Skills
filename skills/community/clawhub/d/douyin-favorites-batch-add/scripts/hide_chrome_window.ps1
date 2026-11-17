# Hide every visible top-level window owned by the dedicated mylike Chrome profile.
# Runs inside the interactive user session (session 1); exits 0 on success.
$ErrorActionPreference = 'Continue'
$log = 'D:\Tools\mylike-fav-import\hide_chrome.log'
function W($m) { ("{0}`t{1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m) | Add-Content -Path $log -Encoding UTF8 }

Add-Type @"
using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public class WinApi {
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

$pids = @(Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
  Where-Object { $_.CommandLine -like '*mylike-fav-import\chrome-profile*' } |
  ForEach-Object { [uint32]$_.ProcessId })
if ($pids.Count -eq 0) { W "no mylike chrome process"; "hidden=0 reason=no-process"; exit 0 }

$visible = 0
$hidden = 0
foreach ($h in [WinApi]::All()) {
  $cls = [WinApi]::Cls($h)
  if ($cls -ne 'Chrome_WidgetWin_1') { continue }
  $wpid = [uint32]0
  [WinApi]::GetWindowThreadProcessId($h, [ref]$wpid) | Out-Null
  if ($pids -notcontains $wpid) { continue }
  if (-not [WinApi]::IsWindowVisible($h)) { continue }
  $visible++
  $title = [WinApi]::Txt($h)
  [WinApi]::ShowWindow($h, 0) | Out-Null
  Start-Sleep -Milliseconds 200
  if (-not [WinApi]::IsWindowVisible($h)) { $hidden++ } else { W ("hide failed pid=" + $wpid + " hwnd=" + $h) }
  W ("hidden title='" + $title + "' pid=" + $wpid + " hwnd=" + $h)
}
W ("done visible_before=" + $visible + " hidden=" + $hidden + " profile_pids=" + ($pids -join ','))
"visible_before=$visible hidden=$hidden profile_pids=$($pids -join ',')"
exit 0
