#!/usr/bin/env pwsh
# OpenClaw Memory System - Nightly Memory Extraction
# Extracts durable facts from daily notes and appends them to MEMORY.md

param(
    [string]$WorkspacePath = "."
)

$ErrorActionPreference = "Stop"

$Workspace = Resolve-Path $WorkspacePath
$MemoryDir = Join-Path $Workspace "memory"
$MemoryFile = Join-Path $Workspace "MEMORY.md"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

Write-Log "Starting nightly memory extraction..."

# Check if memory directory exists
if (-not (Test-Path $MemoryDir)) {
    Write-Log "ERROR: Memory directory not found at $MemoryDir"
    exit 1
}

# Check if MEMORY.md exists
if (-not (Test-Path $MemoryFile)) {
    Write-Log "WARNING: MEMORY.md not found at $MemoryFile. Creating from template..."
    $templatesDir = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..\templates"
    $template = Join-Path $templatesDir "MEMORY.md"
    if (Test-Path $template) {
        Copy-Item $template $MemoryFile
        Write-Log "Created MEMORY.md from template"
    } else {
        Write-Log "ERROR: Template not found. Cannot create MEMORY.md."
        exit 1
    }
}

# Find today's daily notes file
$Today = Get-Date -Format "yyyy-MM-dd"
$TodayFile = Join-Path $MemoryDir "$Today.md"

if (-not (Test-Path $TodayFile)) {
    Write-Log "No daily notes found for today ($Today). Nothing to extract."
    exit 0
}

Write-Log "Reading daily notes: $TodayFile"
$lines = Get-Content $TodayFile

# Significance keywords
$significanceKeywords = @(
    "decided", "decision", "lesson learned", "important", "breakthrough",
    "milestone", "completed", "shipped", "launched", "fixed", "solved",
    "agreed", "confirmed", "approved", "rejected", "failed", "error",
    "new project", "started", "created", "deployed", "published"
)

# Extract significant entries using keywords and structured fields
$extracted = @()
$currentEntry = $null
$currentBody = @()

foreach ($line in $lines) {
    if ($line -match "^##\s+(\d{2}:\d{2})\s+--\s+(.+)$") {
        # Save previous entry if significant
        if ($currentEntry -and $currentBody.Count -gt 0) {
            $fullText = "$currentEntry $($currentBody -join ' ')"
            $isSignificant = $false
            foreach ($kw in $significanceKeywords) {
                if ($fullText -match $kw) {
                    $isSignificant = $true
                    break
                }
            }
            if ($isSignificant) {
                $extracted += @{
                    Title = $currentEntry
                    Body = ($currentBody -join "`n").Trim()
                    Date = $Today
                }
            }
        }
        # Start new entry
        $currentEntry = $Matches[2].Trim()
        $currentBody = @()
    } elseif ($currentEntry -ne $null -and $line -notmatch "^#") {
        $currentBody += $line
    }
}

# Save last entry
if ($currentEntry -and $currentBody.Count -gt 0) {
    $fullText = "$currentEntry $($currentBody -join ' ')"
    $isSignificant = $false
    foreach ($kw in $significanceKeywords) {
        if ($fullText -match $kw) {
            $isSignificant = $true
            break
        }
    }
    if ($isSignificant) {
        $extracted += @{
            Title = $currentEntry
            Body = ($currentBody -join "`n").Trim()
            Date = $Today
        }
    }
}

if ($extracted.Count -eq 0) {
    Write-Log "No significant entries found for extraction."
    exit 0
}

Write-Log "Extracting $($extracted.Count) significant entries to MEMORY.md"

# Append to MEMORY.md under a new "Daily Extracts" section
$extractSection = "`n`n## Daily Extracts - $Today`n`n"

foreach ($item in $extracted) {
    $extractSection = $extractSection + "### $($item.Title)`n- **Date:** $($item.Date)`n- **Details:** $($item.Body -replace "`n", "`n  ")`n`n"
}

Add-Content -Path $MemoryFile -Value $extractSection -Encoding UTF8
Write-Log "Appended $($extracted.Count) extracts to MEMORY.md"

# Mark entries as extracted in daily notes (add a marker)
$marker = "`n`n---`n*Memory extraction completed at $(Get-Date -Format "HH:mm")*"
Add-Content -Path $TodayFile -Value $marker -Encoding UTF8
Write-Log "Marked daily notes as extracted"

# Update heartbeat state
$stateFile = Join-Path $MemoryDir "heartbeat-state.json"
if (Test-Path $stateFile) {
    $state = Get-Content -Raw $stateFile | ConvertFrom-Json
    $state.lastMemoryExtraction = [DateTimeOffset]::Now.ToUnixTimeSeconds()
    $state | ConvertTo-Json -Depth 3 | Set-Content -Path $stateFile -Encoding UTF8
    Write-Log "Updated heartbeat state"
}

Write-Log "Nightly memory extraction complete."
exit 0
