# loop-gate.ps1 — 聚合门禁：把任务级/环境级验收收成一条命令
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用法：
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-gate.ps1 -TaskDir <目录> [-Kind auto|design|requirement|test|all] [-Workspace <ws>] [-AllowMissingDesignContext] [-RequireGrill] [-StateFile <state.json>]
#   powershell -NoProfile -ExecutionPolicy Bypass -File .\loop-gate.ps1 -Environment [-Workspace <ws>]
# 说明：design 类别默认要求 design-context*.md（现有系统设计上下文）；确实不需要时用 -AllowMissingDesignContext 显式跳过并写理由。
#       grill 记录默认 WARN；加 -RequireGrill 变 FAIL（交付前硬门用）。
#       状态写回：单一类别或 -Environment 时，若给了 -StateFile 或工程有 .dsh/loop/project.json，则调用 loop-state.ps1 记录 checks。<类别>。
# 退出码：0 = 无 FAIL（允许 WARN/SKIP）；1 = 有 FAIL；2 = 参数错误
[CmdletBinding()]
param(
    [string]$TaskDir = '',
    [ValidateSet('auto', 'design', 'requirement', 'test', 'all')][string]$Kind = 'auto',
    [string]$Workspace = '',
    [switch]$Environment,
    [switch]$StrictMissing,
    [switch]$AllowMissingDesignContext,
    [switch]$RequireGrill,
    [string]$StateFile = ''
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version 2.0

if (-not $Workspace) { $Workspace = (Get-Location).Path }
if (-not (Test-Path -LiteralPath $Workspace -PathType Container)) {
    Write-Host ('[FAIL] 工作区不存在：' + $Workspace) -ForegroundColor Red
    exit 2
}
$Workspace = (Resolve-Path -LiteralPath $Workspace).Path

if ($TaskDir -ne '' -and -not [System.IO.Path]::IsPathRooted($TaskDir)) {
    $TaskDir = Join-Path $Workspace $TaskDir
}

$results = New-Object System.Collections.ArrayList
function Add-R {
    param([string]$Gate, [string]$Status, [string]$Detail)
    $o = New-Object psobject
    $o | Add-Member -MemberType NoteProperty -Name Gate -Value $Gate
    $o | Add-Member -MemberType NoteProperty -Name Status -Value $Status
    $o | Add-Member -MemberType NoteProperty -Name Detail -Value $Detail
    [void]$results.Add($o)
}

function Invoke-Gate {
    param([string]$Name, [string]$Script, [string[]]$Arguments)
    if (-not (Test-Path -LiteralPath $Script)) {
        if ($StrictMissing) { Add-R $Name 'FAIL' ('门禁脚本缺失：' + $Script); return }
        Add-R $Name 'SKIP' ('门禁脚本缺失（跳过）：' + $Script)
        return
    }
    $cmd = 'powershell -NoProfile -ExecutionPolicy Bypass -File "' + $Script + '" ' + ($Arguments -join ' ')
    Write-Host ''
    Write-Host ('-- ' + $Name + ' --') -ForegroundColor DarkCyan
    Write-Host ('   ' + $cmd) -ForegroundColor Gray
    $output = @()
    $code = 2
    try { $output = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Script @Arguments 2>&1) } catch { $output = @($_.Exception.Message) }
    $code = $LASTEXITCODE
    if ($null -eq $code) { $code = 2 }
    $tail = @($output | Select-Object -Last 18)
    foreach ($ln in $tail) { Write-Host ('   ' + [string]$ln) }
    if ($code -eq 0) { Add-R $Name 'PASS' 'exit 0' } else { Add-R $Name 'FAIL' ('exit ' + [string]$code) }
}

function Add-GrillRow {
    param([string]$Dir, [string]$Hint)
    $g = @(Get-ChildItem -LiteralPath $Dir -File -Filter 'grill-*.md' -Recurse -ErrorAction SilentlyContinue)
    if ($g.Count -gt 0) { Add-R '自对抗评审 grill' 'PASS' $g[0].Name }
    elseif ($RequireGrill) { Add-R '自对抗评审 grill' 'FAIL' ('缺少 grill 记录（-RequireGrill 硬门）：' + $Hint) }
    else { Add-R '自对抗评审 grill' 'WARN' ('建议按 references/75-grill.md 做一轮（' + $Hint + '）；要求硬门时加 -RequireGrill') }
}

# ---------------- 环境门禁 ----------------
if ($Environment) {
    Invoke-Gate '环境验收 post-restart-check' (Join-Path $Workspace 'upgrade\post-restart-check.ps1') @()
}

# ---------------- 任务门禁 ----------------
$kinds = New-Object System.Collections.ArrayList
if ($TaskDir -ne '') {
    if (-not (Test-Path -LiteralPath $TaskDir -PathType Container)) {
        Add-R '任务目录' 'FAIL' ('不存在：' + $TaskDir)
        $TaskDir = ''
    }
}
if ($TaskDir -ne '') {
    if ($Kind -eq 'design' -or $Kind -eq 'requirement' -or $Kind -eq 'test') {
        [void]$kinds.Add($Kind)
    } elseif ($Kind -eq 'all') {
        [void]$kinds.Add('design'); [void]$kinds.Add('requirement'); [void]$kinds.Add('test')
    } else {
        $files = @(Get-ChildItem -LiteralPath $TaskDir -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '\\docs\\handoff\\' } | Select-Object -First 300)
        $names = @($files | ForEach-Object { $_.Name })
        $hasDesign = @($names | Where-Object { $_ -match '^(design-spec|tokens|components|review-design)' }).Count -gt 0
        $hasReq = @($names | Where-Object { $_ -match '^(SRS|review-requirement|README-需求入口)' }).Count -gt 0
        $hasTest = @($names | Where-Object { $_ -match '^(business-rule|test-report|test-cases|business-rules)' }).Count -gt 0
        if ($hasDesign) { [void]$kinds.Add('design') }
        if ($hasReq) { [void]$kinds.Add('requirement') }
        if ($hasTest) { [void]$kinds.Add('test') }
        if ($kinds.Count -eq 0) { Add-R '任务识别' 'SKIP' '未识别到 design/requirement/test 产物（用 -Kind 显式指定）' }
    }

    $teamDir = Join-Path $Workspace 'upgrade\team'
    foreach ($k in $kinds) {
        if ($k -eq 'design') {
            # 设计前置：必须先在现有系统上做设计上下文（references/55-design-intake.md）
            $dc = @(Get-ChildItem -LiteralPath $TaskDir -File -Filter 'design-context*.md' -Recurse -ErrorAction SilentlyContinue)
            if ($dc.Count -gt 0) {
                Add-R '设计上下文 design-context' 'PASS' ($dc[0].Name)
            } elseif ($AllowMissingDesignContext) {
                Add-R '设计上下文 design-context' 'SKIP' '已显式跳过（-AllowMissingDesignContext），理由须写进交付说明'
            } else {
                Add-R '设计上下文 design-context' 'FAIL' '缺失：先按 references/55-design-intake.md 产出 design-context.md（现有主题/组件库/状态/样本页），再出稿'
            }
            Add-GrillRow $TaskDir '设计交付前'
            Invoke-Gate 'G1/G2 设计门 gate-check' (Join-Path $teamDir 'gate-check.ps1') @('-TaskDir', $TaskDir, '-Kind', 'design')
        } elseif ($k -eq 'requirement') {
            Add-GrillRow $TaskDir '进三遍评审前'
            $srs = @(Get-ChildItem -LiteralPath $TaskDir -File -Filter 'SRS*.md' -Recurse -ErrorAction SilentlyContinue)
            if ($srs.Count -gt 0) {
                foreach ($s in $srs) {
                    Invoke-Gate ('需求文档门 ' + $s.Name) (Join-Path $teamDir 'requirement-doc-check.ps1') @('-Path', $s.FullName)
                }
            } else {
                Invoke-Gate '需求文档门（目录扫描）' (Join-Path $teamDir 'requirement-doc-check.ps1') @('-Path', $TaskDir, '-Recurse')
            }
            Invoke-Gate '需求评审门 gate-check' (Join-Path $teamDir 'gate-check.ps1') @('-TaskDir', $TaskDir, '-Kind', 'requirement')
        } elseif ($k -eq 'test') {
            Add-GrillRow $TaskDir '测试前（尤其 oracle 来源）'
            Invoke-Gate '测试门 gate-check' (Join-Path $teamDir 'gate-check.ps1') @('-TaskDir', $TaskDir, '-Kind', 'test')
            Invoke-Gate '测试追溯门 test-traceability' (Join-Path $teamDir 'test-traceability.ps1') @('-TaskDir', $TaskDir)
        }
    }
}

if ($results.Count -eq 0) {
    Write-Host '[WARN] 没有可执行的门禁：给 -TaskDir 或加 -Environment。' -ForegroundColor Yellow
    exit 0
}

# ---------------- 汇总 ----------------
$pass = @($results | Where-Object { $_.Status -eq 'PASS' }).Count
$warn = @($results | Where-Object { $_.Status -eq 'WARN' }).Count
$fail = @($results | Where-Object { $_.Status -eq 'FAIL' }).Count
$skip = @($results | Where-Object { $_.Status -eq 'SKIP' }).Count

Write-Host ''
Write-Host '==== 聚合门禁汇总 ====' -ForegroundColor Cyan
foreach ($r in $results) {
    $color = 'Gray'
    if ($r.Status -eq 'PASS') { $color = 'Green' }
    elseif ($r.Status -eq 'WARN') { $color = 'Yellow' }
    elseif ($r.Status -eq 'FAIL') { $color = 'Red' }
    Write-Host ('  [' + $r.Status + '] ' + $r.Gate + ' — ' + $r.Detail) -ForegroundColor $color
}
Write-Host ('RESULT: ' + $(if ($fail -gt 0) { 'FAIL' } else { 'PASS' }) + '（PASS=' + [string]$pass + ' WARN=' + [string]$warn + ' FAIL=' + [string]$fail + ' SKIP=' + [string]$skip + '）') -ForegroundColor $(if ($fail -gt 0) { 'Red' } else { 'Green' })

if ($fail -gt 0) {
    # ---------------- 状态写回（P0） ----------------
    # 只有单一类别（design/requirement/test）或 -Environment 才写回，避免把 all 的整体结果误记到某一类。
    try {
        $stateTarget = $StateFile
        if ($stateTarget -eq '') {
            $marker = Join-Path (Join-Path (Join-Path $Workspace '.dsh') 'loop') 'project.json'
            if (Test-Path -LiteralPath $marker) {
                $stateTarget = Join-Path (Join-Path (Join-Path $Workspace '.dsh') 'loop') 'state.json'
            }
        }
        if ($stateTarget -ne '') {
            $board = ''
            if ($Environment) { $board = 'environment' }
            elseif ($kinds.Count -eq 1) { $board = [string]$kinds[0] }
            if ($board -ne '') {
                $stateScript = Join-Path $PSScriptRoot 'loop-state.ps1'
                & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $stateScript -Action record-check -StateFile $stateTarget -Root $Workspace -Check $board -Status 'FAIL' -ExitCode 1 -Cmd ('loop-gate -Kind ' + $board) | Out-Host
            }
        }
    } catch {
        Write-Host ('[WARN] 状态写回失败：' + $_.Exception.Message) -ForegroundColor Yellow
    }
    exit 1
}

# ---------------- 状态写回（P0） ----------------
try {
    $stateTarget = $StateFile
    if ($stateTarget -eq '') {
        $marker = Join-Path (Join-Path (Join-Path $Workspace '.dsh') 'loop') 'project.json'
        if (Test-Path -LiteralPath $marker) {
            $stateTarget = Join-Path (Join-Path (Join-Path $Workspace '.dsh') 'loop') 'state.json'
        }
    }
    if ($stateTarget -ne '') {
        $board = ''
        if ($Environment) { $board = 'environment' }
        elseif ($kinds.Count -eq 1) { $board = [string]$kinds[0] }
        if ($board -ne '') {
            $stateScript = Join-Path $PSScriptRoot 'loop-state.ps1'
            & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $stateScript -Action record-check -StateFile $stateTarget -Root $Workspace -Check $board -Status 'PASS' -ExitCode 0 -Cmd ('loop-gate -Kind ' + $board) | Out-Host
        }
    }
} catch {
    Write-Host ('[WARN] 状态写回失败：' + $_.Exception.Message) -ForegroundColor Yellow
}
exit 0
