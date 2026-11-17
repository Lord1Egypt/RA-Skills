# publish.ps1 - Publish grok-geo to SkillHub
# Usage:
#   .\publish.ps1 -Changelog "first release"
#   .\publish.ps1 -Slug geo-agent-skills -Changelog "upgrade to 1.1.0"
#   .\publish.ps1 -DryRun

param(
    [string]$Slug,
    [string]$Changelog = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$skillDir = $PSScriptRoot
$tmpDir = Join-Path $env:TEMP "skillhub-publish-$(Get-Random)"

# SkillHub CLI path
$cliScript = Join-Path $env:USERPROFILE ".skillhub\skills_store_cli.py"
if (-not (Test-Path $cliScript)) {
    Write-Host "[ERROR] SkillHub CLI not found at $cliScript" -ForegroundColor Red
    exit 1
}

# Refresh PATH so python is available
$machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
$env:PATH = "$machinePath;$userPath"
$env:PYTHONIOENCODING = "utf-8"

# File patterns that SkillHub rejects
$excludePatterns = @("VERSION", "*.bak", "*.tpl")

function Find-ExcludedFiles {
    $files = @()
    foreach ($pattern in $excludePatterns) {
        $found = Get-ChildItem -Path $skillDir -Recurse -File -Filter $pattern
        $files += $found
    }
    return $files
}

function Move-ExcludedFilesToTemp($Files, $TempDir) {
    foreach ($file in $Files) {
        $relativePath = $file.FullName.Substring($skillDir.Length + 1)
        $dest = Join-Path $TempDir $relativePath
        $destDir = Split-Path $dest -Parent
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        Move-Item -Path $file.FullName -Destination $dest -Force
    }
}

function Restore-ExcludedFiles($TempDir, $SkillDir) {
    if (-not (Test-Path $TempDir)) { return }
    Get-ChildItem -Path $TempDir -Recurse -File | ForEach-Object {
        $relativePath = $_.FullName.Substring($TempDir.Length + 1)
        $dest = Join-Path $SkillDir $relativePath
        $destDir = Split-Path $dest -Parent
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        Move-Item -Path $_.FullName -Destination $dest -Force
    }
    Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
}

# --- Main ---

$excludedFiles = Find-ExcludedFiles

if ($excludedFiles.Count -gt 0) {
    Write-Host "[INFO] Moving $($excludedFiles.Count) unsupported files to temp..." -ForegroundColor Yellow
    foreach ($f in $excludedFiles) {
        $rel = $f.FullName.Substring($skillDir.Length + 1)
        Write-Host "  -> $rel" -ForegroundColor DarkGray
    }
    New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null
    Move-ExcludedFilesToTemp $excludedFiles $tmpDir
}

$slugModified = $false
$skillMd = Join-Path $skillDir "SKILL.md"
$originalContent = $null

try {
    # Temporarily modify slug if specified
    if ($Slug) {
        $originalContent = Get-Content $skillMd -Raw -Encoding UTF8
        $modifiedContent = $originalContent -replace '(?m)^slug:.*$', "slug: $Slug"
        [System.IO.File]::WriteAllText($skillMd, $modifiedContent, [System.Text.Encoding]::UTF8)
        $slugModified = $true
    }

    # Build args
    $pythonArgs = @($cliScript, "publish", $skillDir)
    if ($DryRun) {
        $pythonArgs += "--dry-run"
    }
    if ($Changelog -and -not $DryRun) {
        $pythonArgs += "--changelog"
        $pythonArgs += $Changelog
    }

    Write-Host "[INFO] Publishing..." -ForegroundColor Cyan
    & python @pythonArgs

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Done!" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Exit code: $LASTEXITCODE" -ForegroundColor Red
    }
}
finally {
    # Restore slug
    if ($slugModified -and $originalContent) {
        [System.IO.File]::WriteAllText($skillMd, $originalContent, [System.Text.Encoding]::UTF8)
    }

    # Always restore excluded files
    if ($excludedFiles.Count -gt 0) {
        Write-Host "[INFO] Restoring $($excludedFiles.Count) files..." -ForegroundColor Yellow
        Restore-ExcludedFiles $tmpDir $skillDir
    }
}