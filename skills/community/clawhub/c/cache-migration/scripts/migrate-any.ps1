# 通用 Junction 迁移脚本
# 用法: powershell -File migrate-any.ps1
#
# 参数:
#   -SourcePath  : C 盘原始路径（例: "C:\Users\Administrator\AppData\Roaming\Code\Cache")
#   -DstPath     : 目标路径（例: "E:\AppData\Local\VSCode\Cache"）
#
# 示例:
#   powershell -File migrate-any.ps1 -SourcePath "C:\Users\Administrator\AppData\Roaming\Code\Cache" -DstPath "E:\AppData\Local\VSCode\Cache"
#   powershell -File migrate-any.ps1 -SourcePath "$env:USERPROFILE\.vscode\extensions" -DstPath "E:\AppData\Local\VSCode\extensions"

param(
    [Parameter(Mandatory=$true)]
    [string]$SourcePath,
    [Parameter(Mandatory=$true)]
    [string]$DstPath
)

$SourcePath = $ExecutionContext.InvokeCommand.ExpandString($SourcePath)
$DstPath = $ExecutionContext.InvokeCommand.ExpandString($DstPath)

Write-Host "=== 通用 Junction 迁移脚本 ===" -ForegroundColor Cyan
Write-Host "源路径:   $SourcePath"
Write-Host "目标路径: $DstPath"
Write-Host ""

# Step 1: 检查源路径
if (-not (Test-Path $SourcePath)) {
    Write-Host "错误: 源路径不存在: $SourcePath" -ForegroundColor Red
    exit 1
}

# Step 2: 复制数据
Write-Host "--- Step 1: 复制数据 ---" -ForegroundColor Yellow

$parentDst = Split-Path $DstPath -Parent
if (-not (Test-Path $parentDst)) {
    New-Item -ItemType Directory -Path $parentDst -Force | Out-Null
    Write-Host "已创建父目录: $parentDst"
}

$srcSize = (Get-ChildItem $SourcePath -Recurse -Force -ErrorAction SilentlyContinue |
    Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
Write-Host ("源大小: {0:N1} MB" -f ($srcSize / 1MB))

if (-not (Test-Path $DstPath)) {
    New-Item -ItemType Directory -Path $DstPath -Force | Out-Null
}
Write-Host "正在复制..."
Copy-Item -Path "$SourcePath\*" -Destination $DstPath -Recurse -Force -ErrorAction Stop

$dstSize = (Get-ChildItem $DstPath -Recurse -Force -ErrorAction SilentlyContinue |
    Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
Write-Host ("复制完成: {0:N1} MB" -f ($dstSize / 1MB)) -ForegroundColor Green

# Step 3: 删除原目录
Write-Host ""
Write-Host "--- Step 2: 删除原目录并创建 Junction ---" -ForegroundColor Yellow
Remove-Item -Path $SourcePath -Recurse -Force -ErrorAction Stop
Write-Host "原目录已删除"

# Step 4: 创建 Junction
$output = cmd /c "mklink /J `"$SourcePath`" `"$DstPath`"" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Junction 创建成功: $SourcePath -> $DstPath" -ForegroundColor Green
} else {
    Write-Host "Junction 创建失败: $output" -ForegroundColor Red
    exit 1
}

# Step 5: 验证
Write-Host ""
Write-Host "--- Step 3: 验证 ---" -ForegroundColor Yellow
$item = Get-Item $SourcePath -Force -ErrorAction SilentlyContinue
if ($item -and ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
    Write-Host "验证通过: $SourcePath 是 Junction" -ForegroundColor Green
    Write-Host ""
    Write-Host "迁移完成！" -ForegroundColor Green
} else {
    Write-Host "验证失败: $SourcePath 不是 Junction" -ForegroundColor Red
    exit 1
}
