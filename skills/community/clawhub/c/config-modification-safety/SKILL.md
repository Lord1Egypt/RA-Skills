---
name: config-modification-safety
description: >
  OpenClaw 配置安全守护。防止 AI 改坏配置文件的双层守护架构，支持 macOS 和 Windows。

  触发场景：AI 修改配置文件后系统崩溃、JSON 语法错误导致 Gateway 无法启动、想给 OpenClaw 配置安全网。

  核心功能：
  - 第一层（铜墙）：配置文件变更时自动校验 JSON，语法错误 1 秒内回滚
  - 第二层（铁壁）：每 5 分钟检查 Gateway 健康状态，崩溃自动恢复
  - 应急回滚：一行命令恢复到最后一次正常配置

  安装后用户获得：铜墙铁壁级别的配置保护，AI 改配置再也不怕搞崩系统了。
---

# config-modification-safety

OpenClaw 配置安全守护 — 给 AI 的配置修改加上双层保险。

## 🔐 这个 Skill 解决什么问题

AI 修改配置时可能犯错导致整个系统崩溃，而且 AI 自己无法修复（因为 Gateway 起不来了）。双层守护架构确保：
- JSON 语法错误 → **< 1 秒**自动回滚
- Gateway 崩溃 → **5~15 分钟**自动恢复
- 完全自动，**不需要人工介入**

## 🚀 快速安装

### macOS（苹果电脑）
```bash
bash ~/.openclaw/skills/config-modification-safety/scripts/install.sh
```
> 使用 macOS 原生 launchd WatchPaths，不需要安装任何额外依赖

### Windows（Windows 10/11）
1. 找到 `~/.openclaw/skills/config-modification-safety/windows/` 目录
2. 右键点击 `install.bat` → **以管理员身份运行**
> 使用 PowerShell FileSystemWatcher + Task Scheduler

## 📊 架构原理

| 层级 | macOS | Windows | 响应时间 | 防什么 |
|------|-------|---------|---------|--------|
| **铜墙（第一层）** | launchd WatchPaths | FileSystemWatcher | < 1 秒 | JSON 语法写错 |
| **铁壁（第二层）** | cron | Task Scheduler | 5~15 分钟 | 配置值错误崩溃 |

## 📋 常用命令

### macOS
```bash
# 手动回滚
python3 ~/.openclaw/workspace/.lib/config-safety/guard.py rollback

# 查看守护日志
tail -f ~/.openclaw/workspace/.lib/config-safety/guard.log

# 检查守护进程
launchctl list | grep config-guard

# 卸载
launchctl unload ~/Library/LaunchAgents/com.openclaw.config-guard.plist
crontab -e  # 删除 config-safety 那行
```

### Windows（命令提示符 / PowerShell）
```cmd
:: 手动回滚
python %USERPROFILE%\.openclaw\workspace\.lib\config-safety\guard.py rollback

:: 查看任务状态
schtasks /query /tn "OpenClaw"

:: 卸载
schtasks /delete /tn "OpenClaw Config Guard" /f
schtasks /delete /tn "OpenClaw Health Check" /f
```

## 🎯 什么时候会触发保护

**第一层（铜墙）触发：** AI 修改配置文件时 JSON 语法写错（多余逗号、引号、花括号），1 秒内自动回滚。

**第二层（铁壁）触发：** JSON 语法正确但值错误（不存在模型名等），导致 Gateway 崩溃，5~15 分钟后自动恢复。

## 🔧 工作目录

### macOS
```
~/.openclaw/workspace/.lib/config-safety/     # 守护脚本
~/.openclaw/config-backups/                  # 配置文件备份（最多 10 份）
```

### Windows
```
%USERPROFILE%\.openclaw\workspace\.lib\config-safety\   # 守护脚本
%USERPROFILE%\.openclaw\config-backups\                 # 配置文件备份
```

## ⚠️ 重要提示

- 备份最多保留 10 份，自动清理旧备份
- 回滚恢复到最近一次成功备份
- 系统完全崩溃时：macOS `guard.py rollback`，Windows `guard.py rollback` 即可 10 秒恢复

## 📤 分享到 ClawHub

打包 Skill：
```bash
python3 ~/.openclaw/skills/skill-creator/scripts/package_skill.py \
  ~/.openclaw/skills/config-modification-safety \
  ~/.openclaw/skills/config-modification-safety/dist
```

分享给其他用户后：
- **macOS 用户**：运行 `install.sh`
- **Windows 用户**：运行 `install.bat`（管理员）
- 门槛极低，体验极佳
