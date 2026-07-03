# start-edge-cdp.ps1
# 启动 Edge 浏览器 CDP 调试模式
# 用途：让 Playwright 可以接管已登录的 Edge 浏览器

param(
    [int]$Port = 9222,
    [switch]$KeepExisting = $false
)

Write-Host "=== 豆包自动化 — Edge CDP 启动器 ===" -ForegroundColor Cyan

# 检查是否已经有 CDP 模式的 Edge 在运行
$existingEdge = Get-Process msedge -ErrorAction SilentlyContinue | Where-Object {
    $_.MainWindowTitle -match "调试" -or $_.MainWindowTitle -ne ""
}

if ($existingEdge -and $KeepExisting) {
    Write-Host "[提示] Edge 已在运行中，尝试复用现有实例..." -ForegroundColor Yellow
    
    # 验证 CDP 端口是否可用
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port/json/version" -UseBasicParsing -TimeoutSec 3
        $data = $response.Content | ConvertFrom-Json
        Write-Host "[成功] CDP 服务已在运行: $($data.Browser)" -ForegroundColor Green
        Write-Host "  WebSocket: $($data.webSocketDebuggerUrl)" -ForegroundColor Gray
        return @{
            Success = $true
            Message = "CDP 服务已在运行"
            WebSocketUrl = $data.webSocketDebuggerUrl
        }
    } catch {
        Write-Host "[警告] Edge 在运行但 CDP 端口不可用，将关闭并重启..." -ForegroundColor Yellow
    }
}

# 关闭所有 Edge 进程
Write-Host "[步骤 1/3] 关闭现有 Edge 进程..." -ForegroundColor Yellow
try {
    Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-Host "  已关闭所有 Edge 进程" -ForegroundColor Green
} catch {
    Write-Host "  没有需要关闭的 Edge 进程" -ForegroundColor Gray
}

# 查找 Edge 可执行文件
Write-Host "[步骤 2/3] 查找 Edge 安装路径..." -ForegroundColor Yellow
$edgePaths = @(
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

$edgePath = $null
foreach ($path in $edgePaths) {
    if (Test-Path $path) {
        $edgePath = $path
        Write-Host "  找到: $edgePath" -ForegroundColor Green
        break
    }
}

if (-not $edgePath) {
    Write-Host "[错误] 未找到 Edge 浏览器！" -ForegroundColor Red
    return @{
        Success = $false
        Message = "未找到 Edge 浏览器"
    }
}

# 以 CDP 模式启动 Edge
Write-Host "[步骤 3/3] 以 CDP 调试模式启动 Edge..." -ForegroundColor Yellow
$args = @(
    "--remote-debugging-port=$Port",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-features=TranslateUI",
    "--user-data-dir=$env:LOCALAPPDATA\Microsoft\Edge\User Data",
    "--profile-directory=Default"
)

try {
    $process = Start-Process -FilePath $edgePath -ArgumentList $args -PassThru
    Write-Host "  Edge 已启动 (PID: $($process.Id))" -ForegroundColor Green
} catch {
    Write-Host "[错误] 启动 Edge 失败: $_" -ForegroundColor Red
    return @{
        Success = $false
        Message = "启动 Edge 失败: $_"
    }
}

# 等待 CDP 服务就绪
Write-Host "  等待 CDP 服务就绪..." -ForegroundColor Gray
$maxWait = 15
for ($i = 0; $i -lt $maxWait; $i++) {
    Start-Sleep -Seconds 1
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port/json/version" -UseBasicParsing -TimeoutSec 2
        $data = $response.Content | ConvertFrom-Json
        Write-Host "[成功] CDP 服务已就绪！" -ForegroundColor Green
        Write-Host "  浏览器: $($data.Browser)" -ForegroundColor Gray
        Write-Host "  WebSocket URL: $($data.webSocketDebuggerUrl)" -ForegroundColor Gray
        return @{
            Success = $true
            Message = "Edge CDP 服务已启动"
            WebSocketUrl = $data.webSocketDebuggerUrl
            BrowserUrl = $data.webSocketDebuggerUrl
        }
    } catch {
        Write-Host "  ." -NoNewline
    }
}

Write-Host ""
Write-Host "[警告] CDP 服务启动超时，但 Edge 进程已在运行" -ForegroundColor Yellow
Write-Host "  请手动打开 http://localhost:$Port/json/version 验证" -ForegroundColor Yellow
return @{
    Success = $true
    Message = "Edge 已启动，CDP 服务可能尚未就绪，请稍后重试"
}
