# 抖音爆款标题生成器 PowerShell 脚本
param(
    [string]$Topic = "",
    [string]$Style = "搞笑",
    [int]$Count = 3,
    [string]$Audience = "",
    [string]$Trending = "",
    [switch]$Export = $false,
    [string]$ExportPath = ""
)

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 错误：未找到Python，请先安装Python" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ 错误：未找到Python，请先安装Python" -ForegroundColor Red
    exit 1
}

# 检查参数
if ([string]::IsNullOrWhiteSpace($Topic)) {
    Write-Host "❌ 错误：必须指定主题参数 --topic" -ForegroundColor Red
    Write-Host "使用方法："
    Write-Host "  .\generate.ps1 --topic '美食制作' --style '搞笑' --count 3"
    Write-Host "  .\generate.ps1 --topic '健身减脂' --audience '年轻人' --trending '减肥'"
    exit 1
}

# 构建Python命令
$pythonCmd = "python main.py --topic `"$Topic`" --style `"$Style`" --count $Count"

if (-not [string]::IsNullOrWhiteSpace($Audience)) {
    $pythonCmd += " --audience `"$Audience`""
}

if (-not [string]::IsNullOrWhiteSpace($Trending)) {
    $pythonCmd += " --trending `"$Trending`""
}

# 执行生成
Write-Host "🎯 正在生成抖音爆款标题..." -ForegroundColor Cyan
Write-Host "主题：$Topic" -ForegroundColor Yellow
Write-Host "风格：$Style" -ForegroundColor Yellow
Write-Host "数量：$Count" -ForegroundColor Yellow
if (-not [string]::IsNullOrWhiteSpace($Audience)) {
    Write-Host "受众：$Audience" -ForegroundColor Yellow
}
if (-not [string]::IsNullOrWhiteSpace($Trending)) {
    Write-Host "热点：$Trending" -ForegroundColor Yellow
}
Write-Host ""

# 执行Python脚本
Invoke-Expression $pythonCmd

# 导出结果
if ($Export) {
    if ([string]::IsNullOrWhiteSpace($ExportPath)) {
        $ExportPath = "douyin_titles_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
    }
    
    # 获取输出并保存到文件
    $output = Invoke-Expression $pythonCmd
    $output | Out-File -FilePath $ExportPath -Encoding UTF8
    Write-Host "✅ 结果已导出到：$ExportPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 抖音爆款标题生成完成！" -ForegroundColor Green