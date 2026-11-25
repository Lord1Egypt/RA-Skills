# loop-state.ps1 — 能力闭环唯一状态源（.dsh/loop/state.json）读写
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用法：
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action init -Root <工程根> [-Mode shadow|on|off]
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action status -Root <工程根> [-Json]
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action set-mode -Root <工程根> -Mode on
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action set-stage -Root <工程根> -Stage WIRE
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action set-next -Root <工程根> -NextLabel "..." -NextCommand "..."
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action record-check -Root <工程根> -Check design -Status FAIL -ExitCode 1 -Cmd "loop-gate -Kind design"
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action add-blocker -Root <工程根> -BlockerText "..." -Owner lead -Due 2026-11-19
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action resolve-blocker -Root <工程根> -BlockerId D-01
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action sync-audit -Root <工程根>`r`n#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-state.ps1 -Action sync-shadow -Root <工程根> [-ShadowTarget 3]
# 退出码：0 = 成功；1 = 运行错误；2 = 参数错误；3 = 未找到（status 时 state 不存在）
[CmdletBinding()]
param(
    [ValidateSet('init', 'status', 'set-mode', 'set-stage', 'set-next', 'record-check', 'add-blocker', 'resolve-blocker', 'sync-audit', 'sync-shadow')]
    [string]$Action = 'status',
    [string]$StateFile = '',
    [string]$Root = '',
    [string]$ProjectName = '',
    [ValidateSet('', 'off', 'shadow', 'on')][string]$Mode = '',
    [ValidateSet('', 'INTAKE', 'AUDIT', 'FIX', 'WIRE', 'HANDOFF', 'GRILL', 'GATE')][string]$Stage = '',
    [string]$NextLabel = '',
    [string]$NextCommand = '',
    [string]$Check = '',
    [ValidateSet('', 'PASS', 'WARN', 'FAIL', 'SKIP', 'MISSING')][string]$Status = '',
    [int]$ExitCode = -1,
    [string]$Cmd = '',
    [string]$Evidence = '',
    [string]$BlockerId = '',
    [string]$BlockerText = '',
    [string]$Owner = '',
    [string]$Due = '',
    [int]$ShadowTarget = 3,
    [string]$SkillVersion = '2.15.0',
    [switch]$Force,
    [switch]$Json
)

$ErrorActionPreference = 'Stop'
$Script:SkillVersion = $SkillVersion
Set-StrictMode -Version 2.0

function Now-Iso {
    return (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
}

function Read-JsonFile {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $text = [System.IO.File]::ReadAllText($Path, (New-Object System.Text.UTF8Encoding($false)))
    if ($text.Trim() -eq '') { return $null }
    return ($text | ConvertFrom-Json)
}

function Write-JsonFile {
    param([string]$Path, $Object)
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $json = $Object | ConvertTo-Json -Depth 10
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $json, $enc)
}

function New-State {
    param([string]$RootPath, [string]$Name, [string]$InitialMode)
    $now = Now-Iso
    $state = New-Object psobject
    $state | Add-Member -MemberType NoteProperty -Name schema -Value 1
    $state | Add-Member -MemberType NoteProperty -Name skillVersion -Value $SkillVersion
    $state | Add-Member -MemberType NoteProperty -Name mode -Value $InitialMode
    $state | Add-Member -MemberType NoteProperty -Name shadowSessions -Value 0
    $project = New-Object psobject
    $project | Add-Member -MemberType NoteProperty -Name name -Value $Name
    $project | Add-Member -MemberType NoteProperty -Name root -Value $RootPath
    $project | Add-Member -MemberType NoteProperty -Name profile -Value 'docs/loop/project-profile.md'
    $project | Add-Member -MemberType NoteProperty -Name intakeAt -Value $now
    $state | Add-Member -MemberType NoteProperty -Name project -Value $project
    $state | Add-Member -MemberType NoteProperty -Name stage -Value 'INTAKE'
    $state | Add-Member -MemberType NoteProperty -Name stageSince -Value $now
    $next = New-Object psobject
    $next | Add-Member -MemberType NoteProperty -Name label -Value '完成接入六问，生成 docs/loop/project-profile.md'
    $next | Add-Member -MemberType NoteProperty -Name command -Value ''
    $state | Add-Member -MemberType NoteProperty -Name next -Value $next
    $state | Add-Member -MemberType NoteProperty -Name checks -Value (New-Object psobject)
    $state | Add-Member -MemberType NoteProperty -Name blockers -Value @()
    $metrics = New-Object psobject
    $metrics | Add-Member -MemberType NoteProperty -Name gatePassRate7d -Value 0
    $metrics | Add-Member -MemberType NoteProperty -Name rework7d -Value 0
    $metrics | Add-Member -MemberType NoteProperty -Name catalogChars -Value 0
    $metrics | Add-Member -MemberType NoteProperty -Name driftAlerts -Value 0
    $state | Add-Member -MemberType NoteProperty -Name metrics -Value $metrics
    $state | Add-Member -MemberType NoteProperty -Name digest -Value ''
    $state | Add-Member -MemberType NoteProperty -Name updatedAt -Value $now
    return $state
}

function Update-Digest {
    param($State)
    $parts = New-Object System.Collections.ArrayList
    [void]$parts.Add([string]$State.mode)
    [void]$parts.Add([string]$State.stage)
    if ($null -ne $State.checks) {
        foreach ($p in @($State.checks.PSObject.Properties | Sort-Object Name)) {
            $st = ''
            if ($null -ne $p.Value -and $null -ne $p.Value.PSObject.Properties['status']) { $st = [string]$p.Value.status }
            [void]$parts.Add([string]$p.Name + '=' + $st)
        }
    }
    foreach ($b in @($State.blockers)) {
        if ($null -ne $b) { [void]$parts.Add('b:' + [string]$b.id) }
    }
    $src = $parts -join '|'
    $sha = [System.Security.Cryptography.SHA1]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($src)
        $hashBytes = $sha.ComputeHash($bytes)
        $hex = ''
        foreach ($hb in $hashBytes) { $hex += $hb.ToString('x2') }
        $State.digest = 'sha1:' + $hex
    } finally {
        $sha.Dispose()
    }
}

function Save-State {
    param($State, [string]$Path)
    # 每次写入都把 skillVersion 对齐到当前脚本版本，避免面板显示 init 时的旧版本。
    if ($null -ne $State.PSObject.Properties['skillVersion']) { $State.skillVersion = $Script:SkillVersion }
    else { $State | Add-Member -MemberType NoteProperty -Name skillVersion -Value $Script:SkillVersion }
    $State.updatedAt = Now-Iso
    Update-Digest -State $State
    Write-JsonFile -Path $Path -Object $State
}

function Get-ProjectJsonPath {
    param([string]$RootPath)
    return (Join-Path (Join-Path (Join-Path $RootPath '.dsh') 'loop') 'project.json')
}

function Save-ProjectJson {
    param([string]$RootPath, [string]$Name, [string]$ModeValue, [string]$StatePath)
    $projPath = Get-ProjectJsonPath -RootPath $RootPath
    $existing = Read-JsonFile -Path $projPath
    if ($null -eq $existing) {
        $proj = New-Object psobject
        $proj | Add-Member -MemberType NoteProperty -Name schema -Value 1
        $proj | Add-Member -MemberType NoteProperty -Name name -Value $Name
        $proj | Add-Member -MemberType NoteProperty -Name mode -Value $ModeValue
        $proj | Add-Member -MemberType NoteProperty -Name profile -Value 'docs/loop/project-profile.md'
        $proj | Add-Member -MemberType NoteProperty -Name createdAt -Value (Now-Iso)
        Write-JsonFile -Path $projPath -Object $proj
        return
    }
    if ($existing.PSObject.Properties['mode']) { $existing.mode = $ModeValue } else { $existing | Add-Member -MemberType NoteProperty -Name mode -Value $ModeValue }
    if ($existing.PSObject.Properties['name'] -and $Name -ne '') { $existing.name = $Name }
    Write-JsonFile -Path $projPath -Object $existing
}

# ---------------- 路径解析 ----------------
$RootPath = $Root
if ($StateFile -ne '') {
    $StateFile = [System.IO.Path]::GetFullPath($StateFile)
    if ($RootPath -eq '') {
        $loopDir = Split-Path -Parent $StateFile
        $dshDir = Split-Path -Parent $loopDir
        if ((Split-Path -Leaf $loopDir) -eq 'loop' -and (Split-Path -Leaf $dshDir) -eq '.dsh') {
            $RootPath = Split-Path -Parent $dshDir
        }
    }
}
if ($RootPath -eq '') { $RootPath = (Get-Location).Path }
if (-not (Test-Path -LiteralPath $RootPath -PathType Container)) {
    Write-Host ('[FAIL] 工程根不存在：' + $RootPath) -ForegroundColor Red
    exit 2
}
$RootPath = (Resolve-Path -LiteralPath $RootPath).Path
if ($StateFile -eq '') {
    $StateFile = Join-Path (Join-Path (Join-Path $RootPath '.dsh') 'loop') 'state.json'
}
$loopPath = Split-Path -Parent $StateFile
$projectJson = Get-ProjectJsonPath -RootPath $RootPath

$existingState = Read-JsonFile -Path $StateFile
$projectMeta = Read-JsonFile -Path $projectJson

# ---------------- status（只读，不创建） ----------------
if ($Action -eq 'status') {
    if ($null -eq $existingState) {
        if ($Json) {
            $none = New-Object psobject
            $none | Add-Member -MemberType NoteProperty -Name state -Value 'missing'
            $none | Add-Member -MemberType NoteProperty -Name path -Value $StateFile
            $none | ConvertTo-Json -Depth 4
        } else {
            Write-Host ('[WARN] 未接入：' + $StateFile) -ForegroundColor Yellow
        }
        exit 3
    }
    if ($Json) {
        $existingState | ConvertTo-Json -Depth 10
        exit 0
    }
    Write-Host ('工程   ：' + [string]$existingState.project.name)
    Write-Host ('根目录 ：' + [string]$existingState.project.root)
    Write-Host ('档位   ：' + [string]$existingState.mode + '（阶段 ' + [string]$existingState.stage + '）')
    if ($null -ne $existingState.PSObject.Properties['shadow'] -and $null -ne $existingState.shadow) {
        $sh = $existingState.shadow
        $line = '影子   ：已观察 ' + [string]$sh.sessions + ' / ' + [string]$sh.target + ' 个会话'
        if ($sh.canUpgrade -eq $true) { $line = $line + ' —— 可升级：-Action set-mode -Mode on' }
        else { $line = $line + '（继续观察）' }
        Write-Host $line
    }
    Write-Host ('下一项 ：' + [string]$existingState.next.label)
    if (@($existingState.checks.PSObject.Properties).Count -gt 0) {
        Write-Host '门禁   ：'
        foreach ($p in @($existingState.checks.PSObject.Properties | Sort-Object Name)) {
            $c = $p.Value
            Write-Host ('  - ' + [string]$p.Name + ' : ' + [string]$c.status + '（exit ' + [string]$c.exit + '）')
        }
    }
    if (@($existingState.blockers).Count -gt 0) {
        Write-Host '阻断   ：'
        foreach ($b in @($existingState.blockers)) {
            Write-Host ('  - ' + [string]$b.id + ' ' + [string]$b.text + '（' + [string]$b.owner + ' · ' + [string]$b.due + '）')
        }
    }
    Write-Host ('状态源 ：' + $StateFile)
    exit 0
}

# ---------------- init ----------------
if ($Action -eq 'init') {
    if ($null -ne $existingState -and -not $Force) {
        Write-Host ('[PASS] 已存在，不覆盖：' + $StateFile) -ForegroundColor Green
        exit 0
    }
    $name = $ProjectName
    if ($name -eq '') {
        if ($null -ne $projectMeta -and [string]$projectMeta.name -ne '') { $name = [string]$projectMeta.name }
        else { $name = Split-Path -Leaf $RootPath }
    }
    $initialMode = $Mode
    if ($initialMode -eq '') {
        if ($null -ne $projectMeta -and [string]$projectMeta.mode -ne '') { $initialMode = [string]$projectMeta.mode }
        else { $initialMode = 'shadow' }
    }
    $state = New-State -RootPath $RootPath -Name $name -InitialMode $initialMode
    Save-ProjectJson -RootPath $RootPath -Name $name -ModeValue $initialMode -StatePath $StateFile
    Save-State -State $state -Path $StateFile
    $gitignore = Join-Path $loopPath '.gitignore'
    if (-not (Test-Path -LiteralPath $gitignore)) {
        [System.IO.File]::WriteAllText($gitignore, "state.json`r`nshadow-log.jsonl`r`n", (New-Object System.Text.UTF8Encoding($false)))
    }
    Write-Host ('[PASS] 已初始化：' + $StateFile) -ForegroundColor Green
    Write-Host ('       档位 ' + $initialMode + '；阶段 INTAKE；下一步：接入六问')
    Write-Host  '       下一步命令：loop-state.ps1 -Action set-stage -Root <工程根> -Stage AUDIT'
    exit 0
}

# ---------------- 需要 state：缺失则按 marker/默认创建 ----------------
$state = $existingState
if ($null -eq $state) {
    $name = $ProjectName
    if ($name -eq '') {
        if ($null -ne $projectMeta -and [string]$projectMeta.name -ne '') { $name = [string]$projectMeta.name }
        else { $name = Split-Path -Leaf $RootPath }
    }
    $initialMode = $Mode
    if ($initialMode -eq '') {
        if ($null -ne $projectMeta -and [string]$projectMeta.mode -ne '') { $initialMode = [string]$projectMeta.mode }
        else { $initialMode = 'shadow' }
    }
    $state = New-State -RootPath $RootPath -Name $name -InitialMode $initialMode
}

switch ($Action) {
    'set-mode' {
        if ($Mode -eq '') {
            Write-Host '[FAIL] set-mode 需要 -Mode off|shadow|on' -ForegroundColor Red
            exit 2
        }
        $state.mode = $Mode
        if ($Mode -eq 'on') { $state.shadowSessions = 0 }
        Save-ProjectJson -RootPath $RootPath -Name ([string]$state.project.name) -ModeValue $Mode -StatePath $StateFile
    }
    'set-stage' {
        if ($Stage -eq '') {
            Write-Host '[FAIL] set-stage 需要 -Stage INTAKE|AUDIT|FIX|WIRE|HANDOFF|GRILL|GATE' -ForegroundColor Red
            exit 2
        }
        if ([string]$state.stage -ne $Stage) {
            $state.stage = $Stage
            $state.stageSince = Now-Iso
        }
        if ($NextLabel -ne '') { $state.next.label = $NextLabel }
        if ($NextCommand -ne '') { $state.next.command = $NextCommand }
    }
    'set-next' {
        if ($NextLabel -eq '' -and $NextCommand -eq '') {
            Write-Host '[FAIL] set-next 需要 -NextLabel 和/或 -NextCommand' -ForegroundColor Red
            exit 2
        }
        if ($NextLabel -ne '') { $state.next.label = $NextLabel }
        if ($NextCommand -ne '') { $state.next.command = $NextCommand }
    }
    'record-check' {
        if ($Check -eq '' -or $Status -eq '') {
            Write-Host '[FAIL] record-check 需要 -Check 与 -Status PASS|WARN|FAIL|SKIP|MISSING' -ForegroundColor Red
            exit 2
        }
        $checks = @{}
        if ($null -ne $state.checks) {
            foreach ($p in @($state.checks.PSObject.Properties)) { $checks[$p.Name] = $p.Value }
        }
        $code = $ExitCode
        if ($code -lt 0) {
            if ($Status -eq 'PASS') { $code = 0 }
            elseif ($Status -eq 'WARN') { $code = 3 }
            elseif ($Status -eq 'FAIL') { $code = 1 }
            else { $code = 0 }
        }
        $ev = @()
        if ($Evidence -ne '') {
            $ev = @($Evidence -split ';' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' })
        }
        $entry = New-Object psobject
        $entry | Add-Member -MemberType NoteProperty -Name status -Value $Status
        $entry | Add-Member -MemberType NoteProperty -Name at -Value (Now-Iso)
        $entry | Add-Member -MemberType NoteProperty -Name exit -Value $code
        $entry | Add-Member -MemberType NoteProperty -Name cmd -Value $Cmd
        $entry | Add-Member -MemberType NoteProperty -Name evidence -Value $ev
        $checks[$Check] = $entry
        $state.checks = $checks
        # 只在 next 为空时给修复提示，避免覆盖用户/上一步设定的真实下一步。
        if ($Status -eq 'FAIL') {
            $curNext = ''
            if ($null -ne $state.next -and $state.next.PSObject.Properties['label']) { $curNext = [string]$state.next.label }
            if ($curNext -eq '') {
                $state.next.label = '门禁 FAIL：' + $Check + '（看证据后修复）'
            }
        }
    }
    'add-blocker' {
        if ($BlockerText -eq '') {
            Write-Host '[FAIL] add-blocker 需要 -BlockerText' -ForegroundColor Red
            exit 2
        }
        $list = New-Object System.Collections.ArrayList
        foreach ($b in @($state.blockers)) { if ($null -ne $b) { [void]$list.Add($b) } }
        $id = $BlockerId
        if ($id -eq '') {
            $max = 0
            foreach ($b in $list) {
                $m = [regex]::Match([string]$b.id, '^D-(\d+)$')
                if ($m.Success) {
                    $n = [int]$m.Groups[1].Value
                    if ($n -gt $max) { $max = $n }
                }
            }
            $id = 'D-' + ([string]($max + 1)).PadLeft(2, '0')
        }
        $blk = New-Object psobject
        $blk | Add-Member -MemberType NoteProperty -Name id -Value $id
        $blk | Add-Member -MemberType NoteProperty -Name text -Value $BlockerText
        $blk | Add-Member -MemberType NoteProperty -Name owner -Value $Owner
        $blk | Add-Member -MemberType NoteProperty -Name due -Value $Due
        [void]$list.Add($blk)
        $state.blockers = @($list)
    }
    'resolve-blocker' {
        if ($BlockerId -eq '') {
            Write-Host '[FAIL] resolve-blocker 需要 -BlockerId' -ForegroundColor Red
            exit 2
        }
        $list = New-Object System.Collections.ArrayList
        $found = $false
        foreach ($b in @($state.blockers)) {
            if ($null -eq $b) { continue }
            if ([string]$b.id -eq $BlockerId) { $found = $true; continue }
            [void]$list.Add($b)
        }
        if (-not $found) {
            Write-Host ('[FAIL] 未找到阻断：' + $BlockerId) -ForegroundColor Red
            exit 1
        }
        $state.blockers = @($list)
    }
    'sync-audit' {
        $auditPath = Join-Path (Join-Path (Join-Path $RootPath '.tmp') 'capability-loop') 'audit-state.json'
        if (-not (Test-Path -LiteralPath $auditPath)) {
            Write-Host ('[WARN] 未找到体检快照：' + $auditPath) -ForegroundColor Yellow
            exit 1
        }
        $audit = Read-JsonFile -Path $auditPath
        if ($null -eq $audit) {
            Write-Host '[WARN] 体检快照为空，未更新' -ForegroundColor Yellow
            exit 1
        }
        if ($null -ne $audit.PSObject.Properties['catalogChars']) { $state.metrics.catalogChars = [int]$audit.catalogChars }
        if ($null -ne $audit.PSObject.Properties['activeSkills']) { $state.metrics | Add-Member -MemberType NoteProperty -Name activeSkills -Value ([int]$audit.activeSkills) -Force }
        if ($null -ne $audit.PSObject.Properties['disabledSkills']) { $state.metrics | Add-Member -MemberType NoteProperty -Name disabledSkills -Value ([int]$audit.disabledSkills) -Force }
        if ($null -ne $audit.PSObject.Properties['indexMB'] -and [string]$audit.indexMB -ne '') { $state.metrics | Add-Member -MemberType NoteProperty -Name indexMB -Value ([double]$audit.indexMB) -Force }
        if ($null -ne $audit.PSObject.Properties['sessions']) { $state.metrics | Add-Member -MemberType NoteProperty -Name sessions -Value ([int]$audit.sessions) -Force }
    }
    'sync-shadow' {
        # 读插件写的影子观察日志（每会话一行），更新 shadowSessions；达到目标提示升级。
        $logPath = Join-Path (Join-Path (Join-Path $RootPath '.dsh') 'loop') 'shadow-log.jsonl'
        if (-not (Test-Path -LiteralPath $logPath)) {
            Write-Host ('[WARN] 未找到影子观察日志：' + $logPath + '（影子档下宿主插件会写；未装插件则无此文件）') -ForegroundColor Yellow
            exit 1
        }
        $logText = ''
        try {
            $logText = [System.IO.File]::ReadAllText($logPath, (New-Object System.Text.UTF8Encoding($false)))
        } catch {
            Write-Host ('[FAIL] 读取影子日志失败：' + $_.Exception.Message) -ForegroundColor Red
            exit 1
        }
        $seen = New-Object System.Collections.Generic.HashSet[string]
        foreach ($line in ($logText -split "`r?`n")) {
            $trimmed = $line.Trim()
            if ($trimmed -eq '') { continue }
            $obj = $null
            try { $obj = $trimmed | ConvertFrom-Json } catch { $obj = $null }
            if ($null -eq $obj) { continue }
            if ($null -ne $obj.PSObject.Properties['session'] -and [string]$obj.session -ne '') {
                [void]$seen.Add([string]$obj.session)
            }
        }
        $count = $seen.Count
        $state.shadowSessions = $count
        $canUpgrade = ($count -ge $ShadowTarget)
        $shadowInfo = New-Object psobject
        $shadowInfo | Add-Member -MemberType NoteProperty -Name sessions -Value $count
        $shadowInfo | Add-Member -MemberType NoteProperty -Name target -Value $ShadowTarget
        $shadowInfo | Add-Member -MemberType NoteProperty -Name canUpgrade -Value $canUpgrade
        $shadowInfo | Add-Member -MemberType NoteProperty -Name at -Value (Now-Iso)
        if ($null -ne $state.PSObject.Properties['shadow']) { $state.shadow = $shadowInfo }
        else { $state | Add-Member -MemberType NoteProperty -Name shadow -Value $shadowInfo }
    }
    default {
        Write-Host ('[FAIL] 未知 Action：' + $Action) -ForegroundColor Red
        exit 2
    }
}

Save-State -State $state -Path $StateFile
if ($Json) {
    $state | ConvertTo-Json -Depth 10
} else {
    Write-Host ('[PASS] ' + $Action + '：' + [string]$state.project.name + ' · ' + [string]$state.mode + ' · ' + [string]$state.stage) -ForegroundColor Green
    if ($null -ne $state.next -and [string]$state.next.label -ne '') {
        Write-Host ('       下一项：' + [string]$state.next.label)
    }
}
exit 0
