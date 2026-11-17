---
name: resume-optimizer
description: 简历 ATS 优化器 — 检测简历关键词匹配度、格式兼容性，提升通过筛选的概率
source:
  type: derived
  repo: skills-repo/career-coach
  path: skills/resume-optimizer/SKILL.md
  url: https://skills.sh/paramchoudhary/resumeskills/resume-ats-optimizer
  version: 1.0.0
  updated: 2026-07-29
metadata:
  author: hope
  category: 简历优化
  platform: 通用
  difficulty: 入门
  version: 1.0.0
  created: 2026-07-29
tags:
  - resume
  - ats
  - job-search
  - career
---

# Resume Optimizer — 简历 ATS 优化器

> 75% 的简历在到达面试官前被 ATS 系统过滤。本技能帮你检查关键词匹配、格式兼容、综合匹配分。

## 能力

- 解析简历文件，检测 ATS（Applicant Tracking System）兼容性
- 对照岗位描述提取关键词，计算匹配度分数
- 识别格式问题：表格、特殊字符、图片、非标准字体
- 建议关键词补充位置和用词优化
- 推荐 ATS 友好的格式调整方案

## 使用方式

```
/resume-optimizer 对比这份简历和 JD
/resume-optimizer 检查我的简历 ATS 兼容性
/resume-optimizer 这个岗位需要什么关键词
```

## 工作流

1. **获取输入** — 用户提供简历文件（PDF/DOCX）和目标岗位描述
2. **格式检查** — 扫描文件格式、字体、排版，标记 ATS 不兼容项
3. **关键词提取** — 从 JD 提取核心技能词和经验词
4. **匹配分析** — 对比简历关键词与 JD 关键词，输出匹配分
5. **改进建议** — 按优先级输出：格式修复 → 关键词补充 → 表达优化

## ATS 兼容快速清单

- 使用 .docx 或 .pdf（非扫描图片）
- 标准字体：Arial, Calibri, Georgia（10-12pt）
- 禁止表格、文本框、分栏布局
- 禁止页眉/页脚中的关键信息
- 使用标准章节标题："Professional Experience" / "Education" / "Skills"
- 文件名：FirstName_LastName_Resume.pdf

## 适用场景

- 投递多份简历无回音，怀疑被 ATS 过滤
- 新岗位投递前，想针对性优化关键词
- 简历格式更改后验证兼容性
- 从非英文岗位转换到英文岗位时的简历适配

## 相关参考（Playbook）

本技能是 L3 细粒度落地动作（ATS 检测），配套方法论见：

- [references/resume-crafting.md](../../references/resume-crafting.md) — 简历撰写方法论（读者模型 / JD 反向工程）
- [references/ats-optimization.md](../../references/ats-optimization.md) — ATS 解析层 + 检索层 + 关键词策略

## 限制

- ATS 系统种类繁多（Workday, Greenhouse, Lever 等），各系统解析规则有差异
- 关键词匹配分仅供参考，不等于通过概率
- 不保证通过所有 ATS 系统
- 不提供虚假经历或夸大内容的建议
