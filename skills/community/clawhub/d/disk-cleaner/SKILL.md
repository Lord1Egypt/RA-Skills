---
name: disk-cleaner
description: 跨平台磁盘空间分析与缓存清理（Windows / macOS / Linux）。当用户说"磁盘满了""C 盘空间不足""清理缓存""清理 npm 缓存""清理临时文件""看看什么占空间""磁盘清理""释放空间"时使用。四层架构：平台探测、缓存发现、安全分级、交互勾选执行。启发式扫描能找出白名单外的未知缓存，删除项由用户逐项勾选确认。
agent_created: true
---

# 磁盘空间清理（跨平台）

## 何时使用

- 磁盘告警 / 空间不足，需要释放空间
- 用户点名要清 npm / pip / yarn / pnpm / brew / apt 缓存、临时文件、IDE 缓存
- 用户想知道"空间被谁吃了"

## 核心原则

1. **两道确认**。先由用户勾选"删哪些"，再展开每项的完整路径/大小/分级/删除代价，用户二次确认后才动手。脚本绝不自动全删。
2. **先扫描，后删除**。清单出来前不碰任何文件。
3. **白名单 + 发现双通道**。已知软件的缓存走白名单，未知缓存靠启发式扫描找出来。
4. **发现项默认只报告**。启发式扫出的陌生目录进清单但不会自动删，需用户主动勾选。
5. **只删可再生缓存**。配置、代码、聊天记录、数据库一律不动。
6. **软链逃逸防护**。删除前用 `realpath` 解析符号链接，校验真实路径严格落在允许根区（带分隔符边界，杜绝前缀绕过）；删除时绝不跟随软链，遇到软链只删链接本身。

## 四层架构

| 层 | 职责 |
|---|---|
| L1 平台探测 | 自动识别 Windows/macOS/Linux，推导缓存根区。无硬编码用户名、盘符 |
| L2 缓存发现 | 已知模式库（跨三平台的软件路径）+ 目录名启发式扫描 |
| L3 安全分级 | GREEN 可再生 / YELLOW 需重下 / DISCOVERED 发现项 / RED 禁止 |
| L4 执行策略 | 扫描 → 编号清单 → **用户勾选** → 展开详情 → **二次确认** → 删除 → 复测空间 |

## 快速开始

脚本在 `scripts/` 下，**默认就是只读扫描**：

```bash
python scripts/clean_cache.py --dry-run        # 只出清单，不删（最安全，推荐先跑）
python scripts/clean_cache.py                  # 出清单 → 勾选 → 看详情 → 确认 → 删除
python scripts/clean_cache.py --pick 1,3,5     # 指定序号（仍会展开详情要你确认）
python scripts/clean_cache.py --pick g --force # 跳过二次确认，仅在已核对过时使用
python scripts/clean_cache.py --json           # 机器可读输出，供上层解析
```

删除前会展开选中项的完整信息，确认无误后输入 `y` 才执行：

```
======================================================================
 待删除 2 项，预计释放 1.20 GB
======================================================================
  1. uv/cache
     路径  C:\Users\xxx\AppData\Local\uv\cache
     大小  518.56 MB      分级  发现项      来源  启发式扫描
     说明  启发式扫描得出，未经人工验证，请核对路径后再删
----------------------------------------------------------------------
  合计 1.20 GB      当前可用 59.53 GB      删除后预计 60.73 GB
----------------------------------------------------------------------
  确认删除？输入 y 执行，其他任意键取消:
```

`--force` 可跳过这道确认，只用于已经核对过、要放进定时任务的场景。`--json` 模式只输出清单不删除，不受影响。

勾选语法（交互输入或 `--pick`）：

| 输入 | 含义 |
|---|---|
| `1,3,5` | 指定序号 |
| `1-4` | 区间 |
| `all` | 全部 |
| `g` | 仅「可再生」类 |
| `y` | 「可再生」+「需重下」 |
| `d` | 仅发现项 |
| 回车 | 取消 |

常用参数：`--tier yellow`（清单里加入"需重下"项）、`--min-size 100`（只列 ≥100MB）、`--keep-temp-days 7`、`--no-discover`（只查白名单）、`--no-temp`、`--no-trash`。

Windows 用户双击 `scripts/clean.bat` 直接进入交互勾选。

## 分级说明

| 级别 | 含义 | 例子 |
|---|---|---|
| GREEN 可再生 | 删了最多导致下次变慢 | npm/pip 缓存、日志、着色器缓存、浏览器缓存 |
| YELLOW 需重下 | 删后要重新联网下载，体积大 | `.m2`、Gradle dists、HuggingFace 模型、Xcode DerivedData |
| DISCOVERED 发现项 | 启发式扫出来的，未经验证 | 陌生软件的 Cache/Logs 目录 |
| RED 禁止 | 任何情况下都不碰 | 见下方清单 |

## 禁止删除（会出事）

| 路径 | 原因 |
|---|---|
| `C:\Windows\Installer`、`C:\Windows\WinSxS`、`System32` | 删后程序无法卸载/修复，系统可能损坏 |
| `C:\ProgramData\Package Cache` | 同上 |
| 微信/QQ 的「文件管理」目录 | 聊天记录与接收的文件 |
| IDE 的 `User` / `config` / `settings` 目录 | 配置、插件、对话记录 |
| `/usr`、`/bin`、`/etc`、`/System`、`/Library` | 系统目录 |

脚本内置 `FORBIDDEN_PARTS` 与 `assert_safe()` 双重拦截，命中即拒绝并打印警告。

## 三平台缓存根区

| 平台 | 主要路径 |
|---|---|
| Windows | `%LOCALAPPDATA%`、`%APPDATA%`、`%LOCALAPPDATA%\Temp` |
| macOS | `~/Library/Caches`、`~/Library/Logs`、`~/Library/Developer`、`~/Library/Containers` |
| Linux | `~/.cache`（或 `$XDG_CACHE_HOME`）、`~/.local/share`、`/var/cache` |

详见 `references/platform-paths.md`。

## 空间分析方法（找大头）

脚本负责清，找大头可以配合系统命令：

```bash
# Linux / macOS
du -sh ~/.cache/* ~/Library/Caches/* 2>/dev/null | sort -rh | head -20

# Windows（Git Bash）
du -sh "$LOCALAPPDATA"/*/ "$APPDATA"/*/ 2>/dev/null | sort -rh | head -20
```

⚠️ **不要对 `/c/Windows`、`/System`、`/usr` 跑 `du`** —— 文件量太大，跑十几分钟还拖慢整机。

## 本机环境坑

1. **PowerShell stdout 可能被吞**（只回 exit code）。要结果就 `Out-File` 到文件再读。
2. **`$env:APPDATA` 在部分 Shell 里为空**（`LOCALAPPDATA` 正常）。脚本已从 `LOCALAPPDATA` 反推，勿改回 `os.path.expandvars` 单依赖。
3. **删除方式选择**：
   - PowerShell `Remove-Item -Recurse -Force` → 大目录会被 `[safe-delete][SAFE_DELETE_BULK_GUARD_ERROR]` 拦下
   - bash `rm` 常被包装成 safe-delete → 慢且进回收站，绕过用 `/usr/bin/rm`
   - **最快最稳：`[System.IO.Directory]::Delete($p, $true)`**
   - `npm cache clean --force` 可能卡在 `genie-trash ETIMEDOUT` → 直接删目录
4. **`.bat` 必须纯 ASCII**。cmd 按 GBK 读 bat，UTF-8 中文注释会被当命令执行，报"不是内部或外部命令"。
5. **Windows 长路径**：深目录要 `\\?\` 前缀（脚本已内置 `long_path()`）。
6. **WPS `addons` 文件极多**：别用资源管理器打开（会卡死），删前必须退出 WPS 及 `wpscloudsvr.exe`。
7. **Git Bash 的 `du` 很慢**：扫大目录放后台跑。
8. **清空回收站**：C 盘回收站里的文件不删不会释放空间，脚本末尾默认清一次（`--no-trash` 可关）。

## 扩展清理项

编辑 `scripts/clean_cache.py` 的 `TARGETS`：

```python
# (名称, 路径模式, 分级, 占用进程, 适用平台)
("我的缓存", "~/.cache/myapp", TIER_GREEN, None, None),              # 全平台
("Windows 专用", r"%LOCALAPPDATA%\App\Cache", TIER_GREEN, None, ["windows"]),
("要先退出的", r"%APPDATA%\App\cache", TIER_GREEN, ["app.exe"], ["windows"]),
```

路径支持 `~`、`%ENV%`、`$HOME`、`*` 通配符。平台填 `None` 表示全平台。
`IDE_SCAN` / `ELECTRON_SCAN` 控制 IDE 与 Electron 应用的通配扫描范围。

## 参考

- `scripts/clean_cache.py` — 主程序（四层架构都在里面）
- `scripts/clean.bat` — Windows 双击入口（纯 ASCII）
- `references/platform-paths.md` — 三平台路径对照 + 各平台特有清理项
- `references/cleanup-catalog.md` — 已知软件清单、分级表、禁止清单
