<#
.SYNOPSIS
    灵刻 AI 图像生成脚本 - 影视概念图生成
.DESCRIPTION
    调用灵刻 AI API 生成图片，支持异步任务提交和自动轮询
.PARAMETER Prompt
    图像描述提示词（必填）
.PARAMETER Model
    模型名称：gpt-image-2 / gemini-3-pro-image-preview / gemini-3.1-flash-image-preview
    默认：gpt-image-2
.PARAMETER Size
    gpt-image-2 的尺寸参数，如 1024x1024, 1024x1536, 1920x1088 等
.PARAMETER AspectRatio
    Gemini 模型的宽高比，如 1:1, 16:9, 9:16, 2:3 等
.PARAMETER ImageSize
    Gemini 模型的分辨率，如 1K, 2K, 4K
.PARAMETER Quality
    gpt-image-2 的质量参数：auto / high / medium / low
.PARAMETER ImageUrl
    参考图 URL（可多次使用）
.PARAMETER TimeoutSeconds
    轮询超时时间（秒），默认 600（10 分钟）
.PARAMETER PollIntervalSeconds
    轮询间隔（秒），默认 5
.EXAMPLE
    .\generate-image.ps1 -Prompt "雨夜的上海弄堂，赛博朋克风格"
    .\generate-image.ps1 -Prompt "电影海报" -Model gemini-3-pro-image-preview -AspectRatio 2:3 -ImageSize 4K
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Prompt,

    [string]$Model = "gpt-image-2",

    [string]$Size = "auto",

    [string]$AspectRatio = "1:1",

    [string]$ImageSize = "2K",

    [string]$Quality = "auto",

    [string[]]$ImageUrl = @(),

    [int]$TimeoutSeconds = 600,

    [int]$PollIntervalSeconds = 5
)

$ErrorActionPreference = "Stop"

$API_KEY_PRIMARY = "sk-79033dcf2ff97cf5a7b711a8255eaa113c948adcd7569616"
$API_KEY_FALLBACK = "sk-4d6f676515c6e3b0c3eca05d4c01b4700e028a68bdf55fe9"
$API_KEY = $API_KEY_PRIMARY
$BASE_URL = "https://api.lk888.ai"

$headers = @{
    "Authorization" = "Bearer $API_KEY"
    "Content-Type"  = "application/json"
}

# 构建请求参数
$params = @{
    "prompt" = $Prompt
}

if ($ImageUrl.Count -gt 0) {
    if ($ImageUrl.Count -eq 1) {
        $params["images"] = $ImageUrl[0]
    } else {
        $params["images"] = $ImageUrl
    }
}

# 根据模型类型构建不同的参数
if ($Model -eq "gpt-image-2") {
    $params["size"] = $Size
    $params["quality"] = $Quality
} else {
    $params["aspectRatio"] = $AspectRatio
    $params["imageSize"] = $ImageSize
}

if ($Model -eq "gemini-3.1-flash-image-preview") {
    $params["web_search"] = $false
}

$body = @{
    "model"  = $Model
    "params" = $params
} | ConvertTo-Json -Depth 5

Write-Host "[1/2] 提交任务到 $Model ..." -ForegroundColor Cyan
Write-Host "  Prompt: $Prompt" -ForegroundColor Gray

try {
    $submitResponse = Invoke-RestMethod -Uri "$BASE_URL/v1/media/generate" -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8"
} catch {
    Write-Host "⚠️ 主 Key 提交失败，尝试备用 Key..." -ForegroundColor Yellow
    # 切换到备用 Key
    $API_KEY = $API_KEY_FALLBACK
    $headers["Authorization"] = "Bearer $API_KEY"
    try {
        $submitResponse = Invoke-RestMethod -Uri "$BASE_URL/v1/media/generate" -Method POST -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8"
        Write-Host "✅ 备用 Key 提交成功" -ForegroundColor Green
    } catch {
        Write-Host "❌ 提交任务失败: $_" -ForegroundColor Red
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $errorBody = $reader.ReadToEnd()
            Write-Host "  响应: $errorBody" -ForegroundColor Red
        }
        exit 1
    }
}

if ($submitResponse.code -ne 200) {
    Write-Host "❌ API 返回错误: $($submitResponse.msg)" -ForegroundColor Red
    exit 1
}

$taskId = $submitResponse.data.task_id
$count = $submitResponse.data."成功数量"
Write-Host "✅ 任务创建成功! task_id: $taskId, 生成数量: $count" -ForegroundColor Green

# 轮询结果
Write-Host "[2/2] 等待生成完成（每 ${PollIntervalSeconds}s 轮询，超时 ${TimeoutSeconds}s）..." -ForegroundColor Cyan

$startTime = Get-Date
$pollCount = 0

while ($true) {
    Start-Sleep -Seconds $PollIntervalSeconds
    $pollCount++

    $elapsed = (Get-Date) - $startTime
    if ($elapsed.TotalSeconds -gt $TimeoutSeconds) {
        Write-Host "⏱️ 超时（${TimeoutSeconds}s），任务可能仍在处理中" -ForegroundColor Yellow
        Write-Host "  可稍后手动查询: task_id = $taskId" -ForegroundColor Yellow
        exit 2
    }

    try {
        $statusResponse = Invoke-RestMethod -Uri "$BASE_URL/v1/media/status?task_id=$taskId" -Method GET -Headers $headers
    } catch {
        Write-Host "⚠️ 轮询失败（第 $pollCount 次）: $_" -ForegroundColor Yellow
        continue
    }

    $status = $statusResponse.status
    $progress = $statusResponse.progress
    $isFinal = $statusResponse.is_final

    if ($isFinal -eq $true) {
        if ($statusResponse.state -eq "success" -and [string]::IsNullOrEmpty($statusResponse.error)) {
            $resultUrl = $statusResponse.result_url
            $cost = $statusResponse.cost
            Write-Host "✅ 生成完成!" -ForegroundColor Green
            Write-Host "  图片 URL: $resultUrl" -ForegroundColor Green
            Write-Host "  花费: $cost" -ForegroundColor Gray
            Write-Host "  耗时: $([math]::Round($elapsed.TotalSeconds, 1))s" -ForegroundColor Gray
            Write-Host "  轮询次数: $pollCount" -ForegroundColor Gray
            # 输出纯 URL 供调用方捕获
            Write-Output $resultUrl
            exit 0
        } else {
            Write-Host "❌ 任务失败: $($statusResponse.error)" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "  ⏳ [$pollCount] $status ($progress%)... ($([math]::Round($elapsed.TotalSeconds, 1))s)" -ForegroundColor DarkGray
    }
}
