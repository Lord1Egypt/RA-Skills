# VSCode 完整迁移脚本
# 用法: powershell -File migrate-vscode.ps1 [-DstBase "E:\AppData\Local\VSCode"]
#
# 迁移内容:
#   1. VSCode 缓存目录 (AppData\Roaming\Code 下 9 个子目录)
#   2. VSCode 插件目录 (.vscode\extensions)
#   3. VSCode 启动脚本 (code.cmd + code bash)
#   4. VSCode settings.json (extensionsPath)

param(
    [string]$DstBase = "E:\AppData\Local\VSCode",
    [string]$ExtDstPath = "",
    [switch]$SkipExtensions,
    [switch]$SkipLaunchers
)

# 默认插件迁移路径
if ([string]::IsNullOrEmpty($ExtDstPath)) {
    $ExtDstPath = Join-Path $DstBase "extensions"
}

$srcCodeBase = "$env:APPDATA\Code"
$srcExt = "$env:USERPROFILE\.vscode\extensions"

$cacheDirs = @(
    "Cache",
    "CachedData",
    "CachedExtensionVSIXs",
    "Code Cache",
    "GPUCache",
    "DawnGraphiteCache",
    "DawnWebGPUCache",
    "CachedProfilesData",
    "CachedConfigurations"
)

Write-Host "=== VSCode 完整迁移 ===" -ForegroundColor Cyan
Write-Host "目标目录: $DstBase"
Write-Host ""

# --- 函数定义 ---
function Invoke-JunctionMigrate {
    param([string]$Src, [string]$Dst, [string]$Name)

    Write-Host "--- $Name ---" -ForegroundColor Yellow
    if (-not (Test-Path $Src)) {
        Write-Host "跳过（不存在）: $Src" -ForegroundColor Gray
        return
    }

    if (-not (Test-Path $Dst)) {
        New-Item -ItemType Directory -Path $Dst -Force | Out-Null
    }

    $size = (Get-ChildItem $Src -Recurse -Force -ErrorAction SilentlyContinue |
        Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    Write-Host ("复制中... ({0:N1} MB)" -f ($size / 1MB))

    Copy-Item -Path "$Src\*" -Destination $Dst -Recurse -Force -ErrorAction SilentlyContinue

    Remove-Item -Path $Src -Recurse -Force -ErrorAction Stop
    cmd /c "mklink /J `"$Src`" `"$Dst`"" 2>&1 | Out-Null

    $item = Get-Item $Src -Force -ErrorAction SilentlyContinue
    if ($item -and ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
        Write-Host "  OK: $Name" -ForegroundColor Green
    } else {
        Write-Host "  FAIL: $Name" -ForegroundColor Red
    }
}

# --- Step 1: 迁移缓存目录 ---
Write-Host "--- Step 1: 迁移 VSCode 缓存目录 ---" -ForegroundColor Cyan
foreach ($dir in $cacheDirs) {
    Invoke-JunctionMigrate -Src "$srcCodeBase\$dir" -Dst "$DstBase\$dir" -Name $dir
}

# --- Step 2: 迁移插件目录 ---
if (-not $SkipExtensions) {
    Write-Host ""
    Write-Host "--- Step 2: 迁移 VSCode 插件 ---" -ForegroundColor Cyan
    Invoke-JunctionMigrate -Src $srcExt -Dst $ExtDstPath -Name "extensions"
}

# --- Step 3: 修改启动脚本 ---
if (-not $SkipLaunchers) {
    Write-Host ""
    Write-Host "--- Step 3: 修改 VSCode 启动脚本 ---" -ForegroundColor Cyan

    # 找 VSCode 安装位置
    $vscodeExe = Get-ChildItem "D:\Programs\Microsoft VS Code\Code.exe" -ErrorAction SilentlyContinue
    if (-not $vscodeExe) {
        $vscodeExe = Get-ChildItem "$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe" -ErrorAction SilentlyContinue
    }
    if (-not $vscodeExe) {
        Write-Host "  警告: 未能定位 VSCode 安装路径，跳过启动脚本修改" -ForegroundColor Yellow
    } else {
        $vscodeBin = Split-Path $vscodeExe.FullName -Parent
        $codeCmd = Join-Path $vscodeBin "bin\code.cmd"
        $codeBash = Join-Path $vscodeBin "bin\code"

        # code.cmd
        if (Test-Path $codeCmd) {
            $content = Get-Content $codeCmd -Raw
            if ($content -notmatch "extensions-dir") {
                # 提取版本号目录
                # 在 %* 之前插入 --extensions-dir 参数（兼容各版本 code.cmd）
                $newContent = $content -replace '(%\*\s*)$', "--extensions-dir `"$ExtDstPath`" %*"
                if ($newContent -eq $content) {
                    # fallback: 在最后一个 %* 前插入
                    $newContent = $content -replace '\s+%\*', " --extensions-dir `"$ExtDstPath`" %*"
                }
                [System.IO.File]::WriteAllText($codeCmd, $newContent, [System.Text.Encoding]::UTF8)
                Write-Host "  OK: code.cmd 已添加 --extensions-dir" -ForegroundColor Green
            } else {
                Write-Host "  跳过: code.cmd 已有 --extensions-dir" -ForegroundColor Gray
            }
        }

        # code (bash)
        if ((Test-Path $codeBash) -and ((Get-Content $codeBash -Raw) -notmatch "extensions-dir")) {
            $content = Get-Content $codeBash -Raw
            $newContent = $content -replace (
                '(ELECTRON_RUN_AS_NODE=1 "\$ELECTRON" "\$CLI")',
                "`$1 --extensions-dir `"$ExtDstPath`""
            )
            if ($newContent -ne $content) {
                Set-Content -Path $codeBash -Value $newContent -NoNewline
                Write-Host "  OK: code (bash) 已添加 --extensions-dir" -ForegroundColor Green
            }
        }
    }

    # settings.json
    Write-Host ""
    Write-Host "--- Step 4: 更新 VSCode settings.json ---" -ForegroundColor Cyan
    $settingsPath = "$env:APPDATA\Code\User\settings.json"
    if (Test-Path $settingsPath) {
        $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($settings) {
            $settings | Add-Member -NotePropertyName "extensionsPath" -NotePropertyValue ($ExtDstPath -replace '\\', '/') -Force
            $settings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -NoNewline
            Write-Host "  OK: settings.json 已添加 extensionsPath" -ForegroundColor Green
        }
    }
}

# --- Step 5: 汇总 ---
Write-Host ""
Write-Host "=== 迁移完成 ===" -ForegroundColor Cyan
$totalSize = (Get-ChildItem $DstBase -Recurse -Force -ErrorAction SilentlyContinue |
    Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
Write-Host ("目标目录数据量: {0:N1} MB ({1:N2} GB)" -f ($totalSize/1MB, $totalSize/1GB)) -ForegroundColor Cyan
