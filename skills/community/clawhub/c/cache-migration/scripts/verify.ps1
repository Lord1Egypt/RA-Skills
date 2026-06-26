# verify.ps1 — 验证 Junction 迁移状态
# 用法:
#   powershell -File verify.ps1                          # 自动扫描所有已知应用
#   powershell -File verify.ps1 -Paths "C:\...", "C:\..." # 验证指定路径列表
#   powershell -File verify.ps1 -ScanDir "E:\AppData"    # 扫描目标目录，显示数据量统计

param(
    [string[]]$Paths,          # 可选：指定要验证的路径列表
    [string]$ScanDir = ""      # 可选：目标目录，用于统计迁移后数据量
)

Write-Host "=== Junction 迁移验证 ===" -ForegroundColor Cyan
Write-Host ""

$allOk = $true
$checked = 0
$junctionCount = 0

function Test-JunctionPoint([string]$Path) {
    $item = Get-Item $Path -Force -ErrorAction SilentlyContinue
    return ($item -and ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint))
}

function Get-JunctionTarget([string]$Path) {
    try {
        $info = cmd /c "fsutil reparsepoint query `"$Path`"" 2>&1
        $match = $info | Select-String "Print Name:\s*(.+)" | Select-Object -First 1
        if ($match) { return $match.Matches[0].Groups[1].Value.Trim() }
    } catch {}
    return ""
}

function Show-JunctionStatus {
    param([string]$Label, [string]$Path)
    $script:checked++
    if (-not (Test-Path $Path -ErrorAction SilentlyContinue)) {
        Write-Host ("  {0,-35} 未迁移（路径不存在）" -f $Label) -ForegroundColor Gray
        return
    }
    $ok = Test-JunctionPoint $Path
    if ($ok) {
        $target = Get-JunctionTarget $Path
        $targetStr = if ($target) { " -> $target" } else { "" }
        Write-Host ("  {0,-35} Junction ✓$targetStr" -f $Label) -ForegroundColor Green
        $script:junctionCount++
    } else {
        Write-Host ("  {0,-35} 实体目录（未迁移）" -f $Label) -ForegroundColor Yellow
    }
}

# ── 模式一：验证用户指定路径 ──────────────────────────────────
if ($Paths -and $Paths.Count -gt 0) {
    Write-Host "--- 验证指定路径 ---" -ForegroundColor Yellow
    foreach ($p in $Paths) {
        $label = Split-Path $p -Leaf
        Show-JunctionStatus $label $p
    }
    Write-Host ""
}
# ── 模式二：自动检查所有已知应用 ──────────────────────────────
else {
    # ---------- 代码编辑器 ----------
    Write-Host "--- 代码编辑器 ---" -ForegroundColor Yellow
    Show-JunctionStatus "VSCode Cache" "$env:APPDATA\Code\Cache"
    Show-JunctionStatus "VSCode CachedData" "$env:APPDATA\Code\CachedData"
    Show-JunctionStatus "VSCode CachedExtensionVSIXs" "$env:APPDATA\Code\CachedExtensionVSIXs"
    Show-JunctionStatus "VSCode Code Cache" "$env:APPDATA\Code\Code Cache"
    Show-JunctionStatus "VSCode GPUCache" "$env:APPDATA\Code\GPUCache"
    Show-JunctionStatus "VSCode DawnGraphiteCache" "$env:APPDATA\Code\DawnGraphiteCache"
    Show-JunctionStatus "VSCode DawnWebGPUCache" "$env:APPDATA\Code\DawnWebGPUCache"
    Show-JunctionStatus "VSCode CachedProfilesData" "$env:APPDATA\Code\CachedProfilesData"
    Show-JunctionStatus "VSCode CachedConfigurations" "$env:APPDATA\Code\CachedConfigurations"
    Show-JunctionStatus "VSCode Extensions" "$env:USERPROFILE\.vscode\extensions"

    Show-JunctionStatus "Cursor Cache" "$env:APPDATA\Cursor\Cache"
    Show-JunctionStatus "Cursor Extensions" "$env:USERPROFILE\.cursor\extensions"

    Write-Host ""
    # ---------- JS/Node 包管理器 ----------
    Write-Host "--- JS/Node 包管理器 ---" -ForegroundColor Yellow
    Show-JunctionStatus "Yarn Cache" "$env:LOCALAPPDATA\Yarn\Cache\v6"
    Show-JunctionStatus "npm Cache" "$env:APPDATA\npm-cache"
    Show-JunctionStatus "pnpm Cache" "$env:LOCALAPPDATA\pnpm\cache"
    Show-JunctionStatus "pnpm Store" "$env:LOCALAPPDATA\pnpm\store"

    Write-Host ""
    # ---------- Python ----------
    Write-Host "--- Python ---" -ForegroundColor Yellow
    Show-JunctionStatus "pip Cache" "$env:LOCALAPPDATA\pip\Cache"
    Show-JunctionStatus "uv Cache" "$env:LOCALAPPDATA\uv\cache"
    Show-JunctionStatus "Poetry Cache" "$env:LOCALAPPDATA\pypoetry\Cache"
    Show-JunctionStatus "conda pkgs" "$env:USERPROFILE\anaconda3\pkgs"

    Write-Host ""
    # ---------- JVM 构建工具 ----------
    Write-Host "--- JVM 构建工具 ---" -ForegroundColor Yellow
    Show-JunctionStatus "Gradle Caches" "$env:USERPROFILE\.gradle\caches"
    Show-JunctionStatus "Gradle Wrapper" "$env:USERPROFILE\.gradle\wrapper"
    Show-JunctionStatus "Maven Repository" "$env:USERPROFILE\.m2\repository"
    Show-JunctionStatus "Maven Wrapper" "$env:USERPROFILE\.m2\wrapper"
    Show-JunctionStatus "NuGet Cache" "$env:LOCALAPPDATA\NuGet\Cache"
    Show-JunctionStatus "NuGet HTTP Cache" "$env:LOCALAPPDATA\NuGet\v3-cache"

    Write-Host ""
    # ---------- JetBrains IDE ----------
    Write-Host "--- JetBrains IDE ---" -ForegroundColor Yellow
    $jbLocalBase = "$env:LOCALAPPDATA\JetBrains"
    $jbRoamBase  = "$env:APPDATA\JetBrains"
    if (Test-Path $jbLocalBase) {
        Get-ChildItem $jbLocalBase -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            Show-JunctionStatus "JetBrains\$($_.Name)" $_.FullName
        }
    }
    if (Test-Path $jbRoamBase) {
        Get-ChildItem $jbRoamBase -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            Show-JunctionStatus "JetBrains(Roam)\$($_.Name)" $_.FullName
        }
    }

    Write-Host ""
    # ---------- 容器/运行时 ----------
    Write-Host "--- 容器/运行时 ---" -ForegroundColor Yellow
    Show-JunctionStatus "Docker Desktop Data" "$env:LOCALAPPDATA\Docker"
    Show-JunctionStatus "Docker Hub Config" "$env:USERPROFILE\.docker"
    Show-JunctionStatus "Rust Cargo Registry" "$env:USERPROFILE\.cargo\registry"
    Show-JunctionStatus "Rust Cargo Git" "$env:USERPROFILE\.cargo\git"
    Show-JunctionStatus "Go Module Cache" "$env:LOCALAPPDATA\go\pkg\mod"
    Show-JunctionStatus "Ruby Gems" "$env:USERPROFILE\.gem"

    Write-Host ""
    # ---------- 浏览器 ----------
    Write-Host "--- 浏览器 ---" -ForegroundColor Yellow
    Show-JunctionStatus "Chrome Cache" "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache"
    Show-JunctionStatus "Edge Cache" "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache"
}

# ── 目标目录数据量统计 ─────────────────────────────────────────
if ($ScanDir -and (Test-Path $ScanDir)) {
    Write-Host "--- 目标目录数据量 ($ScanDir) ---" -ForegroundColor Yellow
    Get-ChildItem $ScanDir -Recurse -Directory -Depth 2 -ErrorAction SilentlyContinue |
        Where-Object { (Get-ChildItem $_.FullName -ErrorAction SilentlyContinue).Count -gt 0 } |
        ForEach-Object {
            $sz = (Get-ChildItem $_.FullName -Recurse -Force -ErrorAction SilentlyContinue |
                   Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
            if ($sz -gt 1MB) {
                [PSCustomObject]@{ SizeMB=[math]::Round($sz/1MB,1); Path=$_.FullName }
            }
        } | Sort-Object SizeMB -Descending | Select-Object -First 20 |
        ForEach-Object {
            Write-Host ("  {0,8:N1} MB  {1}" -f $_.SizeMB, $_.Path) -ForegroundColor Cyan
        }
    Write-Host ""
}

# ── 汇总 ──────────────────────────────────────────────────────
Write-Host "--- 汇总 ---" -ForegroundColor Cyan
Write-Host ("  检查路径数: $checked  |  已迁移 Junction: $junctionCount") -ForegroundColor White
Write-Host ""
if ($junctionCount -eq 0 -and $checked -gt 0) {
    Write-Host "  尚未进行任何迁移。可先运行 scan-usage.ps1 查看可迁移目录。" -ForegroundColor Yellow
} elseif ($checked -gt 0) {
    Write-Host "  已有 $junctionCount 个目录完成 Junction 迁移。" -ForegroundColor Green
}
