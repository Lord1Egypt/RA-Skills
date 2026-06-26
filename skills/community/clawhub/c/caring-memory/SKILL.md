# Caring Memory Skill

> 🧠 AI-powered task reminder system with Ebbinghaus forgetting curve + gamification + active time learning

## Overview

A smart task management system that:

- **Priority-based reminders**: urgent/high/medium/low with auto-upgrade near deadlines
- **Ebbinghaus curve**: reminds at 1h, 24h, 4d, 7d, 15d intervals
- **Gamification**: XP, levels, streaks, achievements
- **Active time learning**: tracks when you're most responsive

## Usage

### Add a task
```bash
python3 caring_memory.py add "Task title" [priority] [deadline]
# priority: urgent/high/medium/low
# deadline: ISO format e.g. "2026-04-10T18:00:00"
```

### Complete a task
```bash
python3 caring_memory.py complete <id>
```

### Cancel a task
```bash
python3 caring_memory.py cancel <id>
```

### List pending tasks
```bash
python3 caring_memory.py list
```

### Generate reminder summary (for cron)
```bash
python3 caring_memory.py remind
```

### View stats
```bash
python3 caring_memory.py stats
```

### Record chat activity
```bash
python3 caring_memory.py chat
```

## OpenClaw Integration

### Recommended Cron Setup

**Morning reminder (08:00)**:
```
Task: python3 skills/caring-memory-skill/caring_memory.py remind
Schedule: 0 8 * * *
```

**Midday check (12:00)**:
```
Task: python3 skills/caring-memory-skill/caring_memory.py remind
Schedule: 0 12 * * *
```

**Evening review (18:00+21:00)**:
```
Task: python3 skills/caring-memory-skill/caring_memory.py remind
Schedule: 0 18,21 * * *
```

### Agent Integration
- **Session start**: Call `chat` to record active time
- **User mentions tasks**: Auto-call `add`
- **User says "done"**: Call `complete`
- **Heartbeat check**: Call `remind` for summary

## Priority Auto-Upgrade

| Time to deadline | Upgrade |
|-----------------|---------|
| < 24h | high → urgent |
| < 48h | medium → high |
| < 96h | low → medium |

## Gamification

| Action | XP |
|--------|-----|
| Complete task | 10 × priority_multiplier |
| Daily streak | +5 bonus |
| Level up | Every 100 XP |

## Trigger Words

- "这很重要" → Add as high priority
- "记住这个" → Add task
- "完成了" / "搞定" → Complete task
- "待办" / "任务" → List tasks
