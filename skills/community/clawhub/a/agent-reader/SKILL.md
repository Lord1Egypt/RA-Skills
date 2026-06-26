---
name: agent-reader
description: "Document beautifier for AI Agents. Converts Markdown to styled webpages, Word, PDF, and image slideshows — the 'last mile' rendering engine for AI output. 专为 AI Agent 设计的文档美化引擎，一键把 Markdown 变成漂亮网页、Word、PDF 和幻灯片。"
metadata:
  author: ebbfijsf
  version: "1.3.7"
  tags: [mcp, markdown, pdf, docx, slideshow, document-converter]
---

# Agent Reader

Document beautifier engine for AI Agents. Turn raw Markdown into delivery-ready documents.
AI Agent 的文档美化引擎，把 Markdown 变成可交付的专业文档。

## Tools / 工具

| Tool | What it does |
|------|-------------|
| `render_markdown` | Markdown → styled webpage with sidebar TOC, code highlighting; can pre-generate PDF/DOCX files 带目录导航的网页，可预生成 PDF/DOCX |
| `export_document` | Markdown → PDF or Word (.docx) with smart formatting 导出 PDF/Word |
| `create_slideshow` | Images → full-screen slideshow with keyboard nav & auto-play 图片幻灯片 |
| `export_slideshow` | Slideshow → PDF or standalone HTML 导出幻灯片 |
| `open_file` | Smart open — auto-picks format based on user preferences 智能打开 |
| `configure_user_preferences` | Set default output format, theme, etc. 设置偏好 |
| `get_user_preferences` | Read current preferences 读取偏好 |

## When to use / 什么时候调用

- User wants a report formatted → `export_document` (format: "pdf" or "docx")
- User says "make it a webpage" → `render_markdown`
- User says "export to Word/PDF" → `export_document`
- User has images for a presentation → `create_slideshow` or `export_slideshow`
- User says "open this file" → `open_file`
- No format specified → `open_file` (auto-selects based on preferences)

## Setup / 接入

Add to your MCP config (Claude Desktop, Cline, OpenClaw, etc.):

```json
{
  "mcpServers": {
    "agent-reader": {
      "command": "npx",
      "args": ["-y", "agent-reader", "mcp"]
    }
  }
}
```

## Quick examples / 快速示例

### Render a webpage 渲染网页
```json
{ "content": "# My Report\n\nHello world...", "theme": "light" }
```

### Render with pre-export 预生成导出文件
```json
{ "content": "# My Report\n\nHello world...", "pre_export": ["pdf", "docx"] }
```

### Export to PDF 导出 PDF
```json
{ "content": "# My Report\n\n...", "format": "pdf" }
```

### Export to Word 导出 Word
```json
{ "content": "# My Report\n\n...", "format": "docx" }
```

### Create slideshow from images 图片做幻灯片
```json
{ "image_dir": "/path/to/images", "auto_play": 5 }
```

## Key parameters / 关键参数

- `content` — Markdown text to render/export Markdown 内容
- `format` — "pdf" or "docx" (for export_document); "pdf" or "html" (for export_slideshow)
- `source_path` — original .md file path, needed if Markdown references local images 原始文件路径（有本地图片时需要）
- `theme` — "light" (default) or "dark"
- `pre_export` — optional `["pdf"]` or `["pdf", "docx"]`; when returning a file path, MCP defaults to pre-generating PDF 可选预生成导出文件；MCP 返回文件路径时默认预生成 PDF
- `return_content` — set `true` to get base64/HTML string instead of file path (for sandbox/Docker)

## Notes / 注意事项

- PDF export requires Puppeteer (auto-installed on first use) PDF 导出需要 Puppeteer
- Word export works without Pandoc, but Pandoc produces better formatting Word 导出无需 Pandoc 也能用
- `return_content: true` keeps inline HTML behavior unless `pre_export` is explicitly set `return_content: true` 默认保持内联返回；显式传 `pre_export` 时会落盘输出
- All output writes to `/tmp/agent-reader/` — no side effects 输出仅写入 /tmp
- MIT licensed, open source 开源协议

## Links

- GitHub: https://github.com/ebbfijsf/agent-reader
- npm: https://www.npmjs.com/package/agent-reader
- Glama: https://glama.ai/mcp/servers/ebbfijsf/agent-reader
