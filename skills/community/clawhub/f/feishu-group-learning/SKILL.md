---
name: feishu-group-learning
description: |
  自动分析飞书群消息，提取学习点和进化建议。
  每6小时自动运行，支持多群监控、关键词提取、学习建议生成。
metadata:
  version: "1.0.0"
  author: "Vita虾助理"
  tags: ["feishu", "learning", "analysis", "automation"]
---

# Feishu Group Learning

自动分析飞书群消息，提取有价值的学习点。

## 功能

- 多群消息监控
- 自动语义分析
- 学习建议生成
- 定时报告推送

## 安装

```bash
clawhub install feishu-group-learning
```

## 配置

编辑 `~/.openclaw/workspace/skills/feishu-group-learning/config.json`:

```json
{
  "chats": [
    {"id": "oc_xxx", "name": "群名称"}
  ],
  "schedule": "0 */6 * * *"
}
```

## 使用

```bash
# 手动运行分析
bash ~/.openclaw/workspace/skills/feishu-group-learning/analyze.sh
```
