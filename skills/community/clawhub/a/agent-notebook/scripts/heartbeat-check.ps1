#!/usr/bin/env pwsh
# OpenClaw Memory System — Heartbeat Check
# Periodic routine: process cron inbox, check state, create daily file if needed

param(
    [string]$WorkspacePath = "."
)

$ErrorActionPreference = "Stop"

$Workspace = Resolve-Path $WorkspacePath
$MemoryDir = Join-Path $Workspace "memory"
$InboxFile = Join-Path $MemoryDir "cron-inbox.md"
$StateFile = Join-Path $MemoryDir "heartbeat-state.json"
$Today = Get-Date -Format "yyyy-MM-dd"
$TodayFile = Join-Path $MemoryDir "$Today.md"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

Write-Log "Starting heartbeat check..."

# Ensure memory directory exists
if (-not (Test-Path $MemoryDir)) {
    Write-Log "ERROR: Memory directory not found at $MemoryDir"
    exit 1
}

# 1. Ensure today's daily notes file exists
if (-not (Test-Path $TodayFile)) {
    Write-Log "Creating daily notes file for today: $TodayFile"
    $templatesDir = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..\templates"
    $template = Join-Path $templatesDir "daily-notes.md"
    if (Test-Path $template) {
        $content = Get-Content -Raw $template
        $content = $content -replace "YYYY-MM-DD", $Today
        Set-Content -Path $TodayFile -Value $content -Encoding UTF8
        Write-Log "Created from template"
    } else {
        # Minimal fallback
        Set-Content -Path $TodayFile -Value "# $Today - Daily Notes`n`n" -Encoding UTF8
        Write-Log "Created minimal daily notes file"
    }
}

# 2. Process cron inbox if it exists and has content
if (Test-Path $InboxFile) {
    $inboxContent = Get-Content -Raw $InboxFile -ErrorAction SilentlyContinue
    $hasEntries = $false
    if ($inboxContent) {
        # Check if there are any entries (lines starting with ## [)
        $lines = $inboxContent -split "`n"
        foreach ($line in $lines) {
            if ($line -match "^##\s+\[") {
                $hasEntries = $true
                break
            }
        }
    }

    if ($hasEntries) {
        Write-Log "Processing cron inbox..."

        $entriesFound = $false
        $appendContent = "`n`n## $(Get-Date -Format 'HH:mm') - Cron Inbox Processing`n"

        foreach ($line in $lines) {
            if ($line -match "^##\s+\[([^\]]+)\]\s+(.+)$") {
                $entriesFound = $true
                $date = $Matches[1].Trim()
                $rest = $Matches[2].Trim()
                $appendContent = $appendContent + "- [$date] $rest`n"
            }
        }

        if ($entriesFound) {
            Add-Content -Path $TodayFile -Value $appendContent -Encoding UTF8
            Write-Log "Appended inbox entries to daily notes"

            # Clear inbox (keep header)
            $processedTime = Get-Date -Format "yyyy-MM-dd HH:mm"
            $header = "# Cron Inbox`n`nCross-session message bus.`n`n---`n`n*Last processed: $processedTime*`n"
            Set-Content -Path $InboxFile -Value $header -Encoding UTF8
            Write-Log "Cleared cron inbox"
        } else {
            Write-Log "Inbox file exists but no parseable entries found"
        }
    } else {
        Write-Log "Inbox is empty or uninitialized"
    }
} else {
    Write-Log "Inbox file not found -- creating empty inbox"
    $templatesDir = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..\templates"
    $template = Join-Path $templatesDir "cron-inbox.md"
    if (Test-Path $template) {
        Copy-Item $template $InboxFile
    } else {
        Set-Content -Path $InboxFile -Value "# Cron Inbox`n`n" -Encoding UTF8
    }
}

# 3. Update heartbeat state
if (Test-Path $StateFile) {
    $state = Get-Content -Raw $StateFile | ConvertFrom-Json
    $state.lastChecks.cronInbox = [DateTimeOffset]::Now.ToUnixTimeSeconds()
    $state | ConvertTo-Json -Depth 3 | Set-Content -Path $StateFile -Encoding UTF8
    Write-Log "Updated heartbeat state"
} else {
    Write-Log "Creating new heartbeat state file"
    $now = [DateTimeOffset]::Now.ToUnixTimeSeconds()
    $state = @{
        lastChecks = @{ cronInbox = $now; email = $null; calendar = $null; weather = $null; social = $null }
        lastMaintenance = $null
        lastMemoryExtraction = $null
        lastWeeklyReview = $null
        version = "1.0.0"
    }
    $state | ConvertTo-Json -Depth 3 | Set-Content -Path $StateFile -Encoding UTF8
}

Write-Log "Heartbeat check complete."
exit 0
