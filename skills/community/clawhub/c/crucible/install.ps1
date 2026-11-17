# crucible-skill installer for Claude Code (Windows PowerShell)
# Usage: .\install.ps1 [-Uninstall]

param(
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"
$ClaudeDir = if ($env:CLAUDE_DIR) { $env:CLAUDE_DIR } else { "$env:USERPROFILE\.claude" }
$SkillName = "crucible"
$SkillDir  = "$ClaudeDir\skills\ccg\$SkillName"
$CmdFile   = "$ClaudeDir\commands\ccg\$SkillName.md"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Write-Info  { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn  { param($msg) Write-Host "[!!] $msg" -ForegroundColor Yellow }
function Write-Err   { param($msg) Write-Host "[XX] $msg" -ForegroundColor Red }

if ($Uninstall) {
    Write-Host "Uninstalling crucible skill..."
    if (Test-Path $SkillDir) {
        Remove-Item -Recurse -Force $SkillDir
        Write-Info "Removed $SkillDir"
    } else {
        Write-Warn "$SkillDir not found, skipping"
    }
    if (Test-Path $CmdFile) {
        Remove-Item -Force $CmdFile
        Write-Info "Removed $CmdFile"
    } else {
        Write-Warn "$CmdFile not found, skipping"
    }
    Write-Info "Uninstall complete."
    exit 0
}

Write-Host ""
Write-Host "Installing Crucible..." -ForegroundColor Cyan
Write-Host ""

# Pre-flight check
if (-not (Test-Path "$ScriptDir\skill")) {
    Write-Err "Cannot find skill\ directory. Run this script from the crucible-skill package root."
    exit 1
}

# Create target directories
New-Item -ItemType Directory -Force -Path $SkillDir | Out-Null
New-Item -ItemType Directory -Force -Path "$ClaudeDir\commands\ccg" | Out-Null

# Copy skill content
Copy-Item -Recurse -Force "$ScriptDir\skill\*" $SkillDir
Write-Info "Installed skill files -> $SkillDir"

# Copy command file
Copy-Item -Force "$ScriptDir\command\$SkillName.md" $CmdFile
Write-Info "Installed command  -> $CmdFile"

Write-Host ""
Write-Info "Installation complete!"
Write-Host ""
Write-Host "  Restart Claude Code or run /skills to see: ccg:crucible"
Write-Host ""
Write-Host "  Usage:"
Write-Host "    /ccg:crucible <task>          # Full 8-stage delivery"
Write-Host "    /ccg:crucible --dev <task>    # Dev + self-review (most used)"
Write-Host "    /ccg:crucible --help          # All modes"
Write-Host ""
