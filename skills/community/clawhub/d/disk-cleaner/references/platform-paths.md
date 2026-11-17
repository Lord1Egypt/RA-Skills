# 三平台缓存路径对照

## 缓存根区（L1 平台探测）

| 平台 | 类型 | 路径 |
|---|---|---|
| Windows | 应用数据 | `%LOCALAPPDATA%`、`%APPDATA%`、`%LOCALAPPDATA%\LocalLow` |
| Windows | 临时 | `%LOCALAPPDATA%\Temp`、`C:\Windows\Temp` |
| macOS | 用户缓存 | `~/Library/Caches` |
| macOS | 日志 | `~/Library/Logs` |
| macOS | 容器缓存 | `~/Library/Containers/*/Data/Library/Caches` |
| macOS | 开发者 | `~/Library/Developer`（Xcode DerivedData、CoreSimulator、Archives） |
| macOS | 应用支持 | `~/Library/Application Support/*/Cache` |
| macOS | 临时 | `$TMPDIR` 或 `/tmp` |
| Linux | 用户缓存 | `~/.cache`（或 `$XDG_CACHE_HOME`） |
| Linux | 应用数据 | `~/.local/share`、`~/.config` |
| Linux | 系统缓存 | `/var/cache`（apt、dnf、pacman） |
| Linux | 回收站 | `~/.local/share/Trash` |
| Linux | 临时 | `/tmp` |

## 各平台特有清理项

### Windows

| 项目 | 路径 |
|---|---|
| npm | `%LOCALAPPDATA%\npm-cache`、`%APPDATA%\npm-cache` |
| Electron 系（VS Code / Trae / Cursor） | `%APPDATA%\<App>\CachedData`、`Code Cache`、`GPUCache`、`WebStorage`、`Partitions` |
| JetBrains | `%LOCALAPPDATA%\JetBrains\*\{caches,index,log,tmp,localHistory}` |
| WPS | `%APPDATA%\kingsoft\wps\addons`（文件极多，别用资源管理器打开） |
| 微信/企业微信 | `%APPDATA%\Tencent\WeChat\XPlugin`、`radium`、`xwechat\radium`、`xplugin` |
| 系统杂项 | `CrashDumps`、`D3DSCache` |

### macOS

| 项目 | 路径 | 分级 |
|---|---|---|
| Homebrew | `~/Library/Caches/Homebrew` | GREEN |
| Xcode 缓存 | `~/Library/Caches/com.apple.dt.Xcode` | GREEN |
| 用户日志 | `~/Library/Logs` | GREEN |
| Xcode 派生数据 | `~/Library/Developer/Xcode/DerivedData` | YELLOW（可达数十 G） |
| iOS 模拟器 | `~/Library/Developer/CoreSimulator` | YELLOW |
| Xcode 归档 | `~/Library/Developer/Xcode/Archives` | YELLOW |
| Docker | `~/Library/Containers/com.docker.docker` | 建议用 Docker Desktop 自带清理 |

系统级：`/Library/Caches`、`/private/var/folders`（需 sudo，交给系统「存储管理」）。

### Linux

| 项目 | 路径 | 分级 |
|---|---|---|
| APT 包缓存 | `/var/cache/apt/archives`（需 `apt clean` 或 root） | GREEN |
| 缩略图 | `~/.cache/thumbnails` | GREEN |
| 回收站 | `~/.local/share/Trash` | GREEN |
| systemd 日志 | `/var/log/journal`（建议 `journalctl --vacuum-size=200M`） | GREEN |
| 用户缓存 | `~/.cache/*` | GREEN |

## 平台差异处理（脚本内已实现）

| 能力 | Windows | macOS | Linux |
|---|---|---|---|
| 剩余空间 | `GetDiskFreeSpaceExW` | `os.statvfs` | `os.statvfs` |
| 长路径 | `\\?\` 前缀 | 不需要 | 不需要 |
| 进程检测 | `tasklist` | `ps -eo comm=` | `ps -eo comm=` |
| 清空回收站 | `SHEmptyRecycleBinW` | 删 `~/.Trash` | 删 `~/.local/share/Trash` |

## 环境变量推导

受限 Shell 里 `APPDATA` / `USERPROFILE` 可能为空，脚本的 `build_context()` 逐级兜底：

1. 直接读环境变量
2. `LOCALAPPDATA` 反推 `APPDATA`：`LOCALAPPDATA[:rfind('appdata\local')] + 'AppData\Roaming'`
3. `HOME` 拼 `AppData\Roaming`

**不要改回只依赖 `os.path.expandvars`**，否则在 Git Bash / 受限会话里会静默跳过大量条目。
