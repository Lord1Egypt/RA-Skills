<#
.SYNOPSIS
    1688 Data Claw - Windows 一键初始化
    安装 skill 时立即执行一次
#>

$ErrorActionPreference = "Stop"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$SCRIPT_DIR\env.ps1"

Write-Host "=== 1688 Data Claw - Windows 初始化 ===" -ForegroundColor Cyan

# 1. 创建隔离目录结构
Write-Host ">>> 创建目录结构..."
@(
    $USER_DATA,
    $OUTPUT_DIR
) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
        Write-Host "  创建: $_"
    }
}

# 2. 下载 Chromium 便携版（从 npmmirror，国内最快）
if (-not (Test-Path $CHROME)) {
    Write-Host ">>> 获取最新 Chromium 版本..."
    $ProgressPreference = 'SilentlyContinue'
    
    # 从 npmmirror 获取最新稳定版号
    $versionJson = Invoke-WebRequest -Uri "https://registry.npmmirror.com/-/binary/chrome-for-testing/last-known-good-versions.json" -UseBasicParsing -TimeoutSec 15
    $version = ($versionJson.Content | ConvertFrom-Json).channels.Stable.version
    Write-Host "  最新稳定版: $version"
    
    # 确保目录存在
    $CHROMIUM_DIR = "$SKILL_DIR\chromium"
    New-Item -ItemType Directory -Path $CHROMIUM_DIR -Force | Out-Null
    
    # 下载 zip（npmmirror CDN，国内 ~4.5MB/s）
    $CHROMIUM_ZIP = "$CHROMIUM_DIR\chrome-win64.zip"
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
    $CHROMIUM_DIR = "$SKILL_DIR\chromium"
    Expand-Archive -Path $CHROMIUM_ZIP -DestinationPath $CHROMIUM_DIR -Force
    Remove-Item $CHROMIUM_ZIP -Force
    Write-Host "✅ Chromium 就位: $CHROME"
} else {
    Write-Host "✅ Chromium 已就位: $CHROME"
}

# 3. 设置嵌入式 Python 3.12（不依赖系统环境变量）
$PYTHON_DIR = "$SKILL_DIR\python3"
$PYTHON_EXE = "$PYTHON_DIR\python.exe"
$PYTHON_ZIP = "$PYTHON_DIR\python-embed.zip"

if (-not (Test-Path $PYTHON_EXE)) {
    Write-Host ">>> 下载嵌入式 Python 3.12..."
    New-Item -ItemType Directory -Path $PYTHON_DIR -Force | Out-Null
    
    $ProgressPreference = 'SilentlyContinue'
    $pyUrl = "https://mirrors.huaweicloud.com/python/3.12.9/python-3.12.9-embed-amd64.zip"
    try {
        Invoke-WebRequest -Uri $pyUrl -OutFile $PYTHON_ZIP -UseBasicParsing -TimeoutSec 120
    } catch {
        Write-Host "华为镜像下载失败，尝试 python.org..."
        Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.9/python-3.12.9-embed-amd64.zip" -OutFile $PYTHON_ZIP -UseBasicParsing -TimeoutSec 120
    }
    
    Write-Host ">>> 解压 Python..."
    Expand-Archive -Path $PYTHON_ZIP -DestinationPath $PYTHON_DIR -Force
    Remove-Item $PYTHON_ZIP -Force
    
    # 启用 site-packages（修改 _pth 文件）
    $pthFile = Get-ChildItem "$PYTHON_DIR\*._pth" | Select-Object -First 1
    if ($pthFile) {
        $pthContent = Get-Content $pthFile.FullName -Raw
        $pthContent = $pthContent -replace '#import site', 'import site'
        Set-Content -Path $pthFile.FullName -Value $pthContent -Encoding ASCII -NoNewline
        # 确保末尾有换行
        Add-Content -Path $pthFile.FullName -Value ""
    }
    
    # 创建 Lib\site-packages 目录
    New-Item -ItemType Directory -Path "$PYTHON_DIR\Lib\site-packages" -Force | Out-Null
    
    # 安装 pip
    Write-Host ">>> 安装 pip..."
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "$PYTHON_DIR\get-pip.py" -UseBasicParsing -TimeoutSec 60
    & $PYTHON_EXE "$PYTHON_DIR\get-pip.py" --no-warn-script-location
    Remove-Item "$PYTHON_DIR\get-pip.py" -Force
    
    Write-Host "✅ Python 就位: $PYTHON_EXE"
} else {
    Write-Host "✅ Python 已就位: $PYTHON_EXE"
}

# 4. 验证并创建 python3.cmd 启动器
$PYTHON_CMD = "$SKILL_DIR\python3.cmd"
if (-not (Test-Path $PYTHON_CMD)) {
    @"
@echo off
REM 1688 Data Claw - Embedded Python 3.12 Launcher
REM Auto-detects skill dir and uses bundled python3\python.exe

set "SKILL_DIR=%~dp0"
set "PYTHON_EXE=%SKILL_DIR%python3\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Embedded Python not found: %PYTHON_EXE%
    echo Please run scripts\setup.ps1 first
    exit /b 1
)

"%PYTHON_EXE%" %*
"@ | Out-File -FilePath $PYTHON_CMD -Encoding ASCII
    Write-Host "✅ python3.cmd 启动器已创建"
}

# 5. 验证插件已存在
if (Test-Path "$EXT_DIR\manifest.json") {
    Write-Host "✅ 插件已就位: $EXT_DIR"
} else {
    Write-Host "❌ 插件缺失: $EXT_DIR\manifest.json"
    exit 1
}

Write-Host ""
Write-Host "=== ✨ 初始化完成 ===" -ForegroundColor Green
Write-Host "运行 .\scripts\start-browser.ps1 启动浏览器"
Write-Host "扩展 ID: ekmgnempbbamlmaolijdfjakeopniion"