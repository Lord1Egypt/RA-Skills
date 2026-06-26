---
name: pdf-processor
description: |
  一站式 PDF 处理技能。支持 PDF 文本/图片/表格提取、格式转换（PDF↔Word/Excel）、合并拆分、OCR 识别、批量处理、水印添加、加密解密、压缩等。使用场景：
  (1) 从 PDF 提取文本内容进行数据分析
  (2) 将 PDF 转换为 Word/Excel 方便编辑
  (3) 合并或拆分 PDF 文件
  (4) 对扫描件进行 OCR 识别提取文字
  (5) 批量处理多个 PDF 文件
  (6) 添加水印或加密保护 PDF
  (7) 压缩 PDF 减小文件体积
---

# PDF 处理技能

## 快速开始

### 安装依赖
```bash
cd D:\PDF.skill\pdf-processor
pip install -r requirements.txt
```

### 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 提取文本 | `python scripts/extract_text.py <pdf_path>` | 提取 PDF 文本内容 |
| 提取图片 | `python scripts/extract_images.py <pdf_path> <output_dir>` | 提取 PDF 中的图片 |
| 提取表格 | `python scripts/extract_tables.py <pdf_path>` | 提取 PDF 中的表格 |
| PDF 转 Word | `python scripts/pdf_to_word.py <pdf_path> <output_path>` | 转换为可编辑 Word |
| PDF 转 Excel | `python scripts/pdf_to_excel.py <pdf_path> <output_path>` | 提取表格到 Excel |
| 合并 PDF | `python scripts/merge_pdfs.py <output_path> <file1> <file2> ...` | 合并多个 PDF |
| 拆分 PDF | `python scripts/split_pdf.py <pdf_path> <output_dir>` | 按页拆分 PDF |
| 添加水印 | `python scripts/add_watermark.py <pdf_path> <output_path> <text>` | 添加文字水印 |
| OCR 识别 | `python scripts/ocr_pdf.py <pdf_path> <output_path>` | OCR 识别扫描件 |
| 加密 PDF | `python scripts/encrypt_pdf.py <input> <output> <password>` | AES-256 加密 |
| 解密 PDF | `python scripts/decrypt_pdf.py <input> <output> <password>` | 解密 PDF |
| 压缩 PDF | `python scripts/compress_pdf.py <input> <output>` | 压缩 PDF 文件 |
| 批量处理 | `python scripts/batch_process.py <input_dir> <output_dir> --operation <op>` | 批量处理 |

## 功能详情

### extract_text.py
提取 PDF 文本内容，支持：
- 纯文本提取
- 保留段落结构
- 提取元数据（标题、作者、创建时间）
```bash
python scripts/extract_text.py input.pdf -o output.txt --metadata
```

### extract_tables.py
提取 PDF 表格数据：
- 自动检测表格边框
- 支持合并单元格
- 输出为 Excel 文件

### pdf_to_word.py
PDF 转 Word 转换：
- 保留原始格式
- 提取图片到 Word
- 表格转换为 Word 表格

### pdf_to_excel.py
PDF 转 Excel：
- 提取表格到不同 Sheet
- 保留文本内容

### add_watermark.py
水印功能：
- 支持文字水印
- 可设置透明度、旋转角度、字体大小
- 支持批量添加

### ocr_pdf.py
OCR 识别（需要安装 Tesseract）：
- 使用 Tesseract 进行中文识别
- 支持多种语言混合识别
- 保留原有 PDF 格式

### encrypt_pdf.py / decrypt_pdf.py
加密解密：
- AES-256 加密
- 支持用户密码和所有者密码

### compress_pdf.py
压缩功能：
- 清理未使用对象
- 压缩图片
- 5 个压缩级别可选

### batch_process.py
批量处理：
- 支持所有单文件操作
- 自动处理目录中所有 PDF
- 生成处理报告

## 使用示例

### 从 PDF 提取文本
```
用户: 帮我提取这个合同的文本内容
AI: 使用 extract_text.py 脚本提取文本
```

### PDF 转 Word
```
用户: 把这个 PDF 转成 Word 文档
AI: 使用 pdf_to_word.py 进行转换
```

### 批量加水印
```
用户: 给这个文件夹里所有 PDF 添加"内部资料"水印
AI: 使用 batch_process.py 批量处理
```

### 加密 PDF
```
用户: 这个文件需要加密
AI: 使用 encrypt_pdf.py 进行 AES-256 加密
```

## 依赖安装

### 基础依赖
```bash
pip install pymupdf pdfplumber python-docx openpyxl pillow
```

### OCR 支持（可选）
```bash
# 安装 Tesseract OCR
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt install tesseract-ocr

pip install pytesseract
```

## 注意事项

- 加密 PDF 需要提供密码
- OCR 需要安装 Tesseract 引擎
- 大文件处理可能需要较长时间
- 转换效果取决于 PDF 原始质量
