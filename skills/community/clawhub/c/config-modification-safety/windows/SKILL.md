---
name: config-modification-safety-windows
description: >
  OpenClaw 配置安全守护 — Windows 版。适用于 Windows 10/11 系统。

  触发场景：AI 修改配置文件后系统崩溃、JSON 语法错误导致 Gateway 无法启动。

  核心功能：
  - 第一层（铜墙）：FileSystemWatcher 监控配置目录，JSON 语法错误 1 秒内回滚
  - 第二层（铁壁）：Task Scheduler 每 5 分钟检查 Gateway 健康状态，崩溃自动恢复
  - 应急回滚：一行命令恢复到最后一次正常配置

  安装：Windows 用户双击 install.bat（管理员身份）即可完成。
---

# config-modification-safety (Windows 版)

OpenClaw 配置安全守护的 Windows 实现，使用 Windows Task Scheduler + PowerShell FileSystemWatcher。

## 快速安装

1. 解压 skill 包
2. 右键点击 `install.bat` → **以管理员身份运行**
3. 完成！两个守护任务已注册到任务计划程序

## 架构对比

| 层级 | macOS | Windows |
|------|-------|---------|
| **第一层** | launchd WatchPaths | PowerShell FileSystemWatcher（.NET） |
| **第二层** | cron（每 5 分钟） | Windows Task Scheduler（每 5 分钟） |
| **触发方式** | 文件变更自动触发 | 连续后台进程 + 定时巡检 |

## 工作原理

**第一层（铜墙）：**
- `config-guard.ps1` 使用 .NET `FileSystemWatcher` 实时监控配置目录
- 每次检测到变更 → 200ms 后校验 JSON → 错误立即回滚
- 以"登录时启动"任务运行，持续守护

**第二层（铁壁）：**
- `health-check.ps1` 每 5 分钟检查 Gateway `/health` 端点
- 不健康则执行回滚脚本并重启 Gateway

## 常用命令

```cmd
# 手动触发备份
python %USERPROFILE%\.openclaw\workspace\.lib\config-safety\guard.py backup

# 手动回滚
python %USERPROFILE%\.openclaw\workspace\.lib\config-safety\guard.py rollback

# 查看守护任务状态
schtasks /query /tn "OpenClaw"

# 卸载两个守护任务
schtasks /delete /tn "OpenClaw Config Guard" /f
schtasks /delete /tn "OpenClaw Health Check" /f
```

## 文件结构

```
%USERPROFILE%\.openclaw\workspace\.lib\config-safety\
├── guard.py              # 回滚核心脚本（Python，跨平台）
├── config-guard.ps1      # 第一层守护（FileSystemWatcher）
├── health-check.ps1      # 第二层守护（健康检查）
├── guard.log           # 第一层日志
└── health-check.log    # 第二层日志

%USERPROFILE%\.openclaw\config-backups\
├── agent-YYYYMMDD-HHMMSS.json   # 配置文件备份
```

## 注意事项

- 安装脚本需要**管理员权限**（用于注册 Task Scheduler 任务）
- 默认监控路径：`%USERPROFILE%\.openclaw\workspace\config\agent.json`
- 也监控主配置：`%USERPROFILE%\.openclaw\config.json`
- 备份最多保留 10 份，自动清理旧备份
