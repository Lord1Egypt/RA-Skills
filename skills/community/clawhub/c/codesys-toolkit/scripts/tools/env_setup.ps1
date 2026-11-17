# env_setup.ps1
# InoProShop environment configuration - detect once, cache forever.
#
# Usage:
#   . "<skill>\scripts\tools\env_setup.ps1"          # load (auto-detects if needed)
#   . "<skill>\scripts\tools\env_setup.ps1" -Force   # force re-detect (after upgrade)
#
# After dot-sourcing, three global vars are ready:
#   $INOPRO_EXE        full path to InoProShop.exe
#   $INOPRO_PROFILE    profile name, e.g. InoProShop(V1.9.0.1)
#   $INOPRO_SKILL_DIR  full path to this skill's root folder
#
# Also writes $env:TEMP\codesys_skill_dir.txt so IronPython scripts
# can locate skill_dir without any hardcoded paths.
#
# Detection logic:
#   - Cache is considered VALID only when env.json exists AND cfg.exe points to a real file.
#   - If the file exists but exe path is invalid (e.g. copied from another machine),
#     detection runs automatically — no need for -Force.
#   - -Force skips the validity check and always re-detects.
#   - When writing a fresh env.json, existing business fields (template, patch_target,
#     patch_pous, patch_no_build, check_target) are preserved from the old file.

param([switch]$Force)

# scripts/tools/ -> scripts/ -> skill root
$toolsDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptsDir = Split-Path -Parent $toolsDir
$skillDir   = Split-Path -Parent $scriptsDir
$envFile    = Join-Path $skillDir "references\env.json"

# ---------------------------------------------------------------
# Helper: write mailbox for IronPython scripts
# ---------------------------------------------------------------
function Write-Mailbox($dir) {
    $mailbox = Join-Path $env:TEMP 'codesys_skill_dir.txt'
    [System.IO.File]::WriteAllText($mailbox, $dir, [System.Text.UTF8Encoding]::new($false))
}

# ---------------------------------------------------------------
# Determine whether cache is usable
# ---------------------------------------------------------------
$cacheValid = $false
$oldCfg     = $null

if ((Test-Path $envFile) -and (-not $Force)) {
    try {
        $raw    = [System.IO.File]::ReadAllText($envFile, [System.Text.UTF8Encoding]::new($false))
        $oldCfg = $raw | ConvertFrom-Json
        # Cache is valid only when exe field exists AND points to a real file on THIS machine
        if ($oldCfg.exe -and (Test-Path $oldCfg.exe)) {
            $cacheValid = $true
        } else {
            Write-Host "[env] Cache exists but exe path invalid or missing — re-detecting..." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[env] Failed to parse env.json — re-detecting..." -ForegroundColor Yellow
    }
}

# ---------------------------------------------------------------
# Load from cache if valid
# ---------------------------------------------------------------
if ($cacheValid) {
    $global:INOPRO_EXE       = $oldCfg.exe
    $global:INOPRO_PROFILE   = $oldCfg.profile
    $global:INOPRO_SKILL_DIR = $oldCfg.skill_dir
    Write-Host "[env] Loaded from cache: $envFile"
    Write-Host "[env] EXE      = $($global:INOPRO_EXE)"
    Write-Host "[env] Profile  = $($global:INOPRO_PROFILE)"
    Write-Host "[env] SkillDir = $($global:INOPRO_SKILL_DIR)"
    Write-Mailbox $global:INOPRO_SKILL_DIR
    return
}

# ---------------------------------------------------------------
# Detection (first run, -Force, or invalid cache)
# ---------------------------------------------------------------
Write-Host "[env] Detecting InoProShop environment..." -ForegroundColor Cyan

$drives = (Get-PSDrive -PSProvider FileSystem | Where-Object { Test-Path $_.Root }).Root

# 1. Find InoProShop.exe (exclude Repair/Tool variants)
$exe = $drives | ForEach-Object {
    cmd /c "dir /b /s `"${_}*InoProShop*.exe`" 2>nul"
} | Where-Object {
    $_ -match 'InoProShop\.exe$' -and $_ -notmatch 'Repair|Tool'
} | Select-Object -First 1

if (-not $exe) {
    Write-Error "[env] InoProShop.exe not found. Is InoProShop installed?"
    return
}
Write-Host "[env] EXE found: $exe"

# 2. Locate profile name from nearby Profiles folder
$exeDir     = Split-Path $exe
$codesysDir = Split-Path $exeDir     # Common -> CODESYS

$profileFile = Get-ChildItem "$codesysDir\Profiles" -Filter 'InoProShop*.profile' `
                 -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $profileFile) {
    $profileFile = Get-ChildItem "$(Split-Path $codesysDir)\Profiles" -Filter 'InoProShop*.profile' `
                     -ErrorAction SilentlyContinue | Select-Object -First 1
}
if (-not $profileFile) {
    $profileFile = Get-ChildItem $exeDir -Filter 'InoProShop*.profile' `
                     -ErrorAction SilentlyContinue | Select-Object -First 1
}
if (-not $profileFile) {
    Write-Error "[env] InoProShop*.profile not found near $exeDir"
    return
}
$profileName = $profileFile.BaseName
Write-Host "[env] Profile found: $profileName"
Write-Host "[env] SkillDir: $skillDir"

# ---------------------------------------------------------------
# Write env.json — merge with existing business fields
# ---------------------------------------------------------------
# Start from old config (preserves template, patch_target, patch_pous,
# patch_no_build, check_target, etc.) or create a fresh base.
$newCfg = [ordered]@{
    exe             = $exe
    profile         = $profileName
    skill_dir       = $skillDir
    template        = ""
    extra_libraries = ""
    generated       = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
    patch_target    = ""
    patch_pous      = ""
    patch_no_build  = ""
    check_target    = ""
}

if ($null -ne $oldCfg) {
    # Preserve every business field that already has a value in the old config
    foreach ($key in @('template','extra_libraries','patch_target','patch_pous','patch_no_build','check_target','workspace_dir','active_project')) {
        $oldVal = $oldCfg.$key
        if ($null -ne $oldVal -and "$oldVal" -ne '') {
            $newCfg[$key] = "$oldVal"
        }
    }
}

# Write UTF-8 WITHOUT BOM so IronPython 2.7 json.load() can read it
$jsonText = $newCfg | ConvertTo-Json -Depth 2
[System.IO.File]::WriteAllText($envFile, $jsonText, [System.Text.UTF8Encoding]::new($false))
Write-Host "[env] Saved to: $envFile"

# ---------------------------------------------------------------
# Export as global vars + write mailbox
# ---------------------------------------------------------------
$global:INOPRO_EXE       = $exe
$global:INOPRO_PROFILE   = $profileName
$global:INOPRO_SKILL_DIR = $skillDir

Write-Mailbox $skillDir
Write-Host "[env] Mailbox written: $(Join-Path $env:TEMP 'codesys_skill_dir.txt')"
