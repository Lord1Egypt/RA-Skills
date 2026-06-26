---
name: academic-paper-citation
description: 学术论文引用自动化处理工具。用于处理中文学术论文（特别是硕士/博士论文）的引用管理工作，包括从Word文档提取内容并转换为Markdown、自动识别和提取参考文献列表、在论文正文中智能插入引用标记、将处理后的Markdown转换回Word格式、扩充论文字数以满足字数要求。适用于需要批量处理引用格式、整理参考文献、或扩充论文内容的学术写作场景。当用户提到以下话题时触发：论文引用、参考文献整理、插入引用标记、Word转Markdown、扩充论文字数、学术论文字数不够、整理参考文献、处理论文引用格式。
---

# 学术论文引用自动化处理

本Skill提供一套完整的学术论文引用处理工具链，帮助自动化处理中文学术论文的引用管理工作。

## 功能概述

1. **Word转Markdown**: 将.docx论文转换为Markdown格式便于处理
2. **参考文献提取**: 自动识别并提取论文中的参考文献列表
3. **引用标记插入**: 在论文正文中智能插入引用标记
4. **Markdown转Word**: 将处理后的Markdown转换回Word格式
5. **论文扩充**: 自动扩充论文字数以满足字数要求

## 使用场景

- 需要为论文添加引用标记但手动操作繁琐
- 需要整理参考文献列表并生成摘要
- 需要扩充论文字数以满足毕业要求
- 需要批量处理多篇论文的引用格式

## 依赖要求

- Python 3.8+
- Node.js 14+
- npm (用于安装docx库)

## 安装步骤

1. 解压技能包到OpenClaw技能目录
2. 进入技能目录安装Node.js依赖: `npm install docx`
3. 重启OpenClaw

## 工具脚本使用

### 1. docx_to_md.py - Word转Markdown

```bash
python3 scripts/docx_to_md.py <输入.docx> [输出.md]
```

### 2. extract_refs.py - 提取参考文献

```bash
python3 scripts/extract_refs.py <论文.md>
```

输出: references.json

### 3. insert_citations_enhanced.py - 插入引用标记

```bash
python3 scripts/insert_citations_enhanced.py <论文.md> <references.json>
```

### 4. expand_paper.py - 扩充论文内容

```bash
python3 scripts/expand_paper.py <论文.md> [目标字数]
```

默认目标字数为50000

### 5. md_to_docx_final.py - Markdown转Word

```bash
python3 scripts/md_to_docx_final.py <论文.md> [输出.docx]
```

### 6. final_check.py - 质量检查

```bash
python3 scripts/final_check.py <原始.md> <处理后.md>
```

## 完整工作流程

```bash
# 1. Word转Markdown
python3 scripts/docx_to_md.py 论文初稿.docx

# 2. 提取参考文献
python3 scripts/extract_refs.py 论文初稿.md

# 3. 生成文献摘要
python3 scripts/generate_abstracts.py 论文初稿.md references.json

# 4. 插入引用标记
python3 scripts/insert_citations_enhanced.py 论文初稿.md references.json

# 5. 扩充论文内容（如需要）
python3 scripts/expand_paper.py 论文初稿_citations_enhanced.md 50000

# 6. Markdown转Word
python3 scripts/md_to_docx_final.py 论文初稿_final.md 论文终稿.docx

# 7. 质量检查
python3 scripts/final_check.py 论文初稿.md 论文初稿_final.md
```

## 引用标记格式

使用Markdown上标格式标记引用：

```markdown
银行核心系统的技术演进与信息技术发展密切相关[4]。
```

转换为Word后显示为上标格式。

## 参考文献格式支持

- `[J]` 期刊论文
- `[M]` 专著/书籍
- `[D]` 学位论文
- `[C]` 会议论文
- `[R]` 研究报告
- `[Z]` 标准/规范

## 技术实现细节

详细实现算法和扩展方法请参阅 `references/implementation.md`

## 注意事项

1. 引用格式: 默认使用 `[n]` 上标格式，如需其他格式请手动调整
2. 字数统计: 中文字符数约等于字数，英文按单词计算
3. 格式兼容性: 生成的Word文档使用标准OOXML格式
4. 备份建议: 处理前建议备份原始文档
