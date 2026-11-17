#Requires -Version 5.1
<#
.SYNOPSIS
  english-memory-method installer v3 (Windows / PowerShell 5.1+)

.DESCRIPTION
  One-liner (installs to EVERY detected agent platform):
    irm https://raw.githubusercontent.com/yxdwind/english-memory-method/main/install.ps1 | iex

  Install to specific platform(s), comma-separated:
    ./install.ps1 -Target "claude,codex,trae"

  Supported platform aliases:
    autoclaw, openclaw, agents, claude, codex, trae, lingma, comate,
    codebuddy, windsurf, continue, roo, kimi, qoder, qwen, workbuddy, minimax

  Install to a custom directory:
    ./install.ps1 -Target "D:\my-skills"
#>
param([string]$Target = "")

$ErrorActionPreference = "Stop"
try {
  [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
} catch { }

$Repo   = "yxdwind/english-memory-method"
$Branch = "main"
$Skill  = "english-memory-method"
$Raw    = "https://raw.githubusercontent.com/$Repo/$Branch"
$Files  = @("SKILL.md", "assets/plan-template.html")

# download sources with fallback: raw -> jsdelivr CDN (China-friendly)
$Sources = @(
  "https://raw.githubusercontent.com/$Repo/$Branch",
  "https://cdn.jsdelivr.net/gh/$Repo@$Branch"
)

function Fetch-File([string]$rel, [string]$out) {
  foreach ($s in $Sources) {
    try {
      Invoke-WebRequest -Uri "$s/$rel" -OutFile $out -UseBasicParsing -TimeoutSec 25
      Write-Host "  [OK] $rel  <- $s"
      return $true
    } catch { }
  }
  Write-Warning "  [FAIL] $rel (all sources)"
  return $false
}

# platform alias -> skills dir (relative to $HOME)
$PlatformMap = [ordered]@{
  "autoclaw"  = ".openclaw-autoclaw\skills"
  "openclaw"  = ".openclaw\skills"
  "agents"    = ".agents\skills"
  "claude"    = ".claude\skills"
  "codex"     = ".codex\skills"
  "trae"      = ".trae\skills"
  "lingma"    = ".lingma\skills"
  "comate"    = ".comate\skills"
  "codebuddy" = ".codebuddy\skills"
  "windsurf"  = ".windsurf\skills"
  "continue"  = ".continue\skills"
  "roo"       = ".roo\skills"
  "kimi"      = ".kimi-code\skills"
  "qoder"     = ".qoderwork\skills"
  "qwen"      = ".qwenworkcn\skills"
  "workbuddy" = ".workbuddy\skills"
  "minimax"   = ".minimax\skills"
}

function Install-To([string]$Dir) {
  $Dest = Join-Path $Dir $Skill
  foreach ($f in $Files) {
    $out = Join-Path $Dest ($f -replace "/", "\")
    New-Item -ItemType Directory -Force -Path (Split-Path $out -Parent) | Out-Null
    if (-not (Fetch-File $f $out)) { throw "download failed: $f" }
  }
  $head = (Get-Content (Join-Path $Dest "SKILL.md") -TotalCount 5 -Encoding UTF8) -join " "
  if ($head -notmatch "english-memory-method") { Write-Warning "  SKILL.md content check failed - verify manually" }
  return $Dest
}

$dests = New-Object System.Collections.Generic.List[string]

if ($Target) {
  if (Test-Path $Target) {
    # explicit filesystem path
    Write-Host "Custom target: $Target"
    $dests.Add((Install-To $Target))
  }
  else {
    # platform alias list, comma separated
    foreach ($name in ($Target -split "," | ForEach-Object { $_.Trim().ToLower() })) {
      if ($PlatformMap.Contains($name)) {
        $dir = Join-Path $HOME $PlatformMap[$name]
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "Platform [$name] -> $dir"
        $dests.Add((Install-To $dir))
      } else {
        Write-Warning "Unknown platform alias: $name (see header for the list)"
      }
    }
  }
}
else {
  # auto mode: install to EVERY detected platform
  Write-Host "Auto-detecting agent platforms..."
  $found = 0
  foreach ($name in $PlatformMap.Keys) {
    $dir = Join-Path $HOME $PlatformMap[$name]
    if (Test-Path $dir) {
      $found++
      Write-Host "Platform [$name] detected -> $dir"
      $dests.Add((Install-To $dir))
    }
  }
  if ($found -eq 0) {
    Write-Warning "No known platform found - falling back to Claude Code default"
    $dir = Join-Path $HOME $PlatformMap["claude"]
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $dests.Add((Install-To $dir))
  }
}

Write-Host ""
Write-Host "[DONE] $Skill installed to $($dests.Count) location(s):"
foreach ($d in $dests) { Write-Host "  - $d" }
Write-Host ""
Write-Host "Trigger: give your agent an English article and say"
Write-Host '"chu bei song fang an" / "memorization plan" / "memory tricks".'
Write-Host "No restart needed on platforms with a skills watcher; otherwise"
Write-Host "start a new conversation first."
