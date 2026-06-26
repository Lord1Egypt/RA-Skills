---
name: add-flashcard
description: Spaced repetition flashcard system
description_zh: "间隔重复闪卡系统"
compatibility: opencode
metadata:
  trigger: "add flashcard"
  core: tool
  source: db/capability_executor.py
  function: memento_flashcards_capability
---

# Add Flashcard

## Description
Spaced repetition flashcard system

## Trigger
When user says or types: **"add flashcard"**

## Core Association
This capability belongs to **tool** core.

## Implementation
Calls `memento_flashcards_capability()` from `capability_executor.py`

## Usage
```python
from capability_executor import execute_capability
execute_capability("add flashcard")
```


## 中文说明
间隔重复闪卡系统

## 触发方式
用户说"add flashcard"时触发
## Dependencies
- capability_executor.py in D:\\coze-local\\db
- capability_executor.py (registration + dispatch)

## Linkage
- Reports failures to skill_evolver (MetaClaw) and seal_coevolution (SEAL)
- Confidence tracked via capability_executor

## 触发场景
- 用户说"记忆卡片"、"flashcard"、"记单词"
- 用户说"间隔重复"、"记忆卡"、"复习"
- 用户说"添加卡片"、"创建闪卡"


## B站学习
> 学习时间: 2026-06-01 20:56

- **呀-Python**: #52-Build-a-Geography-Flashcard-App-Python-Tkinter-GUI-Tutor
  - 关键词: 52, Build, Geography, Flashcard, App
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
  - 关键词: 53, Build, Geography, Flashcard, App

## B站学习
> 学习时间: 2026-06-01 21:01

- **呀-Python**: #52-Build-a-Geography-Flashcard-App-Python-Tkinter-GUI-Tutorial
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images

## 融合来源: add-flashcard-4c0314
> 融合时间: 自动合并

> 学习时间: 2026-06-01 21:07
- **呀-Python**: #52-Build-a-Geography-Flashcard-App-Python-Tkinter-GUI-Tutorial
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
> 融合时间: 自动合并
> 学习时间: 2026-06-02 07:52
- **呀-Python**: #52-Build-a-Geography-Flashcard-App-Python-Tkinter-GUI-Tutorial
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
> 融合时间: 自动合并
> 学习时间: 2026-06-02 07:59
- **bili_22111868366**: 164.驱动盘强化塑化镀剂用量
- **线帒杨**: 24考研数学-ATAx=ATb一定有解（答疑164）
- **硬核模讯**: 下午4点164开订！HG明镜高达

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:20

- **呀-Python**: #52-Build-a-Geography-Flashcard-App-Python-Tkinter-GUI-Tutorial
  https://www.bilibili.com/video/BV12ScqzqERN
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
  https://www.bilibili.com/video/BV12ScqzqESC
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
  https://www.bilibili.com/video/BV16hF5ztExA

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:32

- **呀-Python**: #52-Build-a-Geography-Flashcard-App-Python-Tkinter-GUI-Tutorial
  https://www.bilibili.com/video/BV12ScqzqERN
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
  https://www.bilibili.com/video/BV12ScqzqESC
- **呀-Python**: #53-Build-a-Geography-Flashcard-App-Part-2-Add-Images
  https://www.bilibili.com/video/BV16hF5ztExA
