---
name: document-processor
description: PDF和Word文档处理技能，支持PDF-Word相互转换、页面提取、去水印、合并拆分等操作
tools:
  - exec
  - read
  - write
  - edit
---

# 文档处理技能 📄

专业的PDF和Word文档处理工具集，支持多种文档格式转换和编辑操作。

## 功能特性

### 1. PDF处理
- ✅ PDF页面提取（提取指定页面生成新PDF）
- ✅ PDF转Word（保留格式）
- ✅ PDF合并/拆分
- ✅ PDF去水印
- ✅ PDF压缩优化
- ✅ PDF添加水印/页眉页脚
- ✅ OCR页码识别（识别扫描件PDF中的页码）

### 2. Word处理
- ✅ Word转PDF
- ✅ Word文档合并
- ✅ Word内容提取
- ✅ Word格式清理

### 3. OCR功能
- ✅ 扫描件PDF文字识别
- ✅ 多语言支持（中英文等）
- ✅ 页码自动识别和映射
- ✅ 批量OCR处理

### 4. 其他功能
- ✅ 图片提取（从PDF中提取图片）
- ✅ 批量处理（处理多个文件）

## 工具依赖

本技能需要以下Python库：
- PyPDF2 - PDF处理
- python-docx - Word文档处理
- pdf2docx - PDF转Word
- Pillow - 图片处理
- pdfplumber - 高级PDF处理

安装命令：
```bash
pip install PyPDF2 python-docx pdf2docx pillow pdfplumber
```

## 使用示例

### 1. PDF页面提取
```bash
# 提取第14-29页
python3 pdf_extractor.py "input.pdf" "output_pages_14-29.pdf" -s 14 -e 29

# 提取特定页面
python3 pdf_extractor.py "input.pdf" "output_specific.pdf" -p "1,3,5-7,10"
```

### 2. PDF转Word
```bash
python3 pdf_to_word.py "document.pdf" "document.docx"
```

### 3. Word转PDF
```bash
python3 word_to_pdf.py "document.docx" "document.pdf"
```

### 4. PDF去水印
```bash
python3 remove_watermark.py "input.pdf" "output_no_watermark.pdf"
```

### 5. 批量PDF转Word
```bash
python3 batch_pdf_to_word.py "/path/to/pdf/folder" "/path/to/output/folder"
```

## 脚本文件

本技能包含以下Python脚本：

### 核心脚本
1. `pdf_extractor.py` - PDF页面提取工具
2. `pdf_to_word.py` - PDF转Word工具
3. `word_to_pdf.py` - Word转PDF工具
4. `pdf_ocr.py` - PDF OCR和页码识别工具
5. `remove_watermark.py` - PDF去水印工具
6. `pdf_merger.py` - PDF合并工具
7. `pdf_splitter.py` - PDF拆分工具

### 实用工具
8. `batch_processor.py` - 批量处理工具
9. `pdf_compressor.py` - PDF压缩工具
10. `image_extractor.py` - 图片提取工具
11. `install_dependencies.py` - 依赖安装工具
12. `test_skill.py` - 技能测试工具

## 使用指南

当用户需要处理文档时：

1. **识别需求**：确定用户需要什么功能（转换、提取、编辑等）
2. **检查依赖**：确保所需Python库已安装
3. **选择脚本**：根据需求选择合适的脚本
4. **执行操作**：运行相应的Python脚本
5. **验证结果**：检查输出文件是否满足要求

## 高级功能

### OCR页码识别
```bash
# 分析PDF页码结构
python3 pdf_ocr.py analyze "input.pdf" --start 1 --end 50 --language chi_sim+eng

# 根据标注页码提取页面
python3 pdf_ocr.py extract "input.pdf" "output.pdf" --start-label 14 --end-label 29 --language chi_sim+eng
```

### 自定义水印
```python
# 添加文本水印
python3 add_watermark.py "input.pdf" "output.pdf" --text "CONFIDENTIAL" --position "center"

# 添加图片水印
python3 add_watermark.py "input.pdf" "output.pdf" --image "watermark.png" --opacity 0.3
```

### 批量处理
```bash
# 批量转换文件夹内所有PDF为Word
python3 batch_processor.py --input-dir "./pdfs" --output-dir "./docs" --operation "pdf2word"

# 批量提取所有PDF的封面
python3 batch_processor.py --input-dir "./pdfs" --output-dir "./covers" --operation "extract" --pages "1"
```

## 错误处理

- 文件不存在时提供清晰错误信息
- 格式不支持时建议转换方法
- 权限问题提示解决方案
- 内存不足时建议分批处理

## 性能优化

- 大文件处理时显示进度条
- 支持多线程批量处理
- 提供压缩选项减少文件大小
- 缓存中间结果避免重复处理

## 安全注意事项

- 验证输入文件格式
- 限制文件大小防止内存溢出
- 清理临时文件
- 不处理加密或受保护的PDF
- 用户确认后再执行删除操作

---

**技能维护者**：文档处理团队  
**最后更新**：2026-03-01  
**版本**：1.0.0  
**状态**：✅ 生产就绪