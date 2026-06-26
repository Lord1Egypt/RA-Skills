---
name: app-cache-migration
description: 将 Windows 系统上任意开发工具（如 VSCode、Yarn、npm、pip、Gradle、Docker 等）的缓存、插件、数据目录迁移到指定目录（如 E/D 盘），通过 NTFS Junction 实现对应用完全透明的重定向。当用户请求"迁移应用的缓存到 X 盘"、"将 XX 的数据目录移到 D/E 盘"、"释放 C 盘空间"、"清理并迁移 XX 缓存"或类似意图时触发。 (user)
agent_created: true
---

# App Cache Migration

## Overview

将 Windows 任意应用的缓存/插件/数据目录从当前盘（通常为 C 盘）迁移到用户指定的目标目录，通过 **NTFS Junction** 对应用完全透明地重定向——应用无感知，路径不变，数据在目标盘。

**核心原则（不可跳过）**：**先完整复制 → 再删除原目录 → 最后创建 Junction**，确保迁移中断时数据不丢失。

**适用系统**：Windows 10/11（需管理员权限运行 PowerShell）  
**不适用**：macOS / Linux（用 symlink 替代 Junction）

---

## Step 0: 收集信息

### 0-1 确认目标路径

从用户对话中提取：

| 参数 | 说明 | 示例 |
|------|------|------|
| **应用名** | "迁移 XXX 缓存" | `VSCode`、`Gradle`、`pip` |
| **目标目录** | "移到 E:/AppData" | `E:\AppData\Local` |

若用户未指定目标目录，询问：**"请问希望迁移到哪个目录？（如 E:\AppData\Local）"**

### 0-2 扫描当前占用（推荐先运行）

```powershell
# 运行扫描脚本，显示 AppData 中 >= 20 MB 的目录及迁移建议
powershell -File scan-usage.ps1 -MinSizeMB 20 -TopN 30
```

输出示例：
```
大小(MB)  状态          路径
   820.0  [推荐迁移]    C:\Users\admin\AppData\Local\Yarn\Cache\v6
   612.3  [已迁移]      C:\Users\admin\AppData\Roaming\Code\Cache
   410.0  [推荐迁移]    C:\Users\admin\AppData\Local\pip\Cache
   ...
```

### 0-3 查找应用缓存路径

#### 已知应用速查表

| 应用 | 源路径 | 迁移方式 |
|------|--------|---------|
| **VSCode** | `%APPDATA%\Code\{Cache, CachedData, GPUCache, Code Cache, ...}` | Junction |
| **VSCode Extensions** | `%USERPROFILE%\.vscode\extensions` | Junction + `--extensions-dir` 启动参数 |
| **Cursor** | `%APPDATA%\Cursor\{Cache, CachedData, ...}` | Junction |
| **Cursor Extensions** | `%USERPROFILE%\.cursor\extensions` | Junction |
| **Yarn 1.x** | `%LOCALAPPDATA%\Yarn\Cache\v6` | Junction + `yarn config set cache-folder <新路径>` |
| **npm** | `%APPDATA%\npm-cache` | Junction + `npm config set cache <新路径>` |
| **pnpm** | `%LOCALAPPDATA%\pnpm\cache`、`pnpm\store` | Junction + `pnpm config set cache-dir <新路径>` |
| **pip** | `%LOCALAPPDATA%\pip\Cache` | Junction（或 `pip config set global.cache-dir <新路径>`） |
| **uv** (Python) | `%LOCALAPPDATA%\uv\cache` | Junction（或 `UV_CACHE_DIR` 环境变量） |
| **Poetry** | `%LOCALAPPDATA%\pypoetry\Cache` | Junction |
| **conda/Miniconda** | `%USERPROFILE%\anaconda3\pkgs` | Junction（或 `conda config --set pkgs_dirs <新路径>`） |
| **Gradle** | `%USERPROFILE%\.gradle\caches`、`.gradle\wrapper` | Junction（或 `GRADLE_USER_HOME` 环境变量）|
| **Maven** | `%USERPROFILE%\.m2\repository`、`.m2\wrapper` | Junction（或 `settings.xml localRepository` 节点）|
| **NuGet** | `%LOCALAPPDATA%\NuGet\Cache`、`NuGet\v3-cache` | Junction（或 `nuget config -set globalPackagesFolder=<新路径>`）|
| **IntelliJ IDEA** | `%LOCALAPPDATA%\JetBrains\IntelliJIdea*` | Junction（或 IDE 内 Help → Edit Custom Properties 配置 `idea.system.path`）|
| **PyCharm** | `%LOCALAPPDATA%\JetBrains\PyCharm*` | 同上，`pycharm.system.path` |
| **WebStorm** | `%LOCALAPPDATA%\JetBrains\WebStorm*` | 同上，`webstorm.system.path` |
| **其他 JetBrains** | `%LOCALAPPDATA%\JetBrains\<IDE名>*` | 同上模式 |
| **Docker Desktop** | `%LOCALAPPDATA%\Docker` | Junction（建议同时修改 Docker Desktop → Settings → Resources → Disk image location）|
| **Rust Cargo** | `%USERPROFILE%\.cargo\registry`、`.cargo\git` | Junction（或 `CARGO_HOME` 环境变量）|
| **Go Modules** | `%LOCALAPPDATA%\go\pkg\mod` | Junction（或 `GOPATH` / `GOMODCACHE` 环境变量）|
| **Ruby Gems** | `%USERPROFILE%\.gem` | Junction（或 `GEM_HOME` 环境变量）|
| **Chrome 缓存** | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache` | Junction |
| **Edge 缓存** | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache` | Junction |
| **Electron 应用** | `%APPDATA%\<应用名>\{Cache,Code Cache,GPUCache}` | Junction（Electron 系列路径规律相同）|

#### 未知应用：如何找到缓存路径

若应用不在速查表中，按以下顺序定位缓存目录：

```powershell
# 1. 搜索应用名（模糊匹配）
$appName = "MyApp"  # 替换为实际应用名

# 在 APPDATA\Roaming 中搜索
Get-ChildItem "$env:APPDATA" -Directory | Where-Object Name -like "*$appName*"

# 在 APPDATA\Local 中搜索
Get-ChildItem "$env:LOCALAPPDATA" -Directory | Where-Object Name -like "*$appName*"

# 在用户根目录下搜索隐藏目录（.xxx 格式）
Get-ChildItem "$env:USERPROFILE" -Directory -Force | Where-Object Name -like "*$appName*"

# 2. 查看进程打开的文件（Process Monitor / Handle 工具）
# 也可使用 Sysinternals Process Monitor 运行应用后筛选 "WriteFile" 事件
```

---

## Step 1: 迁移执行

### 通用迁移（适用任意应用，首选）

```powershell
# 语法
powershell -File migrate-any.ps1 -SourcePath "<原路径>" -DstPath "<目标路径>"

# 示例：迁移 pip 缓存
powershell -File migrate-any.ps1 `
  -SourcePath "$env:LOCALAPPDATA\pip\Cache" `
  -DstPath "E:\AppData\Local\pip\Cache"

# 示例：迁移 Gradle 缓存
powershell -File migrate-any.ps1 `
  -SourcePath "$env:USERPROFILE\.gradle\caches" `
  -DstPath "E:\AppData\gradle\caches"

# 示例：迁移 Docker Desktop 数据
powershell -File migrate-any.ps1 `
  -SourcePath "$env:LOCALAPPDATA\Docker" `
  -DstPath "E:\AppData\Docker"

# 示例：迁移 IntelliJ IDEA 本地缓存
powershell -File migrate-any.ps1 `
  -SourcePath "$env:LOCALAPPDATA\JetBrains\IntelliJIdea2024.1" `
  -DstPath "E:\AppData\JetBrains\IntelliJIdea2024.1"
```

`migrate-any.ps1` 会自动完成：复制数据 → 删除原目录 → 创建 Junction → 验证。

### 批量迁移（一次迁移多个目录）

```powershell
function Invoke-JunctionMigrate {
    param([string]$Src, [string]$Dst)
    if (-not (Test-Path $Src)) { Write-Host "跳过(不存在): $Src" -ForegroundColor Gray; return }
    $item = Get-Item $Src -Force
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        Write-Host "跳过(已是Junction): $Src" -ForegroundColor DarkCyan; return
    }
    New-Item -ItemType Directory -Path $Dst -Force | Out-Null
    $sz = (Get-ChildItem $Src -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    Write-Host ("迁移 $Src ({0:N1} MB)..." -f ($sz/1MB)) -ForegroundColor Yellow
    Copy-Item "$Src\*" $Dst -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item $Src -Recurse -Force
    cmd /c "mklink /J `"$Src`" `"$Dst`"" 2>&1 | Out-Null
    $ok = (Get-Item $Src -Force).Attributes -band [IO.FileAttributes]::ReparsePoint
    Write-Host ("  $(if($ok){'✓ Junction OK'}else{'✗ FAIL'}): $Src") -ForegroundColor $(if($ok){"Green"}else{"Red"})
}

# 示例：批量迁移 VSCode + Yarn + pip
$dst = "E:\AppData"
Invoke-JunctionMigrate "$env:APPDATA\Code\Cache"            "$dst\VSCode\Cache"
Invoke-JunctionMigrate "$env:APPDATA\Code\CachedData"       "$dst\VSCode\CachedData"
Invoke-JunctionMigrate "$env:APPDATA\Code\GPUCache"         "$dst\VSCode\GPUCache"
Invoke-JunctionMigrate "$env:LOCALAPPDATA\Yarn\Cache\v6"    "$dst\yarn\v6"
Invoke-JunctionMigrate "$env:LOCALAPPDATA\pip\Cache"        "$dst\pip\Cache"
```

### 应用专用脚本（进阶，含配置同步）

| 脚本 | 适用场景 | 核心参数 |
|------|---------|---------|
| `migrate-vscode.ps1` | VSCode 完整迁移（缓存+插件+修改启动脚本） | `-DstBase <目标根目录>` |
| `migrate-yarn.ps1` | Yarn 缓存迁移 + `yarn config` 配置更新 | `-DstPath <目标路径>` |
| `migrate-npm.ps1` | npm 缓存迁移 + `npm config` 配置更新 | `-DstPath <目标路径>` |

---

## Step 2: 应用配置同步

部分应用需要在 Junction 之外额外同步配置，否则可能绕过 Junction 写入新路径：

### 包管理器类

```bash
yarn config set cache-folder "E:\AppData\yarn"
npm config set cache "E:\AppData\npm-cache"
pnpm config set cache-dir "E:\AppData\pnpm\cache"
pnpm config set store-dir "E:\AppData\pnpm\store"
pip config set global.cache-dir "E:\AppData\pip\Cache"
```

### JVM 工具类（环境变量方式）

```powershell
# 设置用户级别环境变量（持久生效）
[Environment]::SetEnvironmentVariable("GRADLE_USER_HOME", "E:\AppData\gradle", "User")
[Environment]::SetEnvironmentVariable("M2_HOME", "E:\AppData\maven", "User")
# 注意：Maven 通常读 %USERPROFILE%\.m2，Junction 方式更稳定
```

### Go / Rust / Ruby

```powershell
[Environment]::SetEnvironmentVariable("GOMODCACHE", "E:\AppData\go\pkg\mod", "User")
[Environment]::SetEnvironmentVariable("CARGO_HOME", "E:\AppData\cargo", "User")
[Environment]::SetEnvironmentVariable("GEM_HOME", "E:\AppData\gem", "User")
```

### VSCode/Cursor 插件路径（修改启动参数）

```powershell
$codeCmd = (Split-Path (Get-Command code -ErrorAction SilentlyContinue).Source) + "\code.cmd"
if (Test-Path $codeCmd) {
    $content = Get-Content $codeCmd -Raw
    if ($content -notmatch "extensions-dir") {
        # 在调用 Code.exe 的行末尾插入参数
        $newContent = $content -replace '(Code\.exe[^\r\n]*%\*)', '$1 --extensions-dir "E:\AppData\VSCode\extensions"'
        [System.IO.File]::WriteAllText($codeCmd, $newContent, [Text.Encoding]::UTF8)
        Write-Host "已更新 code.cmd" -ForegroundColor Green
    }
}
```

### Docker Desktop（迁移后修改镜像存储位置）

打开 Docker Desktop → Settings → Resources → Advanced → Disk image location → 修改为目标盘路径 → Apply & Restart

---

## Step 3: 验证

```powershell
# 自动检查所有已知应用的 Junction 状态
powershell -File verify.ps1

# 仅验证指定路径
powershell -File verify.ps1 -Paths "$env:LOCALAPPDATA\pip\Cache", "$env:USERPROFILE\.gradle\caches"

# 验证并统计目标目录数据量
powershell -File verify.ps1 -ScanDir "E:\AppData"
```

---

## Step 4: 清理残留（可选）

Junction 迁移后 C 盘原目录已是链接（无实体数据），通常无需清理。

仅在确认迁移成功后，如需删除 Junction 本身（极少数情况）：

```powershell
# 安全删除 Junction（只删链接，不影响目标盘数据）
function Remove-JunctionOnly([string]$Path) {
    $item = Get-Item $Path -Force -ErrorAction SilentlyContinue
    if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        Remove-Item $Path -Force  # 只删 Junction，不递归删目标内容
        Write-Host "已删除 Junction: $Path"
    } else {
        Write-Host "非 Junction，跳过（防止误删）: $Path" -ForegroundColor Red
    }
}
```

---

## Scripts 参考

| 脚本 | 功能 | 关键参数 |
|------|------|---------|
| `scan-usage.ps1` | 扫描 AppData 大目录，标记可迁移路径 | `-MinSizeMB` `-TopN` |
| `migrate-any.ps1` | **通用单目录 Junction 迁移**（首选） | `-SourcePath` `-DstPath` |
| `migrate-vscode.ps1` | VSCode 完整迁移（缓存+插件+启动脚本） | `-DstBase` `-ExtDstPath` |
| `migrate-yarn.ps1` | Yarn 缓存迁移 + 配置更新 | `-DstPath` |
| `migrate-npm.ps1` | npm 缓存迁移 + 配置更新 | `-DstPath` |
| `verify.ps1` | 验证 Junction 状态（支持任意路径） | `-Paths` `-ScanDir` |

---

## 常见问题

**Q: Junction 和软链接（symlink）有什么区别？**  
A: Junction 是目录级 NTFS 重定向，只需普通用户权限（某些系统需管理员），对应用完全透明。symlink 可指向文件，但需要 SeCreateSymbolicLink 权限。对于目录迁移，Junction 是 Windows 上的首选方案。

**Q: 迁移后应用启动报错找不到路径？**  
A: 确认 Junction 已正确创建（`Get-Item $path -Force` 的 Attributes 包含 ReparsePoint）。若应用写死了绝对路径到配置文件，还需同步修改配置（见 Step 2）。

**Q: 迁移时提示"拒绝访问"？**  
A: 以管理员身份运行 PowerShell，或先关闭占用该目录的进程（如 VSCode、IDEA 等）。

**Q: 目标盘格式有什么要求？**  
A: 必须是 **NTFS** 格式。FAT32、exFAT 不支持 Junction。
