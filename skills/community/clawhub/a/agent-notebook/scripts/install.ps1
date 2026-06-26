#!/usr/bin/env pwsh
# OpenClaw Memory System — Installation Script
# Run this to set up the complete memory architecture in your workspace

param(
    [string]$WorkspacePath = ".",
    [switch]$SkipTemplates,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$SkillRoot = Split-Path -Parent $ScriptDir

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $colors = @{ "INFO" = "Cyan"; "OK" = "Green"; "WARN" = "Yellow"; "ERR" = "Red" }
    $color = $colors[$Status]
    Write-Host "[$Status] $Message" -ForegroundColor $color
}

function Test-PathSafe {
    param([string]$Path)
    return Test-Path -Path $Path
}

Write-Status "OpenClaw Memory System Installer v1.0.0" "INFO"

# Resolve paths
$Workspace = $WorkspacePath
Write-Status "Workspace: $Workspace" "INFO"

# Ensure workspace directory exists
if (-not (Test-Path $Workspace)) {
    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $Workspace -Force | Out-Null
    }
    Write-Status "Created workspace directory: $Workspace" "OK"
}

if (-not $DryRun) {
    $Workspace = Resolve-Path $Workspace
}

$MemoryDir = Join-Path $Workspace "memory"
$DiaryDir = Join-Path $MemoryDir "diary"
$DreamsDir = Join-Path $MemoryDir "dreams"
$TemplatesDir = Join-Path $SkillRoot "templates"

# Step 1: Create directory structure
Write-Status "Creating directory structure..." "INFO"
$dirs = @($MemoryDir, $DiaryDir, $DreamsDir)
foreach ($dir in $dirs) {
    if (-not (Test-PathSafe $dir)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
        Write-Status "Created: $dir" "OK"
    } else {
        Write-Status "Already exists: $dir" "WARN"
    }
}

# Step 2: Copy templates
if (-not $SkipTemplates) {
    Write-Status "Installing templates..." "INFO"
    $templateMap = @{
        "MEMORY.md" = (Join-Path $Workspace "MEMORY.md")
        "HEARTBEAT.md" = (Join-Path $Workspace "HEARTBEAT.md")
        "cron-inbox.md" = (Join-Path $MemoryDir "cron-inbox.md")
        "heartbeat-state.json" = (Join-Path $MemoryDir "heartbeat-state.json")
        "platform-posts.md" = (Join-Path $MemoryDir "platform-posts.md")
        "strategy-notes.md" = (Join-Path $MemoryDir "strategy-notes.md")
    }

    foreach ($srcName in $templateMap.Keys) {
        $srcPath = Join-Path $TemplatesDir $srcName
        $dstPath = $templateMap[$srcName]
        if (Test-PathSafe $srcPath) {
            if (-not (Test-PathSafe $dstPath)) {
                if (-not $DryRun) {
                    Copy-Item -Path $srcPath -Destination $dstPath -Force
                }
                Write-Status "Installed: $dstPath" "OK"
            } else {
                Write-Status "Skipped (already exists): $dstPath" "WARN"
            }
        } else {
            Write-Status "Template missing: $srcPath" "ERR"
        }
    }
} else {
    Write-Status "Skipping template installation (--skip-templates)" "WARN"
}

# Step 3: Create today's daily notes file
$Today = Get-Date -Format "yyyy-MM-dd"
$TodayFile = Join-Path $MemoryDir "$Today.md"
if (-not (Test-PathSafe $TodayFile)) {
    $dailyTemplate = Join-Path $TemplatesDir "daily-notes.md"
    if (Test-PathSafe $dailyTemplate) {
        if (-not $DryRun) {
            $content = Get-Content -Raw $dailyTemplate
            $content = $content -replace "YYYY-MM-DD", $Today
            Set-Content -Path $TodayFile -Value $content -Encoding UTF8
        }
        Write-Status "Created daily notes: $TodayFile" "OK"
    }
}

# Step 4: Validate installation
Write-Status "Validating installation..." "INFO"
$allGood = $true

if ($DryRun) {
    Write-Status "Dry run mode -- validation skipped (files would be created in normal mode)" "OK"
} else {
    $requiredFiles = @(
        (Join-Path $Workspace "MEMORY.md"),
        (Join-Path $Workspace "HEARTBEAT.md"),
        (Join-Path $MemoryDir "cron-inbox.md"),
        (Join-Path $MemoryDir "heartbeat-state.json")
    )
    foreach ($file in $requiredFiles) {
        if (Test-PathSafe $file) {
            Write-Status "OK: $file" "OK"
        } else {
            Write-Status "MISSING: $file" "ERR"
            $allGood = $false
        }
    }
}

# Step 5: Print next steps
Write-Host ""
Write-Status "Installation complete!" "OK"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit MEMORY.md with your personal context and preferences"
Write-Host "2. Edit HEARTBEAT.md to customize your periodic routines"
Write-Host "3. Add these lines to your AGENTS.md or session startup:"
Write-Host ""
Write-Host "   ## Every Session" -ForegroundColor Cyan
Write-Host "   1. Read MEMORY.md -- who you are" -ForegroundColor Cyan
Write-Host "   2. Read memory/YYYY-MM-DD.md (today + yesterday) -- recent context" -ForegroundColor Cyan
Write-Host "   3. Check memory/cron-inbox.md -- messages from other sessions" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Set up cron jobs (see scripts/setup-cron.ps1 or setup-cron.sh)"
Write-Host ""

if ($DryRun) {
    Write-Status "This was a dry run. No files were actually created." "WARN"
}

if ($allGood) { exit 0 } else { exit 1 }