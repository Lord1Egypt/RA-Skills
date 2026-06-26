#Requires -Version 5.1
<#
.SYNOPSIS
    Fast backup verification for Guardian safety skill.
.DESCRIPTION
    Checks multiple backup indicators for a target path.
    Returns VERIFIED, STALE, UNVERIFIED, or PARTIAL within 2 seconds.
.PARAMETER TargetPath
    The file or directory to check backup status for.
.EXAMPLE
    .\verify-backup.ps1 -TargetPath "C:\Users\Me\Documents\project"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath
)

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$results = @()
$verdict = "UNVERIFIED"

# Resolve target path
$resolved = Resolve-Path $TargetPath -ErrorAction SilentlyContinue
if (-not $resolved) {
    Write-Output '{"verdict":"UNVERIFIED","reason":"Path not found","checks":[],"elapsed_ms":0}'
    exit 1
}
$target = $resolved.Path

function Add-Check($name, $status, $detail, $recency_hours = $null) {
    $script:results += @{
        name = $name
        status = $status
        detail = $detail
        recency_hours = $recency_hours
    }
}

# 1. Git repository
$gitDir = $target
$foundGit = $false
while ($gitDir.Length -gt 3) {
    if (Test-Path (Join-Path $gitDir ".git")) {
        $foundGit = $true
        break
    }
    $gitDir = Split-Path $gitDir -Parent
}
if ($foundGit) {
    # Check if target is tracked
    $tracked = $false
    try {
        $null = git -C $gitDir ls-files "$($target.Substring($gitDir.Length + 1))" 2>$null
        if ($LASTEXITCODE -eq 0) { $tracked = $true }
    } catch {}
    
    if ($tracked) {
        Add-Check "git-repository" "VERIFIED" "Git repository detected, file tracked" $null
        $verdict = "VERIFIED"
    } else {
        Add-Check "git-repository" "PARTIAL" "Git repository detected, file NOT tracked" $null
    }
}

# 2. File History (Windows)
if ($verdict -ne "VERIFIED") {
    try {
        $fhConfig = Get-WmiObject -Namespace "root\cimv2" -Class "Win32_FileHistoryConfiguration" -ErrorAction SilentlyContinue
        if ($fhConfig -and $fhConfig.Enabled) {
            # Check if target drive is included
            $driveLetter = (Split-Path $target -Qualifier).TrimEnd(':')
            $userPath = [Environment]::GetFolderPath("UserProfile")
            if ($target -like "$userPath*" -or $fhConfig.Include -match $driveLetter) {
                Add-Check "file-history" "VERIFIED" "File History enabled for target drive" $null
                $verdict = "VERIFIED"
            } else {
                Add-Check "file-history" "PARTIAL" "File History enabled but not for target path" $null
            }
        }
    } catch {
        Add-Check "file-history" "UNVERIFIED" "File History check failed: $($_.Exception.Message)" $null
    }
}

# 3. OneDrive / Dropbox / Google Drive / iCloud sync
if ($verdict -ne "VERIFIED") {
    $userProfile = [Environment]::GetFolderPath("UserProfile")
    $cloudPaths = @(
        "$userProfile\OneDrive",
        "$userProfile\Dropbox",
        "$userProfile\Google Drive",
        "$userProfile\iCloudDrive",
        "$userProfile\iCloud Drive"
    )
    $inCloud = $false
    foreach ($cp in $cloudPaths) {
        if ($target -like "$cp*") {
            $inCloud = $true
            break
        }
    }
    if ($inCloud) {
        # Check sync clients running
        $syncProcs = @("OneDrive", "Dropbox", "GoogleDriveFS", "iCloudDrive")
        $running = $syncProcs | ForEach-Object { Get-Process $_ -ErrorAction SilentlyContinue } | Select-Object -First 1
        if ($running) {
            Add-Check "cloud-sync" "VERIFIED" "Path in cloud sync directory, client active" $null
            $verdict = "VERIFIED"
        } else {
            Add-Check "cloud-sync" "PARTIAL" "Path in cloud sync directory but client not running" $null
        }
    }
}

# 4. Explicit backup tools (check for restic/borg/duplicity snapshots)
if ($verdict -ne "VERIFIED") {
    $backupMarkers = @(
        (Join-Path (Split-Path $target -Parent) ".restic"),
        (Join-Path (Split-Path $target -Parent) ".borg"),
        (Join-Path (Split-Path $target -Parent) ".snapshots"),
        (Join-Path (Split-Path $target -Parent) ".backup"),
        "$env:LOCALAPPDATA\.restic",
        "$env:APPDATA\.borg"
    )
    foreach ($marker in $backupMarkers) {
        if (Test-Path $marker) {
            Add-Check "explicit-backup" "VERIFIED" "Backup marker found: $marker" $null
            $verdict = "VERIFIED"
            break
        }
    }
}

# 5. Volume Shadow Copy (Windows)
if ($verdict -ne "VERIFIED") {
    try {
        $vssAdmin = Get-Command "vssadmin" -ErrorAction SilentlyContinue
        if ($vssAdmin) {
            $driveLetter = (Split-Path $target -Qualifier).TrimEnd(':')
            $shadows = vssadmin list shadows /for="$driveLetter`:" 2>$null | Select-String "Shadow Copy"
            if ($shadows) {
                Add-Check "volume-shadow-copy" "VERIFIED" "VSS snapshots exist for target volume" $null
                $verdict = "VERIFIED"
            }
        }
    } catch {
        Add-Check "volume-shadow-copy" "UNVERIFIED" "VSS check failed" $null
    }
}

$elapsed = $stopwatch.ElapsedMilliseconds

# Build output
$output = @{
    verdict = $verdict
    target = $target
    checks = $results
    elapsed_ms = $elapsed
}

# Determine final verdict logic
if ($results | Where-Object { $_.status -eq "VERIFIED" }) {
    $output.verdict = "VERIFIED"
} elseif ($results | Where-Object { $_.status -eq "STALE" }) {
    $output.verdict = "STALE"
} elseif ($results | Where-Object { $_.status -eq "PARTIAL" }) {
    $output.verdict = "PARTIAL"
}

Write-Output ($output | ConvertTo-Json -Depth 3)
exit 0
