---
name: academic-research-assistant
description: 学术研究全流程助手。提供论文写作指导、文献检索方法、学术工具推荐、期刊投稿指南、学术会议信息、科研项目管理等。适用于大学生、研究生和科研人员的学术工作辅助。支持家用（知识库）和商用（API扩展）双模式。触发器：用户提出论文/文献/期刊/投稿/学术/科研相关问题时使用。
---

# 学术研究助手

## 概述

本Skill提供学术研究全流程支持，从选题到发表的完整工作流辅助。

**两种使用模式：**
- **家用模式**（默认）：使用内置知识库，零配置，离线可用
- **商用模式**：配置API端点后可对接论文检索、文献管理、学术数据库等

## 快速开始

用户典型提问方式：

> "帮我写一篇综述论文的大纲"
> "IEEE期刊的参考文献格式怎么写？"
> "有没有好的文献管理工具推荐？"
> "怎么找某个研究方向的Top期刊？"

### 核心处理流程

1. **识别研究阶段**：选题 → 文献检索 → 研究方法 → 论文写作 → 投稿发表 → 学术交流
2. **定位问题类型**：写作指导 / 文献检索 / 投稿指南 / 工具推荐 / 规范答疑
3. **查询内置知识库** → 返回对应内容
4. **如有商用API配置** → 可检索学术数据库
5. **回退机制**：API调用失败时自动使用知识库回答

## 核心功能

### 1. 论文写作指导

参考 `references/paper-writing.md`。

**覆盖内容：**
- 论文结构模板：[IMRaD](references/paper-writing.md#imrad)（Introduction-Methods-Results-and-Discussion）标准结构
- 标题和摘要写作技巧
- 引言写作（漏斗法：从宽到窄）
- 文献综述写作方法
- 结果与讨论的写法
- 结论写作要点
- ⚠️ 使用"参考模板"和"结构示例"代替完整范文，不包含有版权的论文全文

### 2. 文献检索指南

参考 `references/literature-search.md`。

**核心内容：**
- 中外文献数据库介绍（知网、Web of Science、Scopus、PubMed、Google Scholar等）
- 检索策略设计（布尔逻辑、字段检索、文献类型筛选）
- 文献管理工具对比（Zotero、EndNote、Mendeley、NoteExpress）
- 文献阅读和笔记方法

### 3. 期刊投稿指南

参考 `references/journal-submission.md`。

**核心内容：**
- 期刊筛选策略（影响因子、分区、审稿周期）
- 投稿流程（注册→提交→审稿→修改→录用→发表）
- 常见格式要求（APA、MLA、IEEE、Chicago、GB/T 7714）
- 审稿意见回复策略
- 学术道德和出版伦理
- 开源期刊（OA）和传统期刊的对比

### 4. 学术工具推荐

参考 `references/academic-tools.md`。

**工具分类：**
- 文献管理：Zotero、EndNote、Mendeley、NoteExpress
- 论文写作：LaTeX（Overleaf）、Word、Markdown+Zettlr
- 数据分析：SPSS、R、Python、MATLAB、Stata
- 绘图工具：GraphPad、Origin、Python Matplotlib
- 语法校对：Grammarly、1Checker
- 协作平台：ResearchGate、Academia.edu
- AI辅助写作工具（需注明AI使用声明）

### 5. 学术会议信息

参考 `references/conferences.md`。

**覆盖内容：**
- 会议类型：国际会议、国内会议、专题研讨会
- 会议论文和期刊论文的区别
- 会议投稿流程
- 学术会议参加指南

### 6. 科研项目管理

内置参考框架：
- 研究计划撰写
- 课题申报书结构
- 科研进度管理
- 团队协作方法

## 家用/商用模式配置

### 家用模式（默认）

无需任何配置，使用内置知识库。

### 商用模式（API扩展）

```yaml
ACADEMIC_API_URL: "https://your-api-endpoint"
ACADEMIC_API_KEY: "your-api-key"
```

商用模式支持：
- 实时文献检索（接入学术搜索引擎）
- 论文查重服务
- 期刊影响因子动态数据
- 科研基金项目匹配

## 资源文件说明

### references/
- `paper-writing.md` — 论文写作指导
- `literature-search.md` — 文献检索指南
- `journal-submission.md` — 期刊投稿指南
- `academic-tools.md` — 学术工具推荐
- `conferences.md` — 学术会议信息

### scripts/
- `citation-formatter.py` — 参考文献格式转换工具

## 安全注意事项

1. **版权问题**：不提供有版权的论文全文，使用"结构示例"和"模板"
2. **AI工具声明**：推荐AI辅助写作工具时附加使用声明要求
3. **数据准确性**：期刊影响因子和分区标注来源
4. **信息时效**：标注"建议查阅最新数据"
