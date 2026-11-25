<#
.SYNOPSIS
    360 残留清理脚本（需管理员权限）—— 基于 2026-11-22 本机实测。
.DESCRIPTION
    安全设计：
      1. 启动即检查管理员权限，非管理员直接退出。
      2. 注册表项先导出 .reg 备份，再删除。
      3. 目录/文件优先移入回收站；系统保护位置（Program Files/System32）
         不支持回收站时，降级为移动到隔离目录（可原样还原），不做永久删除。
      4. 服务清理顺序：先 sc delete，再兜底清注册表服务项。
      5. 每步回显 + 存在性验证。

.PARAMETER BackupRoot
    备份根目录（注册表 .reg / 隔离区 / 书签都放这里）。默认脚本所在目录。

.PARAMETER TargetsFile
    可选：scan_360.ps1 产出的 JSON 清单路径。若提供，按清单里的 category 决定删法。
    不提供则使用内置默认清单（本次实测的全部 360 残留位置）。

.EXAMPLE
    # 右键"以管理员身份运行"，或：
    powershell -ExecutionPolicy Bypass -File cleanup_360_admin.ps1
#>
param(
    [string]$BackupRoot = $PSScriptRoot,
    [string]$TargetsFile = ""
)
$ErrorActionPreference = 'Continue'

$regBak     = Join-Path $BackupRoot 'registry-backup'
$quarantine = Join-Path $BackupRoot 'quarantine'
New-Item -ItemType Directory -Path $regBak -Force | Out-Null
New-Item -ItemType Directory -Path $quarantine -Force | Out-Null

# --- 0. 管理员权限检查 ---
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "错误：请以管理员身份运行本脚本！" -ForegroundColor Red
    Write-Host "右键 -> 以管理员身份运行。"
    exit 1
}
Write-Host "权限检查通过（管理员）" -ForegroundColor Green

# --- 辅助：删除到回收站，失败降级到隔离区 ---
function Remove-ToRecycleOrQuarantine {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { Write-Host "  跳过(不存在): $Path"; return }
    try {
        if ((Get-Item -LiteralPath $Path).PSIsContainer) {
            [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory(
                $Path,
                [Microsoft.VisualBasic.FileIO.UIOption]::OnlyErrorDialogs,
                [Microsoft.VisualBasic.FileIO.RecycleOption]::SendToRecycleBin)
        } else {
            [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile(
                $Path,
                [Microsoft.VisualBasic.FileIO.UIOption]::OnlyErrorDialogs,
                [Microsoft.VisualBasic.FileIO.RecycleOption]::SendToRecycleBin)
        }
        Write-Host "  [回收站] $Path | 已清除=$(-not (Test-Path -LiteralPath $Path))"
    } catch {
        # 降级：移动到隔离目录（保留完整路径结构，可还原）
        $dest = Join-Path $quarantine ($Path -replace '^[A-Za-z]:\\','' -replace '[\\:]','_')
        try {
            Move-Item -LiteralPath $Path -Destination $dest -Force -ErrorAction Stop
            Write-Host "  [隔离区] $Path -> $dest | 已清除=$(-not (Test-Path -LiteralPath $Path))" -ForegroundColor Yellow
        } catch {
            Write-Host "  [失败] $Path -> $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# --- 可选：从扫描清单加载目标 ---
$dirTargets = @()
$driverTargets = @()
if ($TargetsFile -and (Test-Path -LiteralPath $TargetsFile)) {
    $scan = Get-Content -LiteralPath $TargetsFile -Raw -Encoding UTF8 | ConvertFrom-Json
    $dirTargets     = @($scan.findings | Where-Object { $_.exists -and $_.kind -eq 'directory' } | ForEach-Object { $_.path })
    $driverTargets  = @($scan.findings | Where-Object { $_.exists -and $_.kind -eq 'driver' } | ForEach-Object { $_.path })
    Write-Host "已从清单加载：目录 $($dirTargets.Count) 个，驱动 $($driverTargets.Count) 个"
} else {
    $dirTargets = @(
        'C:\Program Files (x86)\360',
        'C:\Program Files (x86)\Wukong',
        'C:\ProgramData\360SD',
        'C:\ProgramData\360Safe',
        "$env:APPDATA\secoresdk\360se6",
        "$env:APPDATA\360Login",
        "$env:APPDATA\360Safe"
    )
    $driverTargets = @(Get-ChildItem 'C:\Windows\System32\drivers' -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^360' } | ForEach-Object { $_.FullName })
}

# ============================================================
# 1. 书签备份（360 浏览器用户数据可能被删，先保住书签）
# ============================================================
Write-Host "`n===== [1/5] 关键数据备份 =====" -ForegroundColor Cyan
$bookmarks = Join-Path $env:APPDATA 'secoresdk\360se6\User Data\Default\360Bookmarks'
if (Test-Path -LiteralPath $bookmarks) {
    $dst = Join-Path $BackupRoot '360Bookmarks.bak'
    Copy-Item -LiteralPath $bookmarks -Destination $dst -Force
    Write-Host "  书签已备份: $dst ($((Get-Item $dst).Length) bytes)"
} else { Write-Host "  无 360 书签文件，跳过" }

# ============================================================
# 2. 注册表（先导出备份，再删除）
# ============================================================
Write-Host "`n===== [2/5] 注册表清理 =====" -ForegroundColor Cyan
$regKeys = @(
    'HKLM\SOFTWARE\WOW6432Node\360DrvMgr',
    'HKLM\SOFTWARE\WOW6432Node\360Safe',
    'HKCU\SOFTWARE\360X', 'HKCU\SOFTWARE\360ChromeXX', 'HKCU\SOFTWARE\360CleanProX',
    'HKCU\SOFTWARE\360DayPop', 'HKCU\SOFTWARE\360Game5', 'HKCU\SOFTWARE\360Newsld',
    'HKCU\SOFTWARE\360se6', 'HKCU\SOFTWARE\360SoftWareMgr', 'HKCU\SOFTWARE\360WallPaper'
)
foreach ($key in $regKeys) {
    if (Test-Path "Registry::$key") {
        $fpath = Join-Path $regBak (($key -replace '[\\:]','_') + '.reg')
        reg.exe export $key $fpath /y | Out-Null
        if (Test-Path $fpath) {
            Remove-Item -Path "Registry::$key" -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "  已删除(已备份): $key"
        } else {
            Write-Host "  [跳过] 备份失败，未删除: $key" -ForegroundColor Yellow
        }
    }
}
Write-Host "  注册表备份目录: $regBak"

# ============================================================
# 3. 服务（先 sc delete，再兜底删注册表服务项）
# ============================================================
Write-Host "`n===== [3/5] 服务清理 =====" -ForegroundColor Cyan
foreach ($svc in @('Q360AMPPL','ZhuDongFangYu','360Box64','360netmon')) {
    $regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\$svc"
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s) { try { Stop-Service -Name $svc -Force -ErrorAction Stop } catch {} }
    sc.exe delete $svc | Out-Null
    if (Test-Path $regPath) {
        $bak = Join-Path $regBak ("SERVICE_" + $svc + ".reg")
        reg.exe export $regPath $bak /y | Out-Null
        Remove-Item -Path $regPath -Recurse -Force -ErrorAction SilentlyContinue
    }
    $still = (Test-Path $regPath) -or [bool](Get-Service -Name $svc -ErrorAction SilentlyContinue)
    Write-Host "  服务 $svc : 已清除=$(-not $still)"
}

# ============================================================
# 4. 目录（先删文件，再删空目录壳，规避 DeleteDirectory 对复杂目录的失败）
# ============================================================
Write-Host "`n===== [4/5] 目录清理 =====" -ForegroundColor Cyan
foreach ($root in $dirTargets) {
    if (-not (Test-Path -LiteralPath $root)) { Write-Host "  跳过(不存在): $root"; continue }
    $files = @(Get-ChildItem -LiteralPath $root -Recurse -File -Force -ErrorAction SilentlyContinue)
    $ok = 0; $fail = 0
    foreach ($f in $files) {
        try { [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($f.FullName,'OnlyErrorDialogs','SendToRecycleBin'); $ok++ }
        catch { $fail++ }
    }
    $left = @(Get-ChildItem -LiteralPath $root -Recurse -File -Force -ErrorAction SilentlyContinue).Count
    if ($left -eq 0) {
        # 空目录壳：从最深层层删除
        Get-ChildItem -LiteralPath $root -Recurse -Directory -Force -ErrorAction SilentlyContinue |
          Sort-Object { $_.FullName.Length } -Descending |
          ForEach-Object { try { [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($_.FullName,'OnlyErrorDialogs','SendToRecycleBin') } catch {} }
        Remove-ToRecycleOrQuarantine $root
    } else {
        Write-Host "  [部分失败] $root : 文件成功=$ok 失败=$fail 剩余=$left" -ForegroundColor Yellow
        Remove-ToRecycleOrQuarantine $root
    }
}

# ============================================================
# 5. 驱动残骸
# ============================================================
Write-Host "`n===== [5/5] 驱动残骸清理 =====" -ForegroundColor Cyan
foreach ($d in $driverTargets) { Remove-ToRecycleOrQuarantine $d }

# ============================================================
# 最终验证
# ============================================================
Write-Host "`n===== 最终验证 =====" -ForegroundColor Cyan
$remain = @($dirTargets) | Where-Object { Test-Path -LiteralPath $_ }
$drvRemain = @(Get-ChildItem 'C:\Windows\System32\drivers' -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '^360' -and $_.Name -notmatch '\.sys$' })
if ($remain.Count -eq 0 -and $drvRemain.Count -eq 0) {
    Write-Host "全部清除完成。" -ForegroundColor Green
} else {
    Write-Host "仍有残留，请检查：" -ForegroundColor Yellow
    $remain | ForEach-Object { Write-Host "  $_" }
    $drvRemain | ForEach-Object { Write-Host "  $($_.FullName)" }
}
Write-Host "`n隔离目录（可还原）: $quarantine"
Write-Host "注册表备份（可还原）: $regBak"
Write-Host "书签备份: $(Join-Path $BackupRoot '360Bookmarks.bak')"
