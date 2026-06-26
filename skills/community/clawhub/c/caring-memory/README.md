# 🧠 Caring Memory - AI智能任务提醒系统

> 基于艾宾浩斯遗忘曲线 + 游戏化 + 活跃时间学习的智能任务管理

## ✨ 特性

- **智能提醒**: 按优先级 + 艾宾浩斯曲线自动提醒（1h→24h→4d→7d→15d）
- **优先级自动升级**: 接近截止日自动提升优先级
- **游戏化激励**: XP/等级/连续完成奖励
- **活跃时间学习**: 追踪你最活跃的时间段，智能推送
- **OpenClaw集成**: 支持Cron定时提醒 + Agent对话触发

## 🚀 快速开始

```bash
# 添加任务
python3 caring_memory.py add "完成项目文档" high "2026-04-10T18:00:00"

# 查看待办
python3 caring_memory.py list

# 完成任务
python3 caring_memory.py complete 1

# 生成提醒摘要
python3 caring_memory.py remind
```

## 📋 推荐Cron配置

| 时间 | 命令 | 说明 |
|------|------|------|
| 08:00 | `python3 caring_memory.py remind` | 早安提醒 |
| 12:00 | `python3 caring_memory.py remind` | 午间提醒 |
| 18:00 | `python3 caring_memory.py remind` | 晚间提醒 |

## 🎮 游戏化

| 行为 | 奖励 |
|------|------|
| 完成任务 | 10×优先级倍率 XP |
| 每日连续 | +5 XP 奖励 |
| 升级 | 每100 XP |

## 📄 License

MIT
