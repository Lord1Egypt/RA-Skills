<#
.SYNOPSIS
  assist-skills 参考资料包一键部署脚本（Windows / PowerShell）。

.DESCRIPTION
  把技能包内需要在目标项目中落地的全部文件复制到目标项目根目录，并自动把
  rules/ 下的规则文件改名落地到 .trae/rules/ 与 .codebuddy/rules/。
  默认不覆盖目标项目中已存在的同名文件，避免误伤项目既有内容。

.PARAMETER Target
  目标项目根目录，默认为当前目录。

.PARAMETER Force
  覆盖目标项目中已存在的同名文件（默认跳过并提示）。

.PARAMETER DryRun
  只预览将要写入的文件，不实际复制。

.PARAMETER SkipRules
  跳过 .trae/.codebuddy 规则落地（仅使用 Claude Code / opencode 时可加）。

.PARAMETER IncludeSkillFiles
  额外复制技能包自身的说明与脚本（README.md / README.en.md / SKILL.md / scripts/）。

.PARAMETER Auto
  自动判定目标项目根目录，尽量做到"双击即部署、零输入"：
    1) 技能包位于某个项目的子目录（如 <project>\tools\assist-skills）时，自动取该项目根目录；
    2) 否则取当前工作目录（当当前目录不是技能包自身时）；
    3) 仍无法判定时，才提示手工输入。
  由 deploy.cmd 无参数运行时自动带上，命令行执行无需关心。

.PARAMETER Prompt
  未显式指定 -Target 时，在控制台用中文提示输入目标项目根目录（回车 = 当前目录）。

.PARAMETER Pause
  部署结束后等待回车再退出，便于双击/快捷方式启动时看清结果。

.PARAMETER Shortcuts
  在 Windows 的「发送到」菜单和桌面创建"部署AI开发助手(assist-skills)"快捷方式：
  之后在资源管理器里右键任意项目文件夹 → 发送到 → 该项，即可一键部署（免命令、免路径）。

.PARAMETER Vendor
  额外把技能包整体内嵌到目标项目的子目录（默认 tools\assist-skills），
  使该项目自带部署入口：团队成员克隆仓库后直接双击 tools\assist-skills\deploy.cmd
  即可零输入部署，完全不需要安装 ClawHub、不需要技能包、也不需要记路径。

.PARAMETER VendorDir
  内嵌位置，相对目标项目根目录，默认 tools\assist-skills。

.EXAMPLE
  pwsh -File "$HOME\.openclaw\workspace\skills\assist-skills\scripts\deploy.ps1" -Target "D:\your-project"

.EXAMPLE
  pwsh -File .\scripts\deploy.ps1 -Target ..\my-project -DryRun

.EXAMPLE
  pwsh -File .\scripts\deploy.ps1 -Auto -Shortcuts -Pause
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Target = '.',

    [switch]$Force,
    [switch]$DryRun,
    [switch]$SkipRules,
    [switch]$IncludeSkillFiles,
    [switch]$Auto,
    [switch]$Prompt,
    [switch]$Pause,
    [switch]$Shortcuts,
    [switch]$Vendor,

    [string]$VendorDir = 'tools\assist-skills',

    # 兜底：接受多余的位置参数（例如从「发送到」一次选了多个文件夹），只取第一个并提示。
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArguments
)

$ErrorActionPreference = 'Stop'

try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
$OutputEncoding = [System.Text.Encoding]::UTF8

$script:copiedCount = 0
$script:overwrittenCount = 0
$script:skippedCount = 0

function Get-AbsolutePath {
    param([string]$Path)
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }
    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location).Path $Path))
}

function Copy-OneFile {
    param([string]$Source, [string]$Destination)

    $exists = Test-Path -LiteralPath $Destination

    if ($exists -and -not $Force) {
        Write-Host "  [跳过] $Destination（已存在，如需覆盖加 -Force）" -ForegroundColor DarkYellow
        $script:skippedCount++
        return
    }

    if ($DryRun) {
        Write-Host "  [预览] $Destination" -ForegroundColor Gray
        return
    }

    $destDir = Split-Path -Parent $Destination
    if ($destDir -and -not (Test-Path -LiteralPath $destDir)) {
        New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    }

    Copy-Item -LiteralPath $Source -Destination $Destination -Force

    if ($exists) { $script:overwrittenCount++ } else { $script:copiedCount++ }
    Write-Host "  [写入] $Destination" -ForegroundColor Green
}

function Copy-OneTree {
    param([string]$SourceDir, [string]$DestinationDir, [string[]]$ExcludeTopLevel = @())

    Get-ChildItem -LiteralPath $SourceDir -Recurse -File -Force | Sort-Object FullName | ForEach-Object {
        $relative = $_.FullName.Substring($SourceDir.Length).TrimStart('\', '/')
        ${top} = @($relative -split '[\\/]')[0]
        if ($ExcludeTopLevel -contains ${top}) { return }
        Copy-OneFile -Source $_.FullName -Destination (Join-Path $DestinationDir $relative)
    }
}

# ---------- 目标目录解析 ----------

$sep = [System.IO.Path]::DirectorySeparatorChar
$pathCompare = [System.StringComparison]::OrdinalIgnoreCase
$skillRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot)).TrimEnd('\', '/')

# 认定"这是一个项目根目录"的标记文件
$script:projectMarkers = @(
    '.git', 'pom.xml', 'build.gradle', 'build.gradle.kts', 'settings.gradle',
    'package.json', 'pyproject.toml', 'requirements.txt', 'go.mod', 'Cargo.toml',
    'composer.json', '*.sln', '*.csproj'
)

function Get-VendoredProjectRoot {
    param([string]$PackageDir)

    # 全局安装位置（~\.openclaw\...）不参与推断：它的上层 workspace 本身也是 git 仓库，会误判。
    $openclawHome = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.openclaw'
    if ($PackageDir.StartsWith($openclawHome + $sep, $pathCompare)) { return $null }

    $candidate = $null
    $probe = Split-Path -Parent $PackageDir
    $depth = 1
    while ($probe -and $depth -le 4) {
        $parent = Split-Path -Parent $probe
        if (-not $parent -or $parent -eq $probe) { break }

        if ($depth -ge 2) {
            # 深度 1 的情况是"技能包源码仓库"（包是仓库的直属子目录），不能当目标，
            # 否则会把 40+ 个文件直接铺到源码仓库根目录。
            foreach ($marker in $script:projectMarkers) {
                if (Test-Path -Path (Join-Path $probe $marker)) {
                    return [pscustomobject]@{ Root = $probe; HasMarker = $true }
                }
            }
            # 没有标记文件（例如同事直接下载压缩包解压、仓库未初始化 git）时先记为候选，
            # 继续向上找更明确的标记；最终仍无标记则交由调用方让用户确认。
            if (-not $candidate) { $candidate = $probe }
        }
        $probe = $parent
        $depth++
    }

    if ($candidate) { return [pscustomobject]@{ Root = $candidate; HasMarker = $false } }
    return $null
}

function Show-Usage {
    Write-Host ''
    Write-Host '未指定目标项目目录，且当前目录就是技能包自身，无法作为部署目标。' -ForegroundColor Yellow
    Write-Host ''
    Write-Host '用法：'
    Write-Host '  deploy.cmd <目标项目目录>                例如 deploy.cmd D:\my-project'
    Write-Host '  deploy.cmd -Target D:\proj -Vendor       部署，并把技能包内嵌到项目的 tools\assist-skills'
    Write-Host '  deploy.cmd -Target D:\proj -DryRun       只预览将要写入的文件'
    Write-Host ''
    Write-Host '更省事的用法（推荐）：'
    Write-Host '  1) 在 AI 对话里说「把 assist-skills 部署到当前项目」，让 AI 执行；'
    Write-Host '  2) 右键项目文件夹 → 发送到 → 部署AI开发助手(assist-skills)（先运行 deploy.cmd -Shortcuts 生成）；'
    Write-Host '  3) 让项目自带入口：deploy.cmd -Target <项目> -Vendor 之后，双击 <项目>\tools\assist-skills\deploy.cmd 即可。'
    Write-Host ''
}

if ($Auto -and -not $PSBoundParameters.ContainsKey('Target')) {
    $cwd = [System.IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\', '/')
    $vendored = Get-VendoredProjectRoot -PackageDir $skillRoot

    if ($vendored -and $vendored.HasMarker) {
        $Target = $vendored.Root
        Write-Host "[自动] 技能包内嵌在项目中，目标 = 项目根目录：$($vendored.Root)" -ForegroundColor Cyan
    } elseif ($vendored) {
        # 推断出了项目根但缺少标记文件，让用户一下回车即可确认（避免误写目录）
        $Target = $vendored.Root
        Write-Host "[自动] 推断目标项目根目录：$($vendored.Root)（未发现 .git / pom.xml / package.json 等项目标记）" -ForegroundColor Cyan
        $Prompt = $true
    } elseif (-not [string]::Equals($cwd, $skillRoot, $pathCompare)) {
        $Target = $cwd
        Write-Host "[自动] 使用当前目录作为目标：$cwd" -ForegroundColor Cyan
    } else {
        $Prompt = $true
    }
}

if ($Prompt -and -not $PSBoundParameters.ContainsKey('Target')) {
    if ([string]::IsNullOrWhiteSpace($Target) -or $Target -eq '.') {
        $cwdForPrompt = [System.IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\', '/')
        if ([string]::Equals($cwdForPrompt, $skillRoot, $pathCompare)) {
            Show-Usage
            exit 2
        }
        $Target = $cwdForPrompt
    }

    Write-Host ''
    Write-Host "请输入目标项目根目录（直接回车 = $Target）：" -ForegroundColor Cyan
    $answer = Read-Host '  > '
    if ($answer) {
        # 先清洗再判断：终端/管道可能带回不可见字符，清洗后为空则视为"直接回车"，
        # 保留已推断出的目标，不要退回当前目录。
        $answer = ([string]$answer -replace '[\u200B-\u200D\uFEFF]', '').Trim().Trim('"')
        if ($answer) { $Target = $answer }
    }
}

# ---------- 路径规范化与安全校验 ----------

# 剔除不可见字符（首尾 BOM、零宽字符）与包裹引号：
# 管道/终端粘贴可能带入 \uFEFF，会让路径尾部多出隐形字符，进而绕过下面的目录安全校验。
$Target = [string]$Target
$Target = ($Target -replace '[\u200B-\u200D\uFEFF]', '').Trim().Trim('"')
if ([string]::IsNullOrWhiteSpace($Target)) {
    $cwdFallback = [System.IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\', '/')
    if ([string]::Equals($cwdFallback, $skillRoot, $pathCompare)) {
        Show-Usage
        exit 2
    }
    $Target = $cwdFallback
}
$targetRoot = (Get-AbsolutePath $Target).TrimEnd('\', '/')

if ($RemainingArguments -and $RemainingArguments.Count -gt 0) {
    Write-Host "[提示] 忽略多余参数：$($RemainingArguments -join ' ')（只处理第一个目标目录）" -ForegroundColor DarkYellow
}

if ([string]::Equals($targetRoot, $skillRoot, $pathCompare)) {
    throw "目标目录不能是技能包自身目录：$targetRoot"
}
if ($targetRoot.StartsWith($skillRoot + $sep, $pathCompare)) {
    throw "目标目录位于技能包内部，已中止：$targetRoot"
}
if ($skillRoot.StartsWith($targetRoot + $sep, $pathCompare)) {
    $relativeToTarget = $skillRoot.Substring($targetRoot.Length).TrimStart('\', '/')
    $depthUnderTarget = @($relativeToTarget -split '[\\/]' | Where-Object { $_ -ne '' }).Count

    if ($depthUnderTarget -lt 2) {
        throw "目标目录是技能包的上级目录，已中止：$targetRoot（技能包恰好是它的直属子目录，极易误覆盖项目根；若确为内嵌部署，请把技能包放到项目的子目录下，例如 tools\assist-skills）"
    }
    Write-Host "[提示] 内嵌布局：技能包位于目标项目的 $relativeToTarget 子目录下，将按项目根目录部署。" -ForegroundColor DarkYellow
}

Write-Host ''
Write-Host '=== assist-skills 参考资料包部署 ===' -ForegroundColor Cyan
Write-Host "技能包目录：$skillRoot"
Write-Host "目标项目：  $targetRoot"
if ($DryRun) { Write-Host '模式：      预览（不写入文件）' -ForegroundColor Yellow }
Write-Host ''

foreach ($required in @('AGENTS.md', 'ai-pilot')) {
    if (-not (Test-Path -LiteralPath (Join-Path $skillRoot $required))) {
        throw "技能包结构不完整，缺少 $required（技能包目录：$skillRoot）"
    }
}

if (-not (Test-Path -LiteralPath $targetRoot)) {
    if ($DryRun) {
        Write-Host "[预览] 将创建目录 $targetRoot" -ForegroundColor Gray
    } else {
        New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null
        Write-Host "[创建] 目标目录 $targetRoot" -ForegroundColor Green
    }
}

# ---------- 1. 参考资料包主体 ----------

$totalSteps = 2
if ($Vendor) { $totalSteps = 3 }

Write-Host "[1/$totalSteps] 复制参考资料包主体" -ForegroundColor Cyan

foreach ($fileName in @('AGENTS.md', 'CLAUDE.md', 'VERSION.md')) {
    $source = Join-Path $skillRoot $fileName
    if (Test-Path -LiteralPath $source) {
        Copy-OneFile -Source $source -Destination (Join-Path $targetRoot $fileName)
    } else {
        Write-Host "  [警告] 技能包缺少 $fileName，已跳过" -ForegroundColor DarkYellow
    }
}

Copy-OneTree -SourceDir (Join-Path $skillRoot 'ai-pilot') -DestinationDir (Join-Path $targetRoot 'ai-pilot')

if ($IncludeSkillFiles) {
    foreach ($fileName in @('README.md', 'README.en.md', 'SKILL.md')) {
        $source = Join-Path $skillRoot $fileName
        if (Test-Path -LiteralPath $source) {
            Copy-OneFile -Source $source -Destination (Join-Path $targetRoot $fileName)
        }
    }
    $scriptsDir = Join-Path $skillRoot 'scripts'
    if (Test-Path -LiteralPath $scriptsDir) {
        Copy-OneTree -SourceDir $scriptsDir -DestinationDir (Join-Path $targetRoot 'scripts')
    }
}

# ---------- 2. 规则文件落位到点目录 ----------

Write-Host ''
Write-Host "[2/$totalSteps] 落地工具规则文件" -ForegroundColor Cyan

if ($SkipRules) {
    Write-Host '  [跳过] 已指定 -SkipRules，未落地 .trae/.codebuddy 规则' -ForegroundColor DarkYellow
} else {
    $ruleMap = @(
        @{ Source = 'rules\trae-poc-rule.md';      Destination = '.trae\rules\poc-rule.md' },
        @{ Source = 'rules\codebuddy-poc-rule.md'; Destination = '.codebuddy\rules\poc-rule.md' }
    )
    foreach ($rule in $ruleMap) {
        $source = Join-Path $skillRoot $rule.Source
        if (Test-Path -LiteralPath $source) {
            Copy-OneFile -Source $source -Destination (Join-Path $targetRoot $rule.Destination)
        } else {
            Write-Host "  [警告] 技能包缺少 $($rule.Source)，已跳过" -ForegroundColor DarkYellow
        }
    }
}

# ---------- 3. 可选：把技能包内嵌到项目，供团队分发 ----------

$vendorCopied = 0
$vendorSkipped = 0

if ($Vendor) {
    Write-Host ''
    Write-Host "[3/$totalSteps] 内嵌技能包到项目（团队分发用）" -ForegroundColor Cyan

    $vendorRoot = (Get-AbsolutePath (Join-Path $targetRoot $VendorDir)).TrimEnd('\', '/')

    if ([string]::Equals($vendorRoot, $skillRoot, $pathCompare)) {
        Write-Host "  [跳过] 内嵌位置就是技能包自身：$vendorRoot" -ForegroundColor DarkYellow
    } else {
        $copiedBefore = $script:copiedCount
        $skippedBefore = $script:skippedCount

        # 不内嵌安装元数据与依赖目录，保持项目目录干净
        Copy-OneTree -SourceDir $skillRoot -DestinationDir $vendorRoot `
            -ExcludeTopLevel @('_meta.json', '.clawhubignore', '.clawhub', '.git', 'node_modules')

        $vendorCopied = $script:copiedCount - $copiedBefore
        $vendorSkipped = $script:skippedCount - $skippedBefore

        if ($DryRun) {
            Write-Host "[预览] 将内嵌技能包到 $vendorRoot" -ForegroundColor Gray
        } else {
            Write-Host "  [内嵌] $vendorRoot（新写入 $vendorCopied 个文件）" -ForegroundColor Green
            Write-Host '  团队成员克隆该仓库后，直接双击 tools\assist-skills\deploy.cmd 即可零输入部署，无需安装技能包。'
        }
    }
}

# ---------- 汇总 ----------

Write-Host ''
Write-Host '=== 部署完成 ===' -ForegroundColor Cyan
if ($DryRun) {
    Write-Host '预览模式：未写入任何文件。去掉 -DryRun 即可实际执行。' -ForegroundColor Yellow
} else {
    $vendorNote = ''
    if ($Vendor) { $vendorNote = "（其中内嵌技能包 $vendorCopied 个文件）" }
    Write-Host "写入 $script:copiedCount 个新文件$vendorNote，覆盖 $script:overwrittenCount 个文件，跳过 $script:skippedCount 个已存在文件。"
}
if ($script:skippedCount -gt 0) {
    Write-Host '提示：被跳过的文件未做改动，确认可以覆盖后加 -Force 重跑。' -ForegroundColor DarkYellow
}
Write-Host ''
Write-Host '下一步：在 AI 对话中输入「初始化项目」，让 AI 扫描项目并预填 AGENTS.md 第 1-4 节。'

# ---------- 可选：创建「发送到」/ 桌面快捷方式 ----------

function New-DeployShortcut {
    param([string]$LinkPath, [string]$EntryPath, [string]$Arguments = '')

    $shell = New-Object -ComObject WScript.Shell
    $link = $shell.CreateShortcut($LinkPath)
    $link.TargetPath = $EntryPath
    $link.WorkingDirectory = (Split-Path -Parent $EntryPath)
    if ($Arguments) { $link.Arguments = $Arguments }
    $link.Description = 'assist-skills 一键部署（AI 开发流程参考资料包）'
    $link.Save()
}

if ($Shortcuts) {
    Write-Host ''
    if ($env:OS -ne 'Windows_NT') {
        Write-Host '[跳过] -Shortcuts 仅支持 Windows。' -ForegroundColor DarkYellow
    } elseif ($DryRun) {
        Write-Host '[预览] 将创建「发送到」菜单与桌面快捷方式「部署AI开发助手(assist-skills)」。' -ForegroundColor Gray
    } else {
        $entry = Join-Path $skillRoot 'deploy.cmd'
        if (-not (Test-Path -LiteralPath $entry)) {
            Write-Host "[跳过] 未找到 $entry，无法创建快捷方式。" -ForegroundColor DarkYellow
        } else {
            $sendTo = Join-Path $env:APPDATA 'Microsoft\Windows\SendTo'
            $desktop = [Environment]::GetFolderPath('Desktop')
            $linkName = '部署AI开发助手(assist-skills).lnk'

            # 「发送到」：右键文件夹即可部署，Windows 会把所选文件夹路径作为参数传入
            if (Test-Path -LiteralPath $sendTo) {
                New-DeployShortcut -LinkPath (Join-Path $sendTo $linkName) -EntryPath $entry -Arguments '-Pause'
                Write-Host "  [快捷方式] $sendTo\$linkName" -ForegroundColor Green
            }
            # 桌面：双击后提示输入目标目录
            if ($desktop -and (Test-Path -LiteralPath $desktop)) {
                New-DeployShortcut -LinkPath (Join-Path $desktop $linkName) -EntryPath $entry
                Write-Host "  [快捷方式] $desktop\$linkName" -ForegroundColor Green
            }
            Write-Host '提示：以后在资源管理器里右键任意项目文件夹 → 发送到 → 部署AI开发助手(assist-skills)，即可一键部署。'
        }
    }
}

if ($Pause) {
    Write-Host ''
    [void](Read-Host '按回车键退出')
}

Write-Host ''
