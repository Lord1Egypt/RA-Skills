# handoff-smoke.ps1 — DSH↔Trae 交接链路冒烟（只写临时目录，不碰真实工程）
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用途：在真实工程实测「设计驱动交接」前，先用临时工程验证四件套/门禁/取证/唤起解析是否连通。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File .\handoff-smoke.ps1 [-Workspace <工作区>] [-FeatureHandoff <目录>] [-Scratch <目录>] [-Keep]
# 退出码：0 = 全部检查 PASS；1 = 有 FAIL；2 = 参数错误
[CmdletBinding()]
param(
    [string]$Workspace = '',
    [string]$FeatureHandoff = '',
    [string]$Scratch = '',
    [switch]$Keep
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version 2.0

if (-not $Workspace) { $Workspace = (Get-Location).Path }
if (-not (Test-Path -LiteralPath $Workspace -PathType Container)) {
    Write-Host ('[FAIL] 工作区不存在：' + $Workspace) -ForegroundColor Red
    exit 2
}
$Workspace = (Resolve-Path -LiteralPath $Workspace).Path
if (-not $FeatureHandoff) { $FeatureHandoff = Join-Path $env:USERPROFILE '.dsh\skills\feature-handoff' }
if (-not $Scratch) { $Scratch = Join-Path $Workspace '.tmp\handoff-smoke' }

$results = New-Object System.Collections.ArrayList
function Add-R {
    param([string]$Item, [string]$Status, [string]$Detail)
    $o = New-Object psobject
    $o | Add-Member -MemberType NoteProperty -Name Item -Value $Item
    $o | Add-Member -MemberType NoteProperty -Name Status -Value $Status
    $o | Add-Member -MemberType NoteProperty -Name Detail -Value $Detail
    [void]$results.Add($o)
}
function Write-Utf8NoBom {
    param([string]$Path, [string]$Text)
    $enc = New-Object System.Text.UTF8Encoding($false)
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    [System.IO.File]::WriteAllText($Path, $Text, $enc)
}
function Run-PS {
    param([string]$Script, [string[]]$Arguments)
    $out = @()
    $code = 2
    try { $out = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Script @Arguments 2>&1) } catch { $out = @($_.Exception.Message) }
    $code = $LASTEXITCODE
    if ($null -eq $code) { $code = 2 }
    return @{ Code = $code; Output = ($out -join "`n") }
}

$fhScripts = Join-Path $FeatureHandoff 'scripts'
$newH = Join-Path $fhScripts 'new-handoff.ps1'
$checkH = Join-Path $fhScripts 'check-handoff.ps1'
$collectH = Join-Path $fhScripts 'collect-evidence.ps1'
$openH = Join-Path $fhScripts 'open-in-trae.ps1'
$missing = @()
foreach ($p in @($newH, $checkH, $collectH, $openH)) { if (-not (Test-Path -LiteralPath $p)) { $missing += $p } }
if ($missing.Count -gt 0) {
    Add-R 'feature-handoff 脚本' 'FAIL' ('缺失：' + ($missing -join '; '))
    Write-Host ('[FAIL] feature-handoff 未安装或不完整：' + $FeatureHandoff) -ForegroundColor Red
    exit 1
}
Add-R 'feature-handoff 脚本' 'PASS' '四脚本齐全'

# 准备临时工程
if (Test-Path -LiteralPath $Scratch) { Remove-Item -LiteralPath $Scratch -Recurse -Force -ErrorAction SilentlyContinue }
$proj = Join-Path $Scratch 'smoke-project'
New-Item -ItemType Directory -Force -Path (Join-Path $proj 'src') | Out-Null
Add-R '临时工程' 'PASS' $proj
<#
注意：new-handoff 只接受 -Workspace/-Slug/-Title；-DryRun 只打印不落盘，所以这里真实创建到临时工程。
#>
$r1 = Run-PS $newH @('-Workspace', $proj, '-Slug', 'smoke', '-Title', '交接冒烟')
$handoff = Join-Path $proj 'docs\handoff\smoke'
if ($r1.Code -eq 0 -and (Test-Path -LiteralPath (Join-Path $handoff 'tasks.md'))) {
    Add-R 'new-handoff 建包' 'PASS' 'exit 0，四件套已生成'
} else {
    Add-R 'new-handoff 建包' 'FAIL' ('exit ' + [string]$r1.Code + '：' + (($r1.Output -split "`n") | Select-Object -Last 1))
}

# 空模板应被 prepare 门禁拦住
$r2 = Run-PS $checkH @('-Workspace', $proj, '-Slug', 'smoke', '-Stage', 'prepare')
if ($r2.Code -ne 0) {
    Add-R 'prepare 拦截空模板' 'PASS' ('exit ' + [string]$r2.Code + '（符合预期：空模板不得通过）')
} else {
    Add-R 'prepare 拦截空模板' 'FAIL' '空模板竟然通过了 prepare（门禁失效）'
}

# 填一个最小合规包（含设计驱动验收追加段示例）
$brief = @'
# 交接简报 — 交接冒烟
- 任务目录：`docs/handoff/smoke/`
- 状态：待实现

## 1. 背景与目标
冒烟用夹具；目标：验证交接链路。

## 2. 范围
| 类型 | 内容 |
|---|---|
| In scope | 一个按钮文案 |
| Out of scope | 其它 |
'@
$tasks = @'
# 实现任务 — 交接冒烟
## 范围
- 目标工程：`C:\smoke`
## 任务清单
| ID | 任务 | 涉及文件 | 验收 ID | 状态 |
|---|---|---|---|---|
| T-01 | 修改按钮文案 | `src/app.ts` | AC-001 | 待开始 |
## 接口与数据契约
无。
## 禁止变更
- 不得引入新 UI 体系。
## 已完成判定
- 测试通过 + 截图。
## 实现回报
| 任务 | 改动文件 | 命令 | 结果 |
|---|---|---|---|
| T-01 | src/app.ts | node -v | 见 evidence |
'@
$accept = @'
# 验收用例 — 交接冒烟
## 0. 验收前置
- 基线：无 git。
## 1. 用例
| ID | 场景 | Given | When | Then | 证据要求 | 结果 |
|---|---|---|---|---|---|---|
| AC-001 | 文案可见 | 打开页面 | 查看按钮 | 文案为新值 | 截图 | 待测 |
## 2. 不可实测项
| 项 | 为什么 | 补测 |
|---|---|---|
| 浏览器 | 沙箱不可用 | 用户截图 |
## 3. 结论口径
- 全部通过 → PASS。
'@
$record = @'
# 验收结论 — 交接冒烟
- 结论：PASS
## 1. 用例核对
| 验收 ID | 结果 | 证据 |
|---|---|---|
| AC-001 | PASS | evidence/smoke.md |
## 2. 契约核对
- 改动文件在清单内。
'@
Write-Utf8NoBom (Join-Path $handoff 'brief.md') $brief
Write-Utf8NoBom (Join-Path $handoff 'tasks.md') $tasks
Write-Utf8NoBom (Join-Path $handoff 'acceptance.md') $accept
Write-Utf8NoBom (Join-Path $handoff 'record.md') $record
$r3 = Run-PS $checkH @('-Workspace', $proj, '-Slug', 'smoke', '-Stage', 'prepare')
if ($r3.Code -eq 0) { Add-R 'prepare 合规包' 'PASS' 'exit 0' } else { Add-R 'prepare 合规包' 'FAIL' ('exit ' + [string]$r3.Code + '：' + (($r3.Output -split "`n") | Select-Object -Last 1)) }
$r4 = Run-PS $checkH @('-Workspace', $proj, '-Slug', 'smoke', '-Stage', 'deliver')
if ($r4.Code -eq 0) { Add-R 'deliver 门禁' 'PASS' 'exit 0' } else { Add-R 'deliver 门禁' 'FAIL' ('exit ' + [string]$r4.Code + '：' + (($r4.Output -split "`n") | Select-Object -Last 1)) }

# 取证（非 git 工程应 exit 0 并标注 diff 无法取证）
$r5 = Run-PS $collectH @('-Workspace', $proj, '-Slug', 'smoke', '-TestCommand', 'cmd /c echo smoke-ok')
$ev = @(Get-ChildItem -LiteralPath (Join-Path $handoff 'evidence') -File -ErrorAction SilentlyContinue)
if ($r5.Code -eq 0 -and $ev.Count -gt 0) { Add-R 'collect-evidence 取证' 'PASS' ([string]$ev.Count + ' 份证据') }
else { Add-R 'collect-evidence 取证' 'FAIL' ('exit ' + [string]$r5.Code + '：' + (($r5.Output -split "`n") | Select-Object -Last 1)) }

# Trae CLI 解析（DryRun，不真正唤起）
$r6 = Run-PS $openH @('-Workspace', $proj, '-File', 'docs/handoff/smoke/tasks.md', '-DryRun')
if ($r6.Code -eq 0) { Add-R 'open-in-trae DryRun' 'PASS' 'CLI 解析成功（未唤起）' }
else { Add-R 'open-in-trae DryRun' 'FAIL' ('exit ' + [string]$r6.Code + '：' + (($r6.Output -split "`n") | Select-Object -Last 1)) }

# 工程匹配检查（临时工程通常与当前 Trae 窗口不一致，仅提示，不计 FAIL）
$traeStatus = Join-Path $PSScriptRoot 'trae-status.ps1'
if (Test-Path -LiteralPath $traeStatus) {
    $r7 = Run-PS $traeStatus @('-Workspace', $proj)
    $matchLine = @(($r7.Output -split "`n") | Where-Object { $_ -match 'Trae 当前工程' })
    if ($matchLine.Count -gt 0) {
        $line = $matchLine[0].Trim()
        if ($line -match 'MATCH' -and $line -notmatch 'MISMATCH') { Add-R 'Trae 工程匹配检查' 'PASS' $line }
        elseif ($line -match 'MISMATCH|目标 =') { Add-R 'Trae 工程匹配检查' 'WARN' ('临时工程与当前 Trae 窗口不一致（预期；真实交接前必须 MATCH）：' + $line) }
        else { Add-R 'Trae 工程匹配检查' 'WARN' $line }
    } else { Add-R 'Trae 工程匹配检查' 'WARN' '未输出匹配行（Trae 未装/未运行）' }
}

# 汇总
Write-Host ''
Write-Host '==== 交接链路冒烟 ====' -ForegroundColor Cyan
Write-Host ('临时工程：' + $proj)
Write-Host ''
$fail = 0
foreach ($r in $results) {
    $color = 'Gray'
    if ($r.Status -eq 'PASS') { $color = 'Green' } elseif ($r.Status -eq 'WARN') { $color = 'Yellow' } elseif ($r.Status -eq 'FAIL') { $color = 'Red'; $fail++ }
    Write-Host ('  [' + $r.Status + '] ' + $r.Item + ' — ' + $r.Detail) -ForegroundColor $color
}
Write-Host ''
if ($fail -eq 0) {
    Write-Host 'RESULT: PASS（交接链路连通；可进入真实工程设计驱动实测）' -ForegroundColor Green
} else {
    Write-Host ('RESULT: FAIL（' + [string]$fail + ' 项失败）') -ForegroundColor Red
}
if (-not $Keep) {
    Remove-Item -LiteralPath $Scratch -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host '已清理临时工程（-Keep 可保留用于检查）。' -ForegroundColor Gray
} else {
    Write-Host ('保留临时工程：' + $proj) -ForegroundColor Gray
}
if ($fail -gt 0) { exit 1 }
exit 0
