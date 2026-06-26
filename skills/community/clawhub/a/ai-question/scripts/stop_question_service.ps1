# Stop QuizAI Python service
$ErrorActionPreference = "Continue"

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
$servicePidFile = Join-Path $Root "data\quizai.pid"
$stopped = $false

function Stop-ProcessTree($processId) {
    if (-not $processId) { return $false }
    try {
        taskkill /PID $processId /T /F 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Stopped process tree PID $processId"
            return $true
        }
        Stop-Process -Id $processId -Force -ErrorAction Stop
        Write-Host "Stopped process PID $processId"
        return $true
    }
    catch {
        return $false
    }
}

if (Test-Path $servicePidFile) {
    $savedPid = (Get-Content $servicePidFile -Raw).Trim()
    if ($savedPid -match '^\d+$') {
        if (Stop-ProcessTree ([int]$savedPid)) { $stopped = $true }
    }
    Remove-Item $servicePidFile -Force -ErrorAction SilentlyContinue
}

$conns = @(Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue)
foreach ($c in $conns) {
    if (Stop-ProcessTree $c.OwningProcess) { $stopped = $true }
}

if ($stopped) {
    Write-Host "QuizAI service stopped"
}
else {
    Write-Host "No running QuizAI service on port 8000"
}

exit 0
