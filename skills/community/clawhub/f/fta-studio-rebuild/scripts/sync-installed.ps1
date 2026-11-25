# 把项目源码同步到已安装的 FTA Studio 副本
#
# 背景：用户实际运行的是 %LOCALAPPDATA%\FTA Studio 里的安装副本（自带 runtime），
# 而不是开发目录里的源码。改了源码若不同步，用户看到的永远是旧版本。
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File sync-installed.ps1 -SourceDir <项目根目录>
#   powershell -ExecutionPolicy Bypass -File sync-installed.ps1 -SourceDir <项目根目录> -Restart

param(
  [Parameter(Mandatory = $true)][string]$SourceDir,
  [string]$InstallDir = "$env:LOCALAPPDATA\FTA Studio",
  [switch]$Restart
)

$ErrorActionPreference = 'Stop'

$app = Join-Path $InstallDir 'app'
if (-not (Test-Path $app)) {
  Write-Host "未找到安装目录: $app" -ForegroundColor Red
  Write-Host "请先运行「安装到本机.bat」。" -ForegroundColor Yellow
  exit 1
}
if (-not (Test-Path (Join-Path $SourceDir 'src\launch.mjs'))) {
  Write-Host "源目录不像 FTA Studio 项目: $SourceDir" -ForegroundColor Red
  exit 1
}

Write-Host "源目录 : $SourceDir"
Write-Host "安装目录: $app"

foreach ($sub in @('src', 'public', 'examples')) {
  $from = Join-Path $SourceDir $sub
  if (Test-Path $from) {
    Copy-Item "$from\*" (Join-Path $app $sub) -Recurse -Force
    Write-Host ("  同步 {0}/" -f $sub)
  }
}
Copy-Item (Join-Path $SourceDir 'package.json') $app -Force
Write-Host '  同步 package.json'

$js = Join-Path $app 'public\app.js'
$html = Get-Content (Join-Path $app 'public\index.html') -Raw
$v = ([regex]::Match($html, 'app\.js\?v=(\d+)')).Groups[1].Value
Write-Host ("完成。app.js {0:N0} 字节，页面资源版本 v={1}" -f (Get-Item $js).Length, $v) -ForegroundColor Green

if ($Restart) {
  $procs = Get-CimInstance Win32_Process |
    Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -match 'launch\.mjs' }
  foreach ($p in $procs) {
    Write-Host ("  停止旧服务 PID {0}" -f $p.ProcessId)
    Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
  }
  Start-Sleep -Seconds 2
  $nodeExe = Join-Path $InstallDir 'runtime\node.exe'
  if (-not (Test-Path $nodeExe)) { $nodeExe = 'node' }
  Start-Process -FilePath $nodeExe -ArgumentList 'src\launch.mjs', '--no-open' -WorkingDirectory $app -WindowStyle Hidden
  Start-Sleep -Seconds 3
  $listening = (netstat -ano 2>$null | Select-String ':8777.*LISTENING' | Measure-Object).Count
  Write-Host ("  服务已重启，8777 监听={0}" -f $listening) -ForegroundColor Green
  Write-Host '  浏览器需刷新（Ctrl+F5）才能加载新前端。' -ForegroundColor Yellow
}
else {
  Write-Host '提示：加 -Restart 可顺便重启服务；否则请手动重启并 Ctrl+F5 刷新浏览器。' -ForegroundColor Yellow
}
