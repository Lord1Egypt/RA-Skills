# Yarn 缓存迁移脚本
# 用法: powershell -File migrate-yarn.ps1 [-DstPath "E:\AppData\Local\yarn-cache"]

param(
    [string]$DstPath = "E:\AppData\Local\yarn-cache"
)

Write-Host "=== Yarn 缓存迁移 ===" -ForegroundColor Cyan
Write-Host "目标路径: $DstPath"
Write-Host ""

# Step 1: 查找 yarn 缓存路径
$yarnCachePath = "$env:LOCALAPPDATA\Yarn\Cache\v6"
if (-not (Test-Path $yarnCachePath)) {
    Write-Host "未找到 Yarn 缓存目录: $yarnCachePath" -ForegroundColor Yellow
    Write-Host "尝试查找其他位置..."
    $alt = Get-ChildItem "$env:LOCALAPPDATA\Yarn\Cache" -Directory -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
    if ($alt) {
        $yarnCachePath = $alt
        Write-Host "使用: $yarnCachePath" -ForegroundColor Cyan
    } else {
        Write-Host "无法定位 Yarn 缓存，退出" -ForegroundColor Red
        exit 1
    }
}

# Step 2: 迁移
Write-Host "--- 迁移数据 ---" -ForegroundColor Yellow
$size = (Get-ChildItem $yarnCachePath -Recurse -Force -ErrorAction SilentlyContinue |
    Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
Write-Host ("源大小: {0:N1} MB" -f ($size / 1MB))

$dstFull = Join-Path $DstPath (Split-Path $yarnCachePath -Leaf)
if (-not (Test-Path $dstFull)) {
    New-Item -ItemType Directory -Path $dstFull -Force | Out-Null
}

Copy-Item -Path "$yarnCachePath\*" -Destination $dstFull -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path $yarnCachePath -Recurse -Force -ErrorAction Stop
cmd /c "mklink /J `"$yarnCachePath`" `"$dstFull`"" 2>&1 | Out-Null

$item = Get-Item $yarnCachePath -Force -ErrorAction SilentlyContinue
if ($item -and ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
    Write-Host "Junction OK: $yarnCachePath" -ForegroundColor Green
} else {
    Write-Host "Junction 创建失败" -ForegroundColor Red
    exit 1
}

# Step 3: 配置 yarn 全局缓存路径
Write-Host ""
Write-Host "--- 配置 Yarn 缓存路径 ---" -ForegroundColor Yellow
yarn config set cache-folder (($dstFull -replace '\\', '/') -replace '^(.):', '/$1') 2>&1 | Out-Null
$newPath = yarn cache dir 2>&1
Write-Host "Yarn 缓存目录: $newPath" -ForegroundColor Cyan

Write-Host ""
Write-Host "迁移完成！" -ForegroundColor Green
