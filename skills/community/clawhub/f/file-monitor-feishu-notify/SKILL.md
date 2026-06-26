---
name: file-monitor-feishu-notify
version: 1.0.0
description: 文件监控并自动通知到飞书群
metadata:
  short-description: 监控目录，新文件自动发送飞书通知
  tags: ["file", "monitor", "feishu", "notification", "automation"]
source:
  repository: https://github.com/YOUR_USERNAME/file-monitor-feishu-notify
  license: MIT
---

# File Monitor Feishu Notify Skill

## Description
监控指定目录的文件变化，新文件自动发送到飞书群聊。

## Trigger
- 文件监控自动触发
- HEARTBEAT 守护进程运行

## Usage

### 安装
```powershell
# 已本地安装，无需额外操作
```

### 配置
编辑 `config.json`：
```json
{
  "watch_dir": "D:\\云文档同步",
  "notify_file": ".data/.pending_notify.md",
  "feishu": {
    "app_id": "cli_xxx",
    "app_secret": "xxx",
    "chat_id": "oc_xxx"
  },
  "check_interval": 2,
  "log_file": "logs/auto-send.log"
}
```

### 启动
```powershell
# HEARTBEAT 会自动启动，或手动运行：
powershell -ExecutionPolicy Bypass -File "skills/file-monitor-feishu-notify/start-monitor.ps1"
```

## Files
- `scripts/simple-monitor.py` - 文件监控器
- `scripts/auto-send.py` - 自动发送器
- `start-monitor.ps1` - 启动脚本
- `config.json` - 配置文件
- `logs/auto-send.log` - 日志文件

## Tags
`file`, `monitor`, `feishu`, `notification`, `automation`

## Compatibility
- OpenClaw: ✅
- HEARTBEAT: ✅
- Windows: ✅
