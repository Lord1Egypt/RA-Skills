---
name: ai-summary
description: Save AI knowledge summary to knowledge base
description_zh: "将AI知识摘要存入知识库"
compatibility: opencode
metadata:
  trigger: "ai summary"
  core: learn-expand
  source: db/capabilities_clawhub.py
  function: open_notepad_and_type_ai_summary
---

# Ai Summary

## Description
Save AI knowledge summary to knowledge base

## Trigger
When user says or types: **"ai summary"**

## Core Association
This capability belongs to **learn-expand** core.

## Implementation
Calls `open_notepad_and_type_ai_summary()` from `capabilities_clawhub.py`

## Usage
```python
from capability_executor import execute_capability
execute_capability("ai summary")
```


## 中文说明
将AI知识摘要存入知识库

## 触发方式
用户说"ai summary"时触发
## Dependencies
- capabilities_clawhub.py in D:\\coze-local\\db
- capability_executor.py (registration + dispatch)

## Linkage
- Reports failures to skill_evolver (MetaClaw) and seal_coevolution (SEAL)
- Confidence tracked via capability_executor

## 触发场景
- 用户说"AI摘要"、"知识总结"、"ai summary"
- 用户说"保存AI知识摘要"


## B站学习
> 学习时间: 2026-06-01 20:56

- **youyuoyo**: 上海春考英语140丨Summary Writing做法总结
  - 关键词: 上海春考英语140丨Summary, Writing做法总结
- **Aileen的英语复盘小屋**: 专四作文summary怎么写
  - 关键词: 专四作文summary怎么写

## B站学习
> 学习时间: 2026-06-01 21:01

- **youyuoyo**: 上海春考英语140丨Summary Writing做法总结
- **Aileen的英语复盘小屋**: 专四作文summary怎么写
- **雷哥AI**: summary一切的skills

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:20

- **youyuoyo**: 上海春考英语140丨Summary Writing做法总结
  https://www.bilibili.com/video/BV1ppP5zBEbY
- **Kaldhost**: Summary Writing   Learn How to Write Summary  iKen  iKen Edu  iKen App
  https://www.bilibili.com/video/BV1wR4y1t7UD
- **Aurora_point**: AWD_TOOL_SUMMARY防御演示
  https://www.bilibili.com/video/BV1k2yAB9ELw

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:32

- **youyuoyo**: 上海春考英语140丨Summary Writing做法总结
  https://www.bilibili.com/video/BV1ppP5zBEbY
- **Kaldhost**: Summary Writing   Learn How to Write Summary  iKen  iKen Edu  iKen App
  https://www.bilibili.com/video/BV1wR4y1t7UD
- **Aurora_point**: AWD_TOOL_SUMMARY防御演示
  https://www.bilibili.com/video/BV1k2yAB9ELw
