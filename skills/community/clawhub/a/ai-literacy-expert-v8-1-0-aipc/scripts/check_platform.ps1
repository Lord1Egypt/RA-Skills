<#
.SYNOPSIS
    Preflight environment check script for ai-literacy-expert-v7.3 edge-cloud-pipeline (hardware + Python)

.DESCRIPTION
    Phase 1 - Hardware check (must satisfy either condition):
      Condition A - Intel whitelisted dGPU: Arc A770 (16GB) / Arc B580 (12GB), CPU unrestricted
      Condition B - Intel iGPU platform: MTL / LNL / ARL / PTL CPU + Intel iGPU + RAM > 16 GB

    Phase 2 - Python >= 3.10 check:
      Only checks whether host Python is available. No system-level auto-install.
      Project-local .venv, requirements, and edge-cloud-pipeline dependencies are
      handled in Phase 1: Prepare.

    Both phases pass -> exit 0; any failure -> exit 1

.NOTES
    To extend the dGPU whitelist, append model IDs to the $DGPU_WHITELIST array.
#>

# ============================================================
# Configuration
# ============================================================

# dGPU whitelist: use model IDs only (e.g. "B580"), not "Arc B580"
# Actual GPU names include "(TM)", e.g. "Intel(R) Arc(TM) B580 Graphics";
# exact full-name matching can be brittle.
$DGPU_WHITELIST = @("A770", "B580", "B390", "B50", "B60")
$dGpuPattern    = $DGPU_WHITELIST -join "|"

$PYTHON_MIN_MAJOR = 3
$PYTHON_MIN_MINOR = 10

# ============================================================
# Utility functions
# ============================================================

function Find-PythonMin {
    <#
    .SYNOPSIS Find Python >= $PYTHON_MIN_MAJOR.$PYTHON_MIN_MINOR in PATH. Returns a runnable command string, or $null if not found.
    #>
    foreach ($cmd in @("python", "python3")) {
        try {
            $ver = "$(& $cmd --version 2>&1)"
            if ($ver -match "Python (\d+)\.(\d+)\.(\d+)") {
                $maj = [int]$Matches[1]; $min = [int]$Matches[2]
                if ($maj -gt $PYTHON_MIN_MAJOR -or ($maj -eq $PYTHON_MIN_MAJOR -and $min -ge $PYTHON_MIN_MINOR)) {
                    return $cmd
                }
            }
        } catch {}
    }
    # Windows Python Launcher path
    foreach ($pyver in @("3.13","3.12","3.11","3.10")) {
        try {
            $ver = "$(& py -$pyver --version 2>&1)"
            if ($ver -match "Python (\d+)\.(\d+)\.(\d+)") {
                $maj = [int]$Matches[1]; $min = [int]$Matches[2]
                if ($maj -gt $PYTHON_MIN_MAJOR -or ($maj -eq $PYTHON_MIN_MAJOR -and $min -ge $PYTHON_MIN_MINOR)) {
                    return "py -$pyver"
                }
            }
        } catch {}
    }
    return $null
}

function Get-PythonVersion([string]$cmd) {
    try {
        if ($cmd.StartsWith("py -")) {
            $parts = $cmd.Split(" ", 2)
            $pyArg = $parts[1]
            return "$(& py $pyArg --version 2>&1)".Trim()
        }
        return "$(& $cmd --version 2>&1)".Trim()
    } catch { return "unknown" }
}

# ============================================================
# Phase 1: Hardware check
# ============================================================
Write-Host ""
Write-Host "=== Phase 1: Intel hardware platform check =================="

$cpu        = (Get-WmiObject Win32_Processor).Name
$allGpus    = Get-WmiObject Win32_VideoController
$totalMemGB = [math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)

# dGPU: name matches whitelist
$dgpu = $allGpus |
    Where-Object { $_.Name -match "Intel" -and $_.Name -match $dGpuPattern } |
    Select-Object -First 1

# iGPU: Intel integrated GPU, excluding whitelisted dGPU models
$igpu = $allGpus |
    Where-Object {
        $_.Name -match "Intel" -and
        $_.Name -match "UHD|Iris|Xe|Arc" -and
        $_.Name -notmatch $dGpuPattern
    } |
    Select-Object -First 1

# CPU platform code (WMI name includes (TM), e.g. "Intel(R) Core(TM) Ultra 7 155H")
$platform = $null
if     ($cpu -match "Ultra \d+\s+1\d{2}")                                            { $platform = "MTL" }
elseif ($cpu -match "Ultra \d+\s+2\d{2}V")                                           { $platform = "LNL" }
elseif ($cpu -match "Ultra \d+\s+2\d{2}" -and $cpu -notmatch "Ultra \d+\s+2\d{2}V") { $platform = "ARL" }
elseif ($cpu -match "Ultra \d+\s+3\d{2}")                                            { $platform = "PTL" }

$hwPass = $false

if ($dgpu) {
    # Condition A: whitelisted dGPU found, CPU unrestricted
    Write-Host "[PASS] Condition A - Intel dGPU (whitelist): $($dgpu.Name)"
    Write-Host "[INFO] dGPU route: skip CPU platform and memory checks"
    $hwPass = $true
} else {
    # Condition B: MTL/LNL/ARL/PTL + iGPU + RAM > 16 GB
    Write-Host "[INFO] Whitelisted dGPU not found. Checking Condition B (iGPU platform)..."
    $condB = $true

    if ($platform) {
        Write-Host "[PASS] CPU platform: $platform ($cpu)"
    } else {
        Write-Host "[FAIL] Unsupported CPU: $cpu"
        Write-Host "       Requires Intel MTL/LNL/ARL/PTL, or a whitelisted dGPU ($($DGPU_WHITELIST -join ' / '))"
        $condB = $false
    }
    if ($igpu) {
        Write-Host "[PASS] Intel iGPU: $($igpu.Name)"
    } else {
        Write-Host "[FAIL] Intel iGPU not detected"
        $condB = $false
    }
    if ($totalMemGB -gt 16) {
        Write-Host "[PASS] RAM: ${totalMemGB} GB"
    } else {
        Write-Host "[FAIL] Insufficient RAM: ${totalMemGB} GB (required: > 16 GB)"
        $condB = $false
    }
    $hwPass = $condB
}

if (-not $hwPass) {
    Write-Host "============================================================"
    Write-Host ""
    Write-Host "[FAIL] Hardware check failed. Stop before running subsequent steps."
    Write-Host ""
    Write-Host "   Supported Condition A: Intel whitelisted dGPU ($($DGPU_WHITELIST -join ' / '))"
    Write-Host "   Supported Condition B: Intel MTL/LNL/ARL/PTL CPU + Intel iGPU + RAM > 16 GB"
    exit 1
}

Write-Host "============================================================"
Write-Host "[PASS] Phase 1 passed"

# ============================================================
# Phase 2: Python >= 3.10 check
# ============================================================
Write-Host ""
Write-Host "=== Phase 2: Python >= 3.10 environment check ==============="

$pythonCmd = Find-PythonMin

if ($pythonCmd) {
    $verStr = Get-PythonVersion $pythonCmd
    Write-Host "[PASS] Python >= $PYTHON_MIN_MAJOR.${PYTHON_MIN_MINOR}: $verStr (command: $pythonCmd)"
} else {
    Write-Host "[FAIL] Python >= $PYTHON_MIN_MAJOR.$PYTHON_MIN_MINOR not found."
    Write-Host ""
    Write-Host "   Please install Python 3.10+ first, then rerun Phase 1: Prepare."
    Write-Host "   Phase 1 will create <SKILL_DIR>\\.venv and install edge-cloud-pipeline requirements."
    exit 1
}

Write-Host "============================================================"
Write-Host ""
Write-Host "[PASS] All checks passed (hardware + host Python). You can proceed with Phase 1: Prepare."
exit 0
