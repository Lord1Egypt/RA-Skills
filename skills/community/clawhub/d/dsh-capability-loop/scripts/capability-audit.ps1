# capability-audit.ps1 — DSH 能力体检（只读）
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File .\capability-audit.ps1 [-DshHome <dir>] [-Workspace <dir>] [-AppSrc <dir>] [-Source <dir>] [-OutFile <md>] [-Strict] [-Json]
# 退出码：0 = 无 FAIL（或未指定 -Strict）；1 = 有 FAIL 且指定 -Strict；2 = 参数/环境错误
[CmdletBinding()]
param(
    [string]$DshHome = '',
    [string]$Workspace = '',
    [string]$AppSrc = '',
    [string]$Source = '',
    [string]$OutFile = '',
    [switch]$Strict,
    [switch]$Json
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version 2.0

if (-not $DshHome) {
    if ($env:DSH_HOME) { $DshHome = $env:DSH_HOME } else { $DshHome = Join-Path $env:USERPROFILE '.dsh' }
}
if (-not $Workspace) { $Workspace = (Get-Location).Path }

$results = New-Object System.Collections.ArrayList
function Add-R {
    param([string]$Group, [string]$Item, [string]$Status, [string]$Detail)
    $o = New-Object psobject
    $o | Add-Member -MemberType NoteProperty -Name Group -Value $Group
    $o | Add-Member -MemberType NoteProperty -Name Item -Value $Item
    $o | Add-Member -MemberType NoteProperty -Name Status -Value $Status
    $o | Add-Member -MemberType NoteProperty -Name Detail -Value $Detail
    [void]$results.Add($o)
}
function Read-Utf8 {
    param([string]$Path)
    try { return [System.IO.File]::ReadAllText($Path, (New-Object System.Text.UTF8Encoding($false))) } catch { return '' }
}
function Get-FrontmatterDescription {
    param([string]$Text)
    $m = [regex]::Match($Text, '(?s)\A---\s*\r?\n(.*?)\r?\n---')
    if (-not $m.Success) { return '' }
    $lines = $m.Groups[1].Value -split "`r?`n"
    $out = New-Object System.Collections.ArrayList
    $inBlock = $false
    foreach ($ln in $lines) {
        if (-not $inBlock) {
            if ($ln -match '^description:\s*(.*)$') {
                $v = $matches[1].Trim()
                if ($v -eq '|' -or $v -eq '>' -or $v -eq '') { $inBlock = $true }
                else { [void]$out.Add($v); $inBlock = $false }
            }
        } else {
            if ($ln -match '^\s+\S' -or $ln -match '^\s*$') { [void]$out.Add($ln.Trim()) }
            else { $inBlock = $false }
        }
    }
    return (($out -join ' ').Trim())
}
function Get-FrontmatterName {
    param([string]$Text)
    $m = [regex]::Match($Text, '(?m)^name:\s*(.+)$')
    if ($m.Success) { return $m.Groups[1].Value.Trim() }
    return ''
}

# ---------------- A. 运行时 ----------------
$psv = $PSVersionTable.PSVersion.ToString()
Add-R 'A 运行时' 'PowerShell' 'PASS' $psv
foreach ($bin in @('node', 'python', 'pnpm.cmd', 'npx.cmd', 'git')) {
    $c = Get-Command $bin -ErrorAction SilentlyContinue
    if ($c) {
        $ver = ''
        try {
            if ($bin -eq 'node') { $ver = (& node -v 2>&1 | Out-String).Trim() }
            elseif ($bin -eq 'python') { $ver = (& python --version 2>&1 | Out-String).Trim() }
            elseif ($bin -eq 'git') { $ver = (& git --version 2>&1 | Out-String).Trim() }
            elseif ($bin -eq 'pnpm.cmd') { $ver = (& pnpm.cmd -v 2>&1 | Out-String).Trim() }
            elseif ($bin -eq 'npx.cmd') { $ver = (& npx.cmd --version 2>&1 | Out-String).Trim() }
        } catch { $ver = '版本未知' }
        Add-R 'A 运行时' $bin 'PASS' $ver
    } else {
        Add-R 'A 运行时' $bin 'WARN' '未安装或不在 PATH（相关能力标注未实测）'
    }
}
if (Test-Path -LiteralPath $DshHome) {
    Add-R 'A 运行时' 'DSH_HOME' 'PASS' $DshHome
} else {
    Add-R 'A 运行时' 'DSH_HOME' 'FAIL' ('目录不存在：' + $DshHome)
}

# ---------------- B. Skills ----------------
$skillsDir = Join-Path $DshHome 'skills'
$disabledDir = Join-Path $DshHome 'skills-disabled'
$active = @()
if (Test-Path -LiteralPath $skillsDir) { $active = @(Get-ChildItem -LiteralPath $skillsDir -Directory -ErrorAction SilentlyContinue) }
$disabled = @()
if (Test-Path -LiteralPath $disabledDir) { $disabled = @(Get-ChildItem -LiteralPath $disabledDir -Directory -ErrorAction SilentlyContinue) }
Add-R 'B Skills' '活动 skill 数' 'PASS' ([string]$active.Count)
Add-R 'B Skills' '停用 skill 数' 'PASS' ([string]$disabled.Count)

$totalChars = 0
$missing = New-Object System.Collections.ArrayList
$over200 = New-Object System.Collections.ArrayList
$over500 = New-Object System.Collections.ArrayList
$noTrigger = New-Object System.Collections.ArrayList
foreach ($d in $active) {
    $skillMd = Join-Path $d.FullName 'SKILL.md'
    if (-not (Test-Path -LiteralPath $skillMd)) { [void]$missing.Add($d.Name); continue }
    $txt = Read-Utf8 $skillMd
    $desc = Get-FrontmatterDescription $txt
    $nm = Get-FrontmatterName $txt
    $len = 0
    if ($desc.Length -gt 0) { $len = $desc.Length }
    $totalChars += $len
    if ($len -gt 500) { [void]$over500.Add($d.Name + '(' + [string]$len + ')') }
    elseif ($len -gt 200) { [void]$over200.Add($d.Name + '(' + [string]$len + ')') }
    $trigger = '(?i)(use when|when user|when 用户|当用户|触发词|trigger)'
    if (-not [regex]::IsMatch($desc, $trigger)) { [void]$noTrigger.Add($d.Name) }
    if ($nm -ne '' -and $nm -ne $d.Name) { Add-R 'B Skills' ('目录名与 name 不同: ' + $d.Name) 'WARN' ('frontmatter name=' + $nm + '（第三方安装前缀常见；触发以 name/description 为准）') }
}
if ($totalChars -gt 5000) { Add-R 'B Skills' 'description 总字符' 'WARN' ([string]$totalChars + '（超过 5000，catalog 成本偏高；压短或停用）') }
else { Add-R 'B Skills' 'description 总字符' 'PASS' ([string]$totalChars) }
if ($missing.Count -gt 0) { Add-R 'B Skills' '缺少 SKILL.md' 'FAIL' ($missing -join ', ') } else { Add-R 'B Skills' 'SKILL.md 完整性' 'PASS' '全部存在' }
if ($over500.Count -gt 0) { Add-R 'B Skills' 'description >500（会被 catalog 截断）' 'WARN' ($over500 -join ', ') } else { Add-R 'B Skills' 'description >500' 'PASS' '无' }
if ($over200.Count -gt 0) { Add-R 'B Skills' 'description >200（偏贵）' 'WARN' ($over200 -join ', ') } else { Add-R 'B Skills' 'description >200' 'PASS' '无' }
if ($noTrigger.Count -gt 0) { Add-R 'B Skills' '无显式触发词' 'WARN' ($noTrigger -join ', ') } else { Add-R 'B Skills' '触发词' 'PASS' '均有显式触发词' }

# ---------------- C. 角色 ----------------
$agentsDir = Join-Path $DshHome 'agents'
$agentFiles = @()
if (Test-Path -LiteralPath $agentsDir) { $agentFiles = @(Get-ChildItem -LiteralPath $agentsDir -File -Filter '*.md' -ErrorAction SilentlyContinue) }
if ($agentFiles.Count -gt 0) {
    Add-R 'C 角色' 'agents 角色数' 'PASS' ([string]$agentFiles.Count + '：' + (($agentFiles | ForEach-Object { $_.Name }) -join ', '))
} else {
    Add-R 'C 角色' 'agents 角色数' 'WARN' '未安装角色 prompt（团队评审依赖它）'
}

# ---------------- D. profile 配置 ----------------
$profileDir = Join-Path $DshHome 'profiles\web'
$patch = Join-Path $profileDir 'cordis.patch.yml'
if (Test-Path -LiteralPath $patch) {
    $pt = Read-Utf8 $patch
    $lines = $pt -split "`r?`n"
    $openAt = ''
    foreach ($ln in $lines) {
        if ($ln -match '^\s*openAt:\s*(\S+)') { $openAt = $matches[1] }
    }
    if ($openAt -eq 'first-search') { Add-R 'D profile' '检索 openAt' 'PASS' $openAt }
    elseif ($openAt -eq 'never') { Add-R 'D profile' '检索 openAt' 'FAIL' 'never：跨会话检索被关闭' }
    elseif ($openAt -eq '') { Add-R 'D profile' '检索 openAt' 'WARN' '未显式配置（用 bundle 默认）' }
    else { Add-R 'D profile' '检索 openAt' 'WARN' $openAt }

    if ($pt -match "dshHomePath\('session-index\.sqlite'\)") { Add-R 'D profile' '索引持久化' 'PASS' "dshHomePath('session-index.sqlite')" }
    elseif ($pt -match ":memory:") { Add-R 'D profile' '索引持久化' 'FAIL' ':memory:：重启丢索引' }
    else { Add-R 'D profile' '索引持久化' 'WARN' '未显式配置' }

    if ($pt -match '(?m)^\s*journalMode:\s*(\S+)') { Add-R 'D profile' 'journalMode' 'PASS' $matches[1] } else { Add-R 'D profile' 'journalMode' 'WARN' '未显式声明' }
    if ($pt -match '(?m)^\s*searchTimeoutMs:\s*(\d+)') {
        $to = [int]$matches[1]
        if ($to -ge 300000) { Add-R 'D profile' 'searchTimeoutMs' 'PASS' ([string]$to + '（首次建库保护）') }
        else { Add-R 'D profile' 'searchTimeoutMs' 'WARN' ([string]$to + '（首次建库可能被掐断）') }
    } else { Add-R 'D profile' 'searchTimeoutMs' 'WARN' '未配置（默认 30s）' }

    $ti = @($lines | Where-Object { $_ -match 'dsh-token-insights' -and $_ -notmatch '^\s*#' })
    if ($ti.Count -gt 0) { Add-R 'D profile' 'token-insights 残留' 'FAIL' ([string]$ti.Count + ' 行有效引用') } else { Add-R 'D profile' 'token-insights 残留' 'PASS' '无有效引用' }
    $dm = @($lines | Where-Object { $_ -match 'dshmarket' -and $_ -notmatch '^\s*#' })
    if ($dm.Count -gt 0) { Add-R 'D profile' 'dshmarket 残留' 'WARN' ([string]$dm.Count + ' 行有效引用（自重启会抢端口）') } else { Add-R 'D profile' 'dshmarket 残留' 'PASS' '无有效引用' }
    Add-R 'D profile' 'patch 行数' 'PASS' ([string]$lines.Count)
} else {
    Add-R 'D profile' 'cordis.patch.yml' 'FAIL' ('不存在：' + $patch)
}

foreach ($pkg in @('dsh-token-insights', 'dshmarket')) {
    $p = Join-Path $profileDir ('node_modules\' + $pkg)
    if (Test-Path -LiteralPath $p) { Add-R 'D profile' ($pkg + ' 包') 'WARN' 'node_modules 仍存在' } else { Add-R 'D profile' ($pkg + ' 包') 'PASS' '已移除' }
}

# ---------------- E. 会话与索引 ----------------
$idx = @(Get-ChildItem -LiteralPath $DshHome -Filter 'session-index.sqlite*' -File -ErrorAction SilentlyContinue)
$idxMain = $idx | Where-Object { $_.Name -eq 'session-index.sqlite' } | Select-Object -First 1
if ($idxMain) {
    $mb = [math]::Round($idxMain.Length / 1MB, 1)
    if ($idxMain.Length -gt 100MB) { Add-R 'E 记忆' '会话索引' 'PASS' ([string]$mb + ' MB，' + $idxMain.LastWriteTime.ToString('yyyy-MM-dd HH:mm')) }
    elseif ($idxMain.Length -gt 1MB) { Add-R 'E 记忆' '会话索引' 'WARN' ([string]$mb + ' MB（偏小，可能未建完）') }
    else { Add-R 'E 记忆' '会话索引' 'WARN' ([string]$mb + ' MB（空/未建完）') }
} else {
    Add-R 'E 记忆' '会话索引' 'WARN' '不存在：首次搜索会建库（2–3 分钟），或用离线预建工具'
}
$sessDir = Join-Path $DshHome 'sessions'
$sessFilesCount = 0
if (Test-Path -LiteralPath $sessDir) {
    $sessFiles = @(Get-ChildItem -LiteralPath $sessDir -Recurse -File -Filter 'session*.jsonl.zstd' -ErrorAction SilentlyContinue)
    $sessFilesCount = $sessFiles.Count
    $sum = 0
    foreach ($f in $sessFiles) { $sum += $f.Length }
    Add-R 'E 记忆' '会话库' 'PASS' ([string]$sessFiles.Count + ' 个 / ' + [string]([math]::Round($sum / 1MB, 1)) + ' MB')
} else {
    Add-R 'E 记忆' '会话库' 'WARN' 'sessions 目录不存在'
}

# ---------------- F. 桌面壳 ----------------
$candidates = New-Object System.Collections.ArrayList
if ($AppSrc) { [void]$candidates.Add((Join-Path $AppSrc 'main.js')) }
# 从本机环境推导安装路径，不写死源环境盘符；找不到则该项记 WARN/SKIP，不猜测。
if ($env:DSH_APP_SRC) { [void]$candidates.Add((Join-Path $env:DSH_APP_SRC 'main.js')) }
# 从正在运行的 DeepSeek Harness 进程反推：<安装根>\resources\app\src\main.js
try {
    $dshProc = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -like '*DeepSeek Harness*' -and $_.Path } | Select-Object -First 1
    if ($dshProc -and $dshProc.Path) {
        $dshRoot = Split-Path -Parent $dshProc.Path
        [void]$candidates.Add((Join-Path $dshRoot 'resources\app\src\main.js'))
    }
} catch { }
if ($env:LOCALAPPDATA) { [void]$candidates.Add((Join-Path $env:LOCALAPPDATA 'Programs\DeepSeek Harness\resources\app\src\main.js')) }
if ($env:PROGRAMFILES) { [void]$candidates.Add((Join-Path $env:PROGRAMFILES 'DeepSeek Harness\resources\app\src\main.js')) }
if (${env:ProgramFiles(x86)}) { [void]$candidates.Add((Join-Path ${env:ProgramFiles(x86)} 'DeepSeek Harness\resources\app\src\main.js')) }
$mainJs = ''
foreach ($c in $candidates) { if (Test-Path -LiteralPath $c) { $mainJs = $c; break } }
if ($mainJs -ne '') {
    $mt = Read-Utf8 $mainJs
    $probe = ''
    $limit = ''
    $window = ''
    $backoff = ''
    if ($mt -match 'HEALTH_PROBE_TIMEOUT\s*=\s*(\d+)') { $probe = $matches[1] }
    if ($mt -match 'HEALTH_FAILURE_LIMIT\s*=\s*(\d+)') { $limit = $matches[1] }
    if ($mt -match 'HEALTH_DOWN_WINDOW_MS\s*=\s*(\d+)') { $window = $matches[1] }
    if ($mt -match 'CRASH_RESTART_BACKOFF_MS\s*=\s*(\d+)') { $backoff = $matches[1] }
    $hasBusy = $mt -match 'isTcpAccepting'
    $patched = ($probe -eq '12000' -and $limit -eq '6' -and $window -ne '' -and $hasBusy)
    $detail = ('probe=' + $probe + 'ms limit=' + $limit + ' window=' + $window + 'ms backoff=' + $backoff + 'ms busyCheck=' + [string]$hasBusy)
    if ($patched) { Add-R 'F 桌面壳' '健康检查补丁' 'PASS' $detail }
    elseif ($window -ne '' -or $hasBusy) { Add-R 'F 桌面壳' '健康检查补丁' 'WARN' ('部分锚点存在：' + $detail) }
    else { Add-R 'F 桌面壳' '健康检查补丁' 'WARN' ('旧版逻辑（≈23s 误杀窗口）：' + $detail) }

    $dlog = Join-Path $env:APPDATA 'DeepSeek Harness\desktop.log'
    if (Test-Path -LiteralPath $dlog) {
        $tail = @(Get-Content -LiteralPath $dlog -Encoding UTF8 -ErrorAction SilentlyContinue | Select-Object -Last 400)
        $kill = @($tail | Where-Object { $_ -match '3/3' }).Count
        $boot = @($tail | Where-Object { $_ -match '已启动内置服务器' }).Count
        $addr = @($tail | Where-Object { $_ -match 'EADDRINUSE' }).Count
        if ($kill -gt 0) { Add-R 'F 桌面壳' 'desktop.log 近期 3/3 判死' 'WARN' ([string]$kill + ' 次（旧实例残留需区分；重启后应为 0）') } else { Add-R 'F 桌面壳' 'desktop.log 近期 3/3 判死' 'PASS' '0 次' }
        Add-R 'F 桌面壳' 'desktop.log 启动/端口' 'PASS' ('已启动 ' + [string]$boot + ' 次；EADDRINUSE ' + [string]$addr + ' 次')
    } else {
        Add-R 'F 桌面壳' 'desktop.log' 'WARN' ('不存在：' + $dlog)
    }
} else {
    Add-R 'F 桌面壳' 'main.js' 'WARN' '未找到（非桌面版/自定义安装）'
}

# ---------------- G. 工作区资产 ----------------
$assets = New-Object System.Collections.ArrayList
[void]$assets.Add(@('AGENTS.md', (Join-Path $Workspace 'AGENTS.md')))
[void]$assets.Add(@('memory\rules.md', (Join-Path $Workspace 'memory\rules.md')))
[void]$assets.Add(@('memory\decisions.md', (Join-Path $Workspace 'memory\decisions.md')))
[void]$assets.Add(@('standards\ 目录', (Join-Path $Workspace 'standards')))
[void]$assets.Add(@('tools\system-facts\extract-frontend.mjs', (Join-Path $Workspace 'tools\system-facts\extract-frontend.mjs')))
[void]$assets.Add(@('upgrade\post-restart-check.ps1', (Join-Path $Workspace 'upgrade\post-restart-check.ps1')))
[void]$assets.Add(@('upgrade\team\gate-check.ps1', (Join-Path $Workspace 'upgrade\team\gate-check.ps1')))
[void]$assets.Add(@('upgrade\team\requirement-doc-check.ps1', (Join-Path $Workspace 'upgrade\team\requirement-doc-check.ps1')))
[void]$assets.Add(@('upgrade\team\test-traceability.ps1', (Join-Path $Workspace 'upgrade\team\test-traceability.ps1')))
[void]$assets.Add(@('projects\ 目录', (Join-Path $Workspace 'projects')))
[void]$assets.Add(@('handover\ 目录', (Join-Path $Workspace 'handover')))
[void]$assets.Add(@('tools\build-docs-html.py', (Join-Path $Workspace 'tools\build-docs-html.py')))
[void]$assets.Add(@('tools\trae-handoff\ 源目录', (Join-Path $Workspace 'tools\trae-handoff')))
$missAssets = New-Object System.Collections.ArrayList
foreach ($a in $assets) {
    if (Test-Path -LiteralPath $a[1]) { Add-R 'G 资产' $a[0] 'PASS' '存在' } else { [void]$missAssets.Add($a[0]) }
}
if ($missAssets.Count -eq 0) { Add-R 'G 资产' '资产齐全度' 'PASS' '全部存在' }
else { Add-R 'G 资产' '缺失资产' 'WARN' ($missAssets -join ', ') }

foreach ($sk in @('ui-design-production', 'feature-handoff', 'dsh-capability-loop')) {
    $p = Join-Path $skillsDir $sk
    if (Test-Path -LiteralPath $p) { Add-R 'G 资产' ('skill ' + $sk) 'PASS' '已安装' } else { Add-R 'G 资产' ('skill ' + $sk) 'WARN' '未安装' }
}

# Trae 关联能力（只读探测：CLI / 进程 / 交接包目录）
$traeCli = ''
foreach ($n in @('trae-cn', 'trae')) {
    $c = Get-Command $n -ErrorAction SilentlyContinue
    if ($c -and $c.Source) { $traeCli = $c.Source; break }
}
if ($traeCli -eq '') {
    foreach ($cand in @((Join-Path $env:LOCALAPPDATA 'Programs\Trae CN\bin\trae-cn.cmd'), 'D:\Trae CN\bin\trae-cn.cmd')) {
        if ($cand -and (Test-Path -LiteralPath $cand)) { $traeCli = $cand; break }
    }
}
if ($traeCli -ne '') { Add-R 'G 资产' 'Trae CLI' 'PASS' $traeCli } else { Add-R 'G 资产' 'Trae CLI' 'WARN' '未探测到（交接可手动指定 -TraeExe）' }
$traeProcs = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match 'Trae' })
if ($traeProcs.Count -gt 0) { Add-R 'G 资产' 'Trae 进程' 'PASS' ([string]$traeProcs.Count + ' 个运行中') } else { Add-R 'G 资产' 'Trae 进程' 'WARN' '未运行' }
$handoffDir = Join-Path $Workspace 'docs\handoff'
if (Test-Path -LiteralPath $handoffDir) {
    $pkgs = @(Get-ChildItem -LiteralPath $handoffDir -Directory -ErrorAction SilentlyContinue)
    Add-R 'G 资产' '交接包' 'PASS' ([string]$pkgs.Count + ' 个（trae-status.ps1 看明细）')
} else {
    Add-R 'G 资产' '交接包' 'WARN' '暂无 docs\handoff（按需创建）'
}
$userProfile = Join-Path $Workspace 'memory\user-profile.md'
if (Test-Path -LiteralPath $userProfile) {
    $ageDays = ([datetime]::Now - (Get-Item -LiteralPath $userProfile).LastWriteTime).Days
    if ($ageDays -gt 120) { Add-R 'G 资产' '用户偏好记忆' 'WARN' ('memory\user-profile.md 已 ' + [string]$ageDays + ' 天未更新（偏好可能过期，见 references/85-ux-memory.md）') }
    else { Add-R 'G 资产' '用户偏好记忆' 'PASS' ('memory\user-profile.md 存在（' + [string]$ageDays + ' 天前更新）') }
} else {
    Add-R 'G 资产' '用户偏好记忆' 'WARN' '未建 memory\user-profile.md（见 references/85-ux-memory.md）'
}

# ---------------- H. 版本与更新提示 ----------------
$selfRoot = Split-Path -Parent $PSScriptRoot
$verFile = Join-Path $selfRoot 'version.json'
$vInstalled = ''
if (Test-Path -LiteralPath $verFile) {
    $vt = Read-Utf8 $verFile
    $vm = [regex]::Match($vt, '"version"\s*:\s*"([^"]+)"')
    if ($vm.Success) { $vInstalled = $vm.Groups[1].Value; Add-R 'H 自身' 'skill 版本' 'PASS' $vInstalled } else { Add-R 'H 自身' 'skill 版本' 'WARN' 'version.json 无 version 字段' }
} else {
    Add-R 'H 自身' 'skill 版本' 'WARN' 'version.json 不存在'
}
if (-not $Source) { $Source = Join-Path $Workspace 'tools\capability-loop\skill\dsh-capability-loop' }
$vSource = ''
if (Test-Path -LiteralPath $Source) {
    $sf = Join-Path $Source 'version.json'
    if (Test-Path -LiteralPath $sf) {
        $stxt = Read-Utf8 $sf
        $sm = [regex]::Match($stxt, '"version"\s*:\s*"([^"]+)"')
        if ($sm.Success) { $vSource = $sm.Groups[1].Value }
    }
    if ($vSource -ne '' -and $vInstalled -ne '') {
        if ($vSource -eq $vInstalled) { Add-R 'H 自身' '更新检查' 'PASS' ('安装版=源=' + $vInstalled) }
        else { Add-R 'H 自身' '更新检查' 'WARN' ('源版本不同：安装 ' + $vInstalled + ' / 源 ' + $vSource + '（用 skill-status.ps1 查看差异，不自动更新）') }
    } elseif ($vSource -ne '') {
        Add-R 'H 自身' '更新检查' 'PASS' ('源版本 ' + $vSource + '（安装版无 version.json）')
    } else {
        Add-R 'H 自身' '更新检查' 'WARN' '源目录无 version.json'
    }
} else {
    Add-R 'H 自身' '更新检查' 'SKIP' '无源目录（独立分发副本，无法对比）'
}

# ---------------- I. 动态漂移（对比上次体检） ----------------
$stateDir = Join-Path $Workspace '.tmp\capability-loop'
$stateFile = Join-Path $stateDir 'audit-state.json'
$cur = @{}
$cur['activeSkills'] = [string]$active.Count
$cur['disabledSkills'] = [string]$disabled.Count
$cur['catalogChars'] = [string]$totalChars
if (Test-Path -LiteralPath $patch) { $cur['patchLines'] = [string](@((Read-Utf8 $patch) -split "`r?`n").Count) }
$idxNow = @(Get-ChildItem -LiteralPath $DshHome -Filter 'session-index.sqlite*' -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq 'session-index.sqlite' } | Select-Object -First 1)
if ($idxNow.Count -gt 0) { $cur['indexMB'] = [string]([math]::Round($idxNow[0].Length / 1MB, 1)) }
if ($mainJs -ne '') {
    $mt2 = Read-Utf8 $mainJs
    if ($mt2 -match 'HEALTH_DOWN_WINDOW_MS' -and $mt2 -match 'isTcpAccepting') { $cur['shellPatched'] = 'yes' } else { $cur['shellPatched'] = 'no' }
}
if ($patch -and (Test-Path -LiteralPath $patch)) {
    $pt2 = Read-Utf8 $patch
    $oa = [regex]::Match($pt2, '(?m)^\s*openAt:\s*(\S+)')
    if ($oa.Success) { $cur['searchOpenAt'] = $oa.Groups[1].Value }
}
if ($traeCli -ne '') { $cur['traeCli'] = 'yes' } else { $cur['traeCli'] = 'no' }
$cur['sessions'] = [string]$sessFilesCount
$prev = $null
if (Test-Path -LiteralPath $stateFile) {
    try { $prev = (Read-Utf8 $stateFile) | ConvertFrom-Json } catch { $prev = $null }
}
if ($prev) {
    $drift = 0
    foreach ($k in @($prev.PSObject.Properties.Name)) {
        if ($k -eq 'time') { continue }
        $old = [string]$prev.$k
        if (-not $cur.ContainsKey($k)) { Add-R 'I 漂移' ('指标消失：' + $k) 'WARN' ('上次=' + $old); $drift++; continue }
        $new = [string]$cur[$k]
        if ($old -ne $new) { Add-R 'I 漂移' ('变化：' + $k) 'WARN' ('上次=' + $old + ' → 本次=' + $new); $drift++ }
    }
    foreach ($k in @($cur.Keys)) {
        if (-not ($prev.PSObject.Properties.Name -contains $k)) { Add-R 'I 漂移' ('新增指标：' + $k) 'PASS' ('本次=' + [string]$cur[$k]) }
    }
    if ($drift -eq 0) { Add-R 'I 漂移' '与上次体检相比' 'PASS' ('无指标变化（上次：' + [string]$prev.time + '）') }
} else {
    Add-R 'I 漂移' '首次体检' 'PASS' '无历史快照（本次已建立基线，下次自动对比）'
}
$cur['time'] = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
try {
    if (-not (Test-Path -LiteralPath $stateDir)) { New-Item -ItemType Directory -Force -Path $stateDir | Out-Null }
    $stateText = $cur | ConvertTo-Json -Depth 3
    [System.IO.File]::WriteAllText($stateFile, $stateText, (New-Object System.Text.UTF8Encoding($false)))
} catch {
    Add-R 'I 漂移' '写入快照' 'WARN' ('失败：' + $_.Exception.Message + '｜' + ($_.ScriptStackTrace -replace "`r?`n", ' '))
}

# ---------------- 汇总 ----------------
$pass = @($results | Where-Object { $_.Status -eq 'PASS' }).Count
$warn = @($results | Where-Object { $_.Status -eq 'WARN' }).Count
$fail = @($results | Where-Object { $_.Status -eq 'FAIL' }).Count
$skip = @($results | Where-Object { $_.Status -eq 'SKIP' }).Count

Write-Host ''
Write-Host '==== DSH 能力体检 ====' -ForegroundColor Cyan
Write-Host ('DSH_HOME : ' + $DshHome)
Write-Host ('Workspace: ' + $Workspace)
Write-Host ('时间     : ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))
Write-Host ''
$group = ''
foreach ($r in $results) {
    if ($r.Group -ne $group) {
        $group = $r.Group
        Write-Host ('-- ' + $group + ' --') -ForegroundColor DarkCyan
    }
    $color = 'Gray'
    if ($r.Status -eq 'PASS') { $color = 'Green' }
    elseif ($r.Status -eq 'WARN') { $color = 'Yellow' }
    elseif ($r.Status -eq 'FAIL') { $color = 'Red' }
    Write-Host ('  [' + $r.Status + '] ' + $r.Item + ' — ' + $r.Detail) -ForegroundColor $color
}
Write-Host ''
Write-Host ('汇总：PASS=' + [string]$pass + ' WARN=' + [string]$warn + ' FAIL=' + [string]$fail + ' SKIP=' + [string]$skip) -ForegroundColor Cyan

# ---------------- 报告 ----------------
if (-not $OutFile) {
    $dotTmp = Join-Path $Workspace '.tmp'
    try {
        if (-not (Test-Path -LiteralPath $dotTmp)) { New-Item -ItemType Directory -Force -Path $dotTmp | Out-Null }
        $OutFile = Join-Path $dotTmp ('capability-audit-' + (Get-Date).ToString('yyyyMMdd-HHmmss') + '.md')
    } catch { $OutFile = '' }
}
if ($OutFile) {
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.AppendLine('# DSH 能力体检 — ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))
    [void]$sb.AppendLine('')
    [void]$sb.AppendLine('- DSH_HOME: `' + $DshHome + '`')
    [void]$sb.AppendLine('- Workspace: `' + $Workspace + '`')
    [void]$sb.AppendLine('- PowerShell: `' + $psv + '`')
    [void]$sb.AppendLine('- 汇总: PASS=' + [string]$pass + ' / WARN=' + [string]$warn + ' / FAIL=' + [string]$fail)
    [void]$sb.AppendLine('')
    [void]$sb.AppendLine('## 明细')
    [void]$sb.AppendLine('')
    [void]$sb.AppendLine('| 组 | 项 | 判定 | 实测/说明 |')
    [void]$sb.AppendLine('|---|---|---|---|')
    foreach ($r in $results) {
        [void]$sb.AppendLine('| ' + $r.Group + ' | ' + $r.Item + ' | ' + $r.Status + ' | ' + ($r.Detail -replace '\|', '/') + ' |')
    }
    [void]$sb.AppendLine('')
    [void]$sb.AppendLine('> 只读体检：本次未修改任何配置。FAIL 项处理见 skill references/20-runtime-fix.md；WARN 项见 70-playbook.md。')
    try {
        $enc = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($OutFile, $sb.ToString(), $enc)
        Write-Host ('报告已写入：' + $OutFile) -ForegroundColor Gray
    } catch {
        Write-Host ('报告写入失败：' + $_.Exception.Message) -ForegroundColor Yellow
    }
}

if ($Json) {
    $summary = New-Object psobject
    $summary | Add-Member -MemberType NoteProperty -Name pass -Value $pass
    $summary | Add-Member -MemberType NoteProperty -Name warn -Value $warn
    $summary | Add-Member -MemberType NoteProperty -Name fail -Value $fail
    $summary | Add-Member -MemberType NoteProperty -Name results -Value $results
    $summary | ConvertTo-Json -Depth 4
}

if ($Strict -and $fail -gt 0) { exit 1 }
exit 0
