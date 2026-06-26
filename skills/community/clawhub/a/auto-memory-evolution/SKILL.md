---
name: auto-memory-evolution
description: Automatically summarize daily discussions and update memory files. This skill should be used when users want to automatically organize conversation notes into memory files.
---

# Auto Memory Evolution

Automatically summarize daily discussions and archive to memory files.

## When to Use

Use this skill when:
- User wants automatic daily discussion summary
- User needs memory files automatically updated
- User wants idle-triggered memory save

## How It Works

### 1. Daily Evolution Script

Run daily-evolution.py to:
- Read memory files from `~/.openclaw/workspace/memory/`
- Extract discussion topics from markdown files
- Write summaries to `~/.openclaw/workspace/MEMORY.md`

### 2. Heartbeat Check Script

Run heartbeat-check.py to:
- Check user activity every 30 minutes
- Track last message timestamp
- Trigger auto-save after 45 minutes of idle

## Installation

1. Copy skill to `~/.openclaw/skills/auto-memory-evolution/`

2. Set up cron jobs:

```bash
# Daily evolution at 22:00
0 22 * * * python3 ~/.openclaw/skills/auto-memory-evolution/scripts/daily-evolution.py

# Heartbeat every 30 minutes
*/30 * * * * python3 ~/.openclaw/skills/auto-memory-evolution/scripts/heartbeat-check.py
```

## File Structure

```
auto-memory-evolution/
├── SKILL.md
├── scripts/
│   ├── daily-evolution.py
│   └── heartbeat-check.py
└── config.json (optional)
```

## Dependencies

- Python 3.7+
- OpenClaw CLI (for session history)

## Configuration

Edit config.json to customize:

```json
{
  "idle_threshold_minutes": 45,
  "memory_dir": "~/.openclaw/workspace/memory",
  "longterm_memory": "~/.openclaw/workspace/MEMORY.md"
}
```

---

# 自动记忆进化

自动归纳每天讨论内容并归档到记忆文件。

## 何时使用

使用此 Skill 当用户希望：
- 自动每日总结讨论内容
- 自动更新记忆文件
- 空闲时自动保存记忆

## 工作原理

### 1. 每日进化脚本

运行 daily-evolution.py 以：
- 读取 `~/.openclaw/workspace/memory/` 下的记忆文件
- 从 markdown 文件中提取讨论话题
- 将摘要写入 `~/.openclaw/workspace/MEMORY.md`

### 2. 心跳检查脚本

运行 heartbeat-check.py 以：
- 每30分钟检查用户活动
- 记录最后消息时间戳
- 空闲45分钟后触发自动保存

## 安装

1. 将 Skill 复制到 `~/.openclaw/skills/auto-memory-evolution/`

2. 设置定时任务：

```bash
# 每日22:00进化
0 22 * * * python3 ~/.openclaw/skills/auto-memory-evolution/scripts/daily-evolution.py

# 心跳每30分钟
*/30 * * * * python3 ~/.openclaw/skills/auto-memory-evolution/scripts/heartbeat-check.py
```

## 文件结构

```
auto-memory-evolution/
├── SKILL.md
├── scripts/
│   ├── daily-evolution.py
│   └── heartbeat-check.py
└── config.json (可选)
```

## 依赖

- Python 3.7+
- OpenClaw CLI（用于获取会话历史）

## 配置

编辑 config.json 自定义：

```json
{
  "idle_threshold_minutes": 45,
  "memory_dir": "~/.openclaw/workspace/memory",
  "longterm_memory": "~/.openclaw/workspace/MEMORY.md"
}
```
