#!/usr/bin/env pwsh
# OpenClaw Memory System - Automated Tests (PowerShell)
# Run: ./test-memory-system.ps1

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$SkillRoot = Split-Path -Parent $ScriptDir
$TestWorkspace = Join-Path $env:TEMP "openclaw-memory-test-$(Get-Random)"

# Test results
$TestResults = @()
$Passed = 0
$Failed = 0

function Test-Step {
    param(
        [string]$Name,
        [scriptblock]$Script
    )
    Write-Host ""
    Write-Host "[TEST] $Name" -ForegroundColor Cyan
    try {
        Invoke-Command -ScriptBlock $Script
        Write-Host "[PASS] $Name" -ForegroundColor Green
        $script:Passed++
        $script:TestResults += @{ Name = $Name; Status = "PASS"; Error = $null }
    } catch {
        Write-Host "[FAIL] $Name" -ForegroundColor Red
        Write-Host "       $_" -ForegroundColor Red
        $script:Failed++
        $script:TestResults += @{ Name = $Name; Status = "FAIL"; Error = $_.ToString() }
    }
}

function Assert-Exists {
    param([string]$Path, [string]$Message = "File/dir should exist")
    if (-not (Test-Path $Path)) {
        throw "$Message`: $Path"
    }
}

function Assert-Contains {
    param([string]$Path, [string]$Pattern, [string]$Message = "File should contain pattern")
    $content = Get-Content -Raw $Path
    if ($content -notmatch $Pattern) {
        throw "$Message`: '$Pattern' not found in $Path"
    }
}

Write-Host "========================================"
Write-Host "OpenClaw Memory System - Test Suite"
Write-Host "Test workspace: $TestWorkspace"
Write-Host "========================================"

# Setup: Create test workspace
New-Item -ItemType Directory -Path $TestWorkspace -Force | Out-Null

# === TEST 1: Installation ===
Test-Step "Installation script creates correct structure" {
    $installScript = Join-Path $SkillRoot "scripts\install.ps1"
    if (-not (Test-Path $installScript)) { throw "Install script not found" }

    Invoke-Command -ScriptBlock { param($p,$w) & $p -WorkspacePath $w } -ArgumentList $installScript,$TestWorkspace

    # Verify directories
    Assert-Exists (Join-Path $TestWorkspace "memory") "memory dir"
    Assert-Exists (Join-Path $TestWorkspace "memory\diary") "diary dir"
    Assert-Exists (Join-Path $TestWorkspace "memory\dreams") "dreams dir"

    # Verify files
    Assert-Exists (Join-Path $TestWorkspace "MEMORY.md") "MEMORY.md"
    Assert-Exists (Join-Path $TestWorkspace "HEARTBEAT.md") "HEARTBEAT.md"
    Assert-Exists (Join-Path $TestWorkspace "memory\cron-inbox.md") "cron-inbox.md"
    Assert-Exists (Join-Path $TestWorkspace "memory\heartbeat-state.json") "heartbeat-state.json"
    Assert-Exists (Join-Path $TestWorkspace "memory\platform-posts.md") "platform-posts.md"
    Assert-Exists (Join-Path $TestWorkspace "memory\strategy-notes.md") "strategy-notes.md"

    # Verify MEMORY.md has placeholders
    Assert-Contains (Join-Path $TestWorkspace "MEMORY.md") "About \[Your Name" "MEMORY.md template"
}

# === TEST 2: Daily Notes ===
Test-Step "Daily notes file is created and formatted correctly" {
    $today = Get-Date -Format "yyyy-MM-dd"
    $todayFile = Join-Path $TestWorkspace "memory\$today.md"

    Assert-Exists $todayFile "Today's daily notes file"
    Assert-Contains $todayFile "# $today" "Daily notes header"
    Assert-Contains $todayFile "Session Start" "Session start section"
}

# === TEST 3: Cron Inbox Processing ===
Test-Step "Cron inbox entries are processed into daily notes" {
    $inboxFile = Join-Path $TestWorkspace "memory\cron-inbox.md"
    $todayFile = Join-Path $TestWorkspace "memory\$(Get-Date -Format 'yyyy-MM-dd').md"

    # Add a test entry to inbox
    $testEntry = @"

## [$(Get-Date -Format "yyyy-MM-dd HH:mm")] TestBot - Test event
This is a test entry from a cron job.
It has multiple lines.
"@
    Add-Content -Path $inboxFile -Value $testEntry -Encoding UTF8

    # Run heartbeat check
    $heartbeatScript = Join-Path $SkillRoot "scripts\heartbeat-check.ps1"
    Invoke-Command -ScriptBlock { param($p,$w) & $p -WorkspacePath $w } -ArgumentList $heartbeatScript,$TestWorkspace

    # Verify entry was moved to daily notes
    Assert-Contains $todayFile "TestBot" "Inbox entry in daily notes"
    Assert-Contains $todayFile "Cron Inbox Processing" "Inbox processing section"

    # Verify inbox was cleared
    $inboxContent = Get-Content -Raw $inboxFile
    if ($inboxContent -match "TestBot") {
        throw "Inbox was not cleared - TestBot still found"
    }
}

# === TEST 4: Memory Extraction ===
Test-Step "Significant entries are extracted to MEMORY.md" {
    $todayFile = Join-Path $TestWorkspace "memory\$(Get-Date -Format 'yyyy-MM-dd').md"
    $memoryFile = Join-Path $TestWorkspace "MEMORY.md"

    # Add a significant entry to daily notes using ASCII dash
    $significantEntry = @"

## 14:30 -- Major Decision Made
We decided to switch from MongoDB to PostgreSQL for the project.
This is an important architectural decision that will affect scaling.
**Decision:** Use PostgreSQL with TimescaleDB extension.
"@
    # Write using UTF8 without BOM to avoid encoding issues
    [System.IO.File]::AppendAllText($todayFile, $significantEntry, [System.Text.Encoding]::UTF8)

    # Run memory extraction
    $extractScript = Join-Path $SkillRoot "scripts\memory-extract.ps1"
    Invoke-Command -ScriptBlock { param($p,$w) & $p -WorkspacePath $w } -ArgumentList $extractScript,$TestWorkspace

    # Verify extraction
    Assert-Contains $memoryFile "Daily Extracts" "Extracts section in MEMORY.md"
    Assert-Contains $memoryFile "Major Decision Made" "Extracted entry title"
    Assert-Contains $memoryFile "PostgreSQL" "Extracted content"

    # Verify daily notes marked as extracted
    Assert-Contains $todayFile "Memory extraction completed" "Extraction marker"
}

# === TEST 5: Heartbeat State ===
Test-Step "Heartbeat state file is updated correctly" {
    $stateFile = Join-Path $TestWorkspace "memory\heartbeat-state.json"

    Assert-Exists $stateFile "Heartbeat state file"

    $state = Get-Content -Raw $stateFile | ConvertFrom-Json
    if ($state.version -ne "1.0.0") {
        throw "Unexpected version: $($state.version)"
    }
    if (-not $state.lastChecks) {
        throw "Missing lastChecks in state"
    }
}

# === TEST 6: Dry Run ===
Test-Step "Installation dry run does not create files" {
    $dryRunWorkspace = Join-Path $env:TEMP "openclaw-dryrun-$(Get-Random)"
    New-Item -ItemType Directory -Path $dryRunWorkspace -Force | Out-Null

    $installScript = Join-Path $SkillRoot "scripts\install.ps1"
    Invoke-Command -ScriptBlock { param($p,$w) & $p -WorkspacePath $w -DryRun } -ArgumentList $installScript,$dryRunWorkspace

    # Verify MEMORY.md was NOT created
    if (Test-Path (Join-Path $dryRunWorkspace "MEMORY.md")) {
        throw "Dry run created files - it shouldn't"
    }

    # Cleanup
    Remove-Item -Recurse -Force $dryRunWorkspace -ErrorAction SilentlyContinue
}

# === SUMMARY ===
Write-Host ""
Write-Host "========================================" -ForegroundColor White
Write-Host "Test Results" -ForegroundColor White
Write-Host "========================================" -ForegroundColor White

foreach ($result in $TestResults) {
    $color = if ($result.Status -eq "PASS") { "Green" } else { "Red" }
    Write-Host "[$($result.Status)] $($result.Name)" -ForegroundColor $color
}

Write-Host ""
Write-Host "Total: $($TestResults.Count) | Passed: $Passed | Failed: $Failed" -ForegroundColor White

# Cleanup
Write-Host ""
Write-Host "Cleaning up test workspace..." -ForegroundColor Yellow
Remove-Item -Recurse -Force $TestWorkspace -ErrorAction SilentlyContinue

if ($Failed -gt 0) {
    Write-Host ""
    Write-Host "SOME TESTS FAILED" -ForegroundColor Red
    exit 1
} else {
    Write-Host ""
    Write-Host "ALL TESTS PASSED" -ForegroundColor Green
    exit 0
}
