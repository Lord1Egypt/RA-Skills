---
name: desktop-notify
description: >-
  跨平台桌面通知助手：任务完成后播放提示音 + 弹出系统气泡（Windows Toast / macOS 通知中心 / Linux notify-send）。
  当用户希望在一次较长任务结束、或某个后台/长时间任务完成时收到"声音+视觉"提醒时使用。
  支持参数自定义标题与内容。Windows 用 WinRT Toast，macOS 用 osascript，Linux 用 notify-send（缺失时降级为终端响铃）。
---

# Desktop Notify — 跨平台任务完成通知

## 它能做什么

- 播放系统提示音（Windows 用 Asterisk 完成音，Linux 降级为终端响铃）
- 弹出操作系统原生通知气泡，几秒后自动消失
- 不依赖任何第三方软件，纯系统 API

## 何时用

- 你（或用户）在跑一个耗时任务，想"做完叫我一声"
- 长报告/大文件生成完毕，需要明确的可视提醒
- 后台脚本执行结束后的回调通知

## 用法（按系统选脚本）

### Windows
```powershell
PowerShell -File "<skill_dir>/scripts/notify.ps1" -Message "报告已生成" -Title "WorkBuddy"
```
不传参时默认：`标题=WorkBuddy`，`内容=任务完成，请查看`。

### macOS / Linux
```bash
bash "<skill_dir>/scripts/notify.sh" "报告已生成" "WorkBuddy"
```
参数顺序：`$1`=内容，`$2`=标题。macOS 用 `osascript`，Linux 用 `notify-send`；Linux 若没装 notify-send，自动降级为终端响铃 + 打印。

## 一键开启"全局自动通知"（推荐）

装完 skill 跑一次 setup，就把"每次回答完自动发通知"规则写进你自己的用户级全局记忆（`~/.workbuddy/MEMORY.md`），**之后所有项目、所有对话都自动生效**，不用每次手动说指令。脚本幂等，重复运行不会重复写。

### Windows
```powershell
PowerShell -File "<skill_dir>/scripts/setup.ps1"
```

### macOS / Linux
```bash
bash "<skill_dir>/scripts/setup.sh"
```

运行后新开对话即生效。想关掉：删除 `~/.workbuddy/MEMORY.md` 里 `<!-- desktop-notify-auto -->` 标记下那段规则即可。

## 重要边界（发布前必读）

1. **全局生效靠 setup，不是 skill 自动改配置。** WorkBuddy 出于安全，skill 安装时**不能**擅自改用户全局配置。所以"默认全局"由 setup 脚本实现——用户主动跑一次，把规则写进他**自己**的全局记忆。这是能做到全局自动的唯一合规方式。
2. **平台差异。** Windows 走 WinRT Toast；macOS/Linux 走各自原生接口。脚本已做 OS 检测与降级，无需用户手动判断。
3. **UTF-8 BOM。** `.ps1` 必须存为 UTF-8 带 BOM，否则 Windows PowerShell 5.1 按 GBK 读取会中文乱码、解析报错。本 skill 脚本已处理。
4. **无网络、无文件读取（除写自己的 MEMORY.md）、无外部依赖**——安全、可离线运行。

## 发布到平台（SkillHub / LobeHub 等）

本地已可直接用。要上公开平台，按目标平台流程提交：
1. 把本目录（含 SKILL.md + scripts/）作为仓库根或子目录；
2. 在对应平台后台 / 仓库 PR 提交，填写名称、分类（建议：Productivity / 系统工具）、简介与标签；
3. 说明里务必写明"跨平台 + 一键 setup 开启全局自动通知"，引导用户装完先跑 setup。

## 文件清单
- `SKILL.md`（本文件）
- `scripts/notify.ps1` — Windows 通知（UTF-8 BOM）
- `scripts/notify.sh` — macOS / Linux 通知
- `scripts/setup.ps1` — Windows 一键全局配置（UTF-8 BOM）
- `scripts/setup.sh` — macOS / Linux 一键全局配置
