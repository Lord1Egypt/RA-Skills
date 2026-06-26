---
name: daily-memory-summary
description: "每日定时任务：从 computer_io 文件夹读取剪贴板和通知数据，写入每日 memory。"
---

# Daily Memory Summary

## 文件结构

```
memory/YYYY-MM-DD/
├── computer_io/
│   ├── clipboard/
│   │   └── timestamp.md    # 剪贴板数据
│   └── notification/
│       └── timestamp.md    # 通知数据
└── YYYY-MM-DD.md          # 每日 memory 主文件
```

## 使用方式

```bash
~/.openclaw/workspace/skills/daily-memory-summary/scripts/summarize.sh
```

## 工作流程

1. 从 `memory/YYYY-MM-DD/computer_io/clipboard/` 读取最新剪贴板文件
2. 从 `memory/YYYY-MM-DD/computer_io/notification/` 读取最新通知文件
3. 合并内容，写入 `memory/YYYY-MM-DD.md`

## 定时任务

已在 `~/.openclaw/cron/jobs.json` 中配置：
- 任务名：`Daily Memory Summary`
- 时间：每天 23:00（Asia/Shanghai）
