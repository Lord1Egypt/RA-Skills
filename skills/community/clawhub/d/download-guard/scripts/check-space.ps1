param(
    [string]$TargetDrive = "",
    [double]$MinFreeGB = 0.5,
    [double]$WarnFreeGB = 2.0
)

# Config: read config.md
$skillDir   = "$env:USERPROFILE\.workbuddy\skills\download-guard"
$configPath = "$skillDir\config.md"
$downloadRoot = ""

if (Test-Path $configPath) {
    $content = Get-Content $configPath -Raw
    if ($content -match "MIN_FREE_GB:\s*([0-9.]+)")  { $MinFreeGB  = [double]$Matches[1] }
    if ($content -match "WARN_FREE_GB:\s*([0-9.]+)") { $WarnFreeGB = [double]$Matches[1] }
    # Auto-detect TargetDrive from DOWNLOAD_ROOT
    if ($content -match "DOWNLOAD_ROOT:\s*([A-Za-z]):") {
        $configDrive = $Matches[1]
    }
    if ($content -match "DOWNLOAD_ROOT:\s*(.+)") {
        $downloadRoot = $Matches[1].Trim()
    }
}

# Priority: explicit param > config > fallback
# Only override TargetDrive from config if user didn't explicitly pass one
if (-not $TargetDrive) {
    if ($configDrive) { $TargetDrive = $configDrive } else { $TargetDrive = "C" }
}
# If user explicitly passed TargetDrive, use it (even if config says different)

$driveLetter = $TargetDrive.TrimEnd(":\")
$disk = Get-PSDrive -Name $driveLetter -ErrorAction SilentlyContinue

# --- Path availability check (v5.4) ---
# If the drive doesn't exist at all, this is a critical config error
if (-not $disk) {
    Write-Output "CRITICAL: Drive ${driveLetter}: not found!"
    Write-Output "  DOWNLOAD_ROOT ($downloadRoot) points to a drive that is not available."
    Write-Output "  Possible causes: external drive disconnected, network drive offline, or wrong drive letter."
    Write-Output "  ACTION: Update DOWNLOAD_ROOT in config.md or reconnect the drive."
    Write-Output "  BLOCKED: Download blocked to prevent C-drive fallback."
    exit 2
}

# If the drive exists, verify the download root path is writable
if ($downloadRoot -and (Test-Path $downloadRoot)) {
    # Test write permission by creating and deleting a temp file
    $testFile = Join-Path $downloadRoot ".dg-write-test-$(Get-Random).tmp"
    try {
        Set-Content -Path $testFile -Value "test" -ErrorAction Stop
        Remove-Item $testFile -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Output "CRITICAL: DOWNLOAD_ROOT ($downloadRoot) is not writable!"
        Write-Output "  Error: $($_.Exception.Message)"
        Write-Output "  ACTION: Check folder permissions or choose a different path."
        Write-Output "  BLOCKED: Download blocked due to insufficient permissions."
        exit 2
    }
} elseif ($downloadRoot) {
    # Path doesn't exist yet — try to create it
    try {
        New-Item -ItemType Directory -Path $downloadRoot -Force -ErrorAction Stop | Out-Null
        Write-Output "CREATED: Download directory created at $downloadRoot"
    } catch {
        Write-Output "CRITICAL: Cannot create DOWNLOAD_ROOT ($downloadRoot)!"
        Write-Output "  Error: $($_.Exception.Message)"
        Write-Output "  ACTION: Choose a different path or create the directory manually."
        Write-Output "  BLOCKED: Download blocked due to inaccessible path."
        exit 2
    }
}

# --- Disk space check ---
$freeGB = [math]::Round($disk.Free / 1GB, 2)
$totalGB = [math]::Round(($disk.Used + $disk.Free) / 1GB, 2)
$usedPct = [math]::Round($disk.Used / ($disk.Used + $disk.Free) * 100, 1)

Write-Output "DISK_INFO: ${driveLetter}: total=${totalGB}GB used=${usedPct}% free=${freeGB}GB"

if ($freeGB -lt $MinFreeGB) {
    Write-Output "BLOCK: Free space below ${MinFreeGB}GB (current: ${freeGB}GB). Download blocked."
    Write-Output "SUGGESTION: Please clean up old files on ${driveLetter}: before retrying."
    exit 1
}
elseif ($freeGB -lt $WarnFreeGB) {
    Write-Output "WARN: Free space below ${WarnFreeGB}GB (current: ${freeGB}GB). Monitor disk usage."
    Write-Output "ALLOW: Proceeding with download."
    exit 0
}
else {
    Write-Output "OK: Space sufficient (free: ${freeGB}GB). Download allowed."
    exit 0
}
