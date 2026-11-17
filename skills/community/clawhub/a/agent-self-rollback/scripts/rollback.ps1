# ============================================================
# rollback.ps1 - Agent self-rollback (portable snapshot manager)
# ============================================================
# Actions:
#   snapshot            Create a timestamped snapshot of core agent memory files
#   list                List all existing snapshots
#   restore [index]     Restore a snapshot (auto-backup current state first)
#   verify              Compare current core files against the latest snapshot
#
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 snapshot
#   powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 list
#   powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 restore
#   powershell -NoProfile -ExecutionPolicy Bypass -File rollback.ps1 verify
#
# CONFIGURATION (edit for your agent):
#   $AgentDir   -> absolute path of your agent data root
#   $CoreFiles  -> relative paths of the files you want protected
# ============================================================

param(
    [ValidateSet("snapshot", "list", "restore", "verify")]
    [string]$Action = "snapshot",
    [string]$Arg = ""
)

$ErrorActionPreference = "Stop"

# ---------------- config (customize these two!) ----------------
#$AgentDir = "C:\path\to\your\agent\data"
# Example defaults below assume a CherryStudio-like layout. Replace with YOUR paths.
$AgentDir = "."
$CoreFiles = @(
    @{ rel = "SOUL.md";              label = "SOUL     (identity / personality)"           },
    @{ rel = "USER.md";              label = "USER     (about the user)"                   },
    @{ rel = "memory\FACT.md";       label = "FACT     (durable knowledge)"                },
    @{ rel = "memory\JOURNAL.jsonl"; label = "JOURNAL  (events log, append-only)"          }
)

# Snapshot root: one level up from this script by default.
# NOTE: Join-Path takes only TWO path segments in Windows PowerShell 5.1.
$SnapRoot = Join-Path (Join-Path $PSScriptRoot "..") "snapshots"
# ---------------------------------------------------------------

function New-TimeStamp {
    return (Get-Date -Format "yyyyMMdd_HHmmss")
}

function Get-FullCorePath($entry) {
    return Join-Path $AgentDir $entry.rel
}

# ---------------- snapshot ----------------
function Do-Snapshot([string]$reason) {
    if (-not (Test-Path $SnapRoot)) { New-Item -ItemType Directory -Path $SnapRoot | Out-Null }

    $stamp = New-TimeStamp
    $target = Join-Path $SnapRoot $stamp
    New-Item -ItemType Directory -Path $target | Out-Null

    $manifest = @()
    $hashes = @()

    foreach ($f in $CoreFiles) {
        $src = Get-FullCorePath $f
        $name = Split-Path $f.rel -Leaf
        if (Test-Path $src) {
            Copy-Item -Path $src -Destination (Join-Path $target $name) -Force
            $hash = (Get-FileHash -Path $src -Algorithm MD5).Hash
            $manifest += "$($f.rel)`t$name"
            $hashes   += "$($f.rel)`t$hash"
        } else {
            $manifest += "$($f.rel)`t(MISSING)"
            $hashes   += "$($f.rel)`tMISSING"
        }
    }

    # extra paths from -Arg (comma separated) are snapshotted too
    if ($Arg) {
        foreach ($p in ($Arg -split ",")) {
            $p = $p.Trim()
            if (Test-Path $p) {
                Copy-Item -Path $p -Destination (Join-Path $target ("extra_" + (Split-Path $p -Leaf))) -Force
            }
        }
    }

    $reasonText = if ($reason) { $reason } else { "manual" }
    $manifest | Out-File -FilePath (Join-Path $target "MANIFEST.txt") -Encoding utf8
    $hashes   | Out-File -FilePath (Join-Path $target "HASHES.md5")  -Encoding utf8
    Set-Content -Path (Join-Path $target "REASON.txt") -Value $reasonText -Encoding utf8

    Write-Host "[OK] Snapshot created: $stamp  (reason: $reasonText)"
    Write-Host "     Location: $target"
    return $target
}

# ---------------- list ----------------
function Do-List {
    if (-not (Test-Path $SnapRoot)) {
        Write-Host "No snapshots yet. Run snapshot first."
        return
    }
    $dirs = Get-ChildItem -Path $SnapRoot -Directory | Sort-Object Name -Descending
    if ($dirs.Count -eq 0) {
        Write-Host "No snapshots yet. Run snapshot first."
        return
    }
    Write-Host ("{0,4}  {1,-20}  {2}" -f "Idx", "Stamp", "Reason")
    Write-Host ("{0,4}  {1,-20}  {2}" -f "----", "-------------------", "------")
    for ($i = 0; $i -lt $dirs.Count; $i++) {
        $reason = ""
        $reasonFile = Join-Path $dirs[$i].FullName "REASON.txt"
        if (Test-Path $reasonFile) { $reason = (Get-Content $reasonFile -Raw).Trim() }
        Write-Host ("{0,4}  {1,-20}  {2}" -f $i, $dirs[$i].Name, $reason)
    }
    Write-Host ""
    Write-Host "Most recent snapshot is index 0."
    return $dirs
}

# ---------------- restore ----------------
function Do-Restore([string]$argIndex) {
    $dirs = Do-List
    if (-not $dirs) { return }

    $idx = -1
    if ($argIndex -ne "") {
        if (-not [int]::TryParse($argIndex, [ref]$idx)) {
            Write-Host "[ERR] index must be a number."
            return
        }
    } else {
        Write-Host "Enter index to restore (or just press Enter to cancel):"
        $input = Read-Host
        if ($input -eq "") { Write-Host "Cancelled."; return }
        if (-not [int]::TryParse($input, [ref]$idx)) {
            Write-Host "[ERR] invalid input."
            return
        }
    }
    if ($idx -lt 0 -or $idx -ge $dirs.Count) {
        Write-Host "[ERR] index out of range."
        return
    }

    $sel = $dirs[$idx]
    Write-Host ""
    Write-Host "You are about to RESTORE snapshot: $($sel.Name)"
    Write-Host "This will OVERWRITE current core agent memory files."
    Write-Host "A safety backup of the current state will be taken first."
    Write-Host "Type 'yes' to confirm:"
    $confirm = Read-Host
    if ($confirm -ne "yes") { Write-Host "Restore cancelled."; return }

    # safety: backup current state before overwriting
    Do-Snapshot "pre-restore-before-$($sel.Name)" | Out-Null

    # restore each file present in the snapshot
    $restored = 0
    foreach ($f in $CoreFiles) {
        $name = Split-Path $f.rel -Leaf
        $snapFile = Join-Path $sel.FullName $name
        if (Test-Path $snapFile) {
            $dst = Get-FullCorePath $f
            $dstDir = Split-Path $dst -Parent
            if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
            Copy-Item -Path $snapFile -Destination $dst -Force
            $restored++
            Write-Host "  [OK] $($f.rel)"
        } else {
            Write-Host "  [SKIP] $($f.rel) (not present in this snapshot)"
        }
    }
    Write-Host ""
    Write-Host "[DONE] Restored $restored file(s) from snapshot $($sel.Name)."
    Write-Host "       Current state was saved as a separate snapshot (pre-restore)."
}

# ---------------- verify ----------------
function Do-Verify {
    $dirs = Get-ChildItem -Path $SnapRoot -Directory | Sort-Object Name -Descending
    if ($dirs.Count -eq 0) {
        Write-Host "No snapshots to compare against."
        return
    }
    $latest = $dirs[0]
    $hashFile = Join-Path $latest.FullName "HASHES.md5"
    $hashes = @{}
    if (Test-Path $hashFile) {
        Get-Content $hashFile | ForEach-Object {
            $parts = $_ -split "`t"
            if ($parts.Count -ge 2) { $hashes[$parts[0]] = $parts[1] }
        }
    }

    Write-Host "Comparing current files against latest snapshot: $($latest.Name)"
    Write-Host ("{0,-28} {1,-10} {2}" -f "File", "Status", "Detail")
    Write-Host ("{0,-28} {1,-10} {2}" -f "---------------------------", "----------", "----------------------")

    foreach ($f in $CoreFiles) {
        $src = Get-FullCorePath $f
        if (-not (Test-Path $src)) {
            Write-Host ("{0,-28} {1,-10} {2}" -f $f.rel, "MISSING", "file currently absent")
            continue
        }
        $curHash = (Get-FileHash -Path $src -Algorithm MD5).Hash
        if ($hashes.ContainsKey($f.rel)) {
            if ($hashes[$f.rel] -eq $curHash) {
                Write-Host ("{0,-28} {1,-10} {2}" -f $f.rel, "UNCHANGED", "-")
            } else {
                Write-Host ("{0,-28} {1,-10} {2}" -f $f.rel, "CHANGED", "differs from last snapshot")
            }
        } else {
            Write-Host ("{0,-28} {1,-10} {2}" -f $f.rel, "UNKNOWN", "no hash on record in snapshot")
        }
    }
    Write-Host ""
    Write-Host "Note: if a journal/event log is in your core files, expect CHANGED on every run - that is normal."
}

# ---------------- main ----------------
switch ($Action) {
    "snapshot" { Do-Snapshot "" }
    "list"     { Do-List | Out-Null }
    "restore"  { Do-Restore $Arg }
    "verify"   { Do-Verify }
}