# ============================================================
# 稻哲纪烤羊排 Skill · Windows 一键安装
# ============================================================
# 用法：
#   powershell -c "irm https://raw.githubusercontent.com/Liubuq-sys/daozheji-grill-skill/main/install.ps1 | iex"
# ============================================================

$Repo = "https://github.com/Liubuq-sys/daozheji-grill-skill.git"
$SkillName = "daozheji-grill"
$SkillsDir = if ($env:SKILLS_DIR) { $env:SKILLS_DIR } else { "$env:USERPROFILE\.openclaw\workspace\skills" }
$SkillPath = Join-Path $SkillsDir $SkillName

Write-Host "=== 稻哲纪烤羊排 Skill · 安装 ===" -ForegroundColor Green

New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

if (Test-Path "$SkillPath\.git") {
    Write-Host "已安装，正在更新..." -ForegroundColor Yellow
    Set-Location $SkillPath
    git pull --ff-only origin master 2>$null
    if ($LASTEXITCODE -ne 0) { git pull --ff-only origin main 2>$null }
    Write-Host "更新完成！" -ForegroundColor Green
} else {
    Write-Host "正在下载 skill..." -ForegroundColor Cyan
    $TmpDir = Join-Path $env:TEMP "daozheji-skill-$([System.Guid]::NewGuid())"
    git clone --depth 1 $Repo $TmpDir 2>$null

    if (Test-Path $SkillPath) {
        Remove-Item -Recurse -Force $SkillPath
    }
    $SourcePath = Join-Path $TmpDir $SkillName
    if (Test-Path $SourcePath) {
        Copy-Item -Recurse $SourcePath $SkillPath
    } else {
        Copy-Item -Recurse $TmpDir $SkillPath
    }
    Remove-Item -Recurse -Force $TmpDir -ErrorAction SilentlyContinue
    Write-Host "安装完成！" -ForegroundColor Green
}

# 配置计划任务（每天 3:07）
$TaskName = "DaozhejiGrillSkillUpdate"
$Existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if (-not $Existing) {
    $Action = New-ScheduledTaskAction -Execute "powershell" -Argument "-c `"cd '$SkillPath'; git pull --ff-only origin main 2>`$null; if (`$LASTEXITCODE -ne 0) { git pull --ff-only origin master 2>`$null }`"" -WorkingDirectory $SkillPath
    $Trigger = New-ScheduledTaskTrigger -Daily -At 03:07
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Description "稻哲纪烤羊排Skill自动更新" | Out-Null
    Write-Host "自动更新已配置（每天 3:07）" -ForegroundColor Green
}

Write-Host ""
Write-Host "Skill 路径: $SkillPath" -ForegroundColor White
Write-Host "已就绪！现在对 AI 说「稻哲纪烤羊排」即可触发。" -ForegroundColor Green
