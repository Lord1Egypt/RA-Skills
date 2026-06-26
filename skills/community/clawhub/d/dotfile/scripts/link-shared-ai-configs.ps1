# link-shared-ai-configs.ps1
# Create Symbolic Links for shared AI configs folders to Claude and Gemini directories

$AgentDir = Join-Path $Home ".agents"
$ClaudeDir = Join-Path $Home ".claude"
$CodexDir = Join-Path $Home ".codex"
$GeminiDir = Join-Path $Home ".gemini"
$AntigravityDir = Join-Path $GeminiDir "antigravity"

# Exit if shared directory doesn't exist
if (-not (Test-Path $AgentDir -PathType Container)) {
    exit
}

function Link-Folder {
    param (
        [string]$FolderName,
        [string]$DstPath
    )

    $SrcPath = Join-Path $AgentDir $FolderName

    if (Test-Path $DstPath) {
        # Check if already linked to correct target
        $Item = Get-Item $DstPath -Force
        if ($Item.LinkType -eq 'Junction' -or $Item.LinkType -eq 'SymbolicLink') {
            if ($Item.Target -eq $SrcPath) {
                Write-Host "✓ Already linked: $DstPath" -ForegroundColor Green
                return
            }
        }
        
        # Backup existing folder/file
        $Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $DstName = Split-Path $DstPath -Leaf
        $DstParent = Split-Path $DstPath -Parent
        $BackupDir = Join-Path $DstParent ".bak"
        $BackupPath = Join-Path $BackupDir "$DstName-$Timestamp"
        
        if (-not (Test-Path $BackupDir)) {
            New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
        }
        
        Write-Host "⚠️ Backing up: $DstPath → $BackupPath" -ForegroundColor Yellow
        try {
            Move-Item -Path $DstPath -Destination $BackupPath -Force -ErrorAction Stop
        } catch {
            Write-Host "❌ Failed to backup $DstPath. Skipping." -ForegroundColor Red
            return
        }
    }

    # Ensure parent directory of destination exists
    $DstParent = Split-Path $DstPath -Parent
    if (-not (Test-Path $DstParent)) {
        New-Item -ItemType Directory -Path $DstParent -Force | Out-Null
    }

    Write-Host "→ Creating Symbolic Link: $DstPath → $SrcPath" -ForegroundColor Cyan
    try {
        New-Item -ItemType SymbolicLink -Path $DstPath -Target $SrcPath -Force | Out-Null
    } catch {
        Write-Host "❌ Failed to create symbolic link: $DstPath" -ForegroundColor Red
    }
}

# Move Codex system skills into shared skills before linking
function Merge-MoveDirectory {
    param(
        [Parameter(Mandatory = $true)][string]$SrcDir,
        [Parameter(Mandatory = $true)][string]$DstDir
    )

    if (-not (Test-Path $SrcDir -PathType Container)) {
        return
    }

    if (-not (Test-Path $DstDir -PathType Container)) {
        New-Item -ItemType Directory -Path $DstDir -Force | Out-Null
    }

    Get-ChildItem -LiteralPath $SrcDir -Force | ForEach-Object {
        $SrcItem = $_.FullName
        $DstItem = Join-Path $DstDir $_.Name

        if ($_.PSIsContainer) {
            if (Test-Path $DstItem -PathType Container) {
                Merge-MoveDirectory -SrcDir $SrcItem -DstDir $DstItem
                try {
                    Remove-Item -LiteralPath $SrcItem -Force -ErrorAction SilentlyContinue
                } catch {
                    # ignore
                }
            } else {
                Move-Item -LiteralPath $SrcItem -Destination $DstItem -Force
            }
        } else {
            Move-Item -LiteralPath $SrcItem -Destination $DstItem -Force
        }
    }

    try {
        if (-not (Get-ChildItem -LiteralPath $SrcDir -Force -ErrorAction SilentlyContinue)) {
            Remove-Item -LiteralPath $SrcDir -Force -ErrorAction SilentlyContinue
        }
    } catch {
        # ignore
    }
}

# Ensure shared skills contains Codex system skills (so they survive the skills junction)
$CodexSkillsDir = Join-Path $CodexDir "skills"
$CodexSystemSkillsDir = Join-Path $CodexSkillsDir ".system"
$AgentSkillsDir = Join-Path $AgentDir "skills"
$AgentSystemSkillsDir = Join-Path $AgentSkillsDir ".system"
Merge-MoveDirectory -SrcDir $CodexSystemSkillsDir -DstDir $AgentSystemSkillsDir

# Skills
Link-Folder -FolderName "skills" -DstPath (Join-Path $AntigravityDir "skills")
Link-Folder -FolderName "skills" -DstPath (Join-Path $ClaudeDir "skills")
Link-Folder -FolderName "skills" -DstPath (Join-Path $CodexDir "skills")

# Rules
Link-Folder -FolderName "rules" -DstPath (Join-Path $ClaudeDir "rules")

# Agents -> Claude agents, Gemini global_workflows
Link-Folder -FolderName "agents" -DstPath (Join-Path $AntigravityDir "global_workflows")
Link-Folder -FolderName "agents" -DstPath (Join-Path $ClaudeDir "agents")
Link-Folder -FolderName "agents" -DstPath (Join-Path $GeminiDir "agents")
