$ErrorActionPreference = 'SilentlyContinue'

$appName = 'FTA Studio'
$dst     = Join-Path $env:LOCALAPPDATA $appName

Write-Host ''
Write-Host '  Removing FTA Studio ...'
Write-Host ''

Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -match 'launch\.mjs' } |
  ForEach-Object { Write-Host ('  stopping pid ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force }
Start-Sleep -Milliseconds 600

if (Test-Path $dst) {
  Remove-Item $dst -Recurse -Force
  Write-Host "  removed folder : $dst"
}

$desktopLnk = Join-Path ([Environment]::GetFolderPath('Desktop')) 'FTA Studio.lnk'
if (Test-Path $desktopLnk) { Remove-Item $desktopLnk -Force; Write-Host '  removed desktop shortcut' }

$menuLnk = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\FTA Studio.lnk'
if (Test-Path $menuLnk) { Remove-Item $menuLnk -Force; Write-Host '  removed start menu entry' }

Write-Host ''
Write-Host '  Done.'
Write-Host ''
