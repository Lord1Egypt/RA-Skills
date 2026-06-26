param(
    [string]$TargetRoot = ""
)

# Config: read config.md
$skillDir   = "$env:USERPROFILE\.workbuddy\skills\download-guard"
$configPath = "$skillDir\config.md"

if (-not $TargetRoot -and (Test-Path $configPath)) {
    $content = Get-Content $configPath -Raw
    if ($content -match "DOWNLOAD_ROOT:\s*(.+)") {
        $TargetRoot = $Matches[1].Trim()
    }
}
if (-not $TargetRoot) {
    Write-Output "[ERROR] DOWNLOAD_ROOT is not configured."
    Write-Output "        Please tell the Agent your preferred download directory, or set DOWNLOAD_ROOT in config.md."
    Write-Output "        Example: DOWNLOAD_ROOT: D:\AI-Downloads"
    exit 1
}

$drive = ($TargetRoot -replace '\\.*', '').TrimEnd(':')

Write-Output "[MIGRATE] Target root: $TargetRoot"
Write-Output "[MIGRATE] Target drive: ${drive}:"
Write-Output ""

$migrated = 0
$skipped  = 0

function Migrate-Tool {
    param([string]$Label, [string]$NewPath, [scriptblock]$Apply)
    if (-not (Test-Path (Split-Path $NewPath -Parent))) {
        New-Item -ItemType Directory -Path (Split-Path $NewPath -Parent) -Force | Out-Null
    }
    if (-not (Test-Path $NewPath)) {
        New-Item -ItemType Directory -Path $NewPath -Force | Out-Null
    }
    try {
        & $Apply
        Write-Output "[OK] $Label -> $NewPath"
        return $true
    } catch {
        Write-Output "[FAIL] $Label : $($_.Exception.Message)"
        return $false
    }
}

# npm prefix
$npmCurrentPrefix = (npm config get prefix 2>$null) -replace "`n",""
if ($npmCurrentPrefix -match '^C:\\') {
    $newPrefix = "$TargetRoot\npm-global"
    $newCache  = "$TargetRoot\npm-cache"
    $ok = Migrate-Tool "npm prefix" $newPrefix {
        npm config set prefix $newPrefix
    }
    if ($ok) {
        Migrate-Tool "npm cache" $newCache {
            npm config set cache $newCache
        }
        Write-Output "  [ACTION NEEDED] Add to PATH: $newPrefix"
        $migrated++
    }
} else {
    Write-Output "[SKIP] npm prefix already on non-C drive: $npmCurrentPrefix"
    $skipped++
}

# pip cache
$pipRaw = pip cache dir 2>$null
$pipCurrentCache = ($pipRaw | Where-Object { $_ -match '^[A-Za-z]:\\' } | Select-Object -First 1)
if (-not $pipCurrentCache) { $pipCurrentCache = $env:PIP_CACHE_DIR }
if ($pipCurrentCache -match '^[Cc]:\\') {
    $newPipCache = "$TargetRoot\pip-cache"
    Migrate-Tool "pip cache" $newPipCache {
        pip config set global.cache-dir $newPipCache
    }
    [Environment]::SetEnvironmentVariable("PIP_CACHE_DIR", $newPipCache, "User")
    $migrated++
} else {
    Write-Output "[SKIP] pip cache already on non-C drive: $pipCurrentCache"
    $skipped++
}

# yarn cache
try {
    $yarnCurrentCache = (yarn cache dir 2>$null) -replace "`n",""
    if ($yarnCurrentCache -match '^C:\\') {
        $newYarnCache = "$TargetRoot\yarn-cache"
        Migrate-Tool "yarn cache" $newYarnCache {
            yarn config set cache-folder $newYarnCache
        }
        $migrated++
    } else {
        Write-Output "[SKIP] yarn cache already on non-C drive"
        $skipped++
    }
} catch {}

# pnpm store (v5.4)
try {
    $pnpmStore = (pnpm store path 2>$null) -replace "`n",""
    if ($pnpmStore -match '^[Cc]:\\') {
        $newPnpmStore = "$TargetRoot\pnpm-store"
        Migrate-Tool "pnpm store" $newPnpmStore {
            pnpm config set store-dir $newPnpmStore
        }
        $migrated++
    } else {
        if ($pnpmStore) { Write-Output "[SKIP] pnpm store already on non-C drive" }
        $skipped++
    }
} catch {}

# uv cache (v5.4)
try {
    $uvCacheDir = (uv cache dir 2>$null) -replace "`n",""
    if ($uvCacheDir -match '^[Cc]:\\') {
        $newUvCache = "$TargetRoot\uv-cache"
        Migrate-Tool "uv cache" $newUvCache {
            uv cache dir $newUvCache
        }
        [Environment]::SetEnvironmentVariable("UV_CACHE_DIR", $newUvCache, "User")
        $migrated++
    } else {
        if ($uvCacheDir) { Write-Output "[SKIP] uv cache already on non-C drive" }
        $skipped++
    }
} catch {}

# cargo home (v5.4 - env var based, warn only)
$cargoHome = if ($env:CARGO_HOME) { $env:CARGO_HOME } else { "$env:USERPROFILE\.cargo" }
if ($cargoHome -match '^[Cc]:\\') {
    Write-Output "[INFO] cargo home is on C: ($cargoHome)"
    Write-Output "       To migrate: set CARGO_HOME environment variable to a non-C: path and add its bin to PATH"
    Write-Output "       Example: CARGO_HOME=$TargetRoot\cargo"
    $skipped++
}

# go path (v5.4 - env var based, warn only)
$goPath = if ($env:GOPATH) { $env:GOPATH } else { "$env:USERPROFILE\go" }
if ($goPath -match '^[Cc]:\\') {
    Write-Output "[INFO] GOPATH is on C: ($goPath)"
    Write-Output "       To migrate: set GOPATH environment variable to a non-C: path and add its bin to PATH"
    Write-Output "       Example: GOPATH=$TargetRoot\go"
    $skipped++
}

Write-Output ""
Write-Output "[SUMMARY] Migrated: $migrated tool(s), Skipped: $skipped (already OK)"
if ($migrated -gt 0) {
    Write-Output "[NOTE] Changes take effect for new installs. Existing cache on C: is not deleted."
    Write-Output "       To free C: space, manually delete old cache after verifying the new location works."
}
