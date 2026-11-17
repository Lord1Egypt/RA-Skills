#Requires -Version 5.0
<#
.SYNOPSIS
  Install agent-expression for mainstream Agents / IDEs on Windows.

.EXAMPLE
  # One-liner (PowerShell):
  irm https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.ps1 | iex

.EXAMPLE
  .\install.ps1 -Project
  .\install.ps1 -Cursor
  .\install.ps1 -Dir "D:\skills\agent-expression"
#>
[CmdletBinding()]
param(
  [switch]$All,
  [switch]$Project,
  [switch]$NoLink,
  [switch]$Pack,
  [switch]$Hermes,
  [switch]$Cursor,
  [switch]$Claude,
  [switch]$Codex,
  [switch]$Agents,
  [switch]$Home,
  [string]$Dir = ""
)

$ErrorActionPreference = "Stop"
$RepoUrl = if ($env:REPO_URL) { $env:REPO_URL } else { "https://github.com/yyh-001/agent-expression.git" }
$Branch = if ($env:BRANCH) { $env:BRANCH } else { "main" }
$SkillName = "agent-expression"

function Get-UserHome {
  if ($env:USERPROFILE) { return $env:USERPROFILE }
  return $HOME
}

function Get-MemeHome {
  if ($env:MEME_HOME) { return $env:MEME_HOME }
  if ($env:AGENT_EXPRESSION_HOME) { return $env:AGENT_EXPRESSION_HOME }
  return (Join-Path (Get-UserHome) ".agent-expression")
}

function Resolve-Abs([string]$Path) {
  $parent = Split-Path -Parent $Path
  if (-not $parent) { $parent = Get-Location }
  if (-not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
  }
  $leaf = Split-Path -Leaf $Path
  return (Join-Path (Resolve-Path -LiteralPath $parent).Path $leaf)
}

function Find-Git {
  $g = Get-Command git -ErrorAction SilentlyContinue
  if ($g) { return $g.Source }
  $candidates = @(
    "C:\Program Files\Git\cmd\git.exe",
    "C:\Program Files (x86)\Git\cmd\git.exe"
  )
  foreach ($c in $candidates) {
    if (Test-Path -LiteralPath $c) { return $c }
  }
  throw "git not found. Install Git for Windows: https://git-scm.com/download/win"
}

function Find-Python {
  foreach ($name in @("python", "py", "python3")) {
    $c = Get-Command $name -ErrorAction SilentlyContinue
    if ($c) {
      if ($name -eq "py") { return @("py", "-3") }
      return @($c.Source)
    }
  }
  return @("python")
}

function Clone-OrUpdate([string]$Dest) {
  Write-Host "==> Skill content -> $Dest"
  $git = Find-Git
  if (Test-Path -LiteralPath (Join-Path $Dest ".git")) {
    Write-Host "==> Existing git install, updating..."
    & $git -C $Dest fetch --depth 1 origin $Branch
    & $git -C $Dest checkout -q $Branch
    & $git -C $Dest reset --hard "origin/$Branch"
  } elseif (Test-Path -LiteralPath $Dest) {
    $item = Get-Item -LiteralPath $Dest -Force
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
      throw "$Dest is a link/junction; remove it or use -Dir"
    }
    Remove-Item -LiteralPath $Dest -Recurse -Force
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null
    & $git clone --depth 1 --branch $Branch $RepoUrl $Dest
  } else {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Dest) | Out-Null
    & $git clone --depth 1 --branch $Branch $RepoUrl $Dest
  }
}

function Link-Into([string]$Target, [string]$Canon) {
  if ($Target -eq $Canon) { return }
  $parent = Split-Path -Parent $Target
  if (-not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
  }
  if (Test-Path -LiteralPath $Target) {
    $item = Get-Item -LiteralPath $Target -Force
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
      Remove-Item -LiteralPath $Target -Force
    } else {
      Write-Host "==> skip (exists, not a link): $Target"
      return
    }
  }
  # Prefer directory junction (no admin). Fallback: copy.
  $ok = $false
  try {
    New-Item -ItemType Junction -Path $Target -Target $Canon -ErrorAction Stop | Out-Null
    Write-Host "==> junction $Target -> $Canon"
    $ok = $true
  } catch {
    try {
      cmd /c "mklink /J `"$Target`" `"$Canon`"" | Out-Null
      if (Test-Path -LiteralPath $Target) {
        Write-Host "==> junction $Target -> $Canon"
        $ok = $true
      }
    } catch { }
  }
  if (-not $ok) {
    Write-Host "==> junction failed, copying -> $Target"
    Copy-Item -LiteralPath $Canon -Destination $Target -Recurse -Force
  }
}

function Get-SingleDest {
  $h = Get-UserHome
  switch ($true) {
    { $Hermes } { return (Join-Path $h ".hermes\skills\media\$SkillName") }
    { $Cursor } { return (Join-Path $h ".cursor\skills\$SkillName") }
    { $Claude } { return (Join-Path $h ".claude\skills\$SkillName") }
    { $Codex }  {
      $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $h ".codex" }
      return (Join-Path $codexHome "skills\$SkillName")
    }
    { $Agents } { return (Join-Path $h ".agents\skills\$SkillName") }
    { $Home }   { return (Join-Path (Get-MemeHome) "skill") }
    { $Dir }    { return $Dir }
    default     { return (Join-Path (Get-MemeHome) "skill") }
  }
}

$single = $Hermes -or $Cursor -or $Claude -or $Codex -or $Agents -or $Home -or ($Dir -ne "")
if (-not $All -and -not $single) { $All = $true }

if ($single) {
  $Canon = Resolve-Abs (Get-SingleDest)
} else {
  $Canon = Resolve-Abs (Join-Path (Get-MemeHome) "skill")
}

Clone-OrUpdate $Canon

$Linked = @()
if (-not $NoLink -and $All -and -not $single) {
  $h = Get-UserHome
  $targets = @(
    (Join-Path $h ".agents\skills\$SkillName"),
    (Join-Path $h ".cursor\skills\$SkillName"),
    (Join-Path $h ".claude\skills\$SkillName"),
    (Join-Path $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $h ".codex" }) "skills\$SkillName")
  )
  $hermesRoot = Join-Path $h ".hermes"
  if (Test-Path -LiteralPath $hermesRoot) {
    $targets += (Join-Path $hermesRoot "skills\media\$SkillName")
  }
  if ($Project) {
    $cwd = (Get-Location).Path
    $targets += @(
      (Join-Path $cwd ".agents\skills\$SkillName"),
      (Join-Path $cwd ".cursor\skills\$SkillName"),
      (Join-Path $cwd ".claude\skills\$SkillName")
    )
  }
  foreach ($t in $targets) {
    $abs = Resolve-Abs $t
    Link-Into $abs $Canon
    $Linked += $t
  }
} elseif (-not $NoLink -and $Project) {
  $cwd = (Get-Location).Path
  foreach ($t in @(
    (Join-Path $cwd ".agents\skills\$SkillName"),
    (Join-Path $cwd ".cursor\skills\$SkillName"),
    (Join-Path $cwd ".claude\skills\$SkillName")
  )) {
    $abs = Resolve-Abs $t
    Link-Into $abs $Canon
    $Linked += $t
  }
}

$hermesPacks = Join-Path (Get-UserHome) ".hermes\meme-packs"
if (Test-Path -LiteralPath $hermesPacks) {
  $DataHome = if ($env:HERMES_HOME) { $env:HERMES_HOME } else { Join-Path (Get-UserHome) ".hermes" }
} else {
  $DataHome = Get-MemeHome
}
$PackId = if ($env:MEME_PACK_ID) { $env:MEME_PACK_ID } elseif ($env:HERMES_MEME_PACK_ID) { $env:HERMES_MEME_PACK_ID } else { "official-001" }
$PackDir = if ($env:MEME_PACK) { $env:MEME_PACK } else { Join-Path $DataHome "meme-packs\$PackId" }
$MemesDir = Join-Path $PackDir "memes"
$Bundled = Join-Path $Canon "packs\official-001"

function Deploy-BundledPack([string]$Dest, [string]$Src) {
  $srcDb = Join-Path $Src "index.db"
  $srcMemes = Join-Path $Src "memes"
  if (-not ((Test-Path -LiteralPath $srcDb) -and (Test-Path -LiteralPath $srcMemes))) {
    return $false
  }
  New-Item -ItemType Directory -Force -Path $Dest | Out-Null
  $destMemes = Join-Path $Dest "memes"
  if ($Pack -or -not (Test-Path -LiteralPath $destMemes)) {
    if (Test-Path -LiteralPath $destMemes) { Remove-Item -LiteralPath $destMemes -Recurse -Force }
    Copy-Item -LiteralPath $srcMemes -Destination $destMemes -Recurse -Force
  }
  $destDb = Join-Path $Dest "index.db"
  if ($Pack -or -not (Test-Path -LiteralPath $destDb)) {
    Copy-Item -LiteralPath $srcDb -Destination $destDb -Force
  }
  foreach ($f in @("manifest.json", "CREDITS.md")) {
    $sf = Join-Path $Src $f
    if (Test-Path -LiteralPath $sf) {
      Copy-Item -LiteralPath $sf -Destination (Join-Path $Dest $f) -Force
    }
  }
  Write-Host "==> Bundled pack ready: $Dest (index + embeddings included)"
  return $true
}

if (-not (Deploy-BundledPack $PackDir $Bundled)) {
  if ($Pack -or -not (Test-Path -LiteralPath $MemesDir)) {
    New-Item -ItemType Directory -Force -Path $MemesDir | Out-Null
    Write-Host "==> Pack dir ready: $MemesDir\<tag>\ (no bundled pack in this checkout)"
  }
}

$py = Find-Python
$pyCmd = ($py -join " ")

Write-Host ""
Write-Host "OK. agent-expression ready (Windows)."
Write-Host ""
Write-Host "  Content:  $Canon"
Write-Host "  Pack:     $PackDir"
if ($Linked.Count -gt 0) {
  Write-Host "  Linked:"
  foreach ($t in $Linked) { Write-Host "    - $t" }
}
Write-Host ""
Write-Host "Next (bundled pack already searchable):"
Write-Host "  $pyCmd `"$Canon\scripts\search-meme.py`" `"无语`" --pick"
Write-Host ""
Write-Host "Hosts: $Canon\references\hosts.md"
Write-Host "Skill: $Canon\SKILL.md"
Write-Host ""
