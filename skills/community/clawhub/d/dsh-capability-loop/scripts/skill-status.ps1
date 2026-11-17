# skill-status.ps1 — 检查本 skill 版本状态（商店优先 + 本地源回退；只提示，不自动更新）
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File .\skill-status.ps1 [-Workspace <工作区>] [-Source <源目录>] [-MarketData <市场数据目录>] [-Strict]
# 退出码：0 = 已是最新/无法对比；1 = -Strict 且商店或源有新版本 / 文件有差异；2 = 参数错误
# 设计原则：
#   - 上架 skill 商店后，**更新由商店负责**（安装/更新/回滚都在商店 UI 完成）；
#   - 本脚本只读检查「商店记录里的 latestVersion」与「本地 version.json」，给出手动操作提示；
#   - 绝不清空/覆盖用户修改，绝不后台推送（见 references/80-evolution.md §8）。
[CmdletBinding()]
param(
    [string]$Workspace = '',
    [string]$Source = '',
    [string]$MarketData = '',
    [switch]$Strict
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version 2.0

$installed = Split-Path -Parent $PSScriptRoot
if (-not $Workspace) { $Workspace = (Get-Location).Path }
if (-not $Source) { $Source = Join-Path $Workspace 'tools\capability-loop\skill\dsh-capability-loop' }
if (-not $MarketData) { $MarketData = Join-Path $env:USERPROFILE '.dsh\storages\@montersy123\dsh-skill-market\data' }

function Read-Utf8 {
    param([string]$Path)
    try { return [System.IO.File]::ReadAllText($Path, (New-Object System.Text.UTF8Encoding($false))) } catch { return '' }
}
function Get-Version {
    param([string]$Dir)
    $f = Join-Path $Dir 'version.json'
    if (-not (Test-Path -LiteralPath $f)) { return '' }
    $t = Read-Utf8 $f
    $m = [regex]::Match($t, '"version"\s*:\s*"([^"]+)"')
    if ($m.Success) { return $m.Groups[1].Value }
    return ''
}
function Convert-Semver {
    param([string]$V)
    if ($V -match '^(\d+)\.(\d+)\.(\d+)') { return @([int]$matches[1], [int]$matches[2], [int]$matches[3]) }
    return @(-1, -1, -1)
}
function Compare-Ver {
    param([string]$A, [string]$B)
    $x = Convert-Semver $A
    $y = Convert-Semver $B
    for ($i = 0; $i -lt 3; $i++) {
        if ($x[$i] -gt $y[$i]) { return 1 }
        if ($x[$i] -lt $y[$i]) { return -1 }
    }
    return 0
}
function Normalize-Dir {
    param([string]$P)
    if (-not $P) { return '' }
    return ($P.Trim().TrimEnd('\').TrimEnd('/')).ToLowerInvariant()
}

$vInstalled = Get-Version $installed
$skillName = $vInstalled
$verText = Read-Utf8 (Join-Path $installed 'version.json')
$nm = [regex]::Match($verText, '"name"\s*:\s*"([^"]+)"')
if ($nm.Success) { $skillName = $nm.Groups[1].Value } else { $skillName = Split-Path -Leaf $installed }
$installedDirName = Split-Path -Leaf $installed

# ---------- 商店记录 ----------
$storeFound = $false
$storeOrigin = ''
$storeVersion = ''
$storeLatest = ''
$storeId = ''
$storeDetail = ''
$panel = Join-Path $MarketData 'panel.json'
$installedJson = Join-Path $MarketData 'installed.json'
if (Test-Path -LiteralPath $panel) {
    try {
        $pj = (Read-Utf8 $panel) | ConvertFrom-Json
        foreach ($e in @($pj.installed)) {
            if (-not $e) { continue }
            try {
                $regName = ''
                $entName = ''
                $entDir = ''
                $p1 = $e.PSObject.Properties['registeredAs']
                if ($p1 -and $p1.Value) { $regName = [string]$p1.Value }
                $p2 = $e.PSObject.Properties['name']
                if ($p2 -and $p2.Value) { $entName = [string]$p2.Value }
                $p3 = $e.PSObject.Properties['directory']
                if ($p3 -and $p3.Value) { $entDir = [string]$p3.Value }
                $hit = $false
                if ($regName -ne '' -and $regName -eq $skillName) { $hit = $true }
                elseif ($entName -ne '' -and $entName -eq $skillName) { $hit = $true }
                elseif ($entDir -ne '' -and (Normalize-Dir $entDir) -eq (Normalize-Dir $installed)) { $hit = $true }
            } catch { continue }
            if ($hit) {
                $storeFound = $true
                $po = $e.PSObject.Properties['origin']; if ($po -and $po.Value) { $storeOrigin = [string]$po.Value }
                $pv = $e.PSObject.Properties['version']; if ($pv -and $pv.Value) { $storeVersion = [string]$pv.Value }
                $pl = $e.PSObject.Properties['latestVersion']; if ($pl -and $pl.Value) { $storeLatest = [string]$pl.Value }
                $pid2 = $e.PSObject.Properties['id']; if ($pid2 -and $pid2.Value) { $storeId = [string]$pid2.Value }
                $storeDetail = 'origin=' + $storeOrigin + ' version=' + $storeVersion + ' latest=' + $storeLatest
                break
            }
        }
    } catch { $storeDetail = 'panel.json 解析失败：' + $_.Exception.Message }
}
if (-not $storeFound -and (Test-Path -LiteralPath $installedJson)) {
    try {
        $ij = (Read-Utf8 $installedJson) | ConvertFrom-Json
        $prop = $ij.PSObject.Properties[$installedDirName]
        if ($prop -and $prop.Value) {
            $storeFound = $true
            $storeOrigin = 'market'
            $storeVersion = [string]$prop.Value.version
            $storeLatest = ''
            $storeDetail = 'installed.json 记录：version=' + $storeVersion + '（latest 未知，需刷新商店面板）'
        }
    } catch { }
}

# ---------- 本地源（开发/手工安装场景） ----------
$sourceExists = Test-Path -LiteralPath $Source
$vSource = ''
$diffFiles = New-Object System.Collections.ArrayList
$extraFiles = New-Object System.Collections.ArrayList
if ($sourceExists) {
    $vSource = Get-Version $Source
    foreach ($f in @(Get-ChildItem -LiteralPath $Source -Recurse -File -ErrorAction SilentlyContinue)) {
        $rel = $f.FullName.Replace($Source + '\', '')
        $dst = Join-Path $installed $rel
        if (-not (Test-Path -LiteralPath $dst)) { [void]$extraFiles.Add($rel); continue }
        $h1 = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
        $h2 = (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash
        if ($h1 -ne $h2) { [void]$diffFiles.Add($rel) }
    }
}

# ---------- 输出 ----------
Write-Host ''
Write-Host '==== skill 版本状态 ====' -ForegroundColor Cyan
Write-Host ('安装目录：' + $installed)
Write-Host ('技能名  ：' + $skillName)
Write-Host ('安装版本：' + $(if ($vInstalled -ne '') { $vInstalled } else { '（无 version.json）' }))
if ($installed -match '\\tools\\capability-loop\\') {
    Write-Host '提示：当前脚本从「源目录」运行，本脚本的“安装版”会变成源目录自身（源 vs 源，差异恒 0）。' -ForegroundColor Yellow
    Write-Host '      要对比安装版/商店版，请运行 ~\.dsh\skills\dsh-capability-loop\scripts\skill-status.ps1。' -ForegroundColor Yellow
}

Write-Host ''
Write-Host '-- 商店（skill market） --' -ForegroundColor DarkCyan
if ($storeFound) {
    Write-Host ('  记录：' + $storeDetail)
    if ($storeId -ne '') { Write-Host ('  id  ：' + $storeId) }
    if ($storeOrigin -eq 'manual') {
        Write-Host '  说明：当前是手工安装，商店尚未接管；上架后由商店负责更新。' -ForegroundColor Yellow
    } elseif ($storeLatest -eq '') {
        Write-Host '  说明：商店未返回 latestVersion（刷新商店面板后再看，或在商店里点「检查更新」）。' -ForegroundColor Yellow
    }
} else {
    Write-Host '  未找到商店记录（未安装/未上架，或市场数据目录不同）。' -ForegroundColor Gray
}

Write-Host ''
Write-Host '-- 本地源（开发对照） --' -ForegroundColor DarkCyan
if (-not $sourceExists) {
    Write-Host ('  源目录：' + $Source + '（不存在；若是商店安装版，这是正常状态）') -ForegroundColor Gray
} else {
    Write-Host ('  源目录：' + $Source)
    Write-Host ('  源版本：' + $(if ($vSource -ne '') { $vSource } else { '（无 version.json）' }))
    if ($diffFiles.Count -gt 0) { Write-Host ('  有差异文件：' + [string]$diffFiles.Count) -ForegroundColor Yellow }
    if ($extraFiles.Count -gt 0) { Write-Host ('  源中新增/安装版缺失：' + [string]$extraFiles.Count) -ForegroundColor Yellow }
}

# ---------- 结论 ----------
$storeNewer = $false
if ($storeLatest -ne '' -and $vInstalled -ne '') {
    if ((Compare-Ver $storeLatest $vInstalled) -gt 0) { $storeNewer = $true }
}
$sourceNewer = $false
if ($sourceExists -and $vSource -ne '' -and $vInstalled -ne '') {
    if ((Compare-Ver $vSource $vInstalled) -gt 0) { $sourceNewer = $true }
}

Write-Host ''
if ($storeNewer) {
    Write-Host ('结论：商店有新版本 ' + $vInstalled + ' → ' + $storeLatest + '（请在「技能市场」里点更新；本脚本不自动更新）') -ForegroundColor Yellow
} elseif ($storeFound -and $storeLatest -ne '' -and -not $storeNewer) {
    Write-Host '结论：商店版本已是安装版本（或更新）。' -ForegroundColor Green
} elseif ($sourceNewer) {
    Write-Host ('结论：本地源有新版本 ' + $vInstalled + ' → ' + $vSource + '（开发模式；上架后请用商店更新）') -ForegroundColor Yellow
    Write-Host '更新方式（仅开发机，手动）：' -ForegroundColor Gray
    Write-Host ('  Copy-Item -Path "' + $Source + '\*" -Destination "' + $installed + '" -Recurse -Force') -ForegroundColor Gray
} elseif ($diffFiles.Count -gt 0 -or $extraFiles.Count -gt 0) {
    Write-Host '结论：版本号相同但文件有差异（本地修改或未同步），不自动覆盖。' -ForegroundColor Yellow
} elseif ($vInstalled -ne '') {
    Write-Host ('结论：没有可用的新版本信息；安装版本为 ' + $vInstalled + '。') -ForegroundColor Green
} else {
    Write-Host '结论：无法判断版本（缺 version.json）。' -ForegroundColor Yellow
}

if ($storeFound -and $storeOrigin -eq 'market') {
    Write-Host '提示：商店安装版请用商店 UI 更新/回滚，不要手工覆盖目录，否则商店记录会与实际不一致。' -ForegroundColor Gray
}

# 最新 CHANGELOG（优先源，其次安装版）
$changelogDir = ''
if ($sourceExists -and $vSource -ne '') { $changelogDir = $Source } else { $changelogDir = $installed }
$cl = Join-Path $changelogDir 'CHANGELOG.md'
if (Test-Path -LiteralPath $cl) {
    $m = [regex]::Match((Read-Utf8 $cl), '(?m)^## (.+)$')
    if ($m.Success) { Write-Host ('最新 CHANGELOG：' + $m.Groups[1].Value.Trim()) -ForegroundColor Gray }
}

if ($Strict -and ($storeNewer -or $sourceNewer -or $diffFiles.Count -gt 0 -or $extraFiles.Count -gt 0)) { exit 1 }
exit 0
