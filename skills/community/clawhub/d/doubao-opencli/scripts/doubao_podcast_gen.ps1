<#
.SYNOPSIS
  豆包 AI 播客生成脚本 - 通过 opencli browser 桥接自动生成并下载播客音频

.DESCRIPTION
  使用 opencli browser 桥接复用 Edge 登录态，自动完成：
  1. 打开豆包聊天页
  2. 点击 AI 播客按钮
  3. 输入内容（支持文字/网页链接/PDF文件三种方式）
  4. 等待播客生成
  5. 播放播客（等待下载按钮可用）
  6. 点击下载按钮
  7. 从 Downloads 搬运到 output 目录
  8. 裁剪开头广告（ffmpeg）

.PARAMETER Text
  播客主题、完整文章、大纲或脚本文字（与 -Url、-File 三选一）

.PARAMETER Url
  网页链接，豆包自动抓取内容生成播客（与 -Text、-File 三选一）

.PARAMETER File
  PDF 文件路径，豆包根据文档内容生成播客（与 -Text、-Url 三选一）

.PARAMETER OutputDir
  输出目录（默认: output/doubao_podcasts/）

.PARAMETER WaitPlay
  播放等待秒数（默认: 40，下载按钮通常在播放20-40秒后可用）

.PARAMETER TrimSeconds
  切掉音频前N秒（默认: 4，豆包播客开头通常有广告，设为0则不裁剪）

.EXAMPLE
  # 主题模式
  .\doubao_podcast_gen.ps1 -Text "介绍人工智能的发展历史"

  # 网页模式
  .\doubao_podcast_gen.ps1 -Url "https://example.com/article"

  # 文件模式
  .\doubao_podcast_gen.ps1 -File "C:\docs\我的文章.pdf"

  # 自定义参数
  .\doubao_podcast_gen.ps1 -Text "你的主题" -WaitPlay 30 -TrimSeconds 0
#>

param(
    [string]$Text,

    [string]$Url,

    [string]$File,

    [string]$OutputDir = "",

    [int]$WaitPlay = 40,

    [int]$TrimSeconds = 4
)

# --- 参数校验：Text、Url、File 三选一 ---
$inputModes = @()
if ($Text) { $inputModes += "Text" }
if ($Url) { $inputModes += "Url" }
if ($File) { $inputModes += "File" }

if ($inputModes.Count -eq 0) {
    Write-Host "❌ 请指定输入方式：-Text（文字）、-Url（网页链接）、-File（PDF文件），三选一" -ForegroundColor Red
    exit 1
}
if ($inputModes.Count -gt 1) {
    Write-Host "❌ -Text、-Url、-File 不能同时使用，请三选一" -ForegroundColor Red
    exit 1
}

# 如果是文件模式，检查文件是否存在
if ($File -and -not (Test-Path $File)) {
    Write-Host "❌ 文件不存在: $File" -ForegroundColor Red
    exit 1
}

# 如果是文件模式，检查是否为 PDF
if ($File) {
    $ext = [System.IO.Path]::GetExtension($File).ToLower()
    if ($ext -ne ".pdf") {
        Write-Host "❌ 仅支持 PDF 文件上传，当前文件类型: $ext" -ForegroundColor Red
        exit 1
    }
}

# --- 路径配置 ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Workspace = Resolve-Path "$ScriptDir\..\..\.."
if ($OutputDir -eq "") {
    $OutputDir = Join-Path $Workspace "output" | Join-Path -ChildPath "doubao_podcasts"
}
$DownloadsDir = Join-Path $env:USERPROFILE "Downloads"

# 确保输出目录存在
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

Write-Host "=== 豆包 AI 播客生成器 ===" -ForegroundColor Cyan
switch ($inputModes[0]) {
    "Text" { Write-Host "输入方式: 文字" -ForegroundColor Yellow; Write-Host "内容: $Text" -ForegroundColor Gray }
    "Url"  { Write-Host "输入方式: 网页链接" -ForegroundColor Yellow; Write-Host "链接: $Url" -ForegroundColor Gray }
    "File" { Write-Host "输入方式: PDF 文件" -ForegroundColor Yellow; Write-Host "文件: $File" -ForegroundColor Gray }
}
Write-Host ""

# --- Step 1: 打开豆包聊天页并最大化窗口 ---
Write-Host "[1/8] 打开豆包聊天页并最大化窗口..." -ForegroundColor Green
$pageResult = opencli browser open "https://www.doubao.com/chat" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 打开页面失败，请检查 Edge 登录状态" -ForegroundColor Red
    exit 1
}
Start-Sleep 3
# 最大化窗口，确保所有按钮可见（豆包页面在窗口不够大时会隐藏部分按钮）
opencli browser eval "window.moveTo(0,0); window.resizeTo(window.screen.availWidth, window.screen.availHeight);" 2>$null
Start-Sleep 1
Write-Host "  ✅ 窗口已最大化" -ForegroundColor Green

# --- Step 2: 点击 AI 播客按钮 ---
Write-Host "[2/8] 查找并点击 AI 播客按钮..." -ForegroundColor Green
$state = opencli browser state 2>$null
$podcastRef = $null

# 方法1: 用 CSS 选择器找 AI 播客按钮
$findResult = opencli browser find --css "button:has(div:text('AI播客')), div:text('AI播客')" 2>$null
if ($LASTEXITCODE -eq 0 -and $findResult) {
    $podcastRef = ($findResult | Select-String -Pattern "ref=(\d+)" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
}

# 方法2: 在 state 中搜索 AI 播客文本
if (-not $podcastRef) {
    $podcastLine = $state | Select-String -Pattern "AI 播客|AI播客" | Select-Object -First 1
    if ($podcastLine) {
        $podcastRef = ($podcastLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
    }
}

if ($podcastRef) {
    opencli browser click $podcastRef 2>$null
    Write-Host "  -> 点击 ref [$podcastRef]" -ForegroundColor Gray
} else {
    Write-Host "  -> 尝试点击已知位置的 AI 播客按钮 [305]..." -ForegroundColor Gray
    opencli browser click 305 2>$null
}
Start-Sleep 2

# --- Step 3: 输入内容（文字/网页/文件 三选一） ---
switch ($inputModes[0]) {
    "Text" {
        Write-Host "[3/8] 输入播客文字内容..." -ForegroundColor Green
        $state = opencli browser state 2>$null
        $inputRef = $null

        $findResult = opencli browser find --css "textarea[placeholder*='输入主题'], textarea[placeholder*='添加网页']" 2>$null
        if ($LASTEXITCODE -eq 0 -and $findResult) {
            $inputRef = ($findResult | Select-String -Pattern "ref=(\d+)" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
        }

        if (-not $inputRef) {
            $textareaLine = $state | Select-String -Pattern "textarea" | Select-Object -First 1
            if ($textareaLine) {
                $inputRef = ($textareaLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
            }
        }

        if ($inputRef) {
            opencli browser fill $inputRef --value "$Text" 2>$null
            Write-Host "  -> 填入 ref [$inputRef]" -ForegroundColor Gray
        } else {
            Write-Host "  -> 尝试直接填入 textarea..." -ForegroundColor Gray
            opencli browser fill 301 --value "$Text" 2>$null
        }
        Start-Sleep 1
    }

    "Url" {
        Write-Host "[3/8] 输入网页链接..." -ForegroundColor Green
        $state = opencli browser state 2>$null
        $inputRef = $null

        $findResult = opencli browser find --css "textarea[placeholder*='输入主题'], textarea[placeholder*='添加网页']" 2>$null
        if ($LASTEXITCODE -eq 0 -and $findResult) {
            $inputRef = ($findResult | Select-String -Pattern "ref=(\d+)" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
        }

        if (-not $inputRef) {
            $textareaLine = $state | Select-String -Pattern "textarea" | Select-Object -First 1
            if ($textareaLine) {
                $inputRef = ($textareaLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
            }
        }

        if ($inputRef) {
            opencli browser fill $inputRef --value "$Url" 2>$null
            Write-Host "  -> 填入链接 ref [$inputRef]" -ForegroundColor Gray
        } else {
            Write-Host "  -> 尝试直接填入 textarea..." -ForegroundColor Gray
            opencli browser fill 301 --value "$Url" 2>$null
        }
        Start-Sleep 1
    }

    "File" {
        Write-Host "[3/8] 上传 PDF 文件..." -ForegroundColor Green
        # 找文件上传 input
        $state = opencli browser state 2>$null
        $fileInputRef = $null

        $fileInputLine = $state | Select-String -Pattern "type=file" | Select-Object -First 1
        if ($fileInputLine) {
            $fileInputRef = ($fileInputLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
        }

        if ($fileInputRef) {
            # 使用 opencli browser upload 上传文件（如果支持）
            # 否则尝试用 fill 传入文件路径
            $uploadResult = opencli browser fill $fileInputRef --value "$File" 2>$null
            Write-Host "  -> 上传文件到 ref [$fileInputRef]" -ForegroundColor Gray
            Start-Sleep 2
        } else {
            # 备用方案：尝试点击上传区域
            Write-Host "  -> 尝试点击上传区域..." -ForegroundColor Gray
            opencli browser click 303 2>$null
            Start-Sleep 1
            # 通过 fill 到文件输入
            $uploadResult = opencli browser fill 295 --value "$File" 2>$null
            Start-Sleep 2
        }
        Write-Host "  ✅ 文件已上传" -ForegroundColor Green
    }
}

# --- Step 4: 点击发送按钮 ---
Write-Host "[4/8] 发送请求..." -ForegroundColor Green
# 尝试多种方式找到发送按钮
$sendClicked = $false

# 方式1: 通过 SVG data-opencli-ref
opencli browser click 296 2>$null
$sendClicked = $true
Start-Sleep 3

# 方式2: 如果方式1没生效，尝试点 SVG 的父容器
if (-not $sendClicked) {
    opencli browser eval @"
    const svg = document.querySelector('svg[data-opencli-ref]');
    if (svg) {
        const btn = svg.closest('div[role=button], button, div.clickable');
        if (btn) btn.click();
    }
"@ 2>$null
    Start-Sleep 2
}

# --- Step 5: 等待播客生成 ---
Write-Host "[5/8] 等待播客生成..." -ForegroundColor Green
$maxWait = 120
$waited = 0
$podcastReady = $false

while ($waited -lt $maxWait) {
    Start-Sleep 5
    $waited += 5
    $state = opencli browser state 2>$null
    
    # 检查是否出现播客卡片（有封面图或时长信息）
    if ($state -match "\d+:\d+.*\d+:\d+" -or $state -match "byteimg.*tos-cn-i") {
        $podcastReady = $true
        Write-Host "  -> 播客已生成！（等待 $waited 秒）" -ForegroundColor Green
        break
    }
    
    # 也检查页面中是否有播客播放器UI
    $hasPlayer = opencli browser eval "document.querySelector('audio') !== null || document.body.innerText.includes('正在播放') || document.body.innerText.includes('播客') && document.body.innerText.includes('秒')" 2>$null
    if ($hasPlayer -eq "true") {
        $podcastReady = $true
        Write-Host "  -> 检测到播客播放器！（等待 $waited 秒）" -ForegroundColor Green
        break
    }
    
    Write-Host "  -> 等待中... ($waited 秒)" -ForegroundColor Gray
}

if (-not $podcastReady) {
    Write-Host "⚠️ 播客可能还在生成中，继续尝试..." -ForegroundColor Yellow
}

# --- Step 6: 播放并等待下载按钮可用 ---
Write-Host "[6/8] 播放播客，等待下载按钮可用（约${WaitPlay}秒）..." -ForegroundColor Green

# 用 JS 查找播放按钮并点击
$playResult = opencli browser eval @"
(function() {
    // 找播放按钮：播放器区域中有 SVG 且文本包含 1x 的附近按钮
    const allDivs = document.querySelectorAll('div[tabindex]');
    for (const el of allDivs) {
        if (el.offsetParent === null) continue;
        const rect = el.getBoundingClientRect();
        const svg = el.querySelector('svg');
        // 播放按钮：在播放器区域左侧，有 SVG，无 aria-haspopup
        if (svg && rect.top > 350 && rect.top < 400 && rect.left > 270 && rect.left < 310 && rect.width > 20) {
            el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true, view: window}));
            el.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true, view: window}));
            el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
            return 'played_' + el.tagName;
        }
    }
    return 'play_btn_not_found';
})();
"@ 2>$null

Write-Host "  -> JS播放结果: $playResult" -ForegroundColor Gray

# 等待下载按钮可用
$waited = 0
while ($waited -lt $WaitPlay) {
    Start-Sleep 5
    $waited += 5
    Write-Host "  -> 播放中... ($waited 秒)" -ForegroundColor Gray
}

# --- Step 7: 点击下载按钮（JS原生事件触发） ---
Write-Host "[7/8] 点击下载按钮..." -ForegroundColor Green

# 先记录当前 Downloads 目录的快照
$downloadCheckTime = Get-Date
$beforeSnapshot = @{}
Get-ChildItem $DownloadsDir -Filter "*.wav" | ForEach-Object { $beforeSnapshot[$_.Name] = $_.Length }

# 用 JS 原生事件触发下载（opencli browser click 有时无法触发）
$downloadResult = opencli browser eval @"
(function() {
    // 查找下载按钮：class 包含 downloadBtn 的 span[role=img] 的父 div[tabindex]
    const allDivs = document.querySelectorAll('div[tabindex]');
    for (const el of allDivs) {
        const span = el.querySelector('span[role=img]');
        if (span && span.className.includes('downloadBtn')) {
            // 使用原生 MouseEvent 和 PointerEvent 确保触发
            el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true, view: window}));
            el.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true, view: window}));
            el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
            el.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true, cancelable: true, view: window}));
            return 'dispatched_events_on_download_btn';
        }
    }
    return 'download_btn_not_found';
})();
"@ 2>$null

Write-Host "  -> JS触发结果: $downloadResult" -ForegroundColor Gray
Start-Sleep 3

# 等待下载完成（最多等20秒）
$waitDownload = 0
$downloadedFile = $null
while ($waitDownload -lt 20) {
    Start-Sleep 3
    $waitDownload += 3
    
    $currentFiles = Get-ChildItem $DownloadsDir -Filter "*.wav"
    foreach ($f in $currentFiles) {
        $oldSize = $beforeSnapshot[$f.Name]
        if (-not $oldSize) {
            $downloadedFile = $f.FullName
            Write-Host "  -> 检测到新文件: $($f.Name)" -ForegroundColor Gray
            break
        } elseif ($f.Length -ne $oldSize -and $f.LastWriteTime -ge $downloadCheckTime) {
            $downloadedFile = $f.FullName
            Write-Host "  -> 文件已更新: $($f.Name)" -ForegroundColor Gray
            break
        }
    }
    if ($downloadedFile) { break }
    Write-Host "  -> 等待下载... ($waitDownload 秒)" -ForegroundColor Gray
}

if ($downloadedFile -and (Test-Path $downloadedFile)) {
    Write-Host "  ✅ 下载成功: $downloadedFile" -ForegroundColor Green
    
    # 用时间戳命名，避免覆盖旧文件
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $newFileName = "AI新闻播客_${timestamp}.wav"
    $outputFile = Join-Path $OutputDir $newFileName
    
    Copy-Item $downloadedFile $outputFile -Force
    Write-Host "  ✅ 已搬运到: $outputFile" -ForegroundColor Green
    
    $fileInfo = Get-Item $outputFile
    $sizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
    Write-Host "  📊 文件大小: ${sizeMB}MB" -ForegroundColor Cyan
} else {
    Write-Host "  ❌ 下载失败：未检测到新文件" -ForegroundColor Red
    exit 1
}

# --- Step 8: 裁剪开头广告（ffmpeg） ---
if ($TrimSeconds -gt 0) {
    Write-Host "[8/8] 裁剪音频开头 ${TrimSeconds} 秒（去广告）..." -ForegroundColor Green
    
    $trimmedFile = Join-Path $OutputDir "$([System.IO.Path]::GetFileNameWithoutExtension($outputFile))_去广告.wav"
    
    $ffmpegCmd = "ffmpeg -y -i `"$outputFile`" -ss $TrimSeconds -c copy `"$trimmedFile`" 2>&1"
    $ffmpegResult = Invoke-Expression $ffmpegCmd
    
    if ($LASTEXITCODE -eq 0 -and (Test-Path $trimmedFile)) {
        # 删除原文件，用裁剪后的替换
        Remove-Item $outputFile -Force
        Rename-Item $trimmedFile -NewName ([System.IO.Path]::GetFileName($outputFile)) -Force
        
        $trimmedInfo = Get-Item $outputFile
        $trimmedSizeMB = [math]::Round($trimmedInfo.Length / 1MB, 2)
        Write-Host "  ✅ 裁剪完成！已切掉前 ${TrimSeconds} 秒" -ForegroundColor Green
        Write-Host "  📊 最终文件: $outputFile (${trimmedSizeMB}MB)" -ForegroundColor Cyan
        
        # 用 ffprobe 获取裁剪后时长
        $duration = ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$outputFile" 2>$null
        if ($duration) {
            $totalSec = [math]::Round([double]$duration)
            $mins = [math]::Floor($totalSec / 60)
            $secs = $totalSec % 60
            Write-Host "  ⏱️  裁剪后时长: ${mins}分${secs}秒" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ⚠️ 裁剪失败，保留原文件（请确保 ffmpeg 已安装）" -ForegroundColor Yellow
        Write-Host "  ffmpeg 输出: $ffmpegResult" -ForegroundColor Gray
    }
} else {
    Write-Host "[8/8] 跳过裁剪（TrimSeconds=0）" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== 完成 ===" -ForegroundColor Cyan