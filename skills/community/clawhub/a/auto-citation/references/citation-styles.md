# 引用格式规范速查

本文档详细说明支持的三种引用格式及其使用场景。

---

## BibTeX 格式

### 适用场景
- LaTeX 文档
- 需要灵活切换引用样式（plain/unsrt/alpha/ieee/acl）
- 与 Zotero/JabRef 等文献管理工具集成

### 条目类型

| 类型 | 使用场景 | 必需字段 |
|------|---------|---------|
| `@article` | 期刊论文 | title, author, journal, year |
| `@inproceedings` | 会议论文 | title, author, booktitle, year |
| `@misc` | 预印本/技术报告 | title, author, year, eprint |
| `@book` | 书籍 | title, author, publisher, year |
| `@phdthesis` | 学位论文 | title, author, school, year |

### 示例输出

```bibtex
@inproceedings{wang2023gnn,
  title = {Graph Neural Networks for Time Series Prediction},
  author = {Wang, X. and Li, Y.},
  booktitle = {NeurIPS},
  year = {2023},
  pages = {1000--1010},
  doi = {10.5555/1234567}
}

@misc{zhang2024transformer,
  title = {Transformer-based Methods for Long-term Forecasting},
  author = {Zhang, S. and Liu, J.},
  year = {2024},
  eprint = {2401.12345},
  eprinttype = {arXiv}
}
```

### 文中引用

```latex
% 单篇引用
\cite{wang2023gnn}

% 多篇引用
\cite{wang2023gnn,zhang2024transformer}

% 引用并显示页码
\cite[pp. 100]{wang2023gnn}

% 作者 (年份) 格式（需 natbib 宏包）
\citet{wang2023gnn}  % Wang et al. (2023)
\citep{wang2023gnn}  % (Wang et al., 2023)
```

### 完整 LaTeX 示例

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{natbib}  % 或 \usepackage[numbers]{natbib}

\begin{document}

% 正文中的引用
Recent work has explored graph neural networks for time series forecasting \cite{wang2023gnn,zhang2024transformer}.

% 参考文献列表（在 document 末尾）
\bibliographystyle{plain}  % 可选: plain, unsrt, alpha, ieee, acl
\bibliography{references}

\end{document}
```

---

## GB/T 7714 格式（中国国家标准）

### 适用场景
- 中文学位论文（硕士/博士）
- 中文期刊投稿
- 国内学术会议
- 符合中国高校毕业论文规范

### 基本格式

**文中引用**：上标 `[1]`、`[2-4]`、`[1,3,5]`

**文末列表**：按文中出现顺序编号

### 各类文献格式

#### 期刊论文 [J]

```
[1] 作者. 标题[J]. 期刊名, 年份, 卷(期): 页码.
```

示例：
```
[1] 张三, 李四. 基于图神经网络的时间序列预测方法[J]. 计算机学报, 2023, 46(5): 100-120.
```

#### 会议论文 [C]

```
[2] 作者. 标题[C]. 会议名称, 地点, 年份: 页码.
```

示例：
```
[2] Wang X, Li Y. Graph Neural Networks for Time Series Prediction[C]. NeurIPS, 2023: 1000-1010.
```

#### 学位论文 [D]

```
[3] 作者. 标题[D]. 保存地点: 保存单位, 年份.
```

示例：
```
[3] 王五. 深度学习在时间序列分析中的应用研究[D]. 北京: 清华大学, 2022.
```

#### 预印本/电子文献 [EB/OL]

```
[4] 作者. 标题[EB/OL]. arXiv:编号, 年份. https://arxiv.org/abs/编号
```

示例：
```
[4] Zhang S, Liu J. Transformer-based Methods for Long-term Forecasting[EB/OL]. arXiv:2401.12345, 2024. https://arxiv.org/abs/2401.12345
```

### 作者格式规则

| 作者数量 | 格式 | 示例 |
|---------|------|------|
| 1 人 | 全名 | 张三 |
| 2 人 | 全名, 全名 | 张三, 李四 |
| 3 人 | 全名, 全名, 全名 | 张三, 李四, 王五 |
| 4+ 人 | 前 3 人 + "等" | 张三, 李四, 王五, 等 |

### 西文作者格式

- 名在前，姓在后
- 名缩写，姓完整
- 示例：`J. Smith`, `A. B. Johnson`

---

## APA 格式（第 7 版）

### 适用场景
- 国际期刊投稿（心理学、社会科学）
- 英文毕业论文
- APA 风格的学术写作

### 基本格式

**文中引用**：作者-年份制
- 单作者：`(Smith, 2023)`
- 双作者：`(Smith & Jones, 2023)`
- 三作者及以上：`(Smith et al., 2023)`

**文末列表**：按作者姓氏字母顺序排列

### 各类文献格式

#### 期刊论文

```
Author, A. A., & Author, B. B. (Year). Title of article. *Title of Journal*, *volume*(issue), page range. https://doi.org/xx.xxx/xxxx
```

示例：
```
Wang, X., & Li, Y. (2023). Graph neural networks for time series prediction. *Journal of Machine Learning*, *45*(3), 100-120. https://doi.org/10.1037/jml0000123
```

#### 会议论文

```
Author, A. A. (Year). Title of paper. In *Proceedings of Conference* (pp. XX-XX). Publisher. https://doi.org/xx.xxx/xxxx
```

示例：
```
Wang, X., & Li, Y. (2023). Graph neural networks for time series prediction. In *Proceedings of NeurIPS 2023* (pp. 1000-1010). Curran Associates. https://doi.org/10.5555/1234567
```

#### 预印本（arXiv）

```
Author, A. A. (Year). Title of preprint. *arXiv*. https://arxiv.org/abs/XXXX.XXXXX
```

示例：
```
Zhang, S., & Liu, J. (2024). Transformer-based methods for long-term forecasting. *arXiv*. https://arxiv.org/abs/2401.12345
```

### 文中引用详细规则

| 情况 | 首次引用 | 后续引用 |
|------|---------|---------|
| 1 作者 | (Smith, 2023) | (Smith, 2023) |
| 2 作者 | (Smith & Jones, 2023) | (Smith & Jones, 2023) |
| 3 作者 | (Smith, Jones, & Lee, 2023) | (Smith et al., 2023) |
| 4+ 作者 | (Smith et al., 2023) | (Smith et al., 2023) |
| 机构 | (National Institute, 2023) | (NIA, 2023) |

### 特殊规则

1. **同作者同年多篇**：在年份后加小写字母 `(Smith, 2023a)`, `(Smith, 2023b)`
2. **多引用排序**：按作者字母顺序 `(Jones, 2022; Smith, 2023; Wang, 2021)`
3. **引用在句中**：`Smith (2023) found that...`
4. **引用在句末**：`...found significant results (Smith, 2023).`

---

## 格式选择指南

### 按文档类型选择

| 文档类型 | 推荐格式 | 理由 |
|---------|---------|------|
| LaTeX 论文 | BibTeX | 与 LaTeX 原生集成 |
| 中文毕业论文 | GB/T 7714 | 符合国家标准 |
| 英文期刊投稿 | APA / 期刊指定 | 国际通用 |
| 技术博客 | GB/T 7714 / APA | 简洁清晰 |
| 学位论文（国内）| GB/T 7714 | 学校要求 |
| 学位论文（国外）| APA | 学校要求 |

### 按学科选择

| 学科领域 | 推荐格式 |
|---------|---------|
| 计算机科学 | BibTeX / GB/T 7714 |
| 心理学 | APA |
| 社会科学 | APA |
| 工程技术 | GB/T 7714 / IEEE |
| 医学 | Vancouver / APA |
| 自然科学 | GB/T 7714 / Nature/Science 格式 |

---

## 常见问题 (FAQ)

### Q1: 如何切换引用格式？

**A**: 
- **BibTeX**: 修改 `\bibliographystyle{...}` 行
- **其他格式**: 需重新生成引用文本

### Q2: 同一文档可以使用多种格式吗？

**A**: 不建议。全文应保持一致格式。如需转换，使用 `format_citation.py` 重新格式化。

### Q3: 中文作者姓名在 GB/T 7714 中如何排列？

**A**: 中文作者保持原顺序，西文作者姓在前名在后。
示例：`张三, 李四, Smith J A`

### Q4: 如何引用没有 DOI 的论文？

**A**: 
- **BibTeX**: 省略 doi 字段或使用 url 字段
- **GB/T 7714**: 省略 DOI 链接或使用 URL
- **APA**: 使用 URL 或数据库名称

### Q5: arXiv 论文如何引用？

**A**:
- **BibTeX**: 使用 `@misc` 类型，包含 `eprint` 和 `eprinttype`
- **GB/T 7714**: 使用 `[EB/OL]` 类型，标注 arXiv 编号
- **APA**: 标注为预印本，包含 arXiv URL

---

## 工具使用示例

### 生成 BibTeX 格式

```bash
python scripts/format_citation.py \
  --style bibtex \
  --papers papers.json \
  --output references.bib
```

### 生成 GB/T 7714 格式

```bash
python scripts/format_citation.py \
  --style gb7714 \
  --papers papers.json \
  --output references.txt
```

### 生成 APA 格式（含文中标记）

```bash
python scripts/format_citation.py \
  --style apa \
  --papers papers.json \
  --with-markers \
  --output references.txt
```

---

## 参考资源

- [GB/T 7714-2015 官方标准](https://www.tsinghua.edu.cn/)
- [APA Style 第7版官网](https://apastyle.apa.org/)
- [BibTeX 格式说明](http://www.bibtex.org/Format/)
