# desktop-notify 一键全局配置 (Windows)
# 作用：把"每次回答完自动发通知"规则写入用户级全局记忆 ~/.workbuddy/MEMORY.md
# 运行一次即可，之后所有对话全局生效。可重复运行，不会重复写入。

$ErrorActionPreference = "Stop"

# 1. 定位路径
$skillDir  = Split-Path -Parent $PSScriptRoot        # ...\skills\desktop-notify
$notifyPs1 = Join-Path $skillDir "scripts\notify.ps1"
$memoryDir = Join-Path $env:USERPROFILE ".workbuddy"
$memoryMd  = Join-Path $memoryDir "MEMORY.md"

# 2. 确保目录/文件存在
if (-not (Test-Path $memoryDir)) { New-Item -ItemType Directory -Path $memoryDir -Force | Out-Null }
if (-not (Test-Path $memoryMd))  { New-Item -ItemType File -Path $memoryMd -Force | Out-Null }

# 3. 幂等检查：已配置则跳过
$marker  = "<!-- desktop-notify-auto -->"
$content = Get-Content -Path $memoryMd -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
if ($null -eq $content) { $content = "" }
if ($content.Contains($marker)) {
    Write-Host "[skip] 全局通知规则已存在，无需重复配置。"
    Write-Host "位置: $memoryMd"
    exit 0
}

# 4. 追加规则
$rule = @"

$marker
## 自动通知规则 (desktop-notify)
- 每次回答完成后，必须运行以下命令触发桌面通知（提示音 + Toast）：
  ``PowerShell -File "$notifyPs1" -Message "任务完成，请查看" -Title "WorkBuddy"``
- 此规则全局生效（所有项目 / 所有对话）。
"@

Add-Content -Path $memoryMd -Value $rule -Encoding UTF8

Write-Host "[ok] 全局通知规则已写入。"
Write-Host "位置: $memoryMd"
Write-Host "通知脚本: $notifyPs1"
Write-Host "重启对话或新开会话后，AI 每次回答完都会自动发通知。"
