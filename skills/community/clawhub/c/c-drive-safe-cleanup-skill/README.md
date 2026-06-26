# C盘安全清理 Skill

用于 Windows 环境下的 C 盘安全清理，强调白名单目录、逐项确认和可追溯日志。

## 开源信息

- 仓库地址：`https://github.com/wanyvo/c-drive-safe-cleanup-skill`
- 默认分支：`main`
- 许可证：`MIT`（见 `LICENSE`）

## 包内容

- `skill.md`：技能主说明（触发、边界、流程、约束）
- `script/c-drive-safe-cleanup.ps1`：执行脚本
- `references/safety.md`：安全边界说明
- `meta.json`：技能元信息（名称、触发词、入口、能力边界）

## 功能特性

- 仅扫描白名单安全目录（临时文件、缓存、日志、预读、AppData 遗留缓存）
- 若检测到 WPS 安装，额外纳入 WPS 暂存/缓存目录
- 每个目录先解释“作用/垃圾来源/删除影响”，再逐项询问是否清理
- 用户确认后才删除，且只删除目录内容、不删除目录本身
- 输出 Markdown 日志到 `tasks/`
- 下载/桌面大文件仅提醒，不自动删除

## 快速使用

### 演练模式（推荐先试）

```powershell
powershell -ExecutionPolicy Bypass -File ".\script\c-drive-safe-cleanup.ps1" -DryRun
```

### 正式清理

```powershell
powershell -ExecutionPolicy Bypass -File ".\script\c-drive-safe-cleanup.ps1"
```

### 自定义日志路径

```powershell
powershell -ExecutionPolicy Bypass -File ".\script\c-drive-safe-cleanup.ps1" -LogOutputPath ".\tasks\evaluation-2026-04-22-c-disk-cleanup.md"
```

## 推荐唤醒话术

- 请使用 c-drive-safe-cleanup skill，以 DryRun 演示模式执行 C 盘安全清理。
- C盘满了，帮我做一次安全清理演示，只扫白名单目录，不要真正删除。

## 使用示例（建议流程）

1. 先运行演练模式查看扫描结果和每项说明：
   - `powershell -ExecutionPolicy Bypass -File ".\script\c-drive-safe-cleanup.ps1" -DryRun`
2. 确认结果后运行正式清理，按提示逐项选择：
   - `powershell -ExecutionPolicy Bypass -File ".\script\c-drive-safe-cleanup.ps1"`
3. 在 `tasks/` 查看并归档日志：
   - `tasks/evaluation-<YYYY-MM-DD>-c-disk-cleanup.md`

## Screenshots

当前仓库尚未包含截图。建议补充以下 3 张图，便于他人快速理解：

- DryRun 扫描输出（含“预计可释放”与逐项确认）
- 正式清理完成页（含“总释放空间”）
- 日志文件示例（`tasks/` 下的 Markdown 报告）

## 贡献说明

- 提交前请先使用 `-DryRun` 自测，确认不会触碰白名单外路径
- 新增扫描目录时，必须同步更新 `skill.md` 与 `references/safety.md`
- 禁止引入自动删除下载/桌面大文件、注册表修改、系统核心目录清理

## 安全边界

- 不扫描全盘
- 不自动删除下载/桌面大文件
- 不修改注册表
- 不触碰系统核心目录（如 `C:\Windows\System32`、`C:\Windows\WinSxS`、`C:\Program Files`）
