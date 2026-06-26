param(
    [string]$Prompt,
    [switch]$Download
)

$scriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
$parentDir = Split-Path $scriptDir -Parent
$OUTPUT_DIR = $parentDir + "\output\doubao_images"
if (-not (Test-Path $OUTPUT_DIR)) { New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null }

$CREATE_IMAGE_URL = "https://www.doubao.com/chat/create-image"

function Write-Step {
    param($Msg, $Color = "Green")
    Write-Host ("  >> " + $Msg) -ForegroundColor $Color
}

if (-not $Prompt) {
    Write-Host "用法: .\doubao_image_gen.ps1 `"提示词`" [-download]"
    exit
}

Write-Step "打开 AI 创作页面..."
opencli browser open $CREATE_IMAGE_URL 2>&1 | Out-Null
Start-Sleep 3

# 找 textbox - 搜索 contenteditable=true 的行
Write-Step "找到输入框..."
$state = opencli browser state 2>&1
$textboxRef = ""
$lines = $state -split "`n"
foreach ($line in $lines) {
    if ($line -match '\[(\d+)\].*role=textbox.*contenteditable=true') {
        $textboxRef = $matches[1]
        break
    }
}
if (-not $textboxRef) {
    Write-Host "  [FAIL] 找不到输入框" -ForegroundColor Red
    exit 1
}
Write-Host ("  输入框 ref: " + $textboxRef) -ForegroundColor DarkGray

Write-Step "填入提示词..."
$fullPrompt = $Prompt
opencli browser fill $textboxRef $fullPrompt 2>&1 | Out-Null
Start-Sleep 1

Write-Step "点击生成..."
opencli browser click "#flow-end-msg-send" 2>&1 | Out-Null

Write-Step "等待生成中..."
$maxWait = 60
$waited = 0
$found = $false

while ($waited -lt $maxWait) {
    Start-Sleep 5
    $waited = $waited + 5
    $extract = opencli browser extract 2>&1
    if ($extract -match '!\[image\]\(https://[^)]+\.jpeg') {
        $found = $true
        Write-Host ("  [OK] 用时 " + $waited + "s") -ForegroundColor Green
        break
    }
    Write-Host ("  ... " + $waited + "s") -ForegroundColor DarkYellow
}

if (-not $found) {
    Write-Host "  [FAIL] 超时" -ForegroundColor Red
    exit 1
}

Write-Step "提取图片链接..."
$urls = @()
$matches = [regex]::Matches($extract, 'https://p\d+-flow-imagex-sign\.byteimg\.com[^"''\s\)]+\.jpeg[^"''\s\)]*')
foreach ($m in $matches) {
    if ($m.Value -notin $urls) { $urls = $urls + $m.Value }
}

Write-Host ("  [OK] 共 " + $urls.Count + " 张图片") -ForegroundColor Cyan

$idx = 0
foreach ($url in $urls) {
    $idx = $idx + 1
    Write-Host ("  [" + $idx + "] " + $url) -ForegroundColor Cyan
    if ($Download) {
        $file = $OUTPUT_DIR + "\doubao_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + "_" + $idx + ".jpg"
        try {
            Invoke-WebRequest -Uri $url -OutFile $file
            Write-Host ("      已保存: " + $file) -ForegroundColor Green
        } catch {
            Write-Host ("      下载失败: " + $_.Exception.Message) -ForegroundColor Yellow
        }
    }
}

# 保存链接记录
$logFile = $OUTPUT_DIR + "\gen_log_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + ".md"
"# 豆包图片生成记录" | Out-File $logFile -Encoding UTF8
"" | Out-File $logFile -Encoding UTF8 -Append
"提示词: " + $Prompt | Out-File $logFile -Encoding UTF8 -Append
"时间: " + (Get-Date) | Out-File $logFile -Encoding UTF8 -Append
"" | Out-File $logFile -Encoding UTF8 -Append
$idx = 0
foreach ($url in $urls) {
    $idx = $idx + 1
    "- 图片 " + $idx + ": " + $url | Out-File $logFile -Encoding UTF8 -Append
}
Write-Host ("  记录: " + $logFile) -ForegroundColor DarkGray
