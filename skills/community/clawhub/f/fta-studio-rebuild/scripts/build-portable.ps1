<#
.SYNOPSIS
  把 FTA Studio 打包成免安装的 Windows 便携包（内置 Node 运行时）。

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File build-portable.ps1 `
      -SourceDir "D:\code\fta-studio" -OutDir "D:\dist"

.NOTES
  - 目标机器无需安装 Node、无需联网、无需管理员权限
  - 输出: <OutDir>\FTA Studio\  以及 <OutDir>\FTA Studio <ver> (portable).zip
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$SourceDir,
  [string]$OutDir,
  [string]$NodeExe,
  [string]$Version = '1.0.0',
  [switch]$NoZip
)

$ErrorActionPreference = 'Stop'
$SourceDir = (Resolve-Path $SourceDir).Path
if (-not $OutDir) { $OutDir = Join-Path $SourceDir 'dist' }
$OutDir = [IO.Path]::GetFullPath($OutDir)
$pkgName = 'FTA Studio'
$pkg = Join-Path $OutDir $pkgName

Write-Host ""
Write-Host "  FTA Studio - build portable package"
Write-Host "  -----------------------------------"
Write-Host "  source : $SourceDir"
Write-Host "  output : $pkg"

# ---------- 1) 校验源码 ----------
foreach ($f in @('src\launch.mjs', 'src\server.mjs', 'public\index.html')) {
  if (-not (Test-Path (Join-Path $SourceDir $f))) {
    throw "源码不完整，缺少: $f"
  }
}

# ---------- 2) 定位要内置的 node.exe ----------
if (-not $NodeExe) {
  $versions = Join-Path $env:USERPROFILE '.workbuddy\binaries\node\versions'
  if (Test-Path $versions) {
    $latest = Get-ChildItem $versions -Directory |
      Sort-Object { try { [version]($_.Name -replace '[^0-9.].*$','') } catch { [version]'0.0.0' } } -Descending |
      ForEach-Object { Join-Path $_.FullName 'node.exe' } |
      Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($latest) { $NodeExe = $latest }
  }
}
if (-not $NodeExe) {
  $cmd = Get-Command node -ErrorAction SilentlyContinue
  if ($cmd) { $NodeExe = $cmd.Source }
}
if (-not $NodeExe -or -not (Test-Path $NodeExe)) {
  throw "找不到 node.exe。请用 -NodeExe <path> 指定。"
}
Write-Host "  node   : $NodeExe"

# ---------- 3) 组装 ----------
# 已存在则先清理；清理被安全策略拦截时，改用带时间戳的新目录，避免打包到脏文件
if (Test-Path $pkg) {
  try {
    Remove-Item $pkg -Recurse -Force -ErrorAction Stop
  } catch {
    $pkg = "$pkg-" + (Get-Date -Format 'HHmmss')
    Write-Warning "无法清理旧目录，改用: $pkg"
  }
}
New-Item -ItemType Directory -Path (Join-Path $pkg 'runtime'), (Join-Path $pkg 'app') -Force | Out-Null

Copy-Item $NodeExe (Join-Path $pkg 'runtime\node.exe') -Force
foreach ($d in @('src', 'public', 'examples')) {
  $p = Join-Path $SourceDir $d
  if (Test-Path $p) { Copy-Item $p (Join-Path $pkg "app\$d") -Recurse -Force }
}
foreach ($f in @('package.json', 'README.md')) {
  $p = Join-Path $SourceDir $f
  if (Test-Path $p) { Copy-Item $p (Join-Path $pkg "app\$f") -Force }
}

# 启动器模板（与本脚本同级的 assets/launchers）
$tmpl = Join-Path $PSScriptRoot '..\assets\launchers'
if (-not (Test-Path $tmpl)) { throw "找不到启动器模板: $tmpl" }
Copy-Item (Join-Path $tmpl '*') $pkg -Force

# ---------- 4) 编码规范化 ----------
& (Join-Path $PSScriptRoot 'normalize-encoding.ps1') -Directory $pkg | Out-Null

# ---------- 5) 打包 zip ----------
$sizeMB = [math]::Round(((Get-ChildItem $pkg -Recurse -File | Measure-Object Length -Sum).Sum / 1MB), 1)
Write-Host "  size   : $sizeMB MB (uncompressed)"

if (-not $NoZip) {
  $zip = Join-Path $OutDir "$pkgName $Version (portable).zip"
  if (Test-Path $zip) { Remove-Item $zip -Force }
  Compress-Archive -Path $pkg -DestinationPath $zip -CompressionLevel Optimal
  Write-Host "  zip    : $zip  ($([math]::Round((Get-Item $zip).Length/1MB,1)) MB)"
}

Write-Host ""
Write-Host "  Done. Copy the folder or the zip to any Windows PC and run:"
Write-Host "    启动 FTA Studio.bat        (portable, no install)"
Write-Host "    安装到本机.bat             (install + desktop shortcut)"
Write-Host ""
