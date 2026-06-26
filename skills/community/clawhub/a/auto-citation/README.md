# Auto-Citation Skill

自动为学术文章添加参考文献的 Cursor Skill。基于 [academic-search](https://github.com/ustc-ai4science/academic-search) 能力，实现智能解析、精准检索、自动格式化和无缝插入。

---

## 核心功能

**智能解析**
- 自动识别 Markdown / LaTeX / Word (.docx) 文档
- 提取主题关键词和核心概念
- 检测现有引用避免重复

**精准检索**
- 调用 academic-search 8 大平台（arXiv、Semantic Scholar、Google Scholar、CNKI 等）
- 多 query 并行搜索，覆盖率提升 30-50%
- 时效性优先排序（近 6 月论文置顶）

**多格式支持**
- **BibTeX**：LaTeX 文档，兼容各类 bibliography style
- **GB/T 7714**：中文论文标准格式
- **APA**：国际期刊常用格式

**无缝插入**
- Markdown：文末自动生成参考文献章节
- LaTeX：生成 .bib 文件或 thebibliography 环境
- Word：文档末尾添加格式化引用列表

---

## 快速开始

### 1. 安装依赖

```bash
# 安装 academic-search skill（必需依赖）
git clone https://github.com/ustc-ai4science/academic-search ~/.cursor/skills/academic-search
bash ~/.cursor/skills/academic-search/scripts/check-deps.sh

# 安装 auto-citation skill
git clone https://github.com/yourusername/auto-citation ~/.cursor/skills/auto-citation

# 安装 Python 依赖
pip install python-docx
```

### 2. 使用方式

在 Cursor 中直接说：

```
帮我给这篇论文加一些参考文献
```

或指定具体需求：

```
给引言部分找几篇 GNN 相关背景文献，用 BibTeX 格式
```

```
给这个 Word 文档添加 5 篇时间序列预测的最新论文
```

---

## 工作流程

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  用户输入   │────▶│  解析文档    │────▶│ 生成搜索策略 │
│             │     │              │     │              │
└─────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  完成输出   │◄────│ 格式化与插入 │◄────│ 用户确认    │
│             │     │              │     │ 候选推荐    │
└─────────────┘     └──────────────┘     └──────────────┘
                                                  ▲
                                                  │
                                           ┌──────────────┐
                                           │ academic-search│
                                           │  并行检索    │
                                           └──────────────┘
```

---

## 使用示例

### 示例 1：完善学术论文

**用户输入**：
```
帮我给这篇 LaTeX 论文的引言部分加一些背景文献
```

**AI 执行**：
1. 解析 .tex 文件，提取主题"graph neural network time series"
2. 生成多个互补搜索 query
3. 调用 academic-search 检索相关论文
4. 展示候选列表：

```
基于你的引言内容，找到以下相关背景文献：

[1] Spatio-Temporal Graph Neural Networks - 被引 320 次 (2021)
    相关点：全面的 GNN 综述，适合作为领域背景
    
[2] Graph WaveNet - 被引 450 次 (2019)
    相关点：交通预测的 GNN 经典工作

请输入你想引用的编号（如：1,2）：
```

5. 用户确认后，生成 BibTeX 并插入 `\cite{}` 命令

### 示例 2：技术博客引用

**用户输入**：
```
给这篇 Markdown 博客添加 Transformer 和 BERT 的引用
```

**AI 执行**：
1. 识别关键论文需求：Attention is All You Need、BERT
2. 直接检索 arXiv 获取完整元数据
3. 生成 GB/T 7714 格式引用
4. 插入到文章末尾

### 示例 3：Baseline 引用补充

**用户输入**：
```
给实验部分的 baseline 方法添加引用，包括 LSTM、GRU、Transformer
```

**AI 执行**：
1. 精准检索各 baseline 的原始论文
2. 生成格式统一的引用列表
3. 在正文中添加对应的 `\cite{}` 标记

---

## 脚本工具独立使用

### parse_document.py - 文档解析

```bash
python scripts/parse_document.py paper.md
```

输出文档类型、关键词、建议搜索 query 等 JSON 格式信息。

### format_citation.py - 引用格式化

```bash
# BibTeX 格式
python scripts/format_citation.py \
  --style bibtex \
  --papers papers.json \
  --output references.bib

# GB/T 7714 格式
python scripts/format_citation.py \
  --style gb7714 \
  --papers papers.json \
  --output references.txt

# APA 格式（含文中标记）
python scripts/format_citation.py \
  --style apa \
  --papers papers.json \
  --with-markers \
  --output references.txt
```

### insert_citation.py - 引用插入

```bash
# Markdown
python scripts/insert_citation.py \
  --document article.md \
  --citations references.txt \
  --output article_with_refs.md

# LaTeX
python scripts/insert_citation.py \
  --document paper.tex \
  --citations references.bib \
  --style bibtex

# Word
python scripts/insert_citation.py \
  --document report.docx \
  --citations references.txt
```

---

## 项目结构

```
auto-citation/
├── SKILL.md                      # 主指令文件（Cursor 自动加载）
├── README.md                     # 本文件
├── scripts/
│   ├── parse_document.py         # 文档解析器
│   ├── format_citation.py        # 引用格式化工具
│   └── insert_citation.py        # 引用插入工具
└── references/
    ├── citation-styles.md        # 引用格式规范速查
    └── workflow-examples.md      # 使用场景示例
```

---

## 配置选项

### 引用格式选择

**优先级**（从高到低）：

1. 用户明确指定：`"用 GB/T 7714 格式"`
2. 文件内标记：`<!-- citation-style: bibtex -->`
3. 环境变量：`export AUTO_CITATION_STYLE=gb7714`
4. 文件类型推断：`.tex → BibTeX`, `.docx → GB7714`

### 环境变量

```bash
# 默认引用格式
export AUTO_CITATION_STYLE=bibtex  # 可选: bibtex, gb7714, apa

# 搜索年份范围
export AUTO_CITATION_YEAR_RANGE=5   # 近 5 年

# 推荐候选数量
export AUTO_CITATION_CANDIDATES=8
```

---

## 依赖关系

本 Skill 依赖 [academic-search](https://github.com/ustc-ai4science/academic-search) 进行论文检索。

```
auto-citation
    └── academic-search (必需)
        ├── arXiv API
        ├── Semantic Scholar API
        ├── Google Scholar (CDP 浏览器)
        └── CNKI (CDP 浏览器)
```

---

## 支持的文档格式

| 格式 | 扩展名 | 支持程度 | 备注 |
|------|--------|---------|------|
| Markdown | .md | 完全支持 | 推荐 |
| LaTeX | .tex | 完全支持 | BibTeX/thebibliography |
| Word | .docx | 完全支持 | 需 python-docx |
| 纯文本 | .txt | 部分支持 | 提取纯文本 |

---

## 支持的引用格式

| 格式 | 适用场景 | 文中标记 | 文末列表 |
|------|---------|---------|---------|
| **BibTeX** | LaTeX 文档 | `\cite{key}` | .bib 文件 |
| **GB/T 7714** | 中文论文 | `[1], [2]` | 按序号排列 |
| **APA** | 国际期刊 | `(Author, Year)` | 按作者字母排序 |

---

## 相关文档

- [引用格式规范](references/citation-styles.md) - BibTeX/GB7714/APA 详细说明
- [使用场景示例](references/workflow-examples.md) - 6 个典型使用场景
- [academic-search 文档](https://github.com/ustc-ai4science/academic-search) - 底层检索能力

---

## 常见问题

### Q1: 如何确保能找到相关论文？

**A**: 
1. 提供清晰的文章主题或摘要
2. 如搜索结果不理想，可调整关键词或放宽时间范围
3. 指定具体平台（如"找几篇 CVPR 的论文"）

### Q2: 引用格式不正确怎么办？

**A**:
1. 明确指定格式：`"用 GB/T 7714 格式"`
2. 在文件开头添加注释标记：`<!-- citation-style: gb7714 -->`
3. 使用 `format_citation.py` 重新格式化

### Q3: 如何避免重复引用？

**A**: 
- 工具会自动检测文档中已有的引用（DOI/arXiv ID/标题匹配）
- 推荐列表中不会显示已存在的论文

### Q4: 支持批量处理多个文档吗？

**A**: 
- 当前版本支持单文档处理
- 可使用脚本工具批量处理：`for f in *.md; do python scripts/...; done`

---

## 设计理念

> **Skill = 哲学 + 技术事实**

auto-citation 遵循以下设计原则：

1. **人机协作**：AI 负责检索和格式化，用户负责最终确认
2. **灵活输出**：支持多种引用格式，适应不同场景
3. **无缝集成**：与 academic-search 深度集成，复用其平台能力
4. **渐进增强**：基础版本覆盖核心场景，可扩展支持更多格式

---

## 贡献与反馈

欢迎提交 Issue 和 PR：
- 新增引用格式支持
- 改进解析器准确度
- 添加更多使用示例

---

## License

MIT License - 与 academic-search 保持一致

---

## 致谢

本 Skill 基于 [ustc-ai4science/academic-search](https://github.com/ustc-ai4science/academic-search) 构建，感谢其提供的强大检索能力。
