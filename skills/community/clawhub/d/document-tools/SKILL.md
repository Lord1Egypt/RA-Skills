---
name: "document-tools"
description: "文档处理全家桶：Word编辑/PDF处理/OCR/Markdown转换/合并拆分/加密水印"
user-invocable: true
metadata:
  openclaw:
    emoji: "📄"
    tags: ["document", "pdf", "word", "markdown", "conversion"]
---

# Document Tools v2.0

## 1. Word (.docx)
创建编辑/样式管理/表格图片/目录/修订追踪/批注/格式兼容

## 2. PDF
nano-pdf自然语言编辑 + PDF智能工具(OCR/转换/合并拆分/签名/水印/加密)

## 3. Markdown万能转换
```bash
markitdown input.pdf > output.md
```
支持: PDF/Word/PPT/Excel/HTML/CSV/JSON/图片(OCR)/音频(转录)/ZIP/YouTube/EPUB

## 依赖
```bash
pip install python-docx markitdown nano-pdf
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
```
