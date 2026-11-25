$ErrorActionPreference = 'Stop'

$src     = $PSScriptRoot
$appName = 'FTA Studio'
$dst     = Join-Path $env:LOCALAPPDATA $appName

Write-Host ''
Write-Host '  ============================================'
Write-Host '    FTA Studio  -  local install'
Write-Host '  ============================================'
Write-Host ''
Write-Host "  Target folder : $dst"

if (Test-Path $dst) {
  Remove-Item $dst -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $dst -Force | Out-Null

foreach ($d in @('runtime','app')) {
  $p = Join-Path $src $d
  if (Test-Path $p) { Copy-Item $p -Destination $dst -Recurse -Force }
}
Copy-Item (Join-Path $src '*.bat') -Destination $dst -Force
Copy-Item (Join-Path $src '*.ps1') -Destination $dst -Force -ErrorAction SilentlyContinue
Copy-Item (Join-Path $src '*.txt') -Destination $dst -Force -ErrorAction SilentlyContinue

$launcher = Join-Path $dst '启动 FTA Studio.bat'
if (-not (Test-Path $launcher)) {
  Write-Host ''
  Write-Host '  [ERROR] Launcher not found after copy.'
  exit 1
}

$ws = New-Object -ComObject WScript.Shell

$desktop = [Environment]::GetFolderPath('Desktop')
$lnk = $ws.CreateShortcut((Join-Path $desktop 'FTA Studio.lnk'))
$lnk.TargetPath        = $launcher
$lnk.WorkingDirectory  = $dst
$lnk.Description       = 'FTA Studio - Fault Tree Analysis'
$lnk.Save()
Write-Host "  Desktop shortcut : $(Join-Path $desktop 'FTA Studio.lnk')"

$startMenu = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'
$lnk2 = $ws.CreateShortcut((Join-Path $startMenu 'FTA Studio.lnk'))
$lnk2.TargetPath       = $launcher
$lnk2.WorkingDirectory = $dst
$lnk2.Description      = 'FTA Studio - Fault Tree Analysis'
$lnk2.Save()
Write-Host "  Start menu entry : $(Join-Path $startMenu 'FTA Studio.lnk')"

Write-Host ''
Write-Host '  Install finished. Use the "FTA Studio" shortcut on your Desktop.'
Write-Host ''
