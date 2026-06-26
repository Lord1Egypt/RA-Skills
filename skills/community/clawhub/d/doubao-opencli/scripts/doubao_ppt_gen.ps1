<#
.SYNOPSIS
  豆包 AI PPT 生成与下载脚本 - 基于 opencli browser 实测流程

.DESCRIPTION
  使用 opencli browser 桥接复用 Edge 登录态，自动完成：
  1. 打开豆包聊天页，触发 PPT 生成
  2. 支持多种输入源：主题、大纲、草稿文档
  3. 监控生成阶段（思考→素材收集→图片生成→合成渲染→完成）
  4. 点击 PPT 标题打开编辑器
  5. 点击工具栏"下载"按钮 → 选择 PPTX → 自动下载

  实测总耗时：约 13-15 分钟（23页 PPT）
  下载方式：工具栏下载按钮 → 选择 PPTX 格式 → 自动保存到 Downloads

.PARAMETER Topic
  PPT 主题

.PARAMETER Outline
  PPT 大纲文本

.PARAMETER DraftFile
  草稿文档路径（支持 .txt/.md）

.PARAMETER OutputDir
  输出目录（默认: output/doubao_ppt/）

.PARAMETER WaitTimeout
  总等待超时（秒，默认: 1200 = 20分钟）

.PARAMETER MonitorInterval
  页面监控间隔（秒，默认: 15）

.EXAMPLE
  .\doubao_ppt_gen.ps1 -Topic "人工智能发展史"

  .\doubao_ppt_gen.ps1 -Outline "1. 引言`n2. 技术原理`n3. 应用场景"

  .\doubao_ppt_gen.ps1 -DraftFile "C:\docs\my_draft.md"
#>

param(
    [Parameter(ParameterSetName="Topic")]
    [string]$Topic,

    [Parameter(ParameterSetName="Outline")]
    [string]$Outline,

    [Parameter(ParameterSetName="Draft")]
    [string]$DraftFile,

    [string]$OutputDir = "",

    [int]$WaitTimeout = 1200,

    [int]$MonitorInterval = 15
)

# --- 路径配置 ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Workspace = Resolve-Path "$ScriptDir\..\..\.."
if ($OutputDir -eq "") {
    $OutputDir = Join-Path $Workspace "output" | Join-Path -ChildPath "doubao_ppt"
}
$DownloadsDir = Join-Path $env:USERPROFILE "Downloads"
$LogDir = Join-Path $OutputDir "logs"

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

# --- 日志 ---
$LogFile = Join-Path $LogDir ("ppt_log_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + ".md")
function Write-Log {
    param([string]$Msg, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] [$Level] $Msg"
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
    switch ($Level) {
        "ERROR" { Write-Host $line -ForegroundColor Red }
        "WARN"  { Write-Host $line -ForegroundColor Yellow }
        "OK"    { Write-Host $line -ForegroundColor Green }
        "PHASE" { Write-Host $line -ForegroundColor Cyan }
        default { Write-Host $line -ForegroundColor Gray }
    }
}

# --- 辅助函数 ---
function Get-PageExtract {
    return opencli browser extract 2>$null
}

function Get-PageText {
    return opencli browser get text "main" 2>$null
}

function Wait-AndCheck {
    param([int]$Seconds = 5)
    Start-Sleep $Seconds
    return Get-PageExtract
}

# --- 输入验证 ---
$inputSource = ""
$inputValue = ""
if ($Topic) {
    $inputSource = "主题"
    $inputValue = $Topic
} elseif ($Outline) {
    $inputSource = "大纲"
    $inputValue = $Outline
} elseif ($DraftFile) {
    $inputSource = "草稿文档"
    if (-not (Test-Path $DraftFile)) {
        Write-Host "❌ 草稿文档不存在: $DraftFile" -ForegroundColor Red
        exit 1
    }
    $inputValue = Get-Content $DraftFile -Raw -Encoding UTF8
} else {
    Write-Host "❌ 请提供输入源：-Topic / -Outline / -DraftFile" -ForegroundColor Red
    Write-Host "用法: .\doubao_ppt_gen.ps1 -Topic `"PPT主题`"" -ForegroundColor Yellow
    exit 1
}

Write-Log "=== 豆包 AI PPT 生成器 ===" "PHASE"
Write-Log "输入源: $inputSource" "INFO"
Write-Log "输入值: $($inputValue.Substring(0, [Math]::Min(200, $inputValue.Length)))" "INFO"
Write-Log "输出目录: $OutputDir" "INFO"
Write-Log "总超时: ${WaitTimeout}s" "INFO"
Write-Log "日志文件: $LogFile" "INFO"
Write-Host ""

# ============================================================
# Step 1: 打开豆包聊天页
# ============================================================
Write-Log "[1/5] 打开豆包聊天页..." "PHASE"
$pageResult = opencli browser open "https://www.doubao.com/chat" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Log "❌ 打开页面失败，请检查 Edge 登录状态" "ERROR"
    exit 1
}
Start-Sleep 5

# ============================================================
# Step 2: 触发 PPT 生成
# ============================================================
Write-Log "[2/5] 触发 PPT 生成..." "PHASE"

# 构造提示词
$promptText = ""
switch ($inputSource) {
    "主题" { $promptText = "请帮我生成一份关于「${Topic}」的PPT" }
    "大纲" { $promptText = "请根据以下大纲生成PPT：`n${Outline}" }
    "草稿文档" { $promptText = "请根据以下文档内容生成PPT：`n${inputValue}" }
}

# --- 2a: 填入提示词到 textarea ---
# 注意：使用普通聊天模式，不要点击 PPT 快捷按钮
# PPT 快捷按钮模式没有发送按钮，无法提交
Write-Log "  -> 找输入框（textarea）..." "INFO"

$state = opencli browser state 2>$null
$textareaRef = $null

# 找 textarea（普通聊天模式的输入框）
$findResult = opencli browser find --css "textarea[placeholder]" 2>$null
if ($LASTEXITCODE -eq 0 -and $findResult) {
    $textareaRef = ($findResult | Select-String -Pattern "ref=(\d+)" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
}

if ($textareaRef) {
    # 使用 eval 设置 textarea 的值（比 fill 更可靠）
    opencli browser eval "var ta = document.querySelector('textarea[placeholder]'); if(ta) { var setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set; setter.call(ta, '" + $promptText.Replace("'", "\'") + "'); ta.dispatchEvent(new Event('input', {bubbles:true})); 'filled' }" 2>$null
    Write-Log "  -> 填入 textarea ref [$textareaRef]" "INFO"
} else {
    Write-Log "  ⚠️ 找不到 textarea，尝试找 contenteditable div..." "WARN"
    $ceRef = $null
    $ceResult = opencli browser find --css "div[contenteditable=true]" 2>$null
    if ($LASTEXITCODE -eq 0 -and $ceResult) {
        $ceRef = ($ceResult | Select-String -Pattern "ref=(\d+)" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
    }
    if ($ceRef) {
        opencli browser eval "var tb = document.querySelector('div[contenteditable=true]'); if(tb) { tb.textContent = '" + $promptText.Replace("'", "\'") + "'; tb.dispatchEvent(new Event('input', {bubbles:true})); 'filled' }" 2>$null
        Write-Log "  -> 填入 contenteditable ref [$ceRef]" "INFO"
    } else {
        Write-Log "  ❌ 找不到任何输入框" "ERROR"
        exit 1
    }
}
Start-Sleep 2

# --- 2b: 点击发送按钮 ---
Write-Log "  -> 点击发送（#flow-end-msg-send）..." "INFO"
opencli browser click "#flow-end-msg-send" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Log "  ⚠️ #flow-end-msg-send 未找到，尝试找发送按钮..." "WARN"
    # 备用：在 state 中找发送按钮
    $state = opencli browser state 2>$null
    $sendBtnRef = $null
    $sendLine = $state | Select-String -Pattern "flow-end-msg-send" | Select-Object -First 1
    if ($sendLine) {
        $sendBtnRef = ($sendLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
    }
    if ($sendBtnRef) {
        Write-Log "  -> 点击发送按钮 ref [$sendBtnRef]" "INFO"
        opencli browser click $sendBtnRef 2>$null
    } else {
        Write-Log "  ❌ 找不到发送按钮" "ERROR"
        exit 1
    }
}
Start-Sleep 5

# ============================================================
# Step 3: 监控生成进度
# ============================================================
Write-Log "[3/5] 监控生成进度（总超时 ${WaitTimeout}s）..." "PHASE"
Write-Log "开始监控时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "INFO"
Write-Host ""

$startTime = Get-Date
$elapsed = 0
$lastPhase = 0
$phaseStartTime = $startTime
$phaseLog = @()
$stuckCount = 0
$lastContentHash = ""

while ($elapsed -lt $WaitTimeout) {
    Start-Sleep $MonitorInterval
    $elapsed = [math]::Round(((Get-Date) - $startTime).TotalSeconds)
    $now = Get-Date -Format "HH:mm:ss"

    $extract = Get-PageExtract
    $pageText = ""
    try { $pageText = (Get-PageText).value } catch {}

    $contentToCheck = $extract + " " + $pageText

    # 阶段检测
    $currentPhase = 0
    $phaseDesc = "等待开始..."

    if ($contentToCheck -match "已完成PPT生成|已完成.*PPT.*生成|PPT.*已完成") {
        $currentPhase = 5
        $phaseDesc = "PPT已完成"
    } elseif ($contentToCheck -match "正在生成PPT|正在生成.*PPT|PPT.*合成|PPT.*渲染|已生成PPT") {
        $currentPhase = 4
        $phaseDesc = "PPT合成与渲染"
    } elseif ($contentToCheck -match "生成.*图片|图片.*生成|已完成图片生成|配图|插图") {
        $currentPhase = 3
        $phaseDesc = "生成原创图片"
    } elseif ($contentToCheck -match "思考.*优化|补充.*收集|优化.*思考|深入思考|大纲.*整理") {
        $currentPhase = 2
        $phaseDesc = "思考优化 + 补充收集"
    } elseif ($contentToCheck -match "思考中|正在收集|收集素材|分析中|正在分析|PPT素材") {
        $currentPhase = 1
        $phaseDesc = "思考状态 + 素材收集"
    }

    # 阶段变更日志
    if ($currentPhase -ne $lastPhase) {
        if ($lastPhase -gt 0) {
            $phaseDuration = [math]::Round(((Get-Date) - $phaseStartTime).TotalSeconds)
            $phaseLog += "[阶段${lastPhase}] ${phaseDuration}s"
            Write-Log "  └─ 阶段${lastPhase}完成，耗时 ${phaseDuration}s" "OK"
        }
        if ($currentPhase -gt 0) {
            $phaseStartTime = Get-Date
            Write-Log "  ┌─ 进入阶段${currentPhase}: ${phaseDesc} [${now}]" "PHASE"
        }
        $lastPhase = $currentPhase
        $stuckCount = 0
    } else {
        $stuckCount++
    }

    # 完成检测
    if ($currentPhase -eq 5) {
        Write-Log "✅ PPT 生成完成！总耗时 ${elapsed}s" "OK"
        Write-Log "阶段记录: $($phaseLog -join ' → ')" "INFO"
        break
    }

    # 进度输出
    $progressPct = [math]::Round(($currentPhase / 5.0) * 100)
    Write-Host ("  [${now}] ${elapsed}s | ${progressPct}% | ${phaseDesc}") -ForegroundColor DarkGray

    # 卡住检测（连续 8 次无变化 ≈ 2 分钟）
    if ($stuckCount -ge 8) {
        $contentHash = ($extract | Get-FileHash -Algorithm MD5).Hash
        if ($contentHash -eq $lastContentHash) {
            Write-Log "⚠️ 页面 ${stuckCount} 次检查无变化（约 $($stuckCount * $MonitorInterval)s）" "WARN"
        }
        $lastContentHash = $contentHash
    }
}

if ($elapsed -ge $WaitTimeout) {
    Write-Log "❌ 超时 ${WaitTimeout}s，PPT 生成未完成" "ERROR"
    Write-Log "最后检测到的阶段: ${phaseDesc}" "INFO"
    Write-Host "`n⚠️ 超时了！请检查 Edge 浏览器中的豆包页面状态" -ForegroundColor Yellow
    exit 1
}

# ============================================================
# Step 4: 下载 PPT
# ============================================================
Write-Log "[4/5] 下载 PPT..." "PHASE"

$downloaded = $false
$downloadedFile = ""

# 记录下载前文件列表
$beforeFiles = @()
if (Test-Path $DownloadsDir) {
    $beforeFiles = @(Get-ChildItem $DownloadsDir -Filter "*.pptx" | Select-Object -ExpandProperty Name)
}

# --- 4a: 点击 PPT 卡片打开编辑器 ---
Write-Log "  -> 点击 PPT 卡片打开编辑器..." "INFO"

# 刷新 state
$state = opencli browser state 2>$null
$cardRef = $null

# 方法1: 找 PPT 卡片标题文字（通常包含 PPT 主题的关键字）
$titleLine = $state | Select-String -Pattern "创建时间" | Select-Object -First 1
if ($titleLine) {
    $cardRef = ($titleLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
}

# 方法2: 找 PPT 封面图片
if (-not $cardRef) {
    $imgLine = $state | Select-String -Pattern "alt=Asset cover" | Select-Object -First 1
    if ($imgLine) {
        $cardRef = ($imgLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
    }
}

# 方法3: 找 "已完成PPT生成" 附近的卡片区域
if (-not $cardRef) {
    $doneLine = $state | Select-String -Pattern "已完成PPT|已完成.*PPT" | Select-Object -First 1
    if ($doneLine) {
        $cardRef = ($doneLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
    }
}

if ($cardRef) {
    Write-Log "  -> 点击 PPT 卡片 ref [$cardRef]" "INFO"
    opencli browser click $cardRef 2>$null
    Start-Sleep 5
} else {
    Write-Log "  ⚠️ 找不到 PPT 卡片，尝试 JS 查找并点击..." "WARN"
    opencli browser eval "var imgs = document.querySelectorAll('img[alt*=cover]'); if(imgs.length > 0) { imgs[0].closest('[class*=card]')?.click() || imgs[0].parentElement?.click(); 'clicked' } else { 'no cover img' }" 2>$null
    Start-Sleep 5


# --- 4b: 找下载按钮并点击 ---
Write-Log "  -> 找下载按钮..." "INFO"

# 刷新 state
$state = opencli browser state 2>$null

# 方法1: 找包含"下载"文字的按钮（data-dbx-name="button"）
$downloadRef = $null
$downloadLine = $state | Select-String -Pattern "下载" | Select-Object -First 1
if ($downloadLine) {
    $downloadRef = ($downloadLine | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
}

# 方法2: 找 radix 菜单触发器（下载按钮有 aria-haspopup=menu）
if (-not $downloadRef) {
    # 找工具栏中第三个 button（放映、分享、下载）
    $toolbarBtns = $state | Select-String -Pattern "data-dbx-name=button" | Select-Object -First 5
    if ($toolbarBtns) {
        $btnLines = @($toolbarBtns)
        if ($btnLines.Count -ge 3) {
            $downloadRef = ($btnLines[2] | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
        }
    }
}

if ($downloadRef) {
    Write-Log "  -> 点击下载按钮 ref [$downloadRef]" "INFO"
    opencli browser click $downloadRef 2>$null
    Start-Sleep 2

    # --- 4c: 选择 PPTX 格式 ---
    Write-Log "  -> 选择 PPTX 格式..." "INFO"
    $state = opencli browser state 2>$null

    # 找菜单项（role=menuitem）
    $pptxRef = $null
    $menuItems = $state | Select-String -Pattern "role=menuitem" | Select-Object -First 5
    if ($menuItems) {
        $itemLines = @($menuItems)
        if ($itemLines.Count -ge 1) {
            # 第一个 menuitem 是 PPTX
            $pptxRef = ($itemLines[0] | Select-String -Pattern "\[(\d+)\]" | ForEach-Object { $_.Matches.Groups[1].Value } | Select-Object -First 1)
        }
    }

    if ($pptxRef) {
        Write-Log "  -> 点击 PPTX 选项 ref [$pptxRef]" "INFO"
        opencli browser click $pptxRef 2>$null
        Start-Sleep 3

        # 等待下载完成（文件自动保存到 Downloads）
        Write-Log "  -> 等待下载完成..." "INFO"
        Start-Sleep 5

        # 检查下载
        if (Test-Path $DownloadsDir) {
            $afterFiles = @(Get-ChildItem $DownloadsDir -Filter "*.pptx" | Select-Object -ExpandProperty Name)
            $newFiles = $afterFiles | Where-Object { $_ -notin $beforeFiles }
            if ($newFiles) {
                $downloadedFile = Join-Path $DownloadsDir $newFiles[0]
                $downloaded = $true
                Write-Log "  ✅ 下载成功: $downloadedFile" "OK"
            } else {
                Write-Log "  ⚠️ 未检测到新 PPTX 文件，等待 10 秒再检查..." "WARN"
                Start-Sleep 10
                $afterFiles = @(Get-ChildItem $DownloadsDir -Filter "*.pptx" | Select-Object -ExpandProperty Name)
                $newFiles = $afterFiles | Where-Object { $_ -notin $beforeFiles }
                if ($newFiles) {
                    $downloadedFile = Join-Path $DownloadsDir $newFiles[0]
                    $downloaded = $true
                    Write-Log "  ✅ 下载成功: $downloadedFile" "OK"
                }
            }
        }
    } else {
        Write-Log "  ⚠️ 找不到 PPTX 菜单项" "WARN"
    }
} else {
    Write-Log "  ⚠️ 找不到下载按钮" "WARN"
}

# --- 下载失败处理 ---
if (-not $downloaded) {
    Write-Log "❌ 下载未成功" "ERROR"
    Write-Host ""
    Write-Host "⚠️ 下载未成功，可能原因：" -ForegroundColor Yellow
    Write-Host "  1. PPT 编辑器未正确打开" -ForegroundColor Yellow
    Write-Host "  2. 下载按钮位置变化" -ForegroundColor Yellow
    Write-Host "  3. 浏览器下载弹窗被拦截" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请手动在 Edge 浏览器中检查豆包页面，" -ForegroundColor Yellow
    Write-Host "找到下载按钮后点击下载 PPTX。" -ForegroundColor Yellow
    Write-Host "日志已保存到: $LogFile" -ForegroundColor Gray
    exit 1
}

# ============================================================
# Step 5: 搬运到输出目录
# ============================================================
Write-Log "[5/5] 搬运到输出目录..." "PHASE"

if ($downloadedFile -and (Test-Path $downloadedFile)) {
    $outputFileName = "ppt_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + ".pptx"
    $outputFile = Join-Path $OutputDir $outputFileName
    Copy-Item $downloadedFile $outputFile -Force
    Write-Log "  ✅ 已搬运到: $outputFile" "OK"

    $fileInfo = Get-Item $outputFile
    $sizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
    Write-Log "  📊 文件大小: ${sizeMB}MB" "OK"
} else {
    Write-Log "  ⚠️ 下载文件不存在" "WARN"
    $latestPptx = Get-ChildItem $DownloadsDir -Filter "*.pptx" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestPptx) {
        $outputFileName = "ppt_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + ".pptx"
        $outputFile = Join-Path $OutputDir $outputFileName
        Copy-Item $latestPptx.FullName $outputFile -Force
        Write-Log "  ✅ 已搬运（从最近文件）: $outputFile" "OK"
    }
}

# --- 最终日志 ---
Write-Log "" "INFO"
Write-Log "=== 完成 ===" "PHASE"
Write-Log "总耗时: ${elapsed}s" "INFO"
Write-Log "阶段记录: $($phaseLog -join ' → ')" "INFO"
Write-Log "输出文件: $outputFile" "OK"
Write-Log "日志文件: $LogFile" "INFO"

Write-Host ""
Write-Host "=== 完成 ===" -ForegroundColor Cyan
Write-Host "总耗时: ${elapsed}s" -ForegroundColor Cyan
Write-Host "输出: $outputFile" -ForegroundColor Green
Write-Host "日志: $LogFile" -ForegroundColor Gray