---
name: auto-citation
description: |
  自动为学术文章添加参考文献。解析文章内容提取主题和关键词，
  调用 academic-search 检索相关论文，推荐候选文献供用户确认，
  自动插入格式化的引用。支持 Markdown/LaTeX/Word 输入，
  输出 BibTeX/GB/T 7714/APA 格式。当用户说"帮我加参考文献"、
  "给这篇文章找引用"或处理 .md/.tex/.docx 文件时触发。
---

# 自动添加参考文献

## 触发检测

检测以下信号时激活本 Skill：

**意图信号（中文）**
- "加参考文献"/"添加引用"/"找相关论文"
- "补充文献"/"完善参考文献"
- "给这段话加引用"

**意图信号（英文）**
- "add citations"/"find references"
- "complete bibliography"

**文件信号**
- 扩展名：`.md` / `.tex` / `.docx`
- 内容特征：已有正文但引用不足或缺失

---

## 前置依赖

### 必需依赖
本 Skill 依赖 academic-search Skill 进行论文检索。

**安装命令**：
```bash
git clone https://github.com/ustc-ai4science/academic-search ~/.cursor/skills/academic-search
bash ~/.cursor/skills/academic-search/scripts/check-deps.sh
```

### Python 依赖
```bash
pip install python-docx textract
```

---

## 工作流程

### Step 1: 解析文档

运行解析脚本提取文档关键信息：

```bash
python ~/.cursor/skills/auto-citation/scripts/parse_document.py <文件路径>
```

**输出内容**：
- 文档类型（markdown/latex/word）
- 主题摘要（TL;DR）
- 关键词列表（3-7 个核心术语）
- 现有引用列表（避免重复推荐）
- 建议检索方向（2-4 个互补 query）

### Step 2: 生成搜索策略

基于解析结果，生成 2-4 个互补搜索 query：

**策略原则**：
- 覆盖核心概念（主要方法/技术）
- 覆盖应用场景（domain-specific）
- 覆盖 baseline 对比（相关经典工作）
- 近 5 年优先（时效性优先）

### Step 3: 并行检索

调用 academic-search Skill 执行多 query 搜索：

```
子 Agent 任务分发：
├── Query 1: "graph neural network time series" → arXiv + S2
├── Query 2: "GNN temporal data prediction" → arXiv + S2
├── Query 3: "time series forecasting deep learning" → Google Scholar
└── 合并结果，DOI/arXiv ID 去重
```

**搜索参数**：
- 年份范围：近 5 年（或用户指定）
- 排序：时效性优先 → 引用数 → CCF 等级
- 数量：每 query 取前 10 篇

### Step 4: 去重与筛选

**去重规则**（按优先级）：
1. DOI 精确匹配
2. arXiv ID 匹配
3. 标题 + 年份 + 第一作者匹配

**筛选逻辑**：
- 排除已存在的引用
- 按相关性 + 引用数 + 时效性排序
- 保留前 8-12 篇作为候选池

### Step 5: 推荐候选

向用户展示候选列表，格式如下：

```
基于你的文章主题（GNN 时间序列预测），我找到以下相关论文：

[1] Title A - 被引 150 次 (2023)
    作者：Author A, Author B
    相关点：与你第 2 节的方法直接相关，可作为主要对比 baseline
    
[2] Title B - 被引 89 次 (2024) [新]
    作者：Author C et al.
    相关点：最新 SOTA 方法，建议作为主要引用
    
[3] Title C - 被引 320 次 (2021)
    作者：Author D
    相关点：领域经典工作，适合引言背景介绍

请输入你想引用的编号（如：1,3,5），或：
- 输入 "更多" 查看下一批候选
- 输入 "调整" 修改搜索方向
- 输入特定需求（如："找几篇中文文献"）
```

### Step 6: 格式化与插入

**格式选择**（按以下优先级）：
1. 用户明确指定（"用 GB/T 7714 格式"）
2. 文件内标记（`<!-- citation-style: bibtex -->`）
3. 环境变量（`AUTO_CITATION_STYLE=gb7714`）
4. 根据文件类型推断（.tex → BibTeX, .docx → GB7714）

**格式化命令**：
```bash
python ~/.cursor/skills/auto-citation/scripts/format_citation.py \
  --style {bibtex|gb7714|apa} \
  --papers <papers.json> \
  --output <输出路径>
```

**插入命令**：
```bash
python ~/.cursor/skills/auto-citation/scripts/insert_citation.py \
  --document <原文路径> \
  --citations <引用文件> \
  --output <输出路径>
```

---

## 引用格式说明

### BibTeX 格式
适用于 LaTeX 文档。

**文件组织**：
- 生成/更新 `.bib` 文件
- 原文使用 `\cite{key}` 标记
- 支持 `\bibliographystyle` 自定义样式

**示例输出**：
```bibtex
@inproceedings{wang2023gnn,
  title={Graph Neural Networks for Time Series Prediction},
  author={Wang, X. and Li, Y.},
  booktitle={NeurIPS},
  year={2023}
}
```

### GB/T 7714 格式
适用于中文论文和学位论文。

**文中引用**：上标 `[1]` 或 `[1-3]`
**文末列表**：按引用顺序编号

**示例输出**：
```
[1] Wang X, Li Y. Graph Neural Networks for Time Series Prediction[C]. 
    NeurIPS, 2023.
[2] Zhang S. Deep Learning Methods[J]. Journal of AI, 2024, 10(2): 100-120.
```

### APA 格式
适用于社会科学和国际期刊。

**文中引用**：作者-年份制 `(Wang & Li, 2023)`
**文末列表**：按作者字母排序

**示例输出**：
```
Wang, X., & Li, Y. (2023). Graph neural networks for time series prediction. 
    In NeurIPS (pp. 1000-1010).
```

---

## 用户交互模式

### 模式一：全自动推荐
用户未指定具体需求时，AI 自主完成全部流程。

### 模式二：定向补充
用户指定特定位置或主题：
- "给引言加几篇背景文献"
- "实验部分需要 baseline 引用"
- "找几篇用 Transformer 做时间序列的论文"

### 模式三：精确匹配
用户提供部分信息：
- "我记得有一篇 NeurIPS 2023 的 GNN 论文"
- "找这篇论文的完整引用：arxiv:2401.12345"

---

## 质量检查清单

每次执行后自我检查：

- [ ] 推荐的引用是否与文章主题相关
- [ ] 是否避免了重复引用
- [ ] 引用格式是否符合用户要求
- [ ] 年份分布是否合理（既有经典又有最新）
- [ ] 引用位置标注是否正确（文中标记与文末列表对应）

---

## 错误处理

**情况 1: 文档解析失败**
- 尝试用通用方法提取纯文本
- 询问用户文章主题关键词
- 基于关键词手动生成 query

**情况 2: 搜索结果为空**
- 放宽年份限制
- 简化 query（去掉太具体的限制）
- 尝试不同平台（尤其是 CNKI 中文文献）

**情况 3: 用户不满意推荐**
- 询问具体需求（"需要 baseline 还是最新工作？"）
- 调整搜索方向
- 扩大或缩小关键词范围

---

## 相关文件

- 文档解析说明：[references/parser-guide.md](references/parser-guide.md)
- 引用格式规范：[references/citation-styles.md](references/citation-styles.md)
- 使用示例：[references/workflow-examples.md](references/workflow-examples.md)
