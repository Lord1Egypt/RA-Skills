# camscanner-cli upgrade script — checks for new versions and upgrades CLI + Skill files.
# Run by AI Agent at the start of each session. Safe to run repeatedly.
#
# Usage:
#   powershell scripts/upgrade.ps1
#   powershell scripts/upgrade.ps1 -Rollback
#
# Behavior:
#   - If no update needed: exits silently (exit 0)
#   - If network fails: exits silently (exit 0), does not block usage
#   - If upgrade fails: auto-rollback, then exit 1
#   - If lock conflict: exits silently (exit 0)

param(
    [switch]$Rollback
)

$ErrorActionPreference = "Stop"

$CDN_BASE = if ($env:CAMSCANNER_CLI_CDN) { $env:CAMSCANNER_CLI_CDN } else { "https://data.camscanner.com/camscanner-cli" }

# ── Locate paths ────────────────────────────────────────────────────────────

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$SKILL_DIR = Split-Path -Parent $SCRIPT_DIR
$TMP_DIR = Join-Path (Split-Path -Parent $SKILL_DIR) "camscanner-temp"
$BACKUP_DIR = Join-Path $TMP_DIR "backup"
$LOCK_DIR = Join-Path $TMP_DIR "upgrade.lock.d"
$CLI_PATH = $null

# ── Helpers ─────────────────────────────────────────────────────────────────

function Say($msg) { Write-Host "  $msg" }
function Warn($msg) { Write-Warning "  $msg" }
function Err($msg) { Write-Error "  $msg" }

function Get-LocalVersion {
    if ($CLI_PATH -and (Test-Path $CLI_PATH)) {
        $output = & $CLI_PATH --version 2>$null
        if ($output -match '(\d+\.\d+\.\d+)') {
            return $Matches[1]
        }
    }
    return $null
}

function Get-SkillVersion {
    $skillMd = Join-Path $SKILL_DIR "SKILL.md"
    if (Test-Path $skillMd) {
        $content = Get-Content $skillMd -Raw
        if ($content -match 'version:\s*(\d+\.\d+\.\d+)') {
            return $Matches[1]
        }
    }
    return $null
}

function Get-RemoteVersion {
    try {
        $url = "$CDN_BASE/latest-version.txt"
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
        $text = $response.Content.Trim()
        if ($text -match '(\d+\.\d+\.\d+)') {
            return $Matches[1]
        }
    } catch {
        return $null
    }
    return $null
}

function Compare-Versions($v1, $v2) {
    $parts1 = $v1.Split('.') | ForEach-Object { [int]$_ }
    $parts2 = $v2.Split('.') | ForEach-Object { [int]$_ }
    for ($i = 0; $i -lt 3; $i++) {
        $a = if ($i -lt $parts1.Count) { $parts1[$i] } else { 0 }
        $b = if ($i -lt $parts2.Count) { $parts2[$i] } else { 0 }
        if ($a -gt $b) { return 1 }
        if ($a -lt $b) { return -1 }
    }
    return 0
}

function Download-File($url, $dest) {
    try {
        Invoke-WebRequest -Uri $url -OutFile $dest -TimeoutSec 120 -UseBasicParsing -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Get-FileHash256($filePath) {
    $hash = Get-FileHash -Path $filePath -Algorithm SHA256
    return $hash.Hash.ToLower()
}

# ── Lock management ─────────────────────────────────────────────────────────

function Acquire-Lock {
    if (-not (Test-Path (Split-Path -Parent $LOCK_DIR))) {
        New-Item -ItemType Directory -Path (Split-Path -Parent $LOCK_DIR) -Force | Out-Null
    }
    try {
        New-Item -ItemType Directory -Path $LOCK_DIR -ErrorAction Stop | Out-Null
    } catch {
        # Check if lock is stale
        $pidFile = Join-Path $LOCK_DIR "pid"
        if (Test-Path $pidFile) {
            $lockPid = Get-Content $pidFile -ErrorAction SilentlyContinue
            if ($lockPid) {
                $process = Get-Process -Id ([int]$lockPid) -ErrorAction SilentlyContinue
                if ($process) {
                    return $false
                }
            }
            Remove-Item -Path $LOCK_DIR -Recurse -Force -ErrorAction SilentlyContinue
            try {
                New-Item -ItemType Directory -Path $LOCK_DIR -ErrorAction Stop | Out-Null
            } catch {
                return $false
            }
        } else {
            return $false
        }
    }
    $PID | Out-File -FilePath (Join-Path $LOCK_DIR "pid") -NoNewline
    return $true
}

function Release-Lock {
    if (Test-Path $LOCK_DIR) {
        Remove-Item -Path $LOCK_DIR -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# ── Backup & Rollback ───────────────────────────────────────────────────────

function Backup-Current($currentVersion) {
    if (-not (Test-Path $BACKUP_DIR)) {
        New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
    }
    if ($CLI_PATH -and (Test-Path $CLI_PATH)) {
        Copy-Item $CLI_PATH (Join-Path $BACKUP_DIR "camscanner-cli.exe.bak") -Force
    }
    # Backup Skill files as zip
    $backupZip = Join-Path $BACKUP_DIR "skill-${currentVersion}.zip"
    $filesToBackup = @()
    $skillMd = Join-Path $SKILL_DIR "SKILL.md"
    if (Test-Path $skillMd) { $filesToBackup += $skillMd }
    $refsDir = Join-Path $SKILL_DIR "references"
    $scriptsDir = Join-Path $SKILL_DIR "scripts"
    if (Test-Path $backupZip) { Remove-Item $backupZip -Force }
    try {
        Compress-Archive -Path @($skillMd, $refsDir, $scriptsDir) -DestinationPath $backupZip -Force -ErrorAction Stop
    } catch {
        Warn "Backup compression failed, continuing anyway."
    }
    $currentVersion | Out-File -FilePath (Join-Path $BACKUP_DIR "previous-version.txt") -NoNewline
}

function Invoke-Rollback($prevVersion) {
    Warn "Upgrade failed, rolling back to v${prevVersion}..."
    $bakCli = Join-Path $BACKUP_DIR "camscanner-cli.exe.bak"
    if ((Test-Path $bakCli) -and $CLI_PATH) {
        Copy-Item $bakCli $CLI_PATH -Force
    }
    $bakSkill = Join-Path $BACKUP_DIR "skill-${prevVersion}.zip"
    if (Test-Path $bakSkill) {
        Expand-Archive -Path $bakSkill -DestinationPath $SKILL_DIR -Force -ErrorAction SilentlyContinue
    }
    Err "Rolled back to v${prevVersion}"
}

function Do-Rollback {
    $prevFile = Join-Path $BACKUP_DIR "previous-version.txt"
    if (-not (Test-Path $prevFile)) {
        Err "No backup found, cannot rollback."
        exit 1
    }
    $prevVersion = (Get-Content $prevFile).Trim()
    Invoke-Rollback $prevVersion
    Say "Rollback to v${prevVersion} complete."
    exit 0
}

# ── Cleanup ─────────────────────────────────────────────────────────────────

function Invoke-Cleanup {
    Get-ChildItem -Path $TMP_DIR -Filter "camscanner-cli-*" -ErrorAction SilentlyContinue | Remove-Item -Force
    Get-ChildItem -Path $TMP_DIR -Filter "camscanner-skill-*" -ErrorAction SilentlyContinue | Remove-Item -Force
    $checksums = Join-Path $TMP_DIR "checksums.txt"
    if (Test-Path $checksums) { Remove-Item $checksums -Force }
    $skillExtract = Join-Path $TMP_DIR "skill"
    if (Test-Path $skillExtract) { Remove-Item $skillExtract -Recurse -Force }
    Release-Lock
}

# ── Main ────────────────────────────────────────────────────────────────────

function Main {
    if ($Rollback) {
        Do-Rollback
    }

    # Find CLI
    $cliCmd = Get-Command "camscanner-cli" -ErrorAction SilentlyContinue
    if (-not $cliCmd) {
        # PATH may not include the install directory in this session;
        # try the default install location directly.
        $defaultDir = Join-Path $env:LOCALAPPDATA "camscanner-cli"
        $defaultExe = Join-Path $defaultDir "camscanner-cli.exe"
        if (Test-Path $defaultExe) {
            $cliCmd = Get-Item $defaultExe
        } else {
            exit 0
        }
    }
    $script:CLI_PATH = if ($cliCmd.Source) { $cliCmd.Source } else { $cliCmd.FullName }

    # Get versions
    $cliVersion = Get-LocalVersion
    if (-not $cliVersion) {
        exit 0
    }
    $skillVersion = Get-SkillVersion

    # Take the lower of CLI and Skill versions
    if ($skillVersion -and (Compare-Versions $cliVersion $skillVersion) -gt 0) {
        $localVersion = $skillVersion
    } else {
        $localVersion = $cliVersion
    }

    $remoteVersion = Get-RemoteVersion
    if (-not $remoteVersion) {
        exit 0
    }

    # Compare versions
    if ((Compare-Versions $remoteVersion $localVersion) -le 0) {
        exit 0
    }

    # Acquire lock
    if (-not (Acquire-Lock)) {
        exit 0
    }

    try {
        Say "Update available: v${localVersion} -> v${remoteVersion}"

        # Prepare temp directory
        if (-not (Test-Path $TMP_DIR)) {
            New-Item -ItemType Directory -Path $TMP_DIR -Force | Out-Null
        }

        # Download CLI binary
        $arch = if ([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture -eq "Arm64") { "arm64" } else { "amd64" }
        $binSuffix = "camscanner-cli-windows-${arch}.exe"
        # CLI subpath — patched at build time for each target
        $cliSubpath = "clawhub/"

        $binUrl = "${CDN_BASE}/releases/v${remoteVersion}/${cliSubpath}${binSuffix}"

        Say "Downloading CLI binary..."
        $binDest = Join-Path $TMP_DIR $binSuffix
        if (-not (Download-File $binUrl $binDest)) {
            Warn "Download CLI failed, skipping upgrade."
            exit 0
        }

        # Download Skill ZIP
        $skillZip = "camscanner-skill-clawhub-v${remoteVersion}.zip"
        $skillUrl = "${CDN_BASE}/releases/v${remoteVersion}/${skillZip}"
        $skillDest = Join-Path $TMP_DIR $skillZip

        Say "Downloading Skill package..."
        if (-not (Download-File $skillUrl $skillDest)) {
            Warn "Download Skill ZIP failed, skipping upgrade."
            exit 0
        }

        # Download and verify checksums (mandatory — abort if unavailable)
        $checksumsUrl = "${CDN_BASE}/releases/v${remoteVersion}/${cliSubpath}checksums.txt"
        $checksumsDest = Join-Path $TMP_DIR "checksums.txt"
        if (-not (Download-File $checksumsUrl $checksumsDest)) {
            Warn "Cannot download checksums.txt, aborting upgrade for security."
            exit 0
        }

        $checksumContent = Get-Content $checksumsDest
        $cliLine = $checksumContent | Where-Object { $_ -match $binSuffix }

        if (-not $cliLine) {
            Warn "checksums.txt missing entry for CLI binary, aborting upgrade."
            exit 0
        }

        $expectedCli = ($cliLine -split '\s+')[0]
        $actualCli = Get-FileHash256 $binDest
        if ($actualCli -ne $expectedCli) {
            Warn "CLI binary checksum mismatch, skipping upgrade."
            exit 0
        }

        # Verify downloaded CLI binary
        $downloadedVer = & $binDest --version 2>$null
        if (-not ($downloadedVer -match '(\d+\.\d+\.\d+)')) {
            Warn "Downloaded CLI binary is not valid, skipping upgrade."
            exit 0
        }

        # Backup current version
        Say "Backing up current version..."
        Backup-Current $localVersion

        # Replace CLI binary
        Say "Replacing CLI binary..."
        try {
            Copy-Item $binDest $CLI_PATH -Force
        } catch {
            Warn "Cannot write to $CLI_PATH (permission denied or file locked)."
            Invoke-Rollback $localVersion
            exit 1
        }

        # Replace Skill files
        Say "Replacing Skill files..."
        $skillExtractDir = Join-Path $TMP_DIR "skill"
        if (Test-Path $skillExtractDir) { Remove-Item $skillExtractDir -Recurse -Force }
        Expand-Archive -Path $skillDest -DestinationPath $skillExtractDir -Force

        # Find extracted content root
        $skillSrc = $skillExtractDir
        $skillMdPath = Join-Path $skillSrc "SKILL.md"
        if (-not (Test-Path $skillMdPath)) {
            $nested = Get-ChildItem -Path $skillSrc -Filter "SKILL.md" -Recurse -Depth 2 | Select-Object -First 1
            if ($nested) {
                $skillSrc = $nested.DirectoryName
            } else {
                Warn "Skill ZIP does not contain SKILL.md."
                Invoke-Rollback $localVersion
                exit 1
            }
        }

        # Replace SKILL.md
        Copy-Item (Join-Path $skillSrc "SKILL.md") (Join-Path $SKILL_DIR "SKILL.md") -Force

        # Replace references/
        $refsSrc = Join-Path $skillSrc "references"
        if (Test-Path $refsSrc) {
            $refsDest = Join-Path $SKILL_DIR "references"
            if (Test-Path $refsDest) { Remove-Item $refsDest -Recurse -Force }
            Copy-Item $refsSrc $refsDest -Recurse -Force
        }

        # Replace scripts/ (last)
        $scriptsSrc = Join-Path $skillSrc "scripts"
        if (Test-Path $scriptsSrc) {
            $scriptsDest = Join-Path $SKILL_DIR "scripts"
            if (Test-Path $scriptsDest) { Remove-Item $scriptsDest -Recurse -Force }
            Copy-Item $scriptsSrc $scriptsDest -Recurse -Force
        }

        # Verify upgrade
        $newVer = & $CLI_PATH --version 2>$null
        if (-not ($newVer -match $remoteVersion)) {
            Invoke-Rollback $localVersion
            exit 1
        }

        # Clean old skill backups, keep only the latest one
        Get-ChildItem -Path $BACKUP_DIR -Filter "skill-*.zip" -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -ne "skill-${localVersion}.zip" } |
            Remove-Item -Force -ErrorAction SilentlyContinue

        Say "Upgrade complete: v${localVersion} -> v${remoteVersion}"
    } finally {
        Invoke-Cleanup
    }
}

Main
