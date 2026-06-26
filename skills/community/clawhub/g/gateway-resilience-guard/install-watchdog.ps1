param(
  [switch]$Yes,
  [switch]$NoStart,
  [string]$ChannelUrl = "https://ilinkai.weixin.qq.com",
  [string]$HealthUrl = "http://127.0.0.1:18789/healthz",
  [string]$RestartCommand = "",
  [string]$InstallDir = ""
)

$ErrorActionPreference = "Stop"
$TaskName = "OpenClaw Gateway Resilience Guard"
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $InstallDir) {
  $InstallDir = Join-Path $env:LOCALAPPDATA "openclaw-gateway-watchdog"
}
$ConfigDir = Join-Path $env:APPDATA "openclaw-gateway-watchdog"
$StateDir = Join-Path $env:LOCALAPPDATA "openclaw-gateway-watchdog"
$ConfigFile = Join-Path $ConfigDir "watchdog.json"

New-Item -ItemType Directory -Force -Path $InstallDir, $ConfigDir, $StateDir | Out-Null
Copy-Item -LiteralPath (Join-Path $SourceDir "gateway-watchdog.ps1") -Destination $InstallDir -Force
Copy-Item -LiteralPath (Join-Path $SourceDir "uninstall-watchdog.ps1") -Destination $InstallDir -Force
if (Test-Path -LiteralPath (Join-Path $SourceDir "dashboard")) {
  Copy-Item -LiteralPath (Join-Path $SourceDir "dashboard") -Destination $InstallDir -Recurse -Force
}
foreach ($name in @("README.md", "README.zh-CN.md", "SKILL.md", "LICENSE")) {
  $path = Join-Path $SourceDir $name
  if (Test-Path -LiteralPath $path) { Copy-Item -LiteralPath $path -Destination $InstallDir -Force }
}

if (-not (Test-Path -LiteralPath $ConfigFile)) {
  $config = [ordered]@{
    GatewayHealthUrl = $HealthUrl
    GatewayHost = "127.0.0.1"
    GatewayPort = 18789
    ChannelUrl = $ChannelUrl
    NetworkUrls = @("https://www.baidu.com", "https://www.qq.com", "https://api.weixin.qq.com")
    RestartCommand = $RestartCommand
    OpenClawNativeProbes = "auto"
    OpenClawHealthTimeoutMs = 12000
    OpenClawGatewayStrict = $false
    OpenClawChannelsProbe = $true
    OpenClawDiagEnabled = $true
    OpenClawDiagInterval = 300
    OpenClawLogScanEnabled = $true
    OpenClawLogLimit = 200
    OpenClawLogSignalLimit = 40
    OpenClawLogTimeoutMs = 15000
    OpenClawLogWarnPatterns = "fetch failed|fetch timeout|LLM idle timeout|model silent|chat/completions|providerRuntimeFailureKind|ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|socket hang up|TLS|CERT_|proxy|429|rate limit|quota|unauthorized|invalid api key|embedded abort settle timed out|embedded run failover decision|memory-core: narrative generation ended with status=timeout|dreaming.*timeout|health-monitor|event loop|degraded|restartPending|session expired|errcode=-14|Monitor.*stopped|monitor.*ended|config hot reload|config change detected|cron.*error|task.*failed"
    OpenClawDiagAction = "log"
    OpenClawDiagFailuresBeforeAction = 2
    OpenClawDiagCommand = ""
    DashboardEnabled = $true
    DashboardHost = "127.0.0.1"
    DashboardPort = 18790
    DashboardActionsEnabled = $true
    DashboardToken = (([guid]::NewGuid().ToString("N")) + ([guid]::NewGuid().ToString("N")).Substring(0, 16))
    DashboardDir = (Join-Path $InstallDir "dashboard")
    DashboardPython = ""
    ModelProbeEnabled = $false
    ModelEdgeProbeEnabled = $true
    ModelProbeInterval = 1800
    ModelProbeTimeout = 120
    ModelProbeFailuresBeforeAction = 2
    ModelProbeAction = "log"
    ModelProbeCommand = ""
    ModelProbeModel = ""
    ModelProbeThinking = "off"
    ModelProbeSessionId = "watchdog-model-probe"
    ModelProbeMessage = "Reply with exactly OK."
    BaseInterval = 60
    NightInterval = 300
    MaxInterval = 1800
    ChannelFailuresBeforeRestart = 2
    SuccessCountToReset = 5
    MaxRestartsPerHour = 6
    PostRestartSleep = 30
  }
  $config | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $ConfigFile -Encoding utf8
} else {
  Write-Host "Keeping existing config: $ConfigFile"
}

$ScriptPath = Join-Path $InstallDir "gateway-watchdog.ps1"
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" -ConfigPath `"$ConfigFile`""
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$Principal = New-ScheduledTaskPrincipal -UserId $CurrentUser -LogonType Interactive -RunLevel LeastPrivilege

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "External OpenClaw Gateway and channel resilience guard." | Out-Null

if (-not $NoStart) {
  Start-ScheduledTask -TaskName $TaskName
}

Write-Host "Installed Windows Task Scheduler task: $TaskName"
Write-Host "Config: $ConfigFile"
Write-Host "Log:    $(Join-Path $StateDir 'watchdog.log')"
Write-Host "Dashboard: http://127.0.0.1:18790"
Write-Host "Remove: powershell -ExecutionPolicy Bypass -File `"$InstallDir\uninstall-watchdog.ps1`""
