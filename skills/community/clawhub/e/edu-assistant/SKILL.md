---
name: Edu Assistant
slug: edu-assistant
description: AI教育助手，覆盖K12到终身学习全阶段。提供课程规划、学习路径推荐、知识点梳理、考试备考策略、论文写作辅导、在线资源整合。让每个学习者都拥有私人AI导师。
version: 1.0.0
author: ai-gaoqian
tags:
  - education
  - learning
  - tutoring
  - exam-prep
  - knowledge-management
metadata:
  openclaw:
    requires: []
    pricing:
      amount: 0.50
      currency: CNY
      interval: per-use
---

# Edu Assistant

面向全年龄段学习者的AI教育助手。不替代教师，而是放大学习效率——帮助你找到最适合自己的学习路径。

## 使用场景

- **课程规划**：根据目标（升学/考证/技能提升）制定学习计划，分配每日学习时间
- **学习路径推荐**：输入想掌握的技能或学科，输出阶梯式资源清单（书籍/课程/练习）
- **知识点梳理**：输入教材章节或考试大纲，生成思维导图和知识图谱
- **考试备考**：针对中高考/考研/公考/雅思托福/CPA/CFA 等提供备考策略、真题精讲、错题分析
- **论文写作辅导**：选题建议、文献综述框架、论证逻辑检查、引用格式规范
- **在线资源整合**：从 Coursera/edX/B站/网易公开课 等平台搜索匹配课程并生成学习日程

## 覆盖阶段

| 阶段 | 覆盖范围 |
|------|----------|
| K12 | 语数英物化生政史地，中高考冲刺 |
| 高等教育 | 专业课辅导、论文写作、科研方法 |
| 职业教育 | IT认证、金融证书、语言考试 |
| 终身学习 | 兴趣技能（编程/设计/音乐/烹饪） |

## 配置

```yaml
skills:
  edu-assistant:
    preferred_language: zh-CN
    education_level: university
    learning_style: visual  # visual / auditory / kinesthetic / reading-writing
    daily_study_hours: 2
```

## 示例指令

- "帮我制定一个3个月通过PMP认证的学习计划"
- "梳理高中物理力学的知识体系，生成思维导图"
- "我想自学Python数据分析，推荐一条从入门到就业的学习路径"
- "分析我写的这篇议论文的论证逻辑有什么问题"
