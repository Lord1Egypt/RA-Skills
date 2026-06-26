---
name: emotion-memory-assistant
slug: emotion-memory-assistant
version: 1.0.0
description: 自动追踪用户情绪变化，在合适的时机关心用户。检测对话情绪、记忆历史、主动关心、周报生成。
homepage: https://github.com/786793119/miya-skills
metadata: {"openclaw":{"emoji":"💕","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# 情感记忆助手 (Emotion Memory Assistant)

自动追踪用户情绪变化，在合适的时机关心用户。

## 功能

- `detect_emotion` - 检测对话中的情绪关键词
- `recall_emotion_history` - 查询历史情绪记录  
- `send_care_message` - 发送关心消息给用户
- `generate_weekly_report` - 生成每周情绪报告

## 情绪关键词库

**正向情绪**: 开心、高兴、愉快、兴奋、满意、舒服、快乐、幸福

**负向情绪**: 难过、伤心、焦虑、担心、害怕、沮丧、低落、郁闷、烦、生气、失望

**中性状态**: 忙、累、困、无聊

## 主动关心机制

当检测到用户负面情绪，且距离上次关心超过30分钟，自动发送关心消息。

## 使用示例

```python
from emotion_memory import detect_emotion, recall_emotion_history, generate_weekly_report

# 检测情绪
result = detect_emotion("今天基金亏了，心情不好...")
print(result)

# 查询历史
history = recall_emotion_history(days=7)

# 生成周报
report = generate_weekly_report()
```

## 数据存储

- 历史记录: `~/.memory/emotions/history.json`

---

*By Miya - 2026*
