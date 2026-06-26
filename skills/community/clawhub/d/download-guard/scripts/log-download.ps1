param(
    [string]$FileName = "unknown",
    [double]$SizeMB = 0,
    [string]$TargetPath = "unknown",
    [string]$Reason = "agent-download"
)

$logDir   = "$env:USERPROFILE\.workbuddy"
$logFile  = "$logDir\download-log.md"
$skillDir = "$env:USERPROFILE\.workbuddy\skills\download-guard"

# --- Read config ---
$retentionDays = 30
$archiveMaxMB  = 10

if (Test-Path "$skillDir\config.md") {
    $cfg = Get-Content "$skillDir\config.md" -Raw
    if ($cfg -match "LOG_RETENTION_DAYS:\s*(\d+)")   { $retentionDays = [int]$Matches[1] }
    if ($cfg -match "LOG_ARCHIVE_MAX_MB:\s*(\d+)")    { $archiveMaxMB  = [int]$Matches[1] }
}

# --- Ensure log directory ---
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# --- Create log file if not exists ---
if (-not (Test-Path $logFile)) {
    $header = "# AI Agent Download Log`r`n`r`n| Time | File | Size | Path | Reason |`r`n|------|------|------|------|--------|"
    Set-Content -Path $logFile -Value $header -Encoding UTF8
}

# --- Append new entry ---
$timestamp  = Get-Date -Format "yyyy-MM-dd HH:mm"
$sizeDisplay = if ($SizeMB -gt 0) { "${SizeMB}MB" } else { "unknown" }
$newRow = "| $timestamp | $FileName | $sizeDisplay | $TargetPath | $Reason |"
Add-Content -Path $logFile -Value $newRow -Encoding UTF8

Write-Output "LOG_OK: Logged download -> $FileName ($sizeDisplay) -> $TargetPath"

# --- Auto cleanup: archive old entries ---
if ($retentionDays -eq 0) {
    # 0 = never clean up
    exit 0
}

$cutoff = (Get-Date).AddDays(-$retentionDays).ToString("yyyy-MM-dd")

# Read current log
$lines = Get-Content $logFile -Encoding UTF8

# Separate header (first 3 lines: title, blank, table header) from data rows
$headerLines = @()
$dataLines   = @()
$inHeader = $true
foreach ($line in $lines) {
    if ($inHeader -and $line -match '^\|.*\|.*\|.*\|') {
        # This is the table header row
        $headerLines += $line
        $inHeader = $false
        continue
    }
    if ($inHeader) {
        $headerLines += $line
    } else {
        $dataLines += $line
    }
}

# Split data into current (within retention) and old (beyond retention)
$currentLines = @()
$oldLines     = @()
foreach ($dl in $dataLines) {
    # Data rows start with "| yyyy-"
    if ($dl -match '^\|\s*(\d{4}-\d{2}-\d{2})') {
        $rowDate = $Matches[1]
        if ($rowDate -lt $cutoff) {
            $oldLines += $dl
        } else {
            $currentLines += $dl
        }
    } else {
        # Separator or non-data row, keep in current
        $currentLines += $dl
    }
}

# If there are old entries, archive them
if ($oldLines.Count -gt 0) {
    $archiveDate = Get-Date -Format "yyyy-MM-dd"
    $archiveFile = "$logDir\download-log-archive-${archiveDate}.md"

    # Write archive header if new file
    if (-not (Test-Path $archiveFile)) {
        $archHeader = "# Download Log Archive ($archiveDate)`r`n`r`n| Time | File | Size | Path | Reason |`r`n|------|------|------|------|--------|"
        Set-Content -Path $archiveFile -Value $archHeader -Encoding UTF8
    }

    # Append old entries to archive
    foreach ($ol in $oldLines) {
        Add-Content -Path $archiveFile -Value $ol -Encoding UTF8
    }

    # Rebuild current log (header + current rows only)
    $newContent = $headerLines + $currentLines
    Set-Content -Path $logFile -Value $newContent -Encoding UTF8

    Write-Output "ARCHIVE: Moved $($oldLines.Count) old entries to archive ($archiveDate)"

    # --- Cleanup old archives exceeding size limit ---
    $archives = Get-ChildItem "$logDir\download-log-archive-*.md" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending

    foreach ($arch in $archives) {
        $sizeMB = [math]::Round($arch.Length / 1MB, 1)
        if ($sizeMB -gt $archiveMaxMB) {
            Remove-Item $arch.FullName -Force
            Write-Output "ARCHIVE_CLEANUP: Deleted old archive $($arch.Name) (${sizeMB}MB > ${archiveMaxMB}MB limit)"
        }
    }
}
