---
name: all-to-markdown
version: 0.1.0
description: 将任意文件（PDF、Word、Excel、PPT、图片、音频、网页等）转换为 Markdown
author: Ping Si <sipingme@gmail.com>
tags: [markdown, convert, pdf, docx, pptx, xlsx, html, ocr, youtube]
requiredEnvVars: []
---

# All to Markdown

基于 [Microsoft MarkItDown](https://github.com/microsoft/markitdown)，将任意格式的文件或 URL 转换为 Markdown，便于 LLM 分析和处理。

## 支持格式

| 类型 | 格式 |
|------|------|
| 文档 | PDF、DOCX、PPTX、XLSX、XLS、EPUB、MSG |
| 数据 | CSV、JSON、XML |
| 图片 | JPG、PNG 等（含 EXIF 元数据，可选 OCR）|
| 音频 | WAV、MP3（含语音转录，需 OpenAI Key）|
| 网页 | HTML、YouTube URL（含字幕提取）|
| 压缩 | ZIP（逐文件转换）|

## 前置要求

安装 markitdown：

```bash
pip install 'markitdown[all]'
```

## 给 AI 的使用说明

当用户需要将文件或 URL 转换为 Markdown 时，使用以下命令：

```bash
scripts/run.sh <文件路径或URL>
```

可选标志：
- `-o <输出文件>` — 保存到文件
- `--use-plugins` — 启用插件（如 markitdown-ocr）

**重要原则**：
- 转换结果直接输出到 stdout，可供 AI 直接读取分析
- 文件路径使用用户提供的实际路径，不要假设
- 转换大型文件时提前告知用户可能需要较长时间

## 使用示例

### 示例 1：转换 PDF

> 用户：帮我把这个 PDF 转成 Markdown，以便我分析内容

AI 执行：
```bash
scripts/run.sh /path/to/document.pdf
```

### 示例 2：转换并保存

> 用户：把这个 Excel 转成 Markdown 文件保存

AI 执行：
```bash
scripts/run.sh /path/to/data.xlsx -o output.md
```

### 示例 3：转换网页

> 用户：把这篇文章转成 Markdown

AI 执行：
```bash
scripts/run.sh https://example.com/article.html
```

### 示例 4：提取 YouTube 字幕

> 用户：把这个 YouTube 视频的内容提取出来

AI 执行：
```bash
scripts/run.sh https://www.youtube.com/watch?v=xxx
```

## 可选 AI 增强功能

设置 `OPENAI_API_KEY` 后，markitdown 可对图片生成 AI 描述：

```bash
OPENAI_API_KEY=sk-xxx scripts/run.sh image.jpg
```

## 安全说明

- 仅在本地执行文件转换，不发送文件内容到远程服务
- 转换 URL 时会访问对应网络地址
- 启用 LLM 功能时，图片内容会发送到 OpenAI API
