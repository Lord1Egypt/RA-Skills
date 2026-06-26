---
name: agent-security-questions
description: 工作问题收集与分析Skill - 收集AI Agent工作过程中的问题，分析风险，转化为研究课题
metadata:
  openclaw:
    emoji: ❓
    version: 1.0.0

# ❓ agent-security-questions

> 工作问题收集与分析Skill

## 功能

1. **问题收集** - 收集工作过程中的问题
2. **分类分析** - 分析问题类型和风险
3. **研究转化** - 将问题转化为研究课题
4. **知识沉淀** - 沉淀为知识库

## 问题类型

| 类型 | 说明 |
|------|------|
| 工作问题 | Agent工作过程中的问题 |
| 安全风险 | 安全相关风险 |
| 机制问题 | 智能体机制问题 |
| 产出问题 | 产出质量问题 |
| 沟通问题 | 人机协作问题 |

## 使用

```bash
./src/questions.sh add "问题描述"
./src/questions.sh list
./src/questions.sh analyze
```

