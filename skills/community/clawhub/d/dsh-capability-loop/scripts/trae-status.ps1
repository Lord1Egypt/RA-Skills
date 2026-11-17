# trae-status.ps1 — 检查本机 Trae 与交接包状态（只读）
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File .\trae-status.ps1 [-Workspace <工程根>] [-HandoffRoot <目录>] [-TraeExe <path>] [-RequireMatch] [-Strict]
# 退出码：0 = 检查完成（默认）；1 = -Strict 且有未完成交接包 / -RequireMatch 且当前 Trae 工程不是目标工程；2 = 参数错误
# 说明：本脚本只读，不唤起 Trae、不改交接包；「当前工程」来自 Trae 自己的窗口状态（storage.json），避免改到别的项目。
[CmdletBinding()]
param(
    [string]$Workspace = '',
    [string]$HandoffRoot = '',
    [string]$TraeExe = '',
    [switch]$RequireMatch,
    [switch]$Strict
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version 2.0

if (-not $Workspace) { $Workspace = (Get-Location).Path }
if (-not (Test-Path -LiteralPath $Workspace -PathType Container)) {
    Write-Host ('[FAIL] 工程目录不存在：' + $Workspace) -ForegroundColor Red
    exit 2
}
$Workspace = (Resolve-Path -LiteralPath $Workspace).Path
if (-not $HandoffRoot) { $HandoffRoot = Join-Path $Workspace 'docs\handoff' }

$rows = New-Object System.Collections.ArrayList
function Add-R {
    param([string]$Item, [string]$Status, [string]$Detail)
    $o = New-Object psobject
    $o | Add-Member -MemberType NoteProperty -Name Item -Value $Item
    $o | Add-Member -MemberType NoteProperty -Name Status -Value $Status
    $o | Add-Member -MemberType NoteProperty -Name Detail -Value $Detail
    [void]$rows.Add($o)
}

# 1) Trae CLI 探测（顺序：显式 → PATH → 注册表 → 常见路径）
$cli = ''
if ($TraeExe) {
    if (Test-Path -LiteralPath $TraeExe) { $cli = (Resolve-Path -LiteralPath $TraeExe).Path }
} else {
    foreach ($n in @('trae-cn', 'trae')) {
        $c = Get-Command $n -ErrorAction SilentlyContinue
        if ($c -and $c.Source) { $cli = $c.Source; break }
    }
    if ($cli -eq '') {
        $regRoots = @('HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*')
        foreach ($rr in $regRoots) {
            foreach ($k in @(Get-ItemProperty $rr -ErrorAction SilentlyContinue)) {
                if ($k.DisplayName -match 'Trae') {
                    if ($k.InstallLocation) {
                        $cand = Join-Path $k.InstallLocation 'bin\trae-cn.cmd'
                        if (Test-Path -LiteralPath $cand) { $cli = $cand; break }
                    }
                }
            }
            if ($cli -ne '') { break }
        }
    }
    if ($cli -eq '') {
        foreach ($cand in @((Join-Path $env:LOCALAPPDATA 'Programs\Trae CN\bin\trae-cn.cmd'), 'D:\Trae CN\bin\trae-cn.cmd', (Join-Path $env:ProgramFiles 'Trae CN\bin\trae-cn.cmd'))) {
            if ($cand -and (Test-Path -LiteralPath $cand)) { $cli = $cand; break }
        }
    }
}
if ($cli -ne '') { Add-R 'Trae CLI' 'PASS' $cli } else { Add-R 'Trae CLI' 'WARN' '未探测到（可用 -TraeExe 指定）' }

# 2) Trae 进程
$procs = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match 'Trae' })
if ($procs.Count -gt 0) {
    $ids = @($procs | ForEach-Object { [string]$_.Id }) -join ', '
    Add-R 'Trae 进程' 'PASS' ([string]$procs.Count + ' 个（PID ' + $ids + '）')
} else {
    Add-R 'Trae 进程' 'WARN' '未运行（唤起前先确认安装）'
}

# 3) Trae 当前工程是否为目标工程（防改错项目）
$matchState = 'UNKNOWN'
$matchDetail = ''
function Convert-FileUriToPath {
    param([string]$Uri)
    if (-not $Uri) { return '' }
    $p = $Uri
    if ($p -match '^file:///') { $p = $p.Substring(8) }
    $p = [System.Uri]::UnescapeDataString($p)
    $p = $p -replace '/', '\'
    if ($p -match '^\\[A-Za-z]:') { $p = $p.Substring(1) }
    return $p
}
function Normalize-PathText {
    param([string]$Path)
    if (-not $Path) { return '' }
    $x = $Path.Trim().TrimEnd('\').TrimEnd('/')
    return $x.ToLowerInvariant()
}
$activeFolder = ''
$recentFolders = New-Object System.Collections.ArrayList
$traeStore = Join-Path $env:APPDATA 'Trae CN\User\globalStorage\storage.json'
if (Test-Path -LiteralPath $traeStore) {
    try {
        $st = (Get-Content -LiteralPath $traeStore -Raw -Encoding UTF8) | ConvertFrom-Json
        if ($st.windowsState -and $st.windowsState.lastActiveWindow -and $st.windowsState.lastActiveWindow.folder) {
            $activeFolder = Convert-FileUriToPath $st.windowsState.lastActiveWindow.folder
        }
        if ($st.backupWorkspaces -and $st.backupWorkspaces.folders) {
            foreach ($f in @($st.backupWorkspaces.folders)) {
                if ($f.folderUri) {
                    $fp = Convert-FileUriToPath $f.folderUri
                    if ($fp -ne '' -and -not ($recentFolders -contains $fp)) { [void]$recentFolders.Add($fp) }
                }
            }
        }
    } catch { }
}
if ($activeFolder -eq '') {
    $wsRoot = Join-Path $env:APPDATA 'Trae CN\User\workspaceStorage'
    if (Test-Path -LiteralPath $wsRoot) {
        $wj = @(Get-ChildItem -LiteralPath $wsRoot -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $p = Join-Path $_.FullName 'workspace.json'
            if (Test-Path -LiteralPath $p) { $_ }
        } | Sort-Object LastWriteTime -Descending | Select-Object -First 1)
        if ($wj.Count -gt 0) {
            try {
                $w = (Get-Content -LiteralPath (Join-Path $wj[0].FullName 'workspace.json') -Raw -Encoding UTF8) | ConvertFrom-Json
                $u = ''
                if ($w.folder) { $u = $w.folder } elseif ($w.workspace) { $u = $w.workspace }
                if ($u -ne '') { $activeFolder = Convert-FileUriToPath $u }
            } catch { }
        }
    }
}
$targetNorm = Normalize-PathText $Workspace
$activeNorm = Normalize-PathText $activeFolder
if ($activeFolder -ne '') {
    if ($activeNorm -eq $targetNorm) {
        $matchState = 'MATCH'
        $matchDetail = ('Trae 当前工程 = 目标工程：' + $activeFolder)
    } else {
        $matchState = 'MISMATCH'
        $matchDetail = ('Trae 当前工程 = ' + $activeFolder + '；目标 = ' + $Workspace + '。先切到目标工程或重新 open-in-trae，否则可能改错项目。')
    }
} else {
    $matchState = 'UNKNOWN'
    $matchDetail = '读不到 Trae 当前工程（storage.json 缺失/未打开工程）。交接前请先 open-in-trae.ps1 -Workspace 打开目标工程，或人工确认。'
}
if ($matchState -eq 'MATCH') { Add-R 'Trae 当前工程' 'PASS' $matchDetail }
elseif ($matchState -eq 'MISMATCH') { Add-R 'Trae 当前工程' 'FAIL' $matchDetail }
else { Add-R 'Trae 当前工程' 'WARN' $matchDetail }
if ($recentFolders.Count -gt 0) {
    $recentText = @($recentFolders | Select-Object -First 5) -join ' | '
    Add-R 'Trae 最近工程' 'PASS' $recentText
}

# 4) feature-handoff 能力
$fh = Join-Path $env:USERPROFILE '.dsh\skills\feature-handoff\SKILL.md'
if (Test-Path -LiteralPath $fh) { Add-R 'feature-handoff skill' 'PASS' '已安装' } else { Add-R 'feature-handoff skill' 'WARN' '未安装（交接流程走不通）' }

# 5) 交接包状态
$pkgCount = 0
$incomplete = 0
if (Test-Path -LiteralPath $HandoffRoot) {
    $dirs = @(Get-ChildItem -LiteralPath $HandoffRoot -Directory -ErrorAction SilentlyContinue)
    $pkgCount = $dirs.Count
    foreach ($d in $dirs) {
        $brief = Test-Path -LiteralPath (Join-Path $d.FullName 'brief.md')
        $tasks = Test-Path -LiteralPath (Join-Path $d.FullName 'tasks.md')
        $acc = Test-Path -LiteralPath (Join-Path $d.FullName 'acceptance.md')
        $rec = Join-Path $d.FullName 'record.md'
        $hasRec = Test-Path -LiteralPath $rec
        $evidence = @(Get-ChildItem -LiteralPath (Join-Path $d.FullName 'evidence') -File -ErrorAction SilentlyContinue)
        $conclusion = ''
        if ($hasRec) {
            $rt = [System.IO.File]::ReadAllText($rec, (New-Object System.Text.UTF8Encoding($false)))
            $m = [regex]::Match($rt, '(?m)结论[：:]\s*([^\r\n|]+)')
            if ($m.Success) { $conclusion = $m.Groups[1].Value.Trim() }
        }
        $todo = @()
        if (-not $brief) { $todo += '缺 brief' }
        if (-not $tasks) { $todo += '缺 tasks' }
        if (-not $acc) { $todo += '缺 acceptance' }
        if ($evidence.Count -eq 0) { $todo += '无 evidence' }
        if (-not $hasRec) { $todo += '缺 record' }
        elseif ($conclusion -match '待填|待验收|待确认') { $todo += '结论未定' }
        $status = 'PASS'
        if ($todo.Count -gt 0) { $status = 'WARN'; $incomplete++ }
        $detail = 'brief=' + [string]$brief + ' tasks=' + [string]$tasks + ' acc=' + [string]$acc + ' evidence=' + [string]$evidence.Count + ' record=' + [string]$hasRec
        if ($conclusion -ne '') { $detail += ' 结论=' + $conclusion }
        if ($todo.Count -gt 0) { $detail += ' 待办=' + ($todo -join '/') }
        Add-R ('交接包 ' + $d.Name) $status $detail
    }
    if ($pkgCount -eq 0) { Add-R '交接包' 'WARN' ('目录存在但为空：' + $HandoffRoot) }
} else {
    Add-R '交接包' 'WARN' ('无交接包目录：' + $HandoffRoot + '（用 feature-handoff 的 new-handoff.ps1 创建）')
}

# 5) 输出
Write-Host ''
Write-Host '==== Trae / 交接状态 ====' -ForegroundColor Cyan
Write-Host ('工程：' + $Workspace)
Write-Host ''
foreach ($r in $rows) {
    $color = 'Gray'
    if ($r.Status -eq 'PASS') { $color = 'Green' } elseif ($r.Status -eq 'WARN') { $color = 'Yellow' }
    Write-Host ('  [' + $r.Status + '] ' + $r.Item + ' — ' + $r.Detail) -ForegroundColor $color
}
Write-Host ''
if ($matchState -eq 'MATCH') {
    Write-Host '下一步：当前 Trae 工程与目标一致，可 new-handoff.ps1 建包 → 填 brief/tasks/acceptance（record 验收后填）→ check-handoff -Stage prepare → open-in-trae → collect-evidence → record.md → check-handoff -Stage deliver' -ForegroundColor Gray
} elseif ($matchState -eq 'MISMATCH') {
    Write-Host '下一步（先纠正工程再交接）：' -ForegroundColor Yellow
    Write-Host ('  powershell -File "<feature-handoff>\scripts\open-in-trae.ps1" -Workspace "' + $Workspace + '" -File docs/handoff/<slug>/tasks.md') -ForegroundColor Gray
    Write-Host '  然后重跑本脚本确认「Trae 当前工程 = MATCH」；未确认前不要让 Trae 改代码。' -ForegroundColor Gray
} else {
    Write-Host '下一步（工程未知）：先用 open-in-trae.ps1 -Workspace 打开目标工程，或人工确认 Trae 窗口里打开的是目标目录。' -ForegroundColor Yellow
}
if ($pkgCount -eq 0) {
    Write-Host '交接包：暂无，按 feature-handoff 的 new-handoff.ps1 创建。' -ForegroundColor Gray
} elseif ($incomplete -gt 0) {
    Write-Host ('交接包：有 ' + [string]$incomplete + ' 个包未完成，按上面「待办」补齐后跑 check-handoff -Stage prepare/deliver。') -ForegroundColor Gray
} else {
    Write-Host '交接包：全部结构完整，可跑 check-handoff -Stage deliver 并出验收结论。' -ForegroundColor Gray
}
Write-Host ''
Write-Host '说明：本脚本只读，不唤起 Trae、不改交接包；工程匹配来自 Trae 自己的 storage.json 窗口状态。' -ForegroundColor Gray

if ($RequireMatch -and $matchState -ne 'MATCH') { exit 1 }
if ($Strict -and $incomplete -gt 0) { exit 1 }
exit 0
