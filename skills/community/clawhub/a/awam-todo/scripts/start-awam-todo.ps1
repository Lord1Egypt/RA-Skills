# awam-todo single entry: stop any stale UI service, then start the UI backend
# and the capture service (global hotkey -> clipboard -> triage) together.
# Usage:  powershell -NoProfile -ExecutionPolicy Bypass -File scripts\start-awam-todo.ps1 [-Port 8796] [-NoBrowser]
param([int]$Port = 8796, [switch]$NoBrowser)
$ErrorActionPreference = "SilentlyContinue"
$root = Split-Path -Parent $PSScriptRoot
$server = Join-Path $root "web\server.py"

# 0) Read the configured ui.port from env.json when the caller did not override it
$envPath = Join-Path $root "env.json"
$port = $Port
if (Test-Path $envPath) {
    try {
        $cfg = Get-Content $envPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($cfg.ui -and $cfg.ui.port) { $port = [int]$cfg.ui.port }
    } catch { }
}

# 1) Stop stale awam-todo server processes. Match any python running a server.py
#    whose command line references awam-todo or a web\server.py / web/server.py
#    path (covers absolute AND relative-path launches).
$stale = Get-CimInstance Win32_Process -Filter "Name like 'python%'" | Where-Object {
    $_.CommandLine -match "server\.py" -and
    ($_.CommandLine -match "awam-todo" -or $_.CommandLine -match "web[/\\]server\.py")
}
foreach ($p in $stale) {
    Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    Write-Host ("Stopped stale server PID " + $p.ProcessId)
}

# 2) Stop whatever holds the target port if it looks like an awam-todo server
$conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
foreach ($c in $conn) {
    $proc = Get-CimInstance Win32_Process -Filter ("ProcessId = " + $c.OwningProcess)
    if ($proc -and $proc.CommandLine -match "server\.py") {
        Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
        Write-Host ("Stopped stale listener PID " + $c.OwningProcess)
    }
}
for ($i = 0; $i -lt 8; $i++) {
    $still = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if (-not $still) { break }
    Start-Sleep -Milliseconds 250
}

# 3) Start the combined service (web UI backend + capture hotkey listener)
$serverArgs = @($server, "--port", "$port")
if ($NoBrowser) { $serverArgs += "--no-browser" }
Start-Process -FilePath "python" -ArgumentList $serverArgs -WorkingDirectory $root -WindowStyle Hidden
Write-Host ("awam-todo started at http://127.0.0.1:" + $port + "/ (UI + capture service)")

# 4) Self-check: wait for the settings API, then report the capture service state
for ($i = 0; $i -lt 10; $i++) {
    Start-Sleep -Milliseconds 500
    try {
        $resp = Invoke-WebRequest -Uri ("http://127.0.0.1:" + $port + "/api/settings") -UseBasicParsing -TimeoutSec 2
        if ($resp.StatusCode -eq 200) {
            $state = "unknown"
            try {
                $j = $resp.Content | ConvertFrom-Json
                $state = $j.service.state
            } catch { }
            Write-Host ("Capture service state: " + $state)
            break
        }
    } catch { }
}
