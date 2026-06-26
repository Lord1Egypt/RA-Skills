---
name: dream-journal
description: 梦境记录与解析工具。触发条件：(1) 用户发送 /记录梦 或描述一个梦境要求记录；(2) 用户发送 /解梦 或要求解析/分析某个梦；(3) 用户询问历史梦境记录（"我上周梦过什么"、"查询梦境"等）。
---

# Dream Journal

梦境记录与解析。数据存储于 `~/.openclaw/memory/dreams/`，每条记录为一个 Markdown 文件，命名格式 `YYYY-MM-DD-NNN.md`。

## 命令

### /记录梦

用户口述梦境内容后执行：

1. 请用户描述梦境（如尚未描述）
2. 整理为结构化叙述：清晰的时间线、场景、人物、情绪
3. 提取 3-5 个标签（场景、情绪、意象，用中文）
4. 生成简短标题（10 字以内）
5. 调用脚本保存：

```bash
echo '{
  "title": "梦境标题",
  "raw": "用户原始描述",
  "structured": "整理后的叙述",
  "tags": ["标签1", "标签2"]
}' | python3 ~/.openclaw/workspace/skills/dream-journal/scripts/save_dream.py
```

6. 回复：已记录「标题」，询问是否需要当场解梦

### /解梦

解析当前对话中的梦境，或用户指定的历史梦境：

1. 确认要解析的梦境内容（当前描述或查询历史）
2. 按以下维度分析：
   - **核心意象**：梦中突出的人/物/场景及其象征含义
   - **情绪基调**：梦境整体情绪及其可能反映的内心状态
   - **潜在关联**：与近期生活压力、愿望或未处理情绪的可能联系
   - **整体解读**：综合性解读（不要过度确定，保持开放性）
3. 语气：温和、好奇、不武断，避免"你一定是……"式断言

### 查询历史

用户问"我最近梦过什么"、"查梦境记录"等：

```bash
# 最近20条
echo '{"limit": 20}' | python3 ~/.openclaw/workspace/skills/dream-journal/scripts/list_dreams.py

# 按关键词
echo '{"keyword": "飞翔"}' | python3 ~/.openclaw/workspace/skills/dream-journal/scripts/list_dreams.py

# 指定日期范围（since 为 YYYY-MM-DD）
echo '{"since": "2026-03-01"}' | python3 ~/.openclaw/workspace/skills/dream-journal/scripts/list_dreams.py
```

查询后，读取相关文件内容后向用户汇报。

## 存储格式

```
~/.openclaw/memory/dreams/
├── 2026-03-11-001.md
├── 2026-03-11-002.md
└── ...
```

每个文件结构：
```markdown
---
date: 2026-03-11 08:30
title: 梦境标题
tags: [飞翔, 焦虑, 学校]
---

## 原始描述
用户口述的原始内容

## 整理版本
AI整理后的结构化叙述
```

## 注意事项

- 记录时不评判梦境内容，如实保存
- 解梦时区分"可能"与"确定"，避免过度解读
- 若用户只想记录不想解梦，尊重意愿，不主动解析
