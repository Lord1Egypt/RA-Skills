---
slug: cn-markdown-to-html
name: Markdown to HTML
version: "1.0.0"
description: "Convert Markdown to HTML with basic styling. Support headers, bold, italic, links, code blocks. Pure Python standard library, no API key required."
keywords: markdown, html, convert, converter
license: MIT-0
tags:
  - tools
---

# Markdown to HTML

Convert Markdown files to HTML.

## Features

- Convert headers (H1, H2, H3)
- Format bold and italic text
- Convert links
- Format inline and block code
- Generate complete HTML document
- Pure Python, no external dependencies

## Supported Markdown Elements

| Markdown | HTML |
|----------|------|
| # Header | <h1> |
| ## Header | <h2> |
| ### Header | <h3> |
| **bold** | <strong>bold</strong> |
| *italic* | <em>italic</em> |
| `code` | <code>code</code> |
| [text](url) | <a href="url">text</a> |

## Usage

```
python3 scripts/md_to_html.py --file readme.md
```

## Example

Input (readme.md):
```markdown
# My Project

This is **bold** and *italic* text.

[Visit example.com](https://example.com)
```

Output: Complete HTML document with proper formatting.

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
