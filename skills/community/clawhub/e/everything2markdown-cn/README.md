# Everything2Markdown 万物转 Markdown

使用 Microsoft MarkItDown 将各种文档格式转换为 Markdown，专为 AGENT 和 LLM 工作流优化。

## 特性

- 📝 支持 PDF、DOCX、PPTX、XLSX、HTML、EPUB
- 🖼️ 图片 OCR 文字提取
- 🎵 音频转录
- 📺 YouTube 字幕提取
- 🔧 AGENT 优化输出

## 安装

```bash
pip3 install 'markitdown[all]'
```

## 使用

```bash
# 单个文件
markitdown document.pdf -o output.md

# Python API
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("doc.pdf")
print(result.text_content)
```

## 文档

完整文档见 [SKILL.md](SKILL.md)。