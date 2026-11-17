# ============================================================
# 1688 Data Claw - Windows launcher
# Start or reuse an independent Chromium instance (headless)
# Uses a marker file to identify our instance (no process kill)
# ============================================================

Write-Host "1688 Data Claw - Start/Reuse Browser" -ForegroundColor Cyan

$SKILL_DIR = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$CHROME = "$SKILL_DIR\chromium\chrome-win64\chrome.exe"
$USER_DATA = "C:\isolated-profiles\1688-agent"
$EXT_DIR = "$SKILL_DIR\plugin"
$CDP_PORT = 9222
$MARKER = "$USER_DATA\.openclaw_browser_marker"

try {
    $resp = Invoke-WebRequest -Uri "http://127.0.0.1:$CDP_PORT/json/version" -UseBasicParsing -TimeoutSec 3
    if ($resp.StatusCode -eq 200) {
        if (Test-Path $MARKER) {
            Write-Host "Independent Chromium is running, reuse it (CDP port $CDP_PORT)"
            exit 0
        }
        Write-Host "CDP port $CDP_PORT is occupied by another process" -ForegroundColor Red
        Write-Host "Marker file $MARKER not found, not our Chromium instance"
        Write-Host "Please close the process occupying the port and retry"
        exit 1
    }
} catch {
    Write-Host "CDP port not responding, starting browser..."
}

if (-not (Test-Path $USER_DATA)) {
    New-Item -ItemType Directory -Path $USER_DATA -Force | Out-Null
}

$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
"PORT=$CDP_PORT`r`nTimestamp=$timestamp" | Out-File -FilePath $MARKER -Encoding ASCII
Write-Host "Marker written: $MARKER"

Write-Host "Starting headless Chromium..."
$argsList = @(
    "--remote-debugging-port=$CDP_PORT",
    "--user-data-dir=$USER_DATA",
    "--load-extension=$EXT_DIR",
    "--headless=new",
    "--disable-gpu",
    "--disable-sync",
    "--no-first-run",
    "--disable-background-networking",
    "--disable-component-update",
    "--disable-crash-reporter",
    "--disable-default-apps",
    "--no-default-browser-check"
)
Start-Process -NoNewWindow -FilePath $CHROME -ArgumentList $argsList
Write-Host "Browser started, waiting for readiness..."
Start-Sleep -Seconds 3
Write-Host "Startup complete"
