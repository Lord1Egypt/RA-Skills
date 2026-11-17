# download_tools.ps1
# 从美的 GitLab 下载 CODESYS 工具套件
# 需要已登录 GitLab（浏览器有 cookie）

$baseUrl = "https://git.midea.com/DEP-IMRC/IIET/auto/auto-rd-group/2026/mra0626c15-plc/skills/codesys-auto-programmer/-/raw/master/scripts/tools"
$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$files = @(
    "dialog_monitor.ps1",
    "run_script.ps1",
    "export_pou.py",
    "generator_runner.py",
    "list_devices.py",
    "patch_pou.py"
)

Write-Host "=== CODESYS Toolkit 下载工具 ===" -ForegroundColor Cyan
Write-Host "目标目录: $toolsDir"
Write-Host ""

foreach ($file in $files) {
    $outPath = Join-Path $toolsDir $file
    if (Test-Path $outPath) {
        Write-Host "[SKIP] $file (已存在)" -ForegroundColor Yellow
        continue
    }
    
    $url = "$baseUrl/$file"
    Write-Host "[DOWNLOAD] $file ..." -ForegroundColor White
    
    try {
        # 尝试用浏览器 cookie（需要已登录 GitLab）
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 30 -ErrorAction Stop
        [System.IO.File]::WriteAllText($outPath, $response.Content, [System.Text.UTF8Encoding]::new($false))
        Write-Host "  OK ($($response.Content.Length) bytes)" -ForegroundColor Green
    } catch {
        Write-Host "  FAILED: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  请手动从浏览器下载: $url" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=== 下载完成 ===" -ForegroundColor Cyan
Write-Host "已下载文件:"
Get-ChildItem $toolsDir -Filter "*.py" | ForEach-Object { Write-Host "  $($_.Name)" }
Get-ChildItem $toolsDir -Filter "*.ps1" | ForEach-Object { Write-Host "  $($_.Name)" }
