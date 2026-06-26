# npm 缓存迁移脚本
# 用法: powershell -File migrate-npm.ps1 [-DstPath "E:\AppData\Roaming\npm-cache"]

param(
    [string]$DstPath = "E:\AppData\Roaming\npm-cache"
)

Write-Host "=== npm 缓存迁移 ===" -ForegroundColor Cyan
Write-Host "目标路径: $DstPath"
Write-Host ""

$npmCachePath = "$env:APPDATA\npm-cache"
if (-not (Test-Path $npmCachePath)) {
    Write-Host "未找到 npm 缓存目录: $npmCachePath" -ForegroundColor Red
    exit 1
}

# Step 1: 迁移
Write-Host "--- 迁移数据 ---" -ForegroundColor Yellow
$size = (Get-ChildItem $npmCachePath -Recurse -Force -ErrorAction SilentlyContinue |
    Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
Write-Host ("源大小: {0:N1} MB" -f ($size / 1MB))

if (-not (Test-Path $DstPath)) {
    New-Item -ItemType Directory -Path $DstPath -Force | Out-Null
}

Copy-Item -Path "$npmCachePath\*" -Destination $DstPath -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path $npmCachePath -Recurse -Force -ErrorAction Stop
cmd /c "mklink /J `"$npmCachePath`" `"$DstPath`"" 2>&1 | Out-Null

$item = Get-Item $npmCachePath -Force -ErrorAction SilentlyContinue
if ($item -and ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
    Write-Host "Junction OK: $npmCachePath" -ForegroundColor Green
} else {
    Write-Host "Junction 创建失败" -ForegroundColor Red
    exit 1
}

# Step 2: 配置 npm 缓存路径
Write-Host ""
Write-Host "--- 配置 npm 缓存路径 ---" -ForegroundColor Yellow
npm config set cache $DstPath 2>&1 | Out-Null
$newCache = npm config get cache 2>&1
Write-Host "npm 缓存目录: $newCache" -ForegroundColor Cyan

Write-Host ""
Write-Host "迁移完成！" -ForegroundColor Green
