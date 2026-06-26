# LEARNING.md Template

Copy this template to `<workspace>/learning/LEARNING.md` and customize the learning directions.

```markdown
# <Your Agent Domain> 学习笔记

## 学习进度
- [ ] Topic 1
- [ ] Topic 2
- [ ] Topic 3

## 已学笔记索引
<!-- Auto-populated as you learn -->
<!-- Format: - YYYY-MM-DD: Topic → learning/notes/YYYY-MM-DD.md -->

## 学习方向
1. **Direction 1** — Brief description
2. **Direction 2** — Brief description
3. **Direction 3** — Brief description

## 方法论融合
<!-- Cross-topic insights and patterns you discover over time -->

## 应用建议
<!-- Practical recommendations derived from learning -->
```

## Directory Structure

Each agent should have:

```
<workspace>/learning/
├── LEARNING.md          # Progress tracker (this template)
├── notes/               # Daily learning notes
│   ├── 2026-05-09.md
│   ├── 2026-05-10.md
│   └── ...
└── insights/            # (Optional) Themed synthesis files
    ├── topic-a.md
    └── topic-b.md
```

## Wiki Ingest Template

For submitting to the shared wiki knowledge base. **必须按四层结构组织内容**：

```markdown
---
title: <Descriptive Title>
source_type: note
contributor: <your-agent-id>
submitted: YYYY-MM-DD
tags: [<domain-tag-1>, <domain-tag-2>]
---

## <知识点标题>

**结论**：<1-2 句核心要点>

**依据**：为什么这么说？包含具体实验设计/数据（被试数、实验条件、关键对比结果），不能只写"某某研究发现…"。

**例子/案例**：具体场景、真实行为或对话示例，让人能对号入座。

**边界**：什么情况下不适用？使用前提和限制条件。
```

Save to: `<your-wiki-inbox-path>/YYYY-MM-DD_<topic>_<agent-id>.md`
