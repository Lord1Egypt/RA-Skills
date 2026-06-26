# Start QuizAI Python service
$ErrorActionPreference = "Stop"

function Get-QuizaiProjectRoot {
    param([string]$StartDir)
    $dir = $StartDir
    while ($dir) {
        $runPy = Join-Path $dir "run.py"
        $mainPy = Join-Path $dir "app\main.py"
        if ((Test-Path -LiteralPath $runPy) -and (Test-Path -LiteralPath $mainPy)) {
            return (Resolve-Path $dir).Path
        }
        $parent = Split-Path $dir -Parent
        if (-not $parent -or $parent -eq $dir) { break }
        $dir = $parent
    }
    throw "QuizAI project root not found (need run.py and app/main.py). Open the repo root in Agent."
}

$Root = Get-QuizaiProjectRoot -StartDir $PSScriptRoot
Set-Location $Root

function Test-Python {
    try {
        $v = python --version 2>&1
        if ($LASTEXITCODE -ne 0) { return $false }
        Write-Host "Python: $v"
        return $true
    } catch {
        return $false
    }
}

if (-not (Test-Python)) {
    Write-Host "Python not found, trying winget install Python 3.12..."
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
        [System.Environment]::GetEnvironmentVariable("Path", "User")
    if (-not (Test-Python)) {
        Write-Error "Python still unavailable after install"
    }
}

$pythonExe = Join-Path $Root "venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $pythonExe)) {
    Write-Host "Creating venv..."
    python -m venv venv
}
if (-not (Test-Path -LiteralPath $pythonExe)) {
    Write-Error "venv python missing: $pythonExe"
}

Write-Host "Installing dependencies..."
& $pythonExe -m pip install -q --upgrade pip
& $pythonExe -m pip install -q -r (Join-Path $Root "requirements.txt")

$servicePidFile = Join-Path $Root "data\quizai.pid"
$healthUrl = "http://127.0.0.1:8000/health"

try {
    $r = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 2
    if ($r.StatusCode -eq 200) {
        Write-Host "Service already running: $healthUrl"
        exit 0
    }
} catch {}

Write-Host "Starting QuizAI..."
$dataDir = Join-Path $Root "data"
New-Item -ItemType Directory -Force -Path $dataDir | Out-Null

$proc = Start-Process -FilePath $pythonExe -ArgumentList "run.py" -WorkingDirectory $Root -PassThru -WindowStyle Hidden
if (-not $proc) {
    Write-Error "Failed to start: $pythonExe run.py"
}

Start-Sleep -Seconds 3
$proc.Id | Out-File -FilePath $servicePidFile -Encoding utf8

try {
    $r = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 10
    if ($r.Content -match '"status"\s*:\s*"ok"') {
        Write-Host "Service started: http://127.0.0.1:8000 (PID $($proc.Id))"
        exit 0
    }
} catch {}

Write-Host "Process started (PID $($proc.Id)), health check pending. Try http://127.0.0.1:8000"
exit 0
