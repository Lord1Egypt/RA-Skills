# visual-qa-check.ps1 — 浏览器视觉验收能力探测（会写文件：探测 HTML/PNG 与临时 Chrome profile；只删自己创建的临时 profile）
# 兼容 Windows PowerShell 5.1；含中文，必须保存为 UTF-8 带 BOM。
# 用途：设计/视觉验收开始前先跑一次，明确回答「A 路径能不能用」；不能用时**显式提示用户**该切权限/给截图/标未实测，不许静默跳过。
# 写盘边界：只写 -OutDir（默认 <工作区>/.tmp/visual-qa）；OutDir 必须位于工作区或 %TEMP% 下，否则拒绝运行（-AllowOutsideOutDir 可显式放行）。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File .\visual-qa-check.ps1 [-OutDir <目录>] [-ChromePath <exe>] [-Json] [-SimulateBlocked（仅测试提示话术）] [-AllowOutsideOutDir]
# 退出码：0 = A 路径可用（Chrome headless 截图成功）；2 = 权限/环境受限（需 A/B/C 选择）；1 = 其它失败（Chrome 缺失/参数错误）
[CmdletBinding()]
param(
    [string]$OutDir = '',
    [string]$ChromePath = '',
    [switch]$Json,
    [switch]$SimulateBlocked,
    [switch]$AllowOutsideOutDir
)

$ErrorActionPreference = 'Continue'
Set-StrictMode -Version 2.0

$workspace = (Get-Location).Path
if (-not $OutDir) { $OutDir = Join-Path $workspace '.tmp\visual-qa' }
# 写盘边界：默认只允许工作区或 %TEMP% 下的目录；避免把探测产物写到任意位置。
$outFull = [System.IO.Path]::GetFullPath($OutDir)
$allowedRoots = @([System.IO.Path]::GetFullPath($workspace))
if ($env:TEMP) { $allowedRoots += [System.IO.Path]::GetFullPath($env:TEMP) }
$inside = $false
foreach ($root in $allowedRoots) {
    if ($outFull.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) { $inside = $true; break }
}
if (-not $inside -and -not $AllowOutsideOutDir) {
    Write-Host ('[FAIL] -OutDir 不在工作区或 %TEMP% 下：' + $outFull) -ForegroundColor Red
    Write-Host '       如确需写到别处，显式加 -AllowOutsideOutDir；本脚本只应写自己的临时产物。' -ForegroundColor Yellow
    exit 2
}
try { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null } catch { }

function Fail([string]$msg, [int]$code) {
    if ($Json) {
        Write-Host (@{ ok = $false; reason = $msg; exitCode = $code } | ConvertTo-Json -Depth 3)
    } else {
        Write-Host ('[FAIL] ' + $msg) -ForegroundColor Red
    }
    exit $code
}

# 1) Chrome 探测
if ($ChromePath -and -not (Test-Path -LiteralPath $ChromePath)) { Fail ('指定的 Chrome 不存在：' + $ChromePath) 1 }
if ($SimulateBlocked) {
    # 测试用：模拟「权限受限」，验证提示话术与退出码（不真的启动 Chrome）
    if (-not $Json) {
        Write-Host '==== 浏览器视觉验收探测 ====' -ForegroundColor Cyan
        Write-Host '  [FAIL] A 路径不可用（-SimulateBlocked 模拟权限受限）' -ForegroundColor Red
        Write-Host '  原因：模拟 workspace-write 下 Chrome crashpad 被拒（真实错误形如 exit -36863 / OpenProcess 0x5）' -ForegroundColor Yellow
        Write-Host ''
        Write-Host '  请显式告诉用户，并让用户选择（不要静默标「未实测」就继续）：' -ForegroundColor Cyan
        Write-Host '    A) 在当前会话切换 danger-full-access 后重跑本脚本（可自动截图）' -ForegroundColor Gray
        Write-Host '    B) 请用户在自己的浏览器截图：375/768/1024/1440 × 明/暗 → design-qa/<task>/' -ForegroundColor Gray
        Write-Host '    C) 无法截图：交付物写「未实测（浏览器权限不足）+ 原因 + 补测方式」，不得判 PASS' -ForegroundColor Gray
    } else {
        Write-Host (@{ ok = $false; path = 'B/C'; detail = 'simulated blocked'; exitCode = 2 } | ConvertTo-Json -Depth 3)
    }
    exit 2
}
$candidates = New-Object System.Collections.ArrayList
if ($ChromePath) { [void]$candidates.Add($ChromePath) }
[void]$candidates.Add((Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'))
if (${env:ProgramFiles(x86)}) { [void]$candidates.Add((Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe')) }
[void]$candidates.Add((Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe'))
$chrome = ''
foreach ($c in $candidates) { if ($c -and (Test-Path -LiteralPath $c)) { $chrome = $c; break } }
if ($chrome -eq '') { Fail '未找到 Chrome（可用 -ChromePath 指定）。视觉验收可走 B/C 路径。' 1 }

# 2) agent-browser（仅报告，不作为主路径）
$ab = ''
$abCmd = Get-Command 'agent-browser' -ErrorAction SilentlyContinue
if ($abCmd -and $abCmd.Source) { $ab = $abCmd.Source }

# 3) 生成测试页并截图（A 路径探测）
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$htmlPath = Join-Path $OutDir ('probe-' + $stamp + '.html')
$pngPath = Join-Path $OutDir ('probe-' + $stamp + '.png')
$ud = Join-Path $OutDir ('chrome-ud-' + $stamp)
$expectedBg = @(16, 32, 48)
$html = '<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:rgb(16,32,48)"><h1 style="color:rgb(255,0,0);font-family:sans-serif;padding:20px">VISUAL-QA PROBE</h1></body></html>'
[System.IO.File]::WriteAllText($htmlPath, $html, (New-Object System.Text.UTF8Encoding($false)))
$url = 'file:///' + ($htmlPath -replace '\\', '/')
$args = @('--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', ("--user-data-dir=$ud"), '--window-size=1280,720', ("--screenshot=$pngPath"), $url)
$proc = $null
try {
    $proc = Start-Process -FilePath $chrome -ArgumentList $args -PassThru -WindowStyle Hidden -ErrorAction Stop
    $finished = $proc.WaitForExit(45000)
    if (-not $finished) {
        try { $proc.Kill() } catch { }
        Fail 'Chrome headless 45 秒内未退出（可能需要更高权限或被杀软拦截）。视觉验收走 B/C 路径。' 2
    }
    $chromeExit = $proc.ExitCode
} catch {
    Fail ('启动 Chrome 失败：' + $_.Exception.Message + '。视觉验收走 B/C 路径。') 2
}

$ok = $false
$detail = ''
if (Test-Path -LiteralPath $pngPath) {
    $size = (Get-Item -LiteralPath $pngPath).Length
    if ($size -gt 1000) {
        try {
            Add-Type -AssemblyName System.Drawing
            $bmp = [System.Drawing.Bitmap]::FromFile($pngPath)
            $px = $bmp.GetPixel(10, 10)
            $bmp.Dispose()
            $delta = [math]::Abs([int]$px.R - $expectedBg[0]) + [math]::Abs([int]$px.G - $expectedBg[1]) + [math]::Abs([int]$px.B - $expectedBg[2])
            if ($delta -le 30) {
                $ok = $true
                $detail = ('PNG ' + [string]$size + ' B；像素(' + $px.R + ',' + $px.G + ',' + $px.B + ') 与预期一致')
            } else {
                $detail = ('PNG ' + [string]$size + ' B 但像素(' + $px.R + ',' + $px.G + ',' + $px.B + ') 与预期不符（页面可能没渲染）')
            }
        } catch {
            $detail = ('PNG ' + [string]$size + ' B（无法抽样像素：' + $_.Exception.Message + '）')
        }
    } else {
        $detail = ('PNG 过小：' + [string]$size + ' B')
    }
} else {
    $detail = ('没有生成截图（Chrome exit=' + [string]$chromeExit + '）')
}

# 4) 清理临时 profile，保留探测 HTML/PNG 作为证据
try { if (Test-Path -LiteralPath $ud) { Remove-Item -LiteralPath $ud -Recurse -Force -ErrorAction SilentlyContinue } } catch { }

if ($ok) {
    if ($Json) {
        Write-Host (@{ ok = $true; path = 'A'; chrome = $chrome; png = $pngPath; detail = $detail; agentBrowser = $ab } | ConvertTo-Json -Depth 3)
    } else {
        Write-Host '==== 浏览器视觉验收探测 ====' -ForegroundColor Cyan
        Write-Host ('  [PASS] A 路径可用：Chrome headless 截图成功') -ForegroundColor Green
        Write-Host ('  Chrome  ：' + $chrome)
        Write-Host ('  证据    ：' + $pngPath)
        Write-Host ('  明细    ：' + $detail)
        if ($ab -ne '') { Write-Host ('  agent-browser：' + $ab + '（本环境 open 可能挂起，优先用 Chrome 直截）') -ForegroundColor Gray }
        Write-Host ''
        Write-Host '下一步：按 375/768/1024/1440 × 明/暗 批量截图，放 design-qa/<task>/，再按 rubric 评审。' -ForegroundColor Gray
    }
    exit 0
}

# 5) 失败：显式提示权限/路径选择（不要静默标未实测）
if ($Json) {
    Write-Host (@{ ok = $false; path = 'B/C'; chrome = $chrome; png = $pngPath; detail = $detail; exitCode = 2 } | ConvertTo-Json -Depth 3)
} else {
    Write-Host '==== 浏览器视觉验收探测 ====' -ForegroundColor Cyan
    Write-Host '  [FAIL] A 路径不可用（浏览器启动/渲染受限）' -ForegroundColor Red
    Write-Host ('  原因：' + $detail) -ForegroundColor Yellow
    Write-Host '  判定：这通常是**权限/进程限制**（普通 workspace-write 下 Chrome crashpad 被拒），不是「浏览器永远不可用」。' -ForegroundColor Yellow
    Write-Host ''
    Write-Host '  请显式告诉用户，并让用户选择（不要静默标「未实测」就继续）：' -ForegroundColor Cyan
    Write-Host '    A) 在当前会话切换 danger-full-access 后重跑本脚本（可自动截图）' -ForegroundColor Gray
    Write-Host '    B) 请用户在自己的浏览器截图：375/768/1024/1440 × 明/暗 → design-qa/<task>/' -ForegroundColor Gray
    Write-Host '    C) 无法截图：交付物写「未实测（浏览器权限不足）+ 原因 + 补测方式」，不得判 PASS' -ForegroundColor Gray
    Write-Host ''
    if (Test-Path -LiteralPath $pngPath) {
        Write-Host ('  探测证据：' + $pngPath) -ForegroundColor Gray
    } else {
        Write-Host '  探测证据：未生成截图（无 PNG 可看；按 A/B/C 继续）' -ForegroundColor Gray
    }
}
exit 2
