# ai-news-digest skill installer (Claude Code, Windows PowerShell)
# Usage: powershell -c "irm https://raw.githubusercontent.com/yan1sanjin/ai-news-digest/main/install.ps1 | iex"

$ErrorActionPreference = "Stop"

$SkillName = "ai-news-digest"
$SkillDir = "$env:USERPROFILE\.claude\skills\$SkillName"
$SkillUrl = "https://raw.githubusercontent.com/yan1sanjin/ai-news-digest/main/SKILL.md"

# Check Claude Code presence
if (-not (Test-Path "$env:USERPROFILE\.claude")) {
    Write-Host "Error: $env:USERPROFILE\.claude not found. Is Claude Code installed?" -ForegroundColor Red
    Write-Host "       Install from: https://docs.claude.com/claude-code" -ForegroundColor Red
    exit 1
}

# Create skill dir
New-Item -ItemType Directory -Force -Path $SkillDir | Out-Null

# Download SKILL.md
Write-Host "Downloading ai-news-digest skill..."
try {
    Invoke-WebRequest -Uri $SkillUrl -OutFile "$SkillDir\SKILL.md" -UseBasicParsing
} catch {
    Write-Host "Error: failed to download from $SkillUrl" -ForegroundColor Red
    Write-Host "       Check your network or download SKILL.md manually from:" -ForegroundColor Red
    Write-Host "       https://github.com/yan1sanjin/ai-news-digest" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[OK] Installed to $SkillDir\SKILL.md" -ForegroundColor Green
Write-Host ""
Write-Host "Try it in Claude Code:"
Write-Host "  Generate today's AI news digest"
Write-Host "  (Or in Chinese: 生成今日 AI 日报)"
Write-Host ""
Write-Host "Output will be saved to $env:USERPROFILE\Desktop\ai-news\YYYY-MM-DD.md"
Write-Host ""
