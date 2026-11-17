# convert2docx.ps1
# 把各种文档格式转成 .docx，并套用用户指定的 reference.docx
# 本脚本不提供默认 reference.docx，必须由用户自己准备

[CmdletBinding()]
param(
    # 单个输入文件（位置参数）
    [Parameter(Position=0)]
    [string]$File = "",

    # 批量模式：从文件列表读取，一行一个路径
    [string]$FileList = "",

    [string]$ReferencePath = "",
    [string]$PandocPath = "",
    [string]$OutputDir = ""
)

# 汇总输入文件
$InputFiles = @()

if ($FileList) {
    if (-not (Test-Path $FileList)) {
        Write-Error "文件列表不存在: $FileList"
        exit 1
    }
    $InputFiles = @(Get-Content $FileList -Encoding UTF8 | Where-Object { $_.Trim() })
} elseif ($File) {
    $InputFiles = @($File)
}

# 支持分隔符传多个文件（bat 拖拽入口使用）
if ($env:C2D_FILES) {
    $fromEnv = $env:C2D_FILES -split '\|' | Where-Object { $_.Trim() }
    if ($fromEnv) {
        $InputFiles = $fromEnv
    }
}

if ($InputFiles.Count -eq 0) {
    Write-Host ""
    Write-Host "===== convert2docx =====" -ForegroundColor Cyan
    Write-Host "错误：未指定输入文件。" -ForegroundColor Red
    Write-Host ""
    Write-Host "用法："
    Write-Host "  1) 拖拽：把文件拖到 convert2docx.bat 上（推荐，支持批量）"
    Write-Host "  2) 单文件：.\convert2docx.ps1 report.md"
    Write-Host "  3) 批量列表：.\convert2docx.ps1 -FileList list.txt"
    Write-Host ""
    Write-Host "可选参数："
    Write-Host "  -ReferencePath <path>   指定 reference.docx"
    Write-Host "  -OutputDir <path>       指定输出目录"
    Write-Host "  -PandocPath <path>      指定 pandoc.exe"
    exit 1
}

$ErrorActionPreference = "Continue"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = Split-Path -Parent $scriptDir
$configPath = Join-Path $skillRoot "config.ini"

# ===== 初始化配置（首次运行） =====
function Initialize-Config {
    Write-Host ""
    Write-Host "===== 首次运行配置 =====" -ForegroundColor Cyan

    # Pandoc 路径
    $pandoc = $null
    $pandocInPath = Get-Command pandoc.exe -ErrorAction SilentlyContinue
    if ($pandocInPath) {
        $defaultPandoc = $pandocInPath.Source
        Write-Host "已在 PATH 中找到 pandoc: $defaultPandoc"
        $resp = Read-Host "直接回车使用此路径，或输入其他 pandoc.exe 路径"
        $pandoc = if ($resp) { $resp.Trim().Trim('"') } else { $defaultPandoc }
    } else {
        Write-Host "未在 PATH 中找到 pandoc.exe" -ForegroundColor Yellow
        $resp = Read-Host "请输入 pandoc.exe 完整路径（如 C:\Program Files\Pandoc\pandoc.exe）"
        if (-not $resp) {
            Write-Error "pandoc 路径不能为空"
            exit 1
        }
        $pandoc = $resp.Trim().Trim('"')
    }

    # 验证 pandoc 存在
    if (-not (Test-Path $pandoc)) {
        Write-Error "pandoc.exe 不存在: $pandoc"
        Write-Host "请先安装 pandoc: https://pandoc.org/installing.html"
        exit 1
    }

    # reference.docx 路径（必填，不提供则退出）
    Write-Host ""
    Write-Host "本工具不提供默认 reference.docx 模板，你必须自己准备一份。" -ForegroundColor Yellow
    Write-Host "制作方法：用 Word 打开 pandoc 生成的任意 docx，改好样式后另存。" -ForegroundColor Yellow
    $ref = Read-Host "`n请输入 reference.docx 完整路径（必填）"
    $ref = if ($ref) { $ref.Trim().Trim('"') } else { "" }

    if (-not $ref) {
        Write-Error "reference.docx 路径不能为空。请先准备样式模板再运行。"
        exit 1
    }
    if (-not (Test-Path $ref)) {
        Write-Error "reference.docx 不存在: $ref"
        exit 1
    }
    if ([IO.Path]::GetExtension($ref).ToLower() -ne '.docx') {
        Write-Error "reference 文件必须是 .docx 格式"
        exit 1
    }

    # 写入配置
    $iniContent = "[pandoc]`npath=$pandoc`n`n[reference]`npath=$ref`n"
    [IO.File]::WriteAllText($configPath, $iniContent, [Text.UTF8Encoding]::new($false))

    Write-Host ""
    Write-Host "配置已保存到 $configPath" -ForegroundColor Green
    return @{ Pandoc = $pandoc; Reference = $ref }
}

# ===== 读取配置 =====
function Get-Config {
    if (-not (Test-Path $configPath)) {
        return Initialize-Config
    }

    $pandoc = $null
    $ref = $null
    $currentSection = ""

    foreach ($line in [IO.File]::ReadLines($configPath)) {
        $line = $line.Trim()
        if ($line -match '^\[(.+?)\]') {
            $currentSection = $matches[1]
        }
        elseif ($line -match '^path\s*=\s*(.+)$') {
            $value = $matches[1].Trim()
            if ($currentSection -eq 'pandoc') { $pandoc = $value }
            elseif ($currentSection -eq 'reference') { $ref = $value }
        }
    }

    $needsReinit = $false

    if (-not $pandoc -or -not (Test-Path $pandoc)) {
        Write-Warning "config.ini 中 pandoc 路径无效，重新配置..."
        $needsReinit = $true
    }
    if (-not $ref -or -not (Test-Path $ref)) {
        Write-Warning "config.ini 中 reference.docx 路径无效，重新配置..."
        $needsReinit = $true
    }

    if ($needsReinit) {
        return Initialize-Config
    }

    return @{ Pandoc = $pandoc; Reference = $ref }
}

# ===== 转换单个文件 =====
function Convert-OneFile {
    param(
        [string]$FilePath,
        [string]$PandocExe,
        [string]$ReferenceDoc,
        [string]$OutDir
    )

    $ext = [IO.Path]::GetExtension($FilePath).ToLower()
    $baseName = [IO.Path]::GetFileNameWithoutExtension($FilePath)

    # 输出路径
    if ($OutDir) {
        $outputPath = Join-Path $OutDir "$baseName.docx"
    } else {
        $inputDir = Split-Path -Parent $FilePath
        $outputPath = Join-Path $inputDir "$baseName.docx"
    }

    # docx 输入时加 _restyled 后缀，避免覆盖原件
    if ($ext -eq '.docx') {
        $outputPath = $outputPath -replace '\.docx$', '_restyled.docx'
    }

    # 已存在则跳过
    if (Test-Path $outputPath) {
        Write-Host "[跳过] $outputPath 已存在" -ForegroundColor Yellow
        return 'skipped'
    }

    # 调用 pandoc
    $formatMap = @{
        '.md' = 'markdown'; '.markdown' = 'markdown'; '.txt' = 'markdown'
        '.html' = 'html'; '.htm' = 'html'
        '.rtf' = 'rtf'
        '.tex' = 'latex'
        '.rst' = 'rst'
        '.org' = 'org'
        '.docx' = 'docx'
    }
    $inputFormat = $formatMap[$ext]
    if (-not $inputFormat) {
        Write-Host "[失败] 不支持的格式 $ext : $FilePath" -ForegroundColor Red
        return 'failed'
    }

    $pandocArgs = @(
        '-f', $inputFormat,
        '-t', 'docx',
        '-o', "`"$outputPath`"",
        '--reference-doc', "`"$ReferenceDoc`"",
        "`"$FilePath`""
    )

    try {
        $process = Start-Process -FilePath $PandocExe -ArgumentList $pandocArgs -Wait -PassThru -NoNewWindow
        if ($process.ExitCode -eq 0 -and (Test-Path $outputPath)) {
            Write-Host "[成功] $FilePath -> $outputPath" -ForegroundColor Green
            return 'success'
        } else {
            Write-Host "[失败] $FilePath (pandoc exit code: $($process.ExitCode))" -ForegroundColor Red
            return 'failed'
        }
    } catch {
        Write-Host "[失败] $FilePath : $_" -ForegroundColor Red
        return 'failed'
    }
}

# ===== 主流程 =====
Write-Host ""
Write-Host "===== convert2docx =====" -ForegroundColor Cyan
Write-Host "输入文件数: $($InputFiles.Count)"
Write-Host ""

# 获取配置（或首次初始化）
$config = Get-Config
$pandocExe = if ($PandocPath) { $PandocPath } else { $config.Pandoc }
$referenceDoc = if ($ReferencePath) { $ReferencePath } else { $config.Reference }

# 验证 reference 必填
if (-not $referenceDoc) {
    Write-Error "必须指定 reference.docx（用 -ReferencePath 参数或先运行初始化配置）"
    exit 1
}
if (-not (Test-Path $referenceDoc)) {
    Write-Error "reference.docx 不存在: $referenceDoc"
    exit 1
}

# 验证 pandoc
if (-not (Test-Path $pandocExe)) {
    $pandocInPath = Get-Command pandoc.exe -ErrorAction SilentlyContinue
    if ($pandocInPath) {
        $pandocExe = $pandocInPath.Source
    } else {
        Write-Error "找不到 pandoc.exe，请安装或配置路径"
        exit 1
    }
}

Write-Host "pandoc:    $pandocExe"
Write-Host "reference: $referenceDoc"
Write-Host ""

# 支持的格式
$supportedExts = @('.md', '.markdown', '.txt', '.html', '.htm', '.rtf', '.tex', '.rst', '.org', '.docx')

# 批量转换
$success = 0
$failed = 0
$skipped = 0

foreach ($file in $InputFiles) {
    $file = $file.Trim('"')

    if (-not (Test-Path $file)) {
        Write-Host "[失败] 文件不存在: $file" -ForegroundColor Red
        $failed++
        continue
    }

    $ext = [IO.Path]::GetExtension($file).ToLower()
    if ($supportedExts -notcontains $ext) {
        Write-Host "[跳过] 不支持的格式 ${ext}: $file" -ForegroundColor Yellow
        $skipped++
        continue
    }

    $outDir = if ($OutputDir) { $OutputDir } else { Split-Path -Parent $file }

    $result = Convert-OneFile -FilePath $file -PandocExe $pandocExe -ReferenceDoc $referenceDoc -OutDir $outDir
    switch ($result) {
        'success' { $success++ }
        'failed'  { $failed++ }
        'skipped' { $skipped++ }
    }
}

Write-Host ""
Write-Host "===== 转换完成 =====" -ForegroundColor Cyan
Write-Host "成功: $success  失败: $failed  跳过: $skipped"

if ($failed -gt 0) { exit 1 }
exit 0
