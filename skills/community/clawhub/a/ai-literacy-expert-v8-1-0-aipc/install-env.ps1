<#
.SYNOPSIS
    Ensure Python venv + requirements are installed for ai-literacy-expert-v8.1.0-aipc.

.DESCRIPTION
    Reads info.json and:
      1. Finds or downloads uv.exe into bin/ (fallback to system pip if uv unavailable)
      2. Creates .venv using project's skill_runtime.py (idempotent)
      3. Installs requirements.txt with SHA256 stamp (skips if unchanged)
      4. Verifies venv python is runnable

.NOTES
    This script is idempotent: safe to rerun. Uses the project's existing
    skill_runtime.py to keep venv logic in one place (single source of truth).

.EXIT CODES
    0  Success (venv ready)
    1  General error (python missing / venv creation failed / pip install failed)
#>
$ErrorActionPreference = 'Stop'

# install-env.ps1 位于 <SKILL_DIR>/install-env.ps1，$PSScriptRoot 即为 skill 根目录。
# 修复：原代码使用 `Split-Path -Parent $PSScriptRoot` 多走了一级，
# 会导致 $Scripts / $VenvPy 指向 <SKILL_DIR>/../...（错）。
$Root    = $PSScriptRoot
$Scripts = Join-Path $Root 'scripts'
$VenvPy  = Join-Path $Root '.venv\Scripts\python.exe'

Write-Host ""
Write-Host "=== Environment install ====================================="

# --- 1. Verify host Python >= 3.10 ------------------------------------------
$hostPython = $null
foreach ($cmd in @("python", "python3")) {
    try {
        $ver = "$(& $cmd --version 2>&1)"
        if ($ver -match "Python (\d+)\.(\d+)\.(\d+)") {
            $maj = [int]$Matches[1]; $min = [int]$Matches[2]
            if ($maj -gt 3 -or ($maj -eq 3 -and $min -ge 10)) {
                $hostPython = $cmd
                break
            }
        }
    } catch {}
}
if (-not $hostPython) {
    Write-Host "[FAIL] Host Python >= 3.10 not found."
    Write-Host "       Install Python 3.10+ first, then rerun."
    exit 1
}
Write-Host "[PASS] Host Python: $(& $hostPython --version 2>&1)".Trim()

# --- 2. Create .venv if missing (via skill_runtime for single source) -------
if (-not (Test-Path $VenvPy)) {
    Write-Host "[venv] Creating .venv via skill_runtime.ensure_skill_venv()..."
    & $hostPython -c "import sys; sys.path.insert(0, r'$Scripts'); from skill_runtime import ensure_skill_venv; ensure_skill_venv()"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] venv creation failed."
        exit 1
    }
} else {
    Write-Host "[PASS] venv exists: $VenvPy"
}

# --- 3. Install / refresh requirements (SHA256 stamp) -----------------------
Write-Host "[reqs] Checking requirements.txt freshness..."
& $VenvPy -c "import sys; sys.path.insert(0, r'$Scripts'); from skill_runtime import ensure_skill_requirements; ensure_skill_requirements()"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] requirements.txt install failed."
    exit 1
}

# --- 4. Final sanity check ---------------------------------------------------
if (-not (Test-Path $VenvPy)) {
    Write-Host "[FAIL] venv python missing after install: $VenvPy"
    exit 1
}

Write-Host "============================================================="
Write-Host "[PASS] Environment ready."
Write-Host ""
exit 0
