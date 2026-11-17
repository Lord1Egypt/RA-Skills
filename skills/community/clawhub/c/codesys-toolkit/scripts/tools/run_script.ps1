# run_script.ps1  (scripts/tools/)
#
# Unified launcher: kill old InoProShop -> run script -> tail log -> print summary
#
# Usage:
#   .\run_script.ps1 patch                             # run patch_pou.py
#   .\run_script.ps1 check                             # run check_compile.py
#   .\run_script.ps1 export                            # run export_pou.py
#   .\run_script.ps1 list                              # run list_devices.py
#   .\run_script.ps1 workspace\conveyor_generator.py   # relative to skill root
#   .\run_script.ps1 D:\full\path\to\script.py         # absolute path
#
# Parameters:
#   -Script    alias or path (positional, required)
#   -NoKill    keep existing InoProShop instances
#   -Timeout   max seconds to wait (default 120)

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$Script,

    [switch]$NoKill,

    [int]$Timeout = 120
)

# ---------------------------------------------------------------
# Load env config
# ---------------------------------------------------------------
$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $toolsDir "env_setup.ps1")

# ---------------------------------------------------------------
# Helper: update workspace_dir / active_project in env.json
# Called when running 'export' to auto-derive the project folder.
# ---------------------------------------------------------------
function Update-WorkspaceDir {
    param([string]$ProjectPath)

    $envJsonPath = Join-Path $INOPRO_SKILL_DIR "references\env.json"
    if (-not (Test-Path $envJsonPath)) { return $null }

    try {
        $raw    = [IO.File]::ReadAllText($envJsonPath, [Text.UTF8Encoding]::new($false))
        $envObj = $raw | ConvertFrom-Json

        $projName  = [System.IO.Path]::GetFileNameWithoutExtension($ProjectPath)
        $wsDir     = Join-Path (Join-Path $INOPRO_SKILL_DIR "scripts\workspace") $projName

        $builtinWs  = Join-Path $INOPRO_SKILL_DIR "scripts\workspace"
        $currentWs  = $envObj.workspace_dir
        $isExternal = $currentWs -and (-not $currentWs.StartsWith($builtinWs))

        if (-not $isExternal) {
            $envObj | Add-Member -Force -MemberType NoteProperty -Name "active_project" -Value $projName
            $envObj | Add-Member -Force -MemberType NoteProperty -Name "workspace_dir"  -Value $wsDir

            $json = $envObj | ConvertTo-Json -Depth 5
            [IO.File]::WriteAllText($envJsonPath, $json, [Text.UTF8Encoding]::new($false))

            Write-Host "      [env] active_project=$projName" -ForegroundColor Gray
            Write-Host "      [env] workspace_dir=$wsDir"     -ForegroundColor Gray
            return $wsDir
        } else {
            Write-Host "      [env] external workspace_dir detected, keeping: $currentWs" -ForegroundColor Gray
            return $currentWs
        }
    } catch {
        Write-Host "      [WARN] Failed to update env.json workspace_dir: $_" -ForegroundColor Yellow
        return $null
    }
}

# ---------------------------------------------------------------
# Resolve script path (alias or relative/absolute)
# ---------------------------------------------------------------
$aliases = @{
    'patch'    = 'scripts\tools\patch_pou.py'
    'check'    = 'scripts\tools\check_compile.py'
    'list'     = 'scripts\tools\list_devices.py'
    'export'   = 'scripts\tools\export_pou.py'
    'generate' = 'scripts\tools\generator_runner.py'
}

if ($aliases.ContainsKey($Script.ToLower())) {
    $scriptPath = Join-Path $INOPRO_SKILL_DIR $aliases[$Script.ToLower()]

    # generate: check for project-level override before resolving env/log paths.
    # If workspace_dir/generator_override.py exists, use it instead of the
    # shared generator_runner.py so that project-specific fixes never pollute
    # the universal tool.
    if ($Script.ToLower() -eq 'generate') {
        $envJsonPath = Join-Path $INOPRO_SKILL_DIR "references\env.json"
        if (Test-Path $envJsonPath) {
            try {
                $envTmpOv  = [IO.File]::ReadAllText($envJsonPath, [Text.UTF8Encoding]::new($false)) | ConvertFrom-Json
                $wsDir     = $envTmpOv.workspace_dir
                if ($wsDir) {
                    $overridePath = Join-Path $wsDir "generator_override.py"
                    if (Test-Path $overridePath) {
                        Write-Host "  [override] Found generator_override.py in workspace, using it instead of generator_runner.py" -ForegroundColor Cyan
                        $scriptPath = $overridePath
                    }
                }
            } catch { }
        }
    }
} elseif ([System.IO.Path]::IsPathRooted($Script)) {
    $scriptPath = $Script
} else {
    $scriptPath = Join-Path $INOPRO_SKILL_DIR $Script
}

if (-not (Test-Path $scriptPath)) {
    Write-Host "[ERROR] Script not found: $scriptPath" -ForegroundColor Red
    exit 1
}

# Auto-update workspace_dir when running export/patch/check/generate
$_resolvedWsDir = $null
if ($Script.ToLower() -in @('export', 'patch', 'check')) {
    $envJsonPath = Join-Path $INOPRO_SKILL_DIR "references\env.json"
    if (Test-Path $envJsonPath) {
        try {
            $envTmp      = [IO.File]::ReadAllText($envJsonPath, [Text.UTF8Encoding]::new($false)) | ConvertFrom-Json
            $patchTarget = $envTmp.patch_target
            if ($patchTarget -and (Test-Path $patchTarget)) {
                $_resolvedWsDir = Update-WorkspaceDir -ProjectPath $patchTarget
            } else {
                # patch_target not set or file missing — use existing workspace_dir as-is
                $_resolvedWsDir = $envTmp.workspace_dir
            }
        } catch { }
    }
} elseif ($Script.ToLower() -eq 'generate') {
    # generate reads workspace_dir directly from env.json (no patch_target involved)
    # Must resolve here so that snapshot is written after generate completes.
    $envJsonPath = Join-Path $INOPRO_SKILL_DIR "references\env.json"
    if (Test-Path $envJsonPath) {
        try {
            $envTmp = [IO.File]::ReadAllText($envJsonPath, [Text.UTF8Encoding]::new($false)) | ConvertFrom-Json
            $_resolvedWsDir = $envTmp.workspace_dir
        } catch { }
    }
}

# Derive log path from script name
$scriptBase = [System.IO.Path]::GetFileNameWithoutExtension($scriptPath)
$fixedLogNames = @{
    'patch_pou'     = 'patch_pou_log.txt'
    'check_compile' = 'check_compile_log.txt'
    'list_devices'  = 'list_devices_log.txt'
    'export_pou'    = 'export_pou_log.txt'
}

# Use the wsDir returned directly from Update-WorkspaceDir (avoids re-reading env.json)
# Fallback: read env.json once more, then legacy flat workspace/log
if (-not $_resolvedWsDir) {
    try {
        $envFb = [IO.File]::ReadAllText(
            (Join-Path $INOPRO_SKILL_DIR "references\env.json"),
            [Text.UTF8Encoding]::new($false)) | ConvertFrom-Json
        $_resolvedWsDir = $envFb.workspace_dir
    } catch { }
}
$_wsLogDir = if ($_resolvedWsDir) {
    Join-Path $_resolvedWsDir "log"
} else {
    Join-Path (Join-Path $INOPRO_SKILL_DIR "scripts\workspace") "log"
}

if ($fixedLogNames.ContainsKey($scriptBase)) {
    $logPath = Join-Path $_wsLogDir $fixedLogNames[$scriptBase]
} else {
    $logPath = Join-Path $_wsLogDir "${scriptBase}_log.txt"
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " InoProShop Script Runner" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " Script : $scriptPath" -ForegroundColor White
Write-Host " Log    : $logPath" -ForegroundColor Gray
Write-Host "======================================" -ForegroundColor Cyan

# ---------------------------------------------------------------
# Kill old InoProShop instances
# ---------------------------------------------------------------
if (-not $NoKill) {
    $oldProcs = Get-Process -Name "InoProShop" -ErrorAction SilentlyContinue
    if ($oldProcs) {
        Write-Host "`n[1/4] Killing $($oldProcs.Count) old InoProShop instance(s)..." -ForegroundColor Yellow
        $oldProcs | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        Write-Host "      Done" -ForegroundColor Green
    } else {
        Write-Host "`n[1/4] No old instances found" -ForegroundColor Gray
    }
} else {
    Write-Host "`n[1/4] -NoKill specified, keeping existing instances" -ForegroundColor Gray
}

# ---------------------------------------------------------------
# Clear old log
# ---------------------------------------------------------------
$logParent = Split-Path -Parent $logPath
if (-not (Test-Path $logParent)) { New-Item -ItemType Directory -Path $logParent -Force | Out-Null }
if (Test-Path $logPath) { Remove-Item $logPath -Force }

# ---------------------------------------------------------------
# Launch InoProShop
# Set INOPRO_SKILL_DIR in the current process so child processes
# (InoProShop + IronPython scripts) can read it via os.environ.
# This lets generator_override.py locate env.json without counting
# parent directories (which differs from generator_runner.py's depth).
# ---------------------------------------------------------------
Write-Host "`n[2/4] Launching InoProShop..." -ForegroundColor Yellow
$env:INOPRO_SKILL_DIR = $INOPRO_SKILL_DIR
$inoProc = Start-Process -FilePath $INOPRO_EXE `
    -ArgumentList "--Profile=`"$INOPRO_PROFILE`"", "/runscript=`"$scriptPath`"" `
    -PassThru
Write-Host "      Launched (PID=$($inoProc.Id)), waiting for log..." -ForegroundColor Green

# Start dialog monitor as a separate powershell.exe process (not a Job).
# Using Start-Process -PassThru gives us a real PID we can Stop-Process later,
# guaranteeing the C# Win32 message loop is killed immediately on cleanup.
$monitorScript = Join-Path $toolsDir "dialog_monitor.ps1"
$dlgProc = Start-Process -FilePath "powershell.exe" `
    -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$monitorScript`"",
                  $inoProc.Id, "`"$logPath`"", "InoProShop", ($Timeout + 30) `
    -PassThru -WindowStyle Hidden
Write-Host "      Dialog monitor started (PID=$($dlgProc.Id))" -ForegroundColor Gray

# ---------------------------------------------------------------
# Tail log in real-time until done or timeout
# ---------------------------------------------------------------
Write-Host "`n[3/4] Live log:" -ForegroundColor Yellow
Write-Host "--------------------------------------" -ForegroundColor Gray

$lastLine = 0
$elapsed  = 0
$interval = 2
$done     = $false

$waited = 0
while (-not (Test-Path $logPath) -and $waited -lt 20) {
    Start-Sleep -Seconds 1
    $waited++
}
if (-not (Test-Path $logPath)) {
    Write-Host "[WARN] Log file not created after 20s - InoProShop may have failed to start" -ForegroundColor Yellow
}

while (-not $done -and $elapsed -lt $Timeout) {
    if (Test-Path $logPath) {
        $lines = Get-Content $logPath -Encoding UTF8 -ErrorAction SilentlyContinue
        if ($lines -and $lines.Count -gt $lastLine) {
            foreach ($line in $lines[$lastLine..($lines.Count - 1)]) {
                if ($line -match 'DIALOG DETECTED') {
                    Write-Host $line -ForegroundColor Magenta
                } elseif ($line -match 'ERROR' -and $line -notmatch '0 error') {
                    Write-Host $line -ForegroundColor Red
                } elseif ($line -match 'WARNING|WARN') {
                    Write-Host $line -ForegroundColor Yellow
                } elseif ($line -match 'SUCCESS|DONE|BUILD OK') {
                    Write-Host $line -ForegroundColor Green
                } else {
                    Write-Host $line -ForegroundColor White
                }
            }
            $lastLine = $lines.Count
            if ($lines[-1] -match '===\s+\S.*done\s+===|=== done ===|FATAL:') { $done = $true }
            if ($lines | Where-Object { $_ -match 'DIALOG DETECTED' }) { $done = $true }
        }
    }

    # InoProShop process exited - do one final log read before deciding
    if (-not $done -and $inoProc.HasExited) {
        Start-Sleep -Milliseconds 500   # give file system a moment to flush
        if (Test-Path $logPath) {
            $lines = Get-Content $logPath -Encoding UTF8 -ErrorAction SilentlyContinue
            if ($lines -and ($lines[-1] -match '===\s+\S.*done\s+===|=== done ===|FATAL:' -or ($lines | Where-Object { $_ -match 'DIALOG DETECTED' }))) {
                $done = $true   # normal finish, already wrote done marker
            }
        }
        if (-not $done) {
            Write-Host "`n[WARN] InoProShop exited unexpectedly (code=$($inoProc.ExitCode))" -ForegroundColor Yellow
            $done = $true
        }
    }

    if (-not $done) {
        Start-Sleep -Seconds $interval
        $elapsed += $interval
    }
}

if (-not $done) {
    Write-Host "`n[WARN] Timed out after ${Timeout}s, script may still be running" -ForegroundColor Yellow
}

# Stop dialog monitor: direct Stop-Process kills the C# message loop immediately.
# Wait up to 3s for graceful exit first (WatchPid-exit thread may have already fired).
if ($dlgProc -and -not $dlgProc.HasExited) {
    $dlgProc.WaitForExit(3000) | Out-Null
    if (-not $dlgProc.HasExited) {
        Stop-Process -Id $dlgProc.Id -Force -ErrorAction SilentlyContinue
    }
}


# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
Write-Host "`n--------------------------------------" -ForegroundColor Gray
Write-Host "[4/4] Summary:" -ForegroundColor Yellow

if (Test-Path $logPath) {
    $allLines = Get-Content $logPath -Encoding UTF8 -ErrorAction SilentlyContinue
 
    if ($allLines) {
        # Show dialog error if present
        $dlgLines = $allLines | Where-Object { $_ -match 'DIALOG DETECTED|Body\s*:' }
        if ($dlgLines) {
            Write-Host "`n  [!] InoProShop error dialog detected (script aborted):" -ForegroundColor Magenta
            foreach ($l in $dlgLines) { Write-Host "      $l" -ForegroundColor Magenta }
        }

        # Show build result
        $buildResult = $allLines | Where-Object { $_ -match 'BUILD SUCCESS|BUILD FAILED|BUILD OK|CHECK RESULT:|export_pou.py done' } | Select-Object -Last 1
        if ($buildResult) {
            if ($buildResult -match 'SUCCESS|BUILD OK|CHECK RESULT: OK|0 error') {
                Write-Host "  $buildResult" -ForegroundColor Green
            } else {
                Write-Host "  $buildResult" -ForegroundColor Red
            }
        }

        # Show project path
        $projLine = $allLines | Where-Object { $_ -match '\.project' } | Select-Object -Last 1
        if ($projLine) { Write-Host "  $projLine" -ForegroundColor Cyan }
    }
} else {
    Write-Host "  No log file found - check if InoProShop started correctly" -ForegroundColor Red
}

Write-Host ""
