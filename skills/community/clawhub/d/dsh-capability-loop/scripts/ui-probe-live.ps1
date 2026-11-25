# Live UI probe: reload the desktop window, open the "capability-loop" sidebar panel, screenshot.
# Saves screenshots under docs/design/ (workspace, .tmp is ACL-restricted on this machine).
param(
  [string]$Before = 'E:\dsh-capability-loop\docs\design\panel-live-before.png',
  [string]$After = 'E:\dsh-capability-loop\docs\design\panel-live-after.png',
  [int]$ClickX = 60,
  [int]$ClickY = 257,
  [switch]$NoReload
)

$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$code = @'
using System;
using System.Runtime.InteropServices;
public class UiProbeLive {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdcBlt, uint nFlags);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
'@
if (-not ('UiProbeLive' -as [type])) { Add-Type -TypeDefinition $code }

$proc = Get-Process -Name 'DeepSeek Harness' -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $proc) { Write-Host '[FAIL] desktop window not found'; exit 2 }
$hwnd = $proc.MainWindowHandle
[UiProbeLive]::SetForegroundWindow($hwnd) | Out-Null
Start-Sleep -Milliseconds 600

if (-not $NoReload) {
  [System.Windows.Forms.SendKeys]::SendWait('^r')
  Write-Host '[INFO] sent Ctrl+R, waiting for renderer reload'
  Start-Sleep -Seconds 9
}

$rect = New-Object UiProbeLive+RECT
[UiProbeLive]::GetWindowRect($hwnd, [ref]$rect) | Out-Null
Write-Host ('[INFO] window L=' + $rect.Left + ' T=' + $rect.Top + ' W=' + ($rect.Right - $rect.Left) + ' H=' + ($rect.Bottom - $rect.Top))

function Save-Shot([string]$path) {
  $w = $rect.Right - $rect.Left
  $h = $rect.Bottom - $rect.Top
  if ($w -le 0 -or $h -le 0) { return $false }
  $bmp = New-Object System.Drawing.Bitmap($w, $h)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $dc = $g.GetHdc()
  [UiProbeLive]::PrintWindow($hwnd, $dc, 2) | Out-Null
  $g.ReleaseHdc($dc)
  $g.Dispose()
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
  return $true
}

if (Save-Shot $Before) { Write-Host ('[OK] before: ' + $Before) } else { Write-Host '[WARN] before shot failed' }

$clickAbsX = $rect.Left + $ClickX
$clickAbsY = $rect.Top + $ClickY
[UiProbeLive]::SetCursorPos($clickAbsX, $clickAbsY) | Out-Null
Start-Sleep -Milliseconds 500
[UiProbeLive]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
Start-Sleep -Milliseconds 120
[UiProbeLive]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
Write-Host ('[INFO] clicked (' + $clickAbsX + ',' + $clickAbsY + ')')
Start-Sleep -Seconds 5

if (Save-Shot $After) { Write-Host ('[OK] after: ' + $After) } else { Write-Host '[WARN] after shot failed' }
exit 0
