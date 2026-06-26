# Clawhub 技能搜索使用指南 🔍

**在 238+ 个技能中快速找到你需要的工具**

---

## 为什么需要这个指南

OpenClaw 技能库已包含 **238+ 个技能**，涵盖写作、编程、数据分析、学术研究、内容创作等多个领域。

**常见问题：**
- ❌ 技能太多，不知道哪个适合自己
- ❌ 搜索关键词不准确，找不到目标技能
- ❌ 不了解技能的触发条件和使用场景
- ❌ 安装了技能却不知道如何调用

**本指南帮你：**
- ✅ 快速定位所需技能
- ✅ 理解技能触发机制
- ✅ 掌握最佳实践
- ✅ 避免常见错误

---

## 快速开始

### 方法 1：自然语言触发（推荐）

直接描述你的需求，Agent 会自动匹配技能：

```
"帮我搜索关于主观幸福感的文献"
→ 自动触发：citation-management / academic-research-hub

"分析一下这份数据的相关性"
→ 自动触发：statistical-analysis / data-analysis

"润色这段论文摘要"
→ 自动触发：academic-writing
```

### 方法 2：技能名称调用

明确指定技能名称：

```
/run citation-management --query "subjective wellbeing China"
/run statistical-analysis --file data.csv --type regression
```

### 方法 3：分类浏览

按领域浏览技能：

| 领域 | 核心技能 |
|------|---------|
| **学术研究** | citation-management, academic-writing, paper-parse |
| **数据分析** | statistical-analysis, data-analysis, scientific-visualization |
| **内容创作** | wechat-publisher, wechat-mp-publish, wenyan-cli |
| **知识管理** | obsidian, github |

---

## 技能搜索策略

### 策略 1：按任务类型搜索

| 任务类型 | 推荐技能 | 触发关键词 |
|---------|---------|-----------|
| **文献搜索** | citation-management | "搜索文献"、"找论文"、"Google Scholar" |
| **论文写作** | academic-writing | "润色"、"改写"、"学术写作" |
| **论文解析** | paper-parse | "解读论文"、"PDF 分析"、"论文总结" |
| **统计分析** | statistical-analysis | "t 检验"、"回归"、"ANOVA" |
| **数据可视化** | scientific-visualization | "画图"、"可视化"、"图表" |
| **引用管理** | citation-management | "参考文献"、"BibTeX"、"引用格式" |

### 策略 2：按研究领域搜索

| 研究领域 | 相关技能 |
|---------|---------|
| **心理学** | academic-writing, statistical-analysis, paper-parse |
| **数据科学** | data-analysis, scientific-visualization, matplotlib |
| **生物医学** | citation-management (PubMed), academic-research-hub |
| **计算机科学** | citation-management (arXiv), github |

### 策略 3：按输出格式搜索

| 输出格式 | 推荐技能 |
|---------|---------|
| **BibTeX** | citation-management |
| **学术论文** | academic-writing, research-paper-writer |
| **统计报告** | statistical-analysis |
| ** publication-ready 图表** | scientific-visualization |
| **微信公众号文章** | wechat-publisher, wenyan-cli |

---

## 核心技能详解

### 1. citation-management 🔬

**用途**：文献搜索、引用管理、BibTeX 生成

**触发场景**：
- "搜索关于 X 的论文"
- "找 10 篇关于 Y 的文献"
- "把这个 DOI 转成 BibTeX"
- "验证这个引用"

**使用示例**：
```bash
# 搜索文献
citation-management --search "subjective wellbeing China" --count 10

# DOI 转 BibTeX
citation-management --doi "10.1038/s41597-023-01234-x" --format bibtex

# 验证引用
citation-management --validate "reference.bib"
```

**最佳实践**：
- ✅ 使用具体关键词（包含研究对象、方法、地区）
- ✅ 设置合理的数量限制（5-20 篇）
- ✅ 及时保存搜索结果
- ❌ 避免过于宽泛的搜索词

---

### 2. academic-writing ✍️

**用途**：论文写作、语言润色、格式优化

**触发场景**：
- "润色这段文字"
- "帮我写一个摘要"
- "检查语法错误"
- "优化这段的表达"

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
- ✅ 明确润色目标（简洁性、学术性、可读性）
- ✅ 保留原文核心意思
- ❌ 不要期望一次性完美

---

### 3. paper-parse 📄

**用途**：论文解析、PDF 分析、内容提取

**触发场景**：
- "解读这篇论文"
- "总结这篇 PDF 的核心内容"
- "提取这篇论文的研究方法"
- "分析这篇论文的创新点"

**使用示例**：
```bash
# 解析 PDF
paper-parse --file paper.pdf --mode full

# 解析 URL
paper-parse --url "https://arxiv.org/abs/2301.12345"

# 双模式输出
paper-parse --file paper.pdf --mode dual  # Part A 专业版 + Part B 简化版
```

**最佳实践**：
- ✅ 提供高质量 PDF（文字版，非扫描版）
- ✅ 指定关注重点（方法、结果、创新点）
- ✅ 结合多篇论文对比分析
- ❌ 避免扫描版 PDF（OCR 准确率低）

---

### 4. statistical-analysis 📊

**用途**：统计分析、假设检验、结果解读

**触发场景**：
- "这个数据用什么统计方法"
- "帮我做 t 检验"
- "解读这个回归结果"
- "检查统计假设"

**使用示例**：
```bash
# 描述统计
statistical-analysis --file data.csv --type descriptive

# t 检验
statistical-analysis --file data.csv --type t_test --group_var gender --dv wellbeing

# 回归分析
statistical-analysis --file data.csv --type regression --dv wellbeing --iv age income support

# APA 格式报告
statistical-analysis --file data.csv --type anova --output apa_report.md
```

**最佳实践**：
- ✅ 先检查数据质量（缺失值、异常值）
- ✅ 验证统计假设（正态性、方差齐性）
- ✅ 报告效应量和置信区间
- ❌ 不要盲目使用复杂方法

---

### 5. scientific-visualization 📈

**用途**：publication-ready 图表生成

**触发场景**：
- "画一个 publication-ready 的图"
- "生成 Nature 风格的图表"
- "美化这个图"
- "添加误差线和显著性标记"

**使用示例**：
```bash
# 多面板图
scientific-visualization --config nature_style.yaml --data results.csv

# 单图生成
scientific-visualization --type barplot --data data.csv --style journal

# 自定义样式
scientific-visualization --template my_template.json --output figure.png
```

**最佳实践**：
- ✅ 使用色盲友好配色
- ✅ 添加误差线和显著性标记
- ✅ 符合目标期刊格式要求
- ❌ 避免过度装饰

---

### 6. wechat-publisher 📱

**用途**：微信公众号文章发布

**触发场景**：
- "发布这篇文章到公众号"
- "创建草稿"
- "渲染 Markdown 文章"

**使用示例**：
```bash
# 发布到草稿箱
wechat-publisher --file article.md

# 创建草稿
wechat-mp-publish --action create_draft --title "标题" --content "内容"

# 渲染并发布
wenyan publish article.md
```

**最佳实践**：
- ✅ 提前配置环境变量（WECHAT_APP_ID, WECHAT_APP_SECRET）
- ✅ 使用 Markdown 格式
- ✅ 检查排版效果
- ❌ 不要发布敏感内容

---

## 技能搜索技巧

### 技巧 1：使用同义词

| 用户需求 | 可能触发技能 |
|---------|-------------|
| "找文献" | citation-management, academic-research-hub |
| "查论文" | citation-management, paper-parse |
| "搜索研究" | citation-management, web_search |

**建议**：使用更具体的表述，如"搜索关于 X 的论文"

### 技巧 2：组合关键词

```
❌ "分析数据"  → 太模糊
✅ "用 t 检验分析两组数据的差异" → 触发 statistical-analysis

❌ "画图" → 太模糊
✅ "画一个 publication-ready 的柱状图，带误差线" → 触发 scientific-visualization
```

### 技巧 3：指定输出格式

```
"生成 BibTeX 引用" → citation-management
"生成 APA 格式报告" → statistical-analysis
"生成 Markdown 文档" → academic-writing
```

---

## 常见问题

### Q1: 技能没有触发怎么办？

**可能原因**：
1. 关键词不够明确
2. 技能未安装/未启用
3. Agent 配置问题

**解决方案**：
```bash
# 检查技能列表
openclaw skills list

# 启用技能
openclaw skills enable <skill-name>

# 手动调用
openclaw skill run <skill-name> --help
```

### Q2: 多个技能都可以用，选哪个？

**决策树**：
```
需要搜索文献？
├─ 是 → citation-management
└─ 否 → 需要统计分析？
    ├─ 是 → statistical-analysis
    └─ 否 → 需要写作协助？
        ├─ 是 → academic-writing
        └─ 否 → 需要解析论文？
            └─ 是 → paper-parse
```

### Q3: 技能报错怎么办？

**排查步骤**：
1. 检查输入文件格式
2. 验证参数是否正确
3. 查看技能文档（SKILL.md）
4. 检查依赖是否安装

**示例**：
```bash
# 查看技能文档
openclaw skill read citation-management

# 检查依赖
pip list | grep -E "arxiv|scholarly|pubmed"
```

---

## 技能分类索引

### 学术研究类

| 技能 | 用途 | 触发关键词 |
|------|------|-----------|
| **citation-management** | 文献搜索、引用管理 | "搜索文献"、"BibTeX"、"DOI" |
| **academic-writing** | 论文写作、润色 | "润色"、"学术写作"、"摘要" |
| **paper-parse** | 论文解析 | "解读论文"、"PDF 分析" |
| **research-paper-writer** | 完整论文生成 | "写论文"、"research paper" |
| **academic-research-hub** | 多源文献搜索 | "arXiv"、"PubMed"、"Semantic Scholar" |

### 数据分析类

| 技能 | 用途 | 触发关键词 |
|------|------|-----------|
| **statistical-analysis** | 统计分析 | "t 检验"、"回归"、"ANOVA" |
| **data-analysis** | 数据清洗、描述统计 | "数据清洗"、"描述统计" |
| **scientific-visualization** | publication-ready 图表 | "publication-ready"、"Nature 风格" |
| **matplotlib** | 自定义图表 | "matplotlib"、"自定义图" |
| **seaborn** | 统计可视化 | "seaborn"、"统计图" |

### 内容创作类

| 技能 | 用途 | 触发关键词 |
|------|------|-----------|
| **wechat-publisher** | 微信公众号发布 | "公众号"、"发布文章" |
| **wechat-mp-publish** | 草稿管理 | "创建草稿"、"发布草稿" |
| **wenyan-cli** | Markdown 渲染 | "wenyan"、"渲染" |

### 知识管理类

| 技能 | 用途 | 触发关键词 |
|------|------|-----------|
| **obsidian** | 笔记管理 | "Obsidian"、"笔记" |
| **github** | 代码管理 | "GitHub"、"commit"、"PR" |

---

## 最佳实践总结

### ✅ 推荐做法

1. **明确需求** - 具体描述任务目标
2. **提供上下文** - 研究领域、目标期刊、数据特点
3. **迭代优化** - 根据结果调整搜索词
4. **保存结果** - 及时导出和备份
5. **验证输出** - 检查准确性和完整性

### ❌ 避免错误

1. **模糊描述** - "分析一下"、"帮我弄一下"
2. **缺少上下文** - 不提供研究领域或目标
3. **期望过高** - 期望一次性完美结果
4. **忽视验证** - 不检查输出质量
5. **重复搜索** - 不保存之前的搜索结果

---

## 资源链接

- **Clawhub 官网**: https://clawhub.ai
- **技能市场**: https://clawhub.ai/skills
- **OpenClaw 文档**: https://docs.openclaw.ai
- **社区**: https://discord.com/invite/clawd

---

**维护者**: academic-assistant  
**版本**: v1.0  
**更新日期**: 2026-03-15

*帮助你在 238+ 个技能中快速找到所需工具！🔍📚*
