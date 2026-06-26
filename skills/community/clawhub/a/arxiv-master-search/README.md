# arXiv 检索与分析 Skill

一个功能完善的 arXiv 学术论文检索、下载和分析工具集，帮助智能体高效进行文献调研。

## 功能特性

- **多种检索方式**: 关键词、标题、摘要、作者、分类、日期范围
- **批量操作**: 支持批量检索、批量下载
- **格式导出**: JSON、BibTeX、CSV、RIS 格式
- **智能分析**: 论文总结、文献综述、趋势分析
- **速率限制**: 内置限流保护，避免被 arXiv 封禁
- **无需配置文件**: 所有配置通过命令行参数传入，带默认值

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 切换到 scripts 目录

```bash
cd scripts
```

### 基础检索

```bash
# 关键词检索
python search.py --query "quantum computing" --max-results 50

# 保存结果到文件
python search.py --query "deep learning" --output results.json
```

### 下载论文

```bash
# 下载单个论文
python download.py --id 2301.01234

# 从元数据文件批量下载
python download.py --metadata results.json
```

### 导出参考文献

```bash
# 导出 BibTeX
python metadata.py --input results.json --format bibtex --output refs.bib

# 导出 CSV
python metadata.py --input results.json --format csv --output papers.csv
```

### 批量检索

```bash
# 从 JSONL 文件执行批量检索
python batch_search.py --input ../examples/example_queries.jsonl
```

## 目录结构

```
arxiv-search-skill/
├── skill.md                    # 完整使用说明与规范
├── README.md                   # 本文件
├── requirements.txt            # Python 依赖
├── scripts/
│   ├── search.py               # 检索模块
│   ├── download.py             # 下载模块
│   ├── metadata.py             # 元数据处理模块
│   ├── batch_search.py         # 批量检索模块
│   ├── summarize.py            # 论文总结模块
│   └── utils.py                # 工具函数
├── output/                     # 输出目录
│   ├── pdfs/                   # 下载的 PDF 文件
│   ├── metadata/               # 元数据 JSON 文件
│   └── summaries/              # 生成的摘要文件
└── examples/                   # 示例文件
    ├── example_queries.jsonl
    └── ids.txt
```

## 模块说明

| 模块 | 功能 |
|------|------|
| **search.py** | 论文检索（关键词、作者、分类、日期） |
| **download.py** | 论文 PDF 下载（单个/批量） |
| **metadata.py** | 元数据处理（BibTeX/CSV/RIS 导出） |
| **batch_search.py** | 批量检索（JSONL 输入） |
| **summarize.py** | 论文总结与文献综述 |

所有模块都支持 `--help` 查看完整参数列表。

## 快速参数参考

### search.py
```bash
python search.py --query "关键词" --max-results 50 --output results.json
```

### download.py
```bash
python download.py --id arXivID --output-dir my_papers/
```

### metadata.py
```bash
python metadata.py --input results.json --format bibtex --output refs.bib
```

### batch_search.py
```bash
python batch_search.py --input queries.jsonl --output batch_results/
```

### summarize.py
```bash
python summarize.py --metadata results.json --overview --topic "研究主题"
```

## 详细文档

请参考 [skill.md](./skill.md) 查看完整的使用说明、参数文档、API 文档和输出规范。

## 常见 arXiv 分类

| 分类 | 说明 |
|------|------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language |
| cs.CV | Computer Vision |
| cs.LG | Machine Learning |
| cs.NE | Neural and Evolutionary Computing |
| quant-ph | Quantum Physics |
| stat.ML | Machine Learning (Statistics) |

## 完整工作流示例

```bash
cd scripts

# 1. 定义检索查询
cat > my_queries.jsonl << EOF
{"query": "large language model", "max_results": 50, "name": "llm"}
{"query": "chain-of-thought", "max_results": 30, "name": "cot"}
EOF

# 2. 执行批量检索
python batch_search.py --input my_queries.jsonl --output my_results/

# 3. 下载论文
python download.py --metadata my_results/merged_metadata.json

# 4. 生成文献综述
python summarize.py --metadata my_results/merged_metadata.json --overview --topic "LLMs" --output llm_overview.json

# 5. 导出 BibTeX
python metadata.py --input my_results/merged_metadata.json --format bibtex --output references.bib
```

## 许可证

本项目提供用于学术研究目的。
