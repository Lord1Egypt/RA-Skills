# Deep Reading 📚

交互式 PDF 逐行阅读器，支持块级翻页、搜索、书签等。

## 功能

- 📖 打开并阅读 PDF 文档
- ➡️ 块级翻页（下一句、上一句）
- 🔍 关键词搜索
- 🔖 书签管理
- 📊 阅读进度显示
- 🔄 两种提取模式：文本模式 / OCR 模式

## 快速开始

```
用户: 列出PDF
助手: (显示 workspace 下的 PDF 列表)

用户: 开始读 xxx.pdf
助手: 📄 第1页 · 块1/100 · [█░░░░░░░] 1%
     (PDF 内容...)

用户: 下一句
助手: (继续阅读下一块)
```

## 指令

| 指令 | 说明 |
|------|------|
| `开始读 <文件>` | 打开 PDF |
| `模式 text/ocr` | 切换提取模式 |
| `下一句` / `继续` | 下一块 |
| `上一句` / `后退` | 上一块 |
| `去第X页` | 跳转页面 |
| `搜索 <关键词>` | 全文搜索 |
| `书签 添加 <备注>` | 添加书签 |
| `进度` | 显示阅读进度 |

## 安装依赖

首次使用时会自动创建虚拟环境并安装依赖。如需手动安装：

```bash
cd ~/.openclaw/workspace-e/skills/book-walker
python3 -m venv .venv
source .venv/bin/activate
pip install pdfplumber pypdfium2
```

可选（OCR 模式）：
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt install tesseract-ocr
```

## 作者

YoungAndSure
