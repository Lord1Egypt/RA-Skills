# Screenshot the running DSH window at a given size without injecting keyboard/mouse input.
# PrintWindow works while the window is occluded or another app is foreground.
param(
  [int]$Width = 0,
  [int]$Height = 0,
  [string]$Out = 'E:\dsh-capability-loop\docs\design\panel-shot.png'
)

$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName System.Drawing

$code = @'
using System;
using System.Runtime.InteropServices;
public class UiShot {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdcBlt, uint nFlags);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
'@
if (-not ('UiShot' -as [type])) { Add-Type -TypeDefinition $code }

$proc = Get-Process -Name 'DeepSeek Harness' -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $proc) { Write-Host '[FAIL] desktop window not found'; exit 2 }
$hwnd = $proc.MainWindowHandle
if ([UiShot]::IsIconic($hwnd)) { [UiShot]::ShowWindow($hwnd, 9) | Out-Null; Start-Sleep -Seconds 2 }

$rect = New-Object UiShot+RECT
[UiShot]::GetWindowRect($hwnd, [ref]$rect) | Out-Null
$origW = $rect.Right - $rect.Left
$origH = $rect.Bottom - $rect.Top
Write-Host ('[INFO] original ' + $origW + 'x' + $origH + ' at ' + $rect.Left + ',' + $rect.Top)

$targetW = if ($Width -gt 0) { $Width } else { $origW }
$targetH = if ($Height -gt 0) { $Height } else { $origH }
if ($targetW -ne $origW -or $targetH -ne $origH) {
  [UiShot]::MoveWindow($hwnd, $rect.Left, $rect.Top, $targetW, $targetH, $true) | Out-Null
  Start-Sleep -Seconds 2
  [UiShot]::GetWindowRect($hwnd, [ref]$rect) | Out-Null
  Write-Host ('[INFO] resized to ' + ($rect.Right - $rect.Left) + 'x' + ($rect.Bottom - $rect.Top))
}

$w = $rect.Right - $rect.Left
$h = $rect.Bottom - $rect.Top
$bmp = New-Object System.Drawing.Bitmap($w, $h)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$dc = $g.GetHdc()
[UiShot]::PrintWindow($hwnd, $dc, 2) | Out-Null
$g.ReleaseHdc($dc)
$g.Dispose()
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
Write-Host ('[OK] ' + $Out + ' (' + $w + 'x' + $h + ')')

if ($targetW -ne $origW -or $targetH -ne $origH) {
  [UiShot]::MoveWindow($hwnd, $rect.Left, $rect.Top, $origW, $origH, $true) | Out-Null
  Write-Host '[INFO] restored original size'
}
exit 0
