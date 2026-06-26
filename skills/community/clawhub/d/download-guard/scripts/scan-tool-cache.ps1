# scan-tool-cache.ps1
# Scans package manager cache/install locations and reports C-drive usage.

param(
    [switch]$Silent
)

$results = @()

function Get-FolderSizeMB {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return 0 }
    try {
        $size = (Get-ChildItem $Path -Recurse -Force -ErrorAction SilentlyContinue |
                 Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($size) { return [math]::Round($size / 1MB, 1) } else { return 0 }
    } catch { return 0 }
}

function Get-CacheStatus {
    param([string]$Label, [string]$Path)
    if (-not $Path) { return }
    $Path = $Path.Trim()
    $onC = $Path -match '^[Cc]:\\'
    $exists = Test-Path $Path
    $sizeMB = if ($exists -and $onC) { Get-FolderSizeMB $Path } else { 0 }
    $status = if ($onC) { "WARN-C-DRIVE" } else { "OK" }
    [PSCustomObject]@{
        Tool     = $Label
        Path     = $Path
        OnCDrive = $onC
        Exists   = $exists
        SizeMB   = $sizeMB
        Status   = $status
    }
}

# --- npm ---
$npmPrefix = (npm config get prefix 2>$null) -replace "`n",""
$npmCache  = (npm config get cache  2>$null) -replace "`n",""
if ($npmPrefix) { $results += Get-CacheStatus "npm prefix" $npmPrefix }
if ($npmCache)  { $results += Get-CacheStatus "npm cache"  $npmCache }

# --- pip ---
$pipRaw = pip cache dir 2>$null
$pipCache = ($pipRaw | Where-Object { $_ -match '^[A-Za-z]:\\' } | Select-Object -First 1)
if (-not $pipCache) { $pipCache = $env:PIP_CACHE_DIR }
if ($pipCache) { $results += Get-CacheStatus "pip cache" $pipCache }

# --- pip --user site-packages (v5.4: often on C: drive) ---
$pipUserBase = (python -m site --user-site 2>$null) -replace "`n",""
if ($pipUserBase -and $pipUserBase -match '^[A-Za-z]:\\') {
    $results += Get-CacheStatus "pip --user" $pipUserBase
}

# --- yarn ---
try {
    $yarnCache = (yarn cache dir 2>$null) -replace "`n",""
    if ($yarnCache) { $results += Get-CacheStatus "yarn cache" $yarnCache }
} catch {}

# --- conda ---
try {
    $condaInfo = conda info --json 2>$null | ConvertFrom-Json
    if ($condaInfo.pkgs_dirs) {
        foreach ($d in $condaInfo.pkgs_dirs) {
            $results += Get-CacheStatus "conda pkgs" $d
        }
    }
} catch {}

# --- pnpm (v5.4) ---
try {
    $pnpmStore = (pnpm store path 2>$null) -replace "`n",""
    if ($pnpmStore) { $results += Get-CacheStatus "pnpm store" $pnpmStore }
} catch {}

# --- bun (v5.4) ---
try {
    $bunInstall = "$env:USERPROFILE\.bun"
    if (Test-Path $bunInstall) {
        $results += Get-CacheStatus "bun install" $bunInstall
    }
} catch {}

# --- cargo / Rust (v5.4) ---
$cargoHome = if ($env:CARGO_HOME) { $env:CARGO_HOME } else { "$env:USERPROFILE\.cargo" }
if (Test-Path $cargoHome) {
    $results += Get-CacheStatus "cargo home" $cargoHome
}
$cargoRegistry = if ($env:CARGO_HOME) { "$env:CARGO_HOME\registry" } else { "$env:USERPROFILE\.cargo\registry" }
if (Test-Path $cargoRegistry) {
    $results += Get-CacheStatus "cargo cache" $cargoRegistry
}

# --- Go (v5.4) ---
$goPath = if ($env:GOPATH) { $env:GOPATH } else { "$env:USERPROFILE\go" }
if (Test-Path $goPath) {
    $goPkgCache = Join-Path $goPath "pkg"
    if (Test-Path $goPkgCache) {
        $results += Get-CacheStatus "go pkg cache" $goPkgCache
    }
}

# --- uv (v5.4: Python fast installer) ---
try {
    $uvCacheDir = (uv cache dir 2>$null) -replace "`n",""
    if ($uvCacheDir) { $results += Get-CacheStatus "uv cache" $uvCacheDir }
} catch {}

# --- nvm for Windows (v5.4: node version manager) ---
$nvmHome = $env:NVM_HOME
if (-not $nvmHome) {
    $nvmHome = "$env:APPDATA\nvm"
}
if (Test-Path $nvmHome) {
    $results += Get-CacheStatus "nvm home" $nvmHome
}

# --- HuggingFace cache (v5.4) ---
$hfCache = if ($env:HF_HOME) { $env:HF_HOME } else { "$env:USERPROFILE\.cache\huggingface" }
if (Test-Path $hfCache) {
    $results += Get-CacheStatus "HF cache" $hfCache
}

# --- Ollama models (v5.4) ---
$ollamaModels = if ($env:OLLAMA_MODELS) { $env:OLLAMA_MODELS } else { "$env:USERPROFILE\.ollama\models" }
if (Test-Path $ollamaModels) {
    $results += Get-CacheStatus "ollama models" $ollamaModels
}

# C drive space
$cDisk   = Get-PSDrive C -ErrorAction SilentlyContinue
$cFreeGB = if ($cDisk) { [math]::Round($cDisk.Free / 1GB, 1) } else { 0 }
$cUsedGB = if ($cDisk) { [math]::Round($cDisk.Used / 1GB, 1) } else { 0 }

# Header
Write-Output "=============================================="
Write-Output "  Download Guard v5  |  Tool Cache Scan"
Write-Output "=============================================="
Write-Output ""

# C drive status line
$cStatusLabel = if ($cFreeGB -lt 5) { "[WARN] Low on space" } elseif ($cFreeGB -lt 15) { "[CAUTION]" } else { "[OK]" }
Write-Output "  C Drive: Used ${cUsedGB}GB / Free ${cFreeGB}GB  $cStatusLabel"
Write-Output ""
Write-Output "  Tool Cache Locations:"

foreach ($r in $results) {
    $flag    = if ($r.OnCDrive -eq $true) { "  <- [WARN] C: drive" } else { "  [OK]" }
    $sizeStr = if ($r.OnCDrive -eq $true -and $r.SizeMB -gt 0) { " ($($r.SizeMB) MB)" } else { "" }
    Write-Output ("    " + $r.Tool.PadRight(14) + ": " + $r.Path + $sizeStr + $flag)
}

# Summary
$warnItems   = @($results | Where-Object { $_.OnCDrive -eq $true })
$warnCount   = $warnItems.Count
$totalWarnMB = ($warnItems | Measure-Object -Property SizeMB -Sum).Sum

Write-Output ""
if ($warnCount -gt 0) {
    $mbStr = if ($totalWarnMB) { [math]::Round($totalWarnMB, 1) } else { "unknown" }
    Write-Output "[WARN] $warnCount tool cache(s) on C: drive, total ~${mbStr} MB:"
    foreach ($w in $warnItems) {
        $s = if ($w.SizeMB -gt 0) { " ($($w.SizeMB) MB)" } else { "" }
        Write-Output "       - $($w.Tool): $($w.Path)$s"
    }
    Write-Output ""
    Write-Output "  --> Tell the agent: 'Migrate caches' to fix automatically."
} else {
    Write-Output "[OK] All tool caches are off C: drive. System is healthy."
}
Write-Output ""
