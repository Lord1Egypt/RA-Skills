# 使用场景示例

本文档展示 auto-citation skill 在不同场景下的典型使用流程。

---

## 场景一：完善学术论文引言

### 背景
你正在撰写一篇关于"图神经网络在时间序列预测中的应用"的论文，引言部分需要补充相关工作引用。

### 原文（LaTeX）

```latex
\section{Introduction}

Time series forecasting is a fundamental problem in machine learning with 
applications in finance, weather prediction, and traffic management. 
Recent years have witnessed the rapid development of deep learning methods 
for this task. However, capturing complex temporal dependencies remains 
a challenging problem.

In this paper, we propose a novel graph neural network approach...
```

### 用户指令

```
给引言部分加一些背景文献，主要是时间序列预测和GNN方面的
```

### AI 执行流程

1. **解析文档**
   - 主题：GNN + 时间序列预测
   - 关键词：`graph neural network`, `time series forecasting`, `temporal dependencies`
   - 现有引用：无
   - 建议 query：`graph neural network time series`, `deep learning time series forecasting`

2. **搜索论文**
   - arXiv: 近 5 年相关论文
   - Semantic Scholar: 高引用相关工作
   - 筛选出 8 篇候选

3. **推荐候选**

```
基于你的引言内容，我找到以下相关背景文献：

[1] **Spatio-Temporal Graph Neural Networks** - 被引 320 次 (2021)
    作者：Yu et al.
    相关点：全面的时空 GNN 综述，适合作为领域背景
    
[2] **Long-term Time Series Forecasting with Transformers** - 被引 280 次 (2022)
    作者：Zhou et al.
    相关点：时间序列预测的深度学习方法综述
    
[3] **Graph WaveNet** - 被引 450 次 (2019)
    作者：Wu et al.
    相关点：交通预测的 GNN 经典工作，可作为 baseline 引用
    
[4] **STGNN for Multi-step Prediction** - 被引 180 次 (2023) [新]
    作者：Li et al.
    相关点：最新的多步预测方法，展示领域进展

请选择你想引用的论文编号（如：1,2,3）
```

4. **用户选择**

```
用户：选 1, 2, 3，用 BibTeX 格式
```

5. **生成并插入引用**

AI 生成 BibTeX 条目并插入到 .bib 文件，同时在引言中添加 `\cite{}` 命令。

### 最终输出

**引言更新为：**

```latex
\section{Introduction}

Time series forecasting is a fundamental problem in machine learning with 
applications in finance, weather prediction, and traffic management. 
Recent years have witnessed the rapid development of deep learning methods 
for this task \cite{zhou2022transformers}, including various neural network 
architectures \cite{wu2019graphwavenet}. However, capturing complex temporal 
dependencies remains a challenging problem.

Graph neural networks (GNNs) have emerged as a powerful tool for modeling 
spatial-temporal data \cite{yu2021stgnn}. In this paper, we propose a novel 
graph neural network approach...
```

**references.bib 新增：**

```bibtex
@article{yu2021stgnn,
  title = {Spatio-Temporal Graph Neural Networks},
  author = {Yu, B. and Yin, H. and Zhu, Z.},
  journal = {IEEE Transactions on Knowledge and Data Engineering},
  year = {2021},
  doi = {10.1109/TKDE.2021.1234567}
}

@inproceedings{zhou2022transformers,
  title = {Long-term Time Series Forecasting with Transformers},
  author = {Zhou, H. and Zhang, S. and Peng, J.},
  booktitle = {ICLR},
  year = {2022}
}

@inproceedings{wu2019graphwavenet,
  title = {Graph WaveNet for Deep Spatial-Temporal Graph Modeling},
  author = {Wu, Z. and Pan, S. and Long, G. and others},
  booktitle = {IJCAI},
  year = {2019}
}
```

---

## 场景二：技术博客补充引用

### 背景
你写了一篇关于 Transformer 的博客文章，想为关键观点添加学术引用。

### 原文（Markdown）

```markdown
# Transformer 详解：从 Attention 到 BERT

Transformer 架构自 2017 年提出以来，彻底改变了 NLP 领域。
它完全基于注意力机制，摒弃了传统的 RNN 和 CNN 结构。

BERT 进一步扩展了 Transformer 的应用...
```

### 用户指令

```
给这篇文章加一些关键论文引用，用 GB/T 7714 格式
```

### AI 执行流程

1. **解析文档**
   - 主题：Transformer, Attention, BERT
   - 关键词：`transformer`, `attention`, `bert`
   - 识别关键论文需求：原始 Transformer 论文、BERT 论文

2. **精确检索**
   - `arxiv:1706.03762` (Attention is All You Need)
   - `arxiv:1810.04805` (BERT)

3. **推荐候选**

```
找到以下核心论文：

[1] **Attention Is All You Need** - 被引 52000+ 次 (2017)
    作者：Vaswani et al.
    相关点：Transformer 原始论文，适合介绍架构起源
    
[2] **BERT: Pre-training of Deep Transformers** - 被引 38000+ 次 (2019)
    作者：Devlin et al.
    相关点：BERT 论文，适合介绍预训练概念

确认添加这 2 篇？（是/否/更多）
```

4. **用户确认**

```
用户：确认，添加到文末
```

5. **生成并插入**

### 最终输出

**文章末尾新增：**

```markdown
## 参考文献

[1] Vaswani A, Shazeer N, Parmar N, 等. Attention is All You Need[C]. NeurIPS, 2017.

[2] Devlin J, Chang M W, Lee K, 等. BERT: Pre-training of Deep Bidirectional Transformers[J]. 
    NAACL, 2019.
```

---

## 场景三：实验部分补充 baseline

### 背景
你的论文实验部分需要引用对比方法的相关论文。

### 原文片段

```latex
\section{Experiments}

\subsection{Baselines}

We compare our proposed method against the following baselines:
\begin{itemize}
    \item LSTM: A classic RNN-based method
    \item GRU: A gated recurrent unit variant
    \item Transformer: The standard transformer architecture
    \item Informer: An efficient transformer variant
\end{itemize}
```

### 用户指令

```
给这些 baseline 方法加具体引用，每个都要有出处
```

### AI 执行流程

1. **解析需求**
   - 需要 4 篇特定论文的引用
   - 格式：BibTeX

2. **精准检索**

针对每个 baseline 搜索：
- `LSTM Hochreiter Schmidhuber 1997`
- `GRU Cho 2014`
- `Transformer Vaswani 2017`
- `Informer Zhou 2021 AAAI`

3. **推荐确认**

```
找到以下 baseline 论文：

LSTM:
[1] Hochreiter S, Schmidhuber J. Long Short-Term Memory[J]. Neural Computation, 1997.

GRU:
[2] Cho K, van Merriënboer B, Gulcehre C, 等. Learning Phrase Representations 
    using RNN Encoder–Decoder for Statistical Machine Translation[C]. EMNLP, 2014.

Transformer:
[3] Vaswani A, 等. Attention is All You Need[C]. NeurIPS, 2017.

Informer:
[4] Zhou H, Zhang S, Peng J, 等. Informer: Beyond Efficient Transformer for 
    Long Sequence Time-Series Forecasting[C]. AAAI, 2021.

全部确认？
```

4. **插入引用**

AI 生成 BibTeX 并更新正文中的 baseline 列表。

### 最终输出

```latex
\subsection{Baselines}

We compare our proposed method against the following baselines:
\begin{itemize}
    \item LSTM \cite{hochreiter1997lstm}: A classic RNN-based method
    \item GRU \cite{cho2014gru}: A gated recurrent unit variant
    \item Transformer \cite{vaswani2017attention}: The standard transformer architecture
    \item Informer \cite{zhou2021informer}: An efficient transformer variant
\end{itemize}
```

---

## 场景四：中文毕业论文格式转换

### 背景
你有一篇英文论文需要改成中文毕业论文格式（GB/T 7714）。

### 原始引用（APA 格式）

```
Wang, X., & Li, Y. (2023). Graph neural networks for time series prediction. 
    Journal of ML, 45(3), 100-120.
```

### 用户指令

```
把这些引用转成 GB/T 7714 格式
```

### AI 执行流程

1. **格式识别**
   - 当前：APA 格式
   - 目标：GB/T 7714

2. **逐条转换**

**转换结果：**

```
[1] Wang X, Li Y. Graph neural networks for time series prediction[J]. 
    Journal of ML, 2023, 45(3): 100-120.
```

### 中文论文特殊处理

如果涉及中文文献：

```
[2] 张三, 李四. 深度学习在时间序列预测中的应用[J]. 计算机学报, 2022, 45(8): 2000-2015.
```

---

## 场景五：快速引用单篇论文

### 背景
你知道某篇论文的信息，需要快速添加完整引用。

### 用户指令

```
帮我引用这篇论文：arxiv 2401.12345，用 GB/T 7714 格式
```

### AI 执行流程

1. **直接查询 arXiv**
   - 调用 academic-search 获取 arxiv:2401.12345 元数据

2. **生成引用**

```
生成引用：

[1] Zhang S, Liu J, Wang W. Transformer-based Methods for Long-term Forecasting[EB/OL]. 
    arXiv:2401.12345, 2024. https://arxiv.org/abs/2401.12345
```

3. **询问插入位置**

```
是否要插入到当前文档？如果是，请提供文件路径。
```

---

## 场景六：Word 文档引用

### 背景
你在写 Word 格式的综述报告。

### 用户指令

```
给这个 Word 文档加 5 篇 GNN 相关引用
文档路径：report.docx
```

### AI 执行流程

1. **解析 Word 文档**
   - 使用 python-docx 提取内容
   - 主题：图神经网络综述

2. **搜索并推荐**

3. **生成引用**
   - 格式：GB/T 7714（Word 默认推荐）

4. **插入文档**
   - 在文档末尾添加"参考文献"章节
   - 使用 Word 样式格式化

### 最终效果

Word 文档末尾：

```
参考文献

[1] Kipf T N, Welling M. Semi-supervised Classification with Graph Convolutional Networks[C]. 
    ICLR, 2017.
[2] Veličković P, Cucurull G, Casanova A, 等. Graph Attention Networks[C]. ICLR, 2018.
...
```

---

## 使用建议

### 选择合适的工作模式

| 场景 | 推荐模式 | 理由 |
|------|---------|------|
| 完善引言 | 全自动推荐 | 需要探索相关领域 |
| 补充 baseline | 定向补充 | 目标明确 |
| 已知论文信息 | 精确匹配 | 快速定位 |
| 格式转换 | 全自动 | 纯格式操作 |

### 优化搜索结果

如果推荐不精准：
1. 提供更具体的主题描述
2. 指定年份范围（如"近 3 年"）
3. 指定具体平台（如"找几篇 CVPR 的论文"）
4. 排除某些关键词（如"不要 survey"）

### 引用数量建议

| 文档类型 | 建议引用数 | 分布 |
|---------|-----------|------|
| 技术博客 | 3-5 篇 | 核心论文 |
| 会议论文 | 15-25 篇 | 背景 + 方法 + baseline |
| 期刊论文 | 30-50 篇 | 全面覆盖 |
| 学位论文 | 50-100 篇 | 系统性综述 |

---

## 故障排除

### 搜索结果为空

**可能原因**：
- 关键词太具体
- 时间范围限制太严格
- 平台限制（如只用 arXiv 搜医学论文）

**解决方案**：
```
"放宽时间范围到 10 年"
"也搜索一下 Google Scholar"
"用同义词再搜一遍"
```

### 推荐不够相关

**解决方案**：
```
"侧重找方法类的论文，不要综述"
"找交通预测方向的，不是通用 GNN"
"需要中文文献"
```

### 格式不正确

**解决方案**：
```
"用 GB/T 7714 的会议论文格式重新生成"
"作者名需要全大写"
"加上 DOI 链接"
```
