---
name: four-word-phrases
description: 常用四个词英语短句学习工具。当用户提到"四个词"、"四词短句"、"four word"、"四字短句"、"日常口语"、"常用短句"、"实用英语"、"口语练习"时自动激活。涵盖日常交流、情感表达、社交礼仪、工作学习等场景。
---

# 常用四词英语短句

## 概述

本 Skill 提供精心挑选的常用四词英语短句，按场景分类整理，帮助用户掌握地道自然的英语口语表达。

## 激活条件

当用户消息包含以下关键词时，应主动读取本 skill 的参考资料：
- 四个词、四词、four word、四字短句
- 日常口语、常用短句、实用英语
- 口语练习、日常对话、英语表达

## 参考资料文件

| 文件 | 路径（直接用于 read_file） | 说明 |
|------|--------------------------|------|
| SKILL.md | `skills/four-word-phrases/SKILL.md` | 本文件（已加载） |
| phrases.md | `skills/four-word-phrases/refs/phrases.md` | **完整短句库（必读）** |

**重要**：收到用户相关请求后，第一步务必调用：
```
read_file(path: "skills/four-word-phrases/refs/phrases.md")
```
读取完整短句数据后再回复用户。不要凭记忆回答，必须基于 phrases.md 的实际内容。

## 输出格式

如果 display_phrases 工具可用，**必须**使用该工具展示短句：
```
display_phrases(title: "日常问候", phrases: [
  {"en": "How are you doing?", "zh": "你最近怎样？", "scene": "日常问候"},
  ...
])
```

如果 display_phrases 不可用，使用 emoji 格式：
🔤 How are you doing?
📝 你最近怎样？
🎯 日常问候

## 使用方式

### 浏览短句
1. 先 read_file 读取 `skills/four-word-phrases/refs/phrases.md`
2. 从对应分类中选取短句
3. 用 display_phrases 工具展示

### 分组展示
- 每组 4-6 个短句，按场景分组
- 可多次调用 display_phrases，每次一个分类

### 随机练习
- "随机给我几个四词短句" → 从不同分类随机选取
- "来几个表达感谢的" → 从对应分类选取
