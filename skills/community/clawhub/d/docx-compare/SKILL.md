---
name: DOCX Compare / Duplicate Check
slug: docx-compare
version: 1.0.2
homepage: https://clawhub.com/skills/docx-compare
description: "Compare two Word documents (DOCX) to find duplicate text paragraphs and duplicate images. Supports exact string matching, fuzzy matching (difflib), and image MD5 hash comparison. Outputs highlighted DOCX files and a detailed text report. Use when: (1) a user asks to check or compare duplicate content between two Word documents; (2) review for content overlap, version comparison, or plagiarism detection; (3) need to locate duplicated images across documents."
changelog: |
  v1.0.2 — Fix crash on `pars2` typo (should be `paras2`) + escape sequence cleanups
  v1.0.1 — Fix image comment injection: double XML declaration from etree.tostring(standalone=True), and skip of new comments.xml in ZIP output. Add SyntaxWarning fix for invalid escape sequence.
  v1.0.0 — Initial release — text exact/fuzzy dedup, image duplicate detection via MD5 hash, annotated DOCX output and report.
metadata: {"clawdbot":{"emoji":"📑","os":["win32"]}}
---

# DOCX 文档查重工具

比较两个 Word 文档（.docx），找出重复的文本段落和重复的图片。

## 什么时候用

- 用户说"帮我查一下这两个 Word 文档内容有没有重复"
- 比较同一文档的不同版本，找出新增/重复内容
- 需要定位跨文档的重复图片

## 快速开始

```bash
# 最基本用法：比较两个 docx
python scripts/compare_docx.py --file1 文档A.docx --file2 文档B.docx

# 指定输出目录
python scripts/compare_docx.py --file1 文档A.docx --file2 文档B.docx --output ./对比结果
```

## 功能说明

| 模式 | 说明 | 阈值 |
|---|---|---|
| **精确匹配** | 标准化后完全相同的段落 | 100% |
| **模糊匹配** | 相似度超过阈值的段落 | ≥95% |
| **图片查重** | 通过 MD5 哈希值比较图片 | 100% |

## 输出

- `*_标记重复.docx` — 高亮标记了重复文字的原始文档
- `*_标记图片重复.docx` — 标注了重复图片的原始文档
- `*_重复报告.txt` — 纯文本详细对比报告

## 脚本参数

```
python scripts/compare_docx.py \
  --file1 <路径>          # 必需：第一个文档
  --file2 <路径>          # 必需：第二个文档
  --output <目录>         # 可选：输出目录（默认同目录）
  --mode all|text|image   # 可选：检查模式（默认 all）
  --threshold 0.95        # 可选：模糊匹配相似度阈值（默认 0.95）
```

## 依赖

- `python-docx` 用于读写 DOCX 文件
- `difflib`（标准库）用于模糊匹配
- `hashlib`（标准库）用于图片 MD5 计算

安装依赖：
```bash
pip install python-docx
```

## 常见陷阱

- 仅支持 `.docx` 格式，不支持旧版 `.doc`（需要先转换）
- 图片重复检测基于文件内容（MD5），同一张图被不同文件名存储会被判定为重复
- 段落模糊匹配使用 `difflib.SequenceMatcher`，CPU 开销随段落数平方增长
- 输出 DOCX 使用黄色高亮标记，不会修改原始文档
- 中文段落含混合标点时，模糊匹配效果可能低于预期

## 相关 Skill

- `word-docx` — 通用 Word 文档创建、编辑、格式调整

## Feedback

- 如果觉得有用：`clawhub star docx-compare`
- 保持更新：`clawhub sync`
