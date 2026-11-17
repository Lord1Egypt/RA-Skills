$ErrorActionPreference = "Stop"
$SKILL_DIR = "C:\Users\xjj31\.openclaw\workspace\skills\1688-alibaba-data-fetcher"
$SCRIPTS_DIR = "$SKILL_DIR\scripts"

Write-Host "=== 1688 Data Claw - Windows 初始化 ===" -ForegroundColor Cyan

# 1. 创建隔离目录
Write-Host ">>> 创建目录结构..."
$USER_DATA = "C:\isolated-profiles\1688-agent"
if (-not (Test-Path $USER_DATA)) {
    New-Item -ItemType Directory -Path $USER_DATA -Force | Out-Null
    Write-Host "  创建: $USER_DATA"
}

# 2. 下载 Chromium 便携版（从 npmmirror，国内最快）
$CHROME = "$SKILL_DIR\chromium\chrome-win64\chrome.exe"
if (-not (Test-Path $CHROME)) {
    Write-Host ">>> 获取最新 Chromium 版本..."
    $ProgressPreference = 'SilentlyContinue'
    
    $versionJson = Invoke-WebRequest -Uri "https://registry.npmmirror.com/-/binary/chrome-for-testing/last-known-good-versions.json" -UseBasicParsing -TimeoutSec 15
    $version = ($versionJson.Content | ConvertFrom-Json).channels.Stable.version
    Write-Host "  最新稳定版: $version"
    
    $CHROMIUM_ZIP = "$SKILL_DIR\chromium\chrome-win64.zip"
    $downloadUrl = "https://registry.npmmirror.com/-/binary/chrome-for-testing/$version/win64/chrome-win64.zip"
    Write-Host ">>> 下载 Chromium（~150MB，约需 30s）..."
    
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $CHROMIUM_ZIP -UseBasicParsing -TimeoutSec 300
    } catch {
        Write-Host "  npmmirror 下载失败，尝试 Google 官方源..."
        $downloadUrl = "https://storage.googleapis.com/chrome-for-testing-public/$version/win64/chrome-win64.zip"
        Invoke-WebRequest -Uri $downloadUrl -OutFile $CHROMIUM_ZIP -UseBasicParsing -TimeoutSec 300
    }
    
    Write-Host ">>> 解压 Chromium..."
    Expand-Archive -Path $CHROMIUM_ZIP -DestinationPath "$SKILL_DIR\chromium" -Force
    Remove-Item $CHROMIUM_ZIP -Force
    Write-Host "✅ Chromium 就位: $CHROME"
} else {
    Write-Host "✅ Chromium 已就位: $CHROME"
}

# 3. 验证插件
if (Test-Path "$SKILL_DIR\plugin\manifest.json") {
    Write-Host "插件已就位: $SKILL_DIR\plugin"
} else {
    Write-Host "插件缺失: $SKILL_DIR\plugin\manifest.json"
    exit 1
}

# 4. 写入标记文件
$MARKER = "$USER_DATA\.openclaw_browser_marker"
$PID = [System.Diagnostics.Process]::GetCurrentProcess().Id
"PID=$PID`nPort=9222`nTimestamp=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File -FilePath $MARKER -Encoding ASCII
Write-Host "标记文件已写入: $MARKER"

Write-Host ""
Write-Host "=== 初始化完成 ===" -ForegroundColor Green
Write-Host "扩展 ID: ekmgnempbbamlmaolijdfjakeopniion"