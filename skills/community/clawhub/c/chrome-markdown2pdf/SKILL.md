---
name: chrome-markdown2pdf
description: |
  使用 Chrome headless 将 Markdown 文件转为排版精美的 PDF，支持表格、代码块、中文。
  Activate when user mentions: md转pdf、markdown转pdf、转PDF、导出PDF、生成PDF、chrome转pdf。
---

# Markdown 转 PDF 工具

将 Markdown 文件转为带样式的 PDF，排版支持标题、表格、代码块、引用等。

## 使用方法

```bash
python3 ~/.openclaw/workspace/skills/chrome-markdown2pdf/scripts/md2pdf.py \
  --input "/path/to/file.md" \
  --output "/path/to/output.pdf"
```

如果不指定 `--output`，默认输出到输入文件同目录，后缀改为 `.pdf`。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--input` / `-i` | ✅ | 输入 Markdown 文件路径 |
| `--output` / `-o` | 否 | 输出 PDF 路径（默认同目录替换后缀） |

## 依赖

- **Google Chrome**（headless 模式渲染 PDF）

检查是否安装：
```bash
google-chrome --version
```

## 转换流程

1. Markdown → HTML（内置转换器，支持表格、代码块、标题、加粗、斜体、行内代码、引用）
2. HTML → PDF（Chrome headless `--print-to-pdf`）

## PDF 样式

- 中文字体：Microsoft YaHei / PingFang SC
- 表格带边框和斑马纹
- 代码块灰色背景
- 标题彩色层级（H1黑色/H2蓝色/H3绿色/H4紫色）

## 示例

```bash
# 基本用法
python3 ~/.openclaw/workspace/skills/chrome-markdown2pdf/scripts/md2pdf.py \
  -i /home/robot-01/work/report.md

# 指定输出路径
python3 ~/.openclaw/workspace/skills/chrome-markdown2pdf/scripts/md2pdf.py \
  -i /home/robot-01/work/report.md \
  -o /tmp/output.pdf
```
