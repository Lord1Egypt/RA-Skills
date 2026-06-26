# arXiv Paper Resolver

> 自动提取 arXiv 论文章节结构、下载 PDF、解析 HTML 全文，生成按论文自身章节结构编排的中文文档。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

## 📌 功能

- **自动解析**：从 arXiv HTML 实验版（`arxiv.org/html/`）提取论文全文
- **章节拆分**：按 h2 主节 + h3 子节结构拆分为独立文件，跳过 References / Appendix
- **PDF 下载**：自动下载论文 PDF
- **元数据提取**：标题、作者、摘要、arXiv 信息
- **中文文档生成**：支持 LLM 逐章翻译为中文 MD 文档（`$...$` 公式、兼容 Typora）
- **目录归档**：按论文标题自动创建 slug 目录，文件结构清晰

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/jin-liquor/arxiv-paper-resolver.git
cd arxiv-paper-resolver
pip install -r scripts/requirements.txt
```

### 使用

```bash
# 通过 arXiv ID
python3 scripts/arxiv_section_extractor.py 2604.25836

# 通过 URL
python3 scripts/arxiv_section_extractor.py https://arxiv.org/abs/2604.25836

# 指定输出目录
python3 scripts/arxiv_section_extractor.py 2604.25836 -o ~/my_papers

# 通过环境变量配置输出目录
export ARXIV_PAPERS_DIR=~/my_papers
python3 scripts/arxiv_section_extractor.py 2604.25836
```

## 📁 输出结构

```
{output_dir}/{paper-title-slug}/
├── {arxiv_id}.pdf                    ← 原始 PDF
├── {arxiv_id}_metadata.json          ← 元数据（标题、作者、分类等）
├── {arxiv_id}_section_structure.txt  ← 章节结构总览
├── {arxiv_id}_中文文档.md            ← 中文翻译文档（由 LLM 生成）
└── {arxiv_id}_raw_sections/          ← 各章节原文
    ├── 00_abstract.txt
    ├── 01_Introduction.txt
    ├── 02_Method.txt
    └── ...
```

## 🛠️ 与 LLM / AI Agent 搭配使用

本工具设计为 AI Agent 的论文处理前段。典型工作流：

```
用户: "帮我读这篇论文 https://arxiv.org/abs/2604.25836"

Agent:
  1. 运行 extractor 脚本 → 提取章节 + 下载 PDF
  2. 读取各章节原文
  3. 逐章翻译为中文，保持 LaTeX 公式不变
  4. 生成中文 MD 文档

用户: "做成 PPT"
Agent: 基于中文文档生成 HTML 演示文稿
```

可作为 Hermes Agent、Claude Code、Codex 等 AI Agent 的 skill 集成。

## 📋 依赖

- Python 3.8+
- `requests` — HTTP 请求
- `beautifulsoup4` — HTML 解析
- `urllib3` — HTTP 底层库（requests 依赖）

## ⚠️ 注意事项

- PDF 下载失败不影响章节提取流程
- HTML 获取失败会终止流程（自动尝试 `v1` 和裸 ID 两种地址）
- 脚本自动跳过 References、Appendix、Supplementary 等附录章节
- arXiv HTML 实验版（`arxiv.org/html/`）格式可能随 arXiv 更新而变化

## 🤝 贡献

欢迎提交 Issue 和 PR！可贡献方向：

- 多语言翻译支持
- BibTeX 自动生成
- 公式 / 图表提取
- 批量解析
- 与 Obsidian / Notion 等笔记工具集成

## 📄 许可

MIT License
