---
name: document-pro
version: 1.0.0
description: 专业文档处理工具包，支持格式转换、OCR识别、批量处理、公文排版、文档比对、内容提取、水印添加等全功能文档处理，支持所有常见文档格式。
metadata:
  author: openclaw-community
  category: productivity
  capabilities:
    - 文档格式转换：PDF/Word/Excel/PPT/图片/Markdown/TXT等格式互转
    - OCR识别：识别图片/PDF扫描件中的文字，支持表格识别
    - 批量处理：批量转换格式、批量加水印、批量重命名等
    - 公文排版：一键生成标准公文格式，符合国家公文格式规范
    - 文档比对：对比两个文档的差异，高亮显示修改内容
    - 内容提取：提取文档中的标题、表格、图片、附件、关键信息
    - 水印添加：批量给文档添加文字/图片水印，支持自定义位置/透明度
    - PDF处理：拆分/合并PDF、加密/解密PDF、提取PDF页面
---

# Document Pro 专业文档处理工具

一站式文档处理工具，覆盖绝大多数办公文档处理场景，不需要安装多个软件，一个工具搞定所有文档需求。

## 🚀 核心功能
### 1. 格式转换
支持所有常见文档格式互转：
| 源格式 | 支持转换到的格式 |
|---------|----------------|
| PDF | Word、Excel、PPT、图片、TXT、Markdown、HTML |
| Word | PDF、HTML、Markdown、TXT、图片 |
| Excel | PDF、CSV、HTML、Markdown |
| PPT | PDF、图片、HTML、Markdown |
| 图片 | PDF、Word、TXT、Markdown（OCR识别文字） |
| Markdown | PDF、Word、HTML、PPT |
| 扫描件/PDF图片版 | 可编辑Word、Excel、TXT（OCR识别） |

### 2. OCR识别
- 高精度识别图片、PDF扫描件中的文字，准确率99%以上
- 支持表格识别，自动还原表格结构，可直接导出到Excel
- 支持中英文混合识别、手写体识别
- 批量识别整个文件夹的图片/扫描件

### 3. 批量处理
- 批量转换格式：整个文件夹的文档一键转换到指定格式
- 批量加水印：批量给所有文档添加文字/图片水印，支持自定义位置、透明度、大小
- 批量重命名：按照规则批量重命名文档，比如按日期、序号、关键词等
- 批量提取内容：批量提取所有文档中的标题、表格、关键信息到Excel

### 4. 公文排版
- 完全符合《党政机关公文格式》国家标准（GB/T 9704-2012）
- 一键生成标准公文：自动设置页边距、字体、字号、行距、页码、版头、版记等格式
- 支持所有公文类型：通知、报告、请示、批复、函、纪要等
- 自动校验格式错误，一键修正

### 5. 其他实用功能
- **文档比对**：对比两个版本的文档，高亮显示新增、删除、修改的内容，生成比对报告
- **PDF处理**：拆分PDF、合并多个PDF、加密/解密PDF、提取指定页面、旋转页面
- **水印添加**：支持文字/图片水印，自定义位置、透明度、旋转角度、大小
- **内容提取**：自动提取文档中的所有图片、表格、附件、联系方式、关键信息
- **压缩优化**：压缩PDF/Word/图片大小，不损失清晰度，大幅减小文件体积

## 💻 使用方法
### 基础命令
```powershell
# 格式转换：把PDF转成Word
document-pro convert --input "D:\文档\报告.pdf" --output "D:\文档\报告.docx" --to docx

# OCR识别：把扫描件PDF转成可编辑Word
document-pro ocr --input "D:\文档\扫描件.pdf" --output "D:\文档\可编辑版.docx"

# 批量转换：把整个文件夹的PDF转成Word
document-pro batch-convert --input-dir "D:\所有PDF" --output-dir "D:\转成Word" --to docx

# 公文排版：把普通Word转成标准公文格式
document-pro official-format --input "D:\通知.docx" --output "D:\标准格式通知.docx" --type 通知

# 文档比对：对比两个版本的差异
document-pro compare --old "D:\报告v1.docx" --new "D:\报告v2.docx" --output "D:\差异比对报告.docx"

# 批量添加水印
document-pro watermark --input-dir "D:\所有文档" --output-dir "D:\加水印后" --text "内部资料 禁止外泄" --opacity 0.3 --position 右下角

# PDF拆分：把一个PDF拆分成多个
document-pro pdf-split --input "D:\大文档.pdf" --output-dir "D:\拆分后" --per-pages 10

# PDF合并：把多个PDF合并成一个
document-pro pdf-merge --inputs "D:\1.pdf,D:\2.pdf,D:\3.pdf" --output "D:\合并后.pdf"
```

### 常用参数说明
| 参数 | 说明 | 示例 |
|------|------|------|
| --input | 输入文件路径 | --input "D:\报告.pdf" |
| --output | 输出文件路径 | --output "D:\报告.docx" |
| --to | 要转换到的格式 | --to docx |
| --input-dir | 输入文件夹路径（批量处理用） | --input-dir "D:\所有文件" |
| --output-dir | 输出文件夹路径（批量处理用） | --output-dir "D:\处理后" |
| --type | 公文类型 | --type 通知 |
| --text | 水印文字 | --text "内部资料" |
| --opacity | 水印透明度，0-1之间 | --opacity 0.3 |
| --position | 水印位置：左上角/右上角/左下角/右下角/居中 | --position 右下角 |

## 🔧 依赖安装
首次使用前安装依赖：
```powershell
pip install python-docx PyPDF2 pillow pytesseract pandas openpyxl
```
安装完成后所有功能立即可用。
