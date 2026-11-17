---
name: doc-reader
description: |
  本地文档读取技能。从 PDF / DOCX / TXT 抽取纯文本与结构（标题/段落/表格），供摘要、检索、结构化抽取下游使用。内置 doc_extract 脚本（优先本地库，无依赖时回退提示）。适用于合同/简历/报告解析、知识入库、长文预处理。
version: 1.0.0
author: WorkBuddy
agent_created: true
visibility: "public"
tags:
  - pdf
  - docx
  - 文档读取
  - 文本抽取
  - 解析
---

# doc-reader — 本地文档读取

_把 PDF/DOCX 变成"代码能读的文本"，是摘要、检索、结构化抽取的前置环节。_

## 支持格式与依赖
| 格式 | 库 | 安装 |
|------|----|------|
| .pdf | `pypdf` / `PyPDF2` | `pip install pypdf` |
| .docx | `python-docx` | `pip install python-docx` |
| .txt/.md | 内置 | 无 |

## 脚本用法
```bash
# 抽取全文
python scripts/doc_extract.py 报告.pdf --out 报告.txt

# 抽取并保留结构（标题/段落），输出 JSON
python scripts/doc_extract.py 简历.docx --json --out 简历.json

# 只抽前 N 页/段（大文档预览）
python scripts/doc_extract.py 长篇.pdf --max 5
```

## 工作流衔接
1. **读取**：doc_extract 拿到文本/结构
2. **下游**：
   - 长文 → `long-text-summarizer` 分块摘要
   - 字段 → `structured-extraction` 抽 JSON
   - 翻译 → `translate-polish`
3. **知识管理**：抽取结果写入笔记/知识库

## 常见坑
- 扫描版 PDF（无文本层）→ 需先 OCR（依赖外部工具，标记 needs_web）
- DOCX 表格 → python-docx 可逐表读取行列
- 编码 → 统一 utf-8，避免乱码

## 自我进化学习系统
```bash
python scripts/learner.py record <技能目录> --capability pdf抽取 --note "pypdf 比 PyPDF2 更稳"
python scripts/learner.py record <技能目录> --capability docx表格 --fail --error 合并单元格 --note "表格含合并单元格需展平"
python scripts/learner.py insight <技能目录>
python scripts/learner.py reflect <技能目录>
```
记忆落盘 `learned_patterns.json`。

## 安全边界
- 仅读取本人/授权文档；不处理密级、个人隐私文件。
- 不将文档内容外发到第三方，除非已脱敏。
