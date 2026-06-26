# Clawhub 技能搜索使用示例 📝

**真实场景演示：如何用技能搜索指南解决实际问题**

---

## 场景 1：研究生需要搜索文献

### 用户需求
```
"我是心理学研究生，想找一些关于'主观幸福感'和'社会支持'的中文文献，
大概 10-15 篇，用于文献综述。"
```

### 技能匹配过程

**步骤 1：识别任务类型**
- 任务：文献搜索
- 领域：心理学
- 关键词：主观幸福感、社会支持
- 语言：中文
- 数量：10-15 篇

**步骤 2：匹配技能**
```
候选技能：
1. citation-management → ✅ 支持 Google Scholar/PubMed，适合心理学
2. academic-research-hub → ✅ 支持多源搜索
3. web_search → ❌ 学术资源有限

推荐：citation-management（心理学文献首选）
```

**步骤 3：提供指南**
```markdown
## 推荐使用：citation-management

### 执行命令
citation-management --search "subjective wellbeing social support China" --count 15

### 预期输出
- 15 篇相关文献列表
- 每篇包含：标题、作者、年份、摘要、DOI
- 可选：BibTeX 引用格式

### 下一步
我可以帮你：
1. 执行搜索
2. 筛选高质量文献
3. 生成 BibTeX 参考文献

需要我现在开始吗？
```

**步骤 4：执行搜索**
```bash
citation-management --search "subjective wellbeing social support China" --count 15 --language zh
```

**步骤 5：结果整理**
```markdown
## 搜索结果：15 篇文献

### 高相关性文献（推荐优先阅读）
1. 社会支持对主观幸福感的影响：一项元分析
   作者：张三等
   期刊：心理学报
   年份：2023
   引用：Zhang et al. (2023). Acta Psychologica Sinica.
   
2. 中国成年人主观幸福感的城乡差异
   作者：李四等
   期刊：心理科学
   年份：2022
   
...

### 下一步建议
1. 精读前 5 篇高相关性文献
2. 使用 paper-parse 解析 PDF 全文
3. 用 academic-writing 帮助写文献综述

需要我帮你解析哪篇论文的 PDF？
```

---

## 场景 2：研究者需要统计分析

### 用户需求
```
"我有一份问卷数据，包含性别、年龄、收入、主观幸福感等变量。
想看看不同性别的人在幸福感上有没有差异，应该用什么统计方法？"
```

### 技能匹配过程

**步骤 1：识别任务类型**
- 任务：统计分析
- 设计：两组比较（男 vs 女）
- 因变量：主观幸福感（连续变量）
- 自变量：性别（二分类变量）

**步骤 2：匹配技能**
```
候选技能：
1. statistical-analysis → ✅ 专门用于统计分析，支持 t 检验
2. data-analysis → ✅ 可做描述统计
3. scientific-visualization → 后续可视化使用

推荐：statistical-analysis（统计分析首选）
```

**步骤 3：提供指南**
```markdown
## 推荐使用：statistical-analysis

### 统计方法选择
根据你的研究设计：
- 自变量：性别（2 水平：男/女）
- 因变量：主观幸福感（连续变量）
- 推荐方法：独立样本 t 检验

### 执行命令
statistical-analysis --file data.csv --type t_test --group_var gender --dv wellbeing

### 预期输出
- t 值、自由度、p 值
- 效应量（Cohen's d）
- 95% 置信区间
- APA 格式结果报告

### 假设检验前提
- 正态性检验（Shapiro-Wilk）
- 方差齐性检验（Levene's test）

需要我帮你运行分析吗？
```

**步骤 4：执行分析**
```bash
statistical-analysis --file data.csv --type t_test --group_var gender --dv wellbeing --output apa_report.md
```

**步骤 5：结果解读**
```markdown
## 统计分析结果

### 描述统计
| 性别 | N | 均值 | 标准差 |
|------|---|------|--------|
| 男   | 245 | 4.52 | 0.87 |
| 女   | 243 | 4.68 | 0.91 |

### t 检验结果
t(486) = -1.98, p = .048, d = 0.18, 95% CI [-0.32, -0.01]

### APA 格式报告
"独立样本 t 检验结果显示，女性（M = 4.68, SD = 0.91）的主观幸福感显著高于男性（M = 4.52, SD = 0.87），t(486) = -1.98, p = .048, d = 0.18, 95% CI [-0.32, -0.01]。效应量为小到中等。"

### 下一步建议
1. 用 scientific-visualization 生成柱状图（带误差线）
2. 考虑加入协变量（年龄、收入）做 ANCOVA
3. 检查效应量的实际意义

需要我帮你生成图表吗？
```

---

## 场景 3：作者需要润色论文

### 用户需求
```
"我写了一篇 Scientific Data 的论文草稿，想请你帮我润色一下语言，
让它更符合学术写作规范。"
```

### 技能匹配过程

**步骤 1：识别任务类型**
- 任务：论文润色
- 期刊：Scientific Data（Nature 系列）
- 内容：Data Descriptor
- 需求：语言优化、学术规范

**步骤 2：匹配技能**
```
候选技能：
1. academic-writing → ✅ 专门用于学术写作润色
2. research-paper-writer → 用于完整论文生成
3. paper-parse → 用于论文解析

推荐：academic-writing（论文润色首选）
```

**步骤 3：提供指南**
```markdown
## 推荐使用：academic-writing

### 润色模式
针对 Scientific Data 期刊，我会：
- 优化语言流畅性
- 确保学术规范
- 保持技术准确性
- 符合 Nature 系列风格

### 执行命令
academic-writing --file draft.md --action polish --journal scientific_data --output polished.md

### 润色重点
1. Abstract（简洁、信息密集）
2. Background & Summary（逻辑清晰）
3. Methods（可重复性）
4. Data Records（准确描述）
5. Technical Validation（统计支持）

### 预期改进
- 句子结构优化
- 术语使用规范
- 逻辑连接增强
- 冗余表达删除

需要我现在开始润色吗？
```

**步骤 4：执行润色**
```bash
academic-writing --file draft.md --action polish --journal scientific_data --output polished.md
```

**步骤 5：对比展示**
```markdown
## 润色前后对比

### 原文
"We collected data from many people in China. The data is about their wellbeing. 
We used some questionnaires to measure different things."

### 润色后
"We collected a comprehensive dataset from a large-scale sample of Chinese adults (N = 48,845). 
The dataset encompasses multi-dimensional wellbeing measures assessed through validated psychometric instruments."

### 改进点
1. 具体化："many people" → "large-scale sample (N = 48,845)"
2. 专业化："about their wellbeing" → "multi-dimensional wellbeing measures"
3. 精确化："some questionnaires" → "validated psychometric instruments"
4. 学术化：整体语气更符合 Scientific Data 风格

### 全文统计
- 原稿：8,542 词
- 润色：8,234 词（精简 3.6%）
- 可读性：提升 15%（Flesch-Kincaid）

### 下一步建议
1. 逐段审查润色结果
2. 确认技术术语准确性
3. 补充必要的引用
4. 检查格式是否符合期刊要求

需要我帮你检查哪个部分？
```

---

## 场景 4：读者需要解析论文

### 用户需求
```
"这篇 Nature 的论文太长了，能帮我总结一下核心内容吗？
特别是研究方法和主要发现。"
```

### 技能匹配过程

**步骤 1：识别任务类型**
- 任务：论文解析
- 来源：Nature 期刊
- 重点：方法、发现
- 输出：总结报告

**步骤 2：匹配技能**
```
候选技能：
1. paper-parse → ✅ 专门用于论文解析，双模式输出
2. academic-writing → 用于写作
3. citation-management → 用于搜索

推荐：paper-parse（论文解析首选）
```

**步骤 3：提供指南**
```markdown
## 推荐使用：paper-parse

### 解析模式
双模式输出：
- Part A：面向研究者的深度专业解析
- Part B：面向快速理解的核心逻辑与价值提炼

### 执行命令
paper-parse --file nature_paper.pdf --mode dual

### 解析内容
Part A（专业版）:
- 研究问题与假设
- 理论框架
- 方法细节（设计、被试、材料、程序）
- 统计分析
- 结果与讨论
- 局限与未来方向

Part B（简化版）:
- 一句话总结
- 3 个核心发现
- 2 个方法创新
- 1 个实践启示

### 预期输出
- 结构化报告（Markdown 格式）
- 关键图表提取
- 专业术语解释

需要我现在解析吗？
```

**步骤 4：执行解析**
```bash
paper-parse --file nature_paper.pdf --mode dual --output summary.md
```

**步骤 5：输出展示**
```markdown
# 论文解析报告

## Part B：核心逻辑与价值提炼（快速理解）

### 一句话总结
本研究通过 X 方法，发现 Y 现象，揭示了 Z 机制，为 A 领域提供了新视角。

### 3 个核心发现
1. **发现 1**: [具体内容]，效应量 d = 0.45
2. **发现 2**: [具体内容]，p < .001
3. **发现 3**: [具体内容]，调节效应显著

### 2 个方法创新
1. **创新 1**: 首次使用 X 方法研究 Y 问题
2. **创新 2**: 开发了新的测量工具 Z

### 1 个实践启示
[对实际应用的价值]

---

## Part A：深度专业解析（研究者用）

### 1. 研究问题
**核心问题**: [详细描述]
**理论缺口**: [现有研究的不足]
**研究假设**: H1, H2, H3

### 2. 理论框架
[理论基础、概念模型图]

### 3. 方法
**研究设计**: [实验设计类型]
**被试**: N = XXX, 年龄 M = XX, 性别分布
**材料**: [测量工具、实验材料]
**程序**: [实验流程]

### 4. 统计分析
[使用的统计方法、软件]

### 5. 结果
**假设 1**: 支持/不支持，t(X) = X.XX, p = .XXX
**假设 2**: 支持/不支持，F(X, X) = X.XX, p = .XXX
**假设 3**: 支持/不支持，β = .XXX, p = .XXX

### 6. 讨论
**主要贡献**: [理论贡献]
**机制解释**: [结果的理论解释]
**局限性**: [研究局限]
**未来方向**: [后续研究建议]

### 7. 关键图表
[图表提取与说明]

---

### 下一步建议
1. 精读 Part B 快速把握核心
2. 根据需要阅读 Part A 特定部分
3. 用 citation-management 获取 BibTeX 引用
4. 用 academic-writing 帮助写文献综述

需要我帮你获取这篇论文的引用格式吗？
```

---

## 场景 5：创业者需要发布公众号文章

### 用户需求
```
"我写了一篇关于 AI 创业的 Markdown 文章，想发布到微信公众号，
怎么操作？"
```

### 技能匹配过程

**步骤 1：识别任务类型**
- 任务：内容发布
- 平台：微信公众号
- 格式：Markdown
- 需求：排版 + 发布

**步骤 2：匹配技能**
```
候选技能：
1. wechat-publisher → ✅ 直接发布到草稿箱
2. wechat-mp-publish → ✅ 草稿管理
3. wenyan-cli → ✅ Markdown 渲染排版

推荐组合：
- 简单发布：wechat-publisher
- 精美排版：wenyan-cli + wechat-mp-publish
```

**步骤 3：提供指南**
```markdown
## 推荐使用：wechat-publisher + wenyan-cli

### 方案 1：快速发布（推荐）
直接发布 Markdown 到草稿箱：

```bash
wechat-publisher --file article.md
```

### 方案 2：精美排版
使用 wenyan-cli 渲染后发布：

```bash
# 渲染 Markdown
wenyan render article.md

# 发布到草稿箱
wenyan publish article.md
```

### 前置配置
需要设置环境变量：
```bash
export WECHAT_APP_ID=wxd3d9d45b1b9defcd
export WECHAT_APP_SECRET=52bae57620f3432865fbc8d502f5a6da
```

### 预期输出
- 文章发布到草稿箱
- 获得 media_id
- 可在公众号后台预览和编辑

需要我帮你发布吗？
```

**步骤 4：执行发布**
```bash
# 方案 1
wechat-publisher --file ai_startup_article.md

# 或方案 2
wenyan publish ai_startup_article.md
```

**步骤 5：发布确认**
```markdown
## 发布成功 ✅

### 文章信息
- 标题：AI 创业的黄金时代
- 状态：已发布到草稿箱
- media_id: xxxxxxxxxxxx
- 预览链接：[点击查看]

### 下一步
1. 在公众号后台预览效果
2. 检查排版和格式
3. 确认无误后群发
4. 跟踪阅读数据

### 发布技巧
- 最佳发布时间：周五 14:00（根据 AI 周报经验）
- 封面图建议：16:9 比例，清晰醒目
- 摘要：前 54 个字会自动作为摘要

需要我帮你检查排版效果吗？
```

---

## 场景 6：不确定用什么技能

### 用户需求
```
"我想做 AI 和心理学的交叉研究，应该用哪些技能？"
```

### 技能匹配过程

**步骤 1：需求分析**
- 领域：AI + 心理学
- 任务：不明确（需要澄清）
- 阶段：研究规划

**步骤 2：主动澄清**
```markdown
好的，AI 与心理学交叉是一个很好的研究方向！

为了给你推荐最合适的技能，我需要了解：

1. **研究阶段**：
   - 文献调研？
   - 研究设计？
   - 数据收集？
   - 数据分析？
   - 论文写作？

2. **具体方向**：
   - AI as Subject（AI 对用户心理的影响）？
   - AI as Tool（AI 作为研究工具）？
   - AI as Interaction（人机交互体验）？

3. **数据类型**：
   - 问卷数据？
   - 实验数据？
   - 行为日志？
   - 文本数据？

根据你的回答，我会推荐最匹配的技能组合。
```

**步骤 3：根据回答推荐**

假设用户回答：
```
"我想研究 AI 辅助写作对用户自我效能感的影响，
已经有问卷数据了，需要做统计分析和论文写作。"
```

**技能推荐**：
```markdown
## 推荐技能组合

### 1. 统计分析 → statistical-analysis
```bash
# 描述统计
statistical-analysis --file data.csv --type descriptive

# t 检验/ANOVA（组间比较）
statistical-analysis --file data.csv --type anova --group_var condition --dv self_efficacy

# 回归分析（预测模型）
statistical-analysis --file data.csv --type regression --dv self_efficacy --iv ai_usage prior_experience
```

### 2. 数据可视化 → scientific-visualization
```bash
# 组间差异图
scientific-visualization --type barplot --data results.csv --style journal
```

### 3. 论文写作 → academic-writing
```bash
# 润色论文
academic-writing --file draft.md --action polish --journal nature_comm
```

### 4. 文献支持 → citation-management
```bash
# 搜索相关文献
citation-management --search "AI writing self-efficacy" --count 20
```

### 完整工作流
```
文献搜索 → 研究设计 → 数据收集 → 统计分析 → 可视化 → 论文写作 → 投稿
    ↓           ↓           ↓           ↓           ↓           ↓           ↓
citation   (设计)     (收集)   statistical  scientific  academic   (投稿)
-management                      analysis   visualization writing
```

需要我从哪个技能开始帮你？
```

---

## 总结：技能搜索最佳实践

### ✅ 成功模式

1. **明确任务** - 具体描述要做什么
2. **提供上下文** - 研究领域、数据类型、目标
3. **接受推荐** - 信任技能匹配逻辑
4. **迭代优化** - 根据结果调整参数
5. **组合使用** - 多个技能协同工作

### ❌ 失败模式

1. **模糊描述** - "帮我分析一下"
2. **缺少信息** - 不提供数据类型和研究问题
3. **期望过高** - 期望一个技能解决所有问题
4. **忽视指南** - 不按技能文档操作
5. **不保存结果** - 重复劳动

---

**版本**: v1.0 | **更新**: 2026-03-15 | **许可**: Apache 2.0

*通过真实场景学习如何高效使用技能搜索！📚✨*
