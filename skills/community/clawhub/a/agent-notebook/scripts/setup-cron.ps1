#!/usr/bin/env pwsh
# OpenClaw Memory System — Cron Job Setup (Windows / PowerShell)
# Configures scheduled tasks for memory maintenance

param(
    [string]$Workspace = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$SkillRoot = Split-Path -Parent $ScriptDir

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $colors = @{ "INFO" = "Cyan"; "OK" = "Green"; "WARN" = "Yellow"; "ERR" = "Red" }
    Write-Host "[$Status] $Message" -ForegroundColor $colors[$Status]
}

Write-Status "OpenClaw Memory System — Scheduled Task Setup" "INFO"
Write-Status "Workspace: $Workspace" "INFO"

# Check if running as admin (required for scheduled tasks)
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Status "This script requires Administrator privileges to create scheduled tasks." "ERR"
    Write-Status "Please run PowerShell as Administrator and try again." "ERR"
    exit 1
}

# Task names
$TaskPrefix = "OpenClaw-Memory"
$NightlyTask = "$TaskPrefix-NightlyExtraction"
$ReminderTask = "$TaskPrefix-DailyNotesReminder"
$HeartbeatTask = "$TaskPrefix-HeartbeatCheck"

# Remove existing tasks if present
$existing = Get-ScheduledTask -TaskName "$TaskPrefix-*" -ErrorAction SilentlyContinue
if ($existing) {
    Write-Status "Removing existing OpenClaw Memory tasks..." "WARN"
    $existing | Unregister-ScheduledTask -Confirm:$false
}

# 1. Nightly memory extraction (23:00 daily)
Write-Status "Creating nightly memory extraction task (23:00)..." "INFO"
$NightlyAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$SkillRoot\scripts\memory-extract.ps1`" -WorkspacePath `"$Workspace`"" -WorkingDirectory $Workspace
$NightlyTrigger = New-ScheduledTaskTrigger -Daily -At "23:00"
$NightlySettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName $NightlyTask -Action $NightlyAction -Trigger $NightlyTrigger -Settings $NightlySettings -Description "OpenClaw Memory System: Nightly memory extraction from daily notes to MEMORY.md" | Out-Null
Write-Status "Created: $NightlyTask" "OK"

# 2. Daily notes reminder (09:00 daily)
Write-Status "Creating daily notes reminder task (09:00)..." "INFO"
$ReminderAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Command `"Add-Content -Path '$Workspace\memory\$(Get-Date -Format yyyy-MM-dd).md' -Value \"`n## $(Get-Date -Format HH:mm) -- Daily Notes Reminder`n- Start your daily notes for today`n\"`"" -WorkingDirectory $Workspace
$ReminderTrigger = New-ScheduledTaskTrigger -Daily -At "09:00"
$ReminderSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName $ReminderTask -Action $ReminderAction -Trigger $ReminderTrigger -Settings $ReminderSettings -Description "OpenClaw Memory System: Daily notes reminder" | Out-Null
Write-Status "Created: $ReminderTask" "OK"

# 3. Heartbeat check (every 30 minutes)
Write-Status "Creating heartbeat check task (every 30 min)..." "INFO"
$HeartbeatAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$SkillRoot\scripts\heartbeat-check.ps1`" -WorkspacePath `"$Workspace`"" -WorkingDirectory $Workspace
$HeartbeatTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration (New-TimeSpan -Days 9999)
$HeartbeatSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName $HeartbeatTask -Action $HeartbeatAction -Trigger $HeartbeatTrigger -Settings $HeartbeatSettings -Description "OpenClaw Memory System: Periodic heartbeat check and cron inbox processing" | Out-Null
Write-Status "Created: $HeartbeatTask" "OK"

Write-Host ""
Write-Status "Scheduled tasks installed successfully!" "OK"
Write-Host ""
Write-Host "Scheduled tasks:" -ForegroundColor Yellow
Write-Host "  - Nightly memory extraction at 23:00  ($NightlyTask)"
Write-Host "  - Daily notes reminder at 09:00       ($ReminderTask)"
Write-Host "  - Heartbeat check every 30 minutes    ($HeartbeatTask)"
Write-Host ""
Write-Host "View with:" -ForegroundColor Cyan
Write-Host "  Get-ScheduledTask -TaskName '$TaskPrefix-*'"
Write-Host ""
Write-Host "Remove with:" -ForegroundColor Cyan
Write-Host "  Get-ScheduledTask -TaskName '$TaskPrefix-*' | Unregister-ScheduledTask -Confirm:`$false"
