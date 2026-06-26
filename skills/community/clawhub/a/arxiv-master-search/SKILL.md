# arXiv 检索与分析 Skill

## 概述

本 skill 提供强大的 arXiv 学术论文检索、下载和分析功能，帮助智能体高效进行学术文献调研。支持关键词检索、作者检索、日期范围过滤、分类筛选等多种检索方式，并提供批量下载、元数据提取、论文总结等功能。

所有配置均通过命令行参数传入，无需配置文件。可选参数均有合理默认值。

## 目录结构

```
arxiv-search-skill/
├── skill.md                    # 本文件 - 使用说明与规范
├── README.md                   # 快速入门指南
├── requirements.txt            # Python 依赖
├── arxiv_search.py             # 统一入口（可选）
├── scripts/
│   ├── __init__.py
│   ├── utils.py                # 工具函数
│   ├── search.py               # 检索模块
│   ├── download.py             # 下载模块
│   ├── metadata.py             # 元数据处理模块
│   ├── batch_search.py         # 批量检索模块
│   └── summarize.py            # 论文总结模块
├── output/                     # 输出目录
│   ├── pdfs/                   # 下载的 PDF 文件
│   ├── metadata/               # 元数据 JSON 文件
│   └── summaries/              # 生成的摘要文件
└── examples/                   # 使用示例
    ├── example_queries.jsonl
    └── ids.txt
```

## 安装与配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 切换到 scripts 目录

所有脚本在 `scripts/` 目录下运行：

```bash
cd scripts
```

## 核心功能

---

## 1. 检索模块 (search.py)

### 功能
在 arXiv 中按关键词、标题、摘要、作者、分类等检索论文，支持日期范围过滤。

### 使用方法

```bash
python search.py --query "quantum computing" --max-results 50
```

### 命令行参数

#### 检索条件 (至少提供一个)
| 参数 | 简写 | 说明 | 必需 |
|------|------|------|------|
| `--query` | `-q` | 通用查询字符串 | 否 |
| `--title` | `-t` | 标题关键词 | 否 |
| `--abstract` | `-a` | 摘要关键词 | 否 |
| `--author` | `-au` | 作者名 | 否 |
| `--category` | `-c` | arXiv 分类 (如 cs.AI, quant-ph) | 否 |

#### 日期过滤 (可选)
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--start-date` | `-s` | 起始日期 (YYYY-MM-DD) | - |
| `--end-date` | `-e` | 结束日期 (YYYY-MM-DD) | - |

#### 检索控制 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--max-results` | 最大结果数 | 100 |
| `--sort-by` | 排序方式: relevance, lastUpdatedDate, submittedDate | relevance |
| `--sort-order` | 排序顺序: descending, ascending | descending |
| `--timeout` | 请求超时秒数 | 30 |
| `--retry-attempts` | 重试次数 | 3 |

#### 速率限制 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--requests-per-second` | 每秒最大请求数 | 2.0 |
| `--min-delay` | 请求间最小延迟秒数 | 0.5 |

#### 输入输出
| 参数 | 简写 | 说明 |
|------|------|------|
| `--id-list` | - | 从文件读取 arXiv ID 列表进行检索 |
| `--output` | `-o` | 输出元数据 JSON 文件路径 |

#### 日志 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--log-level` | 日志级别: DEBUG, INFO, WARNING, ERROR | INFO |
| `--log-file` | 日志文件路径 | - |

### 高级查询语法

```bash
# 标题中包含关键词
python search.py --query "ti:quantum AND ti:computing"

# 摘要中包含关键词
python search.py --query "abs:machine AND abs:learning"

# 组合条件
python search.py --query "cat:cs.AI AND (ti:neural OR abs:network)"
```

### 使用示例

```bash
# 基础关键词检索
python search.py --query "quantum computing" --max-results 50

# 标题检索
python search.py --title "transformer" --max-results 30

# 作者检索
python search.py --author "Smith, J" --max-results 100

# 分类检索
python search.py --category "cs.AI" --start-date "2023-01-01"

# 组合检索并保存结果
python search.py --query "deep learning" --category "cs.LG" --max-results 50 --output results.json
```

### 输出示例

```json
{
  "search_metadata": {
    "query": "quantum computing",
    "original_query": {
      "query": "quantum computing",
      "title": null,
      "abstract": null,
      "author": null,
      "category": null,
      "start_date": null,
      "end_date": null
    },
    "timestamp": "2023-01-15T10:30:00Z",
    "returned_results": 50
  },
  "papers": [
    {
      "arxiv_id": "2301.01234",
      "arxiv_url": "https://arxiv.org/abs/2301.01234",
      "pdf_url": "https://arxiv.org/pdf/2301.01234.pdf",
      "title": "Quantum Computing for Machine Learning",
      "authors": [
        {"name": "John Smith"},
        {"name": "Alice Johnson"}
      ],
      "abstract": "We present a novel approach...",
      "categories": ["quant-ph", "cs.LG"],
      "primary_category": "quant-ph",
      "published_date": "2023-01-05",
      "updated_date": "2023-01-10",
      "doi": "10.1234/arxiv.2301.01234",
      "journal_ref": null,
      "comments": "15 pages, 5 figures"
    }
  ]
}
```

---

## 2. 下载模块 (download.py)

### 功能
下载单个或批量论文 PDF 文件。

### 使用方法

```bash
python download.py --id 2301.01234
```

### 命令行参数

#### 输入源 (选择一个)
| 参数 | 说明 | 必需 |
|------|------|------|
| `--id` | arXiv ID（可多次指定） | 否 |
| `--id-list` | 包含 arXiv ID 列表的文本文件 | 否 |
| `--metadata` | 包含论文元数据的 JSON 文件 | 否 |

#### 输出选项 (可选)
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--output-dir` | `-o` | 输出目录 | output/pdfs |
| `--skip-existing` | - | 跳过已存在的文件 | 默认启用 |
| `--no-skip-existing` | - | 覆盖已存在的文件 | - |

#### 下载控制 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--parallel` | 并行下载数 | 3 |
| `--chunk-size` | 下载块大小字节 | 8192 |
| `--verify-ssl` | 验证 SSL 证书 | 默认启用 |
| `--no-verify-ssl` | 不验证 SSL 证书 | - |

#### 速率限制 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--requests-per-second` | 每秒最大请求数 | 2.0 |
| `--min-delay` | 请求间最小延迟秒数 | 0.5 |

#### 日志 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--log-level` | 日志级别: DEBUG, INFO, WARNING, ERROR | INFO |
| `--log-file` | 日志文件路径 | - |

### 使用示例

```bash
# 下载单个论文
python download.py --id 2301.01234

# 下载多个论文
python download.py --id 2301.01234 --id 2302.05678

# 从 ID 列表文件下载
python download.py --id-list ids.txt

# 从元数据文件下载
python download.py --metadata results.json

# 指定输出目录
python download.py --id 2301.01234 --output-dir my_papers/

# 强制覆盖已存在的文件
python download.py --id 2301.01234 --no-skip-existing
```

---

## 3. 元数据处理模块 (metadata.py)

### 功能
提取论文元数据，支持多种格式导出（JSON、BibTeX、CSV、RIS），以及合并多个元数据文件。

### 使用方法

```bash
python metadata.py --input results.json --format bibtex --output refs.bib
```

### 命令行参数

#### 输入方式 (选择一个)
| 参数 | 说明 | 必需 |
|------|------|------|
| `--id` | 单个 arXiv ID | 否 |
| `--input` | `-i` | 输入元数据 JSON 文件 | 否 |
| `--merge` | 合并多个元数据文件 | 否 |

#### 输出选项
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--format` | `-f` | 输出格式: json, bibtex, csv, ris | json |
| `--output` | `-o` | 输出文件路径 | - |

#### 日志 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--log-level` | 日志级别: DEBUG, INFO, WARNING, ERROR | INFO |
| `--log-file` | 日志文件路径 | - |

### 使用示例

```bash
# 获取单个论文元数据
python metadata.py --id 2301.01234

# 从元数据文件导出 BibTeX
python metadata.py --input results.json --format bibtex --output refs.bib

# 导出 CSV
python metadata.py --input results.json --format csv --output papers.csv

# 导出 RIS
python metadata.py --input results.json --format ris --output papers.ris

# 合并多个元数据文件
python metadata.py --merge result1.json result2.json --output merged.json
```

### 输出格式

#### BibTeX 格式

```bibtex
@article{smith:2023:quantum,
  title = {Quantum Computing for Machine Learning},
  author = {Smith, John and Johnson, Alice},
  year = {2023},
  month = {01},
  journal = {arXiv preprint 2301.01234},
  eprint = {2301.01234},
  archivePrefix = {arXiv},
  primaryClass = {quant-ph},
  url = {https://arxiv.org/abs/2301.01234},
  abstract = {We present a novel approach...}
}
```

---

## 4. 批量检索模块 (batch_search.py)

### 功能
从 JSONL 文件批量执行多个检索任务。

### 使用方法

```bash
python batch_search.py --input queries.jsonl --output batch_results/
```

### 命令行参数

#### 输入 (必需)
| 参数 | 简写 | 说明 |
|------|------|------|
| `--input` | `-i` | 输入 JSONL 文件路径 |

#### 输出 (可选)
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--output` | `-o` | 输出目录 | output/metadata |
| `--no-individual` | - | 不保存单独的查询结果 | - |

#### 检索控制 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--timeout` | 请求超时秒数 | 30 |
| `--retry-attempts` | 重试次数 | 3 |
| `--requests-per-second` | 每秒最大请求数 | 2.0 |
| `--min-delay` | 请求间最小延迟秒数 | 0.5 |

#### 日志 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--log-level` | 日志级别: DEBUG, INFO, WARNING, ERROR | INFO |
| `--log-file` | 日志文件路径 | - |

### 输入文件格式 (JSONL)

```jsonl
{"query": "deep learning", "max_results": 50}
{"query": "transformer architecture", "category": "cs.CL", "max_results": 30, "name": "transformer_2023"}
{"author": "Bengio, Y", "max_results": 100, "name": "bengio_papers"}
{"category": "cs.AI", "start_date": "2023-01-01", "max_results": 50}
```

JSONL 每行一个查询对象，支持的字段：
- `query` / `q`: 通用查询
- `title` / `t`: 标题关键词
- `abstract` / `a`: 摘要关键词
- `author` / `au`: 作者名
- `category` / `c` / `categories`: 分类
- `start_date` / `start-date` / `s`: 起始日期
- `end_date` / `end-date` / `e`: 结束日期
- `max_results` / `max-results` / `m`: 最大结果数
- `sort_by` / `sort-by`: 排序方式
- `sort_order` / `sort-order`: 排序顺序
- `name`: 查询名称（用于输出文件名）

### 使用示例

```bash
# 从 JSONL 文件运行批量检索
python batch_search.py --input queries.jsonl

# 指定输出目录
python batch_search.py --input queries.jsonl --output batch_results/

# 不保存单独查询结果，只保存合并文件
python batch_search.py --input queries.jsonl --no-individual
```

---

## 5. 论文总结模块 (summarize.py)

### 功能
生成论文摘要和关键点总结，以及文献综述概览。

### 使用方法

```bash
python summarize.py --metadata results.json --overview --topic "deep learning"
```

### 命令行参数

#### 输入方式 (选择一个)
| 参数 | 说明 | 必需 |
|------|------|------|
| `--id` | 单个 arXiv ID | 否 |
| `--metadata` | 包含论文元数据的 JSON 文件 | 否 |

#### 输出选项 (可选)
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--output` | `-o` | 输出文件路径 | - |
| `--output-dir` | - | 输出目录（用于批量模式） | output/summaries |

#### 功能选项 (可选)
| 参数 | 说明 |
|------|------|
| `--overview` | 生成文献综述概览 |
| `--topic` | 研究主题（用于综述） |

#### 日志 (可选)
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--log-level` | 日志级别: DEBUG, INFO, WARNING, ERROR | INFO |
| `--log-file` | 日志文件路径 | - |

### 总结内容

单篇论文总结包括：
- 标题、作者、发表日期
- 分类、URL
- 短摘要（前 500 字符）
- 关键点：
  - 方法关键词
  - 任务关键词
  - 问题陈述
  - 贡献点

文献综述包括：
- 论文集合统计
- 分类分布
- 年份分布
- 方法和任务统计
- 关键洞察

### 使用示例

```bash
# 总结单篇论文
python summarize.py --id 2301.01234

# 从元数据文件批量生成总结
python summarize.py --metadata results.json

# 生成文献综述
python summarize.py --metadata results.json --overview --topic "deep learning" --output overview.json
```

---

## 常见 arXiv 分类

| 分类 | 说明 |
|------|------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language |
| cs.CV | Computer Vision and Pattern Recognition |
| cs.LG | Machine Learning |
| cs.NE | Neural and Evolutionary Computing |
| cs.RO | Robotics |
| quant-ph | Quantum Physics |
| stat.ML | Machine Learning (Statistics) |
| math.OC | Optimization and Control |
| physics.data-an | Data Analysis, Statistics and Probability |

---

## API 使用示例 (Python 模块)

### 基础检索

```python
from search import ArxivSearch

searcher = ArxivSearch()

# 简单关键词检索
results = searcher.search(
    query="transformer architecture",
    max_results=20,
    sort_by="submittedDate"
)

# 高级检索
results = searcher.search(
    query="cat:cs.CL AND abs:transformer",
    start_date="2023-01-01",
    end_date="2023-12-31",
    max_results=50
)
```

### 批量下载

```python
from download import PaperDownloader

downloader = PaperDownloader(output_dir="output/pdfs")

# 下载单个论文
downloader.download_by_id("2301.01234")

# 批量下载
arxiv_ids = ["2301.01234", "2302.05678", "2303.09012"]
papers = [{"arxiv_id": id} for id in arxiv_ids]
downloader.download_batch(papers, skip_existing=True)
```

### 元数据处理

```python
from metadata import MetadataExtractor

extractor = MetadataExtractor()

# 获取元数据
metadata = extractor.get_metadata("2301.01234")

# 导出为 BibTeX
papers = [metadata]
extractor.export_bibtex(papers, "references.bib")
```

---

## 完整工作流示例

```bash
# 1. 定义检索查询列表
cat > my_queries.jsonl << EOF
{"query": "large language model", "max_results": 50, "name": "llm"}
{"query": "chain-of-thought reasoning", "max_results": 30, "name": "cot"}
{"category": "cs.CL", "max_results": 100, "start_date": "2023-01-01", "name": "cl_2023"}
EOF

# 2. 执行批量检索
python batch_search.py --input my_queries.jsonl --output my_results/

# 3. 下载相关论文
python download.py --metadata my_results/merged_metadata.json --output-dir my_pdfs/

# 4. 生成文献综述
python summarize.py --metadata my_results/merged_metadata.json --overview --topic "LLMs" --output llm_overview.json

# 5. 导出 BibTeX
python metadata.py --input my_results/merged_metadata.json --format bibtex --output references.bib
```

---

## 输出规范

### 元数据 JSON 格式规范

见 search.py 输出示例。

### 错误处理规范

所有脚本遵循以下错误码规范：

| 错误码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 通用错误 |
| 2 | 参数错误 |
| 3 | 网络错误 |
| 4 | 文件IO错误 |
| 5 | API 限流 |

### 日志规范

```
[INFO] 2023-01-15 10:30:00 - Starting search for query: "quantum computing"
[INFO] 2023-01-15 10:30:02 - Found 1500 results, returning first 50
[WARNING] 2023-01-15 10:30:03 - Rate limit approaching, slowing down
[ERROR] 2023-01-15 10:30:05 - Failed to download 2301.01234: Connection timeout
```

---

## 高级技巧

### 1. 检索优化

- 使用引号进行精确匹配: `"graph neural network"`
- 使用通配符: `transformer*`
- 使用布尔运算符: `AND`, `OR`, `ANDNOT`
- 字段限定: `ti:`, `abs:`, `au:`, `cat:`

### 2. 分类组合

```bash
# 多个分类
python search.py --query "cat:cs.AI OR cat:cs.LG"

# 排除分类
python search.py --query "cat:cs.* ANDNOT cat:cs.RO"
```

### 3. 时间范围检索

```bash
# 最近一个月 (Linux/Mac)
python search.py --query "deep learning" --start-date "$(date -d '1 month ago' +%Y-%m-%d)"

# 特定年份
python search.py --query "transformer" --start-date "2023-01-01" --end-date "2023-12-31"
```

---

## 常见问题

### Q: 如何提高检索速度？
A: 使用 `--max-results` 限制返回数量，使用分类过滤减少结果集。

### Q: 遇到 rate limit 怎么办？
A: 脚本会自动处理限流。可通过 `--requests-per-second` 和 `--min-delay` 调整速率限制参数。

### Q: 下载的 PDF 文件名格式是什么？
A: 默认格式: `{arxiv_id}_{title_slug}.pdf`，例如: `2301.01234_quantum-computing-for-machine-learning.pdf`

### Q: 所有参数都有默认值吗？
A: 是的，所有可选参数都有合理的默认值。只需提供必需参数（如检索条件、输入源等）即可。

---

## 更新日志

### v1.1.0
- 移除配置文件，所有配置改为命令行参数
- 所有可选参数添加默认值
- 更新文档，添加完整参数说明

### v1.0.0
- 初始版本发布
- 支持基础检索、下载、元数据提取
- 支持批量操作
