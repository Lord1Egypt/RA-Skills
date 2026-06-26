---
name: clawhub-skill-search
description: "Use this skill when users need help finding, discovering, or selecting OpenClaw skills from the Clawhub marketplace. Triggers include: '哪个技能适合', '怎么找到', '技能搜索', 'skill search', 'how to find skill', or any request about navigating the 238+ skill ecosystem. Helps users match their tasks to appropriate skills and understand skill capabilities."
license: Apache 2.0
---

# Clawhub 技能搜索指南 🔍

**在 238+ 个 OpenClaw 技能中快速定位所需工具**

---

## 技能目标

帮助用户：
1. **发现技能** - 根据任务需求找到合适的技能
2. **理解技能** - 了解技能的功能和使用场景
3. **使用技能** - 掌握技能的调用方法和最佳实践
4. **解决问题** - 排查技能使用中的常见问题

---

## 触发条件

### 明确触发

用户直接询问技能相关话题：
- "哪个技能适合做 X？"
- "怎么搜索文献的技能？"
- "OpenClaw 有哪些数据分析技能？"
- "skill search for literature review"
- "how to find the right skill for..."

### 隐式触发

用户描述任务但未指定技能：
- "帮我找一些关于主观幸福感的论文" → 推荐 citation-management
- "分析一下这个数据" → 推荐 statistical-analysis
- "润色这段文字" → 推荐 academic-writing

---

## 核心功能

### 1. 技能推荐引擎

根据用户任务匹配技能：

```
输入："我想搜索关于 AI 和心理学的论文"
↓
匹配过程：
1. 识别任务类型：文献搜索
2. 识别研究领域：AI、心理学
3. 识别输出需求：论文列表、引用
↓
推荐技能：citation-management (优先级 1)
         academic-research-hub (优先级 2)
```

### 2. 技能对比分析

当多个技能都适用时，提供对比：

| 技能 | 适用场景 | 优势 | 限制 |
|------|---------|------|------|
| **citation-management** | Google Scholar/PubMed 搜索 | 准确 metadata、BibTeX 输出 | 需要 API 配置 |
| **academic-research-hub** | 多源搜索 (arXiv/PubMed/Semantic) | 支持下载 PDF、多格式输出 | 需要安装 Python 依赖 |
| **web_search** | 一般网络搜索 | 快速、无需配置 | 学术资源有限 |

### 3. 使用指南生成

为选定技能提供快速上手指南：

```markdown
## citation-management 快速开始

### 基本用法
citation-management --search "your query" --count 10

### 高级功能
citation-management --doi "10.xxxx/xxxxx" --format bibtex
citation-management --validate "references.bib"

### 最佳实践
- 使用具体关键词
- 设置合理数量限制 (5-20)
- 及时保存搜索结果
```

### 4. 问题诊断

当技能使用失败时，提供排查建议：

```
问题：技能没有触发

排查步骤：
1. 检查技能是否启用 → openclaw skills list
2. 验证关键词是否匹配 → 查看 SKILL.md 触发条件
3. 检查 Agent 配置 → 确认 agent 有权限调用
4. 尝试手动调用 → openclaw skill run <skill-name>
```

---

## 技能分类体系

### 按研究领域

| 领域 | 核心技能 |
|------|---------|
| **心理学** | academic-writing, statistical-analysis, paper-parse, citation-management |
| **数据科学** | data-analysis, statistical-analysis, scientific-visualization, matplotlib |
| **生物医学** | citation-management (PubMed), academic-research-hub, academic-writing |
| **计算机科学** | citation-management (arXiv), github, academic-research-hub |

### 按任务类型

| 任务类型 | 推荐技能 | 触发关键词 |
|---------|---------|-----------|
| **文献搜索** | citation-management, academic-research-hub | "搜索文献"、"找论文"、"Google Scholar" |
| **论文写作** | academic-writing, research-paper-writer | "润色"、"改写"、"学术写作"、"摘要" |
| **论文解析** | paper-parse | "解读论文"、"PDF 分析"、"论文总结" |
| **统计分析** | statistical-analysis, data-analysis | "t 检验"、"回归"、"ANOVA"、"相关分析" |
| **数据可视化** | scientific-visualization, matplotlib, seaborn | "画图"、"可视化"、"图表"、"figure" |
| **引用管理** | citation-management | "参考文献"、"BibTeX"、"引用格式"、"DOI" |
| **内容发布** | wechat-publisher, wechat-mp-publish, wenyan-cli | "公众号"、"发布"、"草稿" |
| **知识管理** | obsidian, github | "笔记"、"Obsidian"、"GitHub"、"commit" |

### 按输出格式

| 输出格式 | 推荐技能 |
|---------|---------|
| **BibTeX** | citation-management |
| **学术论文** | academic-writing, research-paper-writer |
| **统计报告 (APA)** | statistical-analysis |
| **publication-ready 图表** | scientific-visualization |
| **微信公众号文章** | wechat-publisher, wenyan-cli |
| **Markdown 文档** | academic-writing, paper-parse |

---

## 使用流程

### 步骤 1：需求澄清

当用户需求模糊时，主动询问：

```
用户："帮我分析一下数据"

助手："好的，我来帮你选择合适的数据分析技能。

请问：
1. 你的数据类型是什么？（问卷数据、实验数据、观测数据）
2. 你想做什么分析？（描述统计、差异检验、关系分析、预测模型）
3. 你的研究问题是什么？

根据回答，我会推荐最合适的技能。"
```

### 步骤 2：技能匹配

根据需求匹配技能：

```
决策树：

需要搜索文献？
├─ 是 → citation-management / academic-research-hub
└─ 否 → 需要分析数据？
    ├─ 是 → 什么分析？
    │   ├─ 描述统计 → data-analysis
    │   ├─ 假设检验 → statistical-analysis
    │   └─ 可视化 → scientific-visualization
    └─ 否 → 需要写作协助？
        ├─ 是 → academic-writing
        └─ 否 → 需要解析论文？
            └─ 是 → paper-parse
```

### 步骤 3：提供指南

为选定技能提供使用指南：

```markdown
## 推荐使用：statistical-analysis

### 适用场景
- t 检验、ANOVA、回归分析
- 假设检验、效应量计算
- APA 格式结果报告

### 基本用法
statistical-analysis --file data.csv --type t_test --group_var gender --dv wellbeing

### 下一步
1. 准备数据文件（CSV 格式）
2. 确认变量名称
3. 我可以帮你运行分析

需要我现在帮你执行吗？
```

### 步骤 4：执行支持

协助用户调用技能：

```bash
# 直接调用
openclaw skill run statistical-analysis --file data.csv --type descriptive

# 或让 Agent 代理
"好的，我来帮你运行统计分析..."
[执行技能调用]
```

---

## 核心技能详解

### citation-management 🔬

**用途**：文献搜索、引用管理、BibTeX 生成

**触发关键词**：
- "搜索文献"
- "找论文"
- "Google Scholar"
- "PubMed"
- "BibTeX"
- "DOI"
- "参考文献"

**使用示例**：
```bash
# 搜索文献
citation-management --search "subjective wellbeing China" --count 10

# DOI 转 BibTeX
citation-management --doi "10.1038/s41597-023-01234-x" --format bibtex

# 验证引用
citation-management --validate "references.bib"
```

**最佳实践**：
- ✅ 使用具体关键词（研究对象 + 方法 + 地区）
- ✅ 设置合理数量（5-20 篇）
- ✅ 及时保存搜索结果
- ❌ 避免过于宽泛的搜索词

---

### academic-writing ✍️

**用途**：论文写作、语言润色、格式优化

**触发关键词**：
- "润色"
- "改写"
- "学术写作"
- "摘要"
- "语法检查"
- "语言优化"

**使用示例**：
```bash
# 润色语言
academic-writing --file draft.md --action polish --output polished.md

# 生成摘要
academic-writing --type abstract --input full_paper.md

# 语法检查
academic-writing --file manuscript.md --action grammar_check
```

**最佳实践**：
- ✅ 提供上下文（研究领域、目标期刊）
- ✅ 明确润色目标（简洁性、学术性）
- ✅ 保留原文核心意思
- ❌ 不要期望一次性完美

---

### paper-parse 📄

**用途**：论文解析、PDF 分析、内容提取

**触发关键词**：
- "解读论文"
- "PDF 分析"
- "论文总结"
- "提取方法"
- "分析创新点"

**使用示例**：
```bash
# 解析 PDF
paper-parse --file paper.pdf --mode full

# 解析 URL
paper-parse --url "https://arxiv.org/abs/2301.12345"

# 双模式输出
paper-parse --file paper.pdf --mode dual
```

**最佳实践**：
- ✅ 提供高质量 PDF（文字版）
- ✅ 指定关注重点
- ✅ 结合多篇论文对比
- ❌ 避免扫描版 PDF

---

### statistical-analysis 📊

**用途**：统计分析、假设检验、结果解读

**触发关键词**：
- "t 检验"
- "回归分析"
- "ANOVA"
- "相关分析"
- "统计方法"
- "效应量"

**使用示例**：
```bash
# 描述统计
statistical-analysis --file data.csv --type descriptive

# t 检验
statistical-analysis --file data.csv --type t_test --group_var gender

# 回归分析
statistical-analysis --file data.csv --type regression --dv wellbeing --iv age income
```

**最佳实践**：
- ✅ 先检查数据质量
- ✅ 验证统计假设
- ✅ 报告效应量和 CI
- ❌ 不要盲目用复杂方法

---

### scientific-visualization 📈

**用途**：publication-ready 图表生成

**触发关键词**：
- "publication-ready"
- "Nature 风格"
- "误差线"
- "显著性标记"
- "色盲友好"

**使用示例**：
```bash
# 多面板图
scientific-visualization --config nature_style.yaml --data results.csv

# 单图生成
scientific-visualization --type barplot --data data.csv --style journal
```

**最佳实践**：
- ✅ 使用色盲友好配色
- ✅ 添加误差线和显著性
- ✅ 符合期刊格式
- ❌ 避免过度装饰

---

## 常见问题解答

### Q1: 技能没有触发怎么办？

**排查步骤**：
```bash
# 1. 检查技能列表
openclaw skills list

# 2. 查看技能状态
openclaw skills info <skill-name>

# 3. 启用技能（如需要）
openclaw skills enable <skill-name>

# 4. 手动调用测试
openclaw skill run <skill-name> --help
```

**常见原因**：
- 技能未启用
- 关键词不匹配
- Agent 配置问题
- 依赖未安装

---

### Q2: 多个技能都适用，怎么选？

**决策原则**：
1. **专用优先** - 选择专门针对该任务的技能
2. **功能覆盖** - 选择功能最全面的技能
3. **输出格式** - 选择符合输出需求的技能
4. **依赖最少** - 选择配置最简单的技能

**示例**：
```
任务：搜索心理学文献

选项：
- citation-management → ✅ 专用、支持 Google Scholar/PubMed
- academic-research-hub → ✅ 多源、支持 arXiv/PubMed/Semantic
- web_search → ❌ 一般搜索，学术资源有限

推荐：citation-management (心理学文献首选)
```

---

### Q3: 技能报错怎么办？

**通用排查流程**：
```
1. 阅读错误信息
   ↓
2. 检查输入格式（文件路径、参数名称）
   ↓
3. 查看技能文档（SKILL.md）
   ↓
4. 检查依赖安装
   ↓
5. 尝试简化参数
   ↓
6. 搜索类似问题（GitHub Issues / Discord）
```

**示例**：
```
错误："FileNotFoundError: data.csv"

解决：
1. 确认文件路径正确
2. 检查文件是否存在：ls data.csv
3. 使用绝对路径：/full/path/to/data.csv
```

---

### Q4: 如何发现新技能？

**方法**：
```bash
# 浏览技能市场
openclaw skills browse

# 搜索技能
openclaw skills search "keyword"

# 查看热门技能
openclaw skills trending

# 访问 Clawhub
https://clawhub.ai/skills
```

**推荐关注**：
- 每周新增技能
- 社区热门技能
- 官方推荐技能

---

## 技能搜索技巧

### 技巧 1：使用具体关键词

```
❌ "分析数据" → 太模糊
✅ "用 t 检验分析两组数据的差异" → 明确触发 statistical-analysis

❌ "画图" → 太模糊
✅ "画一个 publication-ready 的柱状图，带误差线" → 明确触发 scientific-visualization
```

### 技巧 2：指定输出格式

```
"生成 BibTeX 引用" → citation-management
"生成 APA 格式报告" → statistical-analysis
"生成 Markdown 文档" → academic-writing
```

### 技巧 3：使用同义词

| 用户需求 | 可能触发技能 |
|---------|-------------|
| "找文献" | citation-management, academic-research-hub |
| "查论文" | citation-management, paper-parse |
| "搜索研究" | citation-management, web_search |

**建议**：使用更具体的表述

---

## 最佳实践总结

### ✅ 推荐做法

1. **明确需求** - 具体描述任务目标
2. **提供上下文** - 研究领域、目标期刊
3. **迭代优化** - 根据结果调整
4. **保存结果** - 及时导出备份
5. **验证输出** - 检查准确性

### ❌ 避免错误

1. **模糊描述** - "分析一下"
2. **缺少上下文** - 不提供研究领域
3. **期望过高** - 期望一次性完美
4. **忽视验证** - 不检查输出质量
5. **重复搜索** - 不保存之前结果

---

## 资源链接

- **Clawhub 官网**: https://clawhub.ai
- **技能市场**: https://clawhub.ai/skills
- **OpenClaw 文档**: https://docs.openclaw.ai
- **社区 Discord**: https://discord.com/invite/clawd
- **技能开发指南**: https://docs.openclaw.ai/skills/creating

---

**维护者**: academic-assistant  
**版本**: v1.0  
**更新日期**: 2026-03-15  
**许可**: Apache 2.0

*帮助你在 238+ 个技能中快速找到所需工具！🔍📚*
