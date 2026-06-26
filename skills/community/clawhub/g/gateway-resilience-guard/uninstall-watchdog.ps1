param(
  [switch]$Purge,
  [string]$InstallDir = ""
)

$ErrorActionPreference = "Continue"
$TaskName = "OpenClaw Gateway Resilience Guard"
if (-not $InstallDir) {
  $InstallDir = Join-Path $env:LOCALAPPDATA "openclaw-gateway-watchdog"
}
$ConfigDir = Join-Path $env:APPDATA "openclaw-gateway-watchdog"
$StateDir = Join-Path $env:LOCALAPPDATA "openclaw-gateway-watchdog"

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
  Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
  Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

$DashboardPid = Join-Path $StateDir "dashboard.pid"
if (Test-Path -LiteralPath $DashboardPid) {
  $pidValue = Get-Content -LiteralPath $DashboardPid -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($pidValue) {
    Stop-Process -Id ([int]$pidValue) -ErrorAction SilentlyContinue
  }
  Remove-Item -LiteralPath $DashboardPid -Force -ErrorAction SilentlyContinue
}

Remove-Item -LiteralPath $InstallDir -Recurse -Force -ErrorAction SilentlyContinue

if ($Purge) {
  Remove-Item -LiteralPath $ConfigDir -Recurse -Force -ErrorAction SilentlyContinue
  Remove-Item -LiteralPath $StateDir -Recurse -Force -ErrorAction SilentlyContinue
  Write-Host "OpenClaw Gateway Resilience Guard removed, including config and logs."
} else {
  Write-Host "OpenClaw Gateway Resilience Guard removed. Config/logs kept:"
  Write-Host "  $ConfigDir"
  Write-Host "  $StateDir"
  Write-Host "Use -Purge to remove them too."
}
