param(
  [string]$ConfigPath = ""
)

$ErrorActionPreference = "Continue"
$Version = "1.4.4"

$ConfigDir = Join-Path $env:APPDATA "openclaw-gateway-watchdog"
$StateDir = Join-Path $env:LOCALAPPDATA "openclaw-gateway-watchdog"
if (-not $ConfigPath) {
  $ConfigPath = Join-Path $ConfigDir "watchdog.json"
}

$DefaultConfig = [ordered]@{
  GatewayHealthUrl = "http://127.0.0.1:18789/healthz"
  GatewayHost = "127.0.0.1"
  GatewayPort = 18789
  ChannelUrl = "https://ilinkai.weixin.qq.com"
  NetworkUrls = @("https://www.baidu.com", "https://www.qq.com", "https://api.weixin.qq.com")
  RestartCommand = ""
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
  DashboardActionsEnabled = $false
  DashboardToken = ""
  DashboardDir = Join-Path $PSScriptRoot "dashboard"
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
  ConnectTimeout = 5
  MaxTime = 10
  ChannelFailuresBeforeRestart = 2
  SuccessCountToReset = 5
  MaxRestartsPerHour = 6
  PostRestartSleep = 30
  MaxLogBytes = 1048576
}

New-Item -ItemType Directory -Force -Path $ConfigDir, $StateDir | Out-Null
if (Test-Path -LiteralPath $ConfigPath) {
  $UserConfig = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
  foreach ($prop in $UserConfig.PSObject.Properties) {
    $DefaultConfig[$prop.Name] = $prop.Value
  }
}
$Config = [pscustomobject]$DefaultConfig
$LogFile = Join-Path $StateDir "watchdog.log"

$createdNew = $false
$mutex = [System.Threading.Mutex]::new($false, "Global\OpenClawGatewayResilienceGuard", [ref]$createdNew)
if (-not $createdNew) {
  Write-Error "Another watchdog instance is already running."
  exit 0
}

function Write-Log {
  param([string]$Message)
  $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
  $line | Tee-Object -FilePath $LogFile -Append
}

function Rotate-LogIfNeeded {
  if (Test-Path -LiteralPath $LogFile) {
    $size = (Get-Item -LiteralPath $LogFile).Length
    if ($size -gt [int64]$Config.MaxLogBytes) {
      Move-Item -LiteralPath $LogFile -Destination "$LogFile.1" -Force
      Write-Log "LOG: rotated because it exceeded $($Config.MaxLogBytes) bytes"
    }
  }
}

function Test-NativeEnabled {
  return -not (@("0", "false", "off", "no") -contains ([string]$Config.OpenClawNativeProbes).ToLowerInvariant())
}

function Save-ProbeOutput {
  param([string]$Name, [object[]]$Output)
  $path = Join-Path $StateDir $Name
  ($Output -join [Environment]::NewLine) | Out-File -LiteralPath $path -Encoding utf8
  return $path
}

function Invoke-OpenClawProbe {
  param([string[]]$Args, [string]$OutputName)
  if (-not (Test-NativeEnabled)) { return @{ Supported = $false; ExitCode = 127; Text = "" } }
  if (-not (Get-Command openclaw -ErrorAction SilentlyContinue)) {
    return @{ Supported = $false; ExitCode = 127; Text = "" }
  }
  $output = & openclaw @Args 2>&1
  $exitCode = $LASTEXITCODE
  $path = Save-ProbeOutput -Name $OutputName -Output $output
  $text = $output -join "`n"
  $unsupported = $text -match "unknown command|unknown option|unknown argument|unrecognized option|not recognized|invalid command"
  return @{ Supported = (-not $unsupported); ExitCode = $exitCode; Text = $text; Path = $path }
}

function Test-Http {
  param([string]$Url)
  if (-not $Url) { return $false }
  try {
    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec ([int]$Config.MaxTime)
    return ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500)
  } catch {
    $status = $_.Exception.Response.StatusCode.value__
    if ($status) {
      return ($status -ge 200 -and $status -lt 500)
    }
    return $false
  }
}

function Test-Tcp {
  try {
    $client = [System.Net.Sockets.TcpClient]::new()
    $task = $client.ConnectAsync([string]$Config.GatewayHost, [int]$Config.GatewayPort)
    $ok = $task.Wait([int]$Config.ConnectTimeout * 1000) -and $client.Connected
    $client.Dispose()
    return $ok
  } catch {
    return $false
  }
}

function Test-OpenClawGateway {
  $probe = Invoke-OpenClawProbe -Args @("gateway", "status", "--json", "--require-rpc", "--timeout", "$($Config.OpenClawHealthTimeoutMs)") -OutputName "last-openclaw-gateway-status.json"
  if (-not $probe.Supported) { return 2 }
  if ($probe.ExitCode -eq 0) {
    if ($probe.Text -match '"ok"\s*:\s*false') {
      Write-Log "OPENCLAW GATEWAY FAIL: gateway status reported ok=false"
      return 1
    }
    if ($probe.Text -match '"degraded"\s*:\s*true') {
      Write-Log "OPENCLAW GATEWAY WARN: gateway RPC probe is reachable but degraded"
      if ($Config.OpenClawGatewayStrict) { return 1 }
    }
    return 0
  }
  Write-Log "OPENCLAW GATEWAY WARN: gateway status --require-rpc failed; falling back to local probes"
  return 2
}

function Test-Gateway {
  $native = Test-OpenClawGateway
  if ($native -eq 0) { return 0 }
  if ($native -eq 1) { return 1 }
  if (Test-Http -Url $Config.GatewayHealthUrl) { return 0 }
  if (Test-Tcp) { return 0 }
  Write-Log "GATEWAY FAIL: no healthy gateway detected"
  return 1
}

function Test-OpenClawChannel {
  $health = Invoke-OpenClawProbe -Args @("health", "--json", "--verbose", "--timeout", "$($Config.OpenClawHealthTimeoutMs)") -OutputName "last-openclaw-health.json"
  if ($health.Supported) {
    if ($health.ExitCode -eq 0 -and $health.Text -notmatch '"ok"\s*:\s*false') { return 0 }
    Write-Log "OPENCLAW CHANNEL FAIL: health live probe failed"
    return 1
  }
  $deep = Invoke-OpenClawProbe -Args @("status", "--deep") -OutputName "last-openclaw-status-deep.txt"
  if ($deep.Supported) {
    if ($deep.ExitCode -eq 0 -and $deep.Text -notmatch "logged[ -]?out|loggedOut|disconnected|unhealthy|healthy\s*:\s*false|probe\s*-?\s*failed|status\s*:\s*(409|410|411|412|413|414|415|500|501|502|503|504|515)|timeout") { return 0 }
    Write-Log "OPENCLAW CHANNEL FAIL: status --deep probe failed"
    return 1
  }
  if ($Config.OpenClawChannelsProbe) {
    $channels = Invoke-OpenClawProbe -Args @("channels", "status", "--probe") -OutputName "last-openclaw-channels-status.txt"
    if ($channels.Supported) {
      if ($channels.ExitCode -eq 0 -and $channels.Text -notmatch "logged[ -]?out|loggedOut|disconnected|unhealthy|healthy\s*:\s*false|probe\s*-?\s*failed|status\s*:\s*(409|410|411|412|413|414|415|500|501|502|503|504|515)|timeout") { return 0 }
      Write-Log "OPENCLAW CHANNEL FAIL: channels status probe failed"
      return 1
    }
  }
  return 2
}

function Test-Channel {
  $native = Test-OpenClawChannel
  if ($native -eq 0) { return $true }
  if ($native -eq 1) { return $false }
  return Test-Http -Url $Config.ChannelUrl
}

function Test-Network {
  foreach ($url in $Config.NetworkUrls) {
    if (Test-Http -Url $url) { return $true }
  }
  Write-Log "NETWORK FAIL: all network probes failed"
  return $false
}

function Test-ModelProbeEnabled {
  return @("1", "true", "on", "yes") -contains ([string]$Config.ModelProbeEnabled).ToLowerInvariant()
}

function Test-DiagEnabled {
  return -not (@("0", "false", "off", "no") -contains ([string]$Config.OpenClawDiagEnabled).ToLowerInvariant())
}

function Test-LogScanEnabled {
  return -not (@("0", "false", "off", "no") -contains ([string]$Config.OpenClawLogScanEnabled).ToLowerInvariant())
}

function Test-DashboardEnabled {
  return -not (@("0", "false", "off", "no") -contains ([string]$Config.DashboardEnabled).ToLowerInvariant())
}

function Test-DashboardActionsEnabled {
  return @("1", "true", "on", "yes") -contains ([string]$Config.DashboardActionsEnabled).ToLowerInvariant()
}

function Test-ModelEdgeProbeEnabled {
  return -not (@("0", "false", "off", "no") -contains ([string]$Config.ModelEdgeProbeEnabled).ToLowerInvariant())
}

function Get-DashboardPidPath {
  return Join-Path $StateDir "dashboard.pid"
}

function Test-DashboardAlive {
  $pidPath = Get-DashboardPidPath
  if (-not (Test-Path -LiteralPath $pidPath)) { return $false }
  $raw = Get-Content -LiteralPath $pidPath -ErrorAction SilentlyContinue | Select-Object -First 1
  $pidValue = 0
  if (-not [int]::TryParse([string]$raw, [ref]$pidValue)) { return $false }
  return [bool](Get-Process -Id $pidValue -ErrorAction SilentlyContinue)
}

function Get-DashboardPython {
  if ($Config.DashboardPython) {
    $cmd = Get-Command $Config.DashboardPython -ErrorAction SilentlyContinue
    if ($cmd) { return @{ File = $cmd.Source; ArgsPrefix = "" } }
  }
  $python = Get-Command python -ErrorAction SilentlyContinue
  if ($python) { return @{ File = $python.Source; ArgsPrefix = "" } }
  $py = Get-Command py -ErrorAction SilentlyContinue
  if ($py) { return @{ File = $py.Source; ArgsPrefix = "-3 " } }
  return $null
}

function Start-Dashboard {
  if (-not (Test-DashboardEnabled)) { return }
  if (Test-DashboardAlive) { return }
  $dashboardDir = [string]$Config.DashboardDir
  if (-not $dashboardDir) { $dashboardDir = Join-Path $PSScriptRoot "dashboard" }
  $serverPath = Join-Path $dashboardDir "server.py"
  if (-not (Test-Path -LiteralPath $serverPath)) {
    Write-Log "DASHBOARD WARN: $serverPath not found; dashboard disabled for this run"
    $Config.DashboardEnabled = $false
    return
  }
  $python = Get-DashboardPython
  if (-not $python) {
    Write-Log "DASHBOARD WARN: python/py not found; dashboard disabled for this run"
    $Config.DashboardEnabled = $false
    return
  }
  $actions = if (Test-DashboardActionsEnabled) { "1" } else { "0" }
  $psi = [System.Diagnostics.ProcessStartInfo]::new()
  $psi.FileName = $python.File
  $psi.Arguments = "$($python.ArgsPrefix)`"$serverPath`""
  $psi.WorkingDirectory = $dashboardDir
  $psi.UseShellExecute = $false
  $psi.CreateNoWindow = $true
  $psi.Environment["WATCHDOG_STATE_DIR"] = $StateDir
  $psi.Environment["WATCHDOG_CONFIG_FILE"] = $ConfigPath
  $psi.Environment["WATCHDOG_DASHBOARD_HOST"] = [string]$Config.DashboardHost
  $psi.Environment["WATCHDOG_DASHBOARD_PORT"] = [string]$Config.DashboardPort
  $psi.Environment["WATCHDOG_DASHBOARD_ACTIONS_ENABLED"] = $actions
  $psi.Environment["WATCHDOG_DASHBOARD_TOKEN"] = [string]$Config.DashboardToken
  try {
    $proc = [System.Diagnostics.Process]::Start($psi)
    Set-Content -LiteralPath (Get-DashboardPidPath) -Value $proc.Id
    Write-Log "DASHBOARD: http://$($Config.DashboardHost):$($Config.DashboardPort)"
  } catch {
    Write-Log "DASHBOARD WARN: failed to start dashboard: $($_.Exception.Message)"
  }
}

function Get-LogSignalCategories {
  param([string]$Text)
  $categories = New-Object System.Collections.Generic.List[string]
  if ($Text -match "fetch failed|fetch timeout|LLM idle timeout|model silent|chat/completions|providerRuntimeFailureKind.*timeout") { $categories.Add("provider_timeout") }
  if ($Text -match "ECONNRESET|ECONNREFUSED|ETIMEDOUT|ENOTFOUND|socket hang up|TLS|CERT_|proxy") { $categories.Add("proxy_or_network") }
  if ($Text -match "429|rate limit|too many requests|quota") { $categories.Add("provider_rate_limit") }
  if ($Text -match "401|403|unauthorized|forbidden|invalid api key|auth") { $categories.Add("provider_auth") }
  if ($Text -match "embedded abort settle timed out") { $categories.Add("abort_stuck") }
  if ($Text -match "memory-core: narrative generation ended with status=timeout|dreaming.*timeout") { $categories.Add("memory_dream_timeout") }
  if ($Text -match "restartPending|session expired|errcode=-14|Monitor.*stopped|monitor.*ended") { $categories.Add("channel_session") }
  if ($Text -match "event loop|degraded|health-monitor") { $categories.Add("gateway_degraded") }
  if ($Text -match "config hot reload|config change detected") { $categories.Add("config_reload") }
  if ($Text -match "cron.*error|task.*failed|run failover decision") { $categories.Add("task_runtime") }
  if ($Text -match "\bwarn\b|\bwarning\b|\berror\b|\bfailed\b|\btimeout\b") { $categories.Add("openclaw_warning") }
  if ($categories.Count -eq 0) { return "unknown" }
  return ($categories -join ",")
}

function Invoke-OpenClawLogScan {
  if (-not (Test-LogScanEnabled)) { return 2 }
  if (-not (Get-Command openclaw -ErrorAction SilentlyContinue)) { return 2 }

  $logFile = Join-Path $StateDir "last-openclaw-logs.txt"
  $signalsFile = Join-Path $StateDir "last-openclaw-log-signals.txt"
  $categoriesFile = Join-Path $StateDir "last-openclaw-log-signal-categories.txt"
  $fingerprintFile = Join-Path $StateDir "last-openclaw-log-signals.cksum"

  $output = & openclaw logs --plain --limit "$($Config.OpenClawLogLimit)" --timeout "$($Config.OpenClawLogTimeoutMs)" 2>&1
  if ($LASTEXITCODE -ne 0) { return 2 }
  $output | Out-File -LiteralPath $logFile -Encoding utf8
  $pattern = "($($Config.OpenClawLogWarnPatterns))|\b(warn|warning|error|failed|timeout)\b"
  $signals = $output | Select-String -Pattern $pattern | Select-Object -Last ([int]$Config.OpenClawLogSignalLimit)
  if (-not $signals) { return 0 }
  $signalText = ($signals | ForEach-Object { $_.Line }) -join [Environment]::NewLine
  $signalText | Out-File -LiteralPath $signalsFile -Encoding utf8
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($signalText)
  $sha256 = [System.Security.Cryptography.SHA256]::Create()
  try {
    $hashBytes = $sha256.ComputeHash($bytes)
  } finally {
    $sha256.Dispose()
  }
  $hash = [System.BitConverter]::ToString($hashBytes).Replace("-", "").ToLowerInvariant()
  $previous = ""
  if (Test-Path -LiteralPath $fingerprintFile) { $previous = Get-Content -LiteralPath $fingerprintFile -Raw }
  if ($hash -eq $previous.Trim()) { return 0 }
  Set-Content -LiteralPath $fingerprintFile -Value $hash

  $categories = Get-LogSignalCategories -Text $signalText
  Set-Content -LiteralPath $categoriesFile -Value $categories
  Write-Log "OPENCLAW LOG WARN: categories=$categories matches=$($signals.Count) fingerprint=$hash"
  $first = ($signalText -split "`n" | Where-Object { $_.Trim() } | Select-Object -First 1)
  if ($first) { Write-Log "OPENCLAW LOG DETAIL: $($first.Substring(0, [Math]::Min(220, $first.Length)))" }
  return 1
}

function Invoke-OpenClawDiagnostics {
  if (-not (Test-DiagEnabled)) { return 2 }
  if (-not (Test-NativeEnabled)) { return 2 }
  if (-not (Get-Command openclaw -ErrorAction SilentlyContinue)) { return 2 }

  $degraded = $false
  $signals = $false
  $categories = "none"
  $summaryFile = Join-Path $StateDir "last-openclaw-diagnostics.jsonl"

  $gateway = & openclaw gateway status --json --require-rpc --timeout "$($Config.OpenClawHealthTimeoutMs)" 2>&1
  Save-ProbeOutput -Name "last-openclaw-gateway-status.json" -Output $gateway | Out-Null
  $health = & openclaw health --json --verbose --timeout "$($Config.OpenClawHealthTimeoutMs)" 2>&1
  Save-ProbeOutput -Name "last-openclaw-health.json" -Output $health | Out-Null
  $models = & openclaw models status --json 2>&1
  Save-ProbeOutput -Name "last-openclaw-model-status.json" -Output $models | Out-Null
  $statusDeep = & openclaw status --deep --no-color 2>&1
  Save-ProbeOutput -Name "last-openclaw-status-deep.txt" -Output $statusDeep | Out-Null

  $healthText = $health -join "`n"
  if ($healthText -match '"degraded"\s*:\s*true|"ok"\s*:\s*false') {
    $degraded = $true
    Write-Log "OPENCLAW DIAG WARN: health snapshot reports degraded or not ok"
  }
  $modelsText = $models -join "`n"
  if ($modelsText -match '"fallbacks"\s*:\s*\[\]') {
    Write-Log "OPENCLAW DIAG INFO: no model fallbacks configured"
  }

  $logResult = Invoke-OpenClawLogScan
  if ($logResult -eq 1) {
    $signals = $true
    $categoriesFile = Join-Path $StateDir "last-openclaw-log-signal-categories.txt"
    if (Test-Path -LiteralPath $categoriesFile) {
      $categories = (Get-Content -LiteralPath $categoriesFile -Raw).Trim()
    } else {
      $categories = "unknown"
    }
  }

  (@{
    ts = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
    healthDegraded = $degraded
    newLogSignals = $signals
    categories = $categories
  } | ConvertTo-Json -Compress) | Add-Content -LiteralPath $summaryFile

  if ($degraded -or $signals) { return 1 }
  return 0
}

function Invoke-DiagFailureAction {
  param([int]$Failures)
  if ($Failures -lt [int]$Config.OpenClawDiagFailuresBeforeAction) { return }
  if (-not (Test-Network)) {
    Write-Log "OPENCLAW DIAG SAFEGUARD: general network probes failed; skip diagnostic action"
    return
  }
  switch ([string]$Config.OpenClawDiagAction) {
    "restart" {
      Write-Log "OPENCLAW DIAG ACTION: restart gateway after $Failures consecutive diagnostic warnings"
      Restart-Gateway
    }
    "command" {
      if ($Config.OpenClawDiagCommand) {
        Write-Log "OPENCLAW DIAG ACTION: $($Config.OpenClawDiagCommand)"
        cmd.exe /c $Config.OpenClawDiagCommand 2>&1 | Tee-Object -FilePath $LogFile -Append
        if ($LASTEXITCODE -ne 0) { Write-Log "OPENCLAW DIAG ACTION FAIL: command returned non-zero" }
      } else {
        Write-Log "OPENCLAW DIAG ACTION WARN: OpenClawDiagAction=command but OpenClawDiagCommand is empty"
      }
    }
    default {
      Write-Log "OPENCLAW DIAG ACTION: log-only after $Failures consecutive diagnostic warnings"
    }
  }
}

function Invoke-ModelApiEdgeProbe {
  if (-not (Test-ModelEdgeProbeEnabled)) { return 2 }
  if (-not (Get-Command openclaw -ErrorAction SilentlyContinue)) { return 2 }

  $model = [string]$Config.ModelProbeModel
  if (-not $model) {
    $statusOutput = & openclaw models status --json 2>&1
    if ($LASTEXITCODE -ne 0) { return 2 }
    Save-ProbeOutput -Name "last-openclaw-model-status.json" -Output $statusOutput | Out-Null
    try {
      $statusJson = ($statusOutput -join "`n") | ConvertFrom-Json -ErrorAction Stop
      $model = [string]$statusJson.defaultModel
    } catch {
      return 2
    }
  }
  if (-not $model -or $model -notmatch "/") { return 2 }
  $provider = ($model -split "/", 2)[0]

  $providerOutput = & openclaw config get "models.providers.$provider" 2>&1
  if ($LASTEXITCODE -ne 0) { return 2 }
  Save-ProbeOutput -Name "last-openclaw-model-provider.json" -Output $providerOutput | Out-Null
  try {
    $providerJson = ($providerOutput -join "`n") | ConvertFrom-Json -ErrorAction Stop
    $baseUrl = [string]$providerJson.baseUrl
  } catch {
    return 2
  }
  if (-not $baseUrl) { return 2 }

  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  $statusCode = 0
  $ok = $false
  $errorText = ""
  try {
    $response = Invoke-WebRequest -Uri $baseUrl -UseBasicParsing -TimeoutSec ([int]$Config.MaxTime)
    $statusCode = [int]$response.StatusCode
    $ok = ($statusCode -ge 200 -and $statusCode -lt 500)
  } catch {
    $errorText = $_.Exception.Message
    if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
      $statusCode = [int]$_.Exception.Response.StatusCode
      $ok = ($statusCode -ge 200 -and $statusCode -lt 500)
    }
  } finally {
    $sw.Stop()
  }

  $line = "provider=$provider model=$model base=$baseUrl code=$statusCode total=$([Math]::Round($sw.Elapsed.TotalSeconds, 3))s"
  Set-Content -LiteralPath (Join-Path $StateDir "last-model-api-edge-probe.txt") -Value $line
  if ($ok) {
    Write-Log "MODEL API EDGE OK: $line"
    return 0
  }
  Write-Log "MODEL API EDGE FAIL: $line error=$errorText"
  return 1
}

function Invoke-ModelProbe {
  if (-not (Test-ModelProbeEnabled)) { return 2 }
  if (-not (Get-Command openclaw -ErrorAction SilentlyContinue)) {
    Write-Log "MODEL PROBE WARN: openclaw CLI not found; skip model probe"
    return 2
  }

  $outputName = "last-openclaw-model-probe.json"
  $historyPath = Join-Path $StateDir "model-probe-history.jsonl"
  $started = Get-Date
  Invoke-ModelApiEdgeProbe | Out-Null
  $args = @(
    "agent",
    "--session-id", "$($Config.ModelProbeSessionId)",
    "--thinking", "$($Config.ModelProbeThinking)",
    "--timeout", "$($Config.ModelProbeTimeout)",
    "--json",
    "--message", "$($Config.ModelProbeMessage)"
  )
  if ($Config.ModelProbeModel) {
    $args = @(
      "agent",
      "--session-id", "$($Config.ModelProbeSessionId)",
      "--model", "$($Config.ModelProbeModel)",
      "--thinking", "$($Config.ModelProbeThinking)",
      "--timeout", "$($Config.ModelProbeTimeout)",
      "--json",
      "--message", "$($Config.ModelProbeMessage)"
    )
  }

  $output = & openclaw @args 2>&1
  $exitCode = $LASTEXITCODE
  $path = Save-ProbeOutput -Name $outputName -Output $output
  $duration = [int]((Get-Date) - $started).TotalSeconds
  $text = $output -join "`n"
  $status = ""
  $provider = "unknown"
  $model = if ($Config.ModelProbeModel) { "$($Config.ModelProbeModel)" } else { "configured-default" }
  try {
    $json = $text | ConvertFrom-Json -ErrorAction Stop
    $status = [string]$json.status
    if ($json.result.meta.agentMeta.provider) { $provider = [string]$json.result.meta.agentMeta.provider }
    if ($json.result.meta.agentMeta.model) { $model = [string]$json.result.meta.agentMeta.model }
  } catch {
    $status = ""
  }

  if ($exitCode -eq 0 -and $status -eq "ok") {
    Write-Log "MODEL PROBE OK: provider=$provider model=$model duration=${duration}s session=$($Config.ModelProbeSessionId)"
    (@{
      ts = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
      status = "ok"
      provider = $provider
      model = $model
      durationSeconds = $duration
    } | ConvertTo-Json -Compress) | Add-Content -LiteralPath $historyPath
    return 0
  }

  $reason = "failed"
  if ($text -match "timeout|timed out|idle timeout|fetch timeout") {
    $reason = "timeout"
  } elseif ($text -match "rate limit|429|too many requests") {
    $reason = "rate_limited"
  } elseif ($text -match "401|403|unauthorized|forbidden|invalid api key|auth") {
    $reason = "auth"
  } elseif ($text -match "Model override .* not allowed") {
    $reason = "config"
  }

  Write-Log "MODEL PROBE FAIL: reason=$reason rc=$exitCode provider=$provider model=$model duration=${duration}s timeout=$($Config.ModelProbeTimeout)s"
  $detail = ($text -split "`n" | Where-Object { $_.Trim() } | Select-Object -First 1)
  if ($detail) { Write-Log "MODEL PROBE DETAIL: $($detail.Substring(0, [Math]::Min(220, $detail.Length)))" }
  (@{
    ts = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
    status = "fail"
    reason = $reason
    provider = $provider
    model = $model
    durationSeconds = $duration
    exitCode = $exitCode
  } | ConvertTo-Json -Compress) | Add-Content -LiteralPath $historyPath
  return 1
}

function Invoke-ModelProbeFailureAction {
  param([int]$Failures)
  if ($Failures -lt [int]$Config.ModelProbeFailuresBeforeAction) { return }
  if (-not (Test-Network)) {
    Write-Log "MODEL PROBE SAFEGUARD: general network probes failed; skip model action"
    return
  }
  switch ([string]$Config.ModelProbeAction) {
    "restart" {
      Write-Log "MODEL PROBE ACTION: restart gateway after $Failures consecutive model probe failures"
      Restart-Gateway
    }
    "command" {
      if ($Config.ModelProbeCommand) {
        Write-Log "MODEL PROBE ACTION: $($Config.ModelProbeCommand)"
        cmd.exe /c $Config.ModelProbeCommand 2>&1 | Tee-Object -FilePath $LogFile -Append
        if ($LASTEXITCODE -ne 0) { Write-Log "MODEL PROBE ACTION FAIL: command returned non-zero" }
      } else {
        Write-Log "MODEL PROBE ACTION WARN: ModelProbeAction=command but ModelProbeCommand is empty"
      }
    }
    default {
      Write-Log "MODEL PROBE ACTION: log-only after $Failures consecutive model probe failures"
    }
  }
}

function Get-RestartCountFile {
  return Join-Path $StateDir ("restarts.{0}" -f (Get-Date -Format "yyyyMMddHH"))
}

function Test-CanRestart {
  $file = Get-RestartCountFile
  $count = 0
  if (Test-Path -LiteralPath $file) { $count = [int](Get-Content -LiteralPath $file -ErrorAction SilentlyContinue) }
  return ($count -lt [int]$Config.MaxRestartsPerHour)
}

function Register-Restart {
  $file = Get-RestartCountFile
  $count = 0
  if (Test-Path -LiteralPath $file) { $count = [int](Get-Content -LiteralPath $file -ErrorAction SilentlyContinue) }
  Set-Content -LiteralPath $file -Value ($count + 1)
}

function Restart-Gateway {
  if (-not (Test-CanRestart)) {
    Write-Log "CIRCUIT OPEN: restart limit reached ($($Config.MaxRestartsPerHour)/hour); skip restart"
    return
  }
  if ($Config.RestartCommand) {
    Write-Log "ACTION: $($Config.RestartCommand)"
    cmd.exe /c $Config.RestartCommand 2>&1 | Tee-Object -FilePath $LogFile -Append
    if ($LASTEXITCODE -eq 0) {
      Register-Restart
    } else {
      Write-Log "ACTION FAIL: restart command returned non-zero"
    }
    return
  }
  if (Get-Command openclaw -ErrorAction SilentlyContinue) {
    Write-Log "ACTION: openclaw gateway restart"
    & openclaw gateway restart 2>&1 | Tee-Object -FilePath $LogFile -Append
    if ($LASTEXITCODE -eq 0) {
      Register-Restart
    } else {
      Write-Log "ACTION FAIL: openclaw gateway restart failed"
    }
    return
  }
  Write-Log "ACTION FAIL: set RestartCommand in $ConfigPath; no restart method found"
}

function Get-BackoffInterval {
  param([int]$Failures)
  $interval = [int]$Config.BaseInterval
  for ($i = 1; $i -lt $Failures; $i++) {
    $interval *= 2
    if ($interval -ge [int]$Config.MaxInterval) { break }
  }
  return [Math]::Min($interval, [int]$Config.MaxInterval)
}

function Get-SleepInterval {
  $hour = [int](Get-Date -Format "HH")
  if ($hour -ge 1 -and $hour -lt 8) { return [int]$Config.NightInterval }
  return [int]$Config.BaseInterval
}

try {
  $failCount = 0
  $successCount = 0
  $modelFailCount = 0
  $diagFailCount = 0
  $lastDiagAt = [DateTimeOffset]::FromUnixTimeSeconds(0)
  $lastModelProbeAt = [DateTimeOffset]::FromUnixTimeSeconds(0)
  Write-Log "START: OpenClaw Gateway Resilience Guard $Version"
  Write-Log "CONFIG: $ConfigPath"
  Start-Dashboard

  while ($true) {
    Rotate-LogIfNeeded
    Start-Dashboard
    $gateway = Test-Gateway
    if ($gateway -eq 1) {
      $failCount += 1
      $successCount = 0
      Write-Log "CRITICAL: gateway appears down; restarting immediately"
      Restart-Gateway
      Start-Sleep -Seconds ([int]$Config.PostRestartSleep)
      continue
    }

    if (Test-DiagEnabled) {
      $now = [DateTimeOffset]::UtcNow
      if ($lastDiagAt.ToUnixTimeSeconds() -eq 0 -or ($now - $lastDiagAt).TotalSeconds -ge [int]$Config.OpenClawDiagInterval) {
        $lastDiagAt = $now
        $diagResult = Invoke-OpenClawDiagnostics
        if ($diagResult -eq 0) {
          $diagFailCount = 0
        } elseif ($diagResult -eq 1) {
          $diagFailCount += 1
          Invoke-DiagFailureAction -Failures $diagFailCount
        }
      }
    }

    if (Test-ModelProbeEnabled) {
      $now = [DateTimeOffset]::UtcNow
      if ($lastModelProbeAt.ToUnixTimeSeconds() -eq 0 -or ($now - $lastModelProbeAt).TotalSeconds -ge [int]$Config.ModelProbeInterval) {
        $lastModelProbeAt = $now
        $probeResult = Invoke-ModelProbe
        if ($probeResult -eq 0) {
          $modelFailCount = 0
        } elseif ($probeResult -eq 1) {
          $modelFailCount += 1
          Invoke-ModelProbeFailureAction -Failures $modelFailCount
        }
      }
    }

    if (Test-Channel) {
      if ($failCount -gt 0) {
        $successCount += 1
        if ($successCount -ge [int]$Config.SuccessCountToReset) {
          Write-Log "RECOVERED: $($Config.SuccessCountToReset) consecutive channel probes succeeded; failure count reset"
          $failCount = 0
          $successCount = 0
        } else {
          Write-Log "RECOVERING: channel probe succeeded ($successCount/$($Config.SuccessCountToReset))"
        }
      }
      Start-Sleep -Seconds (Get-SleepInterval)
      continue
    }

    $failCount += 1
    $successCount = 0
    Write-Log "CHANNEL FAIL: channel probe failed ($failCount/$($Config.ChannelFailuresBeforeRestart))"
    if (-not (Test-Network)) {
      Write-Log "SAFEGUARD: looks like global network trouble; wait without restarting gateway"
      Start-Sleep -Seconds ([int]$Config.BaseInterval)
      continue
    }
    if ($failCount -lt [int]$Config.ChannelFailuresBeforeRestart) {
      Start-Sleep -Seconds ([int]$Config.BaseInterval)
      continue
    }
    $waitFor = Get-BackoffInterval -Failures $failCount
    Write-Log "BACKOFF: network is reachable; will re-check channel in ${waitFor}s before restart"
    Start-Sleep -Seconds $waitFor
    if (Test-Channel) {
      Write-Log "RECOVERED: channel came back before restart"
      $failCount = 0
      continue
    }
    Restart-Gateway
    Start-Sleep -Seconds ([int]$Config.PostRestartSleep)
  }
} finally {
  $mutex.ReleaseMutex() | Out-Null
  $mutex.Dispose()
}
