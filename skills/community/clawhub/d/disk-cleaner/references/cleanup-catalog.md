# 清理清单与分级表

## 分级规则

| 级别 | 判定标准 | 默认行为 |
|---|---|---|
| GREEN 可再生 | 删掉最多导致下次装包/启动变慢，不丢数据 | 进清单，可勾选 |
| YELLOW 需重下 | 删后要重新联网下载或重建索引，体积通常很大 | 需 `--tier yellow` 才进清单 |
| DISCOVERED 发现项 | 启发式扫出，名字像缓存但未人工验证 | 进清单，标记「发现」，需主动勾选 |
| RED 禁止 | 系统关键目录或个人数据 | 永不进清单，脚本硬拦截 |

## GREEN 清单（节选）

包管理器：npm `_cacache` / `npm-cache`、Yarn、pnpm store、pip、Homebrew、APT
运行时：Codex runtimes、Electron 下载缓存、electron-builder、node-gyp
编辑器：VS Code `CachedExtensionVSIXs`、JetBrains `caches/index/log/tmp/localHistory`、Trae/Cursor 的 `CachedData`/`Code Cache`/`GPUCache`/`WebStorage`/`Partitions`
系统：`CrashDumps`、`D3DSCache`、缩略图缓存、用户日志、临时文件（N 天前）
应用：微信小程序 XPlugin、媒体缓存 radium、企业微信 xplugin

## YELLOW 清单

| 项目 | 路径 | 删除代价 |
|---|---|---|
| Maven 本地仓库 | `~/.m2/repository` | Java 项目要重新联网拉依赖 |
| Gradle 分发包 | `~/.gradle/wrapper/dists` | 构建时重下 Gradle |
| Gradle 构建缓存 | `~/.gradle/caches` | 首次构建变慢 |
| HuggingFace 模型 | `~/.cache/huggingface` | 模型权重重下，可能很慢 |
| Puppeteer / Playwright | `~/.cache/puppeteer`、`ms-playwright` | 浏览器重下 |
| Xcode 派生数据 | `~/Library/Developer/Xcode/DerivedData` | 重新编译 |
| iOS 模拟器 | `~/Library/Developer/CoreSimulator` | 模拟器镜像重建 |

## 启发式发现规则（L2）

命中以下目录名正则，且体积 ≥ 阈值（默认 20MB），且不在保护名单内：

```
^(cache|caches|cache2|cachedata|code cache|gpu.?cache|shader.?cache|
  d3dscache|logs?|crashpad|crash ?dumps?|crashinfo|temp|tmp|
  webstorage|session storage|local storage|partitions|blob_storage|
  deriveddata|thumbnails)$
```

保护名单（命中即排除，避免误伤个人数据）：

```
(user|users|profile|profiles|bookmarks?|preferences|credentials|
 logins?|tokens?|documents?|desktop|downloads?|projects?|workspace)
```

扫描范围：缓存根区下**最多 2 层**，避免深递归导致卡顿。

实测样例（Windows 本机，阈值 100MB）：扫出 `uv/cache`、`Postman/Partitions`、`QQ/Partitions`、`Whistle/Cache`、`node-gyp/Cache`、`CodeBuddyExtension/Logs` 等 7 项共 2.51G —— 这些都不在白名单里，靠白名单永远发现不了。

## 禁止清单（RED）

| 路径 | 原因 |
|---|---|
| `C:\Windows\Installer` | 删后程序无法卸载/修复 |
| `C:\Windows\WinSxS` | 系统组件存储，只能用 DISM 官方命令收缩 |
| `C:\Windows\System32`、`C:\Windows\Servicing` | 系统文件 |
| `C:\ProgramData\Package Cache` | 卸载/修复依赖 |
| `/System`、`/usr`、`/bin`、`/etc`、`/Library` | 系统目录 |
| 微信/QQ「文件管理」目录 | 聊天记录与接收的文件 |
| IDE 的 `User` / `config` / `settings` 目录 | 配置、插件、对话记录 |

脚本内 `FORBIDDEN_PARTS` + `assert_safe()` 双重拦截。

## 实测记录（2026-09-10，Windows）

一轮完整清理 **C 盘可用 15G → 57G（释放约 42G）**：

| 类别 | 释放 |
|---|---|
| WPS addons | 9.5G |
| Trae 系列缓存 | 约 8G |
| JetBrains 缓存 | 约 5G |
| npm 缓存 | 3.2G |
| 微信/企业微信 | 3.5G |
| VS Code 扩展包、Gradle、Codex、其余 | 约 13G |

## 命令速查

```bash
python scripts/clean_cache.py --dry-run            # 只出清单
python scripts/clean_cache.py                      # 交互勾选
python scripts/clean_cache.py --pick 1,3,5         # 指定序号
python scripts/clean_cache.py --pick g             # 只删可再生
python scripts/clean_cache.py --tier yellow        # 清单含「需重下」
python scripts/clean_cache.py --min-size 100       # 只列 ≥100MB
python scripts/clean_cache.py --no-discover        # 只查白名单
python scripts/clean_cache.py --json               # JSON 输出
```
